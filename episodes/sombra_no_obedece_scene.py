from stage import *
from episodes.sombra_no_obedece_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress
EID = 'sombra_no_obedece'
Z0 = 0.08
auto_dress(EID, ENV)
for l in bpy.data.lights:
    if l.type == 'SUN':
        l.energy = 0.6
    else:
        l.energy *= 0.2
sc.world.node_tree.nodes['Background'].inputs[1].default_value = 0.2

WY = 0.5
wall_m = C.mat('wall', (0.97, 0.94, 0.88), rough=0.92)
frame_m = C.mat('wallframe', (0.62, 0.48, 0.85), rough=0.45, coat=0.4)
wall = C.empty('wall', None, (0.1, WY, 0))
C.rounded_box('wall.pane', (0, 0.06, 1.75), (4.0, 0.1, 3.5), 0.04, wall_m, wall)
C.tube('wall.frame', [(-2.0, -0.01, 0), (-2.0, -0.01, 3.32), (-1.82, -0.01, 3.5), (1.82, -0.01, 3.5), (2.0, -0.01, 3.32), (2.0, -0.01, 0)], 0.045, frame_m, wall)
for x in (-2.0, 2.0):
    C.sphere('wall.cap', (x, -0.01, 0.04), (0.09, 0.09, 0.05), frame_m, wall, 20)

L0 = Vector((1.0, -2.45, Z0))
L1 = Vector((-0.95, -2.45, Z0))
lamp = spawn('floor_lamp', 0, 77, (1.0, 0.62, 0.2), tuple(L0), 0.75, 0)
bpy.ops.object.light_add(type='SPOT', location=(0, 0.3, 1.05))
spot = bpy.context.object
spot.parent = lamp
spot.data.energy = 320
spot.data.color = (1.0, 0.93, 0.8)
spot.data.spot_size = math.radians(110)
spot.data.spot_blend = 0.35
spot.data.shadow_soft_size = 0.03
aim = C.empty('aim', None, (0.1, WY, 1.0))
tr = spot.constraints.new('TRACK_TO')
tr.target = aim
tr.track_axis = 'TRACK_NEGATIVE_Z'
tr.up_axis = 'UP_Y'
K(lamp, 'location', 0, tuple(L0))
K(lamp, 'location', 436, tuple(L0))
K(lamp, 'location', 500, tuple(L1))
for k, f in enumerate(range(440, 500, 6)):
    K(lamp, 'rotation_euler', f, (0, math.radians(3 if k % 2 else -3), 0))
K(lamp, 'rotation_euler', 502, (0, 0, 0))

W0 = ((0.1, -7.9, 1.85), (0.1, -0.9, 1.4), 33)
camkey(0, W0)
camkey(560, W0)
camkey(600, ((-0.05, -8.0, 1.8), (-0.05, -0.8, 1.35), 33))
camkey(TOTAL - 1, ((-0.05, -8.0, 1.8), (-0.05, -0.8, 1.35), 33))

pimo = make('pimo', 1.8)
bolita = make('bolita', 1.5)
gruno = make('gruno', 1.85)
PP = Vector((0.2, -0.75, Z0))
B0 = Vector((0.71, -1.84, Z0))
B1 = Vector((-0.7, -1.05, Z0))
B2 = Vector((1.45, -2.42, Z0))
B3 = B2 + (L1 - L0)
B4 = Vector((0.95, -0.95, Z0))
G0 = Vector((-2.4, -1.9, Z0))
G1 = Vector((-0.5, -1.3, Z0))
G2 = Vector((-0.45, -0.62, Z0))
T.place(pimo, 0, PP)
T.turn(pimo, 0, 20)
T.turn(pimo, 30, 20)
T.turn(pimo, 40, 150)
T.place(bolita, 0, B0)
T.turn(bolita, 0, -20)
T.place(gruno, 0, G0 + Vector((0, 0, -4)))
T.place(gruno, 586, G0 + Vector((0, 0, -4)))

