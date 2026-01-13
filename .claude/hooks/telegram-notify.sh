#!/bin/bash

# Claude Code Hook - Telegram Notification
# Usage: telegram-notify.sh [stop|question]
# Required env vars: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

MODE="${1:-stop}"

# Debug log
echo "[$(date)] Hook started (mode: $MODE)" >> /tmp/telegram-hook-debug.log

# Load .env.local if exists (for Claude subprocesses)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
[[ -f "$PROJECT_ROOT/.env.local" ]] && source "$PROJECT_ROOT/.env.local"

# Skip if env vars not set
[[ -z "$TELEGRAM_BOT_TOKEN" || -z "$TELEGRAM_CHAT_ID" ]] && { echo "[$(date)] Missing env vars" >> /tmp/telegram-hook-debug.log; exit 0; }

# Read hook input from stdin
input=$(cat)
echo "[$(date)] Input: $input" >> /tmp/telegram-hook-debug.log

# Extract fields from hook input
session_id=$(echo "$input" | jq -r '.session_id // empty' 2>/dev/null)
transcript_path=$(echo "$input" | jq -r '.transcript_path // empty' 2>/dev/null)
tool_input=$(echo "$input" | jq -r '.tool_input // empty' 2>/dev/null)

# Get project info
project_name=$(basename "$(pwd)")
branch=$(git branch --show-current 2>/dev/null || echo "-")

# Clean text for Telegram (remove markdown, XML tags, limit length)
clean_text() {
    local text="$1"

    # If contains <command-name>, extract just the command
    if echo "$text" | grep -q '<command-name>'; then
        text=$(echo "$text" | sed -n 's/.*<command-name>\([^<]*\)<\/command-name>.*/\1/p')
    fi

    echo "$text" | \
        sed 's/<[^>]*>//g' | \
        tr -d '`*_[]#' | \
        tr '\n' ' ' | \
        sed 's/  */ /g'
}

# Build message based on mode
if [[ "$MODE" == "question" ]]; then
    # Extract question from AskUserQuestion tool input
    questions=$(echo "$tool_input" | jq -r '.questions[]?.question // empty' 2>/dev/null | head -3)
    questions=$(clean_text "$questions" | cut -c1-200)

    message="❓ [${project_name}] ${branch}

${questions:-Claude has a question}"

elif [[ "$MODE" == "permission" ]]; then
    # Extract permission request info
    tool_name=$(echo "$input" | jq -r '.tool_name // empty' 2>/dev/null)
    notification_msg=$(echo "$input" | jq -r '.message // empty' 2>/dev/null)
    notification_msg=$(clean_text "$notification_msg" | cut -c1-200)

    # Extract user question from transcript (same as stop mode)
    user_question=""
    if [[ -n "$transcript_path" && -f "$transcript_path" ]]; then
        user_question=$(grep '"type":"user"' "$transcript_path" | \
            grep -v '"tool_use_id"' | \
            grep -v '"tooluseid"' | \
            tail -1 | \
            jq -r '.message.content // empty' 2>/dev/null)
        user_question=$(clean_text "$user_question" | cut -c1-100)
    fi

    message="⏸️ [${project_name}] ${branch}

Q: ${user_question:-No question}

${tool_name}: ${notification_msg:-Permission needed}"

else
    # Stop mode - existing logic
    # Get GitHub PR URL (if exists)
    pr_url=$(gh pr view --json url -q '.url' 2>/dev/null || echo "")

    # Extract from transcript
    user_question=""
    assistant_answer=""
    if [[ -n "$transcript_path" && -f "$transcript_path" ]]; then
        # Get last user message that's not a tool result
        user_question=$(grep '"type":"user"' "$transcript_path" | \
            grep -v '"tool_use_id"' | \
            grep -v '"tooluseid"' | \
            tail -1 | \
            jq -r '.message.content // empty' 2>/dev/null)
        user_question=$(clean_text "$user_question" | cut -c1-100)

        assistant_answer=$(grep '"type":"assistant"' "$transcript_path" | tail -1 | jq -r '.message.content[]? | select(.type=="text") | .text' 2>/dev/null)
        assistant_answer=$(clean_text "$assistant_answer" | cut -c1-150)
    fi

    message="✅ [${project_name}] ${branch}

Q: ${user_question:-No question}"

    if [[ -n "$assistant_answer" ]]; then
        message="${message}

A: ${assistant_answer}"
    fi

    # Add PR link only if exists
    [[ -n "$pr_url" ]] && message="${message}

PR: ${pr_url}"
fi

# Add session resume command
if [[ -n "$session_id" ]]; then
    message="${message}

claude -r ${session_id}"
else
    message="${message}

claude --continue"
fi

# Send to Telegram (use --data-urlencode for multiline text)
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${TELEGRAM_CHAT_ID}" \
  --data-urlencode "text=${message}" \
  --data-urlencode "disable_web_page_preview=true" \
  > /dev/null 2>&1

exit 0
