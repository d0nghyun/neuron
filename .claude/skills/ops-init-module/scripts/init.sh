#!/bin/bash
# init.sh - Activate a module's skills/agents/hooks
# Usage: init.sh <module-path>
# Example: init.sh arkraft/arkraft-sdk

set -euo pipefail

MODULE="${1:?Usage: init.sh <module-path>}"
PROJECT_DIR="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$PROJECT_DIR"

MODULE_CLAUDE="modules/$MODULE/.claude"
[ -d "$MODULE_CLAUDE" ] || { echo "Module not found: $MODULE" >&2; exit 1; }

PREFIX="${MODULE//\//_}"
MODULE_ABS="$PROJECT_DIR/modules/$MODULE"
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

# Hooks → Merge into neuron settings.json
MODULE_SETTINGS="$MODULE_CLAUDE/settings.json"
NEURON_SETTINGS="$PROJECT_DIR/.claude/settings.json"
TAG="# [module:${PREFIX}]"

if [ -f "$MODULE_SETTINGS" ] && command -v jq &>/dev/null; then
  # Check if module hooks already merged
  if grep -q "\[module:${PREFIX}\]" "$NEURON_SETTINGS" 2>/dev/null; then
    echo "Hooks already merged for $PREFIX"
  else
    has_hooks=$(jq -r 'has("hooks")' "$MODULE_SETTINGS")
    if [ "$has_hooks" = "true" ]; then
      # Build a temp file with merged hooks
      TMP=$(mktemp)
      cp "$NEURON_SETTINGS" "$TMP"

      # Iterate each event type in module hooks
      for event in $(jq -r '.hooks | keys[]' "$MODULE_SETTINGS"); do
        # Get matcher groups for this event
        group_count=$(jq -r ".hooks[\"$event\"] | length" "$MODULE_SETTINGS")
        for i in $(seq 0 $((group_count - 1))); do
          matcher=$(jq -r ".hooks[\"$event\"][$i].matcher" "$MODULE_SETTINGS")
          # Get inner hooks, rewrite relative commands to absolute + tag
          inner_hooks=$(jq -c ".hooks[\"$event\"][$i].hooks | map(
            if .command then
              .command = (
                if (.command | startswith(\"/\")) then .command
                else \"$MODULE_ABS/\" + .command
                end
              ) + \" $TAG\"
            else . end
          )" "$MODULE_SETTINGS")

          # Merge: append as new matcher group under event
          TMP2=$(mktemp)
          jq --arg event "$event" \
             --arg matcher "$matcher" \
             --argjson hooks "$inner_hooks" \
            '.hooks[$event] = (.hooks[$event] // []) + [{matcher: $matcher, hooks: $hooks}]' \
            "$TMP" > "$TMP2"
          mv "$TMP2" "$TMP"
        done
      done

      mv "$TMP" "$NEURON_SETTINGS"
      hook_count=$(jq -r '.hooks | keys | length' "$MODULE_SETTINGS")
      echo "Merged $hook_count hook event(s) from $PREFIX"
      count=$((count + hook_count))
    fi
  fi
fi

echo "Activated $count entries for $MODULE"
