"""
========================================
SAP SIGNAVIO PRODUCT CLASSIFIER
========================================
Maps customer insights to SAP Signavio products based on tags.

SAP Signavio Product Suite:
1. Process Manager - Process modeling, documentation, collaboration
2. Process Governance - Workflow automation, approvals, case management
3. Collaboration Hub - Central access point for process knowledge
4. SAP Signavio Process Intelligence (SPI) - Process mining, analytics
5. Journey Modeler - Customer journey mapping
6. Value Accelerator - Best practices, reference content
7. Process Insights - Analytics, dashboards, reporting
8. Process Mining - Process discovery, conformance checking
"""

import pandas as pd
import re
from typing import List, Dict, Tuple

# ============================================================================
# PRODUCT DEFINITIONS WITH TAG MAPPINGS
# ============================================================================

PRODUCT_DEFINITIONS = {
    "Process Manager": {
        "description": "Process modeling, documentation, and collaborative design tool",
        "capabilities": [
            "BPMN 2.0 process modeling",
            "Process documentation",
            "Diagram editor",
            "Revision management",
            "Dictionary management",
            "Process simulation",
            "Modeling conventions",
            "Import/export",
            "Repository management"
        ],
        "primary_tags": [
            "🏠 Process Manager",
            "sap signavio process manager",
            "Process Modelling",
            "process editor",
            "Editor",
            "bpmn",
            "BPMN",
            "Diagrams",
            "DMN",
            "🏠 Repository & Dictionary",
            "🏠 Documentations",
            "🏠 Solution Manager"
        ],
        "secondary_tags": [
            "Dictionary Entries",
            "Dictionary categories",
            "dictionary attributes",
            "revision",
            "Simulation",
            "bpmn simulation",
            "Convention Checks",
            "modeling convention",
            "modeling rules",
            "Subprocesses",
            "linked diagrams",
            "diagram hierarchy",
            "custom graphics",
            "overlays",
            "Custom Attribute",
            "⛳️  Attributes",
            "import",
            "export",
            "import export dictionary",
            "ArchiMate",
            "Value Chain Diagram",
            "QuickModel",
            "fact sheet",
            "Printing",
            "export PDF",
            "SVG",
            "navigation map",
            "Navigation Maps",
            "🏠 Lean IX"
        ],
        "exclude_tags": []
    },
    
    "Process Governance": {
        "description": "Workflow automation, approvals, and governance management",
        "capabilities": [
            "Workflow management",
            "Approval workflows",
            "Case management",
            "Task management",
            "Publication workflows",
            "User roles and rights",
            "Audit trail",
            "Governance controls"
        ],
        "primary_tags": [
            "🏠 Process Governance",
            "⛳️ Approval-Workflow",
            "🏠 Roles & Access",
            "🏠 Transformation Manager",
            "Process Transformation Manager Beta Program"
        ],
        "secondary_tags": [
            "⛳️ Access Rights",
            "Governance Report",
            "Preview/Publish",
            "re-approval",
            "Risk & Compliance",
            "risk & control",
            "GRC",
            "Risk Management",
            "permissions",
            "⛳️ Administrator"
        ],
        "exclude_tags": []
    },
    
    "Collaboration Hub": {
        "description": "Central access point for process knowledge and stakeholder collaboration",
        "capabilities": [
            "Process portal",
            "Search and discovery",
            "Commenting and feedback",
            "Widgets and dashboards",
            "Process navigation",
            "User engagement",
            "Multi-language support"
        ],
        "primary_tags": [
            "🏠 Collaboration Hub",
            "Hub",
            "Hub Search",
            "hub settings"
        ],
        "secondary_tags": [
            "Widgets",
            "Widgets and Visualizations Enhancements",
            "commenting",
            "Explorer",
            "Search",
            "Smart Search",
            "multilanguage",
            "language",
            "Feeds",
            "preview mode",
            "views",
            "embeding",
            "filter",
            "Filters"
        ],
        "exclude_tags": []
    },
    
    "SAP Signavio Process Intelligence": {
        "description": "Process mining and analytics for data-driven process improvement",
        "capabilities": [
            "Process mining",
            "Analytics dashboards",
            "Conformance checking",
            "Process discovery",
            "Data connectors",
            "ETL pipelines",
            "Actions and signals",
            "Investigation"
        ],
        "primary_tags": [
            "🏠 SAP Signavio Process Intelligence",
            "🏠 SPI Analytics",
            "🏠 SPI PDM",
            "🏠 SPI Engine",
            "🏠 SPI Actions",
            "🏠 SPI API",
            "🏠  SPI Accelerators",
            "PI",
            "IPA"
        ],
        "secondary_tags": [
            "ETL",
            "ETL Templates",
            "Connector",
            "Process Discovery",
            "Investigation",
            "Signal Query",
            "Signavio Data Platform",
            "extraction",
            "⛳️ Data Management",
            "IPA",
            "BPMC"
        ],
        "exclude_tags": []
    },
    
    "Journey Modeler": {
        "description": "Customer and employee journey mapping tool",
        "capabilities": [
            "Journey mapping",
            "Persona modeling",
            "Touchpoint analysis",
            "Customer experience design",
            "Journey analytics"
        ],
        "primary_tags": [
            "🏠 Journey Modeler",
            "⛳️ Journey Mapping",
            "⛳️ SAP Signavio JM Beta",
            "CJM"
        ],
        "secondary_tags": [],
        "exclude_tags": []
    },
    
    "Value Accelerator": {
        "description": "Best practices, templates, and reference content for rapid implementation",
        "capabilities": [
            "Reference architecture",
            "Best practice content",
            "Industry templates",
            "S/4HANA integration",
            "Content packages"
        ],
        "primary_tags": [
            "🏠 Value Accelerator",
            "🏠 VAL",
            "PINS Accelerators"
        ],
        "secondary_tags": [
            "📎 VA Reference Architecture",
            "📎 VA SPX (incl. UX)",
            "📎 VA Content Consumption",
            "📎 VA Customer Experience CX",
            "📎 VA S/4HANA",
            "PDP",
            "PDP Templates"
        ],
        "exclude_tags": []
    },
    
    "Process Insights": {
        "description": "Process analytics, reporting, and visualization dashboards",
        "capabilities": [
            "Analytics dashboards",
            "Process metrics",
            "Reporting",
            "Data visualization",
            "KPI tracking"
        ],
        "primary_tags": [
            "🏠 Process Insights",
            "🏠 SAP Signavio Process Insights",
            "⛳️ Analytics Report"
        ],
        "secondary_tags": [
            "Reporting",
            "Metrics Report",
            "dashboard",
            "metrics",
            "💵 Value Management",
            "Users' Activity Report",
            "License report"
        ],
        "exclude_tags": ["🏠 SPI Analytics"]  # SPI Analytics goes to Process Intelligence
    },
    
    "Process Mining": {
        "description": "Process discovery, conformance checking from event data",
        "capabilities": [
            "Event log analysis",
            "Process discovery",
            "Conformance checking",
            "Variant analysis",
            "Root cause analysis"
        ],
        "primary_tags": [
            "🏠 Variant Management",
            "Process Discovery"
        ],
        "secondary_tags": [],
        "exclude_tags": []
    },
    
    "Suite Foundation": {
        "description": "Platform-level features: APIs, integration, user management, licensing",
        "capabilities": [
            "API access",
            "System integration",
            "User management",
            "License management",
            "Authentication (SSO/SAML)",
            "Platform administration"
        ],
        "primary_tags": [
            "🏠 API",
            "SUITE FOUNDATION",
            "User Management",
            "License Management",
            "Auth & Identity"
        ],
        "secondary_tags": [
            "integration",
            "SSO",
            "saml",
            "License report",
            "⛳️ Administrator",
            "🏠 Tenant",
            "Groups",
            "invitation",
            "Email",
            "🏠 UI/UX",
            "🏠  UX issue",
            "⚙️ Plug & Gain"
        ],
        "exclude_tags": []
    }
}

