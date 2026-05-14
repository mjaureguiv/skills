"""
Build clean ROADMAP_DATA JS array from Signavio PB JSON export.
"""
import json, sys, io, csv, re, html
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PB_JSON = r"C:\Users\I769452\Downloads\pb_features_full_latest.json"
INSIGHTS_CSV = r"C:\Backup\productboard_insights_05.05.2026.csv"

NNL_FIELD_ID = "6763c034-a291-44fa-ae9a-c3525d48c525"
VISIBILITY_FIELD_ID = "a0634072-6ee3-43b4-9eb0-b3357009fb1c"
TARGET_PRODUCTS = {"SAP Signavio Process Manager", "NextGen Modeler"}
NNL_MAP = {"01| Now": "NOW", "02| Next": "NEXT", "03| Later": "LATER"}
ALLOWED_VISIBILITY = {"External", "Internal", ""}

with open(PB_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

features, products, components, cfv_list = (
    data["features"], data["products"], data["components"], data["custom_field_values"]
)

prod_by_id = {p["id"]: p["name"] for p in products}
comp_by_id = {c["id"]: c["name"] for c in components}
comp_parent = {}
for c in components:
    parent = c.get("parent", {})
    for k, v in parent.items():
        if isinstance(v, dict):
            comp_parent[c["id"]] = (k, v.get("id", ""))
        else:
            comp_parent[c["id"]] = (k, str(v))

def get_product_id(feature):
    parent = feature.get("parent", {})
    if "product" in parent:
        return parent["product"].get("id", "")
    elif "component" in parent:
        cid = parent["component"].get("id", "")
        visited = set()
        while cid and cid not in visited:
            visited.add(cid)
            p = comp_parent.get(cid)
            if not p: break
            kind, pid = p
            if kind == "product": return pid
            cid = pid
    return None

cfv_by_feature = defaultdict(dict)
for cfv in cfv_list:
    fid = cfv.get("hierarchyEntity", {}).get("id")
    cid = cfv.get("customField", {}).get("id")
    val = cfv.get("value")
    if not fid or not cid or val is None: continue
    label = val.get("label", "") if isinstance(val, dict) else str(val)
    cfv_by_feature[fid][cid] = label

insights_by_id = defaultdict(int)
try:
    with open(INSIGHTS_CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fid = row.get("feature_id", "").strip()
            if fid: insights_by_id[fid] += 1
except Exception as e:
    sys.stderr.write(f"WARNING: {e}\n")

def get_quarter(feature):
    tf = feature.get("timeframe", {})
    if not tf: return None
    start = tf.get("startDate", "")
    if not start: return None
    m = re.match(r"(\d{4})-(\d{2})", start)
    if not m: return None
    year, month = int(m.group(1)), int(m.group(2))
    return f"Q{(month-1)//3+1} {year}"

def get_component_chain(feature):
    parent = feature.get("parent", {})
    if "component" not in parent: return []
    cid = parent["component"].get("id", "")
    chain, visited = [], set()
    while cid and cid not in visited:
        visited.add(cid)
        name = comp_by_id.get(cid, "")
        if name: chain.append(name)
        p = comp_parent.get(cid)
        if not p: break
        kind, pid = p
        if kind == "product": break
        cid = pid
    chain.reverse()
    return chain

def infer_area(feature, comp_chain):
    text = " ".join([feature.get("name", "")] + comp_chain).lower()
    owner = (feature.get("owner") or {}).get("email", "")
    # Process Modeler first (strong signal)
    modeler_kw = ["modeler", "modelling", "modeling", "nextgen", "shapes", "text to process",
                  "canvas", "ai-assisted", "joule", "image input", "tabular input",
                  "diagram selection", "subprocess link", "variant detection"]
    for kw in modeler_kw:
        if kw in text: return "Process Modeler"
    # Legacy PM
    legacy_kw = ["variant management", "cloud alm", "calm", "leanix", "approval framework",
                 "notification", "provisioning", "synchroniz", "tenant", "data migration",
                 "content language", "vietnamese", "bahasa", "ai agent orchestration"]
    for kw in legacy_kw:
        if kw in text: return "Legacy Process Manager"
    # Suite Repository
    suite_kw = ["dictionary", "suite repository", "process intelligence"]
    for kw in suite_kw:
        if kw in text: return "Suite Repository"
    # Owner-based fallback
    if owner in ("timur.burlaka@sap.com", "thu.huong.dang@sap.com"):
        return "Legacy Process Manager"
    if owner in ("ariel.wu@sap.com", "ahmed.ashraf.saleh.mohamed@sap.com"):
        return "Process Modeler"
    return "Legacy Process Manager"

def clean_name(name):
    # Remove [WIP] prefix
    name = re.sub(r"^\[WIP\]\s*", "", name)
    # Remove emoji (Unicode flags and other emoji)
    name = re.sub(r"[\U0001F1E0-\U0001F1FF\U0001F300-\U0001FFFF☀-⛿✀-➿]+\s*", "", name)
    # Clean special whitespace
    name = re.sub(r"[​‌‍﻿ ]+", " ", name)
    return name.strip()

def clean_desc(feature):
    raw = feature.get("description", "") or ""
    # Strip HTML tags
    text = re.sub(r"<[^>]+>", " ", raw)
    # Decode HTML entities
    text = html.unescape(text)
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    # Trim to ~200 chars at sentence boundary
    if len(text) > 200:
        idx = text.find(". ", 30, 200)
        if idx > 0:
            text = text[:idx+1]
        else:
            text = text[:200].rsplit(" ", 1)[0] + "…"
    # Escape for JS single-quoted string
    text = text.replace("\\", "\\\\").replace("'", "\\'")
    return text

# Extraction
results = []
for feat in features:
    if feat.get("archived") or feat.get("type") == "subfeature": continue
    fid = feat["id"]
    fields = cfv_by_feature.get(fid, {})
    nnl_label = fields.get(NNL_FIELD_ID)
    if not nnl_label: continue
    nnl_status = NNL_MAP.get(nnl_label)
    if not nnl_status: continue
    vis = fields.get(VISIBILITY_FIELD_ID, "")
    if vis == "Dev Only": continue
    pid = get_product_id(feat)
    if not pid: continue
    pname = prod_by_id.get(pid, "")
    if pname not in TARGET_PRODUCTS: continue

    comp_chain = get_component_chain(feat)
    area = infer_area(feat, comp_chain)
    quarter = get_quarter(feat)
    desc = clean_desc(feat)
    name = clean_name(feat.get("name", ""))
    ic = insights_by_id.get(fid) or None

    results.append({
        "name": name,
        "area": area,
        "status": nnl_status,
        "quarter": quarter,
        "insightsCount": ic,
        "desc": desc,
    })

NNL_ORDER = {"NOW": 0, "NEXT": 1, "LATER": 2}
AREA_ORDER = {"Legacy Process Manager": 0, "Suite Repository": 1, "Process Modeler": 2}
results.sort(key=lambda x: (AREA_ORDER.get(x["area"], 9), NNL_ORDER.get(x["status"], 9), x["name"]))

# Print the JS block
print("  // NOW — current sprint/quarter")
last_status = None
last_area = None
for r in results:
    if r["area"] != last_area:
        if last_area is not None:
            print()
        print(f"  // ── {r['area']} ──")
        last_status = None
        last_area = r["area"]
    if r["status"] != last_status:
        label = {"NOW": "NOW — in progress", "NEXT": "NEXT — coming up", "LATER": "LATER — horizon"}.get(r["status"], r["status"])
        print(f"  // {label}")
        last_status = r["status"]

    name_js = r["name"].replace("\\", "\\\\").replace("'", "\\'")
    q_js = f"'{r['quarter']}'" if r["quarter"] else "null"
    ic_js = str(r["insightsCount"]) if r["insightsCount"] else "null"
    print(f"  {{ name:'{name_js}', area:'{r['area']}', status:'{r['status']}', quarter:{q_js}, insightsCount:{ic_js}, desc:'{r['desc']}' }},")

print()

# Summary
from collections import Counter
ctr = Counter((r["area"], r["status"]) for r in results)
sys.stderr.write(f"\nTotal: {len(results)} features\n")
for (area, st), n in sorted(ctr.items(), key=lambda x: (AREA_ORDER.get(x[0][0],9), NNL_ORDER.get(x[0][1],9))):
    sys.stderr.write(f"  {area} / {st}: {n}\n")
