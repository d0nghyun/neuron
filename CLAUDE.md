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
├─ factory/      # Templates + registry.yaml
├─ contexts/     # Session state: identity, focus, project configs
└─ knowledge/    # Reference docs + accumulated learnings
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
- Start with `system-boot` agent → loads contexts, creates tasks
- End with `system-wrapup` agent → persists learnings

**Simple tasks** (read-only, explanations): Skip boot/wrapup.

## Contexts & Knowledge

**Contexts** (`contexts/`): Session state. Loaded by `system-boot`.

| File | Purpose |
|------|---------|
| `ctx-identity.yaml` | User info (name, role, org) |
| `ctx-focus.yaml` | Current priorities |
| `ctx-team.yaml` | Team information |
| `ctx-{project}.yaml` | Project-specific configs |

**Knowledge** (`knowledge/`): Reference docs + learnings. Updated by `system-wrapup`.

| Prefix | Purpose |
|--------|---------|
| `learn-` | Accumulated learnings (lessons, patterns) |
| `guide-` | How-to guides |
| `protocol-` | Rules and policies |
| `workflow-` | Process documentation |
| `ref-` | Reference information |
| `git-` | Git-related docs |

## Conventions

- **Language**: English for all neuron files
- **File size**: Max 200 lines