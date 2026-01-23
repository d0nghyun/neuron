# Unretrospective

> Learnings pending for the next release

## Patterns

> Recurring issues detected by reviewer agent

| Date | PR | Pattern | Status |
|------|-----|---------|--------|
| 2026-01-23 | arkraft-agent-insight | Task verification workflow not followed for refactoring tasks | pending |
| 2026-01-23 | arkraft-agent-insight | Subagent added without corresponding test coverage | pending |
| 2026-01-23 | arkraft-agent-pm#1 | Language policy violation - Korean content in English-only repo without detection | pending |

## Insights

> What worked well, lessons learned (updated by reviewer on each PR)

- 2026-01-23: Modular subagent design (planner) effectively separated concerns between request parsing and insight generation
- 2026-01-23: Visual architecture diagrams in README greatly improved comprehension of multi-agent flow
- 2026-01-23: Using cheaper Haiku model for deterministic parsing demonstrates good cost optimization (P16 Automate Repetition)
- 2026-01-23: Boot/wrapup agent design creates enforced memory system - instructions become executable workflows (P20 Sustainable by Design)
- 2026-01-23: Structured learning types (fact/lesson/pattern) provide clear taxonomy for knowledge accumulation (P2 MECE)
- 2026-01-23: Cache-first API-fallback pattern in /ask command demonstrates good P16 (context cost reduction) while maintaining freshness

## Improvements

> System fixes by self-improve agent

| Date | PR | Target | Change | Root Cause |
|------|-----|--------|--------|------------|

---

*Auto-updated by reviewer and self-improve agents.*
