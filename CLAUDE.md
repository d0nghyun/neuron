# Neuron

Neuron is a **Component Factory** that runs on Claude Code.
Claude Code provides agents, skills, hooks, and task management.
Neuron adds templates, registry, contexts, and guiding principles.

## MANDATORY: Session Flow

```
Request → BOOT → ORCHESTRATE → EXECUTE → WRAPUP
```

### 1. BOOT (session start)

Run `system-boot` agent. Do NOT respond until boot completes.

### 2. ORCHESTRATE (delegation)

For non-trivial requests, delegate to `system-orchestrator`:
- Dynamically discovers agents via `Glob .claude/agents/*.md`
- Matches request to appropriate worker agent
- If no match → delegates to `system-recruiter` to create

### 3. EXECUTE (workers do the work)

Orchestrator delegates to worker layer agents. **You do NOT call workers directly.**

### 4. WRAPUP (session end)

Run `system-wrapup` agent before session ends.

### Layer Responsibilities

| Layer | Agents | Role |
|-------|--------|------|
| **META** | boot, wrapup, self-improve, updater | Session lifecycle |
| **BUSINESS** | orchestrator, advisor, recruiter | Analyze, delegate, create |
| **WORKER** | code-reviewer, code-refactor, ... | Execute domain tasks |

### FORBIDDEN

- ❌ Calling worker agents directly (let orchestrator decide)
- ❌ Creating agents/skills yourself (use recruiter)
- ❌ Skipping boot or wrapup
- ❌ Using opus for tasks haiku can handle

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