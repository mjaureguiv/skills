> ⚠️ **This file contains instructions for GitHub Copilot (Claude), not for humans.**
> If you're a human, see [README.md](README.md) for user-friendly documentation.

---

# Acceptance Criteria Generation - Claude Instructions

You generate acceptance criteria (ACs) from a PRD or feature description, following the team's established format and style.

## Before Starting

Read these context files:
1. `context/product-context.md` - Product overview and domain knowledge
2. `context/team/config.md` - Team conventions

## Trigger

User pastes a PRD, feature description, or user story and asks for ACs.

## AC Format & Style

### Structure

Group ACs by story or feature area. Use a heading per group that matches the scope (e.g., a story name, a capability, or a behavior cluster). Under each heading, write bullet points — one per testable behavior.

```markdown
## [Area / Story Name]
- [Behavior statement]
- [Behavior statement]
```

### Writing Rules

1. **Verb-first** — Start each bullet with an action verb: "Menu appears...", "Font size changes...", "Button toggles..."
2. **Complete behavior** — State the trigger, the action, and the result in one sentence where possible
3. **Explicit states** — Call out visual/interaction states: pressed/unpressed, enabled/disabled, grayed out, open/closed
4. **Undoability** — Explicitly state when an action must be undoable
5. **Platform-specific details** — Call out OS differences where relevant (⌘ for Mac, Ctrl for Windows/Linux)
6. **Keyboard interactions** — Document keyboard shortcuts, navigation (arrow keys, Enter, Escape), and focus behavior
7. **Multi-selection behavior** — Explicitly state whether actions apply to single selection, multi-selection, or both
8. **Destructive actions** — Flag destructive operations (e.g., "styled in red to indicate destructive operation")
9. **Annotations** — Use `⚠️` for open questions, ideas for improvement, or caveats that need follow-up

### What NOT to Do

- Do not use Given/When/Then format
- Do not write vague criteria ("works correctly", "looks good", "behaves as expected")
- Do not duplicate the PRD's prose — translate intent into testable behaviors
- Do not create a single flat list — always group by area

## Process

1. **Read the full PRD** — Understand scope, user stories, and defined stories/phases
2. **Identify groupings** — Map stories or capability areas to AC sections
3. **Extract behaviors** — For each capability, enumerate every discrete testable behavior:
   - Happy path
   - Edge cases (empty state, max items, disabled state)
   - Error states
   - Keyboard / accessibility interactions
   - Visual / state feedback
   - Undo/redo behavior
   - Multi-selection vs. single-selection where relevant
4. **Apply ⚠️ annotations** — Flag anything that is ambiguous, needs design clarification, or is an open question
5. **Scope to "Now" stories by default** — If the PRD defines Now/Next phases, generate ACs for "Now" stories unless the user requests otherwise

## Output Format

```markdown
# Acceptance Criteria — [Feature Name]

## [Story / Area 1]
- [AC]
- [AC]

## [Story / Area 2]
- [AC]
- [AC]
```

Do not include a preamble or explanation — output the ACs directly.

## Working Directory

Create all temporary files in:
```
skills/acceptance-criteria/temp/
```

## Output Location

Save final output to:
```
drafts/ac-[feature-name]-[YYYY-MM-DD].md
```
