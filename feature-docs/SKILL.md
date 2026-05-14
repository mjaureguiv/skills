---
name: feature-docs
description: "Generate user-facing documentation for product features. Use when users need to document new features, enhancements, or changes. Integrates with Jira epics. Outputs clean markdown ready for help documentation."
version: 1.0.0
user-invokable: true
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

# Feature Documentation Skill

Turn feature specs and Jira tickets into clear, user-friendly documentation.

## What This Skill Does

You give it information about a feature (a Jira ticket, some notes, or just a description), and it creates professional documentation that:

- Explains what the feature does in plain language
- Focuses on user benefits, not technical details
- Includes real examples that make sense
- Is ready to publish without heavy editing

**In simple terms**: Instead of staring at a blank page trying to write docs, just tell me about the feature and get polished documentation in minutes.

---

## When to Use This

- You need to write help docs for a new feature
- You're documenting a change to existing functionality
- You have a Jira epic that needs user documentation
- You need a migration guide for a breaking change

**Not for**: Technical specs, API docs, or marketing announcements.

---

## Three Types of Documentation

### 1. Feature Documentation
For new features. Explains what it does, how to use it, and why it matters.

### 2. Update Documentation
For changes to existing features. Shows what changed and whether users need to do anything.

### 3. Migration Guide
For breaking changes. Walks users through what to do step-by-step.

---

## What Happens Behind the Scenes

### Step 1: Understanding the Feature

I'll ask you (or pull from Jira if you give me a ticket number):
- What does this feature do?
- Who's it for? (admins, end users, developers)
- What problem does it solve?
- Any setup required? Any limitations?

### Step 2: Picking the Right Template

Based on what you need, I choose from:
- Feature docs template (for new stuff)
- Update template (for changes)
- Migration guide template (for breaking changes)

### Step 3: Writing the Docs

I structure everything so it's easy to read:
1. Clear title saying what users can do
2. Short overview (1-2 sentences)
3. How it works (step-by-step if needed)
4. Why it matters (user benefits)
5. A real example
6. Links to related docs

### Step 4: Review and Save

I check everything is clear, then save it with a sensible filename like `process-filtering-documentation.md`.

---

## Writing Style

The documentation I create follows these principles:

**Language:**
- Plain English (no jargon)
- User-focused (what can they do, not how it's built)
- Concrete examples (not abstract explanations)
- No marketing speak ("exciting", "powerful", etc.)

**Structure:**
- Short paragraphs (2-3 sentences)
- Lots of headings (easy to scan)
- Bullet points for lists
- Every feature gets an example

---

## Jira Integration

If you give me a Jira ticket number (like SIG-1234), I can pull:
- The feature title
- Description and details
- Acceptance criteria

This saves you from having to type everything out.

---

## Example of Good Documentation

Here's what the output looks like:

```markdown
# Filtering Processes by Status

Users can now filter the process list by lifecycle status (Active, Draft, Archived) to quickly find relevant processes.

## How Filtering Works

From the process list view:
1. Click the "Filter" button in the toolbar
2. Select one or more status values
3. The list updates to show only matching processes

Filter selections persist across sessions.

## Why This Matters

Large organizations may have hundreds of processes. Filtering lets you focus on what's relevant without scrolling through the entire list.
```

Notice: Clear title, short overview, step-by-step instructions, and user benefit.

---

## Works Well With Other Skills

- **powerpoint**: Turn feature docs into presentation slides
- **transcript-to-notes**: Extract feature details from meeting discussions

## What You Can Give Me

- Jira ticket numbers
- Rough notes or bullet points
- Product requirements
- Existing docs that need updating

---

## How You Know It's Working

- Docs are ready to publish without major edits
- Users can understand features without a technical background
- Consistent structure across all your documentation
- Examples are relatable and concrete

---

## Support

Questions or issues? Reach out in #claude-code-help

---

**Original Author**: Aviral Vaid (LeanIX Product Management)
**Category**: Workflow
**Integrated from**: [LeanIX PM Marketplace](https://github.tools.sap/LeanIX/LeanIX-PM-Marketplace)
