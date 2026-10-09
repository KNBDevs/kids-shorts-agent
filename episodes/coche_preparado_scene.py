from stage import *
from episodes.coche_preparado_plan import *
import ep_tools as T
import random
from props.lib import spawn, auto_dress, M, MA
EID = 'coche_preparado'
Z0 = 0.08
auto_dress(EID, ENV)
BEAT = 60 / 124 * FPS

W0 = ((0.0, -6.8, 3.1), (0.0, -1.4, 0.8), 31)
WC = ((0.1, -5.4, 3.0), (0.1, -1.3, 0.75), 31)
WB = ((0.0, -4.4, 2.9), (0.0, -1.2, 0.85), 31)
camkey(0, WC)
camkey(186, WC)
camkey(198, WB)
camkey(268, WB)
camkey(280, WC)
camkey(570, WC)
camkey(582, WB)
camkey(650, WB)
camkey(662, WC)
camkey(770, WC)
camkey(790, W0)
camkey(TOTAL - 1, W0)

CAR0 = Vector((0.0, -1.4, Z0))
YAW = -90
car = spawn('toy_car', 0, 17, 'candy', tuple(CAR0), 1.0, YAW)
wheels = [o for o in car.children if o.name.startswith('wheel')]
steer = next(o for o in car.children if o.name.startswith('steer'))

SEAT_G = (0.12, -0.3)
SEAT_B = (0.12, 0.3)
SEAT_O = (-0.6, 0.04)
ZF = 0.2 + 0.29
ZR = 0.2 + 0.53

gruno = make('gruno', 1.12)
bopi = make('bopi', 1.0)
bol = make('bolita', 0.95)
for ch, sp, z in ((gruno, SEAT_G, ZF), (bol, SEAT_O, ZR)):
    ch['hold'].parent = car
    T.place(ch, 0, (sp[0], sp[1], z))
    T.turn(ch, 0, 90)

def to_local(w):
    d = Vector(w) - CAR0
    a = math.radians(-YAW)
    return Vector((d.x * math.cos(a) - d.y * math.sin(a), d.x * math.sin(a) + d.y * math.cos(a), d.z))


bopi['hold'].parent = car
BO_OUT = to_local((1.08, -1.6, Z0))
T.place(bopi, 0, BO_OUT)
T.turn(bopi, 0, 60)

dash_m = M((0.3, 0.3, 0.36), rough=0.5, coat=0.4)
red = C.mat('lamp_red', (0.95, 0.15, 0.12), rough=0.3, emit=0.35)
grn = C.mat('lamp_grn', (0.15, 0.85, 0.3), rough=0.3, emit=0.35)
lamps = []
for (x, y, z) in ((0.73, -0.3, 0.2 + 0.56), (0.73, 0.0, 0.2 + 0.56), (0.73, 0.3, 0.2 + 0.56)):
    pv = C.empty('lampp', car, (x, y, z))
    C.rounded_box('lb', (0, 0, 0), (0.06, 0.17, 0.15), 0.03, dash_m, pv)
    on = C.empty('on', pv, (0.0, 0, 0.0))
    C.sphere('g', (0.04, 0, 0), (0.04, 0.068, 0.068), grn, on, 16)
    off = C.empty('off', pv, (0.0, 0, 0.0))
    C.sphere('r', (0.04, 0, 0), (0.04, 0.068, 0.068), red, off, 16)
    lamps.append((on, off))


def lamp(k, f, ok):
    on, off = lamps[k]
    K(on, 'scale', f, (1, 1, 1) if ok else (0, 0, 0))
    K(off, 'scale', f, (0, 0, 0) if ok else (1, 1, 1))


lamp(0, 0, True)
lamp(1, 0, False)
lamp(2, 0, False)
lamp(1, 412, False)
lamp(1, 416, True)
lamp(2, 548, False)
lamp(2, 552, True)

