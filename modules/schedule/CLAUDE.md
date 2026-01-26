# Schedule Module

Notion-based schedule management for personal productivity.

## Inherited Policies

From [neuron](../../../CLAUDE.md) (parent)

### Required (Cannot Override)

| Policy | Summary |
|--------|---------|
| SSOT | One source, no duplication |
| Language | English only for all documentation |
| Verify Before Done | Prove it works |

### Configurable

| Policy | Default | This Module |
|--------|---------|-------------|
| Test-First | Required | N/A (no code, API workflow) |

## Skills

| Skill | Purpose |
|-------|---------|
| `workflow-schedule-notion` | Query, add, update schedules via Notion API |

## Usage

Activate module:
```
/workflow-init-module schedule
```

Or use skill directly:
```
/workflow-schedule-notion
```

## Configuration

| Item | Value |
|------|-------|
| Notion DB ID | `2f346706-90ca-8108-b838-dd5861292951` |
| Credentials | `.credentials/notion.json` |

## Notion DB Schema

> Property names are in Korean to match actual DB schema.

| Property | Korean | Type | Values |
|----------|--------|------|--------|
| Title | 제목 | title | - |
| Date | 날짜 | date | YYYY-MM-DD |
| Status | 상태 | select | 예정, 진행중, 완료, 취소 |
| Category | 카테고리 | select | 업무, 개인, 미팅, 기타 |
| Memo | 메모 | rich_text | - |

## Guardrails

- **NEVER** delete schedules without confirmation
- **ALWAYS** confirm before bulk operations
- **ALWAYS** use English for documentation (Korean only for Notion DB property names)

## Conventions

- **Language:** English (inherits from neuron)
- **API:** Notion REST API v2022-06-28
- **SSOT:** Notion Database (not local files)
