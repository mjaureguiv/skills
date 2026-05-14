# IdeaFrame — AI Instructions

When this skill is invoked, check the input first:

- If the input is **`save`** (i.e. `#IdeaFrame save`) → jump directly to the **SAVE TRIGGER** section below.
- Otherwise → execute Steps 1–6 in order to frame the idea.

---

## SAVE TRIGGER — `#IdeaFrame save`

When the user types `#IdeaFrame save`, commit the most recently framed idea to the GitHub repo.

### Step S1 — Collect save details

Ask the user for these three fields (all required). Ask in a single message:

```
To save this idea to the repo, I need three details:

1. **Folder name** (kebab-case slug, e.g. `grc-control-mapper`) — used as the folder name in the repo
2. **Display title** (e.g. `GRC Control Point Mapper`) — used as the heading in README and SKILL.md
3. **Owner name** (your name or team, e.g. `Ling`) — recorded in the SKILL.md
4. **Type** — `skill` or `scenario`
```

If the user provides all four inline (e.g. `#IdeaFrame save grc-control-mapper "GRC Control Point Mapper" Ling skill`), skip asking and use those values directly.

### Step S2 — Call the save API

Run this Bash command with the collected values:

```bash
curl -s -X POST http://localhost:4000/api/ideas/save-to-repo \
  -H "Content-Type: application/json" \
  -d '{"type":"<skill|scenario>","name":"<kebab-slug>","title":"<Display Title>","owner":"<Owner Name>"}'
```

### Step S3 — Report the result

**On success** (HTTP 200), respond with:

```
✅ Saved to repo!

📁 Folder: signavio_process_consultant_experimental/<skills|scenarios>/<name>/
📄 Files created:
   - README.md
   - SKILL.md (or CLAUDE.md for scenarios)
   - metadata.json

🔗 GitHub: https://github.tools.sap/signavio-pm-agent/signavio_process_consultant_experimental/tree/master/<skills|scenarios>/<name>/
```

**On error**, show the error message from the API response and suggest a fix:
- `409 Folder already exists` → suggest a different folder name
- `400 name must be kebab-case` → show a corrected slug
- `400 No processed result` → ask the user to run `#IdeaFrame <idea>` first

---

## Input

The user provides an idea description — anything from a single sentence to a few paragraphs. If the idea is missing, ask: "Please describe the idea you'd like to frame."

---

## STEP 1 — CORE FRAMING

Generate a structured framing of the idea with exactly these 5 fields:

- **problem_statement**: The core problem the idea solves. Describe the current pain, what is missing or broken, and who is affected. 2-3 sentences.
- **user_story**: In the format "As a [persona], I want to [action] so that [outcome]." One sentence.
- **business_outcome**: Named "Business Outcome Value". Quantified business impact where possible (time saved, cost reduced, risk mitigated). Format as 2-3 bullet points, each starting with `- `. Do not write as a paragraph.
- **technical_description**: How the system works — key components, data flow, interactions. 2-3 sentences.
- **analogy**: A vivid real-world analogy that makes the idea instantly clear. One sentence starting with "It's like…"

---

## STEP 2 — AUTO MULTI-FRAME DESCRIPTION

From the same idea, generate a `multi_frame` with exactly these 3 sub-fields. Do NOT reuse wording from Step 1.

- **jtbd**: Jobs-to-be-Done format. Use exactly this sentence structure, keeping the brackets visible so the reader can see the frame:
  "When [situation], I want to [motivation], so I can [outcome]."
  Then follow with 1-2 sentences expanding on the desired outcome and what success looks like.
- **problem_framing**: What problem exists (observable symptom), why it matters (consequence if unsolved), and what constraint or friction causes it (root blocker). 2-3 sentences. Focus on problem space, not solution.
- **system_behavior**: How the system should behave — what it detects, decides, and does. Write from the system's perspective ("The system…"). 2-3 sentences. Do NOT repeat technical_description.

---

