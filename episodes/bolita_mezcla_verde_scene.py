from stage import *
from episodes.bolita_mezcla_verde_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA
from props.basic import anim_color
EID = 'bolita_mezcla_verde'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0, -7.0, 1.35), (0, -1.2, 1.05), 37)
WT = ((0.1, -4.3, 1.55), (0.1, -1.75, 0.6), 40)
WF = ((-0.75, -5.4, 1.5), (-0.8, -1.3, 0.55), 35)
WP = ((-0.75, -6.2, 2.3), (-0.9, -0.9, 0.6), 37)
camkey(0, W0)
camkey(236, W0)
camkey(250, WT)
camkey(440, WT)
camkey(456, W0)
camkey(530, W0)
camkey(544, WF)
camkey(600, WF)
camkey(616, W0)
camkey(646, W0)
camkey(662, WP)
camkey(TOTAL - 1, WP)

BLUE = (0.08, 0.3, 0.95)
YEL = (1.0, 0.78, 0.05)
GREEN = (0.15, 0.72, 0.2)
RED = (0.78, 0.025, 0.02)
TB = Vector((0.1, -1.75, Z0))
tab_m = M((0.98, 0.9, 0.7), rough=0.45, coat=0.4)
leg_m = M((0.55, 0.78, 0.95), rough=0.4, coat=0.5)
TH = 0.42
C.rounded_box('table', tuple(TB + Vector((0, 0, TH - 0.03))), (1.15, 0.52, 0.06), 0.03, tab_m, None)
for x in (-0.5, 0.5):
    for y in (-0.19, 0.19):
        C.tube('tleg', [tuple(TB + Vector((x, y, 0))), tuple(TB + Vector((x, y, TH - 0.05)))], 0.03, leg_m, None)
TOP = TB + Vector((0, 0, TH))
pal = spawn('paint_palette', 1, 8101, (0.98, 0.7, 0.8), tuple(TOP), 1.0, 0)


def pot(loc, col):
    g = C.empty('pot', None, tuple(loc))
    C.lathe('jar', [(0, 0.0), (0, 0.09), (0.02, 0.1), (0.15, 0.1), (0.17, 0.085), (0.18, 0.0)], MA((0.95, 0.97, 1.0), 0.35), g, segs=40)
    C.lathe('paint', [(0, 0.0), (0, 0.088), (0.13, 0.088), (0.14, 0.0)], M(col, rough=0.25, coat=0.8), g, segs=40)
    C.tube('lid', [(math.cos(k * 6.2832 / 40) * 0.092, math.sin(k * 6.2832 / 40) * 0.092, 0.17) for k in range(41)], 0.012, M(col, coat=0.6), g)
    return g


PB = TOP + Vector((-0.44, 0.02, 0))
PY = TOP + Vector((0.44, 0.02, 0))
pot(PB, BLUE)
pot(PY, YEL)
blue_m = C.mat('pblue', BLUE, rough=0.2, coat=0.9)
yel_m = C.mat('pyel', YEL, rough=0.2, coat=0.9)
mixA = TOP + Vector((-0.1, -0.02, 0.07))
mixB = TOP + Vector((0.1, -0.02, 0.07))
MIX = TOP + Vector((0.0, -0.02, 0.07))
bb = C.sphere('blobb', tuple(mixA), (0.1, 0.1, 0.028), blue_m, None, 24)
yb = C.sphere('bloby', tuple(mixB), (0.1, 0.1, 0.028), yel_m, None, 24)
T.pop_in(bb, 274, (0.1, 0.1, 0.028))
T.pop_in(yb, 312, (0.1, 0.1, 0.028))
for k, f in enumerate(range(380, 424, 4)):
    a = k * 1.1
    rr = 0.06 * (1 - k / 11)
    K(bb, 'location', f, tuple(MIX + Vector((-math.cos(a) * rr, -math.sin(a) * rr, 0))))
    K(yb, 'location', f, tuple(MIX + Vector((math.cos(a) * rr, math.sin(a) * rr, 0))))
K(bb, 'location', 379, tuple(mixA))
K(yb, 'location', 379, tuple(mixB))
anim_color(blue_m, 384, BLUE)
anim_color(blue_m, 418, GREEN)
anim_color(yel_m, 384, YEL)
anim_color(yel_m, 418, GREEN)
K(bb, 'scale', 420, (0.1, 0.1, 0.028))
K(bb, 'scale', 428, (0.14, 0.14, 0.034))
K(yb, 'scale', 420, (0.1, 0.1, 0.028))
K(yb, 'scale', 428, (0.0, 0.0, 0.0))

