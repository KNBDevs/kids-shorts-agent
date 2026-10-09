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


def star_plush(r, s, fam, root):
    c, d = _cols(r, fam, 2)
    soft = M(c, rough=0.85, coat=0.05)
    face = M((0.2, 0.12, 0.15), rough=0.6)
    if s == 0:
        balls = [((0, 0, 0), 0.11, (1, 0.7, 1))]
        for k in range(5):
            a = k * 1.2566 + 1.5708
            for j, t in enumerate((0.1, 0.17, 0.23)):
                balls.append(((math.cos(a) * t, 0, math.sin(a) * t), 0.07 - 0.018 * j, (1, 0.8, 1)))
        C.metablob("star", balls, soft, root)
    elif s == 1:
        C.sphere("core", (0, 0, 0), (0.09, 0.07, 0.09), soft, root, 24)
        for k in range(4):
            a = k * 1.5708
            C.sphere("ray", (math.cos(a) * 0.13, 0, math.sin(a) * 0.13), (0.11, 0.04, 0.035), soft, root, 20, rot=(0, -a, 0))
    else:
        pts = [(math.cos(math.radians(a)) * 0.17, 0, math.sin(math.radians(a)) * 0.17) for a in range(60, 301, 20)]
        C.tube("moon", pts, 0.07, soft, root, radii=[0.35, 0.65, 0.85, 1, 1, 1, 1, 1, 1, 1, 0.85, 0.65, 0.35])
        C.sphere("mini", (0.12, 0, 0.12), (0.045, 0.03, 0.045), M(d, rough=0.8), root, 16)
    for sx in (-1, 1):
        C.sphere("eye", (sx * 0.035 + (-0.09 if s == 2 else 0), -0.075 if s != 2 else -0.06, 0.01), (0.012, 0.006, 0.016), face, root, 12)
    C.tube("smile", [((-0.09 if s == 2 else 0) + 0.025 * math.cos(math.radians(a)), -0.078 if s != 2 else -0.063, -0.02 + 0.015 * math.sin(math.radians(a))) for a in range(200, 341, 20)], 0.004, face, root)


def play_door(r, s, fam, root):
    fr, leaf, knob = _cols(r, fam, 3)
    W, H = [(1.1, 1.95), (1.05, 2.0), (1.15, 1.9)][s]
    fm = M(fr, rough=0.45, coat=0.5)
    lm = M(leaf, rough=0.5, coat=0.4)
    for x in (-W / 2 - 0.06, W / 2 + 0.06):
        C.rounded_box("post", (x, 0, H / 2), (0.12, 0.16, H), 0.03, fm, root)
        C.rounded_box("foot", (x, 0, 0.03), (0.2, 0.42, 0.06), 0.025, fm, root)
    if s == 1:
        arc = [(math.cos(math.pi * k / 20) * (W / 2 + 0.06), 0, H + math.sin(math.pi * k / 20) * (W / 2 + 0.06)) for k in range(21)]
        C.tube("arch", arc, 0.065, fm, root)
    else:
        C.rounded_box("top", (0, 0, H + 0.06), (W + 0.24, 0.16, 0.12), 0.03, fm, root)
    hinge = C.empty("door_hinge", root, (-W / 2, 0, 0))
    C.rounded_box("leaf", (W / 2, 0, H / 2 + 0.01), (W - 0.03, 0.07, H - 0.03), 0.025, lm, hinge)
    if s == 1:
        lg = C.empty("leaftop", hinge, (W / 2, 0, H), (math.radians(90), 0, 0))
        C.lathe("ltop", [(-0.035, 0.0), (-0.035, W / 2 - 0.02), (0.035, W / 2 - 0.02), (0.035, 0.0)], lm, lg, segs=48)
    if s == 0:
        win = C.empty("win", hinge, (W / 2, -0.04, H * 0.72), (math.radians(90), 0, 0))
        C.lathe("winr", [(0, 0.0), (0, 0.17), (0.02, 0.19), (0.04, 0.17), (0.04, 0.0)], M(knob, coat=0.6), win, segs=40)
        C.sphere("glass", (W / 2, -0.045, H * 0.72), (0.15, 0.01, 0.15), M((0.75, 0.9, 1.0), rough=0.1, coat=1.0), hinge, 32)
    elif s == 2:
        for x in (W * 0.25, W * 0.5, W * 0.75):
            C.rounded_box("plank", (x, -0.04, H / 2), (0.025, 0.012, H - 0.15), 0.008, M(knob, rough=0.6), hinge)
        C.sphere("port", (W / 2, -0.045, H * 0.75), (0.12, 0.01, 0.12), M((0.75, 0.9, 1.0), rough=0.1, coat=1.0), hinge, 32)
    for sy in (-1, 1):
        C.sphere("knob", (W - 0.12, sy * 0.07, H * 0.48), (0.05, 0.04, 0.05), M(knob, coat=0.8), hinge, 20)


def snack_plate(r, s, fam, root):
    c, d = _cols(r, fam, 2)
    pm = M((0.98, 0.97, 0.94), rough=0.3, coat=0.7)
    if s == 0:
        C.lathe("plate", [(0, 0.0), (0, 0.1), (0.012, 0.13), (0.02, 0.2), (0.035, 0.24), (0.04, 0.235), (0.028, 0.2), (0.022, 0.13), (0.022, 0.0)], pm, root, segs=56)
        for k in range(12):
            a = k * 0.5236
            C.sphere("dot", (math.cos(a) * 0.215, math.sin(a) * 0.215, 0.032), (0.012, 0.012, 0.005), M(c, coat=0.6), root, 10)
    elif s == 1:
        C.rounded_box("plate", (0, 0, 0.015), (0.42, 0.42, 0.03), 0.012, pm, root)
        C.tube("rim", [(-0.19, -0.19, 0.032), (0.19, -0.19, 0.032), (0.19, 0.19, 0.032), (-0.19, 0.19, 0.032), (-0.19, -0.19, 0.032)], 0.01, M(c, coat=0.6), root)
    else:
        C.sphere("plate", (0, 0, 0.012), (0.27, 0.18, 0.016), M(c, rough=0.4, coat=0.6), root, 40)
        C.tube("vein", [(-0.22, 0, 0.026), (0.2, 0, 0.026)], 0.006, M(d, coat=0.4), root)
        for sx in (-1, 1):
            for k in range(3):
                x = -0.12 + 0.1 * k
                C.tube("vein", [(x, 0, 0.026), (x + 0.06, sx * 0.1, 0.026)], 0.005, M(d, coat=0.4), root)


def bubble_blower(r, s, fam, root):
    body, ring, trim = _cols(r, fam, 3)
    bm_ = M(body, rough=0.35, coat=0.7)
    rm = M(ring, rough=0.3, coat=0.8)
    tm = M(trim, rough=0.35, coat=0.7)
    if s == 0:
        C.rounded_box("base", (0, 0, 0.25), (0.6, 0.45, 0.5), 0.08, bm_, root)
        hub = C.empty("nozzle", root, (0, -0.05, 0.62), (math.radians(90), 0, 0))
        C.lathe("fan", [(-0.08, 0.0), (-0.08, 0.2), (0.08, 0.2), (0.08, 0.0)], tm, hub, segs=48)
        C.tube("wand", _ring(0.24, 0.1, 48), 0.025, rm, hub)
        for k in range(4):
            C.sphere("lamp", (-0.2 + 0.13 * k, -0.226, 0.38), (0.035, 0.015, 0.035), M([(1, 0.5, 0.6), (0.5, 0.9, 0.6), (1, 0.85, 0.3), (0.5, 0.7, 1)][k], rough=0.3, emit=1.0), root, 16)
    elif s == 1:
        C.lathe("tank", [(0, 0.0), (0, 0.25), (0.05, 0.27), (0.5, 0.25), (0.56, 0.18), (0.6, 0.0)], bm_, root, segs=48)
        hub = C.empty("nozzle", root, (0, -0.1, 0.75), (math.radians(70), 0, 0))
        C.lathe("horn", [(0.0, 0.05), (0.12, 0.06), (0.22, 0.1), (0.28, 0.18), (0.3, 0.2), (0.28, 0.17), (0.2, 0.08), (0.05, 0.04)], tm, hub, segs=48)
        C.tube("wand", _ring(0.2, 0.31, 48), 0.022, rm, hub)
    else:
        for x in (-0.22, 0.22):
            C.tube("leg", [(x, 0, 0), (x, 0, 0.55)], 0.03, tm, root)
        C.sphere("drum", (0, 0, 0.62), (0.32, 0.26, 0.22), bm_, root, 40)
        hub = C.empty("nozzle", root, (0, -0.24, 0.66), (math.radians(90), 0, 0))
        C.tube("wand", _ring(0.18, 0.06, 48), 0.024, rm, hub)
        C.tube("stick", [(0, 0, 0.0), (0, 0, 0.06)], 0.02, rm, hub)
        C.sphere("bulb", (0, 0, 0.86), (0.06, 0.06, 0.06), M(ring, rough=0.3, emit=0.8), root, 16)


