#!/bin/bash
# cleanup-modules.sh - SessionEnd hook
# Remove module symlinks and merged hooks created by ops-init-module

PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
CLAUDE_DIR="$PROJECT_DIR/.claude"
SETTINGS="$CLAUDE_DIR/settings.json"
count=0

# 1. Remove symlinked skills/agents
for dir in "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents"; do
  [ -d "$dir" ] || continue
  for entry in "$dir"/*; do
    # Case 1: Direct symlink to module (skill-based modules)
    if [ -L "$entry" ]; then
      target=$(readlink "$entry")
      if [[ "$target" == *"/modules/"* || "$target" == *"modules/"* ]]; then
        rm -f "$entry"
        count=$((count + 1))
      fi
    # Case 2: Real directory with symlinked SKILL.md (command-based modules)
    elif [ -d "$entry" ] && [ -L "$entry/SKILL.md" ]; then
      target=$(readlink "$entry/SKILL.md")
      if [[ "$target" == *"/modules/"* || "$target" == *"modules/"* ]]; then
        rm -rf "$entry"
        count=$((count + 1))
      fi
    fi
  done
done

# 2. Remove merged module hooks from settings.json
if [ -f "$SETTINGS" ] && grep -q "\[module:" "$SETTINGS" 2>/dev/null; then
  if command -v jq &>/dev/null; then
    # Remove hook entries tagged with [module:*] from all event arrays
    TMP=$(mktemp)
    FILTER="$CLAUDE_DIR/hooks/cleanup-module-hooks.jq"
    jq -f "$FILTER" "$SETTINGS" > "$TMP" && mv "$TMP" "$SETTINGS"
    echo "Cleaned module hooks from settings.json"
    count=$((count + 1))
  fi
fi

[ "$count" -gt 0 ] && echo "Cleaned $count module entry(ies)" || true
