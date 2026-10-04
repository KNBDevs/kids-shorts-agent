import bpy, bmesh, math
from mathutils import Vector

def mat(name, rgb, rough=0.55, sss=0.0, coat=0.0, emit=0.0, sheen=0.0, metal=0.0):
    m = bpy.data.materials.new(name)
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*rgb, 1)
    p.inputs['Roughness'].default_value = rough
    if metal:
        p.inputs['Metallic'].default_value = metal
    if sss:
        p.inputs['Subsurface Weight'].default_value = sss
        p.inputs['Subsurface Radius'].default_value = (0.4, 0.25, 0.15)
        p.inputs['Subsurface Scale'].default_value = 0.08
    if coat:
        p.inputs['Coat Weight'].default_value = coat
    if sheen:
        p.inputs['Sheen Weight'].default_value = sheen
        p.inputs['Sheen Tint'].default_value = (1, 1, 1, 1)
    if emit:
        p.inputs['Emission Color'].default_value = (*rgb, 1)
        p.inputs['Emission Strength'].default_value = emit
    return m

def link(o, parent=None):
    bpy.context.scene.collection.objects.link(o)
    if parent:
        o.parent = parent
    return o

def empty(name, parent=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    o = link(bpy.data.objects.new(name, None), parent)
    o.location = loc
    o.rotation_euler = rot
    return o

def mesh_obj(name, bm, material, parent, smooth=True, subsurf=0):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = link(bpy.data.objects.new(name, me), parent)
    if material:
        o.data.materials.append(material)
    if smooth:
        for f in o.data.polygons:
            f.use_smooth = True
    if subsurf:
        s = o.modifiers.new('sub', 'SUBSURF')
        s.levels = subsurf
        s.render_levels = subsurf + 1
    return o

def sphere(name, loc, scale, material, parent, seg=40, rot=(0, 0, 0)):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=1.0)
    o = mesh_obj(name, bm, material, parent)
    o.location = loc
    o.scale = scale
    o.rotation_euler = rot
    return o

def rounded_box(name, loc, size, bevel, material, parent):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    o = mesh_obj(name, bm, material, parent, smooth=True)
    o.location = loc
    o.scale = size
    b = o.modifiers.new('bev', 'BEVEL')
    b.width = bevel
    b.segments = 6
    b.limit_method = 'NONE'
    b.affect = 'EDGES'
    s = o.modifiers.new('sub', 'SUBSURF')
    s.levels = 1
    s.render_levels = 2
    return o

def catmull(pts, n=120):
    out = []
    P = [pts[0]] + list(pts) + [pts[-1]]
    per = max(n // (len(pts) - 1), 2)
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = map(Vector, (P[i - 1], P[i], P[i + 1], P[i + 2]))
        for k in range(per):
            t = k / per
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(Vector(pts[-1]))
    return [tuple(v) for v in out]

def lathe(name, profile, material, parent, segs=72, sx=1.0, sy=1.0):
    prof = catmull(profile, 140)
    bm = bmesh.new()
    rings = []
    for z, r in prof:
        rings.append([bm.verts.new((sx * r * math.cos(2 * math.pi * k / segs), sy * r * math.sin(2 * math.pi * k / segs), z)) for k in range(segs)])
    for a, b in zip(rings, rings[1:]):
        for k in range(segs):
            bm.faces.new((a[k], a[(k + 1) % segs], b[(k + 1) % segs], b[k]))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return mesh_obj(name, bm, material, parent, subsurf=1)

def metablob(name, balls, material, parent, voxel=0.018):
    bm = bmesh.new()
    for c, r, s in balls:
        res = bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=r)
        for v in res['verts']:
            v.co = Vector((v.co.x * s[0] + c[0], v.co.y * s[1] + c[1], v.co.z * s[2] + c[2]))
    o = mesh_obj(name, bm, material, parent)
    rm = o.modifiers.new('remesh', 'REMESH')
    rm.mode = 'VOXEL'
    rm.voxel_size = voxel
    sm = o.modifiers.new('smooth', 'CORRECTIVE_SMOOTH')
    sm.iterations = 12
    sm.factor = 0.8
    sm.smooth_type = 'LENGTH_WEIGHTED'
    sm.use_only_smooth = True
    sh = o.modifiers.new('shade', 'SMOOTH')
    sh.factor = 0.6
    sh.iterations = 8
    for p in o.data.polygons:
        p.use_smooth = True
    return o

