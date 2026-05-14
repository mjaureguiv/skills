# Analyst RFI Autofill Research Report

## Executive Summary

This document provides a comprehensive analysis of how SAP fills Requests for Information (RFIs) for multiple market categories. The analysis covers RFIs from QKS Group (SPARK Matrix), Gartner (Magic Quadrant/Market Guide), and supporting documentation from 2021-2026.

### Supported Market Categories

| Market Category | Focus Products | Reference Files |
|-----------------|----------------|-----------------|
| **Digital Twin of an Organization (DTO)** | SAP Signavio, SAP LeanIX, WalkMe | QKS SPARK Matrix, Gartner DTO surveys |
| **Enterprise Architecture Tools (EA Tools)** | SAP LeanIX | Gartner MQ 2025 |

**Purpose**: Enable automated pre-filling of future analyst RFIs by understanding:
1. The structure and categories of questions asked
2. Patterns in how SAP answers different question types
3. Boilerplate responses that can be reused
4. How RFI formats evolve year-over-year
5. Key product capabilities and messaging

---

## Critical Notes for Autofill

### Excel Column Structure: Answers vs. Context

**IMPORTANT**: Not all columns in the RFI Excel files contain actual answers. The column structure typically follows this pattern:

| Column Type | Purpose | Use in Autofill |
|-------------|---------|-----------------|
| **Question Column** | The analyst's question text | Reference only |
| **Answer Guidance** | Instructions on how to answer | Reference only |
| **Character Limit** | Max characters allowed | Constraint to respect |
| **Your Response** | **THE ACTUAL ANSWER** | **Primary source for autofill** |
| **Additional Information** | Supporting details, links, notes | Secondary/optional |
| **Remarks/Comments** | Internal notes, reviewer names | Do NOT include in answers |

**QKS SPARK Matrix typical columns:**
- Column A-B: Question/Sub-question labels
- Column C: **Primary Answer** (use this)
- Column D: Remarks/USP notes (context only)
- Column E: Roadmap information (context only)

**Gartner MQ typical columns:**
- Question Status | Question No. | Question Title | Answer Guidance | Character Count
- **Your Response** ← This is the answer column
- Additional Information | Subsection Name | Is Question New | Last Updated

**When extracting answers**: Focus on the "Your Response" or primary answer column. The additional columns provide helpful context but should not be copied verbatim into new RFI responses.

### Answer Relevance by Year

**IMPORTANT**: When multiple years of RFI responses are available, prioritize the most recent answers.

| Year | Relevance | Usage Guidance |
|------|-----------|----------------|
| **2025/2026** | **Highest** | Use as primary source - most current product info, messaging, capabilities |
| **2024** | High | Good fallback if 2025 doesn't cover a topic; verify product names/versions |
| **2023** | Medium | Useful for historical context; likely needs updates |
| **2021-2022** | Low | Reference only - significant product changes since then |

**Why recency matters:**
- **Product portfolio evolves**: WalkMe added in 2024, LeanIX added in 2023
- **Messaging changes**: "SAP Signavio" branding vs older "Signavio" naming
- **Capability updates**: AI features (Joule, Agentic AI) are recent additions
- **Market positioning**: Competitor landscape and rankings shift yearly
- **Customer references**: Some customers may no longer be referenceable
- **Roadmap items**: Features listed as "planned" may now be GA

**Best practice for autofill:**
1. Start with the most recent answer (2025/2026)
2. If no match, check 2024
3. For older answers, use as inspiration but rewrite with current product info
4. Always verify: product names, version numbers, dates, and roadmap items

---

## Table of Contents