boost = C.empty('boost', car, (SEAT_O[0], SEAT_O[1], 0.2 + 0.41))
C.rounded_box('bs', (0.02, 0, 0.06), (0.38, 0.46, 0.12), 0.05, M((0.55, 0.78, 0.98), rough=0.5, coat=0.4), boost)
C.rounded_box('bsb', (-0.17, 0, 0.2), (0.08, 0.46, 0.32), 0.04, M((0.55, 0.78, 0.98), rough=0.5, coat=0.4), boost)
bar_m = M((0.98, 0.72, 0.3), rough=0.45, coat=0.5)
pad_m = M((0.98, 0.9, 0.7), rough=0.6, coat=0.2)


def lapbar(seat, z, reach, h):
    pv = C.empty('lap', car, (seat[0] - 0.02, seat[1], z + 0.12))
    for y in (-0.22, 0.22):
        C.tube('arm', [(0, y, 0), (reach * 0.6, y, h * 0.8), (reach, y, h)], 0.022, bar_m, pv)
    C.tube('bar', [(reach, -0.22, h), (reach, 0.22, h)], 0.045, pad_m, pv)
    return pv


bg = lapbar(SEAT_G, ZF, 0.46, 0.16)
bo = lapbar(SEAT_O, ZR, 0.4, 0.14)
bb = lapbar(SEAT_B, ZF, 0.46, 0.16)
UP = (0, math.radians(-75), 0)
K(bo, 'rotation_euler', 0, (0, math.radians(-30), 0))
for f in (204, 220):
    K(bo, 'rotation_euler', f, (0, math.radians(-40), 0))
    K(bo, 'rotation_euler', f + 8, (0, math.radians(-25), 0))
K(bo, 'rotation_euler', 396, (0, math.radians(-30), 0))
K(bo, 'rotation_euler', 410, (0, 0, 0))
K(bb, 'rotation_euler', 0, UP)
K(bb, 'rotation_euler', 536, UP)
K(bb, 'rotation_euler', 550, (0, 0, 0))

gog_m = M((0.98, 0.55, 0.3), rough=0.35, coat=0.7)
lens_m = MA((0.6, 0.85, 1.0), 0.5, rough=0.05, emit=0.2)
gog = C.empty('gog2', car, (SEAT_G[0] + 0.42, SEAT_G[1], ZF + 0.6))
gog.rotation_euler = (0, 0, math.radians(90))
for x in (-0.11, 0.11):
    C.tube('rim', [(x + 0.08 * math.cos(k * 6.2832 / 32), 0, 0.08 * math.sin(k * 6.2832 / 32)) for k in range(33)], 0.018, gog_m, gog)
    C.sphere('ln', (x, 0, 0), (0.075, 0.01, 0.075), lens_m, gog, 20)
C.tube('br', [(-0.03, 0, 0.02), (0.03, 0, 0.02)], 0.015, gog_m, gog)
T.pop_in(gog, 292, 1.0, 8)
T.pop_out(gog, 340, 1.0, 6)

note_m = C.mat('notes', (0.25, 0.4, 0.95), rough=0.3, emit=0.6)
rr = random.Random(12)
SONG0, SONG1 = SONG
for j in range(9):
    n = C.empty('note', None, (0, 0, 0))
    C.sphere('h', (0, 0, 0), (0.07, 0.028, 0.056), note_m, n, 12)
    C.tube('s', [(0.064, 0, 0.0), (0.064, 0, 0.22)], 0.014, note_m, n)
    C.tube('fl', [(0.064, 0, 0.22), (0.13, 0, 0.16)], 0.014, note_m, n)
    f0 = SONG0 + j * 32
    p0 = Vector((rr.uniform(-1.0, 1.0), -0.6, rr.uniform(2.2, 2.5)))
    K(n, 'scale', 0, (0, 0, 0))
    K(n, 'scale', f0, (0, 0, 0))
    K(n, 'scale', f0 + 6, (1.15, 1.15, 1.15))
    K(n, 'location', f0, tuple(p0))
    K(n, 'location', f0 + 30, tuple(p0 + Vector((rr.uniform(-0.2, 0.2), 0, 0.3))))
    K(n, 'scale', f0 + 24, (1.15, 1.15, 1.15))
    K(n, 'scale', f0 + 30, (0, 0, 0))

