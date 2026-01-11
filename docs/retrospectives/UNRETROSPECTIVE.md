# Unretrospective

> Learnings pending for the next release

## Patterns

> Recurring issues detected by reviewer agent

| Date | PR | Pattern | Status |
|------|-----|---------|--------|
| 2026-01-11 | #12 | Location decision vs architecture decision confusion | pending |

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

## Improvements

> System fixes by self-improve agent

| Date | PR | Target | Change | Root Cause |
|------|-----|--------|--------|------------|
| 2026-01-11 | #11 | CLAUDE.md | Add decision signal recognition section | AI lacked guidance to distinguish user decisions from genuine ambiguity |
| 2026-01-11 | #12 | CLAUDE.md | Add architecture check before location decisions | Location decisions bypassed architecture principles (new func -> submodule) |

---

*Auto-updated by reviewer and self-improve agents.*
