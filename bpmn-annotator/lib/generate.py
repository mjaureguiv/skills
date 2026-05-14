"""Content generation for the BPMN Annotator.

These functions build structured prompts that Claude uses to generate
documentation content grounded solely in what the BPMN model contains.

Design:
  - Each function returns a prompt STRING (not the generated content).
  - When running as a Claude Code skill via SKILL.md, Claude itself fills
    in the content after reading the prompt.
  - When running in dry_run mode from CLI, prompts are printed so the user
    can inspect what would be sent to the model.
  - build_full_generation_prompt() combines all layers into a single call
    (preferred for efficiency).

Grounding rules enforced in all prompts:
  - Only reference IT systems explicitly named in task labels.
  - Only reference roles that appear as lane names.
  - Mark any inference with "(inferred)".
  - Never invent steps, decisions, or outputs not visible in the model.
"""
import json
from .constants import BA_PREFIX


def build_full_generation_prompt(parsed: dict) -> str:
    """Build a single combined generation prompt for all annotation layers.

    Claude reads this and returns a JSON object with keys:
        task_docs, lane_summaries, gateway_texts, impact_analysis, phase_headers
    """
    lanes_text = "\n".join(
        f"  Lane '{l['name']}' (id={l['id']}): "
        f"tasks={l['tasks']}, "
        f"gateways={[g['name'] or g['type'] for g in l['gateways']]}"
        for l in parsed["lanes"]
    )

    events_text = ", ".join(
        f"{e['type']} '{e['name']}' (lane: {e['lane_name']})"
        for e in parsed["events"]
    ) or "none"

    gateways_text = "\n".join(
        f"  {g['type']} '{g['name']}' (id={g['id']}, lane={g['lane_name']})"
        for g in parsed["gateways"]
    ) or "  (none)"

    # Only preserve human-authored docs (not BA-generated ones)
    human_docs = {
        t["id"]: t["existing_doc"]
        for t in parsed["tasks"]
        if t["existing_doc"] and not t["existing_doc"].startswith(BA_PREFIX)
    }

    task_list = "\n".join(
        f"  id={t['id']} | name='{t['name']}' | lane='{t['lane_name']}'"
        for t in parsed["tasks"]
    )

    return f"""You are a BPMN documentation expert. Generate structured documentation for this process.

Based ONLY on what the model contains — do not invent steps, systems, or roles.

PROCESS: {parsed['title']}

LANES AND TASKS:
{lanes_text}

TASK LIST (use these exact IDs as keys):
{task_list}

GATEWAYS:
{gateways_text}

EVENTS: {events_text}

EXISTING HUMAN DOCUMENTATION (preserve — do not overwrite):
{json.dumps(human_docs, indent=2) if human_docs else "  (none)"}

OUTPUT — return a single JSON object with these exact keys:

{{
  "task_docs": {{
    "<task_id>": "<documentation text>"
  }},
  "lane_summaries": {{
    "<lane_id>": "<summary text>"
  }},
  "gateway_texts": {{
    "<gateway_id>": "<one-line routing explanation>"
  }},
  "impact_analysis": "<full impact analysis table as a single string>",
  "phase_headers": [
    {{"label": "<phase name>", "ref_task_id": "<first task id in phase>"}}
  ]
}}

FORMATTING RULES:

1. Prefix ALL generated values with {BA_PREFIX} on its own first line.

2. Task documentation (max 8 lines):
   [BA]
   Description: <what this task does, 1-2 sentences>
   Purpose:     <why it matters in the process>
   Inputs:      <what comes in>
   Outputs:     <what is produced or decided>
   Responsible: <lane name>
   Systems:     <only systems explicitly in the task label — else "(inferred)">
   Risks:       <only if clearly implied by the task name or context>

3. Lane summary (max 10 lines):
   [BA] <LANE NAME>
   ══════════════════════════════
    Tasks    <count> (<first task name> to <last task name>)
    Systems  <only if a system name appears in a task label>
    Output   <main deliverable of this lane>
    Role     <brief role description>
   ══════════════════════════════
   <2-line narrative about what this lane contributes to the process>

4. Impact analysis — use this exact table structure:
   [BA] IMPACT ANALYSIS  ·  <process title>
   ══════════════════════════════════════════════════════════════
    IT System              Affected Tasks                   Risk
   ──────────────────────────────────────────────────────────────
    <system>               <task names>              HIGH/MED/LOW
   ══════════════════════════════════════════════════════════════
    Role / Dept            Owns                         Tasks
   ──────────────────────────────────────────────────────────────
    <lane name>            <task names>                  <count>
   ══════════════════════════════════════════════════════════════
    RISK STATEMENT
    HIGH  <highest-risk scenario>
    MED   <medium-risk scenario>
   ══════════════════════════════════════════════════════════════
   If no IT systems are explicitly named, write "(none identified from model labels)"

5. Gateway texts — ONE LINE per gateway:
   [BA] <What condition does this gateway evaluate? e.g. "Approved? Yes -> next / No -> rework">

6. Phase headers — only if there are clear logical phases (e.g. Preparation / Execution / Closure).
   Return [] if the process is linear without distinct business phases.

7. Do NOT invent anything — mark inferences with "(inferred)".
8. If an existing_doc is present (non-BA), include it unchanged as the task_doc value.
"""


