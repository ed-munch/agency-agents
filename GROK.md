# Grok Build

The Agency serves the Algorithm.

## Objective

Each specialist is a tool-using procedure, not a character sheet.

- **description** — when + do (activation predicate, not a role slogan)
- **when-to-use** — situation + `/slug`
- **Mission** — the job in one sentence
- **Rules** — constraints that change a decision
- **Method** — sequential steps; each step a verb plus artefact
- **Done when** — a check (workspace command, or the artefact is there)

`/algorithm` is the session OS (five gates, automate last). Specialists are tools of a gate, never the other way around. `/agency` is the catalog.

## Algorithm

Order is the product. Invert it and the run fails, even if the code is good.

1. **Questionner.** Each requirement has a person's name, not a department. Make the requirement less dumb, or drop it.
2. **Delete.** Remove the part or the process. If ~10 % is not added back later, the cut was too shallow.
3. **Simplify / optimize.** Only what survived. Do not optimize a thing that should not exist.
4. **Accelerate.** Shorten the remaining cycle. Do not speed up a process destined to disappear.
5. **Automate.** Last. Scripts, agents, CI, skills — only after 1–4.

Gates 1–2 may finish with zero specialists. Prefer that. Never open a session on `/ai-engineer` or `/devops-automator`.

Artefact: one `ALGORITHM.md` (or `.agency/ALGORITHM.md`) in the **target** repo. Contract: `skills/algorithm/SKILL.md`.

## Core 12 — frozen mapping

Freeze the rest. Adjust only with a written reason in this file.

| Porte | Slug | Rôle sous `/algorithm` |
|---|---|---|
| OS | `algorithm` | enchaîne les 5 portes |
| Routeur | `agency` | 3–5 slugs *de la porte en cours*, pas le catalogue |
| 1 | `product-manager` | exigences nommées, keep / rewrite / kill. **Launch/Deliver/Measure coupés** |
| 1 | `codebase-archaeologist` | d’où vient la contrainte dans le tree ; dead code pour porte 2 |
| 1–2 | `application-security-engineer` | requirement sécu nommé, ou coupe de surface |
| 2–3 | `code-reviewer` | que supprimer / simplifier dans le diff |
| 2–4 | `frontend-developer` | UI existante, pas un nouveau framework |
| 2–3 | `backend-architect` | contrats existants ; pas de nouveau service sans delete d’un ancien |
| 3 | `accessibility-auditor` | interdit de « simplifier » en cassant l’accès |
| 4 | `api-tester` | raccourcir le feedback |
| 4–5 | `devops-automator` | cycle puis automation — **interdit en 1–3** |
| 5 | `ai-engineer` | ML / serving = automation — **interdit avant artefacts 1–4** |

Hors core (long tail) : `data-engineer` (trop SLA-first), `database-optimizer`, `test-results-analyzer`, `ui-designer`, `technical-writer`, `incident-response-commander`.

## Matrice portes × skills

Légende : **P** = porte principale · **ok** = autorisé · **—** = interdit · **!** = la mission v1 pousse à y aller trop tôt

| Skill | 1 Questionner | 2 Delete | 3 Simplify | 4 Accelerate | 5 Automate |
|---|---|---|---|---|---|
| `algorithm` | OS | OS | OS | OS | OS |
| `agency` | routeur | routeur | routeur | routeur | routeur |
| `product-manager` | **P** | ok (kill) | — | — | **!** Launch / Deliver |
| `codebase-archaeologist` | **P** | ok (dead code) | — | — | — |
| `application-security-engineer` | ok | ok | — | — | — |
| `code-reviewer` | — | **P** | **P** | — | — |
| `frontend-developer` | — | ok | **P** | ok | — |
| `backend-architect` | — | ok | **P** | — | **!** « design scalable » |
| `accessibility-auditor` | ok (contrainte nommée) | — | **P** | — | — |
| `api-tester` | — | — | — | **P** | — |
| `devops-automator` | — | — | — | ok | **P** / **!** |
| `ai-engineer` | — | — | — | — | **P** / **!** |

## Result

273 skills in `skills/<slug>/SKILL.md`. Catalog: `skills/agency/SKILL.md`. OS: `skills/algorithm/SKILL.md`.

| Command | What it does |
|---|---|
| `/algorithm` | Five gates. Automate last. |
| `/agency` | Roster. Auto-invoked when the user asks for a specialist. |
| `/<slug>` | Full method for that turn. Long tail stays slash-only. |

## Assign a specialist

Every agent/subagent gets one specialist. No generic helper.

- Protocol: `integrations/grok/assign-specialist.md`
- Load: `python3 integrations/grok/load-specialist.py <slug>` from the plugin root

Stdout is IDENTITY + METHOD (`persona: /slug`, then Mission / Rules / Method / Done when).

Under `/algorithm`, load at most one specialist, and only if the current gate's mapping allows it.
