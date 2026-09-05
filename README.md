# The Agency for Grok Build

Fork of [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents), rewritten as **Grok skills**.

Upstream is a catalog of specialist *personas* (median ~238 lines, ~73k lines total). Grok Build skills need the opposite: short procedures, slash commands, and almost nothing in auto-invoke context.

This fork compresses the roster to **~18% of the original line count**, makes specialists slash-only, and keeps one auto-invocable catalog.

## Install

```bash
grok plugin install ed-munch/agency-agents --trust
```

Or copy skills into your Grok home:

```bash
./scripts/install.sh --tool grok
# -> ~/.grok/skills/<slug>/SKILL.md
```

Subset:

```bash
./scripts/install.sh --tool grok --division engineering,security
./scripts/install.sh --tool grok --agent frontend-developer,code-reviewer
```

Restart the Grok session (or reload plugins) so `/agency` and `/frontend-developer` appear.

## Use

| Command | What it does |
|---|---|
| `/agency` | Catalog. Auto-invoked when you ask for a specialist. |
| `/frontend-developer` | Run that specialist for this turn. |
| `/code-reviewer` | Same, for review. |

Ask: "use the frontend developer and build the settings page." Grok should load `/agency` or the named skill and follow it.

## What changed vs upstream

| | Upstream | This fork |
|---|---|---|
| Unit | Persona `.md` agent | Grok `SKILL.md` |
| Auto-invoke | Every agent description | Only `/agency` |
| Body | Identity, vibe, sample code, templates | Do / Rules / Done when |
| Size | ~73k lines | ~13k lines |
| Install | `~/.claude/agents/` | `grok plugin install` or `~/.grok/skills/` |

Source personas are still in `engineering/`, `design/`, … so you can sync upstream. Generated skills live in `skills/`. See [GROK.md](GROK.md).

## Regenerate

```bash
./scripts/convert.sh --tool grok
```

## Other tools

The original convert/install scripts still target Claude Code, Cursor, Codex, Gemini, and the rest. This fork adds **`grok`** as a first-class tool in `tools.json`.

```bash
./scripts/install.sh --tool claude-code   # unchanged
./scripts/install.sh --tool grok          # new
```

## License

MIT, same as upstream. Personas by [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) contributors. Grok rewrite in this fork.
