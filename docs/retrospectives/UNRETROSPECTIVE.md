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

## Improvements

> System fixes by self-improve agent

| Date | PR | Target | Change | Root Cause |
|------|-----|--------|--------|------------|
| 2026-01-11 | #11 | CLAUDE.md | Add decision signal recognition section | AI lacked guidance to distinguish user decisions from genuine ambiguity |
| 2026-01-11 | #12 | CLAUDE.md | Add architecture check before location decisions | Location decisions bypassed architecture principles (new func -> submodule) |

---

*Auto-updated by reviewer and self-improve agents.*
