---
name: ops-daily-report
description: Unified daily maintenance report. Orchestrates factory-sync, vault-recap, and daily-memo into one output.
allowed-tools: Read, Glob, Grep, Write, Bash, Task
user-invocable: true
---

# Daily Report

> Run all maintenance checks and produce a single unified report in `vault/memory/`.

## When to Activate

- Scheduled nightly via CRON.md
- User runs `/ops-daily-report`
- End of day wrap-up

## Steps

### Step 1: Git Status Summary

```bash
git status --short
git log --oneline -5
git branch --show-current
```

Capture: current branch, dirty file count, recent commit subjects.

### Step 2: Factory Sync Check

Delegate to `ops-factory-sync` logic (or run inline):

```bash
Glob .claude/agents/*.md
Glob .claude/skills/*/SKILL.md
Read .claude/factory/README.md
```

Produce component inventory and drift summary.
Use the factory-sync report format from its SKILL.md.

### Step 3: Vault Recap

Delegate to `ops-vault-recap` logic (or run inline):

```bash
Glob vault/memory/**/*.md
```

Scan session memory, check vault structure, summarize health.
Use the vault-recap report format from its SKILL.md.

### Step 4: Daily Memo Wrapup

Check if today's memo exists:

```bash
Read vault/memory/YYYY-MM-DD.md
```

If exists, extract Done/Decisions/Follow-up sections.
If not, note "No memo recorded today."

### Step 5: Taste Pattern Detection

Scan recent memory files (last 7 days) for repeated review feedback patterns:

```bash
Glob vault/memory/202*.md
```

Look for recurring themes in Follow-up sections:
- Same type of issue mentioned 3+ times → flag as **hook promotion candidate**
- Same naming/structure correction repeated → flag as **lint rule candidate**

Add a `## Promotion Candidates` section to the report if any detected:

```markdown
## Promotion Candidates
- [ ] "{pattern}" seen {N} times → candidate for hook/lint enforcement
```

This creates a feedback loop: review taste → documented pattern → enforceable rule.

### Step 6: Generate Unified Report


Write to `vault/memory/report-YYYY-MM-DD.md`:

```markdown
---
date: YYYY-MM-DD
type: daily-report
---

# Daily Report -- YYYY-MM-DD

## Git Status
- Branch: {branch}
- Dirty files: {count}
- Recent commits:
  - {commit1}
  - {commit2}
  - ...

## Factory Health
- Agents: {count}
- Skills: {count}
- Hooks: {count}
- Drift: {clean | list of issues}

## Vault Health
- Memory files scanned: {count}
- Promoted: {count}
- Structure issues: {count}
- Archived: {count}

## Today's Work
{from daily memo, or "No memo recorded today."}

## Follow-ups
- [ ] {collected from all steps}
```

Rules:
- Skip empty sections (omit header if nothing to report)
- Keep each item to one line
- One report per day (overwrite if re-run same day)

### Step 7: Display Report

Read back the generated report and display to user.

## Integration

- **Input**: Current repo state, vault state, session memory
- **Output**: `vault/memory/report-YYYY-MM-DD.md`
- **Upstream**: `ops-factory-sync`, `ops-vault-recap`, `ops-daily-memo`
- **Downstream**: User review, follow-up task creation

## Notes

- Idempotent: safe to run multiple times per day (overwrites same-day report)
- Headless compatible: works via `claude -p` for cron execution
- Does not modify components or vault structure — read and report only
