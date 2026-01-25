#!/bin/bash
# Claude Code Hook - Load Active Modules
# Symlinks skills/agents from active modules into neuron's .claude/

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
MODULES_FILE="$PROJECT_ROOT/.claude/contexts/ctx-active-modules.yaml"
LOG_FILE="/tmp/neuron-modules.log"

echo "[$(date)] load-active-modules started" >> "$LOG_FILE"

if [ ! -f "$MODULES_FILE" ]; then
  echo "[$(date)] No ctx-active-modules.yaml found" >> "$LOG_FILE"
  exit 0
fi

# Parse active modules from yaml
while IFS= read -r line; do
  # Skip empty lines and yaml keys
  [[ -z "$line" || "$line" =~ ^[[:space:]]*# || "$line" == "active_modules:" ]] && continue

  # Extract module path: "  - arkraft/arkraft-agent-pm" → "arkraft/arkraft-agent-pm"
  module=$(echo "$line" | sed 's/^[[:space:]]*-[[:space:]]*//')
  [[ -z "$module" ]] && continue

  module_claude="$PROJECT_ROOT/modules/$module/.claude"
  # Prefix for symlinks: arkraft/arkraft-agent-pm → arkraft--arkraft-agent-pm
  prefix="${module//\//_}"

  echo "[$(date)] Processing module: $module" >> "$LOG_FILE"

  # Symlink skills
  if [ -d "$module_claude/skills" ]; then
    for skill in "$module_claude/skills"/*; do
      [ -d "$skill" ] || continue
      skill_name=$(basename "$skill")
      target="$PROJECT_ROOT/.claude/skills/${prefix}--${skill_name}"
      if [ ! -L "$target" ]; then
        ln -sf "$skill" "$target"
        echo "[$(date)]   Linked skill: $skill_name" >> "$LOG_FILE"
      fi
    done
  fi

  # Symlink agents
  if [ -d "$module_claude/agents" ]; then
    for agent in "$module_claude/agents"/*.md; do
      [ -f "$agent" ] || continue
      agent_name=$(basename "$agent")
      target="$PROJECT_ROOT/.claude/agents/${prefix}--${agent_name}"
      if [ ! -L "$target" ]; then
        ln -sf "$agent" "$target"
        echo "[$(date)]   Linked agent: $agent_name" >> "$LOG_FILE"
      fi
    done
  fi

  # Symlink commands (as skills)
  if [ -d "$module_claude/commands" ]; then
    for cmd in "$module_claude/commands"/*.md; do
      [ -f "$cmd" ] || continue
      cmd_name=$(basename "$cmd" .md)
      # Commands become skills with the module prefix
      target="$PROJECT_ROOT/.claude/skills/${prefix}--${cmd_name}"
      if [ ! -L "$target" ]; then
        mkdir -p "$target"
        ln -sf "$cmd" "$target/SKILL.md"
        echo "[$(date)]   Linked command as skill: $cmd_name" >> "$LOG_FILE"
      fi
    done
  fi

done < "$MODULES_FILE"

echo "[$(date)] load-active-modules completed" >> "$LOG_FILE"
exit 0
