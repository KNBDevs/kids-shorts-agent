from stage import *
from episodes.vaca_cuidado_plan import *
import ep_tools as T
import random
from props.lib import spawn, auto_dress, M, MA
EID = 'vaca_cuidado'
Z0 = 0.08
auto_dress(EID, ENV)
BEAT = 60 / 124 * FPS

W0 = ((0.0, -6.4, 2.05), (0.0, -1.75, 0.72), 33)
WC = ((0.25, -5.0, 1.75), (0.2, -2.1, 0.55), 32)
WG = ((-0.25, -5.1, 1.75), (-0.25, -1.6, 0.72), 31)
camkey(0, W0)
camkey(150, W0)
camkey(162, WC)
camkey(276, WC)
camkey(288, WG)
camkey(420, WG)
camkey(432, W0)
camkey(TOTAL - 1, W0)

WT_ = Vector((0.36, -2.4, Z0))
HY_ = Vector((0.88, -1.84, Z0))
wat = spawn('farm_trough', 1, 21, 'fresh', tuple(WT_), 0.95, 0, kind='water')
hay = spawn('farm_trough', 0, 22, 'autumn', tuple(HY_), 0.95, 90, kind='hay')
wfill = next(o for o in wat.children if o.name.startswith('fill'))

cow = spawn('cow', 1, 77, 'pastel', (0, 0, 0), 1.12, 0)
head = next(o for o in cow.children if o.name.startswith('head'))
tail = next(o for o in cow.children if o.name.startswith('tail'))
legs = [o for o in cow.children if o.name.startswith('leg')]

C0 = Vector((0.3, -1.72, Z0))
C1 = Vector((-0.06, -1.86, Z0))
C2 = Vector((0.1, -1.8, Z0))


