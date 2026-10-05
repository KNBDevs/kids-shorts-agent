from stage import *
from episodes.mitades_merienda_plan import *
import ep_tools as T
import bmesh
from props.lib import spawn, auto_dress, M
EID = 'mitades_merienda'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0, -7.0, 1.4), (0, -1.15, 1.05), 37)
WA = ((0, -4.6, 1.3), (0, -1.75, 0.75), 40)
camkey(0, W0)
camkey(116, W0)
camkey(132, WA)
camkey(350, WA)
camkey(366, W0)
camkey(TOTAL - 1, W0)

TB = Vector((0.0, -1.8, Z0))
TH = 0.44
tab_m = M((0.98, 0.88, 0.72), rough=0.45, coat=0.4)
C.lathe('tabletop', [(TH - 0.06, 0.0), (TH - 0.06, 0.68), (TH - 0.03, 0.7), (TH, 0.68), (TH, 0.0)], tab_m, None, segs=64, sy=0.62).location = tuple(TB)
C.lathe('tablestem', [(0, 0.0), (0, 0.22), (0.04, 0.2), (0.08, 0.07), (TH - 0.06, 0.06), (TH - 0.06, 0.0)], M((0.55, 0.78, 0.95), rough=0.4, coat=0.5), None, segs=40).location = tuple(TB)
TOP = TB + Vector((0, 0, TH))
plL = spawn('snack_plate', 0, 7701, (0.95, 0.5, 0.6), tuple(TOP + Vector((-0.45, 0.0, 0))), 0.9, 0)
plR = spawn('snack_plate', 0, 7702, (0.4, 0.7, 0.95), tuple(TOP + Vector((0.45, 0.0, 0))), 0.9, 0)
board = C.rounded_box('board', tuple(TOP + Vector((0, 0.0, 0.015))), (0.34, 0.24, 0.03), 0.012, M((0.9, 0.7, 0.45), rough=0.6), None)

skin_m = M((0.88, 0.12, 0.12), rough=0.35, coat=0.6)
flesh_m = M((0.99, 0.93, 0.72), rough=0.6, coat=0.1)
seed_m = M((0.3, 0.16, 0.08), rough=0.4, coat=0.5)
AR = 0.15


def apple_half(name, side):
    g = C.empty(name)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=40, v_segments=24, radius=AR)
    for v in bm.verts:
        v.co.z *= 0.92
        v.co.z += 0.012 * (1 - (v.co.x ** 2 + v.co.y ** 2) / AR ** 2) * (1 if v.co.z > 0 else 0)
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(0, 0, 0), plane_no=(side, 0, 0), clear_inner=True)
    o = C.mesh_obj(name + '.m', bm, skin_m, g)
    C.sphere(name + '.cut', (0, 0, 0), (0.003, AR * 0.97, AR * 0.9), flesh_m, g, 40)
    C.sphere(name + '.core', (-side * 0.003, 0, 0), (0.002, AR * 0.3, AR * 0.32), M((0.97, 0.86, 0.6), rough=0.6), g, 24)
    for k in range(5):
        a = k * 1.2566 + 1.5708
        C.sphere('seed', (-side * 0.0045, math.cos(a) * 0.035, math.sin(a) * 0.035), (0.004, 0.012, 0.02), seed_m, g, 10, rot=(-a + 1.5708, 0, 0))
    if side < 0:
        C.tube('stem', [(-0.012, 0, AR * 0.92 + 0.0), (-0.02, 0, AR * 0.92 + 0.07)], 0.009, M((0.4, 0.25, 0.12), rough=0.6), g)
        C.sphere('leaf', (-0.04, 0, AR * 0.92 + 0.06), (0.035, 0.012, 0.018), M((0.3, 0.7, 0.3), rough=0.5), g, 16, rot=(0, math.radians(25), 0))
    return g


AZ = TOP + Vector((0, 0, 0.03 + AR * 0.92))
hl = apple_half('halfL', -1)
hr = apple_half('halfR', 1)
for h, side in ((hl, -1), (hr, 1)):
    K(h, 'location', 0, tuple(AZ))
    K(h, 'rotation_euler', 0, (0, 0, 0))
    K(h, 'location', 128, tuple(AZ))
    K(h, 'rotation_euler', 128, (0, 0, 0))
    K(h, 'location', 140, tuple(AZ + Vector((side * 0.09, 0, 0.03))))
    K(h, 'location', 150, tuple(AZ + Vector((side * 0.16, 0, 0))))
    K(h, 'rotation_euler', 150, (0, 0, math.radians(-90 if side < 0 else 90)))
SL = AZ + Vector((-0.17, -0.02, 0))
SR = AZ + Vector((0.17, -0.02, 0))
K(hl, 'location', 228, tuple(SL))
K(hr, 'location', 228, tuple(SR))
K(hl, 'location', 240, tuple(SL + Vector((0.17, 0.12, 0.12))))
K(hl, 'location', 252, tuple(SR + Vector((0, 0.02, 0))))
K(hl, 'location', 272, tuple(SR + Vector((0, 0.02, 0))))
K(hl, 'location', 284, tuple(SL + Vector((0.0, 0.1, 0.1))))
K(hl, 'location', 292, tuple(SL))
for f, sc3 in ((294, 1.0), (298, 1.12), (304, 1.0)):
    K(hl, 'scale', f, (sc3,) * 3)
    K(hr, 'scale', f, (sc3,) * 3)
