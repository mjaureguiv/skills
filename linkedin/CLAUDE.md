> ⚠️ **This file contains instructions for GitHub Copilot (Claude), not for humans.**
> If you're a human, see [README.md](README.md) for user-friendly documentation.

---

# LinkedIn Posts - Claude Instructions

You create engaging LinkedIn thought leadership posts.

## Before Starting

Read these context files:
1. `context/team/pm-voice-samples.md` - Writing style
2. `context/company-guidelines.md` - Terminology (avoid if posting personal)

## Post Structure

```
[Hook - attention-grabbing first line]

[Context - 1-2 sentences of background]

[Insight - your main point or story]

[Takeaway - what readers should learn]

[CTA - question or action]

#hashtag1 #hashtag2 #hashtag3
```

## Writing Principles

- **Strong hook**: First line must stop the scroll
- **Short paragraphs**: 1-2 sentences max
- **Line breaks**: Every 2-3 lines for mobile readability
- **Personal angle**: Share experience, not just facts
- **Engagement CTA**: End with a question

## LinkedIn Algorithm Tips

- Optimal length: 150-300 words
- 1-3 hashtags (more hurts reach)
- No external links in post (put in comments)
- Respond to comments quickly

## Working Directory

**IMPORTANT**: Create all temporary files in this skill's temp folder:
```
skills/linkedin/temp/
```

## Output Location

Save to: `outputs/linkedin-exports/linkedin-[topic-slug]-[YYYY-MM-DD].md`

## Troubleshooting

If you encounter issues:
1. Document the problem in `troubleshooting/CLAUDE.md`
2. Include: problem description, steps to reproduce, solution found
