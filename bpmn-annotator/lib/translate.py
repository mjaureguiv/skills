"""Translation layer for BPMN model localization.

Provides three public functions:
  collect_translatable_fields(parsed, model)  — inventory of translatable text
  build_translation_prompt(parsed, model, target_language, source_language)
                                               — prompt string for Claude
  apply_translations(model, translations)      — mutate model in-place
"""
import re


# ── Protected terms ────────────────────────────────────────────────────────────
# These are never translated regardless of target language. Matched as whole
# words (case-sensitive) so "HR" is protected but "her" is not.
PROTECTED_TERMS = frozenset({
    # SAP and ecosystem products
    "SAP", "S/4HANA", "SuccessFactors", "Ariba", "Fieldglass", "Concur",
    "Signavio", "ARIS", "Celonis",
    # Common SaaS tools
    "Jira", "Confluence", "GitHub", "GitLab", "Slack", "Teams",
    "SharePoint", "ServiceNow", "Salesforce", "Workday",
    # Office tools
    "Excel", "Word", "PowerPoint", "Outlook",
    # Process/modeling standards
    "BPMN", "DMN", "CMMN",
    # Enterprise concepts kept as abbreviations
    "ERP", "CRM", "SLA", "KPI", "OKR", "API", "REST", "JSON", "XML",
    "SSO", "LDAP", "SCIM", "IdP",
    # Role abbreviations
    "HR", "IT", "PM", "LM", "CEO", "CFO", "CTO", "CIO", "CHRO", "CPO",
    "COO", "VP",
    # Annotator markers — preserve exactly
    "[BA]", "[BA#]",
})

# Regex to find protected terms as whole words (case-sensitive)
_PROTECTED_RE = re.compile(
    r'(?<!\w)(' +
    '|'.join(re.escape(t) for t in sorted(PROTECTED_TERMS, key=len, reverse=True)) +
    r')(?!\w)'
)


def _find_protected_terms(text: str) -> list:
    """Return sorted unique list of protected terms found in text."""
    return sorted(set(_PROTECTED_RE.findall(text)))


# ── Field collection ───────────────────────────────────────────────────────────

def collect_translatable_fields(parsed: dict, model: dict) -> dict:
    """Collect all translatable text from parsed + raw model.

    Returns a dict with these keys (each value is a list of (id, text) tuples,
    except model_title which is a plain string):

        model_title  — pool/process name
        lanes        — [(id, name), ...]
        tasks        — [(id, name), ...]
        task_docs    — [(id, doc_text), ...]   non-empty docs only
        gateways     — [(id, name), ...]       named gateways only
        events       — [(id, name), ...]       named events only
        flows        — [(id, name), ...]       labeled flows only
        annotations  — [(id, text), ...]       TextAnnotation shapes
        data_objects — [(id, name), ...]       DataObject shapes
    """
    return {
        "model_title": parsed["title"],
        "lanes":       [(l["id"], l["name"]) for l in parsed["lanes"] if l["name"]],
        "tasks":       [(t["id"], t["name"]) for t in parsed["tasks"]],
        "task_docs":   [(t["id"], t["existing_doc"])
                        for t in parsed["tasks"] if t["existing_doc"]],
        "gateways":    [(g["id"], g["name"]) for g in parsed["gateways"] if g["name"]],
        "events":      [(e["id"], e["name"]) for e in parsed["events"] if e["name"]],
        "flows":       [(f["id"], f["name"]) for f in parsed["flows"] if f["name"]],
        "annotations": _collect_annotations(model.get("childShapes", [])),
        "data_objects": _collect_data_objects(model.get("childShapes", [])),
    }


def _collect_annotations(shapes: list) -> list:
    """Recursively collect (id, text) from all TextAnnotation shapes."""
    result = []
    for s in shapes:
        if s.get("stencil", {}).get("id") == "TextAnnotation":
            text = s.get("properties", {}).get("text", "").strip()
            if text:
                result.append((s["resourceId"], text))
        result.extend(_collect_annotations(s.get("childShapes", [])))
    return result


def _collect_data_objects(shapes: list) -> list:
    """Recursively collect (id, name) from all DataObject shapes."""
    result = []
    for s in shapes:
        if s.get("stencil", {}).get("id") == "DataObject":
            name = s.get("properties", {}).get("name", "").strip()
            if name:
                result.append((s["resourceId"], name))
        result.extend(_collect_data_objects(s.get("childShapes", [])))
    return result


