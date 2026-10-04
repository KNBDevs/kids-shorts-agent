"""Kids Shorts pilot — escena 3D procedural (Blender/bpy, headless, CPU).

Formato: "Aprende los colores". Un personaje (Pip) cae sobre una plataforma giratoria,
cada aterrizaje en un botón gigante le cambia el color; final en bucle perfecto.
Todo está parametrizado en SPEC para que el agente genere variantes.
"""
import bpy, math, json, sys, os, random
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 24
BEAT = 12  # 120 BPM -> 12 frames por pulso

SPEC = {
    "seed": 7,
    "body_start": [0.95, 0.96, 1.0],
    "colors": [  # nombre mostrado, RGB lineal aproximado
        {"word": "ROJO",     "rgb": [0.90, 0.05, 0.06]},
        {"word": "AZUL",     "rgb": [0.03, 0.22, 0.95]},
        {"word": "AMARILLO", "rgb": [1.00, 0.72, 0.02]},
        {"word": "VERDE",    "rgb": [0.06, 0.70, 0.12]},
    ],
    "finale_word": "¡MUY BIEN!",
    "sky_top": [0.10, 0.42, 1.0], "sky_bottom": [1.0, 0.62, 0.70],
    "ground": [0.28, 0.80, 0.42],
    "res": [720, 1280], "samples": 8,
}
if len(sys.argv) > 1 and sys.argv[-1].endswith(".json"):
    SPEC.update(json.load(open(sys.argv[-1])))
random.seed(SPEC["seed"])

# ---------- Timeline (en frames) ----------
L = [12 + 108 * i for i in range(len(SPEC["colors"]))]   # aterrizajes
J = [l + 84 for l in L[:-1]]                              # saltos entre botones
FINALE = L[-1] + 48           # 384: giro arcoíris
J_FINAL = 444                 # gran salto que sale por arriba
END = 480                     # frame 480 == frame 0 (loop)

PAD_R, TT_TOP, PAD_H = 2.7, 0.0, 0.3
BASE_Z = TT_TOP + PAD_H

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.frame_start, sc.frame_end = 0, END - 1
sc.render.fps = FPS

# ---------- helpers ----------
def mat(name, rgb, rough=0.3, coat=0.0, sss=0.0, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*rgb, 1)
    p.inputs["Roughness"].default_value = rough
    if coat: p.inputs["Coat Weight"].default_value = coat
    if sss:
        p.inputs["Subsurface Weight"].default_value = sss
        p.inputs["Subsurface Radius"].default_value = (0.3, 0.3, 0.3)
    if emit:
        p.inputs["Emission Color"].default_value = (*rgb, 1)
        p.inputs["Emission Strength"].default_value = emit
    return m

def sphere(name, loc, scale, m, seg=48, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale
    bpy.ops.object.shade_smooth(); o.data.materials.append(m)
    if parent: o.parent = parent
    return o

def cyl(name, loc, r, h, m, bevel=0.08, verts=64):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc)
    o = bpy.context.object; o.name = name; o.data.materials.append(m)
    b = o.modifiers.new("bev", "BEVEL"); b.width = bevel; b.segments = 4
    bpy.ops.object.shade_smooth()
    return o

def empty(name, loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None); o.location = loc
    sc.collection.objects.link(o)
    if parent: o.parent = parent
    return o

def key(o, path, f, val, interp=None):
    setattr(o, path, val) if not isinstance(val, (int, float)) or path != "__" else None
    o.keyframe_insert(path, frame=f)
    if interp:
        for fc in o.animation_data.action.fcurves if hasattr(o.animation_data.action, "fcurves") else []:
            pass
    return o

def kf(o, path, f, val):
    attr = getattr(o, path)
    if hasattr(attr, "__len__"):
        for i, v in enumerate(val): attr[i] = v
    else:
        setattr(o, path, val)
    o.keyframe_insert(path, frame=f)

