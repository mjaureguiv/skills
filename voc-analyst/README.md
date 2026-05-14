# VoC (Voice of Customer) Analyst Skill

Validate your planned features against real customer feedback data. Get go/no-go recommendations with customer evidence.

## Quick Start

**Ask Claude:**
```
Analyze customer feedback for my [Product Area] features
```

Claude will ask for:
1. Product area name
2. Feature list with descriptions, status, and keywords

## Input Format

Provide your features in this format:

| Feature Name | Description | Status | Keywords |
|-------------|-------------|--------|----------|
| Impact Analysis | Show affected processes when linked objects change | Discovery | impact, change, affected, downstream |
| Relationship Graph | Interactive visualization of process relationships | Planned | graph, navigation, explore, connections |
| AI Suggestions | Recommend missing relationships automatically | Discovery | AI, suggest, recommend, missing |

**Status Options:** Discovery, Planned, In Development, Released

## Example Prompts

```
# Simple request
"Validate my Relation Manager features against customer feedback"

# With feature list
"Analyze VoC for these Process Modeler features:
- Impact Analysis (Discovery): impact, change, affected
- Relationship Graph (Planned): graph, navigate, explore"

# Quick validation
"Is there customer demand for [feature name]?"
```

## What You Get

### Word Document Report
`outputs/voc-analyst/[product-area]-feature-validation-[date].docx`

**Contents:**
1. **Executive Summary** - Total features, validation results
2. **Feature Validation Matrix** - Quick view of all features with verdicts
3. **Detailed Analysis** - Use cases, customer quotes, acceptance criteria (for validated features)
4. **Low Demand Features** - Features lacking customer evidence
5. **Customer Companies** - Top companies requesting these capabilities

### Verdicts

| Verdict | Criteria | Recommendation |
|---------|----------|----------------|
| ✅ Strong Demand | 500+ mentions OR 50+ companies | Build it |
| ⚠️ Moderate Demand | 100-500 mentions OR 20-50 companies | Review further |
| ❌ Low Demand | <100 mentions AND <20 companies | Reconsider |

## Data Sources

### ProductBoard (Primary)
- **Location**: `skills/productboard-insights/data/notes-export.csv`
- **Download**: [ProductBoard Notes Export](https://signavio.productboard.com/api/notes/export?export_type=with_features&strip_html=true)

### OneDrive
- Excel files accessible via Microsoft Graph API
- Claude can download directly from your OneDrive

## Output Location

```
outputs/voc-analyst/
├── relation-manager-feature-validation-2026-03-04.docx
├── process-intelligence-feature-validation-2026-03-04.docx
└── [product-area]-feature-validation-[date].docx
```

## Tips for Better Results

1. **Specific Keywords**: Use 3-5 relevant keywords per feature
2. **Short Descriptions**: One sentence explaining the feature
3. **Include All Features**: Even uncertain ones - let the data validate

## Integration

- **PRD Skill**: Use validated features to generate PRD sections
- **Roadmap Skill**: Prioritize based on demand signals
- **Requirements Skill**: Generate user stories from use cases