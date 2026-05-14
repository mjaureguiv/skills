# Writing Personality Skill

**Developer:** Maryna Schedl

Transform any content into one of 16 distinct writing voices — from Storyteller to Builder.

## Quick Start

```
/personality
```

Then specify:
1. Which personality you want
2. What content to write

## The 16 Personalities

| # | Personality | Core Approach |
|---|-------------|---------------|
| 1 | **Storyteller** | Opens with a story. The lesson arrives after you're already inside it. |
| 2 | **Analyst** | Leads with data. Makes the numbers do the persuading. |
| 3 | **Provocateur** | Picks a fight with the obvious take — and wins. |
| 4 | **Teacher** | Obsessed with one thing: the reader getting it before they give up. |
| 5 | **Confessor** | Writes from the pain. Earns trust by going first. |
| 6 | **Visionary** | Sees where things are heading before anyone else names it. |
| 7 | **Curator** | Borrows ideas from other fields and makes them land somewhere new. |
| 8 | **Entertainer** | Makes the point land harder because it made you laugh first. |
| 9 | **Strategist** | Turns complex problems into one clear lever worth pulling. |
| 10 | **Skeptic** | Reads every claim like a lawyer. Keeps the reader honest. |
| 11 | **Encourager** | Meets the reader in their doubt — and stays there until it shifts. |
| 12 | **Philosopher** | Sits with a hard question longer than everyone else, then writes from that place. |
| 13 | **Journalist** | Facts first, always sourced. Opinion earns its place or doesn't appear. |
| 14 | **Mentor** | Speaks from further down the road and hands you the shortcut they wish they'd had. |
| 15 | **Contrarian** | Finds the consensus, then argues the opposite — not to be difficult, but because they checked. |
| 16 | **Builder** | Skips the theory. Gives you the exact steps and gets out of the way. |

## Example Usage

**Request:**
> /personality
> Use the Strategist voice to write about why we should focus on adoption over acquisition.

**Output:**
> Forget the 47 initiatives on your roadmap. There's only one lever that matters: adoption.
>
> Here's the math. You spent $X acquiring each customer. If they churn at month 6, you've burned that investment. If they adopt deeply by month 3, they renew, expand, and refer.
>
> Every other metric is noise. Fix adoption, and everything else follows.

## Combining Personalities

You can blend two personalities:

- **"Storyteller + Analyst"** → A data-rich narrative
- **"Mentor + Builder"** → Experienced advice with actionable steps
- **"Visionary + Skeptic"** → Future vision rigorously grounded

When blending, the first personality leads (60%), the second influences (40%).

## When to Use Each

| If you need to... | Try... |
|-------------------|--------|
| Inspire action | Storyteller, Visionary, Encourager |
| Convince with evidence | Analyst, Journalist, Skeptic |
| Challenge assumptions | Provocateur, Contrarian |
| Teach something complex | Teacher, Builder, Mentor |
| Connect emotionally | Confessor, Encourager, Storyteller |
| Provide fresh perspective | Curator, Philosopher, Contrarian |
| Get laughs + make points | Entertainer |
| Cut to what matters | Strategist, Builder |

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-04-16 | Claude | Initial creation with 16 personalities |
