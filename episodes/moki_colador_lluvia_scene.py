from stage import *
from episodes.moki_colador_lluvia_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, MA, M
EID = 'moki_colador_lluvia'
Z0 = 0.08
auto_dress(EID, ENV)
for l in bpy.data.lights:
    l.energy *= 0.8
sc.world.node_tree.nodes['Background'].inputs[1].default_value = 0.42

W0 = ((0, -7.5, 1.95), (0, -1.1, 1.4), 35)
WC = ((-0.8, -5.7, 2.0), (-0.85, -1.6, 0.8), 36)
WT = ((-0.1, -5.9, 1.6), (-0.1, -1.7, 0.8), 32)
WM = ((-0.65, -6.2, 1.9), (-0.7, -1.1, 1.5), 35)
camkey(0, W0)
camkey(56, W0)
camkey(70, WC)
camkey(116, WC)
camkey(130, W0)
camkey(286, W0)
camkey(300, WT)
camkey(560, WT)
camkey(576, W0)
camkey(650, W0)
camkey(664, WM)
camkey(760, WM)
camkey(774, W0)
camkey(TOTAL - 1, W0)

cloud_m = C.mat('rcloud', (0.86, 0.9, 0.98), rough=0.9, sss=0.2)
cloud = C.empty('rcloud', None, (0, -1.3, 3.35))
for dx, dz, rr in ((0, 0, 0.5), (0.55, -0.05, 0.4), (-0.55, -0.04, 0.42), (1.0, -0.12, 0.3), (-1.0, -0.1, 0.32), (0.25, 0.3, 0.38), (-0.3, 0.28, 0.36)):
    C.sphere('rc', (dx, 0, dz), (rr, rr * 0.75, rr * 0.85), cloud_m, cloud, 28)
for f in range(0, TOTAL, 48):
    K(cloud, 'location', f, (0.08 * math.sin(f / 60), -1.3, 3.35 + 0.04 * math.sin(f / 40)))
cloud.visible_shadow = False
for o in cloud.children:
    o.visible_shadow = False

drop_m = MA((0.45, 0.72, 1.0), 0.8, rough=0.05, emit=0.35)
DROP = (0.022, 0.022, 0.05)


def drop_path(pts, f0, f1, s=DROP):
    o = C.sphere('drop', pts[0], (1, 1, 1), drop_m, None, 12)
    o.visible_shadow = False
    K(o, 'scale', 0, (0, 0, 0))
    K(o, 'scale', f0 - 1, (0, 0, 0))
    K(o, 'scale', f0, s)
    K(o, 'scale', f1, s)
    K(o, 'scale', f1 + 1, (0, 0, 0))
    n = len(pts) - 1
    for k, p in enumerate(pts):
        K(o, 'location', int(f0 + (f1 - f0) * k / n), tuple(p))
    return o


def rain_field(n, xr, yr, f_end, per=16):
    rr = random.Random(5)
    for i in range(n):
        x = rr.uniform(*xr)
        y = rr.uniform(*yr)
        o = C.sphere('rain', (x, y, 3.1), (1, 1, 1), drop_m, None, 10)
        o.visible_shadow = False
        K(o, 'scale', 0, (0, 0, 0))
        f = rr.randint(0, per)
        while f < f_end - per:
            K(o, 'location', f, (x, y, 3.1))
            K(o, 'scale', f, (0, 0, 0))
            K(o, 'scale', f + 1, DROP)
            K(o, 'location', f + per, (x, y, 0.02))
            K(o, 'scale', f + per - 1, DROP)
            K(o, 'scale', f + per, (0, 0, 0))
            f += per + 1
        set_interp(o, 'LINEAR')


rain_field(26, (-1.25, 1.25), (-0.2, 0.6), TOTAL)
rain_field(10, (-1.3, 1.3), (-2.6, -2.3), TOTAL)

moki = make('moki', 1.6)
pimo = make('pimo', 1.75)
M0 = Vector((-0.85, -1.1, Z0))
P0 = Vector((0.95, -1.0, Z0))
PT = Vector((0.88, -1.4, Z0))
T.place(moki, 0, M0)
T.turn(moki, 0, 15)
T.place(pimo, 0, P0)
T.turn(pimo, 0, -20)
bpy.context.view_layer.update()
mbody = moki['body']
top = max((mbody.matrix_world @ Vector(c)).z for c in mbody.bound_box) - Z0
print('MOKITOP', top)