def play_ball(r, s, fam, root):
    cs = _cols(r, fam, 4)
    R = 0.11
    if s == 0:
        C.sphere("ball", (0, 0, R), (R, R, R), M((0.98, 0.97, 0.94), rough=0.35, coat=0.6), root, 32)
        for k in range(3):
            C.sphere("seg", (0, 0, R), (R * 1.004, R * 0.35, R * 1.004), M(cs[k], rough=0.35, coat=0.6), root, 32, rot=(0, 0, k * 1.0472))
    elif s == 1:
        C.sphere("ball", (0, 0, R), (R, R, R), M(cs[0], rough=0.4, coat=0.6), root, 32)
        for k in range(14):
            a = k * 2.399
            z = 1 - 2 * (k + 0.5) / 14
            rr = math.sqrt(1 - z * z)
            n = Vector((math.cos(a) * rr, math.sin(a) * rr, z))
            _dot("spot", Vector((0, 0, R)) + n * R * 1.002, n, R * 0.2, M(cs[1], coat=0.6), root)
    else:
        C.sphere("ball", (0, 0, R), (R, R, R), M(cs[2], rough=0.4, coat=0.6), root, 32)
        C.tube("band", _ring(R * 1.01, R, 48), R * 0.12, M(cs[3], coat=0.6), root)
        C.tube("band2", [(math.cos(k * 6.2832 / 48) * R * 1.01, 0, R + math.sin(k * 6.2832 / 48) * R * 1.01) for k in range(49)], R * 0.12, M(cs[3], coat=0.6), root)


def _font():
    import os
    f = next((x for x in bpy.data.fonts if 'Lilita' in x.name or 'LilitaOne' in x.filepath), None)
    if f is None:
        f = bpy.data.fonts.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "LilitaOne.ttf"))
    return f


def glyph(txt, size, depth, m, parent, loc=(0, 0, 0)):
    cu = bpy.data.curves.new("g", "FONT")
    cu.body = txt
    cu.font = _font()
    cu.align_x = "CENTER"
    cu.align_y = "CENTER"
    cu.size = size
    cu.extrude = depth
    cu.bevel_depth = depth * 0.45
    cu.bevel_resolution = 2
    o = bpy.data.objects.new("glyph", cu)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(m)
    o.parent = parent
    o.location = loc
    o.rotation_euler = (math.radians(90), 0, 0)
    return o


def number_stand(r, s, fam, root, label=None):
    c, d, e = _cols(r, fam, 3)
    label = label if label is not None else str(1 + r.randrange(9))
    body = M(c, rough=0.4, coat=0.6)
    trim = M(d, rough=0.45, coat=0.5)
    ink = M((0.99, 0.98, 0.95), rough=0.3, coat=0.7, emit=0.08) if isinstance(fam, tuple) else M(tuple(v * 0.42 for v in e), rough=0.3, coat=0.7)
    face = C.empty("face", root, (0, 0, 0))
    if s == 0:
        C.rounded_box("foot", (0, 0, 0.03), (0.4, 0.26, 0.06), 0.025, trim, root)
        C.rounded_box("tile", (0, 0, 0.29), (0.44, 0.1, 0.44), 0.07, body, face)
        g = glyph(label, 0.32, 0.018, ink, face, (0, -0.05, 0.27))
    elif s == 1:
        C.lathe("base", [(0, 0.0), (0, 0.17), (0.015, 0.185), (0.04, 0.18), (0.05, 0.15), (0.05, 0.0)], trim, root, segs=48)
        C.tube("peg", [(0, 0, 0.04), (0, 0, 0.12)], 0.035, trim, root)
        dk = C.empty("disc", face, (0, 0.045, 0.33), (math.radians(90), 0, 0))
        C.lathe("dsk", [(0, 0.0), (0, 0.2), (0.02, 0.23), (0.07, 0.23), (0.09, 0.2), (0.09, 0.0)], body, dk, segs=64)
        C.tube("rim", [(math.cos(k * 6.2832 / 48) * 0.205, -0.003, 0.33 + math.sin(k * 6.2832 / 48) * 0.205) for k in range(49)], 0.012, M(d, coat=0.6), face)
        g = glyph(label, 0.3, 0.016, ink, face, (0, -0.06, 0.31))
    else:
        C.rounded_box("plinth", (0, 0, 0.045), (0.46, 0.22, 0.09), 0.03, trim, root)
        C.rounded_box("block", (0, 0, 0.25), (0.38, 0.14, 0.32), 0.05, body, face)
        cap = C.empty("cap", face, (0, 0.0, 0.41), (math.radians(90), 0, 0))
        C.lathe("dome", [(-0.07, 0.0), (-0.07, 0.185), (-0.055, 0.19), (0.055, 0.19), (0.07, 0.185), (0.07, 0.0)], body, cap, segs=48)
        C.sphere("dot", (0, -0.07, 0.47), (0.035, 0.015, 0.035), M(e, coat=0.7), face, 16)
        g = glyph(label, 0.27, 0.016, ink, face, (0, -0.07, 0.25))
    g.name = "glyph_" + label
    return face


def _rich(c, k=1.6, v=0.92):
    import colorsys
    h, ss, vv = colorsys.rgb_to_hsv(*c)
    return colorsys.hsv_to_rgb(h, min(1.0, ss * k + 0.1), vv * v)


def bridge_kit(r, s, fam, root):
    wood, top, extra, rail = [_rich(c) for c in _cols(r, fam, 4)]
    if s == 0:
        wood = (0.86, 0.66, 0.42)
    bm_ = M(wood, rough=0.55 if s == 0 else 0.4, coat=0.3 if s == 0 else 0.6)
    tm = M(top, rough=0.45, coat=0.5)
    xm = M(extra, rough=0.45, coat=0.55)
    water = M((0.45, 0.72, 0.95), rough=0.25, coat=0.8)
    foam = M((0.92, 0.97, 1.0), rough=0.4, coat=0.4)
    C.rounded_box("river", (0, 0, 0.012), (1.36, 0.78, 0.024), 0.01, water, root)
    for k in range(3):
        y = -0.24 + 0.24 * k
        C.tube("wave", [(-0.55 + 0.11 * j, y + 0.03 * math.sin(j * 1.6 + k), 0.026) for j in range(11)], 0.008, foam, root)
    H = 0.3
    parts = {}
    for side in (-1, 1):
        b = C.empty("bk_bank" + ("L" if side < 0 else "R"), root, (side * 0.93, 0, 0))
        if s == 0:
            C.rounded_box("bank", (0, 0, H / 2), (0.5, 0.62, H), 0.04, bm_, b)
            C.rounded_box("step", (side * 0.2, 0, H * 0.25), (0.22, 0.62, H * 0.5), 0.03, tm, b)
        elif s == 1:
            C.sphere("mound", (0, 0, 0.0), (0.3, 0.34, H), bm_, b, 40)
            C.rounded_box("pad", (0, 0, H - 0.04), (0.42, 0.5, 0.06), 0.03, tm, b)
        else:
            C.rounded_box("bank", (0, 0, H / 2), (0.46, 0.6, H), 0.06, bm_, b)
            for y in (-0.2, 0.2):
                C.sphere("stud", (0, y, H + 0.01), (0.05, 0.05, 0.025), xm, b, 16)
        parts[b.name] = b
    for i, x in enumerate((-0.3, 0.3)):
        p = C.empty(f"bk_base{i}", root, (x, 0, 0))
        if s == 0:
            C.rounded_box("pillar", (0, 0, H / 2), (0.14, 0.34, H), 0.025, tm, p)
        elif s == 1:
            C.lathe("pillar", [(0, 0.0), (0, 0.09), (0.02, 0.1), (H - 0.02, 0.1), (H, 0.09), (H, 0.0)], tm, p, segs=40)
        else:
            for y in (-0.12, 0.12):
                C.tube("leg", [(-0.05, y, 0.0), (0, y, H - 0.03)], 0.025, tm, p)
                C.tube("leg", [(0.05, y, 0.0), (0, y, H - 0.03)], 0.025, tm, p)
            C.rounded_box("cap", (0, 0, H - 0.02), (0.14, 0.34, 0.04), 0.015, xm, p)
    D = 0.06

    def plank(name, L, mat):
        p = C.empty(name, root, (0, 0, H + D / 2))
        if s == 1:
            C.rounded_box("deck", (0, 0, 0), (L, 0.36, D), D * 0.45, mat, p)
        else:
            C.rounded_box("deck", (0, 0, 0), (L, 0.36, D), 0.018, mat, p)
        if s == 0:
            n = max(2, int(L / 0.12))
            for k in range(1, n):
                C.tube("seam", [(-L / 2 + L * k / n, -0.181, -D * 0.3), (-L / 2 + L * k / n, -0.181, D * 0.3)], 0.004, M((0.6, 0.42, 0.25), rough=0.7), p)
        elif s == 2:
            for x in (-L / 2 + 0.05, L / 2 - 0.05):
                for y in (-0.16, 0.16):
                    C.tube("post", [(x, y, D / 2), (x, y, D / 2 + 0.1)], 0.012, M(rail, coat=0.6), p)
                    C.sphere("ball", (x, y, D / 2 + 0.11), (0.025,) * 3, M(rail, coat=0.7), p, 12)
        return p

    plank("bk_deck", 1.05, bm_).location.x = -0.2
    plank("bk_last", 0.5, xm).location.x = 0.6
    plank("bk_short", 0.62, M(rail, rough=0.45, coat=0.5)).location.x = -0.45
    return root


