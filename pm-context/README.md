# PM Context Skill

Personal knowledge management system for Product Managers.

---

## Is This Skill For You?

### ✅ Yes, if you:
- Use Claude daily or multiple times per week
- Work on a complex product area that's hard to explain repeatedly
- Want to build a personal knowledge base over time
- Value career continuity (reviews, handoffs, interviews)

### ❌ Maybe not, if you:
- Use Claude occasionally for quick questions
- Work on simple, well-understood products
- Prefer zero-setup, just-ask-and-go interactions
- Don't want to maintain a personal context folder

### 🤔 Not sure?
Start with `#pm-context lite` for minimal setup, then upgrade later.

---

## Why This Skill Exists

### The Problem

| Without Personal Context | Impact |
|-------------------------|--------|
| **Context repetition** | Explain your product area every conversation |
| **Lost learnings** | Insights from today's work forgotten tomorrow |
| **Generic advice** | Claude gives one-size-fits-all PM guidance |
| **Stateless sessions** | No memory between conversations |

### The Solution

Personal PM Context creates a **persistent, personalized knowledge base** that Claude reads FIRST before giving you advice.

### Benefits

| Benefit | How It Helps |
|---------|--------------|
| **Instant context** | Claude already knows your product, epics, roadmap, stakeholders |
| **Accumulated knowledge** | Your learnings compound over time - search past insights |
| **Personalized prompts** | Prompts tailored to YOUR challenges |
| **Career continuity** | Performance reviews, handoffs, interview prep from your own history |
| **Hierarchical expertise** | Answers grounded in YOUR situation, not generic advice |

### Real Impact

| Task | Without Personal Context | With Personal Context |
|------|-------------------------|----------------------|
| Roadmap discussion | "Let me explain my 26 epics..." | Claude already knows |
| Market research | "I'm exploring AI for GRC..." | Claude knows your discovery work |
| Career goals | "I'm a first-time PM who..." | Claude knows your context |
| Stakeholder prep | "I need to present to..." | Claude knows your stakeholders |

**Bottom line:** Stop re-explaining. Start compounding your PM knowledge.

---

## Context Modes

Choose how much personalization you want:

| Mode | Command | Setup Time | Best For |
|------|---------|------------|----------|
| **Full** | `#pm-context init` | 15-30 min | Daily Claude users |
| **Lite** | `#pm-context lite` | 5 min | Weekly Claude users |
| **Bypass** | `#pm-context bypass` | 0 min | Quick one-off questions |

### Full Context (Default)
Complete hierarchical context with folder structure:
cat > skills/pm-context/CLAUDE.md << 'EOF'
# PM Context Skill - Claude Instructions

## Purpose
Personal knowledge management for PMs with hierarchical context loading, multiple modes, and daily learning capture.

---

## Context Modes

### 1. Full Mode (Default)
**Trigger:** User has `context/personal/CLAUDE.md` AND subfolders

**Loading Order:**
1. `context/personal/CLAUDE.md` (personal index)
2. `context/personal/` subfolders
3. `context/team/config.md`
4. Root `CLAUDE.md`

### 2. Lite Mode
**Trigger:** User has only `context/personal/CLAUDE.md`

**Loading Order:**
1. `context/personal/CLAUDE.md`
2. `context/team/config.md`
3. Root `CLAUDE.md`

### 3. Bypass Mode
**Trigger:** User runs `#pm-context bypass`

**Loading Order:**
1. `context/team/config.md`
2. Root `CLAUDE.md`

---

## Commands

### `#pm-context init`
Create full personal context structure.

**Actions:**
1. Create folder structure
2. Copy template to `context/personal/CLAUDE.md`
3. Confirm creation

**Response:**
```markdown
✅ Full context structure created!

Folders:
- context/personal/product-knowledge/
- context/personal/projects/
- context/personal/learnings/
- context/personal/contacts/
- context/personal/roadmap/

Next steps:
1. Edit `context/personal/CLAUDE.md` with your details
2. Add product knowledge
3. Start capturing learnings with `#pm-context save`
cat > skills/pm-context/templates/personal-context-full.md << 'EOF'
# Personal PM Context - [YOUR NAME]

> ⚠️ Claude reads this FIRST. Edit to customize your experience.

## My Role
[Your role, e.g., Product Manager, Connectivity Platform]

## My Product Area
[What you own/work on]

## Quick Context
[2-3 sentences Claude should always know]

## Current Priorities
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

## My Projects
| Project | Jira Key | Status |
|---------|----------|--------|
| [Name] | [KEY] | Active |

## Key Stakeholders
| Name | Role | When to Involve |
|------|------|-----------------|
| [Name] | [Role] | [Context] |

## Where to Find Context
| Topic | Location |
|-------|----------|
| Product knowledge | `product-knowledge/` |
| Projects | `projects/` |
| Learnings | `learnings/` |
| Roadmap | `roadmap/` |

## My Preferences
- [How Claude should interact with you]
