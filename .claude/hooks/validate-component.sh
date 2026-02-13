#!/bin/bash
# Hook: PreToolUse - Validate component structure on Write/Edit
# Blocks agents/skills missing required frontmatter fields

set -euo pipefail

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name // empty')

case "$tool_name" in
  Write|Edit) ;;
  *) echo '{"decision": "approve"}'; exit 0 ;;
esac

file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.filePath // empty')

# --- Agent validation: .claude/agents/*.md ---
if [[ "$file_path" == */.claude/agents/*.md && "$file_path" != */README.md ]]; then
  if [ "$tool_name" = "Write" ]; then
    content=$(echo "$input" | jq -r '.tool_input.content // empty')
    [ -z "$content" ] && { echo '{"decision": "approve"}'; exit 0; }

    first_line=$(echo "$content" | head -1)
    if [ "$first_line" != "---" ]; then
      echo '{"decision": "block", "reason": "Agent must start with --- frontmatter. See RULES.md § Component Rules."}'
      exit 0
    fi

    # Extract frontmatter (between first and second ---)
    fm=$(echo "$content" | sed -n '2,/^---$/p' | sed '$d')

    for field in name description tools model; do
      if ! echo "$fm" | grep -q "^${field}:"; then
        echo "{\"decision\": \"block\", \"reason\": \"Agent frontmatter missing required field: ${field}. See RULES.md § Component Rules.\"}"
        exit 0
      fi
    done
  fi
fi

# --- Skill validation: .claude/skills/*/SKILL.md ---
if [[ "$file_path" == */.claude/skills/*/SKILL.md ]]; then
  if [ "$tool_name" = "Write" ]; then
    content=$(echo "$input" | jq -r '.tool_input.content // empty')
    [ -z "$content" ] && { echo '{"decision": "approve"}'; exit 0; }

    first_line=$(echo "$content" | head -1)
    if [ "$first_line" != "---" ]; then
      echo '{"decision": "block", "reason": "Skill must start with --- frontmatter. See RULES.md § Component Rules."}'
      exit 0
    fi

    fm=$(echo "$content" | sed -n '2,/^---$/p' | sed '$d')

    for field in name description; do
      if ! echo "$fm" | grep -q "^${field}:"; then
        echo "{\"decision\": \"block\", \"reason\": \"Skill frontmatter missing required field: ${field}. See RULES.md § Component Rules.\"}"
        exit 0
      fi
    done
  fi
fi

echo '{"decision": "approve"}'
