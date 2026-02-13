#!/bin/bash
# cleanup-modules.sh - SessionEnd hook
# Remove module symlinks created by ops-init-module
# Only removes symlinks pointing into modules/ (preserves plugin symlinks)

PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
CLAUDE_DIR="$PROJECT_DIR/.claude"
count=0

for dir in "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents"; do
  [ -d "$dir" ] || continue
  for link in "$dir"/*; do
    [ -L "$link" ] || continue
    target=$(readlink "$link")
    if [[ "$target" == *"/modules/"* || "$target" == *"modules/"* ]]; then
      rm -f "$link"
      count=$((count + 1))
    fi
  done
done

[ "$count" -gt 0 ] && echo "Cleaned $count module symlink(s)" || true
