# Jira Integration

Create and manage Jira tickets directly from VS Code.

## What This Skill Does

- Creates well-structured Jira tickets from requirements or notes
- Searches existing tickets
- Adds comments to tickets
- Fetches ticket details

## How to Use

Open Copilot Chat (`Ctrl+Shift+I`) and use the prompt:

```
#create-jira Create a ticket for [your requirement]
```

### Example Prompts

```
#create-jira Create a User Story for implementing SSO with Azure AD

#create-jira Create a bug ticket for the login timeout issue

#create-jira Create tickets from these meeting notes: [paste notes]
```

## Prerequisites

1. **Node.js** installed (Company Portal or https://nodejs.org/)
2. **Jira authentication** configured (see [Setup Guide](../../setup/README.md))

## What Gets Generated

- **For new tickets**: XML files saved to `outputs/jira-exports/`
- **For existing tickets**: Content to copy-paste into Jira

## Available Scripts

| Script | Purpose |
|--------|---------|
| `scripts/create-jira-ticket.js` | Create a new ticket |
| `scripts/get-issue-types.js` | List valid issue types for a project |
| `scripts/get-issue.js` | Fetch ticket details |
| `scripts/search-issues.js` | Search tickets with JQL |
| `scripts/add-comment.js` | Add comment to existing ticket |

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
| **Background** | Orange (#f1a208) | Context, personas, architecture, scope |
| **Acceptance Criteria** | Green (#aad17b) | Testable requirements |
| **Notes** | Gray (#cccccc) | Dependencies, open questions, misc |

Every Epic includes:
- **Value Proposition** - Why this matters
- **Outcomes** - What we want to achieve
- **Background** - Context and scope
- **Acceptance Criteria** - Testable conditions
- **Notes** - Dependencies and open questions

## Tips

- Specify the project key if you have multiple projects
- Include acceptance criteria in your request
- Reference related tickets for linking
- **All content is generated in English** regardless of input language

---

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-02-10 | I526427 | Added standardized Epic format with three colored panels (Background, Acceptance Criteria, Notes) |

---

*For technical implementation details, see [CLAUDE.md](CLAUDE.md)*
