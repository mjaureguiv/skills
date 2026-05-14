---
name: partner-refresh
description: Review and update the Partner Expert knowledge base for freshness. USE THIS SKILL when the user wants to check which partner documents are stale, update reference files with new document versions, or perform a periodic review of the partner knowledge base. Also use when the user says "partner refresh", "update partner docs", or "check partner freshness."
---

# Partner Refresh

You help keep the Partner Expert knowledge base current by identifying stale documents and guiding the user through updates.

## When to Run

- **Quarterly** (recommended) — or whenever the user suspects something has changed
- **After major SAP events** (Sapphire, TechEd, semester planning) when many docs get updated
- **When a new partner is onboarded or an existing one changes status**

## Refresh Workflow

### Step 1: Check Freshness

Read `partner-expert/references/link-registry.md` and identify:

1. **Critical (red)**: ⭐ [MUST] docs not reviewed in >60 days
2. **Stale (yellow)**: Any docs not reviewed in >90 days
3. **Deprecated**: Docs marked deprecated — verify if still relevant or remove

Present results sorted by urgency:
```
🔴 CRITICAL — [MUST] docs overdue for review:
  #1  SAP BBP Strategy PPT — last reviewed 2026-03-25 (X days ago)
  ...

🟡 STALE — Needs review:
  #5  Public Overview: Open Ecosystem — never reviewed
  ...

✅ CURRENT — Recently reviewed:
  ...
```

### Step 2: Guide the Update

For each document the user wants to update:

1. Ask: "Download the latest version and say 'read my latest download'"
2. Read the new document
3. Compare with what's currently in the reference file
4. Update the reference file with new/changed content
5. Update `link-registry.md` with new `Last Reviewed` date and status

### Step 3: Summary

After updates, show:
- How many docs were refreshed
- Which reference files were updated
- Remaining stale docs for next time

## Working Directory

```
skills/partner/partner-refresh/temp/
```
