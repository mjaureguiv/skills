#!/usr/bin/env python3
"""Create SAP Signavio Customer Journey BPMN model in Signavio Process Manager.

Creates a new swim-lane BPMN model representing the end-to-end SAP Signavio
customer journey: Discover → Evaluate → Purchase → Onboard → Adopt → Expand.

Usage:
    python create_customer_journey.py
"""
import sys
import json
import uuid

sys.path.insert(0, r'c:\Signavio_PM_Agent\skills\bpmn-annotator')
from lib.auth import get_auth
from lib.duplicate import create_model

PARENT_FOLDER = "a731acfb31ad46dd81cf277aa9a66583"  # Maria Playground

# ── Color palette ─────────────────────────────────────────────────────────────
BLUE   = {"bgcolor": "#dae8fc", "bordercolor": "#6c8ebf"}   # Customer
GREEN  = {"bgcolor": "#d5e8d4", "bordercolor": "#82b366"}   # Sales
AMBER  = {"bgcolor": "#fff2cc", "bordercolor": "#d6b656"}   # Platform
PINK   = {"bgcolor": "#f8cecc", "bordercolor": "#b85450"}   # Customer Success

# ── Layout constants ──────────────────────────────────────────────────────────
POOL_X, POOL_Y   = 40, 40
POOL_W, POOL_H   = 2580, 720   # canvas width × height
POOL_HEADER_W    = 30           # left pool label strip
LANE_LABEL_W     = 30           # left lane label strip
LANE_H           = 170          # height of each lane
TASK_W, TASK_H   = 130, 60
EVENT_D          = 30           # start/end event diameter
GW_SIZE          = 40           # gateway diamond size

# Absolute canvas position of lane content area (top-left)
# Pool upperLeft is (POOL_X, POOL_Y).  Lanes are childShapes of pool,
# their bounds are relative to pool upperLeft.
# Lane content X (relative to lane origin): starts after lane label strip.
def abs_x(lane_rel_x):
    return POOL_X + POOL_HEADER_W + lane_rel_x

def abs_y(lane_idx, lane_rel_y):
    return POOL_Y + lane_idx * LANE_H + lane_rel_y

