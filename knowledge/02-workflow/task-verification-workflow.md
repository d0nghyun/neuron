# Task Verification Workflow

Defines a universal pattern for task definition, verification, and feedback.

## Philosophy Basis

| Principle | Role |
|-----------|------|
| Test-First (#7) | Define verification criteria WITH task |
| Verify Before Done (#15) | Execute verification before completion |
| Learn from Failure (#17) | Feedback loop on verification failure |

## Workflow

```
┌─────────────────────────────────────────────────────────┐
│ 1. DEFINE: What + How to Verify                         │
│    Task: "Implement feature X"                          │
│    Criteria: ["unit test passes", "API returns 200"]    │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ 2. EXECUTE: Do the work                                 │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ 3. VERIFY: Run verification criteria                    │
│    ✓ unit test passes                                   │
│    ✗ API returns 200 → FAIL                             │
└─────────────────────────────────────────────────────────┘
                         │
            ┌────────────┴────────────┐
            ▼                         ▼
      ┌──────────┐              ┌──────────┐
      │   PASS   │              │   FAIL   │
      │  → Done  │              │  → Loop  │
      └──────────┘              └──────────┘
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                   ┌──────────┐              ┌──────────┐
                   │ Diagnose │              │  Record  │
                   │ root     │              │  pattern │
                   │ cause    │              │  [IMPROVE]│
                   └──────────┘              └──────────┘
                         │                         │
                         ▼                         ▼
                   ┌──────────┐              ┌──────────┐
                   │   Fix    │              │  self-   │
                   │          │              │  improve │
                   └──────────┘              └──────────┘
                         │
                         └─────────→ Return to VERIFY
```

## Step 1: DEFINE

**Task + Verification Criteria must be defined together.**

### Template

```markdown
## Task
<what needs to be done>

## Verification Criteria
| # | Criterion | How to Verify |
|---|-----------|---------------|
| 1 | <expected outcome> | <command/action to check> |
| 2 | <expected outcome> | <command/action to check> |
```

### Examples by Domain

**Code Development**
```markdown
## Task
Add pagination to user list API

## Verification Criteria
| # | Criterion | How to Verify |
|---|-----------|---------------|
| 1 | Returns max 20 items | `curl /users?page=1` → count ≤ 20 |
| 2 | Page parameter works | `curl /users?page=2` → different results |
| 3 | Unit tests pass | `pytest tests/test_users.py` |
```

**Data Pipeline**
```markdown
## Task
Transform raw CSV to normalized parquet

## Verification Criteria
| # | Criterion | How to Verify |
|---|-----------|---------------|
| 1 | Output exists | `ls output/*.parquet` |
| 2 | Row count matches | `input_rows == output_rows` |
| 3 | Schema correct | `pq.read_schema()` matches spec |
| 4 | No nulls in key columns | `df[key_cols].isna().sum() == 0` |
```

**Documentation**
```markdown
## Task
Write API documentation for /users endpoint

## Verification Criteria
| # | Criterion | How to Verify |
|---|-----------|---------------|
| 1 | All params documented | Check against OpenAPI spec |
| 2 | Examples work | Execute example requests |
| 3 | Fresh Claude understands | Task(general-purpose) reads and explains |
```

## Step 2: EXECUTE

Perform the task. No special instructions.

## Step 3: VERIFY

**Execute each criterion before declaring done.**

```markdown
## Verification Results
| # | Criterion | Result | Notes |
|---|-----------|--------|-------|
| 1 | Returns max 20 items | ✓ PASS | |
| 2 | Page parameter works | ✗ FAIL | Always returns same data |
| 3 | Unit tests pass | ✓ PASS | |
```

### On All Pass
- Task complete
- Call `reviewer` if PR needed

### On Any Fail
- **DO NOT declare done**
- Proceed to feedback loop

## Feedback Loop (on FAIL)

### Immediate: Diagnose & Fix

```
1. Diagnose: Why did criterion #2 fail?
   → offset not applied to query

2. Fix: Apply offset to query

3. Re-verify: Run criterion #2 again
   → PASS
```

### Systemic: Record Pattern

If same failure type occurs repeatedly:

```markdown
[IMPROVE] workflow: Pagination always forgets offset
- Pattern: 3 pagination tasks, 3 offset bugs
- Root Cause: No pagination checklist
- Suggested Target: knowledge/api-patterns.md
```

This triggers `self-improve` agent.

## Integration Points

| Phase | Tool |
|-------|------|
| Define | TodoWrite (capture criteria as todos) |
| Verify | Bash (run tests), reviewer (code quality) |
| Feedback | self-improve (systemic patterns) |

## Anti-patterns

| Anti-pattern | Correct Approach |
|--------------|------------------|
| Define task without criteria | Always pair task + criteria |
| Skip verification | Run every criterion |
| Declare done on first pass | Verify first |
| Ignore failure pattern | Record with [IMPROVE] |
| Vague criteria ("it works") | Executable criteria |

## Checklist

Before declaring any task done:

- [ ] Verification criteria defined at task start
- [ ] All criteria are executable (not vague)
- [ ] Each criterion has been run
- [ ] All criteria pass
- [ ] Failures diagnosed and fixed
- [ ] Recurring patterns recorded

## Enforcement Mechanism

**PR Template**: `.github/pull_request_template.md` includes mandatory verification section.

**Reviewer Agent**: Will mark `changes-requested` if:
- No verification criteria defined
- Criteria not executed
- Broken references found (grep for deleted files)

**Pattern Tracking**: Violations logged in `docs/retrospectives/UNRETROSPECTIVE.md`.
- 8+ occurrences → system-level fix required
- `self-improve` agent triggered on [IMPROVE] tags
