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

## MCP (Model Context Protocol)

**When**: Need to integrate with external services/APIs.

```
Examples:
- Notion API (docs sync)
- GitHub API (issues, PRs)
- Database connections
- Slack notifications
```

**Location**: `.mcp.json` (project root, Git shared)

### Configuration Policy

| Transport | CLI | Web (Sandbox) | Use When |
|-----------|-----|---------------|----------|
| **HTTP** | Yes | Yes | Default choice, OAuth services |
| SSE | Yes | Yes | Deprecated, avoid |
| stdio | Yes | No | CLI-only, local tools |

**Policy**: Always use `type: http` for web sandbox compatibility.

### Format (HTTP - Recommended)

```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

### Authentication

OAuth-based services (Atlassian, Notion, GitHub):
- Run `/mcp` command in Claude Code
- Complete browser OAuth flow
- Token managed automatically

### Common MCP Servers

| Service | URL |
|---------|-----|
| Atlassian | `https://mcp.atlassian.com/v1/mcp` |
| Notion | `https://mcp.notion.com/mcp` |
| GitHub | `https://api.githubcopilot.com/mcp/` |

See decision-guide.md for placement decisions (neuron vs project-specific).

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
│ YES → MCP                   │
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
| Call Notion API | MCP |
| Review code quality | Subagent |
| Auto-format on save | Hook |
| Generate PDF report | Skill |
| Create PR with template | Command |

## Related

- [decision-guide.md](decision-guide.md) - Where to place components (neuron vs project)
- [spec-process.md](spec-process.md) - How to develop specifications before building
