---
name: productboard-features
description: Pandas-backed data access layer for ProductBoard features — filtering, hierarchy, column selection, enrichment
dynamic_context:
  - type: file
    path: skills/productboard-features/feature_store.py
    description: Core FeatureStore module
---

# ProductBoard Features Data Access Layer

> ⚠️ This file contains instructions for GitHub Copilot (Claude), not for humans.

## ⚠️ CRITICAL SAFETY RULE: READ-ONLY — NO API CALLS

**This skill NEVER calls the ProductBoard API.** All data comes from the extraction skill's JSON export on SharePoint (`pb_features_full_latest.json`). If a user asks to fetch fresh data from ProductBoard, direct them to the `dirks-skills/productboard-extraction` skill instead.

## Purpose

Foundational data access layer for ProductBoard feature data. Provides:

- **Loading** — Downloads the full JSON export from SharePoint (fallback to local extraction temp)
- **Hierarchy** — Materialized Product → Component → Feature → Sub-feature tree
- **Filtering** — Complex criteria: by product, component, status, owner, timeframe, health, text search, arbitrary predicates
- **Column selection** — Pick specific fields from features, including nested fields via dot notation
- **Lazy enrichment** — On-demand: initiatives, objectives, releases, custom fields, description sections
- **Export** — JSON, CSV, Python dicts, or raw pandas DataFrame

**This is a foundation skill.** Other skills and scripts import `FeatureStore` to build higher-level analyses, dashboards, reports, and automations.

## Before Starting

Read these context files to understand the product domain:

- `context/product-context.md` — SAP Signavio product landscape
- `context/team/config.md` — Team structure and conventions
- `context/active-work.md` — Current priorities

## Before Querying — Mandatory Steps

> **Always** consult the column metadata before writing any filter or query code.
> This ensures you use the right columns, correct values, and required enrichments.

1. **Read query hints first** — Call `FeatureStore.describe_hints()` (or CLI `--describe hints`) to see few-shot examples of natural-language → code translations.
2. **Check column details** — When unsure about a column, call `FeatureStore.describe("column_name")` for its type, allowed values, required enrichment, and aliases.
3. **Follow these mandatory rules:**

### External / Internal / Dev-Only Items

**Always use `cf_Roadmap Visibility`** (requires `enrich_custom_fields()`).

| Value | Meaning |
|-------|---------|
| `"External"` | Visible on external roadmap |
| `"Internal"` | Internal roadmap only |
| `"Dev Only"` | Engineering-internal |

Do **not** use `cf_Roadmap Candidacy` for visibility questions — it is a different field with different semantics.

### Release Timing / "When does it ship?"

**Always use `release_quarter` and `release_date`** (requires `enrich_releases()`).

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| `releases` | `list[str]` | `["R26Q3 (July)", "2601-05"]` | Original release names (inconsistent format) |
| `release_quarter` | `list[str]` | `["Q3 2026"]` | **GENERATED** — normalised quarter labels, deduplicated & sorted |
| `release_date` | `list[str]` | `["2026-07-01"]` | **GENERATED** — normalised ISO dates (start of period), sorted |

- `release_quarter` and `release_date` are **generated at extraction time** by parsing release names. They are not raw ProductBoard fields.
- For temporal filters (e.g. "features shipping in Q1 2026"), always filter on `release_quarter` or `release_date`, **not** on the raw `releases` column.
- If both normalised columns are empty for a feature, the release name could not be parsed — fall back to displaying the raw `releases` list.

## Data Source

### SharePoint (primary)

```
Site:   https://sap.sharepoint.com/teams/ProductStrategyGroup
Path:   Shared Documents/0 General/Data/productboard/features/pb_features_full_latest.json
```

Downloaded via Microsoft Graph API using the shared Outlook token at `~/.claude/tokens/outlook-token.json`.

### Local fallback

```
skills/dirks-skills/productboard-extraction/temp/pb_features_full_latest.json
(sibling folder: ../productboard-extraction/temp/)
```

If SharePoint download fails (network, auth), the module falls back to the local copy left by the extraction skill.

## JSON Structure

The source JSON has 15 top-level keys:

| Key | Type | Description |
|-----|------|-------------|
| `_metadata` | object | Export timestamp, source, warnings |
| `features` | array | All features (~11K) with status, parent, owner, timeframe, health, description, sections |
| `feature_statuses` | array | Status definitions (8 statuses) |
| `products` | array | Product entities (top of hierarchy) |
| `components` | array | Component entities (mid-level, can nest) |
| `custom_fields` | array | Custom field definitions (names, types, options) |
| `custom_field_values` | array | Custom field values per feature |
| `release_assignments` | array | Feature → release assignments |
| `releases` | array | Release definitions |
| `release_groups` | array | Release group definitions |
| `initiatives` | array | Initiative definitions |
| `objectives` | array | Objective definitions |
| `initiative_feature_links` | object | `{ feature_id: [initiative_name, ...] }` |
| `objective_feature_links` | object | `{ feature_id: [objective_name, ...] }` |

### Feature Hierarchy

```
Product (products array)
  └── Component (components array, can nest: component → component)
        └── Feature (features array, type="feature", parent.component)
              └── Sub-feature (features array, type="subfeature", parent.feature)

Features can also be direct children of a Product (parent.product, no component).
```

### Feature Object Fields

