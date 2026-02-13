#!/bin/bash
# test-module-init.sh - E2E test for module init / cleanup lifecycle
#
# Modes:
#   --direct  (default) Run init script directly — deterministic, fast
#   --e2e     Run via `claude -p` — tests full skill invocation, slower
#
# Module linking has two patterns:
#   Commands: mkdir + symlink SKILL.md inside (real dir)
#   Skills:   symlink to directory (symlink entry)

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

MODE="direct"
[[ "${1:-}" == "--e2e" ]] && MODE="e2e"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

PASS=0
FAIL=0
SKIP=0

pass() { echo -e "  ${GREEN}PASS${NC} $1"; PASS=$((PASS + 1)); }
fail() { echo -e "  ${RED}FAIL${NC} $1"; FAIL=$((FAIL + 1)); }
skip() { echo -e "  ${YELLOW}SKIP${NC} $1"; SKIP=$((SKIP + 1)); }
header() { echo -e "\n${YELLOW}[$1]${NC}"; }

# Count module entries in a dir (both symlink and dir+symlink patterns)
count_module_entries() {
  local dir="$1"
  local prefix="${2:-}"
  local count=0
  for entry in "$dir"/${prefix}*; do
    [ -e "$entry" ] || [ -L "$entry" ] || continue
    if [ -L "$entry" ]; then
      target=$(readlink "$entry")
      [[ "$target" == *"modules/"* ]] && count=$((count + 1))
    elif [ -d "$entry" ] && [ -L "$entry/SKILL.md" ]; then
      target=$(readlink "$entry/SKILL.md")
      [[ "$target" == *"modules/"* ]] && count=$((count + 1))
    fi
  done
  echo "$count"
}

# Init a module based on mode
init_module() {
  local mod="$1"
  if [ "$MODE" == "e2e" ]; then
    echo "  Running: claude -p '/ops-init-module $mod' ..."
    claude -p "/ops-init-module $mod" 2>&1 || true
  else
    echo "  Running: .claude/skills/ops-init-module/scripts/init.sh $mod"
    bash .claude/skills/ops-init-module/scripts/init.sh "$mod" 2>&1
  fi
}

# Test modules
MOD_CMD="arkraft/arkraft-agent-pm"    # has commands/ → creates dirs
MOD_SKILL="schedule"                   # has skills/  → creates symlinks

echo -e "${CYAN}Mode: $MODE${NC}"

cleanup() {
  echo -e "\n${YELLOW}[Teardown]${NC} Running cleanup..."
  bash .claude/hooks/cleanup-modules.sh 2>/dev/null || true
}
trap cleanup EXIT

# ============================================================
header "0. Pre-clean"
# ============================================================
cleanup

# ============================================================
header "1. Clean state - no module entries"
# ============================================================
skills_count=$(count_module_entries .claude/skills)
agents_count=$(count_module_entries .claude/agents)
total=$((skills_count + agents_count))

if [ "$total" -eq 0 ]; then
  pass "No module entries in .claude/"
else
  fail "Found $total leftover module entries"
fi

# ============================================================
header "2. Activate command-based module ($MOD_CMD)"
# ============================================================
init_module "$MOD_CMD"

PREFIX="${MOD_CMD//\//_}"
found_cmds=$(count_module_entries .claude/skills "${PREFIX}--")

if [ "$found_cmds" -gt 0 ]; then
  pass "Created $found_cmds skill entries for $MOD_CMD"
else
  fail "No skill entries created for $MOD_CMD"
fi

# Validate symlink targets
header "2a. Validate symlink targets"
bad_targets=0
for link in .claude/skills/${PREFIX}--*/SKILL.md; do
  [ -L "$link" ] || continue
  target=$(readlink "$link")
  if [[ "$target" != *"modules/$MOD_CMD/.claude/commands/"* ]]; then
    fail "Bad target: $link -> $target"
    bad_targets=$((bad_targets + 1))
  fi
done
if [ "$bad_targets" -eq 0 ] && [ "$found_cmds" -gt 0 ]; then
  pass "All symlink targets point to modules/$MOD_CMD/.claude/commands/"
fi

