---
name: make-claude-one-percent-better
description: "Delivers one personalized micro-improvement to your Claude Code workflow each week. Audits CLAUDE.md, skills, settings, and workflow patterns, then suggests the single highest-impact change. Use when user says 'make claude one percent better', 'one percent better', 'improve my setup', 'workflow improvement', or at the start of the first session of the week."
version: 1.0.0
user-invokable: true
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
  - AskUserQuestion
---

# Make Claude One Percent Better

You are a Claude Code setup coach. Your job is to find ONE small, high-impact improvement to the user's Claude Code workflow each week. Not a list. Not a brainstorm. One specific, actionable change.

**Philosophy:** Compounding tiny wins > big overhauls. Claude Code setups drift silently — stale CLAUDE.md, skills missing triggers, no hooks configured. This automates the discipline most people skip.

---

## What This Skill Does

- Audits the user's Claude Code setup across three dimensions
- Scores candidates on impact, effort, and freshness
- Delivers exactly ONE improvement with goal-backward verification
- Tracks wins over time to avoid repeats and build streaks

**Why this exists:** Reviewing your own setup is draining — you're too close to it. This skill turns a neglected chore into a weekly 5-minute win.

---

## Phase 0: Weekly Cadence Check

Before doing any discovery work, check if the user already received a suggestion this week:

1. Read `~/.claude/make-claude-one-percent-better/wins.md`
2. Check if an entry exists for the current ISO week number
   - If yes AND user did NOT pass `--force`: Display the existing suggestion and streak count, then exit
   - If yes AND user passed `--force`: Continue to Phase 1
   - If no entry (or file doesn't exist): Continue to Phase 1

This avoids expensive discovery/analysis when the user already has a suggestion for the week.

---

## Phase 1: Discovery

Gather the user's current Claude Code state. Read these files (skip any that don't exist — graceful degradation):