| Field | Type | Example |
|-------|------|---------|
| `id` | string (UUID) | `"abc-123-..."` |
| `name` | string | `"Collaboration Hub"` |
| `type` | string | `"feature"` or `"subfeature"` |
| `description` | string (HTML) | `"<h2>Problem</h2><p>..."` |
| `status` | object | `{ "id": "...", "name": "In progress" }` |
| `parent` | object | One key: `product`, `component`, or `feature`, each `{ id, links }` |
| `owner` | object or null | `{ "email": "user@sap.com" }` |
| `archived` | boolean | `false` |
| `timeframe` | object | `{ "startDate": "2026-01-01", "endDate": "2026-06-30", "granularity": "quarter" }` |
| `lastHealthUpdate` | object or null | `{ "status": "on-track", "message": "...", "createdAt": "..." }` |
| `links` | object | `{ "self": "https://api...", "html": "https://app..." }` |
| `createdAt` | string (ISO 8601) | `"2025-03-15T10:30:00Z"` |
| `updatedAt` | string (ISO 8601) | `"2026-02-28T14:20:00Z"` |
| `sections` | object | `{ "sec_problem_statement": "...", "sec_scope": "..." }` (in JSON export) |

## Public API — FeatureStore Class

### Loading

```python
from feature_store import FeatureStore

# Auto: SharePoint first, local fallback
fs = FeatureStore.load()

# Explicit SharePoint download
fs = FeatureStore.from_sharepoint()

# From a local file
fs = FeatureStore.from_file("path/to/pb_features_full_latest.json")
```

### Hierarchy

```python
fs.get_products()                    # [{"id": "...", "name": "Process Manager"}, ...]
fs.get_components(product="Process Manager")  # Components under a product
fs.get_product_tree("Process Manager")        # Full subtree as nested dict
fs.get_descendant_ids("some-node-id")         # Flat set of all feature IDs under a node
fs.print_tree("Process Manager", max_depth=2) # Pretty-print the tree
```

### Filtering (chainable, returns new FeatureStore)

```python
# Single filter
pm = fs.filter(product="Process Manager")

# Chained filters (AND logic)
active = fs.filter(product="Process Manager", status=["In progress", "Discovery"], archived=False)

# All supported criteria:
fs.filter(
    product="Process Manager",              # All features under this product (uses hierarchy)
    component="Collaboration",              # All features under this component
    status="In progress",                   # Status name (string or list for OR)
    owner="user@sap.com",                   # Owner email
    type="feature",                         # "feature" or "subfeature"
    archived=False,                         # Archived flag
    health="at-risk",                       # Health status
    timeframe_after="2026-01-01",           # Timeframe start >= date
    timeframe_before="2026-12-31",          # Timeframe end <= date
    search="collaboration",                 # Text search in name + description
    where=lambda df: df[df.name.str.len() > 50],  # Arbitrary DataFrame predicate
)
```

### Column Selection

```python
# Select specific columns → returns new FeatureStore with narrowed DataFrame
result = active.select("name", "status_name", "owner_email")

# After enrichment, enriched columns are available
active.enrich_initiatives()
result = active.select("name", "status_name", "initiatives")
```

### Lazy Enrichment (mutates in-place, idempotent)

```python
fs.enrich_initiatives()     # Adds 'initiatives' column (list of names)
fs.enrich_objectives()      # Adds 'objectives' column (list of names)
fs.enrich_releases()        # Adds 'releases' column (list of release names)
                            #   + 'release_quarter' (GENERATED normalised quarters, e.g. ["Q1 2026"])
                            #   + 'release_date' (GENERATED normalised ISO dates, e.g. ["2026-01-01"])
fs.enrich_custom_fields()   # Adds 'cf_<name>' columns (one per custom field)
fs.enrich_sections()        # Adds 'sec_<name>' columns (parsed from description HTML)
fs.enrich_all()             # Runs all enrichments
```

### Output

```python
df = fs.to_df()                     # Raw pandas DataFrame
records = fs.to_dicts()             # List of plain dicts
json_str = fs.to_json()             # JSON string
fs.to_json("output.json")           # Write to file
fs.to_csv("output.csv")             # Write CSV
len(fs)                             # Feature count
fs.stats()                          # Summary: counts by status, product, type
```

### CLI Usage

```bash
# List products
uv run skills/productboard-features/feature_store.py --products

# Show hierarchy tree
uv run skills/productboard-features/feature_store.py --tree "Process Manager"

# Filter and select columns
uv run skills/productboard-features/feature_store.py \
  --product "Process Manager" \
  --status "In progress" "Discovery" \
  --select name status_name owner_email

# With enrichment
uv run skills/productboard-features/feature_store.py \
  --product "Process Manager" \
  --enrich initiatives \
  --select name initiatives \
  --format json

# Summary statistics
uv run skills/productboard-features/feature_store.py --stats

# Export to file
uv run skills/productboard-features/feature_store.py \
  --product "Process Manager" \
  --enrich all \
  --format csv \
  --output temp/pm_features.csv
```

## Working Directory

All temporary files go into `skills/productboard-features/temp/`. This directory is gitignored.

## How Other Skills Should Use This

```python
import sys
sys.path.insert(0, "skills/productboard-features")
from feature_store import FeatureStore

fs = FeatureStore.load()
pm_active = fs.filter(product="Process Manager", status="In progress")
pm_active.enrich_initiatives()
df = pm_active.to_df()
# ... build your analysis, dashboard, report from df ...
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No Graph token found" | Run `python tools/outlook/outlook_api.py auth` |
| "Could not find Documents drive" | Check SharePoint site permissions |
| SharePoint download fails | Falls back to local file in `dirks-skills/productboard-extraction/temp/` |
| "No JSON data file found" | Run extraction first: `python skills/dirks-skills/productboard-extraction/extract_features.py` |
| SSL certificate errors on macOS | Script includes automatic fallback to unverified context |
