#!/bin/bash
# Load environment variables
# - macmini: from macOS Keychain (personal/ prefix)
# - others: from .env.local file

NEURON_ROOT="${NEURON_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

if [[ "$(hostname)" == *"Macmini"* ]]; then
    # ===== macOS Keychain 방식 (맥미니) =====
    get_secret() {
        security find-generic-password -s "$1" -w 2>/dev/null
    }

    # GitHub
    export GITHUB_PERSONAL_ACCESS_TOKEN=$(get_secret "personal/github-pat")

    # Atlassian (Jira/Confluence)
    export ATLASSIAN_BASE_URL="https://quantit.atlassian.net"
    export ATLASSIAN_USER_EMAIL="dhlee@quantit.io"
    export ATLASSIAN_API_TOKEN=$(get_secret "personal/atlassian")

    # Notion
    export NOTION_API_TOKEN=$(get_secret "personal/notion")

    # GitLab (Quantit Internal)
    export GITLAB_BASE_URL="http://gitlab.quantit.io"
    export GITLAB_API_TOKEN=$(get_secret "personal/gitlab-quantit")

    # Telegram
    export TELEGRAM_BOT_TOKEN=$(get_secret "personal/telegram-bot")
    export TELEGRAM_CHAT_ID="6982701646"

    # Slack
    export SLACK_BOT_TOKEN=$(get_secret "personal/slack-bot")
    export SLACK_CHANNEL_ID="C06457NL2H4"

    # Claude Code
    export CLAUDE_CODE_OAUTH_TOKEN=$(get_secret "personal/claude-oauth")

    # Google Calendar
    export GOOGLE_CLIENT_ID="83942671151-nunvocfrdbc12207sve48vutd10tsa2r.apps.googleusercontent.com"
    export GOOGLE_CLIENT_SECRET=$(get_secret "personal/google-client-secret")
    export GOOGLE_REFRESH_TOKEN=$(get_secret "personal/google-refresh-token")
    export GOOGLE_CALENDAR_ID="primary"

else
    # ===== .env.local 파일 방식 (기본) =====
    if [ -f "$NEURON_ROOT/.env.local" ]; then
        export $(grep -E "^[A-Z_]+=" "$NEURON_ROOT/.env.local" | xargs)
    fi
fi
