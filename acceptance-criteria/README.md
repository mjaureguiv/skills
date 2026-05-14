# Acceptance Criteria Skill

Generate structured, testable acceptance criteria from a PRD or feature description — following the team's established format.

## What It Does

Reads a PRD (or pasted feature description) and produces a grouped list of acceptance criteria (ACs) in the team's standard style:

- Grouped by story or capability area
- Verb-first, behavior-complete bullet points
- Explicit states, keyboard interactions, platform-specific details
- ⚠️ annotations for open questions and caveats
- Scoped to "Now" stories by default

## How to Use

Paste your PRD content into the chat and say:

> "Generate ACs for this PRD"

Or reference a specific scope:

> "Generate ACs for Story 1 and Story 2 only"

## Output Format

```markdown
# Acceptance Criteria — [Feature Name]

## [Story / Area]
- Behavior statement one
- Behavior statement two
- ⚠️ Open question or caveat
```

## Output Location

Saved to `drafts/ac-[feature-name]-[YYYY-MM-DD].md`

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-03-23 | Ariel | Initial skill creation |
