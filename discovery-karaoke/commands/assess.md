# CMD: assess [situation]

**Trigger**: `assess` or smart fallback — classified as a situation description.

**No situation provided**: Apply G11:
> "Describe your situation and I'll recommend the right discovery methods.
> Example: `assess We're considering a self-serve tier for SMBs`
> For a faster result: `quick [situation]` — 4 questions, top methods in under 2 minutes.
> To map the full discovery arc across all stages: `plan [situation]`"

**Data files**:
- `data/risk-method-matrix.md` — Risk × Stage navigation and constraint quick picks
- `data/methods-index.md` — method metadata for shortlisting and constraint filtering
- `data/discovery-methods-full.md` — full prose entries for the 2-3 shortlisted methods only
- `data/anti-patterns.md` — Named anti-patterns for G6 karaoke check
- `data/ai-guardrails.md` — AI acceleration and guardrails (G5)
- `templates/recommendation-template.md` — Output card format

**Step 1: Check for saved config**

Look for `.discovery-karaoke-config.yml` in the working directory. If found:
- Pre-fill constraint fields (company size, business model, user access, team size, customer base, regulated)
- Show the resolved file path and pre-filled values, and ask the user to confirm or adjust — this serves as the staleness check

**Step 1b: Signal-based pre-fill** *(apply before asking Batch 2 — skip questions already answered by signals)*

Scan the situation description for recognizable signals and pre-fill the corresponding constraint fields:

| Signal in description | Pre-fill |
|----------------------|----------|
| "B2B", "enterprise", "sales", "account", "procurement" | Business model → B2B |
| "B2C", "consumer", "app store", "freemium" | Business model → B2C |
| "startup", "pre-launch", "founding", "seed" | Company context → Startup; Product stage → Pre-launch |
| "MVP", "early stage", "first version" | Product stage → MVP |
| "regulated", "GDPR", "HIPAA", "FDA", "EU AI Act", "financial services", "healthcare", "legal" | Regulated → Yes → auto-elevate G4 (skip regulated question in Batch 3) |
| "CCPA", "California", "consumer privacy", "data subject", "right to delete", "opt-out" | Regulated → Yes → auto-elevate G4 |
| "PSD2", "open banking", "payment", "fintech", "CFPB", "lending", "credit", "insurance" | Regulated → Yes → auto-elevate G4 |
| "COPPA", "under 13", "parental consent", "children's data" | Regulated → Yes → auto-elevate G4 + participant ethics clause |
| "employment", "performance review", "hiring", "recruitment", "HR", "workforce", "background check" | Regulated → Yes → auto-elevate G4 (employment discrimination risk) |
| "automated decision", "automated scoring", "algorithmic decision", "risk scoring", "profiling", "recommendation engine", "ranking" | Regulated → Yes → auto-elevate G4 (EU AI Act / automated decision-making exposure) |
| "no users yet", "pre-launch", "no customers" | User access → Limited |
| "large user base", "10K+", "millions" | Customer base → Large |
| "urgent", "this week", "deadline", "by Friday" | Time → Urgent |
| "algorithm", "model accuracy", "spike", "POC", "proof of concept", "can we build" | Feasibility sub-signal → Algorithm viability |
| "integration", "API", "third-party", "dependency", "legacy system" | Feasibility sub-signal → Integration complexity |
| "data", "dataset", "training data", "data pipeline", "data quality", "data availability" | Feasibility sub-signal → Data readiness |
| "minors", "children", "patients", "employees", "vulnerable", "sensitive population" | Ethics flag → auto-elevate G4 participant ethics clause |
| "we've already decided", "already decided", "decision is made", "going ahead with" | Org-readiness flag → elevate Anti-Pattern 9 (Validation Theater) in G6 karaoke check |
| "leadership wants", "CEO wants", "VP wants", "exec wants", "stakeholders want", "stakeholders expect" | Org-readiness flag → elevate Anti-Pattern 8 (Stakeholder Appeasement) in G6 karaoke check |
| "the roadmap says", "on the roadmap", "roadmap committed", "committed to ship", "deadline to launch" | Org-readiness flag → elevate Anti-Pattern 9 (Validation Theater) in G6 karaoke check |
| "need to justify", "need to validate our decision", "confirm our direction", "prove that", "show that users want" | Org-readiness flag → elevate Anti-Pattern 9 (Validation Theater) in G6 karaoke check |
| "we know users want", "users definitely want", "we're confident users" | Org-readiness flag → elevate Anti-Pattern 9 (Validation Theater) in G6 karaoke check |

