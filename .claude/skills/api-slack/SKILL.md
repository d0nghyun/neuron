---
name: api-slack
description: Slack Web API for messaging, channels, and notifications. Uses Bot token for headless/CI. Activate for Slack operations.
allowed-tools: Bash, Read, Grep
user-invocable: true
---

# Slack API Skill

## When to Activate

- Send messages to channels or users
- Post notifications and alerts
- Manage channels
- Upload files
- Read channel history

## Authentication

**Credentials File**: `.credentials/slack.json`

```json
{
  "bot_token": "xoxb-...",
  "channel_id": "C..."
}
```

Create token at: https://api.slack.com/apps → Your App → OAuth & Permissions

**Load credentials before API calls**:
```bash
SLACK_BOT_TOKEN=$(jq -r '.bot_token' /Users/dhlee/Git/personal/neuron/.credentials/slack.json)
SLACK_CHANNEL_ID=$(jq -r '.channel_id' /Users/dhlee/Git/personal/neuron/.credentials/slack.json)
```

**Required Scopes**:
- `chat:write` - Send messages
- `channels:read` - List public channels
- `channels:history` - Read public channel messages
- `groups:history` - Read private channel messages
- `files:write` - Upload files
- `reactions:read` - Read reactions (optional)

## API Base URL

```
https://slack.com/api
```

## Required Headers

```bash
-H "Authorization: Bearer $SLACK_BOT_TOKEN"
-H "Content-Type: application/json"
```

## Common Operations

### Test Authentication
```bash
curl -s -X POST \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/auth.test"
```

### Send Message
```bash
curl -s -X POST \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "CHANNEL_ID",
    "text": "Hello from Claude!"
  }' \
  "https://slack.com/api/chat.postMessage"
```

### Send Message with Blocks (Rich Formatting)
```bash
curl -s -X POST \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "CHANNEL_ID",
    "blocks": [
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Title*\nDescription text"
        }
      }
    ]
  }' \
  "https://slack.com/api/chat.postMessage"
```

### List Channels
```bash
curl -s -X GET \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/conversations.list?types=public_channel,private_channel"
```

### Get Channel History
```bash
curl -s -X GET \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/conversations.history?channel=CHANNEL_ID&limit=10"
```

### Upload File
```bash
curl -s -X POST \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -F "channels=CHANNEL_ID" \
  -F "file=@/path/to/file" \
  -F "initial_comment=File description" \
  "https://slack.com/api/files.upload"
```

### Reply in Thread
```bash
curl -s -X POST \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "CHANNEL_ID",
    "thread_ts": "1234567890.123456",
    "text": "Thread reply"
  }' \
  "https://slack.com/api/chat.postMessage"
```

### Add Reaction
```bash
curl -s -X POST \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "CHANNEL_ID",
    "timestamp": "1234567890.123456",
    "name": "thumbsup"
  }' \
  "https://slack.com/api/reactions.add"
```

## Message Formatting (mrkdwn)

| Format | Syntax |
|--------|--------|
| Bold | `*bold*` |
| Italic | `_italic_` |
| Strike | `~strike~` |
| Code | `` `code` `` |
| Code block | ` ```code``` ` |
| Link | `<https://url|text>` |
| User mention | `<@USER_ID>` |
| Channel mention | `<#CHANNEL_ID>` |

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| `invalid_auth` | Bad token | Check .credentials/slack.json |
| `channel_not_found` | Invalid channel | Verify channel ID |
| `not_in_channel` | Bot not in channel | Invite bot to channel |
| `ratelimited` | Too many requests | Wait and retry |

## Rate Limits

- Tier 1: 1 request per second
- Tier 2: 20 requests per minute
- Tier 3: 50 requests per minute

Implement exponential backoff on `ratelimited` responses.

## References

- [Slack Web API](https://api.slack.com/web)
- [Block Kit Builder](https://app.slack.com/block-kit-builder)
- [Message Formatting](https://api.slack.com/reference/surfaces/formatting)
