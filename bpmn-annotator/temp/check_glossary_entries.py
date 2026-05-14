"""
check_glossary_entries.py — verify that ES glossary entry IDs are reachable.
"""
import sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib import get_auth

ES_MAP = {
    'Departamento de Nómina':                    '0de46c0ab6cb4835a5b7f54c582685b7',
    'Agente de Nómina':                          'ade3eb79764e4f148fdbf0feb90cf02b',
    'Alinear con jefe o empleado':               '3651074c8d304589b0c8d42aec5da3a9',
    'Alinear con admin. del sistema fuente':     '29a3e2d8c831404b8bfb8cc884fb830c',
    'Evaluar alerta':                            '2a5a2acc50a2482cac89f6ab54574eb2',
    'Verificar datos en sistema fuente':         'eedd97f0307a42299b2bdb528675947c',
    'Corregir datos de nómina':                  '73a271b61d6c497c9c9606d10ca62dba',
    'Comentar y cerrar alerta':                  'e28e3f851da9446db8fed49a2caa1bc5',
    '¿La alerta requiere cambio de datos?':      '962918ef2087489b9de15df217703257',
    '¿Hay que actualizar en el sistema fuente?': '4dce47bcab4d48fbaa020e042c6b92ca',
    'Inicio':                                    '84360bfde3e04338bdc3bddbe301b6e9',
    'Fin':                                       '87456970d0664859be397a2958e6d66a',
}

auth = get_auth()

ok, missing = [], []
for name, gid in ES_MAP.items():
    r = auth.session.get(auth.api_base + f'/glossary/{gid}', timeout=15)
    if r.status_code == 200:
        rep = next((x.get('rep', {}) for x in r.json() if x.get('rel') == 'info'), {})
        lang = rep.get('language', '?')
        title = rep.get('title', '?')
        ok.append(f'  OK {r.status_code}  [{lang}] {title!r}  ({gid[:8]})')
    else:
        missing.append(f'  ERR {r.status_code}  {name!r}  ({gid[:8]})')

print(f'Accessible: {len(ok)} / {len(ES_MAP)}')
for line in ok:
    print(line)
if missing:
    print(f'\nNot found ({len(missing)}):')
    for line in missing:
        print(line)
