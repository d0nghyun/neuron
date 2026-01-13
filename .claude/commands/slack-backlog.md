---
description: Extract backlog from Slack message and save to Confluence
tools: Bash, Read
---

# Slack to Confluence Backlog

## Purpose

Extract backlog items from Slack messages and save to Confluence for persistent tracking.

## When to Use

- Extract action items from Slack messages
- Record PM/team requests as backlog items
- Document meeting outcomes and decisions

## Convention

| Project | Confluence Location |
|---------|---------------------|
| **Arkraft** | ARK Space → Arkraft page |
| Other | Project-specific Space |

## Workflow

```
Slack URL → Parse (channel, ts) → Fetch message + thread → Extract items → Check duplicate → Create/Update Confluence
```

## Steps

### 1. Parse Slack URL

URL format: `https://{workspace}.slack.com/archives/{channel}/p{timestamp}`

```bash
# Extract channel and timestamp
# p1768271378755819 → 1768271378.755819
```

### 2. Fetch Message (slack-api skill)

```bash
# Main message
conversations.history?channel={channel}&latest={ts}&inclusive=true&limit=1

# Thread replies
conversations.replies?channel={channel}&ts={ts}
```

### 3. Extract Backlog Items

Identify actionable items:
- Requests, needs confirmation, meeting required
- TODO, action items
- Decisions, next steps

### 4. Check Duplicate (confluence-api skill)

```bash
# CQL search for existing content
cql=space=ARK AND ancestor={parentId} AND text~"{keyword}"
```

### 5. Create Confluence Page

```bash
# Create page under arkraft parent
POST /rest/api/content
{
  "type": "page",
  "title": "[Backlog] {summary}",
  "space": {"key": "ARK"},
  "ancestors": [{"id": "{arkraft-page-id}"}],
  "body": {...}
}
```

## Required Scopes

### Slack Bot
- `channels:history` - Public channels
- `groups:history` - Private channels
- `reactions:read` - Read reactions

### Confluence
- Read/Write permission on ARK Space

## Example

Input:
```
/slack-backlog https://quantitworkspace.slack.com/archives/C0933M2A5CK/p1768271378755819
```

Output:
- Confluence page created: "[Backlog] Arkraft Signal Research Feature Meeting"
- Source link preserved in page
