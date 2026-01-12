# Unretrospective

> Learnings pending for the next release

## Patterns

> Recurring issues detected by reviewer agent

| Date | PR | Pattern | Status |
|------|-----|---------|--------|
| 2026-01-11 | #12 | Location decision vs architecture decision confusion | pending |
| 2026-01-11 | #15 | Language convention violation - non-English content in knowledge files | pending |
| 2026-01-12 | #21 | Language convention violation - Korean content in api-tokens.md | pending |

## Insights

> What worked well, lessons learned (updated by reviewer on each PR)

- 2026-01-11: Executed "put in docs" as location decision immediately, but overlooked neuron architecture principle (submodule separation) - Decision Signal didn't distinguish "where to store" from "which repo it belongs to"
- 2026-01-11: Adding retrospective step to reviewer creates self-reinforcing learning loop - immune system now learns from its own reviews
- 2026-01-11: Simple table-based format in UNRETROSPECTIVE.md makes pattern tracking machine-readable and actionable
- 2026-01-11: SSOT refactoring demonstrates principle in action - eliminating 3 duplicate directory structures reduces maintenance burden and prevents drift
- 2026-01-11: Decision-guide.md alignment verified - Notion MCP placement and docs submodule both follow documented decision frameworks perfectly
- 2026-01-11: Small focused changes (2 files + submodule) demonstrate Incremental principle - adding only what's needed for Notion integration
- 2026-01-11: Sandbox environment without gh CLI → GitHub API via curl patterns work well, documented in knowledge/github-api-patterns.md
- 2026-01-11: Brain-themed naming convention (hippo=hippocampus for memory/docs) adds personality while maintaining semantic meaning
- 2026-01-11: Multiple small commits (5 atomic commits) made review easier - each change independently reviewable and revertible
- 2026-01-11: Documentation-as-discovery pattern effective - github-api-patterns.md captured working solutions discovered during actual implementation
- 2026-01-11: SSOT refactoring reduces net lines (177 deletions vs 123 additions = -54 lines) while improving organization - duplication removal achieved simplification goal
- 2026-01-11: MECE principle in file splitting - clear boundary between git-workflow.md (basics, 116 lines) and git-advanced.md (advanced ops, 85 lines) prevents overlap
- 2026-01-11: Standardization across agent/command formats (`allowed-tools:` → `tools:`) demonstrates consistency pattern - small changes compound into better UX
- 2026-01-11: Cross-references between knowledge files improve discoverability without duplication - maintains SSOT while enabling multi-entry navigation
- 2026-01-11: Single refactor commit with focused scope demonstrates Agile principle - small change, clear boundary, easy to review and revert
- 2026-01-11: Language convention violation detected early by review process - English-only policy (CLAUDE.md line 67) critical for AI-First principle and machine-readability
- 2026-01-11: Good conceptual work (AI axioms for judgment) can still be blocked by convention violations - foundation matters as much as content
- 2026-01-11: Quick convention fix (Korean → English translation) demonstrates responsive correction - blocked status resolved in single commit, review-fix-approve cycle worked efficiently
- 2026-01-11: CLAUDE.md Philosophy table enhancement demonstrates AI-First principle - exposing principle meanings at load time solves root cause of AI misunderstanding (seeing names without semantics)
- 2026-01-11: USB-C philosophy analogy makes module protocol memorable and intuitive - complex system design communicated through familiar metaphor
- 2026-01-11: Machine-readable YAML registry enables future tooling without locking into specific implementation - dashboard-ready design demonstrates forward-thinking architecture
- 2026-01-11: Module protocol demonstrates SSOT principle - single source for module metadata prevents drift between .gitmodules and documentation
- 2026-01-11: Flat structure + registry approach beats nested hierarchies for AI parsing - simple structure with metadata wins over complex directory organization
- 2026-01-12: Work domain submodule registration follows module-protocol.md exactly - consistent process makes adding new modules predictable and low-friction
- 2026-01-12: Official MCP endpoints (Atlassian) demonstrate ecosystem maturity - using https://mcp.atlassian.com/v1/sse instead of custom server simplifies configuration
- 2026-01-12: HTTP transport migration demonstrates Simplicity First - removing stdio/SSE complexity unifies on single transport type with better compatibility
- 2026-01-12: Web sandbox compatibility consideration shows forward-thinking - HTTP-first policy prevents future friction when using Claude Code in browser
- 2026-01-12: Common MCP URLs reference table demonstrates AI-First - machine-readable format makes future MCP additions copy-paste easy
- 2026-01-12: Strategic architecture pivot (OAuth MCP → API Skills) solves root cause - browser authentication incompatible with headless/CI environments, token-based approach enables automation
- 2026-01-12: Consistent skill structure across services (github-api, jira-api, notion-api) demonstrates modularity - each skill independent, easily replaceable, follows same pattern
- 2026-01-12: Moving secrets from tracked (.mcp.json) to gitignored (.env) demonstrates security-first thinking - prevents accidental credential exposure
- 2026-01-12: Breaking change well-documented in release notes - migration path clear (see .env.example), rationale explicit (headless automation)
- 2026-01-12: Comprehensive gh CLI replacement demonstrates thoroughness - all 5 documentation files updated consistently, no partial migration
- 2026-01-12: Confluence API Skill follows established pattern - same structure as github-api, jira-api, notion-api ensures consistency and maintainability
- 2026-01-12: Terminology alignment (MCP → API Skills) demonstrates SSOT principle - single consistent term across all documentation
- 2026-01-12: ATLASSIAN_* variable consolidation demonstrates DRY - single set of credentials serves both Jira and Confluence APIs
- 2026-01-12: Small documentation-only refactor (3 commits, 10 files) demonstrates Incremental principle - focused scope, clear intent, easy to review

## Improvements

> System fixes by self-improve agent

| Date | PR | Target | Change | Root Cause |
|------|-----|--------|--------|------------|
| 2026-01-11 | #11 | CLAUDE.md | Add decision signal recognition section | AI lacked guidance to distinguish user decisions from genuine ambiguity |
| 2026-01-11 | #12 | CLAUDE.md | Add architecture check before location decisions | Location decisions bypassed architecture principles (new func -> submodule) |
| 2026-01-12 | #21 | decision-guide.md | Update MCP terminology to API Skills | MCP-to-API-Skills migration updated extension-mechanisms.md but not decision-guide.md |

---

*Auto-updated by reviewer and self-improve agents.*