col = spawn('colander', 0, 6201, (0.98, 0.6, 0.45), (0, 0, 0), 1.4, 0)
col.parent = moki['hold']
CHB = Vector((0.0, -0.95, 0.25))
RB = (0, 0, math.radians(127))
K(col, 'location', 0, tuple(CHB))
K(col, 'rotation_euler', 0, RB)
T.arm(moki, 'L', 0, fwd=-60, out=None)
T.arm(moki, 'R', 0, fwd=-60, out=None)
CW = M0 + CHB
C2 = CW
table_m = M((0.98, 0.9, 0.55), rough=0.45, coat=0.5)
TB = Vector((0.25, -1.85, Z0))
C.lathe('table', [(0, 0.0), (0, 0.2), (0.04, 0.22), (0.38, 0.12), (0.42, 0.24), (0.46, 0.25), (0.48, 0.0)], table_m, None, segs=48).location = tuple(TB)
cup = spawn('clear_cup', 0, 6202, (0.55, 0.7, 0.98), tuple(TB + Vector((0, 0, 0.48))), 1.6, 25)
wpiv = next(o for o in cup.children_recursive if o.name.startswith('water_pivot'))
T.pop_in(cup, 246, 1.6)
CUPTOP = TB + Vector((0, 0, 0.48 + 0.2 * 1.6))

for k, f in enumerate(range(14, 108, 7)):
    dx = (k % 3 - 1) * 0.08
    dy = ((k + 1) % 3 - 1) * 0.06
    x, y = CW.x + dx, CW.y + dy
    drop_path([(x, y, 3.0), (x, y, CW.z + 0.15), (x, y, CW.z - 0.02), (x, y, 0.06)], f, f + 22)
for k, f in enumerate(range(252, 336, 7)):
    dx = (k % 3 - 1) * 0.06
    x, y = CUPTOP.x + dx, CUPTOP.y + 0.02 * ((k + 1) % 3 - 1)
    lvl = 0.48 + 0.02 + 0.18 * 1.6 * min(1, (f + 14 - 250) / 90)
    drop_path([(x, y, 3.0), (x, y, TB.z + lvl)], f, f + 14)
for f, z in ((0, 0.001), (262, 0.001), (300, 0.45), (340, 0.75), (420, 0.86), (TOTAL - 1, 0.9)):
    K(wpiv, 'scale', f, (1, 1, z))

for k, f in enumerate(range(130, 250, 9)):
    x, y = CW.x + (k % 3 - 1) * 0.08, CW.y + ((k + 2) % 3 - 1) * 0.06
    drop_path([(x, y, 3.0), (x, y, CW.z + 0.15), (x, y, CW.z - 0.02), (x, y, 0.06)], f, f + 22)
for k, f in enumerate(range(352, 452, 10)):
    x, y = C2.x + (k % 3 - 1) * 0.07, C2.y + ((k + 1) % 3 - 1) * 0.05
    drop_path([(x, y, 3.0), (x, y, C2.z + 0.15), (x, y, C2.z - 0.02), (x, y, 0.06)], f, f + 22)

BIG = (0.045, 0.045, 0.07)
hx, hy = C2.x - 0.05, C2.y
bowl_r = 0.2 * 1.4
drop_path([(hx - 0.2, hy, 2.6), (hx - 0.2, hy, C2.z + bowl_r + 0.02), (hx - 0.12, hy, C2.z + 0.12), (hx - 0.02, hy, C2.z + 0.03)], 452, 474, BIG)
drop_path([(hx - 0.02, hy, C2.z + 0.03), (hx - 0.02, hy, C2.z - 0.01), (hx - 0.02, hy, C2.z - 0.04)], 474, 486, (0.03, 0.03, 0.06))
drop_path([(hx - 0.02, hy, C2.z - 0.04), (hx - 0.02, hy, 0.06)], 486, 498, (0.035, 0.035, 0.06))
ring_m = MA((0.55, 0.78, 1.0), 0.6, emit=0.4)
splash = C.empty('splash', None, (hx - 0.02, hy, 0.04))
C.tube('spl', [(math.cos(a * 6.2832 / 32), math.sin(a * 6.2832 / 32), 0) for a in range(33)], 0.06, ring_m, splash)
K(splash, 'scale', 0, (0, 0, 0))
K(splash, 'scale', 497, (0, 0, 0))
K(splash, 'scale', 499, (0.05, 0.05, 0.3))
K(splash, 'scale', 512, (0.22, 0.22, 0.1))
K(splash, 'scale', 514, (0, 0, 0))

T.turn(moki, 10, 15)
T.turn(moki, 60, 15)
T.turn(moki, 70, 5)
for k, f in enumerate(range(98, 116, 3)):
    K(col, 'rotation_euler', f, (0, math.radians(6 if k % 2 else -6), math.radians(127)))
