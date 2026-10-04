import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from episode_lib import current_id, plan, FPS
eid = current_id()
P = plan(eid)
spec = {"template": "episode", "episode_id": eid, "script": "episode_scene.py", "audio": "episode_audio.py",
        "frames": P.TOTAL, "dur": P.TOTAL // FPS}
meta = {"title": P.META["title"][:100], "description": P.META["description"], "tags": P.META["tags"],
        "categoryId": "27", "madeForKids": True, "language": "es"}
json.dump(spec, open(os.path.join(HERE, "spec.json"), "w"), ensure_ascii=False, indent=1)
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), ensure_ascii=False, indent=1)
print(meta["title"])