## STEP 3 — LAYERED TAXONOMY CLASSIFICATION

Before assigning any tags, first perform a brief inference analysis:

**INFERENCE (do this silently before tagging):**
1. **Domain** — What field or discipline does this idea belong to? (e.g. GRC, compliance, product management, HR, IT governance)
2. **Primary user roles** — Who are the 1-3 people most likely to use or benefit from this?
3. **Core problem type** — What category of problem is being solved? (e.g. compliance gap, control mapping, audit inefficiency, process misalignment, risk visibility)
4. **System nature** — Is this primarily analysis / automation / monitoring / orchestration / recommendation?
5. **User pain points** — What specific friction or pain does the user experience today that this idea relieves?

Then map inferences to the controlled vocabulary. Always return at least one value per category. Multiple values allowed.

**domain** (1-4 values — pick most specific and relevant):
`grc` | `compliance` | `audit` | `risk-management` | `process-governance` | `internal-control` | `data-privacy` | `finance` | `hr` | `operations` | `it-governance` | `supply-chain` | `customer-success` | `product-management`

**persona** (1-3 values — pick specific role titles, not generic ones):
`grc-team` | `compliance-officer` | `internal-auditor` | `risk-manager` | `process-owner` | `control-owner` | `data-protection-officer` | `finance-controller` | `it-admin` | `product-manager` | `hr-manager` | `operations-manager` | `executive-sponsor`

**capability** (1-4 values — pick domain-aware capabilities):
`control-mapping` | `compliance-mapping` | `control-design` | `risk-assessment` | `audit-trail-generation` | `evidence-collection` | `policy-mapping` | `regulation-interpretation` | `gap-analysis` | `reporting` | `monitoring` | `notification` | `approval` | `routing` | `integration` | `collaboration`

**system_function** (1-3 values — how the system works technically):
`diagram-analysis` | `process-mining` | `semantic-matching` | `rule-engine` | `ai-recommendation` | `workflow-orchestration` | `data-capture` | `visualization` | `natural-language-processing` | `anomaly-detection`

**user_problem** (1-4 values — specific pain points the idea directly relieves):
`manual-reconciliation` | `compliance-drift` | `audit-preparation` | `process-misalignment` | `control-gap` | `lack-of-visibility` | `data-silos` | `slow-approval` | `error-prone-process` | `knowledge-loss` | `regulatory-risk` | `scalability-constraint` | `duplicate-effort` | `poor-traceability` | `delayed-reporting` | `change-impact-blindness`

**trigger** (1-2 values):
`event-based` | `manual` | `scheduled` | `rule-based`

Output as:
```json
"tags": {
  "domain": [...],
  "persona": [...],
  "capability": [...],
  "system_function": [...],
  "user_problem": [...],
  "trigger": [...]
}
```

---

## STEP 4 — COMPREHENSIVE REPO SEARCH FOR RELATED SOLUTIONS

Search both repositories for related skills and scenarios. Run these Bash commands to get all README files:

```
find /Users/I768266/Signavio_PM_Agent_clone/skills -name "README.md"
find /Users/I768266/Signavio_PM_Agent_clone/scenarios -name "README.md"
find /Users/I768266/Signavio_PM_Agent_clone/signavio_process_consultant_experimental/skills -name "README.md"
find /Users/I768266/Signavio_PM_Agent_clone/signavio_process_consultant_experimental/scenarios -name "README.md"
```

Read every file returned. Identify the 6 most semantically relevant to the submitted idea. For those 6, also read their companion SKILL.md or CLAUDE.md for deeper context.