K(col, 'rotation_euler', 118, RB)
T.turn(moki, 96, 15)
T.turn(moki, 104, 0)
T.turn(moki, 150, 0)
T.turn(moki, 158, 15)
S(moki, 118, (1, 1, 1))
S(moki, 122, (1.06, 1.06, 0.94))
S(moki, 128, (1, 1, 1))
T.blinks(moki, (40, 112, 124))

T.turn(pimo, 168, -20)
T.turn(pimo, 174, -40)
T.arm(pimo, 'R', 174, 0, None)
T.arm(pimo, 'R', 180, fwd=-30, out=80)
T.arm(pimo, 'R', 212, fwd=-30, out=80)
T.rest_arm(pimo, 'R', 220)
T.turn(pimo, 224, -40)
T.turn(pimo, 230, -10)
hop_to(pimo, 232, P0, PT, 12, apex=0.3)
T.turn(pimo, 244, -30)
T.arm(pimo, 'R', 240, 0, None)
T.arm(pimo, 'R', 246, fwd=-55, out=40)
T.arm(pimo, 'R', 256, fwd=-55, out=40)
T.rest_arm(pimo, 'R', 264)
T.turn(pimo, 268, -30)
T.turn(pimo, 276, -60)
T.turn(moki, 236, 15)
T.turn(moki, 246, 35)
T.turn(moki, 334, 35)
T.turn(moki, 340, 10)
gesture(moki, 'breathe', 342)
T.turn(pimo, 400, -60)
T.turn(pimo, 408, -10)
T.turn(pimo, 450, -10)
T.turn(pimo, 456, -55)
T.turn(moki, 446, 10)
T.turn(moki, 454, 25)
T.turn(pimo, 500, -55)
T.turn(pimo, 506, -10)
gesture(pimo, 'hops', 512)

T.turn(moki, 556, 25)
T.turn(moki, 562, 0)
HAT = Vector((0, -0.02, top + 0.2 * 1.4 - 0.07))
T.arm(moki, 'R', 600, fwd=-60, out=None)
T.arm(moki, 'L', 600, fwd=-60, out=None)
T.arm(moki, 'R', 616, fwd=-20, out=150)
T.arm(moki, 'L', 616, fwd=-20, out=150)
T.arm(moki, 'L', 640, fwd=-20, out=150)
T.arm(moki, 'R', 640, fwd=-20, out=150)
T.rest_arm(moki, 'L', 650)
T.rest_arm(moki, 'R', 650)
K(col, 'location', 600, tuple(CHB))
K(col, 'rotation_euler', 600, RB)
K(col, 'location', 612, (0.0, -0.75, top + 0.5))
K(col, 'rotation_euler', 612, (math.radians(100), 0, math.radians(160)))
K(col, 'location', 624, tuple(HAT + Vector((0, 0, 0.18))))
K(col, 'rotation_euler', 624, (math.radians(180), 0, math.radians(200)))
K(col, 'location', 630, tuple(HAT))
K(col, 'location', 636, tuple(HAT + Vector((0, 0, 0.03))))
K(col, 'location', 640, tuple(HAT))
S(moki, 628, (1, 1, 1))
S(moki, 631, (1.08, 1.08, 0.92))
S(moki, 638, (1, 1, 1))
gesture(moki, 'sway', 652)
NOSE = M0 + Vector((0.0, -0.58, 0.83))
drop_path([(NOSE.x, NOSE.y + 0.12, 3.0), (NOSE.x, NOSE.y + 0.12, M0.z + top + 0.32), (NOSE.x, NOSE.y + 0.05, M0.z + top - 0.12)], 684, 700, BIG)
drop_path([(NOSE.x, NOSE.y + 0.05, M0.z + top - 0.12), (NOSE.x, NOSE.y - 0.03, NOSE.z + 0.18), (NOSE.x, NOSE.y - 0.03, NOSE.z)], 700, 708, (0.035, 0.035, 0.05))
S(moki, 707, (1, 1, 1))
S(moki, 710, (0.94, 0.94, 1.08))
S(moki, 716, (1, 1, 1))
T.blinks(moki, (708, 716))
T.blinks(moki, (200, 300, 420, 540, 760))
T.turn(pimo, 690, -10)
T.turn(pimo, 700, -45)
gesture(pimo, 'bounce', 752)
C.wave(pimo, 'R', 780, cycles=2, period=8)
T.lines(EID, LINES)
T.blinks(pimo, (60, 150, 290, 380, 480, 590, 720))
