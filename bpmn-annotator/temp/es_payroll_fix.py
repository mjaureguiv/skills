"""
es_payroll_fix.py

Fixes the 3 missing ES dictionary links in the Spanish Payroll model.
Missing: 'Departamento de Nomina' (Pool), 'Agente de Nomina' (Lane),
         'Alinear con jefe o empleado' (Task).

Approach: fetch the full glossary, find entries by exact title,
          create missing ones, then re-embed all 12 ES links.
"""
import sys
import io
import json
import copy
import time
import urllib.parse
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib import get_auth, fetch_model, submit_model

NEW_MODEL_ID = 'd5d14c5a056a44768dcf960d3b9e21c6'

STENCIL_SET = {
    'Task', 'Lane', 'Pool', 'DataObject', 'ITSystem', 'CollapsedPool',
    'StartNoneEvent', 'EndNoneEvent', 'EndMessageEvent',
    'IntermediateTimerEvent', 'IntermediateMessageEventCatching',
    'Exclusive_Databased_Gateway', 'Parallel_Gateway',
}

# Known good ES map from previous run
ES_MAP_KNOWN = {
    'Alinear con admin. del sistema fuente': '29a3e2d8',
    'Evaluar alerta':                         '2a5a2acc',
    'Verificar datos en sistema fuente':      'eedd97f0',
    'Corregir datos de nómina':               '73a271b6',
    'Comentar y cerrar alerta':               'e28e3f85',
    '¿La alerta requiere cambio de datos?':   '962918ef',
    '¿Hay que actualizar en el sistema fuente?': '4dce47bc',
    'Inicio':                                 '84360bfd',
    'Fin':                                    '87456970',
}
# NOTE: known IDs above are 8-char prefixes — script below fetches full IDs

# Missing ES entries to find/create
MISSING = [
    # (es_name, en_name, stencil, en_desc, es_desc)
    (
        'Departamento de Nómina',
        'Payroll Department',
        'Pool',
        'Department responsible for managing payroll alerts and data corrections.',
        'Departamento responsable de gestionar alertas y correcciones de nómina.',
    ),
    (
        'Agente de Nómina',
        'Payroll Agent',
        'Lane',
        'Role responsible for processing and resolving payroll alerts.',
        'Rol responsable de procesar y resolver alertas de nómina.',
    ),
    (
        'Alinear con jefe o empleado',
        'Align with line manager or employee',
        'Task',
        'Coordinates with the line manager or employee to verify payroll data.',
        'Coordina con el responsable jerárquico o empleado para verificar datos.',
    ),
]


def stencil_meta(stencil, cats):
    if stencil == 'Task':
        return 'ACTIVITY', cats.get('activitiesCategory', '')
    if stencil in ('Lane', 'Pool', 'CollapsedPool'):
        return 'ORGANIZATION', cats.get('organizationalUnitCategory', '')
    if 'Gateway' in stencil:
        return 'ORGANIZATION', cats.get('organizationalUnitCategory', '')
    if 'Event' in stencil:
        return 'STATE', cats.get('stateCategory', '')
    return 'UNDEFINED', cats.get('organizationalUnitCategory', '')


def fetch_all_glossary(auth, page_size=500):
    """Fetch ALL glossary entries, paginated. Returns list of {title: gid}."""
    all_entries = {}
    offset = 0
    while True:
        r = auth.session.get(
            auth.api_base + '/glossary',
            params={'offset': offset, 'limit': page_size},
            timeout=60,
        )
        data = r.json()
        if not data:
            break
        for e in data:
            title = e.get('rep', {}).get('title', '')
            gid   = e.get('href', '').split('/')[-1]
            if title and gid:
                all_entries[title] = gid
        if len(data) < page_size:
            break
        offset += page_size
        time.sleep(0.2)
    return all_entries


def create_entry(auth, title, etype, cat, desc, lang, replaced_id=None, retries=3):
    params = {
        'title': title, 'type': etype,
        'category': cat, 'description': desc, 'language': lang,
    }
    if replaced_id:
        params['replacedItemIds'] = replaced_id
    for attempt in range(1, retries + 1):
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
                print(f'  409 [{lang}] {title!r} — will find via full scan')
                return None  # caller handles via full scan
            print(f'  ERR {r.status_code}: {title!r} — {r.text[:80]}')
            return None
        except Exception as exc:
            print(f'  TIMEOUT attempt {attempt}/{retries}: {exc}')
            if attempt < retries:
                time.sleep(5)
    return None


def embed_links(shapes, name_map):
    count = 0
    for s in shapes:
        sid  = s.get('stencil', {}).get('id', '')
        name = s.get('properties', {}).get('name', '').strip()
        if sid in STENCIL_SET and name and '\n' not in name:
            gid = name_map.get(name)
            if gid:
                s['glossaryLinks'] = {'name': [f'/glossary/{gid}']}
                count += 1
        count += embed_links(s.get('childShapes', []), name_map)
    return count


