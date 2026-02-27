#!/bin/bash

# Claude Code Hook - Telegram + OpenClaw Notification
# Usage: telegram-notify.sh [stop|question|permission|subagent-stop|notification]
# Env: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, CLAWDBOT_WAKE

MODE="${1:-stop}"
echo "[$(date)] Hook started (mode: $MODE)" >> /tmp/telegram-hook-debug.log

# Load .env.local
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
[[ -f "$PROJECT_ROOT/.env.local" ]] && source "$PROJECT_ROOT/.env.local"

# Skip if env vars not set
[[ -z "$TELEGRAM_BOT_TOKEN" || -z "$TELEGRAM_CHAT_ID" ]] && exit 0

# Read hook input from stdin
input=$(cat)

# Extract fields
session_id=$(echo "$input" | jq -r '.session_id // empty' 2>/dev/null)
transcript_path=$(echo "$input" | jq -r '.transcript_path // empty' 2>/dev/null)
tool_input=$(echo "$input" | jq -r '.tool_input // empty' 2>/dev/null)

# Short session ID (first 8 chars)
short_id="${session_id:0:8}"

# Project info
project_name=$(basename "$(pwd)")
branch=$(git branch --show-current 2>/dev/null || echo "-")

# ── Session identity (stable per tmux session name) ──
IDENTITY_MAP_FILE="${PROJECT_ROOT}/.claude/hooks/seafood-map.json"

get_identity() {
    local sid="$1"
    # 1) Try tmux session name → fixed mapping
    local tmux_name=""
    tmux_name=$(tmux display-message -p '#S' 2>/dev/null || echo "")
    if [[ -n "$tmux_name" && -f "$IDENTITY_MAP_FILE" ]]; then
        local mapped
        mapped=$(jq -r --arg k "$tmux_name" '.[$k] // empty' "$IDENTITY_MAP_FILE" 2>/dev/null)
        if [[ -n "$mapped" ]]; then
            echo "$mapped"
            return
        fi
    fi
    # 2) Fallback: hash-based
    local names=("🦐새우맨" "🐙문어맨" "🦀게맨" "🐚조개맨" "🦈상어맨" "🐡복어맨" "🦞랍스터맨" "🐳고래맨" "🦭물범맨" "🐬돌고래맨" "🪼해파리맨" "🐠열대어맨")
    if [[ -n "$sid" ]]; then
        local hash=0
        for ((i=0; i<${#sid}; i++)); do
            hash=$((hash + $(printf '%d' "'${sid:$i:1}")))
        done
        echo "${names[$((hash % ${#names[@]}))]}"
    else
        echo "🐟물고기맨"
    fi
}

# ── Clean text (strip markdown/XML, truncate) ──
clean() {
    local text="$1" max="${2:-150}"
    if echo "$text" | grep -q '<command-name>'; then
        text=$(echo "$text" | sed -n 's/.*<command-name>\([^<]*\)<\/command-name>.*/\1/p')
    fi
    echo "$text" | sed 's/<[^>]*>//g' | tr -d '`*_[]#' | tr '\n' ' ' | sed 's/  */ /g' | cut -c1-"$max"
}

# ── Extract transcript info ──
get_last_question() {
    [[ -z "$transcript_path" || ! -f "$transcript_path" ]] && return
    grep '"type":"user"' "$transcript_path" | grep -v '"tool_use_id"' | grep -v '"tooluseid"' | tail -1 | \
        jq -r '.message.content // empty' 2>/dev/null
}

get_first_question() {
    [[ -z "$transcript_path" || ! -f "$transcript_path" ]] && return
    grep '"type":"user"' "$transcript_path" | grep -v '"tool_use_id"' | grep -v '"tooluseid"' | head -1 | \
        jq -r '.message.content // empty' 2>/dev/null
}

get_last_answer() {
    [[ -z "$transcript_path" || ! -f "$transcript_path" ]] && return
    grep '"type":"assistant"' "$transcript_path" | tail -1 | \
        jq -r '.message.content[]? | select(.type=="text") | .text' 2>/dev/null
}

identity=$(get_identity "$session_id")

# ── Build message ──
case "$MODE" in
    question)
        questions=$(echo "$tool_input" | jq -r '.questions[]?.question // empty' 2>/dev/null | head -3)
        questions=$(clean "$questions" 200)
        task=$(clean "$(get_first_question)" 30)

        message="${identity} ❓ ${project_name}/${branch}
─────────────
${questions:-Claude has a question}
─────────────
📋 ${task:-task}
🔗 claude -r ${short_id}"
        ;;

    permission)
        tool_name=$(echo "$input" | jq -r '.tool_name // empty' 2>/dev/null)
        perm_msg=$(echo "$input" | jq -r '.message // empty' 2>/dev/null)
        perm_msg=$(clean "$perm_msg" 200)
        task=$(clean "$(get_first_question)" 30)

        message="${identity} ⏸️ ${project_name}/${branch}
─────────────
🔒 ${tool_name}: ${perm_msg:-Permission needed}
─────────────
📋 ${task:-task}
🔗 claude -r ${short_id}"
        ;;

    subagent-stop)
        # SubAgent (Explore, Plan 등) 완료
        agent_name=$(echo "$input" | jq -r '.agent_name // .tool_name // empty' 2>/dev/null)
        task=$(clean "$(get_first_question)" 30)

        message="${identity} 🔄 ${project_name}/${branch}
─────────────
🤖 SubAgent 완료: ${agent_name:-agent}
─────────────
📋 ${task:-task}
🔗 claude -r ${short_id}"
        ;;

    notification)
        # CCC가 보내는 일반 알림
        notif_msg=$(echo "$input" | jq -r '.message // empty' 2>/dev/null)
        notif_msg=$(clean "$notif_msg" 200)
        task=$(clean "$(get_first_question)" 30)

        message="${identity} 📢 ${project_name}/${branch}
─────────────
${notif_msg:-Notification}
─────────────
📋 ${task:-task}
🔗 claude -r ${short_id}"
        ;;

    *)  # stop
        q=$(clean "$(get_last_question)" 100)
        a=$(clean "$(get_last_answer)" 200)
        pr_url=$(gh pr view --json url -q '.url' 2>/dev/null || echo "")

        message="${identity} ✅ ${project_name}/${branch}
─────────────
📝 ${q:-no task}
💬 ${a:-done}
─────────────"

        [[ -n "$pr_url" ]] && message="${message}
🔗 ${pr_url}"

        message="${message}
▶ claude -r ${short_id}"
        ;;
esac

# ── Send ──
# Always send both Telegram + Wake (no CLAWDBOT_WAKE check)
# 1) Telegram
openclaw message send --channel telegram --target 6982701646 \
  --message "$message" --silent 2>/dev/null &

# 2) Wake 오징어맨
task_ctx=$(clean "$(get_first_question)" 30)
wake_msg="[ccc:${MODE}] ${identity} ${project_name}/${branch} | ${task_ctx:-idle} | session:${short_id}"
openclaw system event --text "$wake_msg" --mode now > /dev/null 2>&1 &

echo "[$(date)] Wake + Telegram sent via OpenClaw" >> /tmp/telegram-hook-debug.log

exit 0
