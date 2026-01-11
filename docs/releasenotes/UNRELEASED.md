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
  - `knowledge/decision-guide.md` - Project scope and MCP placement decision frameworks
  - `knowledge/extension-mechanisms.md` - When to use skills/MCP/subagent/command/hook
  - `knowledge/spec-process.md` - Scenario-based specification development methodology
- Claude Code configuration:
  - `/pr` command for automated PR creation workflow
  - Reviewer subagent for code review automation
  - Neuron-knowledge skill for referencing project policies
- GitHub integration:
  - Pull request template with summary, changes, test plan, checklist
- Release notes infrastructure in `docs/releasenotes/`
- Submodule structure with `modules/` directory placeholder

## Changed

- Enhanced CLAUDE.md with Knowledge Files section providing overview of all knowledge base files

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
