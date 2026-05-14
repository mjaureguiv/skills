"""Model duplication via SPM REST API.

Creates a copy of an existing model in the same parent folder with a new name.
Used by the translate_duplicate mode to avoid ever modifying the original.
"""
import json
import re
import urllib.parse


def create_model(
    auth,
    name: str,
    parent: str,
    model_json: dict,
    namespace: str = "http://b3mn.org/stencilset/bpmn2.0#",
    model_type: str = "Business Process Diagram (BPMN 2.0)",
    comment: str = "Duplicated by BPMN Annotator",
) -> str:
    """POST a new BPMN model to SPM.

    SPM's REST endpoint for model creation:
        POST /model
        Content-Type: application/x-www-form-urlencoded
        Body: json_xml=...&name=...&parent=...&namespace=...&type=...&comment=...

    The response is the same list-of-{rel,rep} format as PUT /model, or the new
    model ID can be extracted from the 'href' field in the response items.

    Returns:
        The new model ID (32-char hex string).
    Raises:
        requests.HTTPError on non-2xx responses.
        RuntimeError if the model ID cannot be extracted from the response.
    """
    json_xml = json.dumps(model_json, separators=(",", ":"))
    encoded  = urllib.parse.urlencode({
        "json_xml":  json_xml,
        "name":      name,
        "comment":   comment,
        "parent":    parent,
        "namespace": namespace,
        "type":      model_type,
    })
    response = auth.session.post(
        f"{auth.api_base}/model",
        data=encoded,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=120,
    )
    response.raise_for_status()
    result = response.json()

    # SPM returns [{rel: "mod"|"info", rep: {...}, href: "/model/{id}"}, ...]
    if isinstance(result, list):
        for item in result:
            if not isinstance(item, dict):
                continue
            # Try href — most reliable source of new model ID
            href = item.get("href", "")
            m = re.search(r"/model/([a-f0-9]{32})", href)
            if m:
                return m.group(1)
            # Try rep dict
            rep = item.get("rep", {})
            mid = rep.get("modelId") or rep.get("id") or ""
            mid = mid.strip("/").split("/")[-1]
            if re.fullmatch(r"[a-f0-9]{32}", mid):
                return mid

    # Flat dict response (some SPM versions)
    if isinstance(result, dict):
        href = result.get("href", "")
        m = re.search(r"/model/([a-f0-9]{32})", href)
        if m:
            return m.group(1)
        mid = result.get("modelId") or result.get("id") or ""
        if mid:
            return mid.strip("/")

    raise RuntimeError(
        f"Could not extract new model ID from SPM create-model response: {result!r}\n"
        "The model may have been created — check SPM before retrying."
    )


def duplicate_model(
    auth,
    source_model: dict,
    source_info: dict,
    new_name: str,
) -> tuple:
    """Create a copy of source_model in SPM under the same parent folder.

    The copy is POSTed with new_name. The caller is responsible for applying
    any mutations (e.g. translations) to source_model before calling this.

    Args:
        auth         — authenticated SPM session (TokenManager)
        source_model — model JSON dict (already mutated if desired)
        source_info  — info dict with at least 'parent', 'namespace', 'type' keys
        new_name     — display name for the new model in SPM

    Returns:
        (new_model_id, new_info_dict)
        where new_info_dict contains 'name' and 'parent' and is ready for
        use with submit_model() if a subsequent PUT is needed.
    """
    parent     = source_info["parent"]
    namespace  = source_info.get("namespace", "http://b3mn.org/stencilset/bpmn2.0#")
    model_type = source_info.get("type", "Business Process Diagram (BPMN 2.0)")

    new_model_id = create_model(
        auth, new_name, parent, source_model,
        namespace=namespace,
        model_type=model_type,
    )
    new_info = {"name": new_name, "parent": parent}
    return new_model_id, new_info
