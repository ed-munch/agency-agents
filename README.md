# Agency for Grok Build

The Agency serves the Algorithm.

Grok Build plugin: **273 specialists as procedures**, not Claude character sheets. Each skill is a full method (Mission, Rules, Method, Done when). `/algorithm` runs the five gates (question, delete, simplify, accelerate, automate last). Specialists are tools of a gate.

## Result

| Command | What it does |
|---|---|
| `/algorithm` | Five gates. Automate last. |
| `/agency` | Catalog (auto-invocable) |
| `/<slug>` | Full specialist method, slash-only |

Roster: `skills/<slug>/SKILL.md`. Mapping: `GROK.md`.

## Use

```bash
grok plugin install ed-munch/agency-agents --trust
```

Local checkout:

```bash
grok plugin install /path/to/agency-agents --trust
```

Reload plugins or start a new session. Then `/algorithm`, `/agency`, or `/frontend-developer`.

Assign a specialist on a subagent: [`integrations/grok/assign-specialist.md`](integrations/grok/assign-specialist.md) + `python3 integrations/grok/load-specialist.py <slug>`.

## License

MIT. Personas by [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) contributors.
