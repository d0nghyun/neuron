---
name: workflow-schedule-notion
description: Notion schedule management. Query today/weekly schedules, add/modify/complete schedules.
allowed-tools: Bash, Read
user-invocable: true
---

# Notion Schedule Management

> Notion-based schedule query, add, and management workflow.

## When to Activate

- "today's schedule", "this week's schedule" queries
- "add schedule", "register appointment"
- "complete schedule", "cancel schedule"

## Configuration

```yaml
database_id: "2f346706-90ca-8108-b838-dd5861292951"
credentials: .credentials/notion.json
```

## Prerequisites

- api-notion credentials configured
- Integration connected to schedule DB

## Operations

### Query Today's Schedule

```bash
NOTION_API_TOKEN=$(jq -r '.api_token' /Users/dhlee/Git/personal/neuron/.credentials/notion.json)
TODAY=$(date +%Y-%m-%d)

curl -s -X POST \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "{\"filter\": {\"property\": \"날짜\", \"date\": {\"equals\": \"$TODAY\"}}}" \
  https://api.notion.com/v1/databases/2f346706-90ca-8108-b838-dd5861292951/query | \
  jq '[.results[] | {
    id: .id,
    title: .properties.제목.title[0].plain_text,
    date: .properties.날짜.date.start,
    status: .properties.상태.select.name,
    category: .properties.카테고리.select.name
  }]'
```

### Query Weekly Schedule

```bash
NOTION_API_TOKEN=$(jq -r '.api_token' /Users/dhlee/Git/personal/neuron/.credentials/notion.json)
START=$(date +%Y-%m-%d)
END=$(date -v+7d +%Y-%m-%d)

curl -s -X POST \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "{\"filter\": {\"and\": [{\"property\": \"날짜\", \"date\": {\"on_or_after\": \"$START\"}}, {\"property\": \"날짜\", \"date\": {\"on_or_before\": \"$END\"}}]}, \"sorts\": [{\"property\": \"날짜\", \"direction\": \"ascending\"}]}" \
  https://api.notion.com/v1/databases/2f346706-90ca-8108-b838-dd5861292951/query | \
  jq '[.results[] | {
    id: .id,
    title: .properties.제목.title[0].plain_text,
    date: .properties.날짜.date.start,
    status: .properties.상태.select.name,
    category: .properties.카테고리.select.name
  }]'
```

### Add Schedule

```bash
NOTION_API_TOKEN=$(jq -r '.api_token' /Users/dhlee/Git/personal/neuron/.credentials/notion.json)

curl -s -X POST \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "2f346706-90ca-8108-b838-dd5861292951"},
    "properties": {
      "제목": {"title": [{"text": {"content": "{TITLE}"}}]},
      "날짜": {"date": {"start": "{DATE}", "end": "{END_DATE}"}},
      "상태": {"select": {"name": "예정"}},
      "카테고리": {"select": {"name": "{CATEGORY}"}},
      "메모": {"rich_text": [{"text": {"content": "{MEMO}"}}]}
    }
  }' \
  https://api.notion.com/v1/pages
```

**Parameters:**
- `{TITLE}`: Schedule title (required)
- `{DATE}`: Start date YYYY-MM-DD (required)
- `{END_DATE}`: End date (optional, remove if not needed)
- `{CATEGORY}`: 업무 | 개인 | 미팅 | 기타 (Work | Personal | Meeting | Other)
- `{MEMO}`: Memo (optional)

### Update Schedule Status

```bash
NOTION_API_TOKEN=$(jq -r '.api_token' /Users/dhlee/Git/personal/neuron/.credentials/notion.json)

curl -s -X PATCH \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"상태": {"select": {"name": "{STATUS}"}}}}' \
  https://api.notion.com/v1/pages/{PAGE_ID}
```

**Status options:** 예정 (Scheduled), 진행중 (In Progress), 완료 (Completed), 취소 (Cancelled)

## Output Format

```yaml
schedule:
  - title: "Team Meeting"
    date: "2025-01-25"
    status: "예정"
    category: "미팅"
```

## Guardrails

- **NEVER** delete schedules without confirmation
- **ALWAYS** confirm before bulk operations

## Note

Notion DB property names are in Korean (제목, 날짜, 상태, 카테고리, 메모) as they match the actual database schema.
