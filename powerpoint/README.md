# powerpoint

Create SAP-branded PowerPoint presentations using python-pptx. Transforms content into polished `.pptx` files following SAP corporate design guidelines.

## What This Does

- Generates professional SAP-branded presentations
- Follows SAP corporate design guidelines (colors, fonts, layouts)
- Uses official SAP/Signavio templates from repository
- Converts various inputs (bullet points, transcripts, documents) into slides
- Outputs ready-to-use `.pptx` files

**Why this exists**: Creating presentations manually is tedious and often results in inconsistent branding. This automates the layout and styling work so you can focus on content.

## Usage

### Option 1: Describe What You Need
```
Create a 5-slide presentation about our Q1 roadmap highlights
```

### Option 2: Convert Existing Content
```
Turn these meeting notes into a presentation: @path/to/notes.md
```

### Option 3: With Specific Requirements
```
Create a customer-facing deck about our new AI features.
Audience: C-level executives
Slides: 8-10
Focus: Business value, not technical details
```

### Option 4: From Transcript
```
Create a summary presentation from this meeting transcript:
[paste transcript or @path/to/transcript.txt]
```

## How It Works

1. **Analyzes your input** - Identifies presentation type and audience
2. **Asks clarifying questions** - Gathers missing context if needed
3. **Plans slide structure** - Creates outline before generating
4. **Generates presentation** - Applies SAP styling automatically
5. **Quality checks** - Verifies brand compliance
6. **Saves to file** - Ready for immediate use

## Prerequisites

- **Python** installed (Company Portal or https://python.org/)
- Libraries `python-pptx` and `Pillow` (installed automatically)

## Output Location

Presentations are saved to:
```
outputs/[presentation-name].pptx
```

Naming examples:
- `outputs/q1-roadmap-highlights.pptx`
- `outputs/2026-02-27-customer-pitch.pptx`

## Resources

| File | Purpose |
|------|---------|
| [SAP Template](../../templates/powerpoint/SAP%20Template.pptx) | Official PowerPoint template |
| [Style Guide](../../templates/powerpoint/SAP_PowerPoint_Style_Guide.md) | Color palette, typography, layout rules |
| [Signavio Template](../../templates/powerpoint/SAP_Signavio.potx) | Signavio-branded variant |

## Tips for Better Results

- Be specific about your audience (executive, technical, customer-facing)
- Mention how many slides you want
- Reference existing content with "based on [file]"
- Ask for revisions: "Make the bullets shorter" or "Add more visuals"

## Integration with Other Skills

- **transcripts**: Use meeting notes as presentation source
- **productboard-insights**: Pull feature highlights for roadmap decks
- **jira**: Reference sprint goals for planning presentations

## Support

Questions or issues? Reach out in #claude-code-help

---

**Original Author**: Aviral Vaid (LeanIX Product Management)
**Category**: Content Creation
**Integrated from**: [LeanIX PM Marketplace](https://github.tools.sap/LeanIX/LeanIX-PM-Marketplace)
