---
name: workflow-alpha-hypothesis
description: Orchestrates alpha hypothesis validation from qualitative claim to implementation decision via quant-analyst judgment
allowed-tools: Task, Read, Glob, Grep
user-invocable: true
---

# Alpha Hypothesis Workflow

Orchestrates hypothesis → judgment → implementation decision.

## When to Activate

- User proposes an alpha hypothesis
- User says "validate this alpha" or "evaluate this hypothesis"
- New signal needs validation before implementation

## Flow

```
User hypothesis
      │
      ▼
quant-analyst agent (autonomous judgment)
      │
      ├── PROCEED ──▶ finter-alpha (implement)
      ├── MODIFY ───▶ Present modifications → user decides → loop back
      └── REJECT ───▶ Report reasons + alternatives
```

## Steps

### Step 1: Validate Input

```yaml
required:
  hypothesis: "Qualitative claim about market behavior"
  context:
    universe: "kr_stock | us_stock | crypto_test | etc."
    period: "YYYYMMDD-YYYYMMDD"
optional:
  focus_areas: ["cost_structure", "regime_sensitivity", ...]
  constraints: { max_turnover: "etc." }
```

### Step 2: Invoke Quant Analyst

Delegate to `quant-analyst` agent via Task tool:

```yaml
agent: quant-analyst
model: sonnet
input:
  hypothesis: "{user hypothesis}"
  context: "{universe, period, cost structure}"
```

The quant-analyst will autonomously:
1. Derive measurable questions from hypothesis
2. Define its own criteria (NO preset thresholds)
3. Measure using finter-data + finter-explore
4. Judge each question with reasoning
5. Synthesize overall decision

### Step 3: Route on Judgment

#### PROCEED

```yaml
- Confirm quant-analyst findings with user
- Pass analysis insights to finter-alpha
- Implement alpha with validated parameters
```

#### MODIFY

```yaml
- Present required modifications to user
- Await user decision: accept or abandon
- If accepted: loop back to Step 2 with modified hypothesis
- Max 3 modification loops
```

#### REJECT

```yaml
- Present rejection reasons clearly
- List what-would-change-my-mind conditions
- Suggest alternative hypotheses if identified
- Record lesson in knowledge/learn-failures.yaml
```

### Step 4: Record Outcome

After backtest results (if PROCEED):

```yaml
record:
  file: knowledge/learn-failures.yaml
  entry:
    date: YYYY-MM-DD
    hypothesis: "original"
    judgment: "quant-analyst decision"
    outcome: "backtest result"
    lesson: "what we learned"
```

## Guardrails

- **NEVER** skip quant-analyst and go directly to finter-alpha
- **NEVER** override quant-analyst judgment without user approval
- **ALWAYS** present full reasoning, not just pass/fail
- **ALWAYS** record lessons after outcome is known
