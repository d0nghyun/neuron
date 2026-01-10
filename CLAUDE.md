# Neuron - Project Index

## Overview

Neuron is the central hub for personal project management. It orchestrates multiple repositories through git submodules, maintaining core policies and shared knowledge.

## Purpose

- **Hub**: Connects all personal projects as submodules
- **Policy**: Defines conventions, philosophy, and standards
- **Registry**: Manages MCP tools, skills, and configurations
- **Coordination**: Handles cross-project concerns

## Key Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview and usage guide |
| `CLAUDE.md` | This file - AI entry point |
| `knowledge/` | Core policies and detailed philosophy |
| `modules/` | Git submodules (external projects) |
| `.claude/` | Claude Code configuration |

## Philosophy

See [knowledge/philosophy.md](knowledge/philosophy.md) for details.

**Principles**: SSOT, MECE, Simplicity First, Incremental, Modularity, Agile, Test-First, AI-First, Root Cause First, Bounded Creativity

## Conventions

- **Language**: English for all repository content
- **File size**: Max 200 lines per file
- **Documentation**: Structured for AI consumption
- **Commits**: Conventional commits with Co-Authored-By

## Working with This Repository

When adding new functionality:
1. Check if it fits existing modules
2. If new module needed, create separate repo
3. Register as submodule under `modules/`
4. Document in relevant knowledge files

## Current Structure

```
neuron/
├── README.md
├── CLAUDE.md
├── knowledge/
├── modules/
└── .claude/
```