# Service ticket detection patterns
SERVICE_TICKET_PATTERNS = [
    r'\b(unlock|locked out|password reset|reset password|can\'?t log\s?in|cannot log\s?in)\b',
    r'\b(account (locked|disabled|suspended|blocked))\b',
    r'\b(access (denied|issue|problem)|permission (denied|issue))\b',
    r'\b(forgot password|password expired|change password request)\b',
    r'\b(login (issue|problem|error|failed)|authentication (error|failed))\b',
    r'\b(unable to access|no access to|lost access)\b',
    r'\b(SSO (issue|error|problem|not working))\b',
    r'\b(tenant (issue|error|access))\b',
    r'\b(invitation (not working|expired|issue))\b',
    r'\b(please (help|assist|support|unlock|reset))\b'
]


def is_service_ticket(text: str) -> bool:
    """Detect if an insight is a service/support ticket."""
    if pd.isna(text) or not text:
        return False
    
    text = str(text).lower()
    
    # Check service ticket patterns
    for pattern in SERVICE_TICKET_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    
    # Check for very short texts that are likely support requests
    word_count = len(text.split())
    if word_count < 10:
        support_keywords = ['unlock', 'password', 'access', 'help', 'cannot', 'error', 'issue']
        if any(kw in text for kw in support_keywords):
            return True
    
    return False


