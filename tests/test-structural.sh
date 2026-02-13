#!/bin/bash
# tests/test-structural.sh — Structural integrity tests
# Validates dependency rules, hook registration, and component conventions mechanically.
# Inspired by: enforce architecture with structural tests, not just documentation.

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_DIR="$PROJECT_DIR/.claude"
SETTINGS="$CLAUDE_DIR/settings.json"

TOTAL=0 PASSED=0 FAILED=0
RED='\033[0;31m' GREEN='\033[0;32m' NC='\033[0m'

assert() {
  local id="$1" desc="$2" result="$3"
  TOTAL=$((TOTAL + 1))
  if [ "$result" -eq 0 ]; then
    printf "${GREEN}PASS${NC} %-7s %s\n" "$id" "$desc"
    PASSED=$((PASSED + 1))
  else
    printf "${RED}FAIL${NC} %-7s %s\n" "$id" "$desc"
    FAILED=$((FAILED + 1))
  fi
}

# --- ST-01: Neuron-level agents must be system-* prefixed ---
st01_result=0
for f in "$CLAUDE_DIR"/agents/*.md; do
  [ -f "$f" ] || continue
  base=$(basename "$f" .md)
  [[ "$base" == "README" ]] && continue
  # Follow symlinks to check origin, but validate the name at neuron level
  if [[ -L "$f" ]]; then continue; fi  # Skip symlinks (module-activated)
  if ! [[ "$base" =~ ^system- ]]; then
    echo "     neuron agent without system- prefix: $base"
    st01_result=1
  fi
done
assert "ST-01" "Neuron agents are system-* only" "$st01_result"

# --- ST-02: Neuron-level skills must be ops-*/api-*/capability-* prefixed ---
st02_result=0
for d in "$CLAUDE_DIR"/skills/*/; do
  [ -d "$d" ] || continue
  base=$(basename "$d")
  [[ -L "$d" ]] && continue  # Skip symlinks (module-activated)
  if ! [[ "$base" =~ ^(ops|api|capability)- ]]; then
    echo "     neuron skill without valid prefix: $base"
    st02_result=1
  fi
done
assert "ST-02" "Neuron skills are ops-*/api-*/capability-* only" "$st02_result"

# --- ST-03: All hook scripts referenced in settings.json exist ---
st03_result=0
# Extract script paths (first token of command, ignoring arguments)
hook_scripts=$(jq -r '.. | .command? // empty' "$SETTINGS" | grep '\.claude/hooks/' | awk '{print $1}' | sort -u)
while IFS= read -r hook; do
  [ -z "$hook" ] && continue
  if [ ! -f "$PROJECT_DIR/$hook" ]; then
    echo "     settings.json references missing hook: $hook"
    st03_result=1
  fi
done <<< "$hook_scripts"
assert "ST-03" "All registered hooks exist on disk" "$st03_result"

# --- ST-04: All hook scripts on disk are registered in settings.json ---
st04_result=0
for f in "$CLAUDE_DIR"/hooks/*.sh; do
  [ -f "$f" ] || continue
  rel=".claude/hooks/$(basename "$f")"
  if ! echo "$hook_scripts" | grep -qF "$rel"; then
    echo "     hook script not registered in settings.json: $rel"
    st04_result=1
  fi
done
assert "ST-04" "All hook scripts are registered in settings.json" "$st04_result"

# --- ST-05: Every skill directory contains SKILL.md ---
st05_result=0
for d in "$CLAUDE_DIR"/skills/*/; do
  [ -d "$d" ] || continue
  [[ -L "${d%/}" ]] && continue  # Skip symlinks
  if [ ! -f "$d/SKILL.md" ]; then
    echo "     skill directory missing SKILL.md: $(basename "$d")"
    st05_result=1
  fi
done
assert "ST-05" "All skill directories contain SKILL.md" "$st05_result"

# --- ST-06: No broken symlinks in .claude/ ---
st06_result=0
while IFS= read -r link; do
  [ -z "$link" ] && continue
  if [ ! -e "$link" ]; then
    echo "     broken symlink: $link"
    st06_result=1
  fi
done < <(find "$CLAUDE_DIR" -type l 2>/dev/null)
assert "ST-06" "No broken symlinks in .claude/" "$st06_result"

# --- ST-07: Root .md files under 200 lines ---
st07_result=0
for f in "$PROJECT_DIR"/*.md; do
  [ -f "$f" ] || continue
  lines=$(wc -l < "$f" | tr -d ' ')
  if [ "$lines" -gt 200 ]; then
    echo "     over 200 lines: $(basename "$f") ($lines lines)"
    st07_result=1
  fi
done
assert "ST-07" "Root .md files under 200-line limit" "$st07_result"

# Summary
echo ""
printf "Structural: %d total | ${GREEN}%d pass${NC} | ${RED}%d fail${NC}\n" "$TOTAL" "$PASSED" "$FAILED"
[[ "$FAILED" -eq 0 ]]
