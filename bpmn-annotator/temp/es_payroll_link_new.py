"""
es_payroll_link_new.py

Embeds the full ES glossaryLinks into the new Spanish Payroll model
(407543a9285e43c5925f97104abef719) using resolved IDs from es_payroll_result.json.
Then publishes it to the Collaboration Hub.
"""
import sys
import io
import copy
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib import get_auth, fetch_model, submit_model

NEW_MODEL_ID = '407543a9285e43c5925f97104abef719'

STENCIL_SET = {
    'Task', 'Lane', 'Pool', 'DataObject', 'ITSystem', 'CollapsedPool',
    'StartNoneEvent', 'EndNoneEvent', 'EndMessageEvent',
    'IntermediateTimerEvent', 'IntermediateMessageEventCatching',
    'Exclusive_Databased_Gateway', 'Parallel_Gateway',
}

# Full ES glossary IDs resolved from previous payroll run
ES_MAP = {
    'Departamento de Nómina':                    '0de46c0ab6cb4835a5b7f54c582685b7',
    'Agente de Nómina':                          'ade3eb79764e4f148fdbf0feb90cf02b',
    'Alinear con jefe o empleado':                    '3651074c8d304589b0c8d42aec5da3a9',
    'Alinear con admin. del sistema fuente':          '29a3e2d8c831404b8bfb8cc884fb830c',
    'Evaluar alerta':                                 '2a5a2acc50a2482cac89f6ab54574eb2',
    'Verificar datos en sistema fuente':              'eedd97f0307a42299b2bdb528675947c',
    'Corregir datos de nómina':                  '73a271b61d6c497c9c9606d10ca62dba',
    'Comentar y cerrar alerta':                       'e28e3f851da9446db8fed49a2caa1bc5',
    '¿La alerta requiere cambio de datos?':      '962918ef2087489b9de15df217703257',
    '¿Hay que actualizar en el sistema fuente?': '4dce47bcab4d48fbaa020e042c6b92ca',
    'Inicio':                                         '84360bfde3e04338bdc3bddbe301b6e9',
    'Fin':                                            '87456970d0664859be397a2958e6d66a',
}


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


print('=' * 60)
print(f'Target model: {NEW_MODEL_ID}')
print(f'ES entries  : {len(ES_MAP)}')
print('=' * 60)

auth = get_auth()

print('\nFetching model...')
model, info = fetch_model(auth, NEW_MODEL_ID)
model = copy.deepcopy(model)

print('Embedding glossaryLinks...')
n = embed_links(model.get('childShapes', []), ES_MAP)

rev, updated = submit_model(
    auth, NEW_MODEL_ID, model, info,
    comment='Dictionary: embed Spanish glossaryLinks',
)
print(f'  {n} links embedded  rev={rev}  updated={updated}')

print('\nPublishing to Collaboration Hub...')
r = auth.session.post(
    auth.api_base + f'/publish/{NEW_MODEL_ID}',
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
    timeout=30,
)
print(f'  publish status: {r.status_code}')

print()
print('=' * 60)
print(f'DONE  {n}/12 links embedded')
print(f'https://editor.signavio.com/p/hub/model/{NEW_MODEL_ID}')
print('=' * 60)
