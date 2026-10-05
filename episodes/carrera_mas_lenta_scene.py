from stage import *
from episodes.carrera_mas_lenta_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M
EID = 'carrera_mas_lenta'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0, -7.3, 1.35), (0, -1.1, 1.05), 35)
WR = ((0, -6.7, 1.4), (0, -0.9, 1.1), 33)
WT = ((-0.3, -6.4, 1.8), (-0.3, -1.3, 1.25), 35)
camkey(0, W0)
camkey(110, W0)
camkey(124, WR)
camkey(450, WR)
camkey(466, W0)
camkey(TOTAL - 1, W0)

FX = 1.3
fin = spawn('finish_line', 0, 7301, 'pastel', (FX, -1.0, 0.0), 1.0, 90)

BCOL = [(0.95, 0.3, 0.45), (0.25, 0.55, 0.95), (1.0, 0.72, 0.12), (0.3, 0.78, 0.4), (0.62, 0.38, 0.95)]
BS = 0.28


def block(col, k, parent=None):
    o = C.empty('blk', parent)
    C.rounded_box('blkb', (0, 0, BS / 2), (BS, BS, BS), BS * 0.22, M(col, rough=0.6, coat=0.3), o)
    C.sphere('blkd', (0, -BS * 0.5, BS / 2), (BS * 0.2, BS * 0.04, BS * 0.2), M(tuple(min(1, v * 0.6 + 0.4) for v in col), rough=0.6, coat=0.4), o, 16)
    return o


def top_of(ch):
    bpy.context.view_layer.update()
    zs = [(o.matrix_world @ Vector(c)).z for o in ch['root'].children_recursive if o.type == 'MESH' for c in o.bound_box]
    return max(zs)


tuki = make('tuki', 1.4)
ruki = make('ruki', 1.4)
gruno = make('gruno', 1.55)
TS = Vector((-1.2, -1.55, Z0))
TF = Vector((-0.2, -1.55, Z0))
RS = Vector((-1.5, -0.55, Z0))
RF = Vector((0.75, -0.55, Z0))
T.place(tuki, 0, TS)
T.place(ruki, 0, RS + Vector((-1.6, 0, 0)))
T.place(gruno, 0, Vector((-3.6, -1.0, Z0)))
th = top_of(tuki) - Z0
rh = top_of(ruki) - Z0
gh = top_of(gruno) - Z0

ttow = [block(BCOL[k], k, tuki['hold']) for k in range(4)]
for k, b in enumerate(ttow):
    b.location = (0.0, 0.0, th - 0.04 + k * BS)
rtow = [block(BCOL[(k + 1) % 5], k, ruki['hold']) for k in range(4)]
for k, b in enumerate(rtow):
    b.location = (0.0, 0.0, rh - 0.04 + k * BS)
gb = block(BCOL[4], 0, gruno['hold'])
gb.location = (0, 0.0, gh - 0.05)

T.turn(tuki, 0, 20)
T.turn(ruki, 0, 70)
T.turn(gruno, 0, 80)
C.wave(tuki, 'R', 12, cycles=2, period=8)
T.turn(tuki, 34, 20)
T.turn(tuki, 40, 75)
xs = [TS + (TF - TS) * (k / 4) for k in range(5)]
for k in range(4):
    hop_to(tuki, 44 + k * 9, xs[k], xs[k + 1], 9, apex=0.22)
T.place(tuki, 82, TF)
for k, b in enumerate(ttow):
    for f, a in ((40, 0), (50, 6 * (k + 1)), (58, -8 * (k + 1)), (66, 10 * (k + 1))):
        K(b, 'rotation_euler', f, (0, math.radians(a), 0))
    K(b, 'location', 66, (0.0, 0.0, th - 0.04 + k * BS))
fall_end = []
for k, b in enumerate(ttow):
    p0 = Vector((0.0, 0.0, th - 0.04 + k * BS))
    land = Vector((0.4 + 0.3 * k, -0.15 + 0.12 * (k % 2) - 0.05 * k, -Z0 + 0.0))
    f0 = 68 + k * 2
    for t in range(0, 17, 2):
        u = t / 16
        p = p0.lerp(land, u) + Vector((0, 0, 0.5 * 4 * u * (1 - u)))
        K(b, 'location', f0 + t, tuple(p))
        K(b, 'rotation_euler', f0 + t, (math.radians(30 * u * k), math.radians(10 * (k + 1) + 120 * u), math.radians(20 * u)))
    K(b, 'location', f0 + 19, tuple(land + Vector((0, 0, 0.04))))
    K(b, 'location', f0 + 22, tuple(land))
    K(b, 'rotation_euler', f0 + 22, (0, 0, math.radians(15 * k)))
    fall_end.append((land, f0 + 22))
T.turn(tuki, 82, 75)
T.turn(tuki, 90, 150)
S(tuki, 96, (1, 1, 1))
S(tuki, 100, (1.08, 1.08, 0.92))
S(tuki, 108, (1, 1, 1))
T.turn(tuki, 140, 150)
T.turn(tuki, 148, -40)

steps = 10
for k in range(steps + 1):
    u = k / steps
    f = 186 + k * 22
    p = RS.lerp(RF, u)
    K(ruki['hold'], 'location', f, tuple(p))
    if k < steps:
        mid = RS.lerp(RF, u + 0.5 / steps) + Vector((0, 0, 0.05))
        K(ruki['hold'], 'location', f + 11, tuple(mid))
