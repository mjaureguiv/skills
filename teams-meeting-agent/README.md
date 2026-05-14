# Teams Meeting Agent

**Author:** Reagan Korabie

An AI agent that joins your Microsoft Teams or Zoom meetings in real-time to answer questions, take notes, and track action items.

## What This Skill Does

- **Answers questions in meeting chat** - Participants can ask questions and get AI-powered responses
- **Takes live meeting notes** - Captures decisions, action items, and key discussion points in real-time
- **Generates post-meeting summaries** - Creates structured notes with decisions and next steps
- **Proposes Jira tickets** - Identifies action items and proposes tickets (with your approval)
- **Provides proactive suggestions** - Flags important points and suggests relevant context

## Supported Platforms

- ✅ **Microsoft Teams** - Full support (MVP)
- 🔜 **Zoom** - Coming soon

## How to Use

### Start Monitoring a Meeting

Open Copilot Chat (`Ctrl+Shift+I` / `Cmd+Shift+I`) and ask:

```
Start monitoring my next Teams meeting and answer questions in chat
```

or

```
Join the Teams meeting at [meeting URL] and take notes
```

### During the Meeting

**Participants can ask questions in chat**:
- "What were the Q3 priorities we discussed last time?"
- "Can you summarize the decisions made so far?"
- "What action items do we have?"

The agent will respond in the meeting chat with relevant answers based on:
- Current meeting context
- Previous meeting notes
- Company knowledge base

### End of Meeting

When the meeting ends, the agent will:
1. Generate a structured meeting summary
2. Save notes to `drafts/meeting-notes-[date].md`
3. Post summary in meeting chat
4. **Propose Jira tickets** for action items (you approve before creation)

## Example Prompts

```
# Basic monitoring
Start the live meeting agent for my current meeting

# Specific meeting
Monitor the Teams meeting "Product Planning Sync" and take notes

# Stop monitoring
Stop the meeting agent and generate the final summary

# Review what happened
Show me the notes from today's standup meeting
```

## What Gets Generated

### Meeting Notes Format

Saved to: `drafts/meeting-notes-YYYY-MM-DD.md`

```markdown
# Meeting Notes: Product Planning Sync

**Date**: 2026-02-25
**Platform**: Microsoft Teams
**Participants**: Alice, Bob, Charlie

## Summary
[2-3 sentence overview of meeting]

## Key Decisions
- [Decision 1]
- [Decision 2]

## Action Items
| Item | Owner | Deadline |
|------|-------|----------|
| [Task] | [Name] | [Date] |

## Discussion Notes
### [Topic 1]
[Summary]

## Q&A from Chat
- **Q**: [Question asked]
- **A**: [Agent's response]

## Next Steps
- [Step 1]
```

### Jira Ticket Proposals

After the meeting, the agent will present:

```
📋 Proposed Jira Tickets (3 action items found):

1. [PROJ-XXX] Finalize Q2 roadmap priorities
   - Owner: Alice
   - Deadline: 2026-03-01
   - Description: Review and finalize priorities based on today's discussion

2. [PROJ-XXX] Update design mockups for mobile app
   - Owner: Bob
   - Deadline: 2026-02-28

Create these tickets? [Yes / No / Edit]
```

**You must approve** before any Jira tickets are created.

## Features

### Real-Time Q&A

- Agent monitors meeting chat continuously
- Responds to questions from participants
- Uses company context and previous meeting notes
- Configurable response confidence threshold

### Live Note-Taking

- Captures key points as they're discussed
- Identifies decisions being made
- Tracks action items with owners
- Maintains meeting context throughout

### Proactive Assistance

- Suggests related context when relevant
- Flags important discussion points
- Reminds about previous decisions on same topic
- Offers next steps based on discussion

### SAP Compliance

- ✅ Chat messages only (no audio/video recording)
- ✅ OAuth authentication (no stored secrets)
- ✅ Local data storage with user control
- ✅ Explicit consent required from meeting organizer
- ✅ Jira ticket creation requires approval

## Setup

### Prerequisites

1. **Microsoft Teams Integration** must be configured
   - See [tools/teams/README.md](../../tools/teams/README.md) for setup

2. **Jira Integration** (optional, for ticket creation)
   - See [tools/jira/README.md](../../tools/jira/README.md) for setup

3. **Authenticated Accounts**
   - Microsoft account with Teams access
   - Jira account (if using ticket creation)

### First-Time Setup

1. Authenticate with Microsoft Teams:
   ```bash
   # Follow Teams MCP setup instructions
   ```

2. Test the agent:
   ```
   Start monitoring my next Teams meeting
   ```

3. The agent will join and begin monitoring when the meeting starts.

## Configuration

### Polling Interval

Default: Check for new messages every 5 seconds

Adjust in `skills/live-meeting-agent/meeting_processor.py`:
```python
POLLING_INTERVAL = 5  # seconds
```

### Response Confidence

Control when the agent responds to questions:
```python
MIN_CONFIDENCE = 0.7  # Only respond if >70% confident
```

### Auto-Response

Disable automatic responses to questions:
```
Configure live meeting agent to only take notes, don't answer questions
```

## Compliance & Privacy

### What the Agent Accesses

- ✅ Meeting chat messages (text only)
- ✅ Calendar events (to identify meetings)
- ✅ Your company context files

### What the Agent Does NOT Access

- ❌ Audio or video streams
- ❌ Meeting recordings
- ❌ Screen sharing content
- ❌ Private chats outside the meeting
- ❌ Attendee contact information

### Data Storage

- **Meeting notes**: Stored locally in `drafts/`
- **Active meeting state**: Temporary in `skills/live-meeting-agent/temp/`
- **Auth tokens**: Secure storage in `~/.claude/tokens/`

### Participant Consent

**Important**: Meeting participants must be informed that an AI agent is present and monitoring chat. As the meeting organizer, you are responsible for:
1. Notifying participants before the meeting starts
2. Ensuring compliance with company policies
3. Respecting participant privacy preferences

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Agent doesn't respond | Check Teams MCP is authenticated and running |
| No meeting found | Ensure you have an active Teams meeting |
| Authentication expired | Re-authenticate using Teams MCP setup |
| Jira tickets not created | Verify Jira integration is configured |
| Missing responses | Check response confidence threshold setting |

### Debug Mode

Enable verbose logging:
```
Enable debug mode for live meeting agent
```

## Roadmap

### Phase 1 (Current): Teams MVP
- ✅ Join and monitor Teams meetings
- ✅ Answer questions in chat
- ✅ Take live notes
- ✅ Generate post-meeting summary
- ✅ Propose Jira tickets

### Phase 2 (Planned)
- 🔜 Zoom meeting support
- 🔜 Proactive suggestions during meeting
- 🔜 Integration with Confluence for note storage
- 🔜 Meeting intelligence (suggest agenda items, identify risks)

### Phase 3 (Future)
- Multi-language support
- Custom response templates
- Meeting analytics and insights
- Integration with OKR tracking

## Tips

- **Set clear expectations**: Let participants know the agent is there to help
- **Review before sharing**: Always review meeting notes before sharing widely
- **Approve Jira tickets**: Review proposed tickets before creating them
- **Customize context**: Add company-specific context files for better responses

---

## Author & Contributors

**Created by:** Reagan Korabie
**Date:** 2026-02-26
**Team:** SAP Signavio Product Management

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-02-26 | Reagan Korabie | Initial MVP release: Core agent logic, Q&A capability, context-aware responses using Signavio knowledge base, automatic email summary generation |

---

*For technical implementation details, see [CLAUDE.md](CLAUDE.md)*
