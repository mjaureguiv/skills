# ProductBoard Insights Analyzer

Analyze customer feedback from ProductBoard to identify patterns, prioritize features, and synthesize insights into actionable recommendations.

## Quick Start

### 1. Update the Data

Before analyzing, get the latest ProductBoard export:

1. **Login to ProductBoard** via SSO:  
   https://signavio.productboard.com

2. **Download the export** (after login):  
   https://signavio.productboard.com/api/notes/export?export_type=with_features&strip_html=true

3. **Save the file** to:  
   `skills/productboard-insights/data/notes-export.csv`

### 2. Analyze

Ask Copilot to analyze the data:

```
Analyze ProductBoard insights for diagram embedding features
```

```
What are the top requested features from enterprise customers?
```

```
Find all unprocessed customer feedback about reporting
```

## Example Queries

| Query | What it does |
|-------|--------------|
| "Find feedback on SharePoint integration" | Searches for SharePoint-related customer requests |
| "Which companies want Confluence embedding?" | Lists companies requesting Confluence features |
| "Top 10 most requested features" | Ranks features by customer demand |
| "Unprocessed insights from Q4" | Finds new feedback that hasn't been triaged |
| "Security concerns from enterprise customers" | Identifies security-related feedback |

## Data Structure

The CSV export contains customer notes with:

- **Feature info**: feature_name, feature_id, tags
- **Note content**: note_title, note_text, state
- **Customer info**: company_name, company_domain, user_name
- **Metadata**: created_at, last_updated_at, source_url

## Output Examples

### Summary Report
```markdown
## Diagram Embedding - Customer Insights

### Top Requests
1. **Published-only embedding** (8 customers) - Richemont, Mercedes-Benz, TU Darmstadt...
2. **Multi-language support** (5 customers) - Richemont, Migros...
3. **SharePoint integration** (4 customers) - Richemont, Honeywell...

### Key Themes
- Security controls for embedded content
- Version control (show published, not draft)
- Third-party integrations (Confluence, SharePoint)
```

## Tips

- **Be specific**: "reporting features" works better than "reports"
- **Include time ranges**: "feedback from 2024" for recent insights
- **Name the output**: "Create a markdown summary of API feedback"

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "File not found" | Download fresh export from ProductBoard |
| "No results" | Try broader search terms or check spelling |
| Old data | Re-download the CSV export |

## Related Skills

- [Jira](../jira/) - Create tickets from insights
- [PRD](../prd/) - Write PRDs based on customer feedback
- [Roadmap](../roadmap/) - Prioritize features using insights
