# Neuron System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         NEURON (Hub)                            │
│                     Component Factory Layer                     │
│         "Claude Code = Framework, Neuron = Factory"             │
└─────────────────────────────────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLAUDE.md   │    │    modules/     │    │     .claude/    │
│   (SSOT)      │    │   (Submodules)  │    │  (Components)   │
├───────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Philosophy  │    │ • arkraft/      │    │ • agents/       │
│ • Principles  │    │ • modeling/     │    │ • skills/       │
│ • Routing     │    │                 │    │ • factory/      │
│               │    │                 │    │ • memory/       │
│               │    │                 │    │ • knowledge/    │
└───────────────┘    └─────────────────┘    └─────────────────┘
```

## Self-Evolution Pattern

```
┌──────────────────────────────────────────────────────────────────┐
│                    SELF-EVOLUTION FLOW                           │
└──────────────────────────────────────────────────────────────────┘

  [Session Start]
        │
        ▼
┌───────────────┐
│   boot.md     │  Component Resolver
│  (registry)   │
└───────┬───────┘
        │
        ▼
   ┌────────────┐
   │  Missing   │
   │ Component? │
   └─────┬──────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  [YES]      [NO]
    │         │
    ▼         ▼
┌────────┐  ┌────────┐
│Factory │  │ Ready  │
│create()│  │ :true  │
└────┬───┘  └────────┘
     │
     ▼
┌────────────────┐
│ Task created   │
│ (session_      │
│  restart)      │
└────────┬───────┘
         │
         ▼
   [Next Session]
         │
         ▼
┌────────────────┐
│ Component      │
│ Available      │
└────────────────┘
```

## Agent System

```
┌─────────────────────────────────────────────────────────────────┐
│                     NEURON AGENT SYSTEM                         │
│                  "Judgment Components"                          │
└─────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐
    │      BOOT       │  Session Start (MANDATORY)
    │   "Initialize"  │  Load registry, focus, lessons
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │    ADVISOR      │  Pre-decision consultation
    │   "Think First" │  Uncertainty? → Call advisor
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │    REVIEWER     │  Before PR
    │  "Check Quality"│  Code quality, security
    └────────┬────────┘
             │
             ▼ [IMPROVE] signal
    ┌─────────────────┐
    │  SELF-IMPROVE   │  Pattern-based improvement
    │ "Learn & Adapt" │  System evolution
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │     WRAPUP      │  Session End (MANDATORY)
    │ "Persist Learn" │  Extract lessons, update registry
    └─────────────────┘
```

## Component Routing

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER REQUEST                             │
└─────────────────────────────────────────────────────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│     AGENTS      │  │     SKILLS      │  │      HOOKS      │
│  (Judgment)     │  │  (Execution)    │  │  (Automation)   │
├─────────────────┤  ├─────────────────┤  ├─────────────────┤
│ • advisor       │  │ • api-github    │  │ • PreToolUse    │
│ • reviewer      │  │ • api-jira      │  │ • PostToolUse   │
│ • refactor      │  │ • api-notion    │  │ • SubagentStart │
│ • self-improve  │  │ • api-slack     │  │                 │
│                 │  │ • /pr           │  │                 │
│                 │  │ • /release      │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

## Directory Structure (v2)

```
neuron/
├── CLAUDE.md              # AI entry point (SSOT)
├── README.md
│
├── modules/               # Git submodules
│   ├── arkraft/
│   └── modeling/
│
├── docs/
│   ├── diagram.md         # This file
│   └── releasenotes/
│
└── .claude/
    ├── agents/            # Judgment (6)
    │   ├── advisor.md
    │   ├── boot.md
    │   ├── wrapup.md
    │   ├── reviewer.md
    │   ├── refactor.md
    │   └── self-improve.md
    │
    ├── skills/            # Execution (10)
    │   ├── api-*/         # External APIs
    │   ├── capability-*/  # Workflows
    │   └── */             # Others (pr, release)
    │
    ├── factory/           # Component generation
    │   ├── templates/
    │   └── registry.yaml  # Component SSOT
    │
    ├── memory/            # Long-term state
    │   ├── identity.yaml
    │   ├── focus.yaml
    │   ├── team.yaml
    │   └── lessons.yaml
    │
    ├── knowledge/         # Reference docs
    │   └── *.md
    │
    └── contexts/          # Module configs
        └── ctx-*.yaml
```

## Decision Guide

```
┌────────────────────────────────────────────────────────────────┐
│                   WHAT COMPONENT TO USE?                        │
└────────────────────────────────────────────────────────────────┘

  Need judgment/reasoning?
         │
    ┌────┴────┐
    │         │
   YES        NO
    │         │
    ▼         ▼
┌────────┐  External API needed?
│ AGENT  │       │
└────────┘  ┌────┴────┐
            │         │
           YES        NO
            │         │
            ▼         ▼
      ┌──────────┐  Automated trigger?
      │SKILL     │       │
      │(api-*)   │  ┌────┴────┐
      └──────────┘  │         │
                   YES        NO
                    │         │
                    ▼         ▼
              ┌────────┐  ┌────────────┐
              │ HOOK   │  │ SKILL      │
              │        │  │(capability)│
              └────────┘  └────────────┘
```
