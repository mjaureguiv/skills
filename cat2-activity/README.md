# CAT2 Activity Recording Automation

Automate your SAP CAT2 time recording - fill an entire month in seconds instead of clicking day by day.

## What It Does

- Opens CAT2 in your browser via Playwright automation
- **Reads YOUR available categories** directly from CAT2 (not hardcoded!)
- Lets you choose which category to fill
- Fills all work days (Mon-Fri) with 100% allocation
- Skips weekends and days already at 100% (vacation, etc.)

## Quick Start

```
/cat2
```

That's it! Claude handles the rest.

## How It Works

1. **Opens CAT2** - Navigates to SAP IT Launchpad → Activity Recording
2. **Discovers Categories** - Reads your personal task list (e.g., "Product Management | SAP Signavio Dodo")
3. **Asks You to Choose** - Presents YOUR categories via Claude's UI
4. **Bulk Fills** - Clicks each work day, sets 100% for your selected category
5. **Reports Results** - Shows how many days were filled vs. skipped

## Prerequisites

| Requirement | Purpose |
|-------------|---------|
| Playwright MCP | Browser automation |
| SAP SSO Session | Authentication to CAT2 |

**Install Playwright MCP:**
```
/install-mcps
```

## Example Output

```
✅ CAT2 filled for April 2026

| Metric | Value |
|--------|-------|
| Days processed | 11 |
| Days skipped | 11 (already filled/holidays) |
| Category | Product Management | SAP Signavio Dodo |

Your time recording is complete!
```

## Friday Reminder (Optional)

Set up a weekly reminder to run CAT2 every Friday at 4:30 PM:

```bash
# Enable
launchctl load ~/Library/LaunchAgents/com.pm-agent.cat2-weekly.plist

# Disable
launchctl unload ~/Library/LaunchAgents/com.pm-agent.cat2-weekly.plist
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Browser doesn't open | Restart Claude Code to reload Playwright MCP |
| "Save failed" errors | Days already at 100% are automatically skipped |
| Wrong categories shown | Switch profile in CAT2 before running |
| Authentication prompt | Your SAP SSO session expired - log in via browser |

## Technical Details

- Uses Playwright MCP for browser automation
- Leverages SAP's SSO passthrough (no credentials stored)
- Autosave is enabled in CAT2 - changes save automatically
- Works with any CAT2 profile/categories

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-04-24 | 1.1.0 | Dynamic category discovery from CAT2 |
| 2026-04-24 | 1.0.0 | Initial POC with Playwright automation |

## Champion

Maryna Schedl
