#!/bin/bash
# tests/run.sh — Neuron hook test runner
# Usage: tests/run.sh [--id HK-01] [--category hook]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SCENARIOS_DIR="$SCRIPT_DIR/scenarios"
RESULTS_DIR="$SCRIPT_DIR/results"

FILTER_ID="" FILTER_CATEGORY=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --id) FILTER_ID="$2"; shift 2 ;;
    --category) FILTER_CATEGORY="$2"; shift 2 ;;
    *) echo "Unknown: $1"; exit 1 ;;
  esac
done

TOTAL=0 PASSED=0 FAILED=0
RESULTS=()
RED='\033[0;31m' GREEN='\033[0;32m' CYAN='\033[0;36m' NC='\033[0m'

build_input_json() {
  local tool_name="$1" file_path="$2" content="$3" command="$4" content_lines="$5"
  local old_string="$6" new_string="$7"
  if [[ -n "$content_lines" && "$content_lines" != "null" && "$content_lines" != "" ]]; then
    content=$(seq 1 "$content_lines" | sed 's/^/line /')
  fi
  # Resolve ${FIXTURES} in file_path
  file_path="${file_path//\$\{FIXTURES\}/$SCRIPT_DIR/fixtures}"
  if [[ "$tool_name" == "Bash" ]]; then
    jq -n --arg tn "$tool_name" --arg cmd "$command" \
      '{"tool_name":$tn,"tool_input":{"command":$cmd}}'
  elif [[ "$tool_name" == "Edit" ]]; then
    jq -n --arg tn "$tool_name" --arg fp "$file_path" \
      --arg os "$old_string" --arg ns "$new_string" \
      '{"tool_name":$tn,"tool_input":{"file_path":$fp,"old_string":$os,"new_string":$ns}}'
  else
    jq -n --arg tn "$tool_name" --arg fp "$file_path" --arg c "$content" \
      '{"tool_name":$tn,"tool_input":{"file_path":$fp,"content":$c}}'
  fi
}

run_test() {
  local hook="$1" input_json="$2" expect_decision="$3"
  local reason_contains="$4" id="$5" desc="$6"

  local output
  output=$(echo "$input_json" | bash "$PROJECT_DIR/.claude/hooks/$hook" 2>/dev/null) || true
  local actual_decision
  actual_decision=$(echo "$output" | jq -r '.decision // "error"')

  if [[ "$actual_decision" != "$expect_decision" ]]; then
    printf "${RED}FAIL${NC} %-7s %s\n" "$id" "$desc"
    printf "     expected=%s got=%s output=%s\n" "$expect_decision" "$actual_decision" "$output"
    return 1
  fi
  if [[ -n "$reason_contains" ]]; then
    local actual_reason
    actual_reason=$(echo "$output" | jq -r '.reason // ""')
    if ! echo "$actual_reason" | grep -qi "$reason_contains"; then
      printf "${RED}FAIL${NC} %-7s %s\n" "$id" "$desc"
      printf "     reason missing '%s': %s\n" "$reason_contains" "$actual_reason"
      return 1
    fi
  fi
  printf "${GREEN}PASS${NC} %-7s %s\n" "$id" "$desc"
}

process_file() {
  local file="$1"
  local category count
  category=$(yq -r '.category' "$file")
  [[ -n "$FILTER_CATEGORY" && "$category" != *"$FILTER_CATEGORY"* ]] && return

  count=$(yq '.scenarios | length' "$file")
  printf "\n${CYAN}━━━ %s (%d scenarios) ━━━${NC}\n" "$category" "$count"

  for ((i = 0; i < count; i++)); do
    local id desc hook
    id=$(yq -r ".scenarios[$i].id" "$file")
    [[ -n "$FILTER_ID" && "$id" != "$FILTER_ID" ]] && continue
    desc=$(yq -r ".scenarios[$i].desc" "$file")
    hook=$(yq -r ".scenarios[$i].hook" "$file")

    local tool_name file_path content command content_lines expect_decision reason_contains
    local old_string new_string
    tool_name=$(yq -r ".scenarios[$i].input.tool_name" "$file")
    file_path=$(yq -r ".scenarios[$i].input.file_path // \"\"" "$file")
    content=$(yq -r ".scenarios[$i].input.content // \"\"" "$file")
    command=$(yq -r ".scenarios[$i].input.command // \"\"" "$file")
    content_lines=$(yq -r ".scenarios[$i].input.content_lines // \"\"" "$file")
    old_string=$(yq -r ".scenarios[$i].input.old_string // \"\"" "$file")
    new_string=$(yq -r ".scenarios[$i].input.new_string // \"\"" "$file")
    expect_decision=$(yq -r ".scenarios[$i].expect.decision" "$file")
    reason_contains=$(yq -r ".scenarios[$i].expect.reason_contains // \"\"" "$file")

    local input_json
    input_json=$(build_input_json "$tool_name" "$file_path" "$content" "$command" "$content_lines" "$old_string" "$new_string")

    TOTAL=$((TOTAL + 1))
    if run_test "$hook" "$input_json" "$expect_decision" "$reason_contains" "$id" "$desc"; then
      PASSED=$((PASSED + 1))
      RESULTS+=("{\"id\":\"$id\",\"status\":\"pass\"}")
    else
      FAILED=$((FAILED + 1))
      RESULTS+=("{\"id\":\"$id\",\"status\":\"fail\"}")
    fi
  done
}

