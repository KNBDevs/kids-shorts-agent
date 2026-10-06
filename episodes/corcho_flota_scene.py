from stage import *
from episodes.corcho_flota_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA
EID = 'corcho_flota'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0.0, -6.5, 2.05), (0.0, -1.4, 0.8), 31)
WT = ((0.0, -5.4, 1.75), (0.0, -1.7, 1.0), 25)
WS = ((0.0, -3.15, 1.22), (0.0, -2.0, 0.9), 30)
camkey(0, WT)
camkey(70, WT)
camkey(80, WS)
camkey(170, WS)
camkey(182, WT)
camkey(228, WT)
camkey(238, WS)
camkey(500, WS)
camkey(512, WT)
camkey(640, WT)
camkey(650, WS)
camkey(745, WS)
camkey(756, W0)
camkey(TOTAL - 1, W0)

spawn('low_table', 0, 2201, (0.62, 0.8, 0.98), (0.0, -2.0, Z0), 1.0, 0)
TOP = Z0 + 0.62
TUB = Vector((0.0, -2.0, TOP + 0.008))
tub = spawn('water_tray', 1, 618, 'candy', tuple(TUB), 1.0, 0)
for o in tub.children_recursive:
    if o.type == 'MESH' and o.data.materials and o.data.materials[0].name.startswith('pa'):
        a = o.data.materials[0].node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value
        o.data.materials.clear()
        o.data.materials.append(MA((0.4, 0.7, 1.0), 0.16, rough=0.04, emit=0.05) if o.name.startswith('water') else MA((0.95, 0.98, 1.0), 0.08))
SURF = TUB.z + 0.012 + 0.26 * 0.72
FLOOR = TUB.z + 0.012
C.rounded_box('surf', (0, -2.0, SURF), (0.59, 0.33, 0.004), 0.002, MA((0.4, 0.72, 1.0), 0.42, rough=0.03, emit=0.12), None)
spawn('snack_plate', 1, 3150, (0.5, 0.75, 0.6), (0.48, -1.82, TOP), 0.42, 0)


def sticker(parent, front, z, style, seed):
    st = spawn('boat_sticker', style, seed, 'candy', (0, front, z), 0.85, 0, parent=parent)
    st.rotation_euler = (math.radians(90), 0, 0)
    return st


stone = spawn('float_item', 1, 41, (0.35, 0.45, 0.62), (0, 0, 0), 1.6, 0)
sticker(stone, -0.0625, 0.034, 0, 7)
cork = spawn('float_item', 0, 42, 'fresh', (0, 0, 0), 1.6, 0)
for o in (stone, cork):
    for c in o.children_recursive:
        if hasattr(c, 'cycles'):
            c.cycles.use_motion_blur = False

S_HAND = Vector((-0.62, -1.95, TOP + 0.36))
S_ABOVE = Vector((-0.12, -2.0, SURF + 0.18))
S_SURF = Vector((-0.12, -2.0, SURF - 0.04))
S_BOT = Vector((-0.12, -2.02, FLOOR))
K(stone, 'location', 0, tuple(S_HAND))
K(stone, 'location', 56, tuple(S_HAND))
for t in range(0, 23, 2):
    u = t / 22
    p = S_HAND.lerp(S_ABOVE, u)
    p.z += 0.12 * 4 * u * (1 - u)
    K(stone, 'location', 72 + t, tuple(p))
K(stone, 'location', 100, tuple(S_ABOVE))
K(stone, 'location', 106, tuple(S_SURF))
K(stone, 'location', 128, tuple(S_BOT))
K(stone, 'rotation_euler', 100, (0, 0, 0))
K(stone, 'rotation_euler', 128, (0, math.radians(8), math.radians(6)))

bub_m = MA((0.95, 0.98, 1.0), 0.5, rough=0.05, emit=0.3)
for k in range(7):
    b = C.sphere('bub', (0, 0, 0), (0.01, 0.01, 0.01), bub_m, None, 10)
    f0 = 112 + k * 4
    st = S_BOT + Vector((0.03 * math.sin(k * 2.1), 0, 0.06))
    K(b, 'scale', 0, (0, 0, 0))
    K(b, 'scale', f0 - 1, (0, 0, 0))
    K(b, 'scale', f0, (0.008 + 0.002 * (k % 3),) * 3)
    K(b, 'location', f0, tuple(st))
    K(b, 'location', f0 + 18, tuple(st + Vector((0.01, 0, SURF - st.z - 0.01))))
    K(b, 'scale', f0 + 17, (0.008,) * 3)
    K(b, 'scale', f0 + 19, (0, 0, 0))

C_HAND = Vector((0.62, -2.0, TOP + 0.36))
C_ABOVE = Vector((0.14, -2.0, SURF + 0.18))
C_FLOAT = Vector((0.14, -2.0, SURF - 0.045))
K(cork, 'location', 0, tuple(C_HAND))
K(cork, 'scale', 0, (0, 0, 0))
K(cork, 'scale', 214, (0, 0, 0))
K(cork, 'scale', 222, (1.6, 1.6, 1.6))
K(cork, 'location', 230, tuple(C_HAND))
for t in range(0, 21, 2):
    u = t / 20
    p = C_HAND.lerp(C_ABOVE, u)
    p.z += 0.1 * 4 * u * (1 - u)
    K(cork, 'location', 232 + t, tuple(p))
