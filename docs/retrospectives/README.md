# Retrospectives

## Purpose

Capture learnings from the development cycle to continuously improve the system.

## Structure

```
docs/retrospectives/
├── README.md           # This guide
├── UNRETROSPECTIVE.md  # Pending learnings
└── retro-v{X.Y.Z}.md   # Release retrospectives
```

## Sections

| Section | Source | Trigger | Content |
|---------|--------|---------|---------|
| Patterns | reviewer | PR with [IMPROVE] tag | Recurring issues detected |
| Insights | reviewer | Every PR | What worked well, lessons learned |
| Improvements | self-improve | After PR created | System fixes made |

## Workflow

1. **Accumulate**: Agents append to UNRETROSPECTIVE.md during cycle
2. **Flush**: `/release` converts to retro-vX.Y.Z.md
3. **Reset**: UNRETROSPECTIVE.md cleared for next cycle

## Related

- `docs/releasenotes/` - What changed (releases)
- `knowledge/self-improve-policy.md` - Improvement guardrails