**Org-readiness flag handling**: Unlike constraint signals, org-readiness flags do not pre-fill a form field. Instead:
1. Surface the flag visibly at the start of Batch 2 pre-fill display — e.g. "⚠️ Org-readiness signal detected: your description suggests a direction may already be set. The named risk for this is [Anti-Pattern 8: Stakeholder Appeasement / Anti-Pattern 9: Validation Theater]. The recommendation will still run — but the karaoke check will address this directly."
2. In Step 3.8 (G6 karaoke check): prioritise the flagged anti-pattern as one of the 1–2 named patterns surfaced, even if other patterns might score higher in a neutral reading of the situation.
3. Do not ask the user to confirm or deny the signal — surface it transparently and let the output address it.

**REQUIRED**: If any signals were detected in Step 1b, you MUST show the pre-filled values to the user BEFORE presenting Batch 1 questions. Do not silently apply signals. The pre-fill display must appear first, in this format:
> "I detected the following from your description: [list each pre-filled field and value]. Confirm or correct these, then I'll ask the remaining questions."


**Step 2: Gather context** (AskUserQuestion, max 3–4 questions per batch)

*Batch 1 — Situation* (always ask):
1. What are you trying to decide? (free text)
2. Product stage: Pre-launch / MVP / Growth / Mature
3. Primary risk (multi-select 1–2): Value/Desirability / Usability / Feasibility / Viability / Compliance & Ethics
4. *(optional)* Have you already used AI tools to generate user insights, personas, or research findings for this situation? Yes / No
   → If Yes: flag at the top of the recommendation output — "⚠️ AI-generated research detected: any AI-generated insights, personas, or simulated feedback from prior work should be treated as hypotheses, not evidence (G5). The methods below are your path to validating them with real users." Do not block the recommendation — surface the flag and continue.

*After Batch 1 — Usability-only check* (conditional — fire only if Usability is the sole risk selected):
> "Have you confirmed that users want this before testing whether they can use it? Usability without Value confirmation is a common sequencing error — you may be optimising the experience of something people won't choose. If Value hasn't been tested yet, consider adding Value/Desirability as a co-primary risk. Skip to proceed with Usability only."

*Batch 2 — Constraints* (skip fields already in config or pre-filled by signals):
4. Company context: Startup / Scaleup / Enterprise
5. Business model: B2B / B2C / B2B2C / Internal
6. User access: Easy / Moderate / Limited
7. Time available: Urgent (<1 week) / Short (1–4 weeks) / Standard (1–3 months) / Flexible

*Batch 3 — Depth* (medium/large bets only — skip entirely for small bets):
8. Budget: Minimal / Moderate / Significant
9. Team capacity: Solo / Small (2–5) / Cross-functional (5+)
10. Regulated or sensitive context? *(skip if already auto-elevated by signal pre-fill)*
    "Does this product or feature operate in a regulated industry, or handle personal data, financial data, health data, employment decisions, or automated decision-making?" Yes / No / Unsure → Yes or Unsure → auto-elevate Compliance (G4)
11. Customer base: None / Small (<100) / Medium (100–10K) / Large (10K+)
12. Blast radius:
    - **Small** — feature tweak: affects <5% of users, reversible in <1 sprint
    - **Medium** — new feature: visible to a meaningful user segment, moderate rollback cost
    - **Large** — new product, new segment, new business model, or affects >25% of users / hard to reverse

**Step 3: Generate recommendations**