def walk(f0, f1, a, b, r0, r1):
    n = f1 - f0
    for k in range(0, n + 1, 2):
        u = k / n
        u2 = u * u * (3 - 2 * u)
        K(cow, 'location', f0 + k, tuple(a.lerp(b, u2)))
        K(cow, 'rotation_euler', f0 + k, (0, 0, math.radians(r0 + (r1 - r0) * u2)))
    for k in range(0, n + 1, 4):
        for i, lg in enumerate(legs):
            ph = 1 if i in (0, 3) else -1
            a_ = 0 if k in (0, n - n % 4) else ph * (18 if (k // 4) % 2 else -18)
            K(lg, 'rotation_euler', f0 + k, (0, math.radians(a_), 0))
    for lg in legs:
        K(lg, 'rotation_euler', f1, (0, 0, 0))


def munch(f0, f1, low, per=16):
    K(head, 'rotation_euler', f0, (0, 0, 0))
    K(head, 'rotation_euler', f0 + 8, (0, math.radians(low), 0))
    f = f0 + 8
    s = 1
    while f + per // 2 < f1 - 8:
        f += per // 2
        K(head, 'rotation_euler', f, (0, math.radians(low - (8 if s > 0 else 0)), 0))
        s = -s
    K(head, 'rotation_euler', f1, (0, 0, 0))


def swish(f0, f1, per=20):
    f = f0
    s = 1
    while f < f1:
        K(tail, 'rotation_euler', f, (math.radians(18 * s), 0, 0))
        s = -s
        f += per // 2
    K(tail, 'rotation_euler', f1, (0, 0, 0))


K(cow, 'location', 0, tuple(C0))
K(cow, 'rotation_euler', 0, (0, 0, math.radians(195)))
K(head, 'rotation_euler', 0, (0, 0, 0))
K(head, 'rotation_euler', 30, (0, 0, math.radians(-12)))
K(head, 'rotation_euler', 56, (0, 0, math.radians(8)))
K(head, 'rotation_euler', 72, (0, 0, 0))
walk(76, 116, C0, C1, 195, 310)
munch(120, 330, 48, 18)
K(head, 'rotation_euler', 336, (0, math.radians(-6), 0))
K(head, 'rotation_euler', 346, (0, 0, 0))
walk(350, 392, C1, C2, 310, 356)
munch(396, 930, 44, 20)
swish(130, 330)
swish(420, 940, 24)

notes_m = C.mat('notes', (0.25, 0.4, 0.95), rough=0.3, emit=0.6)
rr = random.Random(9)
SONG0, SONG1 = SONG
for j in range(9):
    n = C.empty('note', None, (0, 0, 0))
    C.sphere('h', (0, 0, 0), (0.07, 0.028, 0.056), notes_m, n, 12)
    C.tube('s', [(0.064, 0, 0.0), (0.064, 0, 0.22)], 0.014, notes_m, n)
    C.tube('fl', [(0.064, 0, 0.22), (0.13, 0, 0.16)], 0.014, notes_m, n)
    f0 = SONG0 + j * 30
    p0 = Vector((rr.uniform(-1.2, -0.3), -1.5, rr.uniform(1.75, 2.15)))
    K(n, 'scale', 0, (0, 0, 0))
    K(n, 'scale', f0, (0, 0, 0))
    K(n, 'scale', f0 + 6, (1.15, 1.15, 1.15))
    K(n, 'location', f0, tuple(p0))
    K(n, 'location', f0 + 30, tuple(p0 + Vector((rr.uniform(-0.2, 0.2), 0, 0.32))))
    K(n, 'scale', f0 + 24, (1.15, 1.15, 1.15))
    K(n, 'scale', f0 + 30, (0, 0, 0))

jug_m = M((0.55, 0.78, 0.98), rough=0.3, coat=0.7)
jug = C.empty('jug', None, (0, 0, 0))
C.lathe('jb', [(0, 0.0), (0, 0.1), (0.02, 0.11), (0.16, 0.12), (0.24, 0.08), (0.27, 0.09), (0.27, 0.0)], jug_m, jug, segs=40)
C.tube('jh', [(-0.1, 0, 0.21), (-0.16, 0, 0.17), (-0.16, 0, 0.08), (-0.1, 0, 0.05)], 0.016, jug_m, jug)
C.tube('jl', [(0.08, 0, 0.25), (0.15, 0, 0.29)], 0.022, jug_m, jug)
stream = C.empty('stream', jug, (0.15, 0, 0.29))
C.tube('st', [(0, 0, 0), (0.06, 0, -0.08), (0.08, 0, -0.3)], 0.014, MA((0.4, 0.7, 1.0), 0.7, emit=0.2), stream)
K(stream, 'scale', 0, (0, 0, 0))
J0 = Vector((-0.05, -2.62, 0.8))
T.pop_in(jug, 452, 1.0, 8)
K(jug, 'location', 452, tuple(J0))
K(jug, 'location', 470, (0.12, -2.5, 0.5))
K(jug, 'rotation_euler', 470, (0, 0, 0))
K(jug, 'rotation_euler', 482, (0, math.radians(55), 0))
K(stream, 'scale', 481, (0, 0, 0))
K(stream, 'scale', 486, (1, 1, 1))
K(stream, 'scale', 528, (1, 1, 1))
K(stream, 'scale', 533, (0, 0, 0))
K(jug, 'rotation_euler', 534, (0, math.radians(55), 0))
K(jug, 'rotation_euler', 546, (0, 0, 0))
K(jug, 'location', 546, (0.12, -2.5, 0.5))
T.pop_out(jug, 560, 1.0, 6)
K(wfill, 'location', 484, tuple(wfill.location))
K(wfill, 'location', 530, tuple(wfill.location + Vector((0, 0, 0.03))))
K(wfill, 'scale', 484, (0.85, 0.85, 1))
K(wfill, 'scale', 530, (1, 1, 1))

gruno = make('gruno', 1.55)
G0 = Vector((-1.1, -1.35, Z0))
G1 = Vector((-0.55, -2.6, Z0))
G2 = Vector((-1.0, -1.05, Z0))
T.place(gruno, 0, G0)
T.turn(gruno, 0, -40)
for f in (18, 38, 114, 128, 142):
    T.arm(gruno, 'L', f, fwd=-55, out=110)
    T.arm(gruno, 'L', f + 6, fwd=-35, out=120)
T.arm(gruno, 'L', 160, fwd=-35, out=120)
T.rest_arm(gruno, 'L', 176)
for f in (20, 40, 116, 130, 144):
    S(gruno, f, (1, 1, 1))
    S(gruno, f + 3, (1.04, 1.04, 0.95))
    S(gruno, f + 7, (1, 1, 1))
T.turn(gruno, 200, -60)
gesture(gruno, 'breathe', 296)
T.turn(gruno, 360, -55)
hop_to(gruno, 436, G0, G1, 16, 0.3)
T.turn(gruno, 452, -75)
T.arm(gruno, 'R', 452, 0, None)
T.arm(gruno, 'R', 466, fwd=-60, out=20)
T.arm(gruno, 'R', 548, fwd=-60, out=20)
T.rest_arm(gruno, 'R', 558)
hop_to(gruno, 566, G1, G2, 18, 0.3)
T.turn(gruno, 584, -35)
f = 590
k = 0
while f < SONG1 - 4:
    T.turn(gruno, int(f), -35 + (10 if k % 2 else -10))
    k += 1
    f += BEAT * 2
T.turn(gruno, SONG1 + 4, -40)
hop_to(gruno, 740, G2, G2 + Vector((-0.2, 0.25, 0)), 12, 0.2)
T.place(gruno, 790, G2 + Vector((-0.2, 0.25, 0)))
K(gruno['spin'], 'rotation_euler', 800, (0, 0, math.radians(-30)))
K(gruno['spin'], 'rotation_euler', 812, (math.radians(-22), 0, math.radians(-30)))
K(gruno['spin'], 'rotation_euler', 832, (math.radians(-22), 0, math.radians(-30)))
K(gruno['spin'], 'rotation_euler', 846, (0, 0, math.radians(-30)))
gesture(gruno, 'bounce', 900)

T.lines(EID, LINES)
T.blinks(gruno, (70, 190, 320, 470, 620, 760, 880))
