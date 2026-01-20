---
description: Morning health check and daily briefing for pm-arkraft. Checks Jira sprint status, calendar, and posts report to Slack.
tools: Bash, Read
---

# Morning Routine

Daily health check and briefing for ARK project management.

## What It Does

1. **Jira Health Check**: Sprint status, blocked issues, today's priorities
2. **Calendar Review**: Today's meetings that may affect work
3. **Slack Report**: Post morning briefing to team channel

## Prerequisites

Environment variables in `.env.local`:
- `ATLASSIAN_BASE_URL`, `ATLASSIAN_USER_EMAIL`, `ATLASSIAN_API_TOKEN`
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`
- `SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID`

## Execution

### Step 1: Load Environment Variables

```bash
export $(grep -E "^(ATLASSIAN_|GOOGLE_|SLACK_)" .env.local 2>/dev/null | xargs)
```

### Step 2: Jira Sprint Health Check

```bash
# Get current sprint issues (ARK project)
curl -s -u "$ATLASSIAN_USER_EMAIL:$ATLASSIAN_API_TOKEN" \
  -H "Accept: application/json" \
  -G --data-urlencode "jql=project=ARK AND sprint in openSprints() ORDER BY priority DESC" \
  "$ATLASSIAN_BASE_URL/rest/api/3/search/jql"
```

**Analyze results for**:
- Total issues in sprint
- Issues by status (To Do, In Progress, Done)
- Blocked issues (status = Blocked OR has blocker flag)
- Overdue issues (duedate < today AND status != Done)

### Step 3: Calendar Check (Today's Meetings)

```bash
# Get access token
ACCESS_TOKEN=$(curl -s -X POST "https://oauth2.googleapis.com/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$GOOGLE_CLIENT_ID" \
  -d "client_secret=$GOOGLE_CLIENT_SECRET" \
  -d "refresh_token=$GOOGLE_REFRESH_TOKEN" \
  -d "grant_type=refresh_token" | jq -r '.access_token')

# Get today's events
TODAY=$(date -u +%Y-%m-%dT00:00:00Z)
TOMORROW=$(date -u -d "+1 day" +%Y-%m-%dT00:00:00Z)

curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin=$TODAY&timeMax=$TOMORROW&singleEvents=true&orderBy=startTime"
```

### Step 4: Generate Morning Briefing

Synthesize information into briefing:

```markdown
## Morning Briefing - {DATE}

### Sprint Health
- **Progress**: X/Y issues completed (Z%)
- **In Progress**: N issues
- **Blocked**: M issues (list if any)

### Today's Focus
1. [Highest priority issue]
2. [Second priority]
3. [Third priority]

### Calendar
- HH:MM - Meeting name (duration)
- HH:MM - Meeting name (duration)

### Action Items
- [ ] [Recommended action based on analysis]
```

### Step 5: Post to Slack

```bash
curl -s -X POST \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "'"$SLACK_CHANNEL_ID"'",
    "blocks": [
      {
        "type": "header",
        "text": {"type": "plain_text", "text": "Morning Briefing - '"$(date +%Y-%m-%d)"'"}
      },
      {
        "type": "section",
        "text": {"type": "mrkdwn", "text": "*Sprint Health*\n..."}
      },
      {
        "type": "section",
        "text": {"type": "mrkdwn", "text": "*Today'\''s Focus*\n..."}
      },
      {
        "type": "section",
        "text": {"type": "mrkdwn", "text": "*Calendar*\n..."}
      }
    ]
  }' \
  "https://slack.com/api/chat.postMessage"
```

## Output Format

Return to user:
1. Health status summary (emoji indicators)
2. Key blockers or risks
3. Recommended priorities for the day
4. Confirmation of Slack post

## Error Handling

| Error | Action |
|-------|--------|
| Jira auth fail | Check ATLASSIAN_* env vars |
| Calendar auth fail | Check GOOGLE_* env vars, refresh token may be expired |
| Slack post fail | Check SLACK_BOT_TOKEN and channel permissions |
| No sprint found | Report "No active sprint" |

## Notes

- Run this command at the start of each workday
- [P16] AI judgment required: interpreting health metrics and prioritizing work
- Pairs with `/assign` for creating follow-up tasks from blockers
