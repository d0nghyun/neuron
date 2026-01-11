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
- Auto-commit policy in git-workflow.md defining when Claude commits autonomously vs asking first
- Auto-PR policy in git-workflow.md defining when to automatically run /pr after completing work
- Visual system architecture diagram (diagram.md) with ASCII art showing hub structure, immune system, and data flow
- 11th core principle: Constructive Challenge - encouraging critical thinking and productive disagreement

## Changed

- Enhanced CLAUDE.md with Knowledge Files section providing overview of all knowledge base files
- Updated README.md with documentation table clarifying audience (Human vs AI) and purpose for each file
- Updated CLAUDE.md with references to auto-commit and auto-PR policies
- Updated philosophy count from 10 to 11 principles in README.md and CLAUDE.md

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
