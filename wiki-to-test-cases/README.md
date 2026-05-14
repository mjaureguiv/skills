# wiki-to-test-cases

Generate functional test cases from SAP Wiki feature documentation for PM release validation.

## What This Does

Transforms feature implementation documents into actionable test cases:
- **Fetches** wiki content via SAP Wiki MCP connection
- **Analyzes** requirements, acceptance criteria, and specifications
- **Generates** structured test cases with priorities and categories

Helps PMs validate features before release decisions without writing test cases from scratch.

## Why This Exists

Product Managers need to verify:
- All documented functionality works as expected
- Edge cases are considered
- Nothing was missed between spec and implementation

This skill automates test case creation from existing documentation.

## Usage

### Basic: From Wiki URL

```
/wiki-to-test-cases https://wiki.one.int.sap/wiki/pages/viewpage.action?pageId=123456
```

### With Context

```
/wiki-to-test-cases
URL: https://wiki.one.int.sap/wiki/pages/viewpage.action?pageId=123456
Focus: Permission-related scenarios
Audience: Admin users only
```

### Search First

```
/wiki-to-test-cases
Search for: Process Filtering feature spec
Space: SIGNAVIO
```

## Output Format

### Summary with Checklist
```markdown
# Functional Test Cases: [Feature Name]

**Source**: [Wiki URL]
**Total Test Cases**: 12

## Quick Checklist
- [ ] TC-001: Core workflow validation
- [ ] TC-002: Error handling
...
```

### Detailed Test Cases
```markdown
## Test Case: [TC-001] Filter by Status

**Priority**: High
**Category**: Core Functionality

### Preconditions
- User logged in with appropriate role

### Test Steps
1. Navigate to feature
2. Perform action
3. Verify result

### Expected Results
- Specific observable outcome
```

## Test Case Categories

| Category | Priority | Examples |
|----------|----------|----------|
| Core Functionality | High | Main workflows, critical features |
| Integration | High | Connected features, dependencies |
| Permissions | High | Role-based access, security |
| User Interface | Medium | UI elements, labels, layout |
| Edge Cases | Medium | Empty states, boundaries |
| Error Handling | Medium | Invalid inputs, error messages |

## Requirements

- **SAP Wiki MCP**: Must be configured for wiki access
- **Authentication**: Valid SAP SSO session

## Authentication

If you get authentication errors:
1. The skill will prompt for re-authentication
2. Follow the SAP SSO flow
3. Retry the wiki URL

## Example

**Input**: Wiki page documenting "Process Status Filtering" feature

**Output**:
```markdown
# Functional Test Cases: Process Status Filtering

**Source**: https://wiki.one.int.sap/wiki/pages/viewpage.action?pageId=123456
**Generated**: 2024-01-15
**Total Test Cases**: 12

## Quick Checklist
- [ ] TC-001: Filter by single status (High)
- [ ] TC-002: Filter by multiple statuses (High)
- [ ] TC-003: Clear filters (Medium)
- [ ] TC-004: Filter persistence (Medium)
- [ ] TC-005: Empty results state (Medium)
- [ ] TC-006: Role-based filter options (High)
...
```

## Related Skills

- `feature-docs` - Create feature documentation (input for this skill)
- `jira` - Link test cases to tickets
- `powerpoint` - Release readiness presentations

## Output Location

Test cases are saved to: `skills/wiki-to-test-cases/temp/[feature-name]-test-cases.md`

## Support

Questions or issues? Reach out in #claude-code-help

---

**Original Author**: Signavio PM Team
**Category**: Quality Assurance