brush = C.empty('brush', None)
C.tube('bh', [(0, 0, 0.0), (0, 0, 0.36)], 0.014, M((0.95, 0.55, 0.2), rough=0.4, coat=0.6), brush)
C.tube('bf', [(0, 0, -0.01), (0, 0, 0.04)], 0.018, M((0.8, 0.8, 0.85), rough=0.3, coat=0.5), brush)
tip_m = C.mat('btip', (0.96, 0.9, 0.75), rough=0.6)
C.sphere('btip', (0, 0, -0.05), (0.025, 0.025, 0.06), tip_m, brush, 16)
BR0 = TOP + Vector((0.25, -0.12, 0.03))
K(brush, 'location', 0, tuple(BR0))
K(brush, 'rotation_euler', 0, (0, math.radians(88), math.radians(10)))
K(brush, 'location', 250, tuple(BR0))
K(brush, 'rotation_euler', 250, (0, math.radians(88), math.radians(10)))


def bpath(f, p, tilt=20):
    K(brush, 'location', f, tuple(p))
    K(brush, 'rotation_euler', f, (math.radians(-tilt), math.radians(tilt * 0.5), 0))


UP = Vector((0, 0, 0.32))
bpath(258, PB + Vector((0, -0.02, 0.2)) + UP)
bpath(264, PB + Vector((0, -0.02, 0.17)))
anim_color(tip_m, 263, (0.96, 0.9, 0.75))
anim_color(tip_m, 266, BLUE)
bpath(268, PB + UP)
bpath(272, mixA + Vector((0, 0, 0.1)))
bpath(276, mixA + Vector((0, 0, 0.06)))
bpath(282, mixA + UP)
bpath(296, PY + UP)
bpath(302, PY + Vector((0, -0.02, 0.17)))
anim_color(tip_m, 300, BLUE)
anim_color(tip_m, 304, YEL)
bpath(306, PY + UP)
bpath(310, mixB + Vector((0, 0, 0.1)))
bpath(314, mixB + Vector((0, 0, 0.06)))
bpath(320, mixB + UP)
bpath(376, MIX + UP)
for k, f in enumerate(range(380, 424, 4)):
    a = k * 1.1
    bpath(f, MIX + Vector((math.cos(a) * 0.06, math.sin(a) * 0.04, 0.07)), tilt=15)
anim_color(tip_m, 384, YEL)
anim_color(tip_m, 418, GREEN)
bpath(428, MIX + UP)
bpath(520, MIX + UP)

bolita = make('bolita', 1.4)
pimo = make('pimo', 1.7)
B0 = Vector((-1.0, -1.0, Z0))
B1 = Vector((-1.2, -0.5, Z0))
B2 = Vector((-1.35, -0.05, Z0))
P0 = Vector((1.0, -1.0, Z0))
PT = Vector((1.15, -1.3, Z0))
T.place(bolita, 0, B0)
T.turn(bolita, 0, 20)
T.place(pimo, 0, P0)
T.turn(pimo, 0, -20)

feet_m = C.mat('bfeet', RED, rough=0.3, coat=0.5)
fl = bpy.data.objects['Bolita.foot.L']
fr_ = bpy.data.objects['Bolita.foot.R']
for ft_ in (fl, fr_):
    ft_.data.materials[0] = feet_m
anim_color(feet_m, 0, RED)
anim_color(feet_m, 560, RED)
anim_color(feet_m, 584, GREEN)

S(bolita, 14, (1, 1, 1))
for k, f in enumerate(range(16, 40, 6)):
    S(bolita, f, (1.06, 1.06, 0.94) if k % 2 == 0 else (1, 1, 1))
T.turn(bolita, 86, 20)
T.turn(bolita, 94, 55)
T.arm(bolita, 'R', 96, 0, None)
T.arm(bolita, 'R', 102, fwd=-30, out=80)
T.arm(bolita, 'R', 140, fwd=-30, out=80)
T.rest_arm(bolita, 'R', 148)
T.turn(bolita, 150, 55)
T.turn(bolita, 158, 20)

T.turn(pimo, 176, -20)
T.turn(pimo, 182, -60)
C.wave(pimo, 'R', 184, cycles=2, period=8)
hop_to(pimo, 214, P0, PT, 14, apex=0.3)
T.turn(pimo, 228, -60)
T.turn(pimo, 236, -75)
for f in (258, 296):
    T.arm(pimo, 'R', f - 2, 0, None)
    T.arm(pimo, 'R', f + 4, fwd=-50, out=50)
    T.arm(pimo, 'R', f + 22, fwd=-50, out=50)
    T.rest_arm(pimo, 'R', f + 28)
