# BPMN Annotator

AI-powered enrichment for BPMN 2.0 models in Signavio Process Manager. Generates on-canvas annotations, task documentation, department color coding, and impact analysis — **visible directly inside SPM**.

---

## What It Does

Enriches any SPM BPMN model with structured content that appears directly on the diagram canvas:

| Layer | What Gets Added | Where |
|-------|----------------|-------|
| Task Documentation | BPMN `<documentation>` on every task | Portable with BPMN XML export |
| Color Coding | Department-aware task background colors (ARIS-style) | Task fill color |
| Lane Summaries | Structured key-value summary per swimlane | Right of the pool |
| Impact Analysis | IT systems, roles, risks table | Below the pool |
| Gateway Annotations | Routing decision explanation per gateway | Above each gateway |
| Sequence Flow Labels | Labels on unlabeled conditional flows | On flow arrows |
| Phase Headers | Business phase labels above logical sections | Top of canvas |

All generated content is marked with `[BA]` and `sid-BA-*` IDs so it can be cleanly removed or refreshed.

---

## File Structure

```
skills/bpmn-annotator/
├── annotator.py       ← CLI entry point (python annotator.py --help)
├── lib/
│   ├── __init__.py    ← public API exports
│   ├── constants.py   ← BA_PREFIX, LANE_COLOR_PALETTE, SUPPORTED_MODES
│   ├── auth.py        ← SPM authentication (TokenManager wrapper)
│   ├── fetch.py       ← fetch_model(), submit_model(), extract_model_id()
│   ├── parse.py       ← parse_model() — BPMN JSON → structured data
│   ├── generate.py    ← build_full_generation_prompt(), generate_*() functions
│   ├── annotate.py    ← apply_*() and build_*() layer functions
│   ├── clean.py       ← clean_ba_content(), has_ba_content()
│   ├── review.py      ← review_model_quality()
│   ├── translate.py   ← build_translation_prompt(), apply_translations()
│   └── duplicate.py   ← duplicate_model(), create_model()
├── SKILL.md           ← Claude Code instructions
└── temp/
    └── .gitkeep       ← temp/ is gitignored; use for scratch work
```

---

## Architecture

### Agent Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER (PM)                                │
│              "Duplicate this model into Spanish"                │
└──────────────────────────────┬──────────────────────────────────┘
                               │  model URL + mode
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE  (AI Brain)                      │
│                                                                 │
│   Understands intent · Chooses mode · Generates content        │
│   Translates labels · Makes mid-run decisions · Reports back   │
└──────────┬──────────────────────────────────────┬──────────────┘
           │ orchestrates                          │ generates content
           ▼                                       ▼
┌──────────────────────┐               ┌──────────────────────────┐
│   annotator.py       │               │   Claude LLM             │
│   (CLI / dispatcher) │               │                          │
│                      │               │  · Annotation text       │
│   Reads --url        │               │  · Translations JSON     │
│   Reads --mode       │               │  · Quality report        │
│   Loads --content    │               │  · Layer content JSON    │
└──────────┬───────────┘               └──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      lib/  (Execution Layer)                    │
│                                                                 │
│  auth.py ──────► SAP SSO session token                         │
│  fetch.py ─────► GET model JSON  /  PUT updated model          │
│  parse.py ─────► tasks, lanes, gateways, events, flows         │
│  generate.py ──► build prompts for Claude content generation   │
│  annotate.py ──► apply colors, badges, annotations, docs       │
│  translate.py ─► apply translations to model shapes            │
│  duplicate.py ─► POST new model copy to target folder          │
│  clean.py ─────► strip all [BA]-prefixed content               │
│  layout.py ────► reroute connectors orthogonally               │
└──────────┬──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SIGNAVIO SYSTEMS  (External)                 │
│                                                                 │
│  ┌──────────────────┐  ┌─────────────────┐  ┌───────────────┐  │
│  │  Process Manager │  │   Dictionary /  │  │ Collaboration │  │
│  │  (SPM REST API)  │  │   Glossary API  │  │     Hub       │  │
│  │                  │  │                 │  │               │  │
│  │ GET  /model/{id} │  │ GET  /glossary  │  │ Fact Sheet    │  │
│  │ PUT  /model/{id} │  │ POST /glossary  │  │ Dict. links   │  │
│  │ POST /model      │  │ POST /publish   │  │ visible here  │  │
│  └──────────────────┘  └─────────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

