---
name: powerpoint
description: "Create SAP-branded PowerPoint presentations. Use when user wants to create presentations, pitch decks, slides, any PPTX content, or mentions 'deck', 'slides', or 'presentation'. Transforms content into polished .pptx files following SAP corporate design guidelines."
version: 1.0.0
user-invocable: true
---

# PowerPoint Presentation Skill

Turn your ideas into polished SAP-branded slide decks automatically.

## What This Skill Does

You give it content (bullet points, meeting notes, or just a topic), and it creates a professional PowerPoint file that:

- Looks like it came from SAP's design team (correct colors, fonts, layouts)
- Is ready to present or share immediately (no manual cleanup needed)
- Follows all corporate branding rules automatically
- **Plans before building** - you can review and approve the structure first
- **Validates visually** - exports slides as images to catch layout issues

---

## How to Use This Skill

Just tell me what presentation you need. Here are some examples:

### Just describe it
```
Create a 5-slide presentation about our Q1 roadmap highlights
```

### Point to existing content
```
Turn these meeting notes into a presentation: @path/to/notes.md
```

### Be specific about your audience
```
Create a customer-facing deck about our new AI features.
Audience: C-level executives
Slides: 8-10
Focus: Business value, not technical details
```

---

## Workflow: Reference Deck → Plan → Build

### Step 0: Ask for Reference Deck (Optional)

**IMPORTANT**: Before starting any presentation, I will first ask:

> "Do you have an example slide deck that you'd like me to use as a reference?
> This could be a presentation you love, one that matches your style, or a company template.
>
> - **If yes**: Share the file path and I'll deeply analyze it to learn your preferred patterns
> - **If no**: That's fine! I'll use my built-in SAP presentation patterns"

#### If User Provides a Reference Deck

When you provide a reference deck, I will:

1. **Deeply analyze it** - Extract slide patterns, layouts, color usage, content structure
2. **Prefer your patterns** - For this presentation, I'll prioritize the patterns from your reference over my built-in ones
3. **Compare to existing patterns** - I'll identify what's new vs. what I already know
4. **Offer to update the skill** - I'll ask:
   > "I found these new patterns in your reference deck:
   > - [Pattern 1]: [Description]
   > - [Pattern 2]: [Description]
   >
   > Would you like me to add these to the PowerPoint skill so I can use them in future presentations too?"
5. **Create a PR if approved** - If you want the patterns saved, I'll update the skill and create a pull request for your review

**Privacy note**: I only extract structural patterns (layout, colors, typography). Actual content from your reference deck stays confidential and is never stored in the skill.

---

## Planning: Plan First or Build Directly?

After the reference deck step, I will ask:

> "Would you like me to:
> 1. **Show you a plan first** - I'll create a detailed outline you can review and annotate
> 2. **Build directly** - I'll create the presentation immediately"

### Option 1: Plan First (Recommended for complex presentations)

If you choose "Plan First", I will:

1. **Create a planning document** at `experiment/tmp/presentation-plan.md`
2. The plan includes for EACH slide:
   - Slide type (cover, content, two-column, etc.)
   - Title
   - Detailed content description
   - Visual layout description (what goes where)
   - Design notes (colors, emphasis, spacing)
3. **You review and annotate** the plan
   - Add comments
   - Request changes
   - Approve or modify content
4. **Only after your approval** do I create the actual presentation

### Option 2: Build Directly

If you choose "Build Directly", I will:

1. Create the presentation immediately
2. Run visual validation (see below)
3. Show you the result

---

## The Workflow (Step by Step)

### Step 1: Ask for Reference Deck

```
Do you have an example slide deck you'd like me to use as a reference?

- **If yes**: Share the file path and I'll analyze it to learn your patterns
- **If no**: I'll use my built-in SAP presentation patterns

(This is optional - skip if you're happy with standard SAP styling)
```

### Step 2: (If Reference Provided) Analyze and Offer Pattern Updates

If you provide a reference deck, I will:
1. Analyze the deck for patterns (layouts, structures, visual elements)
2. Show you what I found
3. Ask if you want me to update the skill with new patterns
4. If yes and you approve the changes, I'll create a pull request

### Step 3: Ask Planning Preference

```
Before I create your presentation, would you like to:

1. **See a plan first** - I'll create a detailed outline (presentation-plan.md)
   that you can review, annotate, and approve before I build anything.

2. **Build directly** - I'll create the presentation immediately and
   then validate it visually.

Which do you prefer?
```

### Step 4: (If Plan First) Create Planning Document

