import math
from mathutils import Vector
import common as C

H = 1.3


def _face_kw(**kw):
    base = dict(brow_dz=0.17 * H, brow_w=0.05 * H, mouth_w=0.065 * H, mouth_sag=0.04 * H, blush_x=0.28 * H,
                blush_size=(0.065 * H, 0.04 * H), line_r=0.011 * H, lash=False, look=(0.0, 0.15))
    base.update(kw)
    return base


def pimo(p=None):
    root, rig = C.new_rig("Pimo", H)
    body_m = C.mat("pimo_body", (0.86, 0.30, 0.06), rough=0.62, sss=0.25)
    leaf_m = C.mat("pimo_leaf", (0.02, 0.38, 0.22), rough=0.5, sss=0.15)
    fh = 0.1 * H
    prof = [(fh + z * H, r * H) for z, r in [(0.0, 0.0), (0.02, 0.22), (0.07, 0.33), (0.18, 0.40), (0.30, 0.41), (0.45, 0.37),
                                             (0.60, 0.30), (0.72, 0.21), (0.83, 0.14), (0.92, 0.085), (0.98, 0.045), (1.02, 0.0)]]
    body = C.lathe("Pimo.body", prof, body_m, rig)
    fp = C.face("Pimo", body, C.face_mats("pimo"), rig, eyes_x=0.165 * H, eyes_z=fh + 0.51 * H,
                eye_size=(0.105 * H, 0.128 * H), mouth_z=fh + 0.375 * H, blush_z=fh + 0.38 * H,
                **_face_kw(lash=True, blush_x=0.285 * H))
    top = fh + 1.02 * H
    C.tube("Pimo.stem", [(0, 0, top - 0.05 * H), (0, 0, top + 0.03 * H), (0.008 * H, 0, top + 0.07 * H)], 0.026 * H, leaf_m, rig)
    for nm, ln, wd, ry, rz in (("L", 0.44 * H, 0.17 * H, -66, 38), ("R", 0.56 * H, 0.2 * H, 30, -38)):
        piv = C.empty(f"Pimo.leafpivot.{nm}", rig, (0, 0, top + 0.05 * H), (math.radians(-6), math.radians(ry), math.radians(rz)))
        C.leaf(f"Pimo.leaf.{nm}", ln, wd, 0.05 * H, leaf_m, piv)
    for s, sx in (("L", -1), ("R", 1)):
        C.arm("Pimo", s, rig, (sx * 0.36 * H, -0.01 * H, fh + 0.27 * H), 0.34 * H, 0.085 * H, body_m, out_deg=32)
        C.foot("Pimo", s, root, (sx * 0.175 * H, -0.07 * H, 0.065 * H), (0.18 * H, 0.24 * H, 0.1 * H), body_m)
    return C.result("pimo", root, rig, fp, fh + 1.5 * H, {"body": body, "accent": (0.86, 0.30, 0.06)})