def toy_magnet(r, s, fam, root):
    red = (0.88, 0.16, 0.18) if s != 2 else _rich(_cols(r, fam, 1)[0])
    body = M(red, rough=0.35, coat=0.7)
    tip = M((0.86, 0.88, 0.92), rough=0.25, coat=0.8)
    grip = M(_rich(_cols(r, fam, 2)[1]), rough=0.6, coat=0.2)
    if s == 0:
        arc = [(math.cos(math.pi * k / 20) * 0.11, 0, 0.11 + math.sin(math.pi * k / 20) * 0.11) for k in range(21)]
        C.tube("arc", arc, 0.045, body, root)
        for x in (-0.11, 0.11):
            C.tube("leg", [(x, 0, 0.11), (x, 0, 0.0)], 0.045, body, root)
            C.lathe("tip", [(-0.06, 0.0), (-0.06, 0.045), (-0.005, 0.045), (0.0, 0.035), (0.0, 0.0)], tip, C.empty("t", root, (x, 0, 0)), segs=32)
        C.tube("handle", [(0, 0, 0.22), (0, 0, 0.36)], 0.032, grip, root)
        C.sphere("knob", (0, 0, 0.37), (0.045, 0.045, 0.035), grip, root, 20)
        return (0, 0, -0.06)
    if s == 1:
        C.rounded_box("bar", (0, 0, 0.0), (0.12, 0.12, 0.3), 0.04, body, root)
        C.rounded_box("pole", (0, 0, -0.2), (0.125, 0.125, 0.12), 0.04, tip, root)
        C.tube("handle", [(0, 0, 0.15), (0, 0, 0.3)], 0.03, grip, root)
        C.sphere("knob", (0, 0, 0.31), (0.05, 0.05, 0.035), grip, root, 20)
        return (0, 0, -0.26)
    ring = C.empty("ring", root, (0, 0, 0), (math.radians(90), 0, 0))
    C.lathe("donut", [(-0.04, 0.05), (-0.045, 0.09), (-0.04, 0.12), (0.04, 0.12), (0.045, 0.09), (0.04, 0.05)], body, ring, segs=48)
    C.tube("face", [(math.cos(k * 6.2832 / 40) * 0.085, -0.047, math.sin(k * 6.2832 / 40) * 0.085) for k in range(41)], 0.018, tip, root)
    C.tube("stick", [(0, 0, 0.12), (0, 0, 0.34)], 0.025, grip, root)
    C.sphere("knob", (0, 0, 0.35), (0.04, 0.04, 0.04), grip, root, 20)
    return (0, -0.06, 0)


def fruit(r, s, fam, root):
    leaf = M((0.3, 0.68, 0.25), rough=0.5, coat=0.3)
    stem = M((0.4, 0.25, 0.12), rough=0.7)
    if s == 0:
        C.lathe("apple", [(0.0, 0.0), (0.0, 0.03), (0.01, 0.07), (0.04, 0.1), (0.09, 0.11), (0.14, 0.1), (0.17, 0.07), (0.185, 0.03), (0.175, 0.0)], M((0.9, 0.18, 0.15), rough=0.3, coat=0.8), root, segs=48)
        top = 0.175
    elif s == 1:
        C.lathe("pear", [(0.0, 0.0), (0.0, 0.04), (0.02, 0.09), (0.06, 0.105), (0.11, 0.085), (0.16, 0.055), (0.21, 0.045), (0.245, 0.03), (0.255, 0.0)], M((0.72, 0.85, 0.3), rough=0.35, coat=0.6), root, segs=48)
        top = 0.255
    else:
        C.sphere("orange", (0, 0, 0.095), (0.1, 0.1, 0.095), M((1.0, 0.55, 0.1), rough=0.55, coat=0.4), root, 40)
        C.sphere("navel", (0, 0, 0.19), (0.012, 0.012, 0.004), M((0.55, 0.4, 0.1), rough=0.6), root, 10)
        top = 0.19
    C.tube("stem", [(0, 0, top - 0.01), (0.008, 0, top + 0.04)], 0.007, stem, root)
    C.leaf("leaf", 0.04, 0.02, 0.2, leaf, C.empty("lf", root, (0.012, 0, top + 0.02), (0, math.radians(-60), math.radians(20))))


def low_table(r, s, fam, root):
    top, leg = [_rich(c, 1.3, 0.95) for c in _cols(r, fam, 2)]
    tm = M(top, rough=0.4, coat=0.6)
    lm = M(leg, rough=0.45, coat=0.5)
    Hh = 0.62
    if s == 0:
        C.rounded_box("top", (0, 0, Hh - 0.04), (1.2, 0.6, 0.08), 0.035, tm, root)
        for x in (-0.5, 0.5):
            for y in (-0.22, 0.22):
                C.tube("leg", [(x, y, 0.0), (x, y, Hh - 0.06)], 0.035, lm, root)
                C.sphere("foot", (x, y, 0.02), (0.05, 0.05, 0.025), lm, root, 16)
    elif s == 1:
        C.lathe("top", [(Hh - 0.08, 0.0), (Hh - 0.08, 0.5), (Hh - 0.065, 0.53), (Hh - 0.015, 0.53), (Hh, 0.5), (Hh, 0.0)], tm, root, segs=64, sy=0.6)
        C.lathe("ped", [(0.0, 0.0), (0.0, 0.26), (0.03, 0.27), (0.06, 0.24), (0.08, 0.07), (Hh - 0.08, 0.06), (Hh - 0.08, 0.0)], lm, root, segs=48, sy=0.6)
    else:
        C.rounded_box("top", (0, 0, Hh - 0.04), (1.15, 0.58, 0.08), 0.03, tm, root)
        for x in (-0.45, 0.45):
            for y in (-0.2, 0.2):
                C.tube("leg", [(x, 0, Hh - 0.08), (x + (0.06 if x > 0 else -0.06), y, 0.0)], 0.03, lm, root)
            C.tube("bar", [(x, -0.15, 0.2), (x, 0.15, 0.2)], 0.02, lm, root)
        C.tube("rail", [(-0.45, 0, 0.2), (0.45, 0, 0.2)], 0.02, lm, root)
    return Hh


def play_step(r, s, fam, root):
    a, b, c = [_rich(x, 1.3, 0.95) for x in _cols(r, fam, 3)]
    ma, mb, mc = M(a, rough=0.5, coat=0.4), M(b, rough=0.45, coat=0.5), M(c, rough=0.45, coat=0.5)
    if s == 0:
        C.rounded_box("blk", (0, 0, 0.11), (0.72, 0.46, 0.22), 0.06, ma, root)
        for x in (-0.22, 0.0, 0.22):
            C.rounded_box("strip", (x, -0.232, 0.11), (0.08, 0.01, 0.16), 0.004, mb, root)
        C.rounded_box("pad", (0, 0, 0.225), (0.62, 0.36, 0.02), 0.008, mc, root)
        return 0.235
    if s == 1:
        C.lathe("drum", [(0.0, 0.0), (0.0, 0.3), (0.02, 0.32), (0.2, 0.32), (0.22, 0.3), (0.22, 0.0)], ma, root, segs=56, sy=0.7)
        C.tube("band", [(math.cos(k * 6.2832 / 56) * 0.322, math.sin(k * 6.2832 / 56) * 0.322 * 0.7, 0.11) for k in range(57)], 0.016, mb, root)
        C.lathe("top", [(0.215, 0.0), (0.215, 0.27), (0.228, 0.26), (0.228, 0.0)], mc, root, segs=56, sy=0.7)
        return 0.228
    C.rounded_box("low", (0, 0, 0.07), (0.8, 0.5, 0.14), 0.04, ma, root)
    C.rounded_box("up", (0.12, 0.04, 0.17), (0.5, 0.38, 0.12), 0.04, mb, root)
    for x in (-0.3, 0.38):
        C.sphere("dot", (x, -0.252, 0.07), (0.03, 0.01, 0.03), mc, root, 12)
    return 0.23


def sponge(r, s, fam, root):
    base = (1.0, 0.82, 0.3) if s != 2 else (0.55, 0.85, 1.0)
    pad = (0.35, 0.75, 0.45)
    bm_ = M(base, rough=0.85, coat=0.0)
    pore = M(tuple(v * 0.7 for v in base), rough=0.9)
    if s == 0:
        C.rounded_box("body", (0, 0, 0.045), (0.26, 0.16, 0.09), 0.03, bm_, root)
        C.rounded_box("scrub", (0, 0, 0.1), (0.26, 0.16, 0.025), 0.01, M(pad, rough=0.9), root)
        pts = [(x, -0.081, z) for x in (-0.09, -0.04, 0.02, 0.07, 0.1) for z in (0.02, 0.05, 0.075)]
    elif s == 1:
        C.sphere("body", (0, 0, 0.055), (0.15, 0.1, 0.055), bm_, root, 40)
        pts = [(math.cos(a) * 0.1, -0.075 * abs(math.sin(a + 1.0)) - 0.02, 0.04 + 0.03 * math.sin(3 * a)) for a in [k * 0.6 for k in range(10)]]
    else:
        for k in range(5):
            a = k * 1.2566
            C.sphere("lobe", (math.cos(a) * 0.07, math.sin(a) * 0.07, 0.045), (0.07, 0.07, 0.045), bm_, root, 24)
        C.sphere("mid", (0, 0, 0.05), (0.06, 0.06, 0.05), bm_, root, 24)
        pts = [(math.cos(k * 0.9) * 0.1, -0.09, 0.03 + 0.012 * (k % 3)) for k in range(7)]
    for i, pt in enumerate(pts):
        C.sphere("pore", pt, (0.009 + 0.004 * (i % 2),) * 3, pore, root, 8)
    return bm_


