#!/usr/bin/env python3
"""Compress Agency agent personas into Grok Build skills.

Grok-efficient means:
  - short SKILL.md bodies (procedure, not persona theatre)
  - specialists are slash-only (disable-model-invocation)
  - one auto-invocable catalog skill (`agency`) holds the roster
  - no duplicated code samples, communication-style essays, or memory fluff

Source of truth remains the division `*.md` agent files. This script rewrites
them into skills/ (plugin layout) and optionally integrations/grok/.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DIVISIONS_JSON = REPO_ROOT / "divisions.json"

DROP_HEADER = re.compile(
    r"^(communication style|learning(?: and|&)? memory|deliverable template|"
    r"technical deliverables|image prompt|example |your technical deliverables|"
    r"instructions reference)$"
)
IDENTITY_HEADER = re.compile(r"^(identity|identity(?: and|&)? memory|identity(?: and|&)? role definition)$")
MISSION_HEADER = re.compile(r"^(core mission|mission|executive summary|core capabilities|core competencies)$")
RULES_HEADER = re.compile(r"^(critical rules(?: you must follow)?|rules you must follow)$")
WORKFLOW_HEADER = re.compile(r"^(workflow(?: process)?|process|your process)$")
METRICS_HEADER = re.compile(r"^(success metrics)$")
SKIP_HEADER = re.compile(r"^(when not to use(?: this agent)?)$")
DOMAIN_HEADER = re.compile(
    r"^(domain expertise|specialized skills|decision framework|tooling(?: and|&)? automation|"
    r"tech stack|advanced capabilities)$"
)

EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002700-\U000027BF"
    "\U00002600-\U000026FF"
    "\U0000FE00-\U0000FE0F"
    "\U0000200D"
    "]+",
    flags=re.UNICODE,
)
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)\Z", re.S)
BULLET_RE = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+")
ROLE_RE = re.compile(r"^\s*[-*]?\s*\*\*Role\*\*\s*:?\s*(.+)$", re.I)
FENCE_RE = re.compile(r"^```")
LABEL_RE = re.compile(r"^\*\*([^*]+)\*\*\s*:?\s*")


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def strip_emoji(text: str) -> str:
    return EMOJI_RE.sub("", text)


def yaml_quote(value: str) -> str:
    value = value.replace("\n", " ").strip()
    return "'" + value.replace("'", "''") + "'"


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm: dict[str, str] = {}
    key = None
    acc: list[str] = []
    for raw in m.group(1).splitlines():
        if re.match(r"^[A-Za-z0-9_-]+:\s*", raw) and not raw.startswith(" "):
            if key is not None:
                fm[key] = " ".join(acc).strip().strip('"').strip("'")
            key, rest = raw.split(":", 1)
            key = key.strip()
            acc = [rest.strip()]
        elif key is not None and (raw.startswith(" ") or raw.startswith("\t")):
            acc.append(raw.strip())
    if key is not None:
        fm[key] = " ".join(acc).strip().strip('"').strip("'")
    return fm, m.group(2).lstrip("\n")


def normalize_header(header: str) -> str:
    h = strip_emoji(header)
    h = h.replace("&", " and ")
    h = re.sub(r"[^A-Za-z0-9 ]+", " ", h)
    h = re.sub(r"\b(your|the|my|our)\b", " ", h, flags=re.I)
    h = re.sub(r"\s+", " ", h).strip().lower()
    return h


def split_sections(body: str) -> list[tuple[str, str]]:
    lines = body.splitlines()
    sections: list[tuple[str, str]] = []
    current_h = ""
    buf: list[str] = []
    for line in lines:
        if line.startswith("## "):
            if current_h or buf:
                sections.append((current_h, "\n".join(buf).strip()))
            current_h = line[3:].strip()
            buf = []
        else:
            buf.append(line)
    if current_h or buf:
        sections.append((current_h, "\n".join(buf).strip()))
    return sections


def extract_items(text: str, limit: int) -> list[str]:
    items: list[str] = []
    in_fence = False
    seen: set[str] = set()
    for raw in text.splitlines():
        if FENCE_RE.match(raw.strip()):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = strip_emoji(raw).rstrip()
        if not line.strip():
            continue
        if line.startswith("#"):
            continue
        if not BULLET_RE.match(line):
            continue
        item = BULLET_RE.sub("", line).strip()
        item = LABEL_RE.sub(r"\1: ", item)
        item = re.sub(r"\s+", " ", item).strip(" -")
        low = item.lower()
        if low.startswith(("personality:", "memory:", "experience:")):
            continue
        if low.startswith("role:"):
            item = item.split(":", 1)[1].strip()
        if len(item) < 8:
            continue
        if item.endswith(":"):
            continue
        key = re.sub(r"[^a-z0-9]+", "", item.lower())
        if key in seen:
            continue
        seen.add(key)
        if len(item) > 220:
            item = item[:217].rstrip() + "..."
        items.append(item)
        if len(items) >= limit:
            break
    return items


def harvest_prose_bullets(text: str, limit: int) -> list[str]:
    """If a section has almost no list markers, take short standalone sentences."""
    items = extract_items(text, limit)
    if items:
        return items
    in_fence = False
    out: list[str] = []
    for raw in text.splitlines():
        if FENCE_RE.match(raw.strip()):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = strip_emoji(raw).strip()
        if not line or line.startswith("#") or line.startswith(">"):
            continue
        if line.startswith("You are "):
            continue
        if len(line) < 24 or len(line) > 220:
            continue
        if line.startswith("|") or line.startswith("```"):
            continue
        out.append(re.sub(r"\s+", " ", line).rstrip("."))
        if len(out) >= limit:
            break
    return out


def classify(header: str) -> str | None:
    h = normalize_header(header)
    if not h:
        return "preamble"
    if DROP_HEADER.match(h):
        return None
    if SKIP_HEADER.match(h):
        return "skip"
    if IDENTITY_HEADER.match(h):
        return "identity"
    if MISSION_HEADER.match(h):
        return "mission"
    if RULES_HEADER.match(h):
        return "rules"
    if WORKFLOW_HEADER.match(h):
        return "workflow"
    if METRICS_HEADER.match(h):
        return "metrics"
    if DOMAIN_HEADER.match(h):
        return "domain"
    return "other"


def extract_role(identity_text: str, vibe: str, name: str, description: str) -> str:
    for raw in identity_text.splitlines():
        m = ROLE_RE.match(strip_emoji(raw))
        if m:
            return m.group(1).strip().rstrip(".")
    if vibe:
        return vibe.strip().rstrip(".")
    if description:
        return description.strip().rstrip(".")
    return f"{name} specialist"


def compact_description(description: str, slug: str, limit: int = 280) -> str:
    desc = re.sub(r"\s+", " ", description).strip().rstrip(".")
    suffix = f" Use when the user runs /{slug}."
    room = limit - len(suffix)
    if len(desc) > room:
        desc = desc[: room - 3].rstrip() + "..."
    return desc + "." + suffix


def render_skill(
    *,
    name: str,
    slug: str,
    description: str,
    division: str,
    role: str,
    do_items: list[str],
    rules: list[str],
    output: list[str],
    skip: list[str],
) -> str:
    fm = [
        "---",
        f"name: {slug}",
        f"description: {yaml_quote(description)}",
        "disable-model-invocation: true",
        "user-invocable: true",
        "argument-hint: task",
        "license: MIT",
        "metadata:",
        "  author: The Agency",
        f"  division: {division}",
        f"  short-description: {yaml_quote(name)}",
        "  source: msitarzewski/agency-agents",
        "---",
        "",
        f"# {name}",
        "",
        role.rstrip(".") + ".",
        "",
    ]
    body: list[str] = fm
    if do_items:
        body.append("## Do")
        body.append("")
        for item in do_items:
            body.append(f"- {item}")
        body.append("")
    if rules:
        body.append("## Rules")
        body.append("")
        for item in rules:
            body.append(f"- {item}")
        body.append("")
    if output:
        body.append("## Done when")
        body.append("")
        for item in output:
            body.append(f"- {item}")
        body.append("")
    if skip:
        body.append("## Out of scope")
        body.append("")
        for item in skip:
            body.append(f"- {item}")
        body.append("")
    body.append("Deliver the artifact. Do not recap this persona.")
    body.append("")
    return "\n".join(body)


def convert_agent(path: Path, division: str) -> dict | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return None
    fm, body = parse_frontmatter(text)
    name = fm.get("name") or path.stem.replace("-", " ").title()
    slug = slugify(name)
    if not (2 <= len(slug) <= 64) or not re.match(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$", slug):
        raise SystemExit(f"invalid skill name from {path}: {slug!r}")
    description = fm.get("description") or name
    vibe = fm.get("vibe") or ""

    buckets: dict[str, list[str]] = {
        k: [] for k in ("identity", "mission", "rules", "workflow", "metrics", "skip", "domain", "other")
    }
    identity_text = ""
    for header, content in split_sections(body):
        kind = classify(header)
        if kind is None:
            continue
        if kind == "identity":
            identity_text += content + "\n"
            continue
        if kind == "preamble":
            continue
        limit = {
            "rules": 8,
            "workflow": 8,
            "mission": 8,
            "metrics": 5,
            "skip": 4,
            "domain": 6,
            "other": 6,
        }[kind]
        items = extract_items(content, limit)
        buckets[kind].extend(items)

    role = extract_role(identity_text, vibe, name, description)
    do_items = list(buckets["workflow"] or buckets["mission"] or buckets["domain"] or [])
    if len(do_items) < 4:
        extra = buckets["mission"] + buckets["domain"] + buckets["other"]
        for item in extra:
            if item not in do_items:
                do_items.append(item)
            if len(do_items) >= 8:
                break
    if len(do_items) < 3:
        harvested: list[str] = []
        for header, content in split_sections(body):
            kind = classify(header)
            if kind in (None, "identity"):
                continue
            harvested.extend(harvest_prose_bullets(content, 6))
        for item in harvested:
            if item not in do_items:
                do_items.append(item)
            if len(do_items) >= 6:
                break
    rules = buckets["rules"][:8]
    output = buckets["metrics"][:5]
    skip = buckets["skip"][:4]
    if not rules:
        rules = [i for i in buckets["domain"] if i not in do_items][:6]

    skill_md = render_skill(
        name=name,
        slug=slug,
        description=compact_description(description, slug),
        division=division,
        role=role,
        do_items=do_items[:8],
        rules=rules,
        output=output,
        skip=skip,
    )
    src_lines = text.count("\n") + 1
    out_lines = skill_md.count("\n") + 1
    return {
        "name": name,
        "slug": slug,
        "division": division,
        "description": compact_description(description, slug),
        "one_liner": role,
        "skill_md": skill_md,
        "src_lines": src_lines,
        "out_lines": out_lines,
        "src_path": str(path.relative_to(REPO_ROOT)),
    }


def load_divisions() -> list[str]:
    data = json.loads(DIVISIONS_JSON.read_text())
    return list(data["divisions"].keys())


def division_labels() -> dict[str, str]:
    data = json.loads(DIVISIONS_JSON.read_text())
    return {k: v["label"] for k, v in data["divisions"].items()}


def write_skill_tree(root: Path, records: list[dict], catalog_md: str) -> None:
    if root.exists():
        for child in root.iterdir():
            if child.name in {"README.md"}:
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    root.mkdir(parents=True, exist_ok=True)
    for rec in records:
        d = root / rec["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(rec["skill_md"], encoding="utf-8")
    agency = root / "agency"
    agency.mkdir(parents=True, exist_ok=True)
    (agency / "SKILL.md").write_text(catalog_md, encoding="utf-8")


def render_catalog(records: list[dict]) -> str:
    labels = division_labels()
    by_div: dict[str, list[dict]] = {}
    for rec in records:
        by_div.setdefault(rec["division"], []).append(rec)
    lines = [
        "---",
        "name: agency",
        "description: 'Agency specialist roster for Grok Build. Use when the user wants a specialist agent, an agency role, a domain expert, or runs /agency. Pick the matching slash skill and follow it.'",
        "when-to-use: agency, specialist, roster, persona, agent role, the agency",
        "disable-model-invocation: false",
        "user-invocable: true",
        "argument-hint: role or task",
        "license: MIT",
        "metadata:",
        "  author: The Agency",
        "  short-description: 'Agency specialist catalog'",
        "  source: msitarzewski/agency-agents",
        "---",
        "",
        "# Agency",
        "",
        "This plugin is a compressed rewrite of [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) for Grok Build.",
        "",
        "## How to work",
        "",
        "- Specialists are slash skills (`/frontend-developer`). They have `disable-model-invocation: true` so they do not bloat auto-invoke context.",
        "- If the user names a role, read `skills/<slug>/SKILL.md` in this plugin (or `~/.grok/skills/<slug>/SKILL.md`) and follow it for the rest of the turn.",
        "- If the role is ambiguous, list 3-5 matching slugs from the roster below and ask.",
        "- Deliver the artifact. Do not recap the persona. Do not invent tools the session does not have.",
        "- UI changes: verify in the browser before claiming done.",
        "",
        f"Roster: {len(records)} specialists.",
        "",
    ]
    for div in sorted(by_div):
        label = labels.get(div, div)
        lines.append(f"## {label}")
        lines.append("")
        lines.append("| Skill | Role |")
        lines.append("|---|---|")
        for rec in sorted(by_div[div], key=lambda r: r["slug"]):
            one = rec["one_liner"].replace("|", "/")
            lines.append(f"| `/{rec['slug']}` | {one} |")
        lines.append("")
    return "\n".join(lines)


def collect_agents() -> list[dict]:
    records: list[dict] = []
    for division in load_divisions():
        d = REPO_ROOT / division
        if not d.is_dir():
            continue
        for path in sorted(d.rglob("*.md")):
            rec = convert_agent(path, division)
            if rec:
                records.append(rec)
    records.sort(key=lambda r: (r["division"], r["slug"]))
    slugs = [r["slug"] for r in records]
    if len(slugs) != len(set(slugs)):
        raise SystemExit("duplicate skill slugs")
    return records


def write_index(records: list[dict], dest: Path) -> None:
    payload = [
        {
            "slug": r["slug"],
            "name": r["name"],
            "division": r["division"],
            "src": r["src_path"],
            "src_lines": r["src_lines"],
            "out_lines": r["out_lines"],
        }
        for r in records
    ]
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "integrations" / "grok")
    parser.add_argument("--skills-root", type=Path, default=REPO_ROOT / "skills")
    parser.add_argument("--index", type=Path, default=REPO_ROOT / "skills" / "index.json")
    args = parser.parse_args()

    records = collect_agents()
    catalog = render_catalog(records)
    write_skill_tree(args.skills_root, records, catalog)
    grok_skills = args.out / "skills"
    write_skill_tree(grok_skills, records, catalog)
    args.out.mkdir(parents=True, exist_ok=True)
    readme = args.out / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Grok Build skills\n\n"
            "Generated by `scripts/convert-grok.py`. Install with "
            "`./scripts/install.sh --tool grok` or "
            "`grok plugin install ed-munch/agency-agents --trust`.\n",
            encoding="utf-8",
        )
    write_index(records, args.index)

    src = sum(r["src_lines"] for r in records)
    out = sum(r["out_lines"] for r in records) + catalog.count("\n") + 1
    print(f"Converted {len(records)} agents -> Grok skills")
    print(f"  source lines: {src}")
    print(f"  skill lines:  {out} ({out / src:.0%} of original)")
    print(f"  skills root:  {args.skills_root}")
    print(f"  integrations: {args.out}")
    too_long = [r for r in records if r["out_lines"] > 120]
    if too_long:
        print(f"  warning: {len(too_long)} skills exceed 120 lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
