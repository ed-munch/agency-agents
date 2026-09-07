#!/usr/bin/env python3
"""Convert Agency personas into Grok Build skills.

Keep the full method. Drop Claude character-sheet padding.

Native body is Mission, Rules, Method, Done when. Convert strips Claude padding.
It does not rewrite a Claude method into Grok steps (that is a human rewrite).
It does not author Method. If Claude has no procedure, a human or worker
rewrites the division `*.md`. Convert still only generates `skills/`.
Full method is not cropped to five bullets.

Dropped: identity/memory/personality, communication style, learning & memory,
deliverable-report templates, "You are X" preambles, header emoji.

Specialists are slash-only so 273 files do not auto-load. /agency is the catalog.
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
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)\Z", re.S)
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

DROP = re.compile(
    r"^(identity|identity(?: and|&)? memory|identity(?: and|&)? role definition|"
    r"communication style|learning(?: and|&)? memory|"
    r"deliverable template|your deliverable template|"
    r"technical deliverables|your technical deliverables|"
    r"instructions reference)$"
)
RENAME = {
    "core mission": "Mission",
    "mission": "Mission",
    "executive summary": "Mission",
    "core capabilities": "Mission",
    "core competencies": "Mission",
    "critical rules": "Rules",
    "critical rules you must follow": "Rules",
    "rules you must follow": "Rules",
    "workflow process": "Method",
    "workflow": "Method",
    "process": "Method",
    "your process": "Method",
    "success metrics": "Done when",
    "when not to use this agent": "Out of scope",
    "when not to use": "Out of scope",
    "advanced capabilities": "Advanced",
    "domain expertise": "Domain",
    "specialized skills": "Domain",
    "decision framework": "Decisions",
    "tooling and automation": "Tooling",
    "tech stack": "Tooling",
}

GROK_BY_DIVISION = {
    "engineering": "Edit the repo. Run tests you touch. If UI changed, verify in the browser.",
    "design": "Produce concrete UI/UX artifacts. If the app is on screen, verify in the browser.",
    "testing": "Write or run tests. Report failures with command, output, and file:line.",
    "security": "Inspect real code and config. Cite paths. Do not write exploits.",
    "product": "Turn the ask into a decision, spec, or ticket the repo can execute.",
    "research": "Cite sources. Separate fact from inference.",
    "marketing": "Deliver copy, plans, or assets ready to use. No persona recap.",
    "sales": "Deliver sequences, talk tracks, or deal artifacts ready to use.",
    "paid-media": "Deliver account structure, queries, or creative with numbers attached.",
    "project-management": "Deliver a plan with owners, order, and risks.",
    "support": "Draft the reply or runbook the human can send.",
    "finance": "Show the numbers and the assumption behind each one.",
    "healthcare": "Stay inside documented scope. Flag what a licensed human must sign.",
    "academic": "Cite. Mark speculation.",
    "game-development": "Touch the real project files. Prefer running the game or tests over describing them.",
    "gis": "Work from the actual data/files. State CRS and units.",
    "spatial-computing": "Implement against the real Xcode/Unity/Unreal tree when it is in the workspace.",
    "specialized": "Deliver the artifact. Do not recap this skill.",
}


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def yaml_quote(value: str) -> str:
    value = value.replace("\n", " ").strip()
    return "'" + value.replace("'", "''") + "'"


def strip_emoji(text: str) -> str:
    return EMOJI_RE.sub("", text)


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


def title_header(header: str) -> str:
    h = normalize_header(header)
    if h in RENAME:
        return RENAME[h]
    cleaned = strip_emoji(header).strip()
    cleaned = re.sub(r"^(Your|The|My)\s+", "", cleaned)
    cleaned = re.sub(r"\s+Agent Personality$", "", cleaned)
    return cleaned or header.strip()


def split_sections(body: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current = ""
    buf: list[str] = []
    for line in body.splitlines():
        if line.startswith("## "):
            if current or any(x.strip() for x in buf):
                sections.append((current, "\n".join(buf).strip()))
            current = line[3:].strip()
            buf = []
        else:
            buf.append(line)
    if current or any(x.strip() for x in buf):
        sections.append((current, "\n".join(buf).strip()))
    return sections


def drop_you_are(text: str) -> str:
    out: list[str] = []
    for para in re.split(r"\n\s*\n", text.strip()):
        p = para.strip()
        if not p:
            continue
        if p.startswith("#"):
            continue
        if re.match(r"^You are\b", p):
            continue
        out.append(p)
    return "\n\n".join(out)


def grok_description(description: str, slug: str) -> str:
    desc = re.sub(r"\s+", " ", description).strip().rstrip(".")
    suffix = f" Use when the user runs /{slug}."
    room = 320 - len(suffix)
    if len(desc) > room:
        desc = desc[: room - 3].rstrip() + "..."
    return desc + "." + suffix


def extract_role(identity_text: str, vibe: str, description: str, name: str) -> str:
    for raw in identity_text.splitlines():
        m = re.match(r"^\s*[-*]?\s*\*\*Role\*\*\s*:?\s*(.+)$", strip_emoji(raw), re.I)
        if m:
            return m.group(1).strip().rstrip(".")
    if vibe:
        return vibe.strip().rstrip(".")
    if description:
        return description.strip().rstrip(".")
    return f"{name} specialist"


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

    identity = ""
    kept: list[tuple[str, str]] = []
    seen_titles: set[str] = set()
    for header, content in split_sections(body):
        key = normalize_header(header)
        if not header:
            leftover = drop_you_are(content)
            if leftover:
                kept.append(("Context", leftover))
            continue
        if DROP.match(key):
            if "identity" in key:
                identity += content + "\n"
            continue
        title = title_header(header)
        if title in seen_titles:
            title = f"{title} ({header})"
        seen_titles.add(title)
        kept.append((title, content.strip()))

    role = extract_role(identity, vibe, description, name)
    grok_line = GROK_BY_DIVISION.get(division, "Deliver the artifact. Do not recap this skill.")

    parts = [
        "---",
        f"name: {slug}",
        f"description: {yaml_quote(grok_description(description, slug))}",
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
        "## Grok",
        "",
        "- Follow the method below in full. Do not summarize it back to the user.",
        f"- {grok_line}",
        "- Prefer Grok tools over describing what a human should do.",
        "",
    ]
    if not kept:
        kept.append(("Method", drop_you_are(body) or body.strip()))
    for title, content in kept:
        if not content:
            continue
        parts.append(f"## {title}")
        parts.append("")
        parts.append(content)
        parts.append("")
    skill_md = "\n".join(parts).rstrip() + "\n"
    return {
        "name": name,
        "slug": slug,
        "division": division,
        "one_liner": role,
        "skill_md": skill_md,
        "src_lines": text.count("\n") + 1,
        "out_lines": skill_md.count("\n") + 1,
        "src_path": str(path.relative_to(REPO_ROOT)),
    }


def load_divisions() -> list[str]:
    return list(json.loads(DIVISIONS_JSON.read_text())["divisions"].keys())


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
        "description: 'Agency specialist roster for Grok Build. Full methods, written as Grok procedures. Use when the user wants a specialist, an agency role, or runs /agency.'",
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
        "Specialist skills ported from [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents).",
        "Each skill keeps the **full method**. Claude character-sheet padding is stripped. Nothing is summarized down to a handful of bullets.",
        "",
        "## How to work",
        "",
        "- Specialists are slash skills (`/frontend-developer`). Slash-only, so the roster does not load every turn.",
        "- When the user names a role, read that skill's `SKILL.md` and follow the whole method.",
        "- If the role is ambiguous, list 3-5 matching slugs and ask.",
        "- Every agent/subagent spawn follows `integrations/grok/spawn.md` (slice via `integrations/grok/slice.py`). No generic helper.",
        "- Use Grok tools. Deliver the artifact. Do not recap the skill.",
        "",
        f"Roster: {len(records)} specialists.",
        "",
    ]
    for div in sorted(by_div):
        lines.append(f"## {labels.get(div, div)}")
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
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        json.dumps(
            [
                {
                    "slug": r["slug"],
                    "name": r["name"],
                    "division": r["division"],
                    "src": r["src_path"],
                    "src_lines": r["src_lines"],
                    "out_lines": r["out_lines"],
                }
                for r in records
            ],
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "integrations" / "grok")
    parser.add_argument("--skills-root", type=Path, default=REPO_ROOT / "skills")
    parser.add_argument("--index", type=Path, default=REPO_ROOT / "skills" / "index.json")
    args = parser.parse_args()

    records = collect_agents()
    catalog = render_catalog(records)
    write_skill_tree(args.skills_root, records, catalog)
    write_skill_tree(args.out / "skills", records, catalog)
    args.out.mkdir(parents=True, exist_ok=True)
    readme = args.out / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Grok Build skills\n\n"
            "Full methods as Grok procedures. "
            "`./scripts/install.sh --tool grok` or "
            "`grok plugin install ed-munch/agency-agents --trust`.\n",
            encoding="utf-8",
        )
    write_index(records, args.index)
    src = sum(r["src_lines"] for r in records)
    out = sum(r["out_lines"] for r in records) + catalog.count("\n") + 1
    print(f"Converted {len(records)} agents -> Grok skills (full method, no crop)")
    print(f"  source lines: {src}")
    print(f"  skill lines:  {out} ({out / src:.0%} of original)")
    thin = [r for r in records if r["out_lines"] < 20]
    if thin:
        print(f"  warning: {len(thin)} thin skills: " + ", ".join(t["slug"] for t in thin[:12]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
