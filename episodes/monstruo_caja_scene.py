from stage import *
from episodes.monstruo_caja_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M
EID = 'monstruo_caja'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0, -7.0, 1.35), (0, -1.15, 1.05), 37)
WB = ((0.05, -5.0, 1.55), (0.05, -1.6, 0.75), 38)
camkey(0, W0)
camkey(250, W0)
camkey(266, WB)
camkey(470, WB)
camkey(486, W0)
camkey(TOTAL - 1, W0)

BX = Vector((0.0, -1.85, Z0))
SB = 1.3
box = spawn('lidded_box', 0, 9101, (0.98, 0.72, 0.42), tuple(BX), SB, 0)
hinge = next(o for o in box.children_recursive if o.name.startswith('lid_hinge'))
spk = spawn('toy_speaker', 1, 9102, (0.55, 0.62, 0.95), tuple(BX + Vector((0, 0, 0.04))), 1.25, 0)
led_m = next(m for m in bpy.data.materials if m.name.startswith('led'))
D = 0.5 * SB
H = 0.42 * SB
hole_m = M((0.12, 0.1, 0.16), rough=0.6)
C.sphere('hole', tuple(BX + Vector((0.18, -D / 2 - 0.012, H * 0.7))), (0.05, 0.01, 0.05), hole_m, None, 20)
glow_m = C.mat('glow', (0.3, 1.0, 0.45), rough=0.2, emit=0.0)
C.sphere('glow', tuple(BX + Vector((0.18, -D / 2 - 0.016, H * 0.7))), (0.026, 0.008, 0.026), glow_m, None, 16)
gi = glow_m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
li = led_m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
for f in range(0, TOTAL, 12):
    for inp in (gi, li):
        inp.default_value = 4.0
        inp.keyframe_insert('default_value', frame=f)
        inp.default_value = 0.6
        inp.keyframe_insert('default_value', frame=f + 6)


def wobble(f0, n=6, a=4):
    for k in range(n):
        K(box, 'rotation_euler', f0 + k * 3, (0, math.radians(a * (1 if k % 2 else -1)), 0))
        K(box, 'location', f0 + k * 3, tuple(BX + Vector((0, 0, 0.02 * (k % 2)))))
    K(box, 'rotation_euler', f0 + n * 3, (0, 0, 0))
    K(box, 'location', f0 + n * 3, tuple(BX))


K(box, 'rotation_euler', 0, (0, 0, 0))
K(box, 'location', 0, tuple(BX))
wobble(12)
wobble(160, 5, 3)
K(hinge, 'rotation_euler', 0, (0, 0, 0))
K(hinge, 'rotation_euler', 388, (0, 0, 0))
K(hinge, 'rotation_euler', 396, (math.radians(-20), 0, 0))
K(hinge, 'rotation_euler', 410, (math.radians(-150), 0, 0))
K(hinge, 'rotation_euler', 416, (math.radians(-168), 0, 0))
K(spk, 'location', 0, tuple(BX + Vector((0, 0, 0.04))))
K(spk, 'location', 412, tuple(BX + Vector((0, 0, 0.04))))
K(spk, 'location', 424, tuple(BX + Vector((0, 0, 0.36))))
K(spk, 'location', 430, tuple(BX + Vector((0, 0, 0.32))))
for k, f in enumerate(range(690, 716, 4)):
    K(spk, 'scale', f, ((1.32,) * 3) if k % 2 == 0 else ((1.25,) * 3))
K(spk, 'scale', 689, (1.25,) * 3)
K(spk, 'scale', 718, (1.25,) * 3)

pimo = make('pimo', 1.7)
ruki = make('ruki', 1.45)
gruno = make('gruno', 1.5)
P0 = Vector((-0.85, -1.05, Z0))
P1 = Vector((-0.95, -1.55, Z0))
R0 = Vector((0.95, -0.9, Z0))
R1 = Vector((1.05, -1.0, Z0))
GS = Vector((-3.2, 0.35, Z0))
G1 = Vector((0.0, 0.35, Z0))
T.place(pimo, 0, P0)
T.turn(pimo, 0, 25)
T.place(ruki, 0, R0)
T.turn(ruki, 0, -25)
T.place(gruno, 0, GS)

