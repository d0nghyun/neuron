#!/bin/bash
# memo-on-session-end.sh — SessionEnd hook
# Auto-writes lightweight memo based on git activity since last memo
# Fast, pure shell — no claude -p call (avoids recursion + latency)

PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
TODAY=$(date +%Y-%m-%d)
NOW=$(date +%H:%M)
MEMO_DIR="$PROJECT_DIR/vault/memory"
MEMO_FILE="$MEMO_DIR/$TODAY.md"
MARKER="$MEMO_DIR/.last-memo-commit"

mkdir -p "$MEMO_DIR"

# Determine range: since last memo marker, or today's commits
LAST_COMMIT=""
[ -f "$MARKER" ] && LAST_COMMIT=$(cat "$MARKER")

if [ -n "$LAST_COMMIT" ]; then
  # Validate the commit still exists (branch may have been reset)
  if git -C "$PROJECT_DIR" cat-file -t "$LAST_COMMIT" >/dev/null 2>&1; then
    COMMITS=$(git -C "$PROJECT_DIR" log --oneline "$LAST_COMMIT"..HEAD --format="- %s" 2>/dev/null)
  else
    COMMITS=$(git -C "$PROJECT_DIR" log --oneline --since="$TODAY 00:00" --format="- %s" 2>/dev/null)
  fi
else
  COMMITS=$(git -C "$PROJECT_DIR" log --oneline --since="$TODAY 00:00" --format="- %s" 2>/dev/null)
fi

# Skip if no new commits
[ -z "$COMMITS" ] && exit 0

# Record current HEAD for next run
git -C "$PROJECT_DIR" rev-parse HEAD > "$MARKER"

# Write or append memo
if [ ! -f "$MEMO_FILE" ]; then
  cat > "$MEMO_FILE" <<EOF
---
date: $TODAY
type: daily-memo
---

# $TODAY

## Session $NOW

### Done
$COMMITS
EOF
else
  cat >> "$MEMO_FILE" <<EOF

---

## Session $NOW

### Done
$COMMITS
EOF
fi

echo "Memo appended to vault/memory/$TODAY.md"
