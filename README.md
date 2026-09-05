# The Agency for Grok Build

Fork of [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents). Same specialists, written as **Grok skills**.

Not a cropped Claude dump. Each skill keeps the full method (rules, workflow, frameworks, examples) and drops only the character-sheet padding (personality, memory, communication style). A short Grok block tells the model to use tools and deliver the artifact.

## Install

```bash
grok plugin install ed-munch/agency-agents --trust
```

Or copy into Grok home:

```bash
./scripts/install.sh --tool grok
# -> ~/.grok/skills/<slug>/SKILL.md
```

Subset:

```bash
./scripts/install.sh --tool grok --division engineering,security
./scripts/install.sh --tool grok --agent frontend-developer,code-reviewer
```

Reload plugins or start a new session so `/agency` and `/frontend-developer` appear.

## Use

| Command | What it does |
|---|---|
| `/agency` | Catalog. Auto-invoked when you ask for a specialist. |
| `/frontend-developer` | Full frontend method for this turn. |
| `/code-reviewer` | Full review method for this turn. |

## vs upstream

| | Upstream (Claude) | This fork (Grok) |
|---|---|---|
| Unit | Persona `.md` agent | `SKILL.md` procedure |
| Method | Full | Full (not cropped) |
| Padding | Identity, vibe, memory, voice | Stripped |
| How it runs | Claude Code agent | Slash skill + Grok tools |
| Auto-invoke | Agent descriptions | Only `/agency` |
| Install | `~/.claude/agents/` | `grok plugin install` or `~/.grok/skills/` |

Source personas stay in `engineering/`, `design/`, … Generated skills live in `skills/`. See [GROK.md](GROK.md).

## Regenerate

```bash
./scripts/convert.sh --tool grok
```

## Other tools

Original convert/install still targets Claude Code, Cursor, Codex, Gemini, and the rest. This fork adds **`grok`**.

## License

MIT, same as upstream. Personas by [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) contributors.
