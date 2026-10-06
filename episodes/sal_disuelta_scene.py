from stage import *
from episodes.sal_disuelta_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'sal_disuelta'
Z0 = 0.08
auto_dress(EID, ENV)
rng = random.Random(21)

W0 = ((0.0, -6.5, 2.05), (0.0, -1.4, 0.8), 31)
WT = ((-0.05, -5.2, 1.8), (-0.05, -1.7, 1.0), 28)
WS = ((-0.6, -3.9, 1.35), (-0.6, -1.9, 0.88), 36)
WC = ((-0.35, -3.25, 1.2), (-0.35, -2.0, 0.9), 40)
camkey(0, WS)
camkey(96, WS)
camkey(110, WT)
camkey(250, WT)
camkey(262, W0)
camkey(286, W0)
camkey(298, WT)
camkey(600, WT)
camkey(640, WC)
camkey(745, WC)
camkey(760, W0)
camkey(TOTAL - 1, W0)

TC = Vector((0.0, -2.0, Z0))
spawn('low_table', 1, 77, 'candy', tuple(TC), 1.0, 0)
TOP = Z0 + 0.62
CUP = Vector((-0.35, -2.0, TOP))
cup = spawn('clear_cup', 1, 31, 'fresh', tuple(CUP), 1.6, 0)
piv = next(o for o in cup.children if o.name.startswith('water_pivot'))
piv.scale = (1, 1, 1)
for o in piv.children:
    o.data.materials.clear()
    o.data.materials.append(MA((0.45, 0.72, 1.0), 0.3, rough=0.05, emit=0.08))
spoon = spawn('big_spoon', 1, 12, 'pastel', (0, 0, 0), 1.4, 0)
for o in spoon.children:
    o.cycles.use_motion_blur = False

salt_m = M((1.0, 1.0, 1.0), rough=0.3, coat=0.6, emit=0.9)
grains = []
SP0 = Vector((CUP.x + 0.2, CUP.y, TOP + 0.58))
BOWL = SP0 + Vector((-0.2, 0, 0.05))
for k in range(12):
    g = C.empty('grain', None, (0, 0, 0))
    gb = C.rounded_box('gb', (0, 0, 0), (0.03, 0.03, 0.03), 0.006, salt_m, g)
    gb.cycles.use_motion_blur = False
    a = k * 2.4
    h = BOWL + Vector((math.cos(a) * 0.02 * (k % 3), math.sin(a) * 0.015 * (k % 3), 0.005 * (k % 2)))
    bot = CUP + Vector((math.cos(a) * 0.05 * (0.4 + (k % 3) * 0.3), math.sin(a) * 0.04, 0.05 + 0.006 * (k % 2)))
    K(g, 'location', 0, tuple(h))
    K(g, 'location', 9 + k % 3, tuple(h))
    K(g, 'location', 22 + k % 3, tuple(bot))
    K(g, 'rotation_euler', 0, (0, 0, a))
    for t, f in enumerate(range(34, 80, 6)):
        ang = a + t * 0.9
        rr = 0.05 * (0.4 + (k % 3) * 0.3) * (1 + 0.15 * t)
        K(g, 'location', f, tuple(CUP + Vector((math.cos(ang) * rr, math.sin(ang) * rr * 0.8, 0.06 + 0.012 * t))))
        K(g, 'rotation_euler', f, (t * 0.7, t * 0.4, ang))
    K(g, 'scale', 0, (1, 1, 1))
    K(g, 'scale', 40 + k * 3, (1, 1, 1))
    K(g, 'scale', 58 + k * 3, (0.001, 0.001, 0.001))
    grains.append(g)

