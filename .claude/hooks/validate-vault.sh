#!/bin/bash
# Hook: PreToolUse - Validate vault file structure on Write/Edit
# Checks naming conventions, depth, and frontmatter for vault/ files

set -euo pipefail

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name // empty')

# Only validate Write/Edit on vault files
case "$tool_name" in
  Write|Edit) ;;
  *) echo '{"decision": "approve"}'; exit 0 ;;
esac

file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.filePath // empty')

# Only validate vault/ files
[[ "$file_path" == */vault/* ]] || { echo '{"decision": "approve"}'; exit 0; }

# Skip hidden/internal paths
rel=${file_path##*/vault/}
[[ "$rel" == _* || "$rel" == .* || "$rel" == memory/* ]] && { echo '{"decision": "approve"}'; exit 0; }

# --- Structure checks ---

# Check depth: max 3 levels (L1-folder/L2-folder/file)
depth=$(echo "$rel" | tr '/' '\n' | wc -l | tr -d ' ')
if [ "$depth" -gt 3 ]; then
  echo "{\"decision\": \"block\", \"reason\": \"Vault depth violation (max 3 levels): $rel. Restructure to fit L1/L2/file.md or L1/file.md pattern. See RULES.md § Vault Rules.\"}"
  exit 0
fi

# Check L1 folder prefix: ##-
l1=$(echo "$rel" | cut -d'/' -f1)
if ! [[ "$l1" =~ ^[0-9]{2}- ]]; then
  echo "{\"decision\": \"block\", \"reason\": \"L1 folder must start with ##- prefix: $l1. Use format like 01-Inbox, 02-Projects, 03-Areas. See RULES.md § Vault Rules.\"}"
  exit 0
fi

# Check L2 folder prefix: ###-
if [ "$depth" -ge 2 ]; then
  l2=$(echo "$rel" | cut -d'/' -f2)
  if [[ -d "$(dirname "$file_path")/$l2" ]] || [ "$depth" -ge 3 ]; then
    if ! [[ "$l2" =~ ^[0-9]{3}- ]]; then
      echo "{\"decision\": \"block\", \"reason\": \"L2 folder must start with ###- prefix: $l2. Use format like 021-arkraft, 041-reference. See RULES.md § Vault Rules.\"}"
      exit 0
    fi
  fi
fi

# Check file naming: ###-*.md
filename=$(basename "$file_path")
if [[ "$filename" == *.md ]]; then
  if ! [[ "$filename" =~ ^[0-9]{3}-.+\.md$ ]]; then
    echo "{\"decision\": \"block\", \"reason\": \"Vault .md files must match ###-name.md: $filename. Rename to format like 001-overview.md. See RULES.md § Vault Rules.\"}"
    exit 0
  fi

  # --- Frontmatter check (Write only) ---
  if [ "$tool_name" = "Write" ]; then
    content=$(echo "$input" | jq -r '.tool_input.content // empty')
    if [ -n "$content" ]; then
      first_line=$(echo "$content" | head -1)
      if [ "$first_line" != "---" ]; then
        echo "{\"decision\": \"block\", \"reason\": \"Vault .md files must start with --- frontmatter. Add YAML frontmatter block: ---\\ntype: <type>\\nname: <name>\\n---\"}"
        exit 0
      fi
      if ! echo "$content" | grep -q "^type:"; then
        echo "{\"decision\": \"block\", \"reason\": \"Vault frontmatter missing required field: type. Add 'type: note|project|reference|guide' to frontmatter.\"}"
        exit 0
      fi
      if ! echo "$content" | grep -q "^name:"; then
        echo "{\"decision\": \"block\", \"reason\": \"Vault frontmatter missing required field: name. Add 'name: <descriptive-name>' to frontmatter.\"}"
        exit 0
      fi
    fi
  fi
fi

echo '{"decision": "approve"}'
