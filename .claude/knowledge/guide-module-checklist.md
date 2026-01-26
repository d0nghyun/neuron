# Module Creation/Modification Checklist

Mandatory checks when creating or modifying modules.

## Pre-Completion Checklist

### Language (CRITICAL)

- [ ] All `.md` files in English
- [ ] All `.yaml` files in English
- [ ] `settings.json` descriptions in English
- [ ] Exception: External system field names (e.g., Notion DB properties) can stay in original language but must be documented

### Required Files

- [ ] `README.md` exists at module root
- [ ] `CLAUDE.md` exists at module root
- [ ] `.claude/settings.json` exists (if has skills/agents)

### CLAUDE.md Content

- [ ] Module purpose stated
- [ ] Inherited policies from neuron listed
- [ ] Skills/agents documented
- [ ] Usage instructions included
- [ ] Guardrails defined

### settings.json Content

- [ ] All skill descriptions in English
- [ ] Paths correct relative to `.claude/`

## Common Mistakes to Avoid

| Mistake | Prevention |
|---------|------------|
| Korean in docs | Always write in English first |
| Missing CLAUDE.md | Required for all modules |
| Hardcoded Korean strings in SKILL.md | Use English, note external system names |

## Verification Command

```bash
# Check for non-ASCII in markdown (potential Korean)
grep -r -l '[가-힣]' modules/{module}/*.md modules/{module}/.claude/**/*.md 2>/dev/null

# Check CLAUDE.md exists
ls modules/{module}/CLAUDE.md
```

## Related

- `factory/README.md`: Component creation patterns
- `CLAUDE.md`: Neuron language policy
