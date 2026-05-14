# Opportunity Solution Tree

Build structured Opportunity Solution Trees (OST) for Signavio Process Governance features using the Continuous Discovery Habits framework.

## Purpose

This skill helps Product Managers:
1. Connect business outcomes to customer opportunities
2. Generate and evaluate solution hypotheses
3. Assess product risks (Value, Usability, Feasibility, Viability)
4. Define success criteria and validation plans
5. Make evidence-based prioritization decisions

## The OST Framework

```
OUTCOME (Business Goal)
    │
    ├── OPPORTUNITY 1 (Customer Problem)
    │       ├── Solution A → Experiment
    │       └── Solution B → Experiment
    │
    └── OPPORTUNITY 2 (Customer Problem)
            └── Solution C → Experiment
```

## Quick Start

### Create a Full OST

```
Create an Opportunity Solution Tree for reducing workflow-related support tickets in Process Governance.
```

### From Existing Insights

```
I have these customer insights from Productboard about workflow testing.
Build an OST starting from these opportunities.
```

### Assess a Solution

```
Assess the risks for this solution: "Sandbox testing environment for workflows"
```

## Hypothesis Template

For each solution, structure your hypothesis:

```
We believe that [TARGET CUSTOMER]
have the problem/need of [KEY PAIN OR UNMET NEED]
and that providing [PROPOSED SOLUTION]
will result in [EXPECTED OUTCOME]
```

**Example:**
```
We believe that workflow administrators
have the problem/need of not being able to test workflow changes safely
and that providing a sandbox testing environment
will result in 40% fewer production incidents from workflow changes
```

## Product Risk Assessment

Evaluate four risk dimensions for each solution:

| Risk Type | Question |
|-----------|----------|
| **Value** | Will customers use it / pay for it? |
| **Usability** | Can customers figure out how to use it? |
| **Feasibility** | Can we build it? |
| **Viability** | Should we build it (strategy, compliance)? |

## Success Criteria Types

| Type | Example |
|------|---------|
| **Adoption** | 50% of admins use feature within 3 months |
| **Behavior Change** | Testing before publishing increases to 80% |
| **Outcome Impact** | Production incidents drop 40% |
| **Satisfaction** | NPS improves 15 points |

## Validation Techniques

### Before Building (Discovery)
- Customer interviews
- Prototype testing
- Fake door tests
- Competitor analysis
- Data analysis

### While Building (Delivery)
- A/B testing
- Beta programs
- Feature flag rollouts
- Usage analytics

## Example Output

```markdown
# OST: Reduce Workflow Support Tickets

## Outcome
**Goal**: Reduce workflow-related support tickets by 40%
**Metric**: Monthly support tickets tagged "workflow"
**Target**: From 200 → 120 tickets/month
**Timeframe**: Q2 2026

## Opportunity 1: Cannot test workflows safely
**Evidence**: 17 customer insights, 45% of workflow tickets
**Severity**: High

### Solution A: Sandbox Testing Environment
**Hypothesis**: We believe workflow admins have the problem of
not being able to test changes safely, and that providing a
sandbox environment will reduce production incidents by 40%.

**Risk Assessment**:
| Risk | Level | Evidence |
|------|-------|----------|
| Value | Low | 17 customers requested |
| Usability | Medium | New concept for users |
| Feasibility | Medium | Requires infrastructure |
| Viability | Low | Aligns with governance strategy |

**Success Criteria**:
- 60% adoption within 3 months
- Testing before publishing increases from 20% to 80%
- Production incidents drop 40%

**Validation Plan**:
- Technique: Beta program with 5 customers
- Timeline: 4 weeks
- Success signal: All 5 customers actively using sandbox
```

## Related Skills

- **#productboard-categorization-wizard** - Categorize insights into opportunities
- **#continuous-discovery-habits** - Deeper CDH framework
- **#prd** - Convert validated solutions to PRDs
- **#jira** - Create experiment tickets

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-03-04 | Claude | Initial skill creation |