def big_spoon(r, s, fam, root):
    steel = M((0.82, 0.84, 0.88), rough=0.18, coat=0.9)
    grip = M(_rich(_cols(r, fam, 1)[0]), rough=0.5, coat=0.4)
    L = [0.42, 0.38, 0.46][s]
    bw, bl = [(0.075, 0.11), (0.09, 0.09), (0.065, 0.13)][s]
    C.sphere("bowl", (-L / 2 + bl * 0.5, 0, 0.022), (bl * 0.5, bw * 0.5, 0.022), steel, root, 32)
    C.tube("neck", [(-L / 2 + bl * 0.95, 0, 0.03), (-L / 2 + bl + 0.06, 0, 0.045), (L / 2, 0, 0.055)], 0.011, steel, root)
    if s == 0:
        C.tube("grip", [(L / 2 - 0.14, 0, 0.055), (L / 2, 0, 0.058)], 0.02, grip, root)
    elif s == 1:
        C.sphere("knob", (L / 2, 0, 0.058), (0.03, 0.022, 0.016), grip, root, 16)
    else:
        C.tube("ring", [(L / 2 + 0.025 * math.cos(k * 6.2832 / 20), 0.025 * math.sin(k * 6.2832 / 20), 0.058) for k in range(21)], 0.007, grip, root)


def mixing_bowl(r, s, fam, root):
    c, d = [_rich(x, 1.2, 0.95) for x in _cols(r, fam, 2)]
    R, h = [(0.16, 0.1), (0.14, 0.12), (0.18, 0.08)][s]
    if s == 0:
        prof = [(0.0, 0.0), (0.0, R * 0.5), (h * 0.3, R * 0.8), (h, R), (h + 0.008, R - 0.006), (h * 0.3 + 0.01, R * 0.8 - 0.012), (0.012, R * 0.5 - 0.012), (0.012, 0.0)]
    elif s == 1:
        prof = [(0.0, 0.0), (0.0, R * 0.55), (0.02, R * 0.6), (h, R), (h + 0.008, R - 0.006), (0.03, R * 0.6 - 0.012), (0.03, 0.0)]
    else:
        prof = [(0.0, 0.0), (0.0, R * 0.7), (h * 0.6, R * 0.95), (h, R), (h + 0.008, R - 0.006), (h * 0.6, R * 0.95 - 0.012), (0.012, R * 0.7 - 0.012), (0.012, 0.0)]
    C.lathe("bowl", prof, M(c, rough=0.35, coat=0.7), root, segs=56)
    C.tube("rim", _ring(R - 0.002, h + 0.004, 56), 0.008, M(d, coat=0.7), root)
    piv = C.empty("water_pivot", root, (0, 0, 0.014 if s != 1 else 0.032))
    C.sphere("water", (0, 0, 0.0), (R * 0.62, R * 0.62, 0.01), MA((0.32, 0.64, 1.0), 0.75, rough=0.05, emit=0.15), piv, 32)
    piv.scale = (0.001, 0.001, 0.001)


def toy_elephant(r, s, fam, root):
    body_c = [(0.42, 0.5, 0.78), (0.6, 0.42, 0.78), (0.3, 0.6, 0.68)][s]
    acc = _rich(_cols(r, fam, 1)[0])
    bm_ = M(body_c, rough=0.75 if s != 1 else 0.45, coat=0.05 if s != 1 else 0.5)
    am = M(acc, rough=0.6, coat=0.3)
    ink = M((0.12, 0.1, 0.15), rough=0.4, coat=0.5)
    hi = M((1, 1, 1), rough=0.2, emit=0.3)
    if s == 1:
        C.rounded_box("body", (0, 0, 0.36), (0.5, 0.32, 0.3), 0.08, bm_, root)
        for x in (-0.16, 0.16):
            for y in (-0.1, 0.1):
                C.rounded_box("leg", (x, y, 0.12), (0.12, 0.12, 0.24), 0.04, bm_, root)
        C.rounded_box("head", (-0.3, 0, 0.5), (0.26, 0.28, 0.26), 0.08, bm_, root)
        hx, hz = -0.3, 0.5
        trunk = [(-0.42, 0, 0.48), (-0.5, 0, 0.4), (-0.52, 0, 0.3), (-0.48, 0, 0.24)]
        for sy in (-1, 1):
            C.rounded_box("ear", (-0.24, sy * 0.17, 0.52), (0.04, 0.16, 0.2), 0.02, am, root)
        C.tube("trunk", trunk, 0.045, bm_, root)
    else:
        if s == 0:
            C.sphere("body", (0, 0, 0.36), (0.3, 0.2, 0.2), bm_, root, 40)
            for x in (-0.15, 0.15):
                for y in (-0.1, 0.1):
                    C.tube("leg", [(x, y, 0.3), (x, y, 0.06)], 0.065, bm_, root)
                    C.sphere("pad", (x, y, 0.05), (0.07, 0.07, 0.04), am, root, 16)
            hx, hz = -0.3, 0.52
            C.sphere("head", (hx, 0, hz), (0.17, 0.16, 0.16), bm_, root, 40)
            ear = [(-0.24, 0.18, 0.55)]
            for sy in (-1, 1):
                C.sphere("ear", (-0.25, sy * 0.19, 0.55), (0.04, 0.13, 0.14), am, root, 24, rot=(0, 0, math.radians(sy * 20)))
        else:
            C.sphere("body", (0, 0, 0.34), (0.26, 0.22, 0.24), bm_, root, 40)
            for x in (-0.13, 0.13):
                for y in (-0.11, 0.11):
                    C.sphere("leg", (x, y, 0.09), (0.075, 0.075, 0.09), bm_, root, 20)
            hx, hz = -0.28, 0.5
            C.sphere("head", (hx, 0, hz), (0.15, 0.15, 0.15), bm_, root, 40)
            for sy in (-1, 1):
                C.sphere("ear", (-0.22, sy * 0.17, 0.52), (0.03, 0.11, 0.11), am, root, 20)
            C.sphere("patch", (0.05, -0.2, 0.38), (0.08, 0.03, 0.08), am, root, 16)
        trunk = [(hx - 0.13, 0, hz - 0.02), (hx - 0.21, 0, hz - 0.1), (hx - 0.23, 0, hz - 0.2), (hx - 0.19, 0, hz - 0.26)]
        C.tube("trunk", trunk, 0.04, bm_, root, radii=[1.3, 1.0, 0.85, 0.75])
    HR = [0.165, 0.14, 0.15][s]
    for sy in (-1, 1):
        d = Vector((-0.78, sy * 0.48, 0.4)).normalized()
        e = Vector((hx, 0, hz)) + d * HR
        if s == 1:
            e = Vector((hx - 0.135, sy * 0.07, hz + 0.05))
        C.sphere("eye", tuple(e), (0.022, 0.022, 0.028), ink, root, 12)
        C.sphere("shine", tuple(e + Vector((-0.016, -0.004 * sy, 0.012))), (0.007,) * 3, hi, root, 8)
    C.tube("tail", [(0.28 if s != 1 else 0.25, 0, 0.4), (0.34, 0, 0.34), (0.35, 0, 0.28)], 0.012, bm_, root)
    C.sphere("tuft", (0.35, 0, 0.27), (0.025,) * 3, am, root, 10)


def net_swing(r, s, fam, root):
    post, netc = [_rich(c, 1.3, 0.95) for c in _cols(r, fam, 2)]
    pm = M(post, rough=0.45, coat=0.5)
    nm = M(netc, rough=0.7, coat=0.1)
    W, H = [(0.6, 0.55), (0.52, 0.6), (0.66, 0.5)][s]
    for x in (-W / 2, W / 2):
        if s == 1:
            C.tube("post", [(x, 0, 0.0), (x, 0, H)], 0.022, pm, root)
            C.rounded_box("foot", (x, 0, 0.015), (0.08, 0.3, 0.03), 0.012, pm, root)
        else:
            for y in (-0.13, 0.13):
                C.tube("leg", [(x, y, 0.0), (x, 0, H)], 0.018, pm, root)
        C.sphere("cap", (x, 0, H + 0.01), (0.03,) * 3, pm, root, 12)
    if s == 2:
        arc = [(math.cos(math.pi * k / 16) * W / 2, 0, H + math.sin(math.pi * k / 16) * 0.08) for k in range(17)]
        C.tube("top", arc, 0.016, pm, root)
    else:
        C.tube("top", [(-W / 2, 0, H), (W / 2, 0, H)], 0.016, pm, root)
    hang = C.empty("net_hang", root, (0, 0, H - 0.12))
    for x in (-W / 2 + 0.06, W / 2 - 0.06):
        C.tube("rope", [(x, 0, H - 0.0), (x * 0.92, 0, H - 0.12)], 0.006, nm, root)
    n = 7
    w = W / 2 - 0.06
    for i in range(n):
        u = -1 + 2 * i / (n - 1)
        C.tube("nl", [(u * w * 0.98, -0.05 + 0.1 * j / 6, -0.12 * (1 - (u * 0.98) ** 2) * (1 - 0.3 * abs(j / 6 - 0.5))) for j in range(7)], 0.004, nm, hang)
    for j in range(4):
        v = -0.05 + 0.1 * j / 3
        C.tube("nw", [(-w + 2 * w * k / 12, v, -0.12 * (1 - (-1 + 2 * k / 12) ** 2)) for k in range(13)], 0.004, nm, hang)
    return hang