eq = C.empty('eqs', None, tuple(AZ + Vector((0, -0.05, 0.02))))
wm = M((1, 1, 1), rough=0.3, coat=0.6, emit=0.5)
C.rounded_box('eq1', (0, 0, 0.03), (0.08, 0.02, 0.022), 0.008, wm, eq)
C.rounded_box('eq2', (0, 0, -0.03), (0.08, 0.02, 0.022), 0.008, wm, eq)
T.pop_in(eq, 296, 1.0)
T.pop_out(eq, 356, 1.0)
PL = TOP + Vector((-0.45, 0, 0.03 + AR * 0.92))
PR = TOP + Vector((0.45, 0, 0.03 + AR * 0.92))


def arc_move(o, a, b, f0, f1, h=0.25):
    for f in range(f0, f1 + 1, 2):
        u = (f - f0) / (f1 - f0)
        u = u * u * (3 - 2 * u)
        K(o, 'location', f, tuple(a.lerp(b, u) + Vector((0, 0, h * 4 * u * (1 - u)))))


arc_move(hl, SL, PL, 368, 384)
arc_move(hr, SR, PR, 400, 416)
K(board, 'scale', 418, tuple(board.scale))
K(board, 'scale', 426, (0, 0, 0))

for pl, h, a, b in ((plL, hl, -0.45, 0.45), (plR, hr, 0.45, -0.45)):
    dy = -0.18 if a < 0 else 0.18
    pa = TOP + Vector((a, 0, 0))
    pb = TOP + Vector((b, 0, 0))
    for f in range(576, 609, 4):
        u = (f - 576) / 32
        u = u * u * (3 - 2 * u)
        p = pa.lerp(pb, u) + Vector((0, dy * 4 * u * (1 - u), 0))
        K(pl, 'location', f, tuple(p))
        K(h, 'location', f, tuple(p + Vector((0, 0, 0.03 + AR * 0.92))))
    K(pl, 'location', 570, tuple(pa))
    K(h, 'location', 570, tuple(pa + Vector((0, 0, 0.03 + AR * 0.92))))

pimo = make('pimo', 1.65)
tuki = make('tuki', 1.4)
ruki = make('ruki', 1.4)
P0 = Vector((-1.0, -1.25, Z0))
T0 = Vector((1.0, -1.25, Z0))
R0 = Vector((0.0, -0.45, Z0))
T.place(pimo, 0, P0)
T.place(tuki, 0, T0)
T.place(ruki, 0, R0)
T.turn(pimo, 0, 30)
T.turn(tuki, 0, -30)
T.turn(ruki, 0, 0)

T.turn(pimo, 8, 30)
T.turn(pimo, 14, 60)
T.arm(pimo, 'R', 12, 0, None)
T.arm(pimo, 'R', 18, fwd=-50, out=60)
T.arm(pimo, 'R', 90, fwd=-50, out=60)
T.rest_arm(pimo, 'R', 98)
T.turn(tuki, 46, -30)
T.turn(tuki, 52, -60)
T.arm(tuki, 'L', 50, 0, None)
T.arm(tuki, 'L', 56, fwd=-50, out=60)
T.arm(tuki, 'L', 90, fwd=-50, out=60)
T.rest_arm(tuki, 'L', 98)
for ch, sgn in ((pimo, 1), (tuki, -1)):
    K(ch['hold'], 'location', 20 if ch is pimo else 56, tuple(P0 if ch is pimo else T0))
    K(ch['hold'], 'location', 30 if ch is pimo else 64, tuple((P0 if ch is pimo else T0) + Vector((sgn * 0.08, -0.03, 0))))
    K(ch['hold'], 'location', 96, tuple((P0 if ch is pimo else T0) + Vector((sgn * 0.08, -0.03, 0))))
    K(ch['hold'], 'location', 106, tuple(P0 if ch is pimo else T0))
C.wave(ruki, 'R', 112, cycles=2, period=8)
gesture(ruki, 'breathe', 200)
T.turn(pimo, 120, 60)
T.turn(pimo, 128, 30)
T.turn(tuki, 120, -60)
T.turn(tuki, 128, -30)
T.arm(ruki, 'L', 362, 0, None)
T.arm(ruki, 'L', 368, fwd=-30, out=70)
T.arm(ruki, 'L', 386, fwd=-30, out=70)
T.rest_arm(ruki, 'L', 392)
T.arm(ruki, 'R', 394, 0, None)
T.arm(ruki, 'R', 400, fwd=-30, out=70)
T.arm(ruki, 'R', 418, fwd=-30, out=70)
T.rest_arm(ruki, 'R', 424)
pimo['hold'].location = P0
gesture(pimo, 'hops', 452)
tuki['hold'].location = T0
gesture(tuki, 'hops', 492)
T.turn(pimo, 556, 30)
T.turn(pimo, 562, 50)
C.wave(pimo, 'R', 560, cycles=2, period=8)
T.turn(tuki, 620, -30)
T.turn(tuki, 626, -10)
gesture(tuki, 'bounce', 644)
gesture(pimo, 'bounce', 660)
ruki['hold'].location = R0
gesture(ruki, 'hops', 680)

T.lines(EID, LINES)
T.blinks(pimo, (60, 180, 300, 420, 540, 700))
T.blinks(tuki, (90, 210, 330, 470, 600, 730))
T.blinks(ruki, (40, 160, 260, 380, 520, 640))
