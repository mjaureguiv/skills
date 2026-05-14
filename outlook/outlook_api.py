"""
Direct Microsoft Graph API client for Outlook calendar/mail.
Uses OAuth2 device code flow for authentication - no MCP server required.

Features:
- Calendar: View events, schedule meetings, find available times
- Mail: Read inbox, create drafts, reply to messages
- Authentication: Device code flow with token caching

Usage:
    from outlook_api import get_calendar_events, create_draft, create_meeting
"""

import json
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
import urllib.request
import urllib.parse

# Configuration
CLIENT_ID = "14d82eec-204b-4c2f-b7e8-296a70dab67e"  # Microsoft public client
TOKEN_PATH = Path.home() / ".claude" / "tokens" / "outlook-token.json"
TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
GRAPH_URL = "https://graph.microsoft.com/v1.0"
DEVICE_CODE_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/devicecode"

SCOPES = [
    "Calendars.ReadWrite",
    "Mail.Read",
    "Mail.ReadWrite",
    "Tasks.Read",
    "Files.Read",
    "Contacts.Read",
    "User.Read",
]


# ============== Authentication ==============

def load_tokens():
    """Load tokens from cache file."""
    if not TOKEN_PATH.exists():
        return None
    with open(TOKEN_PATH) as f:
        return json.load(f)


def save_tokens(token_data):
    """Save tokens to cache file."""
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_PATH, "w") as f:
        json.dump(token_data, f, indent=2)


