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

## Overview
Brief description of what this project does.

## Inherits
This project follows Neuron policies (parent directory).

## Commands
| Command | Purpose |
|---------|---------|
| `npm test` | Run tests |
| `npm run build` | Build project |

## Project Rules
- (Project-specific conventions)
- (Tech stack notes)

## Key Files
| File | Purpose |
|------|---------|
| `src/` | Source code |
| `tests/` | Test files |
```

## Registering as Submodule

### 1. Create Repository
```bash
# Create new repo on GitHub
gh repo create <repo-name> --private --clone
cd <repo-name>

# Initialize with required files
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
# Quick setup via gh CLI
gh api repos/{owner}/{repo}/branches/main/protection \
  -X PUT \
  -f required_pull_request_reviews='{"required_approving_review_count":0}' \
  -f enforce_admins=false
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
.gitignore: node_modules/, dist/, .env
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
- [ ] README.md explains the project
- [ ] .gitignore covers build artifacts
- [ ] Branch protection enabled
- [ ] At least one test exists
