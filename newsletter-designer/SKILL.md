---
name: newsletter-designer
description: Generate structured marketing content for internal newsletters using a Problem-Solution-Outcome framework
version: 1.0.0
---

# Newsletter Designer Skill

## Purpose

Generate catchy, structured marketing content for internal newsletters. Content follows a strict **Problem → Solution → Outcome** framework to highlight product improvements and team achievements.

---

## Output Format

Each newsletter entry MUST include these 7 fields in a table row:

| Field | Description | Guidelines |
|-------|-------------|------------|
| **Month** | Publication month | e.g., "March", "Q1 2026" |
| **Prio** | Priority level | High, Medium, Low |
| **Team / PM** | Responsible team or PM | Team name (e.g., "Team Dodo") |
| **Catchy Headline** | Attention-grabbing title | **MAX 5 words**, action-oriented |
| **THE PROBLEM (The Trigger)** | Why this matters | Pain point, metric, or user frustration |
| **THE SOLUTION (The Micro-Delivery)** | What was built/shipped | Concrete feature or fix |
| **THE OUTCOME (The Value)** | Measurable impact | Metrics, %, $ impact, or qualitative win |

---

## Writing Guidelines

### Catchy Headline (Max 5 Words)
- Start with action verb or impactful noun
- Be specific, not generic
- Examples:
  - ✅ "Stopping Checkout Drops"
  - ✅ "Faster Loads, Happier Users"
  - ✅ "Migration Without Downtime"
  - ❌ "We Improved the System" (too vague)
  - ❌ "New Feature Release Update" (boring)

### THE PROBLEM (The Trigger)
- Lead with a specific pain point or metric
- Make it relatable and urgent
- Include numbers when possible
- Example: "15% drop-off at payment because users couldn't see shipping costs."

### THE SOLUTION (The Micro-Delivery)
- Focus on the concrete deliverable
- Keep it technical but accessible
- One sentence, action-oriented
- Example: "Dynamic shipping calc before login."

### THE OUTCOME (The Value)
- Always include measurable impact
- Use metrics: %, $, time saved, users affected
- Make the business value clear
- Example: "Conversion +4.5% ($12K impact)."

---

## Tone & Style

- **Confident** but not boastful
- **Specific** with numbers and metrics
- **Action-oriented** language
- **Internal audience** - can use technical terms
- **Celebratory** - highlight team achievements

---

## Example Entry

| Month | Prio | Team / PM | Catchy Headline | THE PROBLEM | THE SOLUTION | THE OUTCOME |
|-------|------|-----------|-----------------|-------------|--------------|-------------|
| Example | - | Team Alpha | Stopping Checkout Drops | 15% drop-off at payment because users couldn't see shipping costs. | Dynamic shipping calc before login. | Conversion +4.5% ($12K impact). |

---

## Process

1. **Gather input** from user about the feature/achievement
2. **Identify the pain point** - what problem was solved?
3. **Clarify the delivery** - what exactly shipped?
4. **Quantify the outcome** - what's the measurable impact?
5. **Craft the headline** - make it catchy in 5 words or less
6. **Output as table row** - formatted for easy copy-paste

---

## When User Provides Limited Info

If the user only provides a topic or announcement:
1. Ask clarifying questions about problem/solution/outcome
2. OR propose reasonable content based on context
3. Always confirm before finalizing

---

## Output Template

```markdown
| Month | Prio | Team / PM | Catchy Headline (Max 5 words) | THE PROBLEM (The Trigger) | THE SOLUTION (The Micro-Delivery) | THE OUTCOME (The Value) |
|-------|------|-----------|-------------------------------|---------------------------|-----------------------------------|-------------------------|
| [Month] | [Priority] | [Team] | [Headline] | [Problem statement] | [Solution delivered] | [Measurable outcome] |
```
