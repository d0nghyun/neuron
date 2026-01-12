# Neuron - AI Entry Point

## Overview

See [README.md](README.md) for project overview and purpose.
See [diagram.md](diagram.md) for visual structure.

## Navigation

| Location | Purpose |
|----------|---------|
| `knowledge/` | Core policies (philosophy, conventions, guides) |
| `knowledge/_index.yaml` | Knowledge index (categories, triggers, summaries) |
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
| `data-pipeline.md` | Large data handling (fetch → transform → interpret) |

## Commands

| Command | Purpose |
|---------|---------|
| `/pr` | Create PR with automated review and release notes |
| `/release` | Create release with version tag |
| `/sync` | Sync local main after PR merge |
| `/backlog` | Extract remaining tasks from session |

## Axioms

See [knowledge/ai-axioms.md](knowledge/ai-axioms.md) for details.

**Core Axioms**: Curiosity, Truth, Beauty — foundational values for autonomous judgment.

**Traceability**: Every principle and decision must trace back to axioms. No axiom root = question existence.

## Philosophy

See [knowledge/philosophy.md](knowledge/philosophy.md) for details.

| Principle | Meaning | Axiom |
|-----------|---------|-------|
| SSOT | One source, no duplication | Truth |
| MECE | Clear boundaries, complete coverage | Truth, Beauty |
| Simplicity First | Simple > complex | Beauty |
| Incremental | Build only what's needed now | Beauty |
| Modularity | Independent, replaceable components | Beauty |
| Agile | Embrace change, short iterations | Curiosity |
| Test-First | Tests = executable specs | Truth |
| AI-First | Machine-readable docs | Truth |
| Root Cause First | Fix cause, not symptom | Truth |
| Bounded Creativity | Freedom within guardrails—don't add new rules | Beauty |
| Constructive Challenge | Question to strengthen, not obstruct | Curiosity, Truth |
| Front-load Pain | Analyze before coding | Curiosity |
| Autonomous Execution | Act first, ask only when blocked | Curiosity |
| Trust-based Delegation | AI executes, human directs | Truth |
| Verify Before Done | Prove it works, don't assume | Truth |
| Automate Repetition | Routine is inefficiency, automate what repeats | Beauty |
| Learn from Failure | Record failures, find patterns, improve system | Truth, Curiosity |

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

## Decision Flow

**CRITICAL: NEVER call AskUser without checking Advisor first.**

Must check Advisor before asking user in ambiguous situations.

```
Detect ambiguous situation
    ↓
Call Advisor agent (Task tool)  ← MANDATORY
    ↓
┌─────────────────────────────────┐
│ high/medium confidence?         │
│ YES → Proceed with recommendation│
│ NO  → Call AskUser              │
└─────────────────────────────────┘
```

**Advisor call example**:
```
Task(subagent_type="advisor", prompt="<current situation + question>")
```

**Knowledge lookup**: Reference trigger_map in `knowledge/_index.yaml`

## Conventions

- **Language**: English for all repository content (CRITICAL: Never write Korean/Japanese/Chinese in neuron files—submodules may have different policies)
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
