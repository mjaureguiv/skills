"""
========================================
CONFIGURATION FILE
========================================
This file contains all the settings and definitions for the Customer Insight 
Intelligence Dashboard. You can modify these settings without changing the code.

Key Concepts for Beginners:
- A "dictionary" (dict) is like a labeled container: {"key": "value"}
- A "list" is an ordered collection: ["item1", "item2", "item3"]
- We use CAPITAL_LETTERS for constants (values that don't change)
"""

# ============================================================================
# CLUSTER DEFINITIONS
# ============================================================================
# These are the predefined strategic categories for classifying customer insights.
# Structure: Main Cluster → List of Sub-clusters
#
# How it works:
# - Each key (like "APIs") is a main cluster (becomes a "Feature")
# - Each value is a list of sub-clusters (become "Sub-features")
# - Insights get mapped to one main cluster and one sub-cluster

CLUSTER_DEFINITIONS = {
    "APIs": [
        "Trigger",              # API triggers and webhooks
        "REST API",             # RESTful API capabilities
        "Integration",          # Third-party integrations
    ],
    
    "Risk & Compliance": [
        "Governance",           # General governance needs
        "Audit",                # Audit and compliance tracking
        "Regulatory",           # Specific regulatory requirements (GDPR, SOX, etc.)
    ],
    
    "Asset Lifecycles & Approvals": [
        "Versioning",           # Asset version management
        "Approval Workflows",   # Approval process features
        "Lifecycle Management", # Full lifecycle management
    ],
    
    "Enterprise Readiness": [
        "Foundation Readiness", # Core enterprise features
        "Migration to Cloud",   # Cloud migration requirements
        "Security",             # Security and access control
        "Database",             # Database and storage needs
    ],
    
    "Case & Task Management": [
        "Task Management",      # Task management features
        "Case Tracking",        # Case management features
        "Notifications",        # Alerts and notifications
    ],
    
    "Other Collaboration Features": [
        "Sharing",              # Sharing and permissions
        "Comments",             # Comments and discussions
        "Team Collaboration",   # Team-based features
    ],
    
    "WF Management Foundation": [
        "Workflow Builder",     # Workflow creation tools
        "Scripts & Actions",    # Scripting and automation
        "Workflow Editor",      # Workflow editing capabilities
        "Workflow Canvas",      # Visual workflow design
        "Forms Editor",         # Form design and management
    ],
    
    "Workspace Settings": [
        "User & Access Management",  # User management and permissions
        "License Management",        # License tracking and management
        "Configuration",             # Workspace configuration
    ],
    
    "SPG AI": [
        "Joule",                # SAP's AI assistant features
        "AI Recommendations",   # AI-powered suggestions
        "Intelligent Automation", # ML-based automation
    ],
    
    "Service Ticket": [
        "Account Issues",       # Login, password, account locked
        "Access Problems",      # Permission denied, cannot access
        "Technical Support",    # Bugs, errors, not working
    ],
}

# ============================================================================
# KEYWORDS FOR CLASSIFICATION
# ============================================================================
# These keywords help the classifier determine which cluster an insight belongs to.
# The AI uses these as hints, but also understands context beyond exact matches.

