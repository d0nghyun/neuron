# GitHub Settings Guide

## Branch Protection Rules

### Main Branch Protection

Enable via: Settings > Branches > Add rule

| Setting | Value |
|---------|-------|
| Branch name pattern | `main` |
| Require PR before merging | Yes |
| Require approvals | 1 (or 0 for solo) |
| Dismiss stale approvals | Yes |
| Require status checks | Optional |
| Require linear history | Recommended |

### Setup Command
```bash
gh api repos/{owner}/{repo}/branches/main/protection \
  -X PUT \
  -f required_pull_request_reviews='{"required_approving_review_count":0}' \
  -f enforce_admins=false
```

## PR Settings

### Merge Options
- **Squash merge**: Recommended (clean history)
- **Merge commit**: For preserving detailed history
- **Rebase**: For linear history without merge commits

### Auto-delete Head Branches
Enable: Settings > General > Automatically delete head branches

## Code Review Policy

### Before Requesting Review
1. Self-review the diff
2. Ensure tests pass
3. Update documentation if needed
4. Check for sensitive data

### Reviewer Guidelines
- Focus on logic, not style
- Suggest, don't demand
- Approve when "good enough"

### Merge Criteria
- All checks passing
- Required approvals met
- No unresolved conversations

## Labels

Recommended labels for PRs:
| Label | Purpose |
|-------|---------|
| `feature` | New functionality |
| `fix` | Bug fixes |
| `docs` | Documentation |
| `refactor` | Code improvement |
| `breaking` | Breaking changes |

## Repository Settings

### General
- Default branch: `main`
- Features: Issues, Projects enabled
- Wikis: Disabled (use knowledge/)

### Security
- Dependency alerts: Enabled
- Dependabot: Optional
- Secret scanning: Enabled
