import csv, sys, io, re
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Backup\M&C-external-+-internal.csv', 'r', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

TEAM_TO_AREA = {
    'Process Guardians: MXG': 'Legacy Process Manager',
    'Roots: MXG': 'Legacy Process Manager',
    'The Sims: MXG': 'Suite Repository',
    'Dictionary: MXG': 'Suite Repository',
    'Process Pioneers: MXG': 'Process Modeler',
    'Process Vanguards:MXG': 'Process Modeler',
    'Kestrel: MXG': 'Process Modeler',
}
AREA_ORDER = {'Legacy Process Manager':0,'Suite Repository':1,'Process Modeler':2}

months = ['November 2025','December 2025','January 2026','February 2026',
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
    if s in ('👏🏽 GA Release / Done', '😢 Dropped'):
        return 'DONE'
    if s == '🔔 Roll Out':
        return 'NOW'
    if s == '⚙️ In progress':
        if m in current or m in past or m is None:
            return 'NOW'
        if m in near:
            return 'NEXT'
    if s in ('✅ Accepted Idea', '🛠️ Ready for Dev'):
        if m in current or m in past:
            return 'NOW'
        if m in near:
            return 'NEXT'
        return 'LATER'
    if s == '🔍 Discovery':
        return 'LATER'
    return None  # exclude New idea

def short_desc(desc):
    desc = re.sub(r'\\\.', '.', desc)
    desc = re.sub(r'\\([^\n])', r'\1', desc)
    desc = re.sub(r'\*+', '', desc)
    desc = re.sub(r'#+\s*', '', desc)
    desc = re.sub(r'\n+', ' ', desc)
    desc = re.sub(r'!\[.*?\]\(.*?\)', '', desc)  # remove images
    desc = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', desc)  # link text only
    desc = re.sub(r'\s+', ' ', desc).strip()
    # Try to extract after key header
    m = re.search(r'(?:Value [Pp]roposition|[Vv]alue [Pp]rop)[: ]+(.{30,})', desc)
    if m:
        desc = m.group(1)
    elif re.match(r'(?i)(problem|challenge|issue)', desc):
        pass  # use as-is
    if len(desc) > 200:
        idx = desc.find('. ', 30, 200)
        desc = desc[:idx+1] if idx > 0 else desc[:200].rsplit(' ', 1)[0] + chr(8230)
    return desc

results = []
for r in rows:
    if r['entity_type'] != 'Feature':
        continue
    if r['Roadmap Visibility'] not in ('External', 'Internal'):
        continue
    team = r['grouping_Teams']
    if team not in TEAM_TO_AREA:
        continue
    nnl = classify(r)
    if nnl is None or nnl == 'DONE':
        continue
    m = get_month(r) or '-'
    name = re.sub(r'^\[WIP\]\s*', '', r['entity_name'].strip())
    name = re.sub(r'[\U0001F1E0-\U0001F1FF]+\s*', '', name).strip()
    area = TEAM_TO_AREA[team]
    results.append({
        'name': name,
        'area': area,
        'status': nnl,
        'month': m,
        'vis': r['Roadmap Visibility'],
        'pbstatus': r['status_name'],
        'desc': short_desc(r['description']),
    })

NNL_ORDER = {'NOW': 0, 'NEXT': 1, 'LATER': 2}
results.sort(key=lambda x: (AREA_ORDER.get(x['area'], 9), NNL_ORDER.get(x['status'], 9), x['name']))

print(f"{'NNL':<6} {'AREA':<26} {'STATUS':<25} {'MON':<14} {'VIS':<10} NAME")
print('-'*115)
for r in results:
    print(f"{r['status']:<6} {r['area'][:25]:<26} {r['pbstatus'][:24]:<25} {r['month'][:13]:<14} {r['vis']:<10} {r['name'][:55]}")

print(f'\nTotal: {len(results)}')
