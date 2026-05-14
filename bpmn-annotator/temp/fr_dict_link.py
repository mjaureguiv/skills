"""
Create French (fr_fr) glossary entries for all 15 IT Requirements terms
and embed links into the French model in Maria Playground.

Run: py skills/bpmn-annotator/temp/fr_dict_link.py
"""
import sys, copy, urllib.parse
sys.path.insert(0, r'C:\Backup\signavio_process_consultant_experimental\mcp\signavio\spm\src')
sys.path.insert(0, r'C:\Signavio_PM_Agent\skills\bpmn-annotator')
from lib.auth  import get_auth
from lib.fetch import fetch_model, submit_model

auth = get_auth()

FR_MODEL_ID = '0f7f0a3656f741658b16d6d1b2935e14'

# EN glossary entry IDs (from SKILL.md catalogue)
GLOS_MAP_EN = {
    'IT Department':                               '554ef82cdca64b2aa2235f684b9a35ad',
    'Business Analyst':                            'aefc9f9b937944099e1c570d8cfe8cfb',
    'Process Expert':                              'de3d0a9c885f4ac2aaa70bce474203ab',
    'Document requirements in CRM':                'e398648bb85f4444957321a997145b9b',
    'Identify business requirements':              'c34a781a586c488da2d3ef534e00c4f5',
    'Review documented requirements':              '7c500cb1062d4a90850cbb85c0585246',
    'Refine requirements with requester':          '077538d063aa4d1f96df87c8a9b03deb',
    'Business Requirements':                       '0d5f0890f56c49f498941908113e4b02',
    'CRM':                                         '2e04f02c1dff4350871abe0823511dd8',
    'IT Project Started':                          '953bbd836c0448d9bcf0546c15b44211',
    'Requirements Finalized':                      '2a37525bfa914a4a8d6f0916eaa229ec',
    'Are clarifications needed on requirements?':  '168a2225d8414dbca0f3756471f17362',
    'ABC Company GmbH':                            '569c700ee3a34a4886e101abca88dec2',
    'HR Department':                               'ac244edefdae48e1906f84b29fa2ea04',
    'Line Manager':                                '0606d91e66ff4afeb5c0f05596d64753',
}

# French translations (same as what was applied in the model)
FR_NAMES = {
    'IT Department':                               'Service IT',
    'Business Analyst':                            'Analyste Metier',
    'Process Expert':                              'Expert Processus',
    'Document requirements in CRM':                'Documenter les exigences dans CRM',
    'Identify business requirements':              'Identifier les exigences metier',
    'Review documented requirements':              'Reviser les exigences documentees',
    'Refine requirements with requester':          'Affiner les exigences avec le demandeur',
    'Business Requirements':                       'Exigences Metier',
    'CRM':                                         'CRM',
    'IT Project Started':                          'Projet IT demarre',
    'Requirements Finalized':                      'Exigences finalisees',
    'Are clarifications needed on requirements?':  'Des clarifications sont-elles necessaires ?',
    'ABC Company GmbH':                            'ABC Company GmbH',
    'HR Department':                               'Departement RH',
    'Line Manager':                                'Responsable Hierarchique',
}

# ── Step 1: Get glossary category IDs from tenant ──────────────────────────────
print('Fetching glossary categories...')
r = auth.session.get(auth.api_base + '/directory')
r.raise_for_status()
glos = next((x['rep'] for x in r.json() if x.get('rel') == 'glos'), None)
if not glos:
    print('ERROR: could not find glossary in directory response')
    sys.exit(1)
CAT_ACTIVITY = glos['activitiesCategory']
CAT_ORG      = glos['organizationalUnitCategory']
CAT_STATE    = glos['stateCategory']
print(f'  CAT_ACTIVITY={CAT_ACTIVITY[:8]}  CAT_ORG={CAT_ORG[:8]}  CAT_STATE={CAT_STATE[:8]}')

