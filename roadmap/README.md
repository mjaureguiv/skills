# Roadmap Generation

Generate ICE-scored roadmap entries for feature prioritization.

## What This Skill Does

- Creates prioritized roadmap entries
- Applies ICE scoring framework (Impact, Confidence, Ease)
- Helps with feature prioritization decisions
- Generates structured roadmap documentation

## How to Use

Open Copilot Chat (`Ctrl+Shift+I`) and use the prompt:

```
#generate-roadmap Prioritize these features: [list features]
```

### Example Prompts

```
#generate-roadmap Score these features for Q2:
- User dashboard redesign
- API rate limiting
- Mobile push notifications

#pm Help me prioritize these 5 features using ICE scoring
```

## ICE Scoring Framework

| Factor | Scale | Description |
|--------|-------|-------------|
| **Impact** | 1-10 | Business value × User reach |
| **Confidence** | 1-10 | How validated is this? (proven → hypothesis) |
| **Ease** | 1-10 | Inverse of effort (10=XS, 2-4=L) |

**Score** = (Impact × Confidence × Ease) / 100

## What Gets Generated

Roadmap documents are saved to:
```
outputs/roadmap-[date].md
```

## Tips

- Include context about each feature's background
- Mention any data you have (user research, metrics)
- Ask for sensitivity analysis: "What if confidence is lower?"

---

*For technical implementation details, see [CLAUDE.md](CLAUDE.md)*
