"""Shared constants for the BPMN Annotator."""

# ── Marker convention ─────────────────────────────────────────────────────────
# All annotator-generated content carries this prefix so it can be identified
# and removed cleanly by the clean_ba_content() function.
BA_PREFIX = "[BA]"
BA_SID    = "sid-BA-"

# ── Department color palette (ARIS-inspired) ──────────────────────────────────
# Assigned to lanes in order, cycling if > 5 lanes.
LANE_COLOR_PALETTE = [
    {"bgcolor": "#dae8fc", "bordercolor": "#6c8ebf"},  # blue   — HR / Management
    {"bgcolor": "#d5e8d4", "bordercolor": "#82b366"},  # green  — IT / Systems
    {"bgcolor": "#fff2cc", "bordercolor": "#d6b656"},  # amber  — Operations / Line
    {"bgcolor": "#f8cecc", "bordercolor": "#b85450"},  # pink   — External / Customer
    {"bgcolor": "#e1d5e7", "bordercolor": "#9673a6"},  # purple — Finance / Compliance
]

# ── Supported modes ───────────────────────────────────────────────────────────
SUPPORTED_MODES = {
    "full",               # All layers
    "documentation_only", # Task documentation only
    "naming_only",        # Task naming standardization (requires confirmation)
    "numbering_only",     # Auto-number tasks in flow order (adds [BA#] N. prefix)
    "gateway_only",       # Gateway annotations only
    "flows_only",         # Sequence flow labels only
    "phases_only",        # Phase headers only
    "lane_summary_only",  # Lane summary annotations only
    "impact_only",        # Impact analysis only
    "review_only",        # Quality report in chat — no canvas changes
    "clean_and_rerun",    # Remove [BA] content, then rerun full
    "clean_only",         # Remove [BA] content only
    "dry_run",            # Parse + print prompts — no SPM changes
    # ── Translation modes ────────────────────────────────────────────────────
    "translate_dry_run",  # Print translation table + prompt, no SPM changes
    "translate_duplicate",# Duplicate model, translate copy, submit (default safe path)
    "translate_in_place", # Translate original model directly (requires --confirm)
    # ── Native multilingual modes ─────────────────────────────────────────────
    "multilingual_inspect",  # Report which language fields are populated vs. empty
    "multilingual_native",   # Write translations to native properties.names.{lang} fields
    # ── SGX export mode ───────────────────────────────────────────────────────
    "sgx_export",         # Download .sgx ZIP to temp/ for inspection or backup
    # ── Layout modes ─────────────────────────────────────────────────────────
    "layout_cleanup",     # Re-route all connectors orthogonally (dry-run; --confirm to apply)
}

# ── Supported languages for translation ──────────────────────────────────────
# Maps user-friendly language names to SPM language codes.
# Codes confirmed in the SPM REST API; additional codes may depend on tenant config.
SUPPORTED_LANGUAGES = {
    # Core — confirmed in codebase
    "english":            "en_us",
    "spanish":            "es_es",
    "german":             "de_de",
    "japanese":           "ja_jp",
    "french":             "fr_fr",
    "portuguese":         "pt_br",
    # Extended — common SAP Signavio enterprise tenants
    "simplified chinese": "zh_cn",
    "chinese":            "zh_cn",
    "traditional chinese":"zh_tw",
    "dutch":              "nl_nl",
    "italian":            "it_it",
    "korean":             "ko_kr",
    "russian":            "ru_ru",
    "polish":             "pl_pl",
    "swedish":            "sv_se",
    "turkish":            "tr_tr",
    "arabic":             "ar_sa",
    "czech":              "cs_cz",
    "hungarian":          "hu_hu",
    "danish":             "da_dk",
    "finnish":            "fi_fi",
    "norwegian":          "nb_no",
    "thai":               "th_th",
}

# Reverse map: SPM code → display name
LANGUAGE_CODE_TO_NAME = {v: k.title() for k, v in SUPPORTED_LANGUAGES.items()}

# ── SPM authentication source ─────────────────────────────────────────────────
# Path to the spm_mcp package used for direct API access.
SPM_SRC = r'c:\Backup\signavio_process_consultant_experimental\mcp\signavio\spm\src'
