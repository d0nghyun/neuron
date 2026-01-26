#!/bin/bash
# Hook: PreToolUse validation
# Validates tool inputs before execution

set -euo pipefail

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name // empty')

case "$tool_name" in
  Write|Edit)
    file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.filePath // empty')

    # Block writes to credentials
    if [[ "$file_path" == *".credentials"* ]]; then
      echo '{"decision": "block", "reason": "Cannot modify credentials files directly"}'
      exit 0
    fi

    # Warn on settings modification
    if [[ "$file_path" == *"settings.json"* ]]; then
      echo '{"decision": "approve", "reason": "Modifying settings.json - verify hooks configuration"}'
      exit 0
    fi
    ;;

  Bash)
    command=$(echo "$input" | jq -r '.tool_input.command // empty')

    # Warn on force operations
    if echo "$command" | grep -qE 'rm -rf|--force|--hard|force push'; then
      echo '{"decision": "approve", "reason": "Potentially destructive command detected"}'
      exit 0
    fi

    # Warn on credential access
    if echo "$command" | grep -qE '\.credentials|api.key|secret|token' | grep -qE 'cat|echo|print'; then
      echo '{"decision": "approve", "reason": "Command may expose credentials"}'
      exit 0
    fi
    ;;
esac

# Default: approve
echo '{"decision": "approve"}'
