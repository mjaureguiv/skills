"""SPM authentication wrapper.

Uses the spm_mcp TokenManager to authenticate with Signavio Process Manager.
The MCP server session can expire between Claude Code sessions; this module
accesses the API directly so auth is always refreshed.
"""
import sys
from .constants import SPM_SRC

sys.path.insert(0, SPM_SRC)
from spm_mcp.auth import TokenManager, SPMConfig  # noqa: E402


def get_auth():
    """Authenticate with SPM and return the TokenManager instance.

    The returned object exposes:
      auth.session      — requests.Session with valid cookies
      auth.api_base     — base URL for SPM REST calls
    """
    config = SPMConfig()
    auth = TokenManager(config)
    auth.ensure_authenticated()
    return auth