# ── Prompt builder ─────────────────────────────────────────────────────────────

def build_translation_prompt(
    parsed: dict,
    model: dict,
    target_language: str,
    source_language: str = None,
) -> str:
    """Build a Claude translation prompt for the model.

    The returned string is designed to be pasted into Claude, which returns
    a translations JSON to feed back into apply_translations().
    """
    fields = collect_translatable_fields(parsed, model)
    src_label = f" from {source_language}" if source_language else ""

    total = (
        1  # model_title
        + len(fields["lanes"])
        + len(fields["tasks"])
        + len(fields["task_docs"])
        + len(fields["gateways"])
        + len(fields["events"])
        + len(fields["flows"])
        + len(fields["annotations"])
        + len(fields["data_objects"])
    )

    lines = [
        f"You are translating a BPMN process model{src_label} into **{target_language}**.",
        "",
        "## Translation Rules",
        "",
        "1. Use professional business process language.",
        "2. Keep task names SHORT (≤ 40 characters). Use **Verb + Object** format.",
        "3. Keep terminology CONSISTENT — translate each term the same way throughout.",
        "4. Create a mental terminology dictionary and reuse it: if a term appears multiple",
        "   times, translate it identically each time.",
        "5. Preserve `[BA]` and `[BA#]` prefixes **exactly as-is** — translate only the",
        "   text that follows them.",
        "6. Preserve business meaning over literal word-for-word translation.",
        "7. **DO NOT translate** these protected terms — keep them unchanged:",
        "   `" + "`, `".join(sorted(PROTECTED_TERMS)) + "`",
        "8. **DO NOT translate**: IDs, URLs, email addresses, codes, technical tokens,",
        "   or any value that looks like a system identifier.",
        "9. If a product or system name is not listed above but is clearly a proper noun,",
        "   keep it unchanged.",
        "",
        f"## Model: {parsed['title']}",
        f"Target language: {target_language}",
        f"Total text elements to translate: {total}",
        "",
    ]

    # ── Model title ────────────────────────────────────────────────────────────
    lines += [
        "### Pool / Model Title",
        f"  (pool)  →  \"{fields['model_title']}\"",
        "",
    ]

    # ── Lanes ──────────────────────────────────────────────────────────────────
    if fields["lanes"]:
        lines.append("### Lanes")
        for lid, lname in fields["lanes"]:
            protected = _find_protected_terms(lname)
            note = f"  [keep: {', '.join(protected)}]" if protected else ""
            lines.append(f"  {lid}  →  \"{lname}\"{note}")
        lines.append("")

    # ── Tasks ──────────────────────────────────────────────────────────────────
    if fields["tasks"]:
        lines.append("### Tasks")
        for tid, tname in fields["tasks"]:
            protected = _find_protected_terms(tname)
            note = f"  [keep: {', '.join(protected)}]" if protected else ""
            lines.append(f"  {tid}  →  \"{tname}\"{note}")
        lines.append("")

    # ── Gateways ───────────────────────────────────────────────────────────────
    if fields["gateways"]:
        lines.append("### Gateways  (translate the decision question only if meaningful)")
        for gid, gname in fields["gateways"]:
            lines.append(f"  {gid}  →  \"{gname}\"")
        lines.append("")

    # ── Events ─────────────────────────────────────────────────────────────────
    if fields["events"]:
        lines.append("### Events")
        for eid, ename in fields["events"]:
            protected = _find_protected_terms(ename)
            note = f"  [keep: {', '.join(protected)}]" if protected else ""
            lines.append(f"  {eid}  →  \"{ename}\"{note}")
        lines.append("")

    # ── Sequence Flow Labels ───────────────────────────────────────────────────
    if fields["flows"]:
        lines.append("### Sequence Flow Labels  (short condition labels)")
        for fid, fname in fields["flows"]:
            lines.append(f"  {fid}  →  \"{fname}\"")
        lines.append("")

    # ── Data Objects ───────────────────────────────────────────────────────────
    if fields["data_objects"]:
        lines.append("### Data Objects  (documents / data stores)")
        for did, dname in fields["data_objects"]:
            lines.append(f"  {did}  →  \"{dname}\"")
        lines.append("")

    # ── Text annotations ───────────────────────────────────────────────────────
    if fields["annotations"]:
        lines.append("### Text Annotations  (translate full text; preserve [BA] prefix)")
        for aid, atext in fields["annotations"]:
            preview = atext[:100].replace("\n", " ")
            if len(atext) > 100:
                preview += "..."
            lines.append(f"  {aid}  →  \"{preview}\"")
        lines.append("")

    # ── Task documentation ─────────────────────────────────────────────────────
    if fields["task_docs"]:
        lines.append("### Task Documentation  (translate full text; preserve [BA] prefix)")
        for tid, doc in fields["task_docs"]:
            preview = doc[:100].replace("\n", " ")
            if len(doc) > 100:
                preview += "..."
            lines.append(f"  {tid}  →  \"{preview}\"")
        lines.append("")

    # ── Output format ──────────────────────────────────────────────────────────
    src_str = source_language or "auto-detected"
    lines += [
        "## Required Output Format",
        "",
        "Return **ONLY** a valid JSON object. Omit any section that has no entries.",
        "Do not include explanatory text before or after the JSON.",
        "",
        "```json",
        "{",
        f'  "target_language": "{target_language}",',
        f'  "source_language": "{src_str}",',
        '  "model_title": "...",',
        '  "lanes":    { "lane-id": "translated name", ... },',
        '  "tasks":    { "task-id": "translated name", ... },',
        '  "task_docs":{ "task-id": "translated documentation text", ... },',
        '  "gateways": { "gw-id":   "translated label", ... },',
        '  "events":   { "event-id":"translated name", ... },',
        '  "flows":    { "flow-id": "translated label", ... },',
        '  "data_objects": { "do-id": "translated name", ... },',
        '  "annotations": { "annot-id": "translated text", ... }',
        "}",
        "```",
        "",
        "**Important notes:**",
        "- For `task_docs` and `annotations` that start with `[BA]`, keep the `[BA]`",
        "  prefix and translate the rest.",
        "- Keys are element IDs — copy them exactly from the list above.",
        "- Translate all tasks, even if no name change seems needed (e.g. proper nouns",
        "  should still appear in the `tasks` section with the same value).",
    ]

    return "\n".join(lines)


