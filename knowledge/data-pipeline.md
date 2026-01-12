---
id: data-pipeline
category: workflow
triggers:
  - "API response over 100 lines"
  - "pagination required"
  - "large data"
  - "read header only"
related: [philosophy]
---

# Data Pipeline Pattern

AI context is a precious resource. Save data to files, read only summaries.

## Principle

```
❌ Anti-pattern: AI loads large data directly into context
✅ Pattern: Save data via script → analysis script → interpret results only
```

## When to Apply

### Must Use Pipeline (Hard Rules)
- [ ] API with pagination
- [ ] Possibility of re-querying same data
- [ ] Nested array/object structure

### Strongly Recommended (Soft Rules)
- [ ] Expected response > 100 lines
- [ ] Need only some fields from many
- [ ] "Let me look at it first" feeling

### Direct Read OK
- Single record query
- Config files (< 50 lines)
- Error messages/partial logs

## Pattern

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ 1. Fetch     │ ──▶ │ 2. Transform │ ──▶ │ 3. Interpret │
│ Collect data │     │ Analyze/Sum  │     │ Read results │
│ → Save file  │     │ → Save result│     │ (AI role)    │
└──────────────┘     └──────────────┘     └──────────────┘
   File System          Script            AI Context
   (unlimited)         (reusable)         (10-50 lines)
```

## Example

```bash
# 1. Fetch & Store
python scripts/fetch_issues.py \
  --repo owner/repo \
  --state open \
  --output data/raw/issues.json

# 2. Transform & Analyze
python scripts/analyze_issues.py \
  data/raw/issues.json \
  --output data/processed/summary.json

# 3. Interpret (AI only here)
cat data/processed/summary.json
# → Only 20-line summary in context
```

## Directory Structure

```
project/
├── scripts/
│   ├── fetch_*.py      # Data collection
│   └── analyze_*.py    # Analysis/transform
└── data/
    ├── raw/            # Raw data
    └── processed/      # Analysis results
```

## Anti-patterns

| Anti-pattern | Problem | Alternative |
|--------------|---------|-------------|
| Output API result then "show top N lines only" | Info loss | Save all, then analyze |
| Call same API repeatedly exploring different parts | Inefficient + inconsistent | Save once, analyze multiple times |
| Repeatedly filter with jq/grep | Context waste | Consolidate into analysis script |
| Load large data into context and ask "summarize" | Context pressure | Generate summary via script |

## Connection to Philosophy

| Principle | Application |
|-----------|-------------|
| **SSOT** | Data saved to file only once |
| **Modularity** | Fetch / Transform / Interpret separated |
| **Front-load Pain** | Structure data before analysis |
| **Simplicity First** | Only essentials in context |

## Quick Reference

```
"API result might be large" → Pipeline pattern
"Has pagination" → Pipeline pattern
"Should I just read the header?" → STOP! Pipeline pattern
"Need to look at same data again" → Pipeline pattern
```
