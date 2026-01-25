# Repository Setup Guide

## New Repository Checklist

### Required Files
| File | Purpose |
|------|---------|
| `README.md` | Project overview |
| `CLAUDE.md` | AI instructions |
| `.gitignore` | Ignore patterns |

### Optional Files
| File | When Needed |
|------|-------------|
| `LICENSE` | Open source projects |
| `.github/workflows/` | CI/CD automation |
| `package.json` / `pyproject.toml` | Package management |

## CLAUDE.md Template

```markdown
# Project Name

## Critical Rules

1. **Principle-Based Reasoning**: Every decision MUST cite principle(s).
   - Format: `[P#] decision`
   - No decision without principle backing

2. **Autonomous Execution** [P13]: Act first, ask only when truly blocked.

## Overview

Brief description of what this project does.

## Inherited Policies

This project follows [neuron](https://github.com/d0nghyun/neuron) conventions.

### Principles Reference

| # | Principle | When to Apply |
|---|-----------|---------------|
| P1 | SSOT | One source, no duplication |
| P3 | Simplicity First | Simple over complex |
| P4 | Incremental | Build only what's needed now |
| P13 | Autonomous Execution | Act first, ask only when blocked |
| P15 | Verify Before Done | Prove it works |

### Required (cannot override)

| Policy | Summary |
|--------|---------|
| 3 Axioms | Curiosity, Truth, Beauty |
| SSOT | Single source of truth, no duplication |
| Verify Before Done | Prove it works, don't assume |
| Conventional Commits | `type(scope): description` |
| Co-Authored-By | `Claude Opus 4.5 <noreply@anthropic.com>` |

### Configurable

| Policy | Default | This Project |
|--------|---------|--------------|
| Language | English only | (override or keep default) |
| Test-First | Required | (override or keep default) |

## Commands

| Command | Purpose |
|---------|---------|
| `npm test` | Run tests |

## Key Files

| File | Purpose |
|------|---------|
| `src/` | Source code |
```

**IMPORTANT**: Do NOT use parent-relative paths like `../../knowledge/`.
Submodules must work standalone when cloned independently.

## Registering as Submodule

### 1. Create Repository
```bash
# Create new repo on GitHub via API
curl -s -X POST \
  -H "Authorization: Bearer $GITHUB_PERSONAL_ACCESS_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -H "Content-Type: application/json" \
  -d '{"name":"<repo-name>","private":true}' \
  https://api.github.com/user/repos

# Clone and initialize
git clone git@github.com:<user>/<repo-name>.git
cd <repo-name>
echo "# Project Name" > README.md
touch CLAUDE.md .gitignore
git add . && git commit -m "chore: initial setup"
git push -u origin main
```

### 2. Add to Neuron
```bash
cd /path/to/neuron
git submodule add git@github.com:<user>/<repo>.git modules/<repo>
git commit -m "chore: add <repo> submodule"
```

### 3. Configure GitHub Settings
Apply settings from `github-settings.md`:
- Branch protection on `main`
- Auto-delete head branches
- Squash merge default

```bash
# Quick setup via GitHub API
curl -s -X PUT \
  -H "Authorization: Bearer $GITHUB_PERSONAL_ACCESS_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -H "Content-Type: application/json" \
  -d '{"required_pull_request_reviews":{"required_approving_review_count":0},"enforce_admins":false}' \
  https://api.github.com/repos/{owner}/{repo}/branches/main/protection
```

## Working with Submodules

### Start Development
```bash
# From Neuron root, enter submodule
cd modules/<repo>

# Work normally - git commands apply to submodule
git checkout -b feature/new-feature
# ... make changes ...
git commit -m "feat: add feature"
git push
```

### Update Submodule Reference
After submodule commits, update Neuron:
```bash
cd /path/to/neuron
git add modules/<repo>
git commit -m "chore: update <repo> submodule"
```

### Clone with Submodules
```bash
git clone --recurse-submodules <neuron-url>
# or after clone
git submodule update --init --recursive
```

## Project Type Templates

### Node.js
```
.gitignore: node_modules/, dist/, .env.local
Commands: npm test, npm run build, npm start
```

### Python
```
.gitignore: __pycache__/, .venv/, *.pyc
Commands: pytest, python -m build
```

### Go
```
.gitignore: /bin/, *.exe
Commands: go test ./..., go build
```

## Validation Checklist

Before first PR:
- [ ] CLAUDE.md has correct commands
- [ ] CLAUDE.md has `## Inherited Policies` with inlined table
- [ ] No parent-relative paths (works standalone)
- [ ] Configurable policy overrides documented with reasons
- [ ] README.md explains the project
- [ ] .gitignore covers build artifacts
- [ ] Branch protection enabled
- [ ] At least one test exists
