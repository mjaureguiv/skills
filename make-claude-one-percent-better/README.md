# make-claude-one-percent-better

Delivers one personalized micro-improvement to your Claude Code workflow each week.

## What This Does

Audits your Claude Code setup and suggests one small, high-impact change:
- **CLAUDE.md quality** — missing sections, stale content, bloated instructions
- **Skills hygiene** — missing frontmatter, no triggers, files over 500 lines
- **Settings gaps** — no hooks configured, missing environment variables
- **Workflow patterns** — no session continuity, missing startup commands

Philosophy: compounding tiny wins > big overhauls.

## Why This Exists

Claude Code setups drift silently — stale CLAUDE.md, skills missing triggers, no hooks configured. This automates the "review your setup" discipline most people skip.

## Usage

Run at the start of your week:

```
/make-claude-one-percent-better
```

Focus on a specific area:

```
/make-claude-one-percent-better skills
/make-claude-one-percent-better claude-md
/make-claude-one-percent-better settings
```

Force a new suggestion (even if you already got one this week):

```
/make-claude-one-percent-better --force
```

## Example Output

```
ONE PERCENT BETTER — Week of 2026-02-23
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THIS WEEK'S IMPROVEMENT: Add allowed-tools to your transcript-to-notes skill

WHY IT MATTERS: Without allowed-tools, Claude has to guess which tools your
skill needs. Adding explicit tool permissions makes execution faster and
prevents unexpected tool calls.

THE CHANGE:
  File: ~/.claude/skills/transcript-to-notes/SKILL.md
  What: Add `allowed-tools: [Read, Glob, Grep, Write, AskUserQuestion]`
        to the YAML frontmatter

EFFORT: < 5 min

YOU'LL KNOW IT WORKED WHEN: Running /transcript-to-notes no longer
prompts for tool permissions mid-execution.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your wins: 3 applied | streak: 3 weeks
```

## Wins Tracking

Your improvement history is saved to `~/.claude/make-claude-one-percent-better/wins.md`. Each suggestion is logged with date, category, and status. The skill checks this file to avoid repeating suggestions and to maintain your streak.

## Support

Questions or issues? Reach out in #claude-code-help

---

**Original Author**: Aviral Vaid (LeanIX Product Management)
**Category**: Meta / Workflow
**Integrated from**: [LeanIX PM Marketplace](https://github.tools.sap/LeanIX/LeanIX-PM-Marketplace)
