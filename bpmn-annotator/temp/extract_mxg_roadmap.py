"""
Extract MXG roadmap features from pb_features_full_latest.json and cross-reference
with insights CSV to build ROADMAP_DATA for mxc-skills.html.
"""
import json
import sys
import io
import csv
import re
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PB_JSON = r"C:\Users\I769452\Downloads\pb_features_full_latest.json"
INSIGHTS_CSV = r"C:\Backup\productboard_insights_05.05.2026.csv"

NNL_FIELD_ID = "6763c034-a291-44fa-ae9a-c3525d48c525"
VISIBILITY_FIELD_ID = "a0634072-6ee3-43b4-9eb0-b3357009fb1c"

# Products to include
TARGET_PRODUCTS = {"SAP Signavio Process Manager", "NextGen Modeler"}

# Map NNL label -> status key
NNL_MAP = {
    "01| Now": "NOW",
    "02| Next": "NEXT",
    "03| Later": "LATER",
}

# Visibility values to include (exclude "Dev Only")
ALLOWED_VISIBILITY = {"External", "Internal"}

print("Loading JSON...")
with open(PB_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

features = data["features"]
products = data["products"]
components = data["components"]
cfv_list = data["custom_field_values"]

print(f"  {len(features)} features, {len(products)} products, {len(components)} components, {len(cfv_list)} cfv entries")

# Build product id->name map
prod_by_id = {p["id"]: p["name"] for p in products}

# Build component id->name and id->parent map
comp_by_id = {}
comp_parent = {}
for c in components:
    comp_by_id[c["id"]] = c["name"]
    parent = c.get("parent", {})
    for k, v in parent.items():
        if isinstance(v, dict):
            comp_parent[c["id"]] = (k, v.get("id", ""))
        else:
            comp_parent[c["id"]] = (k, v)

# Build feature id -> product resolution (walk up component hierarchy)
def get_product_id(feature):
    parent = feature.get("parent", {})
    if "product" in parent:
        pid = parent["product"].get("id", "")
        return pid
    elif "component" in parent:
        cid = parent["component"].get("id", "")
        # walk up
        visited = set()
        while cid and cid not in visited:
            visited.add(cid)
            p = comp_parent.get(cid)
            if p is None:
                break
            kind, pid = p
            if kind == "product":
                return pid
            cid = pid
    elif "feature" in parent:
        # sub-feature, skip
        return None
    return None

# Build cfv lookup: feature_id -> {field_id: label}
print("Building CFV lookup...")
cfv_by_feature = defaultdict(dict)
for cfv in cfv_list:
    fid = cfv.get("hierarchyEntity", {}).get("id")
    cid = cfv.get("customField", {}).get("id")
    val = cfv.get("value")
    if not fid or not cid or val is None:
        continue
    if isinstance(val, dict):
        label = val.get("label", "")
    else:
        label = str(val)
    cfv_by_feature[fid][cid] = label

print(f"  CFV lookup built for {len(cfv_by_feature)} features")

# Load insights CSV for insight counts by feature_id and feature_name
print("Loading insights CSV...")
insights_by_id = defaultdict(int)
insights_by_name = defaultdict(int)
try:
    with open(INSIGHTS_CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fid = row.get("feature_id", "").strip()
            fname = row.get("feature_name", "").strip()
            if fid:
                insights_by_id[fid] += 1
            if fname:
                insights_by_name[fname] += 1
    print(f"  {sum(insights_by_id.values())} insight rows loaded, {len(insights_by_id)} unique feature IDs")
except Exception as e:
    print(f"  WARNING: Could not load insights CSV: {e}")

# Extract quarter from timeframe
def get_quarter(feature):
    tf = feature.get("timeframe", {})
    if not tf:
        return None
    start = tf.get("startDate", "")
    gran = tf.get("granularity", "")
    if not start:
        return None
    m = re.match(r"(\d{4})-(\d{2})", start)
    if not m:
        return None
    year, month = int(m.group(1)), int(m.group(2))
    q = (month - 1) // 3 + 1
    return f"Q{q} {year}"

# Get component ancestry names for a feature (for area mapping)
def get_component_chain(feature):
    parent = feature.get("parent", {})
    if "component" not in parent:
        return []
    cid = parent["component"].get("id", "")
    chain = []
    visited = set()
    while cid and cid not in visited:
        visited.add(cid)
        name = comp_by_id.get(cid, "")
        if name:
            chain.append(name)
        p = comp_parent.get(cid)
        if p is None:
            break
        kind, pid = p
        if kind == "product":
            break
        cid = pid
    chain.reverse()  # root first
    return chain

# Area mapping heuristics based on component names and keywords
LEGACY_PM_KEYWORDS = [
    "variant management", "approval", "dictionary", "dimension",
    "reporting", "folder", "navigation", "notification",
    "collaboration hub", "process governance", "governance",
    "spm renovation", "legacy", "process hierarchy",
    "cloud alm", "calm", "leanix",
]
PROCESS_MODELER_KEYWORDS = [
    "modeler", "modeling", "modelling", "nextgen", "next gen",
    "shapes", "text to process", "canvas", "ai-assisted",
    "ai assisted", "joule", "diagram",
]
SUITE_REPO_KEYWORDS = [
    "suite", "repository", "process intelligence", "process mining",
    "analysis", "mining", "transformation",
]

def infer_area(feature, component_chain):
    text = " ".join([feature.get("name", "")] + component_chain).lower()
    # Check modeler first (strong signal)
    for kw in PROCESS_MODELER_KEYWORDS:
        if kw in text:
            return "Process Modeler"
    for kw in LEGACY_PM_KEYWORDS:
        if kw in text:
            return "Legacy Process Manager"
    for kw in SUITE_REPO_KEYWORDS:
        if kw in text:
            return "Suite Repository"
    # fallback by product
    parent = feature.get("parent", {})
    if "product" in parent:
        pid = parent["product"].get("id", "")
        pname = prod_by_id.get(pid, "")
        if "NextGen" in pname or "Modeler" in pname:
            return "Process Modeler"
    # Try owner email
    owner = (feature.get("owner") or {}).get("email", "")
    if owner in ("timur.burlaka@sap.com", "thu.huong.dang@sap.com"):
        return "Legacy Process Manager"
    if owner in ("ariel.wu@sap.com", "ahmed.ashraf.saleh.mohamed@sap.com"):
        return "Process Modeler"
    return "Legacy Process Manager"  # default for Process Manager product

# Extract description (strip HTML tags, take first meaningful sentence)
def extract_desc(feature):
    raw = feature.get("description", "") or ""
    # strip HTML
    text = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"\s+", " ", text).strip()
    # take up to 200 chars
    if len(text) > 200:
        # try to cut at sentence boundary
        idx = text.find(". ", 0, 200)
        if idx > 30:
            text = text[:idx+1]
        else:
            text = text[:200].rsplit(" ", 1)[0] + "…"
    return text

# Main extraction
print("\nExtracting NNL features in scope...")
results = []
skipped_visibility = 0
skipped_no_product = 0
skipped_wrong_product = 0
skipped_subfeature = 0

for feat in features:
    if feat.get("archived"):
        continue
    # Skip subfeatures
    if feat.get("type") == "subfeature":
        skipped_subfeature += 1
        continue

    fid = feat["id"]
    fields = cfv_by_feature.get(fid, {})

    nnl_label = fields.get(NNL_FIELD_ID)
    if not nnl_label:
        continue  # Not on the board

    nnl_status = NNL_MAP.get(nnl_label)
    if not nnl_status:
        continue

    # Check visibility
    vis = fields.get(VISIBILITY_FIELD_ID, "")
    if vis not in ALLOWED_VISIBILITY and vis != "":
        skipped_visibility += 1
        continue
    # If visibility not set, include it (neutral)

    # Check product scope
    pid = get_product_id(feat)
    if pid is None:
        skipped_no_product += 1
        continue
    pname = prod_by_id.get(pid, "")
    if pname not in TARGET_PRODUCTS:
        skipped_wrong_product += 1
        continue

    comp_chain = get_component_chain(feat)
    area = infer_area(feat, comp_chain)
    quarter = get_quarter(feat)
    desc = extract_desc(feat)

    # Insight count: prefer by feature_id, fallback by feature_name
    ic = insights_by_id.get(fid) or insights_by_name.get(feat.get("name", "")) or None

    owner_email = (feat.get("owner") or {}).get("email", "")
    status_name = (feat.get("status") or {}).get("name", "")

    results.append({
        "id": fid,
        "name": feat.get("name", ""),
        "area": area,
        "status": nnl_status,
        "quarter": quarter,
        "insightsCount": ic,
        "desc": desc,
        "visibility": vis or "(not set)",
        "product": pname,
        "component_chain": " > ".join(comp_chain),
        "owner": owner_email,
        "pb_status": status_name,
    })

print(f"  Found: {len(results)} features")
print(f"  Skipped: {skipped_visibility} wrong visibility, {skipped_no_product} no product, {skipped_wrong_product} wrong product, {skipped_subfeature} subfeatures")

# Sort: area, then NNL order
NNL_ORDER = {"NOW": 0, "NEXT": 1, "LATER": 2}
results.sort(key=lambda x: (x["area"], NNL_ORDER.get(x["status"], 9), x["name"]))

# Print summary table
print("\n" + "="*110)
print(f"{'NAME':<50} {'AREA':<25} {'STATUS':<6} {'Q':<8} {'IC':<5} {'VISIBILITY':<12} {'OWNER':<30}")
print("="*110)
for r in results:
    ic_str = str(r["insightsCount"]) if r["insightsCount"] else "-"
    q_str = r["quarter"] or "-"
    print(f"{r['name'][:49]:<50} {r['area'][:24]:<25} {r['status']:<6} {q_str:<8} {ic_str:<5} {r['visibility'][:11]:<12} {r['owner'][:29]:<30}")

# Counts by area/status
print("\n--- Counts by area + status ---")
from collections import Counter
ctr = Counter((r["area"], r["status"]) for r in results)
for (area, st), n in sorted(ctr.items()):
    print(f"  {area} / {st}: {n}")

# Generate JavaScript ROADMAP_DATA
print("\n\n--- ROADMAP_DATA JavaScript array ---\n")
print("const ROADMAP_DATA = [")
for r in results:
    name = r["name"].replace("'", "\\'").replace("\\", "\\\\")
    desc = r["desc"].replace("'", "\\'").replace("\\", "\\\\")
    q = f"'{r['quarter']}'" if r["quarter"] else "null"
    ic = str(r["insightsCount"]) if r["insightsCount"] else "null"
    area = r["area"]
    status = r["status"]
    print(f"  {{ name:'{name}', area:'{area}', status:'{status}', quarter:{q}, insightsCount:{ic}, desc:'{desc}' }},")
print("];")
