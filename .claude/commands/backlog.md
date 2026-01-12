---
description: Extract remaining/deferred tasks from session into TodoWrite backlog.
tools: TodoWrite
---

# Extract Session Backlog

## Purpose

Scan current conversation context and extract remaining/deferred tasks into TodoWrite for tracking.

## When to Use

- End of session with incomplete work
- After planning with Phase 2 items
- When switching context mid-task
- User wants to capture "do later" items

## Extraction Patterns

Look for these signals in conversation:

| Signal | Example |
|--------|---------|
| Phase 2/3 | "Phase 2: Hook testing" |
| Later/TODO | "will do later", "TODO:" |
| Deferred | "leaving for now", "skip for now" |
| Remaining | "still need to", "haven't done yet" |
| Blocked | "waiting for", "depends on" |
| Incremental | "gradually", "over time" |

## Execution

1. **Scan context**: Review conversation for remaining work signals
2. **Categorize**: Group by priority (blocking vs nice-to-have)
3. **Write todos**: Use TodoWrite with clear, actionable items

### Output Format

```
TodoWrite([
  { content: "<actionable task>", status: "pending", activeForm: "<-ing form>" },
  ...
])
```

## Example

Conversation mentions:
- "Phase 2: Test AskUserQuestion hook matcher"
- "Gradually add frontmatter to remaining knowledge files"

Output:
```
TodoWrite([
  { content: "Test AskUserQuestion hook matcher", status: "pending", activeForm: "Testing AskUserQuestion hook matcher" },
  { content: "Add frontmatter to remaining knowledge files", status: "pending", activeForm: "Adding frontmatter to knowledge files" }
])
```

## Notes

- Only extract concrete, actionable items
- Skip vague or already-completed items
- Include context if task is ambiguous
- Mark blocking items first
