# Handoff: Neuron v2 Redesign

## State
| Field | Value |
|-------|-------|
| **Status** | in-progress |
| **Updated** | 2026-01-25 |
| **Branch** | claude/neuron-agent-skills-redesign-fgh1M |
| **Session Outcome** | Phase 1-4 Complete, Cleanup Pending |

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
| 5 | E2E Test (arkraft) | ⏳ NEXT |
| 6 | Cleanup (Commands deprecation) | ⏳ PENDING |

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

## Pending: Phase 5 - E2E Test

### Test Scenario: arkraft Module
```
1. Activate arkraft in meta/focus.yaml
2. boot.md detects missing: agent:arkraft-pm, context:ctx-arkraft
3. Factory creates component definitions
4. Tasks created with pending: session_restart
5. Session ends
6. Next session: boot.md loads, components execute
```

### Required for Test
- [ ] Create `meta/focus.yaml` with arkraft active
- [ ] Create `ctx-arkraft.yaml` context
- [ ] Uncomment arkraft section in registry.yaml
- [ ] Run E2E test

---

## Pending: Phase 6 - Cleanup

### Commands Migration Plan

| Command | Action | Target | Reason |
|---------|--------|--------|--------|
| `handoff.md` | ❌ DELETE | - | Replaced by boot/wrapup agents |
| `backlog.md` | ❌ DELETE | - | Replaced by Claude Code Tasks |
| `sync.md` | ❌ DELETE | - | Claude basic capability |
| `pr.md` | ⚠️ MIGRATE | `agent-system/releaser.md` | Needs subagent (reviewer) |
| `release.md` | ⚠️ MIGRATE | `skill-internal/release-mgmt/` | Workflow, not judgment |
| `audit-modules.md` | ⚠️ MIGRATE | `agent-task/module-auditor.md` | Analysis task |

### Migration Steps
```
1. Create new agent/skill files from commands
2. Update registry.yaml with new components
3. Test each migrated component
4. Delete old commands/
5. Update CLAUDE.md routing rules
```

### Directories to Create
- [ ] `.claude/contexts/` - For context files
- [ ] `.claude/pipelines/` - For pipeline definitions (if needed)

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

## Next Session Checklist

```
PHASE 5: E2E TEST
[ ] Create meta/focus.yaml with arkraft module
[ ] Create .claude/contexts/ctx-arkraft.yaml
[ ] Uncomment arkraft in registry.yaml module_components
[ ] Test: boot detects missing components
[ ] Test: factory trigger creates components
[ ] Test: next session loads components

PHASE 6: CLEANUP
[ ] Delete .claude/commands/handoff.md
[ ] Delete .claude/commands/backlog.md
[ ] Delete .claude/commands/sync.md
[ ] Migrate pr.md → agent-system/releaser.md
[ ] Migrate release.md → skill-internal/release-mgmt/
[ ] Migrate audit-modules.md → agent-task/module-auditor.md
[ ] Update CLAUDE.md (remove commands references)
[ ] Update registry.yaml with migrated components
[ ] Commit: "refactor: migrate commands to agents/skills"
```

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
