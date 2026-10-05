from stage import *
from episodes.elefante_limite_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M
EID = 'elefante_limite'
Z0 = 0.08
auto_dress(EID, ENV)
BEAT = 60 / 124 * FPS

W0 = ((0.0, -6.5, 1.95), (0.0, -1.4, 0.8), 31)
WN = ((-0.35, -5.1, 1.55), (-0.35, -1.8, 0.7), 34)
camkey(0, W0)
camkey(70, W0)
camkey(84, WN)
camkey(240, WN)
camkey(256, W0)
camkey(TOTAL - 1, W0)

swing = spawn('net_swing', 0, 31, 'candy', (-0.78, -1.9, Z0), 1.0, 0)
hang = next(o for o in swing.children if o.name.startswith('net_hang'))
step = spawn('play_step', 2, 52, 'pastel', (0.45, -1.75, Z0), 1.15, 0)
STOP = Z0 + 0.23 * 1.15
ele = spawn('toy_elephant', 0, 17, 'pastel', (0, 0, 0), 1.0, 0)
E0 = Vector((-0.2, -2.2, Z0))
ER = 70
K(ele, 'location', 0, tuple(E0))
K(ele, 'rotation_euler', 0, (0, 0, math.radians(ER)))

K(hang, 'scale', 0, (1, 1, 1))
EN = Vector((-0.58, -1.95, Z0 + 0.42))
for f in range(78, 132, 2):
    u = (f - 78) / 54
    u2 = u * u * (3 - 2 * u)
    p = E0.lerp(EN, u2)
    p.z = E0.z + (EN.z - E0.z) * min(1, u * 1.6)
    K(ele, 'location', f, tuple(p))
K(ele, 'rotation_euler', 78, (0, 0, math.radians(ER)))
K(ele, 'rotation_euler', 100, (0, 0, math.radians(30)))
K(hang, 'scale', 108, (1, 1, 1))
K(hang, 'scale', 136, (1.05, 1.0, 2.3))
K(ele, 'location', 150, tuple(EN))
for f in range(156, 186, 2):
    u = (f - 156) / 30
    u2 = u * u * (3 - 2 * u)
    p = EN.lerp(E0, u2)
    p.z = EN.z + (E0.z - EN.z) * u2
    K(ele, 'location', f, tuple(p))
K(ele, 'rotation_euler', 160, (0, 0, math.radians(30)))
K(ele, 'rotation_euler', 186, (0, 0, math.radians(ER)))
K(hang, 'scale', 156, (1.05, 1.0, 2.3))
K(hang, 'scale', 168, (1.0, 1.0, 0.8))
K(hang, 'scale', 176, (1.0, 1.0, 1.15))
K(hang, 'scale', 184, (1.0, 1.0, 0.95))
K(hang, 'scale', 190, (1, 1, 1))

EP = Vector((0.33, -1.78, STOP))
K(ele, 'location', 334, tuple(E0))
for f in range(334, 356, 2):
    u = (f - 334) / 22
    u2 = u * u * (3 - 2 * u)
    p = E0.lerp(EP, u2)
    p.z += 0.4 * 4 * u * (1 - u)
    K(ele, 'location', f, tuple(p))
K(ele, 'location', 356, tuple(EP))
K(ele, 'rotation_euler', 334, (0, 0, math.radians(ER)))
K(ele, 'rotation_euler', 356, (0, 0, math.radians(110)))
K(ele, 'scale', 356, (1, 1, 1))
K(ele, 'scale', 359, (1.08, 1.08, 0.9))
K(ele, 'scale', 364, (1, 1, 1))

SONG0, SONG1 = 372, 662
k = 0
f = SONG0
while f < SONG1:
    fi = int(round(f))
    K(ele, 'location', fi, tuple(EP))
    K(ele, 'location', fi + 5, tuple(EP + Vector((0, 0, 0.07))))
    K(ele, 'rotation_euler', fi + 5, (math.radians(7 if k % 2 else -7), 0, math.radians(110 + (10 if k % 2 else -10))))
    k += 1
    f += BEAT
K(ele, 'location', SONG1 + 4, tuple(EP))
K(ele, 'rotation_euler', SONG1 + 4, (0, 0, math.radians(110)))

sign_m = M((0.98, 0.96, 0.9), rough=0.4, coat=0.5)
post_m = M((0.85, 0.62, 0.4), rough=0.6)
icon_a = M((0.95, 0.45, 0.35), rough=0.4, coat=0.6)
icon_b = M((0.35, 0.55, 0.95), rough=0.4, coat=0.6)


