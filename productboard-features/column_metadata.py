# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Column metadata & data dictionary for ProductBoard features.

Static reference of every column an agent can encounter.
Used by describe() and --describe CLI; no data loading required.

Also contains QUERY_HINTS — few-shot examples to help AI agents
translate natural-language questions into FeatureStore filter code.
"""

from __future__ import annotations

from typing import Any

from section_parser import SECTION_CATEGORIES

# ---------------------------------------------------------------------------
# Column metadata & data dictionary
# ---------------------------------------------------------------------------
# Keys:
#   description  - What the column contains
#   type         - Python type hint (str, bool, date, number, list[str])
#   values       - Finite set of allowed values, or None for free-form
#   requires     - Which enrich_*() call adds this column, or None for base
#   aliases      - Natural-language synonyms an agent can match on

COLUMN_METADATA: dict[str, dict[str, Any]] = {
    # ==================================================================
    # BASE COLUMNS (always present after load)
    # ==================================================================
    "id": {
        "description": "ProductBoard feature UUID",
        "type": "str",
        "values": None,
        "requires": None,
        "aliases": ["feature id", "uuid"],
    },
    "name": {
        "description": "Feature title",
        "type": "str",
        "values": None,
        "requires": None,
        "aliases": ["title", "feature name", "feature title"],
    },
    "type": {
        "description": "Hierarchy level: top-level feature or child sub-feature",
        "type": "str",
        "values": ["feature", "subfeature"],
        "requires": None,
        "aliases": ["feature type", "hierarchy level"],
    },
    "description": {
        "description": "Raw HTML description body",
        "type": "str",
        "values": None,
        "requires": None,
        "aliases": ["body", "html description"],
    },
    "archived": {
        "description": "Whether the feature has been archived",
        "type": "bool",
        "values": [True, False],
        "requires": None,
        "aliases": ["is archived"],
    },
    "status_id": {
        "description": "UUID of the feature status",
        "type": "str",
        "values": None,
        "requires": None,
        "aliases": [],
    },
    "status_name": {
        "description": "Display name of the feature status (includes emoji prefix)",
        "type": "str",
        "values": [
            "\U0001f4a1 New idea",
            "\u2705 Accepted Idea",
            "\U0001f50d Discovery",
            "\U0001f6e0\ufe0f Ready for Dev",
            "\u2699\ufe0f In progress",
            "\U0001f514 Roll Out",
            "\U0001f44f\U0001f3fd GA Release / Done",
            "\U0001f622 Dropped",
        ],
        "requires": None,
        "aliases": [
            "status", "workflow status", "feature status", "stage",
            "new idea", "accepted", "discovery", "ready for dev",
            "in progress", "roll out", "done", "dropped", "ga release",
        ],
    },
    "status_completed": {
        "description": "True if the status is marked as a completed/done status",
        "type": "bool",
        "values": [True, False],
        "requires": None,
        "aliases": ["is completed", "is done"],
    },
    "parent_type": {
        "description": "Type of the parent node in the hierarchy",
        "type": "str",
        "values": ["product", "component", "feature"],
        "requires": None,
        "aliases": ["parent kind"],
    },
    "parent_id": {
        "description": "UUID of the parent node",
        "type": "str",
        "values": None,
        "requires": None,
        "aliases": [],
    },
    "parent_name": {
        "description": "Display name of the parent product, component, or feature",
        "type": "str",
        "values": None,
        "requires": None,
        "aliases": ["parent"],
    },
    "owner_email": {
        "description": "Email address of the feature owner",
        "type": "str",
        "values": None,
        "requires": None,
        "aliases": ["owner", "feature owner", "assigned to"],
    },
    "timeframe_start": {
        "description": "Planned start date (YYYY-MM-DD or empty)",
        "type": "date",
        "values": None,
        "requires": None,
        "aliases": ["start date", "planned start", "timeframe start"],
    },
    "timeframe_end": {
        "description": "Planned end date (YYYY-MM-DD or empty)",
        "type": "date",
        "values": None,
        "requires": None,
        "aliases": ["end date", "planned end", "timeframe end", "due date"],
    },
    "timeframe_granularity": {
        "description": "Granularity of the timeframe",
        "type": "str",
        "values": ["month", "quarter", "half", "year", ""],
        "requires": None,
        "aliases": ["planning granularity", "timeframe precision"],
    },
    "health_status": {
        "description": "Latest health check status",
        "type": "str",
        "values": ["on-track", "needs-attention", ""],
        "requires": None,
        "aliases": [
            "health", "feature health", "at risk", "on track",
            "needs attention", "off track",
        ],
    },
    "health_message": {
        "description": "Text message from the last health update",
        "type": "str",
        "values": None,
        "requires": None,
        "aliases": ["health note", "health comment"],
    },
    "health_date": {
        "description": "ISO 8601 timestamp of the last health update",
        "type": "date",
        "values": None,
        "requires": None,
        "aliases": ["health updated at"],
    },
    "link_self": {
        "description": "ProductBoard API URL for the feature",
        "type": "str",
        "values": None,
        "requires": None,
        "aliases": ["api link"],
    },
    "link_html": {
        "description": "ProductBoard web URL for the feature",
        "type": "str",
        "values": None,
        "requires": None,
        "aliases": ["url", "web link", "productboard link"],
    },
    "created_at": {
        "description": "ISO 8601 timestamp when the feature was created",
        "type": "date",
        "values": None,
        "requires": None,
        "aliases": ["creation date", "created"],
    },
    "updated_at": {
        "description": "ISO 8601 timestamp of the last update",
        "type": "date",
        "values": None,
        "requires": None,
        "aliases": ["last updated", "modified"],
    },

    # ==================================================================
    # ENRICHMENT COLUMNS (added by enrich_*() calls)
    # ==================================================================
    "initiatives": {
        "description": "List of initiative names linked to this feature",
        "type": "list[str]",
        "values": None,
        "requires": "enrich_initiatives()",
        "aliases": ["initiative", "strategic initiative", "linked initiatives"],
    },
    "objectives": {
        "description": "List of objective names linked to this feature",
        "type": "list[str]",
        "values": None,
        "requires": "enrich_objectives()",
        "aliases": ["objective", "okr", "linked objectives"],
    },
    "releases": {
        "description": "List of original release names assigned to this feature. "
                       "Names are raw strings from ProductBoard and use inconsistent "
                       "formats. For temporal queries prefer release_quarter or release_date.",
        "type": "list[str]",
        "values": None,
        "requires": "enrich_releases()",
        "aliases": ["release", "release assignment", "assigned releases"],
    },
    "release_quarter": {
        "description": "GENERATED — normalised quarter labels derived from release names "
                       "at extraction time (e.g. 'Q1 2026'). Deduplicated and sorted. "
                       "Empty list when the release name could not be parsed.",
        "type": "list[str]",
        "values": None,
        "requires": "enrich_releases()",
        "aliases": ["quarter", "release quarter", "ship quarter", "target quarter"],
    },
    "release_date": {
        "description": "GENERATED — normalised ISO dates (start of period) derived from "
                       "release names at extraction time (e.g. '2026-01-01'). "
                       "Deduplicated and sorted. Empty list when unparseable.",
        "type": "list[str]",
        "values": None,
        "requires": "enrich_releases()",
        "aliases": ["release date", "ship date", "release start date"],
    },

    # ==================================================================
    # CUSTOM FIELD COLUMNS — DROPDOWN (added by enrich_custom_fields())
    # ==================================================================
    # Note: all cf_* columns require enrich_custom_fields() first.
    # For multi-dropdown fields, values are "; " separated strings.
    # Two different custom fields may share the name "Priority" —
    # the last-processed value wins per feature. Use context to
    # distinguish the dropdown (High/Medium/Low) from the number variant.

    "cf_Roadmap Visibility": {
        "description": "Whether the feature appears on External, Internal, or Dev Only roadmap",
        "type": "str",
        "values": ["External", "Internal", "Dev Only"],
        "requires": "enrich_custom_fields()",
        "aliases": [
            "roadmap visibility", "external roadmap", "internal roadmap",
            "dev only", "visibility",
        ],
        "notes": "PRIMARY column for external / internal / dev-only classification. "
                 "Always prefer this over cf_Roadmap Candidacy when the user asks "
                 "about external, internal, or dev-only items.",
    },
    "cf_Roadmap Candidacy": {
        "description": "Roadmap candidacy classification",
        "type": "str",
        "values": ["Internal Roadmap", "External Roadmap", "Dev Only"],
        "requires": "enrich_custom_fields()",
        "aliases": ["roadmap candidacy", "roadmap candidate"],
    },
    "cf_Roadmap Concreteness": {
        "description": "How concrete/validated the roadmap item scope is",
        "type": "str",
        "values": ["Concrete", "Vague"],
        "requires": "enrich_custom_fields()",
        "aliases": [
            "concreteness", "roadmap concreteness", "definite", "directional",
            "scope confidence",
        ],
    },
    "cf_Roadmap Type": {
        "description": "Definite (fully refined) vs Directional (subject to change)",
        "type": "str",
        "values": ["Definite", "Directional"],
        "requires": "enrich_custom_fields()",
        "aliases": ["roadmap type", "commitment level"],
    },
    "cf_Roadmap Size and Complexity": {
        "description": "T-Shirt size for roadmap planning",
        "type": "str",
        "values": ["S", "M", "L"],
        "requires": "enrich_custom_fields()",
        "aliases": ["roadmap size", "complexity", "size"],
    },
    "cf_Roadmap themes": {
        "description": "Strategic theme the feature contributes to",
        "type": "str",
        "values": [
            "Drive adoption", "Platform", "Generative AI",
            "Simplicity & Ease of use", "Together as a Suite",
            "End-to-end value", "Cloud Qualities",
        ],
        "requires": "enrich_custom_fields()",
        "aliases": ["roadmap theme", "theme", "strategic theme"],
    },
    "cf_Now\\Next\\Later": {
        "description": "Planning horizon bucket",
        "type": "str",
        "values": ["01|Now", "02|Next", "03|Later"],
        "requires": "enrich_custom_fields()",
        "aliases": [
            "now next later", "planning horizon", "timeline bucket",
            "now", "next", "later",
        ],
    },
    "cf_Priority": {
        "description": "Priority level (dropdown variant). Note: a separate number-type "
                       "Priority field also exists; the value depends on which was set for "
                       "a given feature",
        "type": "str",
        "values": ["High", "Medium", "Low"],
        "requires": "enrich_custom_fields()",
        "aliases": ["priority", "feature priority", "importance"],
    },
    "cf_NEXT Urgency": {
        "description": "Urgency level for NEXT team planning",
        "type": "str",
        "values": ["low", "medium", "high"],
        "requires": "enrich_custom_fields()",
        "aliases": ["urgency", "next urgency"],
    },
    "cf_Initiative (HAIM)": {
        "description": "HAIM classification: Harvest, Acquire, Invest, Maintain",
        "type": "str",
        "values": ["H", "A", "I", "M"],
        "requires": "enrich_custom_fields()",
        "aliases": ["haim", "harvest acquire invest maintain"],
    },
    "cf_Release Confidence %": {
        "description": "Confidence level that the feature will be released as planned",
        "type": "str",
        "values": ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"],
        "requires": "enrich_custom_fields()",
        "aliases": ["release confidence", "confidence percentage", "delivery confidence"],
    },
    "cf_Base/Premium": {
        "description": "Commercialization package: base or premium tier",
        "type": "str",
        "values": ["Base", "Premium", "Unclear", "(not to use)"],
        "requires": "enrich_custom_fields()",
        "aliases": ["base premium", "tier", "package", "commercialization"],
    },
    "cf_Process AI Services": {
        "description": "Whether the feature involves Process AI Services",
        "type": "str",
        "values": ["Yes"],
        "requires": "enrich_custom_fields()",
        "aliases": ["process ai", "ai services"],
    },
    "cf_Effort (T-Shirt)": {
        "description": "Effort estimation using T-Shirt sizes (S=1wk, M=2wk, L=1mo, XL=1qtr, XXL=>1qtr)",
        "type": "str",
        "values": ["S", "M", "L", "XL", "XXL"],
        "requires": "enrich_custom_fields()",
        "aliases": ["effort t-shirt", "effort size", "effort estimation"],
    },
    "cf_Engineering Planning Outcome": {
        "description": "Engineering planning classification for the quarter",
        "type": "str",
        "values": ["Planned", "Stretch Goal", "Ad-hoc"],
        "requires": "enrich_custom_fields()",
        "aliases": [
            "planning outcome", "engineering planning",
            "planned", "stretch goal", "ad-hoc",
        ],
    },
    "cf_Planning Confidence": {
        "description": "Alignment level with interlocked/impacted teams",
        "type": "str",
        "values": ["Low", "Medium", "Confident", "Yes"],
        "requires": "enrich_custom_fields()",
        "aliases": ["planning confidence", "team alignment confidence"],
    },
    "cf_Engineering needed?": {
        "description": "Whether engineering work is required",
        "type": "str",
        "values": ["Yes", "No", "Unclear"],
        "requires": "enrich_custom_fields()",
        "aliases": ["engineering needed", "needs engineering", "requires dev"],
    },
    "cf_Refined": {
        "description": "Whether the item has been refined",
        "type": "str",
        "values": ["Yes", "No", "n/a"],
        "requires": "enrich_custom_fields()",
        "aliases": ["refined", "is refined", "refinement done"],
    },
    "cf_PI-A Growth Type": {
        "description": "Growth classification for PI-A portfolio analysis",
        "type": "str",
        "values": [
            "Expand SAP", "Expand non-SAP", "Extend",
            "Innovate", "Integrate", "Maintenance",
        ],
        "requires": "enrich_custom_fields()",
        "aliases": ["growth type", "pi-a growth", "portfolio growth type"],
    },
    "cf_Product marketing relevance": {
        "description": "Product marketing relevance classification",
        "type": "str",
        "values": ["Yes External", "Yes Internal", "No mention"],
        "requires": "enrich_custom_fields()",
        "aliases": ["marketing relevance", "product marketing"],
    },
    "cf_Product marketing status": {
        "description": "Status within product marketing pipeline",
        "type": "str",
        "values": ["Deep Dive Candidate", "Presented", "High Level Candidate", "Empty"],
        "requires": "enrich_custom_fields()",
        "aliases": ["marketing status"],
    },
    "cf_Product marketing confidence": {
        "description": "Likelihood the feature will be marketed",
        "type": "str",
        "values": ["Highly likely", "Unsure", "Unlikely"],
        "requires": "enrich_custom_fields()",
        "aliases": ["marketing confidence"],
    },
    "cf_Main Product / Component": {
        "description": "Primary product/component mapping (abbreviation)",
        "type": "str",
        "values": ["CHub", "Trafo", "VAL", "SPM", "JM", "PINT", "PINS", "PnG", "Suite", "SWA"],
        "requires": "enrich_custom_fields()",
        "aliases": ["main product", "main component", "product abbreviation"],
    },
    "cf_R4R Category": {
        "description": "Ready-for-Roadmap size category",
        "type": "str",
        "values": ["S", "M", "L"],
        "requires": "enrich_custom_fields()",
        "aliases": ["r4r category", "ready for roadmap size"],
    },
    "cf_Group Ranking": {
        "description": "Group-level priority ranking",
        "type": "str",
        "values": ["A1", "B1", "C1", "D"],
        "requires": "enrich_custom_fields()",
        "aliases": ["group ranking", "group priority"],
    },
    "cf_Value Accelerator Type": {
        "description": "Type of value accelerator",
        "type": "str",
        "values": ["Process Mining", "Process Modelling", "Process Governance"],
        "requires": "enrich_custom_fields()",
        "aliases": ["value accelerator", "accelerator type"],
    },
    "cf_Swimlane (Suite & Cross Topics)": {
        "description": "Swimlane for Suite & Cross topic board views",
        "type": "str",
        "values": ["UX", "Project Topics", "Suite Initiatives", "Non-functional/Technical Topics"],
        "requires": "enrich_custom_fields()",
        "aliases": ["swimlane", "board lane", "cross topic"],
    },
    "cf_Roadmap Type": {
        "description": "Definite (fully refined) vs Directional (subject to change)",
        "type": "str",
        "values": ["Definite", "Directional"],
        "requires": "enrich_custom_fields()",
        "aliases": ["roadmap type", "delivery type"],
    },
    "cf_External Roadmap highlight?": {
        "description": "Whether this is a highlight item on the external roadmap",
        "type": "str",
        "values": ["Yes", "No"],
        "requires": "enrich_custom_fields()",
        "aliases": ["external highlight", "roadmap highlight"],
    },
    "cf_Next Project Type": {
        "description": "Project classification for Signavio Next team",
        "type": "str",
        "values": ["Blue Sky", "Innovation Topic", "Strategic Project", "Internal"],
        "requires": "enrich_custom_fields()",
        "aliases": ["project type", "next project type"],
    },
    "cf_Release type": {
        "description": "Type of release/delivery vehicle",
        "type": "str",
        "values": [
            "DPP", "Microdelivery", "GA", "RTC",
            "Beta (open)", "Beta (closed)", "EAC",
            "Labs", "Labs internal (not for customers)", "AI Service (internal)",
        ],
        "requires": "enrich_custom_fields()",
        "aliases": ["release type", "delivery type", "launch type"],
    },
    "cf_SAP Roadmap Explorer": {
        "description": "Whether published on SAP Roadmap Explorer",
        "type": "str",
        "values": ["Not Published", "Published"],
        "requires": "enrich_custom_fields()",
        "aliases": ["roadmap explorer", "sap roadmap", "published on explorer"],
    },
    "cf_Dependency Level (PAM unification // Roadmap)": {
        "description": "Level of dependency for PAM unification / roadmap delivery",
        "type": "str",
        "values": [
            "Low", "Medium // Low", "High // Low",
            "High // High", "High // Medium", "Medium",
        ],
        "requires": "enrich_custom_fields()",
        "aliases": ["dependency level", "dependency", "pam dependency"],
    },
    "cf_Productboard Implementation": {
        "description": "ProductBoard implementation status",
        "type": "str",
        "values": ["Implemented"],
        "requires": "enrich_custom_fields()",
        "aliases": ["pb implementation", "implementation status"],
    },

    # ==================================================================
    # CUSTOM FIELD COLUMNS — MULTI-DROPDOWN (added by enrich_custom_fields())
    # Values appear as "; " separated strings in the DataFrame.
    # ==================================================================
    "cf_Suite Qualities": {
        "description": "Which suite quality areas the feature addresses (multi-select)",
        "type": "str (multi)",
        "values": [
            "Performance & Scalability", "Integration", "BTP Onboarding",
            "Content", "Security & Compliance", "User Experience",
            "Data Governance", "Analytics", "Composability", "Accessibility",
        ],
        "requires": "enrich_custom_fields()",
        "aliases": ["suite quality", "nfr quality", "quality area"],
    },
    "cf_PTM: JTBD": {
        "description": "Jobs-To-Be-Done classification (multi-select)",
        "type": "str (multi)",
        "values": ["Capture", "Analyze", "Act", "Model", "Collaborate", "Administrate"],
        "requires": "enrich_custom_fields()",
        "aliases": ["jtbd", "jobs to be done", "ptm jtbd"],
    },
    "cf_R4R Maturity Checklist": {
        "description": "Ready-for-Roadmap maturity gate artifacts (multi-select)",
        "type": "str (multi)",
        "values": [
            "Value Prop", "Scope", "Validation Statement",
            "High-level mock-ups", "Sign-off PTL", "Architecture Concept Doc",
            "Dependency Map", "Technical PoC",
            "Delivery Item Breakdown by team with estimate", "Staffing Plan",
        ],
        "requires": "enrich_custom_fields()",
        "aliases": ["r4r checklist", "maturity checklist", "readiness checklist"],
    },
    "cf_Line of Business (Value Accelerators)": {
        "description": "Line of business for value accelerator classification (multi-select)",
        "type": "str (multi)",
        "values": [
            "Cross LoB", "ERP & Business Transformation", "HR",
            "Supply Chain", "Sales", "Finance", "Procurement",
        ],
        "requires": "enrich_custom_fields()",
        "aliases": ["line of business", "lob", "value accelerator lob"],
    },
    "cf_Integrated User Flows - Capabilities (Signavio Next)": {
        "description": "Signavio Next integrated user flow capabilities (multi-select)",
        "type": "str (multi)",
        "values": [
            "Analyze", "Design and simulate", "Improve",
            "Roll out, use and manage assets", "Monitor", "Content",
            "BPM practice management", "Tool administration",
        ],
        "requires": "enrich_custom_fields()",
        "aliases": ["user flow capabilities", "next capabilities", "integrated flows"],
    },
    "cf_Suite Foundation Domains": {
        "description": "Suite foundation domain areas (multi-select)",
        "type": "str (multi)",
        "values": [
            "Suite Enterprise Capabilities", "Suite Essentials",
            "Suite Collaboration Services", "Suite Entry Experience, Hub",
            "Suite User Experience / Shell",
            "Suite Authentication & Identity Management",
            "Suite Tenant Management", "Suite API Experience",
            "Suite Access Management",
        ],
        "requires": "enrich_custom_fields()",
        "aliases": ["foundation domain", "suite domain", "suite foundation"],
    },
    "cf_Strategic Initiative (PA&M)": {
        "description": "Strategy cycle initiative for PA&M team (multi-select of initiative names)",
        "type": "str",
        "values": [
            "Model-Less Conformance", "Widget Builder 2.0",
            "Journey to Process", "Plug and Gain Connector",
            "Prompt Based Process Mining", "Access Rights",
            "Business Object Driven Case Modelling",
            "Relational Data Modelling", "Calculated Attributes",
            "Signal Engine Performance - 2 Billion Events",
            "Metric Time Series Trend Prediction",
            "SAP Datasphere Integration", "(Metrics) Benchmarking",
            "SIGNAL API", "Newtrics - SIGNAL Expression Repository",
            "Value Analysis and Insights Central", "Improved filtering",
            "Process Data Pipelines in VAL",
            "Connectivity to Azure Data Lake", "3rd party connectivity",
            "New redizigned UI", "Improve data transforamation validation",
            "Root cause analysis", "Process atoms and conformance",
            "Activity grouping",
        ],
        "requires": "enrich_custom_fields()",
        "aliases": ["strategic initiative", "pam initiative", "pa&m initiative"],
    },

    # ==================================================================
    # CUSTOM FIELD COLUMNS — NUMBER (added by enrich_custom_fields())
    # ==================================================================
    "cf_TMAI_Business Value": {
        "description": "TMAI scoring: business value (0 = no value, 5 = highest value)",
        "type": "number",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["tmai business value", "business value score"],
    },
    "cf_TMAI_Urgency": {
        "description": "TMAI scoring: urgency (0 = no urgency, 5 = critical within 3 days)",
        "type": "number",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["tmai urgency", "urgency score"],
    },
    "cf_TMAI_Realization Effort": {
        "description": "TMAI scoring: realization effort — INVERTED scale "
                       "(0 = very high effort, 5 = basically no effort)",
        "type": "number",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["tmai effort", "realization effort score"],
    },
    "cf_TMAI_Priority/Value to Customer": {
        "description": "TMAI scoring: customer priority/value (0 = not important, 5 = highly aligned)",
        "type": "number",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["tmai priority", "tmai customer value"],
    },
    "cf_Impact": {
        "description": "Impact score (typically 0.25-3 scale, used in Radar charts)",
        "type": "number",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["impact", "impact score"],
    },
    "cf_Confidence": {
        "description": "Confidence percentage",
        "type": "number",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["confidence score", "confidence %"],
    },
    "cf_Reach": {
        "description": "How many users/customers will be impacted",
        "type": "number",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["reach", "user reach", "customer reach"],
    },
    "cf_Effort": {
        "description": "Effort estimate (numeric)",
        "type": "number",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["effort", "effort points"],
    },
    "cf_Rest Effort": {
        "description": "Remaining effort still needed",
        "type": "number",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["rest effort", "remaining effort"],
    },
    "cf_team Effort": {
        "description": "Team-level effort estimate",
        "type": "number",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["team effort"],
    },
    "cf_Customer Requests Count": {
        "description": "Number of customer requests linked to this feature",
        "type": "number",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["customer requests", "request count", "customer demand"],
    },
    "cf_Stack ranking": {
        "description": "Numeric stack ranking position",
        "type": "number",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["stack rank", "ranking"],
    },
    "cf_Install Base %": {
        "description": "Percentage of install base affected",
        "type": "number",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["install base", "install base percentage"],
    },
    "cf_ARR": {
        "description": "Annual Recurring Revenue impact",
        "type": "number",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["arr", "annual recurring revenue", "revenue"],
    },

    # ==================================================================
    # CUSTOM FIELD COLUMNS — MEMBER (added by enrich_custom_fields())
    # Values are person names/emails. Not listed for data privacy.
    # ==================================================================
    "cf_Product Manager": {
        "description": "Assigned product manager (person name/email)",
        "type": "member",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["product manager", "pm"],
    },
    "cf_Designer": {
        "description": "Assigned designer (person name/email)",
        "type": "member",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["designer", "ux designer"],
    },
    "cf_Product Lead": {
        "description": "Product lead (person name/email)",
        "type": "member",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["product lead", "ptl"],
    },
    "cf_Product Designer": {
        "description": "Product designer (person name/email)",
        "type": "member",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["product designer"],
    },
    "cf_Next Owner": {
        "description": "Owner for Signavio Next team (person name/email)",
        "type": "member",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["next owner"],
    },
    "cf_Owner": {
        "description": "Custom field owner — distinct from base owner_email (person name/email)",
        "type": "member",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["cf owner"],
    },
    "cf_Product Owner/Program Manager": {
        "description": "PO/Program Manager responsible for delivery (person name/email)",
        "type": "member",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["product owner", "program manager", "po"],
    },
    "cf_Epic Owner": {
        "description": "Owner of the epic (person name/email)",
        "type": "member",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["epic owner"],
    },
    "cf_Dev Manager": {
        "description": "Development manager (person name/email)",
        "type": "member",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["dev manager", "development manager"],
    },
    "cf_Stream Lead": {
        "description": "Stream lead (person name/email)",
        "type": "member",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["stream lead"],
    },
    "cf_Data Engineer": {
        "description": "Assigned data engineer (person name/email)",
        "type": "member",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["data engineer"],
    },
    "cf_Content Lead": {
        "description": "Content lead (person name/email)",
        "type": "member",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["content lead"],
    },
    "cf_Team Member 1": {
        "description": "Team member slot 1 (person name/email)",
        "type": "member",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["team member 1"],
    },
    "cf_Team Member 2": {
        "description": "Team member slot 2 (person name/email)",
        "type": "member",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["team member 2"],
    },
    "cf_Partner-in-Crime": {
        "description": "Stand-in for epic owner during absence (person name/email)",
        "type": "member",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["partner in crime", "backup owner"],
    },

    # ==================================================================
    # CUSTOM FIELD COLUMNS — PEOPLE LIST DROPDOWN (enrich_custom_fields())
    # Values are team member names. Not listed for data privacy.
    # ==================================================================
    "cf_Contributor (PA&M)": {
        "description": "PA&M team contributors (multi-select of team member names)",
        "type": "str (multi, people)",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["contributor", "pam contributor"],
    },
    "cf_Next Teammembers": {
        "description": "Signavio Next team members assigned (multi-select of names)",
        "type": "str (multi, people)",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["next team members", "next team"],
    },
    "cf_Next Member": {
        "description": "Signavio Next team member (single-select of name)",
        "type": "str (people)",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["next member"],
    },

    # ==================================================================
    # CUSTOM FIELD COLUMNS — TEXT (added by enrich_custom_fields())
    # ==================================================================
    "cf_Industry": {
        "description": "Industry context for the feature",
        "type": "text",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["industry", "vertical"],
    },
    "cf_Account Type": {
        "description": "Account type context",
        "type": "text",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["account type"],
    },
    "cf_Customer Requests / Problems": {
        "description": "Free-text customer request / problem descriptions",
        "type": "text",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["customer requests text", "customer problems"],
    },
    "cf_Use Case": {
        "description": "Use case description",
        "type": "text",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["use case"],
    },
    "cf_Jira / Figma / Confluence links": {
        "description": "Links to Jira, Figma, Confluence for quick reference",
        "type": "text",
        "values": None,
        "requires": "enrich_custom_fields()",
        "aliases": ["jira link", "figma link", "confluence link", "project links"],
    },

    # ==================================================================
    # SECTION COLUMNS (added by enrich_sections())
    # Parsed from the feature description HTML.
    # ==================================================================
    **{
        sec: {
            "description": f"Description section: {sec.replace('sec_', '').replace('_', ' ').title()}",
            "type": "text",
            "values": None,
            "requires": "enrich_sections()",
            "aliases": [sec.replace("sec_", "").replace("_", " ")],
        }
        for sec in sorted(SECTION_CATEGORIES.keys())
    },
}

# ---------------------------------------------------------------------------
# Query translation hints (few-shot examples for AI agents)
# ---------------------------------------------------------------------------

QUERY_HINTS: list[dict[str, str]] = [
    {
        "query": "show me all external roadmap items",
        "code": 'fs.enrich_custom_fields()\nfs.filter(where=lambda df: df["cf_Roadmap Visibility"] == "External")',
        "notes": "cf_Roadmap Visibility is the PRIMARY column for external/internal/dev-only. "
                 "Always use this column (not cf_Roadmap Candidacy) when asked about visibility.",
    },
    {
        "query": "features on the internal roadmap",
        "code": 'fs.enrich_custom_fields()\nfs.filter(where=lambda df: df["cf_Roadmap Candidacy"] == "Internal Roadmap")',
        "notes": "Use Roadmap Candidacy for Internal Roadmap / External Roadmap / Dev Only",
    },
    {
        "query": "high priority features",
        "code": 'fs.enrich_custom_fields()\nfs.filter(where=lambda df: df["cf_Priority"] == "High")',
        "notes": "Priority dropdown has High/Medium/Low; a separate number Priority field also exists",
    },
    {
        "query": "items planned for now",
        "code": 'fs.enrich_custom_fields()\nfs.filter(where=lambda df: df["cf_Now\\\\Next\\\\Later"] == "01|Now")',
        "notes": "Now\\Next\\Later values are prefixed with sort numbers: 01|Now, 02|Next, 03|Later",
    },
    {
        "query": "features at risk",
        "code": 'fs.filter(health="needs-attention")',
        "notes": "health_status is a base column — no enrichment needed",
    },
    {
        "query": "premium features",
        "code": 'fs.enrich_custom_fields()\nfs.filter(where=lambda df: df["cf_Base/Premium"] == "Premium")',
        "notes": "",
    },
    {
        "query": "definite roadmap commitments",
        "code": 'fs.enrich_custom_fields()\nfs.filter(where=lambda df: df["cf_Roadmap Concreteness"] == "Concrete")',
        "notes": "Concrete = fully refined scope, highest confidence; Vague = subject to change",
    },
    {
        "query": "features in discovery",
        "code": 'fs.filter(status="Discovery")',
        "notes": "filter() auto-matches substrings, so 'Discovery' matches the emoji-prefixed status name",
    },
    {
        "query": "large items on the roadmap",
        "code": 'fs.enrich_custom_fields()\nfs.filter(where=lambda df: df["cf_Roadmap Size and Complexity"] == "L")',
        "notes": "Also consider cf_Effort (T-Shirt) for L/XL/XXL effort sizing",
    },
    {
        "query": "features by product Process Manager",
        "code": 'fs.filter(product="Process Manager")',
        "notes": "product= uses the hierarchy tree (includes all components/sub-features below)",
    },
    {
        "query": "features with Generative AI theme",
        "code": 'fs.enrich_custom_fields()\nfs.filter(where=lambda df: df["cf_Roadmap themes"] == "Generative AI")',
        "notes": "",
    },
    {
        "query": "stretch goals this quarter",
        "code": 'fs.enrich_custom_fields()\nfs.filter(where=lambda df: df["cf_Engineering Planning Outcome"] == "Stretch Goal")',
        "notes": "",
    },
    {
        "query": "features starting in Q2 2026",
        "code": 'fs.filter(timeframe_after="2026-04-01", timeframe_before="2026-06-30")',
        "notes": "timeframe_after/before are base column filters — no enrichment needed",
    },
    {
        "query": "features linked to a specific initiative",
        "code": 'fs.enrich_initiatives()\nfs.filter(where=lambda df: df["initiatives"].apply(lambda i: "Initiative Name" in i))',
        "notes": "Replace 'Initiative Name' with the actual name; initiatives is a list column",
    },
    {
        "query": "features with a problem statement",
        "code": 'fs.enrich_sections()\nfs.filter(where=lambda df: df["sec_problem_statement"] != "")',
        "notes": "Section columns are parsed from description HTML",
    },
    {
        "query": "dropped features",
        "code": 'fs.filter(status="Dropped")',
        "notes": "",
    },
    {
        "query": "suite quality performance features",
        "code": 'fs.enrich_custom_fields()\nfs.filter(where=lambda df: df["cf_Suite Qualities"].str.contains("Performance & Scalability", na=False))',
        "notes": "Multi-dropdown: values are '; ' separated, use str.contains() for matching",
    },
    {
        "query": "Process Manager features in progress",
        "code": 'fs.filter(product="Process Manager", status="In progress")',
        "notes": "Combine product and status filters in one call",
    },
    {
        "query": "features with high release confidence",
        "code": 'fs.enrich_custom_fields()\nfs.filter(where=lambda df: df["cf_Release Confidence %"] == "100%")',
        "notes": "Values are strings: '10%', '20%', ..., '100%'",
    },
    {
        "query": "features published on SAP Roadmap Explorer",
        "code": 'fs.enrich_custom_fields()\nfs.filter(where=lambda df: df["cf_SAP Roadmap Explorer"] == "Published")',
        "notes": "",
    },
    # --- Release timing (normalised, generated at extraction) ---
    {
        "query": "features releasing in Q1 2026",
        "code": 'fs.enrich_releases()\nfs.filter(where=lambda df: df["release_quarter"].apply(lambda qs: "Q1 2026" in qs))',
        "notes": "release_quarter is a GENERATED list[str] of normalised quarter labels. "
                 "Use 'in' to check membership.",
    },
    {
        "query": "when does feature X ship?",
        "code": 'fs.enrich_releases()\nresult = fs.filter(search="feature X").select("name", "releases", "release_quarter", "release_date")',
        "notes": "release_quarter and release_date are the normalised, consistent fields. "
                 "releases keeps the original (inconsistent) names for reference.",
    },
    {
        "query": "features shipping in 2026",
        "code": 'fs.enrich_releases()\nfs.filter(where=lambda df: df["release_date"].apply(lambda ds: any(d.startswith("2026") for d in ds)))',
        "notes": "release_date contains YYYY-MM-DD strings; str.startswith works for year filtering.",
    },
    # --- Visibility (external / internal / dev-only) ---
    {
        "query": "external roadmap items",
        "code": 'fs.enrich_custom_fields()\nfs.filter(where=lambda df: df["cf_Roadmap Visibility"] == "External")',
        "notes": "cf_Roadmap Visibility is the PRIMARY column for external/internal/dev-only. "
                 "Do NOT use cf_Roadmap Candidacy for this.",
    },
    {
        "query": "dev-only features",
        "code": 'fs.enrich_custom_fields()\nfs.filter(where=lambda df: df["cf_Roadmap Visibility"] == "Dev Only")',
        "notes": "cf_Roadmap Visibility is the PRIMARY column for external/internal/dev-only.",
    },
]


# ---------------------------------------------------------------------------
# Describe helpers (used by FeatureStore.describe and CLI --describe)
# ---------------------------------------------------------------------------

def describe_column(column: str) -> str:
    """Return a formatted description of a single column."""
    meta = COLUMN_METADATA.get(column)
    if not meta:
        # Try fuzzy match
        matches = [
            k for k in COLUMN_METADATA
            if column.lower() in k.lower()
            or any(column.lower() in a for a in COLUMN_METADATA[k].get("aliases", []))
        ]
        # dedupe while preserving order
        seen: set[str] = set()
        matches = [m for m in matches if m not in seen and not seen.add(m)]  # type: ignore[func-returns-value]
        if not matches:
            return f"Column not found: {column}\nUse --describe to list all columns."
        if len(matches) == 1:
            column = matches[0]
            meta = COLUMN_METADATA[column]
        else:
            return (
                f"Multiple matches for '{column}':\n"
                + "\n".join(f"  {m}" for m in matches)
                + "\nSpecify the full column name."
            )

    lines = [f"Column: {column}", f"  Type:        {meta['type']}"]
    lines.append(f"  Description: {meta['description']}")
    if meta.get("requires"):
        lines.append(f"  Requires:    {meta['requires']}")
    if meta.get("values"):
        lines.append(f"  Values:      {meta['values']}")
    if meta.get("aliases"):
        lines.append(f"  Aliases:     {', '.join(meta['aliases'])}")
    if meta.get("notes"):
        lines.append(f"  Notes:       {meta['notes']}")
    return "\n".join(lines)


def describe_all_columns() -> str:
    """Return a formatted grouped summary of all columns."""
    groups: dict[str, list[str]] = {
        "Base columns": [],
        "Enrichment columns": [],
        "Custom fields (dropdown)": [],
        "Custom fields (multi-dropdown)": [],
        "Custom fields (number)": [],
        "Custom fields (member)": [],
        "Custom fields (people list)": [],
        "Custom fields (text)": [],
        "Section columns": [],
    }

    for col, meta in COLUMN_METADATA.items():
        ctype = meta.get("type", "")
        vals = meta.get("values")
        val_str = ", ".join(str(v) for v in vals[:6]) if vals else ""
        if vals and len(vals) > 6:
            val_str += f" ... ({len(vals)} total)"

        line = f"  {col:<55} {ctype:<16}"
        if val_str:
            line += f" [{val_str}]"

        if col.startswith("sec_"):
            groups["Section columns"].append(line)
        elif col.startswith("cf_"):
            if "multi" in ctype and "people" in ctype:
                groups["Custom fields (people list)"].append(line)
            elif "people" in ctype:
                groups["Custom fields (people list)"].append(line)
            elif ctype == "member":
                groups["Custom fields (member)"].append(line)
            elif "multi" in ctype:
                groups["Custom fields (multi-dropdown)"].append(line)
            elif ctype == "number":
                groups["Custom fields (number)"].append(line)
            elif ctype == "text":
                groups["Custom fields (text)"].append(line)
            else:
                groups["Custom fields (dropdown)"].append(line)
        elif meta.get("requires"):
            groups["Enrichment columns"].append(line)
        else:
            groups["Base columns"].append(line)

    out = ["ProductBoard Features — Column Data Dictionary", "=" * 50, ""]
    for group_name, entries in groups.items():
        if not entries:
            continue
        out.append(f"\n{group_name} ({len(entries)})")
        out.append("-" * 50)
        out.extend(entries)
    out.append(f"\nTotal: {len(COLUMN_METADATA)} columns")
    out.append(f"Query hints: {len(QUERY_HINTS)} examples (use --describe hints)")
    return "\n".join(out)


def describe_hints() -> str:
    """Return formatted query translation hints."""
    lines = [
        "Query Translation Hints",
        "=" * 50,
        "\nExamples of how to translate natural-language queries into code:\n",
    ]
    for h in QUERY_HINTS:
        lines.append(f'  "{h["query"]}"')
        lines.append(f'    → {h["code"]}')
        if h.get("notes"):
            lines.append(f'    Note: {h["notes"]}')
        lines.append("")
    return "\n".join(lines)
