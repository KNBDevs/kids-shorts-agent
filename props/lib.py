import math, random
import bpy
from mathutils import Vector
import common as C
from props.select import colors
from props.registry import REGISTRY
_M = {}


def M(rgb, rough=0.45, coat=0.4, emit=0.0):
    k = (tuple(round(c, 2) for c in rgb), rough, coat, emit)
    if k not in _M:
        _M[k] = C.mat(f"pm{len(_M)}", rgb, rough=rough, coat=coat, emit=emit)
    return _M[k]


def flower_pot(r, s, fam, root):
    pc, fc1, fc2, lc = colors(r, fam, 4)
    h = [0.32, 0.26, 0.4][s]
    prof = [(0.0, 0.0), (0.16, 0.0), (0.19 if s != 1 else 0.24, h * 0.85), (0.21 if s != 1 else 0.26, h), (0.0, h)]
    C.lathe("pot", prof, M(pc), root, segs=40)
    for i in range(r.randint(2, 4)):
        a = r.uniform(0, 6.28); d = r.uniform(0, 0.08); top = h + r.uniform(0.18, 0.38)
        C.tube("stem", [(math.cos(a) * d, math.sin(a) * d, h), (math.cos(a) * d * 1.6, math.sin(a) * d * 1.6, top)], 0.012, M((0.3, 0.65, 0.35)), root)
        cen = Vector((math.cos(a) * d * 1.6, math.sin(a) * d * 1.6, top))
        for k in range(5 if s != 2 else 7):
            b = k * 6.28 / (5 if s != 2 else 7)
            C.sphere("pet", tuple(cen + Vector((math.cos(b) * 0.05, math.sin(b) * 0.02, math.sin(b) * 0.05))), (0.035, 0.015, 0.035), M(fc1 if i % 2 else fc2, coat=0.2), root, 12)
        C.sphere("ctr", tuple(cen + Vector((0, -0.01, 0))), (0.025,) * 3, M((1, 0.85, 0.3)), root, 12)


def bush(r, s, fam, root):
    g, b2, berry = colors(r, "fresh" if fam != "autumn" else fam, 3)
    g = (g[0] * 0.5, min(1, g[1] * 1.0 + 0.2), g[2] * 0.5)
    n = [5, 7, 4][s]
    for i in range(n):
        a = i * 6.28 / n + r.uniform(-0.3, 0.3)
        rad = r.uniform(0.18, 0.28) * (1.2 if s == 2 else 1)
        C.sphere("b", (math.cos(a) * 0.2, math.sin(a) * 0.12, rad * 0.9 + r.uniform(0, 0.12)), (rad, rad, rad * 0.9), M(g, rough=0.7, coat=0.1), root, 20)
    if s != 1:
        for i in range(r.randint(3, 6)):
            a = r.uniform(0, 6.28)
            C.sphere("berry", (math.cos(a) * 0.32, -0.2 - abs(math.sin(a)) * 0.05, r.uniform(0.15, 0.45)), (0.035,) * 3, M(berry, coat=0.8), root, 10)


def toy_blocks(r, s, fam, root):
    cs = colors(r, fam, 6)
    z = 0
    for i in range([3, 4, 2][s]):
        sz = r.uniform(0.16, 0.22)
        C.rounded_box("blk", (r.uniform(-0.04, 0.04), 0, z + sz / 2), (sz, sz, sz), sz * 0.15, M(cs[i], coat=0.6), root)
        z += sz
    if s == 2:
        C.rounded_box("blk", (0.28, 0.05, 0.09), (0.18, 0.18, 0.18), 0.03, M(cs[4], coat=0.6), root)


