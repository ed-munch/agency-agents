# Grok Build

Compressed skills for [Grok Build](https://github.com/xai-org).

```bash
./scripts/convert.sh --tool grok
./scripts/install.sh --tool grok
```

Preferred install (plugin, one namespace):

```bash
grok plugin install ed-munch/agency-agents --trust
```

Output:

- `skills/` at repo root (committed plugin layout)
- `integrations/grok/skills/` (install.sh mirror, gitignored)

## Spawn protocol

Every Grok subagent gets an Agency specialist. See `spawn.md`. Slice METHOD with `slice.py <slug>`.
