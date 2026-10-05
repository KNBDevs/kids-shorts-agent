from stage import *
from episodes.puente_cooperacion_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M
EID = 'puente_cooperacion'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0.0, -6.6, 1.95), (0.0, -1.3, 0.7), 31)
WL = ((-0.25, -6.3, 1.9), (-0.25, -1.4, 0.65), 33)
WR = ((0.2, -6.3, 1.9), (0.2, -1.4, 0.65), 33)
camkey(0, W0)
camkey(60, W0)
camkey(72, WL)
camkey(150, WL)
camkey(168, WR)
camkey(320, WR)
camkey(338, W0)
camkey(TOTAL - 1, W0)

SCL = 1.1
BR = Vector((0.0, -2.1, Z0))
kit = spawn('bridge_kit', 1, 58, 'fresh', tuple(BR), SCL, 0)
P = {o.name.split('.')[0]: o for o in kit.children if o.name.startswith('bk_')}
H, D = 0.3, 0.06
FINAL = {k: P[k].location.copy() for k in P}
PILE = {
    'bk_deck': Vector((-1.0, 0.68, D / 2)),
    'bk_last': Vector((-1.0, 0.68, D * 1.5)),
    'bk_short': Vector((-1.0, 0.68, D * 2.5 + H)),
    'bk_base0': Vector((-1.25, 0.68, D * 2)),
    'bk_base1': Vector((-0.75, 0.68, D * 2)),
}
for k, v in PILE.items():
    P[k].location = v
    K(P[k], 'location', 0, tuple(v))


def fly(o, f0, a, b, dur=14, apex=0.35, rot0=None, rot1=None):
    for t in range(0, dur + 1, 2):
        u = t / dur
        u2 = u * u * (3 - 2 * u)
        p = a.lerp(b, u2)
        p.z += apex * 4 * u * (1 - u)
        K(o, 'location', f0 + t, tuple(p))
        if rot0 is not None:
            K(o, 'rotation_euler', f0 + t, tuple(Vector(rot0).lerp(Vector(rot1), u2)))
    K(o, 'scale', f0 + dur, (1, 1, 1))
    K(o, 'scale', f0 + dur + 2, (1.1, 1.1, 0.85))
    K(o, 'scale', f0 + dur + 6, (1, 1, 1))
    K(o, 'scale', f0 - 1, (1, 1, 1))


def bump(o, f, base, h=0.08):
    K(o, 'location', f, tuple(base))
    K(o, 'location', f + 4, tuple(base + Vector((0, 0, h))))
    K(o, 'location', f + 8, tuple(base))


sh = P['bk_short']
TIP = Vector((-0.42, 0.0, H + D / 2))
fly(sh, 66, PILE['bk_short'], TIP, 14, 0.4)
K(sh, 'rotation_euler', 80, (0, 0, 0))
K(sh, 'location', 84, tuple(TIP))
K(sh, 'location', 92, tuple(TIP + Vector((0.04, 0, -0.1))))
K(sh, 'rotation_euler', 92, (0, math.radians(20), 0))
K(sh, 'location', 96, tuple(TIP + Vector((0.03, 0, -0.08))))
K(sh, 'rotation_euler', 96, (0, math.radians(17), 0))
K(sh, 'location', 136, tuple(TIP + Vector((0.03, 0, -0.08))))
K(sh, 'rotation_euler', 136, (0, math.radians(17), 0))
fly(sh, 140, TIP + Vector((0.03, 0, -0.08)), Vector((-3.4, 1.4, 0.0)), 20, 1.4, (0, math.radians(17), 0), (math.radians(200), math.radians(60), 0))
K(sh, 'scale', 166, (1, 1, 1))
K(sh, 'scale', 170, (0, 0, 0))

fly(P['bk_base0'], 186, PILE['bk_base0'], FINAL['bk_base0'], 16, 0.45)
fly(P['bk_base1'], 214, PILE['bk_base1'], FINAL['bk_base1'], 16, 0.45)
fly(P['bk_deck'], 262, PILE['bk_deck'], FINAL['bk_deck'], 18, 0.5)
K(P['bk_last'], 'location', 258, tuple(PILE['bk_last']))
K(P['bk_last'], 'location', 264, tuple(PILE['bk_last'] + Vector((0, 0, -D))))
fly(P['bk_last'], 434, PILE['bk_last'] + Vector((0, 0, -D)), FINAL['bk_last'], 18, 0.55)

