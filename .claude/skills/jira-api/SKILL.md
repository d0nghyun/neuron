---
name: jira-api
description: Jira REST API for issues, projects, sprints. Uses API token for headless/CI. Activate for Jira operations.
allowed-tools: Bash, Read, Grep
---

# Jira API Skill

## When to Activate

- Create/read/update Jira issues
- Manage sprints and boards
- Query project information
- Transition issue status

## Authentication

**Environment Variables**:
- `JIRA_BASE_URL` - Your Jira instance (e.g., `https://yourcompany.atlassian.net`)
- `JIRA_USER_EMAIL` - Your Atlassian account email
- `JIRA_API_TOKEN` - API token

Create token at: https://id.atlassian.com/manage-profile/security/api-tokens

## API Base URL

```
{JIRA_BASE_URL}/rest/api/3
```

## Common Operations

### Get Current User
```bash
curl -s -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  -H "Accept: application/json" \
  "$JIRA_BASE_URL/rest/api/3/myself"
```

### Search Issues (JQL)
```bash
curl -s -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  -H "Accept: application/json" \
  --data-urlencode "jql=project=PROJ AND status='In Progress'" \
  "$JIRA_BASE_URL/rest/api/3/search"
```

### Get Issue
```bash
curl -s -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  -H "Accept: application/json" \
  "$JIRA_BASE_URL/rest/api/3/issue/{issueIdOrKey}"
```

### Create Issue
```bash
curl -s -X POST \
  -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
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
  "$JIRA_BASE_URL/rest/api/3/issue"
```

### Transition Issue
```bash
# Get available transitions
curl -s -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  -H "Accept: application/json" \
  "$JIRA_BASE_URL/rest/api/3/issue/{issueIdOrKey}/transitions"

# Apply transition
curl -s -X POST \
  -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"transition": {"id": "31"}}' \
  "$JIRA_BASE_URL/rest/api/3/issue/{issueIdOrKey}/transitions"
```

### Add Comment
```bash
curl -s -X POST \
  -u "$JIRA_USER_EMAIL:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "body": {
      "type": "doc",
      "version": 1,
      "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Comment text"}]}]
    }
  }' \
  "$JIRA_BASE_URL/rest/api/3/issue/{issueIdOrKey}/comment"
```

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Invalid credentials | Check email and API token |
| 403 | No permission | Verify project access |
| 404 | Issue not found | Check issue key |

## References

- [Jira REST API Docs](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