# Entry type per EN term (inferred from context)
ENTRY_TYPES = {
    'IT Department':                               ('ORGANIZATION', CAT_ORG),
    'Business Analyst':                            ('ORGANIZATION', CAT_ORG),
    'Process Expert':                              ('ORGANIZATION', CAT_ORG),
    'Document requirements in CRM':                ('ACTIVITY',     CAT_ACTIVITY),
    'Identify business requirements':              ('ACTIVITY',     CAT_ACTIVITY),
    'Review documented requirements':              ('ACTIVITY',     CAT_ACTIVITY),
    'Refine requirements with requester':          ('ACTIVITY',     CAT_ACTIVITY),
    'Business Requirements':                       ('ORGANIZATION', CAT_ORG),
    'CRM':                                         ('ORGANIZATION', CAT_ORG),
    'IT Project Started':                          ('STATE',        CAT_STATE),
    'Requirements Finalized':                      ('STATE',        CAT_STATE),
    'Are clarifications needed on requirements?':  ('ORGANIZATION', CAT_ORG),
    'ABC Company GmbH':                            ('ORGANIZATION', CAT_ORG),
    'HR Department':                               ('ORGANIZATION', CAT_ORG),
    'Line Manager':                                ('ORGANIZATION', CAT_ORG),
}

# ── Step 2: Create or find FR glossary entries ─────────────────────────────────
print('\nCreating French glossary entries...')
fr_glos_map = {}  # fr_name -> fr_glos_id

for en_name, en_id in GLOS_MAP_EN.items():
    fr_name = FR_NAMES[en_name]
    etype, ecat = ENTRY_TYPES[en_name]
    payload = urllib.parse.urlencode({
        'title':          fr_name,
        'type':           etype,
        'category':       ecat,
        'description':    f'Traduction francaise de "{en_name}"',
        'language':       'fr_fr',
        'replacedItemIds': en_id,
    })
    r = auth.session.post(
        auth.api_base + '/glossary',
        data=payload,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        timeout=15,
    )
    if r.status_code == 200:
        gid = r.json().get('href', '').split('/')[-1]
        fr_glos_map[fr_name] = gid
        print(f'  OK   "{fr_name}"  ({gid[:8]}...)')
    elif r.status_code == 409:
        # Entry already exists — find via search
        sr = auth.session.get(auth.api_base + '/glossary',
                              params={'filter': fr_name[:20], 'limit': 200})
        found = [x for x in sr.json() if x.get('rep', {}).get('title') == fr_name]
        if found:
            gid = found[0]['href'].split('/')[-1]
            fr_glos_map[fr_name] = gid
            print(f'  409  "{fr_name}" already exists ({gid[:8]}...)')
        else:
            print(f'  409  "{fr_name}" exists but NOT found via search — skipping')
    else:
        print(f'  ERR  "{fr_name}"  status={r.status_code}  {r.text[:80]}')

print(f'\nGlossary entries ready: {len(fr_glos_map)}/{len(GLOS_MAP_EN)}')

# ── Step 3: Walk FR model and embed links ──────────────────────────────────────
# Shapes to link: any shape whose name matches a key in fr_glos_map
LINKABLE_STENCILS = {
    'Task', 'Lane', 'Pool', 'DataObject', 'ITSystem', 'CollapsedPool',
    'StartNoneEvent', 'EndNoneEvent',
    'IntermediateTimerEvent', 'IntermediateMessageEventCatching', 'EndMessageEvent',
    'Exclusive_Databased_Gateway', 'Parallel_Gateway',
    'StartEvent', 'EndEvent',  # fallback stencil IDs
}


def embed_links(shapes, gmap):
    count = 0
    for s in shapes:
        sid  = s.get('stencil', {}).get('id', '')
        name = s.get('properties', {}).get('name', '').strip()
        if sid in LINKABLE_STENCILS and name and '\n' not in name:
            gid = gmap.get(name)
            if gid:
                s['glossaryLinks'] = {'name': [f'/glossary/{gid}']}
                count += 1
                print(f'  Linked: [{sid}] "{name}" -> {gid[:8]}...')
        count += embed_links(s.get('childShapes', []), gmap)
    return count


print('\nFetching French model...')
fr_model, fr_info = fetch_model(auth, FR_MODEL_ID)
fr_model = copy.deepcopy(fr_model)

print('Embedding links...')
n = embed_links(fr_model.get('childShapes', []), fr_glos_map)
print(f'Linked {n} shapes')

# ── Step 4: Submit ─────────────────────────────────────────────────────────────
print('\nSubmitting French model...')
rev, updated = submit_model(
    auth, FR_MODEL_ID, fr_model, fr_info,
    comment='Dictionary: embed French (fr_fr) glossaryLinks'
)
print(f'Done  rev={rev}  updated={updated}')
print(f'URL: https://editor.signavio.com/p/hub/model/{FR_MODEL_ID}')
