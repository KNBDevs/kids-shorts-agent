from stage import *
from episodes.donde_esta_tres_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M
EID = 'donde_esta_tres'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0.0, -6.5, 1.9), (0.0, -1.4, 0.75), 34)
WG = ((0.1, -6.6, 1.9), (0.1, -1.4, 0.7), 38)
WB = ((-0.4, -6.6, 1.9), (-0.45, -1.1, 0.7), 37)
WF = ((0.35, -7.7, 2.05), (0.35, -1.3, 0.8), 31)
camkey(0, W0)
camkey(70, W0)
camkey(84, WG)
camkey(250, WG)
camkey(270, WB)
camkey(400, WB)
camkey(424, W0)
camkey(520, W0)
camkey(540, WF)
camkey(TOTAL - 1, WF)

COLS = [(0.92, 0.25, 0.3), (0.98, 0.55, 0.08), (0.15, 0.5, 0.92), (0.3, 0.68, 0.2)]
XS = [-0.85, -0.33, 0.19, 0.71]
RY = -2.2
SC = 1.0
tiles = []
for i in range(4):
    loc = (XS[i], RY, Z0)
    t = spawn('number_stand', 0, 40 + i, COLS[i], loc, SC, 0, label=str(i + 1))
    tiles.append(t)
T3 = tiles[2]

bush = spawn('bush', 2, 77, 'fresh', (-1.15, -0.55, Z0), 1.6, 10)
HID = Vector((-1.0, -0.25, Z0 + 0.36))
T3.location = tuple(HID)
T3.rotation_euler = (0, math.radians(-100), math.radians(25))
K(T3, 'location', 0, tuple(HID))
K(T3, 'rotation_euler', 0, (0, math.radians(-100), math.radians(25)))
for k, f in enumerate(range(196, 246, 6)):
    K(T3, 'location', f, tuple(HID + Vector((0.02 * (1 if k % 2 else -1), 0, 0.13 * (k % 2)))))
    K(bush, 'rotation_euler', f, (0, math.radians(3 if k % 2 else -3), math.radians(10)))
K(T3, 'location', 250, tuple(HID))
K(bush, 'rotation_euler', 250, (0, 0, math.radians(10)))

glow = C.mat('gapglow', (1.0, 0.85, 0.35), rough=0.3, emit=2.0)
gap = C.empty('gap', None, (XS[2], RY, Z0 + 0.01))
pts = []
for k in range(40):
    a = k * 6.2832 / 40
    pts.append((0.3 * math.cos(a) / max(abs(math.cos(a)), abs(math.sin(a))) ** 0.25 * 0.8, 0.18 * math.sin(a) / max(abs(math.cos(a)), abs(math.sin(a))) ** 0.25 * 0.8, 0))
for k in range(0, 40, 2):
    C.tube('dash', [pts[k], pts[(k + 1) % 40]], 0.018, glow, gap)
T.pop_in(gap, 96, 1.0, 8)
for k, f in enumerate(range(110, 420, 12)):
    K(gap, 'scale', f, (1.08,) * 3 if k % 2 else (1.0,) * 3)
T.pop_out(gap, 420, 1.0, 6)


def bounce(o, f, base, h=0.18):
    K(o, 'location', f, tuple(base))
    K(o, 'location', f + 4, tuple(base + Vector((0, 0, h))))
    K(o, 'location', f + 8, tuple(base))
    K(o, 'scale', f + 8, (SC * 1.12, SC * 1.12, SC * 0.86))
    K(o, 'scale', f + 12, (SC,) * 3)
    K(o, 'scale', f - 1, (SC,) * 3)


B = [Vector((x, RY, Z0)) for x in XS]
bounce(tiles[0], 14, B[0])
bounce(tiles[1], 34, B[1])

pimo = make('pimo', 1.45)
gruno = make('gruno', 1.6)
P0 = Vector((-0.6, -1.15, Z0))
P1 = Vector((0.19, -1.2, Z0))
P2 = Vector((-0.55, -0.85, Z0))
T.place(pimo, 0, P0)
T.turn(pimo, 0, 0)
T.arm(pimo, 'R', 8, 0, None)
T.arm(pimo, 'R', 14, fwd=-60, out=20)
T.turn(pimo, 12, -20)
T.turn(pimo, 30, 5)
T.arm(pimo, 'R', 40, fwd=-60, out=20)
T.rest_arm(pimo, 'R', 48)
T.turn(pimo, 46, -35)
T.turn(pimo, 54, 35)
T.turn(pimo, 62, 0)
hop_to(pimo, 70, P0, P1, 16, apex=0.45)
T.turn(pimo, 86, 0)
T.turn(pimo, 92, 10)
T.arm(pimo, 'L', 90, 0, None)
T.arm(pimo, 'L', 96, fwd=-55, out=10)
T.arm(pimo, 'L', 126, fwd=-55, out=10)
T.rest_arm(pimo, 'L', 134)
T.turn(pimo, 150, 0)
for side in ('L', 'R'):
    T.arm(pimo, side, 160, 0, None)
    T.arm(pimo, side, 166, fwd=-20, out=70)
    T.arm(pimo, side, 200, fwd=-20, out=70)
    T.rest_arm(pimo, side, 208)
T.turn(pimo, 168, -25)
T.turn(pimo, 180, 25)
T.turn(pimo, 194, 0)
S(pimo, 214, (1, 1, 1))
S(pimo, 220, (1.04, 1.04, 0.96))
S(pimo, 228, (1, 1, 1))
T.turn(pimo, 252, 0)
T.turn(pimo, 260, -55)
T.arm(pimo, 'R', 256, 0, None)
T.arm(pimo, 'R', 262, fwd=-80, out=30)
T.arm(pimo, 'R', 286, fwd=-80, out=30)
T.rest_arm(pimo, 'R', 292)
pimo['hold'].location = P1
hop_to(pimo, 290, P1, P2, 18, apex=0.45)
T.turn(pimo, 296, -70)
T.turn(pimo, 310, -40)

UP = HID + Vector((0.05, -0.15, 0.45))
CARRY = P2 + Vector((0.5, -0.35, 0.55))
K(T3, 'location', 312, tuple(HID))
K(T3, 'location', 318, tuple(UP))
K(T3, 'location', 330, tuple(CARRY))
K(T3, 'rotation_euler', 330, (0, math.radians(-100), math.radians(25)))
K(T3, 'rotation_euler', 366, (0, math.radians(-100), math.radians(25)))
K(T3, 'rotation_euler', 380, (0, math.radians(8), 0))
K(T3, 'rotation_euler', 386, (0, 0, 0))
K(T3, 'location', 392, tuple(CARRY))
for side in ('L', 'R'):
    T.arm(pimo, side, 316, 0, None)
    T.arm(pimo, side, 324, fwd=-65, out=15)
    T.arm(pimo, side, 412, fwd=-65, out=15)
    T.rest_arm(pimo, side, 426)
T.turn(pimo, 340, -15)
T.turn(pimo, 392, -15)
T.turn(pimo, 396, 30)
pimo['hold'].location = P2
hop_to(pimo, 396, P2, P1, 18, apex=0.35)
for f in range(396, 416, 2):
    u = (f - 396) / 18
    p = CARRY.lerp(P1 + Vector((0.5, -0.35, 0.55)), u)
    p.z += 0.35 * 4 * u * (1 - u)
    K(T3, 'location', f, tuple(p))
K(T3, 'location', 414, tuple(P1 + Vector((0.5, -0.35, 0.55))))
K(T3, 'location', 420, tuple(B[2] + Vector((0, 0, 0.12))))
K(T3, 'location', 424, tuple(B[2]))
K(T3, 'scale', 423, (SC,) * 3)
K(T3, 'scale', 425, (SC * 1.15, SC * 1.15, SC * 0.85))
K(T3, 'scale', 430, (SC,) * 3)
T.turn(pimo, 416, 0)
T.turn(pimo, 426, 0)
for k in range(8):
    o = C.sphere('spk', tuple(B[2] + Vector((0, -0.1, 0.4))), (1, 1, 1), glow, None, 10)
    a = k * 0.785
    K(o, 'scale', 0, (0, 0, 0))
    K(o, 'scale', 423, (0, 0, 0))
    K(o, 'scale', 424, (0.035,) * 3)
    K(o, 'location', 424, tuple(B[2] + Vector((0, -0.1, 0.4))))
    K(o, 'location', 436, tuple(B[2] + Vector((math.cos(a) * 0.55, -0.15, 0.4 + math.sin(a) * 0.45))))
    K(o, 'scale', 434, (0.03,) * 3)
    K(o, 'scale', 438, (0, 0, 0))

