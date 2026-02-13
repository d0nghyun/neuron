# Neuron System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                       NEURON (Factory)                          │
│              "Claude Code = Framework, Neuron = Patterns"       │
└─────────────────────────────────────────────────────────────────┘
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
       ▼                      ▼                      ▼
┌───────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLAUDE.md   │    │    modules/     │    │     .claude/    │
│   (Router)    │    │   (Submodules)  │    │  (Components)   │
├───────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Principles  │    │ • arkraft/      │    │ • agents/       │
│ • Structure   │    │ • (others)      │    │ • skills/       │
│ • Approach    │    │                 │    │ • factory/      │
│               │    │ Each has own    │    │ • hooks/        │
│               │    │ .claude/        │    │ • knowledge/    │
└───────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │     vault/      │
                     │   (Private)     │
                     ├─────────────────┤
                     │ • AGENTS.md     │
                     │ • SOUL.md       │
                     │ • USER.md       │
                     │ • memory/       │
                     │ • 02-Projects/  │
                     └─────────────────┘
```

## Intent-Based Flow

```
┌──────────────┐
│ User Request │
└──────┬───────┘
       │
       ▼
┌──────────────┐     enforce-claude-md.sh injects
│Intent Assess │     system-reminder on every prompt
│              │
│ trivial?     │──YES──▶ DIRECT (just do it)
│ moderate?    │──YES──▶ DELEGATE (subagent)
│ complex?     │──YES──▶ COLLABORATE (agent teams)
└──────────────┘
```

## Factory Agents (Neuron Level Only)

```
┌─────────────────────────────────────────────────┐
│              NEURON AGENTS                       │
│         "Factory management, not workers"        │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────┐   ┌─────────────────┐     │
│  │    Recruiter     │   │    Reviewer      │    │
│  │  "Build"         │   │  "Verify"        │    │
│  │                  │   │                  │    │
│  │  factory/ →      │   │  Checks:         │    │
│  │  create component│   │  • structure     │    │
│  │  at target path  │   │  • SSOT          │    │
│  └─────────────────┘   │  • naming        │    │
│                         │  • file size     │    │
│                         └─────────────────┘    │
│                                                 │
│  Workers live in their modules, not here.       │
└─────────────────────────────────────────────────┘
```

## Component Creation Flow

```
Module needs a component
       │
       ▼
┌──────────────┐
│  Component   │
│  exists?     │
└──────┬───────┘
  ┌────┴────┐
  │         │
 YES        NO
  │         │
  ▼         ▼
[Use it]  ┌──────────────┐
          │  Recruiter   │
          │              │
          │  1. Read factory/pattern-*.md
          │  2. Check naming rules
          │  3. Create at module/.claude/
          │  4. Report result
          └──────┬───────┘
                 │
                 ▼
          ┌──────────────┐
          │  Reviewer    │
          │  (optional)  │
          │              │
          │  Verify quality
          └──────────────┘
```

## What Goes Where

```
┌────────────────────────────────────────────────────────────────┐
│                    WHAT COMPONENT TO USE?                       │
└────────────────────────────────────────────────────────────────┘

  Judgment/reasoning needed?
       │
  ┌────┴────┐
 YES        NO
  │         │
  ▼         ▼
AGENT    External API?
            │
       ┌────┴────┐
      YES        NO
       │         │
       ▼         ▼
  SKILL       Automated trigger?
  (api-*)         │
             ┌────┴────┐
            YES        NO
             │         │
             ▼         ▼
           HOOK     SKILL
                    (workflow-*)
```

## Directory Structure

```
neuron/
├── CLAUDE.md              # Router: principles + approach
├── ARCHITECTURE.md        # System map: what lives where
│
├── modules/               # Git submodules (each has own .claude/)
│   └── arkraft/
│
├── vault/                 # Private (separate git repo, gitignored)
│   ├── AGENTS.md, SOUL.md, USER.md
│   ├── memory/
│   └── 02-Projects/
│
├── docs/
│   ├── diagram.md         # This file
│   └── releasenotes/
│
└── .claude/
    ├── agents/            # Factory management (2)
    │   ├── system-recruiter.md
    │   └── system-reviewer.md
    │
    ├── skills/            # Execution workflows
    │   ├── api-*/         # External API integrations
    │   ├── workflow-*/    # Multi-step processes
    │   └── capability-*/  # Domain capabilities
    │
    ├── factory/           # Component patterns
    │   ├── pattern-agent.md
    │   ├── pattern-skill.md
    │   ├── pattern-hook.md
    │   ├── pattern-knowledge.md
    │   └── ref-claude-code.md
    │
    ├── hooks/             # Event triggers
    │   └── enforce-claude-md.sh
    │
    └── knowledge/         # System guides
        └── guide-*.md
```
