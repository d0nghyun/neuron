---
name: notion-api
description: Notion REST API for pages, databases, blocks. Uses internal integration token for headless/CI. Activate for Notion operations.
allowed-tools: Bash, Read, Grep
---

# Notion API Skill

## When to Activate

- Read/create/update pages
- Query databases
- Manage blocks and content
- Search workspace

## Authentication

**Environment Variable**: `NOTION_API_TOKEN`

Create internal integration at: https://www.notion.so/my-integrations

**Important**: Pages must be shared with the integration to be accessible.

## API Base URL

```
https://api.notion.com/v1
```

## Required Headers

```
Authorization: Bearer $NOTION_API_TOKEN
Notion-Version: 2022-06-28
Content-Type: application/json
```

## Common Operations

### List Users
```bash
curl -s -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  https://api.notion.com/v1/users
```

### Search
```bash
curl -s -X POST \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"query": "search term", "filter": {"property": "object", "value": "page"}}' \
  https://api.notion.com/v1/search
```

### Get Page
```bash
curl -s -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  https://api.notion.com/v1/pages/{page_id}
```

### Query Database
```bash
curl -s -X POST \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"property": "Status", "select": {"equals": "Done"}}}' \
  https://api.notion.com/v1/databases/{database_id}/query
```

### Create Page in Database
```bash
curl -s -X POST \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "{database_id}"},
    "properties": {
      "Name": {"title": [{"text": {"content": "New page title"}}]},
      "Status": {"select": {"name": "In Progress"}}
    }
  }' \
  https://api.notion.com/v1/pages
```

### Append Block Children
```bash
curl -s -X PATCH \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
          "rich_text": [{"type": "text", "text": {"content": "New paragraph"}}]
        }
      }
    ]
  }' \
  https://api.notion.com/v1/blocks/{block_id}/children
```

### Get Block Children
```bash
curl -s -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  "https://api.notion.com/v1/blocks/{block_id}/children?page_size=100"
```

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Invalid token | Check NOTION_API_TOKEN |
| 403 | Page not shared | Share page with integration |
| 404 | Resource not found | Verify page/database ID |
| 429 | Rate limited | Wait and retry |

## Rate Limits

- 3 requests per second average
- Implement exponential backoff

## References

- [Notion API Docs](https://developers.notion.com/reference)
