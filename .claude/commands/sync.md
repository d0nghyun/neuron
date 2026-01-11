---
description: Sync local main branch after PR merge. Checkout main, pull latest, and clean up.
tools: Bash
---

# Sync Main Branch

## Purpose

After PR is merged on GitHub, sync local repository to main branch.

## Steps

1. **Checkout main**: Switch to main branch
2. **Pull latest**: Fetch and pull latest changes
3. **Cleanup**: Prune remote-tracking branches, optionally delete merged local branch

## Execution

```bash
# Get current branch name before switching
CURRENT_BRANCH=$(git branch --show-current)

# Switch to main and pull
git checkout main
git pull --prune

# If was on a feature branch, offer to delete it
if [ "$CURRENT_BRANCH" != "main" ]; then
  git branch -d "$CURRENT_BRANCH" 2>/dev/null && echo "Deleted local branch: $CURRENT_BRANCH"
fi
```

## Notes

- Safe operation: uses `-d` (not `-D`) so unmerged branches won't be deleted
- Run after PR is merged on GitHub
- Automatically cleans up the feature branch you were working on
