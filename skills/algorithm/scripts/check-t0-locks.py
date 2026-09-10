#!/usr/bin/env python3
"""T0/T1/T3 mechanical locks. Couche 3 still needs a live /algorithm session."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "skills"
AGENTS = ROOT / "agents"
FAILED: list[str] = []


def fail(msg: str) -> None:
    FAILED.append(msg)


def read(rel: str) -> str:
    p = ROOT / rel
    if not p.is_file():
        fail(f"missing {rel}")
        return ""
    return p.read_text(encoding="utf-8")


def main() -> int:
    algo = read("skills/algorithm/SKILL.md")
    if "Never open a session on /ai-engineer or /devops-automator" not in algo:
        fail("algorithm SKILL missing T0 opener lock")

    agency = read("skills/agency/SKILL.md")
    if "Never dump the roster" not in agency:
        fail("agency is not a gate router")
    if "| `/anthropologist`" in agency:
        fail("agency SKILL still dumps the roster")
    if "Never propose ai-engineer or devops-automator for gates 1–3" not in agency:
        fail("agency missing 1–3 exclude")
    if not (SKILLS / "agency/references/roster.md").is_file():
        fail("roster.md missing (slash-only catalog)")

    ai = read("skills/ai-engineer/SKILL.md")
    if "Allowed gates: 5 Automate" not in ai:
        fail("ai-engineer not locked to gate 5")
    if "disable-model-invocation: true" not in ai.split("---", 2)[1]:
        fail("ai-engineer must stay slash-only (T0)")

    dev = read("skills/devops-automator/SKILL.md")
    if "Forbidden: 1–3" not in dev:
        fail("devops-automator not forbidden on 1–3")
    if "disable-model-invocation: true" not in dev.split("---", 2)[1]:
        fail("devops-automator must stay slash-only (T0)")

    core = [
        "algorithm",
        "agency",
        "product-manager",
        "codebase-archaeologist",
        "application-security-engineer",
        "code-reviewer",
        "frontend-developer",
        "backend-architect",
        "accessibility-auditor",
        "api-tester",
        "devops-automator",
        "ai-engineer",
    ]
    for slug in core:
        text = read(f"skills/{slug}/SKILL.md")
        if slug == "algorithm":
            if "Tension lock" not in text:
                fail("algorithm missing Tension lock")
            continue
        if slug == "agency":
            if "Tension lock" not in text:
                fail("agency missing Tension lock")
            continue
        if "Agency × Algorithm" not in text or "Tension lock" not in text:
            fail(f"{slug} missing Agency × Algorithm / Tension lock")

    for name in (
        "agency-questioner",
        "agency-cutter",
        "agency-simplifier",
        "agency-accelerator",
        "agency-automator",
        "agency-explorer",
    ):
        if not (AGENTS / f"{name}.md").is_file():
            fail(f"missing agents/{name}.md")

    automator = read("agents/agency-automator.md")
    if "locked" not in automator.lower():
        fail("agency-automator not locked")

    assign = read("integrations/grok/assign-specialist.md")
    if "hors happy path" not in assign.lower() and "off the happy path" not in assign.lower():
        fail("assign-specialist still presents load-specialist as happy path")

    t0 = """# Algorithm
Task: add SageMaker
Started: 2026-09-10

## Requirements   status: done
| id | requirement | owner | source | verdict | why |
|---|---|---|---|---|---|
| R1 | Deploy a model in prod | user | chat | rewrite | Serve /models if present |
| R2 | Use SageMaker | user | chat | kill | Vendor named, absent from repo |

## Deleted        status: done
nothing_to_delete: R2 never landed in-tree.

## Simplified     status: wip

## Cycle          status: wip

## Automate       status: wip
"""
    import tempfile

    script = SKILLS / "algorithm/scripts/validate-algorithm.py"
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as fh:
        fh.write(t0)
        path = Path(fh.name)
    try:
        r2 = subprocess.run(
            [sys.executable, str(script), "--gate", "2", str(path)],
            capture_output=True,
            text=True,
        )
        r5 = subprocess.run(
            [sys.executable, str(script), "--gate", "5", str(path)],
            capture_output=True,
            text=True,
        )
    finally:
        path.unlink(missing_ok=True)
    if r2.returncode != 0:
        fail(f"T0 gate 2 should unlock, got {r2.returncode} {r2.stderr}")
    if r5.returncode != 4:
        fail(f"T0 gate 5 should stay locked (exit 4), got {r5.returncode} {r5.stderr}")

    grok = read("GROK.md")
    if "The Agency serves the Algorithm" not in grok:
        fail("GROK.md missing product line")

    if FAILED:
        print("FAIL:", *FAILED, sep="\n  ", file=sys.stderr)
        return 1
    print("PASS: T0/T1/T3 mechanical locks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
