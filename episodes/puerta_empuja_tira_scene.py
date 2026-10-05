from stage import *
from episodes.puerta_empuja_tira_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M
EID = 'puerta_empuja_tira'
Z0 = 0.08
auto_dress(EID, ENV)

XA = 0.0
XB = 2.7
W0 = ((XA, -7.2, 1.45), (XA, -1.1, 1.15), 36)
W1 = ((XB, -7.2, 1.45), (XB, -1.1, 1.15), 36)
WA = ((XA + 0.35, -4.6, 2.7), (XA + 0.3, -1.25, 0.3), 40)
WB2 = ((XB + 0.35, -4.6, 2.7), (XB + 0.3, -1.25, 0.3), 40)
camkey(0, W0)
camkey(166, W0)
camkey(180, WA)
camkey(300, WA)
camkey(314, W0)
camkey(470, W0)
camkey(496, W1)
camkey(590, W1)
camkey(604, WB2)
camkey(676, WB2)
camkey(690, W1)
camkey(TOTAL - 1, W1)

DY = -0.55
doorA = spawn('play_door', 0, 6601, (0.55, 0.75, 0.98), (XA, DY, Z0), 1.0, 0)
doorB = spawn('play_door', 2, 6602, (0.98, 0.62, 0.55), (XB, DY, Z0), 1.0, 0)
hA = next(o for o in doorA.children_recursive if o.name.startswith('door_hinge'))
hB = next(o for o in doorB.children_recursive if o.name.startswith('door_hinge'))

arrow_m = C.mat('arrow', (1.0, 0.45, 0.2), rough=0.35, coat=0.6, emit=0.4)


def floor_arrow(loc, toward_camera):
    g = C.empty('arrow', None, loc, (0, 0, math.radians(0 if toward_camera else 180)))
    C.rounded_box('ash', (0, 0.16, 0.014), (0.17, 0.5, 0.028), 0.012, arrow_m, g)
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.28, depth=0.028, location=(0, -0.16, 0.014), rotation=(0, 0, math.radians(-90)))
    hd = bpy.context.object
    hd.data.materials.append(arrow_m)
    hd.parent = g
    bv = hd.modifiers.new('b', 'BEVEL')
    bv.width = 0.02
    bv.segments = 3
    return g


aA = floor_arrow((XA + 0.55, DY - 0.8, Z0 + 0.002), True)
aB = floor_arrow((XB + 0.55, DY - 0.8, Z0 + 0.002), False)
ai = arrow_m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
for f in range(0, TOTAL, 16):
    ai.default_value = 0.3
    ai.keyframe_insert('default_value', frame=f)
    ai.default_value = 1.6
    ai.keyframe_insert('default_value', frame=f + 8)


def slide(a, base, d, f0, f1):
    for f in range(f0, f1, 16):
        K(a, 'location', f, tuple(base))
        K(a, 'location', f + 12, tuple(base + d))
        K(a, 'location', f + 13, tuple(base))


slide(aA, Vector((XA + 0.55, DY - 0.8, Z0 + 0.002)), Vector((0, -0.18, 0)), 160, 420)
slide(aB, Vector((XB + 0.55, DY - 0.8, Z0 + 0.002)), Vector((0, 0.18, 0)), 560, 700)
for a in (aA, aB):
    set_interp(a, 'LINEAR')

K(hA, 'rotation_euler', 0, (0, 0, 0))


def rattle(h, f0, n=4, a=2.5):
    for k in range(n):
        K(h, 'rotation_euler', f0 + k * 3, (0, 0, math.radians(a * (1 if k % 2 else -1))))
    K(h, 'rotation_euler', f0 + n * 3, (0, 0, 0))


rattle(hA, 62)
rattle(hA, 82)
K(hA, 'rotation_euler', 404, (0, 0, 0))
K(hA, 'rotation_euler', 418, (0, 0, math.radians(-45)))
K(hA, 'rotation_euler', 426, (0, 0, math.radians(-60)))
K(hA, 'rotation_euler', 432, (0, 0, math.radians(-57)))
K(hA, 'rotation_euler', 458, (0, 0, math.radians(-57)))
K(hA, 'rotation_euler', 474, (0, 0, 0))
K(hB, 'rotation_euler', 0, (0, 0, 0))
rattle(hB, 542, 4, 2)
rattle(hB, 558, 4, 2)
K(hB, 'rotation_euler', 748, (0, 0, 0))
K(hB, 'rotation_euler', 762, (0, 0, math.radians(70)))
K(hB, 'rotation_euler', 770, (0, 0, math.radians(84)))
K(hB, 'rotation_euler', 776, (0, 0, math.radians(80)))

gruno = make('gruno', 1.5)
bopi = make('bopi', 1.45)
G0 = Vector((XA - 1.0, -1.15, Z0))
GA = Vector((XA - 0.3, -1.25, Z0))
GB = Vector((XB - 0.3, -1.3, Z0))
BS = Vector((XA + 2.2, -1.2, Z0))
B0 = Vector((XA + 1.0, -1.2, Z0))
BA = Vector((XA + 0.55, -1.2, Z0))
BB = Vector((XB + 1.05, -1.3, Z0))
T.place(gruno, 0, G0)
T.turn(gruno, 0, 30)
T.place(bopi, 0, BS)
T.turn(bopi, 0, -90)