K(spoon, 'location', 0, tuple(SP0))
K(spoon, 'rotation_euler', 0, (0, 0, 0))
K(spoon, 'rotation_euler', 8, (0, 0, 0))
K(spoon, 'rotation_euler', 16, (math.radians(-110), 0, 0))
K(spoon, 'location', 16, tuple(SP0))
STIR = CUP + Vector((0.0, 0.0, 0.34))
K(spoon, 'location', 28, tuple(STIR + Vector((0.04, 0, 0.08))))
K(spoon, 'rotation_euler', 28, (0, math.radians(-75), 0))
for t, f in enumerate(range(32, 96, 4)):
    ang = t * 1.57
    K(spoon, 'location', f, tuple(STIR + Vector((math.cos(ang) * 0.035, math.sin(ang) * 0.03, 0))))
    K(spoon, 'rotation_euler', f, (0, math.radians(-75), math.radians(t * 90)))
K(spoon, 'location', 112, tuple(STIR))
K(spoon, 'rotation_euler', 112, (0, math.radians(-75), math.radians(1440)))
LIFT = Vector((0.32, -2.12, TOP + 0.5))
K(spoon, 'location', 126, tuple(LIFT))
K(spoon, 'rotation_euler', 126, (0, math.radians(-10), math.radians(1440)))
K(spoon, 'rotation_euler', 150, (math.radians(-55), math.radians(-10), math.radians(1440 + 15)))
K(spoon, 'rotation_euler', 175, (math.radians(-55), math.radians(-10), math.radians(1440 - 15)))
K(spoon, 'rotation_euler', 200, (math.radians(-55), math.radians(-10), math.radians(1440)))
K(spoon, 'location', 230, tuple(LIFT))
REST = Vector((0.05, -2.2, TOP + 0.02))
K(spoon, 'location', 244, tuple(REST))
K(spoon, 'rotation_euler', 244, (0, 0, math.radians(1440 + 20)))

torch = spawn('toy_torch', 0, 404, 'pastel', (0, 0, 0), 1.3, 0)
beam = next(o for o in torch.children_recursive if o.name.startswith('beam'))
TP = Vector((-0.5, -2.02, TOP + 0.38))
K(torch, 'location', 0, tuple(TP + Vector((-0.1, 0.1, -0.3))))
K(torch, 'scale', 0, (0, 0, 0))
K(torch, 'scale', 62, (0, 0, 0))
K(torch, 'scale', 70, (1.3, 1.3, 1.3))
K(torch, 'location', 70, tuple(TP))
K(beam, 'scale', 0, (0.001, 0.001, 0.001))
K(beam, 'scale', 74, (0.001, 0.001, 0.001))
K(beam, 'scale', 78, (1, 1, 1))
for f, yaw, pitch in ((74, -8, 22), (88, 8, 26), (102, -6, 24), (116, 4, 22), (132, -2, -8), (150, -6, -6), (170, 2, -8), (196, -4, -6)):
    K(torch, 'rotation_euler', f, (0, math.radians(pitch), math.radians(yaw)))
K(beam, 'scale', 236, (1, 1, 1))
K(beam, 'scale', 240, (0.001, 0.001, 0.001))
K(torch, 'location', 240, tuple(TP))
K(torch, 'rotation_euler', 240, (0, math.radians(-6), math.radians(-4)))
TREST = Vector((0.08, -1.86, TOP + 0.045))
K(torch, 'location', 254, tuple(TREST))
K(torch, 'rotation_euler', 254, (0, 0, math.radians(150)))

glint_m = C.mat('glint', (1, 1, 1), rough=0.2, emit=3.0)
for k in range(5):
    g = C.sphere('glint', (0, 0, 0), (0.008, 0.008, 0.008), glint_m, None, 10)
    p = CUP + Vector((math.cos(k * 1.3) * 0.06, -0.08, 0.12 + 0.05 * (k % 3)))
    g.location = p
    K(g, 'scale', 0, (0, 0, 0))
    for c in range(3):
        f0 = 460 + c * 30 + k * 5
        K(g, 'scale', f0, (0, 0, 0))
        K(g, 'scale', f0 + 5, (1, 1, 1))
        K(g, 'scale', f0 + 11, (0, 0, 0))

