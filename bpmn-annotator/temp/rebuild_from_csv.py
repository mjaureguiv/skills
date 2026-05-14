"""
Rebuild ROADMAP_DATA from M&C-external-+-internal.csv
"""
import csv, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Backup\M&C-external-+-internal.csv', 'r', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

TEAM_TO_AREA = {
    'Process Guardians: MXG': 'Legacy Process Manager',
    'Roots: MXG':             'Legacy Process Manager',
    'The Sims: MXG':          'Suite Repository',
    'Dictionary: MXG':        'Suite Repository',
    'Process Pioneers: MXG':  'Process Modeler',
    'Process Vanguards:MXG':  'Process Modeler',
    'Kestrel: MXG':           'Process Modeler',
}

months  = ['November 2025','December 2025','January 2026','February 2026',
           'March 2026','April 2026','May 2026','June 2026']
past    = {'November 2025','December 2025','January 2026','February 2026','March 2026','April 2026'}
current = {'May 2026'}
near    = {'June 2026'}

def get_month(r):
    for m in months:
        if r.get(m,'').lower() == 'true':
            return m
    return None

def classify(r):
    s = r['status_name']
    m = get_month(r)
    if s in ('👏🏽 GA Release / Done','😢 Dropped'): return 'DONE'
    if s == '🔔 Roll Out':  return 'NOW'
    if s == '⚙️ In progress':
        if m in near:   return 'NEXT'
        return 'NOW'
    if s in ('✅ Accepted Idea','🛠️ Ready for Dev'):
        if m in current|past: return 'NOW'
        if m in near:         return 'NEXT'
        return 'LATER'
    if s == '🔍 Discovery': return 'LATER'
    return None  # New idea → skip

# Features to SKIP (too granular / purely internal engineering milestones)
SKIP_NAMES = {
    'Canvas foundation',
    'Canvas navigation',
    'Basic micro interactions',
    'Advanced micro interactions',
    'Shapes suggestion',
    'Context menu',
    'Toolbar',
    'Multi-locales',
    'Modeler App Lobby landing page',
    'Shapes Panel All Elements',
    'Shapes Panel Favorites',
    'New Process Modeler (GA) (WIP)',  # will be shown via consolidated entry
    '(Sims) AuditLogs implementation',
    'New Internal APIs for Bulk Creation of Dictionary entries for NGM',
    'Onboard Transformation Manager Initiatives and define standard attributes',
    'Suite Repo - Support Attribute Type Upload /Add URL',
}

# Deduplicate by name (same feature can appear under multiple teams)
seen_names = set()

def clean_name(name):
    name = re.sub(r'^\[WIP\]\s*', '', name.strip())
    name = re.sub(r'[\U0001F1E0-\U0001F1FF]+\s*', '', name)
    name = re.sub(r'\s+', ' ', name)
    return name.strip()

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
    if len(d) > 200:
        idx = d.find('. ', 30, 200)
        d = d[:idx+1] if idx > 0 else d[:200].rsplit(' ',1)[0] + chr(8230)
    return d

results = []
for r in rows:
    if r['entity_type'] != 'Feature': continue
    team = r['grouping_Teams']
    if team not in TEAM_TO_AREA: continue
    nnl = classify(r)
    if nnl is None or nnl == 'DONE': continue
    name = clean_name(r['entity_name'])
    if name in SKIP_NAMES: continue
    if name in seen_names: continue  # deduplicate
    if r['Roadmap Visibility'] not in ('External','Internal'): continue
    seen_names.add(name)
    results.append({
        'name': name,
        'area': TEAM_TO_AREA[team],
        'status': nnl,
        'quarter': None,
        'insightsCount': None,
        'desc': clean_desc(r['description']),
        'vis': r['Roadmap Visibility'],
    })

# Add consolidated entry for New Process Modeler (GA)
results.append({
    'name': 'New Process Modeler (GA)',
    'area': 'Process Modeler',
    'status': 'NEXT',
    'quarter': None,
    'insightsCount': None,
    'desc': 'The full generally-available release of the redesigned process modeler, bringing the complete modern modeling experience to all users.',
    'vis': 'Internal',
})

AREA_ORDER = {'Legacy Process Manager':0,'Suite Repository':1,'Process Modeler':2}
NNL_ORDER  = {'NOW':0,'NEXT':1,'LATER':2}
results.sort(key=lambda x:(AREA_ORDER.get(x['area'],9),NNL_ORDER.get(x['status'],9),x['name']))

# Print summary
print(f"{'NNL':<6} {'AREA':<26} {'VIS':<10} NAME")
print('-'*90)
for r in results:
    print(f"{r['status']:<6} {r['area'][:25]:<26} {r['vis']:<10} {r['name'][:55]}")
print(f'\nTotal: {len(results)}')

# Breakdown
from collections import Counter
ctr = Counter((r['area'],r['status']) for r in results)
print()
for (area,st),n in sorted(ctr.items(),key=lambda x:(AREA_ORDER.get(x[0][0],9),NNL_ORDER.get(x[0][1],9))):
    print(f'  {area} / {st}: {n}')

# Generate JS
print('\n\nconst ROADMAP_DATA = [')
last_area,last_status = None, None
for r in results:
    if r['area'] != last_area:
        if last_area: print()
        print(f"  // ── {r['area']} ──")
        last_area,last_status = r['area'],None
    if r['status'] != last_status:
        lbl = {'NOW':'NOW — in progress','NEXT':'NEXT — coming up','LATER':'LATER — horizon'}[r['status']]
        print(f'  // {lbl}')
        last_status = r['status']
    n = r['name'].replace("'","\\'")
    d = r['desc'].replace("'","\\'")
    q = f"'{r['quarter']}'" if r['quarter'] else 'null'
    ic = str(r['insightsCount']) if r['insightsCount'] else 'null'
    print(f"  {{ name:'{n}', area:'{r['area']}', status:'{r['status']}', quarter:{q}, insightsCount:{ic}, desc:'{d}' }},")
print('];')
