# Epic Breakdown

Get a hierarchical view of all active epics and their child stories in a Jira project.

## What It Does

This skill queries your Jira project and returns:
- All active (non-closed) epics
- Child issues linked to each epic (stories, tasks, bugs)
- Status summary for each epic

## When to Use

- **Sprint planning** - See what work exists under each epic
- **Status reviews** - Understand progress at the epic level
- **Backlog grooming** - Find epics with too many or too few stories
- **Stakeholder updates** - Show epic-level progress

## How to Use

Simply ask:
- "Show me all active epics in SIGDMN"
- "Give me an epic breakdown for project MOB"
- "List epics and their stories in SIGDMN"

## Example Output

```
## Epic Breakdown for SIGDMN

### SIGDMN-491: DMN XML Import
**Status:** In Progress | **Children:** 4

| Key | Type | Summary | Status | Assignee |
|-----|------|---------|--------|----------|
| SIGDMN-537 | Story | Explore error responses | In Progress | I744741 |
| SIGDMN-538 | Story | Import validation | To Do | Unassigned |

---

### SIGDMN-453: Enumeration Expressions
**Status:** Backlog | **Children:** 0
(No linked stories)
```

## Options

- **Filter by status**: "Show only In Progress epics"
- **Summary view**: "Give me a summary of epics" (counts only, no children listed)
- **Limit results**: "Show top 10 epics by story count"

## Related Skills

- [Jira](../jira/) - Create and manage individual tickets
- [Roadmap](../roadmap/) - Generate ICE-scored roadmaps
- [PRD](../prd/) - Write product requirements

---

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-03-02 | Claude | Initial skill creation |