def tube(name, pts, radius, material, parent, radii=None, res=6):
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = radius
    cu.bevel_resolution = res
    cu.use_fill_caps = True
    sp = cu.splines.new('POLY')
    sp.points.add(len(pts) - 1)
    for i, (p, c) in enumerate(zip(sp.points, pts)):
        p.co = (*c, 1)
        if radii:
            p.radius = radii[i]
    o = link(bpy.data.objects.new(name, cu), parent)
    o.data.materials.append(material)
    return o

def leaf(name, length, width, curl, material, parent, thick=0.05):
    bm = bmesh.new()
    nu, nv = (24, 10)
    grid = []
    for i in range(nu + 1):
        u = i / nu
        w = width * math.sin(math.pi * u ** 0.75) ** 0.9
        row = []
        for j in range(nv + 1):
            v = -1 + 2 * j / nv
            row.append(bm.verts.new((v * w, -0.35 * w * (1 - v * v) * 0.5 + curl * u * u, u * length)))
        grid.append(row)
    for i in range(nu):
        for j in range(nv):
            bm.faces.new((grid[i][j], grid[i][j + 1], grid[i + 1][j + 1], grid[i + 1][j]))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-05)
    o = mesh_obj(name, bm, material, parent)
    sol = o.modifiers.new('thick', 'SOLIDIFY')
    sol.thickness = thick
    sol.offset = 0
    s = o.modifiers.new('sub', 'SUBSURF')
    s.levels = 1
    s.render_levels = 2
    return o

class Surface:

    def __init__(self, body):
        bpy.context.view_layer.update()
        self.obj = body
        self.dg = bpy.context.evaluated_depsgraph_get()
        self.mw = body.matrix_world.copy()
        self.inv = self.mw.inverted()

    def hit(self, x, z):
        o = self.inv @ Vector((x, -50.0, z))
        d = (self.inv.to_3x3() @ Vector((0, 1, 0))).normalized()
        ok, loc, nrm, _ = self.obj.evaluated_get(self.dg).ray_cast(o, d)
        if not ok:
            return (None, None)
        p = self.mw @ loc
        n = (self.mw.to_3x3() @ nrm).normalized()
        return (p, n)

    def point(self, x, z, out=0.0):
        p, n = self.hit(x, z)
        return tuple(p + n * out) if p else (x, 0, z)

def recenter_curve(o):
    pts = [p.co for sp in o.data.splines for p in sp.points]
    cx = sum((p[0] for p in pts)) / len(pts)
    cy = sum((p[1] for p in pts)) / len(pts)
    cz = sum((p[2] for p in pts)) / len(pts)
    for sp in o.data.splines:
        for p in sp.points:
            p.co = (p.co[0] - cx, p.co[1] - cy, p.co[2] - cz, p.co[3])
    o.location = (o.location[0] + cx, o.location[1] + cy, o.location[2] + cz)
    return o

def _orient(o, n, roll=0.0):
    q = Vector((0, -1, 0)).rotation_difference(n)
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = q
    return o

