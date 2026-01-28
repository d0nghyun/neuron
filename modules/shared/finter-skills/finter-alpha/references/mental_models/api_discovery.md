# API Discovery Mental Model

## The Core Problem

Financial APIs have complex hierarchies and undocumented behaviors. Guessing method signatures or attribute names leads to runtime errors. The cost of a wrong assumption is wasted compute and failed research sessions.

---

## Mental Model: The Discovery vs Assumption Spectrum

```
    FAST                                              SAFE
      │                                                 │
      ▼                                                 ▼
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  GUESS   │───▶│  ASSUME  │───▶│  CHECK   │───▶│ DISCOVER │
│          │    │          │    │          │    │          │
│ "Probably│    │ "Docs    │    │ "Let me  │    │ "What    │
│  works"  │    │  say X"  │    │  verify" │    │  exists?"│
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │                │               │               │
     │                │               │               │
 HIGH RISK        MED RISK        LOW RISK        NO RISK
 HIGH SPEED       MED SPEED       MED SPEED       LOW SPEED
```

**Key Insight**: The right position on this spectrum depends on how stable the API is and how costly failure is.

---

## Framework 1: The Type Discovery Protocol

### The Problem It Solves
Function return types aren't always obvious:
- Does `get_dates()` return `list`, `pd.Index`, or `np.array`?
- Does `trading_days()` return `list[str]` or `pd.DatetimeIndex`?

Using the wrong type leads to subtle bugs that pass initial tests but fail edge cases.

### The Mental Model
```
API Call ──→ Return Value ──→ Your Code
                 │
                 ▼
         What TYPE is this?
                 │
    ┌────────────┴────────────┐
    │                         │
 DOCUMENTED               DISCOVERED
 • Trust docs             • type(result)
 • Fast path              • dir(result)
 • Risk: docs wrong       • Risk: slower
```

### The Tradeoff
- **Trust documentation**: Fast development, but breaks if docs are outdated
- **Runtime discovery**: Slower, but handles API changes gracefully

### Three Questions to Ask
1. **Is this API stable?** (Change frequency)
   - Stable: Trust documentation
   - Evolving: Discover at runtime

2. **What happens if I'm wrong?** (Failure cost)
   - Silent wrong result: Always discover
   - Loud error: Trust docs, fix on failure

3. **How critical is this path?** (Frequency of use)
   - Called once: Discovery overhead acceptable
   - Inner loop: Cache discovered type

### How to Know It's Working
```
GOOD: "trading_days returned list[str], converting to datetime"
BAD:  AttributeError: 'list' object has no attribute 'strftime'
```

---

## Framework 2: The Attribute Discovery Model

### The Problem It Solves
Objects have attributes you don't know about:
- What methods does a `ContentFetcher` have?
- What attributes does a backtest result contain?

### The Mental Model
```
Unknown Object
      │
      ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   dir()     │────▶│  Filter     │────▶│   Use       │
│             │     │  callable?  │     │             │
│ All names   │     │  private?   │     │  Relevant   │
│             │     │             │     │  attributes │
└─────────────┘     └─────────────┘     └─────────────┘
```

### The Discovery Pattern
```python
# Instead of guessing...
# BAD: obj.getData()  # Might not exist

# Discover what's available
# GOOD: [m for m in dir(obj) if not m.startswith('_')]
```

### When Discovery Helps
- Working with third-party libraries
- APIs that evolved over time (old vs new method names)
- Objects with dynamic attributes

### When Discovery Hurts
- Performance-critical code (dir() has overhead)
- Well-documented, stable interfaces

### How to Know It's Working
```
GOOD: "Found methods: ['get_data', 'fetch', 'load']. Using 'get_data'."
BAD:  AttributeError: 'DataLoader' object has no attribute 'getData'
```

---

## Framework 3: The Error Anticipation Model

### The Problem It Solves
API calls can fail for many reasons:
- Network issues
- Invalid parameters
- Missing data
- Rate limits

Naive code assumes success; robust code anticipates failure.

### The Mental Model
```
API Call ──────────────────────────────────▶ Happy Path
    │
    ├── Network Error ──▶ Retry strategy?
    │
    ├── Invalid Input ──▶ Validate before call?
    │
    ├── Missing Data ──▶ Graceful degradation?
    │
    └── Rate Limit ──▶ Backoff strategy?

Question: Which failure modes can you tolerate?
```

### The Tradeoff
- **Optimistic**: Fast path works, failures crash
- **Defensive**: All paths handled, but verbose code
- **Strategic**: Critical failures handled, rare ones logged

### Classification of Failures
| Failure Type | Frequency | Recovery Strategy |
|-------------|-----------|-------------------|
| Network timeout | Rare | Retry with backoff |
| Invalid params | Should never happen | Validate inputs |
| Missing data | Common | Return NaN/None |
| Rate limit | API-dependent | Backoff + queue |

### How to Know It's Working
```
GOOD: "API returned 404 for TICKER123, excluding from analysis"
BAD:  Entire session crashes because one ticker was delisted
```

---

## Framework 4: The API Contract Model

### The Problem It Solves
APIs have implicit contracts—inputs they expect and outputs they guarantee. Violating contracts leads to undefined behavior.

### The Mental Model
```
┌─────────────────────────────────────────────┐
│               API CONTRACT                   │
├─────────────────┬───────────────────────────┤
│   INPUTS        │   OUTPUTS                 │
│                 │                           │
│ • Expected types│ • Guaranteed types        │
│ • Valid ranges  │ • Possible values         │
│ • Required vs   │ • Error conditions        │
│   optional      │                           │
└─────────────────┴───────────────────────────┘
           │                    │
           ▼                    ▼
    Your responsibility   API's responsibility
    to meet input         to meet output
    contract              contract
```

### The Contract Discovery Process
1. **What inputs are required?** (Signature inspection)
2. **What types are expected?** (Type hints, docs, or testing)
3. **What does success look like?** (Sample output)
4. **What does failure look like?** (Error types)

### Warning Signs of Contract Violation
- Function works sometimes but not always
- Results change with same inputs (non-determinism)
- Silent truncation or rounding

### How to Know It's Working
```
GOOD: "Input validated: date range within available data"
BAD:  Results look reasonable but are actually from wrong date range
```

---

## Summary: The API Discovery Mindset

Instead of prescriptive rules, carry these questions:

| Situation | Question to Ask |
|-----------|-----------------|
| Calling unfamiliar API | "What does this actually return?" |
| Using object attribute | "Does this attribute exist?" |
| Expecting specific type | "What type did I actually get?" |
| Handling API response | "What failure modes are possible?" |

**Remember**: Discovery is not paranoia—it's insurance against the hidden complexity of real-world APIs. The goal is not to check everything, but to check the things that matter for your specific use case.

---

## The Diagnostic-First Principle

When something doesn't work, diagnose before fixing:

```
WRONG approach:
  Error → Guess fix → Try → Error → Guess again → ...

RIGHT approach:
  Error → What type is this? → What's available? → Fix informed by reality
```

This is slower for trivial bugs but dramatically faster for subtle ones.
