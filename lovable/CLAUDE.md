> ⚠️ **This file contains instructions for GitHub Copilot (Claude), not for humans.**
> If you're a human, see [README.md](README.md) for the main documentation.

---

# Lovable Prompt Generation - AI Instructions

## Purpose

Transform PM-style feature descriptions into detailed Lovable AI prompts that can generate production-ready implementations.

**Lovable** is an AI coding assistant that needs structured, technical prompts. This skill converts product management language into developer/AI-friendly implementation instructions with complete technical specifications.

## Input Methods

### Method 1: Jira Issue Key (Preferred)

When user provides a Jira issue key (e.g., "PROJ-123", "SIGNAVIO-456"):

1. **Use Jira MCP tool** to fetch the issue:
   ```
   get_issue(issueKey)
   ```

2. **Extract information:**
   - **Summary**: Feature title
   - **Description**: Feature context and requirements
   - **Issue Type**: Story, Epic, Feature, Bug, Task
   - **Acceptance Criteria**: Look in description (often formatted as bullet points or numbered lists)
   - **Comments**: Additional context, technical notes, clarifications
   - **Custom fields**: Any technical specifications, UI mockups, data requirements

3. **Handle authentication errors:**
   - If Jira call fails with auth error: "Your SAP session needs refresh" → trigger sap-auth
   - If issue not found: Ask user to verify key or provide text instead

### Method 2: Pasted Text (Fallback)

When user pastes feature description directly:

1. **Parse the text** for key elements:
   - Feature title (usually first line or explicitly labeled)
   - Feature description/purpose
   - User persona (who is this for?)
   - User goals (what do they want to accomplish?)
   - Acceptance criteria (look for bullet points, "AC:", "Acceptance Criteria:")
   - Technical requirements (frameworks, APIs, constraints)
   - UI/UX requirements (screens, buttons, flows)

2. **Fill gaps with clarifying questions** if critical information is missing

### Auto-detection

```
User input contains pattern like "PROJ-123" or "PROJECT-456"
  → Method 1: Fetch from Jira

User input is longer text without issue key pattern
  → Method 2: Parse pasted text
```

## Transformation Logic

### Step 1: Extract Information

**From Jira or pasted text, identify:**

1. **Core Feature Info:**
   - Title
   - Purpose/value proposition
   - User persona (who)
   - User goal (what)
   - Business value (why)

2. **Functional Requirements:**
   - What the feature should do
   - User interactions
   - System behaviors
   - Business logic rules

3. **Technical Requirements:**
   - Data models and entities
   - API endpoints needed
   - UI components and layouts
   - Integrations with other systems
   - Performance requirements
   - Security requirements

4. **Acceptance Criteria:**
   - Testable conditions for "done"
   - Edge cases to handle
   - Error scenarios

### Step 2: Generate Detailed Lovable Prompt

Use this comprehensive template:

```markdown
# Feature: [Title]

## User Story

As a [persona - be specific: "Product Manager", "End User", "System Admin"],
I want to [specific goal with action verb],
So that [clear business value and outcome].

## Context & Background

[2-3 paragraphs explaining:]
- Why this feature is needed (business context)
- Current state vs. desired state
- How this fits into the larger product
- Key problems this solves

## User Flow

[Step-by-step interaction from user's perspective:]

1. User navigates to [specific location]
2. User clicks [specific button/link]
3. System displays [specific UI element]
4. User enters [specific data]
5. System validates [specific rules]
6. System responds with [specific feedback]
7. [Continue until flow is complete]

**Alternative flows:**
- If [condition], then [alternative path]
- If [error], then [error handling]

## UI/UX Requirements

### Screen Layout

[Describe the visual structure:]
- Header: [Elements and their positions]
- Main content area: [Layout description]
- Sidebar: [If applicable]
- Footer: [Elements]

### Components Needed

1. **[Component Name]** (e.g., "Export Button")
   - Type: Button
   - Label: "Export to Excel"
   - Position: Dashboard header, top-right
   - Style: Primary action button
   - Icon: Download icon
   - State: Disabled when no data

2. **[Component Name]** (e.g., "Data Table")
   - Type: Data grid
   - Columns: [List columns]
   - Features: Sortable, filterable, paginated
   - Selection: Multi-select with checkboxes
   - Empty state: "No data to display"

3. [Continue for all UI components...]

### Interaction Patterns

- Hover: [What happens on hover]
- Click: [What happens on click]
- Loading: [Loading state indicators]
- Success: [Success feedback]
- Error: [Error feedback]

### Responsive Design

- Desktop: [Layout for large screens]
- Tablet: [Adjustments for medium screens]
- Mobile: [Adjustments for small screens]

## Data Model

### Entities

[Define data structures in TypeScript format:]

```typescript
interface User {
  id: string
  email: string
  name: string
  role: 'admin' | 'user' | 'guest'
  createdAt: Date
}

