# Alpha Reviewer Agent

Post-alpha validation and Finter submission agent.

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Alpha Review Pipeline                         │
│                                                                  │
│  arkraft-agent-alpha     →     arkraft-alpha-reviewer           │
│  (Phases 1-5)                  (Review → Fix → Submit)          │
│                                                                  │
│  phase5/*_eval.json      →     review_result.json               │
│  phase4/{model}/am.py    →     submission_state.json            │
└─────────────────────────────────────────────────────────────────┘
```

## Actions

### 1. REVIEW (default)

Validate alpha strategies for production readiness.

**Input**: `phase5/*_eval.json` + `phase4/{model}/am.py`

**Checks**:
| Check | Description | Severity |
|-------|-------------|----------|
| Forward-Looking Bias | Signal uses future data | CRITICAL |
| Train/Test Leakage | Test period overlaps training | CRITICAL |
| Survivorship Bias | Universe uses future knowledge | HIGH |
| Path Independence | Same output regardless of load date | MEDIUM |

**Forward-Looking Bias Patterns** (in am.py):
```python
# BAD: Using future close price
signal = df['close'].shift(-1)  # Looks ahead!

# BAD: Using rolling that includes current
signal = df['close'].rolling(5).mean()  # Includes today

# GOOD: Lagged signal
signal = df['close'].shift(1).rolling(5).mean()  # Uses past only
```

**Output**: `review_result.json`
```json
{
  "action": "review",
  "alphas_reviewed": ["model_name_1", "model_name_2"],
  "results": {
    "model_name_1": {
      "verdict": "PASS|BIAS_DETECTED|NEEDS_FIX",
      "bias_found": [],
      "recommendations": []
    }
  },
  "overall_verdict": "PASS|BIAS_DETECTED"
}
```

### 2. FIX

Correct detected issues in alpha code.

**Input**: `review_result.json` with `verdict=BIAS_DETECTED`

**Process**:
1. Read bias detection details
2. Load original `phase4/{model}/am.py`
3. Apply fixes (add proper lags, fix rolling windows)
4. Save to `phase4_fixed/{model}/am.py`
5. Re-run validation

**Output**: `fix_result.json`
```json
{
  "action": "fix",
  "fixed_alphas": ["model_name_1"],
  "changes": {
    "model_name_1": {
      "original_issues": ["forward-looking bias in line 23"],
      "fixes_applied": ["added shift(1) before rolling"],
      "new_verdict": "PASS|STILL_ISSUES"
    }
  }
}
```

### 3. SUBMIT

Submit validated alpha to Finter platform.

**Prerequisites**:
- Alpha must have `verdict=PASS` from review
- `outcome=DEPLOYED` in eval.json

**Process**:
1. Verify alpha passed review
2. Prepare submission payload
3. Call Finter submit API
4. Track submission state
5. Handle errors with retry

**Submission State Machine**:
```
PENDING → SUBMITTING → SUBMITTED
                    ↓
              ERROR → RETRY → SUBMITTING
                    ↓
                  FAILED
```

**Output**: `submission_state.json`
```json
{
  "model_name": "momentum_5d_0130_1830",
  "state": "SUBMITTED|FAILED|PENDING",
  "finter_id": "alpha_12345",
  "submitted_at": "2026-01-30T18:30:00+09:00",
  "retry_count": 0,
  "last_error": null
}
```

## Bias Detection Checklist

```python
# Run these checks on am.py

def check_forward_looking_bias(code: str) -> list[str]:
    issues = []

    # Pattern 1: Negative shift (looking ahead)
    if re.search(r'\.shift\s*\(\s*-\d+', code):
        issues.append("Negative shift detected - uses future data")

    # Pattern 2: Rolling without lag
    if re.search(r'\.rolling\s*\([^)]+\)\s*\.(mean|std|sum)\(\)', code):
        # Check if preceded by shift
        if not re.search(r'\.shift\s*\(\s*\d+\s*\)\s*\.rolling', code):
            issues.append("Rolling aggregation may include current period")

    # Pattern 3: Future return as feature
    if re.search(r'pct_change\s*\(\s*-?\d+\s*\)', code):
        issues.append("pct_change detected - verify direction")

    return issues
```

## Finter API Integration

```python
import httpx

FINTER_API_URL = "https://api.finter.ai/v1"

async def submit_alpha(alpha_code: str, metadata: dict) -> dict:
    """Submit alpha to Finter platform."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FINTER_API_URL}/alphas/submit",
            headers={"Authorization": f"Bearer {FINTER_API_KEY}"},
            json={
                "code": alpha_code,
                "name": metadata["model_name"],
                "universe": metadata["universe"],
                "category": metadata["category"],
                "hypothesis": metadata["hypothesis"],
            },
        )
        return response.json()
```

## Error Handling

| Error | Action |
|-------|--------|
| API timeout | Retry with exponential backoff (max 3) |
| Validation failed | Return error details, don't retry |
| Rate limit | Wait and retry |
| Auth error | Fail immediately, notify user |

## File Structure

```
workspace/
├── CLAUDE.md           # This file
├── .mcp.json          # MCP config
├── review_result.json # Review output
├── fix_result.json    # Fix output
├── submission_state.json
└── logs/
    └── reviewer.log
```

## MCP Servers

- **alpha-pool**: Read/write alpha metadata
- **finter**: Submit alphas (if available)

## Skills

None required - uses standard tools (Read, Write, Bash).
