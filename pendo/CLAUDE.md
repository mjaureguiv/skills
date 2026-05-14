> ⚠️ **This file contains instructions for GitHub Copilot (Claude), not for humans.**
> If you're a human, see [README.md](README.md) for user-friendly documentation.

---

<!-- Last verified: April 2026 — contact agnel.joby@sap.com if information seems stale -->

# Pendo Analytics - Claude Instructions

This skill answers questions about how to apply Pendo analytics in SAP Signavio features.
It covers both the PM perspective (what to measure, how to plan tagging, how to use the dashboard)
and the Engineering perspective (how to install, configure, and instrument code).

If the question is ambiguous, show the topic menu and ask the user to specify.

**PM Topics:**
- **What to Measure** — Use case taxonomy: adoption, engagement, retention, funnels, journeys, KPIs
- **Feature Tagging (PM)** — Planning what to tag, naming conventions, auto-tagging vs. manual
- **Analytics Tools** — Data Explorer, Funnels, Paths, Retention, Dashboards, PES — which tool for which question
- **Metadata & Segmentation** — What visitor/account fields are available for filtering and segments
- **Maintaining Pendo** — Keeping pages and features up to date as product evolves

**Engineering Topics:**
- **Setup & Configuration** — Package install, integration paths (Global Header vs. Direct Import), config params
- **Event Tracking (trackPendo)** — Code, when to use vs. feature tags, where results appear
- **CSS Selector Best Practices** — data-analytics-id standard, what to avoid, HTML patterns
- **Feature Tagging (Eng)** — Auto-tagging setup, Visual Design Studio, CSS selector method

**Both:**
- **Key Contacts & Resources** — Who to contact, wiki links, GitHub, dashboard URL

**Answer Style:**
- Be concise but complete
- Include code examples where relevant
- Provide actionable next steps
- Note when something requires PM–Eng collaboration

---

# PM SIDE

## 1. What to Measure — Use Case Taxonomy

Use this as a starting point when planning what to track in your feature. Align with your Eng team on which events need `trackPendo` calls vs. which can be covered by feature tagging.

### Feature Usage & Adoption
| Use Case | What It Tells You |
|----------|-------------------|
| Feature Adoption Rate | How many users start using a feature over time — assess success of launches |
| Adoption Over Time | Week-over-week / month-over-month trends |
| Time to Value (TTV) | How quickly users achieve first value after a feature launches |
| Retention by First Use of Core Features | Does early engagement with feature X correlate with long-term retention? |

### User Engagement & Retention
| Use Case | What It Tells You |
|----------|-------------------|
| Active Users (DAU/WAU/MAU) | Unique users per period; DAU/MAU ratio = stickiness |
| Session Duration | Average time per session — depth of engagement |
| Sessions per User | How often users return — stickiness signal |
| Retention & Return Rate | Are users coming back after N days? Critical for churn analysis |
| Stickiness by Feature | DAU/WAU/MAU scoped to a specific feature |
| Frustration Metrics | Rage clicks, dead clicks, U-turns — surfaces UX pain points |

### Workflow & Funnel Analysis
| Use Case | What It Tells You |
|----------|-------------------|
| Funnel Analysis | Completion rates across multi-step workflows |
| Path Analysis | Sequences of actions users take — reveals navigation patterns and bottlenecks |
| Drop-off / Friction | Where users abandon a process — critical for improving completion |
| Workflow Journeys | End-to-end adoption across multiple features/modules |

### Release & Cross-Feature
| Use Case | What It Tells You |
|----------|-------------------|
| Release Impact Analysis | How a new feature or update changes behavior (useful for beta rollouts) |
| Cross-Feature Interaction | Does using feature A increase adoption of feature B? |
| Cross-Product Analytics | How users interact across multiple Signavio products |

### Reporting & KPIs
| Use Case | What It Tells You |
|----------|-------------------|
| Custom Events & KPIs | Track product-specific events aligned to your success metrics |
| Cohort Analysis | Retention/behavior over time by signup date, plan, or activity |
| Behavioral Segmentation | Group users by actions/frequency — power users vs. inactive |
| Forecasting & Trend Analysis | Use historical data to predict future adoption patterns |

