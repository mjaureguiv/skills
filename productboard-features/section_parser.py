# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Section parsing for ProductBoard feature descriptions.

Extracts recognized section content from HTML-based feature description bodies,
mapping headers (h2, h3, bold, etc.) to canonical section categories.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Section categories — maps canonical name → list of header variants
# ---------------------------------------------------------------------------

SECTION_CATEGORIES: dict[str, list[str]] = {
    "sec_description": [
        "description", "short description", "idea description",
        "description and scope", "feature description", "description (what)",
        "product narrative",
    ],
    "sec_problem_statement": [
        "problem statement", "problem", "problem definition",
        "problem description", "customer problem", "user problem",
        "problem statement / user need", "problem statement/ needs/ user story",
        "problem to solve (need / pain / desire)",
        "opportunity/problem statement", "problem this solves",
        "problem definition", "problem - internal only",
        "epic goal / problem statement", "pain point/target",
        "pain points", "painpoints", "user pain point",
        "problem statement -", "what problem is being addressed",
        "opportunity (need / pain / desire)", "issue",
    ],
    "sec_value_proposition": [
        "value proposition", "value prop", "value statement",
        "value for customer", "value", "value proposition/ benefits",
    ],
    "sec_benefits": [
        "benefits", "key benefits", "business benefit",
        "business value", "customer value", "expected benefits",
        "benefit", "benefit description", "benefits & value",
    ],
    "sec_capabilities": [
        "capabilities", "key capabilities", "core capabilities",
        "main capabilities include", "capability", "capabilites",
        "feature components", "core functionality",
        "what are the key capabilities",
        "(optional) what are the key capabilities",
    ],
    "sec_scope": [
        "scope", "in scope", "in-scope", "technical scope",
        "scope and limitations", "scope and priority",
        "scope definition", "scope for roadmap item",
        "scope & limitations", "what (scope)", "mvp scope",
    ],
    "sec_out_of_scope": [
        "out of scope", "out-of-scope", "limitations",
        "limitations/out of scope", "limitations/ out of scope",
        "limitations/out of scope -", "known limitation",
        "limitations - internal only", "clearly list what this feature does not",
    ],
    "sec_acceptance_criteria": [
        "acceptance criteria", "success criteria",
        "definition of done", "happy path", "ac/happy path",
        "happy scenario", "success/acceptance criteria",
    ],
    "sec_success_metrics": [
        "success metrics", "metrics", "kpis", "metric",
        "measures of success", "measuring success", "success metric",
        "metrics to track", "key metrics",
    ],
    "sec_dependencies": [
        "dependency", "dependencies", "dependencies and risks",
        "risks", "delivery risks", "risks and limitations",
        "risks and mitigations", "constraints", "prerequisites",
    ],
    "sec_background": [
        "background", "context", "context (why)", "summary",
        "overview", "project overview", "idea background",
        "overall context", "current state", "status quo",
        "current challenges", "why", "why?", "motivation",
        "business context / problem statement",
    ],
    "sec_stakeholders": [
        "stakeholders", "persona", "users", "subject matter expert",
        "stakeholders and contacts", "target audience", "personas",
        "stakeholder", "stakeholder landscape",
        "project lead / po / stakeholders", "who",
    ],
    "sec_solution": [
        "solution", "solution description", "proposed solution",
        "solution ideas", "solutions space", "solution direction",
        "solution space", "solution/hypothesis", "solution  proposals",
        "solution ideas / scope & limitations",
        "what's our solution idea", "possible solutions",
    ],
    "sec_user_story": [
        "user stories", "user story", "as a", "i want",
        "so that", "as an", "as a user", "as an admin",
        "as customer",
    ],
    "sec_documentation": [
        "documentation", "links", "artefacts", "artifacts",
        "link to folder", "reference materials", "references",
        "supporting links", "reference", "prior research & supporting material",
        "supporting docs", "relevant links", "jira", "confluence",
        "figma", "related items",
    ],
    "sec_readiness": [
        "design ready", "test data ready", "smj specifications ready",
        "ready criteria", "specifications ready", "ready to get started",
        "(ready criteria)",
    ],
    "sec_breaking_changes": ["breaking changes"],
    "sec_timeline": [
        "timeline", "next milestone", "past milestones",
        "next milestones", "timelines", "next steps",
    ],
    "sec_competition": [
        "competition", "competitor analysis",
        "market & competitor analysis", "competitive research",
        "market insights", "market",
    ],
    "sec_feedback": [
        "feedback", "validation", "user validation",
        "validation statement", "customer impact",
    ],
    "sec_todo": ["to do", "todo", "action", "next steps", "deliverables"],
    "sec_use_cases": [
        "sample use-cases", "sample use cases", "use cases", "use case",
        "sample use cases supported", "customer use case", "scenario",
    ],
    "sec_moscow": ["moscow"],
    "sec_additional_info": [
        "additional info", "additional information", "note", "notes",
        "remark", "other details", "details", "additional notes",
        "additional topics", "extra notes",
    ],
    "sec_design": [
        "design", "mockup", "mocks", "screenshot", "screenshots",
        "screenshot/mockup", "design and wireframes", "designs",
        "design mocks", "visual", "visuals",
    ],
    "sec_testing": [
        "testing", "test scenario", "test scenarios", "test cases",
        "quality assurance", "usability and qa", "validation and qa",
        "unit tests", "e2e tests", "end-to-end tests",
    ],
    "sec_non_functional": [
        "non-functional requirements", "non-functional requirements & opportunities",
        "non functional requirements",
        "information for development", "technical details",
        "technical considerations", "technical notes",
        "high-level requirement", "requirements",
    ],
    "sec_goal": [
        "goal", "objective", "objectives", "goals",
        "goals & objectives", "expected outcome", "outcome",
        "desired outcome", "business objective",
    ],
}

