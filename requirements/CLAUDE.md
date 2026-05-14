> ⚠️ **This file contains instructions for GitHub Copilot (Claude), not for humans.**
> If you're a human, see [README.md](README.md) for user-friendly documentation.

---

# Requirements Extraction - Claude Instructions

You analyze raw input and extract structured, actionable requirements.

## Before Starting

Read these context files:
1. `context/product-context.md` - Product overview (for context)
2. `context/team/config.md` - Team conventions

## Extraction Process

1. **Identify requirement statements** - Look for:
   - "We need...", "Users should...", "The system must..."
   - Pain points and complaints
   - Feature requests
   - Acceptance criteria mentions

2. **Categorize** - Sort into:
   - Functional requirements
   - Non-functional requirements
   - User experience requirements
   - Technical constraints

3. **Structure as user stories**:
   ```
   As a [user type]
   I want [action/capability]
   So that [benefit/outcome]
   ```

4. **Flag ambiguities** - Note:
   - Vague requirements ("should be fast")
   - Missing acceptance criteria
   - Conflicting statements
   - Questions to clarify

## Output Format

```markdown
# Requirements Extracted from [Source]

## Summary
- Total requirements: X
- Functional: X
- Non-functional: X
- Ambiguous/needs clarification: X

## Functional Requirements

### REQ-001: [Title]
- **User Story**: As a... I want... So that...
- **Priority**: High/Medium/Low
- **Notes**: [additional context]

## Open Questions
- [List questions that need answers]
```

## Working Directory

**IMPORTANT**: Create all temporary files in this skill's temp folder:
```
skills/requirements/temp/
```

## Output Location

Save to: `drafts/requirements-[topic]-[YYYY-MM-DD].md`

## Troubleshooting

If you encounter issues:
1. Document the problem in `troubleshooting/CLAUDE.md`
2. Include: problem description, steps to reproduce, solution found
