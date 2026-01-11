# Neuron - AI Entry Point

## Overview

See [README.md](README.md) for project overview and purpose.

## Key Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview and usage guide |
| `CLAUDE.md` | This file - AI entry point |
| `diagram.md` | Visual system architecture |
| `knowledge/` | Core policies and detailed philosophy |
| `modules/` | Git submodules (external projects) |
| `docs/retrospectives/` | Learnings and insights (UNRETROSPECTIVE.md) |
| `.claude/agents/` | Immune system (reviewer, self-improve) |
| `.claude/commands/` | Custom slash commands |
| `.claude/skills/` | Skill definitions |

## Knowledge Files

| File | Purpose |
|------|---------|
| `philosophy.md` | Core principles (SSOT, MECE, etc.) |
| `decision-guide.md` | Where to build (neuron vs submodule, MCP placement) |
| `extension-mechanisms.md` | When to use skills/mcp/agent/command/hook |
| `spec-process.md` | How to develop specs via scenarios |
| `git-workflow.md` | Git conventions and auto-commit policy |
| `self-improve-policy.md` | Self-healing agent constraints |

## Philosophy

See [knowledge/philosophy.md](knowledge/philosophy.md) for details.

**Principles**: SSOT, MECE, Simplicity First, Incremental, Modularity, Agile, Test-First, AI-First, Root Cause First, Bounded Creativity, Constructive Challenge, Front-load Pain, Autonomous Execution, Trust-based Delegation

## Conventions

- **Language**: English for all repository content
- **File size**: Max 200 lines per file
- **Documentation**: Structured for AI consumption
- **Commits**: Conventional commits with Co-Authored-By
- **Auto-commit**: Commit without asking when logical unit complete (see git-workflow.md)
- **Auto-PR**: Run /pr automatically on completion (see git-workflow.md)

## Working with This Repository

When adding new functionality:
1. Check if it fits existing modules
2. If new module needed, create separate repo
3. Register as submodule under `modules/`
4. Document in relevant knowledge files

## Current Structure

See [diagram.md](diagram.md) for directory structure.