# ── Translation application ────────────────────────────────────────────────────

def apply_translations(model: dict, translations: dict) -> list:
    """Apply a translations dict to model JSON in-place.

    Walks the entire childShapes tree and replaces text fields wherever the
    element's resourceId appears in the translations dict.

    Returns:
        List of warning strings (empty if all went well).
    """
    warnings: list = []
    _translate_shapes(model.get("childShapes", []), translations, warnings)
    return warnings


def _translate_shapes(shapes: list, tr: dict, warnings: list) -> None:
    """Recursively apply translations to every shape in the tree."""
    for s in shapes:
        stencil = s.get("stencil", {}).get("id", "")
        rid     = s.get("resourceId", "")
        props   = s.setdefault("properties", {})

        if stencil == "Pool":
            if "model_title" in tr:
                props["name"] = tr["model_title"]

        elif stencil == "Lane":
            new_name = tr.get("lanes", {}).get(rid)
            if new_name is not None:
                props["name"] = new_name

        elif stencil == "Task":
            new_name = tr.get("tasks", {}).get(rid)
            if new_name is not None:
                # Preserve any [BA#] numbering prefix already applied
                existing = props.get("name", "")
                if existing.startswith("[BA#]"):
                    # Strip prefix, replace base name, reattach prefix
                    import re as _re
                    prefix_match = _re.match(r"(\[BA#\]\s+\d+\.\s+)(.*)", existing)
                    if prefix_match:
                        props["name"] = prefix_match.group(1) + new_name
                    else:
                        props["name"] = new_name
                else:
                    props["name"] = new_name
            new_doc = tr.get("task_docs", {}).get(rid)
            if new_doc is not None:
                props["documentation"] = new_doc

        elif "Gateway" in stencil:
            new_name = tr.get("gateways", {}).get(rid)
            if new_name is not None:
                props["name"] = new_name

        elif "Event" in stencil:
            new_name = tr.get("events", {}).get(rid)
            if new_name is not None:
                props["name"] = new_name

        elif stencil == "SequenceFlow":
            new_label = tr.get("flows", {}).get(rid)
            if new_label is not None:
                props["name"] = new_label

        elif stencil == "DataObject":
            new_name = tr.get("data_objects", {}).get(rid)
            if new_name is not None:
                props["name"] = new_name

        elif stencil == "TextAnnotation":
            new_text = tr.get("annotations", {}).get(rid)
            if new_text is not None:
                props["text"] = new_text

        _translate_shapes(s.get("childShapes", []), tr, warnings)