for f in range(10, 90, 8):
    K(car, 'scale', f, (1.0, 1.0, 1.0))
    K(car, 'scale', f + 4, (1.0, 1.0, 1.02))
K(car, 'scale', 96, (1, 1, 1))
K(car, 'location', 0, tuple(CAR0))
K(car, 'location', 790, tuple(CAR0))
CAR1 = CAR0 + Vector((0.0, -0.45, 0))
for k in range(0, 41, 2):
    u = k / 40
    u2 = u * u * (3 - 2 * u)
    K(car, 'location', 790 + k, tuple(CAR0.lerp(CAR1, u2)))
for w in wheels:
    K(w, 'rotation_euler', 790, (math.radians(90), 0, 0))
    K(w, 'rotation_euler', 830, (math.radians(90), 0, math.radians(-160)))
K(steer, 'rotation_euler', 0, tuple(steer.rotation_euler))
for k, f in enumerate(range(16, 80, 10)):
    K(steer, 'rotation_euler', f, (math.radians(12 if k % 2 else -12), math.radians(-60), 0))
K(steer, 'rotation_euler', 90, (0, math.radians(-60), 0))

word3d('¡LISTOS!', (0.35, 0.8, 0.45), (0.0, -1.0, 2.15), 752, 788, 0.26, 1.0)

for f in (14, 30, 46, 62):
    S(gruno, f, (1, 1, 1))
    S(gruno, f + 4, (1.05, 1.05, 0.95))
T.arm(gruno, 'R', 10, fwd=-50, out=30)
T.arm(gruno, 'R', 80, fwd=-50, out=30)
T.rest_arm(gruno, 'R', 92)
T.arm(bopi, 'R', 100, fwd=-70, out=30)
T.arm(bopi, 'R', 150, fwd=-70, out=30)
T.rest_arm(bopi, 'R', 160)
T.turn(bol, 196, 60)
gesture(bol, 'bounce', 200)
T.turn(bol, 240, 90)
T.turn(gruno, 286, 50)
T.turn(gruno, 344, 90)
T.turn(bopi, 350, 40)
T.arm(bopi, 'L', 356, fwd=-60, out=20)
T.arm(bopi, 'L', 400, fwd=-60, out=20)
T.rest_arm(bopi, 'L', 410)
T.turn(bopi, 420, 60)
BO_IN = Vector((SEAT_B[0], SEAT_B[1], ZF))
T.place(bopi, 506, BO_OUT)
hop_to(bopi, 508, BO_OUT, BO_IN, 18, 0.6)
T.place(bopi, 527, BO_IN)
T.turn(bopi, 512, 90)
f = SONG0 + 6
k = 0
while f < SONG1 - 4:
    for ch, a in ((gruno, 90), (bol, 90)):
        T.turn(ch, int(f), a + (8 if k % 2 else -8))
    k += 1
    f += BEAT * 2
for ch in (gruno, bol):
    T.turn(ch, SONG1 + 4, 90)
gesture(bol, 'bounce', 760)
T.arm(gruno, 'L', 856, fwd=-40, out=110)
for ff in (866, 880, 894):
    S(gruno, ff, (1, 1, 1))
    S(gruno, ff + 3, (1.04, 1.04, 0.95))
T.arm(gruno, 'L', 904, fwd=-40, out=110)
T.rest_arm(gruno, 'L', 916)
T.turn(bopi, 926, 120)
T.arm(bopi, 'L', 930, fwd=-70, out=20)
T.arm(bopi, 'L', 970, fwd=-70, out=20)
T.rest_arm(bopi, 'L', 980)
T.turn(gruno, 940, 70)
gesture(gruno, 'bounce', 960)

T.lines(EID, LINES)
T.blinks(gruno, (60, 190, 330, 480, 640, 820, 960))
T.blinks(bopi, (80, 230, 380, 520, 700, 880))
T.blinks(bol, (100, 260, 450, 600, 760, 900))