### Execution Flow by Mode

**Annotation (`full` mode)**
```
User
 │
 ├─► dry_run ──► parse model ──► build prompt ──► Claude generates JSON
 │                                                        │
 └─► full ─────► fetch model ──► clean [BA] ──► apply layers ──► PUT to SPM
                                                  │
                                    colors · docs · badges
                                    summaries · gateways · phases
```

**Translation (`translate_duplicate`)**
```
User
 │
 ├─► translate_dry_run ──► collect all text fields ──► print prompt (no write)
 │
 └─► translate_duplicate
          │
          ├─ 1. Fetch source model  (GET /model/{id})
          ├─ 2. Claude translates   (tasks · lanes · gateways · events
          │                          flows · data objects · annotations)
          ├─ 3. Apply translations  (in-memory deep copy — original untouched)
          ├─ 4. POST new model      (to target folder)
          ├─ 5. Add badges          (numbering_only on new copy)
          └─ 6. Embed dict links    (glossaryLinks → PUT · POST /publish)
```

**Dictionary Linking**
```
model elements                 Signavio Dictionary          Collaboration Hub
      │                               │                            │
      ├─ collect names                │                            │
      │                               │                            │
      ├─ search glossary ────────────►│                            │
      │  GET /glossary?filter=...     │                            │
      │                               │                            │
      ├─ create missing entries ─────►│                            │
      │  POST /glossary               │                            │
      │                               │                            │
      ├─ embed glossaryLinks          │                            │
      │  { "name": ["/glossary/{id}"] }                           │
      │                               │                            │
      ├─ PUT model ──────────────────────────────────────────────►│
      │                                                            │
      └─ POST /publish ───────────────────────────────────────────►
                                              elements clickable in Fact Sheet
```

---

## How to Run

> **Windows / PowerShell users:** Use the PowerShell syntax shown below (no backslash line continuations, URL in quotes).

### 1. Quality review — no SPM changes

```powershell
python skills/bpmn-annotator/annotator.py --url "https://editor.signavio.com/p/hub/model/2c72f43e8ae845cc8f86e90b809b2829" --mode review_only
```

Output: markdown quality report in terminal (task naming, missing events, undocumented tasks, etc.).

---

### 2. Dry run — inspect model structure, get generation prompt

```powershell
# Print to terminal
python skills/bpmn-annotator/annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode dry_run

# Save generation prompt to file
python skills/bpmn-annotator/annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode dry_run --output prompt.txt
```

Output: model structure summary + the generation prompt. No changes to SPM.

---

### 3. Full annotation workflow

**Step 1** — Generate the prompt:
```powershell
python skills/bpmn-annotator/annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode dry_run --output prompt.txt
```

**Step 2** — Paste `prompt.txt` to Claude. Claude returns a JSON block like:
```json
{
  "task_docs":       { "TASK_ID_HERE": "[BA]\nDescription: ..." },
  "lane_summaries":  { "LANE_ID_HERE": "[BA] LANE NAME\n..." },
  "gateway_texts":   { "GATEWAY_ID_HERE": "[BA] Approved? Yes -> ..." },
  "impact_analysis": "[BA] IMPACT ANALYSIS ...",
  "phase_headers":   [{ "label": "Preparation", "ref_task_id": "sid-..." }]
}
```

**Step 3** — Save the JSON response to `content.json`, then apply:
```powershell
python skills/bpmn-annotator/annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode full --content content.json
```

---

### 4. Apply a single layer

```powershell
# Task documentation only
python skills/bpmn-annotator/annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode documentation_only --content content.json

# Impact analysis only
python skills/bpmn-annotator/annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode impact_only --content content.json
```

---

### 5. Clean all annotator content

```powershell
# Remove all [BA] content from SPM
python skills/bpmn-annotator/annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode clean_only

# Remove [BA] content and immediately reapply with new content
python skills/bpmn-annotator/annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode clean_and_rerun --content content.json
```

---

### 6. Translate a model into another language

**Step 1** — Translation dry run (inspect what will be translated, no SPM changes):
```powershell
python skills/bpmn-annotator/annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode translate_dry_run --language Spanish --output translate_prompt.txt
```

