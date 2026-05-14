"""
es_payroll_setup.py

End-to-end script that:
  1. Fetches Payroll Department (96946c6a40ab4e0eb57f2c386142f689)
  2. Applies Spanish translations (original is NEVER modified)
  3. Creates the copy in Maria Playground (a731acfb31ad46dd81cf277aa9a66583)
  4. Adds numbered task badges to the copy
  5. Creates EN + ES dictionary entries for all named elements
  6. Embeds ES glossaryLinks into the copy (for Collaboration Hub Fact Sheet)
  7. Publishes the copy
"""
import sys
import io
import json
import copy
import urllib.parse
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib import (
    get_auth, fetch_model, submit_model, parse_model,
    apply_translations, build_number_badges, number_tasks, strip_task_numbers,
    create_model,
)

# ── Config ─────────────────────────────────────────────────────────────────────
SRC_MODEL   = '96946c6a40ab4e0eb57f2c386142f689'
DEST_FOLDER = 'a731acfb31ad46dd81cf277aa9a66583'
NEW_NAME    = 'Departamento de Nómina'

TRANSLATIONS = json.loads(
    (Path(__file__).parent / 'es_translations.json').read_text(encoding='utf-8')
)

# ── Glossary elements: (stencil, en_name, es_name, en_desc, es_desc) ──────────
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