def toy_torch(r, s, fam, root):
    c, d = [_rich(x, 1.3, 0.95) for x in _cols(r, fam, 2)]
    bm_ = M(c, rough=0.4, coat=0.6)
    tm = M(d, rough=0.45, coat=0.5)
    lens = M((1.0, 0.95, 0.7), rough=0.1, coat=1.0, emit=2.5)
    ax = C.empty("axis", root, (0, 0, 0), (0, math.radians(90), 0))
    if s == 0:
        C.lathe("body", [(-0.13, 0.0), (-0.13, 0.03), (-0.12, 0.036), (0.05, 0.036), (0.07, 0.04), (0.12, 0.062), (0.13, 0.062), (0.13, 0.0)], bm_, ax, segs=48)
        C.tube("band", [(math.cos(k * 6.2832 / 40) * 0.038, math.sin(k * 6.2832 / 40) * 0.038, -0.06) for k in range(41)], 0.008, tm, ax)
        C.sphere("btn", (-0.02, 0, 0.038), (0.016, 0.012, 0.01), tm, root, 12)
        front, lr = 0.132, 0.052
    elif s == 1:
        C.rounded_box("body", (-0.04, 0, 0.0), (0.18, 0.1, 0.11), 0.03, bm_, root)
        C.tube("handle", [(-0.11, 0, 0.05), (-0.1, 0, 0.11), (0.02, 0, 0.11), (0.03, 0, 0.05)], 0.014, tm, root)
        C.lathe("bezel", [(0.04, 0.0), (0.04, 0.05), (0.055, 0.056), (0.07, 0.05), (0.07, 0.0)], tm, ax, segs=40)
        front, lr = 0.071, 0.044
    else:
        C.lathe("body", [(-0.14, 0.0), (-0.14, 0.018), (-0.13, 0.022), (0.08, 0.022), (0.09, 0.028), (0.11, 0.028), (0.11, 0.0)], bm_, ax, segs=40)
        for z in (-0.1, -0.08, -0.06):
            C.tube("rib", [(math.cos(k * 6.2832 / 32) * 0.023, math.sin(k * 6.2832 / 32) * 0.023, z) for k in range(33)], 0.004, tm, ax)
        C.tube("clip", [(-0.1, 0, 0.026), (0.0, 0, 0.034), (0.03, 0, 0.026)], 0.006, tm, root)
        front, lr = 0.112, 0.024
    C.sphere("lens", (front, 0, 0), (0.008, lr, lr), lens, root, 24)
    beam = C.empty("beam", ax, (0, 0, front + 0.005))
    C.lathe("cone", [(0.0, 0.0), (0.0, lr * 0.9), (0.7, 0.2), (0.7, 0.0)], MA((1.0, 0.95, 0.65), 0.22, emit=0.8), beam, segs=40)
    beam.scale = (0.001, 0.001, 0.001)
    return beam


def explain_panel(r, s, fam, root):
    c, d = [_rich(x, 1.3, 0.95) for x in _cols(r, fam, 2)]
    fm = M(c, rough=0.4, coat=0.6)
    sm = M(d, rough=0.45, coat=0.5)
    face = M((0.97, 0.96, 0.92), rough=0.6, coat=0.1, emit=0.15)
    if s == 0:
        R, z0 = 0.34, 0.95
        C.tube("rim", [(math.cos(k * 6.2832 / 64) * R, 0, z0 + math.sin(k * 6.2832 / 64) * R) for k in range(65)], 0.035, fm, root)
        dk = C.empty("dk", root, (0, 0.012, z0), (math.radians(90), 0, 0))
        C.lathe("face", [(-0.012, 0.0), (-0.012, R), (0.012, R), (0.012, 0.0)], face, dk, segs=64)
        C.tube("stem", [(0, 0.02, z0 - R - 0.02), (0, 0.02, 0.05)], 0.03, sm, root)
        C.lathe("foot", [(0, 0.0), (0, 0.2), (0.02, 0.21), (0.05, 0.18), (0.06, 0.0)], sm, root, segs=48, sy=0.7)
        W, H = 2 * R * 0.8, 2 * R * 0.8
    elif s == 1:
        z0 = 0.95
        C.rounded_box("board", (0, 0.02, z0), (0.82, 0.04, 0.62), 0.03, fm, root)
        C.rounded_box("face", (0, -0.002, z0), (0.72, 0.01, 0.52), 0.01, face, root)
        for x in (-0.32, 0.32):
            C.tube("leg", [(x, 0.06, z0 + 0.2), (x * 1.15, 0.0, 0.0)], 0.02, sm, root)
        C.tube("back", [(0, 0.07, z0 + 0.2), (0, 0.36, 0.0)], 0.02, sm, root)
        C.rounded_box("tray", (0, -0.04, z0 - 0.34), (0.78, 0.08, 0.03), 0.012, sm, root)
        W, H = 0.66, 0.46
    else:
        z0 = 1.05
        C.rounded_box("face", (0, 0.0, z0), (0.74, 0.03, 0.5), 0.15, face, root)
        for k in range(9):
            a = k * 6.2832 / 9
            C.sphere("puff", (math.cos(a) * 0.4, 0.02, z0 + math.sin(a) * 0.29), (0.12, 0.03, 0.1), fm, root, 20)
        for k, (x, z, q) in enumerate(((0.05, z0 - 0.4, 0.06), (0.1, z0 - 0.52, 0.04), (0.14, z0 - 0.6, 0.028))):
            C.sphere("tail", (x, 0.01, z), (q, q * 0.5, q), fm, root, 16)
        W, H = 0.62, 0.4
    scr = C.empty("screen", root, (0, -0.03, z0))
    return scr, W, H


def tiny_shoes(r, s, fam, root):
    c, d = [_rich(x, 1.4, 0.95) for x in _cols(r, fam, 2)]
    um = M(c, rough=0.45, coat=0.5)
    sm = M((0.97, 0.95, 0.9), rough=0.55, coat=0.2)
    lm = M(d, rough=0.5, coat=0.3)
    for sx in (-1, 1):
        o = C.empty("shoe", root, (sx * 0.045, 0, 0), (0, 0, math.radians(sx * 6)))
        if s == 0:
            C.rounded_box("sole", (0, 0, 0.008), (0.05, 0.1, 0.016), 0.007, sm, o)
            C.sphere("toe", (0, -0.028, 0.022), (0.026, 0.035, 0.02), um, o, 20)
            C.rounded_box("heel", (0, 0.018, 0.03), (0.048, 0.056, 0.036), 0.016, um, o)
            for k in range(2):
                C.tube("lace", [(-0.016, -0.01 + k * 0.014, 0.046), (0.016, -0.01 + k * 0.014, 0.046)], 0.003, lm, o)
        elif s == 1:
            C.rounded_box("sole", (0, 0, 0.008), (0.052, 0.1, 0.016), 0.007, lm, o)
            C.sphere("toe", (0, -0.028, 0.024), (0.027, 0.034, 0.022), um, o, 20)
            C.rounded_box("shaft", (0, 0.015, 0.05), (0.048, 0.052, 0.08), 0.02, um, o)
            C.tube("cuff", [(math.cos(k * 6.2832 / 24) * 0.026, 0.015 + math.sin(k * 6.2832 / 24) * 0.028, 0.09) for k in range(25)], 0.006, sm, o)
        else:
            C.rounded_box("sole", (0, 0, 0.012), (0.05, 0.098, 0.024), 0.01, um, o)
            C.tube("strap", [(-0.024, -0.02, 0.022), (-0.012, -0.02, 0.042), (0.012, -0.02, 0.042), (0.024, -0.02, 0.022)], 0.006, lm, o)
            C.tube("band", [(-0.024, 0.03, 0.022), (0, 0.03, 0.04), (0.024, 0.03, 0.022)], 0.005, lm, o)
            C.sphere("bead", (0, -0.02, 0.046), (0.008,) * 3, sm, o, 10)


def time_clock(r, s, fam, root):
    c, d = [_rich(x, 1.3, 0.95) for x in _cols(r, fam, 2)]
    cm = M(c, rough=0.4, coat=0.6)
    dm = M(d, rough=0.45, coat=0.5)
    face = M((0.98, 0.97, 0.92), rough=0.5, coat=0.3, emit=0.12)
    ink = M((0.15, 0.18, 0.3), rough=0.4, coat=0.5)
    if s == 0:
        R, z0, fy = 0.16, 0.2, 0.0
        C.tube("rim", [(math.cos(k * 6.2832 / 56) * R, 0, z0 + math.sin(k * 6.2832 / 56) * R) for k in range(57)], 0.03, cm, root)
        for sx in (-1, 1):
            C.sphere("foot", (sx * 0.1, 0.0, 0.025), (0.035, 0.035, 0.03), dm, root, 16)
        C.sphere("knob", (0, 0, z0 + R + 0.035), (0.03, 0.03, 0.025), dm, root, 16)
    elif s == 1:
        R, z0, fy = 0.13, 0.19, -0.03
        C.rounded_box("case", (0, 0.03, 0.16), (0.36, 0.1, 0.32), 0.05, cm, root)
        C.sphere("arch", (0, 0.03, 0.31), (0.18, 0.05, 0.08), cm, root, 32)
        C.rounded_box("base", (0, 0.03, 0.015), (0.42, 0.14, 0.03), 0.012, dm, root)
    else:
        R, z0, fy = 0.17, 0.42, 0.0
        C.tube("rim", [(math.cos(k * 6.2832 / 56) * R, 0, z0 + math.sin(k * 6.2832 / 56) * R) for k in range(57)], 0.022, cm, root)
        C.tube("stem", [(0, 0.03, z0 - R), (0, 0.03, 0.03)], 0.02, dm, root)
        C.lathe("foot", [(0, 0.0), (0, 0.12), (0.02, 0.13), (0.035, 0.1), (0.04, 0.0)], dm, root, segs=40)
    dk = C.empty("dk", root, (0, fy + 0.006, z0), (math.radians(90), 0, 0))
    C.lathe("face", [(-0.008, 0.0), (-0.008, R), (0.008, R), (0.008, 0.0)], face, dk, segs=56)
    for k in range(12):
        a = k * 6.2832 / 12
        q = 0.012 if k % 3 == 0 else 0.007
        C.sphere("tick", (math.cos(a) * R * 0.8, fy - 0.006, z0 + math.sin(a) * R * 0.8), (q, 0.004, q), ink, root, 10)
    hm = C.empty("hand_m", root, (0, fy - 0.012, z0))
    C.tube("hm", [(0, 0, 0), (0, 0, R * 0.7)], 0.008, ink, hm)
    hh = C.empty("hand_h", root, (0, fy - 0.016, z0))
    C.tube("hh", [(0, 0, 0), (0, 0, R * 0.45)], 0.011, M(d, rough=0.4, coat=0.6), hh)
    C.sphere("pin", (0, fy - 0.02, z0), (0.016, 0.008, 0.016), dm, root, 12)
    return hm, hh


