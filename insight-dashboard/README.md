# ProductBoard Insight Dashboard

Generate actionable Excel dashboards from ProductBoard customer insights in one command.

## 🚀 Quick Start (One Command)

```bash
# 1. Navigate to this folder
cd skills/insight-dashboard

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Generate your dashboard
python generate_dashboard.py your_insights.csv
```

That's it! An Excel dashboard will be created with all your insights categorized and prioritized.

## 📊 What You Get

An Excel workbook with:

| Sheet | What's Inside |
|-------|---------------|
| **Cumulative Overview** | High-level metrics, product breakdown, trends |
| **[Product Sheets]** | Per-product analysis with themes, features, charts |
| **All Insights** | Complete data with filters for exploration |

Each product sheet includes:
- 📈 Key metrics (insights, themes, companies)
- 🎯 Theme distribution with pie chart
- 📉 Year-wise trend with line chart
- ⭐ Top features with RICE priority scores
- 🏢 Top companies requesting features
- 🎫 Service tickets section

## 📁 Input Requirements

Your CSV or Excel file needs these columns:

| Column | Required | Description |
|--------|----------|-------------|
| `note_text` | ✅ Yes | The customer insight/feedback text |
| `company_name` | ✅ Yes | Customer company name |
| `tags` | Optional | ProductBoard tags (enables product classification) |
| `created_at` | Optional | Date (enables trend analysis) |

## 💡 Usage Examples

```bash
# Basic usage - auto-generates output filename
python generate_dashboard.py insights.csv

# Specify output location
python generate_dashboard.py insights.xlsx dashboard.xlsx

# Use file from rawnotes folder
python generate_dashboard.py ../../rawnotes/productboard_export.csv

# Save to outputs folder
python generate_dashboard.py data.csv ../../outputs/my_dashboard.xlsx
```

## 🎯 Use with Claude/Copilot

Simply ask:
```
#create-insight-dashboard
```

Or describe what you need:
> "Create a dashboard from the productboard export in rawnotes"

## 📐 RICE Scoring

Features are prioritized using RICE framework:

```
RICE = (Reach × Impact × Confidence) / Effort
```

| Component | What It Measures |
|-----------|------------------|
| **Reach** | Unique companies requesting this |
| **Impact** | Language urgency (critical, urgent, etc.) |
| **Confidence** | Number of insights supporting this |
| **Effort** | Estimated implementation complexity |

**High RICE = High Priority** (shown in green)

## 🏗️ Project Structure

```
insight-dashboard/
├── generate_dashboard.py      # 👈 MAIN ENTRY POINT
├── multi_product_dashboard.py # Core dashboard generation
├── product_classifier.py      # Product classification
├── dynamic_cluster_analyzer.py # Theme identification
├── data_processor.py          # Data loading/cleaning
├── requirements.txt           # Dependencies
├── CLAUDE.md                  # AI assistant instructions
├── README.md                  # This file
└── temp/                      # Working directory
```

## 🔧 Alternative: Interactive Dashboard

For interactive exploration in browser:

```bash
streamlit run app.py
```

Opens at `http://localhost:8501` with upload capability.

## 🐛 Troubleshooting

### "File not found"
- Check file path is correct
- Try absolute path: `python generate_dashboard.py "C:\full\path\to\file.csv"`

### "Missing packages"
```bash
pip install -r requirements.txt
```

### "Column not found"
- Your file must have `note_text` column
- Rename your text column if needed

### Excel won't open
- Close the file if open elsewhere
- Try different output filename

## 📚 SAP Signavio Products

Insights are automatically classified into:

- Process Manager
- Process Governance
- Collaboration Hub
- Process Intelligence (SPI)
- Journey Modeler
- Value Accelerator
- Process Insights
- Process Mining

Classification uses ProductBoard tags when available.

## 🤝 Getting Help

- Check [CLAUDE.md](CLAUDE.md) for AI assistant integration
- See troubleshooting section above
- Contact PM team for support
