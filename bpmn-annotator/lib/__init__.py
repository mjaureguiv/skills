"""BPMN Annotator library — public API."""

from .auth      import get_auth
from .fetch     import extract_model_id, fetch_model, submit_model
from .parse     import parse_model
from .generate  import (
    build_full_generation_prompt,
    generate_task_documentation,
    generate_gateway_explanation,
    generate_flow_label,
    generate_lane_summary,
    generate_impact_analysis,
    generate_phase_headers,
)
from .annotate  import (
    apply_task_docs,
    apply_colors,
    assign_lane_colors,
    apply_flow_labels,
    build_lane_summaries,
    build_impact_analysis,
    build_gateway_annotations,
    build_phase_headers,
    number_tasks,
    build_number_badges,
    strip_task_numbers,
)
from .clean     import clean_ba_content, has_ba_content
from .review    import review_model_quality
from .translate import (
    collect_translatable_fields,
    build_translation_prompt,
    apply_translations,
    build_multilingual_native_prompt,
    apply_native_translations,
    inspect_multilingual_fields,
    PROTECTED_TERMS,
)
from .duplicate import create_model, duplicate_model
from .layout    import (
    compute_layout_changes,
    apply_layout_changes,
    layout_dry_run_report,
)
from .constants import BA_PREFIX, BA_SID, LANE_COLOR_PALETTE, SUPPORTED_MODES, SUPPORTED_LANGUAGES, LANGUAGE_CODE_TO_NAME

__all__ = [
    # auth
    "get_auth",
    # fetch
    "extract_model_id", "fetch_model", "submit_model",
    # parse
    "parse_model",
    # generate
    "build_full_generation_prompt",
    "generate_task_documentation",
    "generate_gateway_explanation",
    "generate_flow_label",
    "generate_lane_summary",
    "generate_impact_analysis",
    "generate_phase_headers",
    # annotate
    "apply_task_docs", "apply_colors", "assign_lane_colors", "apply_flow_labels",
    "build_lane_summaries", "build_impact_analysis",
    "build_gateway_annotations", "build_phase_headers",
    "number_tasks", "build_number_badges", "strip_task_numbers",
    # clean
    "clean_ba_content", "has_ba_content",
    # review
    "review_model_quality",
    # translate
    "collect_translatable_fields", "build_translation_prompt",
    "apply_translations", "build_multilingual_native_prompt",
    "apply_native_translations", "inspect_multilingual_fields", "PROTECTED_TERMS",
    # duplicate
    "create_model", "duplicate_model",
    # layout
    "compute_layout_changes", "apply_layout_changes", "layout_dry_run_report",
    # constants
    "BA_PREFIX", "BA_SID", "LANE_COLOR_PALETTE", "SUPPORTED_MODES",
    "SUPPORTED_LANGUAGES", "LANGUAGE_CODE_TO_NAME",
]
