"""
rebuild_enriched.py — Build ROADMAP_DATA and INSIGHTS_DATA JS blocks
Roadmap columns: DONE (Jan-Mar 2026) / NOW (Apr-Jun 2026) / LATER (Jul-Dec 2026)
Insights: ALL MXG features with customer feedback (not just active roadmap)
"""
import csv, sys, io, re, json
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

MC_CSV       = r'C:\Users\I769452\Downloads\M&C-external-+-internal.csv'
INSIGHTS_CSV = r'C:\Backup\productboard_insights_05.05.2026.csv'

TEAM_TO_AREA = {
    'Process Guardians: MXG': 'Legacy Process Manager',
    'Roots: MXG':             'Legacy Process Manager',
    'The Sims: MXG':          'Suite Repository',
    'Dictionary: MXG':        'Suite Repository',
    'Process Pioneers: MXG':  'Process Modeler',
    'Process Vanguards:MXG':  'Process Modeler',
    'Kestrel: MXG':           'Process Modeler',
}

TEAM_SHORT = {
    'Process Guardians: MXG': 'Process Guardians',
    'Roots: MXG':             'Roots',
    'The Sims: MXG':          'The Sims',
    'Dictionary: MXG':        'Dictionary',
    'Process Pioneers: MXG':  'Process Pioneers',
    'Process Vanguards:MXG':  'Process Vanguards',
    'Kestrel: MXG':           'Kestrel',
}

BOOL_MONTHS = ['November 2025','December 2025',
               'January 2026','February 2026','March 2026',
               'April 2026','May 2026','June 2026']
Q1 = {'January 2026','February 2026','March 2026'}
Q2 = {'April 2026','May 2026','June 2026'}
H2 = ['July 2026','August 2026','September 2026',
      'October 2026','November 2026','December 2026']

SKIP_NAMES = {
    'Canvas foundation','Canvas navigation','Basic micro interactions',
    'Advanced micro interactions','Shapes suggestion','Context menu','Toolbar',
    'Multi-locales','Modeler App Lobby landing page','Shapes Panel All Elements',
    'Shapes Panel Favorites','New Process Modeler (GA) (WIP)',
    '(Sims) AuditLogs implementation',
    'New Internal APIs for Bulk Creation of Dictionary entries for NGM',
    'Onboard Transformation Manager Initiatives and define standard attributes',
    'Suite Repo - Support Attribute Type Upload /Add URL',
}

def get_bool_month(r):
    for m in BOOL_MONTHS:
        if r.get(m,'').lower() == 'true':
            return m
    return None

def get_h2_month(releases):
    if not releases: return None
    rl = releases.lower()
    for m in H2:
        if m.lower() in rl: return m
    short = {'jul':'July 2026','aug':'August 2026','sep':'September 2026',
             'oct':'October 2026','nov':'November 2026','dec':'December 2026'}
    for k, v in short.items():
        if re.search(r'\b' + k, rl): return v
    if 'q3' in rl and '2026' in rl: return 'Q3 2026'
    if 'q4' in rl and '2026' in rl: return 'Q4 2026'
    return None

def classify(r):
    """Return (column, month_label) or (None, None) to skip."""
    s = r.get('status_name','')
    m = get_bool_month(r)
    releases = (r.get('Releases','') or '').strip()
    h2m = get_h2_month(releases)

    # DONE: shipped in Q1 2026
    if s in ('👏🏽 GA Release / Done', '😢 Dropped'):
        if m in Q1:
            return ('DONE', m)
        return (None, None)

    active = {'🔔 Roll Out', '⚙️ In progress', '✅ Accepted Idea', '🛠️ Ready for Dev'}
    if s in active:
        if m in Q2: return ('NOW', m)
        if h2m:     return ('LATER', h2m)
        return (None, None)

    if s in ('🔍 Discovery', '💡 New idea'):
        if h2m: return ('LATER', h2m)
        return (None, None)

    return (None, None)

def clean_name(name):
    name = re.sub(r'^\[WIP\]\s*', '', name.strip())
    name = re.sub(r'[\U0001F1E0-\U0001F1FF]+\s*', '', name)
    return re.sub(r'\s+', ' ', name).strip()

