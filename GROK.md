# Grok Build rewrite

This fork writes each Agency persona as a Grok skill: a tool-using procedure, not a Claude character sheet.

Grok is an agent with tools (read and write files, shell, browser). It loads a `SKILL.md` and does the work. It does not play a character.

## Spec (Grok-native)

A source persona is Grok-native iff all of the following hold. This spec is métier-agnostic. Frontend, sales, and research use the same shape.

### Frontmatter

Keep `name`, `description`, `color`, `vibe` (`color` / `name` / `description` satisfy lint; `vibe` is the convert one-liner).

`description` is an activation predicate: **when** + **do**. Not a role slogan (not "A frontend developer who…").

### Body — required

1. **Mission** — the job in one sentence. No "you are".
2. **Rules** — only constraints that change a decision. Each once.
3. **Method** — 3 to 8 sequential steps. Each step says what to do and which artefact it reads or produces (a file path if the work has one; otherwise the artefact). No "in parallel". Fewer than 3 steps: the job is undefined. More than 8: usually a capability list — cut until it is steps, do not split the persona by default.
4. **Done when** — a check. If the workspace already has a command that decides pass/fail, that is the check. Otherwise the artefact is there and can be pointed at. Not a speech.

No `## Domain`, `## Patterns`, `## Advanced`. If a fact changes a decision, it goes in Rules or in the Method step it constrains. A code sample belongs inside Method only when it *is* the step, not as a dump.

### Forbidden

- "You are X", Identity, Communication, Learning, fill-in templates, title emoji
- Capability laundry lists
- Grafts from another product
- Inventing a stack the target workspace may not have
- Recapping the persona instead of doing the work

### Out of scope for this rewrite

- Which specialist is assigned to which spawn (see `integrations/grok/spawn.md`)
- Hard-coding tools (`npm test`, Lighthouse CLI, VoiceOver)
- Shorter = more Grok (empty crop already rejected)
- Copying harness skills (`oracle`) in place of the specialist method

The convert script prepends a short `## Grok` block (edit the repo, run tests, do not recap). This spec is the **body**.

## Procedure vs form

Form-complete is the shape above. Procedure-complete is different: an agent who is not that specialist, given only this file, produces the Done-when artefact or STOPs because the workspace lacks the stack. Every Method step is a verb plus a livrable, not a noun list (PMax, yokes, auction insights).

## Claude is corpus, not a ceiling

Convert strips padding. It does not invent Method. `git show HEAD:<path>` is the Claude corpus in this repo. If the job is real and Claude has no procedure, author the missing steps in the division source. Never drop a skill because Claude was thin. 273 jobs stay 273 skills.

## How to author a gap

Keep Mission, useful Rules, and tools Claude already named. Write inspect → do → verify. STOP if that stack is absent. Do not graft harness skills. Do not crop to empty bullets. Do not number a capability list and call it Method.

Partial skills stay in the catalog. They are listed in `scripts/grok-native-partial.txt` until a later batch authors the gap.

Which specialist is assigned to which spawn stays out of scope.

## Source and generate

Source of truth: division `*.md` files. Generated: `skills/<slug>/SKILL.md`.
Convert emits specialist `when-to-use` as the situation trigger plus `/{slug}`, not the full description.

Specialists are slash-only. `/agency` is the catalog.

```bash
python3 scripts/convert-grok.py
# or
./scripts/convert.sh --tool grok
```