def set_interp(obj_or_id, mode):
    """Fija interpolación en todas las curvas (compatible con slotted actions de Blender 5)."""
    ad = obj_or_id.animation_data
    if not ad or not ad.action: return
    act = ad.action
    curves = []
    if hasattr(act, "fcurves") and len(getattr(act, "fcurves", [])):
        curves = list(act.fcurves)
    else:
        for layer in act.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    curves += list(bag.fcurves)
    for fc in curves:
        for k in fc.keyframe_points: k.interpolation = mode

# ---------- Mundo / luz / cámara ----------
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.72, 1.0, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.55

bpy.ops.object.light_add(type="SUN", rotation=(math.radians(50), math.radians(-25), math.radians(-30)))
sun = bpy.context.object; sun.data.energy = 3.2; sun.data.color = (1, 0.95, 0.88); sun.data.angle = math.radians(8)
bpy.ops.object.light_add(type="AREA", location=(-5, -10, 7))
fill = bpy.context.object; fill.data.energy = 900; fill.data.size = 8
fill.rotation_euler = (math.radians(55), 0, math.radians(-25))
bpy.ops.object.light_add(type="AREA", location=(4, 6, 6))
rim = bpy.context.object; rim.data.energy = 500; rim.data.size = 5; rim.data.color = (1, 0.85, 0.95)
rim.rotation_euler = (math.radians(-50), math.radians(20), 0)

cam_target = empty("CamTarget", (0, -PAD_R, 2.1))
bpy.ops.object.camera_add(location=(0, -PAD_R - 12.5, 5.0))
cam = bpy.context.object; sc.camera = cam; cam.data.lens = 72
tc = cam.constraints.new("TRACK_TO"); tc.target = cam_target
tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"

# Cielo: gran fondo curvo con degradado
sky_m = bpy.data.materials.new("Sky"); sky_m.use_nodes = True
nt = sky_m.node_tree; nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission")
ramp = nt.nodes.new("ShaderNodeValToRGB"); tco = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
ramp.color_ramp.elements[0].color = (*SPEC["sky_bottom"], 1); ramp.color_ramp.elements[0].position = 0.33
ramp.color_ramp.elements[1].color = (*SPEC["sky_top"], 1); ramp.color_ramp.elements[1].position = 0.46
nt.links.new(tco.outputs["Generated"], sep.inputs[0]); nt.links.new(sep.outputs["Y"], ramp.inputs[0])
nt.links.new(ramp.outputs[0], em.inputs[0]); em.inputs[1].default_value = 1.0
nt.links.new(em.outputs[0], out.inputs[0])
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 24, 10))
sky = bpy.context.object; sky.scale = (120, 60, 1); sky.rotation_euler = (math.radians(90), 0, 0)
sky.data.materials.append(sky_m)

ground_m = mat("Ground", SPEC["ground"], rough=0.8)
bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -0.6)); bpy.context.object.data.materials.append(ground_m)

# Nubes y árboles-piruleta de fondo
cloud_m = mat("Cloud", (1, 1, 1), rough=0.9, sss=0.2)
BG = []
for cx, cz, s in [(-3.6, 8.2, 1.2), (3.4, 9.6, 1.0), (0.6, 11.5, 0.8), (-1.2, 13.5, 1.1)]:
    for dx, dz, r in [(0, 0, 1), (0.9, 0.2, 0.75), (-0.9, 0.1, 0.7), (0.3, 0.6, 0.7)]:
        BG.append(sphere("cloud", (cx + dx * s, 16, cz + dz * s), (r * s, r * s * 0.8, r * s), cloud_m, seg=24))