def sign(x, kind):
    g = C.empty('sign', None, (x, -0.75, Z0))
    C.tube('stick', [(0, 0.02, 0), (0, 0.02, 1.25)], 0.02, post_m, g)
    C.rounded_box('board', (0, 0, 1.38), (0.46, 0.04, 0.34), 0.04, sign_m, g)
    if kind == 'step':
        C.rounded_box('ic', (0, -0.025, 1.31), (0.28, 0.015, 0.08), 0.015, icon_a, g)
        C.sphere('ic2', (0, -0.03, 1.43), (0.055, 0.012, 0.065), icon_a, g, 16)
    else:
        C.sphere('nh', (-0.04, -0.03, 1.31), (0.055, 0.012, 0.045), icon_b, g, 16)
        C.tube('ns', [(0.01, -0.03, 1.32), (0.01, -0.03, 1.48)], 0.013, icon_b, g)
        C.tube('nf', [(0.01, -0.03, 1.48), (0.07, -0.03, 1.44)], 0.013, icon_b, g)
    return g


sa = sign(-0.15, 'step')
sb = sign(0.48, 'note')
T.pop_in(sa, 304, 1.0, 8)
T.pop_in(sb, 312, 1.0, 8)

note_m = C.mat('notes', (0.25, 0.4, 0.95), rough=0.3, emit=0.6)
rr = random.Random(5)
for j in range(10):
    n = C.empty('note', None, (0, 0, 0))
    C.sphere('h', (0, 0, 0), (0.075, 0.03, 0.06), note_m, n, 12)
    C.tube('s', [(0.068, 0, 0.0), (0.068, 0, 0.24)], 0.015, note_m, n)
    C.tube('fl', [(0.068, 0, 0.24), (0.14, 0, 0.18)], 0.015, note_m, n)
    f0 = SONG0 + j * 28
    x = rr.uniform(-1.1, 1.1)
    p0 = Vector((x, -1.6, rr.uniform(1.6, 2.1)))
    K(n, 'scale', 0, (0, 0, 0))
    K(n, 'scale', f0, (0, 0, 0))
    K(n, 'scale', f0 + 6, (1.2, 1.2, 1.2))
    K(n, 'location', f0, tuple(p0))
    K(n, 'location', f0 + 30, tuple(p0 + Vector((rr.uniform(-0.2, 0.2), 0, 0.35))))
    K(n, 'scale', f0 + 24, (1.2, 1.2, 1.2))
    K(n, 'scale', f0 + 30, (0, 0, 0))

gruno = make('gruno', 1.6)
pimo = make('pimo', 1.45)
G0 = Vector((-1.12, -1.05, Z0))
P0 = Vector((1.12, -0.95, Z0))
T.place(gruno, 0, G0)
T.turn(gruno, 0, 25)
T.place(pimo, 0, P0)
T.turn(pimo, 0, -25)
for side in ('L', 'R'):
    T.arm(gruno, side, 6, 0, None)
    T.arm(gruno, side, 14, fwd=-30, out=80)
    T.arm(gruno, side, 50, fwd=-30, out=80)
    T.rest_arm(gruno, side, 60)
S(gruno, 20, (1, 1, 1))
S(gruno, 28, (1.08, 1.08, 0.94))
S(gruno, 40, (1, 1, 1))
T.turn(gruno, 66, 40)
for side in ('L', 'R'):
    T.arm(gruno, side, 70, 0, None)
    T.arm(gruno, side, 80, fwd=-70, out=15)
    T.arm(gruno, side, 150, fwd=-70, out=15)
    T.arm(gruno, side, 164, fwd=-40, out=15)
    T.rest_arm(gruno, side, 190)
T.turn(pimo, 140, -30)
T.arm(pimo, 'R', 144, 0, None)
T.arm(pimo, 'R', 150, fwd=-90, out=40)
T.arm(pimo, 'R', 200, fwd=-90, out=40)
T.rest_arm(pimo, 'R', 210)
pimo['hold'].location = P0
P1 = Vector((1.18, -0.82, Z0))
hop_to(pimo, 140, P0, P1, 10, apex=0.2)
T.turn(gruno, 156, 25)
S(gruno, 158, (1, 1, 1))
S(gruno, 162, (0.94, 0.94, 1.06))
S(gruno, 170, (1, 1, 1))
T.turn(gruno, 226, 35)
for k2, f2 in enumerate(range(230, 270, 8)):
    T.turn(gruno, f2, 35 + (6 if k2 % 2 else -6))
T.turn(gruno, 274, 20)
T.turn(pimo, 296, -10)
T.arm(pimo, 'L', 300, 0, None)
T.arm(pimo, 'L', 306, fwd=-80, out=10)
T.arm(pimo, 'L', 330, fwd=-80, out=10)
T.rest_arm(pimo, 'L', 340)
T.turn(gruno, 330, 50)
T.arm(gruno, 'R', 330, 0, None)
T.arm(gruno, 'R', 336, fwd=-70, out=20)
T.arm(gruno, 'R', 352, fwd=-70, out=20)
T.rest_arm(gruno, 'R', 362)
T.turn(gruno, 368, 15)
T.turn(pimo, 368, -15)

