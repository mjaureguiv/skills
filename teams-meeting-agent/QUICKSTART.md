# Teams Meeting Agent - Quick Start

**Author:** Reagan Korabie

## Two Ways to Start the Agent

### ⭐ Method 1: Voice Activation (Recommended!)

**Control the agent with chat commands**

#### Setup (One Time):
```bash
cd /Users/d062276/Signavio_PM_Agent/skills/live-meeting-agent/temp
python3 agent_listener.py
```
Keep this running in the background. The listener monitors for your commands but **does not join any meetings automatically**.

#### Usage in Any Meeting:
When you're in a meeting and want the agent to join, type in chat:
```
@agent join          # YOU activate the agent when YOU want it
@agent stop          # Stop monitoring and get email summary
@agent help          # Show agent capabilities
@agent status        # Check if agent is active
```

**The agent only joins when you explicitly type `@agent join`** - never automatically!

### Method 2: Manual Start

Start the agent before your meeting:

```bash
cd /Users/d062276/Signavio_PM_Agent/skills/live-meeting-agent/temp
python3 live_meeting_agent_complete.py "meeting name" 60
```

**Parameters:**
- `"meeting name"` - Part of your meeting title (e.g., "standup", "planning")
- `60` - Duration in minutes (default: 60)

**Example:**
```bash
# For "Product Planning Meeting"
python3 live_meeting_agent_complete.py "product planning" 60

# For "Daily Standup"
python3 live_meeting_agent_complete.py "standup" 30

# For any meeting with "test" in the name
python3 live_meeting_agent_complete.py "test" 30
```

### During the Meeting

The agent will:
- ✅ Automatically join the meeting chat
- 👀 Monitor all messages
- 🤔 Detect questions (anything ending with ? or starting with what/how/why/etc.)
- 💡 Respond immediately with context-aware answers
- 📝 Track all Q&A exchanges

### After the Meeting

When the meeting ends (or time limit reached), the agent automatically:
- 📧 **Creates an email draft in Outlook** with the full summary
- 📊 Includes all Q&A exchanges
- ✨ Professionally formatted HTML email

**You just need to:**
1. Open Outlook
2. Go to Drafts folder
3. Find the meeting summary email
4. Add recipients
5. Send!

## Example Output

```
🚀 Teams Meeting Agent - Starting
   Duration: 30 min
   Polling: every 5s

🔍 Finding meeting...
✅ Joined: Meeting Agent test meeting

📨 2 new message(s)
💬 Reagan Korabie: What are our Q1 priorities?
   🤔 Question detected
   ✅ Response sent
💬 Reagan Korabie: What are the OKRs?
   🤔 Question detected
   ✅ Response sent

⏹️  Stopped by user

============================================================
📝 Meeting ended - generating summary...
📧 Creating email summary...
✅ Email draft created successfully!
   Subject: Meeting Summary: Meeting Agent test meeting - Feb 26, 2026
   Check your Outlook Drafts folder
✅ Teams Meeting Agent session complete
```

## Setup Requirements

### 1. Teams Authentication
Already configured ✅

### 2. Outlook Authentication
If email doesn't work, run:
```bash
python skills/outlook/outlook_api.py auth
```

### 3. Knowledge Base
Edit `context/signavio-knowledge-base.md` to add more product knowledge

## Customization

### Add More Knowledge
Edit these files to improve responses:
- `context/signavio-knowledge-base.md` - Product information
- `context/product-context.md` - Current product status
- `context/active-work.md` - Current initiatives

### Change Response Logic
Edit `live_meeting_agent_complete.py` in the `generate_response()` method to customize how the agent answers questions.

## Tips

1. **Start before the meeting** - Launch the agent 1-2 minutes before meeting starts
2. **Use specific names** - Filter by meeting name to avoid joining wrong meetings
3. **Keep it running** - Don't close the terminal during the meeting
4. **Check Drafts** - Email summary is always in Outlook Drafts, never sent automatically

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No meeting found" | Check meeting title filter, ensure meeting is started |
| "Could not create email" | Run Outlook auth: `python skills/outlook/outlook_api.py auth` |
| Agent not responding | Check that questions end with `?` or start with question words |
| Wrong meeting joined | Use more specific meeting name filter |

## Future Enhancements

Coming soon:
- Voice/transcript monitoring (Teams live captions)
- Automatic Jira ticket creation
- Confluence note publishing
- Multi-language support

---

**Questions?** Check [skills/live-meeting-agent/README.md](../README.md) for full documentation.

---

**Created by:** Reagan Korabie | SAP Signavio Product Management | 2026-02-26

