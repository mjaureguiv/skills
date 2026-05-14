# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas"]
# ///
"""
ProductBoard Features — Data Access Layer

Pandas-backed FeatureStore for querying ProductBoard feature data.
Loads the full JSON export from SharePoint, builds a product hierarchy tree,
and provides filtering, column selection, lazy enrichment, and export.

⚠️  READ-ONLY: This module NEVER calls the ProductBoard API.
    All data comes from the extraction skill's JSON export.

Usage as library:
    import sys; sys.path.insert(0, "skills/productboard-features")
    from feature_store import FeatureStore

    fs = FeatureStore.load()
    pm = fs.filter(product="Process Manager", status="In progress")
    pm.enrich_initiatives()
    df = pm.to_df()

Usage as CLI:
    uv run skills/productboard-features/feature_store.py --products
    uv run skills/productboard-features/feature_store.py --product "Process Manager" --stats
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

# ---------------------------------------------------------------------------
# Module imports (split from monolith for editor performance)
# ---------------------------------------------------------------------------

from section_parser import (
    SECTION_COLUMN_NAMES,
    extract_description_sections,
    strip_html,
)
from column_metadata import (
    COLUMN_METADATA,
    QUERY_HINTS,
    describe_column,
    describe_all_columns,
    describe_hints as _describe_hints_fn,
)
from sharepoint_client import download_from_sharepoint, SHAREPOINT_FILENAME
from hierarchy import HierarchyNode, build_hierarchy

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SKILL_DIR = Path(__file__).resolve().parent
TEMP_DIR = SKILL_DIR / "temp"

# Fallback: local extraction temp (sibling folder under dirks-skills/)
EXTRACTION_TEMP = SKILL_DIR.parent / "productboard-extraction" / "temp"


# ---------------------------------------------------------------------------
# FeatureStore
# ---------------------------------------------------------------------------

class FeatureStore:
    """
    Pandas-backed data access layer for ProductBoard features.

    Provides filtering, column selection, enrichment, hierarchy navigation,
    and export. All data comes from the extraction skill's JSON export —
    no ProductBoard API calls are made.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        raw_data: dict[str, Any] | None = None,
        hierarchy_nodes: dict[str, HierarchyNode] | None = None,
        _enriched: set[str] | None = None,
    ):
        self.df = df.reset_index(drop=True)
        self._raw = raw_data or {}
        self._nodes = hierarchy_nodes or {}
        self._enriched: set[str] = _enriched or set()

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    @classmethod
    def load(cls, verbose: bool = False) -> "FeatureStore":
        """Load from SharePoint (primary) with local fallback."""
        # Try SharePoint first
        try:
            if verbose:
                print("Downloading from SharePoint...")
            return cls.from_sharepoint(verbose=verbose)
        except Exception as e:
            if verbose:
                print(f"SharePoint download failed: {e}")
                print("Falling back to local file...")

        # Fallback: local extraction temp
        local_files = [
            TEMP_DIR / SHAREPOINT_FILENAME,
            EXTRACTION_TEMP / SHAREPOINT_FILENAME,
        ]
        # Also check for any pb_features_full_*.json in extraction temp
        if EXTRACTION_TEMP.exists():
            candidates = sorted(EXTRACTION_TEMP.glob("pb_features_full_*.json"), reverse=True)
            local_files.extend(candidates)

        for path in local_files:
            if path and path.exists():
                if verbose:
                    print(f"Loading from local file: {path}")
                return cls.from_file(path, verbose=verbose)

        raise FileNotFoundError(
            "No JSON data file found. Either:\n"
            "  1. Run extraction: python skills/dirks-skills/productboard-extraction/extract_features.py\n"
            "  2. Ensure Graph token exists: python tools/outlook/outlook_api.py auth"
        )

    @classmethod
    def from_sharepoint(cls, filename: str = SHAREPOINT_FILENAME,
                        verbose: bool = False) -> "FeatureStore":
        """Download JSON from SharePoint and build a FeatureStore."""
        data = download_from_sharepoint(filename)
        # Save locally for future fallback
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        local_path = TEMP_DIR / filename
        local_path.write_bytes(data)
        if verbose:
            mb = len(data) / (1024 * 1024)
            print(f"Downloaded {mb:.1f} MB → saved to {local_path}")
        raw = json.loads(data.decode("utf-8"))
        return cls._from_raw(raw, verbose=verbose)

    @classmethod
    def from_file(cls, path: str | Path, verbose: bool = False) -> "FeatureStore":
        """Load from a local JSON file."""
        path = Path(path)
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
        if verbose:
            mb = path.stat().st_size / (1024 * 1024)
            print(f"Loaded {mb:.1f} MB from {path}")
        return cls._from_raw(raw, verbose=verbose)

    @classmethod
    def _from_raw(cls, raw: dict, verbose: bool = False) -> "FeatureStore":
        """Build a FeatureStore from parsed JSON data."""
        features = raw.get("features", [])
        products = raw.get("products", [])
        components = raw.get("components", [])

        # Build lookup dicts for parent name resolution
        features_by_id = {f["id"]: f for f in features}
        components_by_id = {c["id"]: c for c in components}
        products_by_id = {p["id"]: p for p in products}

        # Flatten features into DataFrame rows
        rows = []
        for f in features:
            parent = f.get("parent", {}) or {}
            parent_type = ""
            parent_id = ""
            for key in ("feature", "component", "product"):
                if key in parent:
                    parent_type = key
                    parent_id = parent[key].get("id", "")
                    break

            # Resolve parent name
            parent_name = ""
            if parent_id:
                if parent_type == "feature" and parent_id in features_by_id:
                    parent_name = features_by_id[parent_id].get("name", "")
                elif parent_type == "component" and parent_id in components_by_id:
                    parent_name = components_by_id[parent_id].get("name", "")
                elif parent_type == "product" and parent_id in products_by_id:
                    parent_name = products_by_id[parent_id].get("name", "")
                if not parent_name:
                    parent_name = parent_id

            status = f.get("status", {}) or {}
            status_id = status.get("id", "")
            # Resolve status_completed from feature_statuses
            statuses_by_id = {s["id"]: s for s in raw.get("feature_statuses", [])}
            status_detail = statuses_by_id.get(status_id, {})

            health = f.get("lastHealthUpdate") or {}
            timeframe = f.get("timeframe", {}) or {}
            owner = f.get("owner") or {}
            links = f.get("links", {}) or {}

            rows.append({
                "id": f.get("id", ""),
                "name": f.get("name", ""),
                "type": f.get("type", ""),
                "description": f.get("description", ""),
                "archived": f.get("archived", False),
                "status_id": status_id,
                "status_name": status.get("name", ""),
                "status_completed": status_detail.get("completed", False),
                "parent_type": parent_type,
                "parent_id": parent_id,
                "parent_name": parent_name,
                "owner_email": owner.get("email", ""),
                "timeframe_start": timeframe.get("startDate", "") or "",
                "timeframe_end": timeframe.get("endDate", "") or "",
                "timeframe_granularity": timeframe.get("granularity", "") or "",
                "health_status": health.get("status", ""),
                "health_message": strip_html(health.get("message", "") or ""),
                "health_date": health.get("createdAt", ""),
                "link_self": links.get("self", ""),
                "link_html": links.get("html", ""),
                "created_at": f.get("createdAt", ""),
                "updated_at": f.get("updatedAt", ""),
            })

        df = pd.DataFrame(rows)
        if df.empty:
            df = pd.DataFrame(columns=[
                "id", "name", "type", "description", "archived",
                "status_id", "status_name", "status_completed",
                "parent_type", "parent_id", "parent_name",
                "owner_email", "timeframe_start", "timeframe_end",
                "timeframe_granularity", "health_status", "health_message",
                "health_date", "link_self", "link_html",
                "created_at", "updated_at",
            ])

        # Build hierarchy tree
        nodes = build_hierarchy(products, components, df)

        if verbose:
            meta = raw.get("_metadata", {})
            print(f"Features: {len(df)}")
            print(f"Products: {len(products)}")
            print(f"Components: {len(components)}")
            if meta.get("exported_at"):
                print(f"Exported at: {meta['exported_at']}")

        return cls(df=df, raw_data=raw, hierarchy_nodes=nodes)

    # ------------------------------------------------------------------
    # Hierarchy
    # ------------------------------------------------------------------

    def get_products(self) -> list[dict[str, str]]:
        """List all products: [{"id": "...", "name": "..."}]."""
        return [
            {"id": n.id, "name": n.name}
            for n in self._nodes.values()
            if n.node_type == "product"
        ]

    def get_components(self, product: str | None = None) -> list[dict[str, str]]:
        """List components, optionally filtered to a product."""
        if product:
            node = self._find_node_by_name(product, "product")
            if not node:
                return []
            return [
                {"id": c.id, "name": c.name}
                for c in node.children
                if c.node_type == "component"
            ]
        return [
            {"id": n.id, "name": n.name}
            for n in self._nodes.values()
            if n.node_type == "component"
        ]

    def get_product_tree(self, name_or_id: str) -> dict | None:
        """Get the full subtree for a product as a nested dict."""
        node = self._find_node_by_name(name_or_id, "product")
        if not node:
            # Try by ID
            node = self._nodes.get(name_or_id)
        return node.to_dict() if node else None

    def get_descendant_ids(self, name_or_id: str,
                           node_type: str | None = None) -> set[str]:
        """Get all feature/subfeature IDs under a node (product or component)."""
        node = self._find_node_by_name(name_or_id, node_type)
        if not node:
            node = self._nodes.get(name_or_id)
        if not node:
            return set()
        return node.get_all_feature_ids()

    def print_tree(self, name_or_id: str | None = None,
                   max_depth: int | None = None) -> str:
        """Pretty-print the hierarchy tree. Returns formatted string."""
        if name_or_id:
            node = self._find_node_by_name(name_or_id)
            if not node:
                node = self._nodes.get(name_or_id)
            if not node:
                return f"Node not found: {name_or_id}"
            return node.print_tree(max_depth=max_depth)
        else:
            # Print all products
            lines = []
            products = sorted(
                [n for n in self._nodes.values() if n.node_type == "product"],
                key=lambda n: n.name,
            )
            for p in products:
                lines.append(p.print_tree(max_depth=max_depth))
            return "\n".join(lines)

    def _find_node_by_name(self, name: str,
                           node_type: str | None = None) -> HierarchyNode | None:
        """Find a hierarchy node by name (case-insensitive)."""
        name_lower = name.lower()
        for node in self._nodes.values():
            if node_type and node.node_type != node_type:
                continue
            if node.name.lower() == name_lower:
                return node
        # Partial match fallback
        for node in self._nodes.values():
            if node_type and node.node_type != node_type:
                continue
            if name_lower in node.name.lower():
                return node
        return None

    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------

    def filter(self, **criteria) -> "FeatureStore":
        """
        Filter features by criteria. Returns a new FeatureStore.

        Supported criteria:
            product: str          — All features under this product (hierarchy)
            component: str        — All features under this component (hierarchy)
            status: str | list    — By status name(s)
            owner: str            — By owner email
            type: str             — "feature" or "subfeature"
            archived: bool        — Filter by archived flag
            health: str           — By health status ("on-track", "at-risk", "off-track")
            timeframe_after: str  — Timeframe start >= date (YYYY-MM-DD)
            timeframe_before: str — Timeframe end <= date (YYYY-MM-DD)
            search: str           — Text search in name + description
            where: callable       — Arbitrary predicate: fn(df) -> df
        """
        mask = pd.Series(True, index=self.df.index)

        # Product filter (uses hierarchy tree)
        if "product" in criteria:
            product_name = criteria["product"]
            feature_ids = self.get_descendant_ids(product_name, "product")
            if not feature_ids:
                # Also include features whose parent_name matches directly
                mask &= self.df["parent_name"].str.lower() == product_name.lower()
            else:
                mask &= self.df["id"].isin(feature_ids)

        # Component filter (uses hierarchy tree)
        if "component" in criteria:
            comp_name = criteria["component"]
            feature_ids = self.get_descendant_ids(comp_name, "component")
            if not feature_ids:
                mask &= self.df["parent_name"].str.lower() == comp_name.lower()
            else:
                mask &= self.df["id"].isin(feature_ids)

        # Status filter (supports exact match or substring match for emoji-prefixed names)
        if "status" in criteria:
            statuses = criteria["status"]
            if isinstance(statuses, str):
                statuses = [statuses]
            statuses_lower = [s.lower() for s in statuses]
            # Try exact match first
            exact_mask = self.df["status_name"].str.lower().isin(statuses_lower)
            if exact_mask.any():
                mask &= exact_mask
            else:
                # Fallback: substring/contains match (handles "In progress" matching "⚙️ In progress")
                contains_mask = pd.Series(False, index=self.df.index)
                for s in statuses_lower:
                    contains_mask |= self.df["status_name"].str.lower().str.contains(s, na=False)
                mask &= contains_mask

        # Owner filter
        if "owner" in criteria:
            mask &= self.df["owner_email"].str.lower() == criteria["owner"].lower()

        # Type filter
        if "type" in criteria:
            mask &= self.df["type"] == criteria["type"]

        # Archived filter
        if "archived" in criteria:
            mask &= self.df["archived"] == criteria["archived"]

        # Health filter
        if "health" in criteria:
            mask &= self.df["health_status"].str.lower() == criteria["health"].lower()

        # Timeframe filters
        if "timeframe_after" in criteria:
            cutoff = criteria["timeframe_after"]
            has_start = self.df["timeframe_start"] != ""
            mask &= has_start & (self.df["timeframe_start"] >= cutoff)

        if "timeframe_before" in criteria:
            cutoff = criteria["timeframe_before"]
            has_end = self.df["timeframe_end"] != ""
            mask &= has_end & (self.df["timeframe_end"] <= cutoff)

        # Text search
        if "search" in criteria:
            query = criteria["search"].lower()
            name_match = self.df["name"].str.lower().str.contains(query, na=False)
            desc_match = self.df["description"].str.lower().str.contains(query, na=False)
            mask &= (name_match | desc_match)

        filtered_df = self.df[mask].copy()

        # Apply arbitrary predicate (operates on the already-filtered DataFrame)
        if "where" in criteria:
            fn = criteria["where"]
            filtered_df = fn(filtered_df)

        return FeatureStore(
            df=filtered_df,
            raw_data=self._raw,
            hierarchy_nodes=self._nodes,
            _enriched=set(self._enriched),
        )

    # ------------------------------------------------------------------
    # Column selection
    # ------------------------------------------------------------------

    def select(self, *columns: str) -> "FeatureStore":
        """
        Select specific columns. Returns new FeatureStore with narrowed DataFrame.

        Columns that don't exist yet (e.g. enrichment columns) are silently skipped.
        """
        available = [c for c in columns if c in self.df.columns]
        if not available:
            raise ValueError(
                f"None of the requested columns exist: {columns}\n"
                f"Available: {list(self.df.columns)}"
            )
        return FeatureStore(
            df=self.df[available].copy(),
            raw_data=self._raw,
            hierarchy_nodes=self._nodes,
            _enriched=set(self._enriched),
        )

    # ------------------------------------------------------------------
    # Enrichment (lazy, idempotent, mutates self.df in-place)
    # ------------------------------------------------------------------

    def enrich_initiatives(self) -> "FeatureStore":
        """Add 'initiatives' column: list of initiative names per feature."""
        if "initiatives" in self._enriched:
            return self
        links = self._raw.get("initiative_feature_links", {})
        self.df["initiatives"] = self.df["id"].map(
            lambda fid: links.get(fid, [])
        )
        self._enriched.add("initiatives")
        return self

    def enrich_objectives(self) -> "FeatureStore":
        """Add 'objectives' column: list of objective names per feature."""
        if "objectives" in self._enriched:
            return self
        links = self._raw.get("objective_feature_links", {})
        self.df["objectives"] = self.df["id"].map(
            lambda fid: links.get(fid, [])
        )
        self._enriched.add("objectives")
        return self

    def enrich_releases(self) -> "FeatureStore":
        """Add release columns per feature.

        Columns added:
          - ``releases``        — list of original release names (str)
          - ``release_quarter`` — list of normalised quarter labels,
                                  e.g. ``["Q1 2026"]``, deduplicated & sorted.
                                  *Generated at extraction time* from release names.
          - ``release_date``    — list of normalised ISO dates (start-of-period),
                                  e.g. ``["2026-01-01"]``, deduplicated & sorted.
                                  *Generated at extraction time* from release names.

        The ``_generated_quarter`` / ``_generated_date`` fields are added to
        each release object by the extractor (``_normalize_releases``).  If the
        JSON was produced by an older extractor that lacks these fields, the
        normalised columns will contain empty lists.
        """
        if "releases" in self._enriched:
            return self

        assignments = self._raw.get("release_assignments", [])
        releases = self._raw.get("releases", [])
        releases_by_id = {r["id"]: r for r in releases}

        # Build feature → [release_name, ...] and normalised variants
        feature_releases: dict[str, list[str]] = {}
        feature_quarters: dict[str, list[str]] = {}
        feature_dates: dict[str, list[str]] = {}
        for ra in assignments:
            if not ra.get("assigned", False):
                continue
            fid = (ra.get("feature") or {}).get("id", "")
            rid = (ra.get("release") or {}).get("id", "")
            release = releases_by_id.get(rid, {})
            rname = release.get("name", rid)
            feature_releases.setdefault(fid, []).append(rname)
            # Read pre-computed generated fields (set by extractor)
            gq = release.get("_generated_quarter", "")
            gd = release.get("_generated_date", "")
            if gq:
                feature_quarters.setdefault(fid, []).append(gq)
            if gd:
                feature_dates.setdefault(fid, []).append(gd)

        self.df["releases"] = self.df["id"].map(
            lambda fid: feature_releases.get(fid, [])
        )
        self.df["release_quarter"] = self.df["id"].map(
            lambda fid: sorted(set(feature_quarters.get(fid, [])))
        )
        self.df["release_date"] = self.df["id"].map(
            lambda fid: sorted(set(feature_dates.get(fid, [])))
        )
        self._enriched.add("releases")
        return self

    def enrich_custom_fields(self) -> "FeatureStore":
        """Add 'cf_<name>' columns: one per custom field definition."""
        if "custom_fields" in self._enriched:
            return self

        cf_defs = self._raw.get("custom_fields", [])
        cf_values = self._raw.get("custom_field_values", [])
        cf_names = {cf["id"]: cf.get("name", cf["id"]) for cf in cf_defs}

        # Build { feature_id: { cf_name: value_str } }
        cf_by_feature: dict[str, dict[str, str]] = {}
        for cfv in cf_values:
            he = cfv.get("hierarchyEntity", {})
            if he.get("type") != "feature":
                continue
            fid = he.get("id", "")
            cf_id = (cfv.get("customField") or {}).get("id", "")
            cf_name = cf_names.get(cf_id, cf_id)
            val = cfv.get("value", "")
            if isinstance(val, dict):
                val = val.get("label", val.get("email", json.dumps(val)))
            elif isinstance(val, list):
                val = "; ".join(
                    v.get("label", json.dumps(v)) if isinstance(v, dict) else str(v)
                    for v in val
                )
            else:
                val = str(val) if val is not None else ""
            cf_by_feature.setdefault(fid, {})[cf_name] = val

        # Add one column per custom field
        all_cf_names = sorted(set(cf_names.values()))
        for cf_name in all_cf_names:
            col = f"cf_{cf_name}"
            self.df[col] = self.df["id"].map(
                lambda fid, _cn=cf_name: cf_by_feature.get(fid, {}).get(_cn, "")
            )

        self._enriched.add("custom_fields")
        return self

    def enrich_sections(self) -> "FeatureStore":
        """Add 'sec_<name>' columns: parsed from description HTML."""
        if "sections" in self._enriched:
            return self

        # Check if sections are already in the JSON (extraction adds them)
        features_raw = self._raw.get("features", [])
        features_sections: dict[str, dict[str, str]] = {}
        use_raw_sections = False
        if features_raw and "sections" in features_raw[0]:
            use_raw_sections = True
            for f in features_raw:
                fid = f.get("id", "")
                features_sections[fid] = f.get("sections", {})

        for sec_col in SECTION_COLUMN_NAMES:
            if use_raw_sections:
                self.df[sec_col] = self.df["id"].map(
                    lambda fid, _sc=sec_col: features_sections.get(fid, {}).get(_sc, "")
                )
            else:
                # Parse from description HTML on the fly
                self.df[sec_col] = self.df["description"].apply(
                    lambda html, _sc=sec_col: extract_description_sections(html or "").get(_sc, "")
                )

        self._enriched.add("sections")
        return self

    def enrich_all(self) -> "FeatureStore":
        """Run all enrichments."""
        self.enrich_initiatives()
        self.enrich_objectives()
        self.enrich_releases()
        self.enrich_custom_fields()
        self.enrich_sections()
        return self

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------

    def to_df(self) -> pd.DataFrame:
        """Return the underlying pandas DataFrame."""
        return self.df

    def to_dicts(self) -> list[dict]:
        """Return features as a list of plain dicts."""
        return self.df.to_dict(orient="records")

    def to_json(self, path: str | Path | None = None, indent: int = 2) -> str:
        """Serialize to JSON string. Optionally write to file."""
        # Convert DataFrame to records, handling list columns properly
        records = self.df.to_dict(orient="records")
        result = json.dumps(records, indent=indent, ensure_ascii=False, default=str)
        if path:
            Path(path).write_text(result, encoding="utf-8")
        return result

    def to_csv(self, path: str | Path) -> None:
        """Write to CSV file. List columns are joined with '; '."""
        df_out = self.df.copy()
        # Flatten list columns to semicolon-delimited strings
        for col in df_out.columns:
            if df_out[col].apply(lambda x: isinstance(x, list)).any():
                df_out[col] = df_out[col].apply(
                    lambda x: "; ".join(str(v) for v in x) if isinstance(x, list) else x
                )
        df_out.to_csv(path, index=False, encoding="utf-8")

    def stats(self) -> dict[str, Any]:
        """Summary statistics about the current feature set."""
        result: dict[str, Any] = {
            "total_features": len(self.df),
            "enriched": sorted(self._enriched),
        }
        if "status_name" in self.df.columns:
            result["by_status"] = self.df["status_name"].value_counts().to_dict()
        if "type" in self.df.columns:
            result["by_type"] = self.df["type"].value_counts().to_dict()
        if "archived" in self.df.columns:
            result["archived"] = int(self.df["archived"].sum())
        if "owner_email" in self.df.columns:
            result["unique_owners"] = int(self.df["owner_email"].nunique())
        if "health_status" in self.df.columns:
            health_counts = self.df[self.df["health_status"] != ""]["health_status"].value_counts().to_dict()
            if health_counts:
                result["by_health"] = health_counts
        if "parent_type" in self.df.columns and "parent_name" in self.df.columns:
            product_features = self.df[self.df["parent_type"] == "product"]
            if not product_features.empty:
                result["direct_product_children"] = product_features["parent_name"].value_counts().to_dict()

        # Metadata from raw data
        meta = self._raw.get("_metadata", {})
        if meta.get("exported_at"):
            result["data_exported_at"] = meta["exported_at"]

        return result

    def columns(self) -> list[str]:
        """List available columns."""
        return list(self.df.columns)

    def __len__(self) -> int:
        return len(self.df)

    def __repr__(self) -> str:
        total = len(self._raw.get("features", []))
        filtered = len(self.df)
        enriched_str = ", ".join(sorted(self._enriched)) if self._enriched else "none"
        if total and filtered < total:
            return f"FeatureStore: {filtered} features (filtered from {total}) | enriched: {enriched_str}"
        return f"FeatureStore: {filtered} features | enriched: {enriched_str}"

    def __iter__(self):
        return iter(self.to_dicts())

    # ------------------------------------------------------------------
    # Data dictionary / describe  (delegates to column_metadata module)
    # ------------------------------------------------------------------

    @staticmethod
    def describe(column: str | None = None) -> str:
        """Return a formatted description of available columns.

        Does NOT require loading data — reads from the static COLUMN_METADATA.

        Args:
            column: If given, show detail for that one column.
                    If None, show a grouped summary of all columns.
        """
        if column is not None:
            return describe_column(column)
        return describe_all_columns()

    @staticmethod
    def describe_hints() -> str:
        """Return formatted query translation hints."""
        return _describe_hints_fn()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="ProductBoard Features — Data Access Layer CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Loading
    p.add_argument("--local", type=str, default=None,
                   help="Use a local JSON file instead of SharePoint")
    p.add_argument("--verbose", "-v", action="store_true",
                   help="Verbose output")

    # Filtering
    p.add_argument("--product", type=str, default=None,
                   help="Filter by product name (uses hierarchy)")
    p.add_argument("--component", type=str, default=None,
                   help="Filter by component name (uses hierarchy)")
    p.add_argument("--status", nargs="+", type=str, default=None,
                   help="Filter by status name(s)")
    p.add_argument("--owner", type=str, default=None,
                   help="Filter by owner email")
    p.add_argument("--type", dest="feat_type", type=str, default=None,
                   choices=["feature", "subfeature"],
                   help="Filter by feature type")
    p.add_argument("--search", type=str, default=None,
                   help="Text search in name + description")
    p.add_argument("--archived", action="store_true", default=None,
                   help="Include only archived features")
    p.add_argument("--no-archived", action="store_true",
                   help="Exclude archived features")
    p.add_argument("--health", type=str, default=None,
                   help="Filter by health status")
    p.add_argument("--timeframe-after", type=str, default=None,
                   help="Timeframe start >= date (YYYY-MM-DD)")
    p.add_argument("--timeframe-before", type=str, default=None,
                   help="Timeframe end <= date (YYYY-MM-DD)")

    # Selection & enrichment
    p.add_argument("--select", nargs="+", type=str, default=None,
                   help="Columns to include in output")
    p.add_argument("--enrich", nargs="+", type=str, default=None,
                   choices=["initiatives", "objectives", "releases",
                            "custom_fields", "sections", "all"],
                   help="Enrichments to apply")

    # Output
    p.add_argument("--format", dest="output_format", type=str,
                   default="json", choices=["json", "csv"],
                   help="Output format (default: json)")
    p.add_argument("--output", "-o", type=str, default=None,
                   help="Write to file instead of stdout")
    p.add_argument("--head", type=int, default=None,
                   help="Limit to first N rows")

    # Special commands
    p.add_argument("--products", action="store_true",
                   help="List all products")
    p.add_argument("--components", action="store_true",
                   help="List all components")
    p.add_argument("--stats", action="store_true",
                   help="Show summary statistics")
    p.add_argument("--tree", nargs="?", const="__all__", default=None,
                   help="Show hierarchy tree (optionally rooted at a product)")
    p.add_argument("--max-depth", type=int, default=None,
                   help="Max tree depth (used with --tree)")
    p.add_argument("--columns", action="store_true",
                   help="List available columns")
    p.add_argument("--describe", nargs="?", const="__all__", default=None,
                   metavar="COLUMN",
                   help="Show column data dictionary. Optionally specify a column name "
                        "for detail, or 'hints' for query examples. No data loading needed.")

    return p


