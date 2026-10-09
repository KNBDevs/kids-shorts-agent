from stage import *
from episodes.semilla_brota_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA
EID = 'semilla_brota'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0.0, -6.4, 2.2), (0.0, -1.5, 0.8), 31)
WT = ((0.0, -5.5, 2.35), (0.0, -1.8, 0.8), 30)
WJ = ((0.12, -3.1, 1.45), (0.14, -2.05, 1.0), 30)
camkey(0, WT)
camkey(430, WT)
camkey(442, WJ)
camkey(630, WJ)
camkey(642, WT)
camkey(780, WT)
camkey(794, W0)
camkey(TOTAL - 1, W0)

spawn('low_table', 2, 29, 'pastel', (0.0, -2.0, Z0), 1.05, 0)
TOP = Z0 + 0.62 * 1.05
plate = spawn('snack_plate', 0, 291, 'fresh', (-0.3, -2.12, TOP), 0.55, 0)
jar = spawn('observe_jar', 0, 292, 'fresh', (0.22, -2.05, TOP), 1.25, 0)
jseat = next(o for o in jar.children if o.name.startswith('seat'))
SEAT = Vector((0.22, -2.05 - 0.12, TOP + 0.21))
alb = spawn('photo_album', 1, 293, 'candy', (-0.32, -1.78, TOP), 0.9, 8)
pages = [o for o in alb.children if o.name.startswith('page')]
T.pop_in(alb, 384, 0.9, 8)

seed_m = M((0.86, 0.68, 0.5), rough=0.45, coat=0.5)
eye_m = M((0.72, 0.52, 0.38), rough=0.5, coat=0.3)
root_m = M((0.88, 0.66, 0.4), rough=0.5, coat=0.3)
stem_m = M((0.36, 0.7, 0.28), rough=0.45, coat=0.5)
leaf_m = M((0.26, 0.66, 0.24), rough=0.45, coat=0.5)
seed = C.empty('seed', None, (0, 0, 0))
body = C.empty('sb', seed, (0, 0, 0.03))
C.sphere('bean', (0, 0, 0), (0.06, 0.035, 0.032), seed_m, body, 24)
C.sphere('hilum', (0, -0.033, 0.004), (0.016, 0.004, 0.008), eye_m, body, 12)
S0 = Vector((-0.3, -2.12, TOP + 0.02))
K(seed, 'location', 0, tuple(S0))
K(seed, 'location', 214, tuple(S0))
for k in range(0, 21, 2):
    u = k / 20
    p = S0.lerp(SEAT, u)
    p.z += 0.25 * 4 * u * (1 - u)
    K(seed, 'location', 216 + k, tuple(p))
K(seed, 'location', 236, tuple(SEAT))

rootg = C.empty('rootg', seed, (0.0, 0, 0.02))
C.tube('r', [(0, 0, 0), (0.01, 0, -0.03), (0.0, 0, -0.07), (0.015, 0, -0.11)], 0.008, root_m, rootg)
C.tube('r2', [(0.0, 0, -0.06), (-0.03, 0, -0.08)], 0.004, root_m, rootg)
C.tube('r3', [(0.008, 0, -0.09), (0.04, 0, -0.11)], 0.004, root_m, rootg)
shoot = C.empty('shoot', seed, (0.0, 0, 0.03))
C.tube('st', [(0, 0, 0), (0.0, 0, 0.12), (0.01, 0, 0.24)], 0.011, stem_m, shoot)
for sx in (-1, 1):
    lf = C.empty('lf', shoot, (0.01, 0, 0.24), (0, math.radians(sx * 55), 0))
    C.sphere('l', (0, 0, 0.05), (0.032, 0.012, 0.055), leaf_m, lf, 16)
K(rootg, 'scale', 0, (0.001, 0.001, 0.001))
K(shoot, 'scale', 0, (0.001, 0.001, 0.001))

paper = M((0.75, 0.92, 0.62), rough=0.7, coat=0.1)
pl = C.empty('pleaf', None, (0, 0, 0))
pts = [(0.09 * math.sin(t * 6.2832 / 40) * (1 - 0.3 * math.cos(t * 6.2832 / 40)), 0.0, 0.13 * -math.cos(t * 6.2832 / 40)) for t in range(41)]
C.rounded_box('pp', (0, 0, 0), (0.17, 0.006, 0.24), 0.04, paper, pl)
C.tube('pv', [(0, -0.005, -0.1), (0, -0.005, 0.1)], 0.004, M((0.35, 0.65, 0.3), rough=0.5), pl)
PL0 = Vector((-0.5, -2.2, TOP + 0.16))
PL1 = Vector((-0.42, -2.2, TOP + 0.04))
T.pop_in(pl, 12, 1.0, 8)
K(pl, 'location', 12, tuple(PL0))
K(pl, 'rotation_euler', 12, (0, 0, 0))
K(pl, 'location', 40, tuple(PL1 + Vector((0.08, 0, 0.06))))
K(pl, 'rotation_euler', 40, (math.radians(-80), 0, math.radians(10)))
K(pl, 'location', 680, tuple(PL1 + Vector((0.08, 0, 0.06))))
K(pl, 'rotation_euler', 680, (math.radians(-80), 0, math.radians(10)))
PA = Vector((-0.25, -1.8, TOP + 0.08))
for k in range(0, 21, 2):
    u = k / 20
    p = (PL1 + Vector((0.08, 0, 0.06))).lerp(PA, u)
    p.z += 0.2 * 4 * u * (1 - u)
    K(pl, 'location', 740 + k, tuple(p))
K(pl, 'rotation_euler', 760, (math.radians(-90), 0, math.radians(8)))
K(pl, 'scale', 760, (1, 1, 1))
K(pl, 'scale', 768, (0.85, 0.85, 0.85))

