#!/bin/bash
# Hook: PreToolUse — Dispatch to submodule hooks based on file path
# Detects which module a file belongs to and runs that module's hooks.
# Each module owns its own hooks (SSOT). This dispatcher just routes.

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty')
NEURON_ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"

# Determine file path to check
case "$TOOL" in
  Write|Edit)
    TARGET=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
    ;;
  Bash)
    TARGET=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
    # For Bash, use cwd to determine module context
    CWD=$(echo "$INPUT" | jq -r '.cwd // empty')
    if [[ -n "$CWD" ]] && [[ "$CWD" == *modules/* ]]; then
      TARGET="$CWD"
    fi
    ;;
  *)
    exit 0
    ;;
esac

[[ -z "$TARGET" ]] && exit 0

# Find which module this file belongs to
MODULE_ROOT=""
for module_settings in "$NEURON_ROOT"/modules/*/*/.claude/settings.json; do
  [[ ! -f "$module_settings" ]] && continue
  mod_dir="$(cd "$(dirname "$module_settings")/.." && pwd)"
  if [[ "$TARGET" == "$mod_dir"* ]]; then
    MODULE_ROOT="$mod_dir"
    break
  fi
done

[[ -z "$MODULE_ROOT" ]] && exit 0

# Determine which hooks to run based on tool type
HOOKS_DIR="$MODULE_ROOT/.claude/hooks"
[[ ! -d "$HOOKS_DIR" ]] && exit 0

# Read module's settings.json to find matching hooks
SETTINGS="$MODULE_ROOT/.claude/settings.json"
[[ ! -f "$SETTINGS" ]] && exit 0

# Find PreToolUse hooks matching this tool
HOOK_COMMANDS=$(jq -r --arg tool "$TOOL" '
  .hooks.PreToolUse[]? |
  select(.matcher | test($tool)) |
  .hooks[]? | .command
' "$SETTINGS" 2>/dev/null)

# Run each matching hook, stop on first block (exit 2)
while IFS= read -r cmd; do
  [[ -z "$cmd" ]] && continue
  # Resolve relative paths from module root
  if [[ "$cmd" != /* ]]; then
    cmd="$MODULE_ROOT/$cmd"
  fi
  [[ ! -x "$cmd" ]] && continue

  OUTPUT=$(echo "$INPUT" | "$cmd" 2>&1)
  EXIT_CODE=$?

  if [[ $EXIT_CODE -eq 2 ]]; then
    echo "$OUTPUT" >&2
    exit 2
  fi

  # Pass through non-empty approve/warn output
  if [[ -n "$OUTPUT" ]]; then
    echo "$OUTPUT"
  fi
done <<< "$HOOK_COMMANDS"

# Also run PostToolUse hooks if tool is Write|Edit (for auto-format etc.)
# PostToolUse is handled separately by the PostToolUse event, skip here.

exit 0