def ruki(p=None):
    root, rig = C.new_rig("Ruki", H)
    body_m = C.mat("ruki_body", (0.17, 0.25, 0.68), rough=0.75, sheen=0.4)
    belly_m = C.mat("ruki_belly", (0.86, 0.80, 0.64), rough=0.8, sheen=0.4)
    fh = 0.08 * H
    prof = [(fh + z * H, r * H) for z, r in [(0, 0), (0.03, 0.34), (0.12, 0.46), (0.3, 0.49), (0.5, 0.455), (0.68, 0.38),
                                             (0.84, 0.28), (0.94, 0.18), (0.99, 0.08), (1.0, 0.0)]]
    body = C.lathe("Ruki.body", prof, body_m, rig, sy=0.86)
    surf = C.Surface(body)
    p0, n0 = surf.hit(0, fh + 0.22 * H)
    belly = C.sphere("Ruki.belly", tuple(p0 + n0 * (-0.065 * H)), (0.33 * H, 0.09 * H, 0.2 * H), belly_m, rig)
    C._orient(belly, n0)
    fp = C.face("Ruki", body, C.face_mats("ruki"), rig, eyes_x=0.17 * H, eyes_z=fh + 0.62 * H,
                eye_size=(0.1 * H, 0.118 * H), mouth_z=fh + 0.53 * H, blush_z=fh + 0.5 * H,
                **_face_kw(brow_dz=0.15 * H, blush_size=None, mouth_w=0.06 * H))
    for k, col in enumerate([(0.03, 0.55, 0.32), (0.95, 0.35, 0.05), (0.95, 0.75, 0.05)]):
        pt, nn = surf.hit(0.3 * H, fh + (0.66 - 0.09 * k) * H)
        if pt is not None:
            C.sphere(f"Ruki.dot.{k}", tuple(pt + nn * 0.004), (0.045 * H, 0.03 * H, 0.045 * H),
                     C.mat(f"ruki_dot{k}", col, rough=0.5), rig, 24)
    for s, sx in (("L", -1), ("R", 1)):
        C.arm("Ruki", s, rig, (sx * 0.43 * H, 0.0, fh + 0.36 * H), 0.3 * H, 0.085 * H, body_m, out_deg=22)
        C.foot("Ruki", s, root, (sx * 0.2 * H, -0.04 * H, 0.05 * H), (0.17 * H, 0.2 * H, 0.08 * H), body_m)
    return C.result("ruki", root, rig, fp, fh + 1.0 * H, {"body": body, "accent": (0.17, 0.25, 0.68)})


def luma(p=None):
    root, rig = C.new_rig("Luma", H)
    body_m = C.mat("luma_body", (1.0, 0.60, 0.04), rough=0.3, sss=0.35, coat=0.4)
    fh = 0.08 * H
    C.sphere("Luma.torso", (0, 0, fh + 0.14 * H), (0.23 * H, 0.2 * H, 0.18 * H), body_m, rig)
    b0 = fh + 0.17 * H
    prof = [(b0 + z * H, r * H) for z, r in [(0, 0), (0.04, 0.28), (0.15, 0.42), (0.3, 0.45), (0.46, 0.4), (0.62, 0.3),
                                             (0.78, 0.2), (0.92, 0.13), (1.04, 0.09), (1.12, 0.07)]]
    head = C.lathe("Luma.body", prof, body_m, rig)
    t = b0 + 1.1 * H
    curl = [(0, 0, t - 0.06 * H), (0.0, 0, t + 0.06 * H), (-0.05 * H, 0, t + 0.15 * H), (-0.14 * H, 0, t + 0.19 * H),
            (-0.22 * H, 0, t + 0.15 * H), (-0.24 * H, 0, t + 0.07 * H), (-0.19 * H, 0, t + 0.03 * H)]
    cobj = C.tube("Luma.curl", C.catmull(curl, 40), 0.075 * H, body_m, rig)
    sp = cobj.data.splines[0]
    npts = len(sp.points)
    for i, pt in enumerate(sp.points):
        pt.radius = 1.0 - 0.45 * i / (npts - 1)
    fp = C.face("Luma", head, C.face_mats("luma", iris=(0.09, 0.035, 0.01), blush=(1.0, 0.45, 0.12)), rig,
                eyes_x=0.17 * H, eyes_z=b0 + 0.33 * H, eye_size=(0.1 * H, 0.12 * H), mouth_z=b0 + 0.19 * H,
                blush_z=b0 + 0.2 * H, **_face_kw(lash=True, brow_dz=0.16 * H, blush_x=0.27 * H, mouth_w=0.05 * H, mouth_sag=0.03 * H))
    for s, sx in (("L", -1), ("R", 1)):
        C.arm("Luma", s, rig, (sx * 0.2 * H, -0.02 * H, fh + 0.2 * H), 0.24 * H, 0.065 * H, body_m, out_deg=50)
        C.foot("Luma", s, root, (sx * 0.12 * H, -0.05 * H, 0.05 * H), (0.13 * H, 0.16 * H, 0.07 * H), body_m)
    return C.result("luma", root, rig, fp, t + 0.2 * H, {"body": head, "accent": (1.0, 0.6, 0.04)})


