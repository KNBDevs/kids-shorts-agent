from stage import *
from episodes.roce_suelo_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA
EID = 'roce_suelo'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0.0, -6.9, 2.5), (0.0, -1.3, 0.85), 30)
WT = ((0.0, -5.3, 2.45), (0.0, -1.4, 0.62), 31)
WR = ((-0.7, -4.3, 1.9), (0.2, -1.5, 0.45), 31)
camkey(0, WT)
camkey(560, WT)
camkey(572, WR)
camkey(724, WR)
camkey(736, WT)
camkey(770, WT)
camkey(784, W0)
camkey(TOTAL - 1, W0)

YS, YE = -2.45, -0.45
XR, XL = 0.24, -0.24
LY = (YS + YE) / 2 + 0.1
rough = spawn('test_lane', 0, 31, 'candy', (XR, LY, Z0), 1.0, 90, surface='rough')
smooth = spawn('test_lane', 0, 32, 'fresh', (XL, LY, Z0), 1.0, 90, surface='smooth')
ZT = Z0 + 0.03
lr = spawn('push_launcher', 0, 41, 'pastel', (XR, YS - 0.22, ZT), 1.0, 90)
ll = spawn('push_launcher', 0, 42, 'pastel', (XL, YS - 0.22, ZT), 1.0, 90)
pr = next(o for o in lr.children if o.name.startswith('pusher'))
pl = next(o for o in ll.children if o.name.startswith('pusher'))

line_m = M((1.0, 0.85, 0.3), rough=0.3, coat=0.6, emit=0.4)
marks = []
for x in (XR, XL):
    o = C.empty('mark', None, (x, YS + 0.12, ZT + 0.006))
    C.rounded_box('ln', (0, 0, 0), (0.3, 0.03, 0.008), 0.003, line_m, o)
    marks.append(o)

wood = M((0.93, 0.7, 0.42), rough=0.55, coat=0.4)
grain = M((0.78, 0.52, 0.3), rough=0.6, coat=0.2)


def block(name):
    o = C.empty(name, None, (0, 0, 0))
    C.rounded_box('b', (0, 0, 0.08), (0.19, 0.19, 0.16), 0.04, wood, o)
    for z in (0.045, 0.08, 0.115):
        C.tube('g', [(-0.05, -0.081, z), (0.05, -0.081, z + 0.01)], 0.004, grain, o)
    C.sphere('dot', (0.0, -0.081, 0.09), (0.025, 0.004, 0.025), M((0.98, 0.45, 0.45), rough=0.4, coat=0.5), o, 16)
    return o


BR = block('blk_r')
BL = block('blk_l')
Y0 = YS + 0.2
DR, DL = 0.8, 1.72
NR, NL = 16, 36


def slide(o, x, f0, dist, n):
    for k in range(0, n + 1, 2):
        u = k / n
        y = Y0 + dist * (1 - (1 - u) ** 2)
        K(o, 'location', f0 + k, (x, y, ZT))
    K(o, 'location', f0 + n, (x, Y0 + dist, ZT))
    K(o, 'rotation_euler', f0 + n, (0, 0, 0))
    K(o, 'rotation_euler', f0 + n + 3, (math.radians(-4), 0, 0))
    K(o, 'rotation_euler', f0 + n + 7, (0, 0, 0))


def shove(p, f0):
    K(p, 'location', f0 - 6, (0, 0, 0))
    K(p, 'location', f0 - 2, (-0.06, 0, 0))
    K(p, 'location', f0, (0.06, 0, 0))
    K(p, 'location', f0 + 8, (0, 0, 0))


def reset(o, x, f, yc):
    K(o, 'location', f, (x, yc, ZT))
    T.pop_out(o, f, 1.0, 6)
    K(o, 'location', f + 6, (x, Y0, ZT))
    K(o, 'scale', f + 7, (0, 0, 0))
    K(o, 'scale', f + 12, (1.15, 1.15, 1.15))
    K(o, 'scale', f + 16, (1, 1, 1))


K(BR, 'location', 0, (XR, Y0, ZT))
K(BL, 'location', 0, (XL, Y0, ZT))
K(BL, 'scale', 0, (0, 0, 0))
K(BL, 'scale', 120, (0, 0, 0))
K(BL, 'scale', 126, (1.15, 1.15, 1.15))
K(BL, 'scale', 130, (1, 1, 1))
shove(pr, 4)
slide(BR, XR, 4, DR, NR)
K(BR, 'scale', 0, (1, 1, 1))
reset(BR, XR, 110, Y0 + DR)
for o in marks:
    K(o, 'scale', 196, (1, 1, 1))
    for f in (200, 216, 232):
        K(o, 'scale', f, (1.15, 1, 6))
        K(o, 'scale', f + 8, (1, 1, 1))
