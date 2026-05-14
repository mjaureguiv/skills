# Calculate Claude Productivity

Analyze git history to measure AI-assisted development productivity and generate executive reports for stakeholders.

## What It Does

This skill analyzes a project folder or repository to produce:

- **Executive Summary**: One-table overview for managers
- **Detailed Timeline**: Commit-by-commit breakdown of AI coding sessions
- **Productivity Metrics**: Human vs AI time, lines delivered, ROI

## How to Use

Ask Claude to analyze any folder or feature:

```
Use skill calculate-claude-productivity to calculate how much time was used for creation of feature-categorization-wizard
```

```
Use skill calculate-claude-productivity to analyze the SPM-client prototype
```

```
Calculate productivity stats for skills/powerpoint
```

```
How long did it take to build this scenario?
```

## Sample Output

### Executive Summary

| Metric | Value |
|--------|-------|
| **Human time invested** | ~6 hours |
| **Code delivered** | 6,800 lines |
| **Calendar time** | 3 weeks (4% of PM's time) |
| **Traditional dev estimate** | 2-3 weeks full-time |

**Bottom line:** 6 hours of PM prompting → working prototype that would take a developer 100+ hours.

### Detailed Timeline

| Date | Time | Activity | Lines Changed |
|------|------|----------|---------------|
| 2026-02-23 | 12:56 - 16:45 | Main prototype creation | ~4 hours |
| 2026-03-02 | 11:26 - 20:13 | Feature enhancements | ~9 hours |
| **Total** | | | **~13 hours** |

## Key Metrics Explained

| Metric | Description |
|--------|-------------|
| **Human time** | Time PM spent prompting, reviewing, testing |
| **AI time** | Claude's active coding time (from git/file timestamps) |
| **Productivity multiplier** | Traditional dev time ÷ Human time invested |
| **Lines per human-hour** | Code output relative to human investment |

## Web Dashboard

For an interactive experience, run the web dashboard:

```bash
cd skills/calculate-claude-productivity
pip install flask
python app.py
```

Then open **http://localhost:5050** in your browser.

Features:
- Browse all skills and scenarios
- Click to view productivity metrics
- **Copy Text** button to copy markdown report to clipboard
- Visual executive summary with key metrics

![Dashboard Preview](temp/dashboard-preview.png)

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-03-05 | i745835 | Initial skill creation |