CLASSIFICATION_KEYWORDS = {
    "APIs": [
        "api", "webhook", "trigger", "integration", "rest", "endpoint",
        "callback", "http", "request", "response", "json", "xml",
        "automation", "external system", "third party", "connector",
        "oauth", "authentication", "token", "swagger", "openapi"
    ],
    
    "Risk & Compliance": [
        "risk", "compliance", "regulation", "audit", "gdpr", "sox",
        "control", "governance", "policy", "regulatory", "legal",
        "assessment", "framework", "standard", "certification",
        "internal control", "risk management", "compliance report"
    ],
    
    "Asset Lifecycles & Approvals": [
        "asset", "lifecycle", "approval", "version", "draft", "publish",
        "review", "sign-off", "release", "archive", "deprecate",
        "ownership", "handover", "transition", "approve", "reject",
        "versioning", "release management", "approval chain"
    ],
    
    "Enterprise Readiness": [
        "enterprise", "scale", "performance", "migration", "cloud",
        "security", "sso", "ldap", "database", "backup", "disaster recovery",
        "high availability", "load balancing", "infrastructure",
        "scalability", "saas", "on-premise", "hybrid"
    ],
    
    "Case & Task Management": [
        "task", "case", "ticket", "assignment", "due date", "priority",
        "status", "workflow task", "action item", "todo", "checklist",
        "deadline", "assignee", "responsible", "notification", "alert",
        "reminder", "escalation"
    ],
    
    "Other Collaboration Features": [
        "collaboration", "sharing", "comment", "notification", "team",
        "communication", "discussion", "feedback", "mention",
        "real-time", "co-edit", "share", "invite", "permission"
    ],
    
    "WF Management Foundation": [
        "workflow", "builder", "editor", "canvas", "form", "script",
        "action", "automation", "rule", "condition", "branch",
        "parallel", "gateway", "subprocess", "bpmn", "process",
        "form field", "input", "validation"
    ],
    
    "Workspace Settings": [
        "user", "access", "permission", "role", "license", "authentication",
        "authorization", "group", "admin", "privilege", "seat",
        "user management", "access control", "license management",
        "workspace", "settings", "configuration", "preference"
    ],
    
    "SPG AI": [
        "ai", "artificial intelligence", "machine learning", "ml",
        "joule", "intelligent", "smart", "prediction", "recommendation",
        "nlp", "natural language", "automation", "copilot", "generative",
        "chatbot", "assistant", "suggest", "auto-complete"
    ],
    
    "Service Ticket": [
        "password", "login", "locked", "account locked", "cannot login",
        "forgot password", "reset password", "access denied", "permission denied",
        "not working", "broken", "error", "bug", "issue", "problem",
        "help", "support", "urgent", "fix", "crash", "down", "outage",
        "cannot access", "unable to", "fails", "failure", "stuck",
        "slow", "timeout", "frozen", "unresponsive"
    ],
}

# ============================================================================
# SUB-CLUSTER KEYWORDS
# ============================================================================
# More specific keywords for determining sub-cluster classification

SUBCLUSTER_KEYWORDS = {
    # APIs sub-clusters
    "Trigger": ["trigger", "webhook", "event", "callback", "fire", "invoke", "listen"],
    "REST API": ["rest", "endpoint", "http", "get", "post", "put", "delete", "api call"],
    "Integration": ["integration", "connector", "third party", "external", "sync", "connect"],
    
    # Risk & Compliance sub-clusters
    "Governance": ["governance", "policy", "control", "oversight", "management"],
    "Audit": ["audit", "trail", "log", "track", "history", "record"],
    "Regulatory": ["gdpr", "sox", "hipaa", "pci", "iso", "nist", "regulation", "compliance"],
    
    # Asset Lifecycles sub-clusters
    "Versioning": ["version", "revision", "history", "compare", "diff", "rollback"],
    "Approval Workflows": ["approval", "sign-off", "authorize", "review", "approve", "reject"],
    "Lifecycle Management": ["lifecycle", "stage", "phase", "transition", "state", "publish", "archive"],
    
    # Enterprise Readiness sub-clusters
    "Foundation Readiness": ["foundation", "core", "basic", "essential", "fundamental", "enterprise"],
    "Migration to Cloud": ["cloud", "migration", "saas", "migrate", "move to cloud", "azure", "aws"],
    "Security": ["security", "secure", "encrypt", "protect", "vulnerability", "sso", "ldap"],
    "Database": ["database", "db", "storage", "data", "backup", "sql", "performance"],
    
    # Case & Task Management sub-clusters
    "Task Management": ["task", "todo", "action item", "assignment", "assignee", "responsible"],
    "Case Tracking": ["case", "ticket", "issue", "incident", "request", "support"],
    "Notifications": ["notification", "alert", "reminder", "email", "notify", "escalation"],
    
    # Other Collaboration Features sub-clusters
    "Sharing": ["share", "sharing", "permission", "access", "invite", "collaborate"],
    "Comments": ["comment", "discussion", "feedback", "mention", "reply", "thread"],
    "Team Collaboration": ["team", "collaboration", "co-edit", "real-time", "together"],
    
    # WF Management Foundation sub-clusters
    "Workflow Builder": ["builder", "create workflow", "design workflow", "new workflow"],
    "Scripts & Actions": ["script", "action", "code", "custom logic", "automation", "execute"],
    "Workflow Editor": ["editor", "edit workflow", "modify workflow", "change workflow"],
    "Workflow Canvas": ["canvas", "visual", "drag", "drop", "diagram", "bpmn"],
    "Forms Editor": ["form", "input", "field", "form design", "form builder", "validation"],
    
    # Workspace Settings sub-clusters
    "User & Access Management": ["user", "access", "permission", "role", "group", "admin"],
    "License Management": ["license", "seat", "subscription", "billing", "usage", "quota"],
    "Configuration": ["configuration", "settings", "preference", "customize", "setup"],
    
    # SPG AI sub-clusters
    "Joule": ["joule", "sap ai", "assistant", "copilot"],
    "AI Recommendations": ["recommend", "suggestion", "predict", "intelligent", "smart"],
    "Intelligent Automation": ["automation", "auto", "ml", "machine learning", "ai-powered"],
    
    # Service Ticket sub-clusters
    "Account Issues": ["password", "login", "locked", "account", "forgot", "reset", "credential"],
    "Access Problems": ["access", "permission", "denied", "cannot access", "unable to access"],
    "Technical Support": ["error", "bug", "broken", "not working", "crash", "fix", "issue", "problem"],
}