Output: element count by type, and the translation prompt. No changes to SPM.

**Step 2** — Paste `translate_prompt.txt` to Claude. Claude returns a JSON block like:
```json
{
  "target_language": "Spanish",
  "source_language": "English",
  "model_title": "Proceso de Incorporación de Empleados",
  "lanes":     { "sid-abc": "Recursos Humanos", "sid-def": "TI" },
  "tasks":     { "sid-111": "Enviar formulario de solicitud", "sid-222": "Revisar documentos" },
  "task_docs": { "sid-111": "[BA]\nDescripción: ..." },
  "gateways":  { "sid-333": "¿Documentos completos?" },
  "events":    { "sid-444": "Proceso iniciado", "sid-555": "Proceso completado" },
  "flows":     { "sid-666": "Sí", "sid-777": "No" },
  "annotations": { "sid-BA-LANE-xyz": "[BA] Recursos Humanos\n..." }
}
```

**Step 3** — Save the JSON to `translations.json`, then create the translated copy:
```powershell
python skills/bpmn-annotator/annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode translate_duplicate --language Spanish --content translations.json
```

Output: new model created and opened at `{original name} - Spanish`. Original is untouched.

**Optional — translate in place** (overwrites original, requires explicit `--confirm`):
```powershell
python skills/bpmn-annotator/annotator.py --url "YOUR_MODEL_URL_OR_ID" --mode translate_in_place --language French --content translations.json --confirm
```

---

## Supported Modes

| Mode | Requires `--content` | Requires `--language` | What Runs |
|------|:--:|:--:|-----------|
| `dry_run` *(default)* | No | No | Model summary + generation prompt, no SPM changes |
| `review_only` | No | No | Quality report in terminal, no SPM changes |
| `full` | Yes | No | All layers: docs + colors + summaries + impact + gateways + phases |
| `documentation_only` | Yes | No | Task documentation only |
| `lane_summary_only` | Yes | No | Lane summary annotations only |
| `impact_only` | Yes | No | Impact analysis annotation only |
| `gateway_only` | Yes | No | Gateway explanation annotations only |
| `flows_only` | Yes | No | Sequence flow labels only |
| `phases_only` | Yes | No | Phase header annotations only |
| `numbering_only` | No | No | Auto-number tasks in flow order |
| `clean_only` | No | No | Remove all `[BA]` content |
| `clean_and_rerun` | Yes | No | Remove `[BA]` content, then reapply |
| `translate_dry_run` | No | Yes | Translation table + prompt, no SPM changes |
| `translate_duplicate` | Yes | Yes | Duplicate model, translate the copy (original untouched) |
| `translate_in_place` | Yes | Yes | Translate original model directly (requires `--confirm`) |

---

## Inputs

Accepts either format:
- **Signavio URL**: `https://editor.signavio.com/p/hub/model/2c72f43e8ae845cc8f86e90b809b2829`
- **Model ID directly**: `2c72f43e8ae845cc8f86e90b809b2829`

---

## Using as a Module

```python
from skills.bpmn_annotator.lib import (
    get_auth, fetch_model, parse_model,
    build_full_generation_prompt,
    clean_ba_content, review_model_quality,
)

auth = get_auth()
model, info = fetch_model(auth, "2c72f43e8ae845cc8f86e90b809b2829")
parsed = parse_model(model)

# Quality review
print(review_model_quality(parsed))

# Get generation prompt
print(build_full_generation_prompt(parsed))
```

---

## BPMN-Safe Behavior

This skill only uses BPMN 2.0 compliant augmentations:

| What it adds | BPMN 2.0 element | Notes |
|---|---|---|
| Task documentation | `<documentation>` property | Standard; portable to ARIS, Camunda, Bizagi |
| TextAnnotations | `TextAnnotation` artifact | Standard; placed outside or alongside process |
| Task colors | `bgcolor` / `bordercolor` properties | Cosmetic extension, non-semantic |
| Flow labels | `name` property on SequenceFlow | Standard |

**It never:**
- Changes control flow (no added/rerouted sequence or message flows)
- Invents process logic not visible in the model
- Renames tasks without explicit confirmation (`naming_only` mode requires user approval)
- Removes existing human-authored content (only `[BA]`-prefixed content is cleaned)
- Adds pools, lanes, or gateways

---

