---
name: epic-breakdown
description: "Find all active epics in a Jira project and list their child stories. Use when users need a hierarchical view of epics and their work items for planning, status reviews, or backlog overview."
version: 1.0.0
allowed-tools:
  - mcp__sap-jira__search_issues
  - mcp__sap-jira__get_issue
  - mcp__sap-jira__jql_examples
  - AskUserQuestion
---

# Epic Breakdown Skill

> 🧪 **Experimental MCP**: This skill uses SAP Jira MCP which is NOT listed in the SAP Hyperspace MCP Registry. Do not use with customer data or PII.

Generate a hierarchical view of active epics and their child stories from Jira.

## What This Skill Does

Given a Jira project key, this skill:
1. Finds all active (non-closed) epics in the project
2. For each epic, retrieves all linked child issues (stories, tasks, bugs, etc.)
3. Presents a structured breakdown showing the epic hierarchy

**In simple terms**: Get a bird's-eye view of your epics and what's underneath them.

---

## When to Use This

- Sprint planning - see what work exists under each epic
- Status reviews - understand progress across epics
- Backlog grooming - identify epics with too many/few stories
- Stakeholder updates - show epic-level progress

---

## Execution Steps

### Step 1: Get Project Key

If the user hasn't provided a project key, ask:
- "Which Jira project would you like to analyze? (e.g., SIGDMN, MOB)"

### Step 2: Find Active Epics

Search for epics that are NOT Done or Closed:

```
Use search_issues with:
- projectKey: [user's project]
- additionalJql: "type = Epic AND status NOT IN (Done, Closed)"
```

### Step 3: Get Epic Details

For each epic found, use `get_issue` to retrieve:
- Epic key and summary (name)
- Status
- Epic Name field (customfield_15141)

### Step 4: Find Children for Each Epic

For each epic, search for its children:

```
Use search_issues with:
- projectKey: [user's project]
- additionalJql: "\"Epic Link\" = [EPIC-KEY]"
```

### Step 5: Get Child Details

For each child issue, retrieve:
- Issue key and summary
- Type (Story, Task, Bug, etc.)
- Status
- Assignee

### Step 6: Present the Breakdown

Format the output as a hierarchical view:

```markdown
## Epic Breakdown for [PROJECT]

### [EPIC-KEY]: [Epic Name]
**Status:** [status] | **Children:** [count]

| Key | Type | Summary | Status | Assignee |
|-----|------|---------|--------|----------|
| PROJ-123 | Story | User can login | In Progress | John Doe |
| PROJ-124 | Task | Setup auth service | Done | Jane Smith |

---

### [NEXT-EPIC-KEY]: [Epic Name]
...
```

---

## Output Format Options

### Default: Markdown Table
Best for quick review in chat.

### Alternative: Summary Only
If user asks for "summary" or "overview":
```markdown
## Epic Summary for [PROJECT]

| Epic | Status | Stories | Done | In Progress | To Do |
|------|--------|---------|------|-------------|-------|
| SIGDMN-100: Auth System | In Progress | 5 | 2 | 2 | 1 |
```

---

## Handling Large Projects

If a project has many epics (>20):
1. Ask user if they want all epics or a filtered subset
2. Offer filtering options:
   - By status (e.g., only "In Progress" epics)
   - By component
   - By sprint
   - Top N by story count

---

## JQL Reference

**Find active epics:**
```
project = [KEY] AND type = Epic AND status NOT IN (Done, Closed)
```

**Find children of an epic:**
```
project = [KEY] AND "Epic Link" = [EPIC-KEY]
```

**Find epics in a specific status:**
```
project = [KEY] AND type = Epic AND status = "In Progress"
```

---

## Error Handling

- **No epics found**: Report "No active epics found in [PROJECT]. All epics may be Done/Closed."
- **Epic has no children**: Show epic with "(No linked stories)"
- **Auth required**: Trigger SAP authentication flow and retry

---

## Example Output

```markdown
## Epic Breakdown for SIGDMN

### SIGDMN-491: DMN XML Import
**Status:** In Progress | **Children:** 4

| Key | Type | Summary | Status | Assignee |
|-----|------|---------|--------|----------|
| SIGDMN-537 | Story | Explore error responses | In Progress | I744741 |
| SIGDMN-538 | Story | Import validation | To Do | Unassigned |
| SIGDMN-539 | Task | Error code documentation | Done | I744741 |
| SIGDMN-540 | Bug | Fix timeout handling | To Do | Unassigned |

---

### SIGDMN-453: Enumeration Expressions
**Status:** Backlog | **Children:** 0
(No linked stories)
```

---

## Works Well With

- **roadmap**: Use epic breakdown to inform roadmap planning
- **powerpoint**: Turn epic status into presentation slides
- **jira**: Create missing stories under epics

---

**Category**: Jira & Planning
