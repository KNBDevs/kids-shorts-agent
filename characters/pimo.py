import bpy, bmesh, math
from mathutils import Vector

DEFAULT = {
    "body": [0.86, 0.30, 0.06], "leaf": [0.02, 0.38, 0.22], "iris": [0.10, 0.035, 0.008],
    "blush": [1.0, 0.38, 0.35], "line": [0.16, 0.06, 0.03],
    "height": 1.30,
    "profile": [(0.00, 0.00), (0.02, 0.22), (0.07, 0.33), (0.18, 0.40), (0.30, 0.41), (0.45, 0.37),
                (0.60, 0.30), (0.72, 0.21), (0.83, 0.14), (0.92, 0.085), (0.98, 0.045), (1.02, 0.0)],
}


def _mat(name, rgb, rough=0.55, sss=0.0, coat=0.0, emit=0.0):
    m = bpy.data.materials.new(name)
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*rgb, 1)
    p.inputs["Roughness"].default_value = rough
    if sss:
        p.inputs["Subsurface Weight"].default_value = sss
        p.inputs["Subsurface Radius"].default_value = (0.4, 0.25, 0.15)
        p.inputs["Subsurface Scale"].default_value = 0.08
    if coat:
        p.inputs["Coat Weight"].default_value = coat
    if emit:
        p.inputs["Emission Color"].default_value = (*rgb, 1)
        p.inputs["Emission Strength"].default_value = emit
    return m