interface Feature {
  id: string
  title: string
  description: string
  status: 'draft' | 'active' | 'archived'
  ownerId: string
  createdAt: Date
  updatedAt: Date
}

// Add all relevant entities
```

### Relationships

[Define how entities relate:]
- User **has many** Features (via ownerId)
- Feature **belongs to** User
- [Continue for all relationships...]

### Data Validation Rules

- `email`: Must be valid email format, unique
- `title`: Required, min 3 chars, max 100 chars
- `status`: Must be one of allowed values
- [Continue for all fields...]

## API Requirements

### Endpoints

[Define all API endpoints needed:]

#### 1. Create Feature

```
POST /api/features
```

**Request:**
```json
{
  "title": "string",
  "description": "string",
  "ownerId": "string"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "string",
    "title": "string",
    "description": "string",
    "status": "draft",
    "ownerId": "string",
    "createdAt": "ISO date string"
  }
}
```

**Errors:**
- `400`: Validation error (missing required fields)
- `401`: Unauthorized (no valid session)
- `403`: Forbidden (user lacks permission)

#### 2. Get Feature

```
GET /api/features/:id
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": { /* Feature object */ }
}
```

**Errors:**
- `404`: Feature not found

#### [Continue for all endpoints...]

### Business Logic

[Explain complex logic:]

**When creating a feature:**
1. Validate all required fields
2. Check user has permission to create features
3. Generate unique ID
4. Set default status to "draft"
5. Set timestamps
6. Save to database
7. Return created feature

**When updating a feature:**
1. Verify feature exists
2. Check user is owner or admin
3. Validate updated fields
4. Update `updatedAt` timestamp
5. Save changes
6. Return updated feature

### Authentication & Authorization

- **Authentication**: Required for all endpoints (JWT token in header)
- **Authorization**:
  - Create: Any authenticated user
  - Read: Owner or admin
  - Update: Owner or admin
  - Delete: Admin only

## Acceptance Criteria

[Write testable criteria in Given-When-Then format:]

- [ ] **AC-1**: Given I am logged in as a user, when I click "Create Feature" and fill in title and description, then a new feature is created with status "draft"

- [ ] **AC-2**: Given I am on the features list page, when I click on a feature title, then I see the feature detail page with all information displayed

- [ ] **AC-3**: Given I am viewing my feature, when I click "Edit" and update the title, then the feature title is updated and I see a success message

- [ ] **AC-4**: Given I am not logged in, when I try to access the features page, then I am redirected to the login page

- [ ] **AC-5**: Given I am logged in as a regular user, when I try to edit another user's feature, then I see an error message "You don't have permission"

[Continue for all acceptance criteria...]

## Edge Cases & Error Handling

### Edge Cases

1. **Empty data**: What happens when there are no features to display?
   - Show empty state message: "You haven't created any features yet"
   - Display "Create Feature" button

2. **Very long text**: What happens when title/description exceeds limits?
   - Truncate with ellipsis in list view
   - Show full text in detail view

3. **Network errors**: What happens when API call fails?
   - Show error message: "Failed to load features. Please try again."
   - Provide "Retry" button

4. **Concurrent edits**: What happens when two users edit the same feature?
   - Use optimistic locking (version field)
   - Show conflict error: "This feature was modified by someone else. Please refresh and try again."

### Error Messages

[User-friendly error messages:]

- **Validation errors**: "Please enter a valid email address"
- **Permission errors**: "You don't have permission to perform this action"
- **Not found errors**: "Feature not found. It may have been deleted."
- **Server errors**: "Something went wrong. Please try again later."

### Loading States

- Initial page load: Show skeleton loaders
- Button actions: Show spinner on button, disable button
- Background updates: Show subtle progress indicator

## Technical Constraints

[Specify technical requirements:]

### Framework & Libraries

- **Frontend**: React 18+ with TypeScript
- **Styling**: Tailwind CSS or styled-components
- **State Management**: React Query for server state, Context API for UI state
- **Form Handling**: React Hook Form with Zod validation
- **API Client**: Axios or Fetch API

### Performance Requirements

- Initial page load: < 2 seconds
- API responses: < 500ms (p95)
- UI interactions: < 100ms perceived response time
- List pagination: 50 items per page

### Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Security Requirements

- All API calls over HTTPS
- CSRF protection on mutations
- Input sanitization to prevent XSS
- SQL injection prevention (parameterized queries)
- Rate limiting: 100 requests per minute per user

### Accessibility

- WCAG 2.1 Level AA compliance
- Keyboard navigation support
- Screen reader friendly
- Proper ARIA labels
- Focus indicators visible

## Implementation Guidance

[Provide guidance for the AI:]

### Recommended Approach

1. **Start with data layer**:
   - Define TypeScript interfaces
   - Set up database schema
   - Create API endpoints with validation

2. **Build core UI components**:
   - Create reusable components (Button, Input, Modal)
   - Implement form components
   - Add loading and error states

3. **Implement features incrementally**:
   - Start with "Create" functionality
   - Add "Read/List" functionality
   - Add "Update" functionality
   - Add "Delete" functionality

4. **Add polish**:
   - Error handling
   - Loading states
   - Empty states
   - Success feedback

### File Structure Suggestion

```
src/
├── components/
│   ├── features/
│   │   ├── FeatureList.tsx
│   │   ├── FeatureDetail.tsx
│   │   ├── FeatureForm.tsx
│   │   └── FeatureCard.tsx
│   └── ui/
│       ├── Button.tsx
│       ├── Input.tsx
│       └── Modal.tsx
├── api/
│   └── features.ts
├── types/
│   └── feature.ts
└── hooks/
    └── useFeatures.ts
