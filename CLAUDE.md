# Neuron

Neuron is a **Component Factory** that runs on Claude Code.
Claude Code provides agents, skills, hooks, and task management.
Neuron adds templates, registry, contexts, and guiding principles.

> **Session Protocol**: Enforced via `.claude/hooks/enforce-claude-md.sh` (UserPromptSubmit hook)
> Every message injects mandatory flow: BOOT → ORCHESTRATE → EXECUTE → WRAPUP

## Principles

| # | Principle | Description |
|---|-----------|-------------|
| 1 | **SSOT** | One source of truth. No duplication. Reference, don't copy. |
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
├─ hooks/        # Session enforcement (enforce-claude-md.sh)
└─ knowledge/    # Reference docs + accumulated learnings
```

## Component Lifecycle

### Boot (context loading)

`system-boot` agent loads session context:
- Available components (agents, skills, contexts)
- Current focus and active modules
- Pending tasks from previous session

### Analyze & Resolve (main agent)

Main agent analyzes request and compares against available:

| Situation | Action |
|-----------|--------|
| All needed exist | → execute → wrapup |
| Some missing | → factory → create → execute → wrapup |

### Creation (when missing)

Each component is self-describing. Its `.md` file contains:
- When to use it
- How to invoke it
- What it returns

## Contexts & Knowledge

**Contexts** (`contexts/`): Session state. `ctx-*.yaml` files. Loaded by `system-boot`.

**Knowledge** (`knowledge/`): Reference docs. Prefixed by category. Updated by `system-wrapup`.

## Conventions

- **Language**: English for all neuron files
- **File size**: Max 200 lines
