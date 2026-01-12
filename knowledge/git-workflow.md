---
id: git-workflow
category: workflow
triggers:
  - "commit"
  - "branch"
  - "PR"
  - "auto-commit"
  - "commit message"
related: [git-advanced, release-workflow, github-settings]
---

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

## Auto-commit Policy

See [git-advanced.md](git-advanced.md) for worktree, revert strategy, and PR workflow details.

### Commit Timing

Claude commits autonomously without asking. Do not ask "Should I commit?".

**Commit when**:
- Logical unit of work complete
- 3+ files changed
- User request fulfilled
- Before context switch

**Ask before commit when**:
- Sensitive files (.env.local, credentials, secrets)
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