# --- Main ---
for cmd in jq yq; do
  command -v "$cmd" &>/dev/null || { echo "ERROR: $cmd required"; exit 1; }
done

# Hook scenario tests
for f in "$SCENARIOS_DIR"/*.yaml; do
  [[ -f "$f" ]] || continue
  process_file "$f"
done

# Structural integrity tests
if [[ -z "$FILTER_ID" && -z "$FILTER_CATEGORY" ]]; then
  printf "\n${CYAN}━━━ structural (integrity) ━━━${NC}\n"
  st_output=$(bash "$SCRIPT_DIR/test-structural.sh" 2>&1) || true
  st_passed=$(echo "$st_output" | grep -c "PASS" || true)
  st_failed=$(echo "$st_output" | grep -c "FAIL" || true)
  echo "$st_output" | grep -E "PASS|FAIL|broken|missing|without"
  TOTAL=$((TOTAL + st_passed + st_failed))
  PASSED=$((PASSED + st_passed))
  FAILED=$((FAILED + st_failed))
  for id in $(echo "$st_output" | grep -oE 'ST-[0-9]+' | sort -u); do
    if echo "$st_output" | grep -q "PASS.*$id"; then
      RESULTS+=("{\"id\":\"$id\",\"status\":\"pass\"}")
    else
      RESULTS+=("{\"id\":\"$id\",\"status\":\"fail\"}")
    fi
  done
fi

# Module init/cleanup tests (requires initialized submodules with .claude/ content)
INIT_SCRIPT="$PROJECT_DIR/.claude/skills/ops-init-module/scripts/init.sh"
MOD_TEST_PATH="$PROJECT_DIR/modules/arkraft/arkraft-agent-pm/.claude"
if [[ -z "$FILTER_ID" && -z "$FILTER_CATEGORY" && -f "$INIT_SCRIPT" && -d "$MOD_TEST_PATH" ]]; then
  printf "\n${CYAN}━━━ module-init (lifecycle) ━━━${NC}\n"
  TOTAL=$((TOTAL + 1))
  if bash "$SCRIPT_DIR/test-module-init.sh" > /dev/null 2>&1; then
    PASSED=$((PASSED + 1))
    printf "${GREEN}PASS${NC} module-init lifecycle\n"
    RESULTS+=('{"id":"module-init","status":"pass"}')
  else
    FAILED=$((FAILED + 1))
    printf "${RED}FAIL${NC} module-init lifecycle (run tests/test-module-init.sh for details)\n"
    RESULTS+=('{"id":"module-init","status":"fail"}')
  fi
fi

# Summary
echo ""
printf "Total: %d | ${GREEN}Pass: %d${NC} | ${RED}Fail: %d${NC}\n" "$TOTAL" "$PASSED" "$FAILED"

# Save results
mkdir -p "$RESULTS_DIR"
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
results_json="[$(IFS=,; echo "${RESULTS[*]}")]"
printf '{"timestamp":"%s","total":%d,"passed":%d,"failed":%d,"results":%s}\n' \
  "$timestamp" "$TOTAL" "$PASSED" "$FAILED" "$results_json" > "$RESULTS_DIR/summary.json"

[[ "$FAILED" -eq 0 ]]