def water_tray(r, s, fam, root):
    c, d = [_rich(x, 1.25, 0.95) for x in _cols(r, fam, 2)]
    wm = MA((0.3, 0.6, 1.0), 0.78, rough=0.06, emit=0.15)
    ink = M(tuple(v * 0.45 for v in d), rough=0.4, coat=0.5)
    piv = C.empty("water_pivot", root, (0, 0, 0.0))
    if s == 0:
        R, h, b = 0.3, 0.07, 0.012
        C.lathe("dish", [(0.0, 0.0), (0.0, R * 0.85), (0.01, R * 0.95), (h, R), (h + 0.01, R - 0.008), (h, R - 0.02), (b, R * 0.85 - 0.015), (b, 0.0)], M(c, rough=0.35, coat=0.7), root, segs=64)
        piv.location = (0, 0, b)
        C.lathe("water", [(0.0, 0.0), (0.0, R * 0.86), (h - b - 0.012, R - 0.03), (h - b - 0.012, 0.0)], wm, piv, segs=56)
        C.tube("mark", _ring(R - 0.024, h - 0.012, 64), 0.006, ink, root)
        top = h - 0.012
    elif s == 1:
        W, D, h, t = 0.62, 0.36, 0.26, 0.012
        glass = MA((0.9, 0.96, 1.0), 0.2)
        for x in (-W / 2, W / 2):
            C.rounded_box("wall", (x, 0, h / 2), (t, D, h), 0.005, glass, root)
        for y in (-D / 2, D / 2):
            C.rounded_box("wall", (0, y, h / 2), (W, t, h), 0.005, glass, root)
        C.rounded_box("floor", (0, 0, t / 2), (W, D, t), 0.005, glass, root)
        C.tube("frame", [(-W / 2, -D / 2, h), (W / 2, -D / 2, h), (W / 2, D / 2, h), (-W / 2, D / 2, h), (-W / 2, -D / 2, h)], 0.01, M(c, rough=0.4, coat=0.6), root)
        C.rounded_box("base", (0, 0, -0.008), (W + 0.04, D + 0.04, 0.016), 0.006, M(d, rough=0.45, coat=0.5), root)
        piv.location = (0, 0, t)
        C.rounded_box("water", (0, 0, 0.5 * (h * 0.72)), (W - 2 * t - 0.004, D - 2 * t - 0.004, h * 0.72), 0.004, MA((0.35, 0.65, 1.0), 0.45, rough=0.05, emit=0.1), piv)
        C.tube("mark", [(-W / 2 + 0.03, -D / 2 - 0.008, t + h * 0.72), (-W / 2 + 0.1, -D / 2 - 0.008, t + h * 0.72)], 0.004, ink, root)
        top = t + h * 0.72
    else:
        R, h, b = 0.26, 0.08, 0.012
        C.lathe("dish", [(0.0, 0.0), (0.0, R * 0.8), (0.015, R * 0.92), (h, R), (h + 0.01, R - 0.008), (h, R - 0.02), (b, R * 0.8 - 0.015), (b, 0.0)], M(c, rough=0.35, coat=0.7), root, segs=64, sy=0.7)
        for sx in (-1, 1):
            C.tube("handle", [(sx * (R - 0.01), 0, h * 0.7), (sx * (R + 0.05), 0, h * 0.8), (sx * (R + 0.05), 0, h * 0.6), (sx * (R - 0.005), 0, h * 0.4)], 0.012, M(d, rough=0.4, coat=0.6), root)
        piv.location = (0, 0, b)
        C.lathe("water", [(0.0, 0.0), (0.0, R * 0.81), (h - b - 0.012, R - 0.03), (h - b - 0.012, 0.0)], wm, piv, segs=56, sy=0.7)
        C.tube("mark", _ring(R - 0.024, h - 0.012, 64, 0.7), 0.006, ink, root)
        top = h - 0.012
    return piv, top


def ring_fence(r, s, fam, root):
    c, d = [_rich(x, 1.3, 0.95) for x in _cols(r, fam, 2)]
    pm = M(c, rough=0.45, coat=0.5)
    rm = M(d, rough=0.45, coat=0.5)
    R = 0.38
    n = [14, 10, 18][s]
    for i in range(n):
        a = i * 6.2832 / n
        x, y = math.cos(a) * R, math.sin(a) * R * 0.75
        if s == 0:
            C.rounded_box("pk", (x, y, 0.07), (0.035, 0.014, 0.14), 0.01, pm, root).rotation_euler = (0, 0, a + 1.5708)
            C.sphere("tip", (x, y, 0.145), (0.018, 0.008, 0.016), pm, root, 10)
        elif s == 1:
            C.tube("post", [(x, y, 0.0), (x, y, 0.13)], 0.013, pm, root)
            C.sphere("cap", (x, y, 0.138), (0.02, 0.02, 0.016), rm, root, 12)
        else:
            C.tube("bar", [(x, y, 0.0), (x, y, 0.11)], 0.008, pm, root)
    hz = [(0.045, 0.11), (0.06, 0.11), (0.05, 0.1)][s]
    for z in hz:
        C.tube("rail", _ring(R, z, 64, 0.75), 0.008 if s != 1 else 0.006, rm, root)
    return R


def float_item(r, s, fam, root):
    if s == 0:
        cm = M((0.82, 0.6, 0.36), rough=0.85, coat=0.05)
        C.lathe("cork", [(0.0, 0.0), (0.0, 0.055), (0.006, 0.062), (0.064, 0.064), (0.07, 0.058), (0.07, 0.0)], cm, root, segs=40)
        pm = M((0.55, 0.36, 0.2), rough=0.9)
        for k in range(14):
            a = k * 2.39
            rr = 0.012 + 0.035 * ((k * 7) % 10) / 10
            C.sphere("pore", (math.cos(a) * rr, math.sin(a) * rr, 0.07), (0.006, 0.006, 0.002), pm, root, 8)
        for k in range(10):
            a = k * 0.63
            C.sphere("pore", (math.cos(a) * 0.063, math.sin(a) * 0.063, 0.015 + 0.04 * ((k * 3) % 5) / 5), (0.005, 0.005, 0.005), pm, root, 8)
        return 0.07
    if s == 1:
        c = _rich(_cols(r, fam, 1)[0], 0.4, 0.62)
        C.sphere("stone", (0, 0, 0.034), (0.075, 0.062, 0.036), M(c, rough=0.3, coat=0.5), root, 40)
        C.sphere("fleck", (0.03, -0.03, 0.05), (0.012, 0.008, 0.004), M(tuple(min(1, v * 1.3) for v in c), rough=0.3, coat=0.5), root, 10)
        return 0.068
    wm = M((0.92, 0.72, 0.45), rough=0.6, coat=0.2)
    C.rounded_box("block", (0, 0, 0.03), (0.13, 0.08, 0.06), 0.012, wm, root)
    gm = M((0.75, 0.52, 0.3), rough=0.7)
    for z in (0.018, 0.034, 0.048):
        C.tube("grain", [(-0.06, -0.041, z), (-0.02, -0.041, z + 0.004), (0.02, -0.041, z - 0.003), (0.06, -0.041, z)], 0.0025, gm, root)
    return 0.06


def boat_sticker(r, s, fam, root):
    c, d = [_rich(x, 1.4, 0.95) for x in _cols(r, fam, 2)]
    base = M((0.99, 0.98, 0.95), rough=0.4, coat=0.6)
    if s == 0:
        C.lathe("disc", [(0.0, 0.0), (0.0, 0.045), (0.003, 0.046), (0.003, 0.0)], base, root, segs=40)
    elif s == 1:
        C.rounded_box("disc", (0, 0, 0.0015), (0.09, 0.07, 0.003), 0.001, base, root)
    else:
        for k in range(6):
            a = k * 6.2832 / 6
            C.sphere("lobe", (math.cos(a) * 0.026, math.sin(a) * 0.026, 0.0015), (0.022, 0.022, 0.0015), base, root, 16)
        C.sphere("mid", (0, 0, 0.0015), (0.03, 0.03, 0.0015), base, root, 16)
    C.rounded_box("hull", (0, -0.012, 0.004), (0.05, 0.016, 0.002), 0.004, M(c, rough=0.4, coat=0.5), root)
    C.tube("mast", [(0.0, -0.004, 0.0045), (0.0, 0.03, 0.0045)], 0.002, M((0.4, 0.3, 0.25), rough=0.5), root)
    C.rounded_box("sail", (0.011, 0.014, 0.004), (0.018, 0.028, 0.002), 0.003, M(d, rough=0.4, coat=0.5), root)


