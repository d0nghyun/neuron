# Spec Process

How to develop specifications through scenario-based analysis.

## Overview

Before building, clarify what to build. Use scenarios to discover gaps and define requirements.

## Process Steps

### Step 1: Scenario Presentation

User presents a concrete use case.

```
Example: "I want to manage my resume with Notion"
```

**Goal**: Understand the real need, not just the technical request.

### Step 2: Expected Behavior Analysis

Map out how the system should respond.

```
User Request
    │
    ▼
┌─────────────────────────┐
│ Analyze requirements    │
│ - What's needed?        │
│ - Code required?        │
│ - External services?    │
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ Propose options         │
│ - Option A: Simple      │
│ - Option B: Full        │
└─────────────────────────┘
```

### Step 3: Gap Discovery

Compare expected behavior with current capabilities.

| Expected | Current | Gap |
|----------|---------|-----|
| Decision guide | None | Need decision-guide.md |
| MCP placement | Unclear | Need placement policy |

### Step 4: Document/Structure Derivation

List concrete deliverables to fill gaps. Use [decision-guide.md](decision-guide.md) to determine where each deliverable should live.

```
knowledge/
├── decision-guide.md        # NEW
├── extension-mechanisms.md  # NEW
└── spec-process.md          # NEW
```

### Step 5: Priority Setting

Rank by complexity and dependency.

| Priority | Item | Complexity |
|----------|------|------------|
| 1 | decision-guide.md | Low |
| 2 | extension-mechanisms.md | Low |
| 3 | submodule inheritance | High (separate issue) |

### Step 6: Documentation

Write the specs/guides identified above.

## Checklist

- [ ] Scenario is concrete (not abstract)
- [ ] Expected behavior is mapped
- [ ] Gaps are identified with current state
- [ ] Deliverables are listed
- [ ] Priorities are set
- [ ] Complex items are separated as issues

## Anti-patterns

| Anti-pattern | Better Approach |
|--------------|-----------------|
| Start coding immediately | Analyze scenario first |
| Abstract requirements | Use concrete examples |
| Solve everything at once | Prioritize and separate |
| Skip gap analysis | Compare expected vs current |
