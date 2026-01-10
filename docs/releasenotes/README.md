# Release Notes

## Structure

```
docs/releasenotes/
├── README.md        # This guide
├── UNRELEASED.md    # Pending changes
└── v{X.Y.Z}.md      # Version-specific notes
```

## Version Format

Semantic Versioning: `v{MAJOR}.{MINOR}.{PATCH}`

| Component | Increment When |
|-----------|----------------|
| MAJOR | Breaking changes |
| MINOR | New features (backward compatible) |
| PATCH | Bug fixes |

## Workflow

1. Changes accumulate in `UNRELEASED.md` (auto-updated by reviewer agent)
2. On release: rename `UNRELEASED.md` → `v{X.Y.Z}.md`
3. Create new empty `UNRELEASED.md`
4. Tag the release

## Sections

| Section | Description |
|---------|-------------|
| Added | New features |
| Changed | Changes to existing features |
| Fixed | Bug fixes |
| Removed | Removed features |
| Security | Security fixes |
| Breaking Changes | Incompatible changes |
