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
│ • philosophy  │     │ • project-a/    │     │ • agents/       │
│ • conventions │     │ • project-b/    │     │ • commands/     │
│ • standards   │     │ • project-c/    │     │ • skills/       │
└───────────────┘     └─────────────────┘     └─────────────────┘
```

## Core Roles

```
                    ┌─────────────┐
                    │   Neuron    │
                    │    Hub      │
                    └──────┬──────┘
                           │
     ┌─────────────────────┼─────────────────────┐
     │                     │                     │
     ▼                     ▼                     ▼
┌─────────┐          ┌──────────┐         ┌─────────────┐
│ Policy  │          │ Registry │         │Coordination │
└─────────┘          └──────────┘         └─────────────┘
```

| Role | Description |
|------|-------------|
| Hub | Connects all projects as submodules |
| Policy | Defines conventions, philosophy, standards |
| Registry | Manages MCP tools, skills, configs |
| Coordination | Handles cross-project concerns |

## Immune System

```
┌─────────────────────────────────────────────────────────────────┐
│                      Immune System                              │
│  ┌──────────────────┐              ┌──────────────────────┐    │
│  │    reviewer      │──────────────│    self-improve      │    │
│  │  (Code Review)   │   feedback   │  (System Evolution)  │    │
│  └──────────────────┘              └──────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

- **reviewer**: Validates code quality, updates release notes
- **self-improve**: Analyzes patterns, proposes system improvements

## Data Flow

```
[New Code] ──▶ [reviewer] ──▶ [PR Created]
                   │
                   ▼ (pattern detected)
            [self-improve]
                   │
                   ▼
           [Policy Update]
                   │
                   ▼
          [knowledge/ updated]
```

## Directory Structure

```
neuron/
├── README.md          # Project overview
├── CLAUDE.md          # AI entry point
├── diagram.md         # This file
├── knowledge/         # Policies & philosophy
├── modules/           # Git submodules
└── .claude/
    ├── agents/        # Immune system
    ├── commands/      # Slash commands
    └── skills/        # Skills
```