C.wave(gruno, 'R', 14, cycles=2, period=8)
T.turn(gruno, 38, 30)
T.turn(gruno, 44, 160)
hop_to(gruno, 46, G0, GA, 12, apex=0.3)
T.turn(gruno, 58, 175)
for f in (62, 82):
    K(gruno['hold'], 'location', f - 2, tuple(GA))
    K(gruno['hold'], 'location', f + 1, tuple(GA + Vector((0, 0.1, 0))))
    K(gruno['hold'], 'location', f + 6, tuple(GA))
    S(gruno, f + 1, (1.1, 1.1, 0.9))
    S(gruno, f + 6, (1, 1, 1))
T.turn(gruno, 96, 175)
T.turn(gruno, 104, 10)
for k, f in enumerate(range(106, 150, 8)):
    T.turn(gruno, f, 10 + (10 if k % 2 else -10))
T.turn(gruno, 152, 10)

for k in range(5):
    u = k / 4
    f = 130 + k * 8
    K(bopi['hold'], 'location', f, tuple(BS.lerp(B0, u) + Vector((0, 0, 0.05 * (k % 2)))))
T.turn(bopi, 130, -90)
T.turn(bopi, 166, -90)
T.turn(bopi, 172, -25)
T.arm(bopi, 'R', 176, 0, None)
T.arm(bopi, 'R', 182, fwd=-50, out=40)
T.arm(bopi, 'R', 300, fwd=-50, out=40)
T.rest_arm(bopi, 'R', 308)
T.turn(gruno, 170, 10)
T.turn(gruno, 176, -100)
hop_to(gruno, 180, GA, G0, 14, apex=0.3)
T.turn(gruno, 196, -100)
T.turn(gruno, 204, 20)
T.turn(bopi, 380, -25)
T.turn(bopi, 386, -100)
hop_to(bopi, 388, B0, BA, 10, apex=0.25)
T.turn(bopi, 398, -170)
T.arm(bopi, 'L', 398, 0, None)
T.arm(bopi, 'L', 404, fwd=-70, out=20)
T.arm(bopi, 'L', 412, fwd=-40, out=20)
T.rest_arm(bopi, 'L', 424)
K(bopi['hold'], 'location', 404, tuple(BA))
K(bopi['hold'], 'location', 418, tuple(BA + Vector((0.1, -0.15, 0))))
T.turn(bopi, 430, -170)
T.turn(bopi, 438, -20)
bopi['hold'].location = BA + Vector((0.1, -0.15, 0))
gesture(bopi, 'hops', 440)
gruno['hold'].location = G0
gesture(gruno, 'bounce', 432)

T.turn(gruno, 470, -30)
T.turn(gruno, 478, 90)
G_mid = G0.lerp(GB, 0.5) + Vector((0, -0.5, 0))
hop_to(gruno, 480, G0, G_mid, 12, apex=0.4)
hop_to(gruno, 494, G_mid, GB, 12, apex=0.4)
T.turn(gruno, 508, 90)
T.turn(gruno, 516, 20)
C.wave(gruno, 'R', 512, cycles=2, period=8)
T.turn(gruno, 532, 20)
T.turn(gruno, 538, 175)
for f in (544, 560):
    K(gruno['hold'], 'location', f - 2, tuple(GB))
    K(gruno['hold'], 'location', f + 3, tuple(GB + Vector((0, -0.12, 0))))
    K(gruno['hold'], 'location', f + 8, tuple(GB))
    S(gruno, f + 3, (0.92, 0.92, 1.08))
    S(gruno, f + 8, (1, 1, 1))
T.turn(gruno, 576, 175)
T.turn(gruno, 584, 20)

BAm = BA + Vector((0.1, -0.15, 0))
B_mid = BAm.lerp(BB, 0.5)
T.turn(bopi, 474, -20)
T.turn(bopi, 480, 90)
hop_to(bopi, 484, BAm, B_mid, 14, apex=0.35)
hop_to(bopi, 500, B_mid, BB, 14, apex=0.35)
T.turn(bopi, 516, 90)
T.turn(bopi, 524, -30)
T.arm(bopi, 'R', 594, 0, None)
T.arm(bopi, 'R', 600, fwd=-50, out=40)
T.arm(bopi, 'R', 650, fwd=-50, out=40)
T.rest_arm(bopi, 'R', 658)

T.turn(gruno, 690, 20)
T.turn(gruno, 698, 0)
for k, f in enumerate(range(700, 740, 8)):
    S(gruno, f, (1.05, 1.05, 0.95) if k % 2 else (1, 1, 1))
T.turn(gruno, 740, 0)
T.turn(gruno, 746, 175)
K(gruno['hold'], 'location', 744, tuple(GB))
K(gruno['hold'], 'location', 756, tuple(GB + Vector((0, 0.1, 0))))
K(gruno['hold'], 'location', 764, tuple(GB + Vector((0, 0.14, 0.04))))
K(gruno['hold'], 'location', 770, tuple(GB + Vector((0, 0.12, 0))))
S(gruno, 756, (1.08, 1.08, 0.92))
S(gruno, 764, (0.95, 0.95, 1.06))
S(gruno, 772, (1, 1, 1))
T.turn(gruno, 786, 175)
T.turn(gruno, 796, 30)
bopi['hold'].location = BB
gesture(bopi, 'bounce', 790)

T.lines(EID, LINES)
T.blinks(gruno, (120, 260, 380, 520, 640, 800))
T.blinks(bopi, (200, 300, 460, 580, 700, 810))
word3d('TIRA', (0.9, 0.3, 0.1), (XA, -1.0, 2.35), 236, 470, size=0.42, max_w=1.0)
word3d('EMPUJA', (0.15, 0.4, 0.9), (XB, -1.0, 2.35), 596, TOTAL - 4, size=0.42, max_w=1.2)
