# Skill Pattern

Reference pattern for creating skills (API wrappers, domain knowledge, and workflows).

## Frontmatter (Required)

```yaml
---
name: {name}
description: {one-line description}
allowed-tools: Bash, Read, Grep, {others}
user-invocable: true | false
quality_grade: B                     # A/B/C/D — set by ops-factory-sync
quality_checked: 2026-01-01          # Last audit date
---
```

## Structure for API Skills (api-*)

```markdown
# {Service Name} API Skill

> API wrapper for {service}. Activate for {service} operations.

## When to Activate

- {trigger condition 1}
- {trigger condition 2}

## Authentication

**Credentials File**: `.credentials/{service}.json`

```json
{
  "{key}": "{placeholder}"
}
```

**Setup**: {how to obtain credentials}

**Load credentials**:
```bash
TOKEN=$(jq -r '.{key}' .credentials/{service}.json)
```

## API Base URL

```
https://api.{service}.com/v1
```

## Common Operations

### {Operation Name}

{Description}

```bash
{curl or CLI command}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `{param}` | {type} | Yes/No | {description} |

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Unauthorized | Check credentials |
| 429 | Rate limited | Wait and retry |

## Rate Limits

- **Limit**: {requests per minute}
- **Header**: X-RateLimit-Remaining
```

## Structure for Workflow Skills (workflow-*)

```markdown
# {Workflow Name} Skill

> {One-line description of workflow}

## When to Activate

- {trigger condition}

## Prerequisites

- {required state or component}

## Workflow Steps

### Step 1: {Action}
{Description}

### Step 2: {Action}
{Description}

### Step N: Complete
{Final action and output}

## Output

```yaml
workflow_result:
  status: success | failed
  {result_fields}
```

## Guardrails

- **NEVER** {prohibited action}
- **ALWAYS** {required action}
```

## MECE Boundary

| Concern | Lives In | NOT in Skill |
|---------|----------|--------------|
| How to use tools | Skill | - |
| How to think/judge | Agent (mental_model) | Skill |
| Team composition | Orchestrator CLAUDE.md | Skill |

## Examples

### Domain Skill (preloaded by agents)

```markdown
---
name: domain-{tool-name}
description: {Tool/platform} usage patterns
user-invocable: false
---
# {Tool Name} Skill
## Interface
{Core API patterns with code examples}
## Best Practices
- {Proven pattern}
## Gotchas
- {Common mistake} → {How to avoid}
## Know-how
- {Expert tip from experience}
```

### API Skill (`api-*`, user-invocable)

See existing `api-github`, `api-slack` for reference.

### Workflow Skill (`workflow-*`, user-invocable)

See existing `ops-daily-memo` for reference.

## Checklist

- [ ] Skill already exists? (check skills/)
- [ ] Domain skill → `user-invocable: false`, preloaded by agents
- [ ] API skill → authentication documented?
- [ ] Workflow skill → prerequisites clear?
- [ ] Contains NO judgment or mental model? (that belongs in Agent)
