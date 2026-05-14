"""Copy a model to Maria Playground."""
import sys, copy
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib import get_auth, fetch_model, create_model

MARIA_PLAYGROUND = "/directory/a731acfb31ad46dd81cf277aa9a66583"
SOURCE_ID        = "221198b386c448ad9f34893fdd0c405a"

auth = get_auth()
model, info = fetch_model(auth, SOURCE_ID)
print(f"Source: {info['name']}  ({SOURCE_ID})")

new_id = create_model(
    auth,
    name=info["name"] + " (copy)",
    parent=MARIA_PLAYGROUND,
    model_json=copy.deepcopy(model),
    namespace=info.get("namespace", "http://b3mn.org/stencilset/bpmn2.0#"),
    model_type=info.get("type", "Business Process Diagram (BPMN 2.0)"),
    comment="Duplicated to Maria Playground by BPMN Annotator",
)
print(f"Created: {info['name']} (copy)  ({new_id})")
print(f"Open   : https://editor.signavio.com/p/hub/model/{new_id}")
