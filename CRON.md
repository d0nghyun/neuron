# Cron

Scheduled maintenance jobs. Reduces entropy over time.

Trigger mechanism (crontab, GH Actions, etc.) is configured externally.
Each job maps to an ops skill executed via `claude -p`.

## Jobs

| Job | Schedule | Skill | Description |
|-----|----------|-------|-------------|
| Factory sync | Daily 03:00 | `ops-factory-sync` | Audit factory patterns against actual components, update drift |
| Vault recap | Daily 03:30 | `ops-vault-recap` | Recap session memory into vault, validate structure |
| Doc gardening | Daily 03:45 | `ops-factory-sync` | Scan stale docs and broken refs in .claude/ and vault/ |
| Daily report | Daily 04:00 | `ops-daily-report` | Unified maintenance report (runs after sync + recap) |
| Hook tests | Daily 02:30 | `tests/run.sh` | Deterministic hook enforcement tests (no claude -p) |

## Execution

```bash
# Example crontab entries
30 2 * * * cd ~/Git/personal/neuron && bash tests/run.sh
0  3 * * * cd ~/Git/personal/neuron && claude -p "Run /ops-factory-sync"
30 3 * * * cd ~/Git/personal/neuron && claude -p "Run /ops-vault-recap"
45 3 * * * cd ~/Git/personal/neuron && claude -p "Run /ops-factory-sync --doc-gardening"
0  4 * * * cd ~/Git/personal/neuron && claude -p "Run /ops-daily-report"
```

## Adding Jobs

1. Create an `ops-*` skill for the task
2. Add a row to the Jobs table above
3. Register the crontab entry externally

## Action Tiers

Jobs are classified into tiers by their blast radius:

| Tier | Action | Examples |
|------|--------|----------|
| Auto | Non-destructive, safe to auto-commit | Quality grade update, broken ref fix, stale date update |
| Confirm | Structural changes, needs human review | Component deletion, directory restructure, rule promotion |

Default: all jobs report only. Auto-tier actions can be enabled per-job with `--auto-commit` flag.

## Principles

- Jobs are **idempotent**: safe to run multiple times
- Jobs **report only** by default: auto-tier actions opt-in via `--auto-commit`
- Jobs run **headless**: no user interaction expected
