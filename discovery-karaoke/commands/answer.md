# CMD: answer (Framework Q&A)

**Trigger**: Smart fallback — classified as a framework question.

**No question provided**: Apply G11:
> "Ask a question about the framework and I'll answer it.
> Example: `answer What's the difference between Explore and Validate?`
> For a context-matched recommendation: `assess [situation]`"

**Purpose**: Answer direct questions about the framework, risks, stages, methods, anti-patterns, guardrails, and discovery concepts — without triggering an assessment flow.

**Data files** (read as needed based on topic):
- `data/about.md` — framework overview, risks, stages, toolkit counts *(optional — if absent, draw framework overview from SKILL.md Core Framework section)*
- `data/risk-method-matrix.md` — method navigation, stage relationships
- `data/discovery-methods-full.md` — method details, when to use, evidence strength
- `data/anti-patterns.md` — anti-pattern descriptions, diagnostic, recovery
- `data/ai-guardrails.md` — AI in discovery, M89/M90/M91 *(optional — if absent, note AI guardrails content unavailable)*

**Approach**:
1. Identify the topic of the question (risk type? stage? method? anti-pattern? comparison? concept?)
2. Read the relevant data file(s)
3. Read `templates/answer-template.md`
4. Answer directly and concisely using that card structure — no assessment questions, no recommendation flow
5. If the question implies a situation ("when should I use X?"), answer the question first, then offer: "For a context-matched recommendation: `/discovery-karaoke assess [your situation]`"

**Length guideline**: Answers should be concise. Target ~150 words. Use a table or bullets when listing things — they say more in fewer words than prose. Never pad with preamble or summaries.

**End every answer with 1–2 relevant follow-up commands.**
