from stage import *
from episodes.pelota_cae_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M
EID = 'pelota_cae'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0.15, -6.4, 1.85), (0.15, -1.3, 0.75), 32)
WC = ((0.0, -5.6, 1.65), (0.0, -1.3, 0.7), 34)
camkey(0, W0)
camkey(220, W0)
camkey(236, WC)
camkey(390, WC)
camkey(404, W0)
camkey(TOTAL - 1, W0)

PL = Vector((0.55, -1.45, Z0))
step = spawn('play_step', 0, 33, 'fresh', tuple(PL), 1.0, 0)
PTOP = Z0 + 0.235

BR = 0.11 * 1.6
ball = C.empty('ball', None, (0, 0, 0))
spawn('play_ball', 1, 47, (0.95, 0.3, 0.35), (0, 0, -BR), 1.6, 0, parent=ball)

tuki = make('tuki', 1.45)
ruki = make('ruki', 1.45)
T0 = Vector((-0.9, -1.45, Z0))
T1 = Vector((-0.6, -1.3, Z0))
T2 = Vector((-0.25, -1.4, Z0))
R0 = Vector((1.2, -1.0, Z0))
T.place(tuki, 0, T0)
T.turn(tuki, 0, 10)
T.place(ruki, 0, R0)
T.turn(ruki, 0, -20)

piv = {}
for s_, sx in (('L', -1), ('R', 1)):
    objs = [o for o in tuki['rig'].children if o.name.startswith(f'Tuki.armline.{s_}') or o.name.startswith(f'Tuki.hand.{s_}')]
    sh = next(o for o in objs if o.name.startswith('Tuki.hand')).location.copy()
    p = C.empty(f'tuki_sh_{s_}', tuki['rig'], (sh.x * 0.3 / 0.52, 0.0, sh.z * 0.7 / 0.5))
    for o in objs:
        o.parent = p
        o.location = o.location - p.location
    piv[s_] = p


def tarm(side, f, deg):
    sx = -1 if side == 'L' else 1
    K(piv[side], 'rotation_euler', f, (0, math.radians(-sx * deg), 0))


hand = {s_: next(o for o in piv[s_].children if o.name.startswith('Tuki.hand')) for s_ in ('L', 'R')}
for s_ in ('L', 'R'):
    tarm(s_, 0, 0)

tarm('R', 0, 55)
tarm('L', 0, 0)
tarm('L', 10, 0)
tarm('L', 16, 150)
tarm('L', 50, 150)
tarm('L', 58, 0)
tarm('R', 24, 55)
tarm('R', 30, 40)
tarm('R', 40, 0)
for k, f in enumerate(range(12, 50, 6)):
    S(tuki, f, (1.03, 1.03, 0.97) if k % 2 else (0.98, 0.98, 1.03))
S(tuki, 52, (1, 1, 1))
T.turn(tuki, 34, -10)
T.turn(tuki, 44, 0)
tuki['hold'].location = T0
TP1 = Vector((-0.72, -1.45, Z0))
hop_to(tuki, 62, T0, TP1, 10, apex=0.2)
tarm('R', 70, 0)
tarm('R', 78, 30)
tarm('R', 84, 55)
tuki['hold'].location = TP1
hop_to(tuki, 92, TP1, T1, 12, apex=0.3)
T.turn(tuki, 104, 0)
T.turn(tuki, 114, 160)
tarm('L', 92, 0)
tarm('L', 112, 0)
tarm('L', 118, 150)
tarm('L', 150, 150)
tarm('L', 158, 0)
tarm('R', 122, 55)
tarm('R', 128, 40)
tarm('R', 138, 0)
T.turn(tuki, 160, 160)
T.turn(tuki, 168, 0)
S(tuki, 170, (1, 1, 1))
S(tuki, 174, (1.12, 1.12, 0.88))
S(tuki, 180, (0.95, 0.95, 1.08))
S(tuki, 186, (1, 1, 1))
T.turn(tuki, 190, 20)

T.turn(ruki, 196, -20)
T.turn(ruki, 206, -40)
T.arm(ruki, 'R', 0, 0, None)
T.arm(ruki, 'R', 228, 0, None)
T.arm(ruki, 'R', 236, fwd=-75, out=30)
T.arm(ruki, 'R', 262, fwd=-75, out=30)
T.rest_arm(ruki, 'R', 270)
T.turn(ruki, 272, -25)
T.turn(tuki, 236, 40)
for side in ('L', 'R'):
    T.arm(ruki, side, 296, 0, None)
T.arm(ruki, 'L', 306, fwd=-150, out=10)
T.arm(ruki, 'L', 386, fwd=-150, out=10)
T.rest_arm(ruki, 'L', 396)
gesture(ruki, 'breathe', 330)

T.turn(tuki, 398, 0)
tuki['hold'].location = T1
hop_to(tuki, 404, T1, T2, 12, apex=0.25)
T.turn(tuki, 416, 0)
tarm('R', 410, 0)
tarm('R', 420, 0)
tarm('R', 428, 70)
tarm('R', 452, 70)
tarm('R', 458, 50)
tarm('R', 468, 0)
for k, f in enumerate(range(430, 452, 6)):
    S(tuki, f, (1.04, 1.04, 0.96) if k % 2 else (1, 1, 1))
S(tuki, 452, (1, 1, 1))
T.turn(tuki, 470, 15)
T.turn(ruki, 470, -40)
T.arm(ruki, 'R', 478, 0, None)
T.arm(ruki, 'R', 484, fwd=-30, out=55)
T.arm(ruki, 'R', 530, fwd=-30, out=55)
T.rest_arm(ruki, 'R', 540)

