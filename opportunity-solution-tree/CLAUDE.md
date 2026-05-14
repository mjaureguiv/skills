# Opportunity Solution Tree - Claude Instructions

## Skill Overview

This skill helps Product Managers build **Opportunity Solution Trees (OST)** for Signavio Process Governance features. It combines Teresa Torres' Continuous Discovery Habits framework with structured hypothesis validation.

Your role: Guide PMs through building an OST from outcome to validated experiments, ensuring each layer connects logically.

---

## The OST Framework

### Tree Structure

```
OUTCOME (Business/Product Goal)
    │
    ├── OPPORTUNITY 1 (Customer Pain/Need)
    │       ├── Solution A
    │       │       ├── Experiment 1
    │       │       └── Experiment 2
    │       └── Solution B
    │               └── Experiment 3
    │
    └── OPPORTUNITY 2 (Customer Pain/Need)
            └── Solution C
                    └── Experiment 4
```

### Layer Definitions

| Layer | Definition | Question Answered |
|-------|------------|-------------------|
| **Outcome** | Measurable business/product goal | "What metric are we trying to move?" |
| **Opportunity** | Customer pain point or unmet need | "What problem causes customers to not reach the outcome?" |
| **Solution** | Product capability addressing the opportunity | "What could we build to solve this?" |
| **Experiment** | Test to validate the solution | "How do we know this solution works?" |

---

## Hypothesis Template

For each Solution, create a structured hypothesis:

```
HYPOTHESIS

We believe that [TARGET CUSTOMER/SEGMENT]
have the problem/need of [KEY PAIN, FRUSTRATION, OR UNMET NEED]
and that providing [PROPOSED SOLUTION]
will result in [EXPECTED OUTCOME OR BEHAVIOR CHANGE]
```

### Example (Process Governance)

```
We believe that workflow administrators
have the problem/need of not being able to test workflow changes safely
and that providing a sandbox testing environment
will result in 40% fewer production incidents from workflow changes
```

---

## Product Risk Assessment

For each Solution, evaluate four risk categories:

### 1. Value Risk
**Question**: Will customers use it / pay for it?
- Does this solve a real, frequent problem?
- How many customers have requested this?
- What's the evidence of demand?

### 2. Usability Risk
**Question**: Can customers figure out how to use it?
- Is the interaction model intuitive?
- Does it fit existing mental models?
- What training would be required?

### 3. Feasibility Risk
**Question**: Can we build it?
- Do we have the technical capability?
- What dependencies exist?
- What's the estimated effort?

### 4. Viability Risk
**Question**: Should we build it?
- Does it align with business strategy?
- What's the opportunity cost?
- Are there regulatory/compliance concerns?

### Risk Matrix Output

```markdown
| Risk Type | Level | Evidence | Mitigation |
|-----------|-------|----------|------------|
| Value | Low/Med/High | [Data] | [Action] |
| Usability | Low/Med/High | [Data] | [Action] |
| Feasibility | Low/Med/High | [Data] | [Action] |
| Viability | Low/Med/High | [Data] | [Action] |
```

---

## Success Criteria

Define measurable success criteria for each solution:

### Types of Criteria

| Type | Example | Measurement |
|------|---------|-------------|
| **Adoption** | "50% of workflow admins use sandbox within 3 months" | Usage analytics |
| **Behavior Change** | "Testing before publishing increases from 20% to 80%" | Workflow logs |
| **Outcome Impact** | "Production incidents from workflow changes drop 40%" | Support tickets |
| **Satisfaction** | "NPS for workflow editing improves by 15 points" | Survey |

### Success Criteria Format

```markdown
### Success Criteria for [Solution Name]

**Leading Indicators** (early signals):
1. [Metric] reaches [target] within [timeframe]
2. ...

**Lagging Indicators** (outcome confirmation):
1. [Metric] reaches [target] within [timeframe]
2. ...

**Minimum Success Threshold**: [What's the minimum to consider this successful?]
```

---

## Validation Techniques

Choose appropriate validation methods based on risk level:

### Discovery Techniques (Before Building)

