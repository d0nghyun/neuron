#!/bin/bash
# init.sh - Activate a module's skills/agents via symlinks
# Usage: init.sh <module-path>
# Example: init.sh arkraft/arkraft-agent-pm

set -euo pipefail

MODULE="${1:?Usage: init.sh <module-path>}"
PROJECT_DIR="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$PROJECT_DIR"

MODULE_CLAUDE="modules/$MODULE/.claude"
[ -d "$MODULE_CLAUDE" ] || { echo "Module not found: $MODULE" >&2; exit 1; }

PREFIX="${MODULE//\//_}"
count=0

# Commands → Skills (mkdir + symlink SKILL.md)
if [ -d "$MODULE_CLAUDE/commands" ]; then
  for cmd in "$MODULE_CLAUDE/commands"/*.md; do
    [ -f "$cmd" ] || continue
    cmd_name=$(basename "$cmd" .md)
    target=".claude/skills/${PREFIX}--${cmd_name}"
    mkdir -p "$target"
    ln -sf "$PROJECT_DIR/$cmd" "$target/SKILL.md"
    echo "Linked: /${PREFIX}--${cmd_name}"
    count=$((count + 1))
  done
fi

# Skills → Skills (symlink directory)
if [ -d "$MODULE_CLAUDE/skills" ]; then
  for skill in "$MODULE_CLAUDE/skills"/*; do
    [ -d "$skill" ] || continue
    skill_name=$(basename "$skill")
    ln -sf "$PROJECT_DIR/$skill" ".claude/skills/${PREFIX}--${skill_name}"
    echo "Linked: /${PREFIX}--${skill_name}"
    count=$((count + 1))
  done
fi

# Agents → Agents (symlink file)
if [ -d "$MODULE_CLAUDE/agents" ]; then
  for agent in "$MODULE_CLAUDE/agents"/*.md; do
    [ -f "$agent" ] || continue
    agent_name=$(basename "$agent" .md)
    ln -sf "$PROJECT_DIR/$agent" ".claude/agents/${PREFIX}--${agent_name}.md"
    echo "Linked agent: ${PREFIX}--${agent_name}"
    count=$((count + 1))
  done
fi

echo "Activated $count entries for $MODULE"