def clean_desc(raw):
    d = re.sub(r'\\\.', '.', raw)
    d = re.sub(r'\\([^\n])', r'\1', d)
    d = re.sub(r'\*+', '', d)
    d = re.sub(r'#+\s*', '', d)
    d = re.sub(r'!\[.*?\]\(.*?\)', '', d)
    d = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', d)
    d = re.sub(r'\n+', ' ', d)
    d = re.sub(r'\s+', ' ', d).strip()
    m = re.search(r'(?:Value [Pp]roposition)[: ]+(.{30,})', d)
    if m: d = m.group(1)
    if len(d) > 250:
        idx = d.find('. ', 30, 250)
        d = d[:idx+1] if idx > 0 else d[:250].rsplit(' ',1)[0] + '…'
    return d

# ── Read M&C CSV ──────────────────────────────────────────────────────────────
with open(MC_CSV, 'r', encoding='utf-8-sig') as f:
    mc_rows = list(csv.DictReader(f))

roadmap_features = []     # 2026 roadmap items (DONE/NOW/LATER)
all_mxg_features  = []    # ALL MXG features for insights matching
seen_roadmap = set()
seen_all     = set()

for r in mc_rows:
    if r['entity_type'] != 'Feature': continue
    team = r.get('grouping_Teams','')
    if team not in TEAM_TO_AREA: continue

    name = clean_name(r['entity_name'])
    if name in SKIP_NAMES: continue

    # Collect ALL MXG features for insights
    if name not in seen_all:
        seen_all.add(name)
        all_mxg_features.append({'name': name, 'area': TEAM_TO_AREA[team], 'team': TEAM_SHORT[team]})

    # Roadmap items: only properly visible 2026 features
    col, month = classify(r)
    if col is None: continue
    if r.get('Roadmap Visibility','') not in ('External','Internal'): continue
    if name in seen_roadmap: continue
    seen_roadmap.add(name)

    roadmap_features.append({
        'name':       name,
        'area':       TEAM_TO_AREA[team],
        'team':       TEAM_SHORT[team],
        'status':     col,
        'month':      month,
        'confidence': r.get('Release Confidence %','').strip(),
        'visibility': r.get('Roadmap Visibility','').strip(),
        'desc':       clean_desc(r.get('description','')),
        'pbUrl':      r.get('pb_url','').strip(),
    })

AREA_ORDER = {'Legacy Process Manager':0,'Suite Repository':1,'Process Modeler':2}
COL_ORDER  = {'DONE':0,'NOW':1,'LATER':2}
roadmap_features.sort(key=lambda x:(AREA_ORDER.get(x['area'],9),COL_ORDER.get(x['status'],9),x['name']))

# ── Read Insights CSV ─────────────────────────────────────────────────────────
with open(INSIGHTS_CSV, 'r', encoding='utf-8-sig') as f:
    ins_rows = list(csv.DictReader(f))

# Match insights against ALL MXG features
all_name_map = {f['name'].lower(): f['name'] for f in all_mxg_features}

def best_match(fname):
    if not fname: return None
    fl = fname.lower().strip()
    if fl in all_name_map: return all_name_map[fl]
    for k, v in all_name_map.items():
        if k in fl or fl in k: return v
    return None

insights_by_feature = defaultdict(list)

for row in ins_rows:
    fname   = (row.get('feature_name') or '').strip()
    matched = best_match(fname)
    company = (row.get('company_name') or '').strip()
    state   = (row.get('state') or '').strip()
    title   = (row.get('note_title') or '').strip()
    text    = (row.get('note_text') or '').strip()[:200]
    date    = (row.get('created_at') or '')[:7]
    tags    = (row.get('tags') or '').strip()

    if state == 'Archived': continue
    if not company or company.lower() in ('sap','sap signavio','sap se','sap signavio presales','sap signavio mxc'): continue
    if not title or title.lower() == 'unknown feedback': continue
    if matched:
        insights_by_feature[matched].append({
            'title': title, 'text': text, 'company': company,
            'state': state, 'date': date, 'tags': tags,
        })

