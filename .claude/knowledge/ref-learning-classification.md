# Learning Classification Reference

Guidelines for categorizing learnings and routing them to appropriate destinations.

## Learning Categories

| Category | Description | Destination |
|----------|-------------|-------------|
| convention | Coding style, naming, format rules | knowledge/conventions or factory patterns |
| workflow | Process improvements, automation | skills/ or hooks/ |
| review | Review criteria, checks to add | code-reviewer agent or knowledge/ |
| knowledge | Domain info, API details | knowledge/ reference files |
| failure | Error patterns, debugging insights | knowledge/learn-failures.yaml |

## Improvement Signals

### Convention Updates

Trigger: Same style issue appears 3+ times in reviews

```yaml
signal: repeated_style_issue
pattern: "Inconsistent error message format"
action: Add convention to factory/pattern-*.md
```

### Workflow Automation

Trigger: Manual step repeated across PRs

```yaml
signal: manual_repetition
pattern: "Always run lint before commit"
action: Create hook in hooks/pre-*.sh
```

### Review Criteria Addition

Trigger: Bug that review should have caught

```yaml
signal: missed_in_review
pattern: "Null check missing on API response"
action: Add check to code-reviewer agent
```

### Knowledge Gap

Trigger: Required lookup during task

```yaml
signal: external_lookup_needed
pattern: "Had to search API documentation"
action: Create/update knowledge/ref-*.md
```

## Failure Logging

All failures should be logged to `knowledge/learn-failures.yaml`:

```yaml
- timestamp: "2024-01-15T10:30:00Z"
  context: "PR review for auth module"
  failure: "Missed race condition in login flow"
  category: review
  resolution: "Add concurrency check to review criteria"
  prevented_by: "Explicit race condition review step"
```

## Destination Selection

```
Is it a repeated issue?
├── Yes → Convention or pattern update
└── No → Continue

Is it automation-able?
├── Yes → Skill or hook creation
└── No → Continue

Is it review-related?
├── Yes → Reviewer agent update
└── No → Knowledge file
```

## Priority Levels

| Priority | Criteria | Action Timeline |
|----------|----------|-----------------|
| P0 | Caused production issue | Immediate |
| P1 | Blocked workflow | Same session |
| P2 | Reduced efficiency | Next session |
| P3 | Minor improvement | Backlog |