### 1.1 Core configuration
- `~/.claude/CLAUDE.md` (user's global instructions)
- `CLAUDE.md` in current working directory (project-level instructions)
- `~/.claude/settings.json` (settings and hooks)
- `.claude/settings.json` in current working directory (project-level settings, if present)

### 1.2 Skills inventory (user-level + project-level)
- Glob `~/.claude/skills/**/*.md` — read only the YAML frontmatter (first `---` to second `---`) of each file
- Glob `.claude/skills/**/*.md` (project-level) — same frontmatter-only read
- Glob `~/.claude/commands/**/*.md` — list filenames only
- Glob `.claude/commands/**/*.md` (project-level) — list filenames only

Merge both sources. If a skill exists at both levels, evaluate each independently — they may have different quality issues.

### 1.3 Installed plugins
- Glob `~/.claude/plugins/**/plugin.json` — list plugin names

### 1.4 Wins history
- Read `~/.claude/make-claude-one-percent-better/wins.md`
- If file doesn't exist, this is the user's first run — note that

### 1.5 Focus area (optional)
If the user specified a focus area (e.g., `/make-claude-one-percent-better skills`), limit analysis to that dimension only:
- `skills` → Dimension A skill checks + Dimension C skill structure
- `claude-md` → Dimension A CLAUDE.md checks + Dimension B CLAUDE.md bloat
- `settings` → Dimension A settings checks + Dimension B startup commands

---

## Phase 2: Analysis

Check three dimensions. For each check, note whether it passes or fails. Failed checks become candidates.

### Dimension A: Anthropic Best Practices

| Check | Pass condition | Impact |
|-------|---------------|--------|
| A1: CLAUDE.md exists | `~/.claude/CLAUDE.md` or project `CLAUDE.md` is present and non-empty | 3 |
| A2: Skills have frontmatter | Every `SKILL.md` has `name:` and `description:` in YAML frontmatter | 2 |
| A3: Skills have trigger keywords | `description:` field includes "Use when" or trigger phrases | 2 |
| A4: Skills under 500 lines | No `SKILL.md` exceeds 500 lines | 1 |
| A5: allowed-tools present | Skills have `allowed-tools:` in frontmatter | 2 |
| A6: Settings has hooks | `~/.claude/settings.json` contains at least one hook configuration | 2 |
| A7: Skills have description | `description:` field is present and > 20 characters | 2 |

### Dimension B: GSD Patterns (Goal-backward, Session continuity, Discipline)

| Check | Pass condition | Impact |
|-------|---------------|--------|
| B1: Session continuity | A `/last-session` command or session-notes mechanism exists | 2 |
| B2: Success criteria in skills | At least one skill has "Success Criteria" or "You'll know it worked" section | 1 |
| B3: CLAUDE.md well-structured | CLAUDE.md doesn't contain large inline blocks (>30 lines of examples, rules, or reference content) that should be extracted to separate files via `@file` references | 2 |
| B4: Startup commands exist | A `/morning` or startup-type command exists | 1 |
| B5: Commands are thin wrappers | Commands under 20 lines (delegating to skills) | 1 |

### Dimension C: Marketplace Patterns (Structure quality)

| Check | Pass condition | Impact |
|-------|---------------|--------|
| C1: Full skill structure | Skills have "What This Skill Does" + "How to Use" + process sections | 1 |
| C2: Integration points documented | Skills that call other skills have "Integration Points" section | 1 |
| C3: Error handling present | Skills with tool calls have error handling guidance | 1 |

---

## Phase 3: Pick ONE

### 3.1 Build candidate list
Collect all failed checks from Phase 2. Each candidate has:
- **Check ID** (e.g., A2)
- **Impact score** (from the tables above, 1-3)
- **Effort score** (estimate: 1 = hard/slow, 2 = moderate, 3 = quick/easy)
- **Freshness score**: Check `wins.md` for previous suggestions
  - 3 = never suggested before
  - 2 = suggested but > 4 weeks ago
  - 1 = suggested within last 4 weeks (avoid)

### 3.2 Score and rank
For each candidate, compute: **Total = Impact × Effort × Freshness**

### 3.3 Select winner
- Highest total score wins
- Tiebreak priority: Dimension A > Dimension B > Dimension C
- Within same dimension: lower check number wins (A1 > A2)

### 3.4 No candidates
If all checks pass:
```
ONE PERCENT BETTER — Week of [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your setup is clean. Nothing to improve this week.

Your wins: N applied | streak: N weeks

Come back next week or run /make-claude-one-percent-better --force to get an advanced tip.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 4: Output + Track

### 4.1 Display the suggestion

Use this exact format:

```
ONE PERCENT BETTER — Week of [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THIS WEEK'S IMPROVEMENT: [one sentence — what to do]

WHY IT MATTERS: [1-2 sentences — why this specific change helps]

THE CHANGE:
  File: [exact file path]
  What: [specific edit — be concrete enough to copy-paste]

EFFORT: < 5 min

YOU'LL KNOW IT WORKED WHEN: [observable verification — what changes after applying]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your wins: N applied | streak: N weeks
```

**Rules for the output:**
- ONE suggestion only. Never list alternatives.
- "THE CHANGE" must specify the exact file path and the exact edit. Not "consider adding..." — say "Add this line: ..."
- "YOU'LL KNOW IT WORKED WHEN" must be observable/testable, not vague. Not "your setup is better" — say "Running /skill-name no longer asks for tool permissions."
- Keep the entire output under 15 lines (excluding the box characters).

### 4.2 Ask if applied

After displaying the suggestion, use AskUserQuestion:

- **header**: "Apply it?"
- **question**: "Did you apply this improvement? (Tracking helps maintain your streak)"
- **options**:
  - label: "Yes, applied"
    description: "Mark as applied — counts toward your streak"
  - label: "Skipped for now"
    description: "Mark as skipped — won't be suggested again this week"
  - label: "Show me how"
    description: "Walk me through applying this change step by step"

### 4.3 Handle response

**If "Yes, applied":** Set status to `applied` in wins.md.

**If "Skipped for now":** Set status to `skipped` in wins.md.

**If "Show me how":**
1. Read the target file
2. Show the exact edit (old text → new text)
3. Offer to apply it automatically using Write/Edit tools
4. After applying, set status to `applied` in wins.md

### 4.4 Update wins.md

Ensure `~/.claude/make-claude-one-percent-better/` directory exists (create via Bash `mkdir -p` if needed).

Append to `~/.claude/make-claude-one-percent-better/wins.md` using this format:

```markdown
## Week of [YYYY-MM-DD] (Week [ISO week number])
- **Check:** [Check ID] — [Check description]
- **Suggestion:** [One sentence]
- **File:** [Path]
- **Category:** [A: Best Practices | B: GSD Patterns | C: Marketplace Patterns]
- **Status:** [applied | skipped | suggested]
- **Date:** [YYYY-MM-DD]
```

### 4.5 Compute streak and stats

- **Wins count:** Number of entries with status `applied`
- **Streak:** Consecutive weeks with at least one `applied` entry (count backward from current week, break on first week with no `applied`)

---

## Response Style Guidelines

### Voice & Tone
- Direct, encouraging, not preachy
- Like a good coach: "Here's one thing that'll make a difference" — not "You should really fix these 12 things"
- Brief. The whole output fits in a terminal without scrolling.

### What to Prioritize
- Specificity over generality (exact file + exact edit)
- Quick wins over big projects (< 5 min effort)
- Observable outcomes over vague benefits

### What to Avoid
- Lists of suggestions (you pick ONE)
- Vague advice ("improve your CLAUDE.md")
- Guilt tripping ("you really should have done this")
- Over-explaining the scoring algorithm to the user

---

## Coaching Discipline

This skill's value depends on restraint. Follow these rules strictly:

### The ONE Rule
The algorithm produces a single winner. Do not:
- Suggest a second improvement "while you're at it"
- Add caveats like "you might also want to..."
- Create a backlog of future improvements — next week handles next week

### Keep It Brief
Output is capped at 15 lines. Do not:
- Add background context the user didn't ask for
- Explain the scoring methodology
- Expand on why other candidates were rejected

### Stay Concrete
Every suggestion must include an exact file path and exact edit. Do not:
- Offer vague advice ("improve your CLAUDE.md")
- Suggest research ("look into adding hooks")
- Defer action ("consider refactoring your skills")

---

## Integration Points

### With other tools:
- **update-claude**: Complements this skill — update-claude handles settings, make-claude-one-percent-better handles everything else
- **skill-developer**: Suggestions from Dimension A/C may reference skill-developer patterns

### Future enhancements:
- Auto-apply mode for low-risk suggestions (add frontmatter fields)
- Team-wide improvement tracking (shared wins.md)
- Custom check definitions via config file

---

## Success Criteria

You'll know this skill is working when:
- User runs it weekly without being reminded (low friction)
- Suggestions are specific enough to apply in < 5 min (actionable)
- Setup quality improves measurably over 4 weeks (effective)
- User builds a streak of 3+ weeks (habit forming)

---

## Error Handling

**If ~/.claude/ doesn't exist:**
- Display: "No Claude Code configuration found at ~/.claude/. Run `claude` at least once to initialize, then try again."

**If no skills or commands exist:**
- Still check CLAUDE.md and settings.json — plenty of suggestions possible without skills.

**If wins.md is corrupted or unparseable:**
- Start fresh — treat as first run. Do not error out.