PNL = Vector((0.25, -1.5, Z0))
panel = spawn('explain_panel', 0, 58, 'fresh', tuple(PNL), 1.35, 0)
scr = next(o for o in panel.children if o.name.startswith('screen'))
R = 0.34 * 0.82
disc = C.empty('disc', scr, (0, -0.004, 0), (math.radians(90), 0, 0))
C.lathe('wat', [(-0.003, 0.0), (-0.003, R), (0.003, R), (0.003, 0.0)], M((0.55, 0.8, 1.0), rough=0.5, coat=0.2, emit=0.25), disc, segs=64)
wp_m = M((0.3, 0.58, 0.95), rough=0.4, coat=0.4, emit=0.15)
sp_m = M((1.0, 1.0, 1.0), rough=0.3, coat=0.6, emit=0.5)
ring_m = M((0.35, 0.4, 0.5), rough=0.4)
for i in range(-4, 5):
    for j in range(-4, 5):
        x, z = i * 0.06 + (j % 2) * 0.03, j * 0.055
        if x * x + z * z > (R - 0.03) ** 2:
            continue
        C.sphere('wp', (x, -0.012, z), (0.017, 0.006, 0.017), wp_m, scr, 12)
salts = []
for k in range(8):
    o = C.empty('sp', scr, (0, -0.02, 0))
    C.sphere('spb', (0, 0, 0), (0.022, 0.008, 0.022), sp_m, o, 14)
    C.tube('spr', [(math.cos(q * 6.2832 / 20) * 0.024, -0.002, math.sin(q * 6.2832 / 20) * 0.024) for q in range(21)], 0.003, ring_m, o)
    ci = Vector(((k % 3 - 1) * 0.026, 0, (k // 3 - 1) * 0.026))
    a = k * 6.2832 / 8 + 0.3
    dst = Vector((math.cos(a) * R * (0.45 + 0.35 * (k % 2)), 0, math.sin(a) * R * (0.45 + 0.35 * (k % 2))))
    K(o, 'location', 0, tuple(ci + Vector((0, -0.02, 0))))
    K(o, 'location', 352 + k * 2, tuple(ci + Vector((0, -0.02, 0))))
    K(o, 'location', 392 + k * 3, tuple(dst + Vector((0, -0.02, 0))))
    for c, f in enumerate(range(430, 570, 14)):
        K(o, 'location', f, tuple(dst + Vector((0.012 * math.cos(c * 2 + k), -0.02, 0.012 * math.sin(c * 1.7 + k)))))
    salts.append(o)
pen = C.empty('pencil', panel, (0.24, -0.05, 0.95 - 0.27), (0, math.radians(-40), 0))
C.tube('pb', [(0, 0, -0.07), (0, 0, 0.07)], 0.018, M((1.0, 0.75, 0.25), rough=0.4, coat=0.5), pen)
C.lathe('pt', [(0.07, 0.0), (0.07, 0.019), (0.105, 0.0)], M((0.95, 0.85, 0.7), rough=0.6), pen, segs=20)
C.sphere('pe', (0, 0, -0.08), (0.019, 0.019, 0.02), M((0.95, 0.55, 0.65), rough=0.5), pen, 14)
T.pop_in(panel, 276, 1.35, 10)
T.pop_out(panel, 574, 1.35, 8)

zl_m = M((1.0, 1.0, 1.0), rough=0.3, emit=1.0)
for sx in (-1, 1):
    a = CUP + Vector((sx * 0.13, 0, 0.44))
    b = PNL + Vector((sx * 0.3 * 1.35, -0.04, (0.95 - 0.26) * 1.35))
    zl = C.empty('zl', None, tuple(a))
    C.tube('zlt', [(0, 0, 0), tuple(b - a)], 0.006, zl_m, zl)
    K(zl, 'scale', 0, (0, 0, 0))
    K(zl, 'scale', 282, (0, 0, 0))
    K(zl, 'scale', 292, (1, 1, 1))
    K(zl, 'scale', 566, (1, 1, 1))
    K(zl, 'scale', 572, (0, 0, 0))

tag = C.empty('tag', None, (0, 0, 0))
C.rounded_box('card', (0, 0, 0), (0.24, 0.014, 0.1), 0.012, M((1.0, 0.97, 0.88), rough=0.5, coat=0.3), tag)
C.tube('edge', [(math.cos(q * 6.2832 / 40) * 0.11, -0.009, math.sin(q * 6.2832 / 40) * 0.042) for q in range(41)], 0.004, M((0.95, 0.55, 0.3), rough=0.4), tag)
glyph('SAL AQUÍ', 0.05, 0.004, M((0.2, 0.25, 0.45), rough=0.4, coat=0.4), tag, (0, -0.012, -0.002))
STICK = CUP + Vector((0.0, -0.152, 0.2))
K(tag, 'scale', 0, (0, 0, 0))
K(tag, 'scale', 612, (0, 0, 0))
K(tag, 'location', 612, (-0.7, -1.8, TOP + 0.5))
K(tag, 'scale', 620, (1.1, 1.1, 1.1))
K(tag, 'rotation_euler', 612, (0, 0, math.radians(30)))
K(tag, 'location', 640, (-0.42, -2.0, TOP + 0.45))
K(tag, 'rotation_euler', 640, (0, math.radians(-10), math.radians(10)))
K(tag, 'location', 658, tuple(STICK + Vector((0, -0.04, 0.02))))
K(tag, 'location', 664, tuple(STICK))
K(tag, 'rotation_euler', 664, (0, 0, 0))
K(tag, 'scale', 664, (1.0, 1.0, 1.0))
K(tag, 'scale', 668, (1.12, 1.0, 1.12))
K(tag, 'scale', 674, (1.0, 1.0, 1.0))

bopi = make('bopi', 1.45)
ruki = make('ruki', 1.45)
B0 = Vector((-0.95, -1.6, Z0))
T.place(bopi, 0, B0)
T.turn(bopi, 0, 35)
T.arm(bopi, 'R', 0, fwd=-35, out=15)
T.arm(bopi, 'R', 100, fwd=-35, out=15)
T.arm(bopi, 'L', 60, 0, None)
T.arm(bopi, 'L', 68, fwd=-70, out=10)
T.arm(bopi, 'L', 236, fwd=-70, out=10)
T.rest_arm(bopi, 'L', 248)
T.arm(bopi, 'R', 116, fwd=-80, out=20)
T.arm(bopi, 'R', 236, fwd=-80, out=20)
T.rest_arm(bopi, 'R', 246)
for k, f in enumerate(range(80, 112, 8)):
    T.turn(bopi, f, 30 if k % 2 else 42)
T.turn(bopi, 200, 35)
S(bopi, 200, (1, 1, 1))
S(bopi, 206, (1.08, 1.08, 0.9))
S(bopi, 214, (1, 1, 1))
for side in ('L', 'R'):
    T.arm(bopi, side, 250, 0, None)
T.turn(bopi, 262, 20)

ruki_off = Vector((2.5, -1.2, Z0))
R0 = Vector((0.92, -1.74, Z0))
T.place(ruki, 0, ruki_off)
T.place(ruki, 214, ruki_off)
hop_to(ruki, 216, ruki_off, R0, 20, 0.45)
T.turn(ruki, 0, -40)
T.turn(ruki, 240, -30)
T.turn(bopi, 280, 50)
T.turn(ruki, 360, -15)
T.turn(ruki, 440, -45)
gesture(ruki, 'breathe', 540)
T.turn(bopi, 420, 40)
T.turn(bopi, 590, 30)
T.place(bopi, 596, B0)
gesture(bopi, 'bounce', 598)
T.arm(bopi, 'R', 606, 0, None)
T.arm(bopi, 'R', 614, fwd=-90, out=10)
T.arm(bopi, 'R', 650, fwd=-70, out=10)
T.rest_arm(bopi, 'R', 676)
T.turn(bopi, 676, 15)
T.turn(ruki, 676, -20)
T.place(bopi, 740, B0)
T.place(ruki, 740, R0)
gesture(bopi, 'hops', 742)
gesture(ruki, 'bounce', 748)
C.wave(ruki, 'R', 780, cycles=2, period=8)

T.lines(EID, LINES)
T.blinks(bopi, (50, 160, 300, 420, 560, 700))
T.blinks(ruki, (260, 380, 500, 620, 760))
