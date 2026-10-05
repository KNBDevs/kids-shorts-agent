import math, random
import bpy, bmesh
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


def _cols(r, fam, n):
    if isinstance(fam, tuple) and len(fam) == 3 and all(isinstance(v, (int, float)) for v in fam):
        base = fam
        return [base] + [tuple(min(1, v * 0.55 + 0.45) for v in base)] * (n - 1)
    return colors(r, fam, n)


def soft_token(r, s, fam, root):
    c, lite = _cols(r, fam, 2)
    if s == 0:
        C.sphere("tk", (0, 0, 0.065), (0.17, 0.17, 0.065), M(c, rough=0.6, coat=0.15), root, 40)
        pts = [(math.cos(a) * 0.162, math.sin(a) * 0.162, 0.065) for a in [k * 6.2832 / 48 for k in range(49)]]
        C.tube("pipe", pts, 0.012, M(lite, rough=0.5), root)
        C.sphere("btn", (0, 0, 0.128), (0.032, 0.032, 0.014), M(lite, rough=0.4, coat=0.5), root, 16)
    elif s == 1:
        C.rounded_box("tk", (0, 0, 0.07), (0.3, 0.3, 0.14), 0.05, M(c, rough=0.6, coat=0.15), root)
        for k in range(4):
            a = 0.785 + k * 1.5708
            C.sphere("tuft", (math.cos(a) * 0.17, math.sin(a) * 0.17, 0.07), (0.03, 0.03, 0.03), M(lite, rough=0.5), root, 12)
        C.sphere("btn", (0, 0, 0.142), (0.04, 0.04, 0.012), M(lite, rough=0.4, coat=0.5), root, 16)
    else:
        n = 6
        for k in range(n):
            a = k * 6.2832 / n
            C.sphere("lobe", (math.cos(a) * 0.1, math.sin(a) * 0.1, 0.055), (0.085, 0.085, 0.055), M(c, rough=0.6, coat=0.15), root, 24)
        C.sphere("ctr", (0, 0, 0.07), (0.1, 0.1, 0.06), M(lite, rough=0.5, coat=0.3), root, 24)


def play_mat(r, s, fam, root):
    a, b, c = _cols(r, fam, 3)
    if s == 0:
        C.lathe("mat", [(0, 0), (0, 0.5), (0.025, 0.53), (0.05, 0.5), (0.05, 0)], M(a, rough=0.7), root, segs=64)
        C.tube("ring", [(math.cos(k * 6.2832 / 64) * 0.34, math.sin(k * 6.2832 / 64) * 0.34, 0.05) for k in range(65)], 0.022, M(b, rough=0.6), root)
        C.sphere("dot", (0, 0, 0.05), (0.12, 0.12, 0.008), M(c, rough=0.6), root, 32)
    elif s == 1:
        for i, (x, y) in enumerate(((-0.24, -0.24), (0.24, -0.24), (-0.24, 0.24), (0.24, 0.24))):
            C.rounded_box("tile", (x, y, 0.025), (0.46, 0.46, 0.05), 0.015, M((a, b, c, b)[i], rough=0.75), root)
            C.sphere("nub", (x, y, 0.05), (0.06, 0.06, 0.01), M((b, c, a, c)[i], rough=0.7), root, 16)
    else:
        bm_pts = [(math.cos(k * 6.2832 / 6 + 0.5236) * 0.52, math.sin(k * 6.2832 / 6 + 0.5236) * 0.52) for k in range(6)]
        bm = bmesh.new()
        vs = [bm.verts.new((x, y, 0)) for x, y in bm_pts]
        f = bm.faces.new(vs)
        ext = bmesh.ops.extrude_face_region(bm, geom=[f])
        for v in [e for e in ext["geom"] if isinstance(e, bmesh.types.BMVert)]:
            v.co.z += 0.06
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        o = C.mesh_obj("hex", bm, M(a, rough=0.7), root, smooth=False)
        bv = o.modifiers.new("b", "BEVEL"); bv.width = 0.025; bv.segments = 4
        for k in range(6):
            t = k * 6.2832 / 6
            C.sphere("star", (math.cos(t) * 0.3, math.sin(t) * 0.3, 0.06), (0.05, 0.05, 0.008), M(b if k % 2 else c, rough=0.6), root, 16)


