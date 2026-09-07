#!/usr/bin/env bash
# Regression coverage for YAML frontmatter emitted by convert.sh / convert-grok.py.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$(mktemp -d "${TMPDIR:-/tmp}/agency-convert-frontmatter.XXXXXX")"
trap 'rm -rf "$OUTPUT_DIR"' EXIT

for tool in gemini-cli opencode qwen; do
  "$SCRIPT_DIR/convert.sh" --tool "$tool" --out "$OUTPUT_DIR" >/dev/null
done

# Isolate grok output: convert.sh --tool grok always writes repo-root skills/.
python3 "$SCRIPT_DIR/convert-grok.py" \
  --out "$OUTPUT_DIR/grok" \
  --skills-root "$OUTPUT_DIR/skills" \
  >/dev/null

assert_quoted() {
  local file="$1" field="$2" line prefix
  line="$(awk -v key="$field" '$0 ~ "^" key ":" { print; exit }' "$file")"
  prefix="$field: '"
  [[ "$line" == "$prefix"*"'" ]] || {
    printf 'Expected %s in %s to be a single-quoted YAML scalar, got: %s\n' \
      "$field" "$file" "$line" >&2
    return 1
  }
}

assert_quoted \
  "$OUTPUT_DIR/gemini-cli/agents/developer-tooling-engineer.md" \
  description
assert_quoted \
  "$OUTPUT_DIR/opencode/agents/developer-tooling-engineer.md" \
  name
assert_quoted \
  "$OUTPUT_DIR/opencode/agents/developer-tooling-engineer.md" \
  description
assert_quoted \
  "$OUTPUT_DIR/qwen/agents/programmatic-display-buyer.md" \
  description

assert_quoted \
  "$OUTPUT_DIR/skills/frontend-developer/SKILL.md" \
  when-to-use
fd_wtu="$(awk '/^when-to-use:/ { print; exit }' "$OUTPUT_DIR/skills/frontend-developer/SKILL.md")"
fd_gold="when-to-use: 'Use when the work is a web UI, component, or frontend performance change. /frontend-developer'"
if [[ "$fd_wtu" != "$fd_gold" ]]; then
  case "$fd_wtu" in
    *"Use when the work is a web UI"*"/frontend-developer"*)
      case "$fd_wtu" in
        *implement*)
          printf '%s: when-to-use must not contain implement, got: %s\n' \
            "$OUTPUT_DIR/skills/frontend-developer/SKILL.md" "$fd_wtu" >&2
          exit 1
          ;;
      esac
      ;;
    *)
      printf '%s: when-to-use must equal gold situation trigger, got: %s\n' \
        "$OUTPUT_DIR/skills/frontend-developer/SKILL.md" "$fd_wtu" >&2
      exit 1
      ;;
  esac
fi

missing=0
specialists=0
while IFS= read -r skill; do
  slug="$(basename "$(dirname "$skill")")"
  [[ "$slug" == "agency" ]] && continue
  specialists=$((specialists + 1))
  if ! grep -q '^when-to-use:' "$skill"; then
    printf '%s: missing when-to-use\n' "$skill" >&2
    missing=$((missing + 1))
  fi
done < <(find "$OUTPUT_DIR/skills" -mindepth 2 -maxdepth 2 -name SKILL.md | sort)

if [[ "$specialists" -eq 0 ]]; then
  printf 'No specialist SKILL.md files under %s — convert-grok.py did not write skills.\n' \
    "$OUTPUT_DIR/skills" >&2
  exit 1
fi
if [[ "$missing" -ne 0 ]]; then
  printf '%d specialist SKILL.md file(s) missing when-to-use\n' "$missing" >&2
  exit 1
fi

copied=0
while IFS= read -r skill; do
  slug="$(basename "$(dirname "$skill")")"
  [[ "$slug" == "agency" ]] && continue
  wtu="$(awk '/^when-to-use:/ { print; exit }' "$skill")"
  case "$wtu" in
    *"implement it in the existing stack"*)
      printf '%s: when-to-use copied the full description (contains implement it in the existing stack): %s\n' \
        "$skill" "$wtu" >&2
      copied=$((copied + 1))
      ;;
  esac
done < <(find "$OUTPUT_DIR/skills" -mindepth 2 -maxdepth 2 -name SKILL.md | sort)
if [[ "$copied" -ne 0 ]]; then
  printf '%d specialist when-to-use field(s) still copy the full description\n' "$copied" >&2
  exit 1
fi

agency="$OUTPUT_DIR/skills/agency/SKILL.md"
agency_wtu="$(awk '/^when-to-use:/ { print; exit }' "$agency")"
catalog_wtu='when-to-use: agency, specialist, roster, persona, agent role, the agency'
if [[ "$agency_wtu" != "$catalog_wtu" ]]; then
  printf '%s: catalog when-to-use changed, got: %s\n' "$agency" "$agency_wtu" >&2
  exit 1
fi

echo "PASS: converted YAML frontmatter keeps scalar values safely quoted"
