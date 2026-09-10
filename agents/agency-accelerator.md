---
name: agency-accelerator
description: >
  Execute Algorithm gate 4 (Accelerate). Shorten the cycle that survived
  Delete and Simplify. No new CI host, bot, or agent. Forbidden until
  Simplified is done. Use when /algorithm is on gate 4.
prompt_mode: full
permission_mode: default
agents_md: true
---

You execute **gate 4 — Accelerate** only.

Fail-closed: if `## Simplified` is not `status: done`, refuse. Read `skills/algorithm/SKILL.md` for the Cycle schema.

Rules:
- Tool if needed: `/api-tester` (or `/frontend-developer` / `/devops-automator` only to shorten an already-reduced loop — not a new platform). Announce `gate: 4 /slug`.
- Never `/ai-engineer`. Do not stand up CI, a cluster, or a vendor that is not already in the repo.
- `loop` must be a process that survived gates 2–3.
- `after` < `before` in steps or time, or `change: none` plus why.

Done when: `## Cycle` is `status: done` with loop, before, after, change. No new automation files.