I create `experiment/tmp/presentation-plan.md` with this structure:

```markdown
# Presentation Plan: [Title]

**Audience:** [Who is this for]
**Purpose:** [What should they take away]
**Estimated slides:** [Number]
**Template:** SAP Template

---

## Slide 1: Cover

**Type:** Cover slide (Layout 0)
**Title:** "[Main title here]"
**Subtitle:** "[Subtitle/date/presenter]"

**Visual Layout:**
┌────────────────────────────────────┐
│                                    │
│         [TITLE - Large, White]     │
│         ─────────────────          │
│         [Subtitle - Lighter]       │
│                                    │
│                        [Date]      │
└────────────────────────────────────┘

**Design Notes:**
- Dark blue background (#002A86)
- White title text, 44pt bold
- Accent bar below title

---

## Slide 2: Agenda

**Type:** Agenda slide (Layout 12)
**Title:** "Agenda"

**Content:**
1. [First topic]
2. [Second topic]
3. [Third topic]
4. [Fourth topic]

**Visual Layout:**
┌────────────────────────────────────┐
│ Agenda                             │
├────────────────────────────────────┤
│                                    │
│  1. First topic                    │
│  2. Second topic                   │
│  3. Third topic                    │
│  4. Fourth topic                   │
│                                    │
└────────────────────────────────────┘

**Design Notes:**
- Numbered list, bold numbers
- Max 5 items (current: 4)

---

## Slide 3: [Section Name]
...
```

### Step 5: User Reviews and Approves

You can:
- Edit the plan directly
- Add comments like `<!-- CHANGE: Make this more concise -->`
- Reply with changes you want
- Say "Approved" or "Looks good" to proceed

### Step 6: Build the Presentation

Using the slide_builder library:

```python
from lib.slide_builder import SlideBuilder

builder = SlideBuilder(template="SAP Template.pptx")
builder.add_cover_slide("Title", "Subtitle")
builder.add_agenda_slide(["Topic 1", "Topic 2", "Topic 3"])
# ... more slides based on plan
builder.save("output.pptx")
```

### Step 7: Visual Validation (CRITICAL)

After building, I perform a **slide-by-slide visual check**:

1. **Export each slide as an image** (PNG)
2. **Visually inspect each image** looking for:
   - Overlapping text boxes
   - Elements cut off at edges
   - Misaligned content
   - Text too small to read
   - Color contrast issues
   - Empty or placeholder areas
3. **If issues found**: Fix and regenerate that slide
4. **Iterate** until all slides pass visual inspection

```python
# Visual validation process
from lib.visual_validator import export_slides_as_images

# Export slides as images
images = export_slides_as_images("output.pptx", "tmp/slide_images/")

# I then READ each image to visually inspect it
# If issues are found, I fix the slide and re-export
```

### Step 8: Deliver

- Save final presentation
- Report location to user
- Offer revisions

---

## Available Slide Types

### Core Slides
| Method | What It Creates | When to Use |
|--------|-----------------|-------------|
| `add_cover_slide()` | Title slide with SAP branding | Always first |
| `add_agenda_slide()` | Agenda with numbered items (max 5) | Presentations > 5 slides |
| `add_section_divider()` | Section break slide | Between major sections |
| `add_content_slide()` | Standard bullet point slide | General content |
| `add_thank_you_slide()` | Closing slide | Always last |

### Data & Metrics Slides
| Method | What It Creates | When to Use |
|--------|-----------------|-------------|
| `add_metrics_slide()` | Big numbers with trends (4 KPIs) | Executive summaries, results |
| `add_table_slide()` | Data table with headers | Structured comparisons, data grids |
| `add_status_table_slide()` | Table with RAG status colors | Project status, risk tracking |
| `add_chart_placeholder_slide()` | Chart area with callout | Trends, analytics (manual chart insert) |

### Comparison & Layout Slides
| Method | What It Creates | When to Use |
|--------|-----------------|-------------|
| `add_two_column_slide()` | Side-by-side comparison | Before/After, Pros/Cons |
| `add_three_column_slide()` | Three-column layout | Features, Options, Products |
| `add_quote_slide()` | Testimonial/quote | Customer quotes |

### Visual & Progress Slides
| Method | What It Creates | When to Use |
|--------|-----------------|-------------|
| `add_image_slide()` | Full image with caption | Screenshots, diagrams |
| `add_screenshot_with_callouts_slide()` | Screenshot + numbered callouts | Product demos, UI walkthroughs |
| `add_progress_slide()` | Progress bars with status | Project progress, completion tracking |
| `add_timeline_slide()` | Horizontal timeline | Roadmaps, milestones, schedules |
| `add_feature_showcase_slide()` | Feature with screenshot + status badge (Beta/GA) | Roadmap presentations, product demos |