tarm('R', 556, 0)
tarm('R', 566, 70)
tarm('R', 576, 70)
tarm('R', 590, 120)
tarm('R', TOTAL - 1, 120)
T.turn(tuki, 560, 0)
T.turn(tuki, 590, 0)
tuki['hold'].location = T2
gesture(tuki, 'bounce', 596)
T.turn(ruki, 640, -35)
T.arm(ruki, 'R', 644, 0, None)
T.arm(ruki, 'R', 652, fwd=-150, out=25)
T.arm(ruki, 'R', 700, fwd=-150, out=25)
T.rest_arm(ruki, 'R', 710)
for k, f in enumerate(range(720, 780, 8)):
    S(tuki, f, (1.05, 1.05, 0.95) if k % 2 else (1, 1, 1))
    S(ruki, f + 2, (1.03, 1.03, 0.97) if k % 2 else (1, 1, 1))
C.wave(ruki, 'L', 760, cycles=2, period=8)

T.lines(EID, LINES)
T.blinks(tuki, (60, 160, 260, 380, 520, 640, 760))
T.blinks(ruki, (90, 200, 320, 450, 600, 730))



def hand_pos(rig_hand, f, fwd=0.0):
    sc.frame_set(f)
    h = rig_hand.matrix_world.translation.copy()
    o = rig_hand.parent.matrix_world.translation
    d = (h - o).normalized()
    return h + d * (BR + 0.03) + Vector((0, -0.04, -BR * 0.6))


def ruki_hand(f):
    sc.frame_set(f)
    a = next(o for o in ruki['rig'].children if o.name.endswith('.arm.R'))
    m = next(o for o in a.children if 'armmesh' in o.name)
    tip = m.matrix_world @ Vector((0, 0, -1.0))
    d = (tip - a.matrix_world.translation).normalized()
    return tip + d * (BR + 0.02)


def hold(f0, f1, fn):
    for f in range(f0, f1 + 1, 2):
        K(ball, 'location', f, tuple(fn(f)))


def fall(f0, p0, floor, n=40):
    g = 9.81 / FPS ** 2
    z, v, x = p0.z, 0.0, p0.copy()
    f = f0
    bounces = 0
    while f < f0 + n:
        v -= g
        z += v
        if z <= floor + BR:
            z = floor + BR
            v = -v * 0.35
            bounces += 1
            if abs(v) < 0.01:
                v = 0
        K(ball, 'location', f, (x.x, x.y, z))
        f += 1
    return Vector((x.x, x.y, floor + BR)), f


sc = bpy.context.scene
hold(0, 30, lambda f: hand_pos(hand['R'], f) + Vector((0, 0, BR * 0.6)))
p, f = fall(31, Vector(ball.location), Z0, 28)
rest1 = Vector(p)
K(ball, 'location', 72, tuple(rest1))
hold(84, 128, lambda f: hand_pos(hand['R'], f) + Vector((0, 0, BR * 0.6)))
for f in range(74, 84, 2):
    u = (f - 74) / 10
    K(ball, 'location', f, tuple(rest1.lerp(hand_pos(hand['R'], 84) + Vector((0, 0, BR * 0.6)), u)))
p, f = fall(129, Vector(ball.location), Z0, 30)
rest2 = Vector(p)
restp = rest2
K(ball, 'location', 418, tuple(restp))
for f in range(418, 428, 2):
    u = (f - 418) / 10
    K(ball, 'location', f, tuple(restp.lerp(hand_pos(hand['R'], 428) + Vector((0, 0, BR * 0.6)), u)))
hold(428, 456, lambda f: hand_pos(hand['R'], f) + Vector((0, 0, BR * 0.6)))
p, f = fall(457, Vector(ball.location), PTOP if abs(Vector(ball.location).x - PL.x) < 0.3 and abs(Vector(ball.location).y - PL.y) < 0.2 else Z0, 30)
rest3 = Vector(p)
K(ball, 'location', 558, tuple(rest3))
for f in range(558, 566, 2):
    u = (f - 558) / 8
    K(ball, 'location', f, tuple(rest3.lerp(hand_pos(hand['R'], 566) + Vector((0, 0, BR * 0.6)), u)))
hold(566, TOTAL - 1, lambda f: hand_pos(hand['R'], f) + Vector((0, 0, BR * 0.6)))
glow = C.mat('agl', (1.0, 0.6, 0.2), rough=0.3, emit=2.2)
AX = Vector((rest2.x, rest2.y - 0.05, 0.0))
arrow = C.empty('arrow', None, (AX.x, AX.y, rest2.z + 0.62))
C.tube('ashaft', [(0, 0, 0.32), (0, 0, -0.12)], 0.045, glow, arrow)
C.lathe('ahead', [(-0.32, 0.0), (-0.32, 0.01), (-0.12, 0.13), (-0.11, 0.0)], glow, arrow, segs=32)
T.pop_in(arrow, 300, 1.0, 8)
for k, f in enumerate(range(312, 392, 10)):
    K(arrow, 'location', f, (AX.x, AX.y, rest2.z + 0.62 - (0.08 if k % 2 else 0.0)))
T.pop_out(arrow, 392, 1.0, 6)
gring = C.empty('gring', None, (AX.x, AX.y, Z0 + 0.005))
C.tube('gr', [(math.cos(k * 6.2832 / 40) * 0.22, math.sin(k * 6.2832 / 40) * 0.12, 0) for k in range(41)], 0.02, glow, gring)
T.pop_in(gring, 304, 1.0, 8)
T.pop_out(gring, 392, 1.0, 6)
sc.frame_set(0)
word3d('¡TÚ!', (0.95, 0.4, 0.2), (-0.1, -1.6, 2.4), 660, 760, size=0.5, max_w=1.0)
