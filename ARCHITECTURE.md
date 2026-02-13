# Architecture

Neuron = public component factory + private knowledge vault

## Repositories

| Repo | Path | Visibility | Purpose |
|------|------|------------|---------|
| neuron | `.` | Public | Agents, skills, hooks, factory |
| vault | `vault/` | Private | Identity, projects, memory |

## Setup

```bash
git clone <your-vault-repo> vault/
```

## What Lives Where

### Neuron (`.claude/`)
- `agents/` — Judgment components (system-level only)
- `skills/` — Execution components (workflows, APIs)
- `factory/` — Patterns for component creation
- `hooks/` — Event triggers and enforcement scripts

### Vault (`vault/`)
- `01-Inbox/` — Capture area
- `02-Projects/` — Project configs, domain knowledge
- `03-Areas/` — Ongoing responsibilities (personal, team)
- `04-Resources/` — Reference materials, neuron refs
- `05-Archive/` — Completed/inactive items
- `memory/` — Session state, daily notes

## Component Relationships

```
factory/         creates →  agents/, skills/
hooks/           enforces →  RULES.md compliance
system-reviewer  audits  →  all components
system-recruiter creates →  new components via factory patterns
```

Factory provides patterns. Recruiter uses them to generate components.
Hooks enforce rules automatically. Reviewer audits on demand.

## Execute Modes

| Mode | Pattern | Use When |
|------|---------|----------|
| DIRECT | Handle inline | Trivial: conversation, small edits |
| DELEGATE | Single subagent → result | Moderate: focused independent task |
| COLLABORATE | Worker → Reviewer → Fix loop | Complex: quality-critical, multi-file |

### Collaborate Flow

```
1. Orchestrator spawns worker agent (e.g. feature-dev)
2. Worker produces output
3. Orchestrator spawns reviewer agent (e.g. code-reviewer)
4. Reviewer reports issues (no direct fixes)
5. If issues found → worker fixes → re-review (step 3)
6. Clean review → done
```

Reviewer only reports. Orchestrator decides whether to fix or skip.

## Orchestration Pipeline

When complex intents arrive, components collaborate in a structured flow:

```
Intent arrives
  ├─ Capability exists? → Form team → Execute
  └─ Capability missing?
       └─ Recruiter: create (factory) OR activate (ops-init-module)
            └─ Form team → Execute
                 └─ Reviewer: audit output
                      └─ Memory: ops-daily-memo
                           └─ Vault: ops-vault-recap stores
```

### Flow Details

| Stage | Actor | Action |
|-------|-------|--------|
| Detect gap | Main agent | Determines needed capability is missing |
| Recruit | system-recruiter | Checks `modules/` first (activate via ops-init-module), else creates via factory |
| Team | Task tool | Spawns subagents in parallel for independent work |
| Execute | Worker agents | Produce output (code, config, analysis) |
| Review | system-reviewer | Audits output quality and pattern compliance |
| Record | ops-daily-memo | Captures session decisions and follow-ups |
| Store | ops-vault-recap | Promotes memory to proper vault locations |

### When to Trigger Recruiter

- No agent/skill exists for the intent
- Module exists in `modules/` but isn't activated
- Existing component is outdated or misaligned with need

### Team Assembly

Workers run as Task tool subagents. Independent tasks run in parallel.
Reviewer runs sequentially after workers complete.

## Module Lifecycle

```
1. ops-init-module        → activates module skills/agents via symlink
2. Session work           → module components available in .claude/
3. cleanup-modules.sh     → removes symlinks on SessionEnd
```

Modules live in `modules/{name}/`. Each has its own `.claude/` for domain-specific components.
Neuron-level components are for cross-module concerns only.

## Hook Flow

| Event | Hook | Purpose |
|-------|------|---------|
| UserPromptSubmit | `enforce-claude-md.sh` | Intent-first reminder on every prompt |
| SessionStart | env loader | Loads `.env.local` into session |
| SessionEnd | `cleanup-modules.sh` | Removes module symlinks |
| PreToolUse (Write/Edit) | `pre-validate.sh` | Pre-write validation |
| PreToolUse (Write/Edit) | `validate-vault.sh` | Vault structure enforcement (block) |
| PreToolUse (Write/Edit) | `validate-component.sh` | Agent/skill frontmatter enforcement (block) |
| PreToolUse (Write) | `validate-linecount.sh` | 200-line .md warning (suggest) |
| PreToolUse (AskUserQuestion) | `telegram-notify.sh` | Notify on questions |
| PermissionRequest | `telegram-notify.sh` | Notify on permission requests |
| Stop | `telegram-notify.sh` | Notify on stop |

## Session Flow

1. **Intent**: Assess what user wants and how complex it is
2. **Context**: Load from vault/ as needed (not everything upfront)
3. **Execute**: Direct, delegate (subagent), or collaborate (worker+reviewer)
4. **Review Loop**: Reviewer checks output → worker fixes issues → repeat until clean
5. **Record**: Write to vault/memory/ when session has significant work

## File Map

| Need | Read |
|------|------|
| Enforcement rules | `RULES.md` |
| System overview | `ARCHITECTURE.md` (this file) |
| Principles & conventions | `CLAUDE.md` |
| Component creation | `.claude/factory/README.md` |
| Agent pattern | `.claude/factory/pattern-agent.md` |
| Skill pattern | `.claude/factory/pattern-skill.md` |
| Hook configuration | `.claude/settings.json` |
| Project knowledge | `vault/02-Projects/{project}/` |
| Session memory | `vault/memory/` |