def mushroom_stool(r, s, fam, root):
    cap, stem, dot = colors(r, fam, 3)
    h = [0.28, 0.36, 0.22][s]
    C.lathe("st", [(0, 0), (0.09, 0), (0.08, h), (0, h)], M((0.97, 0.94, 0.88)), root, segs=24)
    C.sphere("cap", (0, 0, h), (0.26, 0.26, 0.14 if s != 1 else 0.18), M(cap, coat=0.6), root, 32)
    for i in range([5, 7, 0][s]):
        a = r.uniform(0, 6.28); e = r.uniform(0.3, 1.0)
        C.sphere("dot", (math.cos(a) * 0.2 * e, math.sin(a) * 0.2 * e, h + 0.13 * math.sqrt(max(0.05, 1 - e * e)) + 0.005), (0.035, 0.035, 0.012), M((1, 1, 1), coat=0.3), root, 10)


def fence(r, s, fam, root):
    c = colors(r, fam, 2)[0]
    n = [5, 7, 4][s]
    for i in range(n):
        x = (i - (n - 1) / 2) * 0.18
        C.rounded_box("pk", (x, 0, 0.22), (0.1, 0.04, 0.44 + (0.06 if s == 2 and i % 2 else 0)), 0.03, M(c, rough=0.6), root)
        C.sphere("tip", (x, 0, 0.46), (0.05, 0.02, 0.04), M(c, rough=0.6), root, 12)
    C.rounded_box("rail", (0, 0.03, 0.3), (n * 0.18, 0.03, 0.05), 0.012, M(c, rough=0.6), root)


def lamp_post(r, s, fam, root):
    c, glow = colors(r, fam, 2)
    h = [1.1, 0.9, 1.3][s]
    C.tube("post", [(0, 0, 0), (0, 0, h * 0.6), (0.04 * (s == 1), 0, h)], 0.035, M(c, rough=0.4), root)
    C.sphere("base", (0, 0, 0.04), (0.12, 0.12, 0.05), M(c), root, 20)
    gl = (1.0, 0.86, 0.55)
    C.sphere("bulb", (0.04 * (s == 1), 0, h + 0.09), (0.11, 0.11, 0.12 if s != 2 else 0.09), M(gl, rough=0.2, coat=0, emit=1.2), root, 24)


def bench(r, s, fam, root):
    c, leg = colors(r, fam, 2)
    w = [0.8, 0.65, 0.95][s]
    for k in range(3 if s != 1 else 2):
        C.rounded_box("sl", (0, -0.06 + k * 0.08, 0.3), (w, 0.07, 0.04), 0.015, M(c, rough=0.6), root)
    for x in (-w / 2 + 0.08, w / 2 - 0.08):
        C.rounded_box("lg", (x, 0, 0.15), (0.06, 0.2, 0.3), 0.02, M(leg), root)
    if s != 2:
        C.rounded_box("bk", (0, 0.12, 0.48), (w, 0.04, 0.16), 0.02, M(c, rough=0.6), root)


def pebbles(r, s, fam, root):
    cs = colors(r, "autumn" if s == 1 else fam, 4)
    for i in range([5, 7, 3][s]):
        sz = r.uniform(0.06, 0.13)
        C.sphere("pb", (r.uniform(-0.35, 0.35), r.uniform(-0.2, 0.2), sz * 0.4), (sz, sz * 0.8, sz * 0.45), M(tuple(0.55 + 0.4 * v for v in cs[i % 4]), rough=0.75, coat=0.1), root, 16)


def bunting(r, s, fam, root):
    cs = colors(r, fam, 5)
    span = [2.0, 1.6, 2.4][s]
    pts = [(-span / 2 + span * t, 0, 1.6 - 0.25 * math.sin(math.pi * t)) for t in [i / 10 for i in range(11)]]
    C.tube("rope", pts, 0.008, M((0.95, 0.92, 0.85)), root)
    C.tube("p1", [(-span / 2, 0, 0), (-span / 2, 0, 1.62)], 0.025, M((0.95, 0.92, 0.85)), root)
    C.tube("p2", [(span / 2, 0, 0), (span / 2, 0, 1.62)], 0.025, M((0.95, 0.92, 0.85)), root)
    n = [8, 6, 10][s]
    for i in range(n):
        t = (i + 0.5) / n
        x = -span / 2 + span * t; z = 1.6 - 0.25 * math.sin(math.pi * t)
        bpy.ops.mesh.primitive_cone_add(vertices=3 if s != 1 else 4, radius1=0.08, depth=0.015, location=(x, 0, z - 0.09), rotation=(math.radians(90), 0, math.radians(90) if s == 1 else 0))
        o = bpy.context.object; o.data.materials.append(M(cs[i % 5], rough=0.6, coat=0)); o.scale = (1, 1.4, 1) if s != 1 else (1, 1, 1); o.parent = root