glow = C.mat('pglow', (1.0, 0.88, 0.4), rough=0.3, emit=2.0)
for f0, k in ((202, 'bk_base0'), (230, 'bk_base1'), (280, 'bk_deck'), (452, 'bk_last')):
    c = BR + FINAL[k] * SCL + Vector((0, -0.2, 0.15))
    for j in range(6):
        o = C.sphere('spk', tuple(c), (1, 1, 1), glow, None, 10)
        a = j * 1.047 + 0.3
        K(o, 'scale', 0, (0, 0, 0))
        K(o, 'scale', f0 - 1, (0, 0, 0))
        K(o, 'scale', f0, (0.03,) * 3)
        K(o, 'location', f0, tuple(c))
        K(o, 'location', f0 + 10, tuple(c + Vector((math.cos(a) * 0.35, -0.05, 0.1 + abs(math.sin(a)) * 0.3))))
        K(o, 'scale', f0 + 9, (0.025,) * 3)
        K(o, 'scale', f0 + 12, (0, 0, 0))

ball = C.empty('ballpiv', None, (0, 0, 0))
spawn('play_ball', 2, 91, 'candy', (0, 0, -0.11 * 1.5), 1.5, 0, parent=ball)
TOPZ = Z0 + (H + D) * SCL + 0.11 * 1.5
K(ball, 'scale', 0, (0, 0, 0))
K(ball, 'scale', 497, (0, 0, 0))
K(ball, 'scale', 502, (1, 1, 1))
for f in range(498, 562, 2):
    u = (f - 498) / 62
    x = -1.15 + 2.3 * u
    K(ball, 'location', f, (x, -2.1, TOPZ))
    K(ball, 'rotation_euler', f, (0, math.radians(360 * 2.6 * u), 0))
K(ball, 'scale', 562, (1, 1, 1))
K(ball, 'scale', 568, (0, 0, 0))

gruno = make('gruno', 1.6)
ruki = make('ruki', 1.45)
pimo = make('pimo', 1.45)
G0 = Vector((-1.05, -0.45, Z0))
R0 = Vector((0.95, -0.45, Z0))
P0 = Vector((0.0, -1.2, Z0))
T.place(gruno, 0, G0)
T.turn(gruno, 0, 15)
T.place(ruki, 0, R0)
T.turn(ruki, 0, -20)
T.place(pimo, 0, P0)
T.turn(pimo, 0, 0)

for side in ('L', 'R'):
    T.arm(gruno, side, 6, 0, None)
    T.arm(gruno, side, 12, fwd=-55, out=60)
    T.arm(gruno, side, 50, fwd=-55, out=60)
    T.rest_arm(gruno, side, 58)
S(gruno, 20, (1, 1, 1))
S(gruno, 28, (1.08, 1.08, 0.94))
S(gruno, 40, (1, 1, 1))
T.turn(pimo, 20, -25)
T.turn(ruki, 20, -35)
T.turn(gruno, 60, 15)
T.turn(gruno, 66, 40)
T.arm(gruno, 'R', 62, 0, None)
T.arm(gruno, 'R', 68, fwd=-70, out=20)
T.arm(gruno, 'R', 84, fwd=-70, out=20)
T.rest_arm(gruno, 'R', 92)
T.turn(gruno, 98, 20)
for k, f in enumerate(range(100, 136, 6)):
    S(gruno, f, (1.12, 1.12, 0.86) if k % 2 == 0 else (1, 1, 1))
    T.turn(gruno, f, 20 + (10 if k % 2 else -10))
T.turn(gruno, 138, 40)
T.arm(gruno, 'R', 136, 0, None)
T.arm(gruno, 'R', 142, fwd=-60, out=20)
T.rest_arm(gruno, 'R', 156)
T.turn(gruno, 158, 15)

T.turn(ruki, 160, -35)
T.turn(ruki, 168, -10)
T.arm(ruki, 'L', 180, 0, None)
T.arm(ruki, 'L', 186, fwd=-60, out=20)
T.arm(ruki, 'L', 206, fwd=-60, out=40)
T.arm(ruki, 'L', 214, fwd=-60, out=20)
T.arm(ruki, 'L', 234, fwd=-60, out=40)
T.rest_arm(ruki, 'L', 244)
T.turn(ruki, 186, -55)
T.turn(ruki, 214, -40)
T.turn(ruki, 244, -15)
T.turn(gruno, 190, 30)
T.turn(gruno, 230, 50)

T.turn(pimo, 250, -30)
for side in ('L', 'R'):
    T.arm(pimo, side, 256, 0, None)
    T.arm(pimo, side, 262, fwd=-75, out=15)
    T.arm(pimo, side, 282, fwd=-75, out=15)
    T.rest_arm(pimo, side, 292)
gesture(pimo, 'bounce', 296)
T.turn(pimo, 300, 0)