K(ruki['hold'], 'location', 120, tuple(RS + Vector((-1.6, 0, 0))))
for k in range(4):
    p = RS + Vector((-1.6 + 0.4 * k, 0, 0))
    K(ruki['hold'], 'location', 130 + k * 12, tuple(p))
    K(ruki['hold'], 'location', 136 + k * 12, tuple(p + Vector((0.2, 0, 0.05))))
K(ruki['hold'], 'location', 178, tuple(RS))
K(ruki['hold'], 'location', 186, tuple(RS))
for k, b in enumerate(rtow):
    for j, f in enumerate(range(186, 410, 22)):
        K(b, 'rotation_euler', f, (0, math.radians((1.5 + 0.8 * k) * (1 if j % 2 else -1)), 0))
    K(b, 'rotation_euler', 412, (0, 0, 0))
T.turn(ruki, 160, 70)
T.turn(ruki, 404, 70)
T.turn(ruki, 412, 10)
gesture(ruki, 'breathe', 300)
T.turn(tuki, 300, -40)
T.turn(tuki, 306, 20)
T.turn(tuki, 360, 20)
T.turn(tuki, 366, 50)

RP = RF + Vector((0.42, -0.2, 0))
for k, b in enumerate(rtow):
    p0 = Vector((0.0, 0.0, rh - 0.04 + k * BS))
    p1 = (RP - RF) + Vector((0, 0, -Z0 + k * BS))
    f0 = 432 + k * 3
    K(b, 'location', f0, tuple(p0))
    K(b, 'location', f0 + 8, tuple(p0.lerp(p1, 0.5) + Vector((0, 0, 0.25))))
    K(b, 'location', f0 + 14, tuple(p1))
T.turn(ruki, 426, 10)
T.turn(ruki, 432, 60)
T.turn(ruki, 452, 60)
T.turn(ruki, 460, 0)
ruki['hold'].location = RF
gesture(ruki, 'hops', 462)
RB = Vector((-0.05, -0.25, Z0))
T.turn(ruki, 496, 0)
T.turn(ruki, 502, -110)
hop_to(ruki, 504, RF, RB, 16, apex=0.35)
T.turn(ruki, 522, -110)
T.turn(ruki, 530, -10)

T.turn(tuki, 466, 50)
T.turn(tuki, 472, 120)
for k, b in enumerate(ttow):
    land, fe = fall_end[k]
    p1 = Vector((0.0, 0.0, th - 0.04 + k * BS))
    f0 = 474 + k * 7
    K(b, 'location', f0, tuple(land))
    K(b, 'rotation_euler', f0, (0, 0, math.radians(15 * k)))
    for t in range(2, 11, 2):
        u = t / 10
        K(b, 'location', f0 + t, tuple(land.lerp(p1, u) + Vector((0, 0, 0.35 * 4 * u * (1 - u)))))
    K(b, 'rotation_euler', f0 + 10, (0, 0, 0))
T.turn(tuki, 504, 120)
T.turn(tuki, 512, 20)
TF2 = Vector((0.85, -1.55, Z0))
for k in range(6):
    u = k / 5
    f = 534 + k * 18
    K(tuki['hold'], 'location', f, tuple(TF.lerp(TF2, u)))
    if k < 5:
        K(tuki['hold'], 'location', f + 9, tuple(TF.lerp(TF2, u + 0.1) + Vector((0, 0, 0.05))))
T.place(tuki, 528, TF)
T.turn(tuki, 526, 20)
T.turn(tuki, 534, 75)
T.turn(tuki, 624, 75)
T.turn(tuki, 632, 0)

GS = Vector((-3.6, -1.0, Z0))
GF = Vector((-1.0, -1.35, Z0))
T.place(gruno, 632, GS)
K(gruno['hold'], 'location', 642, tuple(GS.lerp(GF, 0.85)))
K(gruno['hold'], 'location', 648, tuple(GF + Vector((0.12, 0, 0))))
K(gruno['hold'], 'location', 654, tuple(GF))
for f, sc3 in ((632, (1, 1, 1)), (636, (1.2, 0.9, 0.9)), (646, (1.15, 0.9, 0.95)), (650, (0.9, 1.1, 1.08)), (656, (1.05, 1, 0.97)), (662, (1, 1, 1))):
    S(gruno, f, sc3)
T.turn(gruno, 650, 80)
T.turn(gruno, 658, 10)
gesture(gruno, 'bounce', 672)
T.turn(tuki, 650, 0)
T.turn(tuki, 656, -45)
T.turn(ruki, 650, 0)
T.turn(ruki, 656, -40)
T.arm(tuki, 'L', 728, 0, None)
T.arm(tuki, 'L', 734, fwd=-30, out=90)
T.arm(tuki, 'L', 760, fwd=-30, out=90)
T.rest_arm(tuki, 'L', 768)
T.turn(gruno, 760, 10)
T.turn(gruno, 768, -20)
K(gb, 'rotation_euler', 760, (0, 0, 0))
K(gb, 'rotation_euler', 768, (0, math.radians(-12), 0))
K(gb, 'rotation_euler', 776, (0, math.radians(8), 0))
K(gb, 'rotation_euler', 784, (0, 0, 0))
tuki['hold'].location = TF2
gesture(tuki, 'hops', 790)
ruki['hold'].location = RB
gesture(ruki, 'bounce', 796)

T.lines(EID, LINES)
T.blinks(tuki, (60, 160, 280, 400, 520, 640, 780))
T.blinks(ruki, (150, 270, 380, 500, 620, 740))
T.blinks(gruno, (690, 800))
word3d('¡META!', (0.9, 0.15, 0.35), (0.5, -1.6, 2.6), 420, 500, size=0.5, max_w=1.3)