```

### Testing Strategy

- Unit tests for business logic functions
- Integration tests for API endpoints
- E2E tests for critical user flows
- Accessibility tests with jest-axe

### Potential Challenges

[Warn about potential issues:]

- **Challenge**: Form validation can get complex with nested fields
  - **Solution**: Use Zod schema validation for type-safe validation

- **Challenge**: Real-time updates for concurrent users
  - **Solution**: Consider WebSocket connection or polling for live data

## Related Work

[Reference related tickets or features:]

- **Depends on**: [JIRA-XXX] User Authentication (needed for permissions)
- **Similar to**: [JIRA-YYY] Export to PDF feature (can reuse export button pattern)
- **Blocks**: [JIRA-ZZZ] Advanced filtering (needs basic feature list first)

---

## Metadata

**Source**: [Jira issue key or "User-provided text"]
**Generated**: [YYYY-MM-DD]
**For**: Lovable AI implementation
```

### Step 3: Context Enhancement

**Always read these context files** to enhance the prompt:

1. **`context/product-context.md`**
   - Use product terminology correctly
   - Reference existing product features
   - Align with product architecture

2. **`context/company-guidelines.md`**
   - Use approved terminology
   - Follow naming conventions
   - Apply brand guidelines

### Step 4: Language & Style

**Writing Principles:**

1. **Be specific, not vague**:
   - ❌ "Add a button"
   - ✅ "Add a primary action button labeled 'Export to Excel' in the top-right corner of the dashboard header"

