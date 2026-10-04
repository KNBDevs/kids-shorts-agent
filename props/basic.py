import math
import bpy, bmesh
from mathutils import Vector
import common as C


def prism(name, n, R, depth, material, parent=None, bevel=0.03):
    bm = bmesh.new()
    vs = []
    for k in range(n):
        a = -math.pi / 2 - math.pi / n + 2 * math.pi * k / n
        vs.append(bm.verts.new((R * math.cos(a), -depth / 2, R * math.sin(a))))
    f = bm.faces.new(vs[::-1])
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in [e for e in ext['geom'] if isinstance(e, bmesh.types.BMVert)]:
        v.co.y += depth
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = C.mesh_obj(name, bm, material, parent, smooth=False)
    if bevel:
        b = o.modifiers.new('bev', 'BEVEL')
        b.width = bevel
        b.segments = 4
        b.limit_method = 'ANGLE'
    o.data.polygons.foreach_set('use_smooth', [len(pl.vertices) == 4 for pl in o.data.polygons])
    return o


def disc(name, R, depth, material, parent=None, bevel=0.025):
    return prism(name, 64, R, depth, material, parent, bevel)


def wheel(name, n, R, parent, loc, rim, hub):
    piv = C.empty(name, parent, loc)
    if n == 0:
        prism(name + '.m', 64, R, 0.09, rim, piv)
    else:
        prism(name + '.m', n, R, 0.09, rim, piv, bevel=0.035)
    C.sphere(name + '.hub', (0, -0.055, 0), (0.045, 0.02, 0.045), hub, piv, 20)
    return piv


def cart(name, body_rgb, rim_rgb, loc=(0, 0, 0)):
    root = C.empty(name, None, loc)
    body_m = C.mat(name + '_body', body_rgb, rough=0.35, coat=0.4)
    trim_m = C.mat(name + '_trim', (1.0, 0.95, 0.85), rough=0.4, coat=0.3)
    C.rounded_box(name + '.body', (0, 0, 0.2), (0.95, 0.6, 0.2), 0.06, body_m, root)
    C.rounded_box(name + '.rim', (0, 0, 0.31), (1.0, 0.65, 0.05), 0.02, trim_m, root)
    handle = C.tube(name + '.handle', [(-0.46, 0, 0.3), (-0.62, 0, 0.5), (-0.66, 0, 0.56)], 0.025, trim_m, root)
    return root, handle


def apple(name, parent, loc, r=0.11):
    g = C.empty(name, parent, loc)
    red = C.mat(name + '_red', (0.85, 0.06, 0.05), rough=0.3, coat=0.6)
    grn = C.mat(name + '_leaf', (0.15, 0.6, 0.15), rough=0.5)
    brn = C.mat(name + '_stem', (0.35, 0.2, 0.08), rough=0.7)
    C.lathe(name + '.m', [(0.0, 0.0), (0.05 * r, 0.5 * r), (0.4 * r, 0.95 * r), (0.95 * r, 1.0 * r), (1.5 * r, 0.82 * r), (1.72 * r, 0.32 * r), (1.62 * r, 0.0)], red, g, segs=48)
    C.tube(name + '.stem', [(0, 0, 1.6 * r), (0.02 * r, 0, 2.1 * r), (0.1 * r, 0, 2.4 * r)], 0.07 * r, brn, g)
    lf = C.empty(name + '.lp', g, (0.06 * r, 0, 2.05 * r), (0, math.radians(60), 0))
    C.leaf(name + '.leaf', 0.6 * r, 0.25 * r, 0.05 * r, grn, lf, thick=0.01)
    return g


def shake_cup(name, parent, loc, r=0.1):
    g = C.empty(name, parent, loc)
    glass = C.mat(name + '_cup', (1.0, 0.72, 0.82), rough=0.25, coat=0.8)
    pink = C.mat(name + '_pink', (0.95, 0.25, 0.55), rough=0.35, coat=0.3)
    straw = C.mat(name + '_straw', (0.3, 0.75, 1.0), rough=0.3)
    C.lathe(name + '.cup', [(0.0, 0.0), (0.0, 0.7 * r), (0.6 * r, 0.75 * r), (2.0 * r, 1.0 * r), (2.6 * r, 1.08 * r)], glass, g, segs=48)
    C.lathe(name + '.milk', [(0.05 * r, 0.0), (0.1 * r, 0.65 * r), (1.8 * r, 0.93 * r), (2.25 * r, 0.96 * r), (2.3 * r, 0.0)], pink, g, segs=48)
    C.sphere(name + '.foam', (0, 0, 2.35 * r), (0.95 * r, 0.95 * r, 0.45 * r), pink, g, 32)
    C.tube(name + '.straw', [(0.2 * r, 0, 1.5 * r), (0.4 * r, 0, 3.4 * r), (0.9 * r, 0, 3.9 * r)], 0.12 * r, straw, g)
    return g, pink


def anim_color(m, f, rgb):
    inp = m.node_tree.nodes['Principled BSDF'].inputs['Base Color']
    inp.default_value = (*rgb, 1)
    inp.keyframe_insert('default_value', frame=f)


