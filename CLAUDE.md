# Neuron

Component factory for Claude Code.
Adds templates, registry, and guiding principles.
Private data lives in `vault/` (see ARCHITECTURE.md).

## Principles

| # | Principle | Description |
|---|-----------|-------------|
| 1 | **SSOT** | One source of truth. No duplication. |
| 2 | **Simplicity** | Simple over complex. Build what's needed now. |
| 3 | **Modularity** | Independent, replaceable components. |
| 4 | **Verify** | Prove it works. Don't assume. |
| 5 | **Autonomy** | Act first. Ask only when truly blocked. |

## Structure

```
.claude/
├─ agents/       # Judgment components (self-describing)
├─ skills/       # Execution components (self-describing)
├─ factory/      # Templates for component creation
├─ hooks/        # Event triggers
vault/            # Private: identity, projects, memory (gitignored)
```

## Intent-Based Approach

No rigid protocol. Assess each request:

| Complexity | Approach | When |
|------------|----------|------|
| Trivial | Direct | Conversation, small edits, lookups |
| Moderate | Delegate | Focused work → subagent |
| Complex | Collaborate | Quality-critical → Worker + Reviewer loop |

Load context on demand. Pull what you need when you need it.

## Where to Look

| Need | Read |
|------|------|
| Enforcement rules | `RULES.md` |
| System map & flows | `ARCHITECTURE.md` |
| New component | `.claude/factory/README.md` |
| Module activation | `ops-init-module` skill |
| Component audit | `system-reviewer` agent |
| Scheduled maintenance | `CRON.md` |

## Conventions

- **Language**: English for all neuron files
- **File size**: Max 200 lines
