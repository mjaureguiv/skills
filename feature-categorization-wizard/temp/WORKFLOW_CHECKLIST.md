# Feature Categorization Workflow Checklist

Use this checklist to guide yourself through the feature categorization wizard workflow.

---

## Step 0: Manual Insight Attachment in Productboard

**This is manual work in Productboard—Claude will NOT help with this step**

- [ ] Go to Productboard and find all raw insights for your feature/topic
- [ ] Review each insight individually
- [ ] For each insight, identify which Productboard component or feature it relates to
- [ ] Attach/link the insight to that component (use Productboard's linking feature)
- [ ] Add notes if needed to clarify why it belongs to that component
- [ ] Repeat for all insights
- [ ] Validate that all insights are now linked to appropriate components

---

## Step 1: Create CSV from Productboard Data

**This is manual data collection—Claude will NOT help with this step**

- [ ] Open a spreadsheet application (Excel, Google Sheets, etc.)
- [ ] Create three columns: `INSIGHT_TEXT`, `PRODUCTBOARD_INSIGHT_URL`, `PRODUCTBOARD_FEATURE_URL`
- [ ] Go to Productboard and review the attached insights
- [ ] For each insight:
  - [ ] Copy the full insight text (paste into INSIGHT_TEXT column)
  - [ ] Copy the insight URL from Productboard (paste into PRODUCTBOARD_INSIGHT_URL column)
  - [ ] Copy the feature/component URL it's attached to (paste into PRODUCTBOARD_FEATURE_URL column)
- [ ] Continue for all insights (target: 15-50 insights for good sample size)
- [ ] Save the spreadsheet as CSV format: `[feature-name]_insights.csv`
- [ ] Upload to: `skills/feature-categorization-wizard/temp/[feature-name]_insights.csv`
- [ ] Validate the CSV has all three columns and proper formatting

**Checklist Item - Now ready for Claude:**
```
Copy this into a Claude prompt:

#feature-categorization-wizard Step 2

I've completed manual attachment and CSV creation for the [FEATURE_NAME] feature.

I've prepared a CSV with [X] customer insights: 
`skills/feature-categorization-wizard/temp/[filename].csv`

Please analyze these insights and generate 5-8 mutually exclusive categories with clear focus areas and boundaries.
```

---

## Step 2: AI-Assisted Categorization

- [ ] Go to Productboard and find the feature/topic area
- [ ] Export all customer insights related to this feature
- [ ] For each insight, copy:
  - [ ] Full insight text
  - [ ] Productboard insight URL
  - [ ] Associated feature URL (or leave blank if unsure)
- [ ] Create a CSV file with three columns: `INSIGHT_TEXT`, `PRODUCTBOARD_INSIGHT_URL`, `PRODUCTBOARD_FEATURE_URL`
- [ ] Use the template at: `skills/feature-categorization-wizard/temp/TEMPLATE_insights.csv`
- [ ] Save your CSV as: `skills/feature-categorization-wizard/temp/[feature-name]_insights.csv`
- [ ] Validate that you have 15-50 insights (good sample size for categorization)

**Checklist Item:**
```
Copy this into a Claude prompt:

#feature-categorization-wizard

I'm starting Step 2 for the [FEATURE_NAME] feature.

I've prepared a CSV with [X] customer insights: 
`skills/feature-categorization-wizard/temp/[filename].csv`

Please analyze these insights and generate 5-8 mutually exclusive categories with clear focus areas and boundaries.
```

---

## Step 2: AI-Assisted Categorization

- [ ] Invoke skill with Phase 2 prompt above
- [ ] Review the generated categories
  - [ ] Do the focus areas make sense?
  - [ ] Are boundaries clear (no overlap)?
  - [ ] Are there any insights that don't fit?
  - [ ] Do the categories reflect customer problems, not technical features?
- [ ] Document any questions or concerns
- [ ] Ask Claude for clarification if needed:
  ```
  I'm not sure about the boundary between [Category A] and [Category B].
  Can you clarify what distinguishes them?
  ```
- [ ] When satisfied, save Claude's categorization output to: `skills/feature-categorization-wizard/temp/[feature-name]_categories_v1.md`

---

## Step 3: Manual Review & Assignment in Productboard

- [ ] Open Productboard in a separate browser tab/window
- [ ] For each category Claude generated:
  - [ ] Find the corresponding feature in Productboard (or create one if new)
  - [ ] Review the focus area description
  - [ ] Go through each insight listed for that category
  - [ ] Assign the insight to the feature in Productboard
  - [ ] Add the category name and focus area to the feature description if needed
- [ ] When assigning insights, validate:
  - [ ] Does this insight clearly belong here?
  - [ ] Is there any overlap with other categories?
  - [ ] If unsure, flag it for review in Phase 5
- [ ] Save notes on any insights that felt misaligned
- [ ] Mark Step 3 complete

---

## Step 4: Export & Analysis

- [ ] For each category/feature you created:
  - [ ] Go to Productboard
  - [ ] Select the feature
  - [ ] Click "Export Insights"
  - [ ] Copy all insights for that feature
- [ ] Create a CSV or text file with the exported insights for each category
- [ ] Save to: `skills/feature-categorization-wizard/temp/[feature-name]_[category-name]_insights.csv`
- [ ] For each category, invoke Claude with:
  ```
  #feature-categorization-wizard Step 4
  
  **Category**: [Category Name]
  **Focus Area**: [Description]
  
  Here are the exported insights for this category:
  
  [Paste insights]
  
  Please generate comprehensive analysis:
  1. Customer Problem
  2. Product Gap
  3. User Stories (5-8)
  4. Product Requirements (detailed)
  5. Potential Capabilities (5-8)
  6. Potential Benefits
  ```
- [ ] Review each analysis output
- [ ] Save to: `skills/feature-categorization-wizard/temp/[feature-name]_analysis_[category-name].md`
- [ ] Mark Step 4 complete

---

## Step 5: Iterative Refinement (Repeat as needed)

**Refinement Cycle:**

- [ ] Review the analysis for each category
- [ ] Ask yourself for each: "Do the customer problems really align with the focus area?"
- [ ] If NOT aligned:
  - [ ] Note which insights/problems don't align
  - [ ] Ask Claude:
    ```
    #feature-categorization-wizard Step 5 Refinement
    
    **Issue with Category [Name]**: The analysis shows [specific problem], 
    but the focus area was [expected focus]. These don't align.
    
    Which insights should potentially move to a different category?
    Provide the insight text and Productboard URLs.
    ```
  - [ ] Review Claude's recommendations
  - [ ] Update assignments in Productboard
  - [ ] Re-export insights for affected categories
  - [ ] Ask Claude to regenerate analysis for those categories
  - [ ] Score the alignment: 1=poor, 5=excellent
  - [ ] If score < 4, continue refinement. If > 4, proceed to Phase 6

**Refinement Acceptance Criteria:**
- [ ] All customer problems clearly relate to the category focus area
- [ ] No insight feels "forced" into the category
- [ ] Boundaries between categories are clear and defensible
- [ ] User stories reflect actual use cases, not theoretical ones
- [ ] Product requirements are specific and testable

---

## Step 6: Final Audit & Output

- [ ] Ask Claude to perform final audit:
  ```
  #feature-categorization-wizard Step 6
  
  I'm ready for final validation. Here are my [X] categories:
  
  1. [Category Name]: [Focus Area]
  2. [Category Name]: [Focus Area]
  ... 
  
  Please perform a final audit to ensure:
  - Mutual exclusivity (no insight in multiple categories)
  - Boundary clarity (clear distinction between categories)
  - Scope balance (no category too large or small)
  - Customer voice alignment (reflects real problems, not theory)
  ```
- [ ] Review audit report
- [ ] Make any final adjustments recommended
- [ ] Save audit report to: `skills/feature-categorization-wizard/temp/[feature-name]_final_audit.md`
- [ ] Create final category map document:
  - [ ] List all categories
  - [ ] For each: focus area, number of insights, key URLs
  - [ ] Document boundaries explicitly
  - [ ] Save to: `skills/feature-categorization-wizard/temp/[feature-name]_category_map.md`

---

## Step 7: Next Steps (Choose One)

Now that you have categorized features with comprehensive analysis, you can:

- [ ] **Create PRDs**
  ```
  #create-prd
  Create a PRD for the [Category Name] feature.
  Use this analysis: [Copy analysis from Phase 4]
  ```

- [ ] **Create Jira Tickets**
  ```
  #create-jira
  Create Jira tickets from these categories: [List categories]
  Reference the analysis: [Copy analysis]
  ```

- [ ] **Build Roadmap**
  ```
  #generate-roadmap
  Generate an ICE-scored roadmap from these categories: [List]
  Use this scoring criteria: [Define]
  ```

- [ ] **Announce to Users**
  ```
  #write-whats-new
  Create a user announcement for these new features: [List]
  Tone: [Professional/Casual/Technical]
  ```

---

## Quick Tips

- **Stuck on a refinement?** Frame it as: "This insight talks about [problem], but the category is about [focus]. Where should it go?"
- **Too many categories?** Merge related ones and re-analyze
- **Categories feel forced?** That's a signal—ask Claude to challenge the grouping
- **Insights not fitting anywhere?** That might be a new category—ask Claude
- **Running out of energy?** Save your work and come back later. Note what round of refinement you're on.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| CSV won't load | Verify it's UTF-8 encoded, check for quote marks in text |
| Claude and I disagree on category | Ask Claude to defend the grouping—don't force agreement |
| Insights keep moving between categories | The boundary isn't clear enough—ask Claude to define it |
| Categories feel too similar | They might need merging—ask Claude if they're really distinct |
| Analysis doesn't match customer problems | Go back to Phase 5 and refine—don't proceed to Phase 6 |
| Too many insights for one category | Split into two categories and re-analyze |

