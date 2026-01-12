# Neuron System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         NEURON (Hub)                            │
│                   Central Orchestration Layer                   │
└─────────────────────────────────────────────────────────────────┘
                               │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   knowledge/  │     │    modules/     │     │     .claude/    │
│    (Policy)   │     │   (Registry)    │     │  (Automation)   │
├───────────────┤     ├─────────────────┤     ├─────────────────┤
│ • philosophy  │     │ • hippo/        │     │ • agents/       │
│ • conventions │     │ • pm-arkraft/   │     │ • commands/     │
│ • standards   │     │ • modeling/     │     │ • skills/       │
└───────────────┘     └─────────────────┘     └─────────────────┘
```

## Agent System (Brain Analogy)

```
┌─────────────────────────────────────────────────────────────────┐
│                     NEURON AGENT SYSTEM                         │
│                  "AI Brain for Development"                     │
└─────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐
    │    ADVISOR      │  PFC (Prefrontal Cortex)
    │   "Think First" │  Decision-making, planning
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │    REFACTOR     │  Hippocampus
    │ "Organize Code" │  Memory consolidation, structure
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │    REVIEWER     │  ACC (Anterior Cingulate)
    │  "Check Quality"│  Error detection, conflict monitoring
    └────────┬────────┘
             │
             ▼ [IMPROVE] signal
    ┌─────────────────┐
    │  SELF-IMPROVE   │  Neuroplasticity
    │ "Learn & Adapt" │  System adaptation from patterns
    └─────────────────┘
```

## Advisor-before-AskUser Flow

```
┌──────────────────┐
│ Ambiguous Task   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Call Advisor    │
└────────┬─────────┘
         │
         ▼
    ┌────────────┐
    │ Confidence │
    │   Level?   │
    └─────┬──────┘
          │
    ┌─────┼─────┐
    │     │     │
    ▼     ▼     ▼
 ┌────┐ ┌────┐ ┌────┐
 │High│ │Med │ │Low │
 └──┬─┘ └──┬─┘ └──┬─┘
    │      │      │
    ▼      ▼      ▼
┌──────┐┌──────┐┌──────┐
│Proceed││Proceed││ Ask  │
│ with ││ with ││ User │
│answer││assume││      │
└──────┘└──────┘└──────┘
```

## Routing Table

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER REQUEST                             │
└─────────────────────────────────────────────────────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│     AGENTS      │  │     SKILLS      │  │    COMMANDS     │
│  (Judgment)     │  │  (External API) │  │   (Workflow)    │
├─────────────────┤  ├─────────────────┤  ├─────────────────┤
│ • advisor       │  │ • github-api    │  │ • /pr           │
│ • reviewer      │  │ • jira-api      │  │ • /release      │
│ • refactor      │  │ • notion-api    │  │ • /sync         │
│ • self-improve  │  │ • confluence-api│  │ • /backlog      │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

## PR/Release Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                     DEVELOPMENT CYCLE                           │
└─────────────────────────────────────────────────────────────────┘

  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
  │  Code  │───▶│ Review │───▶│  PR    │───▶│Release │
  │ Change │    │        │    │        │    │        │
  └────────┘    └────────┘    └────────┘    └────────┘
       │             │             │             │
       ▼             ▼             ▼             ▼
  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
  │refactor│    │reviewer│    │  /pr   │    │/release│
  │ agent  │    │ agent  │    │command │    │command │
  └────────┘    └────────┘    └────────┘    └────────┘
                     │
                     ▼ [IMPROVE]
                ┌────────┐
                │  self  │
                │improve │
                └────────┘

Post-merge:
┌────────┐
│ /sync  │  ← Sync main branch, cleanup
└────────┘
```

## Directory Structure

```
neuron/
├── CLAUDE.md              # AI entry point (start here)
├── README.md              # Project overview
│
├── knowledge/             # Policies & philosophy
│   ├── _index.yaml        # Knowledge index
│   ├── philosophy.md      # Core principles (SSOT)
│   ├── module-protocol.md # Module management
│   └── ...
│
├── modules/               # Git submodules
│   ├── _registry.yaml     # Module registry
│   ├── hippo/             # Personal data
│   ├── pm-arkraft/        # Project management
│   └── modeling/          # ML experiments
│
├── docs/
│   ├── diagram.md         # This file
│   ├── releasenotes/      # Version history
│   └── retrospectives/    # Learning records
│
└── .claude/
    ├── agents/            # Thinking agents
    │   ├── advisor.md
    │   ├── reviewer.md
    │   ├── refactor.md
    │   └── self-improve.md
    ├── commands/          # Slash commands
    │   ├── pr.md
    │   ├── release.md
    │   ├── sync.md
    │   └── backlog.md
    ├── procedures/        # Step-by-step guides
    └── skills/            # External API integrations
        ├── github-api/
        ├── jira-api/
        ├── notion-api/
        └── confluence-api/
```
