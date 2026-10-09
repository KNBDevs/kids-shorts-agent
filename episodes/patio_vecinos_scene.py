from stage import *
from episodes.patio_vecinos_plan import *
import ep_tools as T
import random
from props import lib
from props.lib import spawn, auto_dress, M, MA
EID = 'patio_vecinos'
Z0 = 0.08
auto_dress(EID, ENV)
BEAT = 60 / 124 * FPS

W0 = ((0.0, -6.4, 2.2), (0.0, -1.4, 0.75), 31)
WP = ((0.25, -4.7, 1.75), (0.25, -1.45, 0.7), 31)
WM = ((-0.45, -5.3, 2.0), (-0.45, -1.4, 0.6), 31)
camkey(0, W0)
camkey(110, W0)
camkey(122, WP)
camkey(280, WP)
camkey(292, W0)
camkey(720, W0)
camkey(732, WM)
camkey(840, WM)
camkey(852, WP)
camkey(TOTAL - 1, WP)

POT = Vector((0.42, -1.75, Z0))
pr = C.empty('pot', None, tuple(POT))
pr.scale = (1.35, 1.35, 1.35)
pot = lib.cutaway_pot(random.Random(61), 1, 'fresh', pr)
pot['cut'].scale = (0, 0, 0)
plant = pot['plant']
lfs = [o for o in plant.children if o.name.startswith('lf')]

sign = spawn('care_sign', 2, 62, 'candy', (0.95, -1.6, Z0), 1.0, -15)
T.pop_in(sign, 300, 1.0, 8)

MAT = Vector((-0.72, -1.95, Z0))
mat = spawn('play_mat', 0, 63, 'candy', tuple(MAT), 1.35, 0)
T.pop_in(mat, 300, 1.35, 10)

ball = spawn('play_ball', 0, 64, 'candy', (0, 0, 0), 1.5, 0)
B0 = Vector((-0.05, -1.95, Z0))
B1 = Vector((0.0, -1.98, Z0 + 0.45))
K(ball, 'location', 0, tuple(B0))
K(ball, 'location', 96, tuple(B0))
K(ball, 'location', 112, tuple(B1))
K(ball, 'location', 200, tuple(B1))
K(ball, 'location', 214, tuple(B0))
K(ball, 'location', 330, tuple(B0))
BM = MAT + Vector((0.0, -0.25, 0))
for k in range(0, 21, 2):
    u = k / 20
    p = B0.lerp(BM, u)
    p.z += 0.25 * 4 * u * (1 - u)
    K(ball, 'location', 330 + k, tuple(p))
f = 410
side = 1
while f < 690:
    a = BM + Vector((0.32 * side, 0.08, 0))
    b = BM + Vector((-0.32 * side, 0.08, 0))
    K(ball, 'location', int(f), tuple(a))
    K(ball, 'location', int(f + BEAT * 2), tuple(b))
    K(ball, 'rotation_euler', int(f), (0, 0, 0))
    K(ball, 'rotation_euler', int(f + BEAT * 2), (0, math.radians(-side * 200), 0))
    side = -side
    f += BEAT * 2
K(ball, 'location', 760, tuple(BM + Vector((0.0, 0.1, 0))))
K(ball, 'location', 800, tuple(MAT + Vector((0.0, 0.35, 0))))

shoe_m = M((0.98, 0.6, 0.5), rough=0.45, coat=0.5)
sole_m = M((0.97, 0.95, 0.9), rough=0.55, coat=0.2)
shoes = []
for k, x in enumerate((-0.32, 0.32)):
    o = C.empty('shoe', None, tuple(MAT + Vector((x, 0.62, 0))))
    C.rounded_box('sole', (0, 0, 0.02), (0.12, 0.26, 0.04), 0.018, sole_m, o)
    C.sphere('up', (0, 0.02, 0.07), (0.07, 0.12, 0.06), shoe_m, o, 24)
    C.tube('lace', [(-0.03, -0.04, 0.12), (0.03, -0.04, 0.12)], 0.008, sole_m, o)
    T.pop_in(o, 740 + k * 10, 1.0, 8)
    shoes.append(o)

note_m = C.mat('notes', (0.25, 0.4, 0.95), rough=0.3, emit=0.6)
rr = random.Random(31)
SONG0, SONG1 = SONG
for j in range(9):
    n = C.empty('note', None, (0, 0, 0))
    C.sphere('h', (0, 0, 0), (0.07, 0.028, 0.056), note_m, n, 12)
    C.tube('s', [(0.064, 0, 0.0), (0.064, 0, 0.22)], 0.014, note_m, n)
    C.tube('fl', [(0.064, 0, 0.22), (0.13, 0, 0.16)], 0.014, note_m, n)
    f0 = SONG0 + j * 32
    p0 = Vector((rr.uniform(-1.1, 1.0), -1.3, rr.uniform(1.8, 2.15)))
    K(n, 'scale', 0, (0, 0, 0))
    K(n, 'scale', f0, (0, 0, 0))
    K(n, 'scale', f0 + 6, (1.15, 1.15, 1.15))
    K(n, 'location', f0, tuple(p0))
    K(n, 'location', f0 + 30, tuple(p0 + Vector((rr.uniform(-0.2, 0.2), 0, 0.3))))
    K(n, 'scale', f0 + 24, (1.15, 1.15, 1.15))
    K(n, 'scale', f0 + 30, (0, 0, 0))