def classify_insight_to_product(tags: str, text: str = None) -> Tuple[str, float]:
    """
    Classify an insight to a SAP Signavio product based on tags.
    
    Returns:
        Tuple of (product_name, confidence_score)
    """
    if pd.isna(tags) or not tags:
        return ("Unclassified", 0.0)
    
    tags_lower = tags.lower()
    tags_list = [t.strip() for t in str(tags).split(',')]
    
    scores = {}
    
    for product, config in PRODUCT_DEFINITIONS.items():
        score = 0.0
        
        # Check primary tags (high weight)
        for tag in config["primary_tags"]:
            if tag.lower() in tags_lower or tag in tags_list:
                score += 1.0
        
        # Check secondary tags (medium weight)
        for tag in config["secondary_tags"]:
            if tag.lower() in tags_lower or tag in tags_list:
                score += 0.5
        
        # Check exclude tags (penalty)
        for tag in config.get("exclude_tags", []):
            if tag.lower() in tags_lower:
                score -= 0.3
        
        if score > 0:
            scores[product] = score
    
    if not scores:
        return ("Unclassified", 0.0)
    
    # Return product with highest score
    best_product = max(scores, key=scores.get)
    max_score = scores[best_product]
    
    # Normalize confidence (0-1)
    confidence = min(1.0, max_score / 2.0)
    
    return (best_product, confidence)


def classify_all_insights_to_products(df: pd.DataFrame) -> pd.DataFrame:
    """
    Classify all insights in a DataFrame to SAP Signavio products.
    
    Required columns: tags, note_text (or cleaned_text)
    """
    print("\n🏷️ Classifying insights to SAP Signavio products...")
    
    df = df.copy()
    
    # Detect text column
    text_col = 'cleaned_text' if 'cleaned_text' in df.columns else 'note_text'
    tags_col = 'tags'
    
    products = []
    confidences = []
    is_service_tickets = []
    
    for idx, row in df.iterrows():
        tags = row.get(tags_col, '')
        text = row.get(text_col, '')
        
        # First check if it's a service ticket
        if is_service_ticket(text):
            is_service_tickets.append(True)
        else:
            is_service_tickets.append(False)
        
        # Classify to product
        product, confidence = classify_insight_to_product(tags, text)
        products.append(product)
        confidences.append(confidence)
    
    df['product'] = products
    df['product_confidence'] = confidences
    df['is_service_ticket'] = is_service_tickets
    
    # Print distribution
    print("\n📊 Product Distribution:")
    product_counts = df['product'].value_counts()
    total = len(df)
    for product, count in product_counts.items():
        pct = (count / total) * 100
        service_count = df[(df['product'] == product) & (df['is_service_ticket'] == True)].shape[0]
        print(f"   {product}: {count} ({pct:.1f}%), Service Tickets: {service_count}")
    
    return df


def get_product_insights(df: pd.DataFrame, product: str) -> pd.DataFrame:
    """Get all insights for a specific product."""
    return df[df['product'] == product].copy()


def get_product_service_tickets(df: pd.DataFrame, product: str) -> pd.DataFrame:
    """Get service ticket insights for a specific product."""
    return df[(df['product'] == product) & (df['is_service_ticket'] == True)].copy()


def get_product_list() -> List[str]:
    """Get list of all products."""
    return list(PRODUCT_DEFINITIONS.keys())


def get_product_description(product: str) -> str:
    """Get product description."""
    if product in PRODUCT_DEFINITIONS:
        return PRODUCT_DEFINITIONS[product]["description"]
    return ""


def get_product_capabilities(product: str) -> List[str]:
    """Get product capabilities."""
    if product in PRODUCT_DEFINITIONS:
        return PRODUCT_DEFINITIONS[product]["capabilities"]
    return []


if __name__ == "__main__":
    # Test the classifier
    print("Testing product classifier...")
    
    test_cases = [
        ("🏠 Process Manager, Editor, bpmn", "Create better BPMN modeling"),
        ("🏠 Process Governance, ⛳️ Approval-Workflow", "Need faster approval workflows"),
        ("🏠 SAP Signavio Process Intelligence, ETL", "ETL pipeline issues"),
        ("🏠 Collaboration Hub, Widgets", "Add new widget types"),
        ("🏠 Journey Modeler", "Customer journey mapping"),
        ("🏠 Value Accelerator, 📎 VA S/4HANA", "S/4HANA best practices"),
        ("🏠 Process Insights, Reporting", "Better dashboard reports"),
        ("unlock account, User Management", "Can't login please unlock my account")
    ]
    
    for tags, text in test_cases:
        product, conf = classify_insight_to_product(tags, text)
        is_ticket = is_service_ticket(text)
        print(f"Tags: {tags[:40]}... -> {product} (conf: {conf:.2f}, ticket: {is_ticket})")
