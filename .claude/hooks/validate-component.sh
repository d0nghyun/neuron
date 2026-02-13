#!/bin/bash
# Hook: PreToolUse - Validate component structure and naming on Write/Edit
# Blocks agents/skills missing required frontmatter or violating naming conventions

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
  basename=$(basename "$file_path" .md)

  # Naming validation: must match {type}-{name} pattern
  valid_prefixes="system|feature-dev|code"
  if ! echo "$basename" | grep -qE "^(${valid_prefixes})-"; then
    echo "{\"decision\": \"block\", \"reason\": \"Agent name '${basename}' has invalid prefix. Must be: system-*, feature-dev-*, or code-*. See factory/README.md § Naming Conventions.\"}"
    exit 0
  fi

  # Frontmatter validation (Write only)
  if [ "$tool_name" = "Write" ]; then
    content=$(echo "$input" | jq -r '.tool_input.content // empty')
    [ -z "$content" ] && { echo '{"decision": "approve"}'; exit 0; }

    first_line=$(echo "$content" | head -1)
    if [ "$first_line" != "---" ]; then
      echo '{"decision": "block", "reason": "Agent must start with --- frontmatter. See RULES.md § Component Rules."}'
      exit 0
    fi

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
  # Extract skill directory name
  skill_dir=$(basename "$(dirname "$file_path")")

  # Naming validation: must match {type}-{name} pattern
  valid_prefixes="ops|api|workflow|capability"
  if ! echo "$skill_dir" | grep -qE "^(${valid_prefixes})-"; then
    echo "{\"decision\": \"block\", \"reason\": \"Skill name '${skill_dir}' has invalid prefix. Must be: ops-*, api-*, workflow-*, or capability-*. See factory/README.md § Naming Conventions.\"}"
    exit 0
  fi

  # Frontmatter validation (Write only)
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
