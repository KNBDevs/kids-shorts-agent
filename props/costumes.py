import math
import bpy, bmesh
from mathutils import Vector
import common as C
H = 1.3
_M = {}


def m(name):
    if name not in _M:
        spec = {'plum': ((0.2, 0.12, 0.25), 0.55, 0.0), 'plum_d': ((0.13, 0.07, 0.17), 0.6, 0.0), 'sage': ((0.25, 0.36, 0.27), 0.6, 0.0),
                'amber': ((0.95, 0.6, 0.18), 0.35, 0.25), 'pumpkin': ((0.75, 0.28, 0.07), 0.45, 0.0), 'stem': ((0.2, 0.32, 0.12), 0.6, 0.0),
                'moon': ((1.0, 0.8, 0.25), 0.3, 0.4), 'silver': ((0.75, 0.77, 0.8), 0.3, 0.0)}[name]
        mm = C.mat('cos_' + name, spec[0], rough=spec[1], coat=0.3, emit=spec[2])
        _M[name] = mm
    return _M[name]


def flat(name, pts2d, depth, mat, parent, loc=(0, 0, 0), rot=(0, 0, 0), bevel=0.004):
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
    if bevel:
        b = o.modifiers.new('bev', 'BEVEL')
        b.width = bevel
        b.segments = 3
        b.limit_method = 'ANGLE'
    o.location = loc
    o.rotation_euler = rot
    return o


def star_pts(r, ri=0.45, n=5):
    return [((r if k % 2 == 0 else r * ri) * math.cos(math.pi / 2 + k * math.pi / n), (r if k % 2 == 0 else r * ri) * math.sin(math.pi / 2 + k * math.pi / n)) for k in range(2 * n)][::-1]


def crescent_pts(r, n=24):
    out = []
    for k in range(n + 1):
        a = math.radians(50 + 260 * k / n)
        out.append((r * math.cos(a), r * math.sin(a)))
    cx, ri, a0 = 0.4 * r, 0.804 * r, math.radians(-72.4)
    for k in range(1, n):
        a = a0 - math.radians(215.2) * k / n
        out.append((cx + ri * math.cos(a), ri * math.sin(a)))
    return out


def leaf_pts(r):
    out = []
    for k in range(13):
        t = k / 12
        out.append((r * 0.45 * math.sin(math.pi * t), -r + 2 * r * t))
    for k in range(1, 12):
        t = 1 - k / 12
        out.append((-r * 0.45 * math.sin(math.pi * t), -r + 2 * r * t))
    return out


def pumpkin(name, parent, loc, r):
    g = C.empty(name, parent, loc)
    for k in range(6):
        a = 2 * math.pi * k / 6
        C.sphere(f'{name}.rib{k}', (0.45 * r * math.cos(a), 0.45 * r * math.sin(a), 0), (0.6 * r, 0.6 * r, 0.8 * r), m('pumpkin'), g, 16)
    C.tube(name + '.stem', [(0, 0, 0.6 * r), (0.1 * r, 0, 1.05 * r)], 0.16 * r, m('stem'), g)
    return g


def _ring(name, parent, z, rx, ry, r, mat, n=48):
    pts = [(rx * math.cos(2 * math.pi * k / n), ry * math.sin(2 * math.pi * k / n), z) for k in range(n + 1)]
    return C.tube(name, pts, r, mat, parent)


def _hat(name, parent, loc, rot, brim, h, base, mat, band=None, tip=0.0):
    g = C.empty(name, parent, loc, rot)
    C.lathe(name + '.brim', [(0.0, 0.0), (0.0, brim), (0.012, brim * 1.01), (0.025, 0.0)], mat, g, segs=48)
    prof = [(0.02, base), (0.25 * h, base * 0.85), (0.6 * h, base * 0.5), (0.9 * h, base * 0.18), (h, 0.0)]
    cone = C.lathe(name + '.crown', [(0.02, 0.0)] + prof, mat, g, segs=48)
    if tip:
        cone.rotation_euler = (0, math.radians(tip), 0)
    if band:
        _ring(name + '.band', g, 0.05, base * 0.94, base * 0.94, 0.012, band)
    return g