STENCIL_SET = {
    'Task', 'Lane', 'Pool', 'DataObject', 'ITSystem', 'CollapsedPool',
    'StartNoneEvent', 'EndNoneEvent', 'EndMessageEvent',
    'IntermediateTimerEvent', 'IntermediateMessageEventCatching',
    'Exclusive_Databased_Gateway', 'Parallel_Gateway',
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def get_glossary_categories(auth):
    r = auth.session.get(auth.api_base + '/directory')
    data = r.json()
    return next((x['rep'] for x in data if x.get('rel') == 'glos'), {})


def stencil_meta(stencil, cats):
    """Return (entry_type, category_path) for a given stencil."""
    if stencil == 'Task':
        return 'ACTIVITY', cats.get('activitiesCategory', '')
    if stencil in ('Lane', 'Pool', 'CollapsedPool'):
        return 'ORGANIZATION', cats.get('organizationalUnitCategory', '')
    if 'Gateway' in stencil:
        return 'ORGANIZATION', cats.get('organizationalUnitCategory', '')
    if 'Event' in stencil:
        return 'STATE', cats.get('stateCategory', '')
    return 'UNDEFINED', cats.get('organizationalUnitCategory', '')


def create_entry(auth, title, etype, cat, desc, lang, replaced_id=None):
    """Create glossary entry; on 409 retrieve existing ID via search."""
    params = {
        'title': title, 'type': etype,
        'category': cat, 'description': desc, 'language': lang,
    }
    if replaced_id:
        params['replacedItemIds'] = replaced_id

    r = auth.session.post(
        auth.api_base + '/glossary',
        data=urllib.parse.urlencode(params),
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        timeout=15,
    )
    if r.status_code == 200:
        gid = r.json()['href'].split('/')[-1]
        print(f'  OK  [{lang}] {title!r}  ({gid[:8]})')
        return gid
    if r.status_code == 409:
        # Entry already exists — retrieve via search
        sr = auth.session.get(
            auth.api_base + '/glossary',
            params={'filter': title[:25], 'limit': 200},
        )
        found = [x for x in sr.json() if x.get('rep', {}).get('title') == title]
        if found:
            gid = found[0]['href'].split('/')[-1]
            print(f'  409 [{lang}] {title!r}  (existing: {gid[:8]})')
            return gid
        print(f'  WARN 409 but not found in search: {title!r}')
        return None
    print(f'  ERR {r.status_code}: {title!r} — {r.text[:80]}')
    return None


def embed_links(shapes, name_map):
    """Recursively embed glossaryLinks using the 'name' key (not 'title')."""
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
print('Step 1  Authenticate + fetch source model')
print('=' * 60)
auth = get_auth()
model, info = fetch_model(auth, SRC_MODEL)
parsed = parse_model(model)
print(f'  Source : {info["name"]}')
print(f'  Parent : {info["parent"]}')
print(f'  Tasks  : {len(parsed["tasks"])}  Lanes: {len(parsed["lanes"])}')
print(f'  Gways  : {len(parsed["gateways"])}  Events: {len(parsed["events"])}')

# ═══════════════════════════════════════════════════════════════════════════════
print()
print('=' * 60)
print('Step 2  Apply Spanish translations (in-memory only)')
print('=' * 60)
es_model = copy.deepcopy(model)
warnings = apply_translations(es_model, TRANSLATIONS)
for w in warnings:
    print(f'  WARN: {w}')
print('  Translations applied (original model untouched).')

# ═══════════════════════════════════════════════════════════════════════════════
print()
print('=' * 60)
print('Step 3  Create Spanish copy in Maria Playground')
print('=' * 60)
parent = f'/directory/{DEST_FOLDER}'
new_model_id = create_model(
    auth, NEW_NAME, parent, es_model,
    namespace=info.get('namespace', 'http://b3mn.org/stencilset/bpmn2.0#'),
    model_type=info.get('type', 'Business Process Diagram (BPMN 2.0)'),
    comment=f'BPMN Translator: Spanish translation of Payroll Department',
)
new_info = {'name': NEW_NAME, 'parent': parent}
print(f'  Created : {NEW_NAME}')
print(f'  Model ID: {new_model_id}')
print(f'  URL     : https://editor.signavio.com/p/hub/model/{new_model_id}')

# ═══════════════════════════════════════════════════════════════════════════════
print()
print('=' * 60)
print('Step 4  Add numbered task badges to Spanish copy')
print('=' * 60)
# Fetch fresh copy (POST may not return full JSON back)
es_model2, es_info2 = fetch_model(auth, new_model_id)
es_parsed2 = parse_model(es_model2)

# Remove any pre-existing badges (should be none, but be safe)
es_model2['childShapes'] = [
    s for s in es_model2['childShapes']
    if not s.get('resourceId', '').startswith('sid-BA-BADGE-')
]
strip_task_numbers(es_model2['childShapes'])
number_tasks(es_model2['childShapes'], es_parsed2)
badge_shapes = build_number_badges(es_model2, es_parsed2)
es_model2['childShapes'].extend(badge_shapes)

rev, updated = submit_model(
    auth, new_model_id, es_model2, es_info2,
    comment='BPMN Annotator: numbering_only',
)
print(f'  {len(badge_shapes)} badges added  rev={rev}  updated={updated}')

# ═══════════════════════════════════════════════════════════════════════════════
print()
print('=' * 60)
print('Step 5  Get glossary categories from tenant')
print('=' * 60)
cats = get_glossary_categories(auth)
print(f'  activitiesCategory        : {cats.get("activitiesCategory","?")[:40]}')
print(f'  organizationalUnitCategory: {cats.get("organizationalUnitCategory","?")[:40]}')
print(f'  stateCategory             : {cats.get("stateCategory","?")[:40]}')

# ═══════════════════════════════════════════════════════════════════════════════
print()
print('=' * 60)
print('Step 6  Create EN + ES dictionary entries')
print('=' * 60)
en_map = {}  # en_name -> glos_id
es_map = {}  # es_name -> glos_id

for (stencil, en_name, es_name, en_desc, es_desc) in DICT_ENTRIES:
    etype, ecat = stencil_meta(stencil, cats)
    # EN entry
    en_id = create_entry(auth, en_name, etype, ecat, en_desc, 'en_us')
    if en_id:
        en_map[en_name] = en_id
        # ES entry linked to EN
        es_id = create_entry(auth, es_name, etype, ecat, es_desc, 'es_es',
                             replaced_id=en_id)
        if es_id:
            es_map[es_name] = es_id

print(f'\n  EN entries created/found: {len(en_map)} / {len(DICT_ENTRIES)}')
print(f'  ES entries created/found: {len(es_map)} / {len(DICT_ENTRIES)}')

# ═══════════════════════════════════════════════════════════════════════════════
print()
print('=' * 60)
print('Step 7  Embed ES glossaryLinks into Spanish model')
print('=' * 60)
es_model3, es_info3 = fetch_model(auth, new_model_id)
es_model3 = copy.deepcopy(es_model3)
n = embed_links(es_model3.get('childShapes', []), es_map)
rev2, updated2 = submit_model(
    auth, new_model_id, es_model3, es_info3,
    comment='Dictionary: embed Spanish glossaryLinks',
)
print(f'  {n} links embedded  rev={rev2}  updated={updated2}')

# ═══════════════════════════════════════════════════════════════════════════════
print()
print('=' * 60)
print('Step 8  Publish model to Collaboration Hub')
print('=' * 60)
r = auth.session.post(
    auth.api_base + f'/publish/{new_model_id}',
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
    timeout=15,
)
print(f'  publish status: {r.status_code}')

# ═══════════════════════════════════════════════════════════════════════════════
print()
print('╔' + '═' * 58 + '╗')
print('║  COMPLETE                                                ║')
print('╠' + '═' * 58 + '╣')
print(f'║  Model  : {NEW_NAME:<46}  ║')
print(f'║  ID     : {new_model_id:<46}  ║')
print(f'║  Badges : {len(badge_shapes):<46}  ║')
print(f'║  Links  : {n} ES glossary links embedded{" "*(46-len(str(n))-26)}  ║')
print('╠' + '═' * 58 + '╣')
print('║  Original model UNCHANGED:                               ║')
print(f'║  {SRC_MODEL:<56}  ║')
print('╚' + '═' * 58 + '╝')
print()
print(f'New model URL:')
print(f'  https://editor.signavio.com/p/hub/model/{new_model_id}')
print()
print('Note: to see dictionary links in the Collaboration Hub,')
print('right-click the Maria Playground folder in SPM and')
print('select "Publish to Hub" if not already published.')

# ═══════════════════════════════════════════════════════════════════════════════
# Save model ID for reference
out = {
    'new_model_id': new_model_id,
    'new_name': NEW_NAME,
    'source_model_id': SRC_MODEL,
    'dest_folder': DEST_FOLDER,
    'badge_count': len(badge_shapes),
    'dict_links_embedded': n,
    'en_map': en_map,
    'es_map': es_map,
    'url': f'https://editor.signavio.com/p/hub/model/{new_model_id}',
}
out_path = Path(__file__).parent / 'es_payroll_result.json'
out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Result saved to: {out_path}')
