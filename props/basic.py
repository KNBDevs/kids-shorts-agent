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