2. **Use developer language**:
   - ❌ "Users should be able to save"
   - ✅ "POST /api/features endpoint accepts feature data and returns 201 Created"

3. **Include actual code structures**:
   - Use TypeScript interfaces for data models
   - Use HTTP methods and status codes for APIs
   - Use component names for UI elements

4. **Write testable criteria**:
   - Use Given-When-Then format
   - Be specific about expected behavior
   - Include both success and failure cases

5. **Always write in English**:
   - Even if user input is in another language
   - This is a critical requirement per CLAUDE.md

## Working Directory

**Temporary files:** `skills/lovable/temp/`
- Use for intermediate processing
- Never create temp files in root or other locations

**Output location:** `outputs/lovable-prompts/`
- File naming: `lovable-prompt-[issue-key or sanitized-title]-[YYYY-MM-DD].md`
- Examples:
  - `lovable-prompt-PROJ-123-2026-02-14.md`
  - `lovable-prompt-user-authentication-2026-02-14.md`

## Error Handling

### Jira Authentication Errors

```
User: "Generate Lovable prompt for PROJ-123"
[Jira call fails with auth error]

Response: "Your SAP session needs refresh. Let me authenticate..."
[Trigger sap-auth tool]
[Retry Jira call]
```

### Issue Not Found

```
User: "Generate Lovable prompt for PROJ-999"
[Jira returns 404]

Response: "I couldn't find issue PROJ-999. Please verify the issue key, or paste the feature description directly and I'll create the prompt from that."
```

### Missing Information

If critical information is missing from Jira issue or pasted text:

```
Response: "I have the basic feature description, but I'm missing some details for a complete Lovable prompt:

- What UI components are needed? (buttons, forms, tables, etc.)
- What data fields should be included?
- Are there any API endpoints to integrate with?

Can you provide these details, or should I make reasonable assumptions based on similar features?"
```

## Quality Checks

Before outputting the prompt, verify:

- [ ] User story is complete (persona, goal, value)
- [ ] User flow is step-by-step and clear
- [ ] UI components are specifically described
- [ ] Data models use TypeScript interfaces
- [ ] API endpoints have request/response formats
- [ ] Acceptance criteria are testable
- [ ] Edge cases are addressed
- [ ] Technical constraints are specified
- [ ] All text is in English
- [ ] File saved to correct output location

## Example Workflow

```
User: "Generate Lovable prompt for SIGNAVIO-123"

1. Call: get_issue("SIGNAVIO-123")
2. Extract:
   - Summary: "Add export to Excel feature"
   - Description: "Users should be able to export their dashboard data..."
   - Acceptance Criteria: Found in description
3. Read context/product-context.md for product terminology
4. Generate detailed prompt with:
   - User story
   - User flow (navigate → click export → select data → download)
   - UI specs (Export button, file format dropdown)
   - Data model (ExportRequest, ExportResponse)
   - API endpoint (POST /api/export/excel)
   - AC (Button exists, file downloads, data is correct)
   - Edge cases (large datasets, no data, network error)
5. Save to: outputs/lovable-prompts/lovable-prompt-SIGNAVIO-123-2026-02-14.md
6. Confirm to user: "Generated detailed Lovable prompt for SIGNAVIO-123. Output saved to outputs/lovable-prompts/"
```

## Troubleshooting

### Issue: Jira description is vague

**Solution**: Generate prompt with available info, then ask user to clarify:
```
"I've generated a basic prompt, but the Jira issue is missing technical details. Can you clarify:
- What UI screens are involved?
- What data needs to be stored?
- Are there any API integrations?"
```

### Issue: Too many details, prompt is overwhelming

**Solution**: Organize into clear sections, use hierarchical structure. It's better to have comprehensive details than missing information.

### Issue: User provides non-feature content (bug report, question, etc.)

**Solution**: Adapt the template:
- For bugs: Include reproduction steps, expected vs actual behavior
- For questions: Explain this isn't a feature request, ask if they want to rephrase

---

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-02-14 | Initial | Created Lovable prompt generation skill |
