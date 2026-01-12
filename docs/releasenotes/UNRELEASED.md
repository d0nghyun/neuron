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
- 15th core principle: Verify Before Done - require actual execution and multi-source verification, prevent "looks right" trap
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
- Notion MCP server configuration in `.mcp.json` for resume management integration
- Hippo submodule (modules/hippo) for career documentation as SSOT with structure: resume/, projects/, exports/
- Knowledge file `knowledge/github-api-patterns.md` for GitHub API operations in sandbox environments
- Brain-themed naming convention for submodules (hippo = hippocampus for memory/docs)
- Knowledge file `knowledge/ai-axioms.md` defining foundational axioms (Curiosity, Truth, Beauty) for autonomous AI judgment with conflict resolution hierarchy
- Module management protocol (`knowledge/module-protocol.md`) with:
  - USB-C philosophy for standardized module interface
  - YAML registry (`modules/_registry.yaml`) for machine-readable module tracking
  - Standard procedures: register, archive, re-register
  - Dashboard-ready schema with status (active/maintenance/archived) and domain (tools/personal/work/experimental) categorization
  - Module interface standard (README.md, CLAUDE.md, .claude/)
- PM-arkraft submodule (modules/pm-arkraft) registered with work domain for arkraft project management
- Atlassian MCP server configuration in `.mcp.json` using official endpoint (https://mcp.atlassian.com/v1/sse)
- GitHub and Notion MCP servers in `.mcp.json` with HTTP transport for web sandbox compatibility
- HTTP-first MCP configuration policy documented in `knowledge/extension-mechanisms.md` with transport comparison table (HTTP/SSE/stdio)
- Common MCP server URLs reference table in extension-mechanisms.md (Atlassian, Notion, GitHub)

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
- Applied SSOT principle to documentation structure: consolidated all directory structure references to diagram.md (removed duplicates from README.md and CLAUDE.md)
- Corrected principle count to 15 in CLAUDE.md (now includes "Verify Before Done")
- Changed neuron-knowledge skill to use relative path instead of absolute path for better portability
- Added modules/README.md with naming convention table and task management guidance
- Updated retrospectives with insights from Notion integration work
- Split git-workflow.md into focused files: core workflows (116 lines) + git-advanced.md (85 lines) for worktree, revert strategy, and PR workflow details
- Standardized command metadata format: changed `allowed-tools:` to `tools:` for consistency with agent format
- Consolidated release.md templates (158→85 lines): now references README files instead of duplicating template content (SSOT principle)
- Added cross-references between knowledge files (decision-guide.md, extension-mechanisms.md, spec-process.md) for better navigation
- Made Co-Authored-By an explicit convention in CLAUDE.md Conventions section
- Updated CLAUDE.md Knowledge Files table to include all 10 knowledge files with accurate descriptions
- Updated CLAUDE.md with new Axioms section referencing ai-axioms.md and updated Knowledge Files table to include ai-axioms.md
- Enhanced CLAUDE.md Philosophy section: replaced comma-separated principle list with table format showing principle names and one-line meanings to improve AI comprehension at load time
- Updated CLAUDE.md Navigation table to include `modules/_registry.yaml` entry and Knowledge Files table to include `module-protocol.md`
- Migrated Atlassian and Notion MCP servers from stdio/SSE to HTTP transport in `.mcp.json` for consistency

## Fixed

-

## Removed

- Deleted deprecated docs/improvement-log.md (replaced by retrospectives system)

## Security

- No secrets or credentials detected in codebase
- Security review checklist included in reviewer agent

## Breaking Changes

-

---

*Auto-updated by reviewer agent on PR creation.*
