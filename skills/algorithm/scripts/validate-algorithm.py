#!/usr/bin/env python3
"""Couche 1 only: mechanical unlock of an Algorithm gate.

Usage:
  validate-algorithm.py [--gate N] [ALGORITHM.md]

Exit:
  0  requested gate is unlocked
  2  file missing / section missing
  3  fields missing / status not done
  4  gate 5 requested without gates 1–4 done
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SECTIONS = ("Requirements", "Deleted", "Simplified", "Cycle", "Automate")
VERDICTS = frozenset({"keep", "rewrite", "kill"})
DELETED_DONE = frozenset({"cut", "kept_for_addback", "not_in_tree"})
SIMPLIFIED_DONE = frozenset({"landed", "not_needed"})
HEADING = re.compile(
    r"^##\s+(Requirements|Deleted|Simplified|Cycle|Automate)\b(.*)$",
    re.I,
)
STATUS = re.compile(r"status:\s*(done|wip|skipped)\b", re.I)
KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.+?)\s*$")


def fail(code: int, msg: str) -> int:
    print(msg, file=sys.stderr)
    return code


def resolve(path: Path | None) -> Path | None:
    if path is not None:
        return path
    for candidate in (Path("ALGORITHM.md"), Path(".agency/ALGORITHM.md")):
        if candidate.is_file():
            return candidate
    return None


def split_sections(text: str) -> dict[str, tuple[str, str]]:
    """name -> (heading_rest, body)."""
    lines = text.splitlines()
    found: dict[str, tuple[str, str]] = {}
    current: str | None = None
    rest = ""
    buf: list[str] = []
    for line in lines:
        m = HEADING.match(line)
        if m:
            if current is not None:
                found[current] = (rest, "\n".join(buf).strip())
            current = {
                "requirements": "Requirements",
                "deleted": "Deleted",
                "simplified": "Simplified",
                "cycle": "Cycle",
                "automate": "Automate",
            }[m.group(1).lower()]
            rest = m.group(2)
            buf = []
            continue
        if current is not None:
            buf.append(line)
    if current is not None:
        found[current] = (rest, "\n".join(buf).strip())
    return found


def section_status(heading_rest: str, body: str) -> str | None:
    m = STATUS.search(heading_rest)
    if m:
        return m.group(1).lower()
    for line in body.splitlines()[:8]:
        m = STATUS.search(line)
        if m:
            return m.group(1).lower()
    return None


def keys(body: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in body.splitlines():
        m = KEY.match(line.strip())
        if m:
            out[m.group(1).lower()] = m.group(2).strip()
    return out


def tables(body: str) -> list[list[dict[str, str]]]:
    rows_out: list[list[dict[str, str]]] = []
    lines = body.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and "---" not in line:
            headers = [c.strip().lower() for c in line.strip("|").split("|")]
            i += 1
            if i < len(lines) and re.search(r"\|\s*-+", lines[i]):
                i += 1
            rows: list[dict[str, str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cols = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if cols and not all(re.fullmatch(r":?-{3,}:?", c) for c in cols):
                    row = {}
                    for h, v in zip(headers, cols):
                        if h:
                            row[h] = v
                    if row:
                        rows.append(row)
                i += 1
            if rows:
                rows_out.append(rows)
            continue
        i += 1
    return rows_out


def first_rows(body: str) -> list[dict[str, str]]:
    ts = tables(body)
    return ts[0] if ts else []


def check_requirements(body: str) -> str | None:
    rows = first_rows(body)
    if not rows:
        return "Requirements: need ≥1 table row"
    needed = ("id", "requirement", "owner", "source", "verdict")
    for row in rows:
        missing = [k for k in needed if not row.get(k)]
        if missing:
            return f"Requirements: row missing {', '.join(missing)}"
        if row["verdict"].lower() not in VERDICTS:
            return f"Requirements: verdict must be keep|rewrite|kill, got {row['verdict']!r}"
    return None


def check_deleted(body: str) -> str | None:
    kv = keys(body)
    if "nothing_to_delete" in kv:
        return None
    rows = first_rows(body)
    if not rows:
        return "Deleted: need a cut row or nothing_to_delete:"
    for row in rows:
        if not row.get("id") or not row.get("what") or not row.get("kills") or not row.get("done"):
            return "Deleted: row needs id, what, kills, done"
        if row["done"].lower() not in DELETED_DONE:
            return f"Deleted: done must be cut|kept_for_addback|not_in_tree, got {row['done']!r}"
    return None


def check_simplified(body: str) -> str | None:
    kv = keys(body)
    if "not_needed" in kv and kv["not_needed"]:
        return None
    rows = first_rows(body)
    if not rows:
        return "Simplified: need a row or not_needed:"
    for row in rows:
        if not row.get("before") or not row.get("after") or not row.get("done"):
            return "Simplified: row needs before, after, done"
        if row["done"].lower() not in SIMPLIFIED_DONE:
            return f"Simplified: done must be landed|not_needed, got {row['done']!r}"
    return None


def check_cycle(body: str) -> str | None:
    kv = keys(body)
    missing = [k for k in ("loop", "before", "after", "change") if k not in kv]
    if missing:
        # also accept a one-row table
        rows = first_rows(body)
        if rows:
            row = rows[0]
            missing = [k for k in ("loop", "before", "after", "change") if not row.get(k)]
        if missing:
            return f"Cycle: missing {', '.join(missing)}"
    return None


def check_automate(body: str, status: str) -> str | None:
    kv = keys(body)
    if status == "skipped":
        if "reason" not in kv or "checked" not in kv:
            return "Automate skipped: need reason and checked"
        return None
    missing = [k for k in ("what", "path", "run", "uses_existing") if k not in kv]
    if missing:
        rows = first_rows(body)
        if rows:
            missing = [k for k in ("what", "path", "run", "uses_existing") if not rows[0].get(k)]
        if missing:
            return f"Automate: missing {', '.join(missing)}"
    return None


CHECKERS = {
    "Requirements": lambda body, _s: check_requirements(body),
    "Deleted": lambda body, _s: check_deleted(body),
    "Simplified": lambda body, _s: check_simplified(body),
    "Cycle": lambda body, _s: check_cycle(body),
    "Automate": check_automate,
}


def previous_done(sections: dict[str, tuple[str, str]], gate: int) -> tuple[int, str]:
    """Return (exit, msg) if a prior section blocks this gate. gate is 1-based."""
    if gate <= 1:
        return 0, ""
    for idx in range(gate - 1):
        name = SECTIONS[idx]
        if name not in sections:
            return 2, f"missing section ## {name}"
        rest, body = sections[name]
        st = section_status(rest, body)
        if name == "Automate":
            ok = st in {"done", "skipped"}
        else:
            ok = st == "done"
        if not ok:
            if gate == 5:
                return 4, f"gate 5 locked: {name} status is {st or 'missing'}, need done"
            return 3, f"{name} status is {st or 'missing'}, need done to open gate {gate}"
        err = CHECKERS[name](body, st or "")
        if err:
            code = 4 if gate == 5 else 3
            return code, err
    return 0, ""


def validate(path: Path, gate: int) -> int:
    if not path.is_file():
        return fail(2, f"missing file: {path}")
    text = path.read_text(encoding="utf-8")
    sections = split_sections(text)
    missing = [n for n in SECTIONS if n not in sections]
    if missing:
        return fail(2, "missing section(s): " + ", ".join(f"## {n}" for n in missing))
    code, msg = previous_done(sections, gate)
    if code:
        return fail(code, msg)
    return 0


def self_test() -> int:
    import tempfile

    t0 = """# Algorithm
