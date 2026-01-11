# Git Advanced Operations

## Git Worktree

Use worktrees for parallel work without stashing.

### Setup
```bash
# Create worktree for new branch
git worktree add ../neuron-feature feature/new-feature

# List worktrees
git worktree list

# Remove when done
git worktree remove ../neuron-feature
```

### When to Use
- Working on urgent fix while feature in progress
- Reviewing PR while maintaining current work
- Running tests on different branch simultaneously

## Revert Strategy

### With Claude Code
Claude Code makes frequent, atomic commits. Safe revert approach:

```bash
# View recent commits
git log --oneline -10

# Revert specific commit (creates new commit)
git revert <commit-hash>

# Revert multiple commits
git revert <oldest>..<newest>

# If uncommitted changes need reset
git checkout -- <file>
git restore <file>
```

### Recovery Points
- Commit before major refactors
- Use branches for experimental changes
- `git stash` for temporary saves

## PR Workflow

### 1. Create Branch
```bash
git checkout -b feature/my-feature
```

### 2. Make Commits
- Small, atomic commits
- Each commit should pass tests
- Clear commit messages

### 3. Push & Create PR
```bash
git push -u origin feature/my-feature
gh pr create --title "feat: add feature" --body "Description"
```

### 4. Review Process
- Self-review diff before requesting
- Address feedback with new commits
- Squash merge to main

### 5. Cleanup
```bash
git checkout main
git pull
git branch -d feature/my-feature
```

## Claude Code Collaboration

### Best Practices
- Let Claude commit in small units
- Review diffs before approving
- Use `/pr` command for PR creation
- Revert immediately if issues found