def tuki(p=None):
    root, rig = C.new_rig("Tuki", H)
    body_m = C.mat("tuki_body", (0.02, 0.62, 0.60), rough=0.45, coat=0.2)
    leg_m = C.mat("tuki_leg", (0.10, 0.15, 0.24), rough=0.6)
    shoe_m = C.mat("tuki_shoe", (1.0, 0.24, 0.20), rough=0.55)
    C.sphere("Tuki.seg.0", (0, 0, 0.4 * H), (0.34 * H, 0.31 * H, 0.17 * H), body_m, rig)
    C.sphere("Tuki.seg.1", (0, 0, 0.65 * H), (0.35 * H, 0.32 * H, 0.16 * H), body_m, rig)
    head = C.sphere("Tuki.head", (0, 0, 1.03 * H), (0.36 * H, 0.33 * H, 0.32 * H), body_m, rig, 56)
    fp = C.face("Tuki", head, C.face_mats("tuki", iris=(0.015, 0.012, 0.012), blush=(0.55, 0.65, 0.85)), rig,
                eyes_x=0.15 * H, eyes_z=1.07 * H, eye_size=(0.1 * H, 0.115 * H), mouth_z=0.93 * H, blush_z=0.94 * H,
                **_face_kw(brow_dz=0.15 * H, blush_x=0.22 * H, blush_size=(0.05 * H, 0.03 * H), mouth_w=0.05 * H))
    for s, sx in (("L", -1), ("R", 1)):
        C.tube(f"Tuki.armline.{s}", [(sx * 0.3 * H, 0, 0.7 * H), (sx * 0.42 * H, -0.02 * H, 0.6 * H), (sx * 0.5 * H, -0.03 * H, 0.52 * H)],
               0.05 * H, body_m, rig)
        C.sphere(f"Tuki.hand.{s}", (sx * 0.52 * H, -0.03 * H, 0.5 * H), (0.085 * H, 0.08 * H, 0.08 * H), body_m, rig)
        C.tube(f"Tuki.leg.{s}", [(sx * 0.13 * H, 0, 0.3 * H), (sx * 0.13 * H, 0, 0.08 * H)], 0.07 * H, leg_m, root)
        C.foot("Tuki", s, root, (sx * 0.16 * H, -0.06 * H, 0.07 * H), (0.19 * H, 0.24 * H, 0.1 * H), shoe_m)
    return C.result("tuki", root, rig, fp, 1.36 * H, {"body": head, "accent": (0.02, 0.62, 0.6)})


def moki(p=None):
    root, rig = C.new_rig("Moki", H)
    body_m = C.mat("moki_body", (0.48, 0.38, 0.86), rough=0.9, sheen=1.0)
    fh = 0.07 * H
    balls = [((0, 0, fh + 0.45 * H), 0.42 * H, (1, 1, 1)), ((-0.33 * H, 0.0, fh + 0.52 * H), 0.3 * H, (1, 1, 1)),
             ((0.34 * H, 0.04 * H, fh + 0.44 * H), 0.28 * H, (1, 1, 1)), ((-0.1 * H, 0.02 * H, fh + 0.76 * H), 0.3 * H, (1, 1, 1)),
             ((0.17 * H, 0.04 * H, fh + 0.72 * H), 0.28 * H, (1, 1, 1)), ((0.0, 0.12 * H, fh + 0.5 * H), 0.36 * H, (1, 1, 1))]
    body = C.metablob("Moki.body", balls, body_m, rig)
    fp = C.face("Moki", body, C.face_mats("moki", iris=(0.2, 0.06, 0.35), blush=(1.0, 0.45, 0.6)), rig,
                eyes_x=0.15 * H, eyes_z=fh + 0.5 * H, eye_size=(0.075 * H, 0.09 * H), mouth_z=fh + 0.38 * H,
                blush_z=fh + 0.4 * H, **_face_kw(brow_dz=0.14 * H, blush_x=0.25 * H, mouth_w=0.05 * H, mouth_sag=0.03 * H))
    sp, sn = fp["surface"].hit(-0.36 * H, fh + 0.56 * H)
    swg = C.empty("Moki.swirl_rig", rig); swg.location = sp; C._orient(swg, sn)
    sw = []
    for k in range(48):
        a = k / 47 * 1.75 * 2 * math.pi
        r = 0.13 * H * (1 - k / 54)
        sw.append((r * math.cos(a), -0.012 * H - 0.025 * H * (1 - k / 47), r * math.sin(a)))
    C.tube("Moki.swirl", sw[::-1], 0.04 * H, body_m, swg)
    for s, sx in (("L", -1), ("R", 1)):
        C.arm("Moki", s, rig, (sx * 0.4 * H, -0.05 * H, fh + 0.28 * H), 0.22 * H, 0.075 * H, body_m, out_deg=18)
        C.foot("Moki", s, root, (sx * 0.15 * H, -0.03 * H, 0.05 * H), (0.12 * H, 0.15 * H, 0.08 * H), body_m)
    return C.result("moki", root, rig, fp, fh + 1.0 * H, {"body": body, "accent": (0.48, 0.38, 0.86)})


