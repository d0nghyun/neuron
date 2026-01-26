# Release Notes Format Reference

Guidelines for mapping changes to release notes sections.

## Commit Type → Section Mapping

| Commit Type | Release Notes Section | Example Entry |
|-------------|----------------------|---------------|
| feat | Added | New user authentication module |
| fix | Fixed | Resolved memory leak in cache handler |
| refactor | Changed | Simplified database query logic |
| perf | Changed | Improved API response time by 40% |
| docs | Changed | Updated installation instructions |
| BREAKING | Breaking Changes | Removed deprecated v1 API endpoints |
| chore | (skip) | Internal tooling updates |
| test | (skip) | Test coverage improvements |
| ci | (skip) | Pipeline configuration changes |

## Section Order

Release notes should follow this section order:

1. **Breaking Changes** (if any)
2. **Added** (new features)
3. **Changed** (modifications, improvements)
4. **Fixed** (bug fixes)
5. **Deprecated** (upcoming removals)
6. **Removed** (deleted features)
7. **Security** (vulnerability fixes)

## Entry Format

Each entry should be:
- One line, concise description
- User-facing impact, not implementation details
- Present tense ("Add" not "Added")

```markdown
## Added
- Add dark mode toggle in settings
- Add export to CSV functionality

## Fixed
- Fix login timeout on slow connections
- Fix incorrect date formatting in reports
```

## Version Determination

| Change Type | Version Bump |
|-------------|--------------|
| Breaking changes | Major (X.0.0) |
| New features | Minor (0.X.0) |
| Bug fixes only | Patch (0.0.X) |

## File Location

Release notes are maintained in:
- `docs/releasenotes/UNRELEASED.md` - Current work in progress
- `docs/releasenotes/vX.Y.Z.md` - Released versions
