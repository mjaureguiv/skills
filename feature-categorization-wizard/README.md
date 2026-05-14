# Feature Categorization Wizard

A guided, iterative workflow to help Product Managers transform raw customer insights into mutually exclusive, well-defined features with comprehensive product requirements.

## Purpose

This skill guides you through a multi-step process to:
1. Extract and organize customer insights from Productboard
2. Build initial categories using AI-assisted analysis
3. Iteratively refine categories by reviewing and reassigning insights
4. Generate comprehensive product requirements, user stories, and benefits for each category
5. Validate categories are truly mutually exclusive and customer-focused

## Workflow Overview

### Step 0: Manual Insight Attachment (Prerequisite)
**Manual work in Productboard - BEFORE creating CSV**

1. Go to Productboard and review all raw customer insights for your feature/topic
2. For each insight, manually examine it and determine which component(s) it relates to
3. Attach/link each insight to the appropriate Productboard component or feature
4. Add notes or tags if needed to clarify the connection
5. This ensures insights are properly categorized in Productboard first

### Step 1: Insight Collection & CSV Creation
**Manual data collection from Productboard**

1. Review all the attached insights in Productboard
2. One by one, copy the insight text
3. Copy the insight URL and feature/component URL from Productboard
4. Paste into a spreadsheet with three columns: `INSIGHT_TEXT`, `PRODUCTBOARD_INSIGHT_URL`, `PRODUCTBOARD_FEATURE_URL`
5. Export the spreadsheet as CSV format
6. Upload CSV to `/temp/` folder: `skills/feature-categorization-wizard/temp/[feature-name]_insights.csv`

### Phase 2: AI-Assisted Categorization
- Ask Claude to analyze the CSV
- Generate initial mutually exclusive feature categories
- List focus area for each category
- Extract Productboard URLs for traceability

### Phase 3: Manual Review & Assignment
- Review each category and its focus area
- Visit each Productboard URL for the category
- Assign all related insights to that feature in Productboard
- Validate boundaries between categories

### Phase 4: Export & Analysis
- Export insights for each new category from Productboard
- Upload exports to `/temp/` folder
- Ask Claude to generate comprehensive analysis:
  - Customer Problem
  - Product Gap
  - User Stories (5-8 per feature)
  - Product Requirements (detailed and prioritized)
  - Potential Capabilities (how to solve)
  - Potential Benefits (business and user impact)

### Phase 5: Iterative Refinement
- Review generated analysis against original insights
- If a customer problem doesn't match the category, ask Claude which insights should move
- Reassign insights to correct categories in Productboard
- Re-export and regenerate analysis
- Repeat until all categories are clean and mutually exclusive

### Phase 6: Final Output
- Compile final feature definitions with all supporting analysis
- Document category boundaries and why they're distinct
- Create PRD or feature tickets (using other skills)
- Maintain audit trail of how insights were categorized

## How to Use

**Start here:**
```
#feature-categorization-wizard

I want to categorize the insights from [Feature Name or Topic] in Productboard.

First, I need to:
1. Manually review and attach all insights to components in Productboard (Step 0)
2. Create a CSV with insight text and URLs (Step 1)

Once I have prepared the CSV at: [path to CSV]

Please begin Step 2: Analyze these insights and generate initial mutually exclusive categories.
```

**When reviewing insights:**
```
After I assign insights to categories in Productboard, here are the exports for [Category Name]:

[Paste or attach CSV exports]

Please generate Step 4 analysis: Customer Problem, Product Gap, User Stories, Product Requirements, Potential Capabilities, and Potential Benefits.
```

**When refining categories:**
```
The analysis shows [Description of issue]. This doesn't align with the Customer Problem for this category. 

Which insights (and their Productboard URLs) should potentially move to a different category?
```

## Key Principles

1. **Start with manual attachment**: Insights must be attached to components in Productboard first (Step 0)
2. **Then create CSV**: Only after attachment, copy data into CSV (Step 1)
3. **Mutually Exclusive**: Each insight belongs to exactly one category; no overlap.
4. **Customer-Focused**: Categories reflect customer problems, not technical capabilities.
5. **Traceability**: Every insight and feature is linked back to Productboard URLs.
6. **Iterative**: Don't aim for perfection in the first pass; refine through multiple rounds.
7. **Comprehensive**: Each final category has full product requirements, not just naming.

## Output Artifacts

- `[feature-name]_categories_v[n].csv` - Final categorization with URLs
- `[feature-name]_analysis_[category-name].md` - Full analysis for each category
- `[feature-name]_category_map.md` - Boundary definitions between categories
- `[feature-name]_audit_trail.md` - Log of decisions and changes made

## Tips

- Start with 5-8 initial categories (not more than 10)
- Expect 2-3 rounds of refinement before categories stabilize
- When unsure, ask Claude "which insights should move?"
- Use the category focus area to quickly validate placement
- Keep Productboard open in another window while working through categories
