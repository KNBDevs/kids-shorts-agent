import hashlib
PROFILES = {
    "pimo":   {"ref_pitch": 1.22, "post_pitch": 1.06, "tempo": 1.04, "exag": 0.7,  "cfg": 0.4,  "temp": 0.8,  "eq": "bright"},
    "luma":   {"ref_pitch": 1.32, "post_pitch": 1.10, "tempo": 1.06, "exag": 0.9,  "cfg": 0.35, "temp": 0.85, "eq": "bright"},
    "ruki":   {"ref_pitch": 0.97, "post_pitch": 1.00, "tempo": 0.92, "exag": 0.35, "cfg": 0.55, "temp": 0.7,  "eq": "warm"},
    "tuki":   {"ref_pitch": 1.28, "post_pitch": 1.12, "tempo": 1.12, "exag": 0.95, "cfg": 0.3,  "temp": 0.9,  "eq": "bright"},
    "moki":   {"ref_pitch": 1.14, "post_pitch": 1.03, "tempo": 0.9,  "exag": 0.4,  "cfg": 0.5,  "temp": 0.7,  "eq": "soft"},
    "bopi":   {"ref_pitch": 1.08, "post_pitch": 1.04, "tempo": 1.02, "exag": 0.45, "cfg": 0.5,  "temp": 0.6,  "eq": "robot"},
    "bolita": {"ref_pitch": 1.38, "post_pitch": 1.12, "tempo": 1.12, "exag": 1.0,  "cfg": 0.3,  "temp": 0.9,  "eq": "bright"},
    "gruno":  {"ref_pitch": 0.84, "post_pitch": 0.96, "tempo": 0.98, "exag": 0.85, "cfg": 0.35, "temp": 0.85, "eq": "nasal"},
}
BASE_TEXT = "¡Hola! ¿Qué tal estás? Hoy hace un día precioso para jugar en el parque con mis amigos."


def lines():
    from hola_plan import CHARS
    from intro_plan import CAST, GROUP_LINE, GRUNO_LINE, SUBSCRIBE_LINE
    out = {}
    lim_h = (1.6, 3.6, 6.5, 4.3, 2.0, 3.6)
    for cid, d in CHARS.items():
        for k, t in enumerate(d["lines"]):
            out[f"hola_{cid}_{k}"] = {"char": cid, "text": t, "max": lim_h[k]}
    for c in CAST:
        out[f"intro_{c['id']}"] = {"char": c["id"], "text": c["line"], "max": 2.5}
    out["intro_gruno"] = {"char": "gruno", "text": GRUNO_LINE["text"], "max": 2.0}
    for cid in ("pimo", "luma", "tuki", "bolita"):
        out[f"intro_hook_{cid}"] = {"char": cid, "text": "¡Hola!", "max": 1.0}
        out[f"intro_group_{cid}"] = {"char": cid, "text": GROUP_LINE["text"], "max": 1.4}
    for cid in ("luma", "pimo"):
        out[f"intro_sub_{cid}"] = {"char": cid, "text": SUBSCRIBE_LINE["text"], "max": 1.3}
    from episode_lib import voice_lines
    out.update(voice_lines())
    return out


def digest(entry):
    p = PROFILES[entry["char"]]
    return hashlib.sha1(("v2" + entry["text"] + repr(sorted(p.items()))).encode()).hexdigest()[:12]
