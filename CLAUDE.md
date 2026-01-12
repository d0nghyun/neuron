# Neuron - AI Entry Point

## Overview

See [README.md](README.md) for project overview and purpose.
See [diagram.md](diagram.md) for visual structure.

## Navigation

| Location | Purpose |
|----------|---------|
| `knowledge/` | Core policies (philosophy, conventions, guides) |
| `modules/` | Git submodules (external projects) |
| `modules/_registry.yaml` | Module metadata registry |
| `docs/retrospectives/` | Learnings and insights |
| `.claude/agents/` | Immune system (reviewer, self-improve) |
| `.claude/commands/` | Custom slash commands |
| `.claude/skills/` | Skill definitions |

## Knowledge Files

| File | Purpose |
|------|---------|
| `ai-axioms.md` | Foundational axioms (Curiosity, Truth, Beauty) |
| `philosophy.md` | Core principles (SSOT, MECE, etc.) |
| `decision-guide.md` | Where to build (neuron vs submodule, API Skill placement) |
| `extension-mechanisms.md` | When to use skills/mcp/agent/command/hook |
| `spec-process.md` | How to develop specs via scenarios |
| `git-workflow.md` | Commit conventions, branch strategy, auto-commit/PR policies |
| `git-advanced.md` | Worktree, revert strategy, PR workflow, collaboration tips |
| `github-settings.md` | Branch protection, PR settings, review policy |
| `release-workflow.md` | Semantic versioning and release process |
| `repo-setup.md` | New repo and submodule setup guide |
| `module-protocol.md` | Submodule management (register, archive, re-register) |
| `self-improve-policy.md` | Self-healing agent constraints |

## Axioms

See [knowledge/ai-axioms.md](knowledge/ai-axioms.md) for details.

**Core Axioms**: Curiosity, Truth, Beauty — foundational values for autonomous judgment.

## Philosophy

See [knowledge/philosophy.md](knowledge/philosophy.md) for details.

| Principle | Meaning |
|-----------|---------|
| SSOT | One source, no duplication |
| MECE | Clear boundaries, complete coverage |
| Simplicity First | Simple > complex |
| Incremental | Build only what's needed now |
| Modularity | Independent, replaceable components |
| Agile | Embrace change, short iterations |
| Test-First | Tests = executable specs |
| AI-First | Machine-readable docs |
| Root Cause First | Fix cause, not symptom |
| Bounded Creativity | Freedom within guardrails—don't add new rules |
| Constructive Challenge | Question to strengthen, not obstruct |
| Front-load Pain | Analyze before coding |
| Autonomous Execution | Act first, ask only when blocked |
| Trust-based Delegation | AI executes, human directs |
| Verify Before Done | Prove it works, don't assume |

## Decision Signal Recognition

**Before executing location decisions, check architecture first:**
- New functionality? -> Separate repo -> Submodule (see "Working with This Repository")
- Location within neuron? -> Then execute location decision

**Execute immediately when user states:**
- Location: "put in docs", "store in X", "use Y folder" (after architecture check)
- Tool: "use Notion", "with GitHub", "via MCP"
- Approach: "I'll do X", "going to Y", "decided to Z"

**Confirm only when:**
- Multiple valid approaches exist AND user hasn't chosen
- Destructive action without explicit intent
- Ambiguous scope (what vs where vs how unclear)

**Default**: Trust user's stated decision. Act, don't ask.

## Conventions

- **Language**: English for all repository content
- **File size**: Max 200 lines per file
- **Documentation**: Structured for AI consumption
- **Commits**: Conventional commits (see [git-workflow.md](knowledge/git-workflow.md))
- **Co-Authored-By**: `Claude Opus 4.5 <noreply@anthropic.com>` (include in all AI commits)
- **Auto-commit**: Commit without asking when logical unit complete (see git-workflow.md)
- **Auto-PR**: Run /pr automatically on completion (see git-workflow.md)

## External Service Integration

- **Default**: Use API-based Skills, not MCP
- MCP only for manual user-added configurations
- For external services, reference `.claude/skills/*-api/` Skills:
  - GitHub → `github-api` skill
  - Jira → `jira-api` skill
  - Notion → `notion-api` skill
- Environment variables for authentication (see `.env.example`)

## Working with This Repository

When adding new functionality:
1. Check if it fits existing modules
2. If new module needed, create separate repo
3. Register as submodule under `modules/`
4. Document in relevant knowledge files
