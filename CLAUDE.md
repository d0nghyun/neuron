# Neuron

Neuron is a **Component Factory** that runs on Claude Code.
Claude Code provides agents, skills, hooks, and task management.
Neuron adds templates, registry, contexts, and guiding principles.

## MANDATORY: Session Start

**EVERY session MUST begin by running `system-boot` agent.**

Do NOT respond to user requests until boot completes. No exceptions.

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

### Step 1: Boot (context loading)

`system-boot` agent loads session context:
- Available components (agents, skills, contexts)
- Current focus and active modules
- Pending tasks from previous session

### Step 2: Analyze & Resolve (main agent)

Main agent analyzes request and compares against available:

| Situation | Action |
|-----------|--------|
| All needed exist | → execute → wrapup |
| Some missing | → factory → create → execute → wrapup |

### Step 3: Creation (when missing)

**MANDATORY SEQUENCE - NO EXCEPTIONS:**

1. **Read** `factory/README.md` → select component type
2. **Read** `factory/pattern-{type}.md` → get structure
3. **Follow** naming convention from pattern (api-*, workflow-*, etc.)
4. **Create** at correct location with correct prefix
5. Use immediately or create Task with `pending: session_restart`

⚠️ Skip any step → incorrect component structure

Each component is self-describing. Its `.md` file contains:
- When to use it
- How to invoke it
- What it returns

## Session Lifecycle

Every session follows the same flow:

```
boot → execute → wrapup
```

- **boot**: Load contexts, list available components (haiku, lightweight)
- **execute**: Main agent analyzes request, uses/creates components
- **wrapup**: Extract learnings, propose automation

## Contexts & Knowledge

**Contexts** (`contexts/`): Session state. `ctx-*.yaml` files. Loaded by `system-boot`.

**Knowledge** (`knowledge/`): Reference docs. Prefixed by category. Updated by `system-wrapup`.

## Conventions

- **Language**: English for all neuron files
- **File size**: Max 200 lines