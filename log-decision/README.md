# Log Decision Skill

Automatically extract decisions from meeting transcripts and generate structured Decision Records (DRs) in Confluence wiki format.

## Quick Start

```
/log-decision
```

Then either:
- Paste your transcript directly
- Provide a file path: `/log-decision path/to/transcript.vtt`

## Features

- **Privacy-first processing**: Names are pseudonymized locally before LLM analysis
- **Multi-input support**: Pasted text, markdown files, MS Teams VTT exports
- **Multi-decision detection**: Automatically finds multiple decisions and lets you choose which to document
- **Auto-extraction**: Extracts metadata (deciders, date, category) from transcript
- **CODES validation**: Checks decision quality against CODES framework
- **Uncertainty flagging**: Marks sections where extraction confidence is low
- **Confluence output**: Generates wiki markup ready for your SAP Wiki

## Privacy Protection

This skill includes built-in privacy protection for personal data:

1. **Before LLM processing**: All names in the transcript are replaced with pseudonyms (Person_A, Person_B, etc.) locally using `pseudonymize.py`
2. **During LLM analysis**: Only pseudonymized text is processed - real names never leave your machine
3. **After processing**: Original names are restored locally before generating the final output

This ensures compliance with data protection requirements while still enabling AI-assisted decision extraction.

## Input Formats

### Pasted Text
Simply paste your meeting transcript after invoking the skill.

### File Path
```
/log-decision ~/transcripts/team-meeting-2026-02-19.txt
```

### MS Teams Export
Export transcript from MS Teams (VTT format) and provide the file path:
```
/log-decision ~/Downloads/meeting-transcript.vtt
```

## Output

The skill generates a `.confluence` file in the `drafts/` directory:
```
drafts/decision-record-2026-02-19-api-versioning.confluence
```

Copy the contents to your wiki or use the wiki skill to publish.

## CODES Quality Check

Each decision record is validated against the CODES framework:

| | Dimension | What It Checks |
|---|-----------|----------------|
| **C** | Clarity | Is the problem and decision clear? |
| **O** | Ownership | Who owns/is accountable for this decision? |
| **D** | Decision | Are options and chosen path explicit? |
| **E** | Engagement | Which teams affected? Communication plan? |
| **S** | Structure | Are next steps and governance defined? |

Gaps are flagged with improvement suggestions.

## Decision Record Template

The generated DR follows the standard template with these sections:

**Metadata:**
- Project, Technical Story, Status, Category, Function
- Deciders, Authors, Outcome, Date

**Content:**
- Problem Statement and Context
- Decision Drivers
- Considered Options
- Decision Outcome & Rationale
- Positive/Negative Consequences
- Next Steps
- Pros/Cons per Option
- Links

## Example Usage

### From a Teams Meeting
1. Export transcript from MS Teams
2. Run `/log-decision ~/Downloads/transcript.vtt`
3. Select which decision(s) to document
4. Review and confirm extracted metadata
5. Review generated draft with CODES assessment
6. Find output in `drafts/decision-record-*.confluence`

### From Notes
1. Run `/log-decision`
2. Paste your meeting notes
3. Follow prompts to complete the decision record

## Tips

- **Better transcripts = better extraction**: Ensure speakers are identified in the transcript
- **Multiple decisions**: The skill detects multiple decisions - you can document all or select specific ones
- **Review uncertainties**: Look for `⚠️ [UNCERTAIN]` markers and provide clarification
- **CODES gaps**: Address any flagged CODES gaps before publishing

## Related Skills

- [Transcript to Notes](../transcript-to-notes/) - Convert transcripts to meeting notes
- [Wiki](../wiki/) - Search and fetch from SAP Wiki
- [Meeting Facilitator](../meeting-facilitator/) - Facilitation methods

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-02-24 | Claude | Added Changelog section for compliance with CLAUDE.md guidelines |
