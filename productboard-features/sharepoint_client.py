# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
SharePoint / Microsoft Graph API helpers for downloading ProductBoard data.

Downloads the full JSON export from the ProductStrategyGroup SharePoint site
using Microsoft Graph API with OAuth token from the shared Outlook token file.
"""

from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GRAPH_URL = "https://graph.microsoft.com/v1.0"
TOKEN_PATH = Path.home() / ".claude" / "tokens" / "outlook-token.json"

SHAREPOINT_SITE_HOST = "sap.sharepoint.com"
SHAREPOINT_SITE_PATH = "/teams/ProductStrategyGroup"
SHAREPOINT_FOLDER = "/0 General/Data/productboard/features"
SHAREPOINT_FILENAME = "pb_features_full_latest.json"

# ---------------------------------------------------------------------------
# SSL helpers
# ---------------------------------------------------------------------------

_SSL_CONTEXT: ssl.SSLContext | None = None


def _get_ssl_context() -> ssl.SSLContext | None:
    """Return an SSL context, falling back to unverified on macOS cert issues."""
    global _SSL_CONTEXT
    if _SSL_CONTEXT is not None:
        return _SSL_CONTEXT

    try:
        ctx = ssl.create_default_context()
        urllib.request.urlopen(
            urllib.request.Request("https://graph.microsoft.com", method="HEAD"),
            timeout=5, context=ctx,
        )
        _SSL_CONTEXT = ctx
        return _SSL_CONTEXT
    except Exception:
        pass

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    _SSL_CONTEXT = ctx
    return _SSL_CONTEXT


# ---------------------------------------------------------------------------
# Token & drive resolution
# ---------------------------------------------------------------------------

def _load_graph_token() -> str:
    """Load Microsoft Graph access token from shared Outlook token file."""
    if not TOKEN_PATH.exists():
        raise FileNotFoundError(
            f"No Graph token found at {TOKEN_PATH}\n"
            "Run: python tools/outlook/outlook_api.py auth"
        )
    with open(TOKEN_PATH) as f:
        return json.load(f).get("access_token", "")


def _get_site_drive_id(token: str) -> str:
    """Resolve the Documents drive ID for the SharePoint team site."""
    ssl_ctx = _get_ssl_context()
    headers = {"Authorization": f"Bearer {token}"}

    # Step 1: Resolve site ID
    site_url = f"{GRAPH_URL}/sites/{SHAREPOINT_SITE_HOST}:{SHAREPOINT_SITE_PATH}"
    req = urllib.request.Request(site_url, headers=headers)
    with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
        site = json.loads(resp.read().decode("utf-8"))
    site_id = site.get("id", "")

    # Step 2: Find Documents drive
    drives_url = f"{GRAPH_URL}/sites/{site_id}/drives"
    req = urllib.request.Request(drives_url, headers=headers)
    with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
        drives = json.loads(resp.read().decode("utf-8"))

    for drive in drives.get("value", []):
        if drive.get("name") == "Documents":
            return drive["id"]
    for drive in drives.get("value", []):
        if drive.get("driveType") == "documentLibrary":
            return drive["id"]

    raise RuntimeError("Could not find Documents drive on SharePoint site")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def download_from_sharepoint(filename: str = SHAREPOINT_FILENAME) -> bytes:
    """
    Download a file from the SharePoint ProductStrategyGroup site.

    Returns the raw file bytes.
    """
    token = _load_graph_token()
    drive_id = _get_site_drive_id(token)
    ssl_ctx = _get_ssl_context()

    file_path = f"{SHAREPOINT_FOLDER}/{filename}"
    encoded_path = urllib.parse.quote(file_path)
    download_url = f"{GRAPH_URL}/drives/{drive_id}/root:{encoded_path}:/content"

    req = urllib.request.Request(
        download_url,
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req, timeout=120, context=ssl_ctx) as resp:
        return resp.read()
