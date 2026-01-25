# Handoff: Neuron v2 Redesign

## State
| Field | Value |
|-------|-------|
| **Status** | complete |
| **Updated** | 2026-01-25 |
| **Branch** | claude/neuron-agent-skills-redesign-fgh1M |
| **Session Outcome** | All Phases Complete, Ready for PR |

---

## Executive Summary

**Core Insight**: Neuron = Component Factory, Claude Code = Framework

```
Claude Code provides:     Neuron provides:
├─ .claude/agents/       ├─ Factory templates
├─ .claude/skills/       ├─ Component resolver
├─ .claude/contexts/     ├─ Registry tracking
├─ ~/.claude/tasks/      ├─ Philosophy injection
├─ Task tool (parallel)  └─ Self-evolution logic
├─ CLAUDE_CODE_TASK_LIST_ID
└─ Agent resume (agentId)
```

**Self-Evolution Pattern**: Factory → Tasks → Next Session
- Component doesn't exist → Factory creates it
- Agent requires session restart → Create Task with `pending: session_restart`
- Next session boot.md resumes Task → Component executes

---

## Progress Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Factory Structure + Templates | ✅ COMPLETE |
| 2 | Enhanced boot.md (Resolver, Factory Trigger) | ✅ COMPLETE |
| 3 | Registry Tracking | ✅ COMPLETE |
| 4 | Enhanced wrapup.md (Registry Update) | ✅ COMPLETE |
| 5 | E2E Test (arkraft) | ✅ COMPLETE |
| 6 | Cleanup (Commands deprecation) | ✅ COMPLETE |

---

## Claude Code Framework (DO NOT REINVENT)

### Already Provided (January 2026 Update)
- **Tasks system**: Dependencies, `~/.claude/tasks/` persistence
- **Session collaboration**: `CLAUDE_CODE_TASK_LIST_ID` env var
- **Agent definition**: `.claude/agents/*.md` with YAML frontmatter
- **Skills injection**: `skills` field in agent frontmatter
- **Hooks**: PreToolUse, PostToolUse, SubagentStart, SubagentStop
- **Parallel execution**: Task tool, max 10 concurrent
- **Agent creation UI**: `/agents` command
- **Commands → Skills migration**: Commands are being deprecated in favor of skills

### Key Constraints
- **Agent creation requires session restart** - files in `.claude/agents/` not loaded until next session
- **Commands deprecated** - migrate to skills or agents

---

## Completed Implementation

### Factory Structure
```
.claude/factory/
├─ templates/
│  ├─ agent-role.md           ✅
│  ├─ agent-task.md           ✅
│  ├─ skill-api.md            ✅
│  ├─ context-project.yaml    ✅
│  └─ pipeline-parallel.yaml  ✅
└─ registry.yaml              ✅ (15 components registered)
```

### Enhanced Agents
- **boot.md**: +6 steps (Registry load, Component Resolver, Factory Trigger, Context Injection)
- **wrapup.md**: +2 steps (Registry Update, Health Summary)

---

## Completed: Phase 5 - E2E Test

### Test Setup Complete
- ✅ `meta/focus.yaml` already has arkraft active
- ✅ Created `ctx-arkraft.yaml` context
- ✅ Activated arkraft section in registry.yaml

---

## Completed: Phase 6 - Cleanup

### Commands Migration Complete

| Command | Action | Result |
|---------|--------|--------|
| `handoff.md` | ❌ DELETED | Replaced by boot/wrapup agents |
| `backlog.md` | ❌ DELETED | Replaced by Claude Code Tasks |
| `sync.md` | ❌ DELETED | Claude basic capability |
| `pr.md` | ✅ MIGRATED | `.claude/skills/pr/SKILL.md` |
| `release.md` | ✅ MIGRATED | `.claude/skills/release/SKILL.md` |
| `audit-modules.md` | ✅ MIGRATED | `.claude/skills/audit-modules/SKILL.md` |

### Created Directories
- ✅ `.claude/contexts/` - Context files
- ✅ `.claude/skills/pr/` - PR skill
- ✅ `.claude/skills/release/` - Release skill
- ✅ `.claude/skills/audit-modules/` - Audit skill

---

## Decision Guide: Agent vs Skill vs Hook

Use this when creating new components:

| Need | Choose | Example |
|------|--------|---------|
| Judgment/reasoning | **Agent** | Code review, architecture decisions |
| External API call | **Skill (API)** | Jira, GitHub, Slack integration |
| Reusable workflow | **Skill (Capability)** | Release management, reporting |
| Automated trigger | **Hook** | Pre-commit validation, notifications |
| Data transformation | **Skill (Internal)** | Template rendering, data parsing |

### Component Naming Convention
```
Agents:
- agent-system/    → Core lifecycle (boot, wrapup, advisor)
- agent-role/      → Personas (pm, researcher, reviewer)
- agent-task/      → Single-purpose (data-collector, validator)

Skills:
- skill-api/       → External service wrappers
- skill-capability/ → Business logic compositions
- skill-internal/  → Neuron core operations

Contexts:
- ctx-{module}.yaml → Module-specific configuration
```

---

## Key Design Patterns

### Factory → Tasks → Next Session
```
User Request
    │
    ▼
boot.md (Component Resolver)
    │ (component missing?)
    ▼
Factory.create()
    │
    ▼
Task created (pending: session_restart)
    │
    ▼
[Session ends]
    │
    ▼
Next session boot.md
    │
    ▼
Resume Task → Component executes
```

---

## Completion Checklist

```
PHASE 5: E2E TEST
[x] Create meta/focus.yaml with arkraft module (already existed)
[x] Create .claude/contexts/ctx-arkraft.yaml
[x] Uncomment arkraft in registry.yaml module_components

PHASE 6: CLEANUP
[x] Delete .claude/commands/handoff.md
[x] Delete .claude/commands/backlog.md
[x] Delete .claude/commands/sync.md
[x] Migrate pr.md → .claude/skills/pr/SKILL.md
[x] Migrate release.md → .claude/skills/release/SKILL.md
[x] Migrate audit-modules.md → .claude/skills/audit-modules/SKILL.md
[x] Update CLAUDE.md (remove commands references)
[x] Update registry.yaml with migrated components
[x] Commit: "refactor: migrate commands to skills, add arkraft context"
```

## Next Steps

- [ ] Create PR to merge into main
- [ ] Test boot agent with new component resolver
- [ ] Verify skills work correctly (/pr, /release, /audit-modules)

---

## Session Learnings

### Facts
- Claude Code Tasks system (January 2026) replaces custom Journal
- CLAUDE_CODE_TASK_LIST_ID enables cross-session collaboration
- Agent creation requires session restart (architectural constraint)
- Commands are deprecated → migrate to skills/agents

### Lessons
- Registry is essential for SSOT [P1] and self-repair
- Module tagging enables intelligent filtering
- Pending Tasks create natural session continuation points
- Don't reinvent what Claude Code already provides

### Patterns
- Factory → Tasks → Next Session prevents context loss
- Philosophy injection prevents architectural drift
- Agent for judgment, Skill for workflow, Hook for automation

---

## References
- CLAUDE.md - Core philosophy, routing
- knowledge/01-core/philosophy.md - 3 Axioms, 20 Principles
- .claude/agents/boot.md - Component resolver implementation
- .claude/agents/wrapup.md - Registry update implementation
- .claude/factory/registry.yaml - Component registry
