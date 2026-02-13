# Rules

Enforcement rules for all components. Read before creating or modifying any component.

## Component Rules

**Agents** (`.claude/agents/{type}-{name}.md`):
- Frontmatter required: `name`, `description`, `tools`, `model`
- Must have Purpose section and Execution Steps
- System agents: `system-*.md` | Domain agents: `{domain}-*.md`

**Skills** (`.claude/skills/{type}-{name}/`):
- Must contain `SKILL.md` with clear steps
- API skills: `api-*` | Workflow skills: `workflow-*` | Capability skills: `capability-*`

**Hooks** (`.claude/hooks/`):
- Must be registered in `.claude/settings.json`
- Script in `hooks/`, entry in settings

## File Rules

- Max **200 lines** per file
- **English** for all neuron files
- Root `.md` files = category representatives (detail goes in subdirectories)

## Naming Rules

See `.claude/factory/README.md` § Naming Conventions for full patterns.

Do not duplicate naming rules here. Factory README is the single source.

## Dependency Rules

| Level | Allowed Components |
|-------|-------------------|
| neuron (`.claude/`) | Factory agents only (`system-*`, patterns, hooks) |
| module (`modules/{name}/.claude/`) | Worker agents, domain skills |

Start at module level. Promote to neuron only when used by multiple modules.

## Doc Rules

| File | Role |
|------|------|
| Root `.md` | Category entry point (e.g., `RULES.md`, `ARCHITECTURE.md`) |
| `docs/` subdirs | Detailed docs (e.g., `docs/releasenotes/`) |
| `vault/` | Private knowledge, project configs, memory |

## Vault Rules

- Depth limit: **3 levels** max
- Naming: `##-name/###-name` pattern (e.g., `02-Projects/021-arkraft/`)
- Project-specific → `vault/02-Projects/{project}/`
- Reference docs → `vault/04-Resources/`
- Session state → `vault/memory/`

## Enforcement

- `enforce-claude-md.sh` hook: reminds intent-first approach on every prompt
- `system-reviewer` agent: audits compliance on demand
- Hooks enforce automatically; reviewer reports only (never auto-fixes)
