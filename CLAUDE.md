# Neuron

Neuron is a **Component Factory** that runs on Claude Code.
Claude Code provides agents, skills, hooks, and task management.
Neuron adds templates, registry, memory, and guiding principles.

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
├─ factory/      # Templates + registry.yaml
├─ memory/       # Persistent: identity, focus, lessons
└─ knowledge/    # Reference docs
```

## Component Discovery

**Don't memorize routing tables. Discover what you need.**

1. **Need a capability?** → Search `agents/` and `skills/` for matching component
2. **Found it?** → Read its `.md` file for usage
3. **Not found?** → Factory creates it from templates

Each component is self-describing. Its `.md` file contains:
- When to use it
- How to invoke it
- What it returns

## Session Lifecycle

**Complex tasks** (multi-file changes, commits, external APIs):
- Start with `boot` agent → loads memory, creates tasks
- End with `wrapup` agent → persists learnings

**Simple tasks** (read-only, explanations): Skip boot/wrapup.

## Memory

Persistent context across sessions. Loaded by `boot`, updated by `wrapup`.

| File | Purpose |
|------|---------|
| `memory/identity.yaml` | User info (name, role, org) |
| `memory/focus.yaml` | Current priorities |
| `memory/lessons.yaml` | Learnings from past sessions |

## Conventions

- **Language**: English for all neuron files
- **File size**: Max 200 lines