### Transformation & Roadmap Slides (NGM Pattern)
| Method | What It Creates | When to Use |
|--------|-----------------|-------------|
| `add_transformation_slide()` | Past → Future two-column comparison | Migration, evolution, change initiatives |
| `add_capability_cards_slide()` | Grid of icon cards showing capabilities | Product overviews, capability summaries |
| `add_release_phases_slide()` | Alpha → Beta → GA timeline with feature boxes | Release planning, product roadmaps |
| `add_roadmap_table_slide()` | Table with timeline columns (H1/H2/Beyond) | Feature roadmaps, release planning |

### Executive & Status Slides (PPR Pattern)
| Method | What It Creates | When to Use |
|--------|-----------------|-------------|
| `add_highlights_lowlights_slide()` | 2-3 column layout with highlights (green), lowlights (red), actions (blue) | Quarterly reviews, status updates, retrospectives |
| `add_keeps_up_at_night_slide()` | Grid of concern boxes with warning styling | Risk discussions, executive escalations |
| `add_ask_slide()` | Numbered requests with owners | Executive asks, resource requests |
| `add_executive_summary_slide()` | Multi-section KPI dashboard with metrics | Executive summaries, leadership reviews |
| `add_funnel_slide()` | Adoption/conversion funnel with stages | Pipeline analysis, conversion metrics |
| `add_okr_slide()` | OKR tracking with progress bars per objective | OKR reviews, goal tracking |
| `add_win_loss_slide()` | Deal outcomes with wins/losses side-by-side | Sales reviews, deal analysis |

### Slide Type Distribution (Based on PPR Analysis)

Real SAP presentations typically use this distribution:
- **Section Dividers**: 20-35% (heavy use for navigation in long decks)
- **Content/Bullet Slides**: 20-25%
- **Table Slides**: 15-20% (metrics, comparisons, status tracking)
- **Chart Slides**: 5-10%
- **Cover/Title**: 5-8%
- **Quote/Image**: 5-10%

---

## Visual Validation Checklist

For each slide, I check:

- [ ] **No overlapping elements** - Text boxes don't cover each other
- [ ] **Nothing cut off** - All content visible within slide bounds
- [ ] **Proper alignment** - Elements aligned to grid
- [ ] **Readable text** - Font size >= 10pt, good contrast
- [ ] **Consistent spacing** - Even gaps between elements
- [ ] **Correct colors** - Only SAP palette colors used
- [ ] **No placeholders** - No "Click to add text" remnants

---

## SAP Brand Colors (Reference)

| Color | Hex | Used for |
|-------|-----|----------|
| SAP Dark Blue | #002A86 | Headers, title bars |
| SAP Medium Blue | #0070F2 | Accents, links |
| SAP Light Blue | #1B90FF | Highlights |
| White | #FFFFFF | Backgrounds, text on dark |
| Black | #000000 | Body text |
| Green | #97DD40 | Positive trends |
| Red | #EE3939 | Negative trends |

---

## Content Rules (Enforced Automatically)

- **Max 6 bullet points** per slide
- **Max 8 words** per bullet point
- **Max 5 agenda items**
- **Minimum 10pt** font size
- **No italics** (use bold instead)
- **One main idea** per slide

---

## Output Locations

| File | Location |
|------|----------|
| Planning document | `experiment/tmp/presentation-plan.md` |
| Slide images (validation) | `experiment/tmp/slide_images/` |
| Final presentation | `experiment/[name].pptx` |

---

## Response Style Guidelines

### When asking about reference deck
```
Do you have an example slide deck you'd like me to use as a reference?

- **If yes**: Share the file path and I'll analyze it to learn your patterns
- **If no**: I'll use my built-in SAP presentation patterns

(This is optional - just say "no" to skip)
```

### After analyzing reference deck
```
I've analyzed your reference deck and found these patterns:

**New patterns I can learn:**
- [Pattern name]: [Brief description]
- [Pattern name]: [Brief description]

**Patterns similar to what I already know:**
- [Pattern name]: Minor variations in [aspect]

Would you like me to update the PowerPoint skill with these new patterns?
If yes, I'll make the changes and create a PR for your review.
```

### When asking about planning
```
Before I create your presentation, would you like to:

1. **See a plan first** - I'll create a detailed outline you can review
2. **Build directly** - I'll create it now and validate visually

Which do you prefer?
```