def eye(prefix, side, surf, x, z, size, mats, parent, look=(0.0, 0.0), lash=False, depth_in=0.35, sclera=1.0, shine=(-0.3, 0.34), shine2=True):
    a, b = size
    p, n = surf.hit(x, z)
    if p is None:
        return None
    g = empty(f'{prefix}.eye.{side}', parent)
    g.location = p + n * (-a * depth_in)
    _orient(g, n)
    lx, lz = look
    sphere(f'{prefix}.eyewhite.{side}', (0, 0, 0), (a * sclera, a * 0.6, b * sclera), mats['white'], g)
    ir = empty(f'{prefix}.iris_rig.{side}', g, (lx * a * 0.18, 0, lz * b * 0.15))
    sphere(f'{prefix}.iris.{side}', (0, -a * 0.34, -b * 0.04), (a * 0.82, a * 0.36, b * 0.86), mats['iris'], ir)
    sphere(f'{prefix}.pupil.{side}', (0, -a * 0.6, -b * 0.06), (a * 0.46, a * 0.14, b * 0.5), mats['pupil'], ir)
    sphere(f'{prefix}.shine.{side}', (a * shine[0], -a * 0.74, b * shine[1]), (a * 0.22, a * 0.05, b * 0.23), mats['shine'], ir, 20)
    if shine2:
        sphere(f'{prefix}.shine2.{side}', (a * 0.3, -a * 0.68, -b * 0.36), (a * 0.11, a * 0.04, b * 0.11), mats['shine'], ir, 16)
    if lash:
        sx = 1 if side == 'R' else -1
        pts = [(sx * a * 0.72, -a * 0.3, b * 0.62), (sx * a * 0.95, -a * 0.32, b * 0.82), (sx * a * 1.12, -a * 0.3, b * 0.86)]
        tube(f'{prefix}.lash.{side}', pts, a * 0.05, mats['line'], g, radii=[1.0, 0.8, 0.35])
    return g

def arc(prefix, surf, cx, cz, half_w, sag, n=9, out=0.004):
    pts = []
    for k in range(n):
        t = -1 + 2 * k / (n - 1)
        pts.append(surf.point(cx + t * half_w, cz - sag * (1 - t * t), out))
    return pts

def face(prefix, body, mats, parent, eyes_x, eyes_z, eye_size, brow_dz, brow_w, mouth_z, mouth_w, mouth_sag, blush_x, blush_z, blush_size, line_r, lash=False, look=(0.0, 0.15), open_mouth=False, brows=True, sclera=1.0, shine=(-0.3, 0.34), shine2=True):
    surf = Surface(body)
    f = empty(f'{prefix}.face', parent)
    eyes = []
    for side, sx in (('L', -1), ('R', 1)):
        e = eye(prefix, side, surf, sx * eyes_x, eyes_z, eye_size, mats, f, look=(look[0], look[1]), lash=lash, sclera=sclera, shine=shine, shine2=shine2)
        eyes.append(e)
        if brows:
            pts = arc(prefix, surf, sx * eyes_x, eyes_z + brow_dz + brow_w * 0.25, brow_w, -brow_w * 0.28, 5)
            tube(f'{prefix}.brow.{side}', pts, line_r, mats['line'], f, radii=[0.55, 0.9, 1, 0.9, 0.55])
        if blush_size:
            p, n = surf.hit(sx * blush_x, blush_z)
            if p is not None:
                bl = sphere(f'{prefix}.blush.{side}', tuple(p + n * 0.002), (blush_size[0], blush_size[0] * 0.18, blush_size[1]), mats['blush'], f, 24)
                _orient(bl, n)
    pts = arc(prefix, surf, 0.0, mouth_z, mouth_w, mouth_sag, 11, out=0.003)
    mouth = tube(f'{prefix}.mouth', pts, line_r * 1.05, mats['line'], f, radii=[0.6] + [1.0] * 9 + [0.6])
    recenter_curve(mouth)
    return {'eyes': eyes, 'mouth': mouth, 'face': f, 'surface': surf}

