# Skill Pattern

Reference pattern for creating skills (API wrappers and workflows).

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

## Examples

### API Skill

```markdown
---
name: api-github
description: GitHub REST API for issues, PRs, repos
allowed-tools: Bash, Read, Grep
user-invocable: true
quality_grade: A
quality_checked: 2026-02-13
---

# GitHub API Skill

> API wrapper for GitHub. Activate for GitHub operations.

## When to Activate
- User mentions GitHub issues, PRs, repos

## Authentication
**Credentials File**: `.credentials/github.json`

## Common Operations
### List Issues
```bash
gh issue list --repo {owner}/{repo}
```

### Create PR
```bash
gh pr create --title "{title}" --body "{body}"
```
```

### Workflow Skill

```markdown
---
name: workflow-pr
description: Create PR with automated review
allowed-tools: Bash, Read, Glob, Task
user-invocable: true
quality_grade: B
quality_checked: 2026-02-13
---

# PR Workflow Skill

> Create PR from current changes with automated review.

## Workflow Steps
### Step 1: Stage Changes
```bash
git add -A && git status
```
### Step 2: Create Commit
Follow commit conventions.
### Step 3: Push & Create PR
```bash
git push -u origin {branch} && gh pr create
```
### Step 4: Run Reviewer
Invoke reviewer subagent for automated review.
```

## Checklist Before Creating

- [ ] Does this skill already exist? (check skills/)
- [ ] For API: Is authentication documented?
- [ ] For workflow: Are prerequisites clear?
- [ ] Is user-invocable correctly set?
