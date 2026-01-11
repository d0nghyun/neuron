# Module Management Protocol

## Philosophy

Modules connect to neuron like USB-C devices:
- **Standardized interface**: Consistent structure and metadata
- **Plug and play**: Easy registration and removal
- **Independence**: Each module is a standalone repository

## Structure

```
modules/
  _registry.yaml    # Metadata registry (machine-readable)
  _archived/        # Archived module snapshots (optional)
  hippo/            # Active submodule
  blog/             # Active submodule
```

## Registry Schema

All modules are tracked in `modules/_registry.yaml`:

```yaml
# Module entry schema
module_name:
  repo: github.com/user/repo      # Source repository
  domain: tools | personal | work | experimental
  status: active | maintenance | archived
  description: Brief description
  registered_at: YYYY-MM-DD
  tags: [tag1, tag2]

  # Optional fields
  archived_at: YYYY-MM-DD         # When archived
  archive_reason: completed | abandoned | superseded
  superseded_by: new-module-name  # If replaced
```

### Status Definitions

| Status | Description | Action |
|--------|-------------|--------|
| `active` | Under development or regular use | Normal operations |
| `maintenance` | Stable, minimal changes | Bug fixes only |
| `archived` | No longer active | Removed from submodules |

### Domain Categories

| Domain | Description |
|--------|-------------|
| `tools` | CLI tools, utilities, libraries |
| `personal` | Personal projects (blog, resume, etc.) |
| `work` | Work-related projects |
| `experimental` | Prototypes, experiments |

## Procedures

### Register New Module

```bash
# 1. Add submodule
git submodule add https://github.com/user/repo modules/repo-name

# 2. Update _registry.yaml
# Add entry with status: active

# 3. Commit
git add .gitmodules modules/_registry.yaml modules/repo-name
git commit -m "feat(modules): register repo-name"
```

### Archive Module

```bash
# 1. Update registry status
# Set status: archived, add archived_at and archive_reason

# 2. Optional: Create snapshot
mkdir -p modules/_archived
cp -r modules/module-name modules/_archived/module-name-YYYY-MM-DD

# 3. Remove submodule
git submodule deinit modules/module-name
git rm modules/module-name
rm -rf .git/modules/modules/module-name

# 4. Commit
git add .gitmodules modules/_registry.yaml
git commit -m "chore(modules): archive module-name"
```

### Re-register Archived Module

```bash
# 1. Add submodule back
git submodule add https://github.com/user/repo modules/repo-name

# 2. Update registry
# Set status: active, remove archived_at/archive_reason

# 3. Remove snapshot if exists
rm -rf modules/_archived/repo-name-*

# 4. Commit
git add .gitmodules modules/_registry.yaml modules/repo-name
git commit -m "feat(modules): re-register repo-name"
```

### Update All Submodules

```bash
git submodule update --init --recursive
git submodule foreach git pull origin main
```

## Dashboard Integration

The `_registry.yaml` format enables:
- **Status overview**: Quick view of all module states
- **Domain filtering**: Group by category
- **Timeline**: Registration/archive history
- **Health check**: Detect stale or orphaned modules

Future dashboard can parse this YAML directly.

## Module Interface Standard

Each module SHOULD have:

```
module/
  README.md           # Required: Purpose, setup, usage
  CLAUDE.md           # Recommended: AI-specific instructions
  .claude/            # Optional: Claude Code configuration
```

## Related

- [decision-guide.md](decision-guide.md) - When to create new module
- [repo-setup.md](repo-setup.md) - New repository setup
