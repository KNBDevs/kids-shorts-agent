import bpy, math, os, sys, random
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'characters'))
import roster, common as C
from intro_plan import *
import json
try:
    MAN = json.load(open(os.path.join(HERE, 'assets', 'vo', 'manifest.json')))
except Exception:
    MAN = {}
random.seed(11)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.frame_start, sc.frame_end = (0, TOTAL - 1)
sc.render.fps = FPS
K = C.key

def set_interp(idb, mode):
    ad = idb.animation_data
    if not ad or not ad.action:
        return
    act = ad.action
    curves = list(getattr(act, 'fcurves', []))
    if not curves:
        for layer in act.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    curves += list(bag.fcurves)
    for fc in curves:
        for k in fc.keyframe_points:
            k.interpolation = mode
w = bpy.data.worlds.new('W')
sc.world = w
w.node_tree.nodes['Background'].inputs[0].default_value = (0.6, 0.75, 1.0, 1)
w.node_tree.nodes['Background'].inputs[1].default_value = 0.5
bpy.ops.object.light_add(type='SUN', rotation=(math.radians(50), math.radians(-20), math.radians(-30)))
sun = bpy.context.object
sun.data.energy = 3.0
sun.data.color = (1, 0.95, 0.88)
sun.data.angle = math.radians(10)
for loc, rot, e, s in [((-5, -10, 7), (55, 0, -25), 900, 8), ((5, -6, 5), (60, 0, 40), 350, 6), ((0, 9, 6), (-55, 0, 0), 450, 6)]:
    bpy.ops.object.light_add(type='AREA', location=loc, rotation=tuple((math.radians(r) for r in rot)))
    bpy.context.object.data.energy = e
    bpy.context.object.data.size = s
sky_m = bpy.data.materials.new('Sky')
nt = sky_m.node_tree
nt.nodes.clear()
out = nt.nodes.new('ShaderNodeOutputMaterial')
em = nt.nodes.new('ShaderNodeEmission')
ramp = nt.nodes.new('ShaderNodeValToRGB')
tco = nt.nodes.new('ShaderNodeTexCoord')
sep = nt.nodes.new('ShaderNodeSeparateXYZ')
ramp.color_ramp.elements[0].color = (1.0, 0.68, 0.74, 1)
ramp.color_ramp.elements[0].position = 0.36
ramp.color_ramp.elements[1].color = (0.12, 0.45, 1.0, 1)
ramp.color_ramp.elements[1].position = 0.52
nt.links.new(tco.outputs['Generated'], sep.inputs[0])
nt.links.new(sep.outputs['Y'], ramp.inputs[0])
nt.links.new(ramp.outputs[0], em.inputs[0])
nt.links.new(em.outputs[0], out.inputs[0])
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 30, 10))
sky = bpy.context.object
sky.scale = (140, 70, 1)
sky.rotation_euler = (math.radians(90), 0, 0)
sky.data.materials.append(sky_m)
sky.visible_shadow = False
bpy.ops.mesh.primitive_plane_add(size=300, location=(0, 0, 0))
bpy.context.object.data.materials.append(C.mat('ground', (0.3, 0.78, 0.45), rough=0.85))
stage_m = C.mat('stage', (1.0, 0.93, 0.85), rough=0.4, coat=0.3)
ring_m = C.mat('stage_ring', (1.0, 0.45, 0.7), rough=0.3, coat=0.5)
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=1.6, depth=0.16, location=(0, -1.2, -0.04))
st = bpy.context.object
st.data.materials.append(stage_m)
bpy.ops.object.shade_smooth()
b = st.modifiers.new('b', 'BEVEL')
b.width = 0.06
b.segments = 4
bpy.ops.mesh.primitive_torus_add(major_radius=1.62, minor_radius=0.06, location=(0, -1.2, 0.02))
bpy.context.object.data.materials.append(ring_m)
bpy.ops.object.shade_smooth()
BG = []
cloud_m = C.mat('cloud', (1, 1, 1), rough=0.9, sss=0.2)
for cx, cz, s in [(-5, 9, 1.4), (4.5, 11, 1.1), (0.5, 13, 0.9), (-2, 15, 1.2), (6, 7.5, 0.8)]:
    for dx, dz, r in [(0, 0, 1), (0.9, 0.2, 0.75), (-0.9, 0.1, 0.7), (0.3, 0.6, 0.7)]:
        BG.append(C.sphere('cloud', (cx + dx * s, 22, cz + dz * s), (r * s, r * s * 0.8, r * s), cloud_m, None, 24))
