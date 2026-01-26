# Neuron System Architecture

Core architecture reference. Used by `system-updater` for validation.

## Layer Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              NEURON SYSTEM                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                      META LAYER (Lifecycle)                           │  │
│  │                                                                       │  │
│  │   boot (opus)          wrapup (sonnet)       self-improve (opus)      │  │
│  │   Session init         Session teardown      Pattern detection        │  │
│  │                                                                       │  │
│  │   updater (haiku)                                                     │  │
│  │   Component validation                                                │  │
│  └───────────────────────────────────┬───────────────────────────────────┘  │
│                                      │                                      │
│                                      ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    BUSINESS LAYER (Delegation)                        │  │
│  │                                                                       │  │
│  │                      ┌──────────────────┐                             │  │
│  │                      │   orchestrator   │                             │  │
│  │                      │     (opus)       │                             │  │
│  │                      │   "CEO - Decide" │                             │  │
│  │                      └────────┬─────────┘                             │  │
│  │                               │                                       │  │
│  │              ┌────────────────┼────────────────┐                      │  │
│  │              │                │                │                      │  │
│  │              ▼                ▼                ▼                      │  │
│  │      ┌────────────┐   ┌────────────┐   ┌────────────┐                │  │
│  │      │  advisor   │   │  recruiter │   │  [delegate │                │  │
│  │      │  (haiku)   │   │  (haiku)   │   │  to worker]│                │  │
│  │      │ "Counselor"│   │  "HR Dept" │   │            │                │  │
│  │      └────────────┘   └────────────┘   └─────┬──────┘                │  │
│  └──────────────────────────────────────────────┼────────────────────────┘  │
│                                                 │                           │
│                                                 ▼                           │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                      WORKER LAYER (Execution)                         │  │
│  │                                                                       │  │
│  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────┐  │  │
│  │   │code-reviewer │  │code-refactor │  │ [new agent]  │  │  ...    │  │  │
│  │   │  (sonnet)    │  │   (opus)     │  │  (varies)    │  │         │  │  │
│  │   └──────────────┘  └──────────────┘  └──────────────┘  └─────────┘  │  │
│  │                                                                       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Session Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SESSION FLOW                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   User Request                                                              │
│        │                                                                    │
│        ▼                                                                    │
│   ┌─────────┐     ┌─────────────┐     ┌─────────────────────────────────┐  │
│   │  BOOT   │────▶│ ORCHESTRATOR│────▶│  Glob .claude/agents/*.md       │  │
│   │ (meta)  │     │ (business)  │     │  (Dynamic Agent Discovery)      │  │
│   └─────────┘     └──────┬──────┘     └─────────────────────────────────┘  │
│                          │                                                  │
│            ┌─────────────┴─────────────┐                                   │
│            │                           │                                   │
│            ▼                           ▼                                   │
│     Agent exists?                Agent missing?                            │
│            │                           │                                   │
│            ▼                           ▼                                   │
│     ┌────────────┐            ┌────────────┐                               │
│     │  Delegate  │            │  Recruiter │                               │
│     │  to Worker │            │  (create)  │                               │
│     └─────┬──────┘            └─────┬──────┘                               │
│           │                         │                                      │
│           └───────────┬─────────────┘                                      │
│                       ▼                                                    │
│                 ┌────────────┐     ┌────────────┐                          │
│                 │   EXECUTE  │────▶│   WRAPUP   │                          │
│                 │  (worker)  │     │   (meta)   │                          │
│                 └────────────┘     └────────────┘                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## SSOT Reference Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SSOT REFERENCE STRUCTURE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   CLAUDE.md (Principles + Mandatory Rules)                                  │
│        │                                                                    │
│        ├──▶ factory/README.md (Component Types, Naming)                    │
│        │         │                                                          │
│        │         └──▶ factory/pattern-*.md (Templates)                     │
│        │                                                                    │
│        ├──▶ agents/README.md (Layer Model, Flow)                           │
│        │                                                                    │
│        └──▶ knowledge/ref-*.md (Domain Knowledge)                          │
│                  ├── ref-system-architecture.md (this file)                │
│                  ├── ref-model-routing.md                                  │
│                  ├── ref-release-notes-format.md                           │
│                  └── ref-learning-classification.md                        │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │  Content Pattern (SSOT):                                             │  │
│   │                                                                      │  │
│   │    ✗ Duplicate info     ──▶    ✓ **See**: ref-{topic}.md            │  │
│   │    ✗ Inline tables      ──▶    ✓ Reference knowledge/ docs          │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Layer Rules

| Layer | Callable By | Can Call |
|-------|-------------|----------|
| META | Main agent | - (lifecycle only) |
| BUSINESS | Main agent, META | WORKER, BUSINESS |
| WORKER | BUSINESS only | - (execute only) |

## Validation Checklist (for updater)

- [ ] All agents have correct `layer` in frontmatter
- [ ] Worker agents are NOT called directly from main agent
- [ ] Boot runs at session start
- [ ] Wrapup runs at session end
- [ ] Orchestrator uses dynamic discovery (Glob), not hardcoded list
- [ ] New agents created via recruiter, not manually
