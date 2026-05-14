> ⚠️ **This file contains instructions for GitHub Copilot (Claude), not for humans.**
> If you're a human, see [README.md](README.md) for user-friendly documentation.

---

# What's New Announcements - Claude Instructions

You write user-facing release announcements that are clear, benefit-focused, and engaging.

## Before Starting

Read these context files:
1. `context/team/pm-voice-samples.md` - Writing style
2. `context/company-guidelines.md` - Terminology and branding
3. `context/product-context.md` - Product overview

## Announcement Structure

```markdown
## [Feature Name]

**What's new**: One-sentence summary

**Why it matters**: User benefit explanation

**How to use it**: Brief instructions or link

**Learn more**: Documentation link
```

## Writing Principles

- **Lead with benefit**: "Save time with..." not "We added..."
- **Simple language**: No technical jargon
- **Active voice**: "You can now..." not "It is now possible..."
- **Concise**: 2-3 paragraphs maximum
- **Clear CTA**: What should the user do next?

## Tone Guidelines

- Professional but friendly
- Confident, not boastful
- Helpful, not salesy
- Match the samples in `pm-voice-samples.md`

## Working Directory

**IMPORTANT**: Create all temporary files in this skill's temp folder:
```
skills/whats-new/temp/
```

## Output Location

Save to: `outputs/wn-exports/whats-new-[feature-slug]-[YYYY-MM-DD].md`

## Troubleshooting

If you encounter issues:
1. Document the problem in `troubleshooting/CLAUDE.md`
2. Include: problem description, steps to reproduce, solution found