def floor_lamp(r, s, fam, root):
    body, shade, trim = _cols(r, fam, 3)
    cream = (0.98, 0.95, 0.88)
    glow = M((1.0, 0.92, 0.7), rough=0.3, coat=0, emit=3.0)
    h = [1.05, 0.95, 1.15][s]
    if s == 2:
        for k in range(3):
            a = k * 2.0944 + 1.5708
            C.tube("leg", [(math.cos(a) * 0.26, math.sin(a) * 0.26, 0.03), (0, 0, h * 0.45)], 0.022, M(body, rough=0.4), root)
            C.sphere("foot", (math.cos(a) * 0.26, math.sin(a) * 0.26, 0.03), (0.04, 0.04, 0.03), M(trim), root, 12)
        C.tube("pole", [(0, 0, h * 0.45), (0, 0, h - 0.05)], 0.028, M(body, rough=0.4), root)
    else:
        C.lathe("base", [(0, 0), (0, 0.2), (0.03, 0.22), (0.07, 0.17), (0.09, 0.05), (0.09, 0)], M(body, rough=0.4, coat=0.5), root, segs=48)
        for k in range(4):
            a = k * 1.5708 + 0.785
            C.sphere("wheel", (math.cos(a) * 0.17, math.sin(a) * 0.17, 0.03), (0.035, 0.03, 0.035), M((0.3, 0.3, 0.35), rough=0.6), root, 16)
        if s == 0:
            C.tube("pole", [(0, 0, 0.08), (0, 0, h - 0.05)], 0.03, M(cream, rough=0.4), root)
        else:
            C.tube("pole", [(0, 0, 0.08), (0, 0, h * 0.7), (0, 0.06, h * 0.92), (0, 0.12, h - 0.02)], 0.03, M(cream, rough=0.4), root)
    hy = 0.12 if s == 1 else 0.0
    head = C.empty("head", root, (0, hy, h), (math.radians(-90), 0, 0))
    if s == 0:
        C.lathe("shade", [(-0.02, 0.0), (0.0, 0.08), (0.08, 0.17), (0.2, 0.22), (0.22, 0.2), (0.12, 0.13), (0.03, 0.06), (0.0, 0.0)], M(shade, rough=0.35, coat=0.6), head, segs=48)
        C.sphere("rim", (0, 0, 0.21), (0.21, 0.21, 0.018), M(trim, rough=0.4), head, 32)
    elif s == 1:
        C.lathe("shade", [(-0.02, 0.0), (0.0, 0.06), (0.22, 0.2), (0.24, 0.19), (0.04, 0.05), (0.0, 0.0)], M(shade, rough=0.35, coat=0.6), head, segs=48)
        C.tube("band", [(math.cos(k * 6.2832 / 48) * 0.205, math.sin(k * 6.2832 / 48) * 0.205, 0.2) for k in range(49)], 0.014, M(trim), head)
    else:
        C.lathe("shade", [(-0.02, 0.0), (0.0, 0.15), (0.24, 0.17), (0.25, 0.15), (0.04, 0.13), (0.0, 0.0)], M(shade, rough=0.35, coat=0.6), head, segs=48)
        for z in (0.06, 0.14):
            C.tube("stripe", [(math.cos(k * 6.2832 / 48) * 0.162, math.sin(k * 6.2832 / 48) * 0.162, z) for k in range(49)], 0.012, M(trim), head)
    C.sphere("bulb", (0, 0, 0.12), (0.075, 0.075, 0.075), glow, head, 24)
    C.sphere("knob", (0, 0, -0.04), (0.04, 0.04, 0.04), M(trim, coat=0.6), head, 16)


_A = {}


def MA(rgb, alpha, rough=0.08, emit=0.0):
    k = (tuple(round(c, 2) for c in rgb), alpha, rough, emit)
    if k not in _A:
        m = C.mat(f"pa{len(_A)}", rgb, rough=rough, coat=1.0, emit=emit)
        m.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = alpha
        _A[k] = m
    return _A[k]


def _ring(R, z, n=48, sy=1.0):
    return [(math.cos(k * 6.2832 / n) * R, math.sin(k * 6.2832 / n) * R * sy, z) for k in range(n + 1)]


def _dot(name, p, n, size, m, root):
    q = Vector((0, 0, 1)).rotation_difference(Vector(n).normalized())
    return C.sphere(name, tuple(p), (size, size, size * 0.3), m, root, 12, rot=tuple(q.to_euler()))