T.turn(ruki, 326, -15)
T.turn(ruki, 334, 0)
T.arm(ruki, 'R', 340, 0, None)
T.arm(ruki, 'R', 346, fwd=-30, out=70)
T.arm(ruki, 'R', 396, fwd=-30, out=70)
T.rest_arm(ruki, 'R', 404)
S(ruki, 372, (1, 1, 1))
S(ruki, 380, (1.04, 1.04, 0.96))
S(ruki, 390, (1, 1, 1))
T.turn(pimo, 340, 15)
T.turn(gruno, 340, 30)
T.turn(gruno, 404, 0)
gruno['hold'].location = G0
gesture(gruno, 'hops', 408)
T.arm(gruno, 'R', 406, 0, None)
T.arm(gruno, 'R', 412, fwd=-150, out=20)
T.arm(gruno, 'R', 428, fwd=-150, out=20)
T.arm(gruno, 'R', 436, fwd=-70, out=20)
T.arm(gruno, 'R', 452, fwd=-70, out=20)
T.rest_arm(gruno, 'R', 460)
T.turn(gruno, 434, 45)
T.turn(gruno, 462, 15)
T.turn(ruki, 430, -40)
T.turn(pimo, 430, -20)

confetti(492, (0.0, -1.9, 1.2), 30, 2.2)
for ch, f in ((pimo, 490), (ruki, 494), (gruno, 498)):
    T.turn(ch, f, 0)
gruno['hold'].location = G0
gesture(gruno, 'bounce', 500)
pimo['hold'].location = P0
gesture(pimo, 'hops', 492)
ruki['hold'].location = R0
gesture(ruki, 'breathe', 500)
T.turn(pimo, 520, -40)
T.turn(ruki, 520, -50)
T.turn(gruno, 520, 30)
T.turn(pimo, 560, 0)
T.turn(ruki, 560, -10)
T.turn(gruno, 560, 15)
for k, f, ch in (('bk_base0', 572, ruki), ('bk_base1', 576, ruki), ('bk_deck', 592, pimo), ('bk_last', 610, gruno)):
    bump(P[k], f, FINAL[k], 0.07)
    S(ch, f, (1, 1, 1))
    S(ch, f + 4, (1.06, 1.06, 0.94))
    S(ch, f + 10, (1, 1, 1))

T.turn(gruno, 646, 15)
T.turn(gruno, 652, 0)
T.arm(gruno, 'L', 648, 0, None)
T.arm(gruno, 'L', 654, fwd=-120, out=30)
T.arm(gruno, 'L', 668, fwd=-120, out=30)
T.rest_arm(gruno, 'L', 676)
T.turn(gruno, 680, -90)
GX = Vector((-2.9, -0.6, Z0))
hop_to(gruno, 684, G0, GX, 18, apex=0.5)
T.turn(pimo, 690, -45)
T.turn(ruki, 690, -45)
GB = Vector((-1.05, -0.45, Z0))
T.place(gruno, 740, GX)
T.turn(gruno, 738, 90)
hop_to(gruno, 742, GX, GB, 20, apex=0.4)
T.turn(gruno, 764, 25)
plate = spawn('snack_plate', 1, 64, 'candy', (0, 0, 0), 1.25, 0, parent=gruno['hold'])
plate.location = (0.42, -0.42, 0.62)
chip = M((0.35, 0.2, 0.1), rough=0.5, coat=0.3)
dough = M((0.93, 0.7, 0.42), rough=0.65, coat=0.15)
for j, (x, y) in enumerate(((-0.08, -0.05), (0.08, -0.04), (0.0, 0.08))):
    C.sphere('ck', (x, y, 0.05), (0.07, 0.07, 0.022), dough, plate, 24)
    for q in range(3):
        a = q * 2.1 + j
        C.sphere('ckc', (x + math.cos(a) * 0.035, y + math.sin(a) * 0.035, 0.07), (0.01, 0.01, 0.006), chip, plate, 8)
K(plate, 'scale', 0, (0, 0, 0))
K(plate, 'scale', 739, (0, 0, 0))
K(plate, 'scale', 740, (1.25,) * 3)
for side in ('L', 'R'):
    T.arm(gruno, side, 736, fwd=-70, out=25)
    T.arm(gruno, side, TOTAL - 1, fwd=-70, out=25)
T.turn(pimo, 770, -30)
T.turn(ruki, 770, -40)
pimo['hold'].location = P0
gesture(pimo, 'hops', 776)
C.wave(ruki, 'R', 786, cycles=2, period=8)

T.lines(EID, LINES)
T.blinks(gruno, (90, 200, 320, 470, 600, 720, 800))
T.blinks(ruki, (120, 260, 380, 520, 640, 760))
T.blinks(pimo, (80, 210, 350, 480, 610, 740))
word3d('¡JUNTOS!', (0.95, 0.45, 0.15), (0.0, -1.7, 2.35), 494, 570, size=0.5, max_w=1.9)
