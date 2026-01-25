# Factory

Reference pattern library for component generation.

## Purpose

Factory provides patterns (not templates) for creating new components.
When a required component doesn't exist, reference the appropriate pattern to create it.

## Component Selection Guide

Analyze the request to determine the required component type:

| Need | Component Type | Pattern |
|------|----------------|---------|
| Judgment/reasoning/review | Agent | pattern-agent.md |
| External API call | Skill (api-*) | pattern-skill.md |
| Reusable workflow | Skill (workflow-*) | pattern-skill.md |
| Project-specific config | Context | pattern-context.yaml |
| Automatic trigger | Hook | pattern-hook.md |

## Decision Tree

```
External service integration? → Skill (api-*)
Judgment needed? → Agent
Automatic execution? → Hook
Project settings? → Context
Reusable multi-step process? → Skill (workflow-*)
```

## Usage

1. Identify what's missing (via boot or manual search)
2. Read the appropriate pattern file
3. Create the component at the correct location:
   - Agents → `.claude/agents/{type}-{name}.md`
   - Skills → `.claude/skills/{type}-{name}.md`
   - Contexts → `.claude/contexts/ctx-{name}.yaml`
   - Hooks → `.claude/settings.json` (hooks section)
4. Create Task with `pending: session_restart` for handoff

## Patterns

| Pattern | Location | Creates |
|---------|----------|---------|
| pattern-agent.md | agents/ | Judgment components |
| pattern-skill.md | skills/ | API wrappers, workflows |
| pattern-context.yaml | contexts/ | Project configs |
| pattern-hook.md | settings.json | Automatic triggers |

## Naming Conventions

**Agents**: `{type}-{name}.md`
- `system-*`: Core system agents (boot, wrapup)
- `feature-dev-*`: Feature development agents
- `code-review-*`: Code review agents
- Other domain-specific prefixes as needed

**Skills**: `{type}-{name}.md`
- `api-*`: External API integrations
- `workflow-*`: Multi-step processes
- `capability-*`: Domain capabilities

**Contexts**: `ctx-{name}.yaml`
- `ctx-focus.yaml`: Current priorities (always loaded)
- `ctx-{module}.yaml`: Module-specific configs