# ── Native multilingual support ────────────────────────────────────────────────
# SPM stores multiple language versions natively inside a single model using:
#   properties.names     = {"en_us": "name", "de_de": "Name auf Deutsch", ...}
#   properties.documentations = {"en_us": "...", "de_de": "..."}
#
# This is distinct from translate_duplicate (which copies the model and overwrites
# properties.name). Native multilingual keeps ONE model with all language variants,
# which is how enterprise customers like Mercedes-Benz use SPM in practice.

def inspect_multilingual_fields(shapes: list) -> dict:
    """Scan childShapes tree for native multilingual fields.

    Returns a dict mapping lang_code → {"populated": [element_names], "empty": int}
    so the caller can report which languages are filled vs. missing.
    """
    lang_counts: dict = {}

    def _walk(s_list):
        for s in s_list:
            props = s.get("properties", {})
            for field in ("names", "documentations"):
                lang_map = props.get(field)
                if isinstance(lang_map, dict):
                    for lang_code, value in lang_map.items():
                        if lang_code not in lang_counts:
                            lang_counts[lang_code] = {"populated": [], "empty": 0}
                        name = props.get("name", props.get("text", s.get("resourceId", "?")))
                        if value and value.strip():
                            lang_counts[lang_code]["populated"].append(name[:60])
                        else:
                            lang_counts[lang_code]["empty"] += 1
            _walk(s.get("childShapes", []))

    _walk(shapes)
    return lang_counts