def bopi(p=None):
    root, rig = C.new_rig("Bopi", H)
    cream = C.mat("bopi_cream", (0.88, 0.80, 0.64), rough=0.4, coat=0.3)
    navy = C.mat("bopi_navy", (0.025, 0.035, 0.09), rough=0.35, coat=0.4)
    orange = C.mat("bopi_orange", (0.95, 0.30, 0.04), rough=0.4, coat=0.3)
    hz = 0.98 * H
    head = C.sphere("Bopi.head", (0, 0, hz), (0.42 * H, 0.37 * H, 0.34 * H), cream, rig, 64)
    visor = C.rounded_box("Bopi.visor", (0, -0.31 * H, hz - 0.01 * H), (0.6 * H, 0.16 * H, 0.34 * H), 0.07 * H, navy, rig)
    fm = C.face_mats("bopi", iris=(0.02, 0.03, 0.08), line=(0.95, 0.95, 0.95))
    fm["white"] = C.mat("bopi_eyewhite", (0.97, 0.97, 0.97), rough=0.2)
    fp = C.face("Bopi", visor, fm, rig, eyes_x=0.14 * H, eyes_z=hz + 0.01 * H, eye_size=(0.085 * H, 0.1 * H),
                mouth_z=hz - 0.1 * H, blush_z=hz, **_face_kw(sclera=1.12, brows=False, blush_size=None, mouth_w=0.04 * H, mouth_sag=0.022 * H,
                                                              line_r=0.009 * H, look=(0.0, 0.25)))
    kn = C.empty("Bopi.knob", rig, (-0.41 * H, 0, hz), (0, math.radians(90), 0))
    C.sphere("Bopi.knobmesh", (0, 0, 0), (0.13 * H, 0.13 * H, 0.05 * H), orange, kn)
    C.rounded_box("Bopi.knobslot", (0, 0, -0.045 * H), (0.12 * H, 0.025 * H, 0.02 * H), 0.008 * H, C.mat("bopi_slot", (0.6, 0.15, 0.02)), kn)
    prof = [(0.2 * H + z * H, r * H) for z, r in [(0, 0), (0.03, 0.2), (0.12, 0.27), (0.25, 0.28), (0.38, 0.24), (0.48, 0.16), (0.52, 0.0)]]
    C.lathe("Bopi.torso", prof, cream, rig)
    for s, sx in (("L", -1), ("R", 1)):
        a = C.empty(f"Bopi.arm.{s}", rig, (sx * 0.27 * H, 0, 0.6 * H), (0, math.radians(-sx * 18), 0))
        for k in range(3):
            C.sphere(f"Bopi.armseg.{s}{k}", (sx * 0.02 * H, 0, -(0.05 + 0.08 * k) * H), (0.055 * H, 0.055 * H, 0.05 * H), navy, a, 24)
        C.sphere(f"Bopi.hand.{s}", (sx * 0.03 * H, 0, -0.33 * H), (0.085 * H, 0.08 * H, 0.09 * H), cream, a)
        for k in range(2):
            C.sphere(f"Bopi.legseg.{s}{k}", (sx * 0.11 * H, 0, (0.19 - 0.06 * k) * H), (0.055 * H, 0.055 * H, 0.04 * H), navy, root, 24)
        C.sphere(f"Bopi.boot.{s}", (sx * 0.12 * H, -0.04 * H, 0.07 * H), (0.13 * H, 0.17 * H, 0.08 * H), cream, root)
        C.sphere(f"Bopi.sole.{s}", (sx * 0.12 * H, -0.04 * H, 0.025 * H), (0.135 * H, 0.175 * H, 0.025 * H), navy, root)
    return C.result("bopi", root, rig, fp, hz + 0.3 * H, {"body": head, "accent": (0.95, 0.3, 0.04)})


