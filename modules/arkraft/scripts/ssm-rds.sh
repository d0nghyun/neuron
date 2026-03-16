#!/bin/bash
# SSM port forwarding to Arkraft production RDS
set -e

PROFILE="${AWS_PROFILE:-default}"
LOCAL_PORT=25432
REMOTE_HOST="arkraft-postgres.cjjgohlf4jlu.ap-northeast-2.rds.amazonaws.com"
REMOTE_PORT=5432

BASTION_ID=$(aws s3 cp \
  s3://quantit-tfstate/terraform/ai-infra/terraform.tfstate - \
  --profile "$PROFILE" 2>/dev/null \
  | jq -r '.outputs.ssm_bastion_instance_id.value // empty')

if [ -z "$BASTION_ID" ]; then
  echo "ERROR: Failed to resolve bastion instance ID"
  exit 1
fi

echo "Bastion: $BASTION_ID"
echo "Tunnel: localhost:$LOCAL_PORT -> $REMOTE_HOST:$REMOTE_PORT"

exec aws ssm start-session \
  --profile "$PROFILE" \
  --target "$BASTION_ID" \
  --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters "{\"host\":[\"$REMOTE_HOST\"],\"portNumber\":[\"$REMOTE_PORT\"],\"localPortNumber\":[\"$LOCAL_PORT\"]}"
