---
name: workflow-schedule-notion
description: Notion 일정관리. 오늘/주간 일정 조회, 일정 추가/수정/완료 처리.
allowed-tools: Bash, Read
user-invocable: true
---

# Notion 일정관리

> Notion 기반 일정 조회, 추가, 관리 workflow.

## When to Activate

- "오늘 일정", "이번주 일정" 조회
- "일정 추가", "스케줄 등록"
- "일정 완료", "일정 취소"

## Configuration

```yaml
database_id: "2f346706-90ca-8108-b838-dd5861292951"
credentials: .credentials/notion.json
```

## Prerequisites

- api-notion credentials 설정됨
- 일정 DB에 integration 연결됨

## Operations

### 오늘 일정 조회

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
    제목: .properties.제목.title[0].plain_text,
    날짜: .properties.날짜.date.start,
    상태: .properties.상태.select.name,
    카테고리: .properties.카테고리.select.name
  }]'
```

### 주간 일정 조회

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
    제목: .properties.제목.title[0].plain_text,
    날짜: .properties.날짜.date.start,
    상태: .properties.상태.select.name,
    카테고리: .properties.카테고리.select.name
  }]'
```

### 일정 추가

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
- `{TITLE}`: 일정 제목 (필수)
- `{DATE}`: 시작 날짜 YYYY-MM-DD (필수)
- `{END_DATE}`: 종료 날짜 (선택, 없으면 제거)
- `{CATEGORY}`: 업무 | 개인 | 미팅 | 기타
- `{MEMO}`: 메모 (선택)

### 일정 상태 변경

```bash
NOTION_API_TOKEN=$(jq -r '.api_token' /Users/dhlee/Git/personal/neuron/.credentials/notion.json)

curl -s -X PATCH \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"상태": {"select": {"name": "{STATUS}"}}}}' \
  https://api.notion.com/v1/pages/{PAGE_ID}
```

**Status options:** 예정, 진행중, 완료, 취소

## Output Format

```yaml
schedule:
  - 제목: "팀 미팅"
    날짜: "2025-01-25"
    상태: "예정"
    카테고리: "미팅"
```

## Guardrails

- **NEVER** delete schedules without confirmation
- **ALWAYS** confirm before bulk operations
