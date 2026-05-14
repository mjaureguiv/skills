---
name: rfi-response-builder
description: "Build structured RFI responses for analyst questionnaires (QKS SPARK Matrix, Gartner MQ/Market Guide) for SAP solutions. Covers: Digital Twin of an Organization (DTO), Enterprise Architecture Tools (EA Tools/LeanIX). Use when user has an Excel RFI to fill, mentions 'RFI', 'analyst questionnaire', 'SPARK Matrix', 'Gartner survey', 'DTO', 'EA Tools', or 'LeanIX'."
user-invokable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
---

# RFI Response Builder

Build structured RFI responses for analyst questionnaires covering SAP solution portfolios.

## Supported Market Categories

| Market Category | Products Covered | Analysts |
|-----------------|------------------|----------|
| **Digital Twin of an Organization (DTO)** | SAP Signavio, SAP LeanIX, WalkMe | QKS SPARK Matrix, Gartner |
| **Enterprise Architecture Tools (EA Tools)** | SAP LeanIX | Gartner MQ |

## What This Skill Does

When you receive an RFI Excel file from an analyst (QKS Group, Gartner, Forrester, etc.), this skill helps you fill it by:

1. Understanding the questionnaire structure and which columns need answers
2. Matching questions to historical responses from previous years
3. Ensuring answers are current (product names, versions, roadmap items)
4. Preserving the exact Excel structure required by the analyst

**Critical**: This skill fills RFIs **without destroying the file structure**. The analyst's Excel format must be preserved exactly.

---

## How to Use This Skill

```
/rfi-response-builder [path-to-excel-file]
```

Or just describe what you need:
```
Fill this RFI: @path/to/questionnaire.xlsx
```

---

## MANDATORY WORKFLOW

This skill follows a strict 3-phase workflow. **Do not skip phases.**

### Phase 1: Research & Target File Analysis

**Before doing anything else**, understand both your knowledge base AND the target file.

#### Step 1.1: Refresh Knowledge Base

1. **Read the research document**: `skills/rfi-response-builder/RESEARCH.md`
   - This contains the complete knowledge base of how RFIs work
   - Includes boilerplate responses, answer patterns, product capabilities

2. **Check for new reference files**: Scan `skills/rfi-response-builder/reference-data/` for any new files
   - If new files exist that aren't reflected in RESEARCH.md, analyze them
   - Update RESEARCH.md with new findings (new questions, new answer patterns, etc.)

3. **Identify the most recent historical answers** for this type of RFI:
   - QKS SPARK Matrix → Use 2025 as primary, 2024 as fallback
   - Gartner → Use 2026 as primary, 2024 as fallback

#### Step 1.2: Deep Analysis of Target File

**Thoroughly analyze the RFI file the user wants to fill.** Use Python to inspect:

```python
import pandas as pd
from openpyxl import load_workbook

# 1. Get basic file info
xls = pd.ExcelFile(target_file)
print(f"Sheets: {xls.sheet_names}")

# 2. For EACH sheet, analyze column structure
for sheet in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet, header=None)
    print(f"\nSheet: {sheet}")
    print(f"  Dimensions: {df.shape[0]} rows x {df.shape[1]} columns")

    # Show first 10-15 rows to understand structure
    for row in range(min(15, len(df))):
        for col in range(df.shape[1]):
            val = df.iloc[row, col]
            if pd.notna(val):
                print(f"  [{row},{col}]: {str(val)[:60]}...")
```

#### Step 1.3: Present Target File Analysis to User

**CRITICAL: Present your analysis and ASK THE USER TO CONFIRM before proceeding.**

Present the following analysis:

```
═══════════════════════════════════════════════════════════════════════════════
TARGET FILE ANALYSIS
═══════════════════════════════════════════════════════════════════════════════

FILE: [filename.xlsx]
TYPE: [QKS SPARK Matrix / Gartner MQ / Gartner Pre-Survey / Other]
ANALYST FIRM: [QKS Group / Gartner / Forrester / etc.]

───────────────────────────────────────────────────────────────────────────────
SHEET-BY-SHEET STRUCTURE
───────────────────────────────────────────────────────────────────────────────

SHEET 1: "General Questions"
  • Rows: X total (questions appear in rows Y-Z)
  • Column structure detected:
    - Column A: [Section headers / Row labels]
    - Column B: [Question category / Sub-section]
    - Column C: [Question text / Sub-question]
    - Column D: [ANSWER COLUMN ← I will fill this]
    - Column E: [Remarks - will NOT fill]
    - Column F: [Roadmap info - will NOT fill]
  • Sample question from Row 15:
    Q: "What is your revenue for 2024?"
    Current answer cell (D15): [empty / pre-filled value]

SHEET 2: "Criteria Specific Questions"
  • Rows: X total
  • Column structure detected:
    - Column A: [Question number]
    - Column B: [Question + Answer combined in same cell]
  • Note: This sheet appears to have [different structure / merged Q&A]

[Continue for all sheets...]

───────────────────────────────────────────────────────────────────────────────
MY UNDERSTANDING
───────────────────────────────────────────────────────────────────────────────

1. This appears to be a [YEAR] [TYPE] RFI from [ANALYST FIRM]
2. I will fill answers in: [Column D for Sheet 1, Column B for Sheet 2, etc.]
3. I will NOT touch: [Columns A, B, C (questions), E, F (remarks)]
4. Total questions to fill: approximately [X]
5. Similar to our historical file: [2025_QKS_SPARK_Matrix_RFI.txt]

───────────────────────────────────────────────────────────────────────────────
PLEASE CONFIRM
───────────────────────────────────────────────────────────────────────────────

Before I proceed to Phase 2 (planning which answers to use), please confirm:

1. ✓ Is my understanding of the file structure correct?
2. ✓ Did I identify the correct ANSWER column for each sheet?
3. ✓ Are there any columns I should NOT touch that I missed?
4. ✓ Any special instructions for this particular RFI?

Type "confirmed" or tell me what I got wrong.
```

**DO NOT proceed to Phase 2 until the user confirms your file analysis is correct.**

### Phase 2: Answer Mapping & Fill Plan

**After user confirms the file structure analysis**, create the fill plan.

#### Step 2.1: Map Questions to Historical Answers

For each question in the target file:

1. **Search historical answers** (most recent first):
   - 2025/2026 files → direct match
   - 2024 files → match but verify product names
   - 2023 and older → use as inspiration, rewrite

2. **Categorize each question**:
   - **EXACT_MATCH**: Question exists in historical file with same wording
   - **SIMILAR_MATCH**: Question is similar, answer can be adapted
   - **BOILERPLATE**: Revenue/customer count → use standard non-disclosure
   - **NEW_QUESTION**: Not seen before, needs custom answer
   - **SKIP**: Question unclear or not applicable

#### Step 2.2: Save Complete Mapping to MD File

**CRITICAL: Before presenting the fill plan, save the complete question→answer mapping to a reviewable file.**

Create a mapping file with all proposed answers:

```
Filename: RFI_MAPPING_[original-filename]_[timestamp].md
Location: Same folder as the original RFI file
```

The mapping file must contain:

