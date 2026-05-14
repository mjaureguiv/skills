"""
es_payroll_dict.py

Continuation of es_payroll_setup.py — runs Steps 5-8 only.
The Spanish model (d5d14c5a056a44768dcf960d3b9e21c6) is already created with badges.
This script creates EN+ES dictionary entries and embeds glossaryLinks.
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

# ── Known IDs ──────────────────────────────────────────────────────────────────
NEW_MODEL_ID = 'd5d14c5a056a44768dcf960d3b9e21c6'
DEST_FOLDER  = 'a731acfb31ad46dd81cf277aa9a66583'

STENCIL_SET = {
    'Task', 'Lane', 'Pool', 'DataObject', 'ITSystem', 'CollapsedPool',
    'StartNoneEvent', 'EndNoneEvent', 'EndMessageEvent',
    'IntermediateTimerEvent', 'IntermediateMessageEventCatching',
    'Exclusive_Databased_Gateway', 'Parallel_Gateway',
}

# (stencil, en_name, es_name, en_desc, es_desc)
DICT_ENTRIES = [
    (
        'Pool',
        'Payroll Department',
        'Departamento de Nómina',
        'Department responsible for managing payroll alerts and data corrections.',
        'Departamento responsable de gestionar alertas y correcciones de nómina.',
    ),
    (
        'Lane',
        'Payroll Agent',
        'Agente de Nómina',
        'Role responsible for processing and resolving payroll alerts.',
        'Rol responsable de procesar y resolver alertas de nómina.',
    ),
    (
        'Task',
        'Align with line manager or employee',
        'Alinear con jefe o empleado',
        'Coordinates with the line manager or employee to verify payroll data.',
        'Coordina con el responsable jerárquico o empleado para verificar datos.',
    ),
    (
        'Task',
        'Align with source system administrator',
        'Alinear con admin. del sistema fuente',
        'Coordinates with the source system administrator to resolve data discrepancies.',
        'Coordina con el administrador del sistema fuente para resolver discrepancias.',
    ),
    (
        'Task',
        'Assess alert',
        'Evaluar alerta',
        'Reviews and assesses the incoming payroll alert to determine required action.',
        'Revisa y evalúa la alerta de nómina recibida para determinar la acción necesaria.',
    ),
    (
        'Task',
        'Check if data needs to be updated in source system',
        'Verificar datos en sistema fuente',
        'Determines whether a data correction is required in the originating system.',
        'Determina si se requiere una corrección de datos en el sistema de origen.',
    ),
    (
        'Task',
        'Correct payroll-specific data',
        'Corregir datos de nómina',
        'Updates payroll-specific data directly in the payroll system.',
        'Actualiza los datos específicos de nómina directamente en el sistema.',
    ),
    (
        'Task',
        'Provide comment and close alert',
        'Comentar y cerrar alerta',
        'Adds a resolution comment to the payroll alert and marks it as closed.',
        'Añade un comentario de resolución a la alerta de nómina y la cierra.',
    ),
    (
        'Exclusive_Databased_Gateway',
        'Does the alert require a data change?',
        '¿La alerta requiere cambio de datos?',
        'Decision: determines whether the payroll alert requires a data modification.',
        'Decisión: determina si la alerta de nómina requiere una modificación de datos.',
    ),
    (
        'Exclusive_Databased_Gateway',
        'Does the data need to be updated in the source system?',
        '¿Hay que actualizar en el sistema fuente?',
        'Decision: determines whether the correction must be applied in the source system.',
        'Decisión: determina si la corrección debe aplicarse en el sistema de origen.',
    ),
    (
        'StartNoneEvent',
        'Start',
        'Inicio',
        'The process begins when a payroll alert is triggered in the system.',
        'El proceso comienza cuando se genera una alerta de nómina en el sistema.',
    ),
    (
        'EndNoneEvent',
        'End',
        'Fin',
        'The process ends when the payroll alert has been resolved or closed.',
        'El proceso finaliza cuando la alerta de nómina ha sido resuelta o cerrada.',
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


def create_entry(auth, title, etype, cat, desc, lang, replaced_id=None, retries=3):
    """Create glossary entry with retry on timeout. 409 → search existing."""
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
                sr = auth.session.get(
                    auth.api_base + '/glossary',
                    params={'filter': title[:25], 'limit': 200},
                    timeout=60,
                )
                found = [x for x in sr.json()
                         if x.get('rep', {}).get('title') == title]
                if found:
                    gid = found[0]['href'].split('/')[-1]
                    print(f'  409 [{lang}] {title!r}  (existing: {gid[:8]})')
                    return gid
                print(f'  WARN 409 not found in search: {title!r}')
                return None
            print(f'  ERR {r.status_code}: {title!r} — {r.text[:80]}')
            return None
        except Exception as exc:
            print(f'  TIMEOUT attempt {attempt}/{retries}: {title!r} — {exc}')
            if attempt < retries:
                time.sleep(5)
    print(f'  FAILED after {retries} attempts: {title!r}')
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
print('Step 5  Authenticate + get glossary categories')
print('=' * 60)
auth = get_auth()
r = auth.session.get(auth.api_base + '/directory', timeout=30)
cats = next((x['rep'] for x in r.json() if x.get('rel') == 'glos'), {})
print(f'  activitiesCategory        : {cats.get("activitiesCategory","?")[:40]}')
print(f'  organizationalUnitCategory: {cats.get("organizationalUnitCategory","?")[:40]}')
print(f'  stateCategory             : {cats.get("stateCategory","?")[:40]}')

# ═══════════════════════════════════════════════════════════════════════════════
print()
print('=' * 60)
print('Step 6  Create EN + ES dictionary entries (timeout=60s, 3 retries)')
print('=' * 60)
en_map = {}
es_map = {}

for (stencil, en_name, es_name, en_desc, es_desc) in DICT_ENTRIES:
    etype, ecat = stencil_meta(stencil, cats)
    en_id = create_entry(auth, en_name, etype, ecat, en_desc, 'en_us')
    if en_id:
        en_map[en_name] = en_id
        es_id = create_entry(auth, es_name, etype, ecat, es_desc, 'es_es',
                             replaced_id=en_id)
        if es_id:
            es_map[es_name] = es_id
    time.sleep(0.3)   # brief pause between pairs to avoid hammering the API

print(f'\n  EN entries: {len(en_map)} / {len(DICT_ENTRIES)}')
print(f'  ES entries: {len(es_map)} / {len(DICT_ENTRIES)}')

if es_map:
    print('\n  ES map:')
    for k, v in es_map.items():
        print(f'    {k!r} → {v[:8]}')

# ═══════════════════════════════════════════════════════════════════════════════
print()
print('=' * 60)
print('Step 7  Embed ES glossaryLinks into Spanish model')
print('=' * 60)
es_model, es_info = fetch_model(auth, NEW_MODEL_ID)
es_model = copy.deepcopy(es_model)
n = embed_links(es_model.get('childShapes', []), es_map)
rev, updated = submit_model(
    auth, NEW_MODEL_ID, es_model, es_info,
    comment='Dictionary: embed Spanish glossaryLinks',
)
print(f'  {n} links embedded  rev={rev}  updated={updated}')

# ═══════════════════════════════════════════════════════════════════════════════
print()
print('=' * 60)
print('Step 8  Publish to Collaboration Hub')
print('=' * 60)
r = auth.session.post(
    auth.api_base + f'/publish/{NEW_MODEL_ID}',
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
    timeout=30,
)
print(f'  publish status: {r.status_code}')

# ═══════════════════════════════════════════════════════════════════════════════
print()
print('╔' + '═' * 58 + '╗')
print('║  DICTIONARY LINKING COMPLETE                             ║')
print('╠' + '═' * 58 + '╣')
print(f'║  Model ID : {NEW_MODEL_ID:<45}  ║')
print(f'║  EN entries: {len(en_map):<43}  ║')
print(f'║  ES entries: {len(es_map):<43}  ║')
print(f'║  Links embedded: {n:<39}  ║')
print('╚' + '═' * 58 + '╝')
print(f'\nhttps://editor.signavio.com/p/hub/model/{NEW_MODEL_ID}')

# Save result
out_path = Path(__file__).parent / 'es_payroll_result.json'
existing = {}
if out_path.exists():
    try:
        existing = json.loads(out_path.read_text(encoding='utf-8'))
    except Exception:
        pass
existing.update({
    'new_model_id': NEW_MODEL_ID,
    'dict_links_embedded': n,
    'en_map': en_map,
    'es_map': es_map,
    'url': f'https://editor.signavio.com/p/hub/model/{NEW_MODEL_ID}',
})
out_path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Result saved to: {out_path}')
