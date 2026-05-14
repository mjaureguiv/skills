# SPG Customer Assistant

A skill for responding to SPG (SAP Signavio Process Governance) customer inquiries with consistent, accurate answers.

## What It Does

- Answers customer questions using a local knowledge base
- Handles bug reports with known workarounds
- Processes feature requests (single or bulk via Excel)
- Prepares roadmap session materials
- Tracks all customer interactions
- References JIRA ticket history for context

## How to Use

Invoke with `/pm-customer-requests-assistant` and mention SPG, or paste a customer inquiry and ask for help.

**Examples:**
- "Help me answer this customer email"
- "Process these feature requests from Mercedes"
- "Prepare for the Daimler roadmap session"

## Files

| File/Folder | Purpose |
|-------------|---------|
| `customer-log.md` | Audit trail of all interactions |
| `knowledge/faq.md` | Common questions and answers |
| `knowledge/known-issues.md` | Bugs and workarounds |
| `knowledge/jira-tickets/` | JIRA exports for support context |
| `knowledge/release-notes.md` | Recent release information |
| `knowledge/sample-responses/` | Past email examples for tone |
| `roadmap-sessions/` | Session prep and archives |

## Managing the Knowledge Base

### Add a FAQ Entry

Edit `knowledge/faq.md`:

```markdown
### Q: [Customer's question]
**Answer:** [Your answer]
**Related docs:** [Link if applicable]
```

### Add a Known Issue

Edit `knowledge/known-issues.md`:

```markdown
### Issue: [Description]
**Status:** [Under investigation / Fixed in X.Y]
**Workaround:** [Steps]
**ETA:** [If known]
```

### Add a Sample Response

Add to appropriate file in `knowledge/sample-responses/`:
- `feature-requests.md` - Feature request acknowledgments
- `how-to-questions.md` - Support answers
- `bug-reports.md` - Bug report responses

## Customer Interaction Log

All interactions are logged in `customer-log.md` with:
- Date
- Customer name
- Request type
- Summary
- Action taken
- Response date

## Productboard Integration

The skill can:
- Search for existing feature requests
- Create new items from customer feedback
- Link customers to existing features

Requires Productboard MCP tools to be configured.
