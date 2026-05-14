> This file contains instructions for Claude. For human documentation see [README.md](README.md).

---

# BPMN Annotator — Claude Skill Instructions

## What This Skill Does

Enriches any BPMN 2.0 model stored in Signavio Process Manager (SPM) with:

1. **Task Documentation Layer** — AI-generated BPMN `<documentation>` on every task (portable, travels with BPMN XML export)
2. **Color Coding Layer** — department/lane-aware task background colors (ARIS-style)
3. **Lane Summary Layer** — structured `TextAnnotation` per swimlane, placed right of the pool
4. **Impact Analysis Layer** — structured `TextAnnotation` below the pool (IT systems, roles, risks)
5. **Gateway Explanation Layer** — `TextAnnotation` near each gateway explaining its routing logic
6. **Sequence Flow Label Layer** — labels on decision/conditional flows where clarity is missing
7. **Phase Header Layer** — top-level business phase annotations above logical sections
8. **Task Naming Layer** — improve task labels to Verb + Object style (optional, requires confirmation)
9. **Modeling Quality Review Layer** — report on BPMN quality issues in chat (no canvas changes)

All generated content is prefixed with `[BA]` so it can be identified and removed cleanly on re-run.

10. **Dictionary Linking** — link model elements to SAP Signavio dictionary/glossary entries so they appear with descriptions in the Collaboration Hub Fact Sheet. Supports English, Spanish, and German models.

11. **Model Translation (duplicate mode)** — duplicate a BPMN model and translate the copy into any of 18+ languages. Original is never touched.

12. **Native Multilingual Translation** — populate SPM's native `properties.names.{lang_code}` / `properties.documentations.{lang_code}` fields so a single model serves multiple languages. Non-destructive: original text is preserved alongside all translations.

