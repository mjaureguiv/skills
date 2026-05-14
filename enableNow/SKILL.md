---
name: enableNow
description: "Create demo bubble text for SAP enable-now tutorials. Use when user shares feature slides and demo screenshots to generate persona-driven storytelling content for enable-now click-through demos."
version: 1.0.0
user-invocable: true
---

# enableNow Demo Storytelling Skill

Transform feature screenshots into compelling persona-driven demo stories for SAP enable-now tutorials.

## What This Skill Does

You provide:
1. A **feature slide** showing what the feature does
2. **Demo screenshots** showing the user journey

I create:
- **Cover page content** with key improvements and persona descriptions
- **Bubble text** for each screenshot telling an end-to-end story from the persona's perspective
- **Story summary** explaining the value delivered

---

## How to Use This Skill

### Step 1: Share the Feature Slide

Share a slide or description of the feature. I will:
- Identify the key improvements/value propositions
- Analyze who uses, approves, and configures this feature

### Step 2: I Suggest Personas → You Confirm

**I will automatically suggest relevant personas** based on the feature, using the SAP Signavio Personas 2025 framework.

**Example suggestion:**
> Based on this feature, I recommend these personas for the demo:
>
> | Persona | Role in Demo | Why |
> |---------|--------------|-----|
> | **Process Modeler** | End user | Submits process, sees rejection |
> | **Head of Process Excellence** | Approver | Reviews rejected processes |
> | **IT System Admin** | Admin (optional) | Configures the workflow action |
>
> Do you want to proceed with these? You can:
> - ✅ Confirm as-is
> - ➕ Add personas I missed
> - ➖ Remove personas that don't fit
> - ✏️ Provide specific names (e.g., "Maria Chen" instead of "Process Modeler")

**You confirm or adjust**, then I'll generate the cover page content with persona descriptions.

### Step 3: Share Demo Screenshots

For each persona perspective, share the screenshots. I will:
- Number them in sequence
- Write bubble text telling the story from that persona's viewpoint
- Use third-person narrative ("Maria clicks..." not "I click...")

---

## SAP Signavio Personas 2025 Reference

**Archetype 1 - Role in Transformations:**
| Doers | Enablers | Strategists | Executives |
|-------|----------|-------------|------------|
| Process Participant | Process Modeler | Process Analyst | Executive |
| Process Owner | BPM Consultant | Head of Process Excellence | Business Owner |
| Domain Expert | Automation Developer | Enterprise Architect | CPO |
| | IT System Admin | Transformation Lead | CIO |
| | Data Provider | Head of SAP CoE | CFO |
| | Process Mining Consultant | Head of IT | COO |
| | Data Modeler | | |

**Common Demo Personas:**
- **Process Modeler** - Creates/edits process diagrams (end user)
- **Head of Process Excellence** - Approves processes, ensures governance
- **IT System Admin** - Manages system configuration
- **Enterprise Architect** - Maintains IT landscape data

---

## Output Format

### Cover Page Content

```markdown
### Key Improvements:
- [Improvement 1]
- [Improvement 2]
- [Improvement 3]

### Personas

**[Role] - [Name]**
> [Description of persona's responsibilities and goals]

**[Role] - [Name]**
> [Description of persona's responsibilities and goals]
```

### Demo Story (Per Persona)

```markdown
## Demo Story: [Persona Role] Perspective

**Persona**: [Role]
**Name**: [Name]
**Feature**: [Feature Name]
**Scenario**: [What the demo shows]

---

## Screenshot 1: [Screen Title]
**Screen**: [Where in the product]
**Action**: [What's happening]

**Bubble Text**:
> "[Name] [action in third person]..."

---

## Screenshot 2: ...
```

---

## Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Feature Slide  │────▶│  Identify       │────▶│  Cover Page     │
│                 │     │  Personas       │     │  Content        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                        ┌───────────────────────────────┘
                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Demo           │────▶│  Write Bubble   │────▶│  Story          │
│  Screenshots    │     │  Text           │     │  Document       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## Bubble Text Guidelines

### Writing Style
- **Third person**: "Maria clicks..." not "I click..."
- **Present tense**: "She sees..." not "She saw..."
- **Action-oriented**: Describe what they're doing and why
- **Natural dialogue**: Sound like a real person thinking through their task

### Story Arc
1. **Setup**: What is the persona trying to accomplish?
2. **Discovery**: What does the system show them?
3. **Action**: What decision/action do they take?
4. **Outcome**: What's the result? What did they learn?

### Emotional Beats
- **Anticipation**: "Let me check..." / "Time to..."
- **Discovery**: "I can see..." / "There it is..."
- **Surprise**: "Uh oh!" / "Interesting..."
- **Resolution**: "Now I know..." / "This saved us from..."

---

## Example: LeanIX Application Lifecycle Check

### Cover Page

**Key Improvements:**
- Stops blind approvals by exposing lifecycle risks early
- Prevent designs based on expired or soon-to-expire applications
- Reduce rework by catching issues before the approval moves forward

**Personas:**

**Process Modeler - Maria Chen**
> Maria is responsible for creating and maintaining accurate and comprehensive process models and documentation. She works with various business units to document their processes and ensures they get proper approval before publishing.

**Head of Process Excellence - David Martinez**
> David is responsible for establishing and promoting best practices in business process management across the organization. His objective is to improve process efficiency, effectiveness, and consistency across the enterprise.

### Sample Bubble Text

**Screenshot 1** (Diagram View):
> "Maria just finished updating the 'Develop Go-to-Market tactics' process. She notices the approval status shows 'Rejected' from a previous submission. Time to review the diagram and submit it for approval again."

**Screenshot 12** (Invalid Applications Found):
> "Uh oh! The automated check found a problem. 'Invalid Applications Found' shows 'Yes' - specifically 'SAP ERP 6.0 (ECC) / SAP CO' with a lifecycle date of 2022-05-01. This application has reached end-of-life and shouldn't be used in new processes!"

---

## Output Locations

| File | Location |
|------|----------|
| Demo stories | `skills/enableNow/demos/[feature-name]/[persona]-story.md` |
| Temp files | `skills/enableNow/temp/` |

---

## File Structure

```
skills/enableNow/
├── SKILL.md                    # This file
├── README.md                   # Human documentation
├── demos/
│   └── [feature-name]/
│       ├── process-modeler-story.md
│       ├── approver-story.md
│       └── admin-story.md
└── temp/                       # Working files
```

---

## Tips for Great Demo Stories

1. **Name your personas** - "Maria" is more engaging than "the user"
2. **Show the journey** - Include setup, action, and outcome
3. **Highlight the value** - Make clear what problem was solved
4. **Keep it conversational** - Write like someone talking through their task
5. **Add emotional moments** - "Uh oh!" when something goes wrong, "Perfect!" when it works

---

## SAP Signavio Personas Reference

The 22 SAP Signavio personas are organized by:

**Archetype 1 - Role in Transformations:**
- **Doers**: Execute day-to-day work within processes
- **Enablers**: Build and maintain process capabilities
- **Strategists**: Design and oversee process improvements
- **Executives**: Set direction and make investment decisions

**Archetype 2 - Influence on Buying Decision:**
- **Users**: Use the product daily
- **Users with Buying Influence**: Use and influence purchases
- **Buyers**: Make purchasing decisions