def desk_bell(r, s, fam, root):
    base, trim = _cols(r, fam, 2)
    gold = M((1.0, 0.76, 0.28), rough=0.22, coat=0.9)
    if s == 1:
        C.lathe("base", [(0, 0), (0, 0.17), (0.02, 0.18), (0.045, 0.16), (0.05, 0)], M(base, rough=0.4, coat=0.6), root, segs=48)
        piv = C.empty("bell_pivot", root, (0, 0, 0.05))
        C.lathe("dome", [(0, 0.15), (0.03, 0.15), (0.08, 0.13), (0.13, 0.08), (0.155, 0.03), (0.16, 0)], gold, piv, segs=48)
        C.tube("plunger", [(0, 0, 0.15), (0, 0, 0.2)], 0.012, gold, piv)
        C.sphere("knob", (0, 0, 0.215), (0.03, 0.03, 0.022), M(trim, coat=0.8), piv, 20)
        return
    w = 0.42 if s == 0 else 0.36
    C.rounded_box("base", (0, 0, 0.03), (w, 0.2, 0.06), 0.025, M(base, rough=0.5, coat=0.5), root)
    top = 0.5
    if s == 0:
        for x in (-w / 2 + 0.05, w / 2 - 0.05):
            C.tube("post", [(x, 0, 0.05), (x, 0, top)], 0.018, M(trim, rough=0.4), root)
            C.sphere("cap", (x, 0, top + 0.01), (0.03, 0.03, 0.03), M(trim, coat=0.7), root, 16)
        C.tube("bar", [(-w / 2 + 0.05, 0, top), (w / 2 - 0.05, 0, top)], 0.014, M(trim, rough=0.4), root)
        outer = [(-0.205, 0.14), (-0.19, 0.132), (-0.16, 0.1), (-0.11, 0.085), (-0.06, 0.08), (-0.025, 0.066), (-0.008, 0.04), (0.0, 0.0)]
    else:
        arc = [(math.cos(math.pi * k / 24) * (w / 2 - 0.04), 0, 0.06 + math.sin(math.pi * k / 24) * 0.46) for k in range(25)]
        C.tube("arch", arc, 0.02, M(trim, rough=0.4), root)
        top = 0.52
        for sx in (-1, 1):
            C.sphere("bow", (sx * 0.045, 0, top + 0.02), (0.045, 0.02, 0.03), M(trim, coat=0.6), root, 16, rot=(0, math.radians(sx * 20), 0))
        outer = [(-0.19, 0.15), (-0.175, 0.14), (-0.13, 0.09), (-0.09, 0.07), (-0.05, 0.075), (-0.02, 0.06), (-0.006, 0.035), (0.0, 0.0)]
    inner = [(-0.03, 0.0), (-0.05, 0.05)] + [(z - 0.004, rr - 0.014) for z, rr in outer[2:4]][::-1] + [(outer[1][0] + 0.002, outer[1][1] - 0.014)]
    piv = C.empty("bell_pivot", root, (0, 0, top))
    C.lathe("bell", inner + outer, gold, piv, segs=48)
    C.tube("hang", [(0, 0, 0.012), (0, 0, -0.01)], 0.012, M(trim), piv)
    C.sphere("clapper", (0, 0, outer[0][0] + 0.03), (0.03, 0.03, 0.03), M(trim, coat=0.7), piv, 16)


def toy_drum(r, s, fam, root):
    body, rim, dot = _cols(r, fam, 3)
    skin_m = M((0.98, 0.95, 0.88), rough=0.55, coat=0.2)
    R, h = [(0.2, 0.36), (0.3, 0.17), (0.17, 0.5)][s]
    z0 = 0.06 if s == 1 else 0.0
    if s == 2:
        prof = [(z0, 0.0), (z0, R * 0.8), (z0 + h * 0.15, R * 0.92), (z0 + h * 0.6, R * 1.08), (z0 + h, R)]
    else:
        prof = [(z0, 0.0), (z0, R), (z0 + h, R)]
    C.lathe("shell", prof + [(z0 + h, 0.0)], M(body, rough=0.4, coat=0.6), root, segs=48)
    top = z0 + h
    piv = C.empty("skin", root, (0, 0, top))
    C.sphere("skinface", (0, 0, 0.004), (R * 0.97, R * 0.97, 0.012), skin_m, piv, 40)
    C.tube("rimtop", _ring(R * 1.01, top), 0.022, M(rim, coat=0.7), root)
    if s == 0:
        C.tube("rimbot", _ring(R * 1.01, z0 + 0.02), 0.022, M(rim, coat=0.7), root)
        zig = []
        for k in range(17):
            a = k * 6.2832 / 16
            z = z0 + 0.04 if k % 2 == 0 else top - 0.03
            zig.append((math.cos(a) * R * 1.03, math.sin(a) * R * 1.03, z))
        C.tube("cord", zig, 0.011, M(tuple(v * 0.45 for v in body), rough=0.6), root)
        for k in range(8):
            a = k * 6.2832 / 8
            for z in (z0 + 0.02, top):
                C.sphere("lug", (math.cos(a) * R * 1.06, math.sin(a) * R * 1.06, z), (0.022, 0.022, 0.03), M(rim, coat=0.8), root, 12)
        for sx in (-1, 1):
            st = C.empty("stick", root, (0, 0, top + 0.03), (0, math.radians(84), math.radians(sx * 25)))
            C.tube("stk", [(0, 0, -R * 1.1), (0, 0, R * 1.1)], 0.012, M((0.98, 0.85, 0.6), rough=0.5), st)
            C.sphere("stktip", (0, 0, R * 1.1), (0.03, 0.03, 0.03), M(dot, coat=0.7), st, 16)
    elif s == 1:
        for k in range(3):
            a = k * 2.0944 + 0.5
            C.sphere("foot", (math.cos(a) * R * 0.7, math.sin(a) * R * 0.7, 0.04), (0.05, 0.05, 0.045), M(rim, coat=0.6), root, 16)
        for k in range(10):
            a = k * 6.2832 / 10
            _dot("spot", (math.cos(a) * R * 1.005, math.sin(a) * R * 1.005, z0 + h * 0.5), (math.cos(a), math.sin(a), 0), 0.035, M(dot, coat=0.6), root)
    else:
        for z in (z0 + h * 0.3, z0 + h * 0.75):
            rr = R * (1.0 + 0.08 * math.sin(math.pi * (z - z0) / h))
            C.tube("band", _ring(rr * 1.02, z), 0.014, M(dot, coat=0.6), root)


