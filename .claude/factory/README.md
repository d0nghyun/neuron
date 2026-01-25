# Factory

Reference pattern library for component generation.

## Before Creating

**Check `ref-claude-code.md` first** to avoid reinventing built-in features.

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
| Reference docs/guides/lessons | Knowledge | pattern-knowledge.md |

## Decision Tree

```
External service integration? → Skill (api-*)
Judgment needed? → Agent
Automatic execution? → Hook
Project settings? → Context
Reusable multi-step process? → Skill (workflow-*)
Document for reference? → Knowledge
```

## Location Decision

Components can live at **neuron level** or **module level**.

| Question | Location |
|----------|----------|
| Used across multiple modules? | `neuron/.claude/` |
| Specific to one module? | `modules/{module}/.claude/` |
| Will be reused in other projects? | Separate module → submodule |

**Examples**:
- `api-google-calendar` → neuron level (any module can use)
- `workflow-daily-standup` → calendar module (module-specific workflow)
- `code-review` for React project → that project's `.claude/`

**When unsure**: Start at module level. Promote to neuron level only when actually needed by multiple modules.

## Usage

1. Identify what's missing (via boot or manual search)
2. Read the appropriate pattern file
3. Decide location (neuron vs module level)
4. Create the component:
   - Agents → `{root}/.claude/agents/{type}-{name}.md` (auto-registers)
   - Skills → `{root}/.claude/skills/{type}-{name}/SKILL.md` (auto-registers)
   - Contexts → `{root}/.claude/contexts/ctx-{name}.yaml` (loaded by boot)
   - Hooks → `{root}/.claude/settings.json` (manual registration required)
   - Knowledge → `{root}/.claude/knowledge/{prefix}-{name}.md` (reference only)

   Where `{root}` = neuron or module path

**Important**: Agents and Skills auto-register when files are created. Only Hooks require manual registration in settings.json.

5. Create Task with `pending: session_restart` for handoff

## Patterns

| Pattern | Location | Creates |
|---------|----------|---------|
| pattern-agent.md | agents/ | Judgment components |
| pattern-skill.md | skills/ | API wrappers, workflows |
| pattern-context.yaml | contexts/ | Project configs |
| pattern-hook.md | settings.json | Automatic triggers |
| pattern-knowledge.md | knowledge/ | Reference docs, guides, lessons |

## Naming Conventions

**Agents**: `{type}-{name}.md`
- `system-*`: Core system agents (boot, wrapup, advisor, self-improve)
- `feature-dev-*`: Feature development agents
- `code-*`: Code-related agents (code-review-*, code-refactor, etc.)

**Skills**: `{type}-{name}.md`
- `api-*`: External API integrations
- `workflow-*`: Multi-step processes
- `capability-*`: Domain capabilities

**Contexts**: `ctx-{name}.yaml`
- `ctx-focus.yaml`: Current priorities (always loaded)
- `ctx-{module}.yaml`: Module-specific configs

**Knowledge**: `{prefix}-{name}.md`
- `ref-*`: Reference documents, specs
- `guide-*`: Decision guides, how-tos
- `protocol-*`: Procedures, standards
- `workflow-*`: Process specifications
- `learn-*`: Accumulated lessons (YAML)
