> ⚠️ **This file contains instructions for GitHub Copilot (Claude), not for humans.**
> If you're a human, see [README.md](README.md) for user-friendly documentation.

---

# Customized Enablement Material - Claude Instructions

## Purpose

Generate tailored customer enablement documents for SAP Signavio features (Text-to-Process, Joule, AI capabilities) by:
1. Gathering customer context from SharePoint, emails, and research
2. Customizing content based on customer industry and needs
3. Creating professionally formatted Word documents

## When to Use

Trigger this skill when the user asks to:
- "Create enablement material for [customer]"
- "Generate onboarding guide for [customer]"
- "Prepare [feature] documentation for [customer]"
- "Make a customized T2P guide for [customer]"

---

## Libraries

```python
pip install python-docx
```

## Workflow

### Step 1: Gather Customer Context

**Search emails for customer mentions:**

```python
import sys
sys.path.insert(0, 'skills/outlook')
from outlook_api import search_messages, graph_request

# Search for customer emails
results = search_messages('[CustomerName]', max_messages=30)
for m in results:
    msg_id = m.get('id')
    full_msg = graph_request(f'/me/messages/{msg_id}')
    # Extract customer insights, feedback, priorities
```

**Access SharePoint materials:**

```python
import sys
sys.path.insert(0, 'skills/sharepoint')
from sharepoint_api import list_folder, get_file_content

# List enablement materials folder
DRIVE_ID = "b!qZrHVCLiaU6CEgw79hYISQnpVWxqhSFGj-ScZhv2E1pkpJGAuh5FQKA6sKyHMSM7"
items = list_folder("/Customer enablement/Text to Process Enablement Material")
```

**Read user research data** from `research/` folder or SharePoint PDFs.

### Step 2: Create Document Structure

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Set document styles
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)
```

### Step 3: Generate Sections

**Required sections (customize content per customer):**

| Section | Content Source |
|---------|----------------|
| 1. Motivation | Customer emails, known priorities, industry context |
| 2. Overview | Standard T2P/Joule capabilities from SharePoint materials |
| 3. Demo Video | Standard links from enablement templates |
| 4. Activation | Standard prerequisites + customer-specific setup notes |
| 5. Q&A | Standard FAQ + customer-specific concerns from emails |
| 6. Roadmap | Standard roadmap + features customer requested |
| 7. Best Practices | Industry-specific success story + customer modeling conventions |

### Step 4: Apply SAP Styling

```python
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_heading_style(paragraph, size, color_hex="0070C0", bold=True):
    """Apply SAP blue styling to headings."""
    for run in paragraph.runs:
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = RGBColor.from_string(color_hex)

def add_styled_table(doc, headers, rows):
    """Create table with SAP blue header row."""
    table = doc.add_table(rows=len(rows)+1, cols=len(headers))
    table.style = 'Table Grid'
    
    # Blue header row
    header_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        header_cells[i].text = header
        for paragraph in header_cells[i].paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor.from_string("FFFFFF")
        shading = OxmlElement('w:shd')
        shading.set(qn('w:fill'), '0070C0')
        header_cells[i]._tc.get_or_add_tcPr().append(shading)
    
    return table
```

---

## Document Template

### Title Page
- Document title: "AI-Assisted Process Modeler" or feature name
- Subtitle: "Text-to-Process Enablement Guide"
- Customer name: "Prepared for: [Customer]"
- Date: Current month/year
- SAP Signavio branding

### Section 1: Motivation (Customized)
Based on customer context, address:
- Their specific pain points (from emails/feedback)
- Their modeling conventions and standards
- Their transformation initiatives (S/4HANA, etc.)
- Time savings potential based on their workflow

### Section 2: Overview (Standard + Customized)
- Text-to-Process capabilities
- Joule integration (40+ skills)
- Dictionary linking
- BPMN compliance

### Section 3: Demo Video (Standard)
- Link: https://help.sap.com/docs/signavio-process-manager/user-guide/ai-assisted-process-modeler
- 6-step walkthrough

### Section 4: Activation (Standard)
- Prerequisites table
- Data protection notes
- Access rights setup steps
- User guide link

### Section 5: Q&A (Standard + Customized)
- Security & Privacy
- Supported Languages (11 languages)
- Voice-to-Process status
- Helpful Resources table
- Add customer-specific questions from emails

### Section 6: Roadmap (Standard)
- Upcoming features list
- Roadmap explorer link
- Feedback submission channels

### Section 7: Best Practices (Customized)
- Tips based on customer's modeling standards
- Industry-relevant success story (Albatha for manufacturing, etc.)

---

## Working Directory

**IMPORTANT**: Create all temporary files in:
```
skills/enablement-material/temp/
```

## Output Location

Save final files to: `outputs/[CustomerName]_[Feature]_Enablement_Guide.docx`

## Key Reference Materials

| Material | Location |
|----------|----------|
| T2P Training Deck | SharePoint: Customer enablement/Text to Process Enablement Material |
| User Research | SharePoint: T2P & I2P-Research Stream PDF |
| FAQ Document | SharePoint: FINAL_Dec_release_INTERNAL_FAQ |
| Tips Guide | research/text-to-process-tips.md |
| Product Context | context/product-context.md |

## Success Stories by Industry

| Industry | Customer | Key Results |
|----------|----------|-------------|
| Manufacturing | Albatha Holdings LLC | 20-30 min → 5-7 min, 50%+ accuracy, 40+ companies |
| Automotive | (Use Albatha pattern) | S/4HANA transformation focus |
| Financial Services | (Emphasize compliance) | Governance and audit trails |

---

## Troubleshooting

If you encounter issues:
1. Document in `troubleshooting/CLAUDE.md`

### Common Issues

| Issue | Resolution |
|-------|------------|
| SharePoint 401 | Re-authenticate: `python skills/outlook/outlook_api.py auth` |
| No customer emails found | Try variations of customer name, check spelling |
| python-docx not installed | Run: `pip install python-docx` |