---

## 2. Feature Tagging — PM Perspective

### How to Plan What to Tag

1. **Define your KPIs first** — What question do you need to answer? (e.g., "Are users discovering feature X after onboarding?")
2. **Map KPIs to events** — Which user actions answer that question? (page views, button clicks, workflow completions)
3. **Decide the tracking method** for each event:
   - Clickable UI element that's stable → Feature Tag (no code needed)
   - Async operation / workflow completion / anything without a stable click target → `trackPendo` (requires Eng)
4. **Document your tracking plan** — maintain a shared sheet: feature name, selector/event name, method, owner, status
5. **Coordinate with Eng** on `data-analytics-id` attributes and `trackPendo` calls before sprint starts

### Naming Conventions

Consistent naming makes dashboards and reports readable across teams.

**Pages:**
```
Format:  [Product Area] | [Page Name]
Example: Dashboard | Home
Example: Process Repository | Diagram Editor
```

**Features:**
```
Format:  [Page] | [Action]
Example: Dashboard | Search Button

Format:  [Page] | [Element Type] | [Name]
Example: Process Repository | Toolbar | Export Button
```

### Auto-tagging vs. Manual — When to Use Which

| Method | Best For | Requires Eng? |
|--------|----------|---------------|
| Auto-tagging | Scalable bulk coverage once `data-testid`/`data-pa` attributes exist | Yes (attributes must be in code) |
| Visual Design Studio | Quick tagging of stable, visible UI elements | No |
| CSS Selector / trackPendo | Precise targeting or non-UI events | Yes (CSS attributes or code) |

---

## 3. Analytics Tools — Which Tool for Which Question

| Question You're Asking | Tool to Use |
|------------------------|-------------|
| "How many users clicked X in the last 30 days?" | **Data Explorer** |
| "Are users coming back to use this feature?" | **Retention** |
| "Where do users drop off in this multi-step flow?" | **Funnels** |
| "What do users do before/after reaching this page?" | **Paths** |
| "How long does it take users to complete this workflow?" | **Workflows / Journeys** |
| "How do different user segments compare?" | **Data Explorer** + **Segments** |
| "What's the overall product health?" | **PES (Product Engagement Score)** |
| "I need a shareable dashboard for my team/leadership" | **Dashboards** |

### Common Dashboard Setups

- **Feature adoption tracking**: Feature click counts, adoption rate over time, funnel from discovery → first use → repeat use
- **Release impact**: Compare behavior before/after a release using cohort or date filters
- **Roadmap evidence**: Funnel drop-offs and path patterns to surface UX problems
- **Executive readout**: QoQ trends, top growing/declining features, account-level engagement

Pendo Dashboard: https://app.eu.pendo.io/s/4593846254108672/home

---

## 4. Metadata & Segmentation

All metadata is collected automatically by the `ux-analytics-kit` — no extra Eng work needed. Use it in Pendo under **People → Segments** to filter any report.

### Visitor Metadata (filter by user type)

| Field | Use For |
|-------|---------|
| `isAdmin` | Compare admin vs. regular user behavior |
| `isGuestUser` | Filter out or isolate guest user activity |
| `country` | Geographic breakdown of feature usage |
| `prefersDarkMode` / `reducedMotion` | Accessibility usage patterns |
| `acceptedTermsDate` | Cohort users by onboarding date |
| `screenWidth` / `screenHeight` | Viewport breakdown for responsive features |

### Account Metadata (filter by customer/tenant)

| Field | Use For |
|-------|---------|
| `licenses` | Compare behavior by license tier |
| `featurePackages` | Isolate usage for specific feature packages |
| `tenantName` | Account-level analysis (anonymized — no personal names) |
| `groups` | Filter by user group within a tenant |
| `platform` | Platform-specific usage breakdown |
| `valueAccelerator` | Isolate VAL package customers |

