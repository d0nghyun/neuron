#!/bin/bash
# Hook: PostToolUse — Dispatch to submodule PostToolUse hooks (auto-format etc.)

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty')
NEURON_ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"

[[ "$TOOL" != "Write" && "$TOOL" != "Edit" ]] && exit 0

TARGET=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
[[ -z "$TARGET" ]] && exit 0

# Find which module this file belongs to
for module_settings in "$NEURON_ROOT"/modules/*/*/.claude/settings.json; do
  [[ ! -f "$module_settings" ]] && continue
  mod_dir="$(cd "$(dirname "$module_settings")/.." && pwd)"
  if [[ "$TARGET" == "$mod_dir"* ]]; then
    SETTINGS="$module_settings"
    MODULE_ROOT="$mod_dir"
    break
  fi
done

[[ -z "$MODULE_ROOT" ]] && exit 0

# Find PostToolUse hooks matching this tool
HOOK_COMMANDS=$(jq -r --arg tool "$TOOL" '
  .hooks.PostToolUse[]? |
  select(.matcher | test($tool)) |
  .hooks[]? | .command
' "$SETTINGS" 2>/dev/null)

while IFS= read -r cmd; do
  [[ -z "$cmd" ]] && continue
  if [[ "$cmd" != /* ]]; then
    cmd="$MODULE_ROOT/$cmd"
  fi
  [[ ! -x "$cmd" ]] && continue
  echo "$INPUT" | "$cmd" 2>/dev/null || true
done <<< "$HOOK_COMMANDS"

exit 0
