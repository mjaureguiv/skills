"""Orthogonal layout cleanup for Signavio BPMN models.

Replaces diagonal sequence flow dockers with clean orthogonal (90-degree)
routes.  All coordinates in this module are absolute canvas coordinates.

Coordinate system reminder
--------------------------
  Shape bounds in the JSON are stored lane-relative.
  Absolute = pool_ul + lane_ul + elem_ul  (all three additive components).
  Sequence flow dockers are already absolute canvas coordinates.
"""
from __future__ import annotations


# ── Shape index ───────────────────────────────────────────────────────────────

def _build_shape_index(model: dict) -> tuple[dict, dict]:
    """Return (shape_index, flow_to_source).

    shape_index: resourceId -> {abs_ul, abs_lr, abs_cx, abs_cy, lane_idx, stencil}
    flow_to_source: flow_resourceId -> source_shape_resourceId

    Signavio strips `incoming` from SequenceFlow shapes when it stores them.
    The source of a flow is found via the source shape's `outgoing` list:
    any shape whose outgoing references a flow ID is that flow's source.
    """
    index: dict = {}
    flow_to_source: dict = {}

    def _register_shape_outgoing(shape_id: str, shape: dict) -> None:
        for ref in shape.get("outgoing", []):
            flow_id = ref.get("resourceId")
            if flow_id:
                flow_to_source[flow_id] = shape_id

    for top in model.get("childShapes", []):
        stencil_top = top.get("stencil", {}).get("id", "")

        # Register flows at root level that might have outgoing (edge case)
        if stencil_top == "SequenceFlow":
            _register_shape_outgoing(top["resourceId"], top)
            continue

        if stencil_top != "Pool":
            continue

        pool_ul = top["bounds"]["upperLeft"]
        px, py = pool_ul["x"], pool_ul["y"]

        for lane_idx, lane in enumerate(top.get("childShapes", [])):
            if lane.get("stencil", {}).get("id") != "Lane":
                continue

            lane_ul = lane["bounds"]["upperLeft"]
            lx, ly = lane_ul["x"], lane_ul["y"]

            for elem in lane.get("childShapes", []):
                stencil = elem.get("stencil", {}).get("id", "")
                rid = elem["resourceId"]
                b = elem["bounds"]
                ux  = px + lx + b["upperLeft"]["x"]
                uy  = py + ly + b["upperLeft"]["y"]
                lrx = px + lx + b["lowerRight"]["x"]
                lry = py + ly + b["lowerRight"]["y"]
                index[rid] = {
                    "abs_ul":   {"x": ux,  "y": uy},
                    "abs_lr":   {"x": lrx, "y": lry},
                    "abs_cx":   (ux + lrx) / 2,
                    "abs_cy":   (uy + lry) / 2,
                    "lane_idx": lane_idx,
                    "stencil":  stencil,
                }
                # Register this shape's outgoing flow references
                _register_shape_outgoing(rid, elem)

    return index, flow_to_source


# ── Orthogonal router ─────────────────────────────────────────────────────────

def _pt(x: float, y: float) -> dict:
    return {"x": round(x), "y": round(y)}