13. **SGX Export** — download the `.sgx` ZIP archive (Signavio's export format, containing both model JSON and BPMN XML) to a local temp folder for inspection, offline translation, or backup.

---

## When to Use This Skill

Use when the user says anything like:
- "Annotate this process: [URL or ID]"
- "Add documentation to this BPMN model"
- "Generate impact analysis for [URL]"
- "Make this model ARIS-style"
- "Add lane summaries to this diagram"
- "Review the modeling quality of [URL]"
- "Clean the annotations from [URL]"
- `/bpmn-annotator [URL or ID] [mode?]`
- "Link dictionary entries to this model"
- "Add glossary links to [URL or folder]"
- "Make elements clickable in the Collaboration Hub"
- "Create dictionary entries for [model or folder]"
- "Duplicate this model into Spanish: [URL]"
- "Create a German version of this BPMN model"
- "Translate this process to Japanese"
- "Make a French copy of this diagram"
- "Dry run translation to [language] without updating Signavio"
- "Translate only labels, not documentation"
- "Duplicate and translate model, preserving SAP and IT terms"
- "Clean up the layout of this model: [URL]"
- "Fix the arrows and connectors in this BPMN"
- "Reroute connectors orthogonally"
- "The flows in this model look messy, fix the routing"
- "Make this model look like a professionally drawn BPMN"
- "Add step numbers to the tasks in this model"
- "Number the tasks with badges"
- "Add numbered badges to each task"
- "Export the SGX file for this model"
- "Download the .sgx export from Signavio"
- "Inspect the multilingual fields in this model"
- "What languages are available in this BPMN?"
- "Show me which language fields are filled in this model"
- "Translate this model into [language] using native multilingual fields"
- "Add a [language] version inside the model (one model, multiple languages)"
- "Create a multilingual BPMN that keeps the original and adds translations"

---

## Inputs

The user can provide either:
- A **Signavio model URL**: `https://editor.signavio.com/p/hub/model/2c72f43e8ae845cc8f86e90b809b2829`
- A **model ID** directly: `2c72f43e8ae845cc8f86e90b809b2829`

Extract the model ID using this regex: `r'/model/([a-f0-9]{32})'`

If no input is provided, ask the user to paste a Signavio model URL.

---

## Supported Modes

| Mode | What it runs |
|------|-------------|
| `full` (default) | All layers: docs + colors + lane summaries + impact + gateways + flow labels |
| `documentation_only` | Task documentation layer only |
| `naming_only` | Task naming standardization (requires user confirmation before applying) |
| `gateway_only` | Gateway explanation annotations only |
| `flows_only` | Sequence flow labels only |
| `phases_only` | Phase header annotations only |
| `lane_summary_only` | Lane summary annotations only |
| `impact_only` | Impact analysis annotation only |
| `review_only` | Quality review — output in chat, no canvas changes |
| `clean_and_rerun` | Remove all `[BA]`-prefixed content, then rerun full mode |
| `clean_only` | Remove all `[BA]`-prefixed content without rerunning |
| `dictionary_link` | Embed `glossaryLinks` into model shapes and publish to Collaboration Hub |
| `dictionary_create` | Create new EN dictionary entries for all named elements in a model |
| `dictionary_translate` | Create ES, DE, JP (or any language) translation entries linked to existing EN entries, rename all element names, and embed new links |
| `translate_dry_run` | Print translation table and prompt for review — no SPM changes (requires `--language`) |
| `translate_duplicate` | Duplicate the model, translate the copy, submit — **original is never touched** (requires `--language` + `--content`) |
| `translate_in_place` | Translate the original model directly — destructive, requires explicit `--confirm` (requires `--language` + `--content`) |
| `multilingual_inspect` | Scan model for existing `properties.names` / `properties.documentations` language fields; report which languages are populated vs. empty |
| `multilingual_native` | Write translations into native SPM multilingual fields (`properties.names.de_de`, etc.) — non-destructive, one model for all languages (requires `--language` + `--content`) |
| `sgx_export` | Download the `.sgx` ZIP export to `temp/` for inspection, backup, or offline processing |
| `layout_cleanup` | Re-route all connectors orthogonally — dry-run by default; add `--confirm` to apply. No content file needed. |

If the user does not specify a mode, use `full`.

---

## BPMN Safety Rules — NEVER VIOLATE

1. **Never change control flow** — do not add, remove, or reroute sequence flows or message flows unless explicitly asked
2. **Never invent process logic** — only describe what the model already shows; do not assume steps that aren't modeled
3. **Never rename tasks without confirmation** — naming mode requires explicit user approval before writing back
4. **Never remove existing non-annotator content** — only remove shapes/properties with `[BA]` prefix
5. **Never add pools, lanes, or gateways** — structural changes are out of scope
6. **Only use BPMN-safe augmentations:**
   - Task `documentation` property (BPMN 2.0 standard)
   - Task `bgcolor` / `bordercolor` (cosmetic extension, non-semantic)
   - `TextAnnotation` shapes (BPMN 2.0 artifact)
   - `Association_Undirected` connections (BPMN 2.0 artifact)
   - Sequence flow `name` property (BPMN 2.0 standard)

---

## Step-by-Step Execution

### Step 1 — Fetch the model

```python
import sys, json, re, urllib.parse
sys.path.insert(0, r'c:\Users\I769452\signavio_process_consultant_experimental\mcp\signavio\spm\src')
from spm_mcp.auth import TokenManager, SPMConfig

config = SPMConfig()
auth = TokenManager(config)
auth.ensure_authenticated()

# Extract model ID from URL if needed
url_or_id = "<user input>"
match = re.search(r'/model/([a-f0-9]{32})', url_or_id)
model_id = match.group(1) if match else url_or_id.strip()

resp = auth.session.get(f"{auth.api_base}/model/{model_id}/info")
info = resp.json()
resp2 = auth.session.get(f"{auth.api_base}{info['revision']}/json")
model = resp2.json()
```

### Step 2 — Parse model structure

Extract the following from the model JSON for AI analysis:

```python
def parse_model(model):
    result = {
        "title": "",
        "pools": [],       # list of {id, name, bounds}
        "lanes": [],       # list of {id, name, abs_y, height, tasks}
        "tasks": [],       # list of {id, name, lane_id, lane_name, bounds_local, incoming, outgoing_names}
        "gateways": [],    # list of {id, type, name, lane_name, bounds_local, incoming_names, outgoing_names}
        "events": [],      # list of {id, type, name, lane_name}
        "flows": [],       # list of {id, name, source_name, target_name}
        "existing_docs": {},  # task_id -> existing documentation text
    }

    # Pool title
    for s in model["childShapes"]:
        if s.get("stencil", {}).get("id") == "Pool":
            result["title"] = s.get("properties", {}).get("name", "")
            pool_bounds = s["bounds"]
            pool_ul = pool_bounds["upperLeft"]

            # Walk lanes
            for lane in s.get("childShapes", []):
                if lane.get("stencil", {}).get("id") != "Lane":
                    continue
                lane_id = lane["resourceId"]
                lane_name = lane.get("properties", {}).get("name", "")
                lane_bounds = lane["bounds"]
                lane_ul = lane_bounds["upperLeft"]
                abs_y = pool_ul["y"] + lane_ul["y"]
                height = lane_bounds["lowerRight"]["y"] - lane_ul["y"]

                lane_tasks = []
                lane_gws = []

                for elem in lane.get("childShapes", []):
                    stencil = elem.get("stencil", {}).get("id", "")
                    props = elem.get("properties", {})
                    eid = elem["resourceId"]
                    name = props.get("name", "").replace("\n", " ").strip()
                    b = elem["bounds"]
                    ul = b["upperLeft"]

                    if stencil == "Task":
                        incoming = [o["resourceId"] for o in elem.get("incoming", [])] if "incoming" in elem else []
                        outgoing = [o["resourceId"] for o in elem.get("outgoing", [])]
                        existing_doc = props.get("documentation", "")
                        result["tasks"].append({
                            "id": eid, "name": name, "lane_id": lane_id,
                            "lane_name": lane_name, "bounds_local": ul,
                            "outgoing_ids": outgoing,
                            "existing_doc": existing_doc,
                        })
                        lane_tasks.append(name)
                        result["existing_docs"][eid] = existing_doc

                    elif "Gateway" in stencil:
                        outgoing_names = [o["resourceId"] for o in elem.get("outgoing", [])]
                        result["gateways"].append({
                            "id": eid, "type": stencil, "name": name,
                            "lane_name": lane_name, "bounds_local": ul,
                            "outgoing_ids": outgoing_names,
                        })
                        lane_gws.append({"id": eid, "type": stencil, "name": name})

                    elif "Event" in stencil:
                        result["events"].append({
                            "id": eid, "type": stencil, "name": name, "lane_name": lane_name
                        })

                result["lanes"].append({
                    "id": lane_id, "name": lane_name,
                    "abs_y": abs_y, "height": height,
                    "tasks": lane_tasks, "gateways": lane_gws,
                })

    # Top-level sequence flows
    for s in model["childShapes"]:
        if s.get("stencil", {}).get("id") == "SequenceFlow":
            result["flows"].append({
                "id": s["resourceId"],
                "name": s.get("properties", {}).get("name", ""),
            })

    return result
```

### Step 3 — Generate content with AI

After parsing, construct a prompt to yourself (Claude) to generate all documentation content. **Use only what the model contains — do not invent.**

Build a single generation prompt like:

```
You are a BPMN documentation expert. Based ONLY on the information below, generate:
1. For each task: a BPMN documentation block (Description, Purpose, Inputs, Outputs, Responsible, Systems, Risks)
2. For each lane: a compact structured summary (max 8 lines)
3. An impact analysis table (IT systems, roles, risks — derived from task names and lane names only)
4. For each gateway: a one-line routing explanation
5. Phase headers if logical groupings are visible

Process title: {title}
Lanes and tasks:
{for each lane: lane name → [task1, task2, ...]}
Gateways: {list with type and position}
Events: {start/end names}
Existing documentation (if any): {task_id: existing_doc}

Rules:
- Only reference IT systems explicitly named in task labels (e.g. "SAP SuccessFactors" if in task name)
- Only reference roles from lane names
- Mark any inference with "(inferred)"
- Keep task documentation under 6 lines
- Keep lane summaries under 8 lines
- Prefix ALL generated text with [BA]
```

### Step 4 — Apply clean-up (remove previous [BA] content)

```python
BA_PREFIX = "[BA]"

def is_ba_shape(shape):
    """Returns True if this shape was generated by bpmn-annotator."""
    rid = shape.get("resourceId", "")
    text = shape.get("properties", {}).get("text", "")
    return rid.startswith("sid-BA-") or text.startswith(BA_PREFIX)

def clean_ba_content(shapes):
    """Remove all [BA]-prefixed shapes and documentation from tasks."""
    for s in shapes:
        # Remove BA task documentation
        if s.get("stencil", {}).get("id") == "Task":
            doc = s.get("properties", {}).get("documentation", "")
            if doc.startswith(BA_PREFIX):
                s["properties"]["documentation"] = ""
        # Remove BA shapes from childShapes
        s["childShapes"] = [c for c in s.get("childShapes", []) if not is_ba_shape(c)]
        # Remove BA outgoing references from tasks
        if s.get("stencil", {}).get("id") == "Task":
            s["outgoing"] = [o for o in s.get("outgoing", [])
                             if not o.get("resourceId", "").startswith("sid-BA-")]
        clean_ba_content(s.get("childShapes", []))

    # Remove BA shapes from canvas root
    return [s for s in shapes if not is_ba_shape(s)]

model["childShapes"] = clean_ba_content(model["childShapes"])
```

### Step 5 — Apply layers

#### Department Colors
```python
# Map lane names to colors (ARIS-inspired)
LANE_COLOR_PALETTE = [
    {"bgcolor": "#dae8fc", "bordercolor": "#6c8ebf"},  # blue
    {"bgcolor": "#d5e8d4", "bordercolor": "#82b366"},  # green
    {"bgcolor": "#fff2cc", "bordercolor": "#d6b656"},  # amber
    {"bgcolor": "#f8cecc", "bordercolor": "#b85450"},  # red/pink
    {"bgcolor": "#e1d5e7", "bordercolor": "#9673a6"},  # purple
]

def assign_colors(model_data):
    """Returns {lane_id: color_dict} — one color per lane, cycling through palette."""
    return {lane["id"]: LANE_COLOR_PALETTE[i % len(LANE_COLOR_PALETTE)]
            for i, lane in enumerate(model_data["lanes"])}
```

#### Task Documentation
```python
def apply_task_docs(shapes, generated_docs):
    """generated_docs: {task_id: doc_text}"""
    for s in shapes:
        rid = s.get("resourceId", "")
        if s.get("stencil", {}).get("id") == "Task" and rid in generated_docs:
            # Only write if no existing human-written documentation
            existing = s["properties"].get("documentation", "")
            if not existing or existing.startswith(BA_PREFIX):
                s["properties"]["documentation"] = generated_docs[rid]
        apply_task_docs(s.get("childShapes", []), generated_docs)
```

#### TextAnnotation Builder
```python
def make_annotation(annot_id, text, x, y, width, height):
    return {
        "resourceId": annot_id,
        "properties": {"text": text},
        "stencil": {"id": "TextAnnotation"},
        "childShapes": [], "outgoing": [],
        "bounds": {
            "upperLeft":  {"x": x,         "y": y},
            "lowerRight": {"x": x + width, "y": y + height}
        },
        "dockers": []
    }
```

#### Lane Summaries (right of pool)
```python
# Pool right edge: pool_ul_x + pool_width
# Place at x = pool_right + 20, aligned with each lane's abs_y
ANNOT_W, ANNOT_H = 280, 220

def build_lane_summaries(model_data, pool_bounds, generated_lane_summaries):
    pool_right = pool_bounds["upperLeft"]["x"] + (
        pool_bounds["lowerRight"]["x"] - pool_bounds["upperLeft"]["x"]
    )
    annots = []
    for lane in model_data["lanes"]:
        text = generated_lane_summaries.get(lane["id"], "")
        if not text:
            continue
        annot_id = f"sid-BA-LANE-{lane['id'].replace('sid-', '').replace('-', '_')}"
        annots.append(make_annotation(
            annot_id, f"{BA_PREFIX}\n{text}",
            x=pool_right + 20, y=lane["abs_y"] + 5,
            width=ANNOT_W, height=min(ANNOT_H, lane["height"] - 10)
        ))
    return annots
```

#### Impact Analysis (below pool)
```python
def build_impact_analysis(model_data, pool_bounds, generated_impact):
    pool_bottom = pool_bounds["lowerRight"]["y"]
    pool_left   = pool_bounds["upperLeft"]["x"]
    pool_width  = pool_bounds["lowerRight"]["x"] - pool_left
    return make_annotation(
        "sid-BA-IMPACT",
        f"{BA_PREFIX}\n{generated_impact}",
        x=pool_left, y=pool_bottom + 20,
        width=pool_width, height=270
    )
```

#### Gateway Annotations
```python
# Place annotation above each gateway
def build_gateway_annotations(model_data, pool_bounds, generated_gw_texts):
    pool_ul = pool_bounds["upperLeft"]
    annots = []
    for gw in model_data["gateways"]:
        text = generated_gw_texts.get(gw["id"], "")
        if not text:
            continue
        # Find lane abs_y for this gateway
        lane = next((l for l in model_data["lanes"] if l["id"] == gw.get("lane_id", "")), None)
        lane_abs_y = lane["abs_y"] if lane else pool_ul["y"]
        gw_abs_x = pool_ul["x"] + gw["bounds_local"]["x"]
        gw_abs_y = lane_abs_y + gw["bounds_local"]["y"]
        annot_id = f"sid-BA-GW-{gw['id'].replace('sid-', '').replace('-', '_')}"
        annots.append(make_annotation(
            annot_id, f"{BA_PREFIX} {text}",
            x=gw_abs_x - 20, y=gw_abs_y - 60,
            width=160, height=50
        ))
    return annots
```

### Step 6 — Submit updated model

```python
import urllib.parse

def submit_model(auth, model_id, model, info, comment="BPMN Annotator: full enrichment"):
    json_xml = json.dumps(model, separators=(',', ':'))
    encoded = urllib.parse.urlencode({
        "json_xml": json_xml,
        "name": info["name"],
        "comment": comment,
        "parent": info["parent"],
    })
    response = auth.session.put(
        f"{auth.api_base}/model/{model_id}",
        data=encoded,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=120
    )
    result = response.json()
    # Extract revision info
    if isinstance(result, list):
        for item in result:
            if isinstance(item, dict) and item.get("rel") == "info":
                r = item.get("rep", {})
                return r.get("rev"), r.get("updated")
    return None, None
```

---

## Modeling Quality Review (review_only mode)

When running `review_only`, analyze the parsed model and report in chat. Check for:

| Check | Rule |
|---|---|
| Task naming | Should follow Verb + Object pattern |
| Gateway labels | Exclusive gateways should have a question label |
| Flow labels | Conditional flows leaving gateways should be labeled |
| Empty lane | Lanes with no tasks are suspicious |
| Long sequences | More than 8 tasks in a row without a gateway may need decomposition |
| Missing start/end | Every process should have exactly one start and one end event |
| Undocumented tasks | Tasks with no `documentation` property set |
| Swimlane consistency | Tasks in wrong lane relative to their name |

Output as a structured markdown report in chat. Do NOT write to SPM in this mode.

---

## Color Palette (ARIS-inspired, BPMN-safe)

| Lane position | bgcolor | bordercolor | Use case |
|---|---|---|---|
| 1st lane | `#dae8fc` | `#6c8ebf` | HR / Management / Process Owner |
| 2nd lane | `#d5e8d4` | `#82b366` | IT / Systems / Technical |
| 3rd lane | `#fff2cc` | `#d6b656` | Operations / Line roles |
| 4th lane | `#f8cecc` | `#b85450` | External / Customer |
| 5th lane | `#e1d5e7` | `#9673a6` | Finance / Compliance |

Colors cycle if there are more than 5 lanes.

---

## Task Numbering — Badge Style

Tasks are numbered using compact 22×22 px `TextAnnotation` badges placed at each task's top-left corner (slightly overlapping). This is purely cosmetic — it never alters task labels, control flow, or BPMN semantics.

### Badge properties

| Property | Value |
|----------|-------|
| Stencil | `TextAnnotation` |
| Size | 22 × 22 px |
| Position | `(task_abs_x − 11, task_abs_y − 11)` |
| `bgcolor` | `#1473e8` (SAP blue) |
| `bordercolor` | `#1473e8` |
| `resourceId` prefix | `sid-BA-BADGE-` (cleaned by `clean_only` / `clean_and_rerun`) |
| Text | Step number (1-based, left-to-right reading order) |

### Ordering

Tasks are sorted left-to-right by absolute x, breaking ties by y, across all lanes. This matches natural reading order of the diagram.

### Old text-prefix style

The earlier numbering style (`[BA#] N. Task name`) is no longer used. Running `numbering_only` or `full` automatically strips any `[BA#]` prefixes still present on task labels and replaces them with badge annotations.

### SPM rendering note

Signavio Process Manager does not expose a native circle/badge shape via its REST API outside of BPMN event stencils (which carry semantic meaning). Badges are rendered as compact rectangular `TextAnnotation` boxes with blue background properties. The `bgcolor` / `bordercolor` fields control background in the diagram canvas. At 22 × 22 px the box reads as a compact corner badge. If SPM's TextAnnotation stencil definition ignores `bgcolor`, the number is still legible as a small label at the task corner.

---

## [BA] Prefix Convention

All content generated by this skill uses the prefix `[BA]` (BPMN Annotator):

- Task `documentation` property: starts with `[BA]\n`
- All `TextAnnotation` text: starts with `[BA]`
- All generated shape `resourceId` values: start with `sid-BA-`
- All generated sequence flow `name` values: start with `[BA] `

This prefix allows the `clean_only` and `clean_and_rerun` modes to safely remove only annotator-generated content without touching human-authored content.

---

## Output to User

After successful execution, report in chat:

```
BPMN Annotator — [model title]
Mode: full | Revision: X | Updated: YYYY-MM-DD HH:MM

Layers applied:
  ✓ Task documentation    — 8 tasks documented
  ✓ Color coding          — 3 lanes colored
  ✓ Lane summaries        — 3 annotations added (right of pool)
  ✓ Impact analysis       — 1 annotation added (below pool)
  ✓ Gateway annotations   — 2 gateways annotated
  ✗ Flow labels           — skipped (all flows already labeled)

Open model in Signavio to review:
https://editor.signavio.com/p/hub/model/{model_id}
```

---

## Dictionary Linking — How It Works

Dictionary links make element names **clickable in the Collaboration Hub**. When a user opens a model in the Hub, clicking a linked element shows its glossary definition in the right panel and lists it in the "Dictionary items" section of the Fact Sheet.

### Critical technical facts (learned from production)

- The correct `glossaryLinks` key for BPMN task/lane elements is **`"name"`**, NOT `"title"`
  - `"title"` key only works for Image/custom SVG shapes — do NOT use it for Tasks, Lanes, etc.
  - Using `"name"` key causes the Hub feed to say "Linked a dictionary entry" ✓
  - Using `"title"` key causes "Unlinked a dictionary entry" ✗
- `glossaryLinks` must be embedded **directly in the shape JSON** and the model must be **resubmitted via PUT**
- The `POST /glossary/{id}/link` API registers activity feed entries but does NOT create visible Hub links
- Element types that support `glossaryLinks`: `Task`, `Lane`, `Pool`, `CollapsedPool`, `DataObject`, `ITSystem`, `StartNoneEvent`, `EndNoneEvent`, `EndMessageEvent`, `IntermediateTimerEvent`, `IntermediateMessageEventCatching`, `Exclusive_Databased_Gateway`, `Parallel_Gateway`
- Multi-line element names (`\n` in name) cannot be matched — skip them
- The folder must be **manually published to the Collaboration Hub** via the Process Manager UI (right-click folder → Publish to Hub). The API endpoint `POST /publish/{folder_id}` alone is not sufficient.

---

## Dictionary Linking — Step-by-Step

### Step 1 — Build a name→glossary_id map

Scan the glossary to find IDs for element names in the model:

```python
import sys, io, json, copy
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib import get_auth, fetch_model, submit_model

auth = get_auth()

# Collect all element names from the model
def collect_names(shapes, names):
    STENCIL_SET = {'Task','Lane','Pool','DataObject','ITSystem',
                   'StartNoneEvent','EndNoneEvent',
                   'Exclusive_Databased_Gateway','Parallel_Gateway'}
    for s in shapes:
        sid  = s.get('stencil', {}).get('id', '')
        name = s.get('properties', {}).get('name', '').strip()
        if sid in STENCIL_SET and name and '\n' not in name:
            names.add(name)
        collect_names(s.get('childShapes', []), names)

model, info = fetch_model(auth, model_id)
names = set()
collect_names(model.get('childShapes', []), names)

# Search glossary for matching entries
page = 0; size = 200; glos_map = {}
while True:
    r = auth.session.get(auth.api_base + '/glossary',
                         params={'offset': page * size, 'limit': size})
    data = r.json()
    if not data: break
    for e in data:
        title = e.get('rep', {}).get('title', '')
        gid   = e.get('href', '').split('/')[-1]
        if title in names:
            glos_map[title] = gid
    if len(data) < size: break
    page += 1

print(f"Matched {len(glos_map)}/{len(names)} element names to dictionary entries")
```

### Step 2 — Create missing dictionary entries (if needed)

If elements don't have entries yet, create them:

```python
import urllib.parse

# Entry types by stencil:
# Task          -> ACTIVITY
# Lane/Pool     -> ORGANIZATION
# ITSystem      -> IT_SYSTEM
# DataObject    -> UNDEFINED  (or DATA_OBJECT if available)
# Events/GW     -> UNDEFINED

# Default category (find yours via GET /glossarycategory)
DEFAULT_CATEGORY = '/glossarycategory/815d8eb36046452e8a81b2eacf0722d3'

def create_glossary_entry(auth, title, entry_type, description, language='en_us',
                          category=DEFAULT_CATEGORY, replaced_item_id=None):
    params = {
        'title':       title,
        'type':        entry_type,
        'category':    category,
        'description': description,
        'language':    language,
    }
    if replaced_item_id:
        params['replacedItemIds'] = replaced_item_id   # links translation to original

    r = auth.session.post(
        auth.api_base + '/glossary',
        data=urllib.parse.urlencode(params),
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        timeout=15
    )
    if r.status_code == 200:
        return r.json().get('href', '').split('/')[-1]
    elif r.status_code == 409:
        print(f'  SKIP (already exists): {title}')
        return None  # entry exists — search glossary to get its ID
    else:
        print(f'  ERR {r.status_code}: {title} — {r.text[:80]}')
        return None
```

**Entry type mapping:**

| Stencil | entry_type |
|---------|-----------|
| `Task` | `ACTIVITY` |
| `Lane`, `Pool` | `ORGANIZATION` |
| `ITSystem` | `IT_SYSTEM` |
| `DataObject` | `UNDEFINED` |
| `StartNoneEvent`, `EndNoneEvent` | `UNDEFINED` |
| `Exclusive_Databased_Gateway`, `Parallel_Gateway` | `UNDEFINED` |

### Step 3 — Embed glossaryLinks into shapes and resubmit

```python
STENCIL_SET = {'Task','Lane','Pool','DataObject','ITSystem',
               'StartNoneEvent','EndNoneEvent',
               'Exclusive_Databased_Gateway','Parallel_Gateway'}

def embed_links(shapes, name_map):
    """Recursively embed glossaryLinks into matching element shapes.
    IMPORTANT: use 'name' key — 'title' key does NOT work for BPMN elements."""
    count = 0
    for s in shapes:
        sid  = s.get('stencil', {}).get('id', '')
        name = s.get('properties', {}).get('name', '').strip()
        if sid in STENCIL_SET and name and '\n' not in name:
            glos_id = name_map.get(name)
            if glos_id:
                s['glossaryLinks'] = {'name': [f'/glossary/{glos_id}']}  # ← 'name' key!
                count += 1
        count += embed_links(s.get('childShapes', []), name_map)
    return count

model, info = fetch_model(auth, model_id)
model = copy.deepcopy(model)
n = embed_links(model.get('childShapes', []), glos_map)
rev, updated = submit_model(auth, model_id, model, info,
                             comment='Dictionary: embed glossaryLinks')
print(f'{n} links embedded  rev={rev}  updated={updated}')
```

### Step 4 — Create ES/DE translation entries (optional)

```python
TRANSLATIONS = [
    # (en_id, en_name, es_title, es_desc, de_title, de_desc)
    ('554ef82cdca64b2aa2235f684b9a35ad', 'IT Department',
     'Departamento de TI', 'Unidad responsable de sistemas y proyectos de TI.',
     'IT-Abteilung',       'Organisationseinheit fuer IT-Systeme und -Projekte.'),
    # ... add more as needed
]

def get_entry_meta(auth, gid):
    """Get type and category from an existing EN entry."""
    r = auth.session.get(auth.api_base + '/glossary/' + gid)
    rep = next((x for x in r.json() if x.get('rel') == 'info'), {}).get('rep', {})
    return rep.get('type', 'UNDEFINED'), rep.get('category', DEFAULT_CATEGORY)

es_map = {}  # en_name -> es_glos_id
de_map = {}  # en_name -> de_glos_id

for en_id, en_name, es_title, es_desc, de_title, de_desc in TRANSLATIONS:
    if es_title == de_title == 'CRM':   # same term — reuse EN entry
        es_map[en_name] = de_map[en_name] = en_id
        continue

    etype, ecat = get_entry_meta(auth, en_id)

    es_id = create_glossary_entry(auth, es_title, etype, es_desc,
                                   language='es_es', category=ecat,
                                   replaced_item_id=en_id)
    de_id = create_glossary_entry(auth, de_title, etype, de_desc,
                                   language='de_de', category=ecat,
                                   replaced_item_id=en_id)
    if es_id: es_map[en_name] = es_id
    if de_id: de_map[en_name] = de_id
```

Then build native-language maps and embed into ES/DE models the same way as Step 3, using the native element names as keys and the ES/DE glossary IDs as values.

**Note on 409 errors:** If `create_glossary_entry` returns 409, the entry already exists. Search the glossary with a term filter to retrieve its ID:

```python
# Find existing entry by title
r = auth.session.get(auth.api_base + '/glossary', params={'limit': 500})
for e in r.json():
    if e.get('rep', {}).get('title') == es_title:
        es_id = e.get('href', '').split('/')[-1]
        break
```

### Step 5 — Publish models to Collaboration Hub

```python
# Publish individual models
for mid in model_ids:
    r = auth.session.post(auth.api_base + f'/publish/{mid}',
                          headers={'Content-Type': 'application/x-www-form-urlencoded'},
                          timeout=15)
    print(f'  publish {mid[:8]}: {r.status_code}')
```

**To publish the folder itself to the Hub:** The API alone (`POST /publish/{folder_id}`) is not sufficient. The user must:
1. Open Signavio Process Manager
2. Right-click the folder
3. Select **"Publish to Hub"** or **"Share"**

Once the folder is published, all models inside it with `glossaryLinks` embedded will show dictionary items in the Collaboration Hub Fact Sheet.

### Step 6 — Verify

```python
# Verify links are embedded correctly
model, _ = fetch_model(auth, model_id)

def check_links(shapes):
    linked, missing = [], []
    for s in shapes:
        sid  = s.get('stencil', {}).get('id', '')
        name = s.get('properties', {}).get('name', '').strip()
        if sid in STENCIL_SET and name and '\n' not in name:
            gl = s.get('glossaryLinks', {})
            if gl.get('name'):
                linked.append(name)
            else:
                missing.append(f'[{sid}] {name}')
        check_links(s.get('childShapes', []))
    return linked, missing

linked, missing = check_links(model.get('childShapes', []))
print(f'Linked: {len(linked)}  Missing: {len(missing)}')
for m in missing: print(f'  MISS {m}')
```

---

## Dictionary Linking — Using the Reusable Scripts

Pre-built scripts live in `skills/bpmn-annotator/temp/`. They can be re-run for any new set of models by updating the `MODELS` list and `GLOS_MAP`.

| Script | Purpose |
|--------|---------|
| `temp/embed_glossary_links.py` | Embed `glossaryLinks` into all Maria Playground models (EN, ES, DE). Edit `MODELS` list to add new models. |
| `temp/fix_es_de_links.py` | Recreate ES/DE glossary entries when they're missing and embed into ES/DE models. |
| `temp/link_via_api.py` | Register links via `/glossary/{id}/link` API (creates feed entries — use `embed_glossary_links.py` instead for Hub visibility). |

To apply dictionary links to a **new model**:
1. Add it to the `MODELS` list in `embed_glossary_links.py` with the appropriate map (GLOS_MAP for EN, ES_MAP for ES, DE_MAP for DE)
2. If the model has element names not yet in the map, add them to the appropriate map (first creating the glossary entry if needed)
3. Run `python skills/bpmn-annotator/temp/embed_glossary_links.py`
4. Publish the model: `POST /publish/{model_id}`

---

## Dictionary Linking — Creating a Full Multi-Language Set from Scratch

Use this when working with a **new process** that has no dictionary entries yet. The complete workflow:

### Step A — Duplicate source model into target folder

```python
import json, urllib.parse, copy
from lib import get_auth, fetch_model

auth = get_auth()
SRC_MODEL   = '<source_model_id>'
DEST_FOLDER = '<target_folder_id>'

model, info = fetch_model(auth, SRC_MODEL)
payload = urllib.parse.urlencode({
    'name':      info['name'] + ' (copy)',
    'parent':    '/directory/' + DEST_FOLDER,
    'namespace': info.get('namespace', 'http://b3mn.org/stencilset/bpmn2.0#'),
    'type':      info.get('type', 'Business Process Diagram (BPMN 2.0)'),
    'comment':   'Duplicated for dictionary linking',
    'json_xml':  json.dumps(copy.deepcopy(model)),
})
r = auth.session.post(auth.api_base + '/model', data=payload,
                      headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=30)
new_mid = r.json()['href'].split('/')[-1]
print(f'New model: {new_mid}')
```

**To find a folder ID**, list the Shared documents directory:

```python
r = auth.session.get(auth.api_base + '/directory/b39e1bfcef0a43ab8cbdbb27adc6f8cf')
for item in r.json():
    if item.get('rel') == 'dir':
        print(item['rep'].get('name'), item['href'].split('/')[-1])
```

### Step B — Inventory all named elements

```python
STENCIL_SET = {
    'Task', 'Lane', 'Pool', 'DataObject', 'ITSystem',
    'StartNoneEvent', 'EndNoneEvent',
    'IntermediateTimerEvent', 'IntermediateMessageEventCatching', 'EndMessageEvent',
    'Exclusive_Databased_Gateway', 'Parallel_Gateway', 'CollapsedPool',
}

def walk(shapes, depth=0):
    for s in shapes:
        sid  = s.get('stencil', {}).get('id', '')
        name = s.get('properties', {}).get('name', '').strip()
        if sid in STENCIL_SET and name:
            print(f"{'  '*depth}[{sid}] {name!r}")
        walk(s.get('childShapes', []), depth+1)

model, info = fetch_model(auth, new_mid)
walk(model.get('childShapes', []))
```

### Step C — Create EN glossary entries for every element

Use the correct category and type per element kind:

```python
# Get glossary categories from tenant
r = auth.session.get(auth.api_base + '/directory')
glos = next(x['rep'] for x in r.json() if x.get('rel') == 'glos')
CAT_ACTIVITY = glos['activitiesCategory']    # Tasks
CAT_ORG      = glos['organizationalUnitCategory']  # Lanes / Pools
CAT_IT       = glos['itSystemsCategory']     # IT Systems
CAT_DOC      = glos['documentsCategory']     # Data Objects
CAT_STATE    = glos['stateCategory']         # Events

# Entry type + category by stencil
STENCIL_META = {
    'Task':                        ('ACTIVITY',     CAT_ACTIVITY),
    'Lane':                        ('ORGANIZATION', CAT_ORG),
    'Pool':                        ('ORGANIZATION', CAT_ORG),
    'CollapsedPool':               ('ORGANIZATION', CAT_ORG),
    'ITSystem':                    ('IT_SYSTEM',    CAT_IT),
    'DataObject':                  ('DOCUMENT',     CAT_DOC),
    'StartNoneEvent':              ('STATE',        CAT_STATE),
    'EndNoneEvent':                ('STATE',        CAT_STATE),
    'IntermediateTimerEvent':      ('STATE',        CAT_STATE),
    'IntermediateMessageEventCatching': ('STATE',   CAT_STATE),
    'EndMessageEvent':             ('STATE',        CAT_STATE),
    'Exclusive_Databased_Gateway': ('ORGANIZATION', CAT_ORG),
    'Parallel_Gateway':            ('ORGANIZATION', CAT_ORG),
}

ENTRIES = [
    # (element_name, stencil_id, description_EN)
    ('MyStore Inc.',  'Pool',  'The company responsible for managing the payment and order fulfilment process.'),
    # ... add all elements
]

en_map = {}
for (title, stencil, desc) in ENTRIES:
    etype, ecat = STENCIL_META[stencil]
    payload = urllib.parse.urlencode({
        'title': title, 'type': etype, 'category': ecat,
        'description': desc, 'language': 'en_us',
    })
    r = auth.session.post(auth.api_base + '/glossary', data=payload,
                          headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=15)
    if r.status_code == 200:
        gid = r.json()['href'].split('/')[-1]
        en_map[title] = gid
        print(f'  OK  {title}  {gid[:8]}')
    elif r.status_code == 409:
        # Entry exists — retrieve ID via search
        sr = auth.session.get(auth.api_base + '/glossary',
                              params={'filter': title[:20], 'limit': 200})
        found = [x for x in sr.json() if x.get('rep', {}).get('title') == title]
        if found:
            gid = found[0]['href'].split('/')[-1]
            en_map[title] = gid
            print(f'  409 {title} (found existing: {gid[:8]})')
```

**Important:** When a 409 is returned, the entry **already exists** but may return 404 on direct GET (tenant permission quirk). Always retrieve via search — do not skip these entries.

### Step D — Embed EN links and resubmit

```python
from lib import submit_model

def embed_links(shapes, name_map):
    count = 0
    for s in shapes:
        sid  = s.get('stencil', {}).get('id', '')
        name = s.get('properties', {}).get('name', '').strip()
        if sid in STENCIL_SET and name and '\n' not in name:
            gid = name_map.get(name)
            if gid:
                s['glossaryLinks'] = {'name': [f'/glossary/{gid}']}  # ← 'name' key!
                count += 1
        count += embed_links(s.get('childShapes', []), name_map)
    return count

model, info = fetch_model(auth, new_mid)
model = copy.deepcopy(model)
n = embed_links(model.get('childShapes', []), en_map)
rev, updated = submit_model(auth, new_mid, model, info,
                            comment='Dictionary: embed glossaryLinks')
print(f'{n} links embedded  rev={rev}  updated={updated}')
```

### Step E — Duplicate and translate to another language

```python
JP_NAMES = {
    'MyStore Inc.': 'マイストア株式会社',
    # ... all element names
}

def rename_shapes(shapes, name_map):
    for s in shapes:
        name = s.get('properties', {}).get('name', '').strip()
        if name in name_map:
            s['properties']['name'] = name_map[name]
        rename_shapes(s.get('childShapes', []), name_map)

model, info = fetch_model(auth, new_mid)  # fetch EN model as base
jp_model = copy.deepcopy(model)
rename_shapes(jp_model.get('childShapes', []), JP_NAMES)

payload = urllib.parse.urlencode({
    'name':      '支払いプロセス',   # translated process name
    'parent':    '/directory/' + DEST_FOLDER,
    'namespace': 'http://b3mn.org/stencilset/bpmn2.0#',
    'type':      'Business Process Diagram (BPMN 2.0)',
    'comment':   'Japanese translation',
    'json_xml':  json.dumps(jp_model),
})
r = auth.session.post(auth.api_base + '/model', data=payload,
                      headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=30)
jp_mid = r.json()['href'].split('/')[-1]
```

### Step F — Create translation entries and embed into translated model

```python
JP_ENTRIES = [
    # (jp_title, stencil, jp_description, en_element_name)
    ('マイストア株式会社', 'Pool', '注文と支払いプロセスを管理する企業。', 'MyStore Inc.'),
    # ...
]

jp_map = {}
for (jp_title, stencil, jp_desc, en_name) in JP_ENTRIES:
    en_id  = en_map[en_name]
    etype, ecat = STENCIL_META[stencil]
    payload = urllib.parse.urlencode({
        'title': jp_title, 'type': etype, 'category': ecat,
        'description': jp_desc, 'language': 'ja_jp',
        'replacedItemIds': en_id,   # links translation to EN entry
    })
    r = auth.session.post(auth.api_base + '/glossary', data=payload,
                          headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=15)
    if r.status_code == 200:
        jp_map[jp_title] = r.json()['href'].split('/')[-1]

# Embed JP links into JP model
jp_model_data, jp_info = fetch_model(auth, jp_mid)
jp_model_data = copy.deepcopy(jp_model_data)
n = embed_links(jp_model_data.get('childShapes', []), jp_map)
rev, updated = submit_model(auth, jp_mid, jp_model_data, jp_info,
                            comment='Dictionary: embed Japanese glossaryLinks')
print(f'{n} JP links embedded  rev={rev}  updated={updated}')
```

**Supported `language` values** (pass the friendly name to `--language`; the annotator resolves the SPM code):

| Language | SPM Code | Notes |
|----------|----------|-------|
| English | `en_us` | Default source language |
| Spanish | `es_es` | |
| German | `de_de` | |
| French | `fr_fr` | |
| Japanese | `ja_jp` | |
| Portuguese (Brazil) | `pt_br` | |
| Simplified Chinese | `zh_cn` | Verify with tenant admin |
| Traditional Chinese | `zh_tw` | Verify with tenant admin |
| Dutch | `nl_nl` | Verify with tenant admin |
| Italian | `it_it` | Verify with tenant admin |
| Korean | `ko_kr` | Verify with tenant admin |
| Russian | `ru_ru` | Verify with tenant admin |
| Polish | `pl_pl` | Verify with tenant admin |
| Swedish | `sv_se` | Verify with tenant admin |
| Turkish | `tr_tr` | Verify with tenant admin |
| Arabic | `ar_sa` | Verify with tenant admin |
| Czech | `cs_cz` | Verify with tenant admin |
| Hungarian | `hu_hu` | Verify with tenant admin |
| Danish | `da_dk` | Verify with tenant admin |
| Finnish | `fi_fi` | Verify with tenant admin |
| Norwegian | `nb_no` | Verify with tenant admin |
| Thai | `th_th` | Verify with tenant admin |

The first 6 (English through Portuguese) are confirmed in the SPM REST API.
The remaining codes follow SAP's standard locale convention — verify with your Signavio tenant admin before using them for the first time.

---

## Dictionary Linking — Troubleshooting

### ES/DE entries return 404 on direct GET but exist in the tenant

**Symptom:** Model shows only 1 dictionary entry (e.g. CRM) despite all others being embedded. Direct `GET /glossary/{id}` returns 404 for all ES/DE IDs.

**Cause:** Translation entries created by other users or sync scripts may have restricted visibility. Direct GET fails but the entries exist.

**Fix:** Retrieve IDs via search instead of direct GET:

```python
# Instead of: GET /glossary/{id}  (returns 404)
# Use:
r = auth.session.get(auth.api_base + '/glossary',
                     params={'filter': title[:20], 'limit': 200})
found = [x for x in r.json() if x.get('rep', {}).get('title') == es_title]
if found:
    gid = found[0]['href'].split('/')[-1]
```

Then re-embed with the correct IDs via `embed_links()` + `submit_model()`.

### glossaryLinks embedded but nothing shows in Collaboration Hub

1. Verify key is `"name"` not `"title"` — fetch the model and inspect `s['glossaryLinks']`
2. Verify the folder is published in the Hub (Process Manager → right-click folder → Publish to Hub)
3. Hard-refresh the browser in the Hub (Ctrl+Shift+R)
4. Check the model revision feed — look for "Linked a dictionary entry" (good) vs "Unlinked a dictionary entry" (wrong key)

---

## Processed Models Catalogue

All models in **Maria Playground** (`a731acfb31ad46dd81cf277aa9a66583`) that have had dictionary linking applied:

### Payroll Data Alert Handling Set

| Model | Model ID | Language | Badges | Links | Dictionary Map |
|-------|----------|----------|--------|-------|---------------|
| Payroll Data Alert Handling (copy) | `96946c6a40ab4e0eb57f2c386142f689` | EN | — | — | Source only |
| Departamento de Nómina | `d5d14c5a056a44768dcf960d3b9e21c6` | ES | 6 | 12 | ES_MAP_PAYROLL |
| Payroll Data Alert Handling (copy) - Spanish | `407543a9285e43c5925f97104abef719` | ES | 6 | 12 | ES_MAP_PAYROLL |

**Glossary entry IDs for Payroll Process (EN):**

```python
GLOS_MAP_PAYROLL_EN = {
    'Payroll Department':                                   '15b0f652...',  # Pool
    'Payroll Agent':                                        'da355d92...',  # Lane
    'Align with line manager or employee':                  'f3b80f8e...',
    'Align with source system administrator':               'ba358846...',
    'Assess alert':                                         'b09dfc77...',
    'Check if data needs to be updated in source system':   '1de9c637...',
    'Correct payroll-specific data':                        '09b565cd...',
    'Provide comment and close alert':                      'b71e3b9c...',
    'Does the alert require a data change?':                'fce51f94...',
    'Does the data need to be updated in the source system?': 'f7e29fc7...',
    'Start':                                                'b9a1a18b...',
    'End':                                                  'bb49b536...',
}

ES_MAP_PAYROLL = {
    'Departamento de Nómina':                   '0de46c0a...',  # Pool
    'Agente de Nómina':                          'ade3eb79...',  # Lane
    'Alinear con jefe o empleado':               '3651074c...',
    'Alinear con admin. del sistema fuente':     '29a3e2d8...',
    'Evaluar alerta':                            '2a5a2acc...',
    'Verificar datos en sistema fuente':         'eedd97f0...',
    'Corregir datos de nómina':                  '73a271b6...',
    'Comentar y cerrar alerta':                  'e28e3f85...',
    '¿La alerta requiere cambio de datos?':      '962918ef...',
    '¿Hay que actualizar en el sistema fuente?': '4dce47bc...',
    'Inicio':                                    '84360bfd...',
    'Fin':                                       '87456970...',
}
```

---

### IT Requirements Process Set

| Model | Model ID | Language | Links | Dictionary Map |
|-------|----------|----------|-------|---------------|
| IT Project Requirements Capture | `ec68bc0206184c5ca1e957843566e5ea` | EN | 15 | GLOS_MAP (EN) |
| IT Project Requirements Capture (copy) | `ca05ed0379d440a798c259da6f460c82` | EN | 15 | GLOS_MAP (EN) |
| New Employee Onboarding | `2c72f43e8ae845cc8f86e90b809b2829` | EN | 4 | GLOS_MAP (EN) |
| New Employee Onboarding (copy) | `343aa4d42246435bab79772c9cc3d1ce` | EN | 4 | GLOS_MAP (EN) |
| Captura de Requisitos de Proyecto de TI | `7d9bb801d1f041929576ad96ea27ed72` | ES | 15 | ES_MAP |
| Erfassung von IT-Projektanforderungen | `b2a734eea3184bc798ee26ceb317529a` | DE | 15 | DE_MAP |
| IT Project Requirements Capture - French | `0f7f0a3656f741658b16d6d1b2935e14` | FR | 13 | FR_MAP (13/15; CRM+ABC keep EN links) |

**Glossary entry IDs for IT Requirements (EN):**

```python
GLOS_MAP_IT_REQUIREMENTS = {
    'IT Department':                               '554ef82cdca64b2aa2235f684b9a35ad',
    'Business Analyst':                            'aefc9f9b937944099e1c570d8cfe8cfb',
    'Process Expert':                              'de3d0a9c885f4ac2aaa70bce474203ab',
    'Document requirements in CRM':                'e398648bb85f4444957321a997145b9b',
    'Identify business requirements':              'c34a781a586c488da2d3ef534e00c4f5',
    'Review documented requirements':              '7c500cb1062d4a90850cbb85c0585246',
    'Refine requirements with requester':          '077538d063aa4d1f96df87c8a9b03deb',
    'Business Requirements':                       '0d5f0890f56c49f498941908113e4b02',
    'CRM':                                         '2e04f02c1dff4350871abe0823511dd8',
    'IT Project Started':                          '953bbd836c0448d9bcf0546c15b44211',
    'Requirements Finalized':                      '2a37525bfa914a4a8d6f0916eaa229ec',
    'Are clarifications needed on requirements?':  '168a2225d8414dbca0f3756471f17362',
    'ABC Company GmbH':                            '569c700ee3a34a4886e101abca88dec2',
    'HR Department':                               'ac244edefdae48e1906f84b29fa2ea04',
    'Line Manager':                                '0606d91e66ff4afeb5c0f05596d64753',
}
# ES and DE maps in temp/embed_glossary_links.py
```

**Glossary entry IDs for IT Requirements (FR) — `fr_fr` translations:**

```python
GLOS_MAP_IT_REQUIREMENTS_FR = {
    'Service IT':                                    'cd8870c697d54dd1821a73e719b0f963',
    'Analyste Metier':                               '33ad993d05dc4eeb8881c26aeed9eea8',
    'Expert Processus':                              '63a9eb24bfba472b8913d40209834a48',
    'Documenter les exigences dans CRM':             'abc323073fdd4815980cd313cc3f76aa',
    'Identifier les exigences metier':               '6b5def3735ff4a8185f8bd4565ddfa28',
    'Reviser les exigences documentees':             'c0dae0082c7b4a2a9229535ab107a8ca',
    'Affiner les exigences avec le demandeur':       '31836f085f0d4b4ab0d2c62490ca490c',
    'Exigences Metier':                              '58be26fc943c4c8b861b3344b95a78b3',
    'Projet IT demarre':                             '6de740b6dbf748d097bfb3c499bd4c98',
    'Exigences finalisees':                          '895cb5de5dfb40f0afb89dfda35584f2',
    'Des clarifications sont-elles necessaires ?':   '8d346b436d434f8cb318ef6859888aec',
    'Departement RH':                                'df12d20e5445453c9f97fd71769d5f02',
    'Responsable Hierarchique':                      '6a14d57ce09a441db3370c7b5b3121e9',
    # CRM and ABC Company GmbH: no FR entries — linked to EN IDs
}

### Delivery / Order Process Set

| Model | Model ID | Language | Links | Dictionary Map |
|-------|----------|----------|-------|---------------|
| Order delivery process | `a841aff7fb5b46b59600aed5b236aeae` | EN | 13 | GLOS_MAP (EN) |
| Delivery of Raw Material | `053cc44988a848c9b0acaab17d9c159d` | EN | 9 | GLOS_MAP (EN) |

**Glossary entry IDs for Delivery / Order (EN, shared with other maps):**

```python
GLOS_MAP_DELIVERY = {
    'Check stock availability & pick items':         '207309a5e71140688ccd5b1d26d8caf7',
    'Customer Experience Team':                      '603e1655014f488e95d2ae7c7c1f4806',
    'Customer places order online':                  'c877eadf99d041c3b72be4fdf74ae576',
    'Deliver raw material':                          'b5a9bc0f9fca4396b731d1cb2f16084e',
    'Delivery Receipt':                              '0086b54be42e493e9bbfb05b2a0319b8',
    'Delivery Started':                              '930e6f756e924000aa6f0489dad72d17',
    'Delivery Tracking System':                      '6be45e9bf46b4f489bed323fe2ffd494',
    'Delivery Worker':                               'd7cfce2b42864936b9d29c557896b045',
    'Express delivery selected?':                    '8b867ce8c3204454824fbc66d2d4bc2d',
    'Fulfillment & Logistics':                       '12ca7b78de7b446d9ca4720b00afc9c3',
    'Generate VAT-compliant invoice (19% MwSt)':     'af4c8268d2f144beb88b1cfa546c83c2',
    'Hand over parcel to DHL courier':               '9cac913942c9400388eb74e5a3e778f3',
    'Logistics Department':                          'b26e1b4651944d2899948b0af863e722',
    'Order dispatched – DHL tracking active':        'debcfa5907d24c819fa089ccdd2152d4',
    'Pack & label parcel – DHL Express (next day)':  'afa8b050ac6f41b4aa968f381dd6139f',
    'Pack & label parcel – DHL Standard (2–3 days)': '422751100ddb4d00a414c284ca19de97',
    'Receipt Management System':                     '1fb075df81774a9db5bb2c58c41aa20e',
    'Receipt Received':                              '657cf087dfcd401981cc9babff92deb4',
    'Receive receipt note':                          'bb55d0567162402994a18416f912703e',
    'Send invoice PDF to customer via email':         'c33278be33ca4fc59bd787d3abf68451',
    'Validate payment & send order confirmation (incl. Widerrufsbelehrung)': 'c7f3c475ecd9470c9f441d4baa19ae83',
}
```

### Payment Process Set

| Model | Model ID | Language | Links | Notes |
|-------|----------|----------|-------|-------|
| payment process (copy) | `3ccabcf77620442b804677f19c8887a5` | EN | 18 | Duplicated from Ariel playground (`253191de347c4b27991d06095553ae58`) |
| 支払いプロセス | `fe198d1ade1c4f429141c3705d3d650e` | JA | 18 | Full Japanese translation with JP glossary entries |

**Glossary entry IDs for Payment Process (EN):**

```python
GLOS_MAP_PAYMENT_EN = {
    'MyStore Inc.':           'c8a9a28b7ed7446e847aec4dbc42b2d0',
    'Customer AA':            '2991a6535c0149d28ab7d6ab171b2643',
    'finance':                '019ddb9ff3ff4f24b6cac3e582b03684',
    'Create invoice':         'f82647c25c3847648a545f3bef291132',
    'Send invoice':           'af8b26feca774491a81892ffab7de411',
    'Check payment':          '399dbfeb9763459e99a6de5f8c72e417',
    'Send payment reminder':  '6221a6bda1b049e4997c60424f7bfde4',
    'Confirm payment 1':      '190e6d1888194385b5120cd79dc6daac',
    'Cancel order':           'a1ec11327c434e9da48770f899c9db94',
    'order system':           '4319fcecdfa247f88928c563fef1f1b9',
    'invoice':                '997a54956cd048438a596291b0e4c5d8',
    'cancellation':           '8ff3773c9baf44a5bf5a221db4d3695e',
    'Payment process started':'e5e9102c929547db8d9d8e23fcf288b0',
    'payment received':       'f798fae2a4a348a4802a21aa0ee691a9',
    '7 days waited':          'a405a1da444240ae8c3dbc92a5b87a37',
    'order paid':             '38f6630458b74dd5bbb4e0f381711726',
    'order cancelled':        '62ff329e828a40e090848cf6b6c75545',
}

GLOS_MAP_PAYMENT_JP = {
    'マイストア株式会社':         '3ea31cba...',  # see temp/ scripts for full IDs
    '顧客AA':                    '7c31720c...',
    '財務部門':                   'ef62825e...',
    '請求書を作成する':            '10fd1960...',
    '請求書を送付する':            'c9c49032...',
    '支払いを確認する':            '656e8b69...',
    '支払いリマインダーを送る':     '147bbb12...',
    '支払いを承認する':            '4a433ef6...',
    '注文をキャンセルする':         'b1bbf7cf...',
    '注文システム':                '156b9e48...',
    '請求書':                     '27b17c5b...',
    'キャンセル通知書':             'd6904ec6...',
    '支払いプロセス開始':           'b49f65e1...',
    '支払い受領':                  'bba07629...',
    '7日間待機':                  'b7dfa73e...',
    '注文支払い完了':               'a3b8883a...',
    '注文キャンセル済み':           '37083c07...',
}
```

### Key Folder IDs

| Folder | ID |
|--------|----|
| Shared documents (root) | `b39e1bfcef0a43ab8cbdbb27adc6f8cf` |
| Maria Playground | `a731acfb31ad46dd81cf277aa9a66583` |
| Ariel playground | `575a4558aa3e491886e898e2fbce5585` |

---

| Error | Action |
|---|---|
| Model not found | Ask user to verify the URL/ID |
| Auth failure | Run TokenManager re-auth, then retry |
| Timeout on PUT | Retry once with `timeout=180` |
| Model has no lanes | Run in `documentation_only` + `impact_only` mode |
| Model already has `[BA]` content | Ask user: "Annotations already exist. Run `clean_and_rerun` to refresh?" |

---

## Model Translation

### Overview

The translation capability duplicates an existing BPMN model and produces a fully
translated copy in the target language. The original model is **never modified by
default** — `translate_duplicate` always creates a new model first.

Three modes:
- `translate_dry_run` — fetch and inspect, print translation prompt, no writes
- `translate_duplicate` — safe default: duplicate → translate copy → submit
- `translate_in_place` — overwrite original (destructive; requires `--confirm`)

### Step-by-Step Translation Workflow

#### Step 1 — Dry run (optional but recommended)

```python
import sys, subprocess
result = subprocess.run([
    "python", r"skills\bpmn-annotator\annotator.py",
    "--url", model_url_or_id,
    "--mode", "translate_dry_run",
    "--language", "Spanish",
    "--output", r"skills\bpmn-annotator\temp\translate_prompt.txt",
], capture_output=True, text=True)
print(result.stdout)
```

Or run directly in the terminal:
```powershell
python skills/bpmn-annotator/annotator.py --url "MODEL_URL" --mode translate_dry_run --language Spanish --output skills/bpmn-annotator/temp/translate_prompt.txt
```

The dry run prints (or saves to file):
- Element count by type
- All text to be translated, grouped by element type
- The full translation prompt

#### Step 2 — Generate translations

Read `translate_prompt.txt` and produce a `translations.json`:

```python
from skills.bpmn_annotator.lib import (
    get_auth, fetch_model, parse_model,
    collect_translatable_fields, build_translation_prompt,
)
import json

auth = get_auth()
model, info = fetch_model(auth, model_id)
parsed = parse_model(model)

prompt = build_translation_prompt(parsed, model, target_language="Spanish")
# Paste prompt to Claude, receive JSON → save to translations.json
```

As Claude, you can generate the translations yourself directly from the prompt output.
Save the result to `skills/bpmn-annotator/temp/translations.json`.

#### Step 3 — Duplicate and apply

```powershell
python skills/bpmn-annotator/annotator.py --url "MODEL_URL" --mode translate_duplicate --language Spanish --content skills/bpmn-annotator/temp/translations.json
```

Or via Python API:

```python
import copy, json
from pathlib import Path
from skills.bpmn_annotator.lib import (
    get_auth, fetch_model, parse_model, submit_model,
    apply_translations, duplicate_model,
)

auth                = get_auth()
model, info         = fetch_model(auth, model_id)
translations        = json.loads(Path("translations.json").read_text())

translated          = copy.deepcopy(model)
apply_translations(translated, translations)

new_model_id, new_info = duplicate_model(
    auth, translated, info,
    new_name=f"{info['name']} - Spanish",
)
submit_model(auth, new_model_id, translated, new_info,
             comment="BPMN Translator: Spanish translation")
print(f"New model: https://editor.signavio.com/p/hub/model/{new_model_id}")
```

---

### What Gets Translated

| Element | JSON path |
|---------|-----------|
| Pool / model title | `childShapes[pool].properties.name` |
| Lane names | `childShapes[pool].childShapes[lane].properties.name` |
| Task names | `properties.name` |
| Task documentation | `properties.documentation` |
| Gateway labels | `properties.name` |
| Event names | `properties.name` |
| Sequence flow labels | `properties.name` |
| TextAnnotation content | `properties.text` |

The SPM folder entry name (from `info["name"]`) is set to
`{original name} - {language}` when creating the duplicate.

---

### What Is Never Translated (Protected Terms)

The following are always preserved exactly as-is:

**SAP ecosystem:** SAP, S/4HANA, SuccessFactors, Ariba, Fieldglass, Concur, Signavio, ARIS, Celonis

**SaaS tools:** Jira, Confluence, GitHub, GitLab, Slack, Teams, SharePoint, ServiceNow, Salesforce, Workday

**Office tools:** Excel, Word, PowerPoint, Outlook

**Standards:** BPMN, DMN, CMMN, ERP, CRM, SLA, KPI, OKR, API, REST, JSON, XML, SSO, LDAP, SCIM

**Role abbreviations:** HR, IT, PM, LM, CEO, CFO, CTO, CIO, CHRO, CPO, COO, VP

**Annotator markers:** `[BA]`, `[BA#]` (prefixes preserved; content after them is translated)

**Always preserved:** BPMN IDs, layout coordinates, colors, bounds, URLs, emails, codes

---

### Translation Quality Rules

1. Use professional business process language for the target locale.
2. Keep task names ≤ 40 characters; use **Verb + Object** format.
3. Maintain a consistent terminology dictionary throughout the model — identical
   source terms must map to identical target terms.
4. Preserve business meaning over literal word-for-word translation.
5. For gateway labels, translate the decision question (e.g. "Documents complete?").
6. Preserve the `[BA]` prefix on annotator-generated content — translate only the text
   that follows it.
7. Flow labels should be brief conditions ("Yes" / "No", "Approved", "Rejected").

---

### Safety Rules for Translation

1. **Never translate the original model by default** — always use `translate_duplicate`.
2. `translate_in_place` must only be run when the user explicitly requests it AND
   provides the `--confirm` flag or confirms verbally.
3. Do not alter BPMN structure (flows, gateways, task count, layout) during translation.
4. Do not change BPMN IDs or `resourceId` values.
5. Do not remove or modify `[BA]` annotator content — translate it but preserve structure.

---

### translations.json Format

Claude should return (and the CLI accepts) this JSON structure:

```json
{
  "target_language": "Spanish",
  "source_language": "English",
  "model_title": "Proceso de Incorporación de Empleados",
  "lanes": {
    "sid-LANE-ID-1": "Recursos Humanos",
    "sid-LANE-ID-2": "TI"
  },
  "tasks": {
    "sid-TASK-ID-1": "Enviar formulario de solicitud",
    "sid-TASK-ID-2": "Revisar documentos"
  },
  "task_docs": {
    "sid-TASK-ID-1": "[BA]\nDescripción: El empleado completa..."
  },
  "gateways": {
    "sid-GW-ID-1": "¿Documentos completos?"
  },
  "events": {
    "sid-EVENT-ID-1": "Proceso iniciado",
    "sid-EVENT-ID-2": "Proceso completado"
  },
  "flows": {
    "sid-FLOW-ID-1": "Sí",
    "sid-FLOW-ID-2": "No"
  },
  "annotations": {
    "sid-BA-LANE-xyz": "[BA] Recursos Humanos\nResponsabilidades: ..."
  }
}
```

All sections except `target_language`, `source_language`, and `model_title` are optional —
omit any section with no entries. Keys are `resourceId` values copied verbatim from the
translation prompt.

---

### Example Claude Prompts for Translation

```
Duplicate this Signavio model into Spanish: https://editor.signavio.com/p/hub/model/abc123

Create a German version of this BPMN model: [URL]

Dry run translation to Japanese without updating Signavio: [URL]

Translate only labels, not documentation: [URL] --language French

Duplicate and translate model, preserving SAP and IT terms: [URL] --language Spanish

Translate this process into French and keep the IT team names unchanged: [URL]
```

---

## SGX Export & Native Multilingual Architecture

### What Is an SGX File?

An `.sgx` file is SAP Signavio's export format — a **ZIP archive** containing:
- `model.json` — the full model JSON as returned by the SPM REST API (same structure used by all annotator functions)
- `model.bpmn` — a BPMN 2.0 XML export of the same model

SGX files are useful for:
- Offline inspection of the JSON structure without hitting the SPM API
- Understanding how SPM encodes native multilingual fields
- Backup before destructive operations
- Sharing models with parties who don't have SPM access

### Exporting an SGX File

```powershell
python skills/bpmn-annotator/annotator.py --url "MODEL_URL" --mode sgx_export
```

The file is saved to `skills/bpmn-annotator/temp/{model_id}.sgx`.

To inspect:
```python
import zipfile, json, pathlib

sgx_path = pathlib.Path("skills/bpmn-annotator/temp/{model_id}.sgx")
with zipfile.ZipFile(sgx_path) as z:
    print(z.namelist())
    model = json.loads(z.read("model.json"))
    bpmn_xml = z.read("model.bpmn").decode("utf-8")

# Inspect top-level properties
for key in model.keys():
    print(key)

# Walk shapes to see multilingual fields
def inspect_names(shapes, depth=0):
    for s in shapes:
        props = s.get("properties", {})
        name = props.get("name", "")
        names_dict = props.get("names")
        if names_dict:
            print("  " * depth + f"[{s['stencil']['id']}] name={name!r} names={names_dict}")
        inspect_names(s.get("childShapes", []), depth + 1)

inspect_names(model.get("childShapes", []))
```

---

### SPM Native Multilingual Architecture

SPM stores multiple language versions **inside a single model** using language sub-dictionaries on each shape's `properties` object:

```json
{
  "stencil": {"id": "Task"},
  "resourceId": "sid-TASK-001",
  "properties": {
    "name": "Check Documents",
    "names": {
      "en_us": "Check Documents",
      "de_de": "Dokumente prüfen",
      "fr_fr": "Vérifier les documents",
      "ja_jp": "書類を確認する"
    },
    "documentation": "[BA] Purpose: ...",
    "documentations": {
      "en_us": "[BA] Purpose: ...",
      "de_de": "[BA] Zweck: ..."
    }
  }
}
```

**Key rules:**
- `properties.name` is the **display name** — what SPM shows by default (usually English)
- `properties.names` is the multilingual dictionary — SPM switches between these based on the UI language setting
- The same structure applies to `documentation` / `documentations`
- Setting a language entry does **not** affect any other language entry — fully non-destructive

**Contrast with `translate_duplicate`:**

| | `translate_duplicate` | `multilingual_native` |
|---|---|---|
| How it works | Creates a separate model per language | Adds a language slot inside the existing model |
| Original untouched? | Yes — original stays in EN | Yes — `name` field is never changed |
| Model count | 1 per language | 1 model for all languages |
| SPM language switcher | N/A — separate model | Works with SPM's built-in language selector |
| Use case | Separate deliverables per language | Enterprise multilingual process catalogue |

---

### multilingual_inspect Mode

Before adding translations, inspect what language fields already exist:

```powershell
python skills/bpmn-annotator/annotator.py --url "MODEL_URL" --mode multilingual_inspect
```

Output example:
```
Multilingual field inspection for: New Employee Onboarding
──────────────────────────────────────────────────────────
Language    Populated    Empty
──────────────────────────────────────────────────────────
en_us       12           0     ← Full (source language)
de_de        8           4     ← Partial (4 tasks missing)
fr_fr        0          12     ← Empty (not started)
ja_jp        0          12     ← Empty (not started)
──────────────────────────────────────────────────────────
Recommendation: Complete de_de, then start fr_fr.
```

---

### multilingual_native Mode — Step by Step

#### Step 1 — Dry run (inspect + build prompt)

```powershell
python skills/bpmn-annotator/annotator.py --url "MODEL_URL" --mode translate_dry_run --language German
```

This prints the source text for all elements. Review the output, then generate translations.

#### Step 2 — Generate the native translations JSON

Use `build_multilingual_native_prompt()` (from `lib/translate.py`) or the dry-run output to create a `translations.json` with this structure:

```json
{
  "target_language": "German",
  "lang_code": "de_de",
  "source_language": "English",
  "mode": "multilingual_native",
  "model_title": "Neuer Mitarbeiter Onboarding",
  "tasks": {
    "sid-TASK-001": "Dokumente prüfen",
    "sid-TASK-002": "Konto einrichten"
  },
  "lanes": {
    "sid-LANE-001": "Personal"
  },
  "task_docs": {
    "sid-TASK-001": "[BA] Zweck: Der HR-Mitarbeiter prüft..."
  },
  "gateways": {
    "sid-GW-001": "Dokumente vollständig?"
  },
  "events": {
    "sid-EVENT-001": "Prozess gestartet",
    "sid-EVENT-002": "Prozess abgeschlossen"
  },
  "flows": {
    "sid-FLOW-001": "Ja",
    "sid-FLOW-002": "Nein"
  }
}
```

Note the `"mode": "multilingual_native"` field — this tells `apply_native_translations()` to
write to `properties.names.de_de` instead of overwriting `properties.name`.

#### Step 3 — Apply

```powershell
python skills/bpmn-annotator/annotator.py --url "MODEL_URL" --mode multilingual_native --language German --content skills/bpmn-annotator/temp/translations.json
```

The model is updated in place — only the `names.de_de` and `documentations.de_de` fields are
written. All other languages and the base `name` field are untouched.

---

### Python API — apply_native_translations

```python
from lib.translate import apply_native_translations, build_multilingual_native_prompt
import json
from pathlib import Path

# Build the prompt
auth = get_auth()
model, info = fetch_model(auth, model_id)
parsed = parse_model(model)

prompt = build_multilingual_native_prompt(parsed, model, "German", "de_de")
# → paste to Claude, receive translations JSON

# Apply
translations = json.loads(Path("translations.json").read_text())
warnings = apply_native_translations(model, translations, lang_code="de_de")

if warnings:
    for w in warnings:
        print(f"WARNING: {w}")

submit_model(auth, model_id, model, info, comment="Native multilingual: add de_de")
```

---



```
skills/bpmn-annotator/
├── SKILL.md            ← This file (Claude instructions)
├── README.md           ← Human documentation
├── annotator.py        ← CLI entry point
├── lib/
│   ├── __init__.py     ← Public API
│   ├── auth.py         ← SPM authentication
│   ├── fetch.py        ← fetch_model(), submit_model()
│   ├── parse.py        ← parse_model()
│   ├── generate.py     ← Annotation prompt builders
│   ├── annotate.py     ← Layer application functions
│   ├── clean.py        ← clean_ba_content()
│   ├── review.py       ← review_model_quality()
│   ├── translate.py    ← build_translation_prompt(), apply_translations()
│   ├── duplicate.py    ← duplicate_model(), create_model()
│   └── constants.py    ← BA_PREFIX, LANE_COLOR_PALETTE, SUPPORTED_MODES
└── temp/               ← Working files (gitignored)
    └── .gitkeep
```

The skill runs entirely in-memory via MCP calls + Python scripts written to `temp/`. No persistent output files are required — the model in SPM is the output.
