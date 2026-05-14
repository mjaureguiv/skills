# Lovable Prompt Generation

Generate detailed Lovable AI prompts from Jira tickets or feature descriptions.

## What This Skill Does

- **Fetches Jira issues** and extracts feature requirements
- **Transforms PM language** into developer/AI-friendly implementation prompts
- **Generates detailed prompts** with user stories, technical specs, UI/UX requirements, and data models
- **Supports multiple input methods** - Jira issue keys or pasted text
- **Creates structured output** ready for Lovable AI to generate code

## How to Use

### From Jira Issue

```
Generate Lovable prompt for PROJ-123
```

```
Create a Lovable prompt from SIGNAVIO-456
```

### From Pasted Text

```
Generate Lovable prompt for this feature:
[paste your feature description here]
```

```
Convert this to a Lovable prompt:

Feature: User Authentication
Users need to log in with SSO...
```

## What Gets Generated

**Output location:** `outputs/lovable-prompts/`

**File format:** `lovable-prompt-[issue-key or title]-[YYYY-MM-DD].md`

**Content includes:**
- User story (As a... I want... So that...)
- Context and background
- Complete user flow
- UI/UX component specifications
- Data models (TypeScript interfaces)
- API endpoint specifications
- Acceptance criteria
- Edge cases and error handling
- Technical constraints
- Implementation guidance

## Tips

### For Best Results

- **Jira issues should include:**
  - Clear feature description
  - Acceptance criteria
  - UI/UX requirements (if applicable)
  - Technical constraints

- **Pasted text should include:**
  - Feature title and purpose
  - User persona and goals
  - Expected behavior
  - Any technical requirements

### What Makes a Good Lovable Prompt

- **Specific UI details** - Button labels, form fields, screen layouts
- **Clear data models** - Entity structures and relationships
- **API specifications** - Endpoints, request/response formats
- **Edge cases** - What happens when things go wrong
- **User flows** - Step-by-step interaction patterns

## Examples

### Input (Jira Issue PROJ-123)

```
Summary: Add export to Excel feature
Description: Users should be able to export their dashboard data to Excel...
Acceptance Criteria:
- Export button in dashboard header
- Generates Excel file with all visible data
- Includes charts as images
```

### Output (Generated Lovable Prompt)

Detailed prompt with:
- User story for data export feature
- UI specifications for export button placement
- Data model for export format
- API endpoint for generating Excel file
- Error handling for large datasets
- Implementation guidance for Excel library

---

*For AI implementation details, see [CLAUDE.md](CLAUDE.md)*
