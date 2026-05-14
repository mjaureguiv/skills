---
name: productboard-value-prop
description: "Productboard Feature Value Prop — Generate a structured Value Proposition, Core Capabilities, and Key Benefits summary for a product feature. Use when the user provides context about a feature they want to develop or release and needs a concise Productboard-ready feature definition."
version: 1.0.0
user-invokable: true
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

# Productboard Feature Value Prop

Turn raw feature context into a structured Value Proposition, Core Capabilities, and Key Benefits summary.

## When to Trigger

Activate this skill when the user:
- Provides context about a feature and expects a value proposition output
- Asks for a feature definition, feature summary, or release description
- Mentions "value prop", "core capabilities", "key benefits" together
- Gives unstructured feature context and wants it formatted for Productboard or release planning

## What You Do

The user provides **raw context** about a feature — informal notes, meeting summaries, a verbal description, or bullet points. You distill this into exactly three sections using the output format below.

**You do NOT ask clarifying questions unless the context is truly insufficient.** Work with what you have. Make reasonable inferences. Be concise and specific.

## Output Format

Always produce exactly this structure:

```
**[Feature Name]**

**Value Proposition**
[One sentence. What is the strategic purpose of this feature? Why does it exist? Frame it from the perspective of the value it delivers — not what it technically does.]

**Core Capabilities**
- [Capability 1 — what the feature enables or does]
- [Capability 2]
- [Capability 3]
[Typically 3 items. May be 2–4 if the context warrants it.]

**Key Benefits**
- [Benefit 1 — what the user/org gains from this]
- [Benefit 2]
- [Benefit 3]
[Typically 3 items. May be 2–4 if the context warrants it.]
```

## Writing Rules

1. **Value Proposition** — Exactly one sentence. Strategic, not technical. Answers: "Why are we building this?"
2. **Core Capabilities** — Action-oriented. Start with a verb where possible. Describe what the feature makes possible.
3. **Key Benefits** — Outcome-oriented. Describe the impact on users, teams, or the business. Not a restatement of capabilities.
4. **Customer-facing tone** — The output must be ready for external customers to read. Never mention internal concerns such as deprecations, migrations, compliance deadlines, legacy system names, technical debt, or internal team ownership. Frame everything from the customer's perspective: what they gain, not what we're fixing internally.
5. **Language** — Professional, concise, no filler words. No marketing fluff ("exciting", "powerful", "game-changing"). English only.
6. **Specificity** — Use concrete product names and capabilities from the user's context. Avoid generic statements. But strip out internal-only terminology.
7. **Length** — Each bullet should be one line. The entire output should fit in a Productboard description field or a single slide.

## Example

**Input context (from user):**
> We need to build a settings panel in Collaboration Hub for SPG approval configurations. Currently this lives in SPM Explorer which is being deprecated due to ExtJS compliance. The backend stays the same, we just move the UI. Long-term a new Lifecycle Management System will replace this entirely.

**Output:**

**SPG Approval Settings in Collaboration Hub**

**Value Proposition**
Provide centralized approval configuration management directly within Collaboration Hub for a streamlined governance setup experience.

**Core Capabilities**
- Manage all SPG approval settings from within Collaboration Hub
- Configure approval workflows without leaving the governance workspace
- Seamless integration with existing approval processing backend

**Key Benefits**
- Single place to manage approval configurations alongside other governance settings
- Consistent user experience within Collaboration Hub
- Foundation for future Lifecycle Management capabilities

---

## Works Well With

- **productboard-features**: After generating the value prop, create or update the feature in Productboard
- **feature-docs**: Expand the value prop into full user-facing documentation
- **prd**: Use the value prop as input for a detailed Product Requirements Document
- **roadmap**: Feed value props into roadmap planning

---

**Author**: Kaiser Anwar (Signavio Product Management)
**Category**: Product Planning
