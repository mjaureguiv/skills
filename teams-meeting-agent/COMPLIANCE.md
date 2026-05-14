# Live Meeting Agent - Compliance & Security Documentation

This document outlines the compliance, security, and privacy considerations for the Live Meeting Agent skill.

## Overview

The Live Meeting Agent is designed to join Microsoft Teams and Zoom meetings, monitor chat messages, answer questions, and take structured meeting notes. This document ensures SAP compliance and addresses data privacy requirements.

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User                                     │
│          (Meeting Organizer/PM)                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│            Live Meeting Agent (Claude)                      │
│         skills/live-meeting-agent/                          │
└──┬──────────────────┬──────────────────┬───────────────────┘
   │                  │                  │
   ▼                  ▼                  ▼
┌──────────┐   ┌──────────┐      ┌──────────────┐
│ Microsoft│   │  Jira    │      │ Local Files  │
│  Teams   │   │  API     │      │ (~/.claude/  │
│  Graph   │   │          │      │  drafts/)    │
│  API     │   │          │      │              │
└──────────┘   └──────────┘      └──────────────┘
     │              │                    │
     ▼              ▼                    ▼
┌──────────────────────────────────────────┐
│     OAuth Tokens (~/.claude/tokens/)     │
│     - outlook-token.json                 │
│     - teams-token.json (future)          │
└──────────────────────────────────────────┘
```

---

## Permissions Matrix

### What the Agent Can Access

| Resource | Access Level | Purpose | Risk Level |
|----------|-------------|---------|------------|
| **Teams Meeting Chat** | Read | Monitor messages for questions and content | Medium |
| **Teams Meeting Chat** | Write | Send responses to participant questions | Medium |
| **Calendar Events** | Read | Identify meetings with Teams/Zoom URLs | Low |
| **Company Context Files** | Read | Load guidelines for response generation | Low |
| **Meeting Notes (Local)** | Read/Write | Store structured notes in drafts/ | Low |
| **Jira Tickets** | Write (with approval) | Create action item tickets | Medium |

### What the Agent CANNOT Access

| Resource | Restriction | Reason |
|----------|-------------|--------|
| **Audio/Video Streams** | ❌ No Access | Privacy, GDPR, complexity |
| **Meeting Recordings** | ❌ No Access | Privacy, storage, consent |
| **Screen Sharing Content** | ❌ No Access | Privacy, technical limitations |
| **Private Chats** | ❌ No Access | Only meeting-specific chat |
| **Attendee Contact Info** | ❌ No Access | Privacy |
| **Other Mail Folders** | ❌ No Access | Scope limitation |
| **OneDrive Files** | ❌ No Access | Scope limitation |

---

## Authentication & Authorization

### OAuth 2.0 Device Code Flow

**Microsoft Teams/Graph API**:
- Client ID: `14d82eec-204b-4c2f-b7e8-296a70dab67e` (Microsoft public client)
- Authorization: Device Code Flow (no client secrets)
- Token Storage: `~/.claude/tokens/outlook-token.json`
- Token Permissions: `chmod 600` (user-only access)

**Required Scopes**:
```
OnlineMeetings.ReadWrite  # Join and monitor meetings
Chat.ReadWrite            # Read/send chat messages
Calendar.Read             # Find meetings with URLs
User.Read                 # Basic user profile
```

**Zoom (Phase 2)**:
- OAuth 2.0 with Zoom app credentials
- Meeting SDK authentication
- Token storage: `~/.claude/tokens/zoom-token.json`

### Token Security

1. **Storage**:
   - Tokens stored locally in `~/.claude/tokens/`
   - File permissions: `600` (owner read/write only)
   - Not committed to git (in `.gitignore`)

2. **Expiry Management**:
   - Access tokens expire after 1 hour
   - Automatic refresh using refresh token
   - Graceful re-authentication on failure

3. **Secrets Management**:
   - No hardcoded credentials in code
   - No API keys stored in repository
   - Client ID is public (Microsoft standard)

---

## Data Privacy & GDPR Compliance

### Data Collection

| Data Type | Collected | Purpose | Retention |
|-----------|-----------|---------|-----------|
| **Chat Messages** | Yes | Answer questions, take notes | Duration of meeting + 24 hours (temp files) |
| **Participant Names** | Yes | Document attendees in notes | Permanent (in meeting notes) |
| **Timestamps** | Yes | Context for notes | Permanent (in meeting notes) |
| **Meeting Titles** | Yes | Identify meetings | Permanent (in meeting notes) |
| **Audio/Video** | No | N/A | N/A |
| **IP Addresses** | No | N/A | N/A |
| **Contact Details** | No | N/A | N/A |

### Data Processing

1. **Local Processing**: All AI processing happens locally via Claude API (Anthropic)
2. **No Third-Party Sharing**: Data not shared with services beyond Microsoft/Zoom APIs
3. **Temporary Storage**: Active meeting data in `temp/` folder, deleted after meeting
4. **Permanent Storage**: Meeting notes saved to `drafts/` (user-controlled)

### Data Subject Rights (GDPR)

| Right | How Exercised |
|-------|---------------|
| **Right to Access** | User can read all meeting notes in `drafts/` folder |
| **Right to Rectification** | User can edit meeting notes manually |
| **Right to Erasure** | User can delete meeting notes and temp files |
| **Right to Restriction** | User can disable agent or configure to not respond to questions |
| **Right to Data Portability** | Meeting notes in markdown (portable format) |
| **Right to Object** | User can stop agent at any time |

### Consent Management

**Required Before Agent Starts**:
1. Meeting organizer must explicitly start the agent
2. Meeting participants must be informed (organizer's responsibility)
3. Agent confirms consent before monitoring:

```
⚠️ Participant Consent Required

