---
name: getting-started
description: "Explain everything the SAP Signavio PM Agent can do and how to get started. Use when user is new, asks 'what can you do', 'help me get started', 'what is this repo', or needs orientation."
version: 1.0.0
user-invokable: true
allowed-tools:
  - Read
  - Glob
  - AskUserQuestion
---

# Getting Started with SAP Signavio PM Agent

Welcome! This skill helps new users understand what this repository can do and how to make the most of it.

## What This Repository Is

The **SAP Signavio PM Agent** is your AI-powered Product Manager assistant. It's a collection of skills and workflows that automate the tedious parts of PM work so you can focus on strategy and decision-making.

**Think of it as**: A superpowered assistant that can write presentations, create Jira tickets, analyze customer feedback, coach you on PM frameworks, and much more - all from within VS Code.

---

## What Makes This Powerful

### 1. Instant Document Creation

Instead of spending hours in PowerPoint or Word:
- **PowerPoint**: "Create a 5-slide deck about our Q1 roadmap" → Get a SAP-branded presentation
- **Word docs**: Generate professional documents
- **Excel files**: Create spreadsheets and dashboards
- **PRDs**: Write product requirements documents

### 2. Jira Integration

Stop copy-pasting between tools:
- Create Jira tickets directly from conversations
- Convert meeting notes into structured epics and stories
- Extract requirements and turn them into backlog items

### 3. Meeting Superpowers

Never lose track of decisions:
- **Transcript to notes**: Paste a Teams transcript, get structured meeting notes
- **Meeting facilitation**: Get agenda templates and facilitation techniques
- **Decision logging**: Automatically document decisions from meetings

### 4. Content Creation

Write faster and on-brand:
- **What's New articles**: Release announcements
- **LinkedIn posts**: Professional social content
- **Email replies**: Draft responses in your voice
- **Slack messages**: Team announcements

### 5. PM Coaching & Strategy

Get expert advice on demand:
- **PM Advisor**: Strategic product management guidance
- **Marty Cagan Coach**: SVPG frameworks - empowered teams, product discovery, transformation
- **Systemic Coach**: Systems thinking for complex problems
- **Goal Coach**: OKR and performance coaching
- **CDH Framework**: Continuous Discovery Habits guidance
- **Working Backwards**: Amazon-style PR/FAQ method

### 6. Customer Insights

Understand your users better:
- **ProductBoard analysis**: Analyze customer feedback
- **Insight dashboards**: Create Excel dashboards from feedback data
- **Requirements extraction**: Turn raw notes into structured requirements

### 7. Product Knowledge

Deep expertise on SAP Signavio:
- **Product Expert**: SPM product knowledge
- **User Guide assistance**: Documentation help
- **Codebase analysis**: Understand the technical implementation
- **BPMN coaching**: Process modeling standards

### 8. Claude Code Power Features

Become a power user:
- **Claude Code Mastery**: Learn shortcuts, hooks, subagents, MCP servers
- Hidden features most users don't know
- Automation and productivity tips

---

## How to Get Started

### Step 1: Setup (5 minutes)

**For Claude Code (Recommended)**:
Follow the official guide: https://pages.github.tools.sap/hAIperspace/hai-docs/llm-proxy/recipes/claude/

**For GitHub Copilot**:
See [setup/README.md](../../setup/README.md)

### Step 2: Try Your First Skill

Open a chat and try one of these:

```
Create a 3-slide presentation about our new feature
```

```
Help me write a PRD for a user authentication feature
```

```
Turn these meeting notes into action items:
[paste notes]
```

### Step 3: Explore More Skills

See what's available:
- **Full skill list**: [README.md](../../README.md)
- **End-to-end workflows**: [scenarios/](../../scenarios/)

---

## Quick Reference: What Can I Ask For?

| What You Want | What to Say |
|---------------|-------------|
| SAP presentation | "Create a presentation about [topic]" |
| Jira tickets | "Create a Jira ticket for [feature]" |
| Meeting notes | "Turn this transcript into notes: [paste]" |
| PRD | "Write a PRD for [feature]" |
| PM advice | "Help me prioritize these features" |
| Cagan-style coaching | "How do I build an empowered team?" |
| Claude Code tips | "Teach me Claude Code power user features" |
| LinkedIn post | "Write a LinkedIn post about [topic]" |
| Requirements | "Extract requirements from these notes" |
| Roadmap | "Create an ICE-scored roadmap" |
| Email reply | "Draft a reply to this email: [paste]" |
| Feedback analysis | "Analyze these customer insights" |

---

## Repository Structure (Where Things Are)

```
Signavio_PM_Agent/
├── skills/           # Individual capabilities (this is where the magic is)
│   ├── powerpoint/   # SAP-branded presentations
│   ├── jira/         # Ticket creation
│   ├── prd/          # Product requirements
│   ├── transcripts/  # Meeting notes
│   └── ...           # 30+ more skills
├── scenarios/        # End-to-end workflows
├── context/          # Customize for your team
│   ├── team/config.md           # Your Jira keys, conventions
│   └── product-context.md       # Your product info
├── templates/        # PowerPoint templates, etc.
├── outputs/          # Where generated files go
└── setup/            # Getting started guides
```

---

## Tips for Success

### Be Specific
Instead of: "Make a presentation"
Say: "Create a 5-slide customer-facing presentation about our new AI features, focused on business value"

### Reference Files
Use `@filename` to include context:
"Turn @notes/meeting-2026-02-27.md into a PRD"

### Ask for Revisions
Don't like something? Just say:
"Make the bullets shorter"
"Add more detail to slide 3"
"Change the tone to be more executive-friendly"

### Customize Your Setup
Edit these files to make outputs match your team:
- `context/team/config.md` - Your Jira projects, conventions
- `context/team/pm-voice-samples.md` - Your writing style

---

## Getting Help

- **Slack**: #claude-code-help
- **Champions**: See [CHAMPIONS.md](../../CHAMPIONS.md) for skill-specific contacts
- **Issues**: [GitHub Issues](https://github.tools.sap/signavio-pm-agent/Signavio_PM_Agent/issues)

---

## Keep This Skill Updated

**IMPORTANT FOR MAINTAINERS**: When you add or update skills in this repository, update this getting-started skill to reflect the changes. New users rely on this to understand what's possible.

Checklist when updating the repo:
- [ ] Update the "What Makes This Powerful" section if adding major capabilities
- [ ] Update "Quick Reference" table with new skills
- [ ] Update "Repository Structure" if folder structure changes
- [ ] Keep examples current and working

---

## Summary

The SAP Signavio PM Agent saves you hours every week by automating:
- **Document creation** (presentations, PRDs, tickets)
- **Meeting follow-up** (notes, action items, decisions)
- **Content writing** (announcements, posts, emails)
- **PM coaching** (frameworks, strategy, prioritization)

**Start simple**: Try creating a presentation or turning meeting notes into action items. Once you see the power, explore more skills!

---

**Questions?** Just ask: "What else can you help me with?"
