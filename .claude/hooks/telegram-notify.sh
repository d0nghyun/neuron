#!/bin/bash

# Claude Code Stop Hook - Telegram Notification
# Required env vars: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# Skip if env vars not set
[[ -z "$TELEGRAM_BOT_TOKEN" || -z "$TELEGRAM_CHAT_ID" ]] && exit 0

# Read hook input from stdin
input=$(cat)

# Extract session_id from hook input
session_id=$(echo "$input" | jq -r '.session_id // empty' 2>/dev/null)

# Get project info
project_name=$(basename "$(pwd)")
branch=$(git branch --show-current 2>/dev/null || echo "-")
last_commit=$(git log -1 --format="%h %s" 2>/dev/null | cut -c1-40 || echo "-")
timestamp=$(date "+%m/%d %H:%M")

# Count today's commits on this branch
today_commits=$(git log --since="00:00" --oneline 2>/dev/null | wc -l | tr -d ' ')

# Get GitHub PR URL (if exists)
pr_url=$(gh pr view --json url -q '.url' 2>/dev/null || echo "")

# Get GitHub repo URL
repo_url=$(gh repo view --json url -q '.url' 2>/dev/null || echo "")

# Escape special characters for Telegram
escape_telegram() {
    echo "$1" | sed 's/[_*`\[]/\\&/g'
}

last_commit_escaped=$(escape_telegram "$last_commit")
branch_escaped=$(escape_telegram "$branch")

# Build message
message="✅ Claude Task Complete

📁 ${project_name}
🌿 ${branch_escaped}
📝 ${last_commit_escaped}
📊 Commits today: ${today_commits}
⏰ ${timestamp}"

# Add PR link if exists
if [[ -n "$pr_url" ]]; then
    message="${message}

🔗 PR: ${pr_url}"
elif [[ -n "$repo_url" ]]; then
    message="${message}

🔗 Repo: ${repo_url}"
fi

# Add session resume command
if [[ -n "$session_id" ]]; then
    message="${message}

▶️ claude -r ${session_id}"
else
    message="${message}

▶️ claude --continue"
fi

# Send to Telegram
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${TELEGRAM_CHAT_ID}" \
  -d "text=${message}" \
  -d "disable_web_page_preview=true" \
  > /dev/null 2>&1

exit 0
