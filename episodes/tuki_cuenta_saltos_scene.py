from stage import *
from episodes.tuki_cuenta_saltos_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress
EID = 'tuki_cuenta_saltos'
Z0 = 0.08
auto_dress(EID, ENV)
TP = Vector((-0.72, -0.95, Z0 + 0.05))
RP = Vector((0.8, -0.8, Z0))
ST = Vector((0.06, -1.3, Z0))
ROW_Y = -2.12
SLOTS = [Vector((-0.88 + 0.4 * i, ROW_Y, Z0)) for i in range(5)]
COLS = [(1.0, 0.42, 0.42), (0.3, 0.62, 1.0), (1.0, 0.78, 0.15), (0.3, 0.85, 0.5), (0.7, 0.45, 0.95)]
TH = 0.13
DK = [tuple(v * 0.62 for v in c) for c in COLS]

W0 = ((0, -7.2, 1.55), (0, -1.15, 0.95), 36)
W1 = ((0.04, -7.3, 2.35), (0.04, -1.45, 0.72), 36)
W2 = ((0.04, -7.0, 2.25), (0.04, -1.45, 0.75), 36)
camkey(0, W0)
camkey(150, W0)
camkey(182, W1)
camkey(530, W1)
camkey(560, ((-0.05, -7.7, 1.95), (-0.05, -1.2, 1.0), 36))
camkey(612, ((-0.05, -7.7, 1.95), (-0.05, -1.2, 1.0), 36))
camkey(640, W2)
camkey(TOTAL - 1, ((0.04, -6.9, 2.2), (0.04, -1.45, 0.75), 36))

spawn('play_mat', 0, 41, (0.55, 0.85, 0.95), (TP.x, TP.y, Z0), 1.0, 0)
tok = [spawn('soft_token', 0, 100 + i, COLS[i], tuple(ST + Vector((0, 0, TH * i))) if i < 4 else (0, 0, -5), 1.0, 0) for i in range(5)]

tuki = make('tuki', 1.6)
ruki = make('ruki', 1.55)
T.place(tuki, 0, TP)
T.turn(tuki, 0, 15)
T.place(ruki, 0, RP)
T.turn(ruki, 0, -30)

for f, n in JUMPS0:
    hop_to(tuki, f, TP, TP, 12, apex=0.55)
OPEN_X = [-1.05, -0.55, -0.05, 0.45]
OPEN_Z = 2.55
for (f, n), x in zip(JUMPS0, (OPEN_X[0], OPEN_X[1], OPEN_X[3])):
    word3d(str(n), DK[n - 1], (x, -1.3, OPEN_Z), f + 4, 112, size=0.62, max_w=1.0)
word3d('?', (0.3, 0.3, 0.38), (OPEN_X[2], -1.3, OPEN_Z), 72, 112, size=0.62, max_w=1.0)
T.turn(tuki, 60, 15)
T.turn(tuki, 70, 35)
for k, f in enumerate(range(78, 104, 6)):
    T.turn(tuki, f, 35 + (10 if k % 2 else -10))
T.turn(tuki, 108, 20)

T.turn(ruki, 70, -30)
T.turn(ruki, 76, -15)
T.arm(ruki, 'R', 112, 0, None)
T.arm(ruki, 'L', 112, 0, None)
T.arm(ruki, 'L', 120, fwd=-40, out=60)
T.arm(ruki, 'L', 168, fwd=-40, out=60)
T.rest_arm(ruki, 'L', 176)
T.turn(ruki, 176, -40)


def fly(o, f0, a, b, dur=14, apex=0.55):
    K(o, 'location', f0 - 1, tuple(a))
    for t in range(0, dur + 1, 2):
        u = t / dur
        p = a.lerp(b, u)
        p.z += apex * 4 * u * (1 - u)
        K(o, 'location', f0 + t, tuple(p))
    K(o, 'location', f0 + dur, tuple(b))
    K(o, 'scale', f0 + dur, (1, 1, 1))
    K(o, 'scale', f0 + dur + 2, (1.18, 1.18, 0.75))
    K(o, 'scale', f0 + dur + 6, (0.95, 0.95, 1.08))
    K(o, 'scale', f0 + dur + 9, (1, 1, 1))


