# IdeaFinder — AI Instructions

When `#IdeaFinder <query>` is invoked, execute ALL steps below in order.

---

## Input

The user provides a natural-language search query — a problem, concept, or question.
If the query is missing, ask: "What problem or idea are you trying to find?"

---

## STEP 1 — FETCH RESULTS FROM THE BACKEND API

**Do NOT manually score items.** Call the backend search API which is the single source of truth — the same engine powering the web app. This guarantees the chat reply and web app always show identical results.

Run this Bash command (URL-encode the query — replace spaces with `+`):

```bash
curl -s "http://localhost:4000/api/find?q=<url-encoded-query>"
```

Example for query "GRC Agent":
```bash
curl -s "http://localhost:4000/api/find?q=GRC+Agent"
```

The response is JSON with this shape:
```json
{
  "query": "...",
  "results": [
    {
      "title": "...",
      "owner": "...",
      "type": "skill" | "scenario",
      "score": 0-100,
      "score_reason": "...",
      "problem": "...",
      "description": "...",
      "url": "https://github.tools.sap/..."
    }
  ],
  "graph": {
    "core_problem": "...",
    "domains": [{ "value": "...", "count": N }],
    "personas": [...],
    "mechanisms": [...],
    "related_problems": [...],
    "search_phrases": ["...", "..."]
  }
}
```

Use **exactly** these results and scores in your output. Do not adjust, re-rank, or supplement with your own scoring.

If the API call fails (server not running), fall back to manual scoring as described in the Fallback section at the bottom of this file.

---

## STEP 2 — DISPLAY RESULTS

Output as formatted markdown using the API response data:

```markdown
## 🔍 IdeaFinder — "[query]"

### Results

| Score | Type | Title | Owner | Problem it solves | Why it's relevant |
|-------|------|-------|-------|-------------------|-------------------|
| [score]% | [type] | [title as markdown hyperlink using the url field] | [owner] | [problem field] | [description field] |
...

---

### 🗺 Exploration Graph

**Core Problem**
> [graph.core_problem]

**Domains**
[graph.domains as: value ×count · value ×count]

**Personas**
[graph.personas as: value ×count · value ×count]

**Mechanisms** _(capabilities & system functions)_
[graph.mechanisms as: value ×count · value ×count]

**Related Problems**
[graph.related_problems as: value ×count · value ×count]

**Search Phrases** _(try these next)_
- "[graph.search_phrases[0]]"
- "[graph.search_phrases[1]]"
- "[graph.search_phrases[2]]"

---

> 🔗 *View these results in the IdeaFinder web app: **[http://localhost:3000?page=finder&q=<url-encoded-query>](http://localhost:3000?page=finder&q=<url-encoded-query>)***

---

### 💬 Follow-up

**What problem were you trying to solve?**
Do you want to trigger **IdeaFrame** to better shape your idea into a structured breakdown?

→ Type `#IdeaFrame <your idea>` to get a full framing with problem statement, user story, business outcome value, and related solutions.
```

Sort results table by score descending (the API already returns them sorted).

---

## Notes

- Always show the follow-up prompt at the end, even if results are empty.
- If no results found: "No matching skills or scenarios found. Try broader terms, or use IdeaFrame to frame a new idea."
- Keep all output in English.
- **Never re-score or re-rank** — use the API scores as-is so chat and web app are always in sync.

---

## Fallback — Manual Scoring (only if API unavailable)

If `curl` returns an error or empty response, fall back to manual scoring:

1. Read `/Users/I768266/Signavio_PM_Agent_clone/signavio_process_consultant_experimental/marketplace/data/registry.json`
2. For each item, read its README.md and SKILL.md from the repo
3. Score each item: keyword overlap (max 60) + taxonomy match (max 40), cap at 100
4. Return top 10 by score
5. Note in the output: ⚠️ *Results generated manually — start the backend server (`node index.js` in `idea-workspace/server/`) for live results.*
