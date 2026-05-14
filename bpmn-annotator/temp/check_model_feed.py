"""
check_model_feed.py — check the revision history / activity feed for the model.
"""
import sys, io, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib import get_auth

MODEL_ID = '407543a9285e43c5925f97104abef719'

auth = get_auth()

# Fetch model info
r = auth.session.get(auth.api_base + f'/model/{MODEL_ID}/info', timeout=15)
info_data = r.json()
print('=== Model info keys ===')
print(json.dumps(info_data, indent=2, ensure_ascii=False)[:3000])

# Try fetching revision history
print('\n=== Revision list ===')
r2 = auth.session.get(auth.api_base + f'/model/{MODEL_ID}/revisions', timeout=15)
print(f'Status: {r2.status_code}')
if r2.status_code == 200:
    revs = r2.json()
    print(json.dumps(revs[:5] if isinstance(revs, list) else revs, indent=2, ensure_ascii=False)[:3000])
else:
    print(r2.text[:500])

# Also check directory to see if folder is published
print('\n=== Folder published status ===')
r3 = auth.session.get(auth.api_base + '/directory/a731acfb31ad46dd81cf277aa9a66583', timeout=15)
print(f'Status: {r3.status_code}')
if r3.status_code == 200:
    folder_data = r3.json()
    # Look for publish-related fields
    for item in folder_data if isinstance(folder_data, list) else []:
        if item.get('rel') in ('info', 'pub', 'publish', 'dir'):
            print(json.dumps(item, indent=2, ensure_ascii=False))
else:
    print(r3.text[:300])
