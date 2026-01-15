#!/bin/bash
# Audit submodule compliance with neuron inheritance protocol
# Usage: ./scripts/audit-modules.sh [--fix]

set -e

NEURON_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REGISTRY="$NEURON_ROOT/modules/_registry.yaml"
FIX_MODE=false

[[ "$1" == "--fix" ]] && FIX_MODE=true

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}✓${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; }
warn() { echo -e "${YELLOW}!${NC} $1"; }

# Get active modules from registry
get_active_modules() {
    grep -B1 "status: active" "$REGISTRY" | grep -E "^  [a-z]" | sed 's/://g' | tr -d ' '
}

# Check single module compliance
check_module() {
    local name=$1
    local path="$NEURON_ROOT/modules/$name"
    local claude_md="$path/CLAUDE.md"
    local issues=()

    echo ""
    echo "=== $name ==="

    # Check if directory exists and has content
    if [[ ! -d "$path" ]] || [[ -z "$(ls -A "$path" 2>/dev/null)" ]]; then
        warn "Empty directory (submodule not initialized)"
        echo "  Run: git submodule update --init modules/$name"
        return 1
    fi

    # Check 1: CLAUDE.md exists
    if [[ -f "$claude_md" ]]; then
        pass "CLAUDE.md exists"
    else
        fail "CLAUDE.md missing"
        issues+=("missing_claude_md")
    fi

    # Check 2: Has Inherited Policies section
    if [[ -f "$claude_md" ]] && grep -q "## Inherited Policies" "$claude_md"; then
        pass "Has ## Inherited Policies"
    else
        fail "Missing ## Inherited Policies section"
        issues+=("missing_inherited")
    fi

    # Check 3: Has Required table
    if [[ -f "$claude_md" ]] && grep -q "### Required" "$claude_md"; then
        pass "Has ### Required table"
    else
        fail "Missing ### Required table"
        issues+=("missing_required")
    fi

    # Check 4: No parent-relative paths
    if [[ -f "$claude_md" ]] && grep -qE "\.\./\.\." "$claude_md"; then
        fail "Contains parent-relative paths (../../)"
        issues+=("relative_paths")
    else
        pass "No parent-relative paths"
    fi

    # Check 5: References neuron URL
    if [[ -f "$claude_md" ]] && grep -q "github.com/d0nghyun/neuron" "$claude_md"; then
        pass "References neuron URL"
    else
        fail "Missing neuron URL reference"
        issues+=("missing_url")
    fi

    # Check 6: Has required policies inlined
    local required_policies=("3 Axioms" "SSOT" "Verify Before Done" "Conventional Commits" "Co-Authored-By")
    for policy in "${required_policies[@]}"; do
        if [[ -f "$claude_md" ]] && grep -q "$policy" "$claude_md"; then
            pass "Has policy: $policy"
        else
            fail "Missing policy: $policy"
            issues+=("missing_policy_$policy")
        fi
    done

    # Summary
    if [[ ${#issues[@]} -eq 0 ]]; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC} (${#issues[@]} issues)"

        if $FIX_MODE; then
            echo "  → Auto-fix not yet implemented. Apply template manually."
        fi
        return 1
    fi
}

# Main
echo "Neuron Submodule Audit"
echo "======================"
echo "Registry: $REGISTRY"
echo "Fix mode: $FIX_MODE"

MODULES=$(get_active_modules)
TOTAL=0
PASSED=0
FAILED=0

for module in $MODULES; do
    TOTAL=$((TOTAL + 1))
    if check_module "$module"; then
        PASSED=$((PASSED + 1))
    else
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "======================"
echo "Summary: $PASSED/$TOTAL passed"
[[ $FAILED -gt 0 ]] && echo -e "${RED}$FAILED modules need attention${NC}"

exit $FAILED
