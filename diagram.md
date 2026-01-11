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
