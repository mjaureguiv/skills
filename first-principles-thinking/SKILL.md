---
name: first-principles-thinking
description: "Apply first principles thinking to break down complex problems. Use when user wants to analyze assumptions, question fundamentals, or solve problems from ground up."
user-invokable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
---

# First Principles Thinking Coach

Guide users through first principles reasoning to break down complex problems and build solutions from fundamental truths.

---

## What is First Principles Thinking?

First principles thinking is a problem-solving approach that involves:
1. **Breaking down** complex problems into their most basic, fundamental elements
2. **Questioning** every assumption until you reach undeniable truths
3. **Rebuilding** solutions from the ground up based on those truths

Popularized by Aristotle and used by innovators like Elon Musk, it contrasts with reasoning by analogy (copying what others do).

---

## When to Use This Skill

- User says "let's think from first principles"
- User is stuck on a problem and conventional solutions aren't working
- User wants to innovate or find non-obvious solutions
- User needs to challenge industry assumptions
- User asks "why do we do it this way?"

---

## The Process

### Step 1: Define the Problem Clearly

Ask the user to state the problem they want to solve.

```
What specific problem or challenge do you want to analyze?
Be as concrete as possible.
```

### Step 2: Identify Current Assumptions

List all the assumptions embedded in the current approach:

```
Let's uncover the assumptions. For [problem]:

1. What do most people believe about this?
2. What constraints are you assuming exist?
3. What "rules" are you following?
4. What's "always been done this way"?
```

### Step 3: Question Each Assumption

For each assumption, apply the "Five Whys" and ask:

```
Assumption: [X]

- Is this actually true, or just commonly accepted?
- What evidence supports this?
- What would happen if this weren't true?
- Who benefits from this assumption being accepted?
- Is this a law of physics, or a convention?
```

**Categories of assumptions:**
- **Physical constraints** (laws of nature) — Cannot be broken
- **Resource constraints** (time, money, people) — Can often be worked around
- **Social/cultural constraints** (norms, conventions) — Often arbitrary
- **Self-imposed constraints** (beliefs, fears) — Usually breakable

### Step 4: Identify Fundamental Truths

After questioning, identify what remains as undeniably true:

```
The fundamental truths are:
1. [Physics/math/logic that cannot be violated]
2. [Verified facts with strong evidence]
3. [Core user needs that are truly essential]
```

### Step 5: Rebuild from the Ground Up

With only fundamental truths as constraints:

```
If we could start from scratch with only these truths:

1. What's the simplest possible solution?
2. What would an alien with no knowledge of our conventions do?
3. What becomes possible that wasn't before?
4. What's the most direct path from problem to solution?
```

---

## Example: The Tesla Battery Problem

**Problem:** Electric car batteries are too expensive.

**Conventional thinking:** "Batteries cost $600/kWh, that's just what they cost."

**First principles analysis:**

1. **What are batteries made of?** Cobalt, nickel, aluminum, carbon, polymers, steel
2. **What do those materials cost on the commodity market?** ~$80/kWh
3. **Why the gap?** Manufacturing processes, supply chain markups, small scale

**Solution from first principles:** Buy raw materials, build own battery factory at scale → Tesla Gigafactory → batteries now ~$100/kWh

---

## Facilitation Questions

Use these to guide the user:

### Opening
- "What problem would you like to break down to its fundamentals?"
- "What assumption about this problem would be most powerful to challenge?"

### Digging Deeper
- "Why is that true? Can you prove it?"
- "Who says it has to be this way?"
- "What if the opposite were true?"
- "Is this a law of physics or a convention?"

### Rebuilding
- "If you had unlimited resources, what would you build?"
- "What would a solution look like if you started today with no legacy?"
- "What's the minimum viable version of this?"

### Reality Check
- "Which of these fundamental truths is most constraining?"
- "What's the first small experiment you could run?"
- "What would need to be true for this new approach to work?"

---

## Common Pitfalls to Avoid

1. **Stopping too early** — Keep asking "why" until you hit physics/math
2. **Confusing conventions with constraints** — Most "rules" are conventions
3. **Analysis paralysis** — At some point, rebuild and test
4. **Ignoring practical constraints** — First principles gives direction, not complete plans
5. **Thinking alone** — Challenge your own blind spots with others

---

## Output Format

When completing a first principles analysis, summarize:

```markdown
## First Principles Analysis: [Problem]

### The Problem
[Clear statement]

### Assumptions Challenged
| Assumption | Type | Verdict |
|------------|------|---------|
| [assumption] | Convention/Constraint | Breakable/Fixed |

### Fundamental Truths
1. [Truth that cannot be violated]
2. [Truth that cannot be violated]

### New Possibilities
1. [Solution that becomes possible]
2. [Solution that becomes possible]

### Recommended Next Step
[Smallest experiment to test the new approach]
```

---

## Related Frameworks

- **Five Whys** — Root cause analysis
- **Socratic Method** — Questioning to expose assumptions
- **Zero-based thinking** — "If I were starting over..."
- **Inversion** — "What would guarantee failure?"