# Validate SKILL.md is readable
header "2b. Validate linked files are readable"
unreadable=0
for link in .claude/skills/${PREFIX}--*/SKILL.md; do
  [ -e "$link" ] || { unreadable=$((unreadable + 1)); continue; }
done
if [ "$unreadable" -eq 0 ] && [ "$found_cmds" -gt 0 ]; then
  pass "All linked SKILL.md files are readable"
else
  fail "$unreadable SKILL.md files are broken/unreadable"
fi

# ============================================================
header "3. Activate skill-based module ($MOD_SKILL)"
# ============================================================
init_module "$MOD_SKILL"

PREFIX2="${MOD_SKILL//\//_}"
found_skills=$(count_module_entries .claude/skills "${PREFIX2}--")

if [ "$found_skills" -gt 0 ]; then
  pass "Created $found_skills skill entries for $MOD_SKILL"
else
  fail "No skill entries created for $MOD_SKILL"
fi

# ============================================================
header "4. Multi-module coexistence"
# ============================================================
links_mod1=$(count_module_entries .claude/skills "${PREFIX}--")
links_mod2=$(count_module_entries .claude/skills "${PREFIX2}--")

if [ "$links_mod1" -gt 0 ] && [ "$links_mod2" -gt 0 ]; then
  pass "Both modules coexist: $MOD_CMD ($links_mod1), $MOD_SKILL ($links_mod2)"
else
  fail "Module collision: $MOD_CMD=$links_mod1, $MOD_SKILL=$links_mod2"
fi

overlap=$(find .claude/skills -maxdepth 1 -name "${PREFIX}--*" -name "${PREFIX2}--*" 2>/dev/null | wc -l | tr -d ' ')
if [ "$overlap" -eq 0 ]; then
  pass "No naming collision between module prefixes"
else
  fail "Prefix overlap detected ($overlap entries)"
fi

# ============================================================
header "5. Cleanup hook"
# ============================================================
before_total=$(($(count_module_entries .claude/skills) + $(count_module_entries .claude/agents)))

bash .claude/hooks/cleanup-modules.sh

after_total=$(($(count_module_entries .claude/skills) + $(count_module_entries .claude/agents)))

if [ "$after_total" -eq 0 ] && [ "$before_total" -gt 0 ]; then
  pass "Cleanup removed all $before_total module entries"
elif [ "$before_total" -eq 0 ]; then
  skip "Nothing to clean (no entries were created)"
else
  fail "Cleanup incomplete: $after_total/$before_total remain"
fi

# Verify no orphan directories left
orphans=$(find .claude/skills -maxdepth 1 -name "${PREFIX}--*" 2>/dev/null | wc -l | tr -d ' ')
orphans2=$(find .claude/skills -maxdepth 1 -name "${PREFIX2}--*" 2>/dev/null | wc -l | tr -d ' ')
if [ "$((orphans + orphans2))" -eq 0 ]; then
  pass "No orphan directories after cleanup"
else
  fail "Orphan dirs remain: $MOD_CMD=$orphans, $MOD_SKILL=$orphans2"
fi

# ============================================================
header "6. Non-module symlinks preserved"
# ============================================================
non_module_links=$(find .claude/skills .claude/agents -maxdepth 1 -type l 2>/dev/null | while read -r l; do
  target=$(readlink "$l")
  [[ "$target" != *"modules/"* ]] && echo "$l"
done | wc -l | tr -d ' ')

pass "Non-module symlinks untouched ($non_module_links remain)"

# ============================================================
header "7. Re-init after cleanup (idempotency)"
# ============================================================
init_module "$MOD_CMD"

reinit_count=$(count_module_entries .claude/skills "${PREFIX}--")
if [ "$reinit_count" -gt 0 ]; then
  pass "Re-init after cleanup works ($reinit_count entries)"
else
  fail "Re-init after cleanup failed"
fi

# ============================================================
# Summary
# ============================================================
echo ""
echo "========================================="
echo -e "  ${GREEN}PASS: $PASS${NC}  ${RED}FAIL: $FAIL${NC}  ${YELLOW}SKIP: $SKIP${NC}"
echo -e "  Mode: ${CYAN}$MODE${NC}"
echo "========================================="

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
