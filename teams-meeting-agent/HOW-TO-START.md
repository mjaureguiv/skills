# How to Start the Teams Meeting Agent

## Quick Command

```bash
cd /Users/d062276/Signavio_PM_Agent/skills/live-meeting-agent/temp
python3 live_meeting_agent_complete.py "your-meeting-name" 60
```

Replace `"your-meeting-name"` with part of your meeting title (e.g., "standup", "planning", "sync")

## Automatic Start via Voice Activation (NEW!)

**The agent joins ONLY when you explicitly call it with `@agent join`**

### Setup Voice Activation

1. **Start the listener (runs in background):**
   ```bash
   cd /Users/d062276/Signavio_PM_Agent/skills/live-meeting-agent/temp
   python3 agent_listener.py
   ```

2. **The listener monitors your chats but does NOT join any meetings**
   - It only listens for your commands
   - It will ONLY activate when YOU type `@agent join`
   - You have full control over when it joins

### Usage in Meeting

1. Start your Teams meeting
2. When you want the agent, type in chat: **`@agent join`**
3. The agent activates ONLY in that specific meeting
4. Type `@agent stop` when done

### Usage in Meeting

1. Start your Teams meeting
2. In the meeting chat, type: **`@agent join`**
3. The agent will automatically:
   - Detect your message
   - Join the meeting chat
   - Start monitoring and responding
   - Continue until meeting ends or you type `@agent stop`

### Voice Activation Commands

| Command | Action |
|---------|--------|
| `@agent join` | Agent joins and starts monitoring |
| `@agent start` | Same as join |
| `@agent help` | Shows agent capabilities |
| `@agent stop` | Agent stops monitoring and sends email summary |
| `@agent status` | Shows current agent status |

### Example

```
[In Teams meeting chat]

You: @agent join
Agent: 👋 Teams Meeting Agent now monitoring! Ask me about priorities, OKRs, roadmap, or any Signavio questions.

Colleague: What are our Q1 priorities?
Agent: 💡 Signavio Q1 2026 Priorities: 1. AI-Powered Process Intelligence...

You: @agent stop
Agent: ✅ Meeting summary email has been sent to your Outlook Drafts. Thanks!
```

## Which Method Should I Use?

**Use Voice Activation (`@agent join`) when:**
- You want on-demand activation
- Different meetings need the agent at different times
- You're in many meetings and only want it in specific ones

**Use Manual Start when:**
- You know you'll need the agent for specific recurring meetings
- You want to start it before the meeting begins
- You want more control over the configuration

---

**Created by:** Reagan Korabie | SAP Signavio PM | 2026-02-26