# Reverse lookup: normalized_header → category
_HEADER_TO_CATEGORY: dict[str, str] = {}
for _cat, _variants in SECTION_CATEGORIES.items():
    for _v in _variants:
        _HEADER_TO_CATEGORY[_v.lower().strip()] = _cat

SECTION_COLUMN_NAMES: list[str] = sorted(SECTION_CATEGORIES.keys())


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def strip_html(html_str: str) -> str:
    """Basic HTML tag stripping."""
    if not html_str:
        return ""
    text = re.sub(r"<[^>]+>", " ", html_str)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _normalize_header(raw: str) -> str:
    """Normalize a raw header string for matching."""
    h = raw.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    h = h.replace("&quot;", '"').replace("&#39;", "'")
    h = re.sub(r'^[\s{}*:_\-–—•]+', '', h)
    h = re.sub(r'[\s{}*:_\-–—•]+$', '', h)
    return h.strip().lower()


def _classify_header(raw: str) -> str | None:
    """Return the section category for a raw header, or None."""
    normalized = _normalize_header(raw)
    if not normalized:
        return None
    if normalized in _HEADER_TO_CATEGORY:
        return _HEADER_TO_CATEGORY[normalized]
    for variant, cat in _HEADER_TO_CATEGORY.items():
        if normalized.startswith(variant) and len(normalized) - len(variant) <= 5:
            return cat
    return None


def extract_description_sections(html: str) -> dict[str, str]:
    """Parse description HTML and extract recognized section content."""
    if not html:
        return {}

    section_patterns = [
        re.compile(r'<h2[^>]*>(.*?)</h2>', re.IGNORECASE | re.DOTALL),
        re.compile(r'<h3[^>]*>(.*?)</h3>', re.IGNORECASE | re.DOTALL),
        re.compile(r'<p[^>]*>\s*<b>(.*?)</b>\s*</p>', re.IGNORECASE | re.DOTALL),
        re.compile(r'<p[^>]*>\s*<strong>(.*?)</strong>\s*</p>', re.IGNORECASE | re.DOTALL),
        re.compile(r'<p[^>]*>\s*<u>\s*<b>(.*?)</b>\s*</u>\s*</p>', re.IGNORECASE | re.DOTALL),
        re.compile(r'<p[^>]*>\s*<b>\s*<u>(.*?)</u>\s*</b>\s*</p>', re.IGNORECASE | re.DOTALL),
        re.compile(r'<p[^>]*>\s*<span\s+data-color=[^>]*>(.*?)</span>\s*</p>', re.IGNORECASE | re.DOTALL),
        re.compile(r'<p[^>]*>\s*<b>\s*<span[^>]*>(.*?)</span>\s*</b>\s*</p>', re.IGNORECASE | re.DOTALL),
    ]

    boundaries: list[tuple[int, int, str]] = []
    for pat in section_patterns:
        for m in pat.finditer(html):
            raw_header = strip_html(m.group(1)).strip()
            if raw_header and len(raw_header) < 120:
                boundaries.append((m.start(), m.end(), raw_header))

    if not boundaries:
        return {}

    boundaries.sort(key=lambda x: x[0])

    result: dict[str, str] = {}
    for i, (start, end, raw_header) in enumerate(boundaries):
        category = _classify_header(raw_header)
        if category is None:
            continue
        if i + 1 < len(boundaries):
            content_html = html[end:boundaries[i + 1][0]]
        else:
            content_html = html[end:]
        content_text = strip_html(content_html).strip()
        if content_text:
            if category in result:
                result[category] = result[category] + " | " + content_text
            else:
                result[category] = content_text
    return result
