# Cron

Scheduled maintenance jobs. Reduces entropy over time.

Trigger mechanism (crontab, GH Actions, etc.) is configured externally.
Each job maps to an ops skill executed via `claude -p`.

## Jobs

| Job | Schedule | Skill | Description |
|-----|----------|-------|-------------|
| Factory sync | Daily 03:00 | `ops-factory-sync` | Audit factory patterns against actual components, update drift |
| Vault recap | Daily 03:30 | `ops-vault-recap` | Recap session memory into vault, validate structure |
| Daily report | Daily 04:00 | `ops-daily-report` | Unified maintenance report (runs after sync + recap) |

## Execution

```bash
# Example crontab entries
0  3 * * * cd ~/Git/personal/neuron && claude -p "Run /ops-factory-sync"
30 3 * * * cd ~/Git/personal/neuron && claude -p "Run /ops-vault-recap"
0  4 * * * cd ~/Git/personal/neuron && claude -p "Run /ops-daily-report"
```

## Adding Jobs

1. Create an `ops-*` skill for the task
2. Add a row to the Jobs table above
3. Register the crontab entry externally

## Principles

- Jobs are **idempotent**: safe to run multiple times
- Jobs **report only** by default: destructive changes require confirmation
- Jobs run **headless**: no user interaction expected
