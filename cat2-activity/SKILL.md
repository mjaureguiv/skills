---
name: cat2-activity
description: Automate CAT2 Activity Recording - fill your weekly time tracking in bulk
version: 1.1.0
user-invocable: true
author: Maryna Schedl
---

# CAT2 Activity Recording Automation

Fill your SAP CAT2 time recording in bulk - no more clicking day by day!

---

## Quick Start

Just run:
```
/cat2
```

Claude will:
1. Open CAT2 in a browser
2. **Read YOUR available categories** from CAT2
3. **Ask you to choose** which category to use
4. Fill all work days automatically

---

## How It Works

1. Opens CAT2 via Playwright browser automation
2. **Dynamically discovers YOUR categories** from the task list
3. **Presents your categories** for selection in Claude
4. Clicks each work day (Mon-Fri)
5. Sets the selected category to 100%
6. Autosave handles the rest

**Note:** Categories are NOT hardcoded - they come from YOUR CAT2 profile!

---

## Prerequisites

**Required MCPs:**
- `playwright` - Browser automation (install via `/install-mcps`)

**Your CAT2 Profile:** The skill reads whatever categories are available in your profile.

---

## Friday Automation

A reminder runs every **Friday at 4:30 PM** via macOS notification.

**To set up:**
```bash
launchctl load ~/Library/LaunchAgents/com.pm-agent.cat2-weekly.plist
```

**To disable:**
```bash
launchctl unload ~/Library/LaunchAgents/com.pm-agent.cat2-weekly.plist
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Save failed" | Some days already have 100% (vacation) - these are skipped |
| Browser not opening | Restart Claude Code to reload Playwright MCP |
| Wrong profile | Click "Switch profile" in CAT2 before running |
| Categories not showing | Make sure you're logged into CAT2 |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-04-24 | v1.1.0: Dynamic category discovery from CAT2 |
| 2026-04-24 | v1.0.0: Initial POC with Playwright automation |
