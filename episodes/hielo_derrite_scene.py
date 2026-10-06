from stage import *
from episodes.hielo_derrite_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA
EID = 'hielo_derrite'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0.0, -6.5, 2.05), (0.0, -1.4, 0.8), 31)
WT = ((-0.05, -5.2, 1.8), (-0.05, -1.7, 1.0), 28)
WS = ((0.0, -3.05, 1.7), (0.0, -2.0, 0.76), 28)
camkey(0, WT)
camkey(56, WT)
camkey(64, WS)
camkey(94, WS)
camkey(104, WT)
camkey(326, WT)
camkey(336, WS)
camkey(540, WS)
camkey(552, WT)
camkey(730, WT)
camkey(744, W0)
camkey(TOTAL - 1, W0)

spawn('low_table', 0, 318, 'pastel', (0.0, -2.0, Z0), 1.0, 0)
TOP = Z0 + 0.62
ice = MA((0.3, 0.68, 1.0), 0.85, rough=0.15, emit=0.3)
edge = M((0.85, 0.97, 1.0), rough=0.2, coat=0.8, emit=0.6)
hi = M((1, 1, 1), rough=0.2, emit=1.2)
wat = MA((0.3, 0.6, 1.0), 0.85, rough=0.3, emit=0.15)


def plate(x, col, seed):
    return spawn('snack_plate', 0, seed, col, (x, -2.0, TOP), 0.8, 0)


def cube(P):
    o = C.empty('cube', None, tuple(P))
    C.rounded_box('ice', (0, 0, 0.07), (0.14, 0.14, 0.14), 0.03, ice, o)
    C.sphere('shine', (-0.035, -0.072, 0.11), (0.014, 0.004, 0.03), hi, o, 10)
    C.tube('rim', [(-0.06, -0.071, 0.135), (0.06, -0.071, 0.135), (0.071, 0.06, 0.135)], 0.006, edge, o)
    return o


def puddle(P):
    o = C.empty('pud', None, tuple(P + Vector((0, 0, 0.002))))
    C.sphere('pw', (0, 0, 0), (0.15, 0.12, 0.012), wat, o, 32)
    o.scale = (0.001, 0.001, 1)
    return o


def melt(c, p, f0, f1, steps=6):
    for k in range(steps + 1):
        u = k / steps
        f = round(f0 + (f1 - f0) * u)
        s = 1 - u
        K(c, 'scale', f, (max(0.001, s ** 0.6), max(0.001, s ** 0.6), max(0.001, s)))
        K(p, 'scale', f, (max(0.001, 0.25 + 0.75 * u), max(0.001, 0.25 + 0.75 * u), 1))
    K(p, 'scale', f0 - 1, (0.001, 0.001, 1))


P1 = Vector((-0.25, -2.0, TOP + 0.03))
P2 = Vector((0.25, -2.0, TOP + 0.03))
plate(-0.25, (0.55, 0.78, 0.98), 4411)
c1 = cube(P1)
d1 = puddle(P1)
K(c1, 'scale', 0, (1, 1, 1))
K(c1, 'scale', 62, (1, 1, 1))
melt(c1, d1, 64, 90)

pl2 = plate(0.25, (0.98, 0.72, 0.55), 4412)
c2 = cube(P2)
d2 = puddle(P2)
for o in (pl2, c2):
    T.pop_in(o, 232, 0.8 if o is pl2 else 1.0, 8)
K(c2, 'location', 330, tuple(P2))
for f in (340, 356):
    K(c2, 'location', f, tuple(P2 + Vector((0, 0, 0.06))))
    K(c2, 'location', f + 6, tuple(P2))
K(c2, 'scale', 398, (1, 1, 1))
melt(c2, d2, 400, 480, 10)
ring = C.empty('ripple', None, tuple(P2 + Vector((0, 0, 0.018))))
C.tube('rp', [(math.cos(k * 6.2832 / 40) * 0.08, math.sin(k * 6.2832 / 40) * 0.065, 0) for k in range(41)], 0.004, M((1, 1, 1), rough=0.2, emit=0.8), ring)
K(ring, 'scale', 0, (0, 0, 0))
for f in (492, 512):
    K(ring, 'scale', f - 1, (0, 0, 0))
    K(ring, 'scale', f, (0.3, 0.3, 1))
    K(ring, 'scale', f + 14, (1.5, 1.5, 1))
    K(ring, 'scale', f + 15, (0, 0, 0))

clock = spawn('time_clock', 0, 977, 'fresh', (0.0, -1.78, TOP), 1.0, 0)
hm = next(o for o in clock.children if o.name.startswith('hand_m'))
hh = next(o for o in clock.children if o.name.startswith('hand_h'))
K(hm, 'rotation_euler', 0, (0, 0, 0))
K(hh, 'rotation_euler', 0, (0, math.radians(90), 0))
for (f0, f1, turns) in ((62, 92, 3), (398, 482, 6)):
    K(hm, 'rotation_euler', f0, tuple(hm.rotation_euler))
    K(hh, 'rotation_euler', f0, tuple(hh.rotation_euler))
    K(hm, 'rotation_euler', f1, (0, hm.rotation_euler[1] + turns * 6.2832, 0))
    K(hh, 'rotation_euler', f1, (0, hh.rotation_euler[1] + turns * 6.2832 / 12, 0))
