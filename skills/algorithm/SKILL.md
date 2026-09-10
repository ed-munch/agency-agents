---
name: algorithm
description: 'When a task or repo must be questioned and cut before it is accelerated or automated, run the five Algorithm gates in order. Use when the user runs /algorithm, or asks to add a pipeline, agent, CI, or vendor that may not need to exist.'
when-to-use: 'Use when a task or repo must be reduced before it is accelerated or automated. /algorithm'
disable-model-invocation: false
user-invocable: true
argument-hint: task or bottleneck + whose requirement it is
license: MIT
metadata:
  author: The Agency
  short-description: 'Algorithm — five gates, automate last'
  source: ed-munch/agency-agents
---

# Algorithm

The Agency serves the Algorithm. Specialists are tools of a gate, never the other way around.

## Grok

- Edit the repo. Do not recap the Algorithm to the user.
- One gate at a time. The artefact for gate N is required before gate N+1.
- Prefer Grok tools. At most one specialist per gate, announced `tool: /slug`.
- If the gate needs no tool, do not invent one.
- Allowed specialists per gate: `GROK.md` (frozen). Do not renegotiate.

## Mission

Apply the Algorithm to this task or repo until the remaining cycle is as small as it can be — automate only then.

## Rules

Tension lock
- Order 1→5 is the product. Skipping a gate is failure, even if the code is good.
- Gates 1–2 may finish with zero specialists. Prefer that.
- Never open a session on /ai-engineer or /devops-automator. Start at Questionner.
- Gate 5 is locked until Requirements, Deleted, Simplified, and Cycle are written artefacts (a written "nothing to delete, because…" counts).
- One specialist at a time. At most one builder on gate 3.
- If a specialist's Method would add a stack, a platform, or a pipeline before gate 5, interrupt and return to the current gate.

- Never start at Automate or Accelerate.
- A requirement without a person's name is suspect — question it or drop it. No name given → `owner: user`. Inventing a name is failure.
- Delete too little (0 % add-back expected) = cut again.
- Call an Agency skill only to execute the current gate.
- Anti-invention: do not add a stack, SLA, or vendor because a skill names them.
- If the repo does not justify gate 5, stop at 4 and say so.
- Slogan ≠ artefact. Artefact = a path, a command, or a person-owner. If the section has none of those, status goes back to `wip`.

## Method

Work in the target repo, not this plugin.

**Artefact file:** `ALGORITHM.md` at the repo root, or `.agency/ALGORITHM.md` if the root must stay clean. One file. Not five docs. If the repo is read-only, write the same schema in the reply **and** under `.agency/` — chat alone is not a lock.

Skeleton (create it if missing, then fill gate 1):

```markdown
# Algorithm
Task: <one sentence>
Started: <date>

## Requirements   status: wip
## Deleted        status: wip
## Simplified     status: wip
## Cycle          status: wip
## Automate       status: wip
```

Gate N+1 **refuses to start** unless section N is `status: done` (Automate may be `skipped`). Empty section, slogan ("requirements look fine"), or a plan with no owner **does not count**.

Before opening N+1: run `skills/algorithm/scripts/validate-algorithm.py --gate N+1 [ALGORITHM.md]` if that script is reachable; otherwise apply couche 1 by hand (same checklist). Then apply the five locks below. Couche 1 fail → do not run couche 2.

### 1 — Questionner → `## Requirements` `status: done`

Prefer zero specialists. If evidence in the tree is needed: `tool: /codebase-archaeologist`. Named product cuts: `tool: /product-manager`. Named threat: `tool: /application-security-engineer`. Never `/ai-engineer` or `/devops-automator`.

Each in-play requirement, one row:

| Champ | Obligatoire | Règle |
|---|---|---|
| `id` | yes | R1, R2… |
| `requirement` | yes | what is asked, one sentence |
| `owner` | yes | first+last name or handle. Not "the team", "legal", "eng" |
| `source` | yes | ticket, README, comment, "said by X in this chat" |
| `verdict` | yes | `keep` / `rewrite` / `kill` |
| `less_dumb` | if rewrite | the rewritten requirement |
| `why` | if kill or rewrite | one sentence |

Done when: ≥1 requirement; every row has a person-owner and a verdict; if every verdict is `keep` with no `kill` or `rewrite`, write why the cut will come at gate 2 — otherwise gate 1 is too soft.

Does not count: user story with no owner, PRD, Now/Next/Later roadmap, "stakeholders want X".

### 2 — Delete → `## Deleted` `status: done`

Unlocked only if Requirements is `done`. Prefer `/code-reviewer` or an implementer (`/frontend-developer`, `/backend-architect`) — not a designer of new systems.

