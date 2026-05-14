# CMD: ai [situation]

**Trigger**: `ai`

**No situation provided**: Apply G11:
> "Describe the AI feature or capability you're building or evaluating.
> Example: `ai We're building an AI-powered document summarizer`"

**Data files**:
- `data/ai-guardrails.md` — full guardrail framework for AI in discovery
- `data/discovery-methods-full.md` — M89, M90, M91 entries specifically

**Purpose**: Specialized path for teams building or evaluating AI-powered features. Surfaces the M89→M91→M90 sequence, the circularity risk, LLM-as-judge nuance, and the AI-in-discovery guardrails.

**Step 1**: Ask (single batch via AskUserQuestion):
1. What AI feature or capability are you trying to validate? (free text)
2. Where are you in the process?
   - Not started (no architecture decisions made)
   - Capability Contract defined (M89 done)
   - Data readiness assessed (M91 done)
   - Testing capability against data (M90 in progress)
   - Already built — evaluating quality in production
3. Does your feature process personal data, make automated decisions, or potentially fall under EU AI Act scope? Yes / No / Unsure

**Step 2**: Read `data/ai-guardrails.md` in full. Read only the M89, M90, and M91 sections from `data/discovery-methods-full.md` (not the full file). These sections use the headings `## METHOD 89: ...`, `## METHOD 90: ...`, `## METHOD 91: ...` — locate them by searching for this heading pattern.

**Step 3**: Recommend based on where the user is:

- **Not started**: Recommend M89 (Capability Contract Workshop) first. Explain the M89→M91→M90 sequence and why order matters — skipping M89 means testing the wrong capability; skipping M91 means testing on unverified data.
- **M89 done**: Recommend M91 (Data Readiness Assessment). Surface data permission, availability, and quality risks.
- **M91 done**: Recommend M90 (AI Capability Assessment). Explain what a passing threshold means and how to set it — AI cannot set the bar, only humans can.
- **Testing capability**: Explain LLM-as-judge as a legitimate scoring technique at scale (Zheng et al. 2023, MT-Bench), with known biases (position, verbosity, self-enhancement). Clarify: it does not replace the representative test set, the threshold definition, or the human go/no-go decision.
- **Already built**: Recommend AI Red Teaming (M81), Fairness & Bias Assessment (M80), Post-market Compliance Monitoring (M82).

**Step 4**: G4 compliance check. If EU AI Act scope is indicated or possible → surface M76 (DPIA), M83 (FRIA), and the need for qualified legal review. Reference the EU AI Act timing note from `data/ai-guardrails.md`.

**Step 5**: Surface the relevant guardrails from `data/ai-guardrails.md`:
- What AI CAN do in AI product discovery
- What AI CANNOT do (capability confirmation, data readiness verification, compliance sign-off)
- The Simulation Trap warning if the user mentions using AI to simulate user feedback

**Tone**: Precise, non-alarmist. AI feasibility is a technical discovery question like any other — it just has a specific required sequence.
