# Module Management Protocol

## Philosophy

Modules connect to neuron like USB-C devices:
- **Standardized interface**: Consistent structure and metadata
- **Plug and play**: Easy registration and removal
- **Independence**: Each module is a standalone repository

## Independence Requirement

Submodules must work standalone when cloned independently.

**DO NOT use parent-relative paths** like `../../knowledge/`.
These create physical dependency on parent repo structure.

**DO inline core policies** in submodule CLAUDE.md.
Reference neuron conceptually (GitHub URL) but don't depend on it physically.

| Pattern | Status | Why |
|---------|--------|-----|
| `[neuron-base.md](../../knowledge/neuron-base.md)` | WRONG | Breaks standalone |
| Inline policies + GitHub URL reference | CORRECT | Works everywhere |

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

### Rename Module

```bash
# 1. Move submodule
git mv modules/old-name modules/new-name

# 2. Update .gitmodules path
# Change [submodule "modules/old-name"] → [submodule "modules/new-name"]

# 3. Update .git/config
git submodule sync

# 4. Update _registry.yaml (change key name)

# 5. Commit
git add .gitmodules modules/_registry.yaml
git commit -m "refactor(modules): rename old-name to new-name"
```

**Note**: After pulling, run `git submodule update --init modules/new-name`.

### Update All Submodules

```bash
git submodule update --init --recursive
git submodule foreach git pull origin main
```

### Verify Inheritance

When registering or auditing a module:

```bash
# Check CLAUDE.md has inlined policies
grep -A5 "## Inherited Policies" modules/<repo>/CLAUDE.md
```

**Checklist:**
- [ ] CLAUDE.md exists in module root
- [ ] Contains `## Inherited Policies` section with inlined table
- [ ] References neuron via GitHub URL (not relative path)
- [ ] Works standalone when cloned independently
- [ ] Configurable policy overrides documented with reasons

**Common Issues:**

| Issue | Fix |
|-------|-----|
| Missing CLAUDE.md | Create using repo-setup.md template |
| Parent-relative path `../../` | Replace with inlined policies |
| Undocumented override | Add to Configurable table with reason |

## Dashboard Integration

`_registry.yaml` enables status overview, domain filtering, timeline tracking, and health checks.

## Module Interface Standard

Each module MUST have:

```
module/
  README.md           # Required: Purpose, setup, usage
  CLAUDE.md           # Required: AI instructions with inlined policies
  .claude/            # Optional: Claude Code configuration
```

CLAUDE.md must include `## Inherited Policies` section with inlined policy table.
Do NOT use parent-relative paths. See [repo-setup.md](repo-setup.md) for template.

## Related

- [decision-guide.md](decision-guide.md) - When to create new module
- [repo-setup.md](repo-setup.md) - New repository setup
