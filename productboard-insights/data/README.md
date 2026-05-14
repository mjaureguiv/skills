# ProductBoard Data

This folder contains ProductBoard notes exports for analysis.

## Getting Fresh Data

The data file should be refreshed periodically to include latest customer feedback:

1. **Login to ProductBoard** via SSO:  
   https://signavio.productboard.com

2. **Download the export** (must be logged in first):  
   https://signavio.productboard.com/api/notes/export?export_type=with_features&strip_html=true

3. **Save as**: `notes-export.csv` in this folder

## Current Data

| File | Description | Last Updated |
|------|-------------|--------------|
| `notes-export.csv` | Full customer insights export | See file timestamp |

## Note

The CSV file may be large (15-25MB). Consider refreshing monthly or before major planning sessions.