def _orthogonal_route(
    si: dict,  # source shape info from index
    ti: dict,  # target shape info from index
) -> list[dict]:
    """Produce orthogonal docker waypoints for a flow from source to target.

    Returns a list of absolute-coordinate docker dicts.

    Routing decision tree
    ---------------------
    1. Same lane, target to the right
         → horizontal 2-pt: src_right_center → tgt_left_center
    2. Different lane, vertically aligned (|src_cx - tgt_cx| <= 20)
         → vertical 2-pt: src_bottom/top_center → tgt_top/bottom_center
    3. Going down, target is to the right of source right edge
         → Z-bend 3-pt: src_right → (tgt_left_x, src_cy) → tgt_left_center
    4. Going down, target is left of or behind source
         → L-bend 3-pt: src_bottom → (src_cx, tgt_top_y) → tgt_top_center
    5. Going up, target is to the right (backward-upward cross-lane)
         → Bridge 4-pt via right side: src_right → (x_bridge, src_cy)
                                        → (x_bridge, tgt_cy) → tgt_right_center
           where x_bridge = max(src_right_x, tgt_right_x) + 20
    6. Going up, target is to the left
         → L-bend 3-pt: src_top → (src_cx, tgt_bottom_y) → tgt_top_center
    """
    src_ul = si["abs_ul"]
    src_lr = si["abs_lr"]
    tgt_ul = ti["abs_ul"]
    tgt_lr = ti["abs_lr"]

    src_cx  = si["abs_cx"]
    src_cy  = si["abs_cy"]
    tgt_cx  = ti["abs_cx"]
    tgt_cy  = ti["abs_cy"]

    src_right  = src_lr["x"]
    src_left   = src_ul["x"]
    src_top    = src_ul["y"]
    src_bottom = src_lr["y"]

    tgt_right  = tgt_lr["x"]
    tgt_left   = tgt_ul["x"]
    tgt_top    = tgt_ul["y"]
    tgt_bottom = tgt_lr["y"]

    going_down = si["lane_idx"] < ti["lane_idx"]
    going_up   = si["lane_idx"] > ti["lane_idx"]
    same_lane  = si["lane_idx"] == ti["lane_idx"]

    # ── 1. Same lane ──────────────────────────────────────────────────────────
    if same_lane:
        return [_pt(src_right, src_cy), _pt(tgt_left, tgt_cy)]

    # ── 2. Vertically aligned (same column) ──────────────────────────────────
    if abs(src_cx - tgt_cx) <= 20:
        if going_down:
            return [_pt(src_cx, src_bottom), _pt(tgt_cx, tgt_top)]
        else:
            return [_pt(src_cx, src_top), _pt(tgt_cx, tgt_bottom)]

    # ── 3. Going down, target to the right ───────────────────────────────────
    if going_down and tgt_left >= src_right:
        return [
            _pt(src_right, src_cy),
            _pt(tgt_left, src_cy),
            _pt(tgt_left, tgt_cy),
        ]

    # ── 4. Going down, target behind/left of source ───────────────────────────
    if going_down:
        return [
            _pt(src_cx, src_bottom),
            _pt(src_cx, tgt_top),
            _pt(tgt_cx, tgt_top),
        ]

    # ── 5. Going up, target to the right ─────────────────────────────────────
    if going_up and tgt_right >= src_left:
        x_bridge = max(src_right, tgt_right) + 20
        return [
            _pt(src_right, src_cy),
            _pt(x_bridge,  src_cy),
            _pt(x_bridge,  tgt_cy),
            _pt(tgt_right, tgt_cy),
        ]

    # ── 6. Going up, target to the left ──────────────────────────────────────
    return [
        _pt(src_cx, src_top),
        _pt(src_cx, tgt_bottom),
        _pt(tgt_cx, tgt_bottom),
    ]


# ── Public API ────────────────────────────────────────────────────────────────

def compute_layout_changes(model: dict, parsed: dict) -> list[dict]:
    """Compute orthogonal routing for every sequence flow.

    Returns a list of change records (all flows, changed or not).

    Source lookup strategy
    ----------------------
    Signavio strips `incoming` from SequenceFlow shapes on retrieval.
    The source of a flow is identified via the reverse map built from
    each shape's `outgoing` list: shape.outgoing = [flow_id] means
    that shape is the source of that flow.
    Target is always flow.outgoing[0] (Signavio preserves this).
    """
    shape_index, flow_to_source = _build_shape_index(model)

    # Build name map from parsed model for readable output
    name_map: dict[str, str] = {}
    for t in parsed.get("tasks", []):
        name_map[t["id"]] = t["name"]
    for g in parsed.get("gateways", []):
        name_map[g["id"]] = g.get("name") or g["type"]
    for e in parsed.get("events", []):
        name_map[e["id"]] = e.get("name") or e["type"]

    changes = []
    for shape in model.get("childShapes", []):
        if shape.get("stencil", {}).get("id") != "SequenceFlow":
            continue

        flow_id = shape["resourceId"]
        label   = shape.get("properties", {}).get("name", "")

        # Source: look up via reverse map (shape that has this flow in its outgoing)
        src_id = flow_to_source.get(flow_id)
        # Target: flow's own outgoing[0]
        outgoing = shape.get("outgoing", [])
        tgt_id = outgoing[0]["resourceId"] if outgoing else None

        if not src_id or not tgt_id:
            continue
        if src_id not in shape_index or tgt_id not in shape_index:
            continue

        si = shape_index[src_id]
        ti = shape_index[tgt_id]

        old_dockers = shape.get("dockers", [])
        new_dockers = _orthogonal_route(si, ti)

        rule = _rule_label(si, ti)
        changed = (old_dockers != new_dockers)

        changes.append({
            "flow_id":     flow_id,
            "label":       label,
            "src_id":      src_id,
            "tgt_id":      tgt_id,
            "src_name":    name_map.get(src_id, src_id[-8:]),
            "tgt_name":    name_map.get(tgt_id, tgt_id[-8:]),
            "src_lane":    si["lane_idx"],
            "tgt_lane":    ti["lane_idx"],
            "rule":        rule,
            "old_dockers": old_dockers,
            "new_dockers": new_dockers,
            "changed":     changed,
        })

    return changes


