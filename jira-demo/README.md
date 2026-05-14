# Jira Demo

Generate Jira Epic and User Story content from chat — copy and paste into Jira yourself.

## What This Skill Does

A simplified version of the [Jira skill](../jira/README.md) designed for **demos, workshops, and quick prototyping**. Instead of requiring a Wiki page as the source of truth, you provide requirements directly in the conversation.

- Generates well-structured Jira Epic and User Story content in Jira Wiki Markup
- Displays all output directly in the chat window for copy/paste
- **Does NOT create tickets in Jira** — you copy the output and create tickets manually

## How to Use

Open Copilot Chat and describe your requirements:

```
Create an Epic for implementing a process status filter.
Requirements:
- Users can filter by Active, Draft, Archived
- Filters persist across sessions
- Affects process list view only
```

### Example Prompts

```
Create an Epic for SSO integration with Azure AD. The feature should
support SAML 2.0, automatic user provisioning, and role mapping.

Break down this Epic into User Stories: We need a notification system
that alerts process owners when their processes are modified.

Create a User Story for adding bulk export of process diagrams to PDF.
```

## Differences from Jira Skill

| Feature | Jira | Jira Demo |
|---------|------|-----------|
| Requirements source | Wiki page (mandatory) | Chat conversation |
| Wiki link in tickets | Always included | Not included |
| Creates tickets in Jira | Yes (scripts/MCP) | **No** — output only |
| Output | Tickets created in Jira | Jira Wiki Markup in chat window |
| Prerequisites | Node.js, Jira auth, SAP Jira MCP | **None** — fully standalone |
| Best for | Production tickets | Demos, workshops, prototyping |

## Prerequisites

None — this skill is fully standalone. No Jira authentication, MCP tools, or scripts required.

## Ticket Quality Guidelines

Good tickets follow **INVEST** principles:
- **I**ndependent - can be developed separately
- **N**egotiable - details can be discussed
- **V**aluable - delivers user/business value
- **E**stimable - team can estimate effort
- **S**mall - fits in a sprint
- **T**estable - has clear acceptance criteria

## Epic Format

When creating Epics, we use a standardized format with three colored panels:

| Panel | Color | Purpose |
|-------|-------|---------|
| **Background** | Orange (#D97B00) | Context, personas, architecture, scope |
| **Acceptance Criteria** | Green (#3D8B3D) | Testable requirements |
| **Notes** | Gray (#707070) | Dependencies, open questions, misc |

## User Story Format

User Stories use four colored panels:

| Panel | Color | Purpose |
|-------|-------|---------|
| **Background** | Orange (#D97B00) | Context and constraints |
| **Acceptance Criteria** | Green (#3D8B3D) | Testable requirements |
| **Design** | Blue (#2A7AB5) | UI/UX references, mockups, Figma links |
| **Notes** | Gray (#707070) | Technical notes, dependencies |

## Tips

- Provide as much detail as possible in your requirements
- Specify personas, constraints, and expected outcomes
- Reference related tickets for linking
- **All content is generated in English** regardless of input language

---

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-03-19 | I526427 | Initial creation — chat-based variant of Jira skill |
| 2026-03-19 | I526427 | Changed to output-only — no direct Jira creation |

---

*For technical implementation details, see [CLAUDE.md](CLAUDE.md)*
