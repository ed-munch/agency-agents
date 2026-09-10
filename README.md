# Agency for Grok Build

The Agency serves the Algorithm.

Grok Build plugin: **273 specialists as procedures**, not Claude character sheets. `/algorithm` runs five gates (question, delete, simplify, accelerate, **automate last**). Specialists are tools of a gate. `/agency` proposes 3–5 slugs for the **current** gate, or none.

Personas by [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) contributors. The Algorithm is the usage frame.

## Result

| Command | What it does |
|---|---|
| `/algorithm` | Five gates. Automate last. |
| `/agency` | 3–5 slugs for the current gate, or none |
| `/<slug>` | Full specialist method, slash-only |

Mapping: `GROK.md`. Roster (slash lookup only): `skills/agency/references/roster.md`.

Gate agents (one gate each, at most one skill): `agency-questioner`, `agency-cutter`, `agency-simplifier`, `agency-accelerator`, `agency-automator` (locked until 1–4), `agency-explorer` (read-only).

## Use

```bash
grok plugin install ed-munch/agency-agents --trust
```

Local checkout:

```bash
grok plugin install /path/to/agency-agents --trust
```

Reload plugins or start a new session. Then `/algorithm`. Do not start on `/ai-engineer` or `/devops-automator`.

`load-specialist.py` is off the `/algorithm` happy path. See [`integrations/grok/assign-specialist.md`](integrations/grok/assign-specialist.md).

## License

MIT.
