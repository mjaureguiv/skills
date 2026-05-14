# Productboard Feature Value Prop

Generate structured **Value Proposition / Core Capabilities / Key Benefits** summaries for product features.

## What It Does

You provide context about a feature (informal notes, meeting context, a description) and get back a clean, structured summary ready for Productboard or release planning.

## How to Use

1. Invoke the skill: `/productboard-value-prop`
2. Provide your feature context (paste notes, describe verbally, or reference a ticket)
3. Receive a formatted output with Value Proposition, Core Capabilities, and Key Benefits

Or simply provide feature context in conversation — the skill triggers automatically when you're describing a feature to be defined.

## Output Format

```
**[Feature Name]**

**Value Proposition**
One strategic sentence — why are we building this?

**Core Capabilities**
- What the feature enables (typically 3 items)

**Key Benefits**
- What users/org gain from this (typically 3 items)
```

## Example

**Input:**
> "We need approval entry points in Collaboration Hub for NGM diagrams before GA..."

**Output:**
> **Approvals for NGM**
>
> **Value Proposition**
> Enable seamless approval workflows for NGM process diagrams by integrating approval entry points into Collaboration Hub, ensuring feature parity with the legacy SPM Editor before its deprecation.
>
> **Core Capabilities**
> - Provide approval workflow entry points for NGM-created BPMN diagrams in Collaboration Hub
> - Ensure compatibility with existing SPG approval triggers used by legacy diagrams
> - Discover and define additional approval touchpoints needed for GA readiness
>
> **Key Benefits**
> - Uninterrupted approval experience for users transitioning from SPM Editor to NGM
> - No rework on SPG backend – leveraging existing approval infrastructure as is
> - GA readiness by EOY with full approval coverage for NGM process diagrams

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-03-31 | Kaiser Anwar | Initial skill creation |