C.wave(pimo, 'R', 10, cycles=2, period=8)
T.turn(pimo, 56, 150)
T.turn(pimo, 64, 20)
T.turn(pimo, 110, 20)
T.turn(pimo, 118, 40)
C.wave(bolita, 'L', 60, cycles=2, period=8)
T.turn(bolita, 116, -20)
T.turn(bolita, 124, -10)
S(bolita, 128, (1, 1, 1))
S(bolita, 132, (1.08, 1.08, 0.92))
S(bolita, 138, (1, 1, 1))
T.turn(bolita, 184, 0)
hop_to(bolita, 186, B0, B1, 18, apex=0.5)
T.turn(bolita, 206, 30)
T.turn(pimo, 206, 40)
T.turn(pimo, 214, 25)
T.turn(pimo, 234, 25)
T.turn(pimo, 242, 155)
C.wave(pimo, 'R', 244, cycles=3, period=8)
C.wave(pimo, 'L', 250, cycles=2, period=8)
T.turn(pimo, 274, 155)
T.turn(pimo, 284, 0)

T.turn(bolita, 290, 30)
T.turn(bolita, 296, 60)
T.turn(bolita, 300, 0)
T.turn(bolita, 406, 0)
T.turn(bolita, 410, 60)
hop_to(bolita, 412, B1, B2, 22, apex=0.6)
T.turn(bolita, 352, 0)
T.turn(pimo, 352, 0)
T.turn(bolita, 432, 70)
T.arm(bolita, 'L', 430, 0, None)
T.arm(bolita, 'L', 436, fwd=-60, out=30)
T.arm(bolita, 'L', 506, fwd=-60, out=30)
T.rest_arm(bolita, 'L', 514)
K(bolita['hold'], 'location', 436, tuple(B2))
for f in range(440, 501, 4):
    u = (f - 436) / 64
    u = u * u * (3 - 2 * u)
    p = B2.lerp(B3, u)
    p.z += 0.06 * abs(math.sin((f - 436) * 0.5))
    K(bolita['hold'], 'location', f, tuple(p))
K(bolita['hold'], 'location', 500, tuple(B3))
T.turn(pimo, 436, 0)
T.turn(pimo, 470, 120)
T.turn(pimo, 506, 120)
T.turn(pimo, 516, 10)
T.arm(pimo, 'R', 520, 0, None)
T.arm(pimo, 'R', 526, fwd=-30, out=80)
T.arm(pimo, 'L', 520, 0, None)
T.arm(pimo, 'L', 532, fwd=-30, out=80)
T.rest_arm(pimo, 'R', 572)
T.rest_arm(pimo, 'L', 572)
T.turn(bolita, 520, 70)
T.turn(bolita, 528, 20)
hop_to(bolita, 556, B3, B4, 16, apex=0.45)
P2 = Vector((0.35, -0.68, Z0))
hop_to(pimo, 578, PP, P2, 12, apex=0.3)
T.turn(bolita, 574, 30)

hop_to(gruno, 588, G0, G1, 18, apex=0.8)
T.turn(gruno, 588, 30)
T.turn(gruno, 610, 150)
C.wave(gruno, 'R', 618, cycles=3, period=8)
T.turn(gruno, 650, 150)
T.turn(gruno, 660, 20)
T.turn(pimo, 610, 10)
T.turn(pimo, 620, -40)
T.turn(bolita, 670, 30)
T.turn(bolita, 676, -10)
gesture(bolita, 'bounce', 712)
T.turn(gruno, 736, 20)
hop_to(gruno, 742, G1, G2, 16, apex=0.4)
T.turn(gruno, 760, 160)
T.turn(gruno, 772, 160)
T.turn(gruno, 782, 10)
S(gruno, 790, (1, 1, 1))
S(gruno, 796, (1.06, 1.06, 0.94))
S(gruno, 802, (1, 1, 1))
gesture(pimo, 'hops', 800)
T.turn(bolita, 790, 0)
C.wave(bolita, 'L', 806, cycles=2, period=8)

T.lines(EID, LINES)
T.blinks(pimo, (40, 150, 280, 400, 540, 650, 780))
T.blinks(bolita, (30, 170, 330, 460, 600, 720, 820))
T.blinks(gruno, (640, 720, 810))
