# Email Reply Drafting - AI Instructions

## Purpose

Help users draft email responses through an interactive 3-step workflow:
1. Extract critical points from the email
2. Ask user's position on each point
3. Draft reply using their voice profile

## When to Use

Trigger this skill when the user asks to:
- "Help me reply to [email]"
- "Draft a response to [subject]"
- "What should I respond to [Name]?"
- "Reply to the email from [Name]"

---

## Workflow

### Step 0: Pre-Flight Check (CRITICAL)

**Before doing anything else**, verify Outlook authentication:

```python
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(repo_root))

try:
    from skills.outlook.outlook_api import get_access_token
    token = get_access_token()
    print("✅ Outlook: Authenticated")
    outlook_ready = True
except Exception as e:
    print(f"❌ Outlook: Not authenticated")
    outlook_ready = False
```

**If Outlook is NOT authenticated**, show this friendly message:

```
I need to connect to your Outlook to read the email.

**One-time setup** (takes ~30 seconds):

1. I'll run the authentication command
2. You'll see a code and a URL
3. Open the URL in your browser and enter the code
4. Sign in with your SAP account

Ready to set up?
```

**Do NOT proceed until auth succeeds.**

Also check if voice profile exists:

```python
from pathlib import Path
voice_profile_path = Path("context/team/pm-voice-samples.md")
if voice_profile_path.exists():
    print("✅ Voice profile found - will use your writing style")
else:
    print("⚠️ No voice profile - will use professional default style")
    print("   (Run #analyze-voice to create your personal profile)")
```

---

### Step 1: Find & Read the Email

Use the Outlook API to find the email:

```python
from skills.outlook.outlook_api import get_access_token
import requests

token = get_access_token()
headers = {'Authorization': f'Bearer {token}'}

# Get recent emails
response = requests.get(
    'https://graph.microsoft.com/v1.0/me/messages',
    headers=headers,
    params={
        '$top': 50,
        '$select': 'id,subject,from,receivedDateTime,body,bodyPreview',
        '$orderby': 'receivedDateTime desc'
    }
)
```

Parse the email thread to understand the full context.

### Step 2: Extract Critical Points

Analyze the email and identify:

1. **Points requiring response** - Questions asked, decisions needed, opinions requested
2. **Who raised each point** - Track the person for proper attribution
3. **Deadlines or blockers** - Any time-sensitive elements
4. **Assumptions being made** - That may need confirmation or pushback

Present to user in a structured format:

```
Found the email thread about [subject]. Here are the points that need your response:

| # | Point | Raised By | Urgency |
|---|-------|-----------|---------|
| 1 | [Description] | [Name] | [High/Medium/Low] |
| 2 | [Description] | [Name] | [High/Medium/Low] |
```

### Step 3: Ask User's Position

Ask the user's position on each point:

```
For each point above, what's your position?

1. [Point 1]: 
   - Agree / Disagree / Need more info
   - Any specific action you want to propose?

2. [Point 2]:
   - Agree / Disagree / Need more info
   - Any specific action you want to propose?
```

Allow free-form input so user can express nuanced positions.

### Step 4: Draft Reply in Chat

**DO NOT create files.** Output the draft directly in the chat.

1. **Read the voice profile** from `context/team/pm-voice-samples.md`
2. **Apply the user's positions** to each point
3. **Structure the reply** following their patterns:
   - Use their greeting style
   - Use their action phrases
   - Use their structural patterns (bullets, numbered lists)
   - Use their closing signature

Output format:

```markdown
---

**Draft Reply:**

[The actual email text, ready to copy/paste]

---

*Want me to adjust the tone, add/remove points, or make it shorter/longer?*
```

## Voice Profile Integration

Read from `context/team/pm-voice-samples.md` if it exists.

Key elements to apply:
- **Greeting patterns** - Match formality to context
- **Action phrases** - Use their "Please..." or "Would be great if..." style
- **Tone characteristics** - Direct vs. elaborate, warm vs. businesslike
- **Signature vocabulary** - Their distinctive terms
- **Structural patterns** - Bullets, headers, paragraph length
- **Closing signature** - Their sign-off style

If no profile exists, use professional but direct tone.

## Anti-Patterns

**DON'T:**
- Create draft files in the drafts/ folder
- Make assumptions about user's position
- Include points the user didn't address
- Add corporate fluff the user's profile doesn't support
- Send emails without explicit user confirmation

**DO:**
- Always ask position before drafting
- Output draft in chat for easy copy/paste
- Offer to revise
- Match the user's voice exactly