for (tx, ty), col in zip([(-4.6, 8), (4.8, 9), (-6.5, 14), (7, 15), (-2.5, 17), (2.8, 18)], [(1, 0.35, 0.6), (0.6, 0.4, 1), (1, 0.6, 0.15), (0.2, 0.75, 1), (0.3, 0.85, 0.4), (1, 0.8, 0.2)]):
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.16, depth=3, location=(tx, ty, 1.5))
    bpy.context.object.data.materials.append(C.mat('trunk', (1, 0.95, 0.9), 0.5))
    BG.append(bpy.context.object)
    BG.append(C.sphere('tree', (tx, ty, 3.2), (1.1, 1.1, 1.1), C.mat('tree', col, 0.35, coat=0.5), None, 32))
for o in BG + [sky]:
    o.visible_shadow = False
tgt = C.empty('CamTarget')
bpy.ops.object.camera_add()
cam = bpy.context.object
sc.camera = cam
tc = cam.constraints.new('TRACK_TO')
tc.target = tgt
tc.track_axis = 'TRACK_NEGATIVE_Z'
tc.up_axis = 'UP_Y'
SOLO = ((0, -8.2, 2.3), (0, -1.2, 1.25), 45)
WIDE = ((0, -8.6, 6.4), (0, 0.9, 2.6), 30)
GRU = ((0.25, -9.2, 6.0), (0.25, 0.3, 2.6), 30)

def camkey(f, pose):
    cl, tl, lens = pose
    K(cam, 'location', f, cl)
    K(tgt, 'location', f, tl)
    cam.data.lens = lens
    cam.data.keyframe_insert('lens', frame=f)
camkey(0, ((0, -9.5, 3.0), (0, -1.0, 1.5), 40))
camkey(S0 - 2, SOLO)
camkey(GROUP - 6, SOLO)
camkey(GROUP + 14, WIDE)
camkey(GRUNO - 2, WIDE)
camkey(GRUNO + 16, GRU)
camkey(TOTAL - 1, GRU)
font = bpy.data.fonts.load(os.path.join(HERE, 'LilitaOne.ttf'))

def word3d(txt, rgb, loc, f_in, f_out, size=1.0, max_w=3.6, tilt=84):
    holder = C.empty('txt_' + txt, None, loc, (math.radians(tilt), 0, 0))
    objs = []
    for layer, (m, off) in enumerate([(C.mat('tf', rgb, rough=0.25, coat=0.8, emit=0.25), 0.0), (C.mat('to', (1, 1, 1), rough=0.4, emit=0.6), 0.05)]):
        cu = bpy.data.curves.new('t', 'FONT')
        cu.body = txt
        cu.font = font
        cu.align_x = 'CENTER'
        cu.align_y = 'CENTER'
        cu.size = size
        cu.extrude = 0.12 if layer == 0 else 0.06
        cu.bevel_depth = 0.03
        cu.offset = off
        o = bpy.data.objects.new('t', cu)
        sc.collection.objects.link(o)
        o.data.materials.append(m)
        o.parent = holder
        if layer == 1:
            o.location = (0, 0, -0.08)
        objs.append(o)
    bpy.context.view_layer.update()
    s = min(1.0, max_w / max(objs[1].dimensions.x, 0.01))
    K(holder, 'scale', 0, (0, 0, 0))
    K(holder, 'scale', f_in - 1, (0, 0, 0))
    K(holder, 'scale', f_in + 4, (s * 1.25,) * 3)
    K(holder, 'scale', f_in + 8, (s * 0.92,) * 3)
    K(holder, 'scale', f_in + 11, (s,) * 3)
    if f_out:
        K(holder, 'scale', f_out - 4, (s * 1.08,) * 3)
        K(holder, 'scale', f_out, (0, 0, 0))
    return holder
CENTER = Vector((0, -1.2, 0.08))
RIGS = {}

def make(cid, target_h=2.0):
    ch = roster.build(cid)
    hold = C.empty(f'{cid}_hold')
    sq = C.empty(f'{cid}_squash', hold)
    spin = C.empty(f'{cid}_spin', sq)
    s = max(0.75, min(1.7, target_h / ch['height']))
    ch['root'].parent = spin
    ch['root'].scale = (s, s, s)
    ch.update({'hold': hold, 'sq': sq, 'spin': spin, 's': s})
    RIGS[cid] = ch
    return ch

def S(ch, f, sc3):
    K(ch['sq'], 'scale', f, sc3)

