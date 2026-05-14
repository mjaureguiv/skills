---
name: wiki-to-test-cases
description: "Generate functional test cases from SAP Wiki feature documentation. Use when PMs need to create acceptance test cases before release decisions. Connects to SAP Wiki via MCP to fetch and analyze feature specs."
version: 1.0.0
user-invokable: true
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
  - mcp__sap-wiki__wiki_content
  - mcp__sap-wiki__general_search
  - mcp__sap-wiki__cql_search
---

# Wiki to Test Cases Skill

> 🧪 **Experimental MCP**: This skill uses SAP Wiki MCP which is NOT listed in the SAP Hyperspace MCP Registry. Do not use with customer data or PII.

Transform SAP Wiki feature documentation into comprehensive functional test cases for Product Managers.

## What This Skill Does

Given a SAP Wiki URL containing feature implementation documentation, this skill:
1. Fetches the document content via SAP Wiki MCP
2. Analyzes the feature specification, requirements, and acceptance criteria
3. Generates structured functional test cases ready for PM validation

**In simple terms**: Paste a wiki URL → Get a complete test case checklist for your release decision.

---

## When to Use This

- Before a release decision meeting
- When you need to validate feature completeness
- Creating acceptance test cases from feature specs
- Building a QA checklist for PM sign-off
- Ensuring all documented behavior is testable

**Not for**: Unit tests, integration tests, or automated test scripts (those are for developers).

---

## How It Works

### Step 1: Fetch the Wiki Document

When the user provides a SAP Wiki URL, use the `mcp__sap-wiki__wiki_content` tool:

```
URL format: https://wiki.one.int.sap/wiki/pages/viewpage.action?pageId=XXXXX
```

Extract:
- Feature title and overview
- Functional requirements
- User stories or acceptance criteria
- UI/UX specifications
- Edge cases mentioned
- Dependencies and prerequisites

### Step 2: Analyze for Test Coverage

Identify testable scenarios from:
- **Happy paths**: Main user workflows
- **Edge cases**: Boundary conditions, empty states
- **Error scenarios**: Invalid inputs, permission issues
- **Integration points**: How it connects to other features
- **Configuration options**: Different settings/modes

### Step 3: Generate Test Cases

Create test cases using this structure:

```markdown
## Test Case: [TC-XXX] [Descriptive Name]

**Priority**: High | Medium | Low
**Category**: Functional | UI | Integration | Edge Case

### Preconditions
- [Required setup or state]

### Test Steps
1. [Action step]
2. [Action step]
3. [Action step]

### Expected Results
- [Observable outcome]
- [System behavior]

### Test Data
- [Sample inputs if needed]
```

---

## Test Case Categories

Generate test cases across these categories:

### 1. Core Functionality (High Priority)
- Does the main feature work as documented?
- Can users complete the primary workflow?

### 2. User Interface (Medium Priority)
- Are all UI elements present and functional?
- Is the layout correct?
- Are labels and messages accurate?

### 3. Input Validation (Medium Priority)
- How does it handle invalid inputs?
- Are error messages clear?

### 4. Edge Cases (Medium Priority)
- Empty states
- Maximum/minimum values
- Concurrent users
- Large data sets

### 5. Integration (High Priority)
- Does it work with connected features?
- Are dependencies handled correctly?

### 6. Permissions & Access (High Priority)
- Role-based access works correctly?
- Unauthorized access prevented?

---

## Output Format

Save test cases to: `skills/wiki-to-test-cases/temp/[feature-name]-test-cases.md`

### Summary Section
```markdown
# Functional Test Cases: [Feature Name]

**Source**: [Wiki URL]
**Generated**: [Date]
**Total Test Cases**: [Count]

## Coverage Summary
| Category | Count | Priority |
|----------|-------|----------|
| Core Functionality | X | High |
| User Interface | X | Medium |
| Edge Cases | X | Medium |
| Integration | X | High |

## Quick Checklist
- [ ] TC-001: [Name]
- [ ] TC-002: [Name]
...
```

### Detailed Test Cases
Follow with full test case details organized by category.

---

## Priority Guidelines

**High Priority** (Must test before release):
- Core feature functionality
- Critical user workflows
- Security/permissions
- Data integrity

**Medium Priority** (Should test):
- UI polish
- Edge cases
- Error handling
- Performance considerations

**Low Priority** (Nice to test):
- Cosmetic issues
- Minor convenience features
- Rarely-used options

---

## Example Output

```markdown
# Functional Test Cases: Process Status Filtering

**Source**: https://wiki.one.int.sap/wiki/pages/viewpage.action?pageId=123456
**Generated**: 2024-01-15
**Total Test Cases**: 12

## Quick Checklist
- [ ] TC-001: Filter by single status
- [ ] TC-002: Filter by multiple statuses
- [ ] TC-003: Clear all filters
- [ ] TC-004: Filter persistence across sessions
...

---

## Test Case: [TC-001] Filter by Single Status

**Priority**: High
**Category**: Core Functionality

### Preconditions
- User is logged in with Viewer role or higher
- Process list contains processes in different statuses

### Test Steps
1. Navigate to Process List view
2. Click the "Filter" button in the toolbar
3. Select "Active" from the status dropdown
4. Click "Apply"

### Expected Results
- Only processes with "Active" status are displayed
- Filter indicator shows "Status: Active"
- Process count updates to reflect filtered results

### Test Data
- Use test workspace with at least 5 Active, 3 Draft, and 2 Archived processes
```

---

## Handling Missing Information

If the wiki document lacks sufficient detail:

1. **Ask the user** for clarification on:
   - Specific acceptance criteria
   - Expected behavior for edge cases
   - Role/permission requirements

2. **Flag gaps** in the output:
   ```markdown
   ⚠️ **Documentation Gap**: The wiki doesn't specify behavior
   when [scenario]. Consider adding test case after clarification.
   ```

3. **Suggest follow-up**:
   - Link to related documentation
   - Recommend stakeholder review

---

## Integration with Other Skills

Works well with:
- **feature-docs**: If you need to document a feature first
- **jira**: Link test cases to Jira tickets
- **powerpoint**: Create release readiness presentations

---

## SAP Wiki MCP Tools Reference

### Fetch Document Content
```
mcp__sap-wiki__wiki_content
- url: Full wiki page URL
- raw: false (returns clean content)
```

### Search for Related Pages
```
mcp__sap-wiki__general_search
- keyword: Search term
- limit: Max results (default 20)
```

### Advanced CQL Search
```
mcp__sap-wiki__cql_search
- cql: Confluence Query Language query
- limit: Max results
```

---

## Quality Checklist

Before delivering test cases:
- [ ] All documented requirements have corresponding test cases
- [ ] Priorities are assigned based on business impact
- [ ] Preconditions are clear and achievable
- [ ] Expected results are specific and verifiable
- [ ] Test data requirements are specified
- [ ] Edge cases are covered
- [ ] Documentation gaps are flagged

---

## Support

Questions or issues? Reach out in #claude-code-help

---

**Original Author**: Signavio PM Team
**Category**: Quality Assurance