shove(pl, 256)
slide(BL, XL, 256, DL, NL)
shove(pr, 352)
slide(BR, XR, 352, DR, NR)

flags = []
for x, d, col, sx in ((XL, DL, (0.45, 0.8, 0.98), -1), (XR, DR, (0.98, 0.55, 0.45), 1)):
    o = C.empty('flag', None, (x + sx * 0.24, Y0 + d, ZT))
    C.tube('pole', [(0, 0, 0), (0, 0, 0.36)], 0.012, M((0.96, 0.94, 0.9), rough=0.4), o)
    C.rounded_box('fl', (sx * 0.07, 0, 0.3), (0.14, 0.014, 0.09), 0.01, M(col, rough=0.4, coat=0.5), o)
    flags.append(o)
T.pop_in(flags[0], 300, 1.0, 8)
T.pop_in(flags[1], 372, 1.0, 8)

word3d('¡ROZAN!', (0.98, 0.55, 0.4), (0.0, -1.6, 1.3), 484, 540, 0.24, 1.0)

comb_m = M((0.62, 0.45, 0.92), rough=0.35, coat=0.7)
comb = C.empty('comb', None, (0, 0, 0))
C.rounded_box('spine', (0, 0, 0.1), (0.32, 0.07, 0.06), 0.025, comb_m, comb)
for k in range(9):
    x = -0.13 + k * 0.0325
    C.tube('tooth', [(x, 0, 0.08), (x, 0, 0.0)], 0.009, comb_m, comb)
K(comb, 'scale', 0, (0, 0, 0))
K(comb, 'scale', 640, (0, 0, 0))
K(comb, 'scale', 648, (1.1, 1.1, 1.1))
K(comb, 'scale', 652, (1, 1, 1))
K(comb, 'location', 640, (XR, Y0 + 0.2, ZT + 0.06))
for k in range(4):
    f = 652 + k * 12
    K(comb, 'location', f, (XR, Y0 + 0.15, ZT + 0.03))
    K(comb, 'location', f + 6, (XR, Y0 + 0.9, ZT + 0.03))
    K(comb, 'location', f + 11, (XR, Y0 + 0.9, ZT + 0.12))
K(comb, 'location', 700, (XR + 0.15, Y0 + 0.9, ZT + 0.2))
T.pop_out(comb, 702, 1.0, 6)
reset(BR, XR, 690, Y0 + DR)
shove(pr, 716)
slide(BR, XR, 716, DR, NR)

gruno = make('gruno', 1.5)
bopi = make('bopi', 1.35)
GR0 = Vector((1.05, -1.55, Z0))
GR1 = Vector((0.9, -1.15, Z0))
BO0 = Vector((-0.92, -1.6, Z0))
T.place(gruno, 0, GR0)
T.turn(gruno, 0, -30)
T.place(bopi, 0, BO0)
T.turn(bopi, 0, 25)
for f in (12, 22, 32):
    S(gruno, f, (1.06, 1.06, 0.94))
    S(gruno, f + 5, (1, 1, 1))
T.arm(gruno, 'R', 10, fwd=-60, out=30)
T.arm(gruno, 'R', 40, fwd=-60, out=30)
T.rest_arm(gruno, 'R', 50)
gesture(bopi, 'bounce', 90)
T.arm(bopi, 'R', 110, fwd=-70, out=20)
T.arm(bopi, 'R', 130, fwd=-70, out=20)
T.rest_arm(bopi, 'R', 140)
T.turn(bopi, 190, 15)
T.turn(gruno, 250, -60)
T.turn(gruno, 300, -20)
T.arm(bopi, 'L', 300, fwd=-70, out=30)
T.arm(bopi, 'L', 330, fwd=-70, out=30)
T.rest_arm(bopi, 'L', 340)
T.turn(gruno, 352, -50)
T.turn(gruno, 400, -25)
gesture(bopi, 'breathe', 480)
gesture(gruno, 'sway', 550)
hop_to(gruno, 600, GR0, GR1, 16, 0.35)
T.turn(gruno, 616, -65)
T.arm(gruno, 'R', 640, fwd=-50, out=40)
for k in range(4):
    T.arm(gruno, 'R', 652 + k * 12, fwd=-30, out=50)
    T.arm(gruno, 'R', 658 + k * 12, fwd=-60, out=25)
T.rest_arm(gruno, 'R', 704)
T.turn(gruno, 712, -20)
T.turn(gruno, 760, 0)
S(gruno, 744, (1, 1, 1))
S(gruno, 750, (1.05, 1.05, 0.92))
S(gruno, 758, (1, 1, 1))
gesture(bopi, 'bounce', 760)

T.lines(EID, LINES)
T.blinks(gruno, (60, 180, 330, 470, 620, 770))
T.blinks(bopi, (80, 230, 360, 520, 690))
