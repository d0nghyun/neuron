---
description: Create a release with version tag. Converts UNRELEASED.md to version file and creates git tag.
tools: Read, Bash, Edit, Write, Task
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

Reset to empty template with sections from [releasenotes README](../../docs/releasenotes/README.md):
- Header: `# Unreleased` with quote `> Changes pending for the next release`
- Sections: Added, Changed, Fixed, Removed, Security, Breaking Changes (each with `-` placeholder)
- Footer: `*Auto-updated by reviewer agent on PR creation.*`

### Step 4b: Convert Retrospective

1. Read `docs/retrospectives/UNRETROSPECTIVE.md`
2. If has content beyond template (any entries in tables or insights):
   - Create `docs/retrospectives/retro-vX.Y.Z.md` with version header, release date, and content
   - Reset UNRETROSPECTIVE.md to empty template

Reset template structure from [retrospectives README](../../docs/retrospectives/README.md):
- Header: `# Unretrospective` with quote `> Learnings pending for the next release`
- Patterns: empty table `| Date | PR | Pattern | Status |`
- Insights: list with `-` placeholder
- Improvements: empty table `| Date | PR | Target | Change | Root Cause |`
- Footer: `*Auto-updated by reviewer and self-improve agents.*`

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
