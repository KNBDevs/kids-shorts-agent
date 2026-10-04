import math
import bpy, bmesh
from mathutils import Vector
import common as C

PAL = {'ivory': (0.82, 0.74, 0.62), 'slate': (0.04, 0.06, 0.1), 'plum': (0.13, 0.08, 0.16), 'sage': (0.22, 0.29, 0.23),
       'pumpkin': (0.52, 0.18, 0.06), 'amber': (0.8, 0.5, 0.2), 'ghost': (0.9, 0.84, 0.77), 'web': (0.58, 0.61, 0.65),
       'ink': (0.03, 0.04, 0.06)}


def _eyes(prefix, parent, pts, a, b, look_y=-1.0):
    white = C.mat(prefix + '_ew', (0.98, 0.97, 0.95), rough=0.25)
    iris = C.mat(prefix + '_iris', (0.05, 0.03, 0.02), rough=0.3)
    shine = C.mat(prefix + '_shine', (1, 1, 1), emit=5.0)
    out = []
    for k, p in enumerate(pts):
        g = C.empty(f'{prefix}.eye.{k}', parent, p)
        C.sphere(f'{prefix}.eyew.{k}', (0, 0, 0), (a, a * 0.6, b), white, g, 24)
        C.sphere(f'{prefix}.pupil.{k}', (0, -a * 0.42, -b * 0.05), (a * 0.7, a * 0.3, b * 0.75), iris, g, 24)
        C.sphere(f'{prefix}.eshine.{k}', (-a * 0.25, -a * 0.68, b * 0.3), (a * 0.22, a * 0.06, b * 0.22), shine, g, 12)
        out.append(g)
    return out


def _smile(prefix, parent, cx, cy, cz, w, sag, r, m):
    pts = [(cx + t * w, cy - 0.002, cz - sag * (1 - t * t)) for t in [-1 + 2 * k / 8 for k in range(9)]]
    o = C.tube(prefix + '.mouth', pts, r, m, parent, radii=[0.6] + [1] * 7 + [0.6])
    return C.recenter_curve(o)


def spider(name='Seda', span=0.8):
    s = span / 0.8
    root = C.empty(name)
    body = C.empty(name + '.body', root, (0, 0, 0.16 * s))
    plum = C.mat(name + '_plum', (0.3, 0.22, 0.34), rough=0.5, sheen=0.4, coat=0.2)
    dark = C.mat(name + '_leg', (0.22, 0.16, 0.26), rough=0.55, sheen=0.3)
    accent = C.mat(name + '_dot', (0.7, 0.45, 0.75), rough=0.4)
    line = C.mat(name + '_line', (0.06, 0.03, 0.06), rough=0.6)
    blush = C.mat(name + '_blush', (0.9, 0.45, 0.6), rough=0.8)
    ceph = C.sphere(name + '.cephalothorax', (0, -0.08 * s, 0.02 * s), (0.13 * s, 0.12 * s, 0.11 * s), plum, body, 40)
    abd = C.empty(name + '.abdomen', body, (0, 0.1 * s, 0.07 * s))
    C.sphere(name + '.abdomen_mesh', (0, 0.06 * s, 0.03 * s), (0.17 * s, 0.19 * s, 0.16 * s), plum, abd, 40)
    for k, (x, y, z) in enumerate(((0.0, -0.02, 0.17), (-0.08, 0.04, 0.15), (0.08, 0.04, 0.15))):
        C.sphere(f'{name}.spot.{k}', (x * s, y * s + 0.06 * s, z * s), (0.03 * s, 0.03 * s, 0.015 * s), accent, abd, 16)
    spin = C.empty(name + '.spinneret', abd, (0, 0.24 * s, 0.0))
    eyes = _eyes(name, ceph, [(-0.045 * s, -0.1 * s, 0.045 * s), (0.045 * s, -0.1 * s, 0.045 * s)], 0.042 * s, 0.05 * s)
    for e in eyes:
        e.parent = body
        e.location = e.location + Vector((0, -0.08 * s, 0.02 * s))
    mouth = _smile(name, body, 0, -0.2 * s, -0.0 * s, 0.025 * s, 0.012 * s, 0.005 * s, line)
    for sx in (-1, 1):
        C.sphere(f'{name}.blush.{sx}', (sx * 0.085 * s, -0.175 * s, 0.0), (0.02 * s, 0.006 * s, 0.013 * s), blush, body, 12)
    legs = {}
    ang = [-62, -22, 18, 55]
    for side, sx in (('L', -1), ('R', 1)):
        for i, a in enumerate(ang):
            hip = Vector((sx * 0.08 * s, (-0.12 + 0.04 * i) * s, 0.0))
            piv = C.empty(f'{name}.leg_{side}_{i + 1}', body, tuple(hip))
            d = Vector((sx * math.cos(math.radians(a)), math.sin(math.radians(a)), 0))
            reach = (0.3 - 0.015 * abs(i - 1.5)) * s
            knee = d * reach * 0.45 + Vector((0, 0, 0.13 * s))
            foot = d * reach + Vector((0, 0, -0.155 * s))
            pts = C.catmull([(0, 0, 0), tuple(d * reach * 0.2 + Vector((0, 0, 0.07 * s))), tuple(knee), tuple(d * reach * 0.75 + Vector((0, 0, 0.02 * s))), tuple(foot)], 24)
            C.tube(f'{name}.legmesh_{side}_{i + 1}', pts, 0.016 * s, dark, piv, radii=[1.2] + [1.0] * (len(pts) - 2) + [0.8])
            C.sphere(f'{name}.toe_{side}_{i + 1}', tuple(foot), (0.022 * s,) * 3, dark, piv, 12)
            legs[f'leg_{side}_{i + 1}'] = piv
    return {'root': root, 'body': body, 'abdomen': abd, 'spinneret': spin, 'legs': legs, 'eyes': eyes, 'mouth': mouth,
            'height': 0.36 * s}


