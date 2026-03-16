#!/bin/bash
# pgweb connected to production RDS via SSM tunnel
set -e

PROFILE="${AWS_PROFILE:-default}"
LOCAL_PORT=25432

# Wait for SSM tunnel
echo "Waiting for SSM tunnel on port $LOCAL_PORT..."
for i in {1..15}; do
  lsof -i :"$LOCAL_PORT" -t >/dev/null 2>&1 && break
  sleep 2
done

if ! lsof -i :"$LOCAL_PORT" -t >/dev/null 2>&1; then
  echo "ERROR: SSM tunnel not available on port $LOCAL_PORT"
  exit 1
fi

PGPASS=$(aws secretsmanager get-secret-value \
  --secret-id ai-infra/rds/arkraft-postgres \
  --region ap-northeast-2 \
  --profile "$PROFILE" \
  --query SecretString --output text | jq -r .password)

if [ -z "$PGPASS" ]; then
  echo "ERROR: Failed to retrieve RDS password"
  exit 1
fi

echo "Starting pgweb on :5051 (read-only)"
exec pgweb \
  --bind=0.0.0.0 --listen=5051 \
  --host=127.0.0.1 --port="$LOCAL_PORT" \
  --user=arkraft --pass="$PGPASS" --db=arkraft \
  --ssl=require --readonly