T.turn(pimo, 356, -75)
T.turn(pimo, 364, -30)
for k, f in enumerate(range(380, 424, 8)):
    T.arm(pimo, 'R', f, fwd=-50, out=50 + (15 if k % 2 else -10))
T.rest_arm(pimo, 'R', 430)
T.turn(bolita, 250, 20)
T.turn(bolita, 258, 55)
T.turn(bolita, 424, 55)
T.turn(bolita, 430, 20)
gesture(bolita, 'hops', 434)

EQ = Vector((0.05, -1.6, 2.2))
eq = []
for k, (dx, kind) in enumerate(((-0.72, BLUE), (-0.36, '+'), (0.0, YEL), (0.36, '='), (0.72, GREEN))):
    g = C.empty('eq', None, tuple(EQ + Vector((dx, 0, 0))))
    if isinstance(kind, tuple):
        C.sphere('eqd', (0, 0, 0), (0.15, 0.1, 0.15), C.mat('eqm', kind, rough=0.25, coat=0.9, emit=0.15), g, 32)
    else:
        wm = M((1, 1, 1), rough=0.3, coat=0.6, emit=0.4)
        if kind == '+':
            C.rounded_box('pl1', (0, 0, 0), (0.16, 0.05, 0.05), 0.02, wm, g)
            C.rounded_box('pl2', (0, 0, 0), (0.05, 0.05, 0.16), 0.02, wm, g)
        else:
            C.rounded_box('eq1', (0, 0, 0.045), (0.16, 0.05, 0.045), 0.018, wm, g)
            C.rounded_box('eq2', (0, 0, -0.045), (0.16, 0.05, 0.045), 0.018, wm, g)
    T.pop_in(g, 492 + k * 8 + (6 if k == 4 else 0), 1.0)
    T.pop_out(g, 590, 1.0)

T.turn(bolita, 520, 20)
T.turn(bolita, 528, 0)
T.turn(pimo, 520, -30)
T.turn(pimo, 528, -70)
FT = B0 + Vector((0.0, -0.32, 0.06))
bpath(536, FT + Vector((0.3, 0, 0.35)))
bpath(546, FT + Vector((0.15, -0.02, 0.06)), tilt=35)
for k, f in enumerate(range(550, 586, 4)):
    bpath(f, FT + Vector((0.12 * (1 if k < 4 else -1) + 0.03 * (1 if k % 2 else -1), -0.02, 0.06)), tilt=35)
bpath(592, FT + Vector((0.3, 0, 0.4)))
bpath(606, BR0 + Vector((0, 0, 0.05)))
K(brush, 'rotation_euler', 610, (0, math.radians(88), math.radians(10)))
K(brush, 'location', 610, tuple(BR0))
S(bolita, 556, (1, 1, 1))
S(bolita, 560, (1.05, 1.05, 0.95))
S(bolita, 566, (1, 1, 1))
S(bolita, 572, (1.05, 1.05, 0.95))
S(bolita, 578, (1, 1, 1))
bolita['hold'].location = B0
gesture(bolita, 'bounce', 604)

pm = M(GREEN, rough=0.5, coat=0.3)
sp = 0.17
for k, (pos, f0) in enumerate(((B0, 650), (B1, 676))):
    for sx in (-1, 1):
        o = C.sphere('print', tuple(pos + Vector((sx * sp, -0.06, 0.003))), (1, 1, 1), pm, None, 24)
        T.pop_in(o, f0, (0.085, 0.11, 0.004), d=6)
T.turn(bolita, 640, 0)
T.turn(bolita, 646, 165)
hop_to(bolita, 648, B0, B1, 14, apex=0.35)
hop_to(bolita, 674, B1, B2, 14, apex=0.35)
T.turn(bolita, 692, 165)
T.turn(bolita, 702, 20)
T.turn(bolita, 716, 20)
T.turn(bolita, 724, 30)
T.arm(bolita, 'R', 722, 0, None)
T.arm(bolita, 'R', 728, fwd=-40, out=70)
T.arm(bolita, 'R', 770, fwd=-40, out=70)
T.rest_arm(bolita, 'R', 778)
T.turn(pimo, 640, -70)
T.turn(pimo, 648, -40)
bolita['hold'].location = B2
gesture(bolita, 'hops', 790)
pimo['hold'].location = PT
gesture(pimo, 'bounce', 796)

T.lines(EID, LINES)
T.blinks(bolita, (50, 160, 300, 420, 520, 640, 760))
T.blinks(pimo, (80, 200, 340, 470, 600, 720))
