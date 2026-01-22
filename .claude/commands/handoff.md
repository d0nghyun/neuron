---
description: Read and update session handoff state. Run at session start.
tools: Read, Edit, Glob
---

# Handoff - Session Continuity

## Purpose

Maintain work continuity across parallel sessions by tracking per-context state.

## Structure

```
handoff/
├── _index.md       # Overview of all active work
├── <context>.md    # Per-context state files
```

## Execution

### Step 1: Read Index

```
Read handoff/_index.md
```

Show user:
- Active contexts
- Paused work
- Recent completions

### Step 2: Identify Context

Ask user or infer from current directory/task:
- Which context to work on?
- New context needed?

### Step 3: Load Context File

If context file exists:
```
Read handoff/<context>.md
```

Display:
- Current status
- Progress and next steps
- Key context/decisions

### Step 4: Update on Changes

**Starting work:**
- Create/update context file
- Add to _index.md Active table

**Progress made:**
- Update context file with progress

**Session end (normal):**
- Update status (completed/paused)
- Move in _index.md accordingly
- Document next steps if paused

**Context overflow:**
- Document EVERYTHING in context file:
  - Exact progress point
  - All decisions made
  - File paths with line numbers
  - Partial work state
  - What to do next

## Notes

- Parallel sessions use separate context files → no conflicts
- Context names: module, feature, or task based
- Be thorough on overflow - next session has zero memory
