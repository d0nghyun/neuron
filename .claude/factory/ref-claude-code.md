# Claude Code Built-in Reference

Check this before creating new components to avoid reinventing the wheel.

## Built-in Subagent Types

Via `Task` tool with `subagent_type`:

| Type | Purpose | Tools |
|------|---------|-------|
| `Bash` | Command execution, git ops | Bash |
| `general-purpose` | Complex multi-step tasks | All |
| `Explore` | Codebase exploration | Read-only |
| `Plan` | Implementation planning | Read-only |
| `claude-code-guide` | Claude Code questions | Read-only + Web |
| `code-simplifier` | Code simplification | All |

Composite agents (colon-separated):

| Type | Purpose |
|------|---------|
| `feature-dev` | Orchestrated feature development |
| `feature-dev:code-reviewer` | Code review with confidence filtering |
| `feature-dev:code-explorer` | Execution path tracing |
| `feature-dev:code-architect` | Feature architecture design |
| `agent-sdk-dev:agent-sdk-verifier-ts` | TS SDK verification |
| `agent-sdk-dev:agent-sdk-verifier-py` | Python SDK verification |

## Agent Frontmatter

```yaml
---
name: agent-name             # Required: unique identifier
description: When to use...  # Required: trigger conditions
model: haiku | sonnet | opus | inherit
color: blue                  # Optional: terminal color
tools: ["Read", "Bash"]      # Optional: restrict (inherits all if omitted)
disallowedTools: ["Write"]   # Optional: deny specific tools
permissionMode: default | acceptEdits | delegate | dontAsk | bypassPermissions | plan
maxTurns: 50                 # Optional: max agentic turns
skills:                      # Optional: preload skill content
  - skill-name
mcpServers:                  # Optional: MCP servers for this agent
  - server-name
memory: user | project | local  # Optional: persistent memory scope
hooks:                       # Optional: agent-level hooks
  PreToolUse: [...]
---
```

Tool restriction syntax: `Bash(npm *, git *)`, `Task(worker, researcher)`

## Agent Teams

Enable: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

Multiple agents with independent contexts, direct messaging, shared task list.

| | Subagent | Agent Team |
|-|----------|------------|
| Context | Returns results to caller | Fully independent |
| Communication | Report back only | Direct inter-teammate |
| Cost | Lower (summarized) | Higher (separate instances) |

Config: `"teammateMode": "in-process" | "tmux" | "auto"`

## Built-in Tools

| Category | Tools |
|----------|-------|
| File | `Read`, `Write`, `Edit`, `Glob`, `Grep`, `NotebookEdit` |
| Execution | `Bash`, `Task`, `TaskOutput`, `TaskStop` |
| Tasks | `TaskCreate`, `TaskGet`, `TaskUpdate`, `TaskList` |
| Interaction | `AskUserQuestion`, `EnterPlanMode`, `ExitPlanMode` |
| Web | `WebFetch`, `WebSearch` |
| Skills | `Skill` |

### Task Management

```
TaskCreate: subject, description, activeForm (spinner text), metadata
TaskUpdate: taskId, status (pending→in_progress→completed|deleted),
            subject, description, owner, addBlocks, addBlockedBy
TaskGet:    taskId → full details with dependencies
TaskList:   → all tasks with status summary
```

## Skills System

Auto-discovered from `.claude/skills/*/SKILL.md`.

### Skill Frontmatter

```yaml
---
name: skill-name
description: Trigger phrases and what it does
user-invocable: true          # Show in /command menu
disable-model-invocation: true # Prevent auto-trigger
allowed-tools: Read, Bash(git:*)
model: sonnet
argument-hint: "[arg1] [arg2]"
context: fork                 # Run in forked subagent
agent: subagent-type          # Which subagent to use
hooks:                        # Skill-level hooks
  PreToolUse: [...]
once: true                    # Run hook only once per session
---
```

### Substitutions

| Pattern | Description |
|---------|-------------|
| `$ARGUMENTS` | All arguments as string |
| `$N` / `$ARGUMENTS[N]` | Nth positional argument |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `` !`command` `` | Dynamic shell output injection |
| `@file` | File reference attachment |

## Hooks System

Configured in `.claude/settings.json` under `hooks`:

| Hook | Trigger |
|------|---------|
| `SessionStart` | Session begins/resumes |
| `UserPromptSubmit` | User submits prompt |
| `PreToolUse` | Before tool execution |
| `PostToolUse` | After tool succeeds |
| `PostToolUseFailure` | After tool fails |
| `PermissionRequest` | Permission dialog appears |
| `SubagentStart` | Subagent spawned |
| `SubagentStop` | Subagent finishes |
| `Stop` | Claude finishes responding |
| `PreCompact` | Before context compaction |
| `Setup` | `--init` or `--maintenance` |
| `SessionEnd` | Session terminates |
| `Notification` | Notification sent |

### Hook Configuration

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "bash script.sh",
        "timeout": 30
      }]
    }]
  }
}
```

Hook types: `command` (shell), `prompt` (LLM eval), `agent` (subagent with tools).

Options: `timeout` (seconds), `async` (background), `statusMessage` (spinner text).

Matcher: tool name, regex, or `*` for all.

Exit codes: `0`=success (parse stdout JSON), `2`=blocking error (stderr to Claude).

Env: `CLAUDE_PROJECT_DIR`, `CLAUDE_TOOL_INPUT`, `CLAUDE_TOOL_NAME`, `CLAUDE_FILE_PATH`

## MCP Integration

- Tool naming: `mcp__<server>__<tool>`
- Hook matchers support regex: `mcp__memory__.*`
- Resources: `@server:protocol://path` for referencing MCP resources
- Prompts: `/mcp__server__prompt` as slash commands
- Tool Search: Auto-loads tools on demand when MCP tools > 10% of context

## What NOT to Reinvent

| Claude Code Has | Don't Create |
|-----------------|--------------|
| `Explore` subagent | Codebase search agent |
| `Plan` subagent | Planning agent |
| Task tools | Task tracking system |
| Hooks | Automation triggers |
| Skills | Custom command system |
| Agent Teams | Multi-agent coordination |

## Neuron Adds

| Component | Purpose |
|-----------|---------|
| Factory patterns | Standardized component generation |
| Vault (`vault/`) | Private identity, projects, memory |
| Principles | Decision-making framework |

---

*Last updated: 2026-02-13*
