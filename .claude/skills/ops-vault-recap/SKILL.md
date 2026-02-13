---
name: ops-vault-recap
description: Recap session memory into vault and validate vault structure
allowed-tools: Read, Glob, Grep, Bash, Write
user-invocable: true
---

# Vault Recap

## When to Activate

- Scheduled nightly via CRON.md
- User runs `/ops-vault-recap`
- After intensive work sessions

## Purpose

1. Consolidate scattered session notes into proper vault locations
2. Validate vault structure integrity
3. Report and fix structural violations

## Steps

### Step 1: Scan Session Memory

```bash
Glob vault/memory/**/*.md       # All session notes
```

Read each file. Identify entries that should be promoted to vault sections:

| Content Type | Destination |
|-------------|-------------|
| Project decisions | `vault/02-Projects/{project}/` |
| Lessons learned | `vault/02-Projects/{project}/learn-*.yaml` |
| General reference | `vault/04-Resources/` |
| Completed/stale notes | `vault/05-Archive/` |

### Step 2: Recap & Consolidate

For each promotable entry:
1. Extract key information (decisions, insights, references)
2. Check if destination file already exists (append vs create)
3. Write to proper vault location following pattern-knowledge.md format
4. Respect vault naming: `###-name.md` with frontmatter (`name`, `type`)

### Step 3: Validate Structure

Run structural checks on all vault files:

| Check | Rule | Source |
|-------|------|--------|
| Depth | Max 3 levels | RULES.md |
| L1 prefix | `##-name/` | validate-vault.sh |
| L2 prefix | `###-name/` | validate-vault.sh |
| File naming | `###-name.md` | validate-vault.sh |
| Frontmatter | `---` with `name:`, `type:` | validate-vault.sh |

### Step 4: Fix Structural Issues

Auto-fixable (safe):
- Missing frontmatter → add with inferred `name` and `type`
- Wrong file prefix → rename to match `###-` pattern

Report only (needs user):
- Depth violations (moving files changes references)
- Duplicate content across locations
- Orphaned files with no clear destination

### Step 5: Clean Stale Memory

Session notes older than 7 days that have been fully recapped:
- Move to `vault/05-Archive/` (not delete)
- Log what was archived

### Step 6: Generate Report

```yaml
vault_recap:
  timestamp: "{ISO date}"
  memory_scanned: {count}
  promoted: {count}
  structure_checks:
    total: {count}
    passed: {count}
    auto_fixed: {count}
    needs_user: {count}
  archived: {count}
  issues:
    - type: "{structural | duplicate | orphan}"
      path: "{file path}"
      detail: "{description}"
      action: "{fixed | needs_user}"
```

## Notes

- Never deletes vault files (archive instead)
- Respects validate-vault.sh rules as source of truth
- Memory files under `vault/memory/` skip strict naming checks (per hook)
- Idempotent: recapping already-promoted content is a no-op