def ghost(name='Nubi', h=0.75):
    s = h / 0.75
    root = C.empty(name)
    rig = C.empty(name + '.rig', root)
    m = C.mat(name + '_body', PAL['ghost'], rough=0.55, sss=0.15, sheen=0.3)
    z0 = 0.12 * s
    prof = [(z0 + z * s, r * s) for z, r in [(0.02, 0.0), (0.0, 0.2), (0.04, 0.29), (0.2, 0.3), (0.38, 0.28), (0.52, 0.23), (0.61, 0.14), (0.64, 0.0)]]
    body = C.lathe(name + '.body', prof, m, rig, segs=64)
    for k in range(6):
        a = 2 * math.pi * k / 6 + math.pi / 6
        C.sphere(f'{name}.lobe.{k}', (0.2 * s * math.cos(a), 0.2 * s * math.sin(a), z0), (0.11 * s, 0.11 * s, 0.07 * s), m, rig, 24)
    fm = C.face_mats(name.lower(), iris=(0.05, 0.03, 0.03), line=(0.12, 0.08, 0.1), blush=(1.0, 0.55, 0.55))
    fp = C.face(name, body, fm, rig, eyes_x=0.085 * s, eyes_z=z0 + 0.38 * s, eye_size=(0.045 * s, 0.056 * s), brow_dz=0.075 * s,
                brow_w=0.03 * s, mouth_z=z0 + 0.3 * s, mouth_w=0.04 * s, mouth_sag=0.018 * s, blush_x=0.15 * s, blush_z=z0 + 0.31 * s,
                blush_size=(0.035 * s, 0.022 * s), line_r=0.006 * s, look=(0.0, 0.1))
    arms = []
    for side, sx in (('L', -1), ('R', 1)):
        a = C.empty(f'{name}.arm.{side}', rig, (sx * 0.27 * s, -0.02 * s, z0 + 0.24 * s), (0, math.radians(-sx * 35), 0))
        C.sphere(f'{name}.armmesh.{side}', (sx * 0.03 * s, 0, -0.07 * s), (0.05 * s, 0.05 * s, 0.09 * s), m, a, 24)
        arms.append(a)
    return {'root': root, 'rig': rig, 'eyes': fp['eyes'], 'mouth': fp['mouth'], 'arms': arms, 'height': 0.76 * s}


def _wing(name, sx, s, mem, bone, parent):
    piv = C.empty(name, parent, (sx * 0.09 * s, 0.0, 0.2 * s))
    tips = [(0.34, 0.16), (0.42, -0.02), (0.3, -0.16)]
    bm = bmesh.new()
    pts = [(0.0, 0.06), (0.12, 0.13)] + [tips[0]]
    outline = [(0.0, 0.06), (0.14, 0.14), tips[0], (0.33, 0.05), tips[1], (0.3, -0.07), tips[2], (0.18, -0.1), (0.06, -0.14), (0.0, -0.08)]
    vs = [bm.verts.new((sx * x * s, 0.0, z * s)) for x, z in outline]
    bm.faces.new(vs if sx > 0 else vs[::-1])
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    w = C.mesh_obj(name + '.membrane', bm, mem, piv, smooth=True)
    so = w.modifiers.new('t', 'SOLIDIFY')
    so.thickness = 0.012 * s
    so.offset = 0
    sub = w.modifiers.new('sub', 'SUBSURF')
    sub.levels = 1
    sub.render_levels = 2
    arm = [(0, -0.003 * s, 0.06 * s), (sx * 0.14 * s, -0.003 * s, 0.14 * s)]
    C.tube(name + '.forearm', arm, 0.012 * s, bone, piv)
    for k, (tx, tz) in enumerate(tips):
        C.tube(f'{name}.finger.{k}', [arm[1], (sx * tx * s, -0.004 * s, tz * s)], 0.007 * s, bone, piv)
    C.sphere(name + '.thumb', (sx * 0.145 * s, -0.004 * s, 0.155 * s), (0.014 * s,) * 3, bone, piv, 12)
    return piv


def bat(name='Velo', h=0.5):
    s = h / 0.5
    root = C.empty(name)
    rig = C.empty(name + '.rig', root, (0, 0, 0.05 * s))
    fur = C.mat(name + '_fur', (0.27, 0.29, 0.36), rough=0.75, sheen=0.6)
    mem = C.mat(name + '_wing', (0.33, 0.27, 0.38), rough=0.6, sss=0.1)
    bone = C.mat(name + '_bone', (0.22, 0.2, 0.28), rough=0.6)
    inner = C.mat(name + '_ear', (0.75, 0.5, 0.55), rough=0.7)
    snout_m = C.mat(name + '_snout', (0.45, 0.42, 0.5), rough=0.6)
    line = C.mat(name + '_line', (0.06, 0.04, 0.06), rough=0.6)
    C.sphere(name + '.body', (0, 0, 0.15 * s), (0.12 * s, 0.1 * s, 0.15 * s), fur, rig, 40)
    head = C.sphere(name + '.head', (0, -0.01 * s, 0.33 * s), (0.12 * s, 0.11 * s, 0.1 * s), fur, rig, 40)
    for k, sx in enumerate((-1, 1)):
        e = C.empty(f'{name}.ear.{k}', rig, (sx * 0.07 * s, 0.0, 0.41 * s), (0, math.radians(sx * 18), 0))
        C.sphere(f'{name}.earmesh.{k}', (0, 0, 0.05 * s), (0.04 * s, 0.025 * s, 0.07 * s), fur, e, 24)
        C.sphere(f'{name}.earin.{k}', (0, -0.017 * s, 0.05 * s), (0.025 * s, 0.01 * s, 0.05 * s), inner, e, 16)
        C.sphere(f'{name}.foot.{k}', (sx * 0.05 * s, -0.02 * s, 0.0), (0.03 * s, 0.035 * s, 0.018 * s), bone, rig, 12)
    C.sphere(name + '.snout', (0, -0.1 * s, 0.31 * s), (0.04 * s, 0.025 * s, 0.03 * s), snout_m, rig, 20)
    C.sphere(name + '.nose', (0, -0.124 * s, 0.322 * s), (0.012 * s, 0.006 * s, 0.008 * s), line, rig, 12)
    eyes = _eyes(name, rig, [(-0.045 * s, -0.085 * s, 0.355 * s), (0.045 * s, -0.085 * s, 0.355 * s)], 0.028 * s, 0.033 * s)
    mouth = _smile(name, rig, 0, -0.118 * s, 0.288 * s, 0.018 * s, 0.008 * s, 0.004 * s, line)
    wings = [_wing(f'{name}.wing.{side}', sx, s, mem, bone, rig) for side, sx in (('L', -1), ('R', 1))]
    return {'root': root, 'rig': rig, 'wings': wings, 'eyes': eyes, 'mouth': mouth, 'height': 0.52 * s}