## Content Generation Rules

All generation prompts enforce:
- Only reference IT systems **explicitly named in task labels**
- Only reference roles from **lane names**
- Mark any inference with `(inferred)`
- Preserve existing human-authored documentation (never overwrite non-`[BA]` docs)

---

## [BA] Marker Convention

All annotator-generated content is tagged so it can be identified and removed:

| Content type | Marker |
|---|---|
| TextAnnotation shapes | `resourceId` starts with `sid-BA-` |
| Task documentation | `documentation` property starts with `[BA]` |
| Sequence flow labels | `name` property starts with `[BA]` |

This enables `clean_only` and `clean_and_rerun` to remove only annotator content.

---

## Modeling Quality Review Checks

`review_only` mode reports on:

| Check | Rule |
|---|---|
| Task naming | Should follow Verb + Object pattern |
| Gateway labels | Exclusive gateways should carry a question label |
| Conditional flow labels | Flows leaving gateways should be labeled |
| Empty lanes | Lanes with no tasks |
| Missing start/end events | Every process needs at least one of each |
| Undocumented tasks | Tasks with no `documentation` property |
| Long linear sequences | > 7 tasks in a lane with no gateways |
| Complex pool | > 8 swimlanes suggests decomposition |

---

## Color Palette (ARIS-inspired)

| Lane position | Background | Border | Typical use |
|---|---|---|---|
| 1st | `#dae8fc` | `#6c8ebf` | HR / Management / Process Owner |
| 2nd | `#d5e8d4` | `#82b366` | IT / Systems / Technical |
| 3rd | `#fff2cc` | `#d6b656` | Operations / Line roles |
| 4th | `#f8cecc` | `#b85450` | External / Customer |
| 5th | `#e1d5e7` | `#9673a6` | Finance / Compliance |

Colors cycle automatically for models with more than 5 lanes.

---

## Example Prompts (Claude Code)

```
Annotate this process: https://editor.signavio.com/p/hub/model/abc123

Review the modeling quality of: [URL]

Add lane summaries to: [URL]

Clean the annotations from: [URL]

/bpmn-annotator [URL] full

Duplicate this Signavio model into Spanish: [URL]

Create a German version of this BPMN model: [URL]

Dry run translation to Japanese without updating Signavio: [URL]

Translate only labels, not documentation: [URL] --language French

Duplicate and translate model, preserving SAP and IT terms: [URL] --language Spanish
```

---

## Translation Behavior

### What gets translated

| Element | Property |
|---------|----------|
| Model / pool title | `name` on Pool shape + SPM folder entry |
| Lane names | `name` on each Lane shape |
| Task names | `name` property |
| Task documentation | `documentation` property (`[BA]` prefix preserved) |
| Gateway labels | `name` property (decision questions) |
| Event names | `name` property |
| Sequence flow labels | `name` property |
| TextAnnotation content | `text` property (`[BA]` prefix preserved) |

### What is never translated

| Category | Examples |
|----------|----------|
| BPMN / element IDs | `resourceId` values, `sid-*` strings |
| System / product names | SAP, Jira, Slack, ServiceNow, ARIS, Celonis, GitHub, Confluence |
| Role abbreviations | HR, IT, PM, LM, CEO, CFO |
| Technical standards | BPMN, ERP, CRM, SLA, KPI, API, SSO |
| Annotator markers | `[BA]`, `[BA#]` prefixes |
| Layout / style data | coordinates, colors, bounds |
| URLs, emails, codes | any technical identifiers |

### Safety behavior

- **Default is always `translate_duplicate`** — original model is never touched
- `translate_in_place` requires explicit `--confirm` flag
- Translated copy is named `{original name} - {language}` in the SPM folder
- BPMN structure (flows, gateways, task types, layout) is fully preserved
- `[BA]` annotator content is translated but prefixes are kept intact so `clean_only` still works

---

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-04-27 | Claude Code | Translation capability: `translate_duplicate`, `translate_dry_run`, `translate_in_place` modes; `lib/translate.py` and `lib/duplicate.py` |
| 2026-04-14 | Maria Jauregui | Productized: lib/ module structure, CLI entry point, dry-run mode, removed hardcoded onboarding content |
| 2026-04-14 | Maria Jauregui | Initial skill creation — all 9 layers, SKILL.md, prototype annotator |
