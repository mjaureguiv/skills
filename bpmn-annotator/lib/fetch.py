"""Fetch and submit BPMN models from/to Signavio Process Manager."""
import json
import re
import urllib.parse


def extract_model_id(url_or_id: str) -> str:
    """Extract the 32-char hex model ID from a Signavio URL or return the ID as-is."""
    match = re.search(r'/model/([a-f0-9]{32})', url_or_id)
    return match.group(1) if match else url_or_id.strip()


def fetch_model(auth, model_id: str):
    """Fetch model JSON and info dict from SPM.

    Returns:
        (model_dict, info_dict)
    Raises:
        requests.HTTPError on non-2xx responses.
    """
    resp = auth.session.get(f"{auth.api_base}/model/{model_id}/info")
    resp.raise_for_status()
    info = resp.json()

    resp2 = auth.session.get(f"{auth.api_base}{info['revision']}/json")
    resp2.raise_for_status()
    return resp2.json(), info


def submit_model(auth, model_id: str, model: dict, info: dict,
                 comment: str = "BPMN Annotator"):
    """Submit an updated model to SPM.

    Uses a direct session.put() with 120s timeout to handle large payloads.
    The standard SPMClient.put() has a 30s timeout that fires on big models.

    Returns:
        (revision, updated_timestamp) or (None, None) on unexpected response.
    """
    json_xml = json.dumps(model, separators=(',', ':'))
    encoded = urllib.parse.urlencode({
        "json_xml": json_xml,
        "name":     info["name"],
        "comment":  comment,
        "parent":   info["parent"],
    })
    response = auth.session.put(
        f"{auth.api_base}/model/{model_id}",
        data=encoded,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=120,
    )
    result = response.json()
    # SPM PUT returns a list of {rel, rep} objects
    if isinstance(result, list):
        for item in result:
            if isinstance(item, dict) and item.get("rel") == "info":
                r = item.get("rep", {})
                return r.get("rev"), r.get("updated")
    return None, None
