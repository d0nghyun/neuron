# Factory

Reference pattern library for component generation.

## Before Creating

1. **Check `ref-claude-code.md` first** to avoid reinventing built-in features.
2. **Check existing inventory** — if existing skills/agents cover the need, use them directly (DIRECT mode). Only create when no capability exists.

## Purpose

Factory provides patterns (not templates) for creating new components.
When a required component doesn't exist, reference the appropriate pattern to create it.

## Component Selection Guide

Analyze the request to determine the required component type:

| Need | Component Type | Pattern |
|------|----------------|---------|
| Judgment/reasoning/role identity | Agent | pattern-agent.md |
| Tool usage knowledge (SSOT) | Skill (domain-*) | pattern-skill.md |
| External API call | Skill (api-*) | pattern-skill.md |
| Multi-step process | Skill (workflow-*) | pattern-skill.md |
| Neuron factory operation | Skill (ops-*) | pattern-skill.md |
| Multi-agent collaboration | Team Blueprint | pattern-team.md |
| Automatic trigger | Hook | pattern-hook.md |
| Reference docs/guides/lessons | Knowledge | pattern-knowledge.md |

## Decision Tree

```
Multiple agents collaborating? → Team Blueprint
Judgment/identity needed? → Agent
Tool how-to / best practices? → Skill (domain-*)
External service integration? → Skill (api-*)
Neuron factory operation? → Skill (ops-*)
Multi-step process? → Skill (workflow-*)
Automatic execution? → Hook
Document for reference? → Knowledge
```

## Location Decision

Components can live at **neuron level** or **module level**.

| Question | Location |
|----------|----------|
| Used across multiple modules? | `neuron/.claude/` |
| Specific to one module? | `modules/{module}/.claude/` |
| Will be reused in other projects? | Separate module → submodule |

**When unsure**: Start at module level. Promote to neuron level only when actually needed by multiple modules.

## Usage

1. Identify what's missing
2. Read the appropriate pattern file
3. Decide location (neuron vs module level)
4. Create the component:
   - Agents → `{root}/.claude/agents/{type}-{name}.md` (auto-registers)
   - Skills → `{root}/.claude/skills/{type}-{name}/SKILL.md` (auto-registers)
   - Hooks → `{root}/.claude/settings.json` (manual registration required)
   - Knowledge → `vault/04-Resources/` or `vault/02-Projects/{project}/`

   Where `{root}` = neuron or module path

**Important**: Agents and Skills auto-register when files are created. Only Hooks require manual registration in settings.json.

## Patterns

| Pattern | Location | Creates |
|---------|----------|---------|
| pattern-agent.md | agents/ | Role identity + judgment |
| pattern-skill.md | skills/ | Tool knowledge, API wrappers, workflows |
| pattern-team.md | orchestrator CLAUDE.md | Multi-agent collaboration blueprints |
| pattern-hook.md | settings.json | Automatic triggers |
| pattern-knowledge.md | vault/ | Reference docs, guides |

## Naming Conventions

**Agents**: `{type}-{name}.md`
- `system-*`: Core system agents (recruiter, reviewer)
- `{domain}-*`: Domain worker agents

**Skills**: `{type}-{name}/SKILL.md`
- `domain-*`: Tool/platform knowledge (SSOT, preloaded by agents)
- `api-*`: External API integrations
- `ops-*`: Neuron factory operations (init-module, audit, release)
- `workflow-*`: Multi-step processes
- `capability-*`: Standalone capabilities (no external dependency)

**Team Blueprints**: See `pattern-team.md` for structuring orchestrator agents with team composition

**Knowledge** (in `vault/`):
- Project-specific → `vault/02-Projects/{project}/`
- Reference docs → `vault/04-Resources/`
- Session state → `vault/memory/`

## Quality Grades

Components include `quality_grade` and `quality_checked` in frontmatter.
Grades are set by `ops-factory-sync` during scheduled audits.

| Grade | Criteria |
|-------|----------|
| A | All frontmatter fields, <150 lines, SSOT refs, success criteria |
| B | Required frontmatter, <200 lines, has execution steps |
| C | Missing optional sections or approaching line limit |
| D | Missing required fields, >200 lines, or hardcoded content |