# ═══════════════════════════════════════════════════════════════════════════════
print('=' * 60)
print('Step A  Authenticate')
print('=' * 60)
auth = get_auth()

r_dir = auth.session.get(auth.api_base + '/directory', timeout=30)
cats = next((x['rep'] for x in r_dir.json() if x.get('rel') == 'glos'), {})
print(f'  Categories fetched.')

# ═══════════════════════════════════════════════════════════════════════════════
print()
print('=' * 60)
print('Step B  Full glossary scan to find existing entries')
print('=' * 60)
print('  Fetching all glossary entries (this may take a moment)...')
all_glos = fetch_all_glossary(auth)
print(f'  Total entries in glossary: {len(all_glos)}')

# Check which of our known entries exist in the full scan
# (resolving 8-char prefix IDs → full IDs)
es_map = {}

# First, populate from known good list using full scan
for es_title, _short_id in ES_MAP_KNOWN.items():
    full_id = all_glos.get(es_title)
    if full_id:
        es_map[es_title] = full_id
        print(f'  FOUND  {es_title!r}  {full_id[:8]}')
    else:
        print(f'  MISS   {es_title!r}')

# ═══════════════════════════════════════════════════════════════════════════════
print()
print('=' * 60)
print('Step C  Find or create missing ES entries')
print('=' * 60)

for (es_name, en_name, stencil, en_desc, es_desc) in MISSING:
    etype, ecat = stencil_meta(stencil, cats)

    # Check if ES entry already exists in full scan
    if es_name in all_glos:
        es_map[es_name] = all_glos[es_name]
        print(f'  FOUND (scan)  ES {es_name!r}  {all_glos[es_name][:8]}')
        continue

    print(f'  Creating  ES {es_name!r}...')

    # Find or create EN entry
    en_id = all_glos.get(en_name)
    if en_id:
        print(f'    EN {en_name!r} exists: {en_id[:8]}')
    else:
        print(f'    EN {en_name!r} not in scan — creating...')
        en_id = create_entry(auth, en_name, etype, ecat, en_desc, 'en_us')
        if not en_id:
            # try scan again (in case of 409)
            all_glos2 = fetch_all_glossary(auth)
            en_id = all_glos2.get(en_name)
        if not en_id:
            print(f'    SKIP (could not get EN entry for {en_name!r})')
            continue

    # Create ES entry linked to EN
    es_id = create_entry(auth, es_name, etype, ecat, es_desc, 'es_es',
                         replaced_id=en_id)
    if es_id:
        es_map[es_name] = es_id
    else:
        # One more scan attempt
        time.sleep(2)
        all_glos3 = fetch_all_glossary(auth)
        if es_name in all_glos3:
            es_map[es_name] = all_glos3[es_name]
            print(f'    Found after retry: {es_name!r}  {all_glos3[es_name][:8]}')

print(f'\n  ES map now has {len(es_map)} entries (target: 12)')

# ═══════════════════════════════════════════════════════════════════════════════
print()
print('=' * 60)
print('Step D  Embed ALL ES links into Spanish model (full re-embed)')
print('=' * 60)
es_model, es_info = fetch_model(auth, NEW_MODEL_ID)
es_model = copy.deepcopy(es_model)
n = embed_links(es_model.get('childShapes', []), es_map)
rev, updated = submit_model(
    auth, NEW_MODEL_ID, es_model, es_info,
    comment='Dictionary: re-embed all Spanish glossaryLinks (full set)',
)
print(f'  {n} links embedded  rev={rev}  updated={updated}')

# ═══════════════════════════════════════════════════════════════════════════════
print()
print('=' * 60)
print('Step E  Publish to Collaboration Hub')
print('=' * 60)
r = auth.session.post(
    auth.api_base + f'/publish/{NEW_MODEL_ID}',
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
    timeout=30,
)
print(f'  publish status: {r.status_code}')

# ═══════════════════════════════════════════════════════════════════════════════
missing_final = [es for (es, _, __, ___, ____) in MISSING if es not in es_map]
print()
print('╔' + '═' * 58 + '╗')
print('║  FIX COMPLETE                                            ║')
print('╠' + '═' * 58 + '╣')
print(f'║  ES links embedded : {n:<35}  ║')
print(f'║  ES entries total  : {len(es_map)} / 12{" " * 30}  ║')
if missing_final:
    print(f'║  Still missing     : {", ".join(missing_final)[:35]:<35}  ║')
else:
    print(f'║  All 12 entries resolved.{" " * 31}  ║')
print('╚' + '═' * 58 + '╝')
print(f'\nhttps://editor.signavio.com/p/hub/model/{NEW_MODEL_ID}')

# Save updated result
out_path = Path(__file__).parent / 'es_payroll_result.json'
existing = {}
if out_path.exists():
    try:
        existing = json.loads(out_path.read_text(encoding='utf-8'))
    except Exception:
        pass
existing['es_map'] = es_map
existing['dict_links_embedded'] = n
out_path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Result updated: {out_path}')
