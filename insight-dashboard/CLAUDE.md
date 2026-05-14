# ProductBoard Insight Dashboard Skill - Claude Instructions

> ⚠️ **This file is for Claude/Copilot.** For human docs, see [README.md](README.md).

---

## Purpose

Generate actionable Excel dashboards from ProductBoard customer insights. Takes raw CSV/Excel exports and produces a comprehensive, categorized dashboard with:
- Insights organized by SAP Signavio product
- Theme/cluster analysis per product
- RICE-scored feature prioritization
- Year-wise trends and company distributions
- Service ticket identification

## How to Invoke

```
#create-insight-dashboard
#analyze-productboard
```

## When to Use

- User uploads a ProductBoard export (CSV or Excel)
- User wants to analyze customer feedback patterns
- User needs prioritized feature recommendations
- User wants to understand which products get most feedback
- Preparing data for roadmap discussions or planning

---

## Execution Steps

### Step 1: Locate the Input File

User will provide a CSV or Excel file. Common locations:
- Direct path provided by user
- `rawnotes/` folder
- `skills/insight-dashboard/temp/`

Required columns:
- `note_text` - The insight/feedback text (REQUIRED)
- `company_name` - Customer company (REQUIRED for company analysis)
- `tags` - ProductBoard tags (optional, enables product classification)
- `created_at` - Date (optional, enables trend analysis)

### Step 2: Install Dependencies (if needed)

```powershell
cd "c:\Users\I768592\Signavio_PM_Agent\skills\insight-dashboard"
pip install -r requirements.txt
```

### Step 3: Generate the Dashboard

```powershell
cd "c:\Users\I768592\Signavio_PM_Agent\skills\insight-dashboard"
python generate_dashboard.py "<input_file>" [output_file]
```

Examples:
```powershell
# Auto-generate output filename
python generate_dashboard.py "../../rawnotes/insights.csv"

# Specify output location
python generate_dashboard.py "insights.xlsx" "../../outputs/dashboard.xlsx"
```

### Step 4: Report Results

Tell user:
1. Where the dashboard file was created
2. Summary of what's in the dashboard (products, insight count)
3. How to open and use it

---

## Output Structure

The generated Excel dashboard contains:

| Sheet | Contents |
|-------|----------|
| Cumulative Overview | All-products summary, metrics, trends |
| [Product Name] | Per-product analysis with themes, features, charts |
| All Insights | Raw classified data with filters |

Each product sheet includes:
- Key metrics (insights, themes, companies)
- Theme distribution with pie chart
- Year-wise trend with line chart
- Top features with RICE scores
- Top companies
- Service tickets section

---

## Key Files

| File | Purpose |
|------|---------|
| `generate_dashboard.py` | **Main entry point** - simple CLI wrapper |
| `multi_product_dashboard.py` | Core dashboard generation logic |
| `product_classifier.py` | Maps insights to SAP Signavio products |
| `dynamic_cluster_analyzer.py` | Theme/cluster identification |
| `data_processor.py` | Data loading and cleaning |
| `requirements.txt` | Python dependencies |

---

## Troubleshooting

### "File not found" error
- Check the file path is correct
- Use absolute path if relative path doesn't work
- Ensure file extension is .csv, .xlsx, or .xls

### "Missing column" error
- Input file must have `note_text` column
- Create it if data uses different column name:
  ```python
  df['note_text'] = df['your_text_column']
  ```

### "Missing packages" error
```powershell
cd skills/insight-dashboard
pip install -r requirements.txt
```

### Excel file won't open
- Ensure output file isn't open in another program
- Try a different output filename

---

## Alternative: Interactive Dashboard

For interactive exploration (requires browser):

```powershell
cd "c:\Users\I768592\Signavio_PM_Agent\skills\insight-dashboard"
streamlit run app.py
```

Opens at `http://localhost:8501` with upload capability.

---

## Temporary Files

- Working files go in `skills/insight-dashboard/temp/`
- Final outputs go in `outputs/` when possible
- Clear temp folder periodically