glow = C.empty('glow', None, (0.0, -1.86, TOP + 0.2))
C.tube('gl', [(math.cos(k * 6.2832 / 48) * 0.21, 0, math.sin(k * 6.2832 / 48) * 0.21) for k in range(49)], 0.01, M((1, 0.9, 0.5), rough=0.3, emit=2.0), glow)
K(glow, 'scale', 0, (0, 0, 0))
for f0, f1 in ((62, 92), (398, 482)):
    K(glow, 'scale', f0 - 1, (0, 0, 0))
    K(glow, 'scale', f0 + 4, (1, 1, 1))
    K(glow, 'scale', f1 - 4, (1, 1, 1))
    K(glow, 'scale', f1, (0, 0, 0))

shoes = spawn('tiny_shoes', 1, 52, 'candy', (0, 0, 0), 2.1, 0)
SH0 = Vector((-0.62, -1.95, TOP + 0.35))
SH1 = Vector((-0.52, -2.17, TOP))
T.pop_in(shoes, 14, 2.1, 8)
K(shoes, 'location', 14, tuple(SH0))
K(shoes, 'location', 38, tuple(SH0))
for t in range(0, 15, 3):
    u = t / 14
    p = SH0.lerp(SH1, u)
    p.z += 0.12 * 4 * u * (1 - u)
    K(shoes, 'location', 38 + t, tuple(p))
K(shoes, 'location', 52, tuple(SH1))
K(shoes, 'rotation_euler', 52, (0, 0, math.radians(10)))
K(shoes, 'location', 636, tuple(SH1))
K(shoes, 'location', 652, tuple(SH0))
K(shoes, 'rotation_euler', 652, (0, 0, math.radians(-10)))
K(shoes, 'location', 690, tuple(SH0))
K(shoes, 'location', 702, (-0.9, -1.85, TOP + 0.15))
K(shoes, 'scale', 696, (2.1, 2.1, 2.1))
K(shoes, 'scale', 704, (0, 0, 0))

tuki = make('tuki', 1.45)
luma = make('luma', 1.45)
TK0 = Vector((-0.95, -1.6, Z0))
TK_OFF = Vector((-2.6, -1.1, Z0))
T.place(tuki, 0, TK0)
T.turn(tuki, 0, 35)
T.arm(tuki, 'R', 0, 0, None)
T.arm(tuki, 'R', 8, fwd=-80, out=20)
T.arm(tuki, 'R', 40, fwd=-80, out=20)
T.arm(tuki, 'R', 50, fwd=-50, out=10)
T.rest_arm(tuki, 'R', 58)
hop_to(tuki, 60, TK0, TK_OFF, 14, 0.4)
T.turn(tuki, 60, -60)
T.place(tuki, 78, TK_OFF)
T.turn(tuki, 78, 60)
hop_to(tuki, 80, TK_OFF, TK0, 14, 0.4)
T.turn(tuki, 98, 35)
for k, f in enumerate(range(104, 150, 10)):
    T.turn(tuki, f, 10 if k % 2 else 60)
T.turn(tuki, 156, 35)
S(tuki, 120, (1, 1, 1))
S(tuki, 126, (1.08, 1.08, 0.9))
S(tuki, 134, (1, 1, 1))

LU0 = Vector((0.95, -1.72, Z0))
LU_OFF = Vector((2.6, -1.2, Z0))
T.place(luma, 0, LU_OFF)
T.place(luma, 158, LU_OFF)
hop_to(luma, 160, LU_OFF, LU0, 18, 0.45)
T.turn(luma, 0, -40)
T.turn(luma, 180, -35)
T.arm(luma, 'L', 220, 0, None)
T.arm(luma, 'L', 228, fwd=-70, out=20)
T.arm(luma, 'L', 244, fwd=-70, out=20)
T.rest_arm(luma, 'L', 254)
T.turn(tuki, 250, 50)
T.place(tuki, 250, TK0)
T.place(tuki, 266, TK0 + Vector((0.12, -0.05, 0)))
T.place(tuki, 380, TK0 + Vector((0.12, -0.05, 0)))
T.place(tuki, 392, TK0)
T.arm(luma, 'R', 330, 0, None)
T.arm(luma, 'R', 336, fwd=-60, out=15)
T.arm(luma, 'R', 380, fwd=-60, out=15)
T.rest_arm(luma, 'R', 390)
gesture(luma, 'breathe', 410)
T.turn(luma, 490, -50)
T.turn(luma, 540, -35)
T.place(tuki, 566, TK0)
gesture(tuki, 'hops', 570)
T.turn(tuki, 610, 35)
T.arm(tuki, 'R', 632, 0, None)
T.arm(tuki, 'R', 640, fwd=-80, out=20)
T.arm(tuki, 'R', 690, fwd=-80, out=20)
T.rest_arm(tuki, 'R', 704)
T.turn(tuki, 700, 15)
T.turn(luma, 700, -20)
T.place(tuki, 735, TK0)
T.place(luma, 735, LU0)
gesture(tuki, 'bounce', 738)
gesture(luma, 'bounce', 742)
C.wave(luma, 'R', 772, cycles=2, period=8)

T.lines(EID, LINES)
T.blinks(tuki, (50, 170, 300, 440, 600, 720))
T.blinks(luma, (200, 320, 460, 590, 760))
