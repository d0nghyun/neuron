# Unretrospective

> Learnings pending for the next release

## Patterns

> Recurring issues detected by reviewer agent

| Date | PR | Pattern | Status |
|------|-----|---------|--------|
| 2026-01-23 | arkraft-agent-insight | Task verification workflow not followed for refactoring tasks | pending |
| 2026-01-23 | arkraft-agent-insight | Subagent added without corresponding test coverage | pending |
| 2026-01-23 | arkraft-agent-pm#1 | Language policy violation - Korean content in English-only repo without detection | pending |
| 2026-01-25 | docs-factory-boot | Task verification workflow not followed for documentation changes | pending |

## Insights

> What worked well, lessons learned (updated by reviewer on each PR)

- 2026-01-23: Modular subagent design (planner) effectively separated concerns between request parsing and insight generation
- 2026-01-23: Visual architecture diagrams in README greatly improved comprehension of multi-agent flow
- 2026-01-23: Using cheaper Haiku model for deterministic parsing demonstrates good cost optimization (P16 Automate Repetition)
- 2026-01-23: Boot/wrapup agent design creates enforced memory system - instructions become executable workflows (P20 Sustainable by Design)
- 2026-01-23: Structured learning types (fact/lesson/pattern) provide clear taxonomy for knowledge accumulation (P2 MECE)
- 2026-01-23: Cache-first API-fallback pattern in /ask command demonstrates good P16 (context cost reduction) while maintaining freshness
- 2026-01-25: Clear separation of concerns between boot (list available) and main agent (decide needed) follows P3 Modularity and eliminates duplication
- 2026-01-25: Universal boot→execute→wrapup lifecycle (removing conditional logic) creates predictable, consistent session initialization
- 2026-01-25: Aggressive cleanup of 11 obsolete files (1393 lines removed) demonstrates commitment to P1 SSOT and P2 Simplicity
- 2026-01-25: Inlining protocol documentation into relevant components (e.g., module protocol → audit-modules skill) reduces navigation overhead
- 2026-01-25: Location Decision guide added to factory README fills critical documentation gap - clarifies where (neuron vs module) to create components, not just what to create
- 2026-01-25: Correcting glob paths from relative to absolute in system-boot prevents future path resolution issues and improves reliability
- 2026-01-26: Task handoff system (.claude/tasks/{focus}/) enables cross-session continuity without relying on external services
- 2026-01-26: Comprehensive CLAUDE.md restructure with emoji warnings and explicit STOP instructions shows evolution toward clearer, more assertive documentation
- 2026-01-26: Adding permissionMode: bypassPermissions across all agents demonstrates commitment to reducing friction for system-level operations
- 2026-01-26: Changing pre-validate.sh from warn to approve for settings/destructive commands shows maturity in trust model
- 2026-01-26: Task restoration as mandatory Step 2 in boot agent codifies cross-session handoff as first-class workflow
- 2026-01-26: Cleaning up learn-failures.yaml by removing non-systemic errors (user/tool issues) maintains signal-to-noise ratio
- 2026-01-26: Creating modules/shared/ directory centralizes domain-specific skills (finter-skills) following P1 SSOT - one place for Finter knowledge used across multiple modules
- 2026-01-26: Clear documentation in modules/README.md explaining shared/ vs .claude/knowledge/ distinction prevents confusion about where domain skills belong

## Improvements

> System fixes by self-improve agent

| Date | PR | Target | Change | Root Cause |
|------|-----|--------|--------|------------|

---

*Auto-updated by reviewer and self-improve agents.*