def apply_layout_changes(model: dict, changes: list[dict]) -> None:
    """Mutate sequence flow dockers in-place for all changed flows."""
    flow_map = {
        s["resourceId"]: s
        for s in model.get("childShapes", [])
        if s.get("stencil", {}).get("id") == "SequenceFlow"
    }
    for c in changes:
        if not c["changed"]:
            continue
        flow = flow_map.get(c["flow_id"])
        if flow is None:
            continue
        flow["dockers"] = c["new_dockers"]
        # Update bounds to cover the new path
        xs = [d["x"] for d in c["new_dockers"]]
        ys = [d["y"] for d in c["new_dockers"]]
        flow["bounds"] = {
            "upperLeft":  {"x": min(xs), "y": min(ys)},
            "lowerRight": {"x": max(xs), "y": max(ys)},
        }


def layout_dry_run_report(changes: list[dict], parsed: dict) -> str:
    """Build a human-readable dry-run report string."""
    changed = [c for c in changes if c["changed"]]
    clean   = [c for c in changes if not c["changed"]]
    lane_names = [l["name"] for l in parsed.get("lanes", [])]

    def lane_label(idx):
        if 0 <= idx < len(lane_names):
            return f"L{idx} ({lane_names[idx]})"
        return f"L{idx}"

    lines = [
        "=" * 60,
        f"LAYOUT CLEANUP  --  {parsed['title']}",
        "=" * 60,
        f"Flows analyzed  : {len(changes)}",
        f"To reroute      : {len(changed)}",
        f"Already clean   : {len(clean)}",
    ]

    if changed:
        lines.append("\nChanges:")
        for c in changed:
            old_pts = " -> ".join(f"({d['x']},{d['y']})" for d in c["old_dockers"])
            new_pts = " -> ".join(f"({d['x']},{d['y']})" for d in c["new_dockers"])
            flow_label = f"'{c['label']}' " if c["label"] else ""
            lines.append(
                f"\n  [REROUTE] {flow_label}"
                f"{c['src_name']} -> {c['tgt_name']}"
                f"  ({lane_label(c['src_lane'])} -> {lane_label(c['tgt_lane'])})"
            )
            lines.append(f"    rule : {c['rule']}")
            lines.append(f"    old  : {old_pts}")
            lines.append(f"    new  : {new_pts}")

    if clean:
        lines.append("\nAlready orthogonal (no change):")
        for c in clean:
            flow_label = f"'{c['label']}' " if c["label"] else ""
            lines.append(
                f"  [OK]  {flow_label}"
                f"{c['src_name']} -> {c['tgt_name']}"
                f"  ({lane_label(c['src_lane'])} -> {lane_label(c['tgt_lane'])})"
                f"  [{c['rule']}]"
            )

    return "\n".join(lines)


# ── Internal helpers ──────────────────────────────────────────────────────────

def _rule_label(si: dict, ti: dict) -> str:
    going_down = si["lane_idx"] < ti["lane_idx"]
    going_up   = si["lane_idx"] > ti["lane_idx"]
    same_lane  = si["lane_idx"] == ti["lane_idx"]

    if same_lane:
        return "horizontal"
    if abs(si["abs_cx"] - ti["abs_cx"]) <= 20:
        return "vertical-aligned"
    if going_down and ti["abs_ul"]["x"] >= si["abs_lr"]["x"]:
        return "Z-bend-down-right"
    if going_down:
        return "L-bend-down-left"
    if going_up and ti["abs_lr"]["x"] >= si["abs_ul"]["x"]:
        return "bridge-up-right"
    return "L-bend-up-left"
