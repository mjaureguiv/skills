# Solution Refinement Interviews

Validate usability, trust, and real-world value before GA release.

## When to Use

- You have a high-fidelity prototype or working beta
- You need to validate usability and adoption likelihood
- Leadership wants to know: "Will users adopt this?"
- You're identifying launch blockers vs. nice-to-haves
- Preparing for GA release

## What This Does

Helps you:
- Generate interview guides for usability testing
- Create realistic task scenarios for testing
- Identify and categorize issues (blocker vs. enhancement)
- Assess adoption likelihood and trust (especially for AI)

## How to Use

**Generate a guide:**
```
/interview-refinement

Feature: [Feature name]
Test tasks:
1. [Task 1]
2. [Task 2]
3. [Task 3]

Help me create a refinement guide.
```

**Categorize issues:**
```
/interview-refinement

Help me categorize these findings as blockers vs nice-to-haves:
- [Finding 1]
- [Finding 2]
```

## Key Principles

### DO
- Observe behavior, don't just ask
- Test with realistic tasks and real data
- Watch for pauses, confusion, workarounds
- Quantify adoption likelihood (1-10 scale)
- Categorize issues by severity

### DON'T
- Over-guide users step-by-step
- Ask "Does this fit your workflow?" (they'll say yes)
- Treat all issues as equal priority
- Skip trust validation for AI features

## Sample Questions

| Type | Question |
|------|----------|
| **Task** | "Try to complete [task] using this tool." |
| **Reaction** | "What did you expect to happen there?" |
| **Value** | "What's the most valuable part for you?" |
| **Trust** | "Is this good enough to use without verifying?" |
| **Blocker** | "Is there anything that would stop you from using this?" |
| **Stickiness** | "If we removed this tomorrow, what would you miss?" |

## Issue Categorization

| Category | Definition | Action |
|----------|------------|--------|
| **Launch Blocker** | Prevents core task completion | Must fix |
| **High Priority** | Significant friction | Fix if time |
| **Nice-to-Have** | Users work around it | Post-launch |

## Expected Output

After 8 usability test sessions:
- Launch blocker list with fixes needed
- Adoption likelihood scores with quotes
- Trust assessment (critical for AI)
- Post-launch enhancement backlog
- Go/no-go recommendation for GA

After GA, move to [Post-Launch](../post-launch/) interviews.
