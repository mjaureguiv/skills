"""
Update the French model to replace EN glossary links with FR equivalents.
Shapes that already had EN links (copied from source model) need to point
to the French translations created in the previous step.

Run: py skills/bpmn-annotator/temp/fr_dict_update.py
"""
import sys, copy, urllib.parse
sys.path.insert(0, r'C:\Backup\signavio_process_consultant_experimental\mcp\signavio\spm\src')
sys.path.insert(0, r'C:\Signavio_PM_Agent\skills\bpmn-annotator')
from lib.auth  import get_auth
from lib.fetch import fetch_model, submit_model

auth = get_auth()
FR_MODEL_ID = '0f7f0a3656f741658b16d6d1b2935e14'

# ── EN → FR glossary ID replacement map ───────────────────────────────────────
# EN ID → FR ID (full 32-char IDs; resolved via paginated glossary walk)
# For terms without a FR entry (CRM, ABC Company GmbH), keep the EN link.
fr_id_full = {
    # Business Analyst → Analyste Metier
    'aefc9f9b937944099e1c570d8cfe8cfb': '33ad993d05dc4eeb8881c26aeed9eea8',
    # Process Expert → Expert Processus
    'de3d0a9c885f4ac2aaa70bce474203ab': '63a9eb24bfba472b8913d40209834a48',
    # Document requirements in CRM → Documenter les exigences dans CRM
    'e398648bb85f4444957321a997145b9b': 'abc323073fdd4815980cd313cc3f76aa',
    # Identify business requirements → Identifier les exigences metier
    'c34a781a586c488da2d3ef534e00c4f5': '6b5def3735ff4a8185f8bd4565ddfa28',
    # Review documented requirements → Reviser les exigences documentees
    '7c500cb1062d4a90850cbb85c0585246': 'c0dae0082c7b4a2a9229535ab107a8ca',
    # Refine requirements with requester → Affiner les exigences avec le demandeur
    '077538d063aa4d1f96df87c8a9b03deb': '31836f085f0d4b4ab0d2c62490ca490c',
    # Business Requirements → Exigences Metier
    '0d5f0890f56c49f498941908113e4b02': '58be26fc943c4c8b861b3344b95a78b3',
    # IT Project Started → Projet IT demarre
    '953bbd836c0448d9bcf0546c15b44211': '6de740b6dbf748d097bfb3c499bd4c98',
    # Requirements Finalized → Exigences finalisees
    '2a37525bfa914a4a8d6f0916eaa229ec': '895cb5de5dfb40f0afb89dfda35584f2',
    # Are clarifications needed? → Des clarifications sont-elles necessaires ?
    '168a2225d8414dbca0f3756471f17362': '8d346b436d434f8cb318ef6859888aec',
    # IT Department → Service IT
    '554ef82cdca64b2aa2235f684b9a35ad': 'cd8870c697d54dd1821a73e719b0f963',
    # HR Department → Departement RH
    'ac244edefdae48e1906f84b29fa2ea04': 'df12d20e5445453c9f97fd71769d5f02',
    # Line Manager → Responsable Hierarchique
    '0606d91e66ff4afeb5c0f05596d64753': '6a14d57ce09a441db3370c7b5b3121e9',
    # CRM and ABC Company GmbH: no FR entries available, keep EN links as-is
}

print(f'  Using {len(fr_id_full)} pre-resolved mappings')


def update_links(shapes, en_to_fr_full):
    updated = 0
    for s in shapes:
        links = s.get('glossaryLinks', {})
        name_links = links.get('name', [])
        if name_links:
            new_links = []
            changed = False
            for link in name_links:
                # link format: "/glossary/{id}"
                en_id = link.strip('/').split('/')[-1]
                if en_id in en_to_fr_full:
                    fr_id = en_to_fr_full[en_id]
                    new_links.append(f'/glossary/{fr_id}')
                    changed = True
                else:
                    new_links.append(link)  # keep as-is (no FR equivalent)
            if changed:
                s['glossaryLinks'] = {'name': new_links}
                sid = s.get('stencil', {}).get('id', '')
                name = s.get('properties', {}).get('name', '').strip()
                print(f'  Updated [{sid}] "{name[:40]}"')
                updated += 1
        updated += update_links(s.get('childShapes', []), en_to_fr_full)
    return updated


print('\nFetching French model...')
fr_model, fr_info = fetch_model(auth, FR_MODEL_ID)
fr_model = copy.deepcopy(fr_model)

print('Updating EN links to FR links...')
n = update_links(fr_model.get('childShapes', []), fr_id_full)
print(f'Updated {n} shapes')

print('\nSubmitting...')
rev, updated = submit_model(
    auth, FR_MODEL_ID, fr_model, fr_info,
    comment='Dictionary: replace EN glossaryLinks with FR equivalents'
)
print(f'Done  rev={rev}  updated={updated}')
print(f'URL: https://editor.signavio.com/p/hub/model/{FR_MODEL_ID}')