drop_m = MA((0.35, 0.65, 1.0), 0.8, rough=0.05, emit=0.2)
for k, f in enumerate((300, 316, 332)):
    d = C.empty('drop', None, (0.22 + 0.04 * (k - 1), -2.05, TOP + 0.5))
    C.sphere('d', (0, 0, 0), (0.022, 0.022, 0.03), drop_m, d, 12)
    K(d, 'scale', 0, (0, 0, 0))
    K(d, 'scale', f - 1, (0, 0, 0))
    K(d, 'scale', f, (1, 1, 1))
    K(d, 'location', f, (d.location.x, d.location.y, TOP + 0.5))
    K(d, 'location', f + 12, (d.location.x, d.location.y, TOP + 0.12))
    K(d, 'scale', f + 12, (1, 1, 1))
    K(d, 'scale', f + 13, (0, 0, 0))

sun_m = M((1.0, 0.82, 0.3), rough=0.4, coat=0.5, emit=0.3)
moon_m = M((0.55, 0.6, 0.95), rough=0.4, coat=0.5, emit=0.2)
FLIPS = [420, 450, 486, 520, 556]
for k, pg in enumerate(pages):
    ic = C.empty('ic', pg, (0.17, 0.0, 0.004))
    if k % 2 == 0:
        C.sphere('sun', (0, 0, 0), (0.05, 0.05, 0.006), sun_m, ic, 20)
        for j in range(8):
            a = j * 0.785
            C.tube('ray', [(0.065 * math.cos(a), 0.065 * math.sin(a), 0), (0.085 * math.cos(a), 0.085 * math.sin(a), 0)], 0.007, sun_m, ic)
    else:
        C.sphere('moon', (0, 0, 0), (0.05, 0.05, 0.006), moon_m, ic, 20)
        C.sphere('cut', (0.025, 0.012, 0.003), (0.042, 0.042, 0.006), M((0.99, 0.97, 0.92), rough=0.65), ic, 20)
    f = FLIPS[k] if k < len(FLIPS) else 600
    K(pg, 'rotation_euler', 0, (0, 0, 0))
    K(pg, 'rotation_euler', f, (0, 0, 0))
    K(pg, 'rotation_euler', f + 6, (0, math.radians(-100), 0))
    K(pg, 'rotation_euler', f + 12, (0, math.radians(-178), 0))

clock = spawn('time_clock', 1, 978, 'candy', (0.02, -1.66, TOP), 0.7, 0)
hm = next(o for o in clock.children if o.name.startswith('hand_m'))
hh = next(o for o in clock.children if o.name.startswith('hand_h'))
T.pop_in(clock, 400, 0.7, 8)
K(hm, 'rotation_euler', 410, tuple(hm.rotation_euler))
K(hh, 'rotation_euler', 410, tuple(hh.rotation_euler))
K(hm, 'rotation_euler', 600, (0, hm.rotation_euler[1] + 16 * 6.2832, 0))
K(hh, 'rotation_euler', 600, (0, hh.rotation_euler[1] + 16 * 6.2832 / 12, 0))
T.pop_out(clock, 640, 0.7, 6)

K(body, 'scale', 420, (1, 1, 1))
K(body, 'scale', 452, (1.18, 1.25, 1.2))
K(rootg, 'scale', 452, (0.001, 0.001, 0.001))
K(rootg, 'scale', 470, (0.8, 0.8, 0.8))
K(rootg, 'scale', 522, (1.3, 1.3, 1.3))
K(rootg, 'scale', 560, (1.5, 1.5, 1.5))
K(shoot, 'scale', 520, (0.001, 0.001, 0.001))
K(shoot, 'scale', 540, (0.35, 0.35, 0.35))
K(shoot, 'scale', 562, (1.35, 1.35, 1.35))
K(shoot, 'rotation_euler', 540, (0, math.radians(40), 0))
K(shoot, 'rotation_euler', 562, (0, 0, 0))


pimo = make('pimo', 1.3)
ruki = make('ruki', 1.3)
P0 = Vector((-0.92, -1.45, Z0))
R0 = Vector((0.92, -1.4, Z0))
T.place(pimo, 0, P0)
T.turn(pimo, 0, 30)
T.place(ruki, 0, R0)
T.turn(ruki, 0, -30)
T.arm(pimo, 'R', 10, fwd=-70, out=20)
T.arm(pimo, 'R', 44, fwd=-70, out=20)
T.rest_arm(pimo, 'R', 56)
gesture(pimo, 'sway', 110)
T.turn(ruki, 186, -45)
T.arm(ruki, 'L', 206, fwd=-70, out=25)
T.arm(ruki, 'L', 240, fwd=-70, out=25)
T.rest_arm(ruki, 'L', 250)
T.arm(ruki, 'L', 296, fwd=-60, out=20)
T.arm(ruki, 'L', 340, fwd=-60, out=20)
T.rest_arm(ruki, 'L', 350)
T.turn(ruki, 380, -30)
T.turn(pimo, 470, 45)
gesture(pimo, 'hops', 482)
gesture(pimo, 'bounce', 572)
gesture(ruki, 'breathe', 640)
T.arm(pimo, 'R', 736, fwd=-70, out=20)
T.arm(pimo, 'R', 764, fwd=-70, out=20)
T.rest_arm(pimo, 'R', 776)
gesture(pimo, 'bounce', 790)
gesture(ruki, 'bounce', 796)

T.lines(EID, LINES)
T.blinks(pimo, (60, 170, 300, 440, 600, 720))
T.blinks(ruki, (90, 250, 400, 560, 700))
