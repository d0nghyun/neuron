# Alpha API Routes Reference

## Backend (arkraft-api)

### Discovery (`/alpha/discovery`)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | List sessions |
| POST | `/start` | Start new session |
| DELETE | `/{session_id}` | Delete session |
| GET | `/{session_id}/stream` | SSE (session-level) |
| GET | `/{session_id}/{topic_id}/stream` | SSE (topic-level) |
| GET | `/{session_id}/{topic_id}/artifacts` | List artifacts |
| GET | `/{session_id}/{topic_id}/artifacts/download` | Presigned URL |
| GET | `/{session_id}/backtest-navs` | NAV timeseries |

### Optimize (`/alpha/optimize`)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | List sessions |
| POST | `/start` | Start optimize |
| POST | `/{session_id}/builders` | Add builders |
| GET | `/{session_id}/builders/{builder_id}/stream` | SSE (builder) |

### Pool (`/alpha/pool`)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/alpha/pool` | List alphas |
| GET | `/alpha/pool/{session_id}` | Get alpha detail |
| GET | `/alpha/pool-navs` | Pool NAV data |

### Internal (X-Team-Id header, no JWT)

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/alpha-pool` | Register alpha |
| GET | `/alpha-pool/search` | Search alphas |

## Frontend BFF (arkraft-web `/api/alpha`)

### Sessions

| Method | Path | Purpose |
|--------|------|---------|
| GET/POST | `/sessions` | List / Create |
| GET/PATCH | `/sessions/[id]` | Detail / Update |
| POST | `/sessions/[id]/start` | Start |
| POST | `/sessions/[id]/pause` | Pause |
| GET | `/sessions/[id]/stream` | SSE proxy |
| GET | `/sessions/[id]/backtest-navs` | NAV timeseries |
| GET | `/sessions/[id]/alpha-evals` | Evaluations |

### Builders

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/sessions/[id]/builders` | List builders |
| GET | `/sessions/[id]/builders/[bid]` | Builder detail |
| GET | `/sessions/[id]/builders/[bid]/stream` | Builder SSE |
| GET | `/sessions/[id]/builders/[bid]/backtest-nav` | Builder NAV |
| GET | `/sessions/[id]/builders/[bid]/files` | List files |
| GET | `/sessions/[id]/builders/[bid]/files/[...name]` | Get file |

### Optimize

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/optimize/start` | Start optimize |
| POST | `/optimize/[sid]/builders` | Add builders |