| Technique | Best For | Effort |
|-----------|----------|--------|
| **Customer Interviews** | Understanding problems deeply | Low |
| **Prototype Testing** | Usability risk | Medium |
| **Fake Door Test** | Value risk (demand validation) | Low |
| **Concierge MVP** | Value + feasibility risk | Medium |
| **Competitor Analysis** | Market validation | Low |
| **Data Analysis** | Quantifying problem scope | Low |

### Delivery Techniques (While/After Building)

| Technique | Best For | Effort |
|-----------|----------|--------|
| **A/B Test** | Comparing solutions | High |
| **Beta Program** | Early feedback | Medium |
| **Feature Flag Rollout** | Gradual validation | Medium |
| **Usage Analytics** | Adoption tracking | Low |
| **Customer Feedback Loop** | Satisfaction measurement | Low |

### Validation Plan Format

```markdown
### Validation Plan for [Solution Name]

**Riskiest Assumption**: [What's the biggest unknown?]

**Validation Technique**: [Method]

**Success Signal**: [What would prove/disprove the hypothesis?]

**Timeline**: [When will we know?]

**Decision**: If successful → [next step]. If not → [pivot/kill]
```

---

## Workflow Steps

### Step 1: Define the Outcome

**When user provides a goal or problem area:**

1. Clarify the outcome is measurable
2. Ensure it's a business/product metric, not a feature
3. Confirm timeframe and target

**Output:**
```markdown
## Outcome

**Goal**: [Measurable outcome statement]
**Metric**: [Specific KPI]
**Target**: [Number/percentage]
**Timeframe**: [When]
```

### Step 2: Map Opportunities

**Analyze customer insights to identify opportunities:**

1. Review Productboard insights, support tickets, interviews
2. Frame as customer problems (not solutions)
3. Prioritize by frequency and severity
4. Ensure opportunities are distinct (mutually exclusive)

**Output:**
```markdown
## Opportunities

### Opportunity 1: [Customer Problem]
- **Evidence**: [X customers mentioned this, Y support tickets]
- **Severity**: High/Medium/Low
- **Frequency**: How often does this occur?

### Opportunity 2: [Customer Problem]
...
```

### Step 3: Generate Solutions

**For each opportunity, brainstorm solutions:**

1. Generate 2-3 possible solutions per opportunity
2. Keep solutions focused (not feature bundles)
3. Consider build vs buy vs partner

**Output:**
```markdown
## Solutions for [Opportunity Name]

### Solution A: [Name]
- **Description**: [What we would build]
- **Hypothesis**: We believe that...

### Solution B: [Name]
...
```

### Step 4: Assess Risks

**For each solution, evaluate risks:**

1. Score each risk dimension (Low/Medium/High)
2. Identify the riskiest assumption
3. Determine if risks are acceptable

**Output:**
```markdown
## Risk Assessment: [Solution Name]

| Risk | Level | Evidence | Mitigation |
|------|-------|----------|------------|
| Value | | | |
| Usability | | | |
| Feasibility | | | |
| Viability | | | |

**Riskiest Assumption**: [Statement]
```

### Step 5: Define Success Criteria

**For each solution being pursued:**

1. Define leading and lagging indicators
2. Set minimum success thresholds
3. Determine measurement approach

### Step 6: Plan Validation

**For each solution being pursued:**

1. Choose validation technique based on risk
2. Define success signals
3. Set timeline and decision criteria

---

## Process Governance Value Metrics

Use this framework to measure and communicate value from Process Governance implementations.

### The Value Story (4 Steps)

```
Step 1: Measure the baseline (Value Identified) — "This is where we are"
Step 2: Deploy Process Governance workflows
Step 3: Measure the outcome (Value Realized) — "This is what we achieved"
Step 4: Report the delta — "This is the value delivered"
```

### Executive Summary Template

**VALUE IDENTIFIED (Baseline)**:
```
Before Process Governance: [X] day average cycle time, [Y]% compliance gaps,
[Z] hours/week manual coordination, no audit trail, unknown bottlenecks.
```

