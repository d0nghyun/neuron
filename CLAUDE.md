# Neuron

Neuron is a **Component Factory** that runs on Claude Code.
Claude Code provides agents, skills, hooks, and task management.
Neuron adds templates, registry, contexts, and guiding principles.

## Principles

| # | Principle | Description |
|---|-----------|-------------|
| 1 | **SSOT** | One source of truth. No duplication. |
| 2 | **Simplicity** | Simple solutions over complex ones. Build only what's needed now. |
| 3 | **Modularity** | Independent, replaceable components. |
| 4 | **Verify** | Prove it works. Don't assume. |
| 5 | **Learn** | Record failures, find patterns, improve system. |
| 6 | **Autonomy** | Act first. Ask only when truly blocked. |
| 7 | **Sustainability** | Build reproducible, self-evolving processes. |

## Structure

```
.claude/
├─ agents/       # Judgment components (self-describing)
├─ skills/       # Execution components (self-describing)
├─ factory/      # Reference patterns for component generation
├─ contexts/     # Session state: identity, focus, project configs
└─ knowledge/    # Reference docs + accumulated learnings
```

## Component Lifecycle

### Step 1: Analyze Request (MANDATORY)

Before complex tasks, identify required components:

```
Request Analysis → Required components:
  - agents: [advisor, reviewer, ...]
  - skills: [api-jira, workflow-pr, ...]
  - contexts: [ctx-arkraft, ...]
```

### Step 2: Component Resolution

| Situation | Action |
|-----------|--------|
| All exist | → boot → execute → wrapup |
| Some missing | → factory reference → create → session handoff |
| Existing sufficient | → execute directly |

### Step 3: Creation (when missing)

1. Read `factory/README.md` for component selection guide
2. Select pattern: agent | skill | context | hook
3. Create at correct location
4. Create Task with `pending: session_restart`

Each component is self-describing. Its `.md` file contains:
- When to use it
- How to invoke it
- What it returns

## Session Lifecycle

**Complex tasks** (multi-file changes, commits, external APIs):
- Start with `system-boot` agent → loads contexts, creates tasks
- End with `system-wrapup` agent → persists learnings

**Simple tasks** (read-only, explanations): Skip boot/wrapup.

## Contexts & Knowledge

**Contexts** (`contexts/`): Session state. `ctx-*.yaml` files. Loaded by `system-boot`.

**Knowledge** (`knowledge/`): Reference docs. Prefixed by category. Updated by `system-wrapup`.

## Conventions

- **Language**: English for all neuron files
- **File size**: Max 200 lines