def colander(r, s, fam, root):
    body, trim = _cols(r, fam, 2)
    bm = M(body, rough=0.35, coat=0.7)
    hole = M(tuple(v * 0.35 for v in body), rough=0.7, coat=0.0)
    R = [0.2, 0.18, 0.21][s]
    depth = [1.0, 1.15, 0.85][s]
    N = 14
    def rad(t):
        return R * math.sin(t) if s != 2 else R * (0.25 + 0.75 * t / 1.5708)
    def hz(t):
        return depth * (R - R * math.cos(t)) if s != 2 else depth * R * (t / 1.5708) * 1.1
    ts = [k * 1.5708 / N for k in range(N + 1)]
    outer = [(hz(t), rad(t)) for t in ts]
    H = outer[-1][0]
    th = 0.014
    inner = [(z + th, max(0.0, rr - th)) for z, rr in outer][::-1]
    C.lathe("bowl", [(0, 0)] + outer[1:] + [(H + 0.008, outer[-1][1] + 0.012), (H + 0.012, outer[-1][1] - 0.004)] + inner[:-1] + [(th, 0.0)], bm, root, segs=56)
    C.tube("lip", _ring(outer[-1][1] + 0.006, H + 0.006, 56), 0.012, M(trim, coat=0.7), root)
    for row, t in enumerate([0.55, 0.85, 1.1, 1.32]):
        n = int(8 + row * 5)
        for k in range(n):
            a = k * 6.2832 / n + row * 0.3
            z = hz(t); rr = rad(t)
            if s == 2:
                nz = -0.75 * R / (depth * R * 1.1)
                nv = Vector((math.cos(a), math.sin(a), nz)).normalized()
            else:
                nv = Vector((math.sin(t) * math.cos(a), math.sin(t) * math.sin(a), -math.cos(t) / depth)).normalized()
            p = Vector((math.cos(a) * rr, math.sin(a) * rr, z)) + nv * 0.002
            _dot("hole", p, nv, 0.011, hole, root)
            pi = Vector((math.cos(a) * (rr - th), math.sin(a) * (rr - th), z + th)) - nv * 0.002
            _dot("holei", pi, -nv, 0.011, hole, root)
    for k in range(5):
        a = k * 6.2832 / 5
        _dot("holeb", (math.cos(a) * 0.04, math.sin(a) * 0.04, -0.001), (0, 0, -1), 0.011, hole, root)
    rim_r = outer[-1][1]
    if s == 1:
        for sx in (-1, 1):
            C.tube("ear", [(sx * rim_r * 0.98, 0, H - 0.01), (sx * (rim_r + 0.05), 0, H + 0.005), (sx * (rim_r + 0.07), 0, H - 0.03), (sx * (rim_r + 0.04), 0, H - 0.055), (sx * rim_r * 0.99, 0, H - 0.05)], 0.012, M(trim, coat=0.7), root)
        for k in range(3):
            a = k * 2.0944
            C.sphere("foot", (math.cos(a) * 0.07, math.sin(a) * 0.07, -0.012), (0.025, 0.025, 0.018), M(trim, coat=0.6), root, 16)
    else:
        L = 0.22 if s == 0 else 0.26
        C.tube("handle", [(rim_r * 0.98, 0, H - 0.01), (rim_r + L * 0.5, 0, H + 0.015), (rim_r + L, 0, H + 0.02)], 0.016, M(trim, coat=0.7), root)
        if s == 0:
            C.sphere("grip", (rim_r + L, 0, H + 0.02), (0.035, 0.024, 0.024), M(trim, coat=0.7), root, 16)
            C.tube("foot", _ring(0.06, hz(0.42) - 0.012, 36), 0.01, M(trim, coat=0.6), root)
        else:
            C.tube("hook", [(rim_r + L, 0, H + 0.02), (rim_r + L + 0.035, 0, H + 0.035), (rim_r + L + 0.045, 0, H + 0.065), (rim_r + L + 0.025, 0, H + 0.08)], 0.01, M(trim, coat=0.7), root)