S(pimo, 14, (1, 1, 1))
S(pimo, 18, (0.92, 0.92, 1.1))
S(pimo, 26, (1, 1, 1))
K(pimo['hold'], 'location', 16, tuple(P0))
K(pimo['hold'], 'location', 24, tuple(P0 + Vector((-0.08, 0.06, 0))))
for e in pimo['eyes']:
    if e is None:
        continue
    K(e, 'scale', 14, (1, 1, 1))
    K(e, 'scale', 20, (1.15, 1.15, 1.15))
    K(e, 'scale', 60, (1.15, 1.15, 1.15))
    K(e, 'scale', 70, (1, 1, 1))
P0b = P0 + Vector((-0.08, 0.06, 0))
T.turn(pimo, 100, 25)
T.turn(pimo, 108, 40)
T.arm(pimo, 'R', 108, 0, None)
T.arm(pimo, 'R', 114, fwd=-30, out=70)
T.arm(pimo, 'R', 150, fwd=-30, out=70)
T.rest_arm(pimo, 'R', 158)
T.turn(ruki, 150, -25)
T.turn(ruki, 160, -35)
T.turn(ruki, 186, -35)
T.turn(ruki, 194, -50)
for k in range(5):
    u = k / 4
    f = 200 + k * 14
    K(ruki['hold'], 'location', f, tuple(R0.lerp(R1, u)))
    if k < 4:
        K(ruki['hold'], 'location', f + 7, tuple(R0.lerp(R1, u + 0.125) + Vector((0, 0, 0.04))))
T.turn(ruki, 256, -50)
T.turn(ruki, 264, -40)
T.arm(ruki, 'R', 268, 0, None)
T.arm(ruki, 'R', 274, fwd=-40, out=60)
T.arm(ruki, 'R', 310, fwd=-40, out=60)
T.rest_arm(ruki, 'R', 318)
T.turn(pimo, 330, 40)
T.turn(pimo, 338, 30)
T.arm(ruki, 'R', 384, 0, None)
T.arm(ruki, 'R', 392, fwd=-70, out=40)
T.arm(ruki, 'R', 404, fwd=-80, out=55)
T.rest_arm(ruki, 'R', 414)
T.turn(ruki, 420, -40)
T.turn(ruki, 428, -15)
T.turn(pimo, 432, 30)
T.turn(pimo, 438, 45)
hop_to(pimo, 446, P0b, P1, 14, apex=0.35)
T.turn(pimo, 460, 45)
T.turn(pimo, 468, 20)
gesture(ruki, 'breathe', 500)

hop_to(gruno, 566, GS, GS.lerp(G1, 0.5), 12, apex=0.5)
hop_to(gruno, 580, GS.lerp(G1, 0.5), G1, 12, apex=0.5)
T.turn(gruno, 560, 80)
T.turn(gruno, 594, 80)
T.turn(gruno, 600, 25)
C.wave(gruno, 'R', 604, cycles=3, period=8)
T.turn(pimo, 570, 20)
T.turn(pimo, 578, -30)
T.turn(ruki, 570, -15)
T.turn(ruki, 578, -45)
T.turn(gruno, 686, 25)
K(gruno['spin'], 'rotation_euler', 694, (0, 0, math.radians(25)))
K(gruno['spin'], 'rotation_euler', 700, (0, 0, math.radians(70)))
K(gruno['spin'], 'rotation_euler', 706, (0, 0, math.radians(55)))
S(gruno, 694, (1, 1, 1))
S(gruno, 698, (0.94, 0.94, 1.1))
S(gruno, 704, (1.04, 1.04, 0.96))
S(gruno, 710, (1, 1, 1))
for e in gruno['eyes']:
    if e is None:
        continue
    K(e, 'scale', 694, (1, 1, 1))
    K(e, 'scale', 699, (1.2, 1.2, 1.25))
    K(e, 'scale', 740, (1.2, 1.2, 1.25))
    K(e, 'scale', 750, (1, 1, 1))
T.turn(pimo, 720, -30)
T.turn(pimo, 726, 20)
pimo['hold'].location = P1
gesture(pimo, 'hops', 760)
ruki['hold'].location = R1
gesture(ruki, 'bounce', 770)

T.lines(EID, LINES)
T.blinks(pimo, (80, 200, 300, 400, 520, 640, 790))
T.blinks(ruki, (60, 180, 330, 470, 600, 720))
T.blinks(gruno, (640, 780))