def dress(ch, cid, mode='halloween'):
    if mode != 'halloween':
        return None
    rig = ch['rig']
    g = C.empty(f'cos_{cid}', rig)
    if cid == 'pimo':
        fh = 0.1 * H
        _ring('cos_pimo.scarf', g, fh + 0.25 * H, 0.42 * H, 0.42 * H, 0.05 * H, m('plum'))
        flat('cos_pimo.flap', [(-0.2 * H, 0.0), (0.2 * H, 0.0), (0.02 * H, -0.22 * H)], 0.035 * H, m('plum'), g,
             loc=(0.03 * H, -0.43 * H, fh + 0.25 * H), rot=(math.radians(-14), 0, math.radians(4)))
        flat('cos_pimo.leaf', leaf_pts(0.05 * H), 0.012 * H, m('amber'), g, loc=(-0.16 * H, -0.46 * H, fh + 0.23 * H),
             rot=(math.radians(-10), math.radians(30), math.radians(-30)))
    elif cid == 'ruki':
        fh = 0.08 * H
        hat = _hat('cos_ruki.hat', g, (0.04 * H, 0.02 * H, fh + 0.93 * H), (math.radians(-6), math.radians(14), 0), 0.24 * H, 0.32 * H, 0.15 * H, m('sage'), band=m('plum'))
        flat('cos_ruki.star', star_pts(0.05 * H), 0.012 * H, m('amber'), hat, loc=(0.0, -0.14 * H, 0.13 * H), rot=(math.radians(-25), 0, 0))
    elif cid == 'luma':
        fh = 0.08 * H
        flat('cos_luma.star', star_pts(0.075 * H), 0.02 * H, m('amber'), g, loc=(0.0, -0.205 * H, fh + 0.13 * H), rot=(math.radians(-15), 0, 0))
        _ring('cos_luma.ring', g, fh + 0.02 * H, 0.235 * H, 0.205 * H, 0.03 * H, m('plum'))
    elif cid == 'tuki':
        for k, sx in enumerate((-1, 1)):
            flat(f'cos_tuki.cape{k}', [(0.0, 0.0), (sx * 0.2 * H, 0.0), (sx * 0.27 * H, -0.36 * H), (sx * 0.02 * H, -0.32 * H)], 0.02 * H, m('plum'), g,
                 loc=(sx * 0.02 * H, 0.31 * H, 0.83 * H), rot=(math.radians(10), 0, math.radians(sx * -4)))
        C.sphere('cos_tuki.clasp', (0, 0.25 * H, 0.84 * H), (0.05 * H, 0.03 * H, 0.05 * H), m('amber'), g, 16)
        _ring('cos_tuki.tie', g, 0.8 * H, 0.27 * H, 0.255 * H, 0.022 * H, m('plum'))
    elif cid == 'moki':
        fh = 0.07 * H
        hat = _hat('cos_moki.hat', g, (0.22 * H, 0.06 * H, fh + 0.94 * H), (0, math.radians(26), 0), 0.21 * H, 0.42 * H, 0.13 * H, m('plum'), band=m('amber'), tip=10)
    elif cid == 'bopi':
        hz = 0.98 * H
        flat('cos_bopi.plate', [(0.1 * H * math.cos(-2 * math.pi * k / 32), 0.1 * H * math.sin(-2 * math.pi * k / 32)) for k in range(32)], 0.02 * H, m('plum'), g,
             loc=(0.0, -0.285 * H, 0.47 * H), rot=(math.radians(-10), 0, 0))
        flat('cos_bopi.moon', crescent_pts(0.075 * H), 0.02 * H, m('moon'), g, loc=(0.0, -0.302 * H, 0.47 * H), rot=(math.radians(-10), 0, math.radians(20)))
        C.tube('cos_bopi.stalk', [(0, 0, hz + 0.31 * H), (0, 0, hz + 0.42 * H)], 0.014 * H, m('silver'), g)
        rg = C.empty('cos_bopi.halo', g, (0, 0, hz + 0.49 * H), (math.radians(90), 0, 0))
        _ring('cos_bopi.ring', rg, 0, 0.07 * H, 0.07 * H, 0.017 * H, m('amber'))
        C.sphere('cos_bopi.dot', (0, 0, 0), (0.025 * H,) * 3, m('moon'), rg, 16)
    elif cid == 'bolita':
        fh = 0.08 * H
        cz = fh + 0.45 * H
        for k, sx in enumerate((-1, 1)):
            flat(f'cos_bolita.collar{k}', [(0.0, 0.0), (sx * 0.3 * H, 0.0), (sx * 0.4 * H, 0.32 * H), (sx * 0.05 * H, 0.2 * H)], 0.02 * H, m('plum'), g,
                 loc=(sx * 0.05 * H, 0.28 * H, cz - 0.08 * H), rot=(math.radians(-12), 0, math.radians(sx * 22)))
        bt = C.empty('cos_bolita.bow', g, (0, -0.395 * H, cz - 0.27 * H), (math.radians(-35), 0, 0))
        for sx in (-1, 1):
            flat(f'cos_bolita.bow{sx}', [(0.0, 0.0), (sx * 0.1 * H, 0.055 * H), (sx * 0.1 * H, -0.055 * H)], 0.025 * H, m('amber'), bt)
        C.sphere('cos_bolita.knot', (0, -0.01 * H, 0), (0.028 * H, 0.02 * H, 0.03 * H), m('amber'), bt, 16)
    elif cid == 'gruno':
        fh = 0.1 * H
        pk = pumpkin('cos_gruno.pumpkin', g, (0.2 * H, -0.5 * H, fh + 0.34 * H), 0.085 * H)
    return g
