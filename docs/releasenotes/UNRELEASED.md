# Unreleased

> Changes pending for the next release

## Added

- Initial project setup with hub architecture for personal project management
- Core documentation: README.md with project overview and usage guide
- CLAUDE.md as AI entry point with philosophy summary and conventions
- Knowledge base structure with:
  - `knowledge/git-workflow.md` - Commit conventions, branch strategy, worktree usage
  - `knowledge/github-settings.md` - Branch protection, PR settings, review policy
  - `knowledge/release-workflow.md` - Semantic versioning and release process
- Claude Code configuration:
  - `/pr` command for automated PR creation workflow
  - Reviewer subagent for code review automation
  - Neuron-knowledge skill for referencing project policies
- GitHub integration:
  - Pull request template with summary, changes, test plan, checklist
- Release notes infrastructure in `docs/releasenotes/`
- Submodule structure with `modules/` directory placeholder

## Changed

-

## Fixed

-

## Removed

-

## Security

- No secrets or credentials detected in codebase
- Security review checklist included in reviewer agent

## Breaking Changes

-

---

*Auto-updated by reviewer agent on PR creation.*
