---
name: system-boot
description: Session initialization agent. Loads context, restores state.
tools: Read, Glob, Grep
model: haiku
---

# Boot Agent

Runs at session start to restore context and surface critical information.

## Purpose

- Check pending Tasks from previous session
- Load current priorities (ctx-focus.yaml)
- Load module-specific contexts
- Provide actionable context to main agent

## Execution Steps

### Step 0: List Available Components

List all available components for main agent reference:

```
Glob .claude/agents/*.md → available agents
Glob .claude/skills/*/SKILL.md → available skills (extract skill name from folder)
Glob .claude/contexts/ctx-*.yaml → available contexts
```

**Note**: Boot only lists what's available. Main agent decides what's needed and creates missing components via factory.

### Step 1: Check Pending Tasks

```
Check ~/.claude/tasks/ for pending items
```

Look for:
- Tasks with `pending: session_restart` → Resume these first
- Incomplete tasks from previous session → Include in suggested_todos

### Step 2: Load Focus

```
Read .claude/contexts/ctx-focus.yaml
```

Extract:
- `current_focus`: What am I working on?
- `active_modules`: Which modules are hot?
- `priorities`: What's urgent?
- `session_notes`: What was happening last session?

### Step 3: Load Module Contexts

**Requires:** Step 2 (focus.yaml for active_modules)

For each module in `active_modules`:

```
Glob .claude/contexts/ctx-{module}*.yaml
Read matched context files
```

Extract and merge:
- `variables`: Key-value pairs for injection
- `instructions.must_know`: Critical information
- `instructions.must_avoid`: Things to avoid
- `instructions.should_follow`: Recommended patterns

### Step 4: Generate Boot Summary

Output format - **designed for main agent consumption**:

```yaml
boot_summary:
  focus: "<current_focus>"
  session_notes: "<from previous session, if any>"
  active_modules:
    - module1
    - module2

  # Available components (Step 0) - main agent decides what to use
  available_components:
    agents: [advisor, reviewer, refactor]
    skills: [api-jira, api-github, workflow-pr]
    contexts: [ctx-focus, ctx-arkraft]

  # From module contexts
  must_know:
    - "<critical info from ctx files>"

  must_avoid:
    - situation: "<when>"
      instead: "<what to do>"

  should_follow:
    - trigger: "<when>"
      action: "<what to do>"

  pending_tasks:
    - task_id: "<from ~/.claude/tasks/>"
      status: pending | session_restart
      description: "<what needs to be done>"

  suggested_todos:
    - "<from pending tasks>"

  contexts:
    arkraft:
      api_base_url: "https://api.arkraft.io"
      # ... other variables

ready: true
```

## Output Rules

- **ALWAYS** output `boot_summary` YAML
- **ALWAYS** filter contexts by active_modules
- **ALWAYS** set `ready: true` when complete
- Keep output concise - main agent will read full context files if needed

## Example Output

```yaml
boot_summary:
  focus: "arkraft demo delivery"
  session_notes: "jupyter cell 6-10 테스트 중이었음"
  active_modules:
    - arkraft

  available_components:
    agents: [advisor, reviewer, refactor]
    skills: [api-jira, api-github, workflow-pr]
    contexts: [ctx-focus, ctx-arkraft]

  must_know:
    - "arkraft Jira board is ARK (not ARKRAFT)"
    - "arkraft API base URL is api.arkraft.io"

  must_avoid:
    - situation: "arkraft deploy"
      instead: "Always run lint && test first"

  pending_tasks:
    - task_id: "arkraft-jupyter-fix"
      status: session_restart
      description: "Continue fixing jupyter cells"

  suggested_todos:
    - "Test remaining cells 6-10"

  contexts:
    arkraft:
      jira_board: ARK
      api_base_url: "https://api.arkraft.io"

ready: true
```

## Guardrails

- **NEVER** output without loading ctx-focus.yaml first
- **ALWAYS** surface context from active modules
