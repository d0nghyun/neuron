# Model Routing Reference

Decision guide for selecting the right model (haiku/sonnet/opus) based on task characteristics.

## Quick Reference

```
haiku  → Fast and cheap, simple tasks
sonnet → Balanced, general code work
opus   → Powerful, complex architectural decisions
```

## Dimensions

### Scope

| Level | Definition | Examples |
|-------|------------|----------|
| micro | Single function/line | Fix typo, add comment, rename variable |
| file | Single file changes | Refactor function, add method, fix bug |
| module | Multiple related files | New feature, API endpoint with tests |
| system | Cross-cutting changes | Architecture refactor, framework migration |

### Risk

| Level | Definition | Examples |
|-------|------------|----------|
| read | No state changes | Search, analyze, explain, review |
| write | Reversible file changes | Edit code, create file, update config |
| deploy | Production/external impact | Create PR, merge, release, API calls |
| system | System configuration | Modify hooks, settings, credentials |

## Routing Matrix

```
┌────────────┬────────┬────────┬────────┬────────┐
│ Scope\Risk │  read  │ write  │ deploy │ system │
├────────────┼────────┼────────┼────────┼────────┤
│   micro    │ haiku  │ haiku  │ sonnet │ sonnet │
│   file     │ haiku  │ sonnet │ sonnet │  opus  │
│   module   │ sonnet │ sonnet │  opus  │  opus  │
│   system   │ sonnet │  opus  │  opus  │  opus  │
└────────────┴────────┴────────┴────────┴────────┘
```

## Signal Keywords

### Scope Detection

| Keywords | Scope |
|----------|-------|
| "typo", "comment", "rename", "this line" | micro |
| "this file", "function", "method", "class" | file |
| "feature", "endpoint", "module", "component" | module |
| "refactor", "migrate", "architecture", "all" | system |

### Risk Detection

| Keywords | Risk |
|----------|------|
| "check", "find", "search", "explain", "review" | read |
| "fix", "add", "edit", "update", "create file" | write |
| "PR", "merge", "release", "deploy", "push" | deploy |
| "settings", "config", "hooks", "credentials" | system |

## Examples

| Request | Scope | Risk | Model |
|---------|-------|------|-------|
| "Fix typo in README" | micro | write | haiku |
| "Review this function" | file | read | haiku |
| "Add validation to user input" | file | write | sonnet |
| "Create PR for these changes" | file | deploy | sonnet |
| "Implement auth module with tests" | module | write | sonnet |
| "Release version 2.0" | module | deploy | opus |
| "Refactor entire codebase structure" | system | write | opus |

## Cost Considerations

| Model | Relative Cost | Use When |
|-------|---------------|----------|
| haiku | 1x | Simple, fast, low-risk |
| sonnet | 10x | Standard development work |
| opus | 30x | Critical decisions, complex reasoning |

**Default to haiku** unless complexity demands more.

## Override Rules

Always use opus:
- User explicitly requests careful analysis
- Task involves security-sensitive changes
- Architectural decisions with long-term impact

Always use haiku:
- Simple queries and searches
- Formatting and style fixes
- Status checks and listings