# ============================================================================
# RICE SCORING CONFIGURATION
# ============================================================================
# RICE = Reach × Impact × Confidence / Effort
# These settings control how we calculate each component.

# Impact scoring based on language in the insight
# Higher scores = more urgent/important language
IMPACT_KEYWORDS = {
    "critical": 3.0,
    "blocker": 3.0,
    "must have": 3.0,
    "urgent": 2.5,
    "important": 2.0,
    "need": 1.5,
    "require": 1.5,
    "want": 1.0,
    "nice to have": 0.5,
    "would like": 0.5,
}

# Default impact score if no keywords found (scale 0.5 - 3.0)
DEFAULT_IMPACT_SCORE = 1.0

# Effort estimates by cluster (scale 1-10, higher = more effort)
# These are rough estimates - adjust based on your team's experience
EFFORT_BY_CLUSTER = {
    "APIs": 3,                          # Usually moderate effort
    "Risk & Compliance": 7,             # Complex, requires careful implementation
    "Asset Lifecycles & Approvals": 5,  # Medium complexity
    "Enterprise Readiness": 8,          # High effort, infrastructure work
    "Case & Task Management": 4,        # Standard feature development
    "Other Collaboration Features": 3,  # Usually simpler features
    "WF Management Foundation": 6,      # Core product, needs careful work
    "Workspace Settings": 5,            # Important but well-understood
    "SPG AI": 9,                        # Cutting-edge, high complexity
    "Service Ticket": 2,                # Support issues, quick fixes
}

# Default effort if cluster not found
DEFAULT_EFFORT = 5

# ============================================================================
# FILE PATHS
# ============================================================================
# Where to find input data and save outputs

# Default path to the insights data file (CSV or Excel)
DEFAULT_DATA_PATH = "data/notes-export.csv"

# Output directory for exports
OUTPUT_DIR = "./temp/exports"

# ============================================================================
# DASHBOARD SETTINGS
# ============================================================================

# Page configuration
PAGE_TITLE = "Customer Insight Intelligence Dashboard"
PAGE_ICON = "🎯"

# Chart colors (SAP-inspired palette)
CHART_COLORS = [
    "#0070F2",  # SAP Blue
    "#1A9898",  # Teal
    "#C35500",  # Orange
    "#D20A11",  # Red
    "#256F3A",  # Green
    "#5D36FF",  # Purple
    "#7C7C7C",  # Gray
    "#AA0808",  # Dark Red
    "#0A6ED1",  # Light Blue
]

# Number of sample quotes to show in detail view
MAX_SAMPLE_QUOTES = 5