for tx, ty, col in [(-3.4, 10, (1, 0.35, 0.6)), (3.6, 11.5, (0.6, 0.4, 1)), (-5.5, 17, (1, 0.6, 0.15)), (5.8, 18, (0.2, 0.75, 1))]:
    BG.append(cyl("trunk", (tx, ty, 0.6), 0.13, 2.4, mat("trunk", (1, 0.95, 0.9), 0.5), bevel=0.05, verts=16))
    BG.append(sphere("tree", (tx, ty, 2.4), (0.85, 0.85, 0.85), mat("tree", col, 0.35, coat=0.5), seg=32))
for o in BG + [sky]: o.visible_shadow = False

# ---------- Plataforma giratoria con botones ----------
tt = empty("Turntable")
tt_m = mat("TT", (1, 0.96, 0.9), rough=0.4, coat=0.3)
o = cyl("tt_base", (0, 0, TT_TOP - 0.3), 4.0, 0.6, tt_m, bevel=0.12); o.parent = tt
band_m = mat("Band", (1, 0.45, 0.7), rough=0.3, coat=0.5)
bpy.ops.mesh.primitive_torus_add(major_radius=4.02, minor_radius=0.12, location=(0, 0, TT_TOP - 0.3))
band = bpy.context.object; band.data.materials.append(band_m); bpy.ops.object.shade_smooth(); band.parent = tt
pads = []
for i, c in enumerate(SPEC["colors"]):
    a = math.radians(-90 - 90 * i)
    pm = mat(f"pad{i}", c["rgb"], rough=0.18, coat=0.8)
    p = cyl(f"pad{i}", (PAD_R * math.cos(a), PAD_R * math.sin(a), TT_TOP + PAD_H / 2), 1.0, PAD_H, pm, bevel=0.1)
    # origen en la base para que el "pisotón" no levante el botón
    p.location.z = TT_TOP
    bpy.context.view_layer.update()
    for v in p.data.vertices: v.co.z += PAD_H / 2
    p.parent = tt; pads.append(p)

# rotación de la plataforma (90º por salto)
for i, j in enumerate(J):
    kf(tt, "rotation_euler", j, (0, 0, math.radians(90 * i)))
    kf(tt, "rotation_euler", j + 24, (0, 0, math.radians(90 * (i + 1))))
kf(tt, "rotation_euler", 0, (0, 0, 0))
kf(tt, "rotation_euler", J_FINAL, (0, 0, math.radians(90 * (len(L) - 1))))
kf(tt, "rotation_euler", J_FINAL + 28, (0, 0, math.radians(90 * len(L))))

# pisotón de cada botón
for i, l in enumerate(L):
    p = pads[i]
    for f, s in [(l - 1, 1), (l, 0.45), (l + 4, 1.15), (l + 8, 0.95), (l + 11, 1)]:
        kf(p, "scale", f, (1 + (1 - s) * 0.25, 1 + (1 - s) * 0.25, s))

# ---------- Personaje: Pip ----------
body_m = mat("PipBody", SPEC["body_start"], rough=0.2, coat=0.7, sss=0.12)
white = mat("EyeWhite", (1, 1, 1), rough=0.15)
black = mat("Pupil", (0.01, 0.01, 0.02), rough=0.1, coat=1)
shine = mat("Shine", (1, 1, 1), emit=6)
cheek_m = mat("Cheek", (1, 0.25, 0.45), rough=0.5)
mouth_m = mat("Mouth", (0.25, 0.01, 0.04), rough=0.4)
tongue_m = mat("Tongue", (1, 0.3, 0.4), rough=0.4)
gold = mat("Gold", (1, 0.75, 0.1), rough=0.15, coat=1, emit=0.4)

