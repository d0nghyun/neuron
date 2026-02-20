#!/bin/sh

# Claude Code PostToolUse hook: reads pre-push error file after failed git push
# Outputs structured errors as system-reminder for Claude to parse

# Only trigger on git push commands
TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}"
echo "$TOOL_INPUT" | grep -q "git push" || exit 0

# Find error file in current dir or submodule dirs
ERROR_FILE=""
for candidate in \
  ".pre-push-errors.json" \
  "modules/arkraft/arkraft-api/.pre-push-errors.json" \
  "modules/arkraft/arkraft-web/.pre-push-errors.json"; do
  if [ -f "$candidate" ]; then
    ERROR_FILE="$candidate"
    break
  fi
done

[ -z "$ERROR_FILE" ] && exit 0

# Output structured errors for Claude
echo "<pre-push-check-failed>"
cat "$ERROR_FILE"
echo "</pre-push-check-failed>"

# Clean up
rm -f "$ERROR_FILE"
