#!/bin/bash
# PM2 process manager helper
# Usage:
#   ./pm2.sh          - Start default (infra, api, web)
#   ./pm2.sh prod     - Start prod DB viewer (ssm-rds, pgweb-prod)
#   ./pm2.sh all      - Start everything
#   ./pm2.sh stop     - Stop all
#   ./pm2.sh stop prod - Stop prod only

cd "$(dirname "$0")"

DEFAULT_APPS="infra,api,celery,web"
PROD_APPS="ssm-rds,pgweb-prod"

case "${1:-default}" in
  prod)
    echo "Starting prod DB viewer (SSM + pgweb)..."
    pm2 start ecosystem.config.js --only "$PROD_APPS"
    echo ""
    echo "  pgweb-prod: http://localhost:5051 (read-only)"
    echo "  SSM tunnel: localhost:25432 -> RDS:5432"
    ;;
  all)
    echo "Starting all services..."
    pm2 start ecosystem.config.js
    ;;
  stop)
    if [ "$2" = "prod" ]; then
      echo "Stopping prod..."
      pm2 delete ssm-rds pgweb-prod 2>/dev/null
    else
      echo "Stopping all..."
      pm2 delete all
    fi
    ;;
  default|"")
    echo "Starting default (infra, api, web)..."
    # Stop Docker API server if running (avoid port 3002 conflict with pm2 uvicorn --reload)
    docker compose -f arkraft-api/docker-compose.yml stop server celery-worker celery-beat flower 2>/dev/null
    pm2 start ecosystem.config.js --only "$DEFAULT_APPS"
    ;;
  *)
    echo "Usage: $0 [prod|all|stop|stop prod]"
    exit 1
    ;;
esac
