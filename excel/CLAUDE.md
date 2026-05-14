> ⚠️ **This file contains instructions for GitHub Copilot (Claude), not for humans.**
> If you're a human, see [README.md](README.md) for user-friendly documentation.

---

# Excel Generation - Claude Instructions

## Libraries

```python
pip install openpyxl pandas xlsxwriter
```

## Common Operations

### Create Workbook
```python
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws.title = "Data"
```

### Add Data
```python
# Headers
ws.append(['Column1', 'Column2', 'Column3'])
# Data rows
ws.append([value1, value2, value3])
```

### Formatting
```python
from openpyxl.styles import Font, Fill, Alignment

# Bold headers
for cell in ws[1]:
    cell.font = Font(bold=True)

# Column width
ws.column_dimensions['A'].width = 20
```

### Charts
```python
from openpyxl.chart import BarChart, Reference

chart = BarChart()
data = Reference(ws, min_col=2, min_row=1, max_col=3, max_row=10)
chart.add_data(data, titles_from_data=True)
ws.add_chart(chart, "E2")
```

### Save
```python
wb.save('outputs/filename.xlsx')
```

## Working Directory

**IMPORTANT**: Create all temporary files in:
```
skills/excel/temp/
```

## Output Location

Save final files to: `outputs/[filename].xlsx`

## Troubleshooting

If you encounter issues:
1. Document in `troubleshooting/CLAUDE.md`
