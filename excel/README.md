# Excel Generation

Create and manipulate Excel spreadsheets.

## What This Skill Does

- Generates Excel files from data
- Creates formatted tables, charts, and pivot tables
- Manipulates existing spreadsheets
- Exports data in Excel format

## How to Use

Open Copilot Chat (`Ctrl+Shift+I`) and ask:

```
Create an Excel spreadsheet with [your data]

Generate a pivot table from this data

Format this data as an Excel report
```

### Example Prompts

```
Create an Excel file with our Q1 feature priorities and ICE scores

Generate a spreadsheet tracking our Jira tickets status

Create a budget template in Excel
```

## Prerequisites

- **Python** with `openpyxl` library:
  ```bash
  pip install openpyxl pandas
  ```

## What Gets Generated

Excel files are saved to:
```
outputs/[filename].xlsx
```

## Tips

- Describe the structure you want (columns, headers)
- Mention if you need charts or formatting
- Provide sample data or reference existing files

---

*For technical details, see [CLAUDE.md](CLAUDE.md)*
