# Newsletter Designer

Generate catchy, structured marketing content for internal newsletters across teams.

## What It Does

Creates newsletter entries following a **Problem → Solution → Outcome** framework:

| Field | Example |
|-------|---------|
| Catchy Headline | "Stopping Checkout Drops" |
| THE PROBLEM | 15% drop-off at payment because users couldn't see shipping costs. |
| THE SOLUTION | Dynamic shipping calc before login. |
| THE OUTCOME | Conversion +4.5% ($12K impact). |

## How to Use

Simply describe your feature, improvement, or team achievement. The skill will help you craft:
- A catchy headline (max 5 words)
- A compelling problem statement
- A clear solution description
- A measurable outcome

### Example Prompts

- "Write newsletter content for our new search feature that reduced load times by 40%"
- "Create an entry for Team Phoenix's Q1 migration project"
- "Help me write catchy content about our accessibility improvements"

## Output Format

Content is formatted as a table row ready for copy-paste into the newsletter spreadsheet.

## Folder Structure

```
newsletter-designer/
├── spg/                    # SPG (Signavio Product Group) newsletters
│   └── 2026/
│       ├── 01-january/
│       ├── 02-february/    # ← Current entries
│       ├── 03-march/
│       └── ...
├── temp/
├── README.md
└── SKILL.md
```

---

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-03-03 | Claude | Initial skill creation |
| 2026-03-03 | Claude | Renamed to newsletter-designer, added SPG folder structure |
