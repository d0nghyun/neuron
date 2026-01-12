---
description: Create a PR from current changes. Includes automated review and release notes via reviewer subagent.
tools: Read, Glob, Grep, Bash, Edit, Task
---

# Create Pull Request

## Steps

1. **Check status**: Review current changes
2. **Run reviewer**: Delegate to reviewer subagent for review + release notes
3. **Handle result**: Process reviewer feedback
4. **Create branch**: If on main, create feature branch
5. **Commit**: Stage and commit with conventional format
6. **Push**: Push branch to origin
7. **Create PR**: Open PR via GitHub API with review summary

## Execution

### Step 1: Gather Information

```bash
git status
git branch --show-current
git diff --stat
```

### Step 2: Run Reviewer Subagent

Use Task tool to invoke the reviewer subagent:

> Review the current code changes. Check code quality, impact, security, and test coverage. Update docs/releasenotes/UNRELEASED.md with the changes. Return approval status and version recommendation.

The reviewer subagent will:
- Perform comprehensive code review
- Update UNRELEASED.md automatically
- Return: approve / changes-requested / blocked

### Step 3: Handle Reviewer Result

| Status | Action |
|--------|--------|
| blocked | Stop. Show issues to user. Require resolution. |
| changes-requested | Warn user. Allow proceed with confirmation. |
| approve | Continue to PR creation. |

### Step 4-7: PR Creation Flow

If on main with changes, ask user for branch name.

```bash
git checkout -b <branch-name>
git add -A
git commit -m "<type>: <description>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push -u origin <branch-name>
```

Create PR with review summary (using GitHub API):

```bash
curl -s -X POST \
  -H "Authorization: Bearer $GITHUB_PERSONAL_ACCESS_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "<type>: <description>",
    "body": "## Summary\n- <changes>\n\n## Review Result\n<reviewer output>\n\n## Test Plan\n- [ ] <verification>",
    "head": "<branch-name>",
    "base": "main"
  }' \
  https://api.github.com/repos/{owner}/{repo}/pulls
```

## Notes

- Always use conventional commit format
- Include Co-Authored-By for Claude commits
- Ask for confirmation before creating PR
- Reviewer subagent runs in independent context
