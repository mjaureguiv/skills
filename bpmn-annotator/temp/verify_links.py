"""
verify_links.py — inspect glossaryLinks in a model and report what's there.
"""
import sys, io, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib import get_auth, fetch_model

MODEL_ID = '407543a9285e43c5925f97104abef719'

STENCIL_SET = {
    'Task', 'Lane', 'Pool', 'DataObject', 'ITSystem', 'CollapsedPool',
    'StartNoneEvent', 'EndNoneEvent', 'EndMessageEvent',
    'IntermediateTimerEvent', 'IntermediateMessageEventCatching',
    'Exclusive_Databased_Gateway', 'Parallel_Gateway',
}

def walk(shapes, results):
    for s in shapes:
        sid  = s.get('stencil', {}).get('id', '')
        name = s.get('properties', {}).get('name', '').strip()
        if sid in STENCIL_SET and name and '\n' not in name:
            gl = s.get('glossaryLinks', {})
            results.append({
                'stencil': sid,
                'name':    name,
                'glossaryLinks': gl,
            })
        walk(s.get('childShapes', []), results)

auth = get_auth()
model, info = fetch_model(auth, MODEL_ID)

print(f'Model : {info["name"]}')
print(f'Parent: {info["parent"]}')
print()

results = []
walk(model.get('childShapes', []), results)

linked   = [r for r in results if r['glossaryLinks'].get('name')]
unlinked = [r for r in results if not r['glossaryLinks'].get('name')]

print(f'Linked   : {len(linked)} / {len(results)}')
print(f'Unlinked : {len(unlinked)} / {len(results)}')
print()

print('=== LINKED ===')
for r in linked:
    gl_ids = r['glossaryLinks']['name']
    print(f'  [{r["stencil"]}] {r["name"]!r}')
    for g in gl_ids:
        print(f'      → {g}')

if unlinked:
    print()
    print('=== UNLINKED ===')
    for r in unlinked:
        print(f'  [{r["stencil"]}] {r["name"]!r}  glossaryLinks={r["glossaryLinks"]!r}')

# Also dump the raw glossaryLinks from the first pool/lane to check key names
print()
print('=== RAW glossaryLinks dump (first 3 shapes with any glossaryLinks) ===')
count = 0
def raw_dump(shapes):
    global count
    for s in shapes:
        gl = s.get('glossaryLinks')
        if gl and count < 3:
            print(json.dumps({
                'stencil': s.get('stencil',{}).get('id'),
                'name':    s.get('properties',{}).get('name',''),
                'glossaryLinks': gl,
            }, ensure_ascii=False, indent=2))
            count += 1
        raw_dump(s.get('childShapes', []))

raw_dump(model.get('childShapes', []))