**Note**: Pendo data is anonymized — individual user names and workspace names are NOT visible, only the metadata fields above.

---

## 5. Maintaining Pendo Over Time

Pendo pages and feature tags require manual upkeep as your product evolves.

### When a Page URL Changes

1. Go to the Page view in Pendo → **Include Rules**
2. **Add** the new URL rule — do not remove the old one (keeps historical data continuous)
3. URL pattern: use `//*` instead of `https://editor.signavio.com`, then append the path

### When a New Page or Feature Is Added

1. **Page list** → find a similar existing page → **Clone**
2. Update name (follow naming convention) and replace Include Rule with new URL
3. For each Feature on that page: **Clone Feature** → update name and page reference → Save

### How to Avoid the Maintenance Burden

- Use `trackPendo` for programmatic events rather than CSS-based feature tags where possible — more stable
- Add `data-analytics-id` attributes to new UI elements from the start — prevents selector drift
- Keep a shared tracking doc: feature name · selector or event name · owner · last verified date

---

# ENGINEERING SIDE

## 6. Setup & Configuration

### Package

```bash
npm install @signavio/ux-analytics-kit
```

- **GitHub**: `signavio/fiori-bellissima` → `libs/ux-analytics-kit`
- **Version**: Use **LTS** — not V1.1 (legacy)
- **API key**: Contact `agnel.joby@sap.com`

### Integration Path — Choose One

| Path | When | How |
|------|------|-----|
| **Via Global Header** | App already uses the SAP Signavio Global Header MFE | Pass `apiAnalyticsKey` + `isBanner` to `UXAnalyticsConfig` — everything handled automatically |
| **Direct Import** | App does not use Global Header | Call `UXAnalytics.enableUXAnalytics(config)` manually |

**Note**: If your app doesn't have the Global Header yet, integrate it first — contact the Hub team. Pendo cannot be added before GH integration on that path.

### Direct Import — Full Configuration

```javascript
import UXAnalytics from '@signavio/ux-analytics-kit'

UXAnalytics.enableUXAnalytics({
  trustArcScriptSrc: 'https://consent.trustarc.com/your-script.js',
  isBanner: true,        // true = show consent banner, false = preferences link only
  appDomain: 'yourappdomain.com',
  pendoAPIKey: 'your-pendo-api-key',
  userAccountID: 'tenantID'
})
```

| Param | Description |
|-------|-------------|
| `trustArcScriptSrc` | TrustArc consent script URL |
| `isBanner` | `true` = full banner on first visit; `false` = preferences link only |
| `appDomain` | Your application domain |
| `pendoAPIKey` | Pendo API key for your product (get from agnel.joby@sap.com) |
| `userAccountID` | Tenant/account identifier for the current user |

**Reference implementation**: `signavio/global-header` → `src/utils/pendoAnalyticsConfig.ts`

**Important**: Pendo only initializes after the user accepts cookie consent via TrustArc. The `ux-analytics-kit` handles this gate automatically — no extra code needed.

---

## 7. Event Tracking (trackPendo)

### Code

```javascript
import { trackPendo } from '@signavio/ux-analytics-kit'

trackPendo('event-name', { key: 'value', /* any custom properties */ })
```

- Event name: kebab-case string, e.g. `'diagram-export-completed'`
- Second arg: plain object with any metadata you want to attach

### When to Use trackPendo vs. Feature Tagging

| Scenario | Use |
|----------|-----|
| User clicks a stable, visible button | Feature Tag (no code — PM does it in Pendo UI) |
| Async operation completes (upload, export, API call) | `trackPendo` |
| Multi-step workflow reaches a key completion point | `trackPendo` |
| Form submission you want to attach data to | `trackPendo` with metadata |
| Navigation click in stable DOM | Feature Tag |

**Rule of thumb**: If there's no single stable click target, use `trackPendo`.

### Where to Verify

Pendo → **Product** → **Track Events**: https://app.eu.pendo.io/s/4593846254108672/trackevents

