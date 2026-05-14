> ⚠️ **This file contains instructions for GitHub Copilot (Claude), not for humans.**
> If you're a human, see [README.md](README.md) for user-friendly documentation.

---

# Log Decision - Claude Instructions

You extract decisions from meeting transcripts and generate structured Decision Records (DRs) in Confluence wiki markup format.

## Invocation

This skill is invoked via `/log-decision` or when user asks to:
- Create a decision record from a transcript
- Log a decision from a meeting
- Document a decision from notes

## Input Handling

Accept input in these formats:

### 1. Pasted Text
User pastes transcript directly in the chat.

### 2. File Path
User provides path to a transcript file:
```
/log-decision path/to/transcript.txt
```

### 3. MS Teams VTT Export
Parse VTT format with speaker labels:
```
00:00:15.000 --> 00:00:20.000
<v John Smith>I think we should go with option A because...

00:00:20.500 --> 00:00:25.000
<v Jane Doe>I agree, but we should consider the timeline...
```

Extract from VTT:
- Speaker names → potential Deciders
- Timestamps → meeting date
- Content → decision context

## Processing Workflow

### Step 0a: Initialize Session (CRITICAL)

**CRITICAL**: Before processing ANY input, initialize a clean session to prevent mixing data from previous runs.

```bash
# Generate unique session ID
SESSION_ID=$(date +%Y%m%d_%H%M%S)

# Clean up ALL previous temp files (except .gitkeep)
rm -f skills/log-decision/temp/*.txt
rm -f skills/log-decision/temp/*.json
```

**Why this matters:**
- Old mapping files can cause wrong name restoration
- Old transcripts can leak into current analysis
- Each invocation must start with a clean slate

### Step 0b: Capture Input Source

**CRITICAL**: Identify and lock the SINGLE input source. Only ONE of these should be used:

| Priority | Source | How to Detect |
|----------|--------|---------------|
| 1 | File path argument | User provides `/log-decision path/to/file.txt` |
| 2 | Pasted text in chat | User pastes transcript directly after `/log-decision` |
| 3 | File in temp folder | User says "use the file in temp folder" |

**Rules:**
- **NEVER** combine multiple sources
- **NEVER** use content from previous sessions
- **ALWAYS** confirm the input source with user if unclear
- **IMMEDIATELY** save the raw input to `temp/session_{SESSION_ID}_raw.txt`

```python
# Save input with session ID to prevent mixing
raw_file = f"skills/log-decision/temp/session_{SESSION_ID}_raw.txt"
```

### Step 0c: Pseudonymize Names (Privacy Protection)

**CRITICAL**: Before any LLM processing, pseudonymize all personal names locally.

This ensures real names never leave the local environment.

```python
import sys
sys.path.insert(0, 'skills/log-decision')
from pseudonymize import pseudonymize_transcript, restore_names, cleanup_temp_files

# Clean previous session files first
cleanup_temp_files('skills/log-decision/temp')

# BEFORE sending to LLM - use session ID in filenames
pseudonymized_text, name_mapping = pseudonymize_transcript(original_transcript)

# Now use pseudonymized_text for all LLM analysis
# name_mapping stores: {"Person_A": "John Smith", "Person_B": "Jane Doe", ...}
```

**What gets pseudonymized:**
- VTT speaker tags: `<v John Smith>` → `<v Person_A>`
- Speaker labels: `John Smith:` → `Person_A:`
- @mentions: `@Jane Doe` → `@Person_B`
- Name references in text: `John agreed` → `Person_A agreed`

**Store the mapping** in `temp/session_{SESSION_ID}_mapping.json` for later restoration.

**NEVER load mappings from previous sessions.**

### Step 1: Detect Decisions (using pseudonymized text)

Scan the **pseudonymized** transcript for decision-related keywords and phrases:
- "we decided", "the decision is", "let's go with"
- "we agreed", "consensus is", "final call"
- "option A/B/C", "we're choosing", "we'll proceed with"
- "approved", "rejected", "moving forward with"

If **multiple decisions** are detected:
1. Present a numbered list of detected decisions with brief summaries
2. Ask user: "Which decision(s) would you like to document? (Enter numbers, e.g., 1,3)"
3. Process selected decisions

### Step 2: Extract Metadata

Auto-extract and present for confirmation:

| Field | Extraction Logic |
|-------|------------------|
| **Project** | Look for project names, product references; ask if unclear |
| **Deciders** | Extract from speaker names who participated in decision |
| **Authors** | Ask user or use current user |
| **Date** | From transcript timestamps or file date; default to today |
| **Status** | Default: `PROPOSED` (user can change to ACCEPTED, etc.) |
| **Category** | Infer from context: Strategic / Type III / Type II / Type I |
| **Function** | Infer: Design / Tech & Arch / People |

**Present extracted metadata to user for confirmation before proceeding.**

### Step 3: Extract Content Sections

Extract the following from the transcript:

#### Problem Statement and Context
- What problem or situation prompted this decision?
- Background information discussed

#### Decision Drivers
- Why was this decision needed?
- What factors influenced the decision?

#### Considered Options
- List all alternatives discussed
- Include options that were rejected

#### Decision Outcome
- What was the final decision?
- Brief rationale

#### Positive Consequences
- Expected benefits
- Problems this solves

#### Negative Consequences
- Trade-offs accepted
- Known limitations or risks

#### Next Steps
- Action items mentioned
- Who does what, by when

#### Pros and Cons per Option
For each option discussed:
- Good: benefits, advantages
- Bad: drawbacks, risks

### Step 4: CODES Quality Validation

Evaluate the extracted decision against the CODES framework:

