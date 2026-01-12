# API Tokens Registry

API 토큰 발급 정보 관리. 실제 토큰 값은 `.env.local`에 저장.

## Atlassian (Jira, Confluence)

| Field | Value |
|-------|-------|
| URL | https://id.atlassian.com/manage-profile/security/api-tokens |
| Name | neuron |
| Expires | 2026-12-31 |
| Env Var | `ATLASSIAN_API_TOKEN` |

## GitHub

| Field | Value |
|-------|-------|
| URL | https://github.com/settings/tokens |
| Name | cc |
| Expires | Never |
| Env Var | `GITHUB_PERSONAL_ACCESS_TOKEN` |

## Notion

| Field | Value |
|-------|-------|
| URL | https://www.notion.so/my-integrations |
| Name | neuron |
| Expires | Never |
| Env Var | `NOTION_API_TOKEN` |
