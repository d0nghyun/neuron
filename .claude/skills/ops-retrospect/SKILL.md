---
name: ops-retrospect
description: Counterfactual review of decision paths after Moderate+ tasks
allowed-tools: Read, Glob, Grep, Write
user-invocable: true
quality_grade: B
quality_checked: 2026-02-16
---

# Retrospect

> Review decision paths after task completion. Evaluate whether the chosen approach was optimal and extract reusable lessons.

## When to Activate

- After completing a **Moderate or Complex** task
- User runs `/ops-retrospect`
- Supervisor detects a task where outcome diverged from expectation

Skip for Trivial tasks (conversation, status checks, simple lookups).

## Steps

### Step 1: Reconstruct the Path

Identify the decision points from the just-completed task:

| Element | Question |
|---------|----------|
| **Intent** | What did the user actually want? |
| **Complexity** | How did I classify it? (Trivial/Moderate/Complex) |
| **Approach** | Direct / Delegate / Collaborate — which did I pick? |
| **Components** | Which agents, skills, teams did I use? |
| **Branching** | Where did I choose between alternatives? |

### Step 2: Enumerate Alternatives

For each branching point, list what else could have been done:

```
Branch: {decision point}
  Chosen:      {what was done}
  Alternative: {option A} — {why it might have been better or worse}
  Alternative: {option B} — {why it might have been better or worse}
```

Focus on branches where:
- The outcome was suboptimal (errors, revisions, wasted effort)
- The user corrected course mid-task
- Multiple valid approaches existed

### Step 3: Evaluate

Score each branching decision:

| Verdict | Meaning |
|---------|---------|
| **Correct** | Chosen path was optimal or near-optimal |
| **Acceptable** | Worked but a better path existed |
| **Suboptimal** | A clearly better alternative was available |

Only flag **Acceptable** and **Suboptimal** — correct decisions need no action.

### Step 4: Extract Lesson

For each non-correct verdict, write a lesson:

```
Signal:  {what I should have noticed}
Rule:    {decision heuristic for next time}
Scope:   {when this rule applies}
```

### Step 5: Write to Memory

Append to today's memo (`vault/memory/YYYY-MM-DD.md`):

```markdown
## Retrospective

### {Task summary}
- **Path taken**: {approach chosen}
- **Verdict**: {Acceptable/Suboptimal}
- **Better alternative**: {what should have been done}
- **Lesson**: {signal} → {rule} (scope: {scope})
```

If today's memo doesn't exist, create it with only the Retrospective section.

### Step 6: Check for Patterns

Read recent memos (`vault/memory/`) for recurring lessons:

- Same lesson appearing **3+ times** → candidate for CLAUDE.md rule update
- Propose the rule change but do NOT auto-modify CLAUDE.md

## Output

```yaml
retrospect_result:
  task: {summary}
  branches_reviewed: {count}
  verdicts:
    correct: {count}
    acceptable: {count}
    suboptimal: {count}
  lessons: [{signal, rule, scope}]
  pattern_detected: true | false
```

## Guardrails

- **NEVER** auto-modify CLAUDE.md or RULES.md — only propose changes
- **NEVER** run on Trivial tasks — the overhead exceeds the value
- **ALWAYS** write lessons to vault/memory, not inline
- **ALWAYS** be specific — "should have delegated" is too vague; say why and what signal was missed