def bolita(p=None):
    import bmesh
    root, rig = C.new_rig("Bolita", H)
    red = C.mat("bolita_body", (0.78, 0.025, 0.02), rough=0.3, coat=0.5)
    yel = C.mat("bolita_gem", (1.0, 0.62, 0.03), rough=0.3, coat=0.5)
    fh = 0.08 * H
    cz = fh + 0.45 * H
    body = C.sphere("Bolita.body", (0, 0, cz), (0.47 * H, 0.44 * H, 0.45 * H), red, rig, 64)
    fp = C.face("Bolita", body, C.face_mats("bolita", iris=(0.01, 0.01, 0.012), blush=(1.0, 0.45, 0.55)), rig,
                eyes_x=0.15 * H, eyes_z=cz + 0.05 * H, eye_size=(0.11 * H, 0.13 * H), mouth_z=cz - 0.1 * H, blush_z=cz - 0.08 * H,
                **_face_kw(brow_dz=0.18 * H, blush_x=0.27 * H, mouth_w=0.05 * H, mouth_sag=0.03 * H, sclera=1.05))
    top = cz + 0.45 * H
    pts = C.catmull([(0, 0, top - 0.03 * H), (0.03 * H, 0, top + 0.18 * H), (0.13 * H, 0, top + 0.3 * H), (0.26 * H, 0, top + 0.31 * H)], 24)
    C.tube("Bolita.antenna", pts, 0.032 * H, red, rig)
    bm = bmesh.new()
    vs = [bm.verts.new(v) for v in [(0, 0, 1), (0, 0, -1), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]]
    for a, b in ((2, 4), (4, 3), (3, 5), (5, 2)):
        bm.faces.new((vs[0], vs[a], vs[b])); bm.faces.new((vs[1], vs[b], vs[a]))
    gem = C.mesh_obj("Bolita.gem", bm, yel, rig, smooth=False)
    gem.location = (0.34 * H, 0, top + 0.3 * H); gem.scale = (0.14 * H, 0.14 * H, 0.17 * H)
    gem.rotation_euler = (0, math.radians(-25), math.radians(45))
    bv = gem.modifiers.new("bev", "BEVEL"); bv.width = 0.08; bv.segments = 3
    for s, sx in (("L", -1), ("R", 1)):
        C.arm("Bolita", s, rig, (sx * 0.44 * H, -0.02 * H, cz - 0.04 * H), 0.24 * H, 0.085 * H, red, out_deg=72)
        C.foot("Bolita", s, root, (sx * 0.18 * H, -0.06 * H, 0.055 * H), (0.16 * H, 0.2 * H, 0.09 * H), red)
    return C.result("bolita", root, rig, fp, top + 0.45 * H, {"body": body, "accent": (0.78, 0.025, 0.02)})


