"""
patch_dataobjects_es.py
Renames the 6 DataObject shapes in the Spanish Payroll model to Spanish,
creates EN + ES glossary entries for them, embeds glossaryLinks, and submits.
"""
import sys, io, copy, urllib.parse, time
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib import get_auth, fetch_model, submit_model

MODEL_ID = '407543a9285e43c5925f97104abef719'

NAME_MAP = {
    'Payroll data':       'Datos de nómina',
    'Payroll data alert': 'Alerta de datos de nómina',
}

# (stencil, en_name, es_name, en_desc, es_desc)
DICT_ENTRIES = [
    (
        'DataObject',
        'Payroll data',
        'Datos de nómina',
        'Data object representing payroll records relevant to the alert.',
        'Objeto de datos que representa los registros de nómina relacionados con la alerta.',
    ),
    (
        'DataObject',
        'Payroll data alert',
        'Alerta de datos de nómina',
        'Data object representing a triggered payroll data alert requiring resolution.',
        'Objeto de datos que representa una alerta de nómina activada que requiere resolución.',
    ),
]

STENCIL_SET = {'DataObject'}

def stencil_meta(stencil, cats):
    return 'DOCUMENT', cats.get('documentsCategory', '')

def create_entry(auth, title, etype, cat, desc, lang, replaced_id=None):
    params = {'title': title, 'type': etype, 'category': cat,
              'description': desc, 'language': lang}
    if replaced_id:
        params['replacedItemIds'] = replaced_id
    for attempt in range(1, 4):
        try:
            r = auth.session.post(
                auth.api_base + '/glossary',
                data=urllib.parse.urlencode(params),
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                timeout=60,
            )
            if r.status_code == 200:
                gid = r.json()['href'].split('/')[-1]
                print(f'  OK  [{lang}] {title!r}  ({gid[:8]})')
                return gid
            if r.status_code == 409:
                sr = auth.session.get(auth.api_base + '/glossary',
                                      params={'filter': title[:25], 'limit': 200}, timeout=30)
                found = [x for x in sr.json() if x.get('rep', {}).get('title') == title]
                if found:
                    gid = found[0]['href'].split('/')[-1]
                    print(f'  409 [{lang}] {title!r}  (existing: {gid[:8]})')
                    return gid
            print(f'  ERR {r.status_code}: {title!r}')
            return None
        except Exception as exc:
            print(f'  TIMEOUT attempt {attempt}: {exc}')
            if attempt < 3:
                time.sleep(5)
    return None

def rename_and_link(shapes, name_map, link_map):
    renamed, linked = 0, 0
    for s in shapes:
        sid  = s.get('stencil', {}).get('id', '')
        name = s.get('properties', {}).get('name', '').strip()
        if sid == 'DataObject' and name in name_map:
            new_name = name_map[name]
            s['properties']['name'] = new_name
            renamed += 1
            gid = link_map.get(new_name)
            if gid:
                s['glossaryLinks'] = {'name': [f'/glossary/{gid}']}
                linked += 1
        r2, l2 = rename_and_link(s.get('childShapes', []), name_map, link_map)
        renamed += r2; linked += l2
    return renamed, linked

# ── Main ───────────────────────────────────────────────────────────────────────
auth = get_auth()

print('Step 1  Get glossary categories')
r = auth.session.get(auth.api_base + '/directory', timeout=30)
cats = next((x['rep'] for x in r.json() if x.get('rel') == 'glos'), {})
print(f'  documentsCategory: {cats.get("documentsCategory","?")[:40]}')

print('\nStep 2  Create EN + ES glossary entries for DataObjects')
es_map = {}
for (stencil, en_name, es_name, en_desc, es_desc) in DICT_ENTRIES:
    etype, ecat = stencil_meta(stencil, cats)
    en_id = create_entry(auth, en_name, etype, ecat, en_desc, 'en_us')
    if en_id:
        es_id = create_entry(auth, es_name, etype, ecat, es_desc, 'es_es', replaced_id=en_id)
        if es_id:
            es_map[es_name] = es_id
    time.sleep(0.3)
print(f'  ES entries: {len(es_map)} / {len(DICT_ENTRIES)}')

print('\nStep 3  Fetch model, rename DataObjects, embed links')
model, info = fetch_model(auth, MODEL_ID)
model = copy.deepcopy(model)
renamed, linked = rename_and_link(model.get('childShapes', []), NAME_MAP, es_map)
print(f'  Renamed: {renamed}  Linked: {linked}')

print('\nStep 4  Submit')
rev, updated = submit_model(auth, MODEL_ID, model, info,
                            comment='Translate DataObjects to Spanish + embed glossaryLinks')
print(f'  rev={rev}  updated={updated}')

print(f'\nDONE  https://editor.signavio.com/p/hub/model/{MODEL_ID}')
print('Re-publish from SPM UI to make rev visible in the Hub.')
