from stage import *
from episodes.boton_mas_grande_plan import *
import ep_tools as T
import bmesh
from mathutils import Matrix
from props.lib import spawn, auto_dress, M
EID = 'boton_mas_grande'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0, -7.0, 1.35), (0, -1.15, 1.05), 37)
WS = ((0.2, -6.4, 2.3), (0.2, -1.6, 0.9), 35)
camkey(0, W0)
camkey(520, W0)
camkey(540, WS)
camkey(600, WS)
camkey(616, W0)
camkey(TOTAL - 1, W0)

dough = M((0.93, 0.68, 0.38), rough=0.7, coat=0.15)
edge_m = M((0.85, 0.55, 0.28), rough=0.75, coat=0.1)
chip_m = M((0.32, 0.18, 0.1), rough=0.5, coat=0.4)


def wedge(name, R, th, a0, a1, parent, n=16):
    bm = bmesh.new()
    pts = [(0.0, 0.0)] + [(R * math.cos(a0 + (a1 - a0) * k / n), R * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]
    bot = [bm.verts.new((x, y, 0)) for x, y in pts]
    top = [bm.verts.new((x, y, th)) for x, y in pts]
    bm.faces.new(bot[::-1])
    bm.faces.new(top)
    m = len(pts)
    for i in range(m):
        j = (i + 1) % m
        bm.faces.new((bot[i], bot[j], top[j], top[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = C.mesh_obj(name, bm, dough, parent, smooth=False)
    bv = o.modifiers.new('b', 'BEVEL')
    bv.width = th * 0.35
    bv.segments = 4
    bv.limit_method = 'ANGLE'
    for f in o.data.polygons:
        f.use_smooth = True
    return o


TR = Vector((0.25, -1.9, Z0))
tray_m = M((0.62, 0.82, 0.98), rough=0.35, coat=0.7)
C.lathe('tray', [(0, 0.0), (0, 0.58), (0.03, 0.66), (0.05, 0.68), (0.045, 0.6), (0.012, 0.56), (0.012, 0.0)], tray_m, None, segs=64).location = tuple(TR)
cookie = C.empty('cookie', None, tuple(TR + Vector((0, 0, 0.015))))
R0 = 0.085
TH = 0.03
pieces = []
rr = random.Random(3)


def piece(parent, a0, chips):
    wedge('wedge', R0, TH, a0 + 0.02, a0 + math.pi / 2 - 0.02, parent)
    for a, d in chips:
        C.sphere('chip', (math.cos(a) * d, math.sin(a) * d, TH * 0.98), (R0 * 0.09, R0 * 0.09, R0 * 0.05), chip_m, parent, 12)


for q in range(4):
    a0 = q * math.pi / 2 + 0.785
    g = C.empty('q', cookie)
    chips = [(a0 + rr.uniform(0.3, 1.27), rr.uniform(0.35, 0.8) * R0) for k in range(3)]
    piece(g, a0, chips)
    pieces.append((g, a0 + math.pi / 4, a0, chips))
GROW = 6.5
K(cookie, 'scale', 0, (1, 1, 1))
K(cookie, 'scale', 66, (1, 1, 1))
K(cookie, 'scale', 76, (GROW * 0.6, GROW * 0.6, GROW * 0.4))
K(cookie, 'scale', 84, (GROW * 1.08, GROW * 1.08, GROW * 0.55))
K(cookie, 'scale', 90, (GROW, GROW, GROW * 0.5))

emi = C.empty('emitter', None, (-0.15, -0.4, Z0))
body_m = M((0.75, 0.55, 1.0), rough=0.35, coat=0.7)
lime = M((0.55, 0.85, 0.3), rough=0.35, coat=0.7)
for k in range(3):
    a = k * 2.0944 + 0.5
    C.tube('leg', [(math.cos(a) * 0.28, math.sin(a) * 0.28, 0.0), (0, 0, 0.85)], 0.025, body_m, emi)
    C.sphere('foot', (math.cos(a) * 0.28, math.sin(a) * 0.28, 0.02), (0.05, 0.05, 0.03), lime, emi, 12)
head = C.empty('ehead', emi, (0, 0, 0.95))
tgt = TR + Vector((0, 0, 0.1))
d = (tgt - Vector((-0.15, -0.4, Z0 + 0.95))).normalized()
head.rotation_euler = Vector((0, 0, 1)).rotation_difference(d).to_euler()
C.lathe('ebody', [(-0.18, 0.0), (-0.18, 0.12), (-0.05, 0.15), (0.12, 0.13), (0.2, 0.17), (0.24, 0.18), (0.25, 0.0)], body_m, head, segs=40)
lens_m = C.mat('elens', (0.6, 1.0, 0.7), rough=0.2, coat=1.0, emit=0.4)
C.sphere('elens', (0, 0, 0.24), (0.13, 0.13, 0.04), lens_m, head, 32)
C.tube('ering', [(math.cos(k * 6.2832 / 40) * 0.17, math.sin(k * 6.2832 / 40) * 0.17, 0.24) for k in range(41)], 0.022, lime, head)
pl = C.empty('eplus', head, (0.0, -0.155, 0.0), (math.radians(90), 0, 0))
C.rounded_box('ep1', (0, 0, 0), (0.1, 0.025, 0.025), 0.01, M((1, 1, 1), coat=0.5), pl)
C.rounded_box('ep2', (0, 0, 0), (0.025, 0.1, 0.025), 0.01, M((1, 1, 1), coat=0.5), pl)
inp = lens_m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
for f, v in ((0, 0.4), (60, 0.4), (64, 4.0), (88, 4.0), (94, 0.4)):
    inp.default_value = v
    inp.keyframe_insert('default_value', frame=f)
beam_m = C.mat('beam', (0.6, 1.0, 0.7), rough=0.3, emit=3.0)
beam_m.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.55
start = Vector((-0.15, -0.4, Z0 + 0.95)) + d * 0.26
L = (tgt - start).length
beam = C.empty('beam', None, tuple(start))
beam.rotation_euler = head.rotation_euler
C.tube('beamc', [(0, 0, 0), (0, 0, L)], 0.035, beam_m, beam)
K(beam, 'scale', 0, (0, 0, 0))
K(beam, 'scale', 63, (0, 0, 0))
K(beam, 'scale', 66, (1, 1, 1))
K(beam, 'scale', 86, (1, 1, 1))
K(beam, 'scale', 90, (0, 0, 0))
for k in range(10):
    o = C.sphere('spk', tuple(start), (1, 1, 1), beam_m, None, 10)
    f0 = 64 + k * 2
    K(o, 'scale', 0, (0, 0, 0))
    K(o, 'scale', f0 - 1, (0, 0, 0))
    K(o, 'scale', f0, (0.03,) * 3)
    K(o, 'location', f0, tuple(start))
    K(o, 'location', f0 + 8, tuple(tgt + Vector((rr.uniform(-0.3, 0.3), rr.uniform(-0.2, 0.2), rr.uniform(0.0, 0.3)))))
    K(o, 'scale', f0 + 8, (0.03,) * 3)
    K(o, 'scale', f0 + 10, (0, 0, 0))

gruno = make('gruno', 1.6)
ruki = make('ruki', 1.45)
G0 = Vector((-0.95, -0.95, Z0))
GL = Vector((-0.92, -1.9, Z0))
RS = Vector((2.8, -0.9, Z0))
R1 = Vector((1.0, -0.8, Z0))
T.place(gruno, 0, G0)
T.turn(gruno, 0, 20)
T.place(ruki, 0, RS)
T.turn(ruki, 0, -90)
mini = C.empty('mini', ruki['hold'], (0.0, -0.78, 0.62), (math.radians(80), 0, 0))
for q in range(4):
    a0 = q * math.pi / 2
    wedge('mw', 0.11, 0.03, a0, a0 + math.pi / 2, mini)
for k in range(4):
    a = k * 1.7 + 0.4
    C.sphere('mchip', (math.cos(a) * 0.06, math.sin(a) * 0.06, 0.03), (0.01, 0.01, 0.006), chip_m, mini, 10)

C.wave(gruno, 'R', 14, cycles=2, period=8)
T.turn(gruno, 40, 20)
T.turn(gruno, 48, 45)
T.arm(gruno, 'L', 54, 0, None)
T.arm(gruno, 'L', 60, fwd=-45, out=None)
T.arm(gruno, 'L', 64, fwd=-45, out=None)
T.arm(gruno, 'L', 70, 0, None)
S(gruno, 58, (1, 1, 1))
S(gruno, 61, (1.04, 1.04, 0.96))
S(gruno, 66, (1, 1, 1))
gesture(gruno, 'bounce', 92)
T.turn(gruno, 100, 45)
T.turn(gruno, 106, 160)
hop_to(gruno, 108, G0, GL, 16, apex=0.4)
T.turn(gruno, 124, 160)
T.turn(gruno, 130, 70)
T.arm(gruno, 'R', 128, 0, None)
T.arm(gruno, 'R', 134, fwd=-70, out=10)
T.arm(gruno, 'L', 128, 0, None)
T.arm(gruno, 'L', 134, fwd=-70, out=None)
for k, f in enumerate(range(136, 176, 4)):
    S(gruno, f, (1.03, 1.03, 0.97) if k % 2 else (0.98, 0.98, 1.03))
    K(cookie, 'rotation_euler', f, (0, math.radians(-3 if k % 2 else -1), 0))
K(cookie, 'rotation_euler', 178, (0, 0, 0))
S(gruno, 178, (1, 1, 1))
T.rest_arm(gruno, 'R', 182)
T.arm(gruno, 'L', 182, 0, None)
S(gruno, 184, (1.1, 1.1, 0.88))
S(gruno, 192, (1, 1, 1))
T.turn(gruno, 190, 70)
T.turn(gruno, 198, 30)

for f in range(0, 160, 40):
    K(ruki['hold'], 'location', f, tuple(RS))
for k, f in enumerate(range(160, 196, 6)):
    u = (f - 160) / 36
    p = RS.lerp(R1, u)
    p.z += 0.08 * abs(math.sin(k * 1.6))
    K(ruki['hold'], 'location', f, tuple(p))
K(ruki['hold'], 'location', 196, tuple(R1))
T.turn(ruki, 190, -90)
T.turn(ruki, 198, -25)
T.turn(ruki, 304, -25)
T.turn(ruki, 312, -5)
S(ruki, 236, (1, 1, 1))
S(ruki, 240, (1.05, 1.05, 0.95))
S(ruki, 246, (1, 1, 1))
T.turn(ruki, 376, -5)
T.turn(ruki, 384, -30)
T.turn(gruno, 360, 30)
T.turn(gruno, 368, 20)
for k, f in enumerate(range(484, 530, 9)):
    T.turn(gruno, f, 20 + (12 if k % 2 else -6))
T.turn(gruno, 532, 40)

SPLIT0 = 548
for g, mid, _, _ in pieces:
    off = Vector((math.cos(mid), math.sin(mid), 0)) * 0.016
    K(g, 'location', SPLIT0, (0, 0, 0))
    K(g, 'location', SPLIT0 + 8, tuple(off * 1.3))
    K(g, 'location', SPLIT0 + 12, tuple(off))
T.turn(ruki, 540, -30)
T.turn(ruki, 546, -45)
T.arm(ruki, 'R', 540, 0, None)
T.arm(ruki, 'R', 546, fwd=-40, out=60)
T.arm(ruki, 'R', 560, fwd=-40, out=60)
T.rest_arm(ruki, 'R', 568)

gq, gm, ga0, gch = min(pieces, key=lambda p: math.cos(p[1]))
T.place(gruno, 0, G0)
bpy.context.view_layer.update()
GTOP = max((o.matrix_world @ Vector(c)).z for o in gruno['root'].children_recursive if o.type == 'MESH' for c in o.bound_box) - Z0
HOLD = GL + Vector((0.05, -0.74, 0.5))
p0 = TR + Vector((0, 0, 0.015)) + Vector((math.cos(gm), math.sin(gm), 0)) * 0.016 * GROW
big = C.empty('bigq', None, tuple(p0))
piece(big, ga0, gch)
K(gq, 'scale', 603, (1, 1, 1))
K(gq, 'scale', 604, (0, 0, 0))
big.scale = (GROW, GROW, GROW * 0.5)
K(big, 'location', 0, tuple(p0 + Vector((0, 0, -3))))
K(big, 'location', 603, tuple(p0 + Vector((0, 0, -3))))
K(big, 'location', 604, tuple(p0))
K(big, 'rotation_euler', 604, (0, 0, 0))
gq = big
for o in [big] + list(big.children_recursive):
    o.cycles.use_motion_blur = False
mid_dir = Vector((math.cos(gm), math.sin(gm), 0))
for f in range(606, 627, 2):
    u = (f - 604) / 22
    u = u * u * (3 - 2 * u)
    K(gq, 'location', f, tuple(p0.lerp(HOLD - mid_dir * GROW * R0 * 0.5, u) + Vector((0, 0, 0.3 * 4 * u * (1 - u)))))
    K(gq, 'rotation_euler', f, (math.radians(80 * u), 0, 0))
T.turn(gruno, 600, 40)
T.turn(gruno, 608, 10)
for side in ('L', 'R'):
    T.arm(gruno, side, 604, 0, None)
    T.arm(gruno, side, 618, fwd=-60, out=25)
    T.arm(gruno, side, TOTAL - 1, fwd=-60, out=25)
for k, f in enumerate(range(630, TOTAL - 1, 10)):
    S(gruno, f, (1.04, 1.04, 0.95) if k % 2 else (1, 1, 1))
    K(gq, 'location', f, tuple(HOLD - mid_dir * GROW * R0 * 0.5 + Vector((0.03 * (1 if k % 2 else -1), 0, -0.04 * (k % 2)))))
T.turn(ruki, 640, -45)
T.turn(ruki, 648, -20)
gesture(ruki, 'breathe', 700)
C.wave(ruki, 'L', 760, cycles=2, period=8)

T.lines(EID, LINES)
T.blinks(gruno, (100, 220, 330, 450, 560, 700, 790))
T.blinks(ruki, (230, 330, 430, 520, 640, 760))
word3d('GRANDE', (0.95, 0.35, 0.05), (-0.3, -1.6, 2.6), 206, 330, size=0.55, max_w=1.6)
word3d('PEQUEÑA', (0.15, 0.35, 0.95), (0.5, -1.4, 2.05), 236, 330, size=0.34, max_w=1.0)
