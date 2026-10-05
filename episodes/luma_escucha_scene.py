from stage import *
from episodes.luma_escucha_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M
EID = 'luma_escucha'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0, -7.0, 1.35), (0, -1.15, 1.05), 37)
WL = ((0, -5.4, 1.3), (0, -1.35, 0.95), 38)
camkey(0, W0)
camkey(160, W0)
camkey(176, WL)
camkey(290, WL)
camkey(306, W0)
camkey(TOTAL - 1, W0)

luma = make('luma', 1.45)
pimo = make('pimo', 1.7)
tuki = make('tuki', 1.4)
L0 = Vector((0.0, -1.35, Z0))
P0 = Vector((-1.05, -0.9, Z0))
P1 = Vector((-0.95, -1.5, Z0))
T0 = Vector((1.05, -0.9, Z0))
T1 = Vector((0.95, -1.5, Z0))
T.place(luma, 0, L0)
T.place(pimo, 0, P0)
T.place(tuki, 0, T0)
T.turn(luma, 0, 0)
T.turn(pimo, 0, 30)
T.turn(tuki, 0, -30)

lm = bpy.data.materials['luma_body']
pb = lm.node_tree.nodes['Principled BSDF']
pb.inputs['Emission Color'].default_value = (1.0, 0.62, 0.08, 1)
em = pb.inputs['Emission Strength']
for f, v in ((0, 0.35), (150, 0.35), (210, 0.04), (300, 0.04), (420, 0.08), (560, 0.3), (660, 0.55), (TOTAL - 1, 0.55)):
    em.default_value = v
    em.keyframe_insert('default_value', frame=f)
bpy.ops.object.light_add(type='POINT', location=(0, -0.45, 1.0))
glow = bpy.context.object
glow.parent = luma['hold']
glow.data.color = (1.0, 0.75, 0.35)
glow.data.shadow_soft_size = 0.4
for f, v in ((0, 25), (150, 25), (210, 2), (300, 2), (420, 5), (560, 25), (660, 45), (TOTAL - 1, 45)):
    glow.data.energy = v
    glow.data.keyframe_insert('energy', frame=f)

bm_ = [M(c, rough=0.6, coat=0.4) for c in ((0.95, 0.4, 0.5), (0.4, 0.7, 0.95), (1.0, 0.8, 0.3))]
BK = Vector((-1.25, -1.45, Z0))
blocks = []
for k in range(3):
    o = C.rounded_box('pb', tuple(BK + Vector((0.02 * (k % 2), 0, 0.09 + 0.18 * k))), (0.18, 0.18, 0.18), 0.03, bm_[k], None)
    blocks.append(o)
for k, o in enumerate(blocks):
    sz = tuple(o.scale)
    K(o, 'scale', 0, (0, 0, 0) if k else sz)
    if k:
        K(o, 'scale', 104 + k * 12 - 1, (0, 0, 0))
        K(o, 'scale', 104 + k * 12 + 4, tuple(v * 1.15 for v in sz))
        K(o, 'scale', 104 + k * 12 + 8, sz)