k = 0
f = SONG0
while f < SONG1:
    fi = int(round(f))
    for ch, ph in ((gruno, 0), (pimo, 1)):
        sgn = 1 if (k + ph) % 2 else -1
        K(ch['spin'], 'rotation_euler', fi + 5, (0, math.radians(6 * sgn), math.radians((15 if ch is gruno else -15))))
        S(ch, fi, (1, 1, 1))
        S(ch, fi + 3, (1.05, 1.05, 0.95))
        S(ch, fi + 7, (1, 1, 1))
    k += 1
    f += BEAT
T.turn(gruno, SONG1 + 4, 15)
T.turn(pimo, SONG1 + 4, -15)
for side in ('L', 'R'):
    T.arm(gruno, side, SONG0, 0, None)
    T.arm(gruno, side, SONG0 + 8, fwd=-20, out=70)
    T.arm(gruno, side, SONG1, fwd=-20, out=70)
    T.rest_arm(gruno, side, SONG1 + 8)
    T.arm(pimo, side, SONG0, 0, None)
    T.arm(pimo, side, SONG0 + 8, fwd=-20, out=60)
    T.arm(pimo, side, SONG1, fwd=-20, out=60)
    T.rest_arm(pimo, side, SONG1 + 8)
T.turn(pimo, 676, -30)
T.arm(pimo, 'R', 680, 0, None)
T.arm(pimo, 'R', 686, fwd=-70, out=30)
T.arm(pimo, 'R', 720, fwd=-70, out=30)
T.rest_arm(pimo, 'R', 728)

remote = C.empty('remote', None, (0, 0, 0))
C.rounded_box('rb', (0, 0, 0), (0.08, 0.04, 0.18), 0.02, M((0.3, 0.3, 0.38), rough=0.4, coat=0.6), remote)
for j, (x, z, c) in enumerate(((-0.018, 0.05, (1, 0.3, 0.3)), (0.018, 0.05, (0.3, 0.9, 0.4)), (0.0, 0.0, (1.0, 0.8, 0.2)))):
    C.sphere('btn', (x, -0.022, z), (0.013, 0.008, 0.013), M(c, coat=0.7), remote, 10)
RH = G0 + Vector((0.45, -0.4, 0.75))
RN = Vector((-0.78, -1.9, Z0 + 0.55 - 0.12 - 0.11))
K(remote, 'scale', 0, (0, 0, 0))
K(remote, 'scale', 698, (0, 0, 0))
K(remote, 'scale', 704, (1, 1, 1))
K(remote, 'location', 698, tuple(RH))
K(remote, 'location', 728, tuple(RH))
for f in range(728, 750, 2):
    u = (f - 728) / 22
    u2 = u * u * (3 - 2 * u)
    p = RH.lerp(RN, u2)
    p.z += 0.15 * 4 * u * (1 - u)
    K(remote, 'location', f, tuple(p))
K(remote, 'rotation_euler', 728, (0, 0, 0))
K(remote, 'rotation_euler', 750, (math.radians(-80), 0, math.radians(90)))
K(hang, 'scale', 746, (1, 1, 1))
K(hang, 'scale', 752, (1, 1, 1.25))
K(hang, 'scale', 758, (1, 1, 1.08))
K(hang, 'scale', 764, (1, 1, 1.12))
K(remote, 'location', 750, tuple(RN))
K(remote, 'location', 752, tuple(RN + Vector((0, 0, -0.03))))
K(remote, 'location', 758, tuple(RN + Vector((0, 0, -0.01))))
K(remote, 'location', 764, tuple(RN + Vector((0, 0, -0.015))))
T.turn(gruno, 700, 35)
T.arm(gruno, 'R', 700, 0, None)
T.arm(gruno, 'R', 706, fwd=-60, out=20)
T.arm(gruno, 'R', 744, fwd=-60, out=20)
T.rest_arm(gruno, 'R', 754)
T.turn(gruno, 770, 15)
for k2, f2 in enumerate(range(790, 830, 8)):
    T.turn(gruno, f2, 15 + (-30 if k2 % 2 else 30))
T.turn(gruno, 836, 40)
T.turn(pimo, 820, -40)
T.arm(pimo, 'R', 820, 0, None)
T.arm(pimo, 'R', 826, fwd=-85, out=45)
T.arm(pimo, 'R', 860, fwd=-85, out=45)
T.rest_arm(pimo, 'R', 868)
gruno['hold'].location = G0
gesture(gruno, 'bounce', 850)
pimo['hold'].location = P1
gesture(pimo, 'hops', 870)

T.lines(EID, LINES)
T.blinks(gruno, (90, 220, 340, 470, 600, 720, 860))
T.blinks(pimo, (60, 200, 320, 450, 580, 700, 840))
