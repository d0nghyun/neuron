---
name: confluence-api
description: Confluence REST API for pages, spaces, and content. Uses API token for headless/CI. Activate for Confluence operations.
allowed-tools: Bash, Read, Grep
---

# Confluence API Skill

## When to Activate

- Read/create/update pages
- Manage spaces
- Search content
- Handle attachments and labels

## Authentication

**Environment Variables**:
- `ATLASSIAN_BASE_URL`: Your Atlassian instance (e.g., https://your-domain.atlassian.net)
- `ATLASSIAN_USER_EMAIL`: Your Atlassian account email
- `ATLASSIAN_API_TOKEN`: API token from https://id.atlassian.com/manage-profile/security/api-tokens

**IMPORTANT**: Before any API call, load environment variables:
```bash
export $(grep -E "^ATLASSIAN_" /Users/dhlee/Git/personal/neuron/.env.local | xargs)
```

Or use Python with inline loading:
```python
import os
# Load from .env.local
with open('/Users/dhlee/Git/personal/neuron/.env.local') as f:
    for line in f:
        if line.startswith('ATLASSIAN_'):
            key, val = line.strip().split('=', 1)
            os.environ[key] = val
```

## API Base URL

```
$ATLASSIAN_BASE_URL/wiki/rest/api
```

## Required Headers

```bash
-u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN"
-H "Content-Type: application/json"
-H "Accept: application/json"
```

## Common Operations

### Get Current User
```bash
curl -s -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  "$ATLASSIAN_BASE_URL/wiki/rest/api/user/current"
```

### List Spaces
```bash
curl -s -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  "$ATLASSIAN_BASE_URL/wiki/rest/api/space"
```

### Get Space
```bash
curl -s -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  "$ATLASSIAN_BASE_URL/wiki/rest/api/space/{spaceKey}"
```

### Search Content
```bash
curl -s -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  "$ATLASSIAN_BASE_URL/wiki/rest/api/content/search?cql=text~'search term'"
```

### Get Page by ID
```bash
curl -s -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  "$ATLASSIAN_BASE_URL/wiki/rest/api/content/{pageId}?expand=body.storage,version"
```

### Get Page by Title
```bash
curl -s -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  "$ATLASSIAN_BASE_URL/wiki/rest/api/content?title=Page%20Title&spaceKey={spaceKey}&expand=body.storage"
```

### Create Page
```bash
curl -s -X POST \
  -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "page",
    "title": "New Page Title",
    "space": {"key": "{spaceKey}"},
    "body": {
      "storage": {
        "value": "<p>Page content in HTML</p>",
        "representation": "storage"
      }
    }
  }' \
  "$ATLASSIAN_BASE_URL/wiki/rest/api/content"
```

### Update Page
```bash
curl -s -X PUT \
  -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "version": {"number": 2},
    "title": "Updated Title",
    "type": "page",
    "body": {
      "storage": {
        "value": "<p>Updated content</p>",
        "representation": "storage"
      }
    }
  }' \
  "$ATLASSIAN_BASE_URL/wiki/rest/api/content/{pageId}"
```

### Get Page Children
```bash
curl -s -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  "$ATLASSIAN_BASE_URL/wiki/rest/api/content/{pageId}/child/page"
```

### Add Label to Page
```bash
curl -s -X POST \
  -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{"prefix": "global", "name": "label-name"}]' \
  "$ATLASSIAN_BASE_URL/wiki/rest/api/content/{pageId}/label"
```

### Get Page Labels
```bash
curl -s -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  "$ATLASSIAN_BASE_URL/wiki/rest/api/content/{pageId}/label"
```

## CQL (Confluence Query Language)

Common CQL queries:
- `space=SPACEKEY` - Content in specific space
- `type=page` - Only pages
- `title~"keyword"` - Title contains keyword
- `text~"keyword"` - Content contains keyword
- `label=labelname` - Content with label
- `creator=currentUser()` - Created by current user

Combine with AND/OR:
```
space=DEV AND type=page AND label=api
```

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Invalid credentials | Check email and API token |
| 403 | No permission | Verify space/page permissions |
| 404 | Not found | Check page ID or space key |
| 409 | Version conflict | Get latest version and retry |
| 429 | Rate limited | Wait and retry |

## Rate Limits

- Cloud: No published limits, but implement backoff
- Implement exponential backoff on 429 responses

## References

- [Confluence REST API Docs](https://developer.atlassian.com/cloud/confluence/rest/v1/intro/)
- [CQL Reference](https://developer.atlassian.com/cloud/confluence/advanced-searching-using-cql/)
