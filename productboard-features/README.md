# ProductBoard Features — Data Access Layer

Pandas-backed data access layer for querying ProductBoard feature data. Loads the full JSON export from SharePoint, builds a product hierarchy tree, and provides powerful filtering, column selection, and enrichment.

**This is a foundation skill** — other skills and scripts import `FeatureStore` to build dashboards, reports, and automations.

## Quick Start

### As a Python library

```python
import sys
sys.path.insert(0, "skills/productboard-features")
from feature_store import FeatureStore

fs = FeatureStore.load()  # Downloads from SharePoint (fallback: local file)
pm = fs.filter(product="Process Manager", status="In progress")
pm.enrich_initiatives()
print(pm.to_df()[["name", "status_name", "initiatives"]].head(10))
```

### As a CLI tool

```bash
# List all products
uv run skills/productboard-features/feature_store.py --products

# Filter features and select columns
uv run skills/productboard-features/feature_store.py \
  --product "Process Manager" \
  --status "In progress" \
  --select name status_name owner_email

# Show hierarchy tree
uv run skills/productboard-features/feature_store.py --tree "Process Manager"

# Summary statistics
uv run skills/productboard-features/feature_store.py --stats
```

## Prerequisites

| Requirement | How to Set Up |
|-------------|---------------|
| Extraction data | Run `python skills/dirks-skills/productboard-extraction/extract_features.py` at least once |
| Graph API token | Run `python tools/outlook/outlook_api.py auth` (needed for SharePoint download) |
| Python 3.10+ | Required by the script |
| pandas | Auto-installed by `uv run` (PEP 723 inline metadata) |

## Features

### Data Loading

- **SharePoint-first**: Downloads `pb_features_full_latest.json` from the ProductStrategyGroup SharePoint site
- **Local fallback**: Uses sibling `../productboard-extraction/temp/pb_features_full_latest.json` if SharePoint is unavailable
- **Explicit file**: `FeatureStore.from_file("path/to/file.json")`

### Hierarchy Tree

The feature hierarchy is: **Product → Component → Feature → Sub-feature**

```python
fs.get_products()                              # List all products
fs.get_components(product="Process Manager")   # Components under a product
fs.get_product_tree("Process Manager")         # Full nested subtree
fs.print_tree("Process Manager", max_depth=2)  # Pretty-print
```

### Filtering

Filters are chainable and return a new `FeatureStore`. Multiple criteria combine with AND; list values for a single field use OR.

| Criterion | Example | Description |
|-----------|---------|-------------|
| `product` | `"Process Manager"` | All features under a product (uses hierarchy) |
| `component` | `"Collaboration"` | All features under a component |
| `status` | `"In progress"` or `["In progress", "Discovery"]` | By status name(s) |
| `owner` | `"user@sap.com"` | By owner email |
| `type` | `"feature"` or `"subfeature"` | Feature type |
| `archived` | `False` | Exclude/include archived |
| `health` | `"at-risk"` | By health status |
| `timeframe_after` | `"2026-01-01"` | Timeframe start >= date |
| `timeframe_before` | `"2026-12-31"` | Timeframe end <= date |
| `search` | `"collaboration"` | Text search in name + description |
| `where` | `lambda df: df[...]` | Arbitrary DataFrame predicate |

### Enrichment

Enrichments are lazy — call them only when you need the data. Each is idempotent.

| Method | Adds Column(s) | Source |
|--------|----------------|--------|
| `enrich_initiatives()` | `initiatives` (list of names) | `initiative_feature_links` map |
| `enrich_objectives()` | `objectives` (list of names) | `objective_feature_links` map |
| `enrich_releases()` | `releases` (list of release names) | `release_assignments` + `releases` |
| `enrich_custom_fields()` | `cf_<name>` (one per field) | `custom_field_values` + `custom_fields` |
| `enrich_sections()` | `sec_<name>` (parsed from HTML) | Feature `description` HTML |
| `enrich_all()` | All of the above | — |

### Output

| Method | Returns |
|--------|---------|
| `to_df()` | `pandas.DataFrame` |
| `to_dicts()` | `list[dict]` |
| `to_json(path=None)` | JSON string, or writes to file |
| `to_csv(path)` | Writes CSV file |
| `stats()` | Summary dict (counts by status, product, type) |
| `len(fs)` | Feature count |

## DataFrame Columns (base, before enrichment)

| Column | Type | Description |
|--------|------|-------------|
| `id` | str | Feature UUID |
| `name` | str | Feature name |
| `type` | str | `"feature"` or `"subfeature"` |
| `description` | str | HTML description |
| `archived` | bool | Archived flag |
| `status_id` | str | Status UUID |
| `status_name` | str | e.g., "In progress", "Discovery" |
| `status_completed` | bool | Whether this status means "done" |
| `parent_type` | str | `"product"`, `"component"`, or `"feature"` |
| `parent_id` | str | Parent entity UUID |
| `parent_name` | str | Parent entity name |
| `owner_email` | str | Owner email or empty |
| `timeframe_start` | str | Start date or empty |
| `timeframe_end` | str | End date or empty |
| `timeframe_granularity` | str | `"quarter"`, `"month"`, etc. |
| `health_status` | str | `"on-track"`, `"at-risk"`, `"off-track"` or empty |
| `health_message` | str | Health update text |
| `health_date` | str | Health update date |
| `link_self` | str | API URL |
| `link_html` | str | Web URL |
| `created_at` | str | ISO 8601 creation timestamp |
| `updated_at` | str | ISO 8601 last update timestamp |

## CLI Reference

```
uv run skills/productboard-features/feature_store.py [OPTIONS]

Loading:
  --local PATH            Use a local JSON file instead of SharePoint

Filtering:
  --product NAME          Filter by product (uses hierarchy)
  --component NAME        Filter by component (uses hierarchy)
  --status NAME [NAME...] Filter by status name(s)
  --owner EMAIL           Filter by owner email
  --type TYPE             "feature" or "subfeature"
  --search TEXT           Text search in name + description
  --archived              Include only archived features
  --no-archived           Exclude archived features

Selection & Enrichment:
  --select COL [COL...]   Columns to include in output
  --enrich WHAT [WHAT...] Enrichments: initiatives, objectives, releases,
                          custom_fields, sections, all
Output:
  --format json|csv       Output format (default: json)
  --output PATH           Write to file instead of stdout
  --head N                Limit to first N rows
  --stats                 Show summary statistics
  --products              List all products
  --tree [NAME]           Show hierarchy tree (optionally rooted at a product)
  --max-depth N           Max tree depth (used with --tree)
```

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [productboard-extraction](../productboard-extraction/) | Source of the JSON data (runs the actual API extraction) |
| [productboard-insights](../productboard-insights/) | Analyzes customer feedback (notes), not features |
| [insight-dashboard](../insight-dashboard/) | Generates Excel dashboards from ProductBoard exports |
| [jira](../jira/) | Can cross-reference features with Jira tickets |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No Graph token found" | Run `python tools/outlook/outlook_api.py auth` |
| "Could not find Documents drive" | Check SharePoint site permissions |
| SharePoint download fails | Automatically falls back to local file |
| "No JSON data file found" | Run extraction: `python skills/dirks-skills/productboard-extraction/extract_features.py` |
| SSL errors on macOS | Automatic fallback to unverified SSL context |
| Import errors | Ensure `sys.path` includes `skills/productboard-features` |

## Changelog

- **2026-03-05** — Initial version: FeatureStore with pandas backend, hierarchy tree, filtering, enrichment, CLI
