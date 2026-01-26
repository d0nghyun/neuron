---
name: workflow-code-refactor
description: Analyzes refactoring needs and plans incremental structural changes. Prevents over-engineering.
allowed-tools: Read, Glob, Grep, Bash, Edit, Task
user-invocable: true
---

# Code Refactor Workflow

> Structured refactoring that reduces complexity without over-engineering.

## When to Activate

- User requests code refactoring
- Code has become difficult to maintain
- Need to restructure before adding features

## Prerequisites

- Target code identified
- Tests exist for affected code (or plan to add)
- CLAUDE.md available for principles

## Anti-Patterns to Avoid

| Anti-Pattern | Description |
|--------------|-------------|
| Premature Abstraction | Creating helpers for one-time operations |
| Speculative Generality | Designing for hypothetical future needs |
| Over-Decomposition | Breaking into too many tiny pieces |
| Cosmetic Refactoring | Changes that look nice but add no value |
| Big Bang Rewrite | Replacing everything at once |

## Workflow Steps

### Step 1: Load Context

Read CLAUDE.md for project principles. Key applications:

- **Simplicity**: Refactoring must reduce complexity, not add it
- **Modularity**: Break into independent, replaceable units
- **Verify**: Analyze thoroughly before changing

### Step 2: Assess Need

| Question | If No, STOP |
|----------|-------------|
| Is there actual pain? | Do not fix what is not broken |
| Will change reduce complexity? | Refactoring must simplify |
| Is the pain recurring? | One-time pain is not worth refactoring |
| Can current code not handle new needs? | Extend before rewrite |

### Step 3: Root Cause Analysis

| Cause Type | Typical Response |
|------------|------------------|
| Organic growth | Extract and modularize |
| Wrong abstraction | Replace abstraction |
| Missing abstraction | Add minimal abstraction |
| Tech debt accumulation | Incremental cleanup |
| Requirements change | Adapt structure to new reality |

### Step 4: Define Scope

| Scope Level | Description | Risk |
|-------------|-------------|------|
| Surgical | One function/class | Low |
| Module | One file/module | Medium |
| Cross-cutting | Multiple modules | High |
| Architectural | System-wide patterns | Very High |

Rules:
- Start at smallest viable scope
- Only expand if absolutely necessary
- Each scope level requires explicit justification

### Step 5: Plan Increments

Break refactoring into atomic steps that:
- Can be completed in one session
- Leave code in working state
- Can be reviewed independently
- Can be reverted cleanly

### Step 6: Validate Plan

| Check | Question |
|-------|----------|
| Necessity | Would 3 duplicate lines be simpler than this abstraction? |
| Scope creep | Am I adding "nice to have" changes? |
| Complexity | Is the result actually simpler? |
| Tests | Are there tests to verify behavior? |

### Step 7: Execute or Delegate

- **Surgical scope**: Execute directly
- **Module+ scope**: Create plan and request approval

## Output

```yaml
workflow_result:
  status: proceed | stop | defer
  need_assessment:
    pain: "<specific problem>"
    frequency: "<how often>"
    verdict: proceed | stop
  scope:
    level: surgical | module | cross-cutting | architectural
    justification: "<why>"
  plan:
    - step: 1
      action: "<description>"
      files: ["<file1>", "<file2>"]
  risks:
    - "<risk 1>"
  recommendation: execute | plan-approval-needed | stop
```

## Guardrails

- **NEVER** expand scope without explicit justification
- **NEVER** refactor untested code without adding tests first
- **NEVER** break working functionality
- **NEVER** replace more than one module at once
- **ALWAYS** verify the result is simpler than before
