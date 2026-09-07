# Grok Build

## Objective

Each specialist is a tool-using procedure, not a character sheet.

- **description** — when + do (activation predicate, not a role slogan)
- **when-to-use** — situation + `/slug`
- **Mission** — the job in one sentence
- **Rules** — constraints that change a decision
- **Method** — sequential steps; each step a verb plus artefact
- **Done when** — a check (workspace command, or the artefact is there)

Specialists are slash-only. `/agency` is the catalog.

## Result

273 skills in `skills/<slug>/SKILL.md`. Catalog: `skills/agency/SKILL.md`.

| Command | What it does |
|---|---|
| `/agency` | Roster. Auto-invoked when the user asks for a specialist. |
| `/<slug>` | Full method for that turn. |

## Spawn

Every agent/subagent gets one specialist. No generic helper.

- Protocol: `integrations/grok/spawn.md`
- Slice: `python3 integrations/grok/slice.py <slug>` from the plugin root

Stdout is IDENTITY + METHOD (`persona: /slug`, then Mission / Rules / Method / Done when).
