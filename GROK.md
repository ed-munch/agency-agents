# Grok Build rewrite

This fork keeps the upstream Agency personas as source and emits **Grok skills**.

## Why this is smaller

Upstream agents are personality documents (median ~238 lines). Grok loads skill *descriptions* into the model context for auto-invocation. Dumping 273 full personas would waste context and flood `/`.

This rewrite:

1. Compresses each persona to a procedure: **Do / Rules / Done when**.
2. Sets `disable-model-invocation: true` on specialists (slash-only: `/frontend-developer`).
3. Ships one auto-invocable catalog skill: `/agency`.
4. Drops communication-style essays, memory fluff, and sample code.

Regenerate after editing a source agent:

```bash
python3 scripts/convert-grok.py
# or
./scripts/convert.sh --tool grok
```

Source of truth: division `*.md` files. Generated: `skills/<slug>/SKILL.md`.