```markdown
# RFI Answer Mapping

**File**: [filename.xlsx]
**Date**: [YYYY-MM-DD]

---

## Instructions

1. Review each proposed change below
2. Edit answers directly in this file if needed
3. Mark any row with `[SKIP]` to leave unchanged
4. Type "mapping approved" when done

---

# SHEET 1: [Sheet Name]

## Capability/Question 1: [Full question text from the RFI]

### Cell C1 (SAP LeanIX)
**Question**: [Repeat the capability/question here so it's clear what this cell answers]
**CURRENT:**
```
[What's currently in the cell, or "EMPTY" if blank]
```
**PROPOSED:**
```
[What I want to put there]
```
**WHY:** [Source/rationale - e.g., "From 2026 Gartner Pre-Survey ROW 33"]

---

### Cell D1 (SAP Signavio)
**Question**: [Repeat the capability/question here]
**CURRENT:** EMPTY
**PROPOSED:**
```
[Proposed content]
```
**WHY:** [Source/rationale]

---

### Cell E1 (WalkMe)
**Question**: [Repeat the capability/question here]
**CURRENT:** EMPTY
**PROPOSED:**
```
[Proposed content]
```
**WHY:** [Source/rationale]

---

## Capability/Question 2: [Full question text]

### Cell C2 (SAP LeanIX)
**Question**: [Repeat: What capability/question is this cell answering?]
**CURRENT:**
```
[Current value with typos highlighted if any]
```
**PROPOSED:**
```
[Corrected/improved value]
```
**WHY:** Fixed typo: "innitiatives" → "initiatives". Added AI Agent Hub.

---

[Continue for ALL cells...]

---

# Summary

| Type | Count |
|------|-------|
| Typo fixes | X |
| Improvements | Y |
| New content | Z |
| **Total** | **N** |

---

**Type "mapping approved" when ready.**
```

**KEY FORMATTING RULE**: For every cell, always include the **Question** field that repeats what capability/question this cell is answering. This makes it crystal clear to the reviewer what each proposed answer is for, especially when there are multiple cells (C, D, E) under the same capability.
```

**Tell the user where to find this file AND display the full content directly:**

```
═══════════════════════════════════════════════════════════════════════════════
MAPPING FILE CREATED
═══════════════════════════════════════════════════════════════════════════════

I've saved the complete question→answer mapping for your review:

📄 [path/to/RFI_MAPPING_filename_2026-03-04.md]
```

**IMPORTANT: Always display the full mapping file content directly in the conversation.**

Use the Read tool to show the user the complete mapping file content so they can review it without having to open a separate file. This makes it easier for the user to see exactly what will be filled.

**Also open the file in VS Code** so the user can edit it easily:

```bash
code "[path/to/RFI_MAPPING_filename_2026-03-04.md]"
```

```
═══════════════════════════════════════════════════════════════════════════════
FULL MAPPING FILE CONTENT
═══════════════════════════════════════════════════════════════════════════════

[Display the entire contents of the mapping MD file here]
```

After displaying the content, remind the user:

```
───────────────────────────────────────────────────────────────────────────────
REVIEW OPTIONS
───────────────────────────────────────────────────────────────────────────────

You can:
• Review the mapping above
• Edit the file directly at: [path/to/mapping.md]
• Add comments using <!-- comment --> syntax
• Mark answers to skip by changing status to [SKIP]

Once you've reviewed (and optionally edited the file), type "mapping approved"
and I will proceed to fill the Excel with your approved answers.
```

#### Step 2.3: Present Fill Plan Summary to User

After showing the full mapping file, also provide a summary:

```
═══════════════════════════════════════════════════════════════════════════════
FILL PLAN SUMMARY
═══════════════════════════════════════════════════════════════════════════════

STATISTICS:
• Total questions mapped: 85
• Exact matches from 2025: 62 (73%)
• Similar matches from 2024: 15 (18%)
• Boilerplate (non-disclosure): 5 (6%)
• New questions needing review: 3 (3%)

───────────────────────────────────────────────────────────────────────────────
ITEMS REQUIRING YOUR ATTENTION
───────────────────────────────────────────────────────────────────────────────

3 questions marked [NEEDS REVIEW] in the mapping file:
• Row 89: AI Agent Governance (new question - drafted answer)
• Row 134: Sustainability/ESG (new question - drafted answer)
• Row 201: Data residency compliance (answer updated from 2024)

───────────────────────────────────────────────────────────────────────────────
NEXT STEPS
───────────────────────────────────────────────────────────────────────────────

1. Open the mapping file: [path/to/RFI_MAPPING_filename_2026-03-04.md]
2. Review all proposed answers (especially those marked [NEEDS REVIEW])
3. Edit any answers that need changes directly in the file
4. When done, type "mapping approved"

I will NOT fill the Excel until you approve the mapping.
```

**DO NOT proceed to Phase 3 until the user types "mapping approved".**

#### Step 2.4: Re-read Mapping File After Approval

When the user approves the mapping:

1. **Re-read the mapping MD file** to pick up any edits the user made
2. **Parse the edited answers** from the markdown format
3. **Identify any answers marked [SKIP]** - do not fill these
4. **Confirm the changes detected**:

```
═══════════════════════════════════════════════════════════════════════════════
MAPPING APPROVED - CHANGES DETECTED
═══════════════════════════════════════════════════════════════════════════════

I've read your updated mapping file. Changes detected:
• Row 89: Answer edited (you modified the AI governance response)
• Row 134: Marked [SKIP] (will leave blank)
• Row 201: No changes (using original proposal)

Proceeding to Phase 3: Execution...
```

### Phase 3: Execution

**Only after user confirms the plan**, fill the RFI:

1. **Use Python with openpyxl** to preserve Excel formatting:
   ```python
   from openpyxl import load_workbook

   # Load WITHOUT data_only to preserve formulas
   wb = load_workbook(filename, data_only=False)

   # Fill ONLY the answer column
   # Do NOT modify question columns, formatting, or structure
   ```

2. **Fill answers following these rules**:
   - Use most recent year's answer first (2025/2026)
   - Update product names: "Signavio" → "SAP Signavio"
   - Update version numbers to current
   - Check roadmap items - remove if already GA, update dates
   - Respect character limits

3. **Save to a NEW file** (never overwrite the original):
   ```
   original: RFI_Questionnaire.xlsx
   filled:   RFI_Questionnaire_AI_filled.xlsx
   ```

   **CRITICAL: Output file location rules:**
   - **ALWAYS save filled files in the SAME folder as the original file**
   - **NEVER save output files inside this skill's folder or anywhere in the git repo**
   - The mapping MD file should also go next to the original file
   - Example: If original is at `C:/Users/folder/RFI.xlsx`, save to `C:/Users/folder/RFI_AI_filled.xlsx`

4. **Generate a summary report**:
   - Questions filled: X
   - Answers from 2025: Y
   - Answers from 2024: Z
   - Boilerplate responses: N
   - Custom/new answers: M
   - Skipped (unclear): K

---

## Excel Column Rules

### CRITICAL: Do NOT Destroy File Structure

The analyst's Excel files have specific structures. You must:
- **ONLY fill the answer column** (usually "Your Response" or Column C/D)
- **NEVER modify** question text, row numbers, formatting, formulas
- **PRESERVE** merged cells, colors, borders, column widths
- **RESPECT** hidden rows/columns

### Column Type Reference

| Column Type | Purpose | Fill? |
|-------------|---------|-------|
| Question/Label | Analyst's question text | NO - read only |
| Answer Guidance | How to answer | NO - read only |
| Character Limit | Max chars allowed | NO - respect as constraint |
| **Your Response** | **The actual answer** | **YES - fill this** |
| Additional Info | Supporting details | MAYBE - if requested |
| Remarks/Notes | Internal comments | NO - leave empty |
| Status | Completion tracking | NO - analyst fills this |

### QKS SPARK Matrix Typical Structure

```
Column A: Row labels / Category headers
Column B: Question / Sub-question text
Column C: PRIMARY ANSWER COLUMN ← Fill this
Column D: Remarks / USP notes (optional context)
Column E: Roadmap information (optional)
```

### Gartner MQ Typical Structure

```
Column A-E: Question metadata (status, number, title, guidance, char limit)
Column F/G: "Your Response" ← Fill this
Column H+: Additional info, subsection, dates (context only)
```

---

## Answer Priority Rules

When matching questions to historical answers:

| Priority | Source | Usage |
|----------|--------|-------|
| 1 | 2025/2026 RFI answers | Primary source - use directly |
| 2 | 2024 RFI answers | Verify product names are current |
| 3 | 2023 RFI answers | Rewrite with current info |
| 4 | Market reports | For context/messaging only |
| 5 | New answer | When no match exists |

### Boilerplate Triggers

Use standard boilerplate for these question types:

| Question About | Boilerplate |
|----------------|-------------|
| Revenue numbers | Financial non-disclosure |
| Customer count | Financial non-disclosure |
| Growth rates | Financial non-disclosure |
| Market share | Financial non-disclosure |

---

## Reference Data Structure

```
skills/rfi-response-builder/
├── SKILL.md                    # This file
├── RESEARCH.md                 # Main knowledge base (READ FIRST)
└── reference-data/
    ├── historical-answers/     # Previous RFI responses by year
    │   ├── 2026_Gartner_*.txt  # Most recent - highest priority
    │   ├── 2025_QKS_*.txt
    │   ├── 2024_*.txt
    │   ├── 2023_*.txt
    │   ├── 2022_*.txt
    │   └── 2021_*.txt          # Oldest - lowest priority
    ├── market-reports/         # Analyst reports for context
    │   ├── 2025_QKS_SPARK_Matrix_Report.txt
    │   ├── 2024_QKS_SPARK_Matrix_Report.txt
    │   └── 2023_Gartner_DTO_Market_Guide.txt
    └── supporting-docs/        # Vendor profiles, PR messaging
        ├── SAP_Vendor_Profile_2025.txt
        ├── RFI_Evolution_Analysis.txt
        ├── SAP_PR_Messaging_2025.txt
        └── DTO_Demo_Resources.txt
```

---

## Product Reference (Current as of 2026)

### SAP DTO Portfolio

| Product | Full Name | Acquired |
|---------|-----------|----------|
| SAP Signavio | SAP Signavio Process Transformation Suite | 2021 |
| SAP LeanIX | SAP LeanIX Enterprise Architecture Management | 2023 |
| WalkMe | WalkMe Digital Adoption Platform | 2024 |

### Key Capability Mapping

| Capability Area | Primary Product |
|-----------------|-----------------|
| Process Mining | SAP Signavio Process Intelligence |
| Process Modeling | SAP Signavio Process Manager |
| Enterprise Architecture | SAP LeanIX |
| Digital Adoption | WalkMe |
| AI/Copilot | SAP Joule, SAP Business AI |
| Automation | SAP Build |
| Data Integration | SAP BTP, SAP Integration Suite |

---

## Error Handling

### If Excel file won't open
- Check if file is password protected
- Check if file is corrupted
- Ask user to provide an unlocked version

### If column structure is unclear
- Ask user to confirm which column should contain answers
- Never guess - wrong column = destroyed file

### If question doesn't match any historical answer
- Flag for user review
- Suggest similar questions from historical data
- Offer to draft a new answer based on product capabilities

### If character limit is exceeded
- Truncate intelligently (complete sentences)
- Flag which answers were truncated
- Offer expanded version for user reference

---

## Quality Checklist (Before Delivering)

- [ ] Original file structure preserved
- [ ] Only answer column modified
- [ ] All answers from most recent year possible
- [ ] Product names are current (SAP Signavio, not Signavio)
- [ ] No outdated roadmap items (check if features are now GA)
- [ ] Financial questions use non-disclosure boilerplate
- [ ] Character limits respected
- [ ] File saved with new name (not overwritten)
- [ ] Summary report generated

---

## Example Session

**User**: Fill this RFI: @Downloads/QKS_DTO_RFI_2026.xlsx

**Assistant**:
```
═══════════════════════════════════════════════════════════════════════════════
PHASE 1: RESEARCH & TARGET FILE ANALYSIS
═══════════════════════════════════════════════════════════════════════════════

Step 1.1: Knowledge base refreshed
✓ Read RESEARCH.md
✓ Checked reference-data/ for updates
✓ Most recent source: 2025_QKS_SPARK_Matrix_RFI.txt

Step 1.2: Analyzing your target file...

═══════════════════════════════════════════════════════════════════════════════
TARGET FILE ANALYSIS
═══════════════════════════════════════════════════════════════════════════════

FILE: QKS_DTO_RFI_2026.xlsx
TYPE: QKS SPARK Matrix RFI
ANALYST FIRM: QKS Group

───────────────────────────────────────────────────────────────────────────────
SHEET-BY-SHEET STRUCTURE
───────────────────────────────────────────────────────────────────────────────

SHEET 1: "General Questions" (319 rows x 6 columns)
  • Column A: Section headers (e.g., "1. REVENUE DETAILS")
  • Column B: Category labels (e.g., "1a. Overall")
  • Column C: Question text (e.g., "2024", "Growth from 2023")
  • Column D: [ANSWER COLUMN ← I will fill this]
  • Column E: Remarks/USP notes (will NOT fill)
  • Column F: Roadmap info (will NOT fill)

SHEET 2: "Criteria Specific Questions" (41 rows x 2 columns)
  • Column A: Question number
  • Column B: Question + Answer combined
  • Note: Different structure - answers are in Column B

SHEET 3: "Technology Excellence Criteria" (11 rows)
  • Scoring weights - READ ONLY, will not modify

SHEET 4: "SPARK Matrix Criteria" (16 rows)
  • Customer impact weights - READ ONLY, will not modify

───────────────────────────────────────────────────────────────────────────────
MY UNDERSTANDING
───────────────────────────────────────────────────────────────────────────────

1. This is a 2026 QKS SPARK Matrix RFI
2. I will fill answers in: Column D (Sheet 1), Column B (Sheet 2)
3. I will NOT touch: Columns A, C, E, F (Sheet 1), Column A (Sheet 2)
4. I will NOT modify Sheets 3-4 (scoring criteria)
5. Total questions to fill: approximately 147
6. Similar to: 2025_QKS_SPARK_Matrix_RFI.txt

───────────────────────────────────────────────────────────────────────────────
PLEASE CONFIRM FILE STRUCTURE
───────────────────────────────────────────────────────────────────────────────

Is my analysis correct? Type "confirmed" or tell me what I got wrong.
```

**User**: confirmed

**Assistant**:
```
═══════════════════════════════════════════════════════════════════════════════
PHASE 2: ANSWER MAPPING & FILL PLAN
═══════════════════════════════════════════════════════════════════════════════

Mapping questions to historical answers...

═══════════════════════════════════════════════════════════════════════════════
MAPPING FILE CREATED
═══════════════════════════════════════════════════════════════════════════════

I've saved the complete question→answer mapping for your review:

📄 Downloads/RFI_MAPPING_QKS_DTO_RFI_2026_2026-03-04.md

This file contains ALL 147 proposed answers. You can:
• Review each answer
• Edit answers directly in the file
• Add comments using <!-- comment --> syntax
• Mark answers to skip by changing status to [SKIP]

═══════════════════════════════════════════════════════════════════════════════
FILL PLAN SUMMARY
═══════════════════════════════════════════════════════════════════════════════

STATISTICS:
• Total questions mapped: 147
• Exact matches from 2025: 118 (80%)
• Similar matches from 2024: 21 (14%)
• Boilerplate (non-disclosure): 6 (4%)
• New questions needing review: 2 (2%)

───────────────────────────────────────────────────────────────────────────────
ITEMS REQUIRING YOUR ATTENTION
───────────────────────────────────────────────────────────────────────────────

2 questions marked [NEEDS REVIEW] in the mapping file:
• Row 89: AI Agent Governance (new question - drafted answer)
• Row 134: Sustainability/ESG (new question - drafted answer)

───────────────────────────────────────────────────────────────────────────────
NEXT STEPS
───────────────────────────────────────────────────────────────────────────────

1. Open the mapping file: Downloads/RFI_MAPPING_QKS_DTO_RFI_2026_2026-03-04.md
2. Review all proposed answers (especially those marked [NEEDS REVIEW])
3. Edit any answers that need changes directly in the file
4. When done, type "mapping approved"

I will NOT fill the Excel until you approve the mapping.
```

**User**: mapping approved

**Assistant**:
```
═══════════════════════════════════════════════════════════════════════════════
MAPPING APPROVED - READING YOUR CHANGES
═══════════════════════════════════════════════════════════════════════════════

Reading updated mapping file...

Changes detected:
• Row 89: Answer edited (you modified the AI governance response)
• Row 134: Marked [SKIP] (will leave blank)
• All other answers: No changes

═══════════════════════════════════════════════════════════════════════════════
PHASE 3: EXECUTION
═══════════════════════════════════════════════════════════════════════════════

Filling RFI with your approved answers...

✓ Loaded workbook (formatting preserved)
✓ Filled Sheet 1 "General Questions": 138 answers
✓ Filled Sheet 2 "Criteria Specific": 8 answers
✓ Skipped 1 answer marked [SKIP]
✓ Skipped Sheets 3-4 (scoring criteria - read only)
✓ Saved to: Downloads/QKS_DTO_RFI_2026_AI_filled.xlsx

───────────────────────────────────────────────────────────────────────────────
SUMMARY
───────────────────────────────────────────────────────────────────────────────

• Answers from 2025: 118
• Answers from 2024 (updated product names): 21
• Boilerplate responses: 6
• User-edited answers: 1 (Row 89)
• Skipped by user: 1 (Row 134)

───────────────────────────────────────────────────────────────────────────────

File ready at: Downloads/QKS_DTO_RFI_2026_AI_filled.xlsx
Mapping file preserved at: Downloads/RFI_MAPPING_QKS_DTO_RFI_2026_2026-03-04.md
```
