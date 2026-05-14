# Customized Enablement Material

**Generate tailored customer enablement documents for SAP Signavio features.**

## What This Skill Does

- Creates customized Word documents for customer enablement
- Pulls customer context from SharePoint, emails, and user research
- Applies SAP branding and professional formatting
- Tailors content based on customer's industry and specific needs

## How to Use

Open Copilot Chat and ask:

```
Create enablement material for [Customer Name] about [Feature]
```

```
Generate a T2P onboarding guide for [Customer]
```

```
Prepare AI-Assisted Process Modeler documentation for [Customer]
```

### Example Prompts

```
Create enablement material for Eaton Corporation with Text to Process feature

Generate a Joule onboarding document for BMW Group

Prepare AI features enablement guide for Siemens customized to manufacturing
```

## What Gets Generated

The enablement document includes:

| Section | Content |
|---------|---------|
| **1. Motivation** | Customized reasons to use AI features based on customer context |
| **2. Overview** | Available AI functionalities within SAP Signavio |
| **3. Demo Video** | Links to tutorial videos (5-10 minutes) |
| **4. Activation** | Prerequisites, data protection, access rights setup |
| **5. Q&A** | Security, languages, voice-to-process, helpful resources |
| **6. Roadmap** | What's coming next, roadmap explorer, feedback channels |
| **7. Best Practices** | Industry-specific success stories and tips |

## Prerequisites

- **Python** with `python-docx` library:
  ```bash
  pip install python-docx
  ```
- SharePoint authentication (for customer materials):
  ```bash
  python skills/outlook/outlook_api.py auth
  ```
- Outlook authentication (for email context search)

## Output Location

Documents are saved to:
```
outputs/[CustomerName]_[Feature]_Enablement_Guide.docx
```

## Data Sources

The skill pulls context from:

| Source | Purpose |
|--------|---------|
| SharePoint | Reference materials, templates, research documents |
| Outlook | Customer emails, feedback, previous conversations |
| User Research | Survey data, interview insights |
| `context/` folder | Product context, company guidelines |

## Tips

- Be specific about the customer name (enables email search)
- Mention the industry for relevant success stories
- Reference any known customer feedback or priorities
- Specify if you need focus on particular sections

---

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-02-23 | Ling Feng | Initial skill creation with T2P enablement template |

