"""
Test script for the improved PowerPoint skill
Tests all major slide types using the slide_builder library
"""

import sys
import os

# Add the lib directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.slide_builder import SlideBuilder, SAPColors, Layouts, Typography
from lib.validate_presentation import validate_presentation, PresentationValidator

# Output path - uses temp directory relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "temp")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "test-all-slide-types.pptx")

# Template path - relative to repo root
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
TEMPLATE_PATH = os.path.join(REPO_ROOT, "templates", "powerpoint", "SAP Template.pptx")


def create_test_presentation():
    """Create a presentation testing all major slide types"""

    print("=" * 60)
    print("POWERPOINT SKILL TEST")
    print("=" * 60)

    # Initialize builder with template
    print(f"\n1. Loading template: {TEMPLATE_PATH}")
    if os.path.exists(TEMPLATE_PATH):
        builder = SlideBuilder(TEMPLATE_PATH)
        print("   [OK] Template loaded successfully")
    else:
        builder = SlideBuilder()
        print("   [WARN] Template not found, using fallback styling")

    # =========================================================================
    # Test 1: Cover Slide
    # =========================================================================
    print("\n2. Creating slides...")
    print("   - Cover slide")
    builder.add_cover_slide(
        title="SAP Signavio Product Update",
        subtitle="Q1 2026 Quarterly Review",
        date="March 2026"
    )

    # =========================================================================
    # Test 2: Agenda Slide
    # =========================================================================
    print("   - Agenda slide")
    builder.add_agenda_slide([
        "Executive Summary",
        "Key Metrics & Performance",
        "Product Highlights",
        "Challenges & Learnings",
        "Q2 Outlook"
    ])

    # =========================================================================
    # Test 3: Section Divider
    # =========================================================================
    print("   - Section divider")
    builder.add_section_divider(
        title="Executive Summary",
        subtitle="Q1 2026 at a glance"
    )

    # =========================================================================
    # Test 4: Content Slide (Standard Bullets)
    # =========================================================================
    print("   - Content slide (bullets)")
    builder.add_content_slide(
        title="Q1 Highlights",
        bullets=[
            "Launched Process Intelligence 2.0 with AI capabilities",
            "Onboarded 50 new enterprise customers globally",
            "Achieved 99.9% platform uptime across all regions",
            "Expanded partner ecosystem to 25+ certified partners",
            "Released mobile app with 4.8 star rating"
        ]
    )

    # =========================================================================
    # Test 5: Section Divider
    # =========================================================================
    print("   - Section divider")
    builder.add_section_divider(title="Key Metrics")

    # =========================================================================
    # Test 6: Metrics Slide (Big Numbers)
    # =========================================================================
    print("   - Metrics slide")
    builder.add_metrics_slide(
        title="Q1 Performance Dashboard",
        metrics=[
            ("€12.5M", "Revenue", "up"),
            ("850+", "Active Customers", "up"),
            ("99.9%", "Uptime", ""),
            ("47", "NPS Score", "up")
        ]
    )

    # =========================================================================
    # Test 7: Two-Column Slide
    # =========================================================================
    print("   - Two-column slide")
    builder.add_two_column_slide(
        title="Process Transformation Impact",
        left_title="Before Signavio",
        left_bullets=[
            "Manual process documentation",
            "8+ hours per analysis",
            "Siloed data across teams",
            "No real-time visibility"
        ],
        right_title="With Signavio",
        right_bullets=[
            "AI-assisted process discovery",
            "15 minutes per analysis",
            "Unified process repository",
            "Live performance dashboards"
        ]
    )

    # =========================================================================
    # Test 8: Three-Column Slide
    # =========================================================================
    print("   - Three-column slide")
    builder.add_three_column_slide(
        title="Product Portfolio Overview",
        columns=[
            ("Process Manager", [
                "Visual process modeling",
                "Collaboration tools",
                "Version control",
                "Export capabilities"
            ]),
            ("Process Intelligence", [
                "Process mining",
                "Conformance checking",
                "Bottleneck detection",
                "AI recommendations"
            ]),
            ("Journey Modeler", [
                "Customer journeys",
                "Experience mapping",
                "Pain point analysis",
                "Opportunity scoring"
            ])
        ]
    )

    # =========================================================================
    # Test 9: Section Divider
    # =========================================================================
    print("   - Section divider")
    builder.add_section_divider(title="Customer Success")

    # =========================================================================
    # Test 10: Quote Slide
    # =========================================================================
    print("   - Quote slide")
    builder.add_quote_slide(
        quote="SAP Signavio transformed how we understand and improve our processes. We reduced cycle time by 40% in the first quarter alone.",
        attribution="Sarah Chen, VP Operations, Global Manufacturing Inc.",
        title="Customer Testimonial"
    )

    # =========================================================================
    # Test 11: Content Slide (Next Steps)
    # =========================================================================
    print("   - Content slide (next steps)")
    builder.add_content_slide(
        title="Q2 2026 Priorities",
        bullets=[
            "Launch Process Intelligence 3.0 with GenAI features",
            "Expand into APAC market with localized offerings",
            "Deepen SAP S/4HANA Cloud integration",
            "Achieve SOC 2 Type II certification"
        ]
    )

    # =========================================================================
    # Test 12: Table Slide (NEW)
    # =========================================================================
    print("   - Table slide")
    builder.add_table_slide(
        title="Feature Comparison",
        headers=["Feature", "Basic", "Pro", "Enterprise"],
        rows=[
            ["Process Mining", "Limited", "Full", "Full + AI"],
            ["Users", "5", "25", "Unlimited"],
            ["Support", "Email", "Priority", "Dedicated"],
            ["API Access", "No", "Yes", "Yes + Custom"],
        ]
    )

    # =========================================================================
    # Test 13: Status Table Slide (NEW)
    # =========================================================================
    print("   - Status table slide")
    builder.add_status_table_slide(
        title="Project Status Overview",
        items=[
            ("Process Mining", "Q1 development complete, testing phase", "green"),
            ("AI Features", "70% complete, on schedule", "yellow"),
            ("Mobile App", "Dependency on API team", "red"),
            ("Documentation", "Draft complete, review pending", "green"),
        ]
    )

    # =========================================================================
    # Test 14: Progress Slide (NEW)
    # =========================================================================
    print("   - Progress slide")
    builder.add_progress_slide(
        title="Q1 OKR Progress",
        progress_items=[
            ("Revenue Target", 85, "On track to exceed"),
            ("Customer Acquisition", 72, "12 more needed"),
            ("Platform Uptime", 99, "Exceeding target"),
            ("NPS Score", 60, "Improvement ongoing"),
        ]
    )

    # =========================================================================
    # Test 15: Timeline Slide (NEW)
    # =========================================================================
    print("   - Timeline slide")
    builder.add_timeline_slide(
        title="Product Roadmap 2026",
        milestones=[
            ("Q1", "PI 2.0 Launch", "completed"),
            ("Q2", "AI Features", "current"),
            ("Q3", "Mobile App", "upcoming"),
            ("Q4", "Enterprise Suite", "upcoming"),
        ],
        current_index=1
    )

    # =========================================================================
    # Test 16: Chart Placeholder Slide (NEW)
    # =========================================================================
    print("   - Chart placeholder slide")
    builder.add_chart_placeholder_slide(
        title="Revenue Trend Analysis",
        chart_title="Quarterly Revenue",
        chart_description="Bar chart showing Q1-Q4 revenue by region",
        insight="EMEA growth of 35% YoY is outpacing other regions"
    )

    # =========================================================================
    # Test 17: Feature Showcase Slide (NEW - Roadmap Pattern)
    # =========================================================================
    print("   - Feature showcase slide")
    builder.add_feature_showcase_slide(
        title="AI-Powered Process Discovery",
        description="Automatically discover and document business processes from event logs",
        status="Beta",
        key_points=[
            "90% faster process mapping",
            "Automatic bottleneck detection",
            "Integration with SAP ERP"
        ]
    )

    # =========================================================================
    # Test 18: Highlights/Lowlights Slide (NEW - PPR Pattern)
    # =========================================================================
    print("   - Highlights/lowlights slide")
    builder.add_highlights_lowlights_slide(
        title="Q1 2026 Highlights and Lowlights",
        highlights=[
            "Exceeded revenue target by 15%",
            "NPS score improved to 47",
            "Successfully launched 3 major features",
            "Zero critical security incidents"
        ],
        lowlights=[
            "Mobile app delayed by 2 months",
            "Documentation backlog growing",
            "Key engineer attrition",
            "Partner certification behind schedule"
        ],
        actions=[
            "Accelerate mobile development",
            "Hire technical writer",
            "Implement retention program",
            "Reschedule partner workshop"
        ]
    )

    # =========================================================================
    # Test 19: What Keeps Us Up at Night (NEW - PPR Pattern)
    # =========================================================================
    print("   - Keeps up at night slide")
    builder.add_keeps_up_at_night_slide(
        title="What Keeps Us Up at Night",
        concerns=[
            ("Market Competition", "New entrants gaining traction with lower pricing models"),
            ("Technical Debt", "Legacy codebase slowing feature velocity by 30%"),
            ("Talent Retention", "Three senior engineers considering offers elsewhere"),
            ("Customer Dependency", "Top 3 customers represent 40% of revenue"),
            ("Regulatory Risk", "GDPR audit scheduled for Q2 with known gaps"),
        ],
        layout="grid"
    )

    # =========================================================================
    # Test 20: Ask Slide (NEW - PPR Pattern)
    # =========================================================================
    print("   - Ask slide")
    builder.add_ask_slide(
        title="Our Ask to Leadership",
        asks=[
            ("Additional Headcount", "Need 2 senior engineers to accelerate mobile development", "Q2 2026"),
            ("Budget Approval", "Marketing budget increase for APAC expansion", "CFO - March"),
            ("Executive Sponsor", "Customer escalation requires VP-level engagement", "Urgent"),
        ]
    )

    # =========================================================================
    # Test 21: Transformation Slide (NEW - NGM Pattern)
    # =========================================================================
    print("   - Transformation slide")
    builder.add_transformation_slide(
        title="From Legacy to Modern Architecture",
        before_title="Past",
        before_points=[
            "Monolithic architecture",
            "Manual deployments",
            "Siloed data",
            "Limited scalability"
        ],
        after_title="Future",
        after_points=[
            "Microservices architecture",
            "CI/CD pipelines",
            "Unified data platform",
            "Cloud-native scalability"
        ],
        transition_text="Evolution"
    )

    # =========================================================================
    # Test 22: Capability Cards Slide (NEW - NGM Pattern)
    # =========================================================================
    print("   - Capability cards slide")
    builder.add_capability_cards_slide(
        title="SAP Signavio Process Modeler Capabilities",
        capabilities=[
            ("PM", "Process Modeling", "Visual process design with BPMN 2.0 notation"),
            ("AI", "AI-Powered Discovery", "Automatic process mining from event logs"),
            ("CO", "Collaboration", "Real-time multi-user editing and commenting"),
            ("IN", "Integration", "Seamless connection to SAP ecosystem"),
        ],
        badge_text="By end of 2026"
    )

    # =========================================================================
    # Test 23: Release Phases Slide (NEW - NGM Pattern)
    # =========================================================================
    print("   - Release phases slide")
    builder.add_release_phases_slide(
        title="Process Modeler Release Phases",
        phases=[
            ("Alpha", "Dec '25", "gray", ["Internal testing", "Core features"]),
            ("Beta", "May '26", "orange", ["Advanced modeling", "Feedback iteration", "Partner access"]),
            ("GA", "Dec '26", "green", ["Full feature set", "Commercial launch", "Support ready"]),
        ]
    )

    # =========================================================================
    # Test 24: Roadmap Table Slide (NEW - NGM Pattern)
    # =========================================================================
    print("   - Roadmap table slide")
    builder.add_roadmap_table_slide(
        title="Feature Roadmap 2026-2027",
        categories=["Core Modeling", "AI Features", "Integration"],
        timeframes=["H1 2026", "H2 2026", "2027+"],
        items=[
            [["Canvas redesign", "Shape management"], ["Version control", "View/Edit modes"], ["Advanced export"]],
            [["Text to Process"], ["Conversational AI", "Auto-suggestion"], ["Process optimization"]],
            [["Suite connectivity"], ["Dictionary integration"], ["S/4HANA deep integration"]],
        ]
    )

    # =========================================================================
    # Test 25: Executive Summary Slide (NEW - PPR Pattern)
    # =========================================================================
    print("   - Executive summary slide")
    builder.add_executive_summary_slide(
        title="Executive Summary Dashboard",
        sections=[
            ("Revenue", [
                ("$12.5M", "Q1 Revenue", "up"),
                ("23%", "YoY Growth", "up"),
            ]),
            ("Customers", [
                ("850+", "Active", "up"),
                ("47", "NPS", ""),
            ]),
            ("Operations", [
                ("99.9%", "Uptime", ""),
                ("15min", "Avg Response", "down"),
            ]),
        ]
    )

    # =========================================================================
    # Test 26: Funnel Slide (NEW - PPR Pattern)
    # =========================================================================
    print("   - Funnel slide")
    builder.add_funnel_slide(
        title="Customer Acquisition Funnel",
        stages=[
            ("Awareness", "50,000", "+15%", "Website visitors"),
            ("Interest", "12,000", "+8%", "Demo requests"),
            ("Consideration", "3,500", "+12%", "Qualified leads"),
            ("Purchase", "850", "+23%", "New customers"),
        ]
    )

    # =========================================================================
    # Test 27: OKR Slide (NEW - PPR Pattern)
    # =========================================================================
    print("   - OKR slide")
    builder.add_okr_slide(
        title="Q1 2026 OKR Progress",
        objectives=[
            ("Grow Revenue", [
                ("Achieve $12M quarterly revenue", 85, "on_track"),
                ("Close 3 enterprise deals", 66, "at_risk"),
                ("Expand EMEA by 20%", 100, "completed"),
            ]),
            ("Improve Product", [
                ("Launch AI features", 90, "on_track"),
                ("Reduce load time by 50%", 45, "at_risk"),
            ]),
        ]
    )

    # =========================================================================
    # Test 28: Win/Loss Slide (NEW - PPR Pattern)
    # =========================================================================
    print("   - Win/loss slide")
    builder.add_win_loss_slide(
        title="Q1 Deal Analysis",
        wins=[
            ("Acme Corp", "$2.5M"),
            ("TechGlobal", "$1.8M"),
            ("FinServe Inc", "$950K"),
        ],
        losses=[
            ("MegaRetail", "Price - lost to competitor"),
            ("DataFirst", "Feature gap - no mobile support"),
        ],
        summary_stats={
            "Win Rate": "65%",
            "Avg Deal Size": "$1.4M",
            "Pipeline": "$15M",
        }
    )

    # =========================================================================
    # Test 29: Thank You Slide
    # =========================================================================
    print("   - Thank you slide")
    builder.add_thank_you_slide(
        title="Thank You",
        contact_info="questions@sap.com | sap.com/signavio",
        next_steps=[
            "Schedule follow-up discussion",
            "Access demo environment",
            "Review detailed metrics report"
        ]
    )

    # =========================================================================
    # Save the presentation
    # =========================================================================
    print(f"\n3. Saving presentation to: {OUTPUT_FILE}")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    builder.save(OUTPUT_FILE)
    print("   [OK] Presentation saved successfully")

    # Check for any issues during building
    issues = builder.get_issues()
    if issues:
        print(f"\n   [WARN] Builder issues:")
        for issue in issues:
            print(f"     - {issue}")

    print(f"\n   Slides created: {builder.get_slide_count()}")

    # =========================================================================
    # Validate the presentation
    # =========================================================================
    print("\n4. Validating presentation...")
    is_valid, report = validate_presentation(OUTPUT_FILE)

    print("\n" + report)

    if is_valid:
        print("\n[OK] TEST PASSED: Presentation is valid!")
    else:
        print("\n[WARN] TEST COMPLETED: Some validation issues found (see report above)")

    return OUTPUT_FILE


if __name__ == "__main__":
    output_path = create_test_presentation()
    print(f"\nOutput: {output_path}")
