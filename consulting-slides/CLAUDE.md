# Consulting Slides Skill - Claude Instructions

## Purpose

Transform raw materials (documents, screenshots, data) into McKinsey-style consulting presentation slides using Python and python-pptx.

## Workflow

1. **Read inputs** from `inputs/` folder (screenshots, documents, data files)
2. **Analyze content** and identify key messages, data points, insights
3. **Create Python script** in `temp/` using python-pptx library
4. **Generate PowerPoint** in `outputs/` folder
5. **Create presenter narrative** (optional) for storytelling support

## Slide Design Principles

### McKinsey Style
- **One key message per slide** - the "so what"
- **Action title** - complete sentence stating the insight
- **Supporting evidence** - data, charts, bullets that prove the title
- **Source line** - data provenance at bottom

### Visual Hierarchy
- Use color strategically (red for problems, green for solutions, blue for neutral)
- Create clear visual comparison boxes
- Use consistent fonts and spacing

## Key Code Patterns

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Widescreen dimensions
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Add blank slide
slide = prs.slides.add_slide(prs.slide_layouts[6])
```

## Strategic Thinking

When creating slides:
1. **Start with the story** - What's the narrative arc?
2. **Lead with insight** - Hook → Problem → Discovery → Solution → Action
3. **Make it actionable** - PMs and leadership should know what to do
4. **Use data** - Numbers make arguments compelling

## Folder Structure

```
consulting-slides/
├── README.md          # Human documentation
├── CLAUDE.md          # This file (AI instructions)
├── inputs/            # Drop materials here (not committed)
├── outputs/           # Generated slides (not committed)
└── temp/              # Working scripts (not committed)
```

## Dependencies

- python-pptx: `pip install python-pptx`
