# Git Workflow Guide

## Commit Convention

Conventional Commits format:
```
<type>(<scope>): <description>

[optional body]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Types
| Type | Purpose |
|------|---------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation only |
| refactor | Code change without feature/fix |
| test | Adding/updating tests |
| chore | Maintenance tasks |
| improve | System self-improvement |

### Rules
- Lowercase type and description
- No period at end
- Imperative mood ("add" not "added")
- Max 72 characters for subject line

## Branch Strategy

### Protected Branches
- `main` - Production ready, always stable
- Direct push disabled, PR required

### Working Branches
```
feature/<name>   # New features
fix/<name>       # Bug fixes
chore/<name>     # Maintenance
docs/<name>      # Documentation
improve/<name>   # System improvements (self-improve agent)
```

### Naming
- Lowercase, hyphen-separated
- Short but descriptive
- Example: `feature/user-auth`, `fix/login-timeout`

### Auto-branch Policy

Claude creates branch names automatically. Do not ask user.

**Format**: `<type>/<short-description>`

**Type mapping** (from commit type):
| Commit Type | Branch Prefix |
|-------------|---------------|
| feat | feature/ |
| fix | fix/ |
| docs | docs/ |
| refactor, chore | chore/ |
| improve | improve/ |

**Description**: 2-4 words from change summary, hyphenated.

**Examples**:
- "docs: add MCP configuration guide" → `docs/mcp-config-guide`
- "feat: add user authentication" → `feature/user-auth`
- "fix: resolve login timeout" → `fix/login-timeout`

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

### Auto-commit Policy

Claude commits autonomously without asking. Do not ask "커밋할까요?".

**Commit when**:
- Logical unit of work complete
- 3+ files changed
- User request fulfilled
- Before context switch

**Ask before commit when**:
- Sensitive files (.env, credentials, secrets)
- Large deletions (10+ lines removed)
- Breaking changes
- Uncertain about scope

### Commit Frequency
- After each logical change
- Before switching context
- After successful test run

### Auto-PR Policy

Development complete → run `/pr` automatically.

**Trigger conditions (ALL must be met)**:
- User request fulfilled
- Code compiles/runs without error
- Commits made

**Skip auto-PR when**:
- Exploratory work (research, prototyping)
- User explicitly says "don't create PR"
- Working on existing PR branch (just push)

**Flow**:
1. Development complete
2. Final commit
3. Run `/pr` → reviewer → PR creation