def _catmull(pts, n=80):
    out = []
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = map(Vector, (P[i - 1], P[i], P[i + 1], P[i + 2]))
        for k in range(n // (len(pts) - 1)):
            t = k / (n // (len(pts) - 1))
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(Vector(pts[-1]))
    return out


def _obj(name, mesh, mat, parent):
    o = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(mat)
    o.parent = parent
    for f in o.data.polygons:
        f.use_smooth = True
    return o


def _sphere(name, loc, scale, mat, parent, seg=40):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=1.0)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = _obj(name, me, mat, parent)
    o.location = loc; o.scale = scale
    return o


def _lathe(name, prof, mat, parent, segs=72):
    bm = bmesh.new()
    rings = []
    for z, r in prof:
        ring = [bm.verts.new((r * math.cos(2 * math.pi * k / segs), r * math.sin(2 * math.pi * k / segs), z))
                for k in range(segs)]
        rings.append(ring)
    for a, b in zip(rings, rings[1:]):
        for k in range(segs):
            bm.faces.new((a[k], a[(k + 1) % segs], b[(k + 1) % segs], b[k]))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = _obj(name, me, mat, parent)
    s = o.modifiers.new("sub", "SUBSURF"); s.levels = 1; s.render_levels = 2
    return o


def _tube(name, pts, radius, mat, parent):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"
    cu.bevel_depth = radius; cu.bevel_resolution = 4; cu.use_fill_caps = True
    sp = cu.splines.new("POLY"); sp.points.add(len(pts) - 1)
    for p, c in zip(sp.points, pts):
        p.co = (*c, 1)
    o = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(mat); o.parent = parent
    return o


def _leaf(name, length, width, curl, mat, parent):
    bm = bmesh.new()
    nu, nv = 24, 10
    grid = []
    for i in range(nu + 1):
        u = i / nu
        w = width * math.sin(math.pi * u ** 0.75) ** 0.9
        row = []
        for j in range(nv + 1):
            v = -1 + 2 * j / nv
            x = v * w
            z = u * length
            y = -0.35 * w * (1 - v * v) * 0.5 + curl * u * u
            row.append(bm.verts.new((x, y, z)))
        grid.append(row)
    for i in range(nu):
        for j in range(nv):
            bm.faces.new((grid[i][j], grid[i][j + 1], grid[i + 1][j + 1], grid[i + 1][j]))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = _obj(name, me, mat, parent)
    sol = o.modifiers.new("thick", "SOLIDIFY"); sol.thickness = 0.05; sol.offset = 0
    sub = o.modifiers.new("sub", "SUBSURF"); sub.levels = 1; sub.render_levels = 2
    return o


def build(params=None, location=(0, 0, 0)):
    P = dict(DEFAULT); P.update(params or {})
    H = P["height"]
    prof = [(z * H, r * H) for z, r in _catmull(P["profile"], 120)]

    def radius_at(z):
        for (z0, r0), (z1, r1) in zip(prof, prof[1:]):
            if z0 <= z <= z1:
                return r0 + (r1 - r0) * (z - z0) / max(z1 - z0, 1e-6)
        return 0.0

    def surf_y(x, z):
        r = radius_at(z)
        return -math.sqrt(max(r * r - x * x, 0.0))

    M = {
        "body": _mat("pimo_body", P["body"], rough=0.62, sss=0.25),
        "leaf": _mat("pimo_leaf", P["leaf"], rough=0.5, sss=0.15),
        "white": _mat("pimo_white", (0.97, 0.96, 0.93), rough=0.25),
        "iris": _mat("pimo_iris", P["iris"], rough=0.35, coat=0.3),
        "pupil": _mat("pimo_pupil", (0.02, 0.01, 0.01), rough=0.15, coat=1.0),
        "shine": _mat("pimo_shine", (1, 1, 1), emit=4.0),
        "line": _mat("pimo_line", P["line"], rough=0.6),
        "blush": _mat("pimo_blush", P["blush"], rough=0.8),
    }
    root = bpy.data.objects.new("Pimo", None); bpy.context.scene.collection.objects.link(root)
    root.location = location
    body_rig = bpy.data.objects.new("Pimo.body_rig", None)
    bpy.context.scene.collection.objects.link(body_rig); body_rig.parent = root

    foot_h = 0.1 * H
    body = _lathe("Pimo.body", [(z + foot_h, r) for z, r in prof], M["body"], body_rig)

    def fz(z):
        return z + foot_h

    def place(x, z, out=0.0):
        y = surf_y(x, z)
        ang = math.atan2(x, -y)
        return (x - out * math.sin(ang), y - out * math.cos(ang), fz(z)), ang

    face = bpy.data.objects.new("Pimo.face", None); bpy.context.scene.collection.objects.link(face)
    face.parent = body_rig
    eye_z, eye_x = 0.51 * H, 0.165 * H
    E = 1.3
    for side, sx in (("L", -1), ("R", 1)):
        loc, ang = place(sx * eye_x, eye_z, -0.028 * H)
        eye = bpy.data.objects.new(f"Pimo.eye.{side}", None)
        bpy.context.scene.collection.objects.link(eye); eye.parent = face
        eye.location = loc; eye.rotation_euler = (0, 0, ang)
        _sphere(f"Pimo.eyewhite.{side}", (0, 0, 0), (0.085 * H * E, 0.05 * H, 0.1 * H * E), M["white"], eye)
        _sphere(f"Pimo.iris.{side}", (0, -0.026 * H, -0.004 * H * E), (0.078 * H * E, 0.032 * H, 0.093 * H * E), M["iris"], eye)
        _sphere(f"Pimo.pupil.{side}", (0, -0.05 * H, -0.01 * H * E), (0.042 * H * E, 0.016 * H, 0.052 * H * E), M["pupil"], eye)
        _sphere(f"Pimo.shine.{side}", (-0.024 * H * E, -0.064 * H, 0.032 * H * E), (0.02 * H * E, 0.006 * H, 0.023 * H * E), M["shine"], eye, 20)
        _sphere(f"Pimo.shine2.{side}", (0.026 * H * E, -0.062 * H, -0.038 * H * E), (0.012 * H * E, 0.005 * H, 0.012 * H * E), M["shine"], eye, 16)
        bz = eye_z + 0.175 * H
        brow = [place(sx * eye_x + d * 0.05 * H, bz + 0.014 * H * (1 - d * d), 0.004)[0] for d in (-1, -0.5, 0, 0.5, 1)]
        _tube(f"Pimo.brow.{side}", brow, 0.012 * H, M["line"], face)
        cl, cang = place(sx * 0.285 * H, 0.38 * H, -0.004)
        ch = _sphere(f"Pimo.blush.{side}", cl, (0.055 * H, 0.012 * H, 0.035 * H), M["blush"], face, 24)
        ch.rotation_euler = (0, 0, cang)
    smile = [place(t * 0.065 * H, 0.375 * H - 0.04 * H * (1 - t * t), 0.003)[0] for t in [-1 + 2 * k / 8 for k in range(9)]]
    _tube("Pimo.mouth", smile, 0.012 * H, M["line"], face)

    top = fz(prof[-1][0])
    _tube("Pimo.stem", [(0, 0, top - 0.05 * H), (0, 0, top + 0.03 * H), (0.008 * H, 0, top + 0.07 * H)],
          0.026 * H, M["leaf"], body_rig)
    for name, length, width, rot_y, rot_z in (("L", 0.44 * H, 0.17 * H, -66, 38), ("R", 0.56 * H, 0.2 * H, 30, -38)):
        piv = bpy.data.objects.new(f"Pimo.leafpivot.{name}", None)
        bpy.context.scene.collection.objects.link(piv); piv.parent = body_rig
        piv.location = (0, 0, top + 0.05 * H)
        piv.rotation_euler = (math.radians(-6), math.radians(rot_y), math.radians(rot_z))
        _leaf(f"Pimo.leaf.{name}", length, width, 0.05 * H, M["leaf"], piv)

    # arms
    for side, sx in (("L", -1), ("R", 1)):
        az = 0.27 * H
        ax = sx * (radius_at(az) - 0.05 * H)
        sh = bpy.data.objects.new(f"Pimo.arm.{side}", None)
        bpy.context.scene.collection.objects.link(sh); sh.parent = body_rig
        sh.location = (ax, -0.01 * H, fz(az))
        sh.rotation_euler = (0, math.radians(-sx * 32), 0)
        _sphere(f"Pimo.armmesh.{side}", (sx * 0.05 * H, 0, -0.1 * H), (0.085 * H, 0.09 * H, 0.17 * H), M["body"], sh)

    # feet (on root, so body can squash independently)
    for side, sx in (("L", -1), ("R", 1)):
        _sphere(f"Pimo.foot.{side}", (sx * 0.175 * H, -0.07 * H, 0.065 * H), (0.18 * H, 0.24 * H, 0.1 * H),
                M["body"], root)
    return root