def gourd_trio(r, s, fam, root):
    cs = colors(r, "autumn", 3)
    base = [(0.88, 0.45, 0.14), (0.96, 0.82, 0.55), (0.62, 0.7, 0.5)]
    stem = M((0.33, 0.42, 0.22), rough=0.6, coat=0.1)
    if s == 0:
        spec = [(0.0, 0.0, 0.2, 0.75), (0.26, 0.06, 0.13, 0.85), (-0.24, 0.05, 0.11, 0.9)]
    elif s == 1:
        spec = [(0.0, 0.0, 0.15, 1.35), (0.2, -0.02, 0.12, 1.0)]
    else:
        spec = [(0.0, 0.0, 0.19, 0.62), (0.03, 0.01, 0.12, 0.75, 1), (0.25, -0.03, 0.09, 0.85)]
    z0 = 0.0
    for i, sp in enumerate(spec):
        x, y, rad, sq = sp[:4]
        z = z0 + rad * sq if len(sp) < 5 else spec[0][2] * spec[0][3] * 2 + rad * sq * 0.85
        col = tuple(0.7 * a + 0.3 * b for a, b in zip(base[i % 3], cs[i % 3]))
        for k in range(8):
            a = k * 6.2832 / 8
            C.sphere("rib", (x + math.cos(a) * rad * 0.42, y + math.sin(a) * rad * 0.42, z), (rad * 0.62, rad * 0.62, rad * sq), M(col, rough=0.45, coat=0.35), root, 20)
        C.tube("stem", [(x, y, z + rad * sq * 0.85), (x + 0.012, y, z + rad * sq * 0.85 + 0.07)], 0.016, stem, root)


def led_lantern(r, s, fam, root):
    c, d = colors(r, "autumn", 2)
    glow = M((1.0, 0.82, 0.45), rough=0.3, coat=0.2, emit=2.0)
    frame = M(c, rough=0.4, coat=0.5)
    if s == 0:
        C.rounded_box("base", (0, 0, 0.02), (0.2, 0.2, 0.04), 0.012, frame, root)
        C.rounded_box("glass", (0, 0, 0.15), (0.16, 0.16, 0.22), 0.03, MA((1.0, 0.9, 0.7), 0.35), root)
        C.sphere("led", (0, 0, 0.14), (0.04, 0.04, 0.06), glow, root, 16)
        C.rounded_box("roof", (0, 0, 0.28), (0.22, 0.22, 0.04), 0.015, frame, root)
        C.lathe("cap", [(0.3, 0), (0.3, 0.06), (0.35, 0.0)], frame, root, segs=24)
        C.tube("loop", [(-0.04, 0, 0.35), (0, 0, 0.39), (0.04, 0, 0.35)], 0.008, frame, root)
    elif s == 1:
        C.lathe("foot", [(0, 0), (0, 0.09), (0.03, 0.08), (0.03, 0)], frame, root, segs=32)
        C.sphere("globe", (0, 0, 0.13), (0.11, 0.11, 0.1), MA((1.0, 0.92, 0.75), 0.4), root, 28)
        C.sphere("led", (0, 0, 0.12), (0.035,) * 3, glow, root, 16)
        C.lathe("top", [(0.22, 0), (0.22, 0.05), (0.25, 0.035), (0.255, 0)], M(d, rough=0.4, coat=0.5), root, segs=24)
    else:
        C.lathe("jar", [(0, 0), (0, 0.08), (0.12, 0.09), (0.2, 0.06), (0.2, 0)], MA((0.95, 0.92, 0.85), 0.3), root, segs=32)
        for k in range(5):
            a = k * 1.25
            C.sphere("bead", (math.cos(a) * 0.045, math.sin(a) * 0.045, 0.05 + k * 0.025), (0.016,) * 3, glow, root, 10)
        C.lathe("lid", [(0.2, 0), (0.2, 0.065), (0.23, 0.065), (0.23, 0)], frame, root, segs=32)


def hay_seat(r, s, fam, root):
    c = colors(r, "autumn", 2)[1]
    hay = M(tuple(0.6 * a + 0.4 * b for a, b in zip((0.93, 0.78, 0.45), c)), rough=0.85, coat=0.05)
    band = M((0.55, 0.32, 0.2), rough=0.6, coat=0.1)
    if s == 0:
        C.rounded_box("bale", (0, 0, 0.13), (0.5, 0.3, 0.26), 0.05, hay, root)
        for x in (-0.13, 0.13):
            C.rounded_box("band", (x, 0, 0.13), (0.025, 0.31, 0.27), 0.01, band, root)
    elif s == 1:
        C.lathe("roll", [(0, 0), (0, 0.2), (0.12, 0.22), (0.24, 0.2), (0.24, 0)], hay, root, segs=40)
        C.lathe("ring", [(0.1, 0.215), (0.12, 0.225), (0.14, 0.215)], band, root, segs=40)
    else:
        C.rounded_box("low", (0, 0, 0.09), (0.56, 0.32, 0.18), 0.05, hay, root)
        C.rounded_box("up", (0.06, 0.02, 0.26), (0.36, 0.26, 0.16), 0.05, hay, root)
        C.rounded_box("band", (0, 0, 0.09), (0.57, 0.025, 0.19), 0.01, band, root)

def date_card(r, s, fam, root, label=("31", "OCT")):
    c, d, e = [_rich(x, 1.2, 0.95) for x in _cols(r, fam, 3)]
    paper = M((0.97, 0.94, 0.88), rough=0.55, coat=0.3)
    band = M(_rich(c, 1.5, 0.78), rough=0.4, coat=0.6)
    trim = M(d, rough=0.45, coat=0.5)
    ink = M((0.16, 0.18, 0.26), rough=0.35, coat=0.5)
    face = C.empty("face", root, (0, 0, 0))
    if s == 0:
        C.rounded_box("foot", (0, 0.02, 0.025), (0.36, 0.2, 0.05), 0.02, trim, root)
        C.rounded_box("pad", (0, 0, 0.24), (0.34, 0.06, 0.38), 0.03, paper, face)
        C.rounded_box("head", (0, -0.002, 0.405), (0.345, 0.065, 0.08), 0.03, band, face)
        for x in (-0.09, 0.0, 0.09):
            C.tube("coil", [(x, -0.035, 0.43), (x, -0.045, 0.47), (x, 0.0, 0.49), (x, 0.035, 0.46)], 0.01, M((0.8, 0.8, 0.84), rough=0.3), face)
        glyph(label[0], 0.19, 0.012, ink, face, (0, -0.034, 0.23))
        glyph(label[1], 0.06, 0.008, M((0.97, 0.94, 0.88), rough=0.4), face, (0, -0.036, 0.4))
    elif s == 1:
        tent = C.empty("tent", face, (0, 0, 0))
        for k, sy in enumerate((-1, 1)):
            C.rounded_box(f"leaf{k}", (0, sy * 0.06, 0.17), (0.36, 0.018, 0.36), 0.04, paper if sy < 0 else band, tent).rotation_euler = (math.radians(sy * 14), 0, 0)
        C.tube("ridge", [(-0.17, 0, 0.345), (0.17, 0, 0.345)], 0.016, trim, tent)
        f = C.empty("front", tent, (0, -0.062, 0.17), (math.radians(-14), 0, 0))
        C.rounded_box("strip", (0, -0.012, 0.11), (0.3, 0.004, 0.06), 0.012, band, f)
        glyph(label[0], 0.15, 0.01, ink, f, (0, -0.016, -0.02))
        glyph(label[1], 0.05, 0.007, M((0.97, 0.94, 0.88), rough=0.4), f, (0, -0.018, 0.11))
    else:
        C.lathe("base", [(0, 0.0), (0, 0.16), (0.012, 0.175), (0.035, 0.17), (0.045, 0.14), (0.045, 0.0)], trim, root, segs=48, sy=0.6)
        arch = C.empty("arch", face, (0, 0, 0.045))
        pts = [(-0.15, 0.0), (0.15, 0.0)] + [(0.15 * math.cos(math.pi * k / 16), 0.27 + 0.15 * math.sin(math.pi * k / 16)) for k in range(17)]
        bm = bmesh.new()
        vs = [bm.verts.new((x, 0.0, z)) for x, z in pts]
        fc = bm.faces.new(vs)
        ext = bmesh.ops.extrude_face_region(bm, geom=[fc])
        for v in [x for x in ext["geom"] if isinstance(x, bmesh.types.BMVert)]:
            v.co.y += 0.05
        for v in bm.verts:
            v.co.y -= 0.025
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        o = C.mesh_obj("archb", bm, paper, arch, smooth=False)
        b = o.modifiers.new("bev", "BEVEL")
        b.width = 0.012
        b.segments = 3
        C.sphere("gem", (0, -0.03, 0.36), (0.03, 0.012, 0.03), M(e, coat=0.8), arch, 16)
        C.tube("rim", [(0.15 * math.cos(math.pi * k / 24), -0.027, 0.27 + 0.15 * math.sin(math.pi * k / 24)) for k in range(25)], 0.01, band, arch)
        glyph(label[0], 0.16, 0.01, ink, arch, (0, -0.03, 0.15))
        glyph(label[1], 0.06, 0.008, M(tuple(v * 0.35 for v in _rich(c, 1.5, 0.8)), rough=0.4), arch, (0, -0.03, 0.285))
    return face


