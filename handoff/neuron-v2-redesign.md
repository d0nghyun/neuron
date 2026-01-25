# Handoff: Neuron v2 Redesign

## State
| Field | Value |
|-------|-------|
| **Status** | in-progress |
| **Updated** | 2026-01-25 |
| **Branch** | claude/neuron-agent-skills-redesign-fgh1M |
| **Session Outcome** | Architectural Design Complete |

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

## Claude Code Framework (DO NOT REINVENT)

### Already Provided (January 2026 Update)
- **Tasks system**: Dependencies, `~/.claude/tasks/` persistence
- **Session collaboration**: `CLAUDE_CODE_TASK_LIST_ID` env var
- **Agent definition**: `.claude/agents/*.md` with YAML frontmatter
- **Skills injection**: `skills` field in agent frontmatter
- **Hooks**: PreToolUse, PostToolUse, SubagentStart, SubagentStop
- **Parallel execution**: Task tool, max 10 concurrent
- **Agent creation UI**: `/agents` command

### Key Constraint
- **Agent creation requires session restart** - files created in `.claude/agents/` are not loaded until next session

---

## Neuron v2 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      PHILOSOPHY LAYER                           │
│              3 Axioms, 20 Principles (Immutable)                │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      COMPONENT FACTORY                          │
│  .claude/factory/                                               │
│  ├─ templates/          # Agent, skill, context, pipeline       │
│  └─ registry.yaml       # Created components tracking           │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CLAUDE CODE FRAMEWORK                         │
│  .claude/agents/   ← Factory outputs here                       │
│  .claude/skills/   ← Factory outputs here                       │
│  .claude/contexts/ ← Factory outputs here                       │
│  ~/.claude/tasks/  ← Tasks for cross-session coordination       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Implementation Plan

### Phase 1: Factory Structure + Templates [IMMEDIATE]
```
.claude/factory/
├─ templates/
│  ├─ agent-role.md           # Role agents (pm, researcher)
│  ├─ agent-task.md           # Task agents (data-collector)
│  ├─ skill-api.md            # API skill wrapper
│  ├─ context-project.yaml    # Project context
│  └─ pipeline-parallel.yaml  # Parallel pipeline
└─ registry.yaml              # Component registry
```

### Phase 2: Enhanced boot.md
- Component Resolver: detect missing components
- Factory Trigger: create missing components + Tasks
- Context Injection: load `.claude/contexts/ctx-*.yaml`

### Phase 3: Registry Tracking
- boot.md: load registry, track component health
- wrapup.md: update registry with new components

### Phase 4: Enhanced wrapup.md
- Registry update logic
- Component health tracking
- Lesson extraction with module tagging

### Phase 5: Test with arkraft Scenario
- End-to-end test: missing agent → factory → task → next session → execute

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

### Component Resolver Logic
```
1. Load registry.yaml
2. For each active module:
   - Check required agents/skills exist
   - Collect missing components
3. Return missing list to Factory Trigger
```

### Factory Trigger Logic
```
1. For each missing component:
   - Load appropriate template
   - Populate with parameters
   - Inject philosophy preamble
   - Write to .claude/{agents|skills|contexts}/
   - Create Task with dependencies
   - Update registry.yaml
```

---

## Files to Create

| Phase | File | Description |
|-------|------|-------------|
| 1 | `.claude/factory/templates/agent-role.md` | Role agent template |
| 1 | `.claude/factory/templates/agent-task.md` | Task agent template |
| 1 | `.claude/factory/templates/skill-api.md` | API skill template |
| 1 | `.claude/factory/templates/context-project.yaml` | Project context template |
| 1 | `.claude/factory/templates/pipeline-parallel.yaml` | Pipeline template |
| 1 | `.claude/factory/registry.yaml` | Initial empty registry |
| 2 | `.claude/agents/boot.md` | ENHANCE with resolver |
| 4 | `.claude/agents/wrapup.md` | ENHANCE with registry update |

---

## Session Learnings

### Facts
- Claude Code Tasks system (January 2026) replaces need for custom Journal
- CLAUDE_CODE_TASK_LIST_ID enables cross-session collaboration
- Agent creation requires session restart (architectural constraint)

### Lessons
- Registry is essential for SSOT [P1] and self-repair
- Module tagging enables intelligent filtering
- Pending Tasks create natural session continuation points

### Patterns
- Factory → Tasks → Next Session prevents context loss
- Philosophy injection prevents architectural drift

---

## Next Session Checklist

```
[ ] Read this handoff
[ ] Check .claude/factory/ exists (if not, create)
[ ] Start Phase 1: Create templates
[ ] Create registry.yaml
[ ] Commit: "feat: initial factory structure"
[ ] Proceed to Phase 2 if time permits
```

---

## References
- CLAUDE.md - Core philosophy, routing
- knowledge/01-core/philosophy.md - 3 Axioms, 20 Principles
- .claude/agents/boot.md - Current implementation
- .claude/agents/wrapup.md - Current implementation