def refresh_token(refresh_token_str, scopes=None):
    """Refresh access token using refresh token."""
    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token_str,
        "scope": scopes or " ".join(SCOPES),
    }).encode("utf-8")
    
    req = urllib.request.Request(
        TOKEN_URL,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    
    if "access_token" in result:
        save_tokens({
            "access_token": result["access_token"],
            "refresh_token": result.get("refresh_token", refresh_token_str),
            "expires_in": result.get("expires_in", 3600),
            "scope": result.get("scope", ""),
            "token_type": result.get("token_type", "Bearer"),
        })
        return result["access_token"]
    return None


def device_code_auth():
    """Authenticate using device code flow (opens browser)."""
    print("Starting device code authentication...")
    
    # Step 1: Get device code
    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "scope": " ".join(SCOPES),
    }).encode("utf-8")
    
    req = urllib.request.Request(
        DEVICE_CODE_URL,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        device_response = json.loads(resp.read().decode("utf-8"))
    
    print(f"\n{device_response['message']}\n")
    
    # Step 2: Poll for token
    interval = device_response.get("interval", 5)
    expires_in = device_response.get("expires_in", 900)
    device_code = device_response["device_code"]
    
    start_time = time.time()
    while time.time() - start_time < expires_in:
        time.sleep(interval)
        
        poll_data = urllib.parse.urlencode({
            "client_id": CLIENT_ID,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "device_code": device_code,
        }).encode("utf-8")
        
        poll_req = urllib.request.Request(
            TOKEN_URL,
            data=poll_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        
        try:
            with urllib.request.urlopen(poll_req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                if "access_token" in result:
                    save_tokens({
                        "access_token": result["access_token"],
                        "refresh_token": result.get("refresh_token"),
                        "expires_in": result.get("expires_in", 3600),
                        "scope": result.get("scope", ""),
                        "token_type": result.get("token_type", "Bearer"),
                        "saved_at": time.time(),
                    })
                    print("Authentication successful!")
                    return result["access_token"]
        except urllib.error.HTTPError as e:
            error_body = json.loads(e.read().decode("utf-8"))
            error_code = error_body.get("error", "")
            if error_code == "authorization_pending":
                print(".", end="", flush=True)
                continue
            elif error_code == "slow_down":
                interval += 5
                continue
            else:
                raise Exception(f"Auth failed: {error_body}")
    
    raise Exception("Device code expired without authentication")


def get_access_token():
    """Get a valid access token, refreshing or re-authenticating if needed."""
    tokens = load_tokens()
    
    if tokens and tokens.get("access_token"):
        # Check if we have a saved timestamp to determine if token is still valid
        saved_at = tokens.get("saved_at")
        expires_in = tokens.get("expires_in", 3600)
        
        if saved_at:
            # Check if token has expired
            elapsed = time.time() - saved_at
            if elapsed < expires_in - 300:  # 5 minute buffer
                # Token is still valid, use it
                return tokens["access_token"]
        else:
            # No timestamp saved - assume token is valid for now
            # Add timestamp for future reference
            tokens["saved_at"] = time.time()
            save_tokens(tokens)
            return tokens["access_token"]
        
        # Token expired, try to refresh
        if tokens.get("refresh_token"):
            try:
                scopes = tokens.get("scope", "")
                token = refresh_token(tokens["refresh_token"], scopes)
                if token:
                    return token
            except Exception as e:
                print(f"Token refresh failed: {e}", file=sys.stderr)
    
    # Need fresh authentication
    return device_code_auth()


def graph_request(endpoint, method="GET", params=None, body=None):
    """Make a request to Microsoft Graph API."""
    token = get_access_token()
    
    url = f"{GRAPH_URL}{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            response_body = resp.read().decode("utf-8")
            if response_body:
                return json.loads(response_body)
            return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Graph API error {e.code}: {error_body}", file=sys.stderr)
        raise


# ============== Calendar Functions ==============

def get_calendar_events(days=7, max_events=50):
    """Get calendar events for the next N days."""
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=days)
    
    start_str = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_str = end.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    params = {
        "startDateTime": start_str,
        "endDateTime": end_str,
        "$orderby": "start/dateTime",
        "$top": max_events,
        "$select": "subject,start,end,location,organizer,attendees,isOnlineMeeting,onlineMeetingUrl,bodyPreview",
    }
    
    result = graph_request("/me/calendarview", params=params)
    return result.get("value", [])


def format_event(event):
    """Format a calendar event for display."""
    start = event.get("start", {})
    end = event.get("end", {})
    subject = event.get("subject", "No subject")
    location = event.get("location", {}).get("displayName", "")
    organizer = event.get("organizer", {}).get("emailAddress", {}).get("name", "")
    teams_url = event.get("onlineMeetingUrl", "")
    
    start_dt = start.get("dateTime", "")[:16].replace("T", " ") if start.get("dateTime") else "All day"
    end_dt = end.get("dateTime", "")[:16].replace("T", " ") if end.get("dateTime") else ""
    
    lines = [f"📅 {subject}"]
    lines.append(f"   🕐 {start_dt} - {end_dt[-5:] if end_dt else ''}")
    if location:
        lines.append(f"   📍 {location}")
    if organizer:
        lines.append(f"   👤 {organizer}")
    if teams_url:
        lines.append(f"   🔗 Teams meeting")
    
    return "\n".join(lines)


def list_meetings(days=7):
    """List upcoming meetings in a readable format."""
    print(f"\n📆 Your meetings for the next {days} days:\n")
    print("=" * 60)
    
    events = get_calendar_events(days=days)
    
    if not events:
        print("No meetings found.")
        return events
    
    current_date = None
    for event in events:
        start = event.get("start", {}).get("dateTime", "")[:10]
        if start != current_date:
            current_date = start
            print(f"\n--- {start} ---\n")
        
        print(format_event(event))
        print()
    
    return events


def find_meeting_times(attendee_emails, duration_minutes=30, days_ahead=7):
    """Find available meeting times using Microsoft Graph findMeetingTimes API."""
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=days_ahead)
    
    body = {
        "attendees": [
            {"emailAddress": {"address": email}, "type": "required"}
            for email in attendee_emails
        ],
        "timeConstraint": {
            "activityDomain": "work",
            "timeSlots": [
                {
                    "start": {"dateTime": now.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": "UTC"},
                    "end": {"dateTime": end.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": "UTC"}
                }
            ]
        },
        "meetingDuration": f"PT{duration_minutes}M",
        "returnSuggestionReasons": True,
        "minimumAttendeePercentage": 100
    }
    
    result = graph_request("/me/findMeetingTimes", method="POST", body=body)
    return result.get("meetingTimeSuggestions", [])


def create_meeting(subject, start_datetime, end_datetime, attendee_emails, body_text="", is_online=True):
    """Create a calendar meeting with optional Teams link.
    
    Args:
        subject: Meeting title
        start_datetime: Start time as "YYYY-MM-DDTHH:MM:SS"
        end_datetime: End time as "YYYY-MM-DDTHH:MM:SS"
        attendee_emails: List of attendee email addresses
        body_text: Optional meeting body/description
        is_online: If True, creates Teams meeting link
    
    Returns:
        Created event object
    """
    event = {
        "subject": subject,
        "body": {
            "contentType": "Text",
            "content": body_text
        },
        "start": {
            "dateTime": start_datetime,
            "timeZone": "Europe/Berlin"
        },
        "end": {
            "dateTime": end_datetime,
            "timeZone": "Europe/Berlin"
        },
        "attendees": [
            {
                "emailAddress": {"address": email},
                "type": "required"
            }
            for email in attendee_emails
        ],
        "isOnlineMeeting": is_online,
        "onlineMeetingProvider": "teamsForBusiness" if is_online else None
    }
    
    result = graph_request("/me/events", method="POST", body=event)
    return result


# ============== Mail Functions ==============

def get_inbox(max_messages=25, filter_newsletters=True):
    """Get recent inbox messages."""
    params = {
        "$top": max_messages,
        "$orderby": "receivedDateTime desc",
        "$select": "subject,from,receivedDateTime,bodyPreview,isRead,importance",
    }
    
    result = graph_request("/me/messages", params=params)
    messages = result.get("value", [])
    
    if filter_newsletters:
        newsletter_indicators = ["unsubscribe", "newsletter", "noreply", "no-reply", "notifications@"]
        messages = [m for m in messages if not any(
            ind in m.get("from", {}).get("emailAddress", {}).get("address", "").lower() or
            ind in m.get("bodyPreview", "").lower()
            for ind in newsletter_indicators
        )]
    
    return messages


def search_messages(query, max_messages=20):
    """Search messages using Microsoft Graph $search.
    
    Args:
        query: Search query (e.g., '"subject text"' or 'from:email@domain.com')
        max_messages: Maximum results to return
    
    Returns:
        List of matching messages
    """
    params = {
        "$search": query,
        "$top": max_messages,
        "$select": "id,subject,from,receivedDateTime,bodyPreview"
    }
    result = graph_request("/me/messages", params=params)
    return result.get("value", [])


def format_message(msg):
    """Format an email message for display."""
    from_addr = msg.get("from", {}).get("emailAddress", {})
    sender = from_addr.get("name", from_addr.get("address", "Unknown"))
    subject = msg.get("subject", "No subject")
    received = msg.get("receivedDateTime", "")[:16].replace("T", " ")
    preview = msg.get("bodyPreview", "")[:100]
    is_read = "✓" if msg.get("isRead") else "•"
    importance = "❗" if msg.get("importance") == "high" else ""
    
    return f"{is_read}{importance} [{received}] {sender}\n   {subject}\n   {preview}..."


def list_inbox(max_messages=15):
    """List recent inbox messages."""
    print(f"\n📧 Recent inbox messages:\n")
    print("=" * 60)
    
    messages = get_inbox(max_messages=max_messages)
    
    if not messages:
        print("No messages found.")
        return messages
    
    for msg in messages:
        print(format_message(msg))
        print()
    
    return messages


# ============== Draft Functions ==============

def create_draft(to_email, subject, body):
    """Create a draft email.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body text
    
    Returns:
        Created draft message object
    """
    draft = {
        "subject": subject,
        "body": {
            "contentType": "Text",
            "content": body
        },
        "toRecipients": [
            {
                "emailAddress": {
                    "address": to_email
                }
            }
        ]
    }
    
    result = graph_request("/me/messages", method="POST", body=draft)
    return result


def create_reply_draft(message_id, body, reply_all=False):
    """Create a reply draft to a specific message.
    
    Args:
        message_id: ID of the message to reply to
        body: Reply body text
        reply_all: If True, reply to all recipients
    
    Returns:
        Created draft message object
    """
    endpoint = f"/me/messages/{message_id}/createReply" if not reply_all else f"/me/messages/{message_id}/createReplyAll"
    
    result = graph_request(endpoint, method="POST", body={})
    
    draft_id = result.get("id")
    if draft_id and body:
        update_body = {
            "body": {
                "contentType": "Text",
                "content": body
            }
        }
        result = graph_request(f"/me/messages/{draft_id}", method="PATCH", body=update_body)
    
    return result


# ============== Mail Folder Functions ==============

def get_mail_folders(parent_folder_id=None):
    """Get mail folders from the mailbox.
    
    Args:
        parent_folder_id: Optional parent folder ID. If None, gets top-level folders.
    
    Returns:
        List of folder objects with id, displayName, childFolderCount, etc.
    """
    if parent_folder_id:
        endpoint = f"/me/mailFolders/{parent_folder_id}/childFolders"
    else:
        endpoint = "/me/mailFolders"
    
    params = {
        "$top": 100,
        "$select": "id,displayName,parentFolderId,childFolderCount,unreadItemCount,totalItemCount"
    }
    
    result = graph_request(endpoint, params=params)
    return result.get("value", [])


def create_mail_folder(display_name, parent_folder_id=None):
    """Create a new mail folder.
    
    Args:
        display_name: Name for the new folder
        parent_folder_id: Optional parent folder ID. If None, creates in root (Inbox level).
    
    Returns:
        Created folder object with id, displayName, etc.
    """
    if parent_folder_id:
        endpoint = f"/me/mailFolders/{parent_folder_id}/childFolders"
    else:
        endpoint = "/me/mailFolders"
    
    body = {"displayName": display_name}
    
    try:
        result = graph_request(endpoint, method="POST", body=body)
        print(f"✓ Created folder: {display_name} (ID: {result.get('id', 'N/A')[:20]}...)")
        return result
    except urllib.error.HTTPError as e:
        if e.code == 409:
            print(f"⚠ Folder already exists: {display_name}")
            return None
        raise


def create_mail_folders(folder_names, parent_folder_id=None):
    """Create multiple mail folders at once.
    
    Args:
        folder_names: List of folder names to create
        parent_folder_id: Optional parent folder ID for all folders
    
    Returns:
        List of created folder objects (None for folders that already exist)
    """
    results = []
    for name in folder_names:
        result = create_mail_folder(name, parent_folder_id)
        results.append(result)
    return results


def delete_mail_folder(folder_id):
    """Delete a mail folder by ID.
    
    Args:
        folder_id: The ID of the folder to delete
    
    Returns:
        None on success
    """
    graph_request(f"/me/mailFolders/{folder_id}", method="DELETE")
    print(f"✓ Deleted folder: {folder_id[:20]}...")
    return None


def rename_mail_folder(folder_id, new_display_name):
    """Rename a mail folder.
    
    Args:
        folder_id: The ID of the folder to rename
        new_display_name: The new name for the folder
    
    Returns:
        Updated folder object
    """
    body = {"displayName": new_display_name}
    result = graph_request(f"/me/mailFolders/{folder_id}", method="PATCH", body=body)
    print(f"✓ Renamed folder to: {new_display_name}")
    return result


def move_message_to_folder(message_id, destination_folder_id):
    """Move a message to a specific folder.
    
    Args:
        message_id: The ID of the message to move
        destination_folder_id: The ID of the destination folder
    
    Returns:
        Moved message object
    """
    body = {"destinationId": destination_folder_id}
    result = graph_request(f"/me/messages/{message_id}/move", method="POST", body=body)
    return result


def list_mail_folders():
    """List all mail folders in a readable format."""
    print("\n📁 Your mail folders:\n")
    print("=" * 60)
    
    folders = get_mail_folders()
    
    if not folders:
        print("No folders found.")
        return folders
    
    for folder in folders:
        name = folder.get("displayName", "Unknown")
        total = folder.get("totalItemCount", 0)
        unread = folder.get("unreadItemCount", 0)
        children = folder.get("childFolderCount", 0)
        
        unread_indicator = f" ({unread} unread)" if unread > 0 else ""
        children_indicator = f" [+{children} subfolders]" if children > 0 else ""
        
        print(f"  📂 {name}: {total} items{unread_indicator}{children_indicator}")
    
    print()
    return folders


# ============== Inbox Rules Functions ==============

def get_inbox_rules():
    """Get all inbox rules.
    
    Returns:
        List of rule objects with id, displayName, sequence, isEnabled, conditions, actions, exceptions
    """
    result = graph_request("/me/mailFolders/inbox/messageRules")
    return result.get("value", [])


def get_inbox_rule(rule_id):
    """Get a specific inbox rule by ID.
    
    Args:
        rule_id: The ID of the rule to retrieve
    
    Returns:
        Rule object with full details
    """
    return graph_request(f"/me/mailFolders/inbox/messageRules/{rule_id}")


def create_inbox_rule(display_name, conditions, actions, exceptions=None, is_enabled=True, sequence=None):
    """Create a new inbox rule.
    
    Args:
        display_name: Name of the rule
        conditions: Dict of conditions (e.g., {"fromAddresses": [{"emailAddress": {"address": "x@y.com"}}]})
        actions: Dict of actions (e.g., {"moveToFolder": "folder_id", "stopProcessingRules": True})
        exceptions: Optional dict of exceptions (same structure as conditions)
        is_enabled: Whether the rule is enabled (default True)
        sequence: Optional sequence number for rule ordering
    
    Returns:
        Created rule object
    """
    body = {
        "displayName": display_name,
        "isEnabled": is_enabled,
        "conditions": conditions,
        "actions": actions,
    }
    
    if exceptions:
        body["exceptions"] = exceptions
    
    if sequence is not None:
        body["sequence"] = sequence
    
    result = graph_request("/me/mailFolders/inbox/messageRules", method="POST", body=body)
    print(f"✓ Created rule: {display_name}")
    return result


def update_inbox_rule(rule_id, display_name=None, conditions=None, actions=None, exceptions=None, is_enabled=None):
    """Update an existing inbox rule.
    
    Args:
        rule_id: The ID of the rule to update
        display_name: New name for the rule (optional)
        conditions: New conditions (optional)
        actions: New actions (optional)
        exceptions: New exceptions (optional, set to {} to clear exceptions)
        is_enabled: Enable/disable the rule (optional)
    
    Returns:
        Updated rule object
    """
    body = {}
    
    if display_name is not None:
        body["displayName"] = display_name
    if conditions is not None:
        body["conditions"] = conditions
    if actions is not None:
        body["actions"] = actions
    if exceptions is not None:
        body["exceptions"] = exceptions
    if is_enabled is not None:
        body["isEnabled"] = is_enabled
    
    result = graph_request(f"/me/mailFolders/inbox/messageRules/{rule_id}", method="PATCH", body=body)
    print(f"✓ Updated rule: {rule_id[:20]}...")
    return result


def delete_inbox_rule(rule_id):
    """Delete an inbox rule.
    
    Args:
        rule_id: The ID of the rule to delete
    
    Returns:
        None on success
    """
    graph_request(f"/me/mailFolders/inbox/messageRules/{rule_id}", method="DELETE")
    print(f"✓ Deleted rule: {rule_id[:20]}...")
    return None


def list_inbox_rules():
    """List all inbox rules in a readable format."""
    print("\n📋 Your inbox rules:\n")
    print("=" * 60)
    
    rules = get_inbox_rules()
    
    if not rules:
        print("No rules found.")
        return rules
    
    for rule in rules:
        name = rule.get("displayName", "Unknown")
        enabled = "✓" if rule.get("isEnabled", False) else "✗"
        sequence = rule.get("sequence", "?")
        rule_id = rule.get("id", "")
        
        conditions = rule.get("conditions", {})
        actions = rule.get("actions", {})
        exceptions = rule.get("exceptions", {})
        
        # Format conditions summary
        cond_parts = []
        if conditions.get("fromAddresses"):
            addrs = [a.get("emailAddress", {}).get("address", "") for a in conditions["fromAddresses"]]
            cond_parts.append(f"from: {', '.join(addrs)}")
        if conditions.get("senderContains"):
            cond_parts.append(f"sender contains: {conditions['senderContains']}")
        if conditions.get("subjectContains"):
            cond_parts.append(f"subject contains: {conditions['subjectContains']}")
        if conditions.get("bodyContains"):
            cond_parts.append(f"body contains: {conditions['bodyContains']}")
        
        # Format actions summary
        action_parts = []
        if actions.get("moveToFolder"):
            action_parts.append(f"move to folder")
        if actions.get("delete"):
            action_parts.append("delete")
        if actions.get("markAsRead"):
            action_parts.append("mark as read")
        
        # Format exceptions summary
        exc_parts = []
        if exceptions.get("bodyContains"):
            exc_parts.append(f"body contains: {exceptions['bodyContains']}")
        if exceptions.get("subjectContains"):
            exc_parts.append(f"subject contains: {exceptions['subjectContains']}")
        
        print(f"\n  [{enabled}] {name} (seq: {sequence})")
        print(f"      ID: {rule_id}")
        if cond_parts:
            print(f"      Conditions: {'; '.join(cond_parts)}")
        if action_parts:
            print(f"      Actions: {'; '.join(action_parts)}")
        if exc_parts:
            print(f"      Exceptions: {'; '.join(exc_parts)}")
    
    print()
    return rules


# ============== CLI ==============

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Outlook API direct access")
    parser.add_argument("command", choices=["meetings", "inbox", "folders", "create-folder", "auth"], 
                       help="Command to run")
    parser.add_argument("--days", type=int, default=7, help="Days to look ahead for meetings")
    parser.add_argument("--count", type=int, default=15, help="Max items to show")
    parser.add_argument("--name", type=str, help="Folder name for create-folder command")
    parser.add_argument("--names", type=str, help="Comma-separated folder names for batch creation")
    
    args = parser.parse_args()
    
    if args.command == "auth":
        device_code_auth()
    elif args.command == "meetings":
        list_meetings(days=args.days)
    elif args.command == "inbox":
        list_inbox(max_messages=args.count)
    elif args.command == "folders":
        list_mail_folders()
    elif args.command == "create-folder":
        if args.names:
            folder_list = [n.strip() for n in args.names.split(",")]
            create_mail_folders(folder_list)
        elif args.name:
            create_mail_folder(args.name)
        else:
            print("Error: --name or --names required for create-folder command")
