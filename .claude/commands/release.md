---
description: Create a release with version tag. Converts UNRELEASED.md to version file and creates git tag.
allowed-tools: Read, Bash, Edit, Write, Task
---

# Create Release

## Steps

1. **Check UNRELEASED.md**: Verify there are changes to release
2. **Determine version**: Analyze changes for version bump
3. **Convert release notes**: UNRELEASED.md → vX.Y.Z.md
4. **Create new UNRELEASED.md**: Reset for next cycle
5. **Commit**: Stage and commit release notes
6. **Create tag**: git tag vX.Y.Z
7. **Push**: Push commit and tag to origin

## Execution

### Step 1: Check UNRELEASED.md

Read `docs/releasenotes/UNRELEASED.md` and verify it has content beyond the template.

If empty (only template placeholders), abort with message: "No changes to release."

### Step 2: Determine Version

Check existing tags:
```bash
git tag -l 'v*' --sort=-v:refname | head -5
```

Analyze UNRELEASED.md content:
- Breaking Changes section has content → MAJOR bump
- Added section has content → MINOR bump
- Only Fixed/Changed → PATCH bump

Ask user to confirm version number.

### Step 3: Convert Release Notes

1. Read UNRELEASED.md content
2. Create `docs/releasenotes/vX.Y.Z.md` with:
   - Version header
   - Release date (today)
   - Content from UNRELEASED.md

### Step 4: Reset UNRELEASED.md

Write fresh template to UNRELEASED.md:

```markdown
# Unreleased

> Changes pending for the next release

## Added

-

## Changed

-

## Fixed

-

## Removed

-

## Security

-

## Breaking Changes

-

---

*Auto-updated by reviewer agent on PR creation.*
```

### Step 4b: Convert Retrospective

1. Read `docs/retrospectives/UNRETROSPECTIVE.md`
2. If has content beyond template (any entries in tables or insights):
   - Create `docs/retrospectives/retro-vX.Y.Z.md` with header and content
   - Reset UNRETROSPECTIVE.md to template

Template for retro-vX.Y.Z.md:
```markdown
# Retrospective vX.Y.Z

> Release: YYYY-MM-DD

## Patterns

<copy from UNRETROSPECTIVE.md>

## Insights

<copy from UNRETROSPECTIVE.md>

## Improvements

<copy from UNRETROSPECTIVE.md>
```

Reset UNRETROSPECTIVE.md template:
```markdown
# Unretrospective

> Learnings pending for the next release

## Patterns

> Recurring issues detected by reviewer agent

| Date | PR | Pattern | Status |
|------|-----|---------|--------|

## Insights

> What worked well, lessons learned (updated by reviewer on each PR)

-

## Improvements

> System fixes by self-improve agent

| Date | PR | Target | Change | Root Cause |
|------|-----|--------|--------|------------|

---

*Auto-updated by reviewer and self-improve agents.*
```

### Step 5-7: Commit, Tag, Push

```bash
git add docs/releasenotes/ docs/retrospectives/
git commit -m "chore: release vX.Y.Z

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git tag vX.Y.Z
git push origin main --tags
```

## Notes

- Always confirm version with user before creating tag
- Tags trigger GitHub Actions (if configured)
- After release, UNRELEASED.md is ready for next cycle