def build_multilingual_native_prompt(
    parsed: dict,
    model: dict,
    target_language: str,
    lang_code: str,
    source_language: str = None,
) -> str:
    """Build a translation prompt for native multilingual field population.

    Instead of overwriting properties.name, this targets properties.names.{lang_code}
    and properties.documentations.{lang_code}. The original names remain untouched.
    """
    fields = collect_translatable_fields(parsed, model)
    src_label = f" from {source_language}" if source_language else ""

    total = (
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

    lines = [
        f"You are populating the **{target_language}** (`{lang_code}`) language field in a",
        f"native multilingual BPMN model{src_label}.",
        "",
        "## Context",
        "",
        "SAP Signavio Process Manager stores multiple language versions inside ONE model.",
        "Each element has `properties.names` and `properties.documentations` dictionaries",
        f"keyed by language code. You are filling in the `{lang_code}` entries.",
        "The original `properties.name` values (shown below as source text) are NOT changed.",
        "",
        "## Translation Rules",
        "",
        "1. Use professional business process language for the target locale.",
        "2. Keep task names SHORT (≤ 40 characters). Use **Verb + Object** format.",
        "3. Maintain a CONSISTENT terminology dictionary throughout.",
        "4. Preserve `[BA]` and `[BA#]` prefixes exactly — translate only the text after them.",
        "5. Preserve business meaning over literal word-for-word translation.",
        "6. **DO NOT translate** these protected terms — keep them unchanged:",
        "   `" + "`, `".join(sorted(PROTECTED_TERMS)) + "`",
        "7. **DO NOT translate**: IDs, URLs, email addresses, codes, technical tokens.",
        "",
        f"## Model: {parsed['title']}",
        f"Target language: {target_language} (code: {lang_code})",
        f"Total elements: {total}",
        "",
        "### Source Text → Translate to fill `names[\"{lang_code}\"]`",
        "",
    ]

    if fields["tasks"]:
        lines.append("#### Tasks")
        for tid, tname in fields["tasks"]:
            lines.append(f"  {tid}  →  \"{tname}\"")
        lines.append("")

    if fields["lanes"]:
        lines.append("#### Lanes")
        for lid, lname in fields["lanes"]:
            lines.append(f"  {lid}  →  \"{lname}\"")
        lines.append("")

    if fields["gateways"]:
        lines.append("#### Gateways")
        for gid, gname in fields["gateways"]:
            lines.append(f"  {gid}  →  \"{gname}\"")
        lines.append("")

    if fields["events"]:
        lines.append("#### Events")
        for eid, ename in fields["events"]:
            lines.append(f"  {eid}  →  \"{ename}\"")
        lines.append("")

    if fields["flows"]:
        lines.append("#### Sequence Flow Labels")
        for fid, fname in fields["flows"]:
            lines.append(f"  {fid}  →  \"{fname}\"")
        lines.append("")

    if fields["data_objects"]:
        lines.append("#### Data Objects")
        for did, dname in fields["data_objects"]:
            lines.append(f"  {did}  →  \"{dname}\"")
        lines.append("")

    if fields["task_docs"]:
        lines.append("#### Task Documentation  (fill `documentations[\"{lang_code}\"]`)")
        for tid, doc in fields["task_docs"]:
            preview = doc[:100].replace("\n", " ")
            if len(doc) > 100:
                preview += "..."
            lines.append(f"  {tid}  →  \"{preview}\"")
        lines.append("")

    src_str = source_language or "auto-detected"
    lines += [
        "## Required Output Format",
        "",
        "Return **ONLY** a valid JSON object. Keys are resourceId values.",
        "Omit any section that has no entries.",
        "",
        "```json",
        "{",
        f'  "target_language": "{target_language}",',
        f'  "lang_code": "{lang_code}",',
        f'  "source_language": "{src_str}",',
        '  "mode": "multilingual_native",',
        '  "model_title": "...",',
        '  "tasks":    { "task-id": "translated name", ... },',
        '  "lanes":    { "lane-id": "translated name", ... },',
        '  "task_docs":{ "task-id": "translated documentation text", ... },',
        '  "gateways": { "gw-id":   "translated label", ... },',
        '  "events":   { "event-id":"translated name", ... },',
        '  "flows":    { "flow-id": "translated label", ... },',
        '  "data_objects": { "do-id": "translated name", ... }',
        "}",
        "```",
    ]

    return "\n".join(lines)


def apply_native_translations(model: dict, translations: dict, lang_code: str) -> list:
    """Apply translations to native multilingual fields (properties.names.{lang_code}).

    Unlike apply_translations(), this writes to the `names` / `documentations`
    sub-dictionaries rather than overwriting `properties.name`. The original name
    is preserved; only the target-language slot is filled or updated.

    Returns:
        List of warning strings (empty if all went well).
    """
    warnings: list = []
    _apply_native_shapes(model.get("childShapes", []), translations, lang_code, warnings)
    return warnings


def _apply_native_shapes(shapes: list, tr: dict, lang_code: str, warnings: list) -> None:
    """Recursively apply native multilingual translations."""
    for s in shapes:
        stencil = s.get("stencil", {}).get("id", "")
        rid     = s.get("resourceId", "")
        props   = s.setdefault("properties", {})

        def _set_name(section: str, new_value) -> None:
            if new_value is None:
                return
            names_dict = props.setdefault(section, {})
            if not isinstance(names_dict, dict):
                # Upgrade scalar to dict: preserve existing value as en_us
                existing = names_dict
                props[section] = {"en_us": existing}
                names_dict = props[section]
            names_dict[lang_code] = new_value

        if stencil == "Pool":
            _set_name("names", tr.get("model_title"))

        elif stencil == "Lane":
            _set_name("names", tr.get("lanes", {}).get(rid))

        elif stencil == "Task":
            _set_name("names", tr.get("tasks", {}).get(rid))
            _set_name("documentations", tr.get("task_docs", {}).get(rid))

        elif "Gateway" in stencil:
            _set_name("names", tr.get("gateways", {}).get(rid))

        elif "Event" in stencil:
            _set_name("names", tr.get("events", {}).get(rid))

        elif stencil == "SequenceFlow":
            _set_name("names", tr.get("flows", {}).get(rid))

        elif stencil == "DataObject":
            _set_name("names", tr.get("data_objects", {}).get(rid))

        _apply_native_shapes(s.get("childShapes", []), tr, lang_code, warnings)