This agent will monitor meeting chat and respond to questions.
All participants should be informed that an AI agent is present.

Have meeting participants been notified? [Yes/No]
```

**Opt-Out**: Participants can request agent to be stopped via meeting chat or direct message to organizer.

---

## SAP-Specific Requirements

### Classification: Internal

- Meeting notes classified as **Internal** per `context/company-guidelines.md`
- Not to be shared publicly or with external parties without review
- Jira tickets created in internal SAP Jira instance

### Authentication

- Uses SAP SSO for Jira integration (via `tools/jira/`)
- Microsoft/Zoom OAuth for meeting platform access
- No separate authentication system

### Data Residency

- All data stored locally on user's SAP-managed device
- OAuth tokens cached locally (not in cloud)
- Meeting notes in local `drafts/` folder (user-controlled)
- Optional: Upload to SharePoint (SAP-approved cloud storage)

### Audit Trail

Logged actions:
- Meeting monitoring start/stop
- Questions answered with timestamp
- Jira tickets created (with approval confirmation)
- Authentication events

Log location: `skills/live-meeting-agent/temp/audit-log.json`

---

## Risk Assessment

### High Risk Scenarios

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Confidential info leaked** | Low | High | No audio recording; chat-only; explicit consent required |
| **Unauthorized access to meetings** | Low | High | OAuth authentication; user-initiated only |
| **Incorrect AI responses** | Medium | Medium | Confidence threshold; user can disable auto-response |
| **Data breach (stolen tokens)** | Low | High | Local storage with restricted permissions; automatic token expiry |

### Medium Risk Scenarios

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Meeting notes contain PII** | Medium | Medium | User review before sharing; local storage only |
| **Accidental Jira ticket creation** | Low | Low | Explicit approval required before creating tickets |
| **Agent responds inappropriately** | Medium | Low | Confidence threshold; human oversight; can be disabled |

### Low Risk Scenarios

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **API rate limiting** | Medium | Low | Exponential backoff; graceful degradation |
| **Token refresh failure** | Low | Low | Clear error message; re-authentication flow |
| **Temp file not cleaned up** | Low | Low | Automatic cleanup; 24-hour retention max |

---

## Security Best Practices

### For Users

1. **Review before sharing**: Always review meeting notes before sharing widely
2. **Inform participants**: Ensure all meeting participants know the agent is present
3. **Disable when sensitive**: Don't use agent for confidential/restricted discussions
4. **Protect tokens**: Don't share your `~/.claude/tokens/` folder
5. **Approve Jira tickets**: Review all proposed tickets before approving creation

### For Developers

1. **No hardcoded secrets**: All credentials via OAuth or environment variables
2. **Validate inputs**: Sanitize all meeting chat messages before processing
3. **Rate limiting**: Implement exponential backoff for API calls
4. **Error handling**: Graceful degradation on API failures
5. **Logging**: Log security-relevant events without exposing sensitive data

---

## Compliance Checklist

### Before Deployment

- [x] OAuth authentication implemented (no stored secrets)
- [x] Participant consent mechanism in place
- [x] Data retention policy documented
- [x] GDPR rights supported (access, erasure, etc.)
- [ ] Security review completed by SAP InfoSec (pending)
- [x] Privacy impact assessment documented (this file)
- [x] Audit logging implemented
- [x] Token storage secured (chmod 600)

### Ongoing

- [ ] Regular security audits (quarterly)
- [ ] User feedback on privacy concerns (monthly review)
- [ ] Token expiry and refresh monitoring
- [ ] Compliance with updated SAP policies

---

## Data Retention Policy

| Data Type | Retention Period | Deletion Method |
|-----------|------------------|-----------------|
| **Active meeting data** (temp files) | Duration of meeting | Automatic deletion after meeting ends |
| **Meeting notes** (drafts/) | Indefinite (user-controlled) | User manual deletion |
| **OAuth tokens** | Until expiry or user logout | Automatic expiry; manual deletion on logout |
| **Audit logs** | 90 days | Automatic rotation |
| **Jira tickets** | Per Jira retention policy | Follow Jira admin settings |

---

## Incident Response

### Data Breach

1. **Immediate**:
   - Revoke OAuth tokens: Delete `~/.claude/tokens/`
   - Stop all active agents
   - Notify SAP Security team

2. **Investigation**:
   - Review audit logs for unauthorized access
   - Identify scope of breach (which meetings)
   - Determine if PII was exposed

3. **Remediation**:
   - Reset OAuth credentials
   - Notify affected meeting participants
   - Update security measures

### Unauthorized Access

1. Check who initiated agent (audit log)
2. Review meeting notes for sensitive data
3. Revoke access if unauthorized
4. Report to manager and InfoSec

### Privacy Violation

1. Stop agent immediately
2. Delete affected meeting notes
3. Notify meeting participants
4. Document incident in `troubleshooting/CLAUDE.md`

---

## Contact

For security or privacy concerns:

- **SAP InfoSec**: [Contact via SAP internal portal]
- **Data Protection Officer**: [Contact via SAP internal portal]
- **PM Agent Support**: [GitHub Issues](https://github.tools.sap/signavio-pm-agent/Signavio_PM_Agent/issues)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-25 | Initial compliance documentation |

---

## Appendix: API Endpoints Used

### Microsoft Graph API

| Endpoint | Purpose | Data Accessed |
|----------|---------|---------------|
| `GET /me/events` | List calendar meetings | Meeting titles, times, URLs |
| `GET /me/onlineMeetings` | List Teams meetings | Meeting details, chat IDs |
| `GET /chats/{id}/messages` | Read meeting chat | Chat messages (text only) |
| `POST /chats/{id}/messages` | Send chat message | N/A (write only) |

### Jira API (via tools/jira)

| Endpoint | Purpose | Data Accessed |
|----------|---------|---------------|
| `POST /rest/api/2/issue` | Create ticket | N/A (write only) |

---

*This document is subject to updates as compliance requirements evolve.*
