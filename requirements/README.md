# Requirements Extraction

Extract structured requirements from raw notes, documents, or conversations.

## What This Skill Does

- Analyzes raw input (meeting notes, transcripts, emails)
- Extracts actionable requirements
- Structures them into user stories or specifications
- Identifies gaps and ambiguities

## How to Use

Open Copilot Chat (`Ctrl+Shift+I`) and use the prompt:

```
#extract-requirements [paste your raw notes]
```

### Example Prompts

```
#extract-requirements 
Here are my notes from the customer call:
[paste notes]

#extract-requirements Analyze this document and extract all requirements:
[paste document]
```

## What Gets Generated

Extracted requirements are saved to:
```
drafts/requirements-[topic]-[date].md
```

## Output Format

For each requirement:
- Clear user story format
- Priority indication
- Open questions (if any)
- Dependencies identified

## Tips

- Include as much context as possible
- Mention the source (customer call, internal meeting, etc.)
- Flag if you need a specific format (Jira-ready, PRD section)

---

*For technical implementation details, see [CLAUDE.md](CLAUDE.md)*