def main():
    parser = _build_parser()
    args = parser.parse_args()

    # --describe runs without loading data
    if args.describe is not None:
        if args.describe == "__all__":
            print(FeatureStore.describe())
        elif args.describe.lower() == "hints":
            print(FeatureStore.describe_hints())
        else:
            print(FeatureStore.describe(args.describe))
        return

    # Load data
    if args.local:
        fs = FeatureStore.from_file(args.local, verbose=args.verbose)
    else:
        fs = FeatureStore.load(verbose=args.verbose)

    # Special commands (exit early)
    if args.products:
        products = fs.get_products()
        for p in sorted(products, key=lambda x: x["name"]):
            print(f"  {p['name']}")
        print(f"\n{len(products)} products")
        return

    if args.components:
        components = fs.get_components(product=args.product)
        for c in sorted(components, key=lambda x: x["name"]):
            print(f"  {c['name']}")
        print(f"\n{len(components)} components")
        return

    if args.tree is not None:
        name = None if args.tree == "__all__" else args.tree
        print(fs.print_tree(name, max_depth=args.max_depth))
        return

    if args.columns:
        for col in fs.columns():
            print(f"  {col}")
        return

    # Build filter criteria
    criteria: dict[str, Any] = {}
    if args.product:
        criteria["product"] = args.product
    if args.component:
        criteria["component"] = args.component
    if args.status:
        criteria["status"] = args.status if len(args.status) > 1 else args.status[0]
    if args.owner:
        criteria["owner"] = args.owner
    if args.feat_type:
        criteria["type"] = args.feat_type
    if args.search:
        criteria["search"] = args.search
    if args.archived:
        criteria["archived"] = True
    elif args.no_archived:
        criteria["archived"] = False
    if args.health:
        criteria["health"] = args.health
    if args.timeframe_after:
        criteria["timeframe_after"] = args.timeframe_after
    if args.timeframe_before:
        criteria["timeframe_before"] = args.timeframe_before

    # Apply filters
    if criteria:
        fs = fs.filter(**criteria)

    # Apply enrichments
    if args.enrich:
        if "all" in args.enrich:
            fs.enrich_all()
        else:
            for e in args.enrich:
                getattr(fs, f"enrich_{e}")()

    # Stats command (after filtering)
    if args.stats:
        stats = fs.stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False, default=str))
        return

    # Limit rows
    if args.head:
        fs.df = fs.df.head(args.head)

    # Column selection
    if args.select:
        fs = fs.select(*args.select)

    # Output
    if args.output_format == "csv":
        if args.output:
            fs.to_csv(args.output)
            print(f"Written {len(fs)} rows to {args.output}")
        else:
            print(fs.df.to_csv(index=False))
    else:
        result = fs.to_json(path=args.output)
        if args.output:
            print(f"Written {len(fs)} features to {args.output}")
        else:
            print(result)


if __name__ == "__main__":
    main()
