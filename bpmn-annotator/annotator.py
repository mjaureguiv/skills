#!/usr/bin/env python3
"""
BPMN Annotator — CLI entry point for Signavio Process Manager.

Enriches any BPMN 2.0 model in SPM with AI-generated annotations:
  task documentation · department colors · lane summaries
  impact analysis · gateway explanations · phase headers

Also translates models into any language by duplicating first:
  translate_dry_run · translate_duplicate · translate_in_place

Usage (PowerShell / Windows)
──────────────────────────────
  # Quality review (no SPM changes)
  python annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode review_only

  # Dry run: print model structure + generation prompt (no SPM changes)
  python annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode dry_run

  # Save generation prompt to file for editing before use
  python annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode dry_run --output prompt.txt

  # Apply pre-generated content (full mode)
  python annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode full --content content.json

  # Apply one layer only
  python annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode documentation_only --content content.json

  # Clean all [BA] annotator content
  python annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode clean_only

  # Clean then reapply with new content
  python annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode clean_and_rerun --content content.json

  # Translation dry run — print what would be translated (no SPM changes)
  python annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode translate_dry_run --language Spanish

  # Duplicate and translate (safe default — original is never touched)
  python annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode translate_duplicate --language German --content translations.json

  # Translate in place (requires explicit --confirm)
  python annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode translate_in_place --language French --content translations.json --confirm

Workflow for full annotation
────────────────────────────
  1. python annotator.py --url "YOUR_URL" --mode dry_run --output prompt.txt
  2. Paste prompt.txt to Claude → Claude returns a JSON block
  3. Save that JSON block to content.json
  4. python annotator.py --url "YOUR_URL" --mode full --content content.json

Workflow for model translation
──────────────────────────────
  1. python annotator.py --url "YOUR_URL" --mode translate_dry_run --language Spanish --output translate_prompt.txt
  2. Paste translate_prompt.txt to Claude → Claude returns a translations JSON
  3. Save that JSON to translations.json
  4. python annotator.py --url "YOUR_URL" --mode translate_duplicate --language Spanish --content translations.json
"""
import argparse
import copy
import json
import sys
from pathlib import Path

# Add the skill root to sys.path so `lib` is importable
sys.path.insert(0, str(Path(__file__).parent))

from lib import (                        # noqa: E402
    get_auth,
    extract_model_id,
    fetch_model,
    submit_model,
    parse_model,
    build_full_generation_prompt,
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
    clean_ba_content,
    has_ba_content,
    review_model_quality,
    collect_translatable_fields,
    build_translation_prompt,
    apply_translations,
    build_multilingual_native_prompt,
    apply_native_translations,
    inspect_multilingual_fields,
    duplicate_model,
    compute_layout_changes,
    apply_layout_changes,
    layout_dry_run_report,
    SUPPORTED_MODES,
    SUPPORTED_LANGUAGES,
    LANGUAGE_CODE_TO_NAME,
)

# ── Layer mode map ─────────────────────────────────────────────────────────────
# Maps each mode to the set of content keys it consumes.
LAYER_MAP = {
    "full":               {"task_docs", "colors", "lane_summaries", "impact_analysis",
                           "gateway_texts", "flow_labels", "phase_headers", "numbering"},
    "documentation_only": {"task_docs"},
    "lane_summary_only":  {"lane_summaries"},
    "impact_only":        {"impact_analysis"},
    "gateway_only":       {"gateway_texts"},
    "flows_only":         {"flow_labels"},
    "phases_only":        {"phase_headers"},
    "numbering_only":     {"numbering"},
}


# ── Commands ───────────────────────────────────────────────────────────────────

def cmd_review(parsed: dict) -> None:
    """Print quality review to stdout. No SPM changes."""
    print(review_model_quality(parsed))


