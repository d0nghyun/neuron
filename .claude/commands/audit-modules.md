---
description: Audit submodule compliance with neuron inheritance protocol
tools: Read, Bash, Grep
---

# Audit Submodule Inheritance

## Purpose

Verify all registered submodules follow the correct CLAUDE.md template per module-protocol.md.

## Steps

### Step 1: Load Registry

```bash
cat modules/_registry.yaml
```

Get list of active submodules (status: active).

### Step 2: Initialize Submodules

```bash
git submodule update --init
```

### Step 3: Check Each Submodule

For each active module, run compliance checks:

| Check | Command | Pass |
|-------|---------|------|
| CLAUDE.md exists | `test -f modules/<name>/CLAUDE.md` | File exists |
| Has Inherited Policies | `grep "## Inherited Policies" modules/<name>/CLAUDE.md` | Found |
| Has Required table | `grep "### Required" modules/<name>/CLAUDE.md` | Found |
| No parent-relative paths | `grep -E "\.\./\.\." modules/<name>/CLAUDE.md` | No matches |
| References neuron URL | `grep "github.com/d0nghyun/neuron" modules/<name>/CLAUDE.md` | Found |

### Step 4: Output Report

```markdown
## Submodule Audit Report

| Module | Status | Issues |
|--------|--------|--------|
| <name> | PASS/FAIL | <issues or "None"> |

### Summary
- Total: X modules
- Passing: Y
- Failing: Z

### Remediation
For failing modules, apply template from knowledge/repo-setup.md
```

## Notes

- Run after registering new submodules
- Submodules with empty directories (shallow clone) will fail - run `git submodule update --init` first
- See `knowledge/module-protocol.md` for full verification checklist
