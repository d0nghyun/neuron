---
name: ops-factory-sync
description: Audit factory patterns against actual components and update drift
allowed-tools: Read, Glob, Grep, Edit, Write
user-invocable: true
---

# Factory Sync

## When to Activate

- Scheduled nightly via CRON.md
- User runs `/ops-factory-sync`
- After bulk component changes

## Purpose

Keep factory patterns aligned with reality.
Detect drift between what factory documents say and what actually exists.

## Steps

### Step 1: Inventory Components

```bash
Glob .claude/agents/*.md          # List all agents
Glob .claude/skills/*/SKILL.md    # List all skills
Read .claude/settings.json        # List all hooks
```

### Step 2: Read Factory State

```bash
Read .claude/factory/README.md
Read RULES.md
```

### Step 3: Check Alignment

For each component type, verify:

| Check | Source of Truth | Actual |
|-------|----------------|--------|
| Agent naming prefixes | factory/README.md § Naming | agents/*.md filenames |
| Skill naming prefixes | factory/README.md § Naming | skills/*/SKILL.md dirs |
| Component types listed | factory/README.md § Selection Guide | existing components |
| Hook registrations | settings.json | hooks/ scripts |

### Step 4: Check Hook-Rules Alignment

Compare enforcement hooks against RULES.md declarations:

```
Read RULES.md § Component Rules     → extract required fields per type
Read .claude/hooks/validate-component.sh → extract enforced fields
```

| Check | Source of Truth | Enforcement |
|-------|----------------|-------------|
| Agent required fields | RULES.md § Component Rules | validate-component.sh `for field in ...` |
| Skill required fields | RULES.md § Component Rules | validate-component.sh `for field in ...` |
| Vault structure rules | RULES.md § Vault Rules | validate-vault.sh checks |

Flag if RULES.md declares fields that hooks don't enforce, or vice versa.

### Step 5: Detect Drift

Flag:
- Components using unlisted naming prefixes
- Patterns described in factory but no components exist
- Hooks in settings.json pointing to missing scripts
- Components missing required structure (per RULES.md)
- Hook enforcement out of sync with RULES.md declarations

### Step 6: Generate Report

```yaml
factory_sync:
  timestamp: "{ISO date}"
  components:
    agents: {count}
    skills: {count}
    hooks: {count}
  drift:
    - type: "{naming | missing | orphan | structure}"
      detail: "{description}"
      suggestion: "{fix}"
  status: clean | drift_detected
```

### Step 7: Auto-fix (Safe Only)

Only fix these automatically:
- Update component counts in factory docs
- Add missing naming prefixes to README examples

All other fixes: report only, let user decide.

## Notes

- Idempotent: safe to run repeatedly
- Never deletes components
- Never modifies component logic, only factory metadata
