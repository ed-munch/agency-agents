#!/usr/bin/env python3
"""Locate + slice a specialist SKILL.md. Contract: spawn.md

Usage:
  slice.py <slug>    IDENTITY + METHOD on stdout

Exit: 0 ok, 2 LOC_PLUGIN_MISSING, 3 LOC_SLUG_UNKNOWN, 4 LOC_SKILL_UNREADABLE
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PLUGIN = "agency-agents"
REGISTRY = Path.home() / ".grok/installed-plugins/registry.json"
LEVEL2 = re.compile(r"^##[ \t]+([^#\s].*?)\s*$")
IN_EXACT = {"Grok", "Rules", "Method", "Done when"}
FALLBACK = {"Context", "Domain"}
LOC_PLUGIN_MISSING, LOC_SLUG_UNKNOWN, LOC_SKILL_UNREADABLE = 2, 3, 4


def plugin_root() -> Path | None:
    here = Path(__file__).resolve().parents[2]
    if (here / "plugin.json").is_file() and (here / "skills").is_dir():
        return here
    if not REGISTRY.is_file():
        return None
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    for repo in (data.get("repos") or {}).values():
        plugins = repo.get("plugins") or {}
        if PLUGIN in plugins:
            p = Path(repo["path"])
            return p if p.is_dir() else None
    return None


def is_in_title(title: str, method_present: bool) -> bool:
    if title in IN_EXACT:
        return True
    if title == "Mission" or title.startswith("Mission"):
        return True
    if not method_present and title in FALLBACK:
        return True
    return False


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    raw = text[3:end].strip()
    body = text[end + 4 :].lstrip("\n")
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip("'\"")
    return meta, body


def sections(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines(keepends=True)
    marks: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        m = LEVEL2.match(line.rstrip("\n"))
        if m:
            marks.append((i, m.group(1).strip()))
    out: list[tuple[str, str]] = []
    for i, (start, title) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(lines)
        out.append((title, "".join(lines[start:end])))
    return out


def one_liner(meta: dict[str, str], body: str) -> str:
    sd = meta.get("metadata.short-description") or meta.get("short-description")
    if not sd:
        # nested YAML "  short-description: x" already flattened poorly; scan meta keys
        for k, v in meta.items():
            if k.endswith("short-description") and v:
                sd = v
                break
    if sd:
        return sd
    for line in body.splitlines():
        s = line.strip()
        if s and not s.startswith("#") and s != "---":
            return s
    return ""


def slice_skill(text: str) -> tuple[bool, str]:
    secs = sections(text)
    method_present = any(t == "Method" for t, _ in secs)
    chunks = [body for title, body in secs if is_in_title(title, method_present)]
    return method_present, "".join(chunks).rstrip() + ("\n" if chunks else "")


def load(slug: str) -> tuple[int, Path | None, str]:
    if slug == "agency":
        return LOC_SLUG_UNKNOWN, None, ""
    root = plugin_root()
    if root is None:
        return LOC_PLUGIN_MISSING, None, ""
    path = root / "skills" / slug / "SKILL.md"
    if not path.parent.is_dir():
        return LOC_SLUG_UNKNOWN, path, ""
    try:
        return 0, path, path.read_text(encoding="utf-8")
    except OSError:
        return LOC_SKILL_UNREADABLE, path, ""


def main(argv: list[str]) -> int:
    args = argv[1:]
    if len(args) != 1 or not args[0] or "/" in args[0]:
        sys.stderr.write("usage: slice.py <slug>\n")
        return 2
    slug = args[0]
    code, _path, text = load(slug)
    if code:
        return code
    meta, body = parse_frontmatter(text)
    _has_method, method = slice_skill(text)
    ident = one_liner(meta, body)
    sys.stdout.write(f"persona: /{slug}\n{ident}\n\n")
    sys.stdout.write(f"method-source: skills/{slug}/SKILL.md\n")
    sys.stdout.write(method)
    if method and not method.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
