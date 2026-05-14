# Signavio Partner Process & Onboarding

> Sources:
> - How to Become a SAP Signavio Technology Partner (Manuel Taechl, public — link #20)
> - Think Tank BBP (Dec 12, 2025, internal — link #22)
> - SAP Signavio Ecosystem Integrations (Mar 6, 2026, internal — link #27)
> - SAP Signavio Integration and Extension Guide (Mar 2026, public — link #29)
> Last updated: 2026-03-27

---

## The 4-Phase Partner Journey

### Phase 1: Evaluate & Apply
- **Intro & Demos**: Show Signavio solutions, explore joint value proposition
- **Explore**: SAP Signavio 30-day Trial available
- **Discuss**: Joint use cases, develop PoCs/PoVs
- **Identify**: Potential joint customers and partners
- **NDA**: Sign NDA/agreements if needed
- **Apply**:
  - SAP PartnerEdge OpenEcosystem, Build (free) — pre-market, access to BTP/dev resources
  - SAP PartnerEdge, Build (annual fee) — for market-ready solutions

### Phase 2: Build & Integrate
- Read SAP Signavio API & Integrations Overview
- Read SAP Signavio Integration and Extension Guide
- Access SAP Signavio APIs and SAP Business Accelerator Hub
- Obtain TDD (Test, Demo & Development) license

### Phase 3: Validate & Publish
- **Due Diligence**: SAP evaluates partner
- **ARC**: Application Readiness Check (technical assessment)
- **SAP Store**: Sign agreement, onboard solution, follow content guidelines

### Phase 4: Launch & Grow
- Announcement + press release (partner-initiated)
- GTM enablement, badges, logos
- Transact via SAP Store (revenue share)
- Attend events, develop success stories
- Progress through Partner Solution Progression Framework

**Contact**: Manuel Taechl (manuel.taechl@sap.com)

---

## BBP at Signavio: Think Tank Insights (Dec 2025)

### HPOM Makes BBP a PM Responsibility
- Harmonized Product and Operations Model (HPOM) now places Build/Buy/Partner decisions under Product Management — not just PES/BD
- PM drives BBP at the product level, as part of product discovery

### Why Technology Partners? Three Pillars

**1. Customer Engagement & Retention**
- Increase stickiness, prevent churn (e.g., GRC use cases)
- Foster adoption and time-to-value (e.g., pre-built risk mining content)
- Expand use cases to new departments (risk, data governance)

**2. Market Growth & Competitive Advantage**
- Expand addressable market (niche or mid-market capabilities)
- Revenue growth (revenue share, referrals, bigger deal sizes)
- Competitive advantage and analyst attractiveness (e.g., strategy-to-execution play with Tangible Growth)
- Leverage vendor credibility in RFPs

**3. Product & Innovation Enhancements**
- Complement functionality we won't build (e.g., Task Mining)
- Innovation/differentiation (e.g., Risk Mining)
- Integrated journeys (e.g., synchronize repository)
- Data access (e.g., sentiment via Medallia, manufacturing via ONIQ)

### The E2E Process (Whitespace → GTM)

Two parallel streams running the partner lifecycle:

| Stream | Roles |
|---|---|
| **Products & Engineering** | Product Management, Product Marketing, Product Strategy |
| **PES (ISV)** | Portfolio Lead, Business Development, Partner Management |

Phases: E2E Planning → Semester Planning → Whitespace Identification → Partner Scouting → Evaluation → Onboarding → Integration → GTM Activation → Performance Management

### Honest Assessment (Observations from Think Tank)
- **"Partner-first, not whitespace-first"**: Partners come to us; we don't proactively identify gaps and then find partners
- BBP needs to be part of **(A) SAP Signavio Product Strategy** and **(B) Product Area Strategies**
- PES and GTM work at BTM-level; BBP at Signavio is Signavio-only
- **Asks (Q4 2025 / Q1 2026)**: Product Areas to drive Whitespace identification; create Suite-wide capability matrix; align BBP as strategy practice

### Business Capability Matrix
A template for mapping:
- Business Areas → Business Capabilities → Maturity levels → Partner(s)
- Used to identify whitespace systematically rather than reactively

---

## Signavio Integration Ecosystem

### Scale
- **20+ SAP integrations** (S/4HANA, Ariba, SuccessFactors, LeanIX, Cloud ALM, etc.)
- **30+ technical ecosystem integrations** (non-SAP)
- **5 strategic tech partner categories** + SAP Store partner solutions

### Strategic Technology Partner Categories

| Category | Partners | Value |
|---|---|---|
| **Task Mining** | KNOA, KYP.ai, Mimica | Granular user-task analysis combined with event logs for AI & automation |
| **Risk Mining & Financial Integrity** | Datricks | Audit, risk, compliance, fraud — rapid time-to-value with instant risk insights |
| **Strategy Management** | Tangible Growth | Bridge strategy-to-execution gap; link strategic choices to Signavio analytics |
| **Experience Management** | Medallia | Omnichannel experience data correlated with operational process logs |
| **Data Transformation** | (emerging) | Accelerate process mining with reliable, high-quality data models |

### 5 Integration Patterns

| # | Pattern | Direction | Examples |
|---|---|---|---|
| 1 | **Analyze Enterprise Apps & Data** | Inbound | ERP data, task mining (KNOA/KYP/Mimica), risk mining (Datricks), sentiment (Medallia) |
| 2 | **Trigger Workflows & Automation** | Bidirectional | SAP Build, Integration Suite, Event Mesh, UiPath, webhooks |
| 3 | **Integrated Repository** | Bidirectional | Sync dictionary with LeanIX, Cloud ALM, RAM, Collibra, SuccessFactors |
| 4 | **Extract Process Data for Reporting** | Outbound | SAP Analytics Cloud, Datasphere, Power BI, OData API |
| 5 | **Embed Content** | Outbound | Diagrams in Confluence, SharePoint, iFrames; widgets in Journey Models |

### Integration Tools (by complexity)

| Tool | Best For | License |
|---|---|---|
| **SAP Signavio Process Governance** | Approval workflows with manual steps, BPMN-based | Included (free) |
| **SAP Integration Suite** | Complex logic, external systems, scheduled jobs, on-premise access | Separate license |
| **SAP Datasphere** | Data integration, replication flows | Separate license |
| **SAP Build Process Automation** | Low-code workflow automation, RPA | Separate license |
| **Scripting / Custom Apps** | Postman, programming languages, API testing | N/A |

### Signavio as Orchestrator
SAP Signavio positioned as central orchestrator for business transformations:
- Inbound: enterprise systems, adjacent data (task mining, risk mining, sentiment)
- Processing: process intelligence, governance, modeling
- Outbound: analytics, automation triggers, embedded content, toolchain sync

### Key Stats
- 83% of organizations consider enterprise integration a top-5 business priority (SAP 2022)
- 39% cite integrations as most important factor when selecting software (Gartner 2023)

---

## Technical Deep Dives (from Extension Guide)

### Process Intelligence Integration
- **Data Management**: Connect to ERP, CRM, DBMS via native connectors; Ingestion API for custom sources; SAP Integration Suite for Salesforce/Coupa/Workday
- **Adjacent Data**: Risk mining (Datricks), task mining (KNOA/KYP/Mimica), sentiment (Medallia/Qualtrics)
- **Analytics**: OData SIGNAL API for external reporting (Excel, SAP Analytics Cloud)
- **Actions**: Trigger SAP Build Process Automation, SAP Event Mesh, SAP Integration Suite, webhooks (UiPath), Microsoft Teams notifications

### Process Manager Integration
- **Repository Sync**: LeanIX (IT systems), Cloud ALM/Solution Manager (ALM), RAM (risks/controls), Collibra (data objects), SuccessFactors (HR data)
- **Content Export**: Process landscape → EAM/ALM/GRC tools
- **Embedding**: Diagrams as images/HTML in Confluence, SharePoint; iFrames for Collaboration Hub
- **New**: Central API Gateway introduced for harmonized API management across the suite

### Journey Modeler Integration
- Embed external widgets (Qualtrics, Tableau, SAP Analytics Cloud) for live data in journey maps
- API for pushing customer experience metrics

---

## To Be Added

- [ ] Signavio tech partner funnel stages (link #21)
- [ ] PPWG specifics for Signavio nominations (link #14)
- [ ] Timeline expectations per stage
- [ ] Common blockers and how to resolve them
