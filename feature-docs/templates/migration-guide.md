# Migration Guide Template

Use this template for documenting breaking changes or significant workflow updates that require user action.

---

## Template Structure

```markdown
# Migration Guide: {Feature or Change Name}

{1-2 sentence summary of what is changing and why users need to take action.}

## Overview

{Explain the change at a high level. What was the old approach? What is the new approach? Why is this change being made?}

## Who Is Affected

{Clearly state which users or use cases are impacted.}

- Users who {specific condition 1}
- Organizations that {specific condition 2}
- Workflows involving {specific feature or configuration}

**Not affected:** {Users or scenarios that don't need to change anything}

## Timeline

| Milestone | Date |
|-----------|------|
| Announcement | {date} |
| New behavior available | {date} |
| Migration deadline | {date} |
| Old behavior deprecated | {date, if applicable} |

## Before and After

| Aspect | Before | After |
|--------|--------|-------|
| {Behavior 1} | {Old approach} | {New approach} |
| {Behavior 2} | {Old approach} | {New approach} |
| {Configuration} | {Old setting} | {New setting} |

## Step-by-Step Migration

### Step 1: {First Action}

{Detailed instructions for the first step. Include specific UI paths, field names, or API endpoints.}

1. Navigate to {location}
2. Select {option}
3. Configure {setting}

### Step 2: {Second Action}

{Continue with clear, numbered steps.}

### Step 3: {Verification}

{How users can verify the migration was successful.}

To confirm your migration is complete:
- {Verification check 1}
- {Verification check 2}

## What Happens If You Don't Migrate

{Be clear about consequences without being alarmist.}

- {Consequence 1}
- {Consequence 2}

## Frequently Asked Questions

### Q: {Common question about the migration}

A: {Clear, direct answer}

### Q: {Another common question}

A: {Answer}

### Q: {Question about edge cases}

A: {Answer}

## Need Help?

{Contact information or support resources.}

- Review the [{related documentation}]({link})
- Contact {support channel} for assistance
- See [{troubleshooting guide}]({link}) for common issues
```

---

## Template Guidelines

### Title
- Start with "Migration Guide:"
- Use clear, descriptive change name
- Good: "Migration Guide: Process Versioning Model"
- Bad: "Migration Guide: Q4 Changes"

### Overview
- Set context before diving into details
- Explain the "why" briefly
- Keep to 2-3 sentences

### Who Is Affected
- Be specific about affected users
- Include "Not affected" section to reduce anxiety
- Help users self-identify quickly

### Timeline
- Always include dates
- Use a table for easy scanning
- Include migration deadline prominently

### Before and After
- Use a comparison table
- Be specific about changes
- Help users understand the delta

### Step-by-Step Migration
- Number all steps
- Include specific UI paths and field names
- Add a verification step at the end

### What Happens If You Don't Migrate
- Be factual, not threatening
- Help users prioritize
- Include specific consequences

### FAQ
- Include 3-5 common questions
- Address edge cases
- Keep answers concise

### Need Help
- Provide multiple support channels
- Link to related documentation
- Include troubleshooting resources