pip = empty("Pip", (0, -PAD_R, BASE_Z))
sq = empty("PipSquash", parent=pip)
spin = empty("PipSpin", parent=sq)
body = sphere("body", (0, 0, 1.1), (1, 0.92, 1.1), body_m, seg=64, parent=spin)
eyes = []
for sx in (-1, 1):
    e = empty(f"eye{sx}", (0.37 * sx, -0.79, 1.40), parent=spin)
    sphere("eyeW", (0, 0, 0), (0.31, 0.29, 0.34), white, parent=e)
    sphere("pupil", (0.0, -0.17, 0.03), (0.2, 0.17, 0.23), black, parent=e)
    sphere("shine", (-0.07, -0.33, 0.12), (0.075, 0.04, 0.075), shine, seg=16, parent=e)
    sphere("shine2", (0.07, -0.33, -0.04), (0.035, 0.02, 0.035), shine, seg=12, parent=e)
    c = sphere("cheek", (0.64 * sx, -0.66, 0.93), (0.16, 0.05, 0.10), cheek_m, seg=24, parent=spin)
    c.rotation_euler = (0, 0, math.radians(-42 * sx))
    eyes.append(e)
mouth = sphere("mouth", (0, -0.86, 0.80), (0.20, 0.08, 0.15), mouth_m, seg=32, parent=spin)
sphere("tongue", (0, -0.89, 0.72), (0.12, 0.06, 0.06), tongue_m, seg=24, parent=spin)
ant = empty("antenna", (0, 0, 2.12), parent=spin)
bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.5, location=(0, 0, 0.22))
st = bpy.context.object; st.data.materials.append(body_m); st.parent = ant
sphere("antball", (0, 0, 0.5), (0.13, 0.13, 0.13), gold, seg=24, parent=ant)

# --- color del cuerpo (cambio seco en cada aterrizaje) ---
bsdf = body_m.node_tree.nodes["Principled BSDF"]
def body_color(f, rgb):
    bsdf.inputs["Base Color"].default_value = (*rgb, 1)
    bsdf.inputs["Base Color"].keyframe_insert("default_value", frame=f)
body_color(0, SPEC["body_start"])
for i, l in enumerate(L):
    body_color(l, SPEC["colors"][i]["rgb"])
# arcoíris final
rb_cols = [c["rgb"] for c in SPEC["colors"]]
for k, f in enumerate(range(FINALE, FINALE + 36, 4)):
    body_color(f, rb_cols[k % len(rb_cols)])
body_color(FINALE + 40, SPEC["colors"][-1]["rgb"])
body_color(J_FINAL + 16, SPEC["body_start"])  # ya fuera de cuadro
# flash de brillo al cambiar color
def flash(f):
    for ff, v in [(f - 1, 0.0), (f, 1.4), (f + 2, 0.45), (f + 3, 0.0)]:
        bsdf.inputs["Emission Strength"].default_value = v
        bsdf.inputs["Emission Strength"].keyframe_insert("default_value", frame=ff)
bsdf.inputs["Emission Color"].default_value = (1, 1, 1, 1)
for l in L: flash(l)
set_interp(body_m.node_tree, "CONSTANT")

# --- trayectoria vertical y squash & stretch ---
def z_at(f):
    return BASE_Z + f
# caída inicial (cuadrática), sale de arriba
for f in range(0, 13):
    kf(pip, "location", f, (0, -PAD_R, BASE_Z + 9.5 * (1 - (f / 12) ** 2)))

def S(f, s): kf(sq, "scale", f, s)
def landing(l):
    S(l - 3, (0.86, 0.86, 1.2)); S(l, (1.32, 1.32, 0.68)); S(l + 3, (0.9, 0.9, 1.12))
    S(l + 6, (1.07, 1.07, 0.95)); S(l + 9, (0.98, 0.98, 1.02)); S(l + 12, (1, 1, 1))