def _slab(name, pts, depth, m, root, z=0.0, bev=0.02):
    bm = bmesh.new()
    vs = [bm.verts.new((x, y, z)) for x, y in pts]
    fc = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[fc])
    for v in [x for x in ext["geom"] if isinstance(x, bmesh.types.BMVert)]:
        v.co.z += depth
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = C.mesh_obj(name, bm, m, root, smooth=False)
    b = o.modifiers.new("bev", "BEVEL")
    b.width = bev
    b.segments = 4
    b.limit_method = "ANGLE"
    return o


def leaf_pad(r, s, fam, root):
    from props.select import tint
    c = tint(r.choice([(0.86, 0.45, 0.16), (0.78, 0.32, 0.15), (0.92, 0.64, 0.22), (0.6, 0.62, 0.3)]), r, 0.03)
    d = (0.45, 0.28, 0.18)
    lm = M(c, rough=0.5, coat=0.5)
    vm = M(tuple(min(1, v * 0.55 + 0.42) for v in c), rough=0.45, coat=0.5)
    R = 0.5
    n = 96
    if s == 0:
        pts = []
        for k in range(n):
            t = 2 * math.pi * k / n
            rr = R * (0.8 + 0.2 * math.cos(5 * t)) * (1.0 + 0.12 * math.sin(t))
            pts.append((rr * math.cos(t), rr * math.sin(t) * 0.9))
        tip = (0.0, R * 1.0)
    elif s == 1:
        pts = []
        for k in range(n):
            t = 2 * math.pi * k / n
            x = R * 0.62 * math.sin(t) * (1 - 0.25 * math.cos(t))
            y = -R * 1.05 * math.cos(t)
            pts.append((x, y))
        pts = pts[::-1]
        tip = (0.0, R * 1.05)
    else:
        pts = []
        for k in range(n):
            t = 0.22 + (2 * math.pi - 0.44) * k / (n - 1)
            pts.append((R * math.sin(t), R * math.cos(t)))
        pts.append((0.0, R * 0.35))
        pts = pts[::-1]
        tip = (0.0, -R)
    o = _slab("pad", pts, 0.06, lm, root)
    z = 0.065
    if s == 2:
        for k in range(7):
            a = math.pi + (k - 3) * 0.42
            C.tube("vein", [(0, R * 0.2, z), (R * 0.8 * math.sin(a), R * 0.2 + R * 0.8 * math.cos(a), z)], 0.008, vm, root)
    else:
        C.tube("mid", [(0, -tip[1] * 0.85, z), (0, tip[1] * 0.8, z)], 0.011, vm, root)
        for k in range(3):
            y0 = -tip[1] * 0.5 + k * tip[1] * 0.45
            for sx in (-1, 1):
                C.tube("vein", [(0, y0, z), (sx * R * 0.38, y0 + R * 0.25, z)], 0.008, vm, root)
        C.tube("stem", [(0, -tip[1] * 0.85, 0.03), (0.03, -tip[1] * 1.12, 0.03), (0.08, -tip[1] * 1.22, 0.05)], 0.02, M(d, rough=0.5, coat=0.4), root)
    return 0.065


def _face(root):
    return C.empty("face", root, (0, 0, 0), (math.radians(90), 0, 0))


def hand_fan(r, s, fam, root):
    c, d = [_rich(x, 1.3, 0.95) for x in _cols(r, fam, 2)]
    fm = M(c, rough=0.45, coat=0.5)
    sm = M(d, rough=0.4, coat=0.6)
    lm = M(tuple(min(1, v * 0.5 + 0.5) for v in c), rough=0.5, coat=0.4)
    C.tube("grip", [(0, 0, 0.0), (0, 0, 0.2)], 0.018, sm, root)
    C.sphere("cap", (0, 0, 0.0), (0.024, 0.024, 0.02), sm, root, 16)
    f = _face(root)
    if s == 0:
        n, R, a0 = 9, 0.3, math.radians(-70)
        for k in range(n):
            t0 = a0 + k * math.radians(140) / n
            t1 = a0 + (k + 1) * math.radians(140) / n
            pts = [(0.06 * math.sin(t0), 0.2 + 0.06 * math.cos(t0)), (R * math.sin(t0), 0.2 + R * math.cos(t0)),
                   (R * math.sin(t1), 0.2 + R * math.cos(t1)), (0.06 * math.sin(t1), 0.2 + 0.06 * math.cos(t1))]
            _slab("pleat", pts, 0.012, fm if k % 2 else lm, f, z=-0.006 + (0.004 if k % 2 else 0), bev=0.004)
        for k in range(n + 1):
            t = a0 + k * math.radians(140) / n
            C.tube("rib", [(0.0, 0, 0.2), (R * 0.98 * math.sin(t), -0.012, 0.2 + R * 0.98 * math.cos(t))], 0.006, sm, root)
        C.sphere("pin", (0, -0.016, 0.2), (0.022, 0.012, 0.022), sm, root, 16)
    elif s == 1:
        R = 0.17
        pts = [(R * math.cos(2 * math.pi * k / 64), 0.4 + R * math.sin(2 * math.pi * k / 64)) for k in range(64)]
        _slab("disc", pts, 0.022, fm, f, z=-0.011, bev=0.008)
        C.tube("rim", [(R * math.cos(2 * math.pi * k / 64), -0.014, 0.4 + R * math.sin(2 * math.pi * k / 64)) for k in range(65)], 0.009, sm, root)
        C.tube("stick", [(0, 0, 0.2), (0, 0, 0.26)], 0.02, sm, root)
        for k in range(5):
            a = 2 * math.pi * k / 5 + 0.3
            C.sphere("dot", (0.09 * math.cos(a), -0.013, 0.4 + 0.09 * math.sin(a)), (0.022, 0.006, 0.022), lm, root, 16)
    else:
        pts = []
        for k in range(96):
            t = 2 * math.pi * k / 96
            rr = 0.15 * (1 + 0.14 * math.cos(6 * t))
            pts.append((rr * math.cos(t) * 1.15, 0.4 + rr * math.sin(t)))
        _slab("cloud", pts, 0.024, fm, f, z=-0.012, bev=0.008)
        C.tube("stick", [(0, 0, 0.2), (0, 0, 0.27)], 0.02, sm, root)
        C.tube("vein", [(-0.1, -0.014, 0.4), (0.1, -0.014, 0.4)], 0.006, lm, root)
        C.tube("vein", [(0, -0.014, 0.3), (0, -0.014, 0.5)], 0.006, lm, root)
    return 0.4


def pinwheel(r, s, fam, root):
    cs = [_rich(x, 1.3, 0.95) for x in _cols(r, fam, 3)]
    sm = M((0.96, 0.94, 0.9), rough=0.45, coat=0.4)
    hm = M(cs[0], rough=0.35, coat=0.7)
    H = 0.55
    if s == 2:
        C.lathe("base", [(0, 0.0), (0, 0.13), (0.03, 0.14), (0.06, 0.1), (0.07, 0.0)], M(cs[1], rough=0.45, coat=0.5), root, segs=40)
        C.tube("post", [(0, 0, 0.06), (0, 0, H)], 0.022, M(cs[1], rough=0.45, coat=0.5), root)
    else:
        C.tube("stick", [(0, 0, 0), (0, 0, H)], 0.014, sm, root)
    hub = C.empty("rotor", root, (0, -0.045, H), (math.radians(90), 0, 0))
    if s == 0:
        for k in range(4):
            a = k * math.pi / 2
            m = M(cs[k % 3], rough=0.45, coat=0.5)
            bl = C.empty("bl", hub, (0, 0, 0), (0, 0, a))
            _slab("blade", [(0.02, 0.0), (0.2, 0.0), (0.2, 0.2), (0.05, 0.05)], 0.01, m, bl, z=-0.005, bev=0.004)
            bl.rotation_euler = (0, math.radians(14), a)
    elif s == 1:
        for k in range(6):
            a = k * math.pi / 3
            m = M(cs[k % 3], rough=0.45, coat=0.5)
            bl = C.empty("bl", hub, (0, 0, 0), (0, math.radians(18), a))
            pts = []
            for j in range(40):
                t = 2 * math.pi * j / 40
                pts.append((0.1 + 0.085 * math.cos(t), 0.045 * math.sin(t)))
            _slab("petal", pts, 0.012, m, bl, z=-0.006, bev=0.005)
    else:
        for k in range(3):
            a = k * 2 * math.pi / 3
            m = M(cs[k % 3], rough=0.45, coat=0.5)
            bl = C.empty("bl", hub, (0, 0, 0), (math.radians(16), 0, a))
            C.tube("arm", [(0.02, 0, 0), (0.08, 0, 0)], 0.01, sm, bl)
            C.rounded_box("paddle", (0.15, 0, 0), (0.15, 0.08, 0.016), 0.006, m, bl)
    C.sphere("cap", (0, 0, 0.012), (0.03, 0.03, 0.022), hm, hub, 20)
    return hub


GEN = {k: v for k, v in globals().items() if k in REGISTRY}


def spawn(name, style=0, seed=0, family="pastel", loc=(0, 0, 0), scale=1.0, rot=0.0, parent=None, **kw):
    root = C.empty(f"prop_{name}", parent, loc, (0, 0, math.radians(rot)))
    GEN[name](random.Random(seed), style, family, root, **kw)
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
