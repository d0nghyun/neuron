---
name: api-jira
description: Jira REST API for issues, projects, sprints. Uses API token for headless/CI. Activate for Jira operations.
allowed-tools: Bash, Read, Grep
user-invocable: true
---

# Jira API Skill

## When to Activate

- Create/read/update Jira issues
- Manage sprints and boards
- Query project information
- Transition issue status

## Authentication

**Credentials File**: `.credentials/atlassian.json`

```json
{
  "base_url": "https://yourcompany.atlassian.net",
  "user_email": "your@email.com",
  "api_token": "..."
}
```

Create token at: https://id.atlassian.com/manage-profile/security/api-tokens

**Load credentials before API calls**:
```bash
ATLASSIAN_BASE_URL=$(jq -r '.base_url' /Users/dhlee/Git/personal/neuron/.credentials/atlassian.json)
ATLASSIAN_USER_EMAIL=$(jq -r '.user_email' /Users/dhlee/Git/personal/neuron/.credentials/atlassian.json)
ATLASSIAN_API_TOKEN=$(jq -r '.api_token' /Users/dhlee/Git/personal/neuron/.credentials/atlassian.json)
```

## API Base URL

```
$ATLASSIAN_BASE_URL/rest/api/3
```

## Common Operations

### Get Current User
```bash
curl -s -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  -H "Accept: application/json" \
  "$ATLASSIAN_BASE_URL/rest/api/3/myself"
```

### Search Issues (JQL)
```bash
# Note: Use /search/jql endpoint (2026+ API change)
curl -s -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  -H "Accept: application/json" \
  -G --data-urlencode "jql=project=PROJ AND status='In Progress'" \
  "$ATLASSIAN_BASE_URL/rest/api/3/search/jql"
```

### Get Issue
```bash
curl -s -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  -H "Accept: application/json" \
  "$ATLASSIAN_BASE_URL/rest/api/3/issue/{issueIdOrKey}"
```

### Create Issue
```bash
curl -s -X POST \
  -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "PROJ"},
      "summary": "Issue summary",
      "description": {
        "type": "doc",
        "version": 1,
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Description"}]}]
      },
      "issuetype": {"name": "Task"}
    }
  }' \
  "$ATLASSIAN_BASE_URL/rest/api/3/issue"
```

### Transition Issue
```bash
# Get available transitions
curl -s -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  -H "Accept: application/json" \
  "$ATLASSIAN_BASE_URL/rest/api/3/issue/{issueIdOrKey}/transitions"

# Apply transition
curl -s -X POST \
  -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"transition": {"id": "31"}}' \
  "$ATLASSIAN_BASE_URL/rest/api/3/issue/{issueIdOrKey}/transitions"
```

### Add Comment
```bash
curl -s -X POST \
  -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "body": {
      "type": "doc",
      "version": 1,
      "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Comment text"}]}]
    }
  }' \
  "$ATLASSIAN_BASE_URL/rest/api/3/issue/{issueIdOrKey}/comment"
```

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Invalid credentials | Check email and API token |
| 403 | No permission | Verify project access |
| 404 | Issue not found | Check issue key |

## References

- [Jira REST API Docs](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