### After planning document created
```
I've created the presentation plan at:
experiment/tmp/presentation-plan.md

Please review it and let me know:
- Any changes you'd like to make
- "Approved" when you're ready for me to build it
```

### After visual validation
```
I've validated all 12 slides visually:
- Slides 1-11: ✓ Passed
- Slide 12: Fixed overlapping text, re-validated ✓

Presentation saved to: experiment/q1-update.pptx
```

---

## File Structure

```
skills/powerpoint/
├── SKILL.md                          # This file
├── lib/
│   ├── slide_builder.py              # Slide building functions
│   ├── validate_presentation.py      # Brand compliance validation
│   ├── visual_validator.py           # Image export & visual checks
│   └── brand_config.yaml             # Brand rules
├── blueprints/
│   ├── customer_presentation.yaml
│   ├── internal_update.yaml
│   ├── technical_overview.yaml
│   └── quarterly_review.yaml
└── temp/                             # Generated scripts

templates/powerpoint/
├── SAP Template.pptx                 # Main template (45 layouts)
└── SAP_PowerPoint_Style_Guide.md     # Brand reference
```

---

## Example Planning Document

Here's what a planning document looks like:

```markdown
# Presentation Plan: Q1 Product Update

**Audience:** Leadership team
**Purpose:** Share Q1 progress and Q2 priorities
**Estimated slides:** 8
**Template:** SAP Template

---

## Slide 1: Cover

**Type:** Cover slide
**Title:** "Q1 2026 Product Update"
**Subtitle:** "SAP Signavio Team | March 2026"

**Visual Layout:**
┌────────────────────────────────────────┐
│  ████████████████████████████████████  │ <- Dark blue bg
│                                        │
│       Q1 2026 Product Update           │ <- White, 44pt, bold
│       ══════════════════════           │ <- Blue accent line
│       SAP Signavio Team                │ <- Light blue, 24pt
│                                        │
│                          March 2026    │ <- Bottom right
└────────────────────────────────────────┘

---

## Slide 2: Agenda

**Type:** Agenda slide
**Title:** "Agenda"

**Content:**
1. Executive Summary
2. Key Metrics
3. Product Highlights
4. Q2 Priorities

**Visual Layout:**
┌────────────────────────────────────────┐
│ ▓▓ Agenda                              │ <- Header bar
├────────────────────────────────────────┤
│                                        │
│   1. Executive Summary                 │
│   2. Key Metrics                       │
│   3. Product Highlights                │
│   4. Q2 Priorities                     │
│                                        │
└────────────────────────────────────────┘

---

## Slide 3: Executive Summary

**Type:** Content slide (bullets)
**Title:** "Executive Summary"

**Content:**
• Strong Q1 with 25% revenue growth
• Launched 3 major features
• Customer satisfaction at all-time high
• On track for annual targets

**Visual Layout:**
┌────────────────────────────────────────┐
│ ▓▓ Executive Summary                   │
├────────────────────────────────────────┤
│                                        │
│   • Strong Q1 with 25% revenue growth  │
│   • Launched 3 major features          │
│   • Customer satisfaction at ATH       │
│   • On track for annual targets        │
│                                        │
└────────────────────────────────────────┘

---

## Slide 4: Key Metrics

**Type:** Metrics slide (big numbers)
**Title:** "Key Metrics"

**Content:**
| Value | Label | Trend |
|-------|-------|-------|
| €12.5M | Revenue | ↑ |
| 850+ | Customers | ↑ |
| 99.9% | Uptime | - |
| 47 | NPS | ↑ |

**Visual Layout:**
┌────────────────────────────────────────┐
│ ▓▓ Key Metrics                         │
├────────────────────────────────────────┤
│                                        │
│  €12.5M    850+     99.9%     47       │ <- Big, bold
│    ↑         ↑                 ↑       │ <- Trend arrows
│  Revenue  Customers  Uptime   NPS      │ <- Gray labels
│                                        │
└────────────────────────────────────────┘

**Design Notes:**
- 4 metrics in a row
- Green color for "up" trends
- Gray labels below numbers
```

---

## Quality Guarantee

Every presentation goes through:

1. **Plan** (optional) - Detailed outline for your review
2. **Build** - Using tested, reusable functions
3. **Validate (brand)** - Automatic compliance check
4. **Validate (visual)** - Export as images, inspect each slide
5. **Fix & Iterate** - Resolve any issues found
6. **Deliver** - Clean, polished output

You get consistent, brand-compliant, visually-verified presentations every time.