def gruno(p=None):
    root, rig = C.new_rig("Gruno", H)
    purple = C.mat("gruno_body", (0.24, 0.05, 0.42), rough=0.8, sheen=0.5)
    teal = C.mat("gruno_coat", (0.02, 0.22, 0.26), rough=0.75, sheen=0.4)
    cream = C.mat("gruno_belly", (0.85, 0.76, 0.58), rough=0.8)
    orange = C.mat("gruno_orange", (0.95, 0.28, 0.03), rough=0.45, coat=0.3)
    lime = C.mat("gruno_lime", (0.45, 0.65, 0.04), rough=0.4, coat=0.4)
    glass = C.mat("gruno_glass", (0.01, 0.08, 0.1), rough=0.05, coat=1.0)
    brow_m = C.mat("gruno_brow", (0.09, 0.015, 0.16), rough=0.8)
    fh = 0.1 * H
    P = [(0, 0), (0.03, 0.4), (0.12, 0.52), (0.28, 0.55), (0.45, 0.52), (0.62, 0.45), (0.78, 0.34), (0.9, 0.22), (0.97, 0.11), (1.0, 0.0)]
    body = C.lathe("Gruno.body", [(fh + z * H, r * H) for z, r in P], purple, rig, sy=0.86)
    coat = C.lathe("Gruno.coat", [(fh + z * H, r * H * 1.03) for z, r in P[:5]] + [(fh + 0.47 * H, 0.0)], teal, rig, sy=0.86)
    import bmesh as _b0
    bt = _b0.new(); _b0.ops.create_circle(bt, cap_ends=False, segments=64, radius=1.0)
    col = C.mesh_obj("Gruno.collar", bt, None, rig)
    import bpy as _bp
    _bp.data.objects.remove(col)
    rr = 0.52 * H * 1.03
    ring = [(rr * math.cos(2 * math.pi * k / 64), 0.86 * rr * math.sin(2 * math.pi * k / 64), fh + 0.45 * H) for k in range(65)]
    C.tube("Gruno.collar", ring, 0.045 * H, teal, rig)
    surf = C.Surface(body)
    pb, nb = surf.hit(0, fh + 0.2 * H)
    bel = C.sphere("Gruno.belly", tuple(pb + nb * (-0.05 * H)), (0.3 * H, 0.1 * H, 0.22 * H), cream, rig)
    C._orient(bel, nb)
    pbt, nbt = surf.hit(0, fh + 0.43 * H)
    C.sphere("Gruno.button", tuple(pbt + nbt * 0.04 * H), (0.06 * H, 0.025 * H, 0.06 * H), orange, rig, 32)
    fm = C.face_mats("gruno", iris=(0.62, 0.22, 0.02), line=(0.09, 0.015, 0.16))
    fp = C.face("Gruno", body, fm, rig, eyes_x=0.19 * H, eyes_z=fh + 0.72 * H, eye_size=(0.11 * H, 0.1 * H),
                mouth_z=fh + 0.58 * H, blush_z=0, **_face_kw(brows=False, blush_size=None, mouth_w=0.12 * H,
                                                             mouth_sag=0.035 * H, line_r=0.012 * H, look=(0.35, -0.1),
                                                             shine=(-0.28, -0.2), shine2=False))
    for side, e in zip(("L", "R"), fp["eyes"]):
        C.lid("Gruno", side, e, 0.11 * H, 0.1 * H, purple, closed=0.42 if side == "L" else 0.5)
    # asymmetric thick brows: left arched, right lowered toward the centre (cheeky look)
    bl = [surf.point(-0.19 * H + t * 0.09 * H, fh + 0.815 * H + 0.03 * H * (1 - t * t) + 0.01 * H * t, 0.022 * H) for t in (-1, -0.5, 0, 0.5, 1)]
    br = [surf.point(0.19 * H + t * 0.09 * H, fh + 0.79 * H - 0.025 * H * t + 0.012 * H * (1 - t * t), 0.022 * H) for t in (-1, -0.5, 0, 0.5, 1)]
    C.tube("Gruno.brow.L", bl, 0.034 * H, brow_m, fp["face"], radii=[0.6, 1, 1.1, 1, 0.6])
    C.tube("Gruno.brow.R", br, 0.034 * H, brow_m, fp["face"], radii=[0.6, 1, 1.1, 1, 0.6])
    # lopsided smirk replaces the default mouth
    import bpy as _bpy
    _bpy.data.objects.remove(fp["mouth"])
    sm = [surf.point(t * 0.12 * H, fh + 0.58 * H - 0.035 * H * (1 - t * t) + 0.03 * H * max(t, 0) ** 2, 0.004) for t in [-1 + 2 * k / 10 for k in range(11)]]
    fp["mouth"] = C.tube("Gruno.mouth", sm, 0.013 * H, fm["line"], fp["face"], radii=[0.5] + [1] * 9 + [0.7])
    # goggles on the forehead: two unequal lime rings with dark lenses
    gg = C.empty("Gruno.goggles", rig)
    for k, (gx, r) in enumerate(((-0.15 * H, 0.15 * H), (0.17 * H, 0.18 * H))):
        gp, gn = surf.hit(gx * 0.85, fh + 0.9 * H)
        if gp is None:
            continue
        g = C.empty(f"Gruno.goggle.{k}", gg); g.location = gp + gn * 0.06 * H + Vector((gx * 0.15, 0, 0.07 * H)); C._orient(g, (gn + Vector((0, -0.6, 0))).normalized())
        import bmesh as _bm
        b = _bm.new(); _bm.ops.create_cone(b, cap_ends=True, segments=48, radius1=1, radius2=1, depth=1)
        ring = C.mesh_obj(f"Gruno.goggle_ring.{k}", b, lime, g)
        ring.rotation_euler = (math.radians(90), 0, 0); ring.scale = (r, r, 0.07 * H)
        bv = ring.modifiers.new("bev", "BEVEL"); bv.width = 0.02 * H; bv.segments = 4
        C.sphere(f"Gruno.lens.{k}", (0, -0.045 * H, 0), (r * 0.72, 0.03 * H, r * 0.72), glass, g)
    # tufts
    top = fh + 1.0 * H
    for nm, d in (("L", -1), ("R", 1)):
        o = 0.05 * H if nm == "L" else 0.17 * H
        pts = C.catmull([(o - 0.08 * H, 0.06 * H, top - 0.14 * H), (o - 0.03 * H, 0.08 * H, top + 0.0 * H),
                         (o + 0.06 * H, 0.12 * H, top + 0.1 * H), (o + 0.16 * H, 0.16 * H, top + 0.13 * H)], 30)
        t = C.tube(f"Gruno.tuft.{nm}", pts, 0.1 * H, purple, rig)
        n = len(t.data.splines[0].points)
        for i, pt in enumerate(t.data.splines[0].points):
            pt.radius = 1.0 - 0.9 * i / (n - 1)
    for s, sx in (("L", -1), ("R", 1)):
        arm = C.arm("Gruno", s, rig, (sx * 0.5 * H, -0.02 * H, fh + 0.4 * H), 0.3 * H, 0.095 * H, purple,
                    out_deg=(135 if s == "L" else 30), fwd_deg=(-25 if s == "L" else 0))
        if s == "L":
            hand_arm = arm
        C.foot("Gruno", s, root, (sx * 0.22 * H, -0.06 * H, 0.06 * H), (0.2 * H, 0.26 * H, 0.1 * H), teal)
    # optional remote in the raised hand
    rem = C.empty("Gruno.remote", hand_arm, (-0.03 * H, -0.05 * H, -0.36 * H), (0, math.radians(-135), 0))
    C.sphere("Gruno.remote_body", (0, 0, 0), (0.07 * H, 0.05 * H, 0.1 * H), orange, rem)
    C.sphere("Gruno.remote_btn", (0, -0.045 * H, 0.015 * H), (0.035 * H, 0.015 * H, 0.035 * H), C.mat("gruno_btn", (0.25, 0.75, 0.45), rough=0.3), rem, 24)
    return C.result("gruno", root, rig, fp, top + 0.3 * H, {"body": body, "accent": (0.24, 0.05, 0.42)})


ROSTER = {"pimo": pimo, "ruki": ruki, "luma": luma, "tuki": tuki, "moki": moki, "bopi": bopi, "bolita": bolita, "gruno": gruno}


def build(name, params=None):
    return ROSTER[name](params)