def flap(b, f0, f1, period=12, amp=38, fold=False):
    for f in range(f0, f1 + 1, period // 2):
        up = ((f - f0) // (period // 2)) % 2 == 0
        for k, w in enumerate(b['wings']):
            sx = -1 if k == 0 else 1
            a = amp if up else -amp * 0.6
            C.key(w, 'rotation_euler', f, (0, math.radians(-sx * a), 0))
            C.key(w, 'scale', f, (1, 1, 1))


def fold_wings(b, f, amt=1.0):
    for k, w in enumerate(b['wings']):
        sx = -1 if k == 0 else 1
        C.key(w, 'rotation_euler', f, (0, math.radians(sx * 72 * amt), 0))
        C.key(w, 'scale', f, (1 - 0.55 * amt, 1, 1))


def _m(name, rgb, rough=0.5, emit=0.0, coat=0.2, sss=0.0):
    k = 'hw_' + name
    return bpy.data.materials.get(k) or C.mat(k, rgb, rough=rough, emit=emit, coat=coat, sss=sss)


def _flat(name, pts2d, depth, mat, parent, loc=(0, 0, 0), rot=(0, 0, 0)):
    bm = bmesh.new()
    vs = [bm.verts.new((x, 0.0, z)) for x, z in pts2d]
    f = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in [e for e in ext['geom'] if isinstance(e, bmesh.types.BMVert)]:
        v.co.y += depth
    for v in bm.verts:
        v.co.y -= depth / 2
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = C.mesh_obj(name, bm, mat, parent, smooth=False)
    b = o.modifiers.new('bev', 'BEVEL')
    b.width = min(0.006, depth * 0.3)
    b.segments = 2
    b.limit_method = 'ANGLE'
    o.location = loc
    o.rotation_euler = rot
    return o


def _circle(r, n=24, cx=0.0, cz=0.0, sx=1.0):
    return [(cx + sx * r * math.cos(-2 * math.pi * k / n), cz + r * math.sin(-2 * math.pi * k / n)) for k in range(n)]


def pumpkin(name, loc=(0, 0, 0), h=0.4, face=False, parent=None, rgb=(0.82, 0.36, 0.08)):
    g = C.empty(name, parent, loc)
    body = _m('pumpkin_%d%d%d' % tuple(int(c * 9) for c in rgb), rgb, rough=0.45, coat=0.3)
    stem = _m('stem', (0.28, 0.33, 0.14), rough=0.7)
    r = h * 0.62
    for k in range(8):
        a = 2 * math.pi * k / 8
        C.sphere(f'{name}.rib{k}', (0.42 * r * math.cos(a), 0.42 * r * math.sin(a), 0.42 * h), (0.6 * r, 0.6 * r, 0.42 * h), body, g, 24)
    C.tube(name + '.stem', [(0, 0, 0.78 * h), (0.02 * h, 0, 0.95 * h), (0.09 * h, 0, 1.04 * h)], 0.055 * h, stem, g)
    if face:
        glow = _m('glow', (1.0, 0.62, 0.2), rough=0.4, emit=3.0, coat=0.0)
        fy = -0.98 * r
        f = C.empty(name + '.face', g, (0, fy, 0.45 * h))
        for sx in (-1, 1):
            _flat(f'{name}.eye{sx}', _circle(0.075 * h, 16, sx * 0.17 * h, 0.08 * h), 0.03 * h, glow, f)
        sm = [(-0.2 * h + 0.4 * h * k / 12, -0.08 * h - 0.09 * h * math.sin(math.pi * k / 12)) for k in range(13)]
        sm += [(0.2 * h - 0.4 * h * k / 12, -0.08 * h - 0.04 * h * math.sin(math.pi * k / 12)) for k in range(1, 12)]
        _flat(name + '.smile', sm[::-1], 0.03 * h, glow, f)
        bpy.ops.object.light_add(type='POINT', location=(0, 0, 0.45 * h))
        L = bpy.context.object
        L.data.energy = 6 * h
        L.data.color = (1.0, 0.6, 0.25)
        L.data.shadow_soft_size = 0.05
        L.parent = g
        L.location = (0, -0.3 * r, 0.45 * h)
    return g


def turnip_lantern(name, loc=(0, 0, 0), h=0.24, parent=None):
    g = C.empty(name, parent, loc)
    cream = _m('turnip', (0.9, 0.86, 0.76), rough=0.6, sss=0.1)
    violet = _m('turnip_top', (0.48, 0.24, 0.5), rough=0.5)
    leaf = _m('turnip_leaf', (0.3, 0.42, 0.25), rough=0.6)
    prof = [(0.0, 0.0), (0.03 * h, 0.12 * h), (0.25 * h, 0.4 * h), (0.5 * h, 0.46 * h), (0.75 * h, 0.38 * h), (0.9 * h, 0.2 * h), (0.95 * h, 0.0)]
    C.lathe(name + '.body', prof, cream, g, segs=40)
    C.lathe(name + '.top', [(0.55 * h, 0.0), (0.56 * h, 0.462 * h), (0.75 * h, 0.39 * h), (0.9 * h, 0.21 * h), (0.965 * h, 0.0)], violet, g, segs=40)
    C.tube(name + '.root', [(0, 0, 0.02 * h), (0.02 * h, 0, -0.08 * h)], 0.02 * h, cream, g)
    for k, a in enumerate((-25, 5, 30)):
        C.tube(f'{name}.leaf{k}', [(0, 0, 0.93 * h), (math.sin(math.radians(a)) * 0.15 * h, 0, 1.2 * h)], 0.025 * h, leaf, g)
    glow = _m('glow', (1.0, 0.62, 0.2), rough=0.4, emit=3.0, coat=0.0)
    f = C.empty(name + '.face', g, (0, -0.44 * h, 0.42 * h))
    for sx in (-1, 1):
        _flat(f'{name}.eye{sx}', _circle(0.055 * h, 14, sx * 0.13 * h, 0.07 * h), 0.03 * h, glow, f)
    sm = [(-0.14 * h + 0.28 * h * k / 10, -0.06 * h - 0.06 * h * math.sin(math.pi * k / 10)) for k in range(11)]
    sm += [(0.14 * h - 0.28 * h * k / 10, -0.06 * h - 0.025 * h * math.sin(math.pi * k / 10)) for k in range(1, 10)]
    _flat(name + '.smile', sm[::-1], 0.03 * h, glow, f)
    return g


def led_light(name, loc=(0, 0, 0), h=0.1, parent=None):
    g = C.empty(name, parent, loc)
    base = _m('led_base', (0.92, 0.9, 0.85), rough=0.4)
    C.lathe(name + '.base', [(0.0, 0.0), (0.0, 0.32 * h), (0.6 * h, 0.3 * h), (0.62 * h, 0.0)], base, g, segs=32)
    flame = _m('led_glow', (1.0, 0.72, 0.3), rough=0.3, emit=4.0, coat=0.0)
    C.lathe(name + '.drop', [(0.6 * h, 0.0), (0.65 * h, 0.1 * h), (0.78 * h, 0.13 * h), (0.92 * h, 0.08 * h), (1.0 * h, 0.0)], flame, g, segs=24)
    return g


def led_candle(name, loc=(0, 0, 0), h=0.22, parent=None, rgb=(0.92, 0.88, 0.8)):
    g = C.empty(name, parent, loc)
    wax = _m('candle_' + '%d%d%d' % tuple(int(c * 9) for c in rgb), rgb, rough=0.5, sss=0.1)
    C.lathe(name + '.wax', [(0.0, 0.0), (0.0, 0.2 * h), (0.75 * h, 0.2 * h), (0.78 * h, 0.15 * h), (0.79 * h, 0.0)], wax, g, segs=32)
    flame = _m('led_glow', (1.0, 0.72, 0.3), rough=0.3, emit=4.0, coat=0.0)
    C.lathe(name + '.drop', [(0.79 * h, 0.0), (0.82 * h, 0.05 * h), (0.9 * h, 0.065 * h), (0.98 * h, 0.035 * h), (1.04 * h, 0.0)], flame, g, segs=20)
    return g


def web(name, loc=(0, 0, 0), r=0.35, spokes=8, rings=5, corner=False, parent=None, rot=(0, 0, 0)):
    g = C.empty(name, parent, loc, rot)
    silk = _m('silk', (0.78, 0.8, 0.83), rough=0.5, emit=0.15, coat=0.0)
    a0, a1 = (0.0, math.pi / 2) if corner else (0.0, 2 * math.pi)
    n = spokes if not corner else max(spokes // 2, 3)
    angs = [a0 + (a1 - a0) * k / (n - (1 if corner else 0)) for k in range(n)]
    parts = []
    for k, a in enumerate(angs):
        parts.append(C.tube(f'{name}.spoke{k}', [(0, 0, 0), (r * math.cos(a), 0, -r * math.sin(a))], 0.004, silk, g))
    for j in range(1, rings + 1):
        rr = r * j / (rings + 0.4)
        pts = []
        seq = angs + ([] if corner else [angs[0]])
        for k, a in enumerate(seq):
            pts.append((rr * math.cos(a), 0, -rr * math.sin(a)))
            if k + 1 < len(seq):
                b = seq[k + 1] if k + 1 < len(seq) else angs[0]
                m_ = (a + (b if b > a else b + 2 * math.pi)) / 2
                pts.append((rr * 0.93 * math.cos(m_), 0, -rr * 0.93 * math.sin(m_)))
        parts.append(C.tube(f'{name}.ring{j}', pts, 0.003, silk, g))
    return g, parts


def reveal(parts, f0, f1):
    n = len(parts)
    for k, o in enumerate(parts):
        a = f0 + (f1 - f0) * k / n
        b = a + (f1 - f0) / n * 1.5
        o.data.bevel_factor_mapping_end = 'SPLINE'
        o.data.bevel_factor_end = 0.0
        o.data.keyframe_insert('bevel_factor_end', frame=0)
        o.data.keyframe_insert('bevel_factor_end', frame=int(a))
        o.data.bevel_factor_end = 1.0
        o.data.keyframe_insert('bevel_factor_end', frame=int(b) + 1)


def autumn_leaf(name, loc=(0, 0, 0), size=0.12, rgb=(0.75, 0.38, 0.12), parent=None, rot=(0, 0, 0)):
    g = C.empty(name, parent, loc, rot)
    mt = _m('leaf_%d%d%d' % tuple(int(c * 9) for c in rgb), rgb, rough=0.6)
    pts = []
    for k in range(25):
        t = k / 24
        a = math.pi * t
        w = size * 0.42 * math.sin(a) * (1 + 0.25 * math.sin(5 * a))
        pts.append((w, -size + 2 * size * t))
    pts += [(-x, z) for x, z in pts[-2:0:-1]]
    _flat(name + '.m', pts, size * 0.04, mt, g)
    C.tube(name + '.vein', [(0, -size * 0.022, -size * 1.15), (0, -size * 0.022, size * 0.8)], size * 0.02, _m('leaf_vein', (0.45, 0.25, 0.1)), g)
    return g


def bunting(name, a, b, n=7, sag=0.18, parent=None, cols=None):
    a, b = Vector(a), Vector(b)
    g = C.empty(name, parent)
    cord = _m('cord', (0.9, 0.86, 0.78), rough=0.6)
    pts = [tuple(a.lerp(b, k / 20) - Vector((0, 0, sag * 4 * (k / 20) * (1 - k / 20)))) for k in range(21)]
    C.tube(name + '.cord', pts, 0.008, cord, g)
    cols = cols or [(0.2, 0.12, 0.25), (0.82, 0.36, 0.08), (0.25, 0.36, 0.27), (0.95, 0.6, 0.18)]
    for k in range(n):
        u = (k + 0.5) / n
        p = a.lerp(b, u) - Vector((0, 0, sag * 4 * u * (1 - u)))
        mt = _m('flag%d' % (k % len(cols)), cols[k % len(cols)], rough=0.6)
        _flat(f'{name}.flag{k}', [(-0.08, 0.0), (0.08, 0.0), (0.0, -0.16)], 0.006, mt, g, loc=tuple(p))
    return g


def paper_bat(name, loc=(0, 0, 0), s=0.18, parent=None, string=0.3):
    g = C.empty(name, parent, loc)
    paper = _m('paper_bat', (0.16, 0.13, 0.2), rough=0.8)
    pts = [(0.0, 0.18), (0.12, 0.25), (0.32, 0.3), (0.5, 0.18), (0.42, 0.12), (0.36, 0.0), (0.26, 0.06), (0.18, -0.04), (0.08, 0.04), (0.0, -0.12)]
    full = [(x * s, z * s) for x, z in pts] + [(-x * s, z * s) for x, z in pts[-2:0:-1]]
    _flat(name + '.m', full[::-1], 0.01 * s, paper, g)
    for sx in (-1, 1):
        C.sphere(f'{name}.ear{sx}', (sx * 0.06 * s, 0, 0.24 * s), (0.04 * s, 0.01 * s, 0.07 * s), paper, g, 8)
    C.tube(name + '.str', [(0, 0, 0.2 * s), (0, 0, string)], 0.002, _m('cord', (0.9, 0.86, 0.78)), g)
    return g


def wrapped_treat(name, loc=(0, 0, 0), s=0.07, rgb=(0.95, 0.6, 0.18), parent=None, rot=(0, 0, 0)):
    g = C.empty(name, parent, loc, rot)
    mt = _m('treat_%d%d%d' % tuple(int(c * 9) for c in rgb), rgb, rough=0.25, coat=0.6)
    C.sphere(name + '.m', (0, 0, 0), (0.5 * s, 0.32 * s, 0.32 * s), mt, g, 20)
    for sx in (-1, 1):
        C.lathe(f'{name}.end{sx}', [(0.0, 0.0), (0.02 * s, 0.12 * s), (0.25 * s, 0.25 * s), (0.27 * s, 0.0)], mt, C.empty(f'{name}.e{sx}', g, (sx * 0.42 * s, 0, 0), (0, math.radians(sx * 90), 0)), segs=12)
    return g


def treat_basket(name, loc=(0, 0, 0), h=0.2, parent=None, rgb=(0.82, 0.36, 0.08)):
    g = C.empty(name, parent, loc)
    mt = _m('basket', rgb, rough=0.45, coat=0.3)
    C.lathe(name + '.pail', [(0.0, 0.0), (0.0, 0.42 * h), (0.15 * h, 0.5 * h), (0.75 * h, 0.55 * h), (0.8 * h, 0.56 * h), (0.8 * h, 0.5 * h), (0.15 * h, 0.44 * h), (0.06 * h, 0.0)], mt, g, segs=40)
    pts = [(0.55 * h * math.cos(math.pi * k / 16), 0, 0.78 * h + 0.45 * h * math.sin(math.pi * k / 16)) for k in range(17)]
    C.tube(name + '.handle', pts, 0.025 * h, _m('cord', (0.9, 0.86, 0.78)), g)
    return g


def card(name, text, font, loc=(0, 0, 0), w=0.32, h=0.2, bg=(0.91, 0.87, 0.81), ink=(0.15, 0.2, 0.26), parent=None, rot=(0, 0, 0)):
    g = C.empty(name, parent, loc, rot)
    C.rounded_box(name + '.board', (0, 0, 0), (w, 0.02, h), 0.01, _m('card_%d%d%d' % tuple(int(c * 9) for c in bg), bg, rough=0.6), g)
    cu = bpy.data.curves.new(name + '.t', 'FONT')
    cu.body = text
    cu.font = font
    cu.align_x = 'CENTER'
    cu.align_y = 'CENTER'
    cu.size = h * 0.55
    cu.extrude = 0.004
    o = bpy.data.objects.new(name + '.text', cu)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(_m('ink_%d%d%d' % tuple(int(c * 9) for c in ink), ink, rough=0.5))
    o.parent = g
    o.location = (0, -0.014, 0)
    o.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.view_layer.update()
    if o.dimensions.x > w * 0.88:
        k = w * 0.88 / o.dimensions.x
        o.scale = (k, k, k)
    return g


def toy_skeleton(name, loc=(0, 0, 0), h=0.7, parent=None, rot=(0, 0, 0)):
    g = C.empty(name, parent, loc, rot)
    card_m = _m('cardboard', (0.93, 0.89, 0.8), rough=0.7)
    ink = _m('sk_ink', (0.2, 0.17, 0.24), rough=0.6)
    blush = _m('sk_blush', (0.95, 0.55, 0.55), rough=0.8)
    d = 0.012 * h / 0.7
    _flat(name + '.head', _circle(0.13 * h, 32, 0, 0.82 * h, 1.1), d, card_m, g)
    for sx in (-1, 1):
        _flat(f'{name}.eye{sx}', _circle(0.03 * h, 16, sx * 0.05 * h, 0.85 * h), d, ink, g, loc=(0, -d, 0))
        _flat(f'{name}.blush{sx}', _circle(0.02 * h, 12, sx * 0.09 * h, 0.79 * h), d, blush, g, loc=(0, -d, 0))
    C.tube(name + '.smile', [(-0.05 * h, -1.6 * d, 0.77 * h), (0, -1.6 * d, 0.745 * h), (0.05 * h, -1.6 * d, 0.77 * h)], 0.007 * h, ink, g)
    C.tube(name + '.spine', [(0, 0, 0.69 * h), (0, 0, 0.36 * h)], 0.022 * h, card_m, g)
    for k in range(3):
        z = 0.64 * h - k * 0.075 * h
        w = (0.14 - k * 0.02) * h
        C.tube(f'{name}.rib{k}', [(-w, 0, z - 0.02 * h), (0, 0, z), (w, 0, z - 0.02 * h)], 0.018 * h, card_m, g)
    for sx in (-1, 1):
        C.tube(f'{name}.arm{sx}', [(sx * 0.12 * h, 0, 0.66 * h), (sx * 0.2 * h, 0, 0.5 * h), (sx * 0.24 * h, 0, 0.38 * h)], 0.02 * h, card_m, g)
        C.sphere(f'{name}.hand{sx}', (sx * 0.245 * h, 0, 0.36 * h), (0.035 * h, 0.012 * h, 0.035 * h), card_m, g, 12)
        C.tube(f'{name}.leg{sx}', [(sx * 0.05 * h, 0, 0.36 * h), (sx * 0.07 * h, 0, 0.06 * h)], 0.022 * h, card_m, g)
        C.sphere(f'{name}.foot{sx}', (sx * 0.08 * h, -0.01 * h, 0.04 * h), (0.045 * h, 0.02 * h, 0.03 * h), card_m, g, 12)
    C.tube(name + '.pelvis', [(-0.07 * h, 0, 0.37 * h), (0.07 * h, 0, 0.37 * h)], 0.025 * h, card_m, g)
    return g


def plush_snake(name, loc=(0, 0, 0), L=0.9, parent=None, rot=(0, 0, 0)):
    g = C.empty(name, parent, loc, rot)
    body = _m('snake', (0.42, 0.52, 0.36), rough=0.85)
    spot = _m('snake_spot', (0.95, 0.6, 0.18), rough=0.8)
    belly = _m('snake_belly', (0.93, 0.86, 0.68), rough=0.85)
    r = 0.07 * L
    pts, radii = [], []
    for k in range(25):
        t = k / 24
        pts.append((-L / 2 + L * t, 0.12 * L * math.sin(t * 2.2 * math.pi), r))
        radii.append(0.35 + 0.65 * math.sin(math.pi * min(t * 1.1, 1.0)) ** 0.5)
    C.tube(name + '.body', pts, r, body, g, radii=radii)
    for k in range(4, 22, 3):
        x, y, z = pts[k]
        C.sphere(f'{name}.spot{k}', (x, y, z + r * radii[k] * 0.85), (r * 0.45, r * 0.45, r * 0.2), spot, g, 12)
    hx, hy, hz = pts[-1]
    hd = C.empty(name + '.head', g, (hx + r * 0.8, hy, hz + r * 0.6))
    C.sphere(name + '.headm', (0, 0, 0), (r * 1.7, r * 1.4, r * 1.3), body, hd, 24)
    C.sphere(name + '.chin', (r * 0.3, 0, -r * 0.5), (r * 1.3, r * 1.1, r * 0.7), belly, hd, 20)
    _eyes(name, hd, [(r * 0.7, -r * 0.7, r * 0.6), (r * 0.7, r * 0.7, r * 0.6)], r * 0.32, r * 0.38)
    for e in [o for o in hd.children if o.name.startswith(name + '.eye.')]:
        e.rotation_euler = (0, 0, math.radians(90))
    return g


def album(name, loc=(0, 0, 0), w=0.42, h=0.3, parent=None, rot=(0, 0, 0), cover=(0.4, 0.25, 0.42)):
    g = C.empty(name, parent, loc, rot)
    cov = _m('album_cover', cover, rough=0.5, coat=0.3)
    pg = _m('album_page', (0.96, 0.93, 0.86), rough=0.7)
    C.rounded_box(name + '.back', (0, 0, 0.012), (w, h, 0.02), 0.006, cov, g)
    C.rounded_box(name + '.block', (0, 0, 0.032), (w * 0.95, h * 0.94, 0.03), 0.004, pg, g)
    spine = C.empty(name + '.spine', g, (0, 0, 0.05))
    pages = []
    for k in range(2):
        piv = C.empty(f'{name}.page{k}', spine, (0, 0, 0.002 * k))
        C.rounded_box(f'{name}.pagem{k}', (-w * 0.235, 0, 0), (w * 0.47, h * 0.92, 0.004), 0.002, pg, piv)
        pages.append(piv)
    lid = C.empty(name + '.lid', spine, (0, 0, 0.006))
    C.rounded_box(name + '.coverm', (-w * 0.25, 0, 0.004), (w * 0.5, h, 0.012), 0.004, cov, lid)
    _flat(name + '.leafdeco', [(x * 0.6, z * 0.6) for x, z in [(0.0, 0.08), (0.03, 0.03), (0.08, 0.0), (0.03, -0.03), (0.0, -0.08), (-0.03, -0.03), (-0.08, 0.0), (-0.03, 0.03)]][::-1],
          0.004, _m('album_star', (0.95, 0.6, 0.18), rough=0.4, emit=0.2), lid, loc=(-w * 0.25, 0, 0.012), rot=(math.radians(-90), 0, 0))
    return {'root': g, 'lid': lid, 'pages': pages, 'spine': spine}


def harvest_basket(name, loc=(0, 0, 0), h=0.3, parent=None):
    g = C.empty(name, parent, loc)
    wick = _m('wicker', (0.62, 0.42, 0.22), rough=0.8)
    C.lathe(name + '.b', [(0.0, 0.0), (0.0, 0.35 * h), (0.1 * h, 0.42 * h), (0.45 * h, 0.55 * h), (0.5 * h, 0.58 * h), (0.5 * h, 0.52 * h), (0.1 * h, 0.38 * h), (0.05 * h, 0.0)], wick, g, segs=40)
    for k in range(3):
        _ring(f'{name}.band{k}', g, (0.12 + 0.14 * k) * h, (0.43 + 0.05 * k) * h, (0.43 + 0.05 * k) * h, 0.012 * h, wick)
    red = _m('apple_red', (0.8, 0.12, 0.08), rough=0.35, coat=0.5)
    for k, (x, y) in enumerate(((-0.18, 0.0), (0.15, 0.08), (0.0, -0.15), (0.05, 0.18))):
        C.sphere(f'{name}.ap{k}', (x * h, y * h, 0.55 * h), (0.15 * h, 0.15 * h, 0.14 * h), red, g, 20)
    return g


def _ring(name, parent, z, rx, ry, r, mat, n=48):
    pts = [(rx * math.cos(2 * math.pi * k / n), ry * math.sin(2 * math.pi * k / n), z) for k in range(n + 1)]
    return C.tube(name, pts, r, mat, parent)


def door(name, loc=(0, 0, 0), h=1.5, parent=None, rgb=(0.4, 0.25, 0.42)):
    g = C.empty(name, parent, loc)
    frame = _m('door_frame', (0.92, 0.88, 0.8), rough=0.5)
    panel = _m('door_' + '%d%d%d' % tuple(int(c * 9) for c in rgb), rgb, rough=0.45, coat=0.3)
    w = h * 0.55
    C.rounded_box(name + '.wall', (0, 0.06, h * 0.55), (w * 2.2, 0.1, h * 1.1), 0.02, _m('wall', (0.86, 0.78, 0.66), rough=0.8), g)
    for x in (-w / 2 - 0.04, w / 2 + 0.04):
        C.rounded_box(name + '.jamb', (x, 0, h / 2), (0.08, 0.12, h), 0.015, frame, g)
    C.rounded_box(name + '.lintel', (0, 0, h + 0.04), (w + 0.16, 0.12, 0.08), 0.015, frame, g)
    hinge = C.empty(name + '.hinge', g, (-w / 2, -0.02, 0))
    C.rounded_box(name + '.panel', (w / 2, 0, h / 2), (w, 0.06, h), 0.02, panel, hinge)
    C.sphere(name + '.knob', (w * 0.85, -0.06, h * 0.48), (0.04, 0.04, 0.04), _m('amber_knob', (0.95, 0.6, 0.18), rough=0.3, coat=0.6), hinge, 16)
    return {'root': g, 'hinge': hinge}


def marigold(name, loc=(0, 0, 0), r=0.05, parent=None, rot=(0, 0, 0)):
    g = C.empty(name, parent, loc, rot)
    pet = [_m('cempa_a', (1.0, 0.45, 0.02), rough=0.6), _m('cempa_b', (1.0, 0.58, 0.05), rough=0.6)]
    C.sphere(name + '.core', (0, 0, 0.25 * r), (0.5 * r, 0.5 * r, 0.35 * r), pet[0], g, 16)
    for ring, (rr, z, n) in enumerate(((0.85, 0.05, 14), (0.65, 0.3, 11), (0.4, 0.5, 8))):
        for k in range(n):
            a = 2 * math.pi * (k + 0.5 * ring) / n
            C.sphere(f'{name}.p{ring}_{k}', (rr * r * math.cos(a), rr * r * math.sin(a), z * r), (0.28 * r, 0.2 * r, 0.22 * r), pet[(k + ring) % 2], g, 10,
                     rot=(0, math.radians(-20), a))
    return g


def petal_path(name, pts, parent=None, n=40, seed=3):
    import random as R
    R.seed(seed)
    g = C.empty(name, parent)
    pet = [_m('cempa_a', (1.0, 0.45, 0.02), rough=0.6), _m('cempa_b', (1.0, 0.58, 0.05), rough=0.6)]
    P = [Vector(p) for p in pts]
    for k in range(n):
        u = k / max(n - 1, 1) * (len(P) - 1)
        i = min(int(u), len(P) - 2)
        p = P[i].lerp(P[i + 1], u - i) + Vector((R.uniform(-0.04, 0.04), R.uniform(-0.04, 0.04), 0.004))
        C.sphere(f'{name}.{k}', tuple(p), (0.016, 0.011, 0.004), pet[k % 2], g, 8, rot=(0, 0, R.uniform(0, 3.14)))
    return g


def papel_picado(name, a, b, n=6, parent=None, sag=0.1):
    a, b = Vector(a), Vector(b)
    g = C.empty(name, parent)
    C.tube(name + '.cord', [tuple(a.lerp(b, k / 20) - Vector((0, 0, sag * 4 * (k / 20) * (1 - k / 20)))) for k in range(21)], 0.005, _m('cord', (0.9, 0.86, 0.78)), g)
    cols = [(0.95, 0.3, 0.5), (1.0, 0.55, 0.05), (0.55, 0.3, 0.75), (0.2, 0.65, 0.55), (0.95, 0.8, 0.15)]
    W, Hh = 0.2, 0.24
    for k in range(n):
        u = (k + 0.5) / n
        p = a.lerp(b, u) - Vector((0, 0, sag * 4 * u * (1 - u)))
        mt = _m('pp%d' % (k % len(cols)), cols[k % len(cols)], rough=0.7)
        mt.use_backface_culling = False
        bm = bmesh.new()
        nx, nz = 10, 12
        cells = {}
        holes = set()
        for i in range(nx):
            for j in range(nz):
                cx, cz = (i + 0.5) / nx, (j + 0.5) / nz
                if 0.15 < cz < 0.85 and ((i + j) % 3 == 0 or ((cx - 0.5) ** 2 + (cz - 0.5) ** 2 < 0.03 and (i + j) % 2 == 0)):
                    holes.add((i, j))
        vs = {}
        for i in range(nx + 1):
            for j in range(nz + 1):
                x = -W / 2 + W * i / nx
                z = -Hh * (1 - j / nz)
                if j == 0:
                    z -= 0.012 * (1 if i % 2 else 0)
                vs[i, j] = bm.verts.new((x, 0, z))
        for i in range(nx):
            for j in range(nz):
                if (i, j) not in holes:
                    bm.faces.new((vs[i, j], vs[i + 1, j], vs[i + 1, j + 1], vs[i, j + 1]))
        loose = [v for v in bm.verts if not v.link_faces]
        bmesh.ops.delete(bm, geom=loose, context='VERTS')
        o = C.mesh_obj(f'{name}.p{k}', bm, mt, g, smooth=False)
        o.location = tuple(p)
        so = o.modifiers.new('t', 'SOLIDIFY')
        so.thickness = 0.003
    return g


def photo_frame(name, loc=(0, 0, 0), h=0.24, parent=None, rot=(0, 0, 0)):
    g = C.empty(name, parent, loc, rot)
    w = h * 0.8
    fr = _m('frame_wood', (0.55, 0.36, 0.2), rough=0.5, coat=0.3)
    C.rounded_box(name + '.frame', (0, 0, h / 2), (w, 0.03, h), 0.012, fr, g)
    C.rounded_box(name + '.bg', (0, -0.016, h / 2), (w * 0.8, 0.004, h * 0.82), 0.002, _m('photo_bg', (0.75, 0.85, 0.9), rough=0.8), g)
    C.tube(name + '.stand', [(0, 0.015, h * 0.5), (0, 0.09, 0.0)], 0.008, fr, g)
    f = C.empty(name + '.pic', g, (0, -0.02, h * 0.5))
    skin = _m('portrait_skin', (0.85, 0.65, 0.5), rough=0.8)
    hair = _m('portrait_hair', (0.86, 0.86, 0.88), rough=0.8)
    shirt = _m('portrait_shirt', (0.35, 0.5, 0.42), rough=0.8)
    ink = _m('portrait_ink', (0.2, 0.15, 0.15), rough=0.6)
    _flat(name + '.shirt', [(-0.3 * w, -0.4 * h), (0.3 * w, -0.4 * h), (0.24 * w, -0.2 * h), (-0.24 * w, -0.2 * h)][::-1], 0.002, shirt, f)
    _flat(name + '.hair', _circle(0.2 * h, 28, 0, 0.06 * h, 0.95), 0.002, hair, f, loc=(0, 0.001, 0))
    _flat(name + '.bun', _circle(0.08 * h, 18, 0, 0.27 * h), 0.002, hair, f, loc=(0, 0.001, 0))
    _flat(name + '.face', _circle(0.16 * h, 28, 0, 0.01 * h, 0.88), 0.002, skin, f, loc=(0, -0.002, 0))
    for sx in (-1, 1):
        _ring(f'{name}.glass{sx}', C.empty(f'{name}.gl{sx}', f, (sx * 0.06 * h, -0.004, 0.04 * h), (math.radians(90), 0, 0)), 0, 0.04 * h, 0.035 * h, 0.004 * h, ink)
        _flat(f'{name}.eye{sx}', _circle(0.012 * h, 10, sx * 0.06 * h, 0.04 * h), 0.002, ink, f, loc=(0, -0.004, 0))
    C.tube(name + '.smile', [(-0.05 * h, -0.005, -0.05 * h), (0, -0.005, -0.075 * h), (0.05 * h, -0.005, -0.05 * h)], 0.005 * h, ink, f)
    return g


def pan_de_muerto(name, loc=(0, 0, 0), r=0.08, parent=None):
    g = C.empty(name, parent, loc)
    bread = _m('bread', (0.78, 0.48, 0.2), rough=0.6, coat=0.2)
    sugar = _m('bread_sugar', (0.95, 0.88, 0.75), rough=0.9)
    C.sphere(name + '.dome', (0, 0, 0.35 * r), (r, r, 0.55 * r), bread, g, 32)
    for k in range(4):
        a = math.pi * k / 4
        pts = [(math.cos(a) * r * t, math.sin(a) * r * t, 0.35 * r + 0.55 * r * math.sqrt(max(0, 1 - t * t)) + 0.03 * r) for t in [-0.95 + 1.9 * i / 10 for i in range(11)]]
        C.tube(f'{name}.bone{k}', pts, 0.07 * r, bread, g)
    C.sphere(name + '.knob', (0, 0, 0.95 * r), (0.18 * r, 0.18 * r, 0.14 * r), bread, g, 16)
    return g


def water_glass(name, loc=(0, 0, 0), h=0.1, parent=None):
    g = C.empty(name, parent, loc)
    gl = _m('glass_clear', (0.85, 0.93, 1.0), rough=0.08, coat=1.0)
    wt = _m('water', (0.55, 0.78, 0.95), rough=0.1, coat=0.6)
    C.lathe(name + '.g', [(0.0, 0.0), (0.0, 0.3 * h), (0.05 * h, 0.32 * h), (1.0 * h, 0.4 * h), (1.0 * h, 0.37 * h), (0.07 * h, 0.29 * h), (0.07 * h, 0.0)], gl, g, segs=32)
    C.lathe(name + '.w', [(0.07 * h, 0.0), (0.07 * h, 0.285 * h), (0.7 * h, 0.35 * h), (0.71 * h, 0.0)], wt, g, segs=32)
    return g


def remembrance_table(name, loc=(0, 0, 0), w=0.95, parent=None, cloth=(0.92, 0.88, 0.8)):
    g = C.empty(name, parent, loc)
    wood = _m('table_wood', (0.6, 0.42, 0.26), rough=0.5, coat=0.2)
    cl = _m('cloth_%d%d%d' % tuple(int(c * 9) for c in cloth), cloth, rough=0.8)
    hh = 0.42
    C.rounded_box(name + '.top', (0, 0, hh), (w, 0.48, 0.04), 0.01, wood, g)
    for sx in (-1, 1):
        for sy in (-1, 1):
            C.rounded_box(name + '.leg', (sx * (w / 2 - 0.05), sy * 0.19, hh / 2), (0.05, 0.05, hh), 0.01, wood, g)
    C.rounded_box(name + '.cloth', (0, 0, hh + 0.025), (w * 1.02, 0.5, 0.012), 0.004, cl, g)
    C.rounded_box(name + '.drape', (0, -0.25, hh - 0.06), (w * 1.02, 0.012, 0.16), 0.004, cl, g)
    return {'root': g, 'top': hh + 0.032}


def bouquet(name, loc=(0, 0, 0), h=0.26, parent=None, cols=((0.95, 0.92, 0.88), (0.95, 0.75, 0.8), (0.98, 0.85, 0.4))):
    g = C.empty(name, parent, loc)
    green = _m('stemg', (0.25, 0.45, 0.22), rough=0.6)
    C.lathe(name + '.vase', [(0.0, 0.0), (0.0, 0.07 * h / 0.26), (0.08, 0.08), (0.14, 0.05), (0.16, 0.055), (0.16, 0.0)], _m('vase', (0.45, 0.55, 0.68), rough=0.3, coat=0.5), g, segs=32)
    for k in range(7):
        a = 2 * math.pi * k / 7
        tip = (0.06 * math.cos(a), 0.05 * math.sin(a), h * (0.85 + 0.1 * (k % 3) / 2))
        C.tube(f'{name}.s{k}', [(0, 0, 0.1), tip], 0.006, green, g)
        col = cols[k % len(cols)]
        mt = _m('bq_%d%d%d' % tuple(int(c * 9) for c in col), col, rough=0.6)
        fg = C.empty(f'{name}.f{k}', g, tip)
        for j in range(5):
            b = 2 * math.pi * j / 5
            C.sphere(f'{name}.pt{k}_{j}', (0.018 * math.cos(b), 0.018 * math.sin(b), 0.0), (0.02, 0.02, 0.012), mt, fg, 10)
        C.sphere(f'{name}.c{k}', (0, 0, 0.006), (0.012, 0.012, 0.01), _m('bq_center', (0.95, 0.75, 0.2)), fg, 10)
    return g


def shadow_screen(name, loc=(0, 0, 0), w=1.0, h=0.8, parent=None):
    g = C.empty(name, parent, loc)
    fr = _m('screen_frame', (0.4, 0.25, 0.42), rough=0.5)
    pane = _m('screen_pane', (0.97, 0.94, 0.88), rough=0.9)
    pane.node_tree.nodes['Principled BSDF'].inputs['Subsurface Weight'].default_value = 0.0
    C.rounded_box(name + '.pane', (0, 0, 0.25 + h / 2), (w, 0.01, h), 0.003, pane, g)
    for x in (-w / 2, w / 2):
        C.rounded_box(name + '.post', (x, 0, (0.25 + h) / 2 + 0.02), (0.05, 0.05, 0.25 + h + 0.04), 0.01, fr, g)
    C.rounded_box(name + '.topbar', (0, 0, 0.25 + h + 0.02), (w + 0.05, 0.05, 0.05), 0.01, fr, g)
    return g


def bare_tree(name, loc=(0, 0, 0), h=1.6, parent=None):
    g = C.empty(name, parent, loc)
    bark = _m('bark', (0.42, 0.3, 0.22), rough=0.8)
    C.tube(name + '.trunk', [(0, 0, 0), (0.03 * h, 0, 0.35 * h), (-0.02 * h, 0, 0.62 * h), (0.0, 0, 0.8 * h)], 0.06 * h, bark, g, radii=[1.3, 1.0, 0.8, 0.5])
    for k, (z, a, L) in enumerate(((0.45, 40, 0.3), (0.55, -35, 0.32), (0.68, 55, 0.25), (0.74, -60, 0.22), (0.8, 10, 0.2))):
        r = math.radians(a)
        p0 = (0, 0, z * h)
        p1 = (math.sin(r) * L * h * 0.6, 0.05 * h * (k % 2), (z + 0.12) * h)
        p2 = (math.sin(r) * L * h, 0.08 * h * (k % 2), (z + 0.18 + 0.05 * (k % 2)) * h)
        C.tube(f'{name}.br{k}', [p0, p1, p2], 0.028 * h, bark, g, radii=[1.0, 0.7, 0.45])
        C.sphere(f'{name}.tip{k}', p2, (0.013 * h,) * 3, bark, g, 10)
    return g


def pictogram(name, kind, loc=(0, 0, 0), s=0.08, parent=None, rot=(0, 0, 0)):
    g = C.empty(name, parent, loc, rot)
    if kind == 'sun':
        y = _m('pic_sun', (0.98, 0.72, 0.15), rough=0.4, emit=0.3)
        _flat(name + '.c', _circle(0.5 * s, 24), 0.01, y, g)
        for k in range(8):
            a = 2 * math.pi * k / 8
            _flat(f'{name}.r{k}', [(0.0, 0.0), (0.12 * s, 0.0), (0.06 * s, 0.25 * s)][::-1], 0.01, y, g, loc=(0.7 * s * math.cos(a), 0, 0.7 * s * math.sin(a)), rot=(0, -a + math.pi / 2, 0))
    elif kind == 'snow':
        b = _m('pic_snow', (0.45, 0.65, 0.9), rough=0.4)
        for k in range(3):
            a = math.pi * k / 3
            C.tube(f'{name}.a{k}', [(-s * math.cos(a), 0, -s * math.sin(a)), (s * math.cos(a), 0, s * math.sin(a))], 0.07 * s, b, g)
    elif kind == 'apple':
        r = _m('apple_red', (0.8, 0.12, 0.08), rough=0.35, coat=0.5)
        _flat(name + '.a', _circle(0.55 * s, 24), 0.01, r, g)
        C.tube(name + '.st', [(0, 0, 0.5 * s), (0.1 * s, 0, 0.8 * s)], 0.06 * s, _m('stem', (0.28, 0.33, 0.14)), g)
    elif kind == 'leaf':
        autumn_leaf(name + '.l', (0, 0, 0), s, parent=g)
    return g
