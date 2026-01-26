---
name: workflow-pr
description: Create a PR from current changes. Includes automated review and release notes via code-review skill.
allowed-tools: Read, Glob, Grep, Bash, Edit, Task
user-invocable: true
---

# Create Pull Request

## When to Activate

- User runs `/pr` command
- User asks to create a pull request
- Feature is ready for review

## Steps

1. **Check status**: Review current changes
2. **Run code review**: Invoke workflow-code-review skill for review + release notes
3. **Handle result**: Process review feedback
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

### Step 2: Invoke Code Review Skill

Use Skill tool to invoke workflow-code-review:

```
Skill: workflow-code-review
```

The skill will:
- Perform comprehensive code review (quality, impact, security, tests)
- Update docs/releasenotes/UNRELEASED.md automatically
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

Create PR with review summary (using gh CLI):

```bash
gh pr create --title "<type>: <description>" \
  --body "## Summary
- <changes>

## Review Result
<reviewer output>

## Test Plan
- [ ] <verification>"
```

## Notes

- Always use conventional commit format
- Include Co-Authored-By for Claude commits
- Ask for confirmation before creating PR
- workflow-code-review skill handles review and release notes