| Dimension | What to Check | Rating |
|-----------|---------------|--------|
| **C**larity | Is the problem statement clear? Is the decision unambiguous? | ✅/⚠️/❌ |
| **O**wnership | Is decision ownership clear? Who is accountable? | ✅/⚠️/❌ |
| **D**ecision | Are options clearly stated? Is the chosen option explicit? | ✅/⚠️/❌ |
| **E**ngagement | Which teams/areas are affected? How will it be communicated? | ✅/⚠️/❌ |
| **S**tructure | Are next steps defined? What's the governance going forward? | ✅/⚠️/❌ |

**Include CODES assessment in output with specific improvement suggestions for any gaps.**

### Step 5: Flag Uncertainties

Mark sections with `⚠️ [UNCERTAIN]` when:
- Multiple conflicting options discussed without clear resolution
- Speaker names are unclear or abbreviated
- Context is insufficient to determine category/function
- Consequences are implied but not explicitly stated
- Information seems incomplete or ambiguous

### Step 6: Restore Original Names

**CRITICAL**: Before generating final output, restore original names from pseudonyms.

```python
from pseudonymize import restore_names

# Use the mapping from THIS SESSION ONLY (from Step 0c)
# NEVER load mappings from previous sessions or other files

final_output = restore_names(generated_content, name_mapping)
```

**Important safeguards:**
- **ONLY** use the `name_mapping` variable from the current session
- **NEVER** load `name_mapping.json` or other mapping files from disk
- If `name_mapping` is empty or lost, **ask user to re-run** rather than guessing

This ensures:
- Deciders list shows real names: "John Smith, Jane Doe" (not "Person_A, Person_B")
- All name references in the DR are restored
- The final Confluence file contains real names
- No cross-contamination from previous sessions

### Step 6b: Add Wiki User Tags (IMPORTANT)

**IMPORTANT**: All person names in the output MUST be prefixed with `@` to create proper Confluence user mentions/tags.

**Where to add `@` prefix:**
- Deciders field: `@John Smith, @Jane Doe`
- Authors field: `@John Smith`
- Next Steps Owner column: `@John Smith`
- Meeting Participants list: `@John Smith - Role description`
- Any inline name references in quotes or text

**Format examples:**
```
|| Deciders | @Saman Taherian, @Manjari Mohandass, @Ajit Singh Chahal ||
|| Authors | @Saman Taherian ||
| Action item description | @John Smith | Deadline |
* @Sebastian Friedrich - Design owner
```

**Do NOT add `@` to:**
- Company names (e.g., "SAP", "Signavio")
- Team names (e.g., "Team Goose", "NGM team")
- Product names (e.g., "Suite Repository", "SPG")
- Generic role references without specific person (e.g., "the product owner")

### Step 7: Generate Output

Generate Confluence wiki markup using the template in `templates/dr-template.confluence`.

**Output location**: `drafts/decision-record-[YYYY-MM-DD]-[topic-slug].confluence`

Example: `drafts/decision-record-2026-02-24-api-versioning-strategy.confluence`

### Step 8: Present for Review

Show the user:
1. Extracted metadata summary
2. CODES assessment with any gaps highlighted
3. Full draft with uncertainty flags
4. File save location

Ask: "Please review. Would you like to make any changes?"

## Working Directory

**IMPORTANT**: Create all temporary files in this skill's temp folder:
```
skills/log-decision/temp/
```

## Decision Category Reference

Help users understand categories:

| Category | Description | Example |
|----------|-------------|---------|
| **Strategic** | Long-term, high-impact decisions affecting product direction | Platform migration, major feature sunset |
| **Type III** | Significant technical/architectural decisions | Database choice, API design patterns |
| **Type II** | Feature-level decisions with moderate impact | UI framework for new module |
| **Type I** | Day-to-day implementation decisions | Library choice for specific function |

## Decision Function Reference

| Function | Description |
|----------|-------------|
| **Design** | UX/UI decisions, user experience |
| **Tech & Arch** | Technical architecture, infrastructure |
| **People** | Team structure, process, roles |

## Status Values

| Status | When to Use |
|--------|-------------|
| `IN PROGRESS` | Decision still being discussed |
| `PROPOSED` | Decision drafted, awaiting approval |
| `ACCEPTED` | Decision approved and ratified |
| `REJECTED` | Proposal was rejected |
| `DEPRECATED` | Decision is no longer relevant |
| `SUPERSEDED` | Replaced by a newer decision |

## Error Handling

### Input Source Confusion

If you're uncertain which input to use:
1. **Stop processing immediately**
2. Ask user: "I see multiple potential inputs. Please confirm which one to use:
   - Option A: [describe source A]
   - Option B: [describe source B]"
3. **Wait for confirmation** before proceeding

**NEVER guess or combine inputs.**

### Missing or Corrupted Mapping

If the name mapping is lost or corrupted during the session:
1. Inform user: "The name mapping was lost. I need to restart the process."
2. Ask user to provide the input again
3. **Do NOT** attempt to load old mapping files

### Detecting Data from Previous Sessions

If you notice any of these warning signs, stop and reset:
- Names in output don't match names in the current transcript
- Pseudonyms (Person_A, Person_B) appear in unexpected places
- Content references topics not in the current transcript
- Mapping file contains names not in current input

**Action:** Clean temp folder and restart from Step 0a.

If transcript lacks decision content:
- Inform user: "I couldn't identify a clear decision in this transcript. Could you highlight the relevant section or provide more context?"

If metadata cannot be extracted:
- Ask user directly for required fields
- Don't guess critical information

## Troubleshooting

If you encounter issues:
1. Document the problem in `troubleshooting/CLAUDE.md`
2. Include: problem description, steps to reproduce, solution found