def hop(f0, h=0.6, d=12):
    # pequeño bote de celebración sobre el pulso
    S(f0 - 3, (1.12, 1.12, 0.88)); S(f0, (0.94, 0.94, 1.08))
    kf(pip, "location", f0 - 3, (0, -PAD_R, BASE_Z))
    kf(pip, "location", f0 + d // 2, (0, -PAD_R, BASE_Z + h))
    kf(pip, "location", f0 + d, (0, -PAD_R, BASE_Z))
    S(f0 + d // 2, (1, 1, 1)); S(f0 + d, (1.15, 1.15, 0.86)); S(f0 + d + 4, (1, 1, 1))

def jump(j, apex=2.4, spin_turns=0):
    S(j - 8, (1, 1, 1)); S(j - 2, (1.22, 1.22, 0.76)); S(j + 2, (0.84, 0.84, 1.22)); S(j + 12, (1, 1, 1))
    kf(pip, "location", j - 1, (0, -PAD_R, BASE_Z))
    for t in range(0, 25, 2):
        u = t / 24
        kf(pip, "location", j + t, (0, -PAD_R, BASE_Z + apex * 4 * u * (1 - u)))
    if spin_turns:
        kf(spin, "rotation_euler", j, (0, 0, 0))
        kf(spin, "rotation_euler", j + 22, (0, 0, math.radians(360 * spin_turns)))
        kf(spin, "rotation_euler", j + 23, (0, 0, 0))

for l in L:
    landing(l)
    kf(pip, "location", l, (0, -PAD_R, BASE_Z))
for i, l in enumerate(L):
    hop(l + 36, 0.55); hop(l + 60, 0.75)
for i, j in enumerate(J):
    jump(j, spin_turns=[0, 1, 0][i % 3])
# remate: giro arcoíris + gran salto en loop
kf(spin, "rotation_euler", FINALE - 1, (0, 0, 0))
kf(spin, "rotation_euler", FINALE + 36, (0, 0, math.radians(360)))
kf(spin, "rotation_euler", FINALE + 37, (0, 0, 0))
S(FINALE + 36, (1, 1, 1)); S(FINALE + 42, (1.15, 1.15, 0.87)); S(FINALE + 48, (1, 1, 1))
kf(pip, "location", J_FINAL - 2, (0, -PAD_R, BASE_Z))
S(J_FINAL - 8, (1, 1, 1)); S(J_FINAL - 2, (1.28, 1.28, 0.7)); S(J_FINAL + 3, (0.8, 0.8, 1.3))
for t in range(0, 25, 2):
    u = t / 24
    kf(pip, "location", J_FINAL + t, (0, -PAD_R, BASE_Z + 13 * (1 - (1 - u) ** 2)))
S(J_FINAL + 24, (0.86, 0.86, 1.2)); S(END - 1, (0.86, 0.86, 1.2))
S(0, (0.86, 0.86, 1.2))

d = cam_target.driver_add("location", 2).driver
d.type = "SCRIPTED"
v = d.variables.new(); v.name = "z"; v.targets[0].id = pip; v.targets[0].data_path = "location.z"
d.expression = "2.1 + min(0.5 * (z - %.3f), 0.9)" % BASE_Z

# antena: retraso (secondary motion) en cada aterrizaje / salto
def wob(f, amp):
    for k, a in enumerate([amp, -amp * 0.6, amp * 0.35, -amp * 0.15, 0]):
        kf(ant, "rotation_euler", f + k * 3, (math.radians(a), math.radians(a * 0.4), 0))
kf(ant, "rotation_euler", 0, (0, 0, 0))
for l in L: wob(l, 22)
for j in J: wob(j, -18)
for l in L: wob(l + 48, 10)

# parpadeos
def blink(f):
    for e in eyes:
        kf(e, "scale", f - 1, (1, 1, 1)); kf(e, "scale", f + 1, (1, 1, 0.08)); kf(e, "scale", f + 4, (1, 1, 1))
for e in eyes: kf(e, "scale", 0, (1, 1, 1))
for l in L: blink(l + 28)
blink(FINALE + 44)

# boca: se abre al "decir" cada color
def talk(f):
    kf(mouth, "scale", f - 1, (0.20, 0.08, 0.15)); kf(mouth, "scale", f + 3, (0.24, 0.09, 0.24))
    kf(mouth, "scale", f + 10, (0.20, 0.08, 0.15))
kf(mouth, "scale", 0, (0.20, 0.08, 0.15))
for l in L: talk(l + 3)
talk(FINALE + 40)

# ---------- Salpicaduras + onda expansiva ----------
def splash(l, rgb, n=18):
    m = mat("splash", rgb, rough=0.15, coat=0.8, emit=0.3)
    base = Vector((0, -PAD_R, BASE_Z + 0.2))
    for k in range(n):
        a = 2 * math.pi * k / n + random.uniform(-0.15, 0.15)
        sp = random.uniform(3.0, 5.0)
        vel = Vector((math.cos(a) * sp, math.sin(a) * sp * 0.6 - 0.8, random.uniform(3.0, 6.0)))
        r = random.uniform(0.09, 0.17)
        d = sphere("drop", base, (0, 0, 0), m, seg=16)
        kf(d, "scale", l - 1, (0, 0, 0))
        for t in range(0, 22, 2):
            tt_ = t / FPS
            pos = base + vel * tt_ + Vector((0, 0, -9.8 * tt_ * tt_ / 2))
            pos.z = max(pos.z, 0.05)
            kf(d, "location", l + t, tuple(pos))
            s = r * (1 - t / 22) if t else r
            kf(d, "scale", l + t, (s, s, s * (1.3 if t < 8 else 1)))
        kf(d, "scale", l + 22, (0, 0, 0))
        set_interp(d, "LINEAR")
    bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=0.06, location=(0, -PAD_R, BASE_Z + 0.03))
    ring = bpy.context.object; ring.data.materials.append(mat("ring", rgb, emit=1.5)); bpy.ops.object.shade_smooth()
    kf(ring, "scale", l - 1, (0, 0, 0)); kf(ring, "scale", l, (0.8, 0.8, 1))
    kf(ring, "scale", l + 8, (2.6, 2.6, 0.5)); kf(ring, "scale", l + 11, (0, 0, 0))
for i, l in enumerate(L):
    splash(l, SPEC["colors"][i]["rgb"])

# confeti del final
conf_ms = [mat(f"conf{i}", c["rgb"], rough=0.3, emit=0.4) for i, c in enumerate(SPEC["colors"])]
cf0 = FINALE + 38
for k in range(36):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -PAD_R, 3))
    c = bpy.context.object; c.data.materials.append(conf_ms[k % len(conf_ms)])
    a = random.uniform(0, 2 * math.pi); sp = random.uniform(2, 4.5)
    vel = Vector((math.cos(a) * sp, math.sin(a) * sp * 0.5 - 1.0, random.uniform(3, 7)))
    kf(c, "scale", cf0 - 1, (0, 0, 0))
    for t in range(0, 44, 2):
        tt_ = t / FPS
        drag = 1 - min(t / 60, 0.6)
        pos = Vector((0, -PAD_R, 2.6)) + vel * tt_ * drag + Vector((0, 0, -4.5 * tt_ * tt_))
        kf(c, "location", cf0 + t, tuple(pos))
        kf(c, "rotation_euler", cf0 + t, (t * 0.4 + k, t * 0.3, t * 0.2 + k))
        s = 0.16 if t < 34 else 0.16 * (44 - t) / 10
        kf(c, "scale", cf0 + t, (s, s * 0.25, s * 0.7))
    kf(c, "scale", cf0 + 44, (0, 0, 0))
    set_interp(c, "LINEAR")