def cmd_dry_run(parsed: dict, output_path: str = None) -> None:
    """Print model structure summary and generation prompt. No SPM changes."""
    prompt = build_full_generation_prompt(parsed)

    if output_path:
        Path(output_path).write_text(prompt, encoding="utf-8")
        print(f"Generation prompt saved to: {output_path}")
        _print_summary(parsed)
        print("\n[Next step] Paste the prompt to Claude, save the JSON response,")
        print(f"            then run:")
        print(f"            python annotator.py --url \"{parsed.get('_url','YOUR_URL')}\" --mode full --content content.json")
        return

    sep = "=" * 68
    print(sep)
    print(f"DRY RUN  --  {parsed['title']}")
    print(sep)
    _print_summary(parsed)
    print(f"\n{sep}")
    print("GENERATION PROMPT")
    print("─" * 68)
    print(prompt)
    print(sep)
    print("[DRY RUN complete — no changes submitted to SPM]")
    print("[Next step] Paste the prompt above to Claude and save the JSON response.")
    print("[Then run ] python annotator.py --url \"YOUR_URL\" --mode full --content content.json")


def cmd_clean(auth, model_id: str, model: dict, info: dict) -> None:
    """Remove all [BA] content (annotations + docs + task numbers) and submit."""
    model["childShapes"] = clean_ba_content(model["childShapes"])
    strip_task_numbers(model["childShapes"])
    rev, updated = submit_model(
        auth, model_id, model, info,
        comment="BPMN Annotator: clean [BA] content",
    )
    print(f"Cleaned.  Revision: {rev}  |  Updated: {updated}")


def cmd_apply(auth, model_id: str, model: dict, info: dict,
              parsed: dict, content: dict, mode: str) -> None:
    """Apply generated content to the model and submit to SPM."""
    layers = LAYER_MAP.get(mode, LAYER_MAP["full"])

    # Always clean first to avoid duplicate annotations
    model["childShapes"] = clean_ba_content(model["childShapes"])

    new_shapes = []
    applied    = []

    if "task_docs" in layers:
        task_docs = content.get("task_docs", {})
        if task_docs:
            apply_task_docs(model["childShapes"], task_docs)
            applied.append(f"  Task documentation    - {len(task_docs)} tasks")

    if "colors" in layers:
        lane_colors = assign_lane_colors(parsed)
        apply_colors(model["childShapes"], lane_colors)
        applied.append(f"  Color coding          - {len(lane_colors)} lanes")

    if "lane_summaries" in layers:
        summaries = content.get("lane_summaries", {})
        shapes = build_lane_summaries(parsed, summaries)
        new_shapes.extend(shapes)
        applied.append(f"  Lane summaries        - {len(shapes)} annotations")

    if "impact_analysis" in layers:
        ia_text = content.get("impact_analysis", "")
        ia = build_impact_analysis(parsed, ia_text)
        if ia:
            new_shapes.append(ia)
            applied.append("  Impact analysis       - 1 annotation")

    if "gateway_texts" in layers:
        gw_texts = content.get("gateway_texts", {})
        shapes = build_gateway_annotations(parsed, gw_texts)
        new_shapes.extend(shapes)
        applied.append(f"  Gateway annotations   - {len(shapes)} annotations")

    if "flow_labels" in layers:
        flow_labels = content.get("flow_labels", {})
        if flow_labels:
            apply_flow_labels(model["childShapes"], flow_labels)
            applied.append(f"  Flow labels           - {len(flow_labels)} flows")

    if "phase_headers" in layers:
        phases = content.get("phase_headers", [])
        shapes = build_phase_headers(parsed, phases)
        new_shapes.extend(shapes)
        if shapes:
            applied.append(f"  Phase headers         - {len(shapes)} headers")

    if "numbering" in layers:
        number_tasks(model["childShapes"], parsed)
        badge_shapes = build_number_badges(model, parsed)
        new_shapes.extend(badge_shapes)
        applied.append(f"  Task numbering        - {len(badge_shapes)} badges (corner badge style)")

    model["childShapes"].extend(new_shapes)

    rev, updated = submit_model(
        auth, model_id, model, info,
        comment=f"BPMN Annotator: {mode}",
    )

    # ── Output report ──────────────────────────────────────────────────────────
    print(f"\nBPMN Annotator  --  {parsed['title']}")
    print(f"Mode: {mode}  |  Revision: {rev}  |  Updated: {updated}")
    print(f"\nLayers applied:")
    for line in applied:
        print(line)
    print(
        f"\nOpen in Signavio: "
        f"https://editor.signavio.com/p/hub/model/{model_id}"
    )