For each of the 6, extract:
- **title**: name of the skill or scenario
- **owner**: from the "Owner(s)" section of the README. Use "Unknown" if not found.
- **problem**: one sentence on what problem this skill/scenario solves (from the skill's perspective)
- **description**: one sentence on specifically why it relates to the submitted idea
- **type**: `skill` or `scenario`
- **path**: full relative path from repo root, e.g. `signavio_process_consultant_experimental/skills/agentic-ai-grc/` or `skills/prd/`
- **score**: integer 0–100 using this rubric:
  - 90–100: Core topic is identical or near-identical
  - 70–89: Directly addresses same domain and primary capability
  - 50–69: Overlaps significantly on one key dimension
  - 30–49: Tangentially related — useful as a next step
  - 0–29: Weak connection only
  Be honest and differentiated — scores should spread across the range.
- **score_reason**: one sentence explaining why this score was assigned
- **url**: GitHub URL constructed as follows:
  - If path starts with `signavio_process_consultant_experimental/`: `https://github.tools.sap/signavio-pm-agent/signavio_process_consultant_experimental/tree/master/{path with the prefix stripped}`
  - Otherwise (skills/ or scenarios/): `https://github.tools.sap/signavio-pm-agent/Signavio_PM_Agent/tree/master/{path}`

---

## STEP 5 — DISPLAY RESULTS IN CHAT

Output the full result as formatted markdown in the chat. Use this structure:

```markdown
## 🖼️ IdeaFrame — [idea title, max 8 words]

---

### 🏷️ Tags & Taxonomy
**Domain:**          [tag] · [tag]
**Persona:**         [tag] · [tag]
**Capability:**      [tag] · [tag] · [tag]
**System Function:** [tag] · [tag]
**User Problem:**    [tag] · [tag] · [tag]
**Trigger:**         [tag]

---

### 🎯 Core Framing

**Problem Statement**
[text]

**User Story**
[text]

**Business Outcome Value**
- [bullet 1]
- [bullet 2]
- [bullet 3]

**Technical Description**
[text]

**Analogy**
[text]

---

### 🔀 Auto Multi-Frame Description

**Jobs-to-be-Done**
[text]

**Problem Framing**
[text]

**System Behaviour**
[text]

---

### 🔗 Related & Similar Solutions

| Score | Title | Type | Owner | Why relevant |
|-------|-------|------|-------|--------------|
| [score]% | [title as a markdown hyperlink using the url field] | [type] | [owner] | [score_reason] |
...

> 💡 *Results also written to the IdeaFrame web app at http://localhost:3000*
> 💾 *Happy with this framing? Type `#IdeaFrame save` to commit it to the GitHub repo.*
```

Sort the Related Solutions table by score descending.

---

## STEP 6 — WRITE TO WEB APP QUEUE

Write the following JSON to `/Users/I768266/Signavio_PM_Agent_clone/idea-workspace/queue/results.json` so the results appear in the IdeaFrame web app at http://localhost:3000:

```json
{
  "id": "[generate a UUID or use timestamp-based id]",
  "status": "done",
  "result": {
    "problem_statement": "...",
    "user_story": "...",
    "business_outcome": "...",
    "technical_description": "...",
    "analogy": "...",
    "multi_frame": {
      "jtbd": "...",
      "problem_framing": "...",
      "system_behavior": "..."
    },
    "tags": {
      "domain": [...],
      "persona": [...],
      "capability": [...],
      "system_function": [...],
      "user_problem": [...],
      "trigger": [...]
    }
  },
  "related": [
    {
      "title": "...",
      "owner": "...",
      "problem": "...",
      "description": "...",
      "type": "skill" | "scenario",
      "path": "...",
      "score": 0-100,
      "score_reason": "..."
    }
  ],
  "processedAt": "[current ISO timestamp]"
}
```

Also update `/Users/I768266/Signavio_PM_Agent_clone/idea-workspace/queue/pending.json` to set `"status": "processed"` if a matching pending entry exists.

If writing to the web app queue fails (e.g. path not found), skip silently — the chat output is the primary deliverable.

---

## Notes

- Always complete all steps even if the idea is vague — make reasonable inferences and note any assumptions.
- Keep all outputs in English regardless of the language used in the input.
- Do not repeat wording across sections — each framing layer should add new perspective.
- The skill should feel like a senior PM reviewing your idea and returning a structured brief within seconds.
