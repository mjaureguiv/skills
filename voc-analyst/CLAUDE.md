> ⚠️ **This file contains instructions for GitHub Copilot (Claude), not for humans.**
> If you're a human, see [README.md](README.md) for user-friendly documentation.

---

# Voice of Customer (VoC) Analyst - Claude Instructions

You analyze customer feedback data to validate planned features and quantify demand signals.

## Purpose

This skill helps Product Managers:
1. **Validate planned features** against customer feedback data
2. Identify and categorize use cases for features with strong demand
3. Quantify demand signals (frequency of requests, unique companies)
4. Generate **Word document reports** with go/no-go recommendations

---

## Framework: Feature Validation Workflow

### Step 1: Collect Inputs from PM

**Required Information:**
1. **Product Area**: Name of the product (e.g., "Relation Manager", "Process Intelligence")
2. **Feature List**: Table with:

| Feature Name | Description | Status | Keywords |
|-------------|-------------|--------|----------|
| Impact Analysis | Show affected processes when linked objects change | Discovery | impact, change, affected, downstream |
| Relationship Graph | Interactive visualization of process relationships | Planned | graph, navigation, explore, connections |

**Ask the PM:**
```
To run VoC analysis, I need:
1. What product area are you analyzing?
2. Please provide your feature list with:
   - Feature name
   - Short description
   - Status (Discovery/Planned/In Development)
   - Search keywords for each feature
```

### Step 2: Load ProductBoard Data

```python
# Primary source: ProductBoard notes export
data_path = "skills/productboard-insights/data/notes-export.csv"

# Alternative: OneDrive file
# Use outlook_api.py to download from /me/drive
```

### Step 3: Analyze Each Feature

For each feature in the list:
1. **Search** ProductBoard data using keywords
2. **Count** matches (mentions) and unique companies
3. **Categorize** demand level:
   - ✅ **Strong Demand**: 500+ mentions OR 50+ companies
   - ⚠️ **Moderate Demand**: 100-500 mentions OR 20-50 companies
   - ❌ **Low Demand**: <100 mentions AND <20 companies
4. **Extract** use cases if demand is Strong/Moderate

### Step 4: Generate Word Document Report

**Output**: `outputs/voc-analyst/[product-area]-feature-validation-[YYYY-MM-DD].docx`

---

## Report Structure (Word Document)

### Title Page
- Product Area: [Name]
- Generated: [Date]
- Data Source: ProductBoard (X records)

### 1. Executive Summary
- Total features analyzed
- Validation results: X validated, Y need review, Z low demand
- Top customer companies

### 2. Feature Validation Matrix

| Feature | Status | Mentions | Companies | Verdict | Priority |
|---------|--------|----------|-----------|---------|----------|
| Impact Analysis | Discovery | 5,561 | 958 | ✅ Strong | P0 |
| ... | ... | ... | ... | ... | ... |

### 3. Validated Features (Detailed Analysis)

For each feature with Strong/Moderate demand:

#### [Feature Name]
**Demand Signal:** X mentions from Y companies
**Verdict:** ✅ Worth Building

**Problem Statement:**
[Extracted from customer feedback patterns]

**Use Cases:**
1. As a [role], I want to [action], so that [outcome]
2. ...

**Customer Evidence:**
> "[Quote]" — Company Name

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

### 4. Features Needing Review

Features with Moderate demand that need further validation.

### 5. Low Demand Features

Features with insufficient customer evidence. Recommend:
- Revisit problem definition
- Consider alternative solutions
- Deprioritize or remove from roadmap

### 6. Appendix: Top Customer Companies

| Company | Total Mentions | Key Features Requested |
|---------|---------------|----------------------|

---

## Working Directories

- **Temp files**: `skills/voc-analyst/temp/`
- **Output files**: `outputs/voc-analyst/`

## Dependencies

- `python-docx` for Word document generation
- `pandas` for data analysis
- `skills/outlook/outlook_api.py` for OneDrive access

## Integration

- **PRD Skill**: Feed validated use cases into PRD documents
- **Roadmap Skill**: Use validation verdicts for prioritization
- **ProductBoard Insights**: Complement with feature-level analysis