for i, (f, n) in enumerate(JUMPS):
    hop_to(tuki, f, TP, TP, 14, apex=0.6)
    src = ST + Vector((0, 0, TH * (3 - i)))
    o = tok[3 - i]
    K(o, 'scale', 0, (1, 1, 1))
    fly(o, f + 2, src, SLOTS[i])
    word3d(str(n), DK[3 - i], (SLOTS[i].x, ROW_Y - 0.08, 0.5), f + 14, None, size=0.36, max_w=0.6)
    T.turn(ruki, f - 2, -40)
    T.arm(ruki, 'L', f - 2, 0, None)
    T.arm(ruki, 'L', f + 3, fwd=-55, out=40)
    T.rest_arm(ruki, 'L', f + 18)
    C.blink(ruki, f + 20)
    T.turn(tuki, f + 16, 10)
    T.turn(tuki, f + 22, 20)

T.turn(ruki, 350, -40)
T.turn(ruki, 358, 0)
T.turn(tuki, 350, 20)
T.turn(tuki, 360, 5)
for i, f in enumerate(PULSE):
    o = tok[3 - i]
    K(o, 'scale', f - 1, (1, 1, 1))
    K(o, 'scale', f + 3, (1.3, 1.3, 1.3))
    K(o, 'scale', f + 7, (1, 1, 1))
    K(o, 'location', f - 1, tuple(SLOTS[i]))
    K(o, 'location', f + 3, tuple(SLOTS[i] + Vector((0, 0, 0.12))))
    K(o, 'location', f + 7, tuple(SLOTS[i]))
T.turn(ruki, 436, 0)
T.turn(ruki, 444, -30)
gesture(tuki, 'bounce', 444)
T.arm(ruki, 'R', 472, 0, None)
T.arm(ruki, 'R', 478, fwd=-35, out=80)
T.arm(ruki, 'L', 472, 0, None)
T.arm(ruki, 'L', 478, fwd=-35, out=80)
T.rest_arm(ruki, 'R', 526)
T.rest_arm(ruki, 'L', 526)

T.turn(tuki, 530, 20)
T.turn(tuki, 538, 0)
hop_to(tuki, BIG, TP, TP, 22, apex=1.1)
K(tuki['spin'], 'rotation_euler', BIG, (0, 0, 0))
K(tuki['spin'], 'rotation_euler', BIG + 22, (0, 0, math.radians(360)))
K(tuki['spin'], 'rotation_euler', BIG + 23, (0, 0, 0))
foot = TP + Vector((0.16, -0.12, 0.2))
o5 = tok[4]
K(o5, 'location', 0, (0, 0, -5))
K(o5, 'location', 566, tuple(foot + Vector((0, 0, 3.4))))
K(o5, 'scale', 0, (0, 0, 0))
K(o5, 'scale', 565, (0, 0, 0))
K(o5, 'scale', 568, (1, 1, 1))
for t in range(0, 17, 2):
    u = t / 16
    K(o5, 'location', 566 + t, tuple(foot + Vector((0, 0, 3.4 * (1 - u * u)))))
K(o5, 'rotation_euler', 566, (0, 0, 0))
K(o5, 'rotation_euler', 582, (math.radians(10), 0, 0))
K(o5, 'rotation_euler', 600, (0, 0, math.radians(360)))
fly(o5, 584, foot, SLOTS[4], dur=18, apex=0.5)
S(tuki, 582, (1, 1, 1))
S(tuki, 585, (1.06, 1.06, 0.94))
S(tuki, 590, (1, 1, 1))
word3d('5', DK[4], (SLOTS[4].x, ROW_Y - 0.08, 0.5), 602, None, size=0.36, max_w=0.6)
T.turn(tuki, 590, 0)
T.turn(tuki, 598, -25)
T.turn(ruki, 596, -30)
T.turn(ruki, 604, -10)
for i in range(5):
    f = 640 + i * 7
    o = tok[[3, 2, 1, 0, 4][i]]
    K(o, 'scale', f - 1, (1, 1, 1))
    K(o, 'scale', f + 3, (1.2, 1.2, 1.2))
    K(o, 'scale', f + 7, (1, 1, 1))
confetti(690, (0.0, -1.6, 2.6), n=26, spread=2.2)
T.turn(tuki, 696, 15)
gesture(tuki, 'hops', 702)
gesture(ruki, 'sway', 702)
C.wave(ruki, 'R', 740, cycles=2, period=8)

T.lines(EID, LINES)
T.blinks(tuki, (60, 150, 250, 380, 470, 560, 650, 740))
T.blinks(ruki, (40, 140, 300, 400, 520, 620, 720))