def flower_head(name, parent, loc, r, petal_m, center_m, n=8):
    g = C.empty(name, parent, loc)
    C.sphere(name + '.center', (0, -0.02 * r, 0), (0.42 * r, 0.25 * r, 0.42 * r), center_m, g, 24)
    for k in range(n):
        a = 2 * math.pi * k / n
        C.sphere(f'{name}.petal.{k}', (0.72 * r * math.cos(a), 0.02 * r, 0.72 * r * math.sin(a)), (0.42 * r, 0.1 * r, 0.24 * r), petal_m, g, 20,
                 rot=(0, -a, 0))
    return g


def potted_flower(name, loc, petal_m, h=0.85):
    root = C.empty(name, None, loc)
    pot = C.mat(name + '_pot', (0.75, 0.32, 0.18), rough=0.6)
    soil = C.mat(name + '_soil', (0.25, 0.14, 0.08), rough=0.9)
    green = C.mat(name + '_green', (0.15, 0.55, 0.18), rough=0.5)
    center = C.mat(name + '_center', (0.55, 0.28, 0.06), rough=0.6)
    C.lathe(name + '.pot', [(0.0, 0.0), (0.0, 0.11), (0.2, 0.15), (0.24, 0.17), (0.27, 0.17), (0.27, 0.0)], pot, root, segs=48)
    C.sphere(name + '.soil', (0, 0, 0.245), (0.15, 0.15, 0.02), soil, root, 24)
    top = h - 0.15
    C.tube(name + '.stem', [(0, 0, 0.25), (0.02, 0, 0.45), (-0.01, 0, top - 0.05), (0, 0, top)], 0.018, green, root)
    for sx, z in ((-1, 0.38), (1, 0.48)):
        lp = C.empty(f'{name}.lp{sx}', root, (0, 0, z), (0, math.radians(sx * 70), 0))
        C.leaf(f'{name}.leaf{sx}', 0.16, 0.06, 0.02, green, lp, thick=0.012)
    head = flower_head(name + '.head', root, (0, -0.02, top), 0.15, petal_m, center)
    return root, head


def banana(name, parent, loc, m, L=0.55):
    g = C.empty(name, parent, loc)
    tip = C.mat(name + '_tip', (0.3, 0.2, 0.08), rough=0.7)
    pts = []
    for k in range(13):
        t = -1 + 2 * k / 12
        pts.append((t * L * 0.5, 0, 0.16 * L * (t * t)))
    radii = [0.3 + 0.7 * math.sin(math.pi * k / 12) ** 0.6 for k in range(13)]
    C.tube(name + '.m', pts, 0.085 * L, m, g, radii=radii, res=8)
    for e in (pts[0], pts[-1]):
        C.sphere(name + '.tip', e, (0.025 * L, 0.025 * L, 0.025 * L), tip, g, 12)
    return g


def color_vacuum(name, loc):
    root = C.empty(name, None, loc)
    lime = C.mat(name + '_body', (0.45, 0.65, 0.04), rough=0.4, coat=0.4)
    purple = C.mat(name + '_trim', (0.3, 0.08, 0.5), rough=0.5, coat=0.3)
    orange = C.mat(name + '_nozzle', (0.95, 0.3, 0.04), rough=0.4, coat=0.3)
    fill_m = C.mat(name + '_fill', (1.0, 0.82, 0.05), rough=0.3, emit=0.3)
    C.rounded_box(name + '.body', (0, 0, 0.3), (0.62, 0.46, 0.38), 0.07, lime, root)
    for sx in (-1, 1):
        for sy in (-1, 1):
            C.sphere(f'{name}.wheel', (sx * 0.24, sy * 0.17, 0.08), (0.08, 0.06, 0.08), purple, root, 20)
    for k, col in enumerate(((0.95, 0.3, 0.04), (0.25, 0.75, 0.45))):
        C.sphere(f'{name}.btn{k}', (-0.12 + 0.24 * k, -0.235, 0.32), (0.045, 0.02, 0.045), C.mat(f'{name}_b{k}', col, rough=0.3), root, 16)
    tank = C.empty(name + '.tank', root, (0, 0.04, 0.49))
    C.lathe(name + '.base', [(0.0, 0.0), (0.0, 0.17), (0.04, 0.17), (0.05, 0.0)], purple, tank, segs=48)
    for k in range(3):
        a = 2 * math.pi * k / 3 + math.pi / 2
        C.tube(f'{name}.bar{k}', [(0.165 * math.cos(a), 0.165 * math.sin(a), 0.03), (0.165 * math.cos(a), 0.165 * math.sin(a), 0.38)], 0.012, purple, tank)
    C.lathe(name + '.cap', [(0.36, 0.0), (0.37, 0.17), (0.42, 0.17), (0.44, 0.0)], purple, tank, segs=48)
    lvl = C.empty(name + '.level', tank, (0, 0, 0.045))
    C.lathe(name + '.fill', [(0.0, 0.0), (0.0, 0.14), (1.0, 0.14), (1.0, 0.0)], fill_m, lvl, segs=48)
    lvl.scale = (1, 1, 0.001)
    arm = C.empty(name + '.arm', root, (0, -0.18, 0.42))
    C.tube(name + '.hose', [(0, 0, 0), (0, -0.2, 0.02), (0, -0.4, 0)], 0.045, purple, arm)
    C.lathe(name + '.cone', [(0.0, 0.05), (0.08, 0.09), (0.16, 0.13), (0.17, 0.0)], orange, C.empty(name + '.nz', arm, (0, -0.38, 0), (math.radians(90), 0, 0)), segs=32)
    return {'root': root, 'tank': tank, 'level': lvl, 'arm': arm, 'fill': fill_m}
