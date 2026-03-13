---
name: domain-alpha-discovery-ops
description: Alpha discovery local testing and production monitoring
allowed-tools: Bash, Read, Grep, Glob
user-invocable: false
quality_grade: A
quality_checked: 2026-03-13
---

# Alpha Discovery Ops Skill

> How to test alpha discovery locally and monitor sessions in production.

## Module Path

`modules/arkraft/arkraft-agent-alphav2`

## Local Testing

### Quick Test (no Docker)

```bash
cd modules/arkraft/arkraft-agent-alphav2

# Single step
uv run python test_run.py design

# All 6 steps sequentially
uv run python test_run.py all
```

- Creates test workspace at `workspace/test-run/`
- Auto-generates `topic.json` with example hypothesis if missing
- Output: timing summary (cost, turns, duration per step)

### CLI Direct Execution

```bash
python main.py --session-id SID --topic-id TID design      # Phase 1
python main.py --session-id SID --topic-id TID prep         # Phase 2
python main.py --session-id SID --topic-id TID explore      # Phase 3
python main.py --session-id SID --topic-id TID review       # Phase 4
python main.py --session-id SID --topic-id TID implement    # Phase 5
python main.py --session-id SID --topic-id TID evaluate     # Phase 6

# Override max turns
python main.py --session-id SID --topic-id TID explore -t 30
```

### Step Turn Defaults (STEP_MAX_TURNS in base.py)

| Step | Default |
|------|---------|
| design | 15 |
| prep | 40 |
| explore | 50 |
| review | 15 |
| implement | 40 |
| evaluate | 60 |

### Docker Dev

```bash
# Interactive shell with live code reload (mounts ./src:/app/src)
docker-compose run agent-dev

# Inside container
python main.py --session-id test --topic-id my-topic design
```

Requires: external `arkraft` Docker network.

### Environment Variables

| Variable | Local Default | Purpose |
|----------|--------------|---------|
| `CLAUDE_OAUTH_TOKEN_{1,2,3}` | — | OAuth tokens (rotation) |
| `AVAILABLE_TOKENS` | `1,2,3` | Token indices |
| `S3_BUCKET` | `arkraft.quantit.ai` | Output bucket |
| `AWS_REGION` | `ap-northeast-2` | AWS region |
| `REDIS_URL` | `redis://localhost:6379` | Event pub/sub |
| `RABBITMQ_URL` | `amqp://arkraft:arkraft@rabbitmq:5672/arkraft` | Callback queue |
| `ARKRAFT_TEAM_ID` | — | Tenant ID |
| `ARKRAFT_API_URL` | — | API base URL |

### Lint & Format

```bash
uv run ruff check src/
uv run ruff format src/
```

## Production Monitoring

### Architecture

```
Agent → RabbitMQ callback → Celery task → DB update + Redis Pub/Sub → SSE → Web UI
Agent → S3 workspace sync (chat_logs, artifacts)
```

### Routes

Full route reference: [ROUTES.md](ROUTES.md)

Key SSE endpoints:
- `GET /alpha/discovery/{session_id}/stream` — session-level
- `GET /alpha/discovery/{session_id}/{topic_id}/stream` — topic-level
- `GET /api/alpha/sessions/{id}/stream` — web BFF proxy

### Redis Pub/Sub

| Channel | Events |
|---------|--------|
| `alpha:discovery:{session_id}` | topic_added, update_status, insight_started/failed |
| `alpha:topic:{topic_id}` | alpha.registered, alpha.evaluated, workspace.sync |

### Callback Flow

Agent → RabbitMQ (`agent.callback` / `callback.alpha`) → Celery (`handle_alpha_callback`) → DB + Redis Pub/Sub.
Fallback: S3 sentinels at `callback-sentinels/alpha/{session_id}/{topic_id}/`.

### Session States

`created` → `running` → `completed` / `failed` (terminal, cannot overwrite)

### Observability

- **Logs**: JSON Lines to stdout (K8s/ELK)
- **Tool usage**: `src/usage_tracker.py` — call count, duration, errors
- **Token rotation**: every 2h (`now.hour // 2 % len(tokens)`)
- **Resume**: `.claude-id` + `_cli.jsonl` per step (cleared at step start)

## Gotchas

- `test_run.py` bypasses S3/callback — artifacts stay in local `workspace/test-run/`
- Docker build context is parent dir (`modules/arkraft/`), not the repo root
- OAuth tokens are build ARGs but runtime env overrides them
- `.claude-id` is per-step only — cannot resume across different steps
- RabbitMQ callback uses fire-and-forget (broker_pool_limit=0, heartbeat=0) for AWS MQ resilience
