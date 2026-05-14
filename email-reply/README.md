# Email Reply Drafting

**Interactive workflow to draft email responses using your voice profile.**

## What This Skill Does

1. **Finds & reads** the email you want to reply to
2. **Extracts critical points** that need your response
3. **Asks your position** on each point
4. **Drafts the reply** in chat using your voice profile

## Quick Start

Ask Copilot:

```
Help me reply to the email from [Name] about [topic]
```

```
Draft a response to [subject line]
```

```
What should I respond to [Name]'s email?
```

## Workflow Example

**Step 1 - Analysis:**
> "Found the email from Maryna about Dodo Roadmap. Here are the points that need your response:
> 
> 1. **CRNK deadline** (raised by Christopher): November is a hard deadline
> 2. **SPG-HAIM scope** (raised by Sonja): Needs clearer naming and expanded scope
> 3. **Security items** (raised by Christopher): Not visible in ProductBoard"

**Step 2 - Your input:**
> "What's your position on each?
> 1. CRNK deadline: [your view]
> 2. SPG-HAIM: [your view]
> 3. Security items: [your view]"

**Step 3 - Draft:**
> "Here's your reply based on your positions and voice profile:
> [Draft appears in chat]"

## Prerequisites

- Outlook skill authenticated
- Voice profile at `context/team/pm-voice-samples.md` (optional but recommended)

## Output

- Draft appears **in chat** (no files created)
- You can copy/paste directly to Outlook
- Or ask for revisions before sending

---

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-02-19 | Adriana Rotaru | Added pre-flight auth checks and voice profile detection |
| 2026-02-19 | Adriana Rotaru | Initial skill creation with 3-step interactive workflow |
