# Self-Improvement Policy

## Purpose

Governs the self-improve agent's ability to modify Neuron system files.
All changes require human approval via PR review.

## Scope

### Allowed Targets

| Path | Description |
|------|-------------|
| `CLAUDE.md` | Project index and conventions |
| `knowledge/*.md` | Policies and philosophy |
| `.claude/agents/*.md` | Agent definitions |
| `.claude/commands/*.md` | Command definitions |
| `.claude/skills/*/SKILL.md` | Skill definitions |

### Forbidden Targets

| Path | Reason |
|------|--------|
| `modules/` | External repositories |
| `.github/` | GitHub configuration |
| Executable code | Safety |

## Guardrails

| Constraint | Value |
|------------|-------|
| Lines per change | 20 max |
| Files per PR | 1 |
| Deletions | Not allowed |
| New files | Only in docs/ |
| File types | `.md`, `.json` only |

## Trigger Conditions

| Trigger | Description |
|---------|-------------|
| Manual | User runs `/self-improve` command |
| Reviewer tag | `[IMPROVE]` tag in review findings |
| Pattern (3+) | Same issue type in 3+ reviews |

## Approval Process

1. Agent creates PR on `improve/*` branch
2. PR labeled `self-improve` and `system-modification`
3. Human reviews change
4. Human approves or rejects
5. If approved, squash merge to main

## Root Cause Analysis

Apply 5-Whys framework:

| Question | Purpose |
|----------|---------|
| What happened? | Identify symptom |
| Why? | Immediate cause |
| Why was that possible? | Contributing factor |
| Why wasn't it prevented? | Gap in policy |
| What needs to change? | Improvement target |

## Rollback

```bash
git revert <commit-hash>
```

## History

Track all improvements in `docs/improvement-log.md`.
