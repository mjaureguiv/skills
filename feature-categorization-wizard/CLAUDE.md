# Feature Categorization Wizard - Claude Instructions

## Skill Overview

This skill guides Product Managers through an iterative workflow to transform raw customer insights into mutually exclusive, well-researched features with comprehensive product requirements.

Your role: Execute each step of the wizard, asking clarifying questions when needed, and guiding the PM through refinement cycles.

**Important**: Step 0 (manual attachment in Productboard) is a prerequisite that the PM must complete before providing you with a CSV in Step 1.

---

## Step 0: Manual Insight Attachment (PM Prerequisite)

This step is completed by the PM directly in Productboard BEFORE engaging Claude.

**What the PM does:**
1. Reviews all raw customer insights for the feature/topic
2. For each insight, manually examines and determines which component(s) it relates to
3. Attaches/links each insight to the appropriate Productboard component or feature
4. Adds notes if needed to clarify the connection

**Output**: Insights now properly tagged/linked in Productboard

**Claude's role**: None in this step. This is manual PM work.

---

## Step 1: CSV Creation (PM Prerequisite)

This step is also completed by the PM before engaging Claude.

**What the PM does:**
1. Reviews all attached insights in Productboard
2. Copies insight text and URLs one by one
3. Creates a CSV with three columns: `INSIGHT_TEXT`, `PRODUCTBOARD_INSIGHT_URL`, `PRODUCTBOARD_FEATURE_URL`
4. Exports as CSV format
5. Uploads to `/temp/` folder

**Output**: `[feature-name]_insights.csv` ready for Claude analysis

**Claude's role**: None in this step. This is manual PM work.

---

## Step 2: Initial Categorization Analysis

**When User Provides CSV of Insights:**

1. **Read and analyze the CSV**
   - Extract all insight text
   - Note Productboard insight URLs (traceability)
   - Note associated feature URLs (if provided)

2. **Identify initial themes and patterns**
   - Group similar insights
   - Note conflicting or overlapping themes
   - Flag insights that don't clearly fit anywhere

3. **Recommend mutually exclusive categories**
   - Generate 5-8 initial categories
   - Each category should have a clear, customer-focused focus area
   - Write a brief description of what each category covers and what it DOES NOT cover
   - Ensure minimal overlap between categories

4. **Validate boundaries**
   - For each pair of similar categories, explicitly state the boundary:
     - "Category A (HOW) vs Category B (WHAT)" 
     - "Category A (User control) vs Category B (Admin control)"
   - If two categories seem redundant, flag this for the PM to decide

5. **Provide output:**
   ```markdown
   ## Recommended Categories for [Feature Name]
   
   ### Category 1: [Focus Area]
   - **Focus**: [What this solves]
   - **Does NOT include**: [Boundary definition]
   - **Insights count**: X
   - **Associated Productboard URLs**: [List]
   
   [Repeat for each category]
   
   ### Boundary Clarifications
   - **Category A vs B**: [Explains distinction]
   ```

---

## Step 4: Comprehensive Analysis Generation

**When User Provides Exported Insights for a Category:**

1. **Analyze the insights deeply**
   - Read all insights in context
   - Identify recurring themes and pain points
   - Note any conflicting perspectives
   - Extract specific examples and evidence

2. **Generate comprehensive analysis** with these sections:

   **Customer Problem:**
   - What is the specific pain customers are experiencing?
   - Include concrete examples from the insights
   - Quantify if possible (e.g., "X customers," "Y% reported")
   - Explain impact on their work

   **Product Gap:**
   - What capability is currently missing?
   - What's the current workaround (if any)?
   - Why is it insufficient?
   - Be specific (not vague)

   **User Stories** (5-8, varied):
   - "As a [role], I want [capability], so that [benefit]"
   - Cover different personas and use cases
   - Include both user and admin stories where relevant
   - Ground each story in specific insights where possible

   **Product Requirements:**
   - Break into logical groups (e.g., User-Level, Admin-Level, System-Level)
   - Make each requirement specific and testable
   - Prioritize if possible (must-have vs nice-to-have)
   - Include acceptance criteria where relevant

   **Potential Capabilities:**
   - What technical/product features would solve this?
   - List 5-8 concrete capabilities
   - Each capability should map to one or more requirements
   - Consider feasibility and scope

   **Potential Benefits:**
   - User/business benefits (separate these out)
   - Quantify where possible (e.g., "reduce support tickets by X%")
   - Link benefits back to customer problems identified