| Champ | Obligatoire | Règle |
|---|---|---|
| `id` | yes | D1, D2… |
| `what` | yes | file, symbol, process, doc, CI job, screen |
| `path` | if code/doc | path in the tree |
| `kills` | yes | requirement id (`R3`) or `orphan` |
| `done` | yes | `cut` / `kept_for_addback` / `not_in_tree` |
| `addback_risk` | no | if ~10 % might come back |

Every `cut` needs a **git diff** (or a named patch). `not_in_tree` is allowed: the piece existed only as process / habit.

Done when: ≥1 Deleted row **or** a `nothing_to_delete:` paragraph that cites the keep requirements and why a cut would break a named owner; every `cut` has a path or process-only proof; if 0 `cut` and 0 `kept_for_addback`, note that gate 2 is suspect and offer a second pass — do not invent deletes.

Does not count: "we should clean later", a TODO, a refactor announced with no diff.

### 3 — Simplify → `## Simplified` `status: done`

Unlocked only if Deleted is `done`. Builder: `/frontend-developer` or `/backend-architect`. `/accessibility-auditor` blocks a "simplify" that drops a required WCAG path.

| Champ | Obligatoire | Règle |
|---|---|---|
| `id` | yes | S1, S2… |
| `before` | yes | path / API / steps before |
| `after` | yes | the smaller version |
| `survives` | yes | Requirement keep ids |
| `done` | yes | `landed` / `not_needed` |

Every `landed` needs a **diff**.

Done when: every gate-1 `keep` is either unchanged and `not_needed`, or pointed at by an `S*`; nothing with verdict `kill` is "simplified"; an UI cut that breaks an already-required WCAG criterion is not `landed`.

Does not count: cosmetic rewrite, new framework, "extract a package".

### 4 — Accelerate → `## Cycle` `status: done`

Unlocked only if Simplified is `done`. Tool if needed: `/api-tester`. Not a new CI host.

| Champ | Obligatoire | Règle |
|---|---|---|
| `loop` | yes | which round-trip is timed (e.g. "PR → test → preview") |
| `before` | yes | current step count or duration, even approximate |
| `after` | yes | target / obtained step count or duration |
| `change` | yes | path of the change, or `none` |
| `blocked_by` | no | what still blocks speed without automating |

Done when: `loop` is a process that *survived* gates 2–3; `after` < `before` in steps or time, **or** `change: none` plus why ("already one step"); no new CI runner / bot / agent in this section.

Does not count: "we'll add CI", a micro-bench unrelated to the loop.

### 5 — Automate → `## Automate` `status: done` or `skipped`

Unlocked only if Cycle is `done` **and** Requirements, Deleted, Simplified, Cycle are all `done`. Only then may `/devops-automator` or `/ai-engineer` enter. If the remaining cycle does not need automation: `skipped`, do not call them.

If `done`:

| Champ | Obligatoire | Règle |
|---|---|---|
| `what` | yes | the Cycle process being automated |
| `path` | yes | script / workflow already in the tree, or added *now* |
| `run` | yes | exact command to run it |
| `uses_existing` | yes | `true` if the stack was already here |
| `specialist` | if called | `/devops-automator` or `/ai-engineer` |

If `skipped`:

```
status: skipped
reason: <the remaining cycle does not justify automation>
checked: <what was looked at in the repo>
```

Done when: `done` ⇒ `path` exists, `run` was executed or is executable, `uses_existing: true` **or** a justification for a minimal add; `skipped` ⇒ `reason` + `checked`, and **no** new automation file in this session's diff; forbidden if Cycle is not `done`.

Does not count: an automation plan, a Dockerfile "for later", a vendor named in a skill.

### Fail-closed (before acting)

1. `ALGORITHM.md` or `.agency/ALGORITHM.md` exists.
2. The **previous** gate's section is `status: done`.
3. Gate 5: sections 1–4 are `done`.
4. `status: wip` or a missing section = stay on that gate. Do not "advance in chat" without writing.

### Locks (before N+1; any red keeps `wip`)

1. Owner = a person or `user`.
2. No `keep` on a vendor / SLA / add-verb.
3. Every `cut` / `landed` / `run` has a path or a command in the repo.
4. No section N carries a `kill` id from N−1, except Deleted.
5. Automate targets only Cycle's `loop`.

Causality: `keep|rewrite` may exist in gates 3–5; `kill` belongs in Deleted only; `cut` pieces are forbidden in Simplify / Automate; Cycle.loop is a still-living process; Automate.what is that loop.

### T0 — "add SageMaker" (must pass)

Do **not** call `/ai-engineer`. Write Requirements (vendor `kill` or rewrite to a result), then stop or continue only as far as the tree justifies. A well-formed file that precedes an `/ai-engineer` call is a fail.

## Done when

The five sections of `ALGORITHM.md` are Done (section 5 may be `skipped`). The tree reflects Deleted / Simplified (diffs, not prose). Touched tests pass if they exist. No automation appears in the tree before Cycle is Done.
