# enableNow Demo Storytelling

Create persona-driven demo stories and bubble text for SAP enable-now tutorials.

## What It Does

This skill helps you create compelling demo content by:

1. **Analyzing feature slides** to identify key value propositions
2. **Suggesting relevant personas** from SAP Signavio Personas 2025 (you confirm)
3. **Writing bubble text** for each screenshot in a demo flow
4. **Creating story summaries** that explain the value delivered

## Quick Start

```
/enableNow
```

## Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  You share      │────▶│  I suggest      │────▶│  You confirm    │
│  feature slide  │     │  personas       │     │  or adjust      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                        ┌───────────────────────────────┘
                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  You share      │────▶│  I write        │────▶│  Complete       │
│  screenshots    │     │  bubble text    │     │  demo story     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Example Interaction

### 1. You share a feature slide

> "Here's the LeanIX Application Lifecycle Status feature"

### 2. I suggest personas

> Based on this feature, I recommend:
>
> | Persona | Role in Demo | Why |
> |---------|--------------|-----|
> | **Process Modeler** | End user | Submits process, sees rejection |
> | **Head of Process Excellence** | Approver | Reviews rejected processes |
>
> Do you want to proceed with these?

### 3. You confirm

> "Yes, use Maria Chen and David Martinez"

### 4. You share screenshots

> "Here are 14 screenshots for the Process Modeler journey"

### 5. I write bubble text

> **Screenshot 1**: "Maria just finished updating the 'Develop Go-to-Market tactics' process..."

## Outputs

| Output | Description |
|--------|-------------|
| Cover page content | Key improvements + persona descriptions |
| Bubble text | Third-person narrative for each screenshot |
| Story summary | Value delivered explanation |

## Personas Supported

Based on SAP Signavio Personas 2025 (22 personas):

| Category | Example Personas |
|----------|------------------|
| **Doers** | Process Participant, Process Owner, Domain Expert |
| **Enablers** | Process Modeler, IT System Admin, BPM Consultant |
| **Strategists** | Process Analyst, Head of Process Excellence, Enterprise Architect |
| **Executives** | CPO, CIO, CFO, COO |

## File Structure

```
skills/enableNow/
├── SKILL.md          # AI instructions
├── README.md         # This file
├── demos/            # Generated demo stories
│   └── leanix-app-lifecycle/
│       └── process-modeler-story.md
└── temp/             # Working files
```

## Tips

- **I suggest, you confirm** - I'll recommend personas based on the feature, you approve or adjust
- **Provide names** - "Maria Chen" is more engaging than "Process Modeler"
- **Third person narrative** - Stories read as "Maria clicks..." not "I click..."
- **Emotional beats** - "Uh oh!" when something goes wrong, "Perfect!" when it works

---

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-04-21 | Abdelrahman Elfar | Initial skill creation with LeanIX demo pilot |
| 2026-04-21 | Abdelrahman Elfar | Updated workflow: AI suggests personas, user confirms |