def generate_task_documentation(task: dict, process_title: str) -> str:
    """Build a per-task documentation prompt (single task, for selective generation)."""
    return f"""Generate BPMN task documentation for one task.

PROCESS: {process_title}
TASK: '{task['name']}' in lane '{task['lane_name']}'
EXISTING DOC: {task['existing_doc'] or '(none)'}

Return a single documentation text block (no JSON wrapper):

[BA]
Description: <what this task does, 1-2 sentences>
Purpose:     <why it matters>
Inputs:      <what comes in>
Outputs:     <what is produced>
Responsible: {task['lane_name']}
Systems:     <only if system name is explicit in '{task['name']}' — else "(inferred)">
Risks:       <only if clearly implied>

Rules:
- Do NOT invent anything not visible in the task name or lane name
- Mark inferences with "(inferred)"
- Keep under 8 lines
"""


def generate_gateway_explanation(gateway: dict, process_title: str) -> str:
    """Build a per-gateway explanation prompt (single gateway)."""
    return f"""Generate a one-line routing explanation for this BPMN gateway.

PROCESS: {process_title}
GATEWAY TYPE: {gateway['type']}
GATEWAY LABEL: '{gateway['name'] or '(no label)'}'
LANE: '{gateway['lane_name']}'

Return a single line prefixed with [BA]:
[BA] <What decision or condition does this gateway evaluate?>

Rules:
- ONE LINE only
- Only describe routing visible from the gateway name and context
- Example format: "[BA] Contract complete? Yes -> register / No -> request corrections"
"""


def generate_flow_label(flow: dict, process_title: str) -> str:
    """Build a flow label prompt for an unlabeled conditional flow."""
    return f"""Generate a short label for this BPMN sequence flow.

PROCESS: {process_title}
FROM: '{flow['source_name']}' TO: '{flow['target_name']}'
CURRENT LABEL: '{flow['name'] or '(none)'}'

Return a short label (2-5 words) prefixed with [BA]:
[BA] <label>

Rules:
- Only label if the flow represents a conditional path leaving a gateway
- Return empty string if the flow is a simple unconditional continuation
"""


def generate_lane_summary(lane: dict, process_title: str) -> str:
    """Build a per-lane summary prompt."""
    return f"""Generate a structured summary for this BPMN swimlane.

PROCESS: {process_title}
LANE: '{lane['name']}'
TASKS: {lane['tasks']}
GATEWAYS: {[g['name'] or g['type'] for g in lane['gateways']]}

Return the summary text (no JSON wrapper):

[BA] {lane['name'].upper()}
══════════════════════════════
 Tasks    <count> (<first> to <last>)
 Systems  <only if a system name appears explicitly in a task label>
 Output   <main deliverable of this lane>
 Role     <brief role description>
══════════════════════════════
<2-line narrative about what this lane does in the process>

Rules:
- Only name IT systems that appear in task labels
- Keep under 10 lines
"""


def generate_impact_analysis(parsed: dict) -> str:
    """Build the impact analysis prompt for the full process."""
    tasks_by_lane = "\n".join(
        f"  [{l['name']}] {', '.join(l['tasks'])}"
        for l in parsed["lanes"]
    )
    return f"""Generate an impact analysis for this BPMN process.

PROCESS: {parsed['title']}

TASKS BY LANE:
{tasks_by_lane}

Return the analysis as a formatted text block (no JSON):

[BA] IMPACT ANALYSIS  ·  {parsed['title']}
══════════════════════════════════════════════════════════════
 IT System              Affected Tasks                   Risk
──────────────────────────────────────────────────────────────
 <system>               <task names>              HIGH/MED/LOW
══════════════════════════════════════════════════════════════
 Role / Dept            Owns                         Tasks
──────────────────────────────────────────────────────────────
 <lane name>            <task names>                  <count>
══════════════════════════════════════════════════════════════
 RISK STATEMENT
 HIGH  <describe highest-risk scenario>
 MED   <describe medium risk>
══════════════════════════════════════════════════════════════

Rules:
- Only include IT systems explicitly named in task labels
- If none: write "(none identified from model labels)"
- Risk levels: HIGH = single point of failure, MED = delays possible, LOW = isolated impact
"""


def generate_phase_headers(parsed: dict) -> str:
    """Build the phase header generation prompt."""
    task_list = "\n".join(
        f"  [{t['lane_name']}] id={t['id']} name='{t['name']}'"
        for t in parsed["tasks"]
    )
    return f"""Identify logical business phases in this process.

PROCESS: {parsed['title']}

TASKS IN SEQUENCE:
{task_list}

Return a JSON array, or [] if no clear phases exist:
[
  {{"label": "<phase name>", "ref_task_id": "<id of first task in this phase>"}}
]

Rules:
- Only create phases if there are clear logical groupings (e.g. Preparation / Execution / Closure)
- Return [] for linear processes without distinct phases
- Phase labels: 1-3 words
- ref_task_id must be an exact ID from the list above
"""
