# Hook Pattern

Reference pattern for creating hooks (automatic triggers).

## What is a Hook?

Hooks are shell commands that execute automatically in response to Claude Code events.
They are configured in `.claude/settings.json` under the `hooks` section.

## Hook Types

| Type | Triggers When |
|------|---------------|
| `PreToolUse` | Before a tool executes |
| `PostToolUse` | After a tool succeeds |
| `PostToolUseFailure` | After a tool fails |
| `PermissionRequest` | When permission dialog appears |
| `Notification` | Claude sends a notification |
| `UserPromptSubmit` | When user submits a message |
| `Stop` | Claude completes response |
| `SubagentStop` | When a subagent completes |
| `PreCompact` | Before context compaction |
| `Setup` | On repo init/maintenance |
| `SessionStart` | When session starts/resumes |
| `SessionEnd` | When session ends |

## Configuration Location

Hooks are defined in `.claude/settings.json`:

```json
{
  "hooks": {
    "{hook_type}": [
      {
        "matcher": "{tool_name or pattern}",
        "hooks": [
          {
            "type": "command",
            "command": "{shell command}"
          }
        ]
      }
    ]
  }
}
```

## Structure

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "{tool_name}",
        "hooks": [
          {
            "type": "command",
            "command": "{validation command}"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "{tool_name}",
        "hooks": [
          {
            "type": "command",
            "command": "{follow-up command}"
          }
        ]
      }
    ]
  }
}
```

## Examples

### Pre-commit Lint Hook

Run linter before any Bash command that includes "git commit":

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'git commit'; then npm run lint; fi"
          }
        ]
      }
    ]
  }
}
```

### Post-deploy Notification Hook

Send notification after deployment:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'deploy'; then echo 'Deployed!' | notify; fi"
          }
        ]
      }
    ]
  }
}
```

### Edit Validation Hook

Validate file edits before they happen:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Editing: '$CLAUDE_FILE_PATH"
          }
        ]
      }
    ]
  }
}
```

## Environment Variables

Available in hook commands:

| Variable | Description |
|----------|-------------|
| `CLAUDE_TOOL_NAME` | Name of the tool being used |
| `CLAUDE_TOOL_INPUT` | Input parameters (JSON) |
| `CLAUDE_FILE_PATH` | File path (for file operations) |

## Best Practices

1. **Keep hooks fast** - They run synchronously and block execution
2. **Use conditionals** - Check tool input before acting
3. **Fail gracefully** - Don't break the workflow on hook errors
4. **Log sparingly** - Excessive output clutters the session

## Checklist Before Creating

- [ ] Is automatic execution truly needed?
- [ ] Can this be done with a skill instead? (more flexible)
- [ ] Is the matcher specific enough?
- [ ] Will the command execute quickly?
