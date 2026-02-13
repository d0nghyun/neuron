---
name: ops-daily-memo
description: Write daily memo to vault/memory for nightly recap consolidation
allowed-tools: Read, Glob, Grep, Write, Bash
user-invocable: true
---

# Daily Memo

> Capture today's work as a memo in vault/memory. Nightly ops-vault-recap consolidates it.

## When to Activate

- User runs `/ops-daily-memo`
- End of a significant work session
- User wants to log decisions, progress, or follow-ups

## Steps

### Step 1: Determine Today's File

```
vault/memory/YYYY-MM-DD.md
```

Check if today's file already exists. If yes, append. If no, create.

### Step 2: Gather Context

Ask the user (or infer from session) what to record. Categories:

| Section | Content | Required |
|---------|---------|----------|
| Done | What was accomplished today | Yes |
| Decisions | Key decisions and rationale | If any |
| Follow-up | Tasks or items for tomorrow | If any |
| Notes | Anything else worth remembering | If any |

### Step 3: Write Memo

Create or append to today's file:

```markdown
---
date: YYYY-MM-DD
type: daily-memo
---

# YYYY-MM-DD

## Done
- {accomplishment}

## Decisions
- {decision}: {rationale}

## Follow-up
- [ ] {task}

## Notes
- {note}
```

Rules:
- One file per day (append if multiple sessions)
- When appending, add a `---` separator and new session block
- Keep entries concise — one line per item
- Skip empty sections (don't write headers with no content)

### Step 4: Confirm

Show the user what was written and the file path.

## Integration

- **Input**: Session context, user input
- **Output**: `vault/memory/YYYY-MM-DD.md`
- **Downstream**: `ops-vault-recap` (nightly) consolidates memos into proper vault locations

## Notes

- Memos in `vault/memory/` skip strict vault naming checks (per validate-vault.sh)
- ops-vault-recap handles promotion to `vault/02-Projects/`, `vault/04-Resources/`, etc.
- Old memos get archived to `vault/05-Archive/` after recap
