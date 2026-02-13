#!/bin/bash
# cleanup-modules.sh - SessionEnd hook
# Remove module symlinks created by ops-init-module
# Only removes symlinks pointing into modules/ (preserves plugin symlinks)

PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
CLAUDE_DIR="$PROJECT_DIR/.claude"
count=0

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

[ "$count" -gt 0 ] && echo "Cleaned $count module entry(ies)" || true
