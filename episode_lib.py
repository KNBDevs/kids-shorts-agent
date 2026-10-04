import importlib, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 24


def current_id():
    eid = os.environ.get("EPISODE")
    p = os.environ.get("SPEC_FILE")
    if not eid and p and os.path.exists(p):
        eid = json.load(open(p)).get("episode_id")
    return eid


def plan(eid):
    return importlib.import_module(f"episodes.{eid}_plan")


def all_ids():
    d = os.path.join(HERE, "episodes")
    return sorted(f[:-8] for f in os.listdir(d) if f.endswith("_plan.py"))


def voice_lines():
    out = {}
    for eid in all_ids():
        P = plan(eid)
        for key, char, text, frame, mx in P.LINES:
            out[f"ep_{eid}_{key}"] = {"char": char, "text": text, "max": mx}
    return out