# ── Translation commands ───────────────────────────────────────────────────────

def cmd_translate_dry_run(
    parsed: dict,
    model: dict,
    target_language: str,
    output_path: str = None,
) -> None:
    """Print translation table and prompt. No SPM changes."""
    fields = collect_translatable_fields(parsed, model)
    total  = (
        1
        + len(fields["lanes"])
        + len(fields["tasks"])
        + len(fields["task_docs"])
        + len(fields["gateways"])
        + len(fields["events"])
        + len(fields["flows"])
        + len(fields["annotations"])
        + len(fields["data_objects"])
    )

    sep = "=" * 68
    print(sep)
    print(f"TRANSLATION DRY RUN  --  {parsed['title']}")
    print(f"Target language     : {target_language}")
    print(sep)

    print(f"\nElements to translate: {total}")
    for key, label in [
        ("lanes",       "Lanes          "),
        ("tasks",       "Tasks          "),
        ("task_docs",   "Task docs      "),
        ("gateways",    "Gateways       "),
        ("events",      "Events         "),
        ("flows",       "Flow labels    "),
        ("data_objects","Data objects   "),
        ("annotations", "Annotations    "),
    ]:
        count = len(fields.get(key, []))
        if count:
            print(f"  {label}: {count}")

    prompt = build_translation_prompt(parsed, model, target_language)

    if output_path:
        Path(output_path).write_text(prompt, encoding="utf-8")
        print(f"\nTranslation prompt saved to: {output_path}")
        print("\n[Next step] Paste the prompt to Claude — Claude returns a translations JSON.")
        print(f"[Then run ] python annotator.py --url \"YOUR_URL\" "
              f"--mode translate_duplicate --language \"{target_language}\" "
              f"--content translations.json")
        return

    print(f"\n{sep}")
    print("TRANSLATION PROMPT")
    print("-" * 68)
    print(prompt)
    print(sep)
    print("[DRY RUN complete — no changes submitted to SPM]")
    print("[Next step] Paste the prompt above to Claude and save the JSON response.")
    print(f"[Then run ] python annotator.py --url \"YOUR_URL\" "
          f"--mode translate_duplicate --language \"{target_language}\" "
          f"--content translations.json")


def cmd_translate_duplicate(
    auth,
    model_id: str,
    model: dict,
    info: dict,
    target_language: str,
    translations: dict,
) -> None:
    """Duplicate model, apply translations to the copy, submit. Original untouched."""
    original_name = info["name"]
    new_name      = f"{original_name} - {target_language}"

    print(f"Duplicating '{original_name}' -> '{new_name}' ...")

    # Deep copy so apply_translations doesn't mutate the original model dict
    translated_model = copy.deepcopy(model)
    warnings         = apply_translations(translated_model, translations)

    new_model_id, new_info = duplicate_model(
        auth, translated_model, info, new_name
    )
    print(f"Created    : {new_name}  (ID: {new_model_id})")

    rev, updated = submit_model(
        auth, new_model_id, translated_model, new_info,
        comment=f"BPMN Translator: {target_language} translation",
    )

    print(f"\nTranslation complete  --  {new_name}")
    print(f"Language  : {target_language}  |  Revision: {rev}  |  Updated: {updated}")
    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  ! {w}")
    print(f"\nNew model URL:")
    print(f"  https://editor.signavio.com/p/hub/model/{new_model_id}")
    print(f"\nOriginal model unchanged:")
    print(f"  https://editor.signavio.com/p/hub/model/{model_id}")


