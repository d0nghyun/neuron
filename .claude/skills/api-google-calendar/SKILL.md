---
name: api-google-calendar
description: Google Calendar API for events and schedules. Uses OAuth2 refresh token for headless/CI. Activate for calendar operations.
allowed-tools: Bash, Read, Grep
user-invocable: true
---

# Google Calendar Skill

## When to Activate

- Query today's/weekly events
- Create meeting events
- Update or delete events
- Integrate with `/weekly` command

## Authentication

**Credentials File**: `.credentials/google.json`

```json
{
  "client_id": "...",
  "client_secret": "...",
  "refresh_token": "..."
}
```

Create credentials at: https://console.cloud.google.com/apis/credentials

**Setup Steps**:
1. Create OAuth2 credentials in Google Cloud Console
2. Enable Google Calendar API
3. Get refresh token via OAuth2 flow
4. Store in `.credentials/google.json`

**Load credentials before API calls**:
```bash
GOOGLE_CLIENT_ID=$(jq -r '.client_id' /Users/dhlee/Git/personal/neuron/.credentials/google.json)
GOOGLE_CLIENT_SECRET=$(jq -r '.client_secret' /Users/dhlee/Git/personal/neuron/.credentials/google.json)
GOOGLE_REFRESH_TOKEN=$(jq -r '.refresh_token' /Users/dhlee/Git/personal/neuron/.credentials/google.json)
```

## API Base URL

```
https://www.googleapis.com/calendar/v3
```

## Get Access Token

Refresh tokens to get short-lived access tokens:
```bash
ACCESS_TOKEN=$(curl -s -X POST "https://oauth2.googleapis.com/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$GOOGLE_CLIENT_ID" \
  -d "client_secret=$GOOGLE_CLIENT_SECRET" \
  -d "refresh_token=$GOOGLE_REFRESH_TOKEN" \
  -d "grant_type=refresh_token" | jq -r '.access_token')
```

## Common Operations

### List Events (Today)
```bash
TODAY=$(date +%Y-%m-%dT00:00:00Z)
TOMORROW=$(date -v+1d +%Y-%m-%dT00:00:00Z)

curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://www.googleapis.com/calendar/v3/calendars/${GOOGLE_CALENDAR_ID:-primary}/events?timeMin=$TODAY&timeMax=$TOMORROW&singleEvents=true&orderBy=startTime"
```

### List Events (This Week)
```bash
TODAY=$(date +%Y-%m-%dT00:00:00Z)
WEEK_END=$(date -v+7d +%Y-%m-%dT23:59:59Z)

curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://www.googleapis.com/calendar/v3/calendars/${GOOGLE_CALENDAR_ID:-primary}/events?timeMin=$TODAY&timeMax=$WEEK_END&singleEvents=true&orderBy=startTime"
```

### Create Event
```bash
curl -s -X POST \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Meeting Title",
    "description": "Meeting description",
    "start": {
      "dateTime": "2026-01-20T14:00:00+09:00",
      "timeZone": "Asia/Seoul"
    },
    "end": {
      "dateTime": "2026-01-20T15:00:00+09:00",
      "timeZone": "Asia/Seoul"
    },
    "attendees": [
      {"email": "attendee@example.com"}
    ]
  }' \
  "https://www.googleapis.com/calendar/v3/calendars/${GOOGLE_CALENDAR_ID:-primary}/events"
```

### Update Event
```bash
curl -s -X PATCH \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Updated Title"
  }' \
  "https://www.googleapis.com/calendar/v3/calendars/${GOOGLE_CALENDAR_ID:-primary}/events/{eventId}"
```

### Delete Event
```bash
curl -s -X DELETE \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://www.googleapis.com/calendar/v3/calendars/${GOOGLE_CALENDAR_ID:-primary}/events/{eventId}"
```

## Integration with /weekly

The `/weekly` command can query calendar events to auto-populate the weekly update:

```bash
# Load credentials
GOOGLE_CLIENT_ID=$(jq -r '.client_id' /Users/dhlee/Git/personal/neuron/.credentials/google.json)
GOOGLE_CLIENT_SECRET=$(jq -r '.client_secret' /Users/dhlee/Git/personal/neuron/.credentials/google.json)
GOOGLE_REFRESH_TOKEN=$(jq -r '.refresh_token' /Users/dhlee/Git/personal/neuron/.credentials/google.json)

# Get this week's meetings for /weekly
ACCESS_TOKEN=$(curl -s -X POST "https://oauth2.googleapis.com/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$GOOGLE_CLIENT_ID" \
  -d "client_secret=$GOOGLE_CLIENT_SECRET" \
  -d "refresh_token=$GOOGLE_REFRESH_TOKEN" \
  -d "grant_type=refresh_token" | jq -r '.access_token')

curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin=$(date -v-7d +%Y-%m-%dT00:00:00Z)&timeMax=$(date +%Y-%m-%dT23:59:59Z)&singleEvents=true&orderBy=startTime" \
  | jq '.items[] | {summary, start: .start.dateTime, attendees: [.attendees[]?.email]}'
```

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Invalid/expired token | Refresh access token |
| 403 | Insufficient permissions | Check OAuth2 scopes |
| 404 | Calendar/event not found | Verify calendar ID |
| 429 | Rate limit exceeded | Wait and retry |

## OAuth2 Scopes Required

- `https://www.googleapis.com/auth/calendar.readonly` - Read events
- `https://www.googleapis.com/auth/calendar.events` - Create/update/delete events

## References

- [Google Calendar API Docs](https://developers.google.com/calendar/api/v3/reference)
- [OAuth2 for Server Apps](https://developers.google.com/identity/protocols/oauth2/web-server)