K(cork, 'location', 258, tuple(C_FLOAT + Vector((0, 0, -0.03))))
K(cork, 'location', 266, tuple(C_FLOAT + Vector((0, 0, 0.012))))
K(cork, 'location', 274, tuple(C_FLOAT))
for k, f in enumerate(range(282, 660, 24)):
    K(cork, 'location', f, tuple(C_FLOAT + Vector((0, 0, 0.008 if k % 2 else -0.004))))
    K(cork, 'rotation_euler', f, (math.radians(3 if k % 2 else -3), 0, math.radians(6 * math.sin(k))))
C_END = Vector((-0.16, -1.98, C_FLOAT.z))
for t in range(0, 91, 6):
    u = t / 90
    p = Vector((C_FLOAT.x, -2.0, C_FLOAT.z)).lerp(C_END, u * u * (3 - 2 * u))
    p.z += 0.006 * math.sin(t * 0.5)
    K(cork, 'location', 672 + t, tuple(p))
    K(cork, 'rotation_euler', 672 + t, (math.radians(3 * math.sin(t * 0.4)), 0, math.radians(-8 * u)))

st2 = spawn('boat_sticker', 2, 19, 'candy', (0, 0, 0), 0.85, 0)
K(st2, 'scale', 0, (0, 0, 0))
K(st2, 'scale', 596, (0, 0, 0))
K(st2, 'scale', 604, (0.95, 0.95, 0.95))
K(st2, 'location', 596, (-0.6, -1.9, TOP + 0.42))
K(st2, 'rotation_euler', 596, (math.radians(90), 0, math.radians(20)))
K(st2, 'location', 618, (-0.1, -2.1, TOP + 0.45))
K(st2, 'location', 632, tuple(C_FLOAT + Vector((0, -0.12, 0.08))))
K(st2, 'rotation_euler', 632, (math.radians(90), 0, 0))
K(st2, 'scale', 632, (0.95, 0.95, 0.95))
K(st2, 'scale', 634, (0, 0, 0))
st3 = sticker(cork, -0.0645, 0.05, 2, 19)
K(st3, 'scale', 0, (0, 0, 0))
K(st3, 'scale', 633, (0, 0, 0))
K(st3, 'scale', 637, (1.0, 1.0, 1.0))
K(st3, 'scale', 641, (0.85, 0.85, 0.85))

spark_m = C.mat('spk', (1, 0.95, 0.6), rough=0.3, emit=3.0)
for k in range(4):
    g = C.empty('spk', None, (0, 0, 0))
    C.sphere('spkb', (0, 0, 0), (0.014,) * 3, spark_m, g, 10)
    g.location = S_BOT + Vector((math.cos(k * 1.57) * 0.14, -0.09, 0.06 + 0.03 * (k % 2)))
    K(g, 'scale', 0, (0, 0, 0))
    for f0 in (366, 446):
        K(g, 'scale', f0 + k * 4, (0, 0, 0))
        K(g, 'scale', f0 + k * 4 + 5, (1, 1, 1))
        K(g, 'scale', f0 + k * 4 + 12, (0, 0, 0))

bolita = make('bolita', 1.4)
ruki = make('ruki', 1.45)
B0 = Vector((-0.95, -1.62, Z0))
R0 = Vector((0.95, -1.72, Z0))
T.place(bolita, 0, B0)
T.turn(bolita, 0, 35)
T.place(ruki, 0, R0)
T.turn(ruki, 0, -35)
T.arm(bolita, 'R', 0, fwd=-80, out=20)
T.arm(bolita, 'R', 56, fwd=-80, out=20)
T.arm(bolita, 'R', 72, fwd=-60, out=10)
T.rest_arm(bolita, 'R', 86)
gesture(bolita, 'bounce', 20)
T.turn(bolita, 120, 50)
S(bolita, 126, (1, 1, 1))
S(bolita, 132, (1.1, 1.1, 0.85))
S(bolita, 156, (1.1, 1.1, 0.85))
S(bolita, 164, (1, 1, 1))
T.turn(bolita, 180, 35)
T.arm(ruki, 'L', 210, 0, None)
T.arm(ruki, 'L', 220, fwd=-80, out=20)
T.arm(ruki, 'L', 236, fwd=-80, out=20)
T.rest_arm(ruki, 'L', 250)
T.turn(ruki, 200, -45)
T.turn(ruki, 290, -40)
T.turn(ruki, 360, -55)
T.turn(ruki, 440, -35)
gesture(ruki, 'breathe', 446)
T.turn(bolita, 300, 45)
T.turn(bolita, 520, 35)
T.place(bolita, 560, B0)
gesture(bolita, 'hops', 564)
T.arm(bolita, 'R', 590, 0, None)
T.arm(bolita, 'R', 598, fwd=-85, out=20)
T.arm(bolita, 'R', 620, fwd=-70, out=10)
T.rest_arm(bolita, 'R', 634)
T.turn(bolita, 660, 40)
C.wave(bolita, 'R', 676, cycles=4, period=8)
T.turn(ruki, 660, -30)
T.place(ruki, 740, R0)
T.place(bolita, 740, B0)
gesture(ruki, 'bounce', 744)
gesture(bolita, 'bounce', 748)

T.lines(EID, LINES)
T.blinks(bolita, (40, 170, 300, 430, 560, 720))
T.blinks(ruki, (90, 230, 380, 520, 650, 770))