def cmd_translate_in_place(
    auth,
    model_id: str,
    model: dict,
    info: dict,
    parsed: dict,
    target_language: str,
    translations: dict,
) -> None:
    """Translate the original model in place (destructive — requires --confirm)."""
    warnings = apply_translations(model, translations)

    rev, updated = submit_model(
        auth, model_id, model, info,
        comment=f"BPMN Translator: {target_language} in-place translation",
    )

    print(f"\nIn-place translation complete  --  {parsed['title']}")
    print(f"Language  : {target_language}  |  Revision: {rev}  |  Updated: {updated}")
    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  ! {w}")
    print(f"\nOpen in Signavio: https://editor.signavio.com/p/hub/model/{model_id}")


# ── Layout cleanup ─────────────────────────────────────────────────────────────

def cmd_layout_cleanup(
    auth,
    model_id: str,
    model: dict,
    info: dict,
    parsed: dict,
    apply: bool = False,
) -> None:
    """Reroute all sequence flows orthogonally.

    Without --confirm: print dry-run report only (no SPM changes).
    With    --confirm: apply changes and submit to SPM.
    """
    changes = compute_layout_changes(model, parsed)
    changed = [c for c in changes if c["changed"]]

    print(layout_dry_run_report(changes, parsed))

    if not apply:
        print(f"\n[Dry run - no changes written to SPM]")
        print(f"Run with --confirm to apply {len(changed)} routing fix(es):")
        print(f'  py annotator.py --url "{model_id}" --mode layout_cleanup --confirm')
        return

    if not changed:
        print("\nNothing to change - all flows already orthogonal.")
        return

    apply_layout_changes(model, changes)
    rev, updated = submit_model(
        auth, model_id, model, info,
        comment="BPMN Annotator: layout_cleanup - orthogonal routing",
    )
    print(f"\nLayout cleanup applied.  Revision: {rev}  |  Updated: {updated}")
    print(f"  {len(changed)} flow(s) rerouted orthogonally.")
    print(f"\nOpen in Signavio: https://editor.signavio.com/p/hub/model/{model_id}")


# ── SGX export ────────────────────────────────────────────────────────────────

def cmd_sgx_export(auth, model_id: str, info: dict, output_dir: str = None) -> None:
    """Download the .sgx ZIP export for a model to temp/ (or output_dir)."""
    import zipfile, io
    dest_dir = Path(output_dir) if output_dir else Path(__file__).parent / "temp"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / f"{model_id}.sgx"

    # SPM exports via /model/{id}/export.sgx
    url = auth.api_base + f"/model/{model_id}/export.sgx"
    r = auth.session.get(url, timeout=60)
    if r.status_code != 200:
        print(f"SGX export failed: HTTP {r.status_code}", file=sys.stderr)
        sys.exit(1)

    dest_path.write_bytes(r.content)
    print(f"SGX export saved: {dest_path}")
    print(f"  Size: {len(r.content) // 1024} KB")

    # Preview contents
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        print(f"\nArchive contents:")
        for entry in z.namelist():
            info_entry = z.getinfo(entry)
            print(f"  {entry:40s}  {info_entry.file_size // 1024} KB")

    print(f"\nTo inspect JSON structure:")
    print(f"  python -c \"import zipfile,json; z=zipfile.ZipFile('{dest_path}'); "
          f"m=json.loads(z.read('model.json')); print(list(m.keys()))\"")


# ── Multilingual inspection ────────────────────────────────────────────────────

def cmd_multilingual_inspect(model: dict, info: dict) -> None:
    """Report which SPM native language fields are populated vs. empty."""
    results = inspect_multilingual_fields(model.get("childShapes", []))

    title = info.get("name", "Unknown")
    print(f"\nMultilingual field inspection for: {title}")
    print("─" * 60)
    if not results:
        print("No native multilingual fields found (properties.names / .documentations).")
        print("\nThis model uses single-language mode.")
        print("Use 'translate_duplicate' to create a language copy,")
        print("or 'multilingual_native' to start populating language fields.")
        return

    print(f"{'Language':<16}  {'Code':<8}  {'Populated':>10}  {'Empty':>6}")
    print("─" * 60)
    for lang_code, data in sorted(results.items()):
        populated = len(data["populated"])
        empty = data["empty"]
        name = LANGUAGE_CODE_TO_NAME.get(lang_code, lang_code)
        print(f"{name:<16}  {lang_code:<8}  {populated:>10}  {empty:>6}")

    print("─" * 60)
    missing = [
        f"{LANGUAGE_CODE_TO_NAME.get(lc, lc)} ({lc})"
        for lc, d in results.items() if d["empty"] > 0
    ]
    if missing:
        print(f"\nIncomplete languages: {', '.join(missing)}")
        print("Use --mode multilingual_native --language <lang> to fill gaps.")


