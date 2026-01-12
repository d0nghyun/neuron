---
name: github-api
description: GitHub REST API for issues, PRs, repos. Uses PAT for headless/CI. Activate for GitHub operations.
allowed-tools: Bash, Read, Grep
---

# GitHub API Skill

## When to Activate

- Create/read/update issues
- Manage pull requests
- Query repository information
- Access GitHub Actions status

## Authentication

**Environment Variable**: `GITHUB_PERSONAL_ACCESS_TOKEN`

Create at: https://github.com/settings/tokens

Required scopes:
- `repo` - Full repository access
- `workflow` - GitHub Actions (optional)

## API Base URL

```
https://api.github.com
```

## Common Operations

### Get Authenticated User
```bash
curl -s -H "Authorization: Bearer $GITHUB_PERSONAL_ACCESS_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user
```

### List Repository Issues
```bash
curl -s -H "Authorization: Bearer $GITHUB_PERSONAL_ACCESS_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/{owner}/{repo}/issues?state=open"
```

### Create Issue
```bash
curl -s -X POST \
  -H "Authorization: Bearer $GITHUB_PERSONAL_ACCESS_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -H "Content-Type: application/json" \
  -d '{"title":"Issue title","body":"Issue body","labels":["bug"]}' \
  https://api.github.com/repos/{owner}/{repo}/issues
```

### Get Pull Request
```bash
curl -s -H "Authorization: Bearer $GITHUB_PERSONAL_ACCESS_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}
```

### Create Pull Request
```bash
curl -s -X POST \
  -H "Authorization: Bearer $GITHUB_PERSONAL_ACCESS_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -H "Content-Type: application/json" \
  -d '{"title":"PR title","body":"PR body","head":"feature-branch","base":"main"}' \
  https://api.github.com/repos/{owner}/{repo}/pulls
```

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Invalid token | Check GITHUB_PERSONAL_ACCESS_TOKEN |
| 403 | Rate limit or scope | Wait or check permissions |
| 404 | Not found or no access | Verify repo/resource exists |

## Rate Limits

- Authenticated: 5,000 requests/hour
- Check: `X-RateLimit-Remaining` header

## References

- [GitHub REST API Docs](https://docs.github.com/en/rest)
