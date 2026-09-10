---
name: agency
description: 'When an Algorithm gate is in progress and the user asks which specialist to use, propose 3–5 slugs allowed on that gate only — never the full roster. Use when the user runs /agency, or asks for a specialist during /algorithm.'
when-to-use: agency, specialist, which tool for this gate, the agency
disable-model-invocation: false
user-invocable: true
argument-hint: current gate or role
license: MIT
metadata:
  author: The Agency
  short-description: 'Agency — gate router, not the roster'
  source: msitarzewski/agency-agents
---

# Agency

The Agency serves the Algorithm. This skill is a **gate router**, not the catalog dump.

Slash `/<slug>` still loads a specialist method. The 273-row roster lives in `skills/agency/references/roster.md` — do not paste it.

## Grok

- Propose 3–5 slugs allowed on the **current** gate. Never dump the roster.
- If the user already named a slug, read that skill's `SKILL.md` and follow the whole method.
- If the gate can finish with zero specialists, say so and propose none.
- Use Grok tools. Deliver the artifact. Do not recap this skill.

## Mission

Name the smallest set of tools that can finish the current Algorithm gate — or none.

## Rules

Tension lock
- Propose 3–5 slugs allowed on the current gate only. Never dump the roster.
- Never propose ai-engineer or devops-automator for gates 1–3.
- If the gate can finish with zero specialists, say so and propose none.

- Frozen mapping: `GROK.md`. Do not renegotiate.
- Long tail stays slash-only. Do not auto-load it during `/algorithm`.
- `data-engineer` is long tail: not before gate 5, and only if an existing pipeline survived gates 1–4.
- `load-specialist.py` is off the `/algorithm` happy path. Happy path = `/algorithm` then at most one in-gate slug.

## Method

1. **Find the gate** — Read `ALGORITHM.md` or `.agency/ALGORITHM.md`. Current gate = the first section that is not `status: done` (`skipped` counts as done only on Automate). If the file is missing and the user asked to automate, ship, scale, or add a pipeline: point them to `/algorithm` and propose **none**. Artefact: `gate: N`.

2. **Filter the mapping** — Open `GROK.md` (core 12 × portes). Keep slugs whose cell for this gate is **P** or **ok**. Drop **—** and **!**. Artefact: allowed list.

3. **Prefer none** — Gates 1–2 may finish with zero specialists. If the parent can write the section without a tool, propose none. Artefact: `none` or 3–5 slugs, each one line of why.

4. **Hard excludes** — Gates 1–3: never `/ai-engineer`, never `/devops-automator`. Gate 5 is locked until Requirements, Deleted, Simplified, and Cycle are `done`. Artefact: the same list, filtered.

5. **Hand off** — If the user picks a slug, read `skills/<slug>/SKILL.md` only. Announce `gate: N /slug`. Do not merge another specialist's Method.

## Done when

3–5 in-gate slugs (or an explicit `none`) can be pointed at. The roster was not dumped. `/ai-engineer` and `/devops-automator` were not proposed for gates 1–3.
