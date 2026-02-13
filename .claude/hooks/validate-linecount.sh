#!/bin/bash
# Hook: PreToolUse - Block .md files exceeding 200 lines
# Enforces RULES.md § File Rules mechanically

set -euo pipefail

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name // empty')

case "$tool_name" in
  Write|Edit) ;;
  *) echo '{"decision": "approve"}'; exit 0 ;;
esac

file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.filePath // empty')

# Only check .md files
[[ "$file_path" == *.md ]] || { echo '{"decision": "approve"}'; exit 0; }

# For Write: check new content directly
if [ "$tool_name" = "Write" ]; then
  content=$(echo "$input" | jq -r '.tool_input.content // empty')
  [ -z "$content" ] && { echo '{"decision": "approve"}'; exit 0; }
  line_count=$(echo "$content" | wc -l | tr -d ' ')
fi

# For Edit: estimate resulting file size
if [ "$tool_name" = "Edit" ]; then
  [ -f "$file_path" ] || { echo '{"decision": "approve"}'; exit 0; }
  old_str=$(echo "$input" | jq -r '.tool_input.old_string // empty')
  new_str=$(echo "$input" | jq -r '.tool_input.new_string // empty')
  old_lines=$(echo "$old_str" | wc -l | tr -d ' ')
  new_lines=$(echo "$new_str" | wc -l | tr -d ' ')
  current=$(wc -l < "$file_path" | tr -d ' ')
  line_count=$(( current - old_lines + new_lines ))
fi

if [ "${line_count:-0}" -gt 200 ]; then
  echo "{\"decision\": \"block\", \"reason\": \"BLOCKED: ${line_count} lines exceeds 200-line limit. Split the file into smaller components. See RULES.md § File Rules.\"}"
  exit 0
fi

echo '{"decision": "approve"}'
