# Neuron v2 Vision

> **Neuron is a Component Factory running on Claude Code framework, a philosophy-driven self-evolving system.**

---

## 1. Identity

```
Neuron ≠ Framework
Neuron = Component Factory

Claude Code = Framework (already provided)
Neuron = Factory (runs on top)
```

---

## 2. No Reinventing the Wheel

| Claude Code Provides | Neuron Adds |
|---------------------|-------------|
| `.claude/agents/*.md` | **Factory** - Template-based generation |
| `.claude/skills/` | **Contexts** - Module-specific state |
| `~/.claude/tasks/` | **Philosophy** - 3 Axioms, 20 Principles |
| Task tool (10 parallel) | **Automation** - lessons → hooks/skills |
| Hooks | **Self-Evolution** - Self-growth |
| Agent resume (agentId) | |

---

## 3. Self-Evolution Pattern

```
system-boot.md (Component detection)
    │ missing?
    ▼
Factory.create() (Template-based generation)
    │
    ▼
Task creation (pending: session_restart)
    │
    ▼
Next session → Component available
```

---

## 4. Component Classification

| Type | Role | Examples |
|------|------|----------|
| **Agent** | Judgment | advisor, reviewer, refactor |
| **Skill** | Execution | api-*, capability-*, /pr |
| **Hook** | Automation | PreToolUse, PostToolUse |

### Decision Criteria

```
Requires judgment/reasoning? → Agent
External API? → Skill (api-*)
Reusable workflow? → Skill (capability-*)
Auto-trigger? → Hook
```

---

## 5. SSOT Principle

| SSOT | Role |
|------|------|
| `CLAUDE.md` | Philosophy, routing, core rules |
| `.claude/contexts/ctx-*.yaml` | Module-specific state and config |
| `.claude/knowledge/learn-lessons.yaml` | Non-automatable learnings (human ref) |

---

## 6. Session Lifecycle

```
Session Start → system-boot.md (MANDATORY)
    ├─ Check pending Tasks
    ├─ Load Focus (ctx-focus.yaml)
    └─ Inject module contexts

[Work]

Session End → system-wrapup.md (MANDATORY)
    ├─ Extract learnings (facts, lessons, patterns)
    ├─ Propose automation (hooks, skills)
    └─ Ensure session continuity (Tasks)
```

---

## 7. Naming Conventions

```
Agents:   .claude/agents/{category}-{name}.md
          - system-*     → Core lifecycle (boot, wrapup, advisor)
          - role-*       → Judgment/review (reviewer, refactor)
          - task-*       → Task-oriented (self-improve)

Skills:   .claude/skills/{category}-{name}/SKILL.md
          - api-*        → External service wrappers
          - capability-* → Reusable workflows
          - workflow-*   → Internal workflows (pr, release)

Contexts: .claude/contexts/ctx-{name}.yaml
          - ctx-identity, ctx-focus, ctx-team (global)
          - ctx-{project} (project-specific)

Knowledge: .claude/knowledge/{prefix}-{name}.md
          - learn-*     → Accumulated learnings
          - guide-*     → Guides
          - protocol-*  → Rules/policies
          - workflow-*  → Processes
          - ref-*       → Reference documents
          - git-*       → Git related
```

---

## 8. Philosophy Foundation

### 3 Axioms

| Axiom | Question | Drives |
|-------|----------|--------|
| Curiosity | "What if?" | Exploration, learning, proactive action |
| Truth | "Is it correct?" | Accuracy, verification, SSOT |
| Beauty | "Is it clean?" | Simplicity, elegance, minimal complexity |

### Core Principles

| # | Principle | Description |
|---|-----------|-------------|
| P1 | SSOT | Single source of truth |
| P3 | Simplicity First | Prefer simple solutions |
| P13 | Autonomous Execution | Execute before asking |
| P15 | Verify Before Done | Verify before completion |
| P17 | Learn from Failure | Learn from mistakes |

---

## 9. Autonomous Execution Principle

```
"Questions are failures"

User → Sets direction
AI   → Responsible for execution

Uncertain? → advisor first (before asking user)
```

---

## 10. v2 Folder Structure

```
neuron/
├─ CLAUDE.md                 # SSOT
├─ .claude/
│  ├─ agents/                # Judgment (auto-discovered)
│  ├─ skills/                # Execution (auto-discovered)
│  ├─ factory/               # Templates for component generation
│  ├─ contexts/              # Session state (focus, module configs)
│  └─ knowledge/             # Reference docs + learnings
└─ modules/                  # Submodules
```

---

## References

- `CLAUDE.md` - Core rules and routing
- `.claude/contexts/ctx-*.yaml` - Module-specific contexts
- `.claude/knowledge/learn-lessons.yaml` - Non-automatable learnings (human ref)