def land(ch, f):
    S(ch, f - 2, (0.88, 0.88, 1.16))
    S(ch, f, (1.28, 1.28, 0.72))
    S(ch, f + 3, (0.92, 0.92, 1.1))
    S(ch, f + 6, (1.05, 1.05, 0.96))
    S(ch, f + 10, (1, 1, 1))

def hop_to(ch, f0, a, b, dur, apex=1.4):
    S(ch, f0 - 5, (1, 1, 1))
    S(ch, f0 - 1, (1.18, 1.18, 0.8))
    S(ch, f0 + 2, (0.86, 0.86, 1.18))
    S(ch, f0 + 8, (1, 1, 1))
    for t in range(0, dur + 1, 2):
        u = t / dur
        p = a.lerp(b, u)
        p.z += apex * 4 * u * (1 - u)
        K(ch['hold'], 'location', f0 + t, tuple(p))
    land(ch, f0 + dur)

def gesture(ch, kind, f0):
    if kind == 'wave':
        C.wave(ch, 'R', f0, cycles=3, period=8)
    elif kind == 'breathe':
        for k in range(2):
            S(ch, f0 + k * 18, (1, 1, 1))
            S(ch, f0 + k * 18 + 9, (1.07, 1.07, 1.07))
            S(ch, f0 + k * 18 + 17, (1, 1, 1))
    elif kind == 'spin':
        K(ch['spin'], 'rotation_euler', f0, (0, 0, 0))
        K(ch['spin'], 'rotation_euler', f0 + 22, (0, 0, math.radians(720)))
        K(ch['spin'], 'rotation_euler', f0 + 23, (0, 0, 0))
    elif kind == 'sway':
        for k, a in enumerate((0, 9, -9, 9, -6, 0)):
            K(ch['spin'], 'rotation_euler', f0 + k * 7, (0, math.radians(a), 0))
    elif kind in ('hops', 'bounce'):
        n = 3 if kind == 'hops' else 4
        per = 11 if kind == 'hops' else 8
        base = ch['hold'].location.copy()
        for k in range(n):
            f = f0 + k * per
            K(ch['hold'], 'location', f, tuple(base))
            K(ch['hold'], 'location', f + per // 2, tuple(base + Vector((0, 0, 0.35))))
            K(ch['hold'], 'location', f + per, tuple(base))
            S(ch, f + per, (1.12, 1.12, 0.88))
            S(ch, f + per + 3, (1, 1, 1))
for i, c in enumerate(CAST):
    ch = make(c['id'])
    s0 = c['start']
    slot = Vector((c['slot'][0], c['slot'][1], 0))
    hidden = Vector((0, -1.2, 14))
    K(ch['hold'], 'location', 0, tuple(hidden))
    K(ch['hold'], 'location', s0 - 1, tuple(hidden))
    for t in range(0, 9):
        u = t / 8
        K(ch['hold'], 'location', s0 + t, tuple(CENTER + Vector((0, 0, 7.5 * (1 - u * u)))))
    S(ch, 0, (0.85, 0.85, 1.2))
    land(ch, s0 + 8)
    _d = MAN.get(f"intro_{c['id']}", {}).get('dur')
    C.talk(ch, s0 + 12, syllables=max(4, round(_d * FPS / 4) if _d else len(c['line']) // 4), step=4)
    C.blink(ch, s0 + 40)
    gesture(ch, c['gesture'], s0 + 16)
    word3d(c['name'], ch['accent'], (0, -1.6, 3.15), s0 + 10, s0 + 52, size=1.0, max_w=2.6)
    hop_to(ch, s0 + 54, CENTER, slot, 12, apex=1.6)
    for f in range(s0 + 90, TOTAL, 70 + 7 * i):
        C.blink(ch, f)
for i, c in enumerate(CAST):
    ch = RIGS[c['id']]
    base = Vector((c['slot'][0], c['slot'][1], 0))
    f = GROUP + 18 + i * 3
    K(ch['hold'], 'location', f, tuple(base))
    K(ch['hold'], 'location', f + 7, tuple(base + Vector((0, 0, 0.7))))
    K(ch['hold'], 'location', f + 14, tuple(base))
    land(ch, f + 14)
    C.wave(ch, 'R', GROUP + 40 + i * 2, cycles=2, period=10)
    g = GRUNO + 34 + i % 3
    K(ch['hold'], 'location', g, tuple(base))
    K(ch['hold'], 'location', g + 5, tuple(base + Vector((0, 0, 0.45))))
    K(ch['hold'], 'location', g + 10, tuple(base))
word3d('¡SOMOS PIMORUKI!', (1.0, 0.3, 0.6), (0, 2.4, 4.6), GROUP + 16, GRUNO + 4, size=1.0, max_w=5.0, tilt=80)
conf_ms = [C.mat(f'conf{k}', col, rough=0.3, emit=0.4) for k, col in enumerate([(1, 0.2, 0.3), (0.2, 0.5, 1), (1, 0.8, 0.1), (0.2, 0.8, 0.3), (0.7, 0.3, 1)])]

def confetti(f0, center, n=40, spread=3.0):
    for k in range(n):
        bpy.ops.mesh.primitive_cube_add(size=1, location=center)
        cb = bpy.context.object
        cb.data.materials.append(conf_ms[k % len(conf_ms)])
        a = random.uniform(0, 2 * math.pi)
        sp = random.uniform(1.5, spread)
        vel = Vector((math.cos(a) * sp, math.sin(a) * sp * 0.5 - 1.2, random.uniform(3, 7)))
        K(cb, 'scale', 0, (0, 0, 0))
        K(cb, 'scale', f0 - 1, (0, 0, 0))
        for t in range(0, 48, 2):
            tt = t / FPS
            pos = Vector(center) + vel * tt * (1 - min(t / 70, 0.6)) + Vector((0, 0, -4.5 * tt * tt))
            K(cb, 'location', f0 + t, tuple(pos))
            K(cb, 'rotation_euler', f0 + t, (t * 0.4 + k, t * 0.3, t * 0.2 + k))
            sz = 0.14 if t < 38 else 0.14 * (48 - t) / 10
            K(cb, 'scale', f0 + t, (sz, sz * 0.25, sz * 0.7))
        K(cb, 'scale', f0 + 48, (0, 0, 0))
        set_interp(cb, 'LINEAR')
confetti(2, (0, -1.2, 2.2), 36)
confetti(GROUP + 16, (0, 1.5, 3.2), 50, 4.0)
word3d('¡HOLA!', (0.2, 0.55, 1.0), (0, -1.6, 2.4), 2, S0 - 2, size=1.2, max_w=3.0)
gr = make('gruno', target_h=2.3)
gp = Vector((1.35, -2.6, 0))
K(gr['hold'], 'location', 0, tuple(gp + Vector((0, 0, -4))))
K(gr['hold'], 'location', GRUNO - 1, tuple(gp + Vector((0, 0, -4))))
K(gr['hold'], 'location', GRUNO + 10, tuple(gp + Vector((0, 0, 0.25))))
K(gr['hold'], 'location', GRUNO + 14, tuple(gp))
land(gr, GRUNO + 14)
K(gr['spin'], 'rotation_euler', 0, (0, 0, math.radians(-25)))
C.talk(gr, GRUNO_LINE['frame'], syllables=8, step=4)
C.blink(gr, GRUNO + 60)
word3d('¡SUSCRÍBETE!', (0.95, 0.12, 0.12), (0.25, 1.6, 4.9), SUBSCRIBE, None, size=1.0, max_w=4.2, tilt=80)
r = sc.render
r.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = int(os.environ.get('SAMPLES', '8'))
sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.05
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 4
sc.cycles.diffuse_bounces = 2
sc.cycles.glossy_bounces = 2
sc.cycles.transmission_bounces = 0
sc.cycles.volume_bounces = 0
sc.cycles.caustics_reflective = False
r.use_persistent_data = True
r.resolution_x, r.resolution_y = (720, 1280)
r.use_motion_blur = True
r.motion_blur_shutter = 0.35
r.image_settings.file_format = 'PNG'
sc.view_settings.view_transform = 'Standard'
sc.view_settings.exposure = -0.1
if __name__ == '__main__':
    out_dir = os.environ.get('OUT', os.path.join(HERE, 'frames'))
    os.makedirs(out_dir, exist_ok=True)
    frames = os.environ.get('FRAMES')
    if frames and '-' in frames:
        a, b2 = map(int, frames.split('-'))
        frames = list(range(a, b2 + 1))
    elif frames:
        frames = [int(x) for x in frames.split(',')]
    else:
        frames = list(range(sc.frame_start, sc.frame_end + 1))
    step = int(os.environ.get('STEP', '1'))
    off = int(os.environ.get('OFFSET', '0'))
    for f in frames[off::step]:
        p = os.path.join(out_dir, f'f{f:04d}.png')
        if os.path.exists(p):
            continue
        sc.frame_set(f)
        r.filepath = p
        bpy.ops.render.render(write_still=True)
        print('DONE', f, flush=True)
