# Extension Mechanisms

Claude Code extension points and when to use each.

## Overview

| Mechanism | Purpose | Trigger |
|-----------|---------|---------|
| **Skills** | Execute code | User invokes |
| **MCP** | External service integration | Tool call |
| **Subagent** | Autonomous judgment | Task delegation |
| **Commands (Slash)** | Simple policy execution | `/command` |
| **Hooks** | Fully automated scripts | System events |

## Skills

**When**: Need to execute code as part of a workflow.

```
Examples:
- PDF generation
- Build & test execution
- Data transformation
```

**Location**: `.claude/skills/<skill-name>/SKILL.md`

## External Service Integration

**Default Policy**: Use API-based Skills, not MCP.

### MCP vs API Skills

| Scenario | Recommended | Reason |
|----------|-------------|--------|
| CI/CD, headless | API Skill | No browser for OAuth |
| Automation pipeline | API Skill | Env vars only |
| Local interactive | MCP (optional) | User can add manually |

### API Skills (Default)

**Location**: `.claude/skills/*-api/SKILL.md`

| Service | Skill | Auth Env Var |
|---------|-------|--------------|
| GitHub | `github-api` | `GITHUB_PERSONAL_ACCESS_TOKEN` |
| Jira | `jira-api` | `JIRA_API_TOKEN` |
| Notion | `notion-api` | `NOTION_API_TOKEN` |

See `.env.example` for all required environment variables.

### MCP (Manual Only)

**When**: User manually adds for local interactive use.

**Location**: `.mcp.json` (gitignored)

OAuth-based hosted MCP servers require browser authentication.
Not suitable for automation/CI.

## Subagent

**When**: Task requires autonomous judgment and decision-making.

```
Examples:
- reviewer: Analyze code quality, make judgments
- self-improve: Detect patterns, propose changes
- explorer: Navigate codebase, find relevant info
```

**Location**: `.claude/agents/<agent-name>.md`

## Commands (Slash)

**When**: Simple, repeatable policy execution triggered by user.

```
Examples:
- /pr: Create pull request with standard format
- /release: Tag and release with changelog
- /commit: Commit with conventional format
```

**Location**: `.claude/commands/<command>.md`

## Hooks

**When**: Fully automated, no human trigger needed.

```
Examples:
- pre-commit: Lint, format check
- post-push: Notify, deploy
- on-error: Auto-report
```

**Location**: `.claude/settings.json` or project hooks config

## Decision Flowchart

```
Need to extend Claude Code?
           │
           ▼
┌─────────────────────────────┐
│ External service needed?    │
│ YES → API Skill (default)   │
│ NO  → ▼                     │
└─────────────────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Autonomous judgment needed? │
│ YES → Subagent              │
│ NO  → ▼                     │
└─────────────────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Fully automated (no human)? │
│ YES → Hook                  │
│ NO  → ▼                     │
└─────────────────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Complex code execution?     │
│ YES → Skill                 │
│ NO  → Command (Slash)       │
└─────────────────────────────┘
```

## Quick Reference

| Need | Use |
|------|-----|
| Call GitHub/Jira/Notion API | API Skill |
| Review code quality | Subagent |
| Auto-format on save | Hook |
| Generate PDF report | Skill |
| Create PR with template | Command |

## Related

- [decision-guide.md](decision-guide.md) - Where to place components (neuron vs project)
- [spec-process.md](spec-process.md) - How to develop specifications before building