def clear_cup(r, s, fam, root):
    trim, accent = _cols(r, fam, 2)
    glass = MA((0.9, 0.96, 1.0), 0.22)
    water = MA((0.32, 0.64, 1.0), 0.72, rough=0.05, emit=0.15)
    R, h = [(0.11, 0.2), (0.095, 0.27), (0.12, 0.22)][s]
    th = 0.008
    if s == 1:
        out = [(0, 0.0), (0, R * 0.82), (h, R)]
        bot = 0.03
    elif s == 2:
        out = [(0, 0.0), (0, R * 0.9), (0.02, R), (h * 0.7, R), (h * 0.85, R * 0.78), (h, R * 0.72)]
        bot = 0.014
    else:
        out = [(0, 0.0), (0, R * 0.95), (0.015, R), (h, R)]
        bot = 0.014
    inn = [(z, rr - th) for z, rr in out[2:]][::-1] + [(bot, out[1][1] - th), (bot, 0.0)]
    C.lathe("glass", out + [(h + 0.004, out[-1][1] - th * 0.5)] + inn, glass, root, segs=48)
    C.tube("rimband", _ring(out[-1][1] + 0.002, h - 0.012, 48), 0.008, M(trim, coat=0.7), root)
    if s == 0:
        C.tube("handle", [(R, 0, h * 0.8), (R + 0.06, 0, h * 0.75), (R + 0.07, 0, h * 0.45), (R + 0.05, 0, h * 0.25), (R, 0, h * 0.22)], 0.016, M(accent, coat=0.7), root)
    elif s == 1:
        C.tube("base", _ring(R * 0.82, 0.012, 48), 0.012, M(accent, coat=0.7), root)
    else:
        C.tube("neck", _ring(R * 0.74, h * 0.85, 48), 0.012, M(accent, coat=0.7), root)
    piv = C.empty("water_pivot", root, (0, 0, bot + 0.002))
    wr = min(rr for z, rr in out[1:]) - th - 0.004
    wh = (h * 0.7 if s == 2 else h - 0.02) - bot
    C.lathe("water", [(0, 0.0), (0, wr), (wh, wr), (wh, 0.0)], water, piv, segs=40)
    piv.scale = (1, 1, 0.001)


def birdhouse(r, s, fam, root):
    body, roof, trim = _cols(r, fam, 3)
    hp = [1.0, 0.85, 1.15][s]
    C.tube("pole", [(0, 0, 0), (0, 0, hp)], 0.035, M(trim, rough=0.5), root)
    C.sphere("foot", (0, 0, 0.02), (0.12, 0.12, 0.03), M(trim, coat=0.5), root, 24)
    if s == 0:
        C.rounded_box("box", (0, 0, hp + 0.14), (0.3, 0.26, 0.28), 0.04, M(body, coat=0.5), root)
        for sx in (-1, 1):
            C.rounded_box("roof", (sx * 0.09, 0, hp + 0.33), (0.22, 0.34, 0.035), 0.015, M(roof, coat=0.6), root).rotation_euler = (0, math.radians(sx * 35), 0)
        door_z = hp + 0.15
    elif s == 1:
        C.lathe("box", [(hp, 0.0), (hp, 0.14), (hp + 0.02, 0.15), (hp + 0.28, 0.15), (hp + 0.3, 0.0)], M(body, coat=0.5), root, segs=40)
        C.lathe("roof", [(hp + 0.27, 0.0), (hp + 0.27, 0.2), (hp + 0.29, 0.21), (hp + 0.48, 0.02), (hp + 0.5, 0.0)], M(roof, coat=0.6), root, segs=40)
        C.sphere("tip", (0, 0, hp + 0.51), (0.035,) * 3, M(trim, coat=0.7), root, 16)
        door_z = hp + 0.15
    else:
        C.lathe("box", [(hp, 0.0), (hp, 0.15), (hp + 0.26, 0.17), (hp + 0.28, 0.0)], M(body, coat=0.5), root, segs=6)
        C.lathe("roof", [(hp + 0.27, 0.0), (hp + 0.27, 0.24), (hp + 0.31, 0.24), (hp + 0.33, 0.0)], M(roof, coat=0.6), root, segs=48)
        door_z = hp + 0.14
    C.sphere("door", (0, -0.13 if s == 0 else -0.145, door_z), (0.045, 0.02, 0.045), M((0.15, 0.1, 0.12), rough=0.7), root, 20)
    C.tube("perch", [(0, -0.13, door_z - 0.07), (0, -0.22, door_z - 0.07)], 0.01, M(trim), root)


