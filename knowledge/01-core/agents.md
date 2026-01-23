# Agent System

Agents embody philosophical principles as executable components.

## Why Agents?

**Autonomous Execution [P13]** + **Trust-based Delegation [P14]** = AI solves problems independently before interrupting user.

## Agent Roles

| Agent | Brain Analogy | Purpose | Implements |
|-------|---------------|---------|------------|
| `boot` | Hippocampus (recall) | Session init, load context, surface learnings | Learn from Failure [P17] |
| `wrapup` | Hippocampus (encode) | Session teardown, extract learnings, persist | Sustainable by Design [P20] |
| `advisor` | PFC (Prefrontal Cortex) | Philosophy interpretation, ambiguity resolution | Constructive Challenge [P11] |
| `reviewer` | ACC (Anterior Cingulate) | Code quality, PR review, release notes | Verify Before Done [P15] |
| `refactor` | Hippocampus | Structure improvement, complexity reduction | Simplicity First [P3], MECE [P2] |
| `self-improve` | Neuroplasticity | System improvement from recurring patterns | Learn from Failure [P17] |

## How to Call

```
Task(subagent_type="boot", prompt="Initialize session")
Task(subagent_type="wrapup", prompt="End session")
Task(subagent_type="advisor", prompt="...")
Task(subagent_type="reviewer", prompt="...")
Task(subagent_type="refactor", prompt="...")
```

## Session Lifecycle (boot/wrapup)

**MANDATORY** for complex tasks. Enforced by Critical Rule #6.

```
Session Start → boot agent → loads handoff, focus, lessons
                         → outputs must_know, must_avoid, should_follow
    ↓
Work (with context awareness)
    ↓
Session End → wrapup agent → extracts facts/lessons/patterns
                          → updates handoff and lessons.yaml
```

### When to Use

| Complexity | Use boot/wrapup? | Examples |
|------------|------------------|----------|
| **Complex** | YES | Multi-file changes, commits, requires handoff |
| **Simple** | NO | Read-only queries, single-file reads, explanations |

### Boot Agent

Loads context at session start:
- `handoff/_index.md` - previous session state
- `meta/focus.yaml` - current priorities
- `meta/lessons.yaml` - facts, lessons, patterns

Outputs actionable summary:
- `must_know`: Facts main agent MUST remember
- `must_avoid`: Mistakes main agent MUST not repeat
- `should_follow`: Recommended patterns

### Wrapup Agent

Persists learnings at session end:
- Scans conversation for facts/lessons/patterns
- Updates `meta/lessons.yaml`
- Updates `handoff/_index.md` and context file

Detection signals:
- User corrects AI → **fact**
- Same mistake twice → **lesson**
- Solution works reliably → **pattern**

## Advisor Flow

```
Ambiguous situation → advisor → confidence high/medium? → Proceed
                              → confidence low? → Ask user
```

**Confidence Levels:**
- **High**: Clear answer from principles. Proceed.
- **Medium**: Reasonable inference. Proceed with stated assumption.
- **Low**: Genuinely unclear. Ask user.

### Example

```
User: "Add logging"
AI thinking: New file or existing?
  [P4 Incremental] Build only what's needed → add to existing
  [P1 SSOT] One place for logging → find existing logger
AI response: "[P4, P1] Adding to existing logger in utils/logger.ts"
  → Executes without asking
```

**Anti-pattern:**
```
AI: "Should I create a new file or add to existing?"  ← Unnecessary question
```

## Reviewer Usage

Before any PR:
```
Task(subagent_type="reviewer", prompt="Review staged changes for PR")
```

## Refactor Triggers

- File > 200 lines
- Duplication detected
- Unclear boundaries

```
Task(subagent_type="refactor", prompt="Module X has 3 similar functions")
```

## Self-Improve Activation

When reviewer outputs `[IMPROVE]`:
```
Task(subagent_type="self-improve", prompt="Pattern: <description>")
```