def face_mats(prefix, iris=(0.05, 0.02, 0.006), line=(0.14, 0.05, 0.03), blush=(1.0, 0.36, 0.36), white=(0.98, 0.97, 0.95)):
    return {'white': mat(f'{prefix}_white', white, rough=0.25), 'iris': mat(f'{prefix}_iris', iris, rough=0.4), 'pupil': mat(f'{prefix}_pupil', (0.012, 0.008, 0.006), rough=0.2), 'shine': mat(f'{prefix}_shine', (1, 1, 1), emit=5.0), 'line': mat(f'{prefix}_line', line, rough=0.6), 'blush': mat(f'{prefix}_blush', blush, rough=0.85)}

def arm(prefix, side, parent, shoulder, length, radius, material, out_deg=30, fwd_deg=0, hand=None):
    sx = -1 if side == 'L' else 1
    g = empty(f'{prefix}.arm.{side}', parent, shoulder, (math.radians(fwd_deg), math.radians(-sx * out_deg), 0))
    sphere(f'{prefix}.armmesh.{side}', (sx * radius * 0.3, 0, -length * 0.5), (radius, radius * 1.05, length * 0.6), material, g)
    return g

def foot(prefix, side, parent, loc, size, material, sole=None):
    o = sphere(f'{prefix}.foot.{side}', loc, size, material, parent)
    return o

def new_rig(name, height):
    root = empty(name)
    rig = empty(f'{name}.body_rig', root)
    return (root, rig)

def result(name, root, rig, face_parts, height, extra=None):
    d = {'name': name, 'root': root, 'rig': rig, 'height': height}
    d.update(face_parts)
    d.update(extra or {})
    return d

def key(o, path, f, val):
    attr = getattr(o, path)
    if hasattr(attr, '__len__'):
        for i, v in enumerate(val):
            attr[i] = v
    else:
        setattr(o, path, val)
    o.keyframe_insert(path, frame=f)

def blink(ch, f, dur=4):
    for e in ch['eyes']:
        if e is None:
            continue
        key(e, 'scale', f - 1, (1, 1, 1))
        key(e, 'scale', f + dur // 2, (1, 1, 0.08))
        key(e, 'scale', f + dur, (1, 1, 1))

def talk(ch, f0, syllables, step=4):
    m = ch['mouth']
    base = tuple(m.scale)
    key(m, 'scale', f0 - 1, base)
    for k in range(syllables):
        key(m, 'scale', f0 + k * step, (base[0] * 1.15, base[1], base[2] * 2.2))
        key(m, 'scale', f0 + k * step + step // 2, (base[0], base[1], base[2] * 0.9))
    key(m, 'scale', f0 + syllables * step + 1, base)

def wave(ch, side, f0, cycles=3, period=8, amp=55):
    arm = next((o for o in ch['rig'].children if o.name.endswith(f'.arm.{side}')), None)
    if arm is None:
        return
    rest = tuple(arm.rotation_euler)
    sx = -1 if side == 'L' else 1
    key(arm, 'rotation_euler', f0 - 1, rest)
    for c in range(cycles):
        for k, a in enumerate((amp, amp * 0.55)):
            key(arm, 'rotation_euler', f0 + c * period + k * period // 2 + 3, (rest[0], rest[1] + math.radians(-sx * (120 + (a - amp))), rest[2]))
    key(arm, 'rotation_euler', f0 + cycles * period + 6, rest)

def lid(prefix, side, eye_grp, a, b, material, closed=0.45):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=40, v_segments=20, radius=1.0)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -0.02], context='VERTS')
    piv = empty(f'{prefix}.lid_rig.{side}', eye_grp)
    o = mesh_obj(f'{prefix}.lid.{side}', bm, material, piv)
    o.scale = (a * 1.1, a * 0.86, b * 1.1)
    sol = o.modifiers.new('t', 'SOLIDIFY')
    sol.thickness = 0.04
    sol.offset = 1
    piv.rotation_euler = (math.radians((closed - 0.5) * 180), 0, 0)
    return piv
