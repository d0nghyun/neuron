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
- Refactor agent (.claude/agents/refactor.md) for judging when and how to refactor code with:
  - Need assessment preventing unnecessary refactoring
  - Anti-pattern detection (premature abstraction, speculative generality, etc.)
  - Scope control (surgical → module → cross-cutting → architectural)
  - Incremental planning with atomic steps
  - Strong guardrails against big bang rewrites and untested changes
- Retrospective documentation system (`docs/retrospectives/`) with:
  - UNRETROSPECTIVE.md for accumulating learnings (Patterns, Insights, Improvements)
  - Flush mechanism to retro-vX.Y.Z.md on release
  - Machine-readable table format for future pattern detection

## Changed

- Enhanced CLAUDE.md with Knowledge Files section providing overview of all knowledge base files
- Updated README.md with documentation table clarifying audience (Human vs AI) and purpose for each file
- Updated CLAUDE.md with references to auto-commit and auto-PR policies
- Updated philosophy count from 10 to 11 principles in README.md and CLAUDE.md
- Enhanced extension-mechanisms.md with detailed MCP configuration documentation including .mcp.json file location, structure, format example, and activation settings via .claude/settings.local.json
- Added auto-branch policy to git-workflow.md for automatic branch naming without user prompts
- Updated reviewer agent with Step 7b for logging patterns and insights to UNRETROSPECTIVE.md
- Updated self-improve agent with Step 8b for logging improvements to UNRETROSPECTIVE.md
- Updated release command with Step 4b for flushing retrospectives on release
- Deprecated improvement-log.md in favor of retrospectives system

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
