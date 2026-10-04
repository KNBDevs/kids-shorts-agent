import os, json, math
import bpy
from mathutils import Vector
from stage import C, K, FPS, RIGS
HERE = os.path.dirname(os.path.abspath(__file__))
try:
    MAN = json.load(open(os.path.join(HERE, 'assets', 'vo', 'manifest.json')))
except Exception:
    MAN = {}
REST = {}


def dur(key, text=''):
    d = MAN.get(key, {}).get('dur')
    return d if d else max(0.8, len(text) / 14)


def say(ch, f, key, text=''):
    n = round(dur(key, text) * FPS / 4)
    C.talk(ch, f, syllables=max(2, n), step=4)


def lines(eid, LINES):
    for key, cid, text, f, mx in LINES:
        if cid in RIGS:
            say(RIGS[cid], f, f'ep_{eid}_{key}', text)


def place(ch, f, xyz):
    K(ch['hold'], 'location', f, tuple(xyz))


def turn(ch, f, deg):
    K(ch['spin'], 'rotation_euler', f, (0, 0, math.radians(deg)))


def _arm(ch, side):
    return next((o for o in ch['rig'].children if o.name.endswith(f'.arm.{side}')), None)


def arm(ch, side, f, fwd=0.0, out=None):
    a = _arm(ch, side)
    if a is None:
        return
    if a.name not in REST:
        REST[a.name] = tuple(a.rotation_euler)
    r = REST[a.name]
    sx = -1 if side == 'L' else 1
    ry = r[1] if out is None else math.radians(-sx * out)
    K(a, 'rotation_euler', f, (r[0] + math.radians(fwd), ry, r[2]))


def rest_arm(ch, side, f):
    a = _arm(ch, side)
    if a is None:
        return
    REST.setdefault(a.name, tuple(a.rotation_euler))
    K(a, 'rotation_euler', f, REST[a.name])


def hide_stage():
    for o in bpy.data.objects:
        if o.type == 'MESH' and o.data.materials and o.data.materials[0] and o.data.materials[0].name.startswith('stage'):
            o.hide_render = True
            o.hide_viewport = True


def blinks(ch, frames):
    for f in frames:
        C.blink(ch, f)


def pop_in(o, f, s=1.0, d=8):
    sc = (s,) * 3 if not hasattr(s, '__len__') else tuple(s)
    K(o, 'scale', 0, (0, 0, 0))
    K(o, 'scale', f - 1, (0, 0, 0))
    K(o, 'scale', f + d * 0.6, tuple(v * 1.2 for v in sc))
    K(o, 'scale', f + d, sc)


def pop_out(o, f, s=1.0, d=6):
    sc = (s,) * 3 if not hasattr(s, '__len__') else tuple(s)
    K(o, 'scale', f, sc)
    K(o, 'scale', f + d * 0.4, tuple(v * 1.15 for v in sc))
    K(o, 'scale', f + d, (0, 0, 0))
