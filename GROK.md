# Grok Build rewrite

This fork keeps the **full method** from each Agency persona and writes it as a Grok skill: a tool-using procedure, not a Claude character sheet.

## What is kept

Everything the specialist actually uses to do the job:

- mission
- rules
- workflow / method
- domain frameworks (for example signal-based outbound, ICPs)
- code patterns and examples
- advanced capabilities
- done-when / out-of-scope

Nothing in those sections is summarized down to a handful of bullets.

## What is dropped

Claude agent padding that does not change the work:

- "You are X" personality preambles
- Identity / Memory / Experience
- Communication Style
- Learning & Memory
- report-template deliverables
- header emoji

## How Grok loads it

Specialists are slash-only (`/frontend-developer`) so 273 full files do not auto-load every turn. `/agency` is the catalog and the only auto-invocable skill. When a specialist runs, Grok gets the whole method.

```bash
python3 scripts/convert-grok.py
# or
./scripts/convert.sh --tool grok
```

Source of truth: division `*.md` files. Generated: `skills/<slug>/SKILL.md`.
