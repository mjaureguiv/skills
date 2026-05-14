---
name: calculate-claude-productivity
description: Analyze git history to measure AI-assisted development productivity and generate executive reports
version: 1.0.0
---

# Calculate Claude Productivity

Analyze git history to measure AI-assisted development productivity and generate executive reports.

## Purpose

This skill analyzes a folder or repository to calculate:
- How much time Claude (AI) spent coding
- How much time the human spent prompting/reviewing
- Lines of code delivered
- Productivity multiplier vs traditional development

## When to Use

- User asks "how long did it take to build X"
- User wants productivity metrics for a project
- User needs to justify AI-assisted development to stakeholders
- User asks for "Claude productivity" or "development statistics"

## Analysis Process

### Step 1: Gather Git History

```bash
# Get all commits related to the folder/feature
git log --all --format="%H %ai %s" -- [folder-path]

# Get commits with line counts
git show [commit-hash] --numstat --format=""
```

### Step 2: Analyze File Timestamps

```bash
# Check file modification times for session duration
find [folder] -type f \( -name "*.py" -o -name "*.js" -o -name "*.html" \) \
  -exec stat -f "%Sm %N" -t "%Y-%m-%d %H:%M" {} \;
```

### Step 3: Calculate Metrics

1. **Calendar Duration**: First commit date → Last commit date
2. **AI Coding Time**: Sum of session durations (based on file timestamps within commits)
3. **Human Time**: Estimate ~30% of AI time (prompting, reviewing, testing)
4. **Lines Delivered**: Total lines in final codebase
5. **Traditional Estimate**: Lines ÷ 50 lines/hour = developer hours

### Step 4: Generate Reports

#### Executive Summary (for managers)

```markdown
## [Project Name] - Executive Summary

| Metric | Value |
|--------|-------|
| **Human time invested** | ~X hours |
| **Code delivered** | X,XXX lines |
| **Calendar time** | X weeks (X% of PM's time) |
| **Traditional dev estimate** | X-X weeks full-time |

**Bottom line:** X hours of PM prompting → working prototype that would take a developer XXX+ hours.
```

#### Detailed Timeline (for detailed analysis)

```markdown
## Timeline Overview

> **Note:** The times below represent Claude's active coding sessions based on git commits and file timestamps. The human (PM) spent approximately **X hours** providing prompts and reviewing outputs, while Claude spent **~X hours** generating code.

| Date | Time | Activity | Lines Changed |
|------|------|----------|---------------|
| YYYY-MM-DD | HH:MM - HH:MM | Description | ~X hours |
| **Total** | | | **~X hours** |

**Human vs AI effort:**
- **Human (PM):** ~X hours (prompting, reviewing, testing)
- **Claude (AI):** ~X hours (coding, debugging, documentation)
- **Ratio:** 1 hour human input → X hours AI output
```

## Estimation Formulas

### AI Coding Time
- Measure time span between first and last file modification in a commit session
- Sessions are grouped by day unless timestamps show continuous work

### Human Time Estimate
- **Rule of thumb**: Human time ≈ 25-35% of AI coding time
- Breakdown:
  - Prompting: 10-15% of AI time
  - Reviewing: 10-15% of AI time
  - Testing: 5-10% of AI time

### Traditional Development Estimate
- Average developer: ~50 lines of production code per hour
- Traditional estimate = Total lines ÷ 50
- Add 20% for testing, documentation, meetings

### Productivity Multiplier
- Multiplier = Traditional estimate ÷ Human time invested
- Typical range: 10x - 20x for AI-assisted development

## Example Output

When user asks: "How long did it take to create the SPM-client prototype?"

Provide:
1. **Executive Summary** (always first, for quick consumption)
2. **Detailed Timeline** (if user wants more detail)
3. **Methodology note** (explain how estimates were calculated)

## Key Messages for Stakeholders

- AI doesn't replace developers, it multiplies PM/analyst productivity
- Human time is spent on high-value activities (requirements, decisions, testing)
- AI handles repetitive coding, boilerplate, and iteration
- Result: Working prototypes in hours instead of weeks
