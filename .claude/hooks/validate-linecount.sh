#!/bin/bash
# Hook: PreToolUse - Suggest when .md files exceed 200 lines
# Non-blocking: approves with warning message

set -euo pipefail

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name // empty')

[ "$tool_name" = "Write" ] || { echo '{"decision": "approve"}'; exit 0; }

file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.filePath // empty')

# Only check .md files
[[ "$file_path" == *.md ]] || { echo '{"decision": "approve"}'; exit 0; }

content=$(echo "$input" | jq -r '.tool_input.content // empty')
[ -z "$content" ] && { echo '{"decision": "approve"}'; exit 0; }

line_count=$(echo "$content" | wc -l | tr -d ' ')

if [ "$line_count" -gt 200 ]; then
  echo "{\"decision\": \"approve\", \"reason\": \"File is ${line_count} lines (convention: max 200). Consider splitting. See RULES.md § File Rules.\"}"
  exit 0
fi

echo '{"decision": "approve"}'