---

## 8. CSS Selector Best Practices

Pendo feature tags are saved as DOM selectors. If a selector breaks (CSS refactor, translation change, build hash), historical data gaps appear. Use only attributes that are stable by design.

### Preferred: data-analytics-id

```html
<!-- Format: noun.action (lowercase, dot-separated) -->
<button data-analytics-id="payment.submit">Submit Payment</button>
<button data-analytics-id="payment.cancel">Cancel</button>
<a data-analytics-id="nav.help">Help</a>
```

Why: tool-neutral (not Pendo-specific), survives class renames, translations, and rebuilds; grep-friendly.

### Also Acceptable

| Attribute | Format | Notes |
|-----------|--------|-------|
| `data-analytics-id` | `noun.action` | Preferred — SPG/tool-neutral standard |
| `data-pa` | descriptive string | Signavio-specific, widely used |
| `data-testid` | descriptive string | Shared with test automation |

### What to Avoid

| Pattern | Why It Breaks |
|---------|--------------|
| `.MenuItem_container__2Xd5-` | Hashed CSS-in-JS class — changes every build |
| `li:nth-child(2) > div > button` | Positional — breaks on any DOM restructure |
| `div:nth-child(2) > .list > div:nth-child(1)` | Deep positional path — extremely fragile |
| Text-content selectors | Break on copy changes and translations |

---

## 9. Feature Tagging — Engineering Steps

### Auto-Tagging (recommended for scale)

1. Add `data-testid` or `data-pa` attributes to UI elements in code
2. In Pendo: **Settings** → **Subscription Settings** → **Applications** → app → **Tagging & Guide Settings**
3. Add the attribute name under "Collect custom HTML attributes"
4. Enable **Automatic tagging with custom HTML Attributes** → select your attribute
5. Features appear in **Product → Features** within 24h — PM renames and assigns to product areas

### Visual Design Studio (no Eng work needed — PM driven)

Pendo → **Product** → **Features** → **Tag Feature** → enter URL → **Launch Designer** → click element → fill details → Save.
Requires accepted cookies in the Signavio app.

### Manual CSS Selector (Eng provides selector, PM enters in Pendo)

1. Eng: add `data-analytics-id` or `data-pa` attribute to the target element
2. PM: Pendo → **Product** → **Features** → **Create Feature** → **CSS Selector** → enter selector → **Test Rule** → Save

---

## 10. Key Contacts & Resources

| Topic | Contact |
|-------|---------|
| Pendo API key, onboarding, setup questions | agnel.joby@sap.com (Joby Agnel) |
| ux-analytics-kit architecture decisions | Dominik Srednicki, Maximilian Kautetzky, Sebastian Friedrich |

### Internal Wiki

| Resource | Space | Page ID |
|----------|-------|---------|
| Main Pendo integration guide | SIGAVENGERS | 5695885331 |
| Pendo Analytics Playbook | PRODEX | 5927154224 |
| UX Analytics Kit + TrustArc technical guide | SIGDS | 4287244025 |
| TrustArc step-by-step guide | SIGDS | 4505802844 |
| Pendo metadata reference | SIGDS | 4401494290 |
| Pendo Q&A | SIGDS | 4093874492 |
| uxAnalyticsKit technical Q&A | SIGDS | 4224650186 |
| Pendo best practices and champions | SIGDS | 5156052406 |
| Pendo Tracking Selectors standard | SPG | 5240678208 |

Open any page: `https://wiki.one.int.sap/wiki/spaces/{SPACE}/pages/{PAGE_ID}/`

### GitHub

| Path | Contents |
|------|---------|
| `signavio/fiori-bellissima` → `libs/ux-analytics-kit` | Package source |
| `signavio/global-header` → `src/utils/pendoAnalyticsConfig.ts` | Reference implementation |

### Dashboard

- EU instance: https://app.eu.pendo.io/s/4593846254108672/home
- Track Events: https://app.eu.pendo.io/s/4593846254108672/trackevents
