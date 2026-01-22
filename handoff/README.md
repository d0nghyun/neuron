# Handoff Directory

Session state files for parallel work continuity.

## Structure

```
handoff/
├── README.md          # This file
├── _index.md          # Quick overview of all active sessions
├── <context>.md       # Per-context state (module, task, or feature)
```

## Naming Convention

Use context-based names:
- `arkraft.md` - Module-level work
- `arkraft-demo.md` - Specific feature/task
- `infra-setup.md` - Cross-cutting work

## File Template

```markdown
# Handoff: <Context Name>

## State
| Field | Value |
|-------|-------|
| **Status** | in-progress / blocked / paused |
| **Updated** | YYYY-MM-DD HH:MM |
| **Branch** | feature/xxx (if applicable) |

## Current Task
- **Goal**: What to achieve
- **Progress**: Where we are
- **Next**: Immediate next step
- **Blockers**: What's stopping progress

## Context
Key decisions, file locations, important notes for continuation.

## History
- [YYYY-MM-DD] What happened
```

## Usage

1. **Start session**: Run `/handoff` → reads `_index.md` and relevant context file
2. **During work**: Update context file when significant progress
3. **End session**: Update status and next steps
4. **Context overflow**: Document everything needed to continue