def planter_box(r, s, fam, root):
    box, f1, f2, f3 = _cols(r, fam, 4)
    leaf = M((0.35, 0.72, 0.4), rough=0.5)
    if s == 0:
        C.rounded_box("box", (0, 0, 0.13), (0.9, 0.26, 0.26), 0.05, M(box, rough=0.5, coat=0.4), root)
        spots = [(-0.3 + 0.15 * k, 0) for k in range(5)]
        top = 0.26
    elif s == 1:
        C.rounded_box("box", (0, 0, 0.42), (0.8, 0.24, 0.18), 0.05, M(box, rough=0.5, coat=0.4), root)
        for x in (-0.33, 0.33):
            for y in (-0.08, 0.08):
                C.tube("leg", [(x, y, 0.0), (x, y, 0.34)], 0.02, M(box, rough=0.5), root)
        spots = [(-0.27 + 0.135 * k, 0) for k in range(5)]
        top = 0.51
    else:
        spots = []
        for k, (x, z, rr) in enumerate(((-0.32, 0.0, 0.14), (0.0, 0.18, 0.13), (0.32, 0.36, 0.12))):
            C.rounded_box("step", (x, 0.02, z / 2 + 0.0001), (0.3, 0.3, max(z, 0.02)), 0.02, M((0.95, 0.92, 0.86), rough=0.5), root) if z > 0 else None
            C.lathe("pot", [(z, 0.0), (z, rr * 0.75), (z + rr * 1.2, rr), (z + rr * 1.3, 0.0)], M([box, f3, box][k], coat=0.5), root, segs=36)
            spots.append((x, z + rr * 1.3))
        for k, (x, z) in enumerate(spots):
            C.tube("stem", [(x, 0, z), (x, 0, z + 0.22)], 0.012, leaf, root)
            C.sphere("bloom", (x, 0, z + 0.25), (0.06, 0.06, 0.06), M([f1, f2, f1][k], coat=0.6), root, 20)
            C.leaf("lf", 0.12, 0.05, 0.3, leaf, root).location = (x + 0.03, 0, z + 0.1)
        return
    for k, (x, y) in enumerate(spots):
        h = 0.18 + 0.08 * ((k * 7) % 3)
        C.tube("stem", [(x, y, top), (x, y, top + h)], 0.012, leaf, root)
        if s == 0:
            for j in range(5):
                a = j * 1.2566
                C.sphere("pet", (x + math.cos(a) * 0.04, y - 0.01, top + h + math.sin(a) * 0.04), (0.03, 0.012, 0.03), M(f1 if k % 2 else f2, coat=0.3), root, 12)
            C.sphere("ctr", (x, y - 0.015, top + h), (0.022,) * 3, M((1, 0.85, 0.3)), root, 12)
        else:
            C.lathe("tulip", [(top + h - 0.02, 0.0), (top + h, 0.035), (top + h + 0.06, 0.04), (top + h + 0.09, 0.0)], M(f1 if k % 2 else f3, coat=0.5), root, segs=16).location = (x, y, 0)


def pouf(r, s, fam, root):
    c, d, e = _cols(r, fam, 3)
    if s == 0:
        C.metablob("bag", [((0, 0, 0.2), 0.3, (1, 1, 0.75)), ((0, 0.04, 0.42), 0.2, (1, 1, 1))], M(c, rough=0.8, coat=0.1), root)
    elif s == 1:
        C.lathe("pouf", [(0, 0.0), (0, 0.28), (0.04, 0.32), (0.26, 0.32), (0.3, 0.28), (0.31, 0.0)], M(c, rough=0.75, coat=0.1), root, segs=48)
        C.sphere("btn", (0, 0, 0.31), (0.04, 0.04, 0.02), M(d, coat=0.6), root, 16)
        C.tube("seam", _ring(0.322, 0.155, 48), 0.012, M(d, rough=0.6), root)
    else:
        z = 0.0
        for k, (w, h) in enumerate(((0.62, 0.12), (0.52, 0.11), (0.4, 0.1))):
            C.rounded_box("cush", (0.02 * k, 0, z + h / 2), (w, w, h), 0.05, M([c, d, e][k], rough=0.75, coat=0.1), root).rotation_euler = (0, 0, math.radians(12 * k))
            z += h


