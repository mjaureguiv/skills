"""BPMN modeling quality review.

Analyzes a parsed model and returns a markdown report.
Never modifies the model or submits anything to SPM.
"""


def review_model_quality(parsed: dict) -> str:
    """Return a markdown quality report for the given parsed model.

    Checks:
      1. Task naming     — should follow Verb + Object pattern
      2. Gateway labels  — exclusive gateways should have a question label
      3. Flow labels     — conditional flows leaving gateways should be labeled
      4. Empty lanes     — lanes with no tasks
      5. Start/end events — every process needs at least one of each
      6. Undocumented tasks — tasks with no documentation property
      7. Long sequences  — > 7 tasks in a lane without a gateway
      8. Pool complexity — > 8 lanes suggests decomposition needed
    """
    issues = []

    # 1. Task naming (Verb + Object = at least 2 words)
    for t in parsed["tasks"]:
        words = t["name"].split()
        if len(words) < 2:
            issues.append(
                f"- **Task naming** `{t['name']}` in lane `{t['lane_name']}` "
                "— too short, should follow Verb + Object pattern "
                "(e.g. 'Send Contract', 'Review Application')"
            )

    # 2. Unlabeled exclusive gateways
    for gw in parsed["gateways"]:
        if "Exclusive" in gw["type"] and not gw["name"]:
            issues.append(
                f"- **Unlabeled exclusive gateway** `{gw['id']}` in lane `{gw['lane_name']}` "
                "— should carry a question label (e.g. 'Approved?')"
            )

    # 3. Conditional flow labels (heuristic: majority unlabeled + gateways present)
    unlabeled = [f for f in parsed["flows"] if not f["name"]]
    if parsed["gateways"] and unlabeled:
        ratio = len(unlabeled) / max(1, len(parsed["flows"]))
        if ratio > 0.5:
            issues.append(
                f"- **Unlabeled flows** — {len(unlabeled)} of {len(parsed['flows'])} "
                "sequence flows have no label; consider labeling paths leaving gateways "
                "(e.g. 'Yes', 'No', 'Approved', 'Rejected')"
            )

    # 4. Empty lanes
    for lane in parsed["lanes"]:
        if not lane["tasks"]:
            issues.append(
                f"- **Empty lane** `{lane['name']}` contains no tasks "
                "— remove or add tasks to justify the swimlane"
            )

    # 5. Missing or multiple start/end events
    starts = [e for e in parsed["events"] if "Start" in e["type"]]
    ends   = [e for e in parsed["events"] if "End"   in e["type"]]
    if not starts:
        issues.append("- **Missing start event** — no start event found; every process needs one")
    if not ends:
        issues.append("- **Missing end event** — no end event found; every process needs one")
    if len(starts) > 1:
        issues.append(
            f"- **Multiple start events** ({len(starts)}) "
            "— verify this is intentional (e.g. parallel entry points)"
        )

    # 6. Undocumented tasks
    undoc = [t for t in parsed["tasks"] if not t["existing_doc"]]
    if undoc:
        names = ", ".join(f"`{t['name']}`" for t in undoc[:5])
        more  = f" (+{len(undoc) - 5} more)" if len(undoc) > 5 else ""
        issues.append(
            f"- **Undocumented tasks** ({len(undoc)}): {names}{more} "
            "— run `--mode documentation_only` to generate documentation"
        )

    # 7. Long linear sequences
    for lane in parsed["lanes"]:
        if len(lane["tasks"]) > 7 and not lane["gateways"]:
            issues.append(
                f"- **Long linear sequence** — lane `{lane['name']}` has "
                f"{len(lane['tasks'])} tasks with no gateways; "
                "consider decomposing into a sub-process"
            )

    # 8. Complex pool
    if len(parsed["lanes"]) > 8:
        issues.append(
            f"- **Complex pool** — {len(parsed['lanes'])} swimlanes is high; "
            "consider decomposing into multiple processes or sub-processes"
        )

    # ── Build report ──────────────────────────────────────────────────────────
    header = f"## BPMN Quality Review\n**Process:** {parsed['title']}\n\n"
    stats  = (
        f"**Model summary:** {len(parsed['tasks'])} tasks · "
        f"{len(parsed['gateways'])} gateways · "
        f"{len(parsed['lanes'])} lanes · "
        f"{len(parsed['events'])} events · "
        f"{len(parsed['flows'])} flows\n\n"
    )

    if not issues:
        return header + stats + "**No issues found.** Model looks well-structured.\n"

    return (
        header + stats
        + f"**Issues found ({len(issues)}):**\n\n"
        + "\n".join(issues) + "\n"
    )