C.wave(luma, 'R', 14, cycles=2, period=8)
T.arm(luma, 'L', 30, 0, None)
T.arm(luma, 'L', 36, fwd=-20, out=110)
T.arm(luma, 'L', 64, fwd=-20, out=110)
T.rest_arm(luma, 'L', 72)
T.turn(tuki, 56, -30)
T.turn(tuki, 62, -70)
tuki['hold'].location = T0
gesture(tuki, 'hops', 66)
gesture(tuki, 'hops', 112)
T.turn(pimo, 96, 30)
T.turn(pimo, 102, 140)
T.arm(pimo, 'L', 108, 0, None)
T.arm(pimo, 'L', 114, fwd=-50, out=40)
T.arm(pimo, 'L', 140, fwd=-50, out=40)
T.rest_arm(pimo, 'L', 148)
T.turn(luma, 150, 0)
K(luma['spin'], 'rotation_euler', 170, (0, 0, 0))
K(luma['spin'], 'rotation_euler', 190, (math.radians(10), 0, 0))
K(luma['spin'], 'rotation_euler', 300, (math.radians(10), 0, 0))
K(luma['spin'], 'rotation_euler', 312, (0, 0, 0))
S(luma, 170, (1, 1, 1))
S(luma, 190, (0.97, 0.97, 0.93))
S(luma, 300, (0.97, 0.97, 0.93))
S(luma, 316, (1, 1, 1))
for e in luma['eyes']:
    if e is None:
        continue
    K(e, 'scale', 180, (1, 1, 1))
    K(e, 'scale', 190, (1, 1, 0.75))
    K(e, 'scale', 300, (1, 1, 0.75))
    K(e, 'scale', 310, (1, 1, 1))
T.turn(tuki, 150, -70)
T.turn(tuki, 160, 50)

T.turn(pimo, 226, 140)
T.turn(pimo, 236, 45)
hop_to(pimo, 270, P0, P1, 16, apex=0.3)
T.turn(pimo, 286, 45)
T.turn(pimo, 292, 60)
T.arm(pimo, 'R', 298, 0, None)
T.arm(pimo, 'R', 304, fwd=-40, out=50)
T.arm(pimo, 'R', 330, fwd=-40, out=50)
T.rest_arm(pimo, 'R', 338)
T.turn(tuki, 336, 50)
T.turn(tuki, 344, -60)
hop_to(tuki, 350, T0, T1, 16, apex=0.3)
T.turn(tuki, 368, -60)
for ch in (pimo, tuki):
    S(ch, 380, (1, 1, 1))
    S(ch, 388, (1.05, 1.05, 0.93))
    S(ch, 640, (1.05, 1.05, 0.93))
    S(ch, 648, (1, 1, 1))
T.turn(luma, 316, 0)
T.turn(luma, 324, -15)
T.turn(luma, 400, 15)
T.turn(luma, 410, 0)

star = spawn('star_plush', 0, 5301, (1.0, 0.85, 0.35), (0, -1.55, 2.0), 1.4, 0)
star.rotation_euler = (0, 0, 0)
T.pop_in(star, 446, 1.4, d=10)
for k, f in enumerate(range(456, 620, 16)):
    K(star, 'location', f, (0.05 * math.sin(k), -1.55, 2.0 + 0.05 * (1 if k % 2 else -1)))
    K(star, 'rotation_euler', f, (0, math.radians(8 * (1 if k % 2 else -1)), 0))
T.pop_out(star, 620, 1.4, d=8)
T.arm(luma, 'R', 430, 0, None)
T.arm(luma, 'R', 438, fwd=-20, out=120)
T.arm(luma, 'R', 470, fwd=-20, out=120)
T.rest_arm(luma, 'R', 478)
gesture(luma, 'sway', 540)
luma['hold'].location = L0
gesture(luma, 'bounce', 662)

for k, f in enumerate(range(684, 716, 6)):
    T.arm(tuki, 'L', f, fwd=-55, out=10 if k % 2 else 35)
    T.arm(tuki, 'R', f, fwd=-55, out=10 if k % 2 else 35)
T.rest_arm(tuki, 'L', 722)
T.rest_arm(tuki, 'R', 722)
gesture(tuki, 'sway', 726)
gesture(tuki, 'spin', 770)
tuki['hold'].location = T1
gesture(tuki, 'bounce', 792)
T.turn(pimo, 690, 60)
T.turn(pimo, 698, 30)
C.wave(pimo, 'R', 760, cycles=2, period=8)

T.lines(EID, LINES)
T.blinks(luma, (60, 140, 350, 480, 600, 720))
T.blinks(pimo, (50, 170, 320, 450, 580, 740))
T.blinks(tuki, (90, 230, 400, 520, 650, 780))
