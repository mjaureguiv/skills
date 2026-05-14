# Incremental Update Template

Use this template for documenting changes to existing functionality.

---

## Template Structure

```markdown
# {Feature Name}: {Brief Change Description}

{1 sentence explaining what changed and why it matters.}

## What Changed

{Description of the change in user terms. Be specific about the before and after states.}

**Previously:** {Old behavior - describe what users experienced before}

**Now:** {New behavior - describe what users experience after the change}

## How the Updated {Feature} Works

{If the change affects how users interact with the feature, explain the new workflow or behavior.}

{Include specific details:}
- {New capability or behavior 1}
- {New capability or behavior 2}
- {What stays the same}

### Example

{Concrete example showing the change in practice:}

Example: {specific scenario with real values}

{Explanation of what the example demonstrates.}

## Why This Change Was Made

{Brief explanation of the user benefit or problem solved. Focus on what users gain, not internal reasons.}

## Impact on Your Workflow

{Explain if any user action is required.}

**No action required:** This change is automatic and applies to all users.

OR

**Action required:** {Describe what users need to do}
1. {Step 1}
2. {Step 2}

## Related Documentation

- [{Original Feature Documentation}]({link})
- [{Related Configuration Guide}]({link})
```

---

## Template Guidelines

### Title
- Include the feature name for context
- Add a brief change descriptor
- Good: "Process Filtering: Multi-Select Support"
- Bad: "Update to Filtering"

### What Changed
- Be explicit about before/after states
- Use the **Previously:** / **Now:** format for clarity
- Avoid vague descriptions

### How It Works (Updated)
- Only include if the change affects user interaction
- Focus on what's different
- Mention what stays the same to reduce confusion

### Why This Change Was Made
- Keep it brief (1-2 sentences)
- Focus on user benefit
- Avoid internal justifications

### Impact on Workflow
- Be explicit: action required or not
- If action required, provide numbered steps
- Link to guides for complex actions

### Related Documentation
- Always link to the original feature documentation
- Help users understand the full context