# Task center helpers
def tcx(lane_rel_x):  return abs_x(lane_rel_x + TASK_W // 2)
def tcy(lane_idx):    return abs_y(lane_idx, (LANE_H - TASK_H) // 2 + TASK_H // 2)
def ecx(lane_rel_x):  return abs_x(lane_rel_x + EVENT_D // 2)
def ecy(lane_idx):    return abs_y(lane_idx, (LANE_H - EVENT_D) // 2 + EVENT_D // 2)
def gcx(lane_rel_x):  return abs_x(lane_rel_x + GW_SIZE // 2)
def gcy(lane_idx):    return abs_y(lane_idx, (LANE_H - GW_SIZE) // 2 + GW_SIZE // 2)

# ── Shape builders ────────────────────────────────────────────────────────────
def _sid():
    return "sid-" + uuid.uuid4().hex[:28]

def _task(rid, name, lane_rel_x, colors=None):
    y = (LANE_H - TASK_H) // 2
    c = colors or {}
    return {
        "resourceId": rid,
        "properties": {
            "name": name,
            "documentation": "",
            "bgcolor":     c.get("bgcolor",     "#ffffff"),
            "bordercolor": c.get("bordercolor", "#000000"),
        },
        "stencil":     {"id": "Task"},
        "childShapes": [],
        "outgoing":    [],
        "incoming":    [],
        "bounds": {
            "upperLeft":  {"x": lane_rel_x,          "y": y},
            "lowerRight": {"x": lane_rel_x + TASK_W,  "y": y + TASK_H},
        },
        "dockers": [],
    }

def _event(rid, name, stencil_id, lane_rel_x):
    y = (LANE_H - EVENT_D) // 2
    return {
        "resourceId": rid,
        "properties": {"name": name, "documentation": ""},
        "stencil":     {"id": stencil_id},
        "childShapes": [],
        "outgoing":    [],
        "incoming":    [],
        "bounds": {
            "upperLeft":  {"x": lane_rel_x,           "y": y},
            "lowerRight": {"x": lane_rel_x + EVENT_D,  "y": y + EVENT_D},
        },
        "dockers": [],
    }

def _gateway(rid, name, lane_rel_x):
    y = (LANE_H - GW_SIZE) // 2
    return {
        "resourceId": rid,
        "properties": {"name": name, "documentation": ""},
        "stencil":     {"id": "Exclusive_Databased_Gateway"},
        "childShapes": [],
        "outgoing":    [],
        "incoming":    [],
        "bounds": {
            "upperLeft":  {"x": lane_rel_x,            "y": y},
            "lowerRight": {"x": lane_rel_x + GW_SIZE,   "y": y + GW_SIZE},
        },
        "dockers": [],
    }

def _flow(rid, name, src_id, tgt_id, src_cx, src_cy, tgt_cx, tgt_cy):
    """Sequence flow with two dockers (absolute canvas coords)."""
    return {
        "resourceId": rid,
        "properties": {"name": name},
        "stencil":     {"id": "SequenceFlow"},
        "childShapes": [],
        "incoming":    [{"resourceId": src_id}],
        "outgoing":    [{"resourceId": tgt_id}],
        "dockers": [
            {"x": src_cx, "y": src_cy},
            {"x": tgt_cx, "y": tgt_cy},
        ],
        "bounds": {
            "upperLeft":  {"x": min(src_cx, tgt_cx), "y": min(src_cy, tgt_cy)},
            "lowerRight": {"x": max(src_cx, tgt_cx), "y": max(src_cy, tgt_cy)},
        },
    }

def _connect(shape, flow_id, direction):
    """Add a flow reference to a shape's outgoing or incoming list."""
    shape[direction].append({"resourceId": flow_id})


# ── Define shapes by lane ─────────────────────────────────────────────────────
#
# X positions (lane-relative, after label strip)
# Phases roughly aligned across lanes:
#   Discover  ~  60–290
#   Evaluate  ~ 290–610
#   Purchase  ~ 610–870
#   Onboard   ~ 870–1280
#   Adopt     ~1280–1730
#   Expand    ~1730–2100
#
# Lane indices:  0=Customer  1=Sales  2=Platform  3=CustomerSuccess

# IDs
ids = {k: _sid() for k in [
    "start",
    "t_research",       # L0 Discover
    "t_qualify",        # L1 Discover
    "t_demo",           # L1 Evaluate
    "t_prov_trial",     # L2 Evaluate
    "t_eval_trial",     # L0 Evaluate
    "t_proposal",       # L1 Purchase
    "gw_buy",           # L0 Purchase — "Proceed to purchase?"
    "t_sign",           # L0 Purchase — Yes branch
    "t_prov_prod",      # L2 Onboard
    "t_kickoff",        # L3 Onboard
    "t_training",       # L3 Onboard/Adopt
    "t_onboard_emails", # L2 Onboard
    "t_build_lib",      # L0 Adopt
    "t_qbr",            # L3 Expand
    "t_expand",         # L1 Expand
    "end",
]}

F = {k: _sid() for k in [
    "f01", "f02", "f03", "f04", "f05", "f06", "f07",
    "f08", "f09", "f10", "f11", "f12", "f13", "f14",
    "f15", "f16",
]}

# ── Lane 0: Customer / Prospect ───────────────────────────────────────────────
L0 = 0
shapes_l0 = [
    _event(  ids["start"],     "Customer\nidentifies need",     "StartNoneEvent",               40),
    _task(   ids["t_research"],"Research process\nmanagement solutions", 100,                    BLUE),
    _task(   ids["t_eval_trial"], "Explore trial &\nattend workshops",   500,                    BLUE),
    _gateway(ids["gw_buy"],    "Proceed to\npurchase?",                  880),
    _task(   ids["t_sign"],    "Review & sign\ncontract",               1000,                    BLUE),
    _task(   ids["t_build_lib"],"Build enterprise\nprocess library",    1650,                    BLUE),
    _event(  ids["end"],       "Customer achieves\nprocess excellence", "EndNoneEvent",           2100),
]

# ── Lane 1: Sales & Pre-Sales ─────────────────────────────────────────────────
L1 = 1
shapes_l1 = [
    _task(ids["t_qualify"],  "Qualify inbound\nlead",              100,  GREEN),
    _task(ids["t_demo"],     "Conduct product\ndemo & POC",         400,  GREEN),
    _task(ids["t_proposal"], "Prepare & send\ncustom proposal",     700,  GREEN),
    _task(ids["t_expand"],   "Upsell additional\nlicenses & modules",1900, GREEN),
]

# ── Lane 2: Signavio Platform ─────────────────────────────────────────────────
L2 = 2
shapes_l2 = [
    _task(ids["t_prov_trial"],    "Provision trial\nenvironment",    400, AMBER),
    _task(ids["t_prov_prod"],     "Provision production\ntenant",   1100, AMBER),
    _task(ids["t_onboard_emails"],"Send automated\nonboarding emails",1350, AMBER),
]

# ── Lane 3: Customer Success ──────────────────────────────────────────────────
L3 = 3
shapes_l3 = [
    _task(ids["t_kickoff"],  "Run project\nkickoff meeting",        1100, PINK),
    _task(ids["t_training"], "Deliver enablement\ntraining sessions",1400, PINK),
    _task(ids["t_qbr"],      "Conduct quarterly\nbusiness review",  1900, PINK),
]

# ── Sequence flows ────────────────────────────────────────────────────────────
# Helper: right-center of a task (absolute canvas)
def rc(lane_idx, lane_rel_x):  # right-center of task at lane_rel_x
    return abs_x(lane_rel_x + TASK_W), abs_y(lane_idx, (LANE_H - TASK_H)//2 + TASK_H//2)

def lc(lane_idx, lane_rel_x):  # left-center of task
    return abs_x(lane_rel_x), abs_y(lane_idx, (LANE_H - TASK_H)//2 + TASK_H//2)

def rc_e(lane_idx, lane_rel_x):  # right-center of event
    return abs_x(lane_rel_x + EVENT_D), abs_y(lane_idx, (LANE_H - EVENT_D)//2 + EVENT_D//2)

def lc_e(lane_idx, lane_rel_x):  # left-center of event
    return abs_x(lane_rel_x), abs_y(lane_idx, (LANE_H - EVENT_D)//2 + EVENT_D//2)

def rc_g(lane_idx, lane_rel_x):  # right-center of gateway
    return abs_x(lane_rel_x + GW_SIZE), abs_y(lane_idx, (LANE_H - GW_SIZE)//2 + GW_SIZE//2)

def lc_g(lane_idx, lane_rel_x):  # left-center of gateway
    return abs_x(lane_rel_x), abs_y(lane_idx, (LANE_H - GW_SIZE)//2 + GW_SIZE//2)

def bc(lane_idx, lane_rel_x, w, h):  # bottom-center
    return abs_x(lane_rel_x + w//2), abs_y(lane_idx, (LANE_H - h)//2 + h)

def tc(lane_idx, lane_rel_x, w):  # top-center
    return abs_x(lane_rel_x + w//2), abs_y(lane_idx, (LANE_H - TASK_H)//2)

# Flow definitions: (flow_id, label, src_id, tgt_id, src_cx, src_cy, tgt_cx, tgt_cy)
flow_defs = [
    # Start → Research (L0)
    ("f01", "", "start",       "t_research",    *rc_e(L0, 40),    *lc(L0, 100)),
    # Research → Qualify (L0→L1) cross-lane
    ("f02", "", "t_research",  "t_qualify",     *bc(L0, 100, TASK_W, TASK_H),  *tc(L1, 100, TASK_W)),
    # Qualify → Demo (L1)
    ("f03", "", "t_qualify",   "t_demo",        *rc(L1, 100),     *lc(L1, 400)),
    # Demo → Prov Trial (L1→L2) cross-lane
    ("f04", "", "t_demo",      "t_prov_trial",  *bc(L1, 400, TASK_W, TASK_H),  *tc(L2, 400, TASK_W)),
    # Prov Trial → Eval Trial (L2→L0) cross-lane up
    ("f05", "", "t_prov_trial","t_eval_trial",  *tc(L2, 400, TASK_W),  *bc(L0, 500, TASK_W, TASK_H)),
    # Eval Trial → Proposal (L0→L1) cross-lane
    ("f06", "", "t_eval_trial","t_proposal",    *bc(L0, 500, TASK_W, TASK_H),  *tc(L1, 700, TASK_W)),
    # Proposal → GW Buy (L1→L0) cross-lane up
    ("f07", "", "t_proposal",  "gw_buy",        *tc(L1, 700, TASK_W),  *bc(L0, 880, GW_SIZE, GW_SIZE)),
    # GW Buy → Sign Contract (L0, Yes)
    ("f08", "Yes", "gw_buy",   "t_sign",        *rc_g(L0, 880),   *lc(L0, 1000)),
    # Sign Contract → Prov Prod (L0→L2) cross-lane
    ("f09", "", "t_sign",      "t_prov_prod",   *bc(L0, 1000, TASK_W, TASK_H),  *tc(L2, 1100, TASK_W)),
    # Prov Prod → Kickoff (L2→L3) cross-lane
    ("f10", "", "t_prov_prod", "t_kickoff",     *bc(L2, 1100, TASK_W, TASK_H),  *tc(L3, 1100, TASK_W)),
    # Kickoff → Onboard Emails (L3→L2) cross-lane up
    ("f11", "", "t_kickoff",   "t_onboard_emails", *rc(L3, 1100), *lc(L2, 1350)),
    # Kickoff → Training (L3)
    ("f12", "", "t_kickoff",   "t_training",    *rc(L3, 1100),    *lc(L3, 1400)),
    # Training → Build Library (L3→L0) cross-lane up
    ("f13", "", "t_training",  "t_build_lib",   *tc(L3, 1400, TASK_W),  *bc(L0, 1650, TASK_W, TASK_H)),
    # Build Library → QBR (L0→L3) cross-lane
    ("f14", "", "t_build_lib", "t_qbr",         *bc(L0, 1650, TASK_W, TASK_H),  *tc(L3, 1900, TASK_W)),
    # QBR → Expand (L3→L1) cross-lane up
    ("f15", "", "t_qbr",       "t_expand",      *tc(L3, 1900, TASK_W),  *bc(L1, 1900, TASK_W, TASK_H)),
    # Expand → End (L1→L0) cross-lane up
    ("f16", "", "t_expand",    "end",           *tc(L1, 1900, TASK_W),  *lc_e(L0, 2100)),
]

# Build flow shapes and wire up outgoing/incoming on sources/targets
all_shapes_by_id = {}
for sh in shapes_l0 + shapes_l1 + shapes_l2 + shapes_l3:
    all_shapes_by_id[sh["resourceId"]] = sh

sequence_flows = []
for fdef in flow_defs:
    fkey, label, src_key, tgt_key, sx, sy, tx, ty = fdef
    fid = F[fkey]
    src_id = ids[src_key]
    tgt_id = ids[tgt_key]
    sf = _flow(fid, label, src_id, tgt_id, sx, sy, tx, ty)
    sequence_flows.append(sf)
    # Wire up source and target shapes
    all_shapes_by_id[src_id]["outgoing"].append({"resourceId": fid})
    all_shapes_by_id[tgt_id]["incoming"].append({"resourceId": fid})

# ── Build lanes ───────────────────────────────────────────────────────────────
def _lane(rid, name, lane_idx, child_shapes):
    y_start = lane_idx * LANE_H
    return {
        "resourceId": rid,
        "properties": {"name": name, "documentation": ""},
        "stencil":     {"id": "Lane"},
        "childShapes": child_shapes,
        "outgoing":    [],
        "incoming":    [],
        "bounds": {
            "upperLeft":  {"x": POOL_HEADER_W, "y": y_start},
            "lowerRight": {"x": POOL_W,         "y": y_start + LANE_H},
        },
        "dockers": [],
    }

lane_ids = [_sid() for _ in range(4)]
lanes = [
    _lane(lane_ids[0], "Customer / Prospect",   0, shapes_l0),
    _lane(lane_ids[1], "Sales & Pre-Sales",      1, shapes_l1),
    _lane(lane_ids[2], "Signavio Platform",       2, shapes_l2),
    _lane(lane_ids[3], "Customer Success",        3, shapes_l3),
]

# ── Build pool ────────────────────────────────────────────────────────────────
pool_id = _sid()
pool = {
    "resourceId": pool_id,
    "properties": {
        "name":          "SAP Signavio Customer Journey",
        "documentation": "",
        "bgcolor":       "#ffffff",
        "bordercolor":   "#000000",
    },
    "stencil":     {"id": "Pool"},
    "childShapes": lanes,
    "outgoing":    [],
    "incoming":    [],
    "bounds": {
        "upperLeft":  {"x": POOL_X,           "y": POOL_Y},
        "lowerRight": {"x": POOL_X + POOL_W,  "y": POOL_Y + POOL_H},
    },
    "dockers": [],
}

# ── Assemble full model ───────────────────────────────────────────────────────
model_root_id = _sid()
model = {
    "resourceId": model_root_id,
    "properties": {
        "title":         "SAP Signavio Customer Journey",
        "documentation": "",
        "process_id":    "",
        "version":       "",
        "author":        "BPMN Annotator",
        "language":      "English",
    },
    "stencil":     {"id": "BPMNDiagram"},
    "childShapes": [pool] + sequence_flows,
    "bounds": {
        "upperLeft":  {"x": 0,    "y": 0},
        "lowerRight": {"x": 3000, "y": 2000},
    },
    "stencilset": {
        "url":       "/stencilsets/bpmn2.0/bpmn2.0.json",
        "namespace": "http://b3mn.org/stencilset/bpmn2.0#",
    },
    "ssextensions": [],
}

# ── Create in Signavio ────────────────────────────────────────────────────────
def main():
    print("Authenticating with Signavio...")
    auth = get_auth()
    print(f"OK Authenticated - API base: {auth.api_base}")

    print("\nCreating model 'SAP Signavio Customer Journey' in Maria Playground...")
    new_model_id = create_model(
        auth,
        name="SAP Signavio Customer Journey",
        parent=PARENT_FOLDER,
        model_json=model,
        comment="Created by PM Agent - SAP Signavio Customer Journey",
    )
    print(f"\nModel created successfully!")
    print(f"  Model ID : {new_model_id}")
    print(f"  View URL : {auth.api_base.replace('/api', '')}/p/hub/model/{new_model_id}")
    return new_model_id

if __name__ == "__main__":
    main()
