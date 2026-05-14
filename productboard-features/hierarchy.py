# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas"]
# ///
"""
Product hierarchy tree for ProductBoard features.

Builds and navigates the Product → Component → Feature → Sub-feature hierarchy.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


class HierarchyNode:
    """A node in the Product → Component → Feature → Sub-feature tree."""

    __slots__ = ("id", "name", "node_type", "children", "parent_id", "data")

    def __init__(self, id: str, name: str, node_type: str,
                 parent_id: str = "", data: dict | None = None):
        self.id = id
        self.name = name
        self.node_type = node_type  # "product", "component", "feature", "subfeature"
        self.children: list[HierarchyNode] = []
        self.parent_id = parent_id
        self.data = data or {}

    def to_dict(self, include_data: bool = False) -> dict:
        """Convert to a nested dict (for JSON serialization)."""
        d: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "type": self.node_type,
            "children": [c.to_dict(include_data) for c in self.children],
        }
        if include_data:
            d["data"] = self.data
        return d

    def get_all_descendant_ids(self) -> set[str]:
        """Recursively collect IDs of all descendants."""
        ids: set[str] = set()
        for child in self.children:
            ids.add(child.id)
            ids.update(child.get_all_descendant_ids())
        return ids

    def get_all_feature_ids(self) -> set[str]:
        """Recursively collect IDs of all feature/subfeature descendants."""
        ids: set[str] = set()
        if self.node_type in ("feature", "subfeature"):
            ids.add(self.id)
        for child in self.children:
            ids.update(child.get_all_feature_ids())
        return ids

    def print_tree(self, indent: int = 0, max_depth: int | None = None) -> str:
        """Pretty-print the tree. Returns the formatted string."""
        if max_depth is not None and indent > max_depth:
            return ""
        type_icons = {
            "product": "📦",
            "component": "🧩",
            "feature": "✨",
            "subfeature": "  ↳",
        }
        icon = type_icons.get(self.node_type, "•")
        lines = [f"{'  ' * indent}{icon} {self.name}"]
        for child in sorted(self.children, key=lambda c: c.name):
            child_str = child.print_tree(indent + 1, max_depth)
            if child_str:
                lines.append(child_str)
        return "\n".join(lines)


def build_hierarchy(products: list[dict], components: list[dict],
                    features_df: pd.DataFrame) -> dict[str, HierarchyNode]:
    """
    Build the full hierarchy tree from products, components, and features.

    Returns a dict of { node_id: HierarchyNode } for all nodes.
    The top-level nodes are products (no parent).
    """
    nodes: dict[str, HierarchyNode] = {}

    # 1. Create product nodes
    for p in products:
        pid = p.get("id", "")
        nodes[pid] = HierarchyNode(pid, p.get("name", ""), "product", data=p)

    # 2. Create component nodes
    for c in components:
        cid = c.get("id", "")
        parent = c.get("parent", {})
        parent_id = ""
        if "product" in parent:
            parent_id = parent["product"].get("id", "")
        elif "component" in parent:
            parent_id = parent["component"].get("id", "")
        nodes[cid] = HierarchyNode(cid, c.get("name", ""), "component",
                                   parent_id=parent_id, data=c)

    # 3. Create feature/subfeature nodes from the DataFrame
    for _, row in features_df.iterrows():
        fid = row.get("id", "")
        ftype = row.get("type", "feature")
        parent_id = row.get("parent_id", "")
        nodes[fid] = HierarchyNode(fid, row.get("name", ""), ftype,
                                   parent_id=parent_id)

    # 4. Wire up parent → child relationships
    for node in nodes.values():
        if node.parent_id and node.parent_id in nodes:
            nodes[node.parent_id].children.append(node)

    return nodes