# ---------- Texto 3D con contorno ----------
font = bpy.data.fonts.load(os.path.join(HERE, "LilitaOne.ttf"))
def word3d(txt, rgb, f_in, f_out, z=4.3, max_w=2.8):
    holder = empty("txt_" + txt, (0, -PAD_R - 0.6, z))
    holder.rotation_euler = (math.radians(82), 0, 0)
    objs = []
    for layer, (m, off, dy) in enumerate([(mat("tf", rgb, rough=0.2, coat=0.8, emit=0.25), 0.0, 0.0),
                                          (mat("to", (1, 1, 1), rough=0.4, emit=0.6), 0.045, 0.06)]):
        cu = bpy.data.curves.new("t", "FONT"); cu.body = txt; cu.font = font
        cu.align_x = "CENTER"; cu.align_y = "CENTER"; cu.size = 1.0
        cu.extrude = 0.12 if layer == 0 else 0.06; cu.bevel_depth = 0.03; cu.offset = off
        o = bpy.data.objects.new("t", cu); sc.collection.objects.link(o)
        o.data.materials.append(m); o.parent = holder; o.location = (0, 0, -dy * 0) ; o.location.y = 0
        o.location.z = 0; o.location = (0, 0, 0)
        if layer == 1: o.location = (0, 0, -0.08)
        objs.append(o)
    bpy.context.view_layer.update()
    w_ = objs[1].dimensions.x
    s = min(1.25, max_w / max(w_, 0.01))
    kf(holder, "scale", 0, (0, 0, 0)); kf(holder, "scale", f_in - 1, (0, 0, 0))
    kf(holder, "scale", f_in + 4, (s * 1.25, s * 1.25, s * 1.25)); kf(holder, "scale", f_in + 8, (s * 0.92,) * 3)
    kf(holder, "scale", f_in + 11, (s,) * 3); kf(holder, "scale", f_out - 4, (s * 1.08,) * 3)
    kf(holder, "scale", f_out, (0, 0, 0))
    # balanceo suave
    kf(holder, "rotation_euler", f_in, (math.radians(82), 0, math.radians(-4)))
    kf(holder, "rotation_euler", (f_in + f_out) // 2, (math.radians(82), 0, math.radians(4)))
    kf(holder, "rotation_euler", f_out, (math.radians(82), 0, math.radians(-2)))
for i, l in enumerate(L):
    f_out = J[i] - 6 if i < len(J) else FINALE + 2
    word3d(SPEC["colors"][i]["word"], SPEC["colors"][i]["rgb"], l + 2, f_out)
word3d(SPEC["finale_word"], (1, 0.35, 0.65), FINALE + 38, J_FINAL - 4)

# ---------- Render ----------
r = sc.render
r.engine = "CYCLES"; sc.cycles.device = "CPU"
sc.cycles.samples = SPEC["samples"]; sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.05; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2
sc.cycles.transmission_bounces = 0; sc.cycles.volume_bounces = 0; sc.cycles.caustics_reflective = False
r.use_persistent_data = True
r.resolution_x, r.resolution_y = SPEC["res"]
r.use_motion_blur = True; r.motion_blur_shutter = 0.4
r.image_settings.file_format = "PNG"
try:
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.exposure = -0.15
except TypeError:
    pass

if __name__ == "__main__":
    out_dir = os.environ.get("OUT", os.path.join(HERE, "frames"))
    os.makedirs(out_dir, exist_ok=True)
    frames = os.environ.get("FRAMES")  # "a-b" o lista "1,5,9"
    if frames and "-" in frames:
        a, b = map(int, frames.split("-")); frames = list(range(a, b + 1))
    elif frames:
        frames = [int(x) for x in frames.split(",")]
    else:
        frames = list(range(sc.frame_start, sc.frame_end + 1))
    step = int(os.environ.get("STEP", "1")); off = int(os.environ.get("OFFSET", "0"))
    frames = frames[off::step]
    if os.environ.get("SAVE_BLEND"):
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "scene.blend"))
    for f in frames:
        p = os.path.join(out_dir, f"f{f:04d}.png")
        if os.path.exists(p): continue
        sc.frame_set(f); r.filepath = p
        bpy.ops.render.render(write_still=True)
        print("DONE", f, flush=True)
