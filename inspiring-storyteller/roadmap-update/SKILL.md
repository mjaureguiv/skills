---
name: roadmap-update
description: Prepare compelling roadmap update materials for leadership reviews using ProductBoard data
version: 1.0.0
---

# Roadmap Update for Leadership Round

> 🧪 **Experimental MCP**: This skill uses ProductBoard MCP which is NOT listed in the SAP Hyperspace MCP Registry. Do not use with customer data or PII.

## Purpose

Prepare compelling roadmap update materials for leadership reviews. Transform ProductBoard roadmap data into leadership-ready deliverables with value propositions, confidence levels, and changelog summaries.

---

## When to Use

- Monthly/Quarterly leadership roadmap reviews
- Preparing materials for leadership rounds
- Creating changelog slides for roadmap updates
- Generating PB links and confidence summaries

---

## Required Input

User provides one of:
1. **ProductBoard CSV export** (Release checks monthly/quarterly view)
2. **ProductBoard view link** (for MCP fetch)
3. **Manual list** of features to include

### Expected CSV Columns
Key columns from ProductBoard export:
- `entity_name` - Feature name
- `description` - Contains Value proposition, Benefits, Capabilities, Screenshots
- `pb_url` - ProductBoard link
- `Release Confidence %` - Confidence level (High/Medium/Low or %)
- `status_name` - Current status
- `Roadmap Visibility` - External/Internal/Confidential
- Month columns (e.g., "April 2026", "May 2026") - Release timing
- `NOW/NEXT/LATER` - Release horizon

---

## Output Deliverables

### 1. Feature Summary Table (for PB Links)

Generate a markdown table with:

| Feature | Value Proposition | Confidence | PB Link | Target Release |
|---------|-------------------|------------|---------|----------------|
| Feature name | One-line value prop | High/Med/Low | [Link](url) | Month Year |

**Instructions:**
- Extract value proposition from description (first paragraph after "Value proposition")
- Map confidence: 80%+ = High, 50-79% = Medium, <50% = Low
- Only include features with `Roadmap Visibility = External`
- Sort by release date (earliest first)

---

### 2. Changelog Slide Content

Create a **single slide** summarizing roadmap changes. Structure:

```
ROADMAP CHANGELOG
[Month] Leadership Review

MONTHLY VIEW CHANGES:
+ Added: [List new features added this month]
→ Moved: [Features with date changes]
- Removed: [Features removed from roadmap]
⚠ Confidence: [Features with changed confidence]

QUARTERLY VIEW CHANGES:
Q[X] [Year]:
  • [Key additions/changes]

Q[X+1] [Year]:
  • [Key additions/changes]

KEY HIGHLIGHTS:
• [2-3 most significant changes in human language]
```

---

### 3. Confidence Summary

Group features by confidence level:

```markdown
## Confidence Overview

### High Confidence (80%+)
- Feature A - [Target: Month Year]
- Feature B - [Target: Month Year]

### Medium Confidence (50-79%)
- Feature C - [Target: Month Year] - [Risk note if available]

### Low Confidence (<50%)
- Feature D - [Target: Month Year] - [Blocker/risk]

### Missing Confidence
- Feature E - [No confidence set - needs update]
```

---

## Process

### Step 1: Data Extraction
1. Read the ProductBoard CSV or fetch via MCP
2. Filter to `Roadmap Visibility = External` (unless user specifies otherwise)
3. Parse the `description` field to extract structured data

### Step 2: Parse Value Proposition
From description, extract:
- **Value proposition**: Text after "Value proposition" header
- **Benefits**: Bullet list after "Benefits" header
- **Capabilities**: Bullet list after "Capabilities" header
- **Screenshots**: Image URLs (for reference)

### Step 3: Build Deliverables
1. Create Feature Summary Table
2. Compare with previous export (if available) to generate changelog
3. Group by confidence level
4. Format for leadership presentation

### Step 4: Generate Outputs
Save outputs to `skills/inspiring-storyteller/roadmap-update/temp/`:
- `feature-summary-[date].md` - PB links table
- `changelog-slide-[date].md` - Slide content
- `confidence-summary-[date].md` - Confidence breakdown

---

## Changelog Detection

To identify changes, compare current export with previous:

### New Features
- Present in current but not in previous export (by `entity_uuid`)

### Moved Features
- Same `entity_uuid` but different month column has "X"
- Document: "Feature X moved from [Old Month] to [New Month]"

### Removed Features
- Present in previous but not in current export

### Confidence Changes
- Same `entity_uuid` but different `Release Confidence %`

---

## Slide Formatting Guidelines

For the changelog slide:
- **Keep it scannable** - Leadership reviews are fast
- **Use icons/emojis** sparingly for visual grouping
- **Highlight risks** - Call out low confidence items
- **Be specific** - "Moved from May to July" not "date changed"
- **Max 10-12 items** - Summarize if more changes

---

## Example Output

### Feature Summary Table

| Feature | Value Proposition | Confidence | PB Link | Target |
|---------|-------------------|------------|---------|--------|
| AI-assisted process documentation | Use SPG to control AI-generated actions before execution | High | [View](https://productboard.com/...) | Apr 2026 |
| Workflow templates library | Pre-built templates for common governance scenarios | Medium | [View](https://productboard.com/...) | May 2026 |

### Changelog Slide

```
ROADMAP CHANGELOG
March 2026 Leadership Review

MONTHLY VIEW:
+ Added: AI document summarization, Bulk approval workflows
→ Moved: Template library (Apr → May), Mobile approvals (Q2 → Q3)
- Removed: Legacy export feature (deprecated)

QUARTERLY VIEW:
Q2 2026: +3 AI features, Template library delayed 1 month
Q3 2026: Mobile-first initiative begins, 2 features moved from Q2

KEY HIGHLIGHTS:
• AI capabilities expanding faster than planned - 3 new features
• Template library delayed due to UX research findings
• Q3 scope increased with mobile initiative kickoff
```

---

## Deadline Awareness

When user mentions a deadline:
- Prioritize the deliverables they need
- Surface blockers early (missing data, unclear requirements)
- Provide draft outputs quickly, then refine

**Example**: "Send by Thursday 12pm" →
- Generate quick draft immediately
- Flag any missing information
- Ask clarifying questions early, not at deadline

---

## Integration with ProductBoard MCP

If ProductBoard MCP is available, you can:
1. Fetch features directly: `productboard_search_features()`
2. Get confidence values: `productboard_get_custom_field_value()`
3. Build the summary from live data

This provides more accurate, real-time data than CSV exports.
