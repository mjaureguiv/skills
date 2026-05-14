# Solution Validation Interviews

Test early concepts and prototypes to see if solutions resonate with users.

## When to Use

- You have a validated problem
- You have 2-4 rough solution concepts (sketches, wireframes, narratives)
- You want to test desirability BEFORE building
- You need to validate mental model fit
- You're choosing between solution directions

## What This Does

Helps you:
- Generate interview guides for concept testing
- Frame solution concepts neutrally for testing
- Identify mental model matches and mismatches
- Evaluate workflow fit of different approaches

## How to Use

**Generate a guide:**
```
/interview-solution

Problem: [Validated problem]
Concepts:
1. [Concept A description]
2. [Concept B description]
3. [Concept C description]

Help me create a validation guide.
```

**Mental model test:**
```
/interview-solution

How do I test if users understand what my solution is trying to solve?
```

## Key Principles

### DO
- Keep prototypes rough (low-fidelity)
- Ask "What problem does this solve?" (mental model test)
- Test multiple concepts
- Let them react before explaining

### DON'T
- Show polished designs (they'll be too polite)
- Ask "Would you use this?"
- Explain how it works before getting reactions
- Defend the concept when they're confused

## Sample Questions

| Type | Question |
|------|----------|
| **Reaction** | "What's your initial reaction?" |
| **Mental Model** | "What problem do you think this is solving?" |
| **Fit** | "How would this fit your current workflow?" |
| **Barriers** | "What would make you hesitant?" |
| **Gaps** | "What's missing that you'd expect?" |

## The Mental Model Test

Show concept → Ask "What problem do you think this is solving?"
- If they get it right → mental model fit ✓
- If they get it wrong → critical insight! Don't explain, explore why.

## Expected Output

After 8-10 solution validation interviews:
- Winning solution direction with evidence
- Known mental model issues to address
- Workflow fit requirements
- Risk and trust concerns identified

Take the winning concept to [Solution Refinement](../solution-refinement/) for high-fi testing.
