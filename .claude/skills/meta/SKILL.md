---
name: meta
description: Update meta/ files (identity, focus, team) to record learnings and prevent repeated conversations. Use at session end or when context changes.
allowed-tools: Read, Edit, Write, AskUserQuestion
---

# Meta Update Skill

## Purpose

Update AI long-term memory (`meta/` folder) to:
- Record session learnings
- Update current focus/priorities
- Add/modify team information
- Prevent repeated mistakes and conversations

## Files

| File | Purpose | When to Update |
|------|---------|----------------|
| `meta/identity.yaml` | Who I am | Role/org changes |
| `meta/focus.yaml` | Current priorities | Focus shift, new project |
| `meta/team.yaml` | Team registry | Team member changes |

## Workflow

1. **Ask** which file to update:
   - identity (rare)
   - focus (priority/project changes)
   - team (member changes)
   - Or describe what to record

2. **Read** current state of target file

3. **Propose** changes to user

4. **Apply** after confirmation

## Quick Update Patterns

### Focus Change
```yaml
# meta/focus.yaml
current_focus: <new focus>
```

### New Priority
```yaml
# meta/focus.yaml - add to priorities.high/medium/low
priorities:
  high:
    - <new priority>
```

### Team Member
```yaml
# meta/team.yaml - add under members
members:
  새이름:
    email: name@quantit.io
    jira_account_id: "..."
    slack_id: "..."
    role: "..."
```

## Execution

When `/meta` is invoked:

1. Ask user what to update:
   - "What would you like to record in meta?"
   - Options: focus change, new learning, team update, other

2. Read relevant file(s)

3. Show proposed changes

4. Apply with user confirmation

**Always commit changes after update.**
