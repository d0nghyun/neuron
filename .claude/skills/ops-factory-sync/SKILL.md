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

### Step 5.5: Doc Gardening (with `--doc-gardening` flag or CRON)

Scan `.claude/` and `vault/` for stale docs and broken references.

**Stale doc detection**:
```bash
# Find .md files not modified in 30+ days
find .claude vault/ -name '*.md' -mtime +30 -not -path '*/node_modules/*'
```

**Broken reference detection**:
- Extract internal links (e.g., `RULES.md`, `factory/README.md`, `vault/02-Projects/...`)
- Verify each target file exists
- Flag broken links with file:line location

**Scope**: `.claude/**/*.md`, `vault/**/*.md`, root `.md` files

Report stale/broken docs in the drift section with type `stale` or `broken_ref`.

### Step 5.6: Assess Quality Grades

For each agent and skill, compute grade per `factory/README.md § Quality Grades`:

| Grade | Criteria |
|-------|----------|
| A | All frontmatter fields, <150 lines, SSOT refs only, success criteria present |
| B | Required frontmatter, <200 lines, has execution steps |
| C | Missing optional sections or 150-200 lines |
| D | Missing required fields, >200 lines, or hardcoded content |

Process:
1. Read each component's frontmatter and content
2. Score against criteria above
3. Compare with existing `quality_grade` in frontmatter
4. If grade changed: update `quality_grade` and `quality_checked` via Edit
5. Include grade changes in report

Grading checks:
```
line_count < 150 AND has all fields AND refs only → A
line_count < 200 AND has required fields AND has steps → B
missing optional OR 150 ≤ line_count ≤ 200 → C
missing required OR line_count > 200 OR hardcoded → D
```

### Step 6: Generate Report

```yaml
factory_sync:
  timestamp: "{ISO date}"
  components:
    agents: {count}
    skills: {count}
    hooks: {count}
  quality:
    summary: {A: n, B: n, C: n, D: n}
    changes:
      - component: "{name}"
        previous: "{old grade}"
        current: "{new grade}"
        reason: "{why}"
  drift:
    - type: "{naming | missing | orphan | structure | grade | stale | broken_ref}"
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
