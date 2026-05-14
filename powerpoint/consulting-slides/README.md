# Consulting Slides Skill

Transform raw materials (documents, screenshots, data) into McKinsey-style consulting presentation slides.

## What It Does

- Analyzes input materials (screenshots, documents, data files)
- Extracts key insights and data points
- Creates professional PowerPoint presentations using python-pptx
- Optionally generates presenter narratives for storytelling

## Usage

1. Drop your materials into `inputs/` folder (screenshots, docs, data)
2. Ask Claude to create slides based on the inputs
3. Find generated PowerPoint in `outputs/` folder

## Example Prompts

- "Create a slide summarizing the key points from the screenshots in the inputs folder"
- "Build a presentation about [topic] using the data I provided"
- "Make this into a McKinsey-style executive summary slide"

## Design Principles

### McKinsey Style
- **One key message per slide** - the "so what"
- **Action titles** - complete sentences stating the insight
- **Supporting evidence** - data, charts, bullets that prove the title
- **Visual hierarchy** - strategic use of color and layout

### Storytelling Structure
1. **Hook** - Grab attention with a provocative question or insight
2. **Problem/Discovery** - Present the tension or finding
3. **Insight** - Reveal the key understanding
4. **Solution/Path** - Show the way forward
5. **Call to Action** - Inspire action

## Folder Structure

```
consulting-slides/
├── README.md          # This file
├── CLAUDE.md          # AI instructions
├── inputs/            # Drop your materials here
├── outputs/           # Generated slides appear here
└── temp/              # Working files
```

## Dependencies

Requires `python-pptx`:
```bash
pip install python-pptx
```

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-03-02 | I745835 | Initial skill creation |