for i, f in enumerate((432, 446, 460, 474)):
    bounce(tiles[i], f, B[i], 0.22)
T.arm(pimo, 'R', 430, 0, None)
for i, f in enumerate((432, 446, 460, 474)):
    T.turn(pimo, f, -40 + 25 * i)
    T.arm(pimo, 'R', f, fwd=-50, out=25)
    T.arm(pimo, 'R', f + 7, fwd=-35, out=25)
T.rest_arm(pimo, 'R', 492)
T.turn(pimo, 492, 0)
gesture(pimo, 'bounce', 494)

GS = Vector((2.9, -1.3, Z0))
GF = Vector((0.0, -2.85, Z0))
GE = Vector((1.2, -1.5, Z0))
T.place(gruno, 0, GS)
T.turn(gruno, 0, -90)
T.place(gruno, 516, GS)
hop_to(gruno, 518, GS, GF, 20, apex=0.6)
T.turn(gruno, 538, -90)
T.turn(gruno, 544, 0)
for side in ('L', 'R'):
    T.arm(gruno, side, 544, 0, None)
    T.arm(gruno, side, 550, fwd=-30, out=75)
    T.arm(gruno, side, 580, fwd=-30, out=75)
    T.rest_arm(gruno, side, 590)
T.turn(pimo, 540, 0)
T.turn(pimo, 548, 20)
S(pimo, 552, (1.06, 1.06, 0.92))
S(pimo, 560, (1, 1, 1))
T.arm(pimo, 'R', 614, 0, None)
T.arm(pimo, 'R', 620, fwd=-80, out=40)
T.arm(pimo, 'R', 650, fwd=-80, out=40)
T.rest_arm(pimo, 'R', 658)
T.turn(pimo, 616, 45)
T.turn(gruno, 630, 0)
T.turn(gruno, 640, 60)
gruno['hold'].location = GF
hop_to(gruno, 650, GF, GE, 20, apex=0.5)
T.turn(gruno, 670, 60)
T.turn(gruno, 678, -15)
T.turn(pimo, 676, 0)
S(gruno, 698, (1, 1, 1))
S(gruno, 706, (1.12, 1.12, 1.12))
S(gruno, 760, (1.12, 1.12, 1.12))
S(gruno, 768, (1, 1, 1))
for side in ('L', 'R'):
    T.arm(gruno, side, 700, 0, None)
    T.arm(gruno, side, 708, fwd=10, out=-20)
    T.arm(gruno, side, 770, fwd=10, out=-20)
    T.rest_arm(gruno, side, 780)
T.turn(pimo, 730, 30)
for k, f in enumerate(range(740, 790, 8)):
    S(pimo, f, (1.04, 1.04, 0.95) if k % 2 else (1, 1, 1))
T.turn(pimo, 792, 0)
C.wave(pimo, 'L', 786, cycles=2, period=8)
for i, f in enumerate((776, 782, 788, 794)):
    bounce(tiles[i], f, B[i], 0.12)

T.lines(EID, LINES)
T.blinks(pimo, (60, 150, 240, 330, 450, 560, 680, 770))
T.blinks(gruno, (560, 640, 720, 790))
word3d('?', (0.95, 0.45, 0.2), (0.55, -1.6, 2.2), 164, 250, size=0.7, max_w=0.6)
word3d('1  2  3  4', (0.25, 0.45, 0.95), (-0.05, -2.1, 2.3), 432, 520, size=0.5, max_w=2.2)