for o in lfs:
    r0 = tuple(o.rotation_euler)
    K(o, 'rotation_euler', 0, r0)
    K(o, 'rotation_euler', 856, r0)
    for k, f in enumerate(range(860, 940, 10)):
        K(o, 'rotation_euler', f, (r0[0] + math.radians(12 if k % 2 else -6), r0[1], r0[2]))
    K(o, 'rotation_euler', 944, r0)
K(plant, 'rotation_euler', 856, (0, 0, 0))
K(plant, 'rotation_euler', 876, (0, math.radians(-5), 0))
K(plant, 'rotation_euler', 896, (0, math.radians(3), 0))
K(plant, 'rotation_euler', 916, (0, 0, 0))
breeze = MA((1.0, 1.0, 1.0), 0.45, emit=0.6)
for k in range(2):
    o = C.empty('air', None, (0.25, -2.05 - 0.05 * k, Z0 + 0.62 + 0.06 * k))
    C.tube('st', [(-0.2 * j / 10, 0, 0.02 * math.sin(j + k)) for j in range(11)], 0.007, breeze, o)
    K(o, 'scale', 0, (0, 0, 0))
    K(o, 'scale', 858 + k * 6, (0, 0, 0))
    K(o, 'scale', 864 + k * 6, (1, 1, 1))
    K(o, 'location', 864 + k * 6, tuple(o.location))
    K(o, 'location', 900 + k * 6, tuple(o.location + Vector((0.35, 0, 0))))
    K(o, 'scale', 900 + k * 6, (1, 1, 1))
    K(o, 'scale', 906 + k * 6, (0, 0, 0))

tuki = make('tuki', 1.35)
moki = make('moki', 1.3)
ruki = make('ruki', 1.35)
TK0 = Vector((-0.42, -1.7, Z0))
MO0 = Vector((1.25, -1.0, Z0))
MO1 = Vector((0.5, -1.12, Z0))
RU0 = Vector((-1.35, -0.7, Z0))
RU1 = Vector((-1.0, -0.95, Z0))
T.place(tuki, 0, TK0)
T.turn(tuki, 0, 40)
T.place(moki, 0, MO0)
T.turn(moki, 0, -30)
T.place(ruki, 0, RU0)
T.turn(ruki, 0, 30)
T.arm(tuki, 'R', 14, fwd=-80, out=20)
T.arm(tuki, 'R', 60, fwd=-80, out=20)
T.rest_arm(tuki, 'R', 70)
T.turn(tuki, 96, 60)
hop_to(moki, 112, MO0, MO1, 16, 0.35)
T.turn(moki, 128, -50)
T.arm(moki, 'L', 132, fwd=-70, out=30)
T.arm(moki, 'L', 190, fwd=-70, out=30)
T.rest_arm(moki, 'L', 200)
T.turn(tuki, 210, 30)
S(tuki, 214, (1, 1, 1))
S(tuki, 220, (0.96, 0.96, 0.95))
S(tuki, 240, (1, 1, 1))
hop_to(ruki, 270, RU0, RU1, 16, 0.35)
T.turn(ruki, 286, 20)
T.arm(ruki, 'R', 292, fwd=-70, out=25)
T.arm(ruki, 'R', 340, fwd=-70, out=25)
T.rest_arm(ruki, 'R', 350)
TK1 = MAT + Vector((0.45, 0.05, 0))
RU2 = MAT + Vector((-0.5, 0.15, 0))
hop_to(tuki, 352, TK0, TK1, 16, 0.35)
hop_to(ruki, 360, RU1, RU2, 16, 0.35)
T.turn(tuki, 372, 80)
T.turn(ruki, 380, -80)
hop_to(moki, 380, MO1, Vector((0.95, -1.15, Z0)), 16, 0.35)
T.turn(moki, 398, -40)
f = SONG0 + 10
k = 0
while f < SONG1 - 4:
    T.turn(moki, int(f), -40 + (12 if k % 2 else -12))
    k += 1
    f += BEAT * 2
T.turn(moki, SONG1 + 4, -40)
T.turn(tuki, 704, 30)
T.turn(ruki, 704, -10)
T.arm(tuki, 'R', 734, fwd=-80, out=20)
T.arm(tuki, 'R', 770, fwd=-80, out=20)
T.rest_arm(tuki, 'R', 780)
gesture(tuki, 'hops', 790)
T.turn(moki, 846, -60)
C.wave(moki, 'L', 880, cycles=2, period=8)
gesture(ruki, 'bounce', 900)
gesture(tuki, 'bounce', 906)

T.lines(EID, LINES)
T.blinks(tuki, (60, 170, 300, 460, 620, 760))
T.blinks(moki, (90, 240, 420, 580, 720, 880))
T.blinks(ruki, (120, 260, 450, 640, 800))