def finish_line(r, s, fam, root):
    c1, c2 = _cols(r, fam, 2)
    W = [1.8, 1.9, 1.7][s]
    white = M((0.98, 0.97, 0.94), rough=0.5)
    dark = M((0.2, 0.18, 0.28), rough=0.5)
    if s != 1:
        n = 12
        for i in range(n):
            for j in range(2):
                C.rounded_box("chk", (-W / 2 + W * (i + 0.5) / n, (j - 0.5) * 0.15, 0.006), (W / n, 0.15, 0.012), 0.004, white if (i + j) % 2 else dark, root)
    if s == 0:
        for x in (-W / 2 - 0.08, W / 2 + 0.08):
            C.tube("pole", [(x, 0, 0), (x, 0, 0.8)], 0.025, M(c1, coat=0.6), root)
            C.sphere("cap", (x, 0, 0.82), (0.04,) * 3, M(c2, coat=0.7), root, 16)
            fl = C.empty("flag", root, (x, 0, 0.62))
            for i in range(3):
                for j in range(2):
                    C.rounded_box("fl", (0.04 + 0.06 * i, 0, 0.03 + 0.06 * j), (0.06, 0.012, 0.06), 0.004, white if (i + j) % 2 else dark, fl)
    elif s == 1:
        H = 1.5
        pts = [(math.cos(math.pi * k / 24) * W / 2, 0, math.sin(math.pi * k / 24) * H) for k in range(25)]
        C.tube("arch", pts, 0.06, M(c1, coat=0.6, rough=0.35), root)
        for k in range(1, 24, 2):
            x, _, z = pts[k]
            C.sphere("ball", (x, -0.05, z), (0.05,) * 3, M(c2, coat=0.7), root, 16)
        C.rounded_box("line", (0, 0, 0.006), (W, 0.12, 0.012), 0.005, white, root)
    else:
        for x in (-W / 2 - 0.1, W / 2 + 0.1):
            C.lathe("cone", [(0, 0.0), (0, 0.13), (0.03, 0.13), (0.04, 0.09), (0.36, 0.03), (0.38, 0.0)], M(c1, coat=0.5, rough=0.4), root, segs=32).location = (x, 0, 0)
            C.tube("band", [(x + math.cos(k * 6.2832 / 32) * 0.065, math.sin(k * 6.2832 / 32) * 0.065, 0.2) for k in range(33)], 0.012, white, root)
        C.tube("tape", [(-W / 2 - 0.1, 0, 0.3), (0, 0, 0.26), (W / 2 + 0.1, 0, 0.3)], 0.012, M(c2, coat=0.3), root)


def paint_palette(r, s, fam, root):
    base, rim = _cols(r, fam, 2)
    white = M((0.98, 0.97, 0.95), rough=0.4, coat=0.5)
    wells = []
    if s == 0:
        bm = bmesh.new()
        pts = []
        for k in range(40):
            a = k * 6.2832 / 40
            rr = 0.3 * (1 + 0.12 * math.cos(2 * a)) * (0.82 if abs(math.sin(a / 2 - 1.2)) < 0.12 else 1.0)
            pts.append((math.cos(a) * rr, math.sin(a) * rr * 0.75))
        bot = [bm.verts.new((x, y, 0)) for x, y in pts]
        top = [bm.verts.new((x, y, 0.035)) for x, y in pts]
        bm.faces.new(bot[::-1])
        bm.faces.new(top)
        for i in range(len(pts)):
            j = (i + 1) % len(pts)
            bm.faces.new((bot[i], bot[j], top[j], top[i]))
        o = C.mesh_obj("pal", bm, M(base, rough=0.45, coat=0.6), root, smooth=False)
        bv = o.modifiers.new("b", "BEVEL"); bv.width = 0.012; bv.segments = 3
        C.sphere("hole", (0.2, -0.05, 0.036), (0.04, 0.035, 0.004), M((0.2, 0.18, 0.25)), root, 20)
        wells = [(-0.17, 0.08), (-0.05, 0.13), (0.08, 0.12), (-0.2, -0.06)]
        z = 0.037
    elif s == 1:
        C.rounded_box("tray", (0, 0, 0.03), (0.62, 0.36, 0.06), 0.025, M(base, rough=0.45, coat=0.6), root)
        C.tube("rim", [(-0.31, -0.18, 0.06), (0.31, -0.18, 0.06), (0.31, 0.18, 0.06), (-0.31, 0.18, 0.06), (-0.31, -0.18, 0.06)], 0.012, M(rim, coat=0.6), root)
        wells = [(-0.2 + 0.2 * i, 0.08) for i in range(3)] + [(-0.2 + 0.2 * i, -0.08) for i in range(3)]
        z = 0.061
    else:
        C.lathe("tray", [(0, 0.0), (0, 0.26), (0.02, 0.29), (0.04, 0.28), (0.04, 0.0)], M(base, rough=0.45, coat=0.6), root, segs=60)
        wells = [(math.cos(k * 1.2566 + 0.3) * 0.18, math.sin(k * 1.2566 + 0.3) * 0.18) for k in range(5)] + [(0, 0)]
        z = 0.041
    for x, y in wells:
        C.sphere("well", (x, y, z), (0.055, 0.055, 0.008), white, root, 24)


