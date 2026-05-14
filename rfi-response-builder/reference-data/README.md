# Analyst RFI Reference Data

This folder contains all historical RFI answers and supporting materials for the Analyst RFI Autofill skill.

## Supported Markets

| Market Category | Key Product | Files |
|-----------------|-------------|-------|
| Digital Twin of an Organization (DTO) | SAP Signavio, LeanIX, WalkMe | QKS SPARK Matrix, Gartner surveys |
| Enterprise Architecture Tools (EA Tools) | SAP LeanIX | Gartner MQ 2025 |

## Folder Structure

```
reference-data/
├── README.md                   # This file
├── historical-answers/         # Previous RFI responses (PRIMARY SOURCE)
├── market-reports/             # Published analyst reports
└── supporting-docs/            # Vendor profiles, PR, demos
```

---

## historical-answers/

**Purpose**: Contains extracted text from previously filled RFI questionnaires. This is the PRIMARY source for autofilling new RFIs.

**Files** (ordered by priority - most recent first):

### DTO Market Files
| File | Year | Source | Priority |
|------|------|--------|----------|
| `2026_Gartner_DTO_Presurvey.txt` | 2026 | Gartner Pre-Survey | **Highest** |
| `2026_Gartner_Process_Intelligence_MQ.txt` | 2026 | Gartner MQ | **Highest** |
| `2025_QKS_SPARK_Matrix_RFI.txt` | 2025 | QKS Group | **Highest** |
| `2024_QKS_SPARK_Matrix_RFI.txt` | 2024 | QKS Group | High |
| `2024_Gartner_Market_Guide_Survey.txt` | 2024 | Gartner | High |
| `2023_QKS_SPARK_Matrix_RFI.txt` | 2023 | QKS Group | Medium |
| `2022_Gartner_Market_Guide_Survey.txt` | 2022 | Gartner | Low |
| `2021_QKS_SPARK_Matrix_RFI.txt` | 2021 | QKS Group | Low |

### EA Tools Market Files
| File | Year | Source | Priority |
|------|------|--------|----------|
| `2025_Gartner_EA_Tools_MQ.txt` | 2025 | Gartner MQ | **Highest** |

**Usage Rule**: Always start with the most recent year. Only use older years if the question doesn't exist in newer files.

---

## market-reports/

**Purpose**: Published analyst reports that provide context on market definitions, evaluation criteria, and SAP's positioning.

| File | Description |
|------|-------------|
| `2025_QKS_SPARK_Matrix_Report.txt` | QKS SPARK Matrix evaluation criteria and vendor profiles |
| `2024_QKS_SPARK_Matrix_Report.txt` | Previous year's evaluation for trend comparison |
| `2023_Gartner_DTO_Market_Guide.txt` | Gartner's DTO market definition and building blocks |

**Usage**: Reference for understanding how analysts evaluate DTO solutions. NOT for copying directly into answers.

---

## supporting-docs/

**Purpose**: Additional materials that support RFI responses with messaging, demos, and analysis.

| File | Description | Use For |
|------|-------------|---------|
| `SAP_Vendor_Profile_2025.txt` | Official SAP vendor profile from QKS | Company description, strengths, challenges |
| `RFI_Evolution_Analysis.txt` | Analysis of how RFI questions changed 2024→2025 | Predicting new question types |
| `SAP_PR_Messaging_2025.txt` | Press release and analyst quotes | Marketing-approved language |
| `DTO_Demo_Resources.txt` | Links to DTO demos and recordings | Answering demo-related questions |

---

## Adding New Files

When adding new RFI responses or reference materials:

1. **Name files with year prefix**: `YYYY_Source_Description.txt`
2. **Extract to plain text**: Use Python/pandas to extract from Excel
3. **Preserve structure**: Include row numbers and column separators
4. **Update RESEARCH.md**: Document any new question types or patterns found

### Extraction Command Example

```python
import pandas as pd

xls = pd.ExcelFile('new_rfi.xlsx')
with open('YYYY_Source_RFI.txt', 'w', encoding='utf-8') as f:
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        f.write(f"\n{'='*80}\nSHEET: {sheet}\n{'='*80}\n\n")
        for i, row in df.iterrows():
            vals = [str(v).strip() for v in row.values if pd.notna(v) and str(v).strip()]
            if vals:
                f.write(f"ROW {i}: {' | '.join(vals)}\n")
```

---

## File Format Convention

All extracted files follow this format:

```
================================================================================
SHEET: Sheet Name
================================================================================

ROW 0: Column A Value | Column B Value | Column C Value
ROW 1: Question | Sub-question | Answer
...
```

This makes it easy to:
- Search for specific questions (grep "question text")
- Identify which row contains an answer
- Understand the original Excel structure
