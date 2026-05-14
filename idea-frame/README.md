# IdeaFrame

Transform a rough product idea into a fully structured, classified, and contextualised brief — with automatic discovery of related skills and scenarios across both PM Agent repos.

## What This Skill Does

Given a one-line or paragraph idea description, IdeaFrame produces:

| Output | Description |
|--------|-------------|
| **Core Framing** | Problem statement, user story, business outcome, technical description, analogy |
| **Auto Multi-Frame Description** | Jobs-to-be-Done, problem framing, system behaviour |
| **Tags & Taxonomy** | Classified by Persona, Capability, and Trigger (controlled vocabulary) |
| **Related & Similar Solutions** | Up to 6 matching skills/scenarios from both repos, each with similarity score, owner, problem summary, and score rationale |

Results appear **in the Claude Code chat** and are **also written to the IdeaFrame web app** at `http://localhost:3000` if it is running.

## How to Use

```
#idea-frame I want to build a GRC agent that maps control points to business process diagrams
```

Or simply describe your idea after invoking the skill:

```
#idea-frame
[paste your idea here — one line or several paragraphs]
```

## Example Output (chat)

```
## 🖼️ IdeaFrame — GRC Control Mapping Agent

### 🏷️ Tags & Taxonomy
Persona:    process · operations · legal
Capability: monitoring · automation · visualization · integration
Trigger:    event-based · manual

---

### 🎯 Core Framing

**Problem Statement**
Business process teams have no automated way to link governance control
points to steps in their BPMN diagrams...

**User Story**
As a process owner, I want a GRC agent that maps control points to my
process diagram so that I can see compliance gaps instantly...

[... all 5 fields ...]

---

### 🔀 Auto Multi-Frame Description

**Jobs-to-be-Done**  ...
**Problem Framing**  ...
**System Behaviour** ...

---

### 🔗 Related & Similar Solutions

| Score | Title | Type | Owner | Why relevant |
|-------|-------|------|-------|--------------|
| 94%   | Agentic AI for GRC | Skill | Steffen K | Near-identical scope... |
| 88%   | Governance Rule Validator | Skill | SPG Team | Step-level control verification... |
...
```

## Taxonomy Reference

### Persona
`finance` · `hr` · `process` · `operations` · `it` · `sales` · `legal` · `customer-success`

### Capability
`notification` · `approval` · `routing` · `reporting` · `monitoring` · `integration` · `visualization` · `automation` · `data-capture` · `collaboration`

### Trigger
`event-based` · `manual` · `scheduled` · `rule-based`

## Web App Integration

If the IdeaFrame web app is running at `http://localhost:3000`, results are automatically written to `idea-workspace/queue/results.json` so they appear in the browser alongside the chat output.

To start the web app:
```bash
# Backend (port 4000)
cd idea-workspace/server && node index.js &

# Frontend (port 3000)
cd idea-workspace/client && npm run dev &
```

## Related Skills

- [Requirements](../requirements/) — Extract structured requirements from the framed idea
- [PRD](../prd/) — Generate a full PRD from the idea frame output
- [Opportunity Solution Tree](../opportunity-solution-tree/) — Validate solution hypotheses from the framing
- [Epic Breakdown](../epic-breakdown/) — Decompose the framed idea into Jira epics and stories

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-04-09 | Claude | Initial skill creation |