Task: add SageMaker
Started: 2026-09-10

## Requirements   status: done
| id | requirement | owner | source | verdict | why |
|---|---|---|---|---|---|
| R1 | Deploy a model in prod | user | chat | rewrite | Prod unnamed. Serve /models if present |
| R2 | Use SageMaker | user | chat | kill | Vendor named, absent from repo |

## Deleted        status: done
nothing_to_delete: R2 never landed in-tree. No SageMaker files to cut.

## Simplified     status: wip

## Cycle          status: wip

## Automate       status: wip
"""
    empty = "# Algorithm\n"
    failed: list[str] = []

    def expect(name: str, text: str, gate: int, want: int) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as fh:
            fh.write(text)
            p = Path(fh.name)
        got = validate(p, gate)
        p.unlink(missing_ok=True)
        if got != want:
            failed.append(f"{name}: want {want} got {got}")

    t0_deleted_wip = t0.replace(
        "## Deleted        status: done",
        "## Deleted        status: wip",
    )
    expect("t0-gate1", t0, 1, 0)
    expect("t0-gate2", t0, 2, 0)
    expect("t0-gate3", t0, 3, 0)  # Deleted done → gate 3 unlocked
    expect("t0-gate5", t0, 5, 4)
    expect("deleted-wip-blocks-3", t0_deleted_wip, 3, 3)
    expect("missing-sections", empty, 1, 2)
    if failed:
        print("FAIL:", *failed, sep="\n  ", file=sys.stderr)
        return 1
    print("PASS: validate-algorithm self-test")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, help="ALGORITHM.md path")
    parser.add_argument("--gate", type=int, default=1, metavar="N", help="gate to unlock (1–5)")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.gate < 1 or args.gate > 5:
        return fail(3, "--gate must be 1..5")
    path = resolve(args.path)
    if path is None:
        return fail(2, "missing file: ALGORITHM.md (or .agency/ALGORITHM.md)")
    code = validate(path, args.gate)
    if code == 0:
        print(f"gate {args.gate} unlocked ({path})")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
