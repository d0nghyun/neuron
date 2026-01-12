# Self-Test Protocol

## Purpose

Verify that CLAUDE.md is comprehensible to a fresh Claude instance.

**Principle**: Verify Before Done (#15) — don't assume CLAUDE.md is clear, prove it.

**Reference**: Axioms and principles defined in `knowledge/philosophy.md`

## When to Run

- Before committing CLAUDE.md changes to `main`
- After significant changes to agent system or routing

## How to Run

Spawn a fresh Claude agent:

```
Task(subagent_type="general-purpose", prompt="Read CLAUDE.md only. Explain:
1. The three Axioms and their meaning
2. All 16 principles with their axiom mapping
3. How to call each agent and when
4. The Advisor-before-AskUser workflow
5. Rate your confidence 1-10 in operating this system.")
```

## Pass Criteria

| Metric | Threshold |
|--------|-----------|
| Confidence | ≥ 8/10 |
| Axioms | All 3 correctly explained |
| Principles | All 16 listed with correct axiom mapping |
| Agent workflow | Advisor-before-AskUser flow correct |
| Critical misunderstandings | None |

## On Pass

1. Commit CLAUDE.md changes
2. Add entry to Test History below

## On Fail

1. Identify which section caused confusion
2. Revise CLAUDE.md for clarity
3. Re-run test until pass

## Test History

| Date | Result | Notes |
|------|--------|-------|
| 2025-01-12 | 9/10 ✓ | Initial full test after adding 16 principles |
| 2025-01-12 | 8/10 ✓ | Final test after Self-Test section refactor |
