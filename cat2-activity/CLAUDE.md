> This file contains instructions for Claude, not for humans.
> See SKILL.md for user-friendly documentation.

---

# CAT2 Activity Recording - Claude Instructions

You automate CAT2 time recording using Playwright browser automation.

---

## CRITICAL: Dynamic Category Discovery

**DO NOT hardcode categories!** Each user has different categories based on their CAT2 profile.

You MUST:
1. Open CAT2 first
2. Read categories from the task list
3. Present ONLY those categories to the user
4. Fill with user's selection

---

## Before Starting

Ensure Playwright MCP is available. Check for `mcp__playwright__*` tools.

If not available, tell the user to restart Claude Code.

---

## Main Workflow

### Step 1: Open CAT2

```javascript
await mcp__playwright__browser_navigate({
  url: "https://sapit-home-prod-004.launchpad.cfapps.eu10.hana.ondemand.com/site#cat2activityrecording-Display"
});
```

### Step 2: Wait and take snapshot to discover categories

```javascript
await mcp__playwright__browser_wait_for({ time: 2 });
await mcp__playwright__browser_snapshot();
```

### Step 3: Extract categories from snapshot

Look in the snapshot for the task list. Categories appear in patterns like:

```yaml
- list [ref=...]:
  - listitem: Administrative
  - listitem: Personal education
  - listitem: Development | Project Name (cPro ID: XXXXX)
  - listitem: Product Management | Project Name (cPro ID: XXXXX)
  - listitem: Vacation
```

**Extract ALL category names** you find - these are the user's available categories.

### Step 4: Ask user to choose (if not specified in arguments)

Use AskUserQuestion with the ACTUAL categories found:

```javascript
// Example - use real categories from snapshot!
{
  "questions": [{
    "question": "Which category should I fill for all work days?",
    "header": "CAT2 Category",
    "multiSelect": false,
    "options": [
      { "label": "Product Management | SAP Signavio Dodo", "description": "cPro ID: 2470467" },
      { "label": "Development | SAP Signavio Dodo", "description": "cPro ID: 2470466" },
      { "label": "Administrative", "description": "General admin tasks" },
      { "label": "Personal education", "description": "Training, learning" }
    ]
  }]
}
```

### Step 5: Run bulk fill script with selected category

Use `browser_run_code` - pass the selected category name:

```javascript
async (page) => {
  const frame = page.frameLocator('iframe[title="Application"]');

  // Calculate work days for current month
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth(); // 0-indexed
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const workDays = [];
  for (let day = 1; day <= daysInMonth; day++) {
    const date = new Date(year, month, day);
    const dayOfWeek = date.getDay();
    if (dayOfWeek !== 0 && dayOfWeek !== 6) { // Not weekend
      workDays.push(day);
    }
  }

  // USER'S SELECTED CATEGORY - replace with actual selection!
  const category = "SELECTED_CATEGORY_NAME_HERE";

  let processed = 0;
  let skipped = 0;

  for (const day of workDays) {
    try {
      // Click day
      await frame.getByText(day.toString(), { exact: true }).first().click();
      await page.waitForTimeout(400);

      // Check current allocation
      const tasksText = await frame.locator('text=/\\d+%\\s*\\/\\s*100%/').first().textContent();
      const currentPercent = parseInt(tasksText.match(/(\d+)%/)?.[1] || '0');

      if (currentPercent < 100) {
        // Find and click the category
        const task = frame.locator(`text=${category}`).first();
        if (await task.isVisible({ timeout: 1000 })) {
          await task.click();
          await page.waitForTimeout(300);
          processed++;
        } else {
          skipped++;
        }
      } else {
        skipped++; // Already 100% (vacation, etc.)
      }
    } catch (e) {
      skipped++;
    }
  }

  return { processed, skipped, category, month: month + 1, year };
}
```

---

## Handling User Arguments

If user specifies category in command (e.g., `/cat2 Product Management`):
- Search for matching category in the discovered list
- Use fuzzy matching: "PM" → "Product Management | ..."
- If no match, show all options and ask

---

## Error Handling

### "Save failed" or ">100% activity"
Day already has 100% allocated - script skips these automatically.

### Browser closed
Re-navigate to CAT2 URL.

### Category not found
Show user the available categories and ask them to choose.

---

## Response Format

After filling, report:

```
✅ CAT2 filled for [Month Year]

| Metric | Value |
|--------|-------|
| Days processed | X |
| Days skipped | Y (already filled/vacation) |
| Category | [Selected Category] |

Your time recording is complete!
```

---

## Quick Reference

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Open CAT2 |
| `browser_snapshot` | Get categories & element refs |
| `browser_click` | Click days/tasks |
| `browser_run_code` | Bulk automation |
| `browser_wait_for` | Wait for page load |
| `browser_take_screenshot` | Visual confirmation |
