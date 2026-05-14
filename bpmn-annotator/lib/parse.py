"""Parse Signavio BPMN JSON into a structured representation.

Works on any BPMN 2.0 Pool/Lane model regardless of process domain.
No assumptions are made about task names, lane names, or the number of lanes.
"""


def parse_model(model: dict) -> dict:
    """Extract structured data from a Signavio BPMN JSON model.

    Returns a dict with:
        title       — process/pool name
        pool_bounds — {"upperLeft": {x,y}, "lowerRight": {x,y}} | None
        lanes       — list of lane dicts
        tasks       — list of task dicts
        gateways    — list of gateway dicts
        events      — list of event dicts
        flows       — list of sequence/message flow dicts

    Lane dict:
        id, name, abs_y (absolute y on canvas), height, tasks (names), gateways

    Task dict:
        id, name, lane_id, lane_name, bounds_local {x,y},
        outgoing_ids, incoming_ids, existing_doc

    Gateway dict:
        id, type (stencil id), name, lane_id, lane_name,
        bounds_local {x,y}, outgoing_ids

    Event dict:
        id, type (stencil id), name, lane_id, lane_name

    Flow dict:
        id, type, name, source_id, target_id, source_name, target_name
    """
    result = {
        "title": "",
        "pool_bounds": None,
        "lanes":    [],
        "tasks":    [],
        "gateways": [],
        "events":   [],
        "flows":    [],
    }

    # Build a resource-ID-to-name map for resolving flow endpoints later
    id_to_name: dict = {}

    for top in model.get("childShapes", []):
        stencil = top.get("stencil", {}).get("id", "")

        # ── Sequence / Message flows at root level ────────────────────────────
        if stencil in ("SequenceFlow", "MessageFlow"):
            result["flows"].append({
                "id":        top["resourceId"],
                "type":      stencil,
                "name":      top.get("properties", {}).get("name", "").strip(),
                "source_id": (top.get("incoming") or [{}])[0].get("resourceId", ""),
                "target_id": (top.get("outgoing") or [{}])[0].get("resourceId", ""),
                "source_name": "",  # resolved below
                "target_name": "",
            })
            continue

        # ── Skip non-Pool shapes ──────────────────────────────────────────────
        if stencil in ("TextAnnotation", "Association_Undirected",
                       "CollapsedPool", "DataObject", "DataStore"):
            continue

        # ── Pool ─────────────────────────────────────────────────────────────
        if stencil == "Pool":
            result["title"] = top.get("properties", {}).get("name", "").strip()
            pb = top["bounds"]
            result["pool_bounds"] = pb
            pool_ul = pb["upperLeft"]

            for lane in top.get("childShapes", []):
                if lane.get("stencil", {}).get("id") != "Lane":
                    continue

                lid   = lane["resourceId"]
                lname = lane.get("properties", {}).get("name", "").strip()
                lb    = lane["bounds"]
                abs_y = pool_ul["y"] + lb["upperLeft"]["y"]
                lh    = lb["lowerRight"]["y"] - lb["upperLeft"]["y"]
                lane_tasks, lane_gws = [], []

                for elem in lane.get("childShapes", []):
                    estencil = elem.get("stencil", {}).get("id", "")
                    props    = elem.get("properties", {})
                    eid      = elem["resourceId"]
                    ename    = props.get("name", "").replace("\n", " ").strip()
                    eb       = elem["bounds"]["upperLeft"]
                    id_to_name[eid] = ename

                    if estencil == "Task":
                        result["tasks"].append({
                            "id":           eid,
                            "name":         ename,
                            "lane_id":      lid,
                            "lane_name":    lname,
                            "bounds_local": {"x": eb["x"], "y": eb["y"]},
                            "outgoing_ids": [o["resourceId"] for o in elem.get("outgoing", [])],
                            "incoming_ids": [o["resourceId"] for o in elem.get("incoming", [])],
                            "existing_doc": props.get("documentation", ""),
                        })
                        lane_tasks.append(ename)

                    elif "Gateway" in estencil:
                        result["gateways"].append({
                            "id":           eid,
                            "type":         estencil,
                            "name":         ename,
                            "lane_id":      lid,
                            "lane_name":    lname,
                            "bounds_local": {"x": eb["x"], "y": eb["y"]},
                            "outgoing_ids": [o["resourceId"] for o in elem.get("outgoing", [])],
                        })
                        lane_gws.append({"id": eid, "type": estencil, "name": ename})

                    elif "Event" in estencil:
                        result["events"].append({
                            "id":        eid,
                            "type":      estencil,
                            "name":      ename,
                            "lane_id":   lid,
                            "lane_name": lname,
                        })

                result["lanes"].append({
                    "id":       lid,
                    "name":     lname,
                    "abs_y":    abs_y,
                    "height":   lh,
                    "tasks":    lane_tasks,
                    "gateways": lane_gws,
                })

    # Resolve flow endpoint names now that id_to_name is complete
    for f in result["flows"]:
        f["source_name"] = id_to_name.get(f["source_id"], "")
        f["target_name"] = id_to_name.get(f["target_id"], "")

    return result