# Enrich roadmap features with insight counts
for f in roadmap_features:
    ins = insights_by_feature.get(f['name'], [])
    f['insightsCount'] = len(ins)
    f['topCompanies']  = list(dict.fromkeys(i['company'] for i in ins))[:5]
    f['insights']      = sorted(ins, key=lambda x: x['date'], reverse=True)[:8]

# Build INSIGHTS_DATA: roadmap features first, then non-roadmap MXG features with insights
insights_data = []
seen_ins = set()

for f in roadmap_features:
    if f['name'] not in seen_ins and f.get('insights'):
        seen_ins.add(f['name'])
        insights_data.append({
            'featureName':   f['name'],
            'area':          f['area'],
            'status':        f['status'],
            'insightsCount': f['insightsCount'],
            'topCompanies':  f['topCompanies'],
            'insights':      f['insights'],
        })

for f in all_mxg_features:
    if f['name'] not in seen_ins:
        ins = insights_by_feature.get(f['name'], [])
        if ins:
            seen_ins.add(f['name'])
            companies = list(dict.fromkeys(i['company'] for i in ins))[:5]
            recent    = sorted(ins, key=lambda x: x['date'], reverse=True)[:8]
            insights_data.append({
                'featureName':   f['name'],
                'area':          f['area'],
                'status':        'IDEA',
                'insightsCount': len(ins),
                'topCompanies':  companies,
                'insights':      recent,
            })

insights_data.sort(key=lambda x: -x['insightsCount'])

# ── Print summary to stderr ───────────────────────────────────────────────────
sys.stderr.write('\n=== ROADMAP FEATURES ===\n')
for f in roadmap_features:
    sys.stderr.write(
        f"  [{f['status']:5}] [{f['area'][:22]:22}] [{f.get('confidence',''):6}]"
        f" [{f['month'] or '—':14}] {f['name'][:50]}\n"
    )
sys.stderr.write(f'\nTotal roadmap: {len(roadmap_features)}\n')
sys.stderr.write(f'Features with insights: {sum(1 for f in insights_data if f["insightsCount"]>0)}\n')
sys.stderr.write(f'Total insights: {sum(f["insightsCount"] for f in insights_data)}\n')

# ── Output JS blocks ──────────────────────────────────────────────────────────
def js_str(s):
    if s is None: return 'null'
    return "'" + str(s).replace('\\','\\\\').replace("'","\\'") + "'"

print('// AUTO-GENERATED — rebuild_enriched.py — 2026-05-06')
print('const ROADMAP_DATA = [')
last_area, last_col = None, None
for f in roadmap_features:
    if f['area'] != last_area:
        if last_area: print()
        print(f"  // ── {f['area']} ──")
        last_area, last_col = f['area'], None
    if f['status'] != last_col:
        labels = {'DONE':'DONE — Jan-Mar 2026','NOW':'NOW — Apr-Jun 2026','LATER':'LATER — Jul-Dec 2026'}
        print(f"  // {labels[f['status']]}")
        last_col = f['status']
    print(
        f"  {{ name:{js_str(f['name'])}, area:{js_str(f['area'])}, team:{js_str(f['team'])}, "
        f"status:{js_str(f['status'])}, month:{js_str(f['month'])}, "
        f"confidence:{js_str(f['confidence'])}, visibility:{js_str(f['visibility'])}, "
        f"insightsCount:{f['insightsCount'] or 'null'}, "
        f"pbUrl:{js_str(f['pbUrl']) if f['pbUrl'] else 'null'}, "
        f"desc:{js_str(f['desc'])} }},"
    )
print('];')

print()
print('const INSIGHTS_DATA = [')
for f in insights_data:
    if not f['insights']: continue
    ins_js       = json.dumps(f['insights'], ensure_ascii=False)
    companies_js = json.dumps(f['topCompanies'], ensure_ascii=False)
    print(
        f"  {{ featureName:{js_str(f['featureName'])}, area:{js_str(f['area'])}, "
        f"status:{js_str(f['status'])}, insightsCount:{f['insightsCount']}, "
        f"topCompanies:{companies_js}, insights:{ins_js} }},"
    )
print('];')
