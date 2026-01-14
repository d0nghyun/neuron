# Unreleased

> Changes pending for the next release

## Added

- pm-arkraft: `/assign` command for Jira issue creation with Slack notifications
- pm-arkraft: `/healthcheck` command for ARK-307 epic status check via Slack
- pm-arkraft: `team-registry.yaml` as SSOT for team member Jira/Slack IDs
- pm-arkraft: Setup guide with API token configuration instructions
- **Trading Dashboard** (`modules/arkraft-fe`): New trading page with Portrader integration
  - Real-time trading strategy status and rebalance history
  - BTC price chart with trade markers using ECharts
  - Portfolio analysis and recent order tracking
  - Navigation item added to GlobalNav
- **Portrader API Integration** (`modules/arkraft-fe`): GraphQL proxy endpoint for trading data
- **Market Data API** (`modules/arkraft-fe`): Binance BTC price endpoint with caching

## Changed

- **Arkraft Claude Agent Refactoring** (`modules/arkraft/agents/claude-agent/src`):
  - Split `run_agent.py` (454→192 lines) - extracted `results.py`, `logging_utils.py`
  - Split `system_prompts.py` (652 lines deleted) into separate modules per agent type
  - Added `user_prompts.py` for centralized user prompt builders
  - Updated `config.py` to support IAM credentials with agent-specific override (backwards compatible with Bearer Token)
- **Portrader Endpoint Configuration** (`modules/arkraft-fe`):
  - Updated default GraphQL endpoint from internal IP to production domain (finter.quantit.io/trading)
  - Added `PORTRADER_GRAPHQL_URL` to `.env.example` for environment-specific configuration
- **AWS Bedrock Cost Tracking** (`modules/pm-arkraft`):
  - Migrated documentation from Git to Confluence ADR-0005 (SSOT)
  - Enhanced ADR with Cache Write pricing (25% premium), cost calculation formulas, and CloudWatch dashboard details
  - Documented managed IAM policy (arn:aws:iam::696201523565:policy/BedrockInvokePolicy)

## Fixed

-

## Removed

-

## Security

-

## Breaking Changes

-

---

*Auto-updated by reviewer agent on PR creation.*
