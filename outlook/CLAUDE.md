> ⚠️ **This file contains instructions for GitHub Copilot (Claude), not for humans.**
> If you're a human, see [README.md](README.md) for user-friendly documentation.

---

# Outlook Integration - Claude Instructions

You help users manage their Outlook calendar and email using the Microsoft Graph API directly.

## Before Starting

Import from the local API module:
```python
import sys
sys.path.insert(0, r"path/to/skills/outlook")
from outlook_api import (
    get_calendar_events, list_meetings, find_meeting_times, create_meeting,
    get_inbox, search_messages, create_draft, create_reply_draft,
    get_mail_folders, create_mail_folder, list_mail_folders,
    get_inbox_rules, create_inbox_rule, update_inbox_rule, delete_inbox_rule, list_inbox_rules
)
```

## Authentication

Tokens are cached at `~/.claude/tokens/outlook-token.json`. If a request fails with 403 or authentication error, tell the user to run:
```bash
python skills/outlook/outlook_api.py auth
```

## Calendar Operations

### List Meetings
```python
events = get_calendar_events(days=7, max_events=50)
# Or use the formatted version:
list_meetings(days=7)
```

### Find Available Time
```python
suggestions = find_meeting_times(
    attendee_emails=["user@sap.com"],
    duration_minutes=30,
    days_ahead=7
)
# Returns list of {meetingTimeSlot: {start, end}, confidence}
```

### Schedule Meeting
```python
result = create_meeting(
    subject="Meeting Title",
    start_datetime="2026-02-15T14:00:00",  # ISO format, no timezone
    end_datetime="2026-02-15T14:30:00",
    attendee_emails=["user@sap.com"],
    body_text="Optional description",
    is_online=True  # Creates Teams link
)
```

## Email Operations

### Read Inbox
```python
messages = get_inbox(max_messages=25, filter_newsletters=True)
# Or formatted:
list_inbox(max_messages=15)
```

### Search Emails
```python
# Search by content
messages = search_messages('"quarterly review"', max_messages=20)

# Search by sender
messages = search_messages('"from:john.doe@sap.com"', max_messages=20)
```

### Create Draft
```python
draft = create_draft(
    to_email="user@sap.com",
    subject="Subject Line",
    body="Email body text"
)
print(f"Draft created: {draft.get('subject')}")
```

### Reply to Email
```python
# First find the message
messages = search_messages('"subject text"')
message_id = messages[0].get('id')

# Create reply draft
reply = create_reply_draft(
    message_id=message_id,
    body="Reply text here",
    reply_all=False
)
```

## Best Practices

1. **Always confirm before scheduling** - Show the user meeting details before creating
2. **Use search for replies** - Find the specific message to reply to
3. **Handle errors gracefully** - If auth fails, tell user how to re-authenticate
4. **Format dates properly** - Use ISO format without timezone suffix

## Common Patterns

### "Schedule meeting with X"
1. Ask for missing details (duration, time preference)
2. Call `find_meeting_times()` to suggest slots
3. Show options to user
4. Call `create_meeting()` with confirmed slot

### "Reply to email from X about Y"
1. Search: `search_messages('"from:x" "Y"')`
2. Get message ID
3. Call `create_reply_draft(message_id, body)`
4. Confirm draft created

### "Draft email to X"
1. Call `create_draft(to_email, subject, body)`
2. Confirm draft is in Outlook drafts folder

## Inbox Rules

### List Rules
```python
rules = get_inbox_rules()
# Or formatted:
list_inbox_rules()
```

### Get Specific Rule
```python
rule = get_inbox_rule(rule_id)
```

### Create Rule
```python
rule = create_inbox_rule(
    display_name="Move ProductBoard emails",
    conditions={
        "senderContains": ["productboard"]
    },
    actions={
        "moveToFolder": "folder_id",
        "stopProcessingRules": True
    },
    exceptions={
        "bodyContains": ["@myusername"]  # Don't move if I'm mentioned
    }
)
```

### Update Rule (add exceptions)
```python
# Add exception to skip rule if body mentions user
updated = update_inbox_rule(
    rule_id="rule-id-here",
    exceptions={
        "bodyContains": ["@username"]
    }
)
```

### Delete Rule
```python
delete_inbox_rule(rule_id)
```

### Common Rule Conditions
- `fromAddresses`: List of email address objects
- `senderContains`: List of strings to match in sender
- `subjectContains`: List of strings to match in subject
- `bodyContains`: List of strings to match in body

### Common Rule Actions
- `moveToFolder`: Folder ID to move message to
- `delete`: Boolean to delete message
- `markAsRead`: Boolean to mark as read
- `stopProcessingRules`: Boolean to stop processing other rules

## Error Handling

| Error | Solution |
|-------|----------|
| 403 Forbidden | Re-authenticate with `auth` command |
| 400 Bad Request | Check datetime format, email format |
| Timeout | Retry after a few seconds |

## Output Format

When displaying calendar or email data, use emoji formatting:
- 📅 for meetings
- 📧 for emails
- 🕐 for times
- 📍 for locations
- 👤 for organizers
- 🔗 for Teams links