def lidded_box(r, s, fam, root):
    body, lid, trim = _cols(r, fam, 3)
    W, D, H = [(0.62, 0.5, 0.42), (0.56, 0.56, 0.4), (0.7, 0.44, 0.38)][s]
    if s == 1:
        C.lathe("box", [(0, 0.0), (0, W / 2), (H, W / 2), (H, W / 2 - 0.02), (0.02, W / 2 - 0.02), (0.02, 0.0)], M(body, rough=0.5, coat=0.4), root, segs=56)
        C.tube("band", _ring(W / 2 + 0.005, H * 0.5, 56), 0.014, M(trim, coat=0.6), root)
    else:
        th = 0.025
        C.rounded_box("bot", (0, 0, th / 2), (W, D, th), 0.01, M(body, rough=0.5, coat=0.4), root)
        for sx in (-1, 1):
            C.rounded_box("side", (sx * (W / 2 - th / 2), 0, H / 2), (th, D, H), 0.01, M(body, rough=0.5, coat=0.4), root)
        for sy in (-1, 1):
            C.rounded_box("side", (0, sy * (D / 2 - th / 2), H / 2), (W, th, H), 0.01, M(body, rough=0.5, coat=0.4), root)
        C.rounded_box("strip", (0, -D / 2 - 0.004, H * 0.5), (W * 0.18, 0.012, H * 0.98), 0.005, M(trim, coat=0.6), root)
    hinge = C.empty("lid_hinge", root, (0, D / 2 if s != 1 else W / 2, H))
    if s == 0:
        C.rounded_box("lid", (0, -D / 2, 0.03), (W + 0.04, D + 0.04, 0.06), 0.02, M(lid, rough=0.45, coat=0.6), hinge)
        C.sphere("knob", (0, -D - 0.025, 0.03), (0.035, 0.025, 0.025), M(trim, coat=0.7), hinge, 16)
    elif s == 1:
        lg = C.empty("lidg", hinge, (0, -W / 2, 0))
        C.lathe("lid", [(0, 0.0), (0, W / 2 + 0.02), (0.07, W / 2 + 0.02), (0.08, 0.0)], M(lid, rough=0.45, coat=0.6), lg, segs=56)
        C.sphere("knob", (0, 0, 0.1), (0.04, 0.04, 0.03), M(trim, coat=0.7), lg, 16)
    else:
        lg = C.empty("lidg", hinge, (0, -D / 2, 0))
        bm_ = C.lathe("lid", [(0, 0.0), (0.0, D / 2 + 0.02), (0.08, D / 2 * 0.8), (0.14, 0.0)], M(lid, rough=0.45, coat=0.6), lg, segs=40, sx=(W + 0.04) / (D + 0.04), sy=1.0)
        C.rounded_box("clasp", (0, -D / 2 - 0.03, -0.02), (0.08, 0.02, 0.08), 0.01, M(trim, coat=0.8), lg)


def toy_speaker(r, s, fam, root):
    body, grille, accent = _cols(r, fam, 3)
    dark = M((0.16, 0.15, 0.22), rough=0.55, coat=0.3)
    if s == 0:
        C.rounded_box("cab", (0, 0, 0.17), (0.3, 0.22, 0.34), 0.05, M(body, coat=0.6), root)
        for z, rr in ((0.22, 0.09), (0.09, 0.05)):
            fc = C.empty("cone", root, (0, -0.112, z), (math.radians(90), 0, 0))
            C.lathe("ring", [(0, 0.0), (0, rr), (0.01, rr + 0.012), (0.018, rr), (0.018, 0.0)], M(grille, coat=0.5), fc, segs=40)
            C.sphere("dust", (0, 0, 0.012), (rr * 0.8, rr * 0.8, 0.02), dark, fc, 24)
        led = (0.11, -0.112, 0.31)
    elif s == 1:
        C.lathe("cyl", [(0, 0.0), (0, 0.11), (0.02, 0.12), (0.26, 0.12), (0.28, 0.11), (0.28, 0.0)], M(body, coat=0.6), root, segs=48)
        for z in (0.07, 0.11, 0.15, 0.19):
            C.tube("grl", _ring(0.122, z, 48), 0.006, M(grille, rough=0.5), root)
        led = (0.0, -0.122, 0.24)
    else:
        C.rounded_box("cab", (0, 0, 0.13), (0.42, 0.18, 0.26), 0.06, M(body, coat=0.6), root)
        C.tube("handle", [(-0.15, 0, 0.25), (-0.12, 0, 0.34), (0.12, 0, 0.34), (0.15, 0, 0.25)], 0.014, M(accent, coat=0.6), root)
        fc = C.empty("cone", root, (-0.07, -0.092, 0.13), (math.radians(90), 0, 0))
        C.lathe("ring", [(0, 0.0), (0, 0.08), (0.012, 0.09), (0.02, 0.08), (0.02, 0.0)], M(grille, coat=0.5), fc, segs=40)
        C.sphere("dial", (0.12, -0.092, 0.16), (0.035, 0.015, 0.035), M(accent, coat=0.7), root, 20)
        led = (0.12, -0.092, 0.07)
    lm = C.mat("led", (0.3, 1.0, 0.45), rough=0.2, emit=3.0)
    C.sphere("led", led, (0.018, 0.012, 0.018), lm, root, 16)


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
