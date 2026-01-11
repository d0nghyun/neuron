# GitHub API Patterns

When `gh` CLI is unavailable (sandbox, restricted environments), use curl with GitHub API.

## Authentication

```bash
# Use GH_TOKEN environment variable
curl -H "Authorization: token $GH_TOKEN" ...
```

## Common Operations

### Create Repository

```bash
curl -s -X POST \
  -H "Authorization: token $GH_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/user/repos" \
  -d '{"name":"repo-name","private":true,"description":"..."}'
```

### Rename Repository

```bash
curl -s -X PATCH \
  -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/OWNER/REPO" \
  -d '{"name":"new-name"}'
```

### Create File

```bash
CONTENT=$(cat file.md | base64 -w 0)
curl -s -X PUT \
  -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/OWNER/REPO/contents/path/file.md" \
  -d "{\"message\":\"commit msg\",\"content\":\"$CONTENT\"}"
```

### Create Pull Request

```bash
curl -s -X POST \
  -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/OWNER/REPO/pulls" \
  -d '{"title":"...","head":"branch","base":"main","body":"..."}'
```

## Submodule with Token

```bash
TOKEN=$(echo -n "$GH_TOKEN" | tr -d ' \n')
git submodule add "https://${TOKEN}@github.com/OWNER/REPO.git" path/
# Then remove token from .gitmodules before committing
```