def gear_tower(r, s, fam, root):
    cs = colors(r, "candy", 4)
    z = 0
    for i in range([3, 2, 4][s]):
        rad = r.uniform(0.14, 0.24)
        bpy.ops.mesh.primitive_cylinder_add(vertices=10 + 2 * i, radius=rad, depth=0.08, location=(r.uniform(-0.05, 0.05), 0, z + 0.04))
        o = bpy.context.object; o.data.materials.append(M(cs[i % 4], coat=0.7)); o.parent = root
        bv = o.modifiers.new("b", "BEVEL"); bv.width = 0.015; bv.segments = 2
        K = C.key
        K(o, "rotation_euler", 0, (0, 0, 0)); K(o, "rotation_euler", 240, (0, 0, math.radians((1 if i % 2 else -1) * 360)))
        for fc in (o.animation_data.action.fcurves if hasattr(o.animation_data.action, "fcurves") else []):
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"
        z += 0.1
    C.sphere("knob", (0, 0, z + 0.05), (0.06,) * 3, M((1, 0.55, 0.2), coat=0.8), root, 16)


def leaf_pile(r, s, fam, root):
    cs = colors(r, "autumn", 5)
    for i in range([9, 14, 6][s]):
        a = r.uniform(0, 6.28); d = r.uniform(0, 0.3)
        C.sphere("lf", (math.cos(a) * d, math.sin(a) * d * 0.6, r.uniform(0.01, 0.12) * (1 - d)), (0.07, 0.045, 0.012), M(cs[i % 5], rough=0.65, coat=0.1), root, 10, rot=(r.uniform(-0.4, 0.4), r.uniform(-0.4, 0.4), a))


def ball_basket(r, s, fam, root):
    cs = colors(r, fam, 5)
    bc = (0.85, 0.7, 0.5) if s != 1 else cs[4]
    C.lathe("bk", [(0, 0), (0.22, 0), (0.27, 0.22), (0.25, 0.24), (0, 0.24)], M(bc, rough=0.7, coat=0.1), root, segs=32)
    for i in range([3, 4, 2][s]):
        a = i * 2.1
        C.sphere("ball", (math.cos(a) * 0.1, math.sin(a) * 0.08, 0.27 + 0.03 * (i % 2)), (0.1,) * 3, M(cs[i], coat=0.7), root, 20)


GEN = {k: v for k, v in globals().items() if k in REGISTRY}


def spawn(name, style=0, seed=0, family="pastel", loc=(0, 0, 0), scale=1.0, rot=0.0, parent=None):
    root = C.empty(f"prop_{name}", parent, loc, (0, 0, math.radians(rot)))
    GEN[name](random.Random(seed), style, family, root)
    root.scale = (scale, scale, scale)
    return root


def dress(choice, parent=None, offset=(0, 0, 0)):
    out = []
    for d in choice["decor"]:
        loc = tuple(a + b for a, b in zip(d["loc"], offset))
        out.append(spawn(d["prop"], d["style"], d["seed"], choice.get("family", "pastel"), loc, d["scale"], d["rot"], parent))
    return out


def auto_dress(eid, env, parent=None, count=6, offset=(0, 0, 0)):
    from props.select import choose
    return dress(choose(eid, env, REGISTRY, count=count), parent, offset)
