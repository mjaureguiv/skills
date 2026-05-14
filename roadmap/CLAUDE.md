> ⚠️ **This file contains instructions for GitHub Copilot (Claude), not for humans.**
> If you're a human, see [README.md](README.md) for user-friendly documentation.

---

# Roadmap Generation - Claude Instructions

You help product managers prioritize features using the ICE scoring framework.

## Before Starting

Read these context files:
1. `context/templates/roadmap-template.md` - ICE scoring rubrics
2. `context/product-context.md` - Product overview
3. `context/active-work.md` - Current initiatives

## ICE Scoring Framework

### Impact (1-10)
- 10: Massive business impact, affects all users
- 7-9: High impact, affects majority of users
- 4-6: Moderate impact, affects subset of users
- 1-3: Low impact, affects few users

### Confidence (1-10)
- 10: Proven with data, shipped similar before
- 7-9: Strong validation (user research, A/B tests)
- 4-6: Some validation (interviews, surveys)
- 1-3: Hypothesis, no validation

### Ease (1-10)
- 10: XS (hours)
- 7-9: S (days)
- 4-6: M (1-2 weeks)
- 2-4: L (sprints)
- 1: XL (quarters)

### Score Calculation
```
Score = (Impact × Confidence × Ease) / 100
```

## Output Format

For each feature:
```markdown
## [Feature Name]

**Summary**: One-sentence description

**ICE Scores**:
- Impact: X/10 - [justification]
- Confidence: X/10 - [justification]  
- Ease: X/10 - [justification]
- **Total Score**: X.XX

**Recommendation**: [Prioritize/Defer/Investigate]
```

## Working Directory

**IMPORTANT**: Create all temporary files in this skill's temp folder:
```
skills/roadmap/temp/
```

## Output Location

Save to: `outputs/roadmap-[YYYY-MM-DD].md`

## Troubleshooting

If you encounter issues:
1. Document the problem in `troubleshooting/CLAUDE.md`
2. Include: problem description, steps to reproduce, solution found
