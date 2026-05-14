# Partner Skills

All SAP Signavio technology partner knowledge, tools, and workflows — organized in one place.

## Skills

| Skill | Prompt | What It Does | Status |
|-------|--------|--------------|--------|
| [Partner Expert](partner-expert/) | `#partner-expert` | Answer partner questions, guide onboarding, explain models | 🚧 Building |
| [Partner KIT](partner-kit/) | `#partner-kit` | Generate enablement PPT deck from knowledge base | 📋 Planned |
| [Partner Refresh](partner-refresh/) | `#partner-refresh` | Review & update partner knowledge base freshness | 📋 Planned |

## How It Works

The partner sub-repo uses **progressive disclosure**:

1. **SKILL.md** — The router (<500 lines). Knows what's available and when to load what.
2. **references/** — Deep knowledge files loaded on demand. This is where the real content lives.
3. **temp/** — Working directory for intermediate files.

## Knowledge Base Structure

All reference material lives in `partner-expert/references/`:

| File | Content | Populated? |
|------|---------|------------|
| `link-registry.md` | All ~50 partner links with categories, priority, freshness tracking | ✅ |
| `bbp-framework.md` | SAP Build/Buy/Partner strategy summary | ✅ Seeded |
| `partner-models.md` | SolEx vs Endorsed vs Store vs OEM — decision criteria | ⬜ Pending docs |
| `signavio-partners.md` | Current partner portfolio & status | ⬜ Pending docs |
| `signavio-process.md` | How to become a Signavio tech partner | ⬜ Pending docs |
| `glossary.md` | Partner terminology & abbreviations | ✅ Seeded |

## Feeding Documents

To grow the knowledge base:

1. Download a document from SharePoint/Teams
2. Say: "read my latest download" (or drop the file)
3. The agent extracts content and appends to the correct reference file
4. The link registry gets updated with `last_reviewed` date

## Folder Structure

```
skills/partner/
├── README.md                        ← You are here
├── partner-expert/
│   ├── SKILL.md                     # AI instructions
│   ├── README.md                    # Human docs
│   ├── references/                  # Deep knowledge (loaded on demand)
│   │   ├── bbp-framework.md
│   │   ├── partner-models.md
│   │   ├── signavio-partners.md
│   │   ├── signavio-process.md
│   │   ├── link-registry.md
│   │   └── glossary.md
│   └── temp/
├── partner-kit/
│   ├── SKILL.md
│   ├── README.md
│   └── temp/
└── partner-refresh/
    ├── SKILL.md
    ├── README.md
    └── temp/
```

## Champion

Adriana Rotaru
