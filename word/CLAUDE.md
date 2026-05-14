> ⚠️ **This file contains instructions for GitHub Copilot (Claude), not for humans.**
> If you're a human, see [README.md](README.md) for user-friendly documentation.

---

# Word Document Generation - Claude Instructions

## Libraries

```python
pip install python-docx
```

## Common Operations

### Create Document
```python
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
```

### Add Content
```python
# Title
doc.add_heading('Document Title', 0)

# Heading levels
doc.add_heading('Section 1', level=1)
doc.add_heading('Subsection', level=2)

# Paragraphs
doc.add_paragraph('Normal text here.')

# Bullet lists
doc.add_paragraph('First item', style='List Bullet')
doc.add_paragraph('Second item', style='List Bullet')

# Numbered lists
doc.add_paragraph('Step 1', style='List Number')
```

### Tables
```python
table = doc.add_table(rows=3, cols=3)
table.style = 'Table Grid'
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Header 1'
```

### Save
```python
doc.save('outputs/filename.docx')
```

## SAP Template

If SAP template exists, load it:
```python
doc = Document('templates/SAP_Template.docx')
```

## Working Directory

**IMPORTANT**: Create all temporary files in:
```
skills/word/temp/
```

## Output Location

Save final files to: `outputs/[filename].docx`

## Troubleshooting

If you encounter issues:
1. Document in `troubleshooting/CLAUDE.md`
