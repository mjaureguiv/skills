# transcript-to-notes

Convert Microsoft Teams meeting transcripts into structured, actionable notes in under 2 minutes.

## What This Does

Takes meeting transcripts from Microsoft Teams and generates clean, structured notes with:
- Key discussion points
- Decisions made
- Action items
- Follow-ups needed
- Relevant context/links

## Why This Exists

Extracting value from meeting transcripts manually drains energy. This automates the documentation work so you can focus on outcomes.

## Usage

### Option 1: Paste Transcript
```
Please use the transcript-to-notes skill on this transcript:

[paste transcript here]
```

### Option 2: File Upload
```
Please use the transcript-to-notes skill on @path/to/transcript.txt
```

### Option 3: With Context
```
Please use the transcript-to-notes skill. This was a meeting about [topic] with [attendees].

[paste transcript]
```

## Features

- **Outlook Calendar Integration**: Automatically fetches meeting details from your calendar
- **Microsoft Teams Transcripts**: Works with Teams .vtt, .docx, or pasted text
- **Auto-Filing**: Saves notes to `meetings/` directory with proper naming

## Prerequisites

**Optional (enhances output):**
- Microsoft Graph API token for calendar access
- Get from: https://developer.microsoft.com/en-us/graph/graph-explorer

**Note**: Works perfectly fine without calendar integration - just generates notes from transcript only.

## Output Format

```markdown
# Meeting Notes: [Topic/Title]

**Date**: [Date]
**Attendees**: [List with roles]

## Quick Summary
[2-3 sentences]

## Key Discussion Points
...

## Decisions Made
...

## Action Items
...

## Follow-ups Needed
...
```

## Getting Teams Transcripts

1. Open the meeting chat in Microsoft Teams
2. Click on the transcript tab
3. Download as .vtt or .docx file
4. Provide file path to this skill (or copy/paste the text)

## Tips

- Provide meeting context for better results
- Works with partial transcripts
- Handles poor quality transcripts gracefully

## Related Skills

- `powerpoint` - Convert notes into presentation slides
- `sbi-feedback` - Extract feedback situations from discussions

## Support

Questions or issues? Reach out in #claude-code-help

---

**Original Author**: Aviral Vaid (LeanIX Product Management)
**Category**: Workflow Automation
**Integrated from**: [LeanIX PM Marketplace](https://github.tools.sap/LeanIX/LeanIX-PM-Marketplace)