3. **Example output format:**
   ```markdown
   ## Feature Analysis: [Category Name]
   
   ### Customer Problem
   - [Description with examples]
   
   ### Product Gap
   - [Description with specifics]
   
   ### User Stories
   1. **As a** [role], **I want** [capability], **so that** [benefit]
   2. [Continue...]
   
   ### Product Requirements
   #### User-Level
   - [Requirement 1]
   - [Requirement 2]
   
   ### Potential Capabilities
   - [Capability 1 - how to solve]
   - [Capability 2 - how to solve]
   
   ### Potential Benefits
   - [Benefit 1 with impact]
   - [Benefit 2 with impact]
   ```

---

## Step 5: Iterative Refinement

**When User Reports Misalignment:**

1. **Understand the issue**
   - Ask: "Which specific customer problems don't fit this category?"
   - Ask: "What category would better address this?"

2. **Provide recommendations**
   - Review the insights that don't fit
   - Recommend which insights should move to which category
   - Explain why the move makes sense
   - Provide Productboard URLs for the insights to move

3. **Format**:
   ```markdown
   ## Suggested Refinement for [Category Name]
   
   **Issue**: [Description of what doesn't fit]
   
   **Recommendations**:
   - Move insight "[Text snippet]" ([URL]) to [Category Name]
     - Reason: [Explanation]
   - Keep insight "[Text snippet]" ([URL]) because: [Explanation]
   
   **Next Steps**:
   1. Reassign these insights in Productboard to the correct features
   2. Re-export all affected categories
   3. I'll regenerate analysis for those categories
   ```

---

## Step 6: Final Audit & Validation

**When User is Ready to Finalize:**

1. **Review all categories for**:
   - True mutual exclusivity (no insight in multiple categories)
   - Consistency in scope (some not too large, others too small)
   - Alignment with customer voice (language reflects actual pain points)
   - Boundary clarity (could someone definitively choose between categories?)

2. **Generate final audit report**:
   ```markdown
   ## Final Category Audit for [Feature Name]
   
   ### Mutual Exclusivity Check ✓
   - All insights are uniquely assigned to one category
   - No overlaps identified
   
   ### Boundary Clarity ✓
   - [Category A] vs [Category B]: [Clear distinction]
   
   ### Scope Balance ✓
   - Largest category: X insights
   - Smallest category: Y insights
   - Ratio acceptable: [Yes/No]
   
   ### Customer Voice Alignment ✓
   - Language reflects actual insights: [Validation]
   - All major pain points captured: [Validation]
   - No artificial or theoretical problems: [Validation]
   
   ### Ready for Next Steps? [Yes/No]
   ```

---

## General Guidelines

### Best Practices
- **Ask clarifying questions** when CSV or exports are ambiguous
- **Reference specific insights** when making recommendations (quote the insight text)
- **Include Productboard URLs** in all recommendations for traceability
- **Validate assumptions** (e.g., "Is this a user-level or admin-level problem?")
- **Challenge the PM** if categories seem forced or overlapping

### Common Pitfalls to Avoid
- Creating categories based on technical solutions instead of customer problems
- Over-engineering (too many categories with too few insights)
- Under-engineering (too few categories that are too broad)
- Ignoring outlier insights (don't just ignore them—ask where they belong)
- Creating categories that sound different but address the same problem

### When to Push Back
- If a PM wants to keep similar categories, ask them to articulate the boundary
- If an insight doesn't fit any category, ask if a new category is needed or if the existing categories need refinement
- If the number of insights in a category seems disproportionate, ask if it needs splitting

---

## Workflow Commands

When a user invokes this skill with these prompts, execute the corresponding step:

- **"Step 2: [CSV description]"** → Initial categorization analysis
- **"Step 4: [Category + exported insights]"** → Comprehensive analysis
- **"Step 5: Refine [Category]"** → Iterative refinement
- **"Step 6: Final audit"** → Validation and final report

**Note**: Steps 0 and 1 are manual PM work in Productboard—not Claude work. You engage starting at Step 2.

---

## Skill Integration

This skill works with other skills:
- **#create-prd** - Convert final categories into PRDs
- **#create-jira** - Create Jira tickets from final categories
- **#write-whats-new** - Announce new features to users
- **#extract-requirements** - Extract requirements from unstructured notes

After completing this skill, users typically move to one of these downstream skills.
