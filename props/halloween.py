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
