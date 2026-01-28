# Claude Code Built-in Reference

Reference document for Claude Code's built-in features.
Check this before creating new components to avoid reinventing the wheel.

## Built-in Subagent Types

Available via `Task` tool with `subagent_type` parameter:

| Type | Purpose | Tools |
|------|---------|-------|
| `Bash` | Command execution, git operations | Bash |
| `general-purpose` | Multi-step tasks, code search | All |
| `Explore` | Codebase exploration, file search | Read-only (no Write, Edit) |
| `Plan` | Implementation planning | Read-only (no Write, Edit) |
| `claude-code-guide` | Claude Code usage questions | Read-only + Web |
| `statusline-setup` | Configure status line | Read, Edit |
| `code-simplifier` | Code simplification | All |
| `reviewer` | Code review, release notes | Read, Glob, Grep, Bash, Edit |
| `wrapup` | Session teardown, learnings | Read, Edit, Glob, Grep |
| `self-improve` | System improvements | All + Task |
| `boot` | Session initialization | Read, Glob, Grep |
| `refactor` | Refactoring planning | Read, Glob, Grep, Bash, Task |
| `advisor` | Knowledge-based recommendations | Read, Glob, Grep |

### Feature Development Agents

| Type | Purpose |
|------|---------|
| `feature-dev:code-reviewer` | Code review with confidence filtering |
| `feature-dev:code-explorer` | Execution path tracing, architecture mapping |
| `feature-dev:code-architect` | Feature architecture design |

### Agent SDK Agents

| Type | Purpose |
|------|---------|
| `agent-sdk-dev:agent-sdk-verifier-ts` | TypeScript SDK verification |
| `agent-sdk-dev:agent-sdk-verifier-py` | Python SDK verification |
| `agent-sdk-dev:new-sdk-app` | New SDK app creation |

## Built-in Tools

### File Operations
| Tool | Purpose |
|------|---------|
| `Read` | Read files (text, images, PDFs, notebooks) |
| `Write` | Create/overwrite files |
| `Edit` | Exact string replacement in files |
| `Glob` | File pattern matching |
| `Grep` | Content search with regex |
| `NotebookEdit` | Jupyter notebook cell editing |

### Execution
| Tool | Purpose |
|------|---------|
| `Bash` | Shell command execution |
| `Task` | Launch subagents |
| `TaskOutput` | Get task output |
| `TaskStop` | Stop background tasks |

### Task Management
| Tool | Purpose |
|------|---------|
| `TaskCreate` | Create todo items |
| `TaskGet` | Get task details |
| `TaskUpdate` | Update task status |
| `TaskList` | List all tasks |

### User Interaction
| Tool | Purpose |
|------|---------|
| `AskUserQuestion` | Ask clarifying questions |
| `EnterPlanMode` | Enter planning mode |
| `ExitPlanMode` | Exit planning mode |

### Web
| Tool | Purpose |
|------|---------|
| `WebFetch` | Fetch URL content |
| `WebSearch` | Search the web |

### Skills
| Tool | Purpose |
|------|---------|
| `Skill` | Execute registered skills |

## Hooks System

Event-driven automation via `.claude/settings.json`:

| Hook | Trigger |
|------|---------|
| `SessionStart` | Session begins or resumes |
| `UserPromptSubmit` | User submits a prompt |
| `PreToolUse` | Before tool execution |
| `PermissionRequest` | When permission dialog appears |
| `PostToolUse` | After tool succeeds |
| `PostToolUseFailure` | After tool fails |
| `SubagentStart` | When spawning a subagent |
| `SubagentStop` | When subagent finishes |
| `Stop` | Claude finishes responding |
| `PreCompact` | Before context compaction |
| `Setup` | With `--init` or `--maintenance` flags |
| `SessionEnd` | Session terminates |
| `Notification` | Claude Code sends notifications |

Hook types:
- `command`: Execute shell command
- `prompt`: LLM-based evaluation (for Stop, SubagentStop, etc.)

## Agent Features

| Feature | Description |
|---------|-------------|
| Agent resume | Continue agent with `resume` parameter using agent ID |
| Background agents | `run_in_background: true` for async execution |
| Parallel agents | Multiple Task calls in single message |
| Model selection | `model: "sonnet" | "opus" | "haiku" | "inherit"` |
| CLI-defined agents | `--agents` flag with JSON for session-only agents |

### Subagent Frontmatter Fields

| Field | Description |
|-------|-------------|
| `name` | Unique identifier (required) |
| `description` | When to delegate to this agent (required) |
| `tools` | Allowed tools (inherits all if omitted) |
| `disallowedTools` | Tools to deny from inherited list |
| `model` | Model: opus (Opus 4.5), sonnet (Sonnet 4.5), haiku, inherit |
| `permissionMode` | default, acceptEdits, dontAsk, bypassPermissions, plan |
| `skills` | Skills to preload into agent context |
| `hooks` | Lifecycle hooks (PreToolUse, PostToolUse, Stop) |

## Skills System

Skills are auto-discovered from `.claude/skills/*/SKILL.md` and subdirectories.

### Skill Frontmatter Fields

| Field | Description |
|-------|-------------|
| `name` | Unique identifier (required) |
| `description` | What the skill does (required) |
| `user-invocable` | Show in menu, allow `/skill-name` invocation |
| `disable-model-invocation` | Prevent auto-invocation by Claude |
| `allowed-tools` | Restrict available tools |
| `model` | Model to use |
| `context: fork` | Run in forked subagent |
| `agent` | Subagent type to use |
| `hooks` | Skill-level hooks (PreToolUse, PostToolUse, Stop) |
| `once: true` | Run hook only once per session |

### String Substitutions

| Pattern | Description |
|---------|-------------|
| `$ARGUMENTS` | All arguments as string |
| `$ARGUMENTS[N]` | Nth argument (0-indexed) |
| `$N` | Shorthand for `$ARGUMENTS[N]` |
| `${CLAUDE_SESSION_ID}` | Current session ID |

### Dynamic Context Injection

Use `` !`command` `` to inject shell output into skill prompts (preprocessed before execution).

## MCP Integration

MCP tools follow naming: `mcp__<server>__<tool>`

Hook matchers support regex: `mcp__memory__.*`, `mcp__.*__write.*`

## What NOT to Reinvent

| Claude Code Has | Don't Create |
|-----------------|--------------|
| `Explore` subagent | Custom codebase search agent |
| `Plan` subagent | Custom planning agent |
| `reviewer` subagent | Custom review agent |
| Task tools | Custom task tracking |
| Hooks | Custom automation triggers |
| Skill tool | Custom skill execution |

## Neuron Adds (Not in Claude Code)

| Component | Purpose |
|-----------|---------|
| Factory patterns | Standardized component generation |
| Contexts (`ctx-*.yaml`) | Session state, module configs |
| Knowledge docs | Reference materials, learnings |
| Philosophy/principles | Decision-making framework |

## Platform Support

- CLI (primary)
- VS Code extension
- JetBrains IDEs
- Desktop app (preview)
- Web (Claude.ai integration)
- GitHub Actions

---

*Last updated: 2026-01-28*
*Update this when Claude Code releases new features*
