# CLAUDE.md - Insight Feature Analysis Skill

## Purpose
Automate the extraction, deduplication, and feature mapping of customer insights for SAP Signavio licensing and user management.

## Workflow
1. Accepts a list of insights (numbered or free-form)
2. Deduplicates and summarizes insights
3. Maps each unique insight/group to a feature
4. Outputs a markdown table with mapping

## File Organization
- temp/ : For intermediate and output files (e.g., insight_feature_table.md)
- README.md : Human documentation
- CLAUDE.md : Copilot/Claude instructions

## Quality Checklist
- [ ] Deduplication logic robust
- [ ] Features actionable and non-overlapping
- [ ] Output table clear and complete
- [ ] Temp files in temp/
- [ ] README and CLAUDE.md updated

## Changelog
| Date | Contributor | Change |
|------|-------------|--------|
| 2026-02-20 | Copilot | Initial creation |