1. Read `data/risk-method-matrix.md` → identify candidate method IDs for the risk × stage combination and applicable constraint quick picks
2. Read `data/methods-index.md` → narrow candidates by constraints (Needs Existing Users, Needs Live Traffic, Needs Legal Review, Effort, Cost, Tier, Stage match)
3. Shortlist 3-5 candidates from the index. Then read only those entries from `data/discovery-methods-full.md` for full prose content
4. **Derive the primary assumption being tested** from the dominant risk × stage combination. This will appear in the recommendation Context Summary. Use these inference rules as a starting point — adapt the wording to the specific situation:
   - Value × Explore → "Customers have [problem] at sufficient frequency and intensity to prioritise a solution"
   - Value × Validate → "Customers will choose [solution] over their current workaround or alternative"
   - Usability × Validate → "Users can complete [key task] without guidance within an acceptable time and error rate"
   - Usability × Optimize → "[Change] improves task completion rate or reduces friction on [flow]"
   - Feasibility × Explore → "[Capability/approach] can be built with available technology and resources in the required timeframe"
   - Feasibility × Validate → "[Specific implementation] meets the required performance, quality, or scale threshold"
   - Viability × Explore → "A business model exists that makes [direction] financially sustainable at target scale"
   - Viability × Validate → "[Pricing/model/channel] generates sufficient margin and willingness to pay at realistic volume"
   - Compliance × any → "[Feature/data use] can be made compliant without prohibitive redesign or regulatory risk"
   - If two risks are active: derive the primary assumption for the dominant risk; note the secondary assumption briefly

   **Framing check**: After deriving the assumption, check whether it is solution-framed or problem-framed.
   - **Solution-framed** assumption (risk): starts with "users will like / prefer / use [feature]", "the feature will [outcome]", or otherwise takes the existence of a solution as given.
   - **Problem-framed** assumption (correct): starts with "users have [problem]", "customers experience [friction]", or tests whether a need exists before testing whether a solution meets it.
   - If the derived assumption is solution-framed AND the stage is Explore: add a note in the Context Summary — "⚠️ Framing note: the stated assumption tests a solution, but the stage is Explore. The underlying assumption not yet tested: [reframe as problem-framed equivalent]. If this problem assumption hasn't been validated, consider starting there." Do not block the recommendation — flag it and continue.
5. **If Feasibility is active, identify the sub-type** — use signal pre-fill if detected, otherwise ask: "Is the core unknown about (a) whether the algorithm or model can work, (b) integrating with external systems or dependencies, or (c) data availability and quality?" Then adjust method selection:
   - **Algorithm viability** → recommend technical spikes / POCs; if AI-adjacent, surface M89 (Capability Contract Workshop) as the entry point
   - **Integration complexity** → recommend architecture review, integration spikes, and technical discovery sessions with engineering
   - **Data readiness** → surface M91 (Data Readiness Assessment) as primary method; probe data permission, availability, and quality risks
6. Select 1–2 primary methods (G10); sequence with explicit decision points — what each method's output unlocks for the next step
7. Suggest 1 companion context tool
8. G6 karaoke check: read `data/anti-patterns.md` → identify the 1–2 anti-patterns **by name** most relevant to the situation → surface the specific pattern name, its warning signs, and its recovery action
9. G4 compliance check: if regulated or AI/data-sensitive, surface M75/M76 or M89/M91 as early as Explore
10. G5 AI opportunities: read `data/ai-guardrails.md` for relevant acceleration notes

**Step 4**: Check output_mode (config or `full` suffix). Read `templates/recommendation-template.md`. Deliver output using the Compact Template if output_mode is `compact`, Full Template if `standard` or `full` suffix was used.

**Step 5: Offer follow-up**:
- `/discovery-karaoke describe M##` — deep-dive on any recommended method
- `/discovery-karaoke compare M## vs M##` — compare with the alternative not recommended
- `/discovery-karaoke review [plan]` — critique an existing plan
- `/discovery-karaoke plan [same situation]` — map the full discovery arc across all stages
- `/discovery-karaoke diagnose` — check if karaoke patterns extend across your broader discovery practice
- Ask any framework question freeform — e.g. "What is blast radius?" or "How does G10 work?"
- Offer to help design the specific research instrument (interview guide, survey, test plan)