# ── Native multilingual translation ───────────────────────────────────────────

def cmd_multilingual_native(
    auth,
    model_id: str,
    model: dict,
    info: dict,
    target_language: str,
    translations: dict,
) -> None:
    """Write translations into native SPM multilingual fields (non-destructive)."""
    lang_code = translations.get("lang_code")
    if not lang_code:
        # Fall back to SUPPORTED_LANGUAGES lookup
        lang_code = SUPPORTED_LANGUAGES.get(target_language.lower())
    if not lang_code:
        print(
            f"Cannot determine SPM language code for '{target_language}'.\n"
            "Add 'lang_code' to your translations.json or use a supported language name.",
            file=sys.stderr,
        )
        sys.exit(1)

    warnings = apply_native_translations(model, translations, lang_code)

    rev, updated = submit_model(
        auth, model_id, model, info,
        comment=f"BPMN Annotator: multilingual_native add {lang_code}",
    )
    print(f"\nNative multilingual update  --  {info.get('name', model_id)}")
    print(f"Language: {target_language} ({lang_code})")
    print(f"Revision: {rev}  |  Updated: {updated}")
    if warnings:
        print(f"Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  ! {w}")
    print(f"\nOpen in Signavio: https://editor.signavio.com/p/hub/model/{model_id}")




def _print_summary(parsed: dict) -> None:
    print(f"\nProcess  : {parsed['title']}")
    print(f"Lanes    : {[l['name'] for l in parsed['lanes']]}")
    print(f"Tasks    : {len(parsed['tasks'])}")
    print(f"Gateways : {len(parsed['gateways'])}")
    print(f"Events   : {len(parsed['events'])}")
    print(f"Flows    : {len(parsed['flows'])}")
    print(f"\nTasks by lane:")
    for lane in parsed["lanes"]:
        print(f"  [{lane['name']}] {lane['tasks']}")


