# Unretrospective

> Learnings pending for the next release

## Patterns

> Recurring issues detected by reviewer agent

| Date | PR | Pattern | Status |
|------|-----|---------|--------|
| 2026-01-11 | #12 | Location decision vs architecture decision confusion | pending |
| 2026-01-11 | #15 | Language convention violation - non-English content in knowledge files | pending |
| 2026-01-12 | #21 | Language convention violation - Korean content in api-tokens.md | pending |
| 2026-01-12 | #TBD | Language convention violation - Korean content in advisor.md, _index.yaml, data-pipeline.md, CLAUDE.md | pending |

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
- 2026-01-12: Moving secrets from tracked (.mcp.json) to gitignored (.env.local) demonstrates security-first thinking - prevents accidental credential exposure
- 2026-01-12: Breaking change well-documented in release notes - migration path clear (see .env.example), rationale explicit (headless automation)
- 2026-01-12: Comprehensive gh CLI replacement demonstrates thoroughness - all 5 documentation files updated consistently, no partial migration
- 2026-01-12: Confluence API Skill follows established pattern - same structure as github-api, jira-api, notion-api ensures consistency and maintainability
- 2026-01-12: Terminology alignment (MCP → API Skills) demonstrates SSOT principle - single consistent term across all documentation
- 2026-01-12: ATLASSIAN_* variable consolidation demonstrates DRY - single set of credentials serves both Jira and Confluence APIs
- 2026-01-12: Small documentation-only refactor (3 commits, 10 files) demonstrates Incremental principle - focused scope, clear intent, easy to review
- 2026-01-12: GitLab API integration enables internal repo access - ark/arkraft group contains alpha-agent, arkraft-fe, pm-arkraft projects
- 2026-01-12: Environment variable loading pattern (export $(grep -v '^#' .env.local | xargs)) enables API calls without sourcing
- 2026-01-12: pm-arkraft as central hub connecting Confluence (docs), Jira (issues), GitLab (code) demonstrates integration-first approach
- 2026-01-12: Capturing Confluence page IDs in CLAUDE.md enables programmatic access without URL parsing
- 2026-01-12: Documentation consistency fix (`.env` → `.env.local`) across 2 knowledge files demonstrates thoroughness - systematic correction prevents confusion
- 2026-01-12: Configuration-only changes (no skill implementation yet) demonstrate Incremental principle - add environment variables first, implementation later when needed
- 2026-01-12: Advisor agent introduces intelligent decision layer - reduces unnecessary AskUser calls while maintaining user control through confidence levels
- 2026-01-12: Knowledge index system (_index.yaml) demonstrates AI-First principle - trigger map enables automatic knowledge discovery without manual search
- 2026-01-12: Data pipeline pattern addresses root cause of context bloat - systematic approach (Fetch → Transform → Interpret) prevents token waste
- 2026-01-12: Frontmatter metadata in knowledge files improves discoverability - machine-readable triggers, categories, and relations enable autonomous navigation
- 2026-01-12: Fourth consecutive language convention violation signals systemic issue - reactive review catching not preventing non-English content creation
- 2026-01-12: /backlog command demonstrates Automate Repetition principle - codifies task extraction pattern that was done manually repeatedly
- 2026-01-12: SSOT implementation in action - removing redundant YAML frontmatter (36 lines deleted) consolidates knowledge metadata into single _index.yaml source
- 2026-01-12: Documentation consistency refactor demonstrates systematic thinking - fixing missing principle, documenting commands, and cleaning up SSOT violations in single logical commit
- 2026-01-12: Two-commit structure (feature + refactor) shows good separation of concerns - new functionality isolated from cleanup work
- 2026-01-12: Jira API endpoint change (/search → /search/jql) discovered during implementation - API deprecation caught and fixed in skill documentation immediately
- 2026-01-12: /status command demonstrates On-Demand over Auto-Sync pattern - SSOT preserved (Confluence is source), no stale data risk, explicit user control
- 2026-01-12: Confluence as status SSOT over git file - team sharing easier, version history built-in, no merge conflicts on status updates
- 2026-01-12: Submodule-specific commands (.claude/commands/) enable project-local customization while inheriting parent policies
- 2026-01-12: neuron-base.md inheritance contract solves vague "follows Neuron policies" problem - explicit reference file with SSOT links prevents policy drift
- 2026-01-12: Required vs Configurable policy separation demonstrates bounded flexibility - core axioms immutable, operational details overridable with documentation
- 2026-01-12: Override protocol with documented reasons enables legitimate exceptions while maintaining transparency - pm-arkraft Korean override justified by client requirement
- 2026-01-12: Verification checklist with grep command demonstrates automation-first thinking - manual audit made scriptable
- 2026-01-12: CLAUDE.md made required (was recommended) for modules - policy clarification strengthens contract without breaking existing submodules
- 2026-01-12: Inheritance mechanism enables consistent policy enforcement across 2+ submodules without duplication - scales better than inline policy docs in each CLAUDE.md
- 2026-01-12: Formalizing existing practice as principle strengthens system - retrospectives already existed, "Learn from Failure" principle makes it explicit and traceable to axioms
- 2026-01-12: Small documentation changes (5 lines) can have high strategic value - connecting existing mechanism to philosophy creates conceptual clarity
- 2026-01-12: Principle #17 demonstrates meta-learning - system now has formal principle about learning from failures, closing the feedback loop

## Improvements

> System fixes by self-improve agent

| Date | PR | Target | Change | Root Cause |
|------|-----|--------|--------|------------|
| 2026-01-11 | #11 | CLAUDE.md | Add decision signal recognition section | AI lacked guidance to distinguish user decisions from genuine ambiguity |
| 2026-01-11 | #12 | CLAUDE.md | Add architecture check before location decisions | Location decisions bypassed architecture principles (new func -> submodule) |
| 2026-01-12 | #21 | decision-guide.md | Update MCP terminology to API Skills | MCP-to-API-Skills migration updated extension-mechanisms.md but not decision-guide.md |
| 2026-01-12 | #28 | CLAUDE.md | Add CRITICAL language enforcement warning | 4+ language violations - reactive review not preventing non-English content |
| 2026-01-12 | #29 | CLAUDE.md | Add CRITICAL Advisor-before-AskUser enforcement | AI skipped Advisor agent, asked user questions that knowledge could answer |

---

*Auto-updated by reviewer and self-improve agents.*
