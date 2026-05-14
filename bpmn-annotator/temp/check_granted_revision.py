"""
check_granted_revision.py
Fetches the granted (Hub-visible) revision and checks whether glossaryLinks
are present in it. Also checks the current revision for comparison.
"""
import sys, io, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib import get_auth

MODEL_ID = '407543a9285e43c5925f97104abef719'

STENCIL_SET = {
    'Task', 'Lane', 'Pool', 'CollapsedPool',
    'StartNoneEvent', 'EndNoneEvent', 'EndMessageEvent',
    'Exclusive_Databased_Gateway', 'Parallel_Gateway',
}

def count_links(shapes):
    linked, total = 0, 0
    for s in shapes:
        sid  = s.get('stencil', {}).get('id', '')
        name = s.get('properties', {}).get('name', '').strip()
        if sid in STENCIL_SET and name and '\n' not in name:
            total += 1
            if s.get('glossaryLinks', {}).get('name'):
                linked += 1
        cl, ct = count_links(s.get('childShapes', []))
        linked += cl; total += ct
    return linked, total

auth = get_auth()

# 1. Fresh model info
r = auth.session.get(auth.api_base + f'/model/{MODEL_ID}/info', timeout=15)
info = r.json()
print(f'Model        : {info["name"]}')
print(f'Latest rev   : {info["rev"]}')
print(f'Granted rev  : {info["granted_revision_number"]}')
print(f'Status.publish: {info["status"]["publish"]}')
print(f'Granted href  : {info["granted_revision"]}')
print()

# 2. Check glossaryLinks in the GRANTED revision
granted_href = info['granted_revision']  # e.g. /revision/abc...
granted_id   = granted_href.split('/')[-1]
print(f'=== Fetching GRANTED revision ({info["granted_revision_number"]}) ===')
r2 = auth.session.get(auth.api_base + f'{granted_href}/json', timeout=30)
granted_model = r2.json()
gl, gt = count_links(granted_model.get('childShapes', []))
print(f'glossaryLinks in granted rev: {gl} / {gt} named elements')

# 3. Check glossaryLinks in the LATEST revision
print(f'\n=== Fetching LATEST revision ({info["rev"]}) ===')
r3 = auth.session.get(auth.api_base + info['revision'] + '/json', timeout=30)
latest_model = r3.json()
ll, lt = count_links(latest_model.get('childShapes', []))
print(f'glossaryLinks in latest  rev: {ll} / {lt} named elements')

# 4. Diagnosis
print()
if gl == 0 and ll > 0:
    print('ROOT CAUSE: Hub is serving the granted revision which has NO glossaryLinks.')
    print(f'  Granted rev {info["granted_revision_number"]} = no links')
    print(f'  Latest  rev {info["rev"]} = {ll} links embedded')
    print()
    print('FIX: Re-publish the model from SPM UI to advance the')
    print('     granted revision to the latest (rev {}).'.format(info["rev"]))
elif gl > 0:
    print(f'Granted revision already has {gl} links — Hub should show them.')
    print('Issue may be browser cache or Hub publish timing.')
else:
    print('Both granted and latest have no links — re-embedding needed.')