def _load_content(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        print(f"Error: content file not found: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in {path}: {exc}", file=sys.stderr)
        sys.exit(1)


def _requires_content_file(mode: str) -> bool:
    # numbering_only derives everything from the parsed model — no content file needed
    no_content_modes = {"numbering_only", "clean_and_rerun"}
    if mode in no_content_modes and mode != "clean_and_rerun":
        return False
    return mode in LAYER_MAP or mode == "clean_and_rerun"


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="annotator.py",
        description="BPMN Annotator — enrich or translate Signavio BPMN models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Annotation modes:
  review_only          Quality report in terminal, no SPM changes
  dry_run              Model summary + generation prompt, no SPM changes
  full                 All layers (requires --content)
  documentation_only   Task documentation only (requires --content)
  lane_summary_only    Lane summaries only (requires --content)
  impact_only          Impact analysis only (requires --content)
  gateway_only         Gateway annotations only (requires --content)
  flows_only           Sequence flow labels only (requires --content)
  phases_only          Phase headers only (requires --content)
  clean_only           Remove all [BA] content from SPM
  clean_and_rerun      Remove [BA] then reapply (requires --content)

Translation modes:
  translate_dry_run    Print translation table + prompt, no SPM changes (requires --language)
  translate_duplicate  Duplicate model, translate copy (requires --language + --content)
  translate_in_place   Translate original model directly (requires --language + --content + --confirm)

Examples (PowerShell):
  python annotator.py --url "MODEL_URL" --mode review_only
  python annotator.py --url "MODEL_URL" --mode dry_run --output prompt.txt
  python annotator.py --url "MODEL_URL" --mode full --content content.json
  python annotator.py --url "MODEL_URL" --mode clean_only
  python annotator.py --url "MODEL_URL" --mode translate_dry_run --language Spanish --output t.txt
  python annotator.py --url "MODEL_URL" --mode translate_duplicate --language German --content translations.json
  python annotator.py --url "MODEL_URL" --mode translate_in_place --language French --content translations.json --confirm
        """,
    )
    parser.add_argument("--url",
                        required=True,
                        help="Signavio model URL or 32-char hex model ID")
    parser.add_argument("--mode",
                        default="dry_run",
                        choices=sorted(SUPPORTED_MODES - {"naming_only"}),
                        help="Operation mode (default: dry_run)")
    parser.add_argument("--content",
                        default=None,
                        metavar="FILE",
                        help="JSON file with Claude-generated content "
                             "(required for annotation/translation apply modes)")
    parser.add_argument("--output",
                        default=None,
                        metavar="FILE",
                        help="Save generation/translation prompt to file "
                             "(dry_run and translate_dry_run modes only)")
    parser.add_argument("--language",
                        default=None,
                        metavar="LANG",
                        help="Target language for translation modes "
                             "(e.g. Spanish, German, Japanese, French)")
    parser.add_argument("--confirm",
                        action="store_true",
                        help="Required safety flag for translate_in_place mode")

    args = parser.parse_args()

    # ── Validate translate mode requirements ───────────────────────────────────
    if args.mode.startswith("translate_"):
        if not args.language:
            print(
                f"\nMode '{args.mode}' requires --language.\n"
                "Example: --language Spanish",
                file=sys.stderr,
            )
            sys.exit(1)
        if args.mode == "translate_in_place" and not args.confirm:
            print(
                "\nMode 'translate_in_place' will overwrite the original model.\n"
                "Add --confirm to proceed, or use --mode translate_duplicate to\n"
                "create a safe copy instead.",
                file=sys.stderr,
            )
            sys.exit(1)

    # ── Extract model ID ───────────────────────────────────────────────────────
    model_id = extract_model_id(args.url)
    print(f"Model ID : {model_id}")
    print(f"Mode     : {args.mode}")

    # ── Authenticate + fetch ───────────────────────────────────────────────────
    auth         = get_auth()
    model, info  = fetch_model(auth, model_id)
    parsed       = parse_model(model)
    print(f"Process  : {parsed['title']}")

    # ── Warn if BA content already exists (annotation modes only) ─────────────
    if args.mode not in (
        "review_only", "dry_run", "clean_only", "clean_and_rerun",
        "translate_dry_run", "translate_duplicate", "translate_in_place",
        "layout_cleanup",
    ):
        if has_ba_content(model):
            print(
                "\nWarning: model already contains [BA] annotator content.\n"
                "         Use --mode clean_and_rerun to refresh, or --mode clean_only to remove."
            )

    # ── Dispatch ───────────────────────────────────────────────────────────────
    if args.mode == "review_only":
        cmd_review(parsed)

    elif args.mode == "dry_run":
        cmd_dry_run(parsed, output_path=args.output)

    elif args.mode == "clean_only":
        cmd_clean(auth, model_id, model, info)

    elif args.mode == "numbering_only":
        # Numbering-only: add/refresh numbers WITHOUT touching any other BA layers.
        # We do NOT call cmd_apply() here because cmd_apply() leads with
        # clean_ba_content(), which would wipe lane summaries, gateway annotations,
        # and all other previously-applied BA content.
        # Remove old BA badge shapes and any old text-prefix numbers first.
        model["childShapes"] = [
            s for s in model["childShapes"]
            if not s.get("resourceId", "").startswith("sid-BA-BADGE-")
        ]
        strip_task_numbers(model["childShapes"])
        number_tasks(model["childShapes"], parsed)
        badge_shapes = build_number_badges(model, parsed)
        model["childShapes"].extend(badge_shapes)
        rev, updated = submit_model(
            auth, model_id, model, info,
            comment="BPMN Annotator: numbering_only",
        )
        print(f"\nTask numbering  --  {parsed['title']}")
        print(f"Mode: numbering_only  |  Revision: {rev}  |  Updated: {updated}")
        print(f"  Task numbering        - {len(badge_shapes)} badges (corner badge style)")
        print(f"\nOpen in Signavio: https://editor.signavio.com/p/hub/model/{model_id}")

    elif args.mode == "clean_and_rerun":
        content = _load_content(args.content) if args.content else {}
        if not content:
            print("No --content provided for clean_and_rerun. Run dry_run first.")
            sys.exit(1)
        cmd_apply(auth, model_id, model, info, parsed, content, "full")

    # ── Translation modes ──────────────────────────────────────────────────────
    elif args.mode == "translate_dry_run":
        cmd_translate_dry_run(parsed, model, args.language, output_path=args.output)

    elif args.mode == "translate_duplicate":
        if not args.content:
            print(
                f"\nMode 'translate_duplicate' requires a --content translations file.\n\n"
                "Workflow:\n"
                f"  1. python annotator.py --url \"{args.url}\" "
                f"--mode translate_dry_run --language \"{args.language}\" "
                "--output translate_prompt.txt\n"
                "  2. Paste translate_prompt.txt to Claude — Claude returns a JSON block\n"
                "  3. Save that JSON to translations.json\n"
                f"  4. python annotator.py --url \"{args.url}\" "
                f"--mode translate_duplicate --language \"{args.language}\" "
                "--content translations.json",
                file=sys.stderr,
            )
            sys.exit(1)
        translations = _load_content(args.content)
        cmd_translate_duplicate(auth, model_id, model, info, args.language, translations)

    elif args.mode == "translate_in_place":
        if not args.content:
            print(
                f"\nMode 'translate_in_place' requires a --content translations file.",
                file=sys.stderr,
            )
            sys.exit(1)
        translations = _load_content(args.content)
        cmd_translate_in_place(auth, model_id, model, info, parsed, args.language, translations)

    elif args.mode == "layout_cleanup":
        cmd_layout_cleanup(auth, model_id, model, info, parsed, apply=bool(args.confirm))

    # ── SGX / Native multilingual modes ───────────────────────────────────────
    elif args.mode == "sgx_export":
        cmd_sgx_export(auth, model_id, info, output_dir=args.output)

    elif args.mode == "multilingual_inspect":
        cmd_multilingual_inspect(model, info)

    elif args.mode == "multilingual_native":
        if not args.content:
            print(
                f"\nMode 'multilingual_native' requires a --content translations file.\n\n"
                "Workflow:\n"
                f"  1. python annotator.py --url \"{args.url}\" "
                f"--mode translate_dry_run --language \"{args.language}\" "
                "--output translate_prompt.txt\n"
                "  2. Paste prompt to Claude — Claude returns JSON with "
                "\"mode\": \"multilingual_native\" and \"lang_code\": \"xx_xx\"\n"
                "  3. Save that JSON to translations.json\n"
                f"  4. python annotator.py --url \"{args.url}\" "
                f"--mode multilingual_native --language \"{args.language}\" "
                "--content translations.json",
                file=sys.stderr,
            )
            sys.exit(1)
        translations = _load_content(args.content)
        cmd_multilingual_native(auth, model_id, model, info, args.language, translations)

    elif _requires_content_file(args.mode):
        if not args.content:
            print(
                f"\nMode '{args.mode}' requires a --content file.\n\n"
                "Workflow:\n"
                f"  1. python annotator.py --url \"{args.url}\" --mode dry_run --output prompt.txt\n"
                "  2. Paste prompt.txt to Claude — Claude returns a JSON block\n"
                "  3. Save that JSON to content.json\n"
                f"  4. python annotator.py --url \"{args.url}\" --mode {args.mode} "
                "--content content.json",
                file=sys.stderr,
            )
            sys.exit(1)
        content = _load_content(args.content)
        cmd_apply(auth, model_id, model, info, parsed, content, args.mode)

    else:
        print(f"Unknown mode: {args.mode}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