**VALUE REALIZED (Outcome)**:
```
After Process Governance: [A] day cycle time ([B]% faster), [C]% compliance rate,
[D] hours/week saved, 100% audit coverage, top [E] bottlenecks identified and addressed.
```

### Value Metrics Table

| Metric Category | Value Identified (Measure First) | Value Realized (Then Track) | Frequency |
|-----------------|----------------------------------|----------------------------|-----------|
| **Speed** | Baseline cycle time (days) | Current cycle time, % reduction | Weekly |
| **Volume** | Manual capacity (cases/month) | Current throughput, % increase | Monthly |
| **Quality** | Compliance gap %, error rate | Compliance rate %, error reduction | Monthly |
| **Risk** | Audit findings, documentation gaps | Audit trail completeness % | Quarterly |
| **Adoption** | Target users, processes to cover | Active users, workflows deployed | Monthly |
| **Efficiency** | Manual hours/week, FTE cost | Hours saved, FTE equivalent freed | Quarterly |

### Value Metrics Output Format

```markdown
## Process Governance Value Report: [Process Name]

### Baseline (Value Identified)
| Metric | Before | Date Measured |
|--------|--------|---------------|
| Cycle Time | X days | YYYY-MM-DD |
| Compliance Rate | Y% | YYYY-MM-DD |
| Manual Hours/Week | Z hrs | YYYY-MM-DD |
| Audit Coverage | W% | YYYY-MM-DD |

### Outcome (Value Realized)
| Metric | After | Improvement |
|--------|-------|-------------|
| Cycle Time | A days | B% faster |
| Compliance Rate | C% | +D points |
| Manual Hours/Week | E hrs | F hrs saved |
| Audit Coverage | 100% | Full coverage |

### Value Summary
- **Time Saved**: [X] hours/week → [Y] hours/year
- **FTE Equivalent**: [Z] FTE freed for higher-value work
- **Risk Reduction**: [W] audit findings eliminated
- **ROI**: [Calculate based on time saved × hourly rate]
```

---

## Signavio Process Governance Context

### Common Outcomes

- Reduce workflow-related support tickets
- Increase workflow adoption across customer base
- Improve workflow development efficiency
- Decrease time-to-value for new workflow implementations
- Improve governance compliance rates

### Common Opportunity Areas

1. **Testing & Validation** - Cannot test workflows safely before production
2. **Publishing & Version Control** - Lack of controls for releasing workflows
3. **Design & Authoring** - Builder lacks needed capabilities
4. **Execution & Scheduling** - Cannot control runtime behavior
5. **Integration** - Data doesn't flow between systems
6. **Compliance** - Cannot meet audit requirements

### Typical Solutions

- Sandbox/test environments
- Approval workflows for publishing
- Form builder enhancements
- Scheduling capabilities
- API integrations
- Audit logging

---

## Commands

| User Says | Claude Does |
|-----------|-------------|
| "Create OST for [outcome/problem]" | Full OST generation |
| "Map opportunities for [area]" | Opportunity discovery |
| "Generate solutions for [opportunity]" | Solution brainstorming |
| "Assess risks for [solution]" | Risk matrix |
| "Define success criteria for [solution]" | Success criteria |
| "Plan validation for [solution]" | Validation plan |
| "Create value metrics for [process]" | Value Identified/Realized report |

---

## Output Templates

### Full OST Document

```markdown
# Opportunity Solution Tree: [Outcome]

## 1. Outcome
**Goal**: [Statement]
**Metric**: [KPI]
**Target**: [Number]

## 2. Opportunities
[List with evidence]

## 3. Solutions
[Per opportunity, with hypotheses]

## 4. Risk Assessments
[Per solution]

## 5. Success Criteria
[Per solution being pursued]

## 6. Validation Plans
[Per solution being pursued]

## 7. Recommended Path
[Which solution to pursue first and why]
```

---

## Integration with Other Skills

- **#productboard-categorization-wizard** - Use categorized insights as opportunity input
- **#prd** - Convert validated solutions into PRDs
- **#jira** - Create experiment tickets
- **#continuous-discovery-habits** - Deeper CDH framework guidance