1. [RFI Sources Overview](#1-rfi-sources-overview)
2. [QKS SPARK Matrix RFI Structure](#2-qks-spark-matrix-rfi-structure)
3. [Gartner RFI Structure](#3-gartner-rfi-structure)
4. [Standard Answer Patterns](#4-standard-answer-patterns)
5. [Boilerplate Responses](#5-boilerplate-responses)
6. [Product Capabilities Reference](#6-product-capabilities-reference)
7. [Year-over-Year Evolution](#7-year-over-year-evolution)
8. [Key Customer References](#8-key-customer-references)
9. [Partner Ecosystem](#9-partner-ecosystem)
10. [Competitive Positioning](#10-competitive-positioning)
11. [Extracted Data Files](#11-extracted-data-files)
12. [Autofill Strategy](#12-autofill-strategy)

---

## 1. RFI Sources Overview

### Available Source Documents

| Source | Type | Years | Files |
|--------|------|-------|-------|
| **QKS Group** | SPARK Matrix RFI | 2021, 2023, 2024, 2025 | 4 Excel files |
| **Gartner** | Market Guide Survey | 2022, 2024 | 2 Excel files |
| **Gartner** | MQ Questionnaire | 2026 | 1 Excel file |
| **Gartner** | Pre-Survey | 2026 | 1 Excel file |

### Product Being Evaluated

**2025 Configuration**: SAP Signavio, SAP LeanIX, and WalkMe
- SAP Signavio: Process Transformation Suite (acquired 2021)
- SAP LeanIX: Enterprise Architecture Management (acquired 2023)
- WalkMe: Digital Adoption Platform (acquired 2024)

### Primary Analyst Contacts (2025)

| Analyst Firm | Contact | Email |
|--------------|---------|-------|
| QKS Group | Nipuna M | nipunam@qksgroup.com |
| QKS Group | Nikhilesh Naik | nikhileshn@qksgroup.com |
| Gartner | Marc Kerremans | (DTO research lead) |

---

## 2. QKS SPARK Matrix RFI Structure

### Sheet Structure (4 Sheets)

1. **General Questions** - Company info, revenue, customers, capabilities, roadmap
2. **Criteria Specific Questions** - Technical deep-dive questions
3. **Technology Excellence Criteria** - Weighted scoring criteria
4. **SPARK Matrix Criteria** - Customer Impact scoring

### General Questions Categories (2025)

| # | Category | Rows | Questions |
|---|----------|------|-----------|
| 1 | Revenue Details | 11-32 | Revenue by year, geography, company size, deployment |
| 2 | Customer Details | 34-48 | Customer counts, by size, top customers |
| 3 | Industry Presence | 50-65 | Industry vertical rankings (1-12) |
| 4 | Product Capabilities | 67-153 | Features, use cases, scalability (LARGEST SECTION) |
| 5 | Enhancements & R&D | 155-188 | New features 2024, R&D investment, roadmap |
| 6 | Competitors | 190-210 | Top 5 competitors by geography |
| 7 | Differentiators | 214-218 | Technology & strategic differentiators |
| 8 | Partner Ecosystem | 220-245 | Technology & channel partners |
| 9 | Technology Trends | 248-287 | Market trends, selection criteria, driving factors |

### Product Capabilities Sub-Categories (Section 4a)

| Sub-Category | Focus Area | Key Products |
|--------------|------------|--------------|
| **A. Process Mining & Intelligence** | Mining, modeling, simulation | SAP Signavio Process Intelligence |
| **B. Business Performance & Decision Intelligence** | KPIs, metrics, dashboards | SAP Signavio Process Transformation Manager |
| **C. Enterprise Architecture & IT Landscape** | Meta model, discovery, APIs | SAP LeanIX |
| **D. Governance, Risk & Compliance** | SBOM, GRC integration | SAP Signavio + Datricks |
| **E. Business Transformation & Roadmap** | Planning, value tracking | SAP Signavio Transformation Manager |
| **F. Customer, Employee & Journey Intelligence** | Journey modeling, adoption | WalkMe + SAP Signavio |
| **G. Automation & Agentic AI** | AI orchestration | SAP Business AI, Joule |

### Technology Excellence Criteria Weights (2025)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Advanced Digital Modeling & Simulation | **0.25** | High-fidelity models, process simulation |
| Real-Time Data Integration | **0.20** | IoT, ERP, CRM synchronization |
| AI-Driven Predictive Analytics | 0.15 | Forecasting, optimization |
| Interoperability and Integration | 0.15 | Enterprise app connectivity |
| Scenario Planning & What-If Analysis | 0.10 | Risk evaluation, change impact |
| Scalability & Cloud-Native Architecture | 0.05 | Cloud deployment flexibility |
| Technology Vision & Roadmap | 0.05 | Future direction |
| Application Diversity and Use Cases | 0.05 | Cross-departmental applicability |

### Customer Impact Criteria Weights

| Criterion | Weight |
|-----------|--------|
| Product Strategy & Performance | 0.20 |
| Market Presence | 0.20 |
| Proven Record | 0.15 |
| Ease of Deployment & Use | 0.15 |
| Customer Service Excellence | 0.15 |
| Unique Value Proposition | 0.15 |

---

## 3. Gartner RFI Structure

### Gartner Pre-Survey Structure (2026)

| Section | Questions |
|---------|-----------|
| 1. Alignment to DTO Market | Named platform, branding, GTM strategy |
| 2. Revenue, Growth, Customer Base | Logos by region, acquisitions, revenue range |
| 3. Capabilities Checklist | 25 capability areas (Native/3rd Party/None) |
| 4. Use Cases | 12 use cases with priority rating |
| 5. Competition | Top 3-5 competing vendors |

### Gartner MQ Questionnaire Structure (2026)

16 sheets covering:
- Product or Service
- Overall Viability
- Sales Execution/Pricing
- Market Responsiveness/Record
- Marketing Execution
- Customer Experience
- Operations
- Market Understanding
- Marketing Strategy
- Sales Strategy
- Offering (Product) Strategy
- Business Model
- Vertical/Industry Strategy
- Innovation
- Geographic Strategy
- Data

### Gartner DTO Building Blocks (Gartner Market Guide 2023)

| Block | Description |
|-------|-------------|
| **Map** | Digitalized business operations model |
| **Destination** | Digital transformation goals |
| **Performance** | Business performance management |
| **Situation** | Business operations intelligence |
| **Value** | Business decisions creating stakeholder value |

### Gartner Capability Areas (2026 Pre-Survey)

| # | Capability | SAP Response |
|---|------------|--------------|
| 1 | Models of processes and tasks | Native (SAP Signavio) |
| 2 | Models of capabilities and resources | Native (SAP LeanIX) |
| 3 | Models of agentic capabilities | Native (SAP LeanIX + Signavio) |
| 4 | Models of deliverables and components | Native (SAP Signavio) |
| 5 | Models of client/supplier stakeholders | Native (SAP Signavio Journey Modeler) |
| 6 | Orchestration repository | Native |
| 7 | Performance measurement schemes | Native |
| 8 | Advanced analysis techniques - Root cause | Native |
| 9 | Advanced analysis techniques - Scenario testing | Native |
| 10 | Advanced analysis techniques - External data | Native |
| 11 | Risk management and monitoring | Native |
| 12 | Event processing | Native (SAP Integration Suite) |
| 13 | Data connectivity | Native |
| 14 | AI - Conversational/explainability | Native (Joule) |
| 15 | AI - Data discovery/cleaning | Native (SAP Syniti) |
| 16 | AI - Interdependency interpretation | Native |
| 17 | AI - Real-time monitoring/anomaly detection | Native |
| 18 | Real-time intelligence | Native (SAP BDC) |
| 19 | Process mining capabilities | Native (SAP Signavio) |
| 20 | Simulation capabilities | Native |
| 21 | Graphical capabilities | Native |
| 22 | Decision Intelligence | Native |
| 23 | Process automation support | Native (SAP Build) |
| 24 | Project/program data access | Native |
| 25 | Ecosystem support | Native |

---

## 4. Enterprise Architecture Tools (EA Tools) Market

### Gartner MQ for EA Tools - Structure (2025)

The Gartner Magic Quadrant for Enterprise Architecture Tools covers SAP LeanIX specifically and has a 16-sheet structure:

**Sheets:**
1. **Product or Service** - Core product capabilities (Q1-Q65)
2. **Overall Viability** - Financial health, cash flow, debt (Q124-Q140)
3. **Sales Execution/Pricing** - Deal closing rates, pricing models (Q141-Q151)
4. **Market Responsiveness/Record** - Market reaction, examples (Q152-Q157)
5. **Marketing Execution** - Promotion, messages, initiatives (Q158-Q168)
6. **Customer Experience** - Support, time-to-value, churn (Q169-Q187)
7. **Operations** - Support capabilities, FTE counts (Q188-Q194)
8. **Market Understanding** - Competitors, use cases (Q195-Q204)
9. **Marketing Strategy** - Elevator pitch, differentiation (Q205-Q211)
10. **Sales Strategy** - Multi-year deals, pricing options (Q212-Q222)
11. **Offering (Product) Strategy** - Entry level, differentiators (Q223-Q229)
12. **Business Model** - Current model, partnerships (Q230-Q235)
13. **Vertical/Industry Strategy** - Customer distribution by industry (Q236-Q238)
14. **Innovation** - R&D investment, innovation examples (Q239-Q245)
15. **Geographic Strategy** - Regional presence, FTEs (Q246-Q256)
16. **Data** - Dropdown options (skip)

### Key SAP LeanIX Differentiators (EA Tools)

| Differentiator | Description |
|----------------|-------------|
| **AI-agent-ready architecture** | Cloud-native microservices, no on-prem legacy, daily feature delivery |
| **Automated discoveries** | SaaS shadow IT, self-built software, SAP landscape discovery |
| **Built-in reference data** | IT component lifecycles, tech categories, integrated workflows |
| **ServiceNow integration** | Bidirectional, real-time, asset aggregation, multi-instance |
| **SAP Business AI access** | Joule integration, multi-vendor AI/LLM technology |
| **Unlimited user pricing** | Crowd-sourcing, broad collaboration beyond architects |

### SAP LeanIX Top 10 Use Cases (EA Tools 2025)

1. Application Portfolio Assessment
2. Business Capability Modeling
3. Application Rationalization
4. Obsolescence Risk Management
5. Application Modernization
6. ERP Transformation
7. Post Merger IT Integration & Carve Out
8. AI Adoption & Governance
9. Automated product architecture & SBOM
10. Digital Operational Resiliency Act (DORA)

### Key EA Tools URLs

| Resource | URL |
|----------|-----|
| LeanIX Documentation | http://docs-eam.leanix.net |
| SAP Help (from July 2025) | https://help.sap.com/docs/LEANIX |
| LeanIX Website | https://www.leanix.net |

---

## 5. Standard Answer Patterns

### Pattern 1: Capability Description (Three-Part Structure)

```
[Capability Name]

[Feature Description - 1-3 paragraphs detailing what it does]

Value for Digital Twin of an Organization: [1-2 paragraphs explaining DTO relevance]

[Roadmap]: [Optional - future developments with dates if known]
```

**Example**:
```
Process Modeling

Enables comprehensive process modeling and governance using various notations
such as BPMN and DMN. Supports hierarchical process structures with traceability
from enterprise-level processes down to detailed tasks.

Value for Digital Twin of an Organization: Provides a structured approach to
gather, organize and manage process knowledge, enabling organizations to create
accurate digital representations of their operations.

[Roadmap]: The AI-assisted process modeler, including text-to-process conversion,
is currently in SAP Labs and planned for general availability in March 2025.
```

### Pattern 2: Rating with Justification

```
[Question about capability/service]

Rating: [X/10]

[Multi-paragraph justification with bullet points covering]:
- Evidence/proof points
- Specific features supporting the rating
- Customer testimonials or metrics
```

### Pattern 3: Use Case Description

```
[Use Case Name]

[Context paragraph - what challenge does this address]

[Solution paragraph - how SAP addresses it]

[Customer examples/outcomes if available]
```

### Pattern 4: Partner Description

```
[Partner Name] - [Capability/Role]

[1-2 sentence partnership description]
[Integration details if relevant]
```

### Pattern 5: Trend Response

```
[Trend Name]

[Challenge/Context paragraph - why this trend matters]

[SAP Response paragraph - how SAP/DTO addresses it]
```

---

## 6. Boilerplate Responses

### Boilerplate 1: Financial Non-Disclosure (CRITICAL - Use for ALL revenue/customer count questions)

```
SAP is a publicly traded company, we can't disclose revenue-sensitive information
or projections outside our scheduled public financial disclosures to avoid
information asymmetry in the market. Customer and revenue numbers fall in this
category, because these function as a signal to the market on how SAP's execution
is tracking against our strategy. For more info please go to
http://www.sap.com/investors/en.html
```

### Boilerplate 2: DTO Value Statement

```
Value for Digital Twin of an Organization: [INSERT CAPABILITY-SPECIFIC TEXT]
```

### Boilerplate 3: Reference to Prior Section

```
This section contains the same information as previously stated in the table above.
Please refer to the earlier response for details.
```

### Boilerplate 4: Feature Availability Notes

**For Beta Features**:
```
NOTE: This feature is currently available to a select group of clients, and its
general availability is scheduled for Q[X] 2025.
```

**For Lab Features**:
```
...is currently available in the SAP Lab Space.
```

**For Open Beta**:
```
...is currently in open beta.
```

### Boilerplate 5: Company Overview

```
SAP is a global software company that provides enterprise solutions to manage
business operations and customer relations. Its offerings include multiple
solutions such as Enterprise Resource Planning (ERP), data analytics, supply
chain management, and cloud-based services. SAP's Digital Twin of the
Organization (DTO) capabilities are delivered through the SAP Signavio Process
Transformation Suite (acquired in 2021), SAP LeanIX Enterprise Architecture
(acquired in 2023), and WalkMe Digital Adoption Platform (acquired in 2024).
```

### Boilerplate 6: GTM Strategy

```
GTM strategy focuses on observable enterprise value. It empowers organizations,
through dynamically composable and AI-powered solutions, to establish
transformation as a capability; powered by intelligent processes, enterprise
architecture, consolidated data landscapes, to accelerate and de-risk continuous
transformation.

Strategy leverages marketing campaigns, global partner ecosystem; customer
testimonials; analysts; communities & academia.
```

---

## 7. Product Capabilities Reference

### SAP Signavio Capabilities

| Capability | Description | DTO Value |
|------------|-------------|-----------|
| Process Modeling | BPMN 2.0, DMN, CMMN, EPC, Value Chains | Structured process knowledge organization |
| Process Mining | Event log analysis, variant detection | Data-driven process insights |
| Process Simulation | Discrete Event Simulation (DES) | What-if analysis, optimization |
| Process Intelligence | Real-time dashboards, KPIs | Performance monitoring |
| Root Cause Analysis | AI-assisted hypothesis evaluation | Identify improvement drivers |
| Transformation Manager | Initiative tracking, value management | Transformation governance |
| Journey Modeler | Customer/employee experience mapping | Stakeholder journey visualization |
| Collaboration Hub | Process publishing, feedback collection | Cross-functional alignment |
| AI Process Analyzer | Natural language process queries | Democratized insights |

### SAP LeanIX Capabilities

| Capability | Description | DTO Value |
|------------|-------------|-----------|
| Meta Model | Flexible data model configuration | Customizable architecture views |
| Application Portfolio | IT landscape visualization | Technology stack management |
| Business Capability Mapping | Capability-to-application linkage | Business-IT alignment |
| SAP Landscape Discovery | Automated SAP product detection | Accurate landscape representation |
| Technology Lifecycle Catalog | EOL/EOS tracking | Risk mitigation |
| ServiceNow Integration | CMDB synchronization | IT data accuracy |
| GraphQL/REST APIs | Programmatic access | Integration flexibility |
| Reference Catalog | Pre-built best practices | Accelerated adoption |

### WalkMe Capabilities

| Capability | Description | DTO Value |
|------------|-------------|-----------|
| Digital Adoption Platform | In-app guidance | User behavior understanding |
| Session Analytics | Usage pattern detection | Adoption measurement |
| ActionBots | Task automation | Efficiency improvement |
| Flow Analytics | User journey analysis | Friction point identification |

### Cross-Platform Capabilities

| Capability | Products Involved | Description |
|------------|-------------------|-------------|
| Joule Integration | All | AI copilot for natural language interaction |
| SAP Business AI | All | AI-powered insights and automation |
| SAP Build Integration | Signavio | Process automation handoff |
| SAP Cloud ALM | LeanIX, Signavio | Project management integration |
| SAP BTP | All | Platform services and connectivity |

---

## 8. Year-over-Year Evolution

### Key Changes 2024 → 2025

#### Questions Added (2025)

**Data Management Questions**:
- Data ingestion from multiple sources
- Pre-built connectors for enterprise systems
- Data normalization and synchronization
- Supported data formats and protocols
- Batch vs real-time data processing

**Architecture Questions**:
- Underlying platform architecture (microservices, monolithic, hybrid)
- Distributed computing for scaling
- Digital twin model expansion scalability
- Failover, redundancy, and high availability

**AI/ML Questions**:
- Predictive analytics capabilities
- AI/ML for predictive maintenance and demand forecasting
- Edge computing management

**Security/UX Questions**:
- Authentication, authorization, and auditing
- User interface customization
- Lifecycle management

#### Criteria Weight Changes

| Criterion | 2024 | 2025 | Change |
|-----------|------|------|--------|
| Digital Modeling | 0.15 | 0.25 | +67% |
| Real-Time Data Integration | 0.05 | 0.20 | **+300%** |
| Interoperability | 0.07 | 0.15 | +114% |
| Communication & Collaboration | 0.08 | REMOVED | - |
| Supporting Technologies | 0.10 | REMOVED | - |
| Scalability/Cloud-Native | NEW | 0.05 | NEW |

### Predicted Future Trends (for 2026+ RFIs)

Based on observed evolution:

1. **More AI/Agentic Questions**: Expect questions about AI agents, autonomous operations
2. **Deeper Integration Questions**: Cross-platform data flow, ecosystem connectivity
3. **Sustainability/ESG**: Environmental and governance considerations
4. **Security/Compliance**: Zero trust, data sovereignty
5. **Value Realization**: ROI measurement, business outcome tracking

---

## 9. Key Customer References

### Top 5 Customers (Referenceable)

| Customer | Industry | Use Case |
|----------|----------|----------|
| NTT | Technology | Digital Transformation |
| Hilti | Manufacturing | Operational Excellence |
| JP Morgan | Financial Services | Process Optimization |
| General Motors | Automotive | Transformation |
| Southern California Edison | Energy | Regulatory Compliance |

### Customers by Use Case (2026 Gartner Pre-Survey)

| Use Case | Customer References |
|----------|---------------------|
| Business Operations | Mondi AG, Marc O'Polo AG, Barco |
| Supply Chain | Takeda Pharmaceuticals, Fujitsu |
| Digital Transformation | Volkswagen, NTT, Travis Perkins, SAP SE, Accenture |
| Customer Excellence | Hilti, DKB, Sirius XM |
| GRC | Moog BV, Revenue NSW, Forvia Hella, Amtrust |
| Operational Excellence | Philip Morris, Yamaha, Vodafone, Viohalco, Southern California Edison |
| Enterprise Cost Optimization | Siemens, Estee Lauder, Sefe, First Abu Dhabi Bank |
| Strategy Realization | Virgin Australia, Villeroy & Boch, Viasat |
| Dynamic State Architecture | E.on, Volkswagen |

### Industry Rankings (2025)

| Rank | Industry |
|------|----------|
| 1 | CPG & Retail |
| 2 | Energy & Utilities |
| 3 | Automotive |
| 4 | Manufacturing |
| 5 | Healthcare & Lifesciences |
| 6 | Banking |
| 7 | Professional Services |
| 8 | Electronics & Semiconductor |
| 9 | Food & Beverages |
| 10 | Govt & Public Sector |
| 11 | Logistics & Transportation |
| 12 | Education |

---

## 10. Partner Ecosystem

### Technology Partners

| Partner | Capability | Integration Type |
|---------|------------|------------------|
| Datricks | Risk mining | Native integration with Signavio |
| Tangible Growth | Strategy management (OKR) | Planning integration |
| ServiceNow | IT Visibility (CMDB) | Bidirectional sync with LeanIX |
| Collibra | Data Governance | Data catalog integration |
| KYP AI | Task/user behavior mining | Event data enrichment |
| Mimica | Task mining | Process discovery |
| UiPath | Task mining, RPA | Automation handoff |
| Qualtrics | Sentiment/CX data | Experience analytics |
| Medallia | Sentiment/CX data | VoC integration |

### Channel Partners (Top 10)

| Partner | Focus |
|---------|-------|
| NTT Data | Global systems integration |
| All for One | SAP implementation |
| Kapish EA | Enterprise architecture |
| IBM | Large enterprise transformation |
| Carahsoft Technology | Government sector |
| PT Equine Global | APAC market |
| Accenture | Strategy and transformation |
| Scheer GmbH | Process consulting |
| KING ICT | CEE region |
| Valantic ERP Consulting | ERP modernization |

### Advisory Partners

McKinsey, BCG, Bain, Capgemini, Deloitte, KPMG, Infosys, PwC, Cognizant

---

## 11. Competitive Positioning

### Main Competitors (2025)

| Competitor | Geography | Strength |
|------------|-----------|----------|
| Celonis | Global (#1) | Process mining market leader |
| IBM | NA, EMEA | Enterprise breadth |
| Microsoft | NA | Platform integration |
| Software AG / ARIS | EMEA | Process modeling heritage |
| GBTEC | EMEA | BPM focus |
| iGrafx | NA | Process analysis |
| Fujitsu | JAPAC | Regional presence |

### SAP Differentiators

**Technology Differentiators**:
1. End-to-end process visibility from strategy to execution
2. Native AI integration (SAP Business AI, Joule)
3. Pre-built SAP ecosystem connectors
4. Unified platform across Process Mining, EA, and Digital Adoption
5. Enterprise-grade scalability and security
6. Multi-region global hosting
7. Continuous innovation with frequent releases

**Strategic Differentiators**:
1. SAP's existing ERP customer base
2. Integrated acquisition strategy (Signavio → LeanIX → WalkMe)
3. Global partner ecosystem
4. Investment in AI and agentic capabilities
5. Focus on business value realization
6. Strong analyst relations and recognition

---

## 12. Extracted Data Files

All historical RFI data is now in `reference-data/historical-answers/` with **clear Question → Answer format**.

### File Format

Each extracted file uses this standardized format:
```
### ROW X: [Category] > [Question]
**ANSWER:** [The actual answer SAP provided]
**REMARKS:** [Optional context/USP notes]
**ROADMAP:** [Optional future plans]
```

For Gartner files:
```
### Question X: [Question Title]
**GUIDANCE:** [How to answer - from analyst]
**CHAR_LIMIT:** [Maximum characters allowed]
**ANSWER:** [SAP's response]
```

### QKS RFI Extractions (SPARK Matrix)
| File | Year | Priority |
|------|------|----------|
| `2025_QKS_SPARK_Matrix_RFI.txt` | 2025 | **Highest** |
| `2024_QKS_SPARK_Matrix_RFI.txt` | 2024 | High |
| `2023_QKS_SPARK_Matrix_RFI.txt` | 2023 | Medium |
| `2021_QKS_SPARK_Matrix_RFI.txt` | 2021 | Low |

### Gartner Extractions
| File | Year | Type | Priority |
|------|------|------|----------|
| `2026_Gartner_DTO_Presurvey.txt` | 2026 | DTO Pre-Survey | **Highest** |
| `2026_Gartner_Process_Intelligence_MQ.txt` | 2026 | MQ Questionnaire | **Highest** |
| `2024_Gartner_Market_Guide_Survey.txt` | 2024 | Market Guide Survey | High |
| `2022_Gartner_Market_Guide_Survey.txt` | 2022 | Market Guide Survey | Low |

### Supporting Documents
| File | Description |
|------|-------------|
| `Comparison_2024_vs_2025.txt` | Analysis of RFI changes |
| `SAP_Vendor_Profile_2025.txt` | Official vendor profile |
| `DTO_Demo_URLs.txt` | Demo resources |
| `DTO_Demo_Script_2025.txt` | Demo script |
| `SAP_PR_Analyst_Quote_2025.txt` | PR messaging |

### Market Reports
| File | Description |
|------|-------------|
| `QKS_Abridged_Report_2025.txt` | SPARK Matrix report 2025 |
| `SPARK_Matrix_Report_2024.txt` | Full SPARK Matrix 2024 |
| `Gartner_Market_Guide_2023.txt` | Gartner DTO Market Guide |

---

## 13. Autofill Strategy

### Phase 1: Question Recognition

When receiving a new RFI, classify each question into:

| Classification | Autofill Strategy |
|----------------|-------------------|
| **Revenue/Customer Numbers** | Use financial non-disclosure boilerplate |
| **Capability Questions** | Match to capability reference table |
| **Use Case Questions** | Match to use case descriptions |
| **Partner Questions** | Pull from partner ecosystem database |
| **Competitor Questions** | Pull from competitor reference |
| **Trend/Market Questions** | Match to market trend responses |
| **Technical Architecture** | Use technical capability descriptions |
| **AI/ML Questions** | Use AI capability reference |

### Phase 2: Answer Generation

For each question type:

1. **Match keywords** in the question to capability areas
2. **Retrieve base answer** from previous RFI responses
3. **Update dates/versions** to current
4. **Check for product name updates** (e.g., SAP Signavio vs Signavio)
5. **Apply standard patterns** (three-part capability structure)
6. **Add roadmap items** if applicable

### Phase 3: Review Checklist

Before submission, verify:

**Source Verification:**
- [ ] Answers pulled from "Your Response" column, not context columns
- [ ] Most recent year's answer used as primary source (2025/2026 > 2024 > older)
- [ ] Older answers updated with current product names and versions

**Content Accuracy:**
- [ ] All financial questions use non-disclosure boilerplate
- [ ] Customer names are approved for reference
- [ ] Product versions are current (check SAP Signavio release notes)
- [ ] Dates in roadmap are accurate (not outdated "planned" features)
- [ ] All "Native" capability claims are accurate
- [ ] Partner information is current
- [ ] URLs and links are valid

**Format Compliance:**
- [ ] Character limits are respected (Gartner uses 1000 char limits)
- [ ] Only answer columns filled - context columns left for internal use

### Key URLs to Maintain

| Resource | URL |
|----------|-----|
| Investor Relations | http://www.sap.com/investors/en.html |
| SAP Trust Center | https://www.sap.com/about/trust-center.html |
| Signavio Help Docs | https://help.sap.com/docs/signavio-process-intelligence/ |
| LeanIX Developer Docs | https://docs-eam.leanix.net/reference/welcome-developer-docs |
| LeanIX Integrations | https://docs-eam.leanix.net/docs/out-of-the-box-integrations |

---

## Appendix: Quick Reference Card

### When Asked About...

| Topic | Response Strategy |
|-------|-------------------|
| Revenue | ALWAYS use non-disclosure boilerplate |
| Customer count | ALWAYS use non-disclosure boilerplate |
| Customer names | Use approved list only (NTT, Hilti, JP Morgan, GM, SCE) |
| Competitors | Celonis #1, IBM #2, then region-specific |
| Deployment | Cloud = Yes, On-premise = Limited/NA |
| AI capabilities | Native - reference Joule, SAP Business AI |
| Integration | Native - reference APIs, BTP, pre-built connectors |
| Process Mining | SAP Signavio Process Intelligence |
| Enterprise Architecture | SAP LeanIX |
| Digital Adoption | WalkMe |
| All capabilities | Answer "Native" for almost everything |

---

*Report generated: 2026-03-04*
*All reference data is stored in: `skills/rfi-response-builder/reference-data/`*
