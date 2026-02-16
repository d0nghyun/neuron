# Rules

Enforcement rules for all components. Read before creating or modifying any component.

## Component Rules

**Agents** (`.claude/agents/{type}-{name}.md`):
- Frontmatter required: `name`, `description`, `tools`, `model`
- Must have Purpose section and Execution Steps
- System agents: `system-*.md` | Domain agents: `{domain}-*.md`

**Skills** (`.claude/skills/{type}-{name}/`):
- Must contain `SKILL.md` with clear steps
- Types per factory README naming conventions

**Teams** (in orchestrator's CLAUDE.md or agent definition):
- Must define orchestrator + members (by agent name reference)
- Must define phases with clear handoff artifacts
- Composition only — no tool how-to (→ Skill) or judgment logic (→ Agent)

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

## MECE Boundary Rules

Each component type has exclusive responsibility. No overlap.

| Component | Contains | Does NOT Contain |
|-----------|----------|------------------|
| Skill | Tool how-to, best practices, gotchas | Judgment, mental model, team structure |
| Agent | Identity, mental model, judgment criteria | Tool usage details, team composition |
| Team (in orchestrator) | Members, phases, routing | Individual agent logic, tool details |

## Dependency Rules

| Level | Allowed Components |
|-------|-------------------|
| neuron (`.claude/`) | Factory agents only (`system-*`, patterns, hooks) |
| module (`modules/{name}/.claude/`) | Worker agents, domain skills, team blueprints |

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
