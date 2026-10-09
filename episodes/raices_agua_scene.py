from stage import *
from episodes.raices_agua_plan import *
import ep_tools as T
import random
from props import lib
from props.lib import spawn, auto_dress, M, MA
EID = 'raices_agua'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0.0, -6.4, 2.1), (0.0, -1.5, 0.8), 31)
WT = ((0.0, -5.2, 2.0), (0.0, -1.8, 0.75), 30)
WP = ((0.0, -4.0, 1.5), (0.0, -2.0, 0.86), 30)
camkey(0, WT)
camkey(180, WT)
camkey(192, WP)
camkey(540, WP)
camkey(552, WT)
camkey(760, WT)
camkey(776, W0)
camkey(TOTAL - 1, W0)

spawn('low_table', 1, 301, 'pastel', (0.0, -2.0, Z0), 0.85, 0)
TOP = Z0 + 0.62 * 0.85
PC = Vector((0.05, -2.05, TOP))
pr = C.empty('pot', None, tuple(PC))
pr.scale = (1.15, 1.15, 1.15)
pot = lib.cutaway_pot(random.Random(31), 0, 'candy', pr)
front, cut, roots, plant = pot['front'], pot['cut'], pot['roots'], pot['plant']
HT = pot['top'] * 1.15

K(cut, 'scale', 0, (0, 0, 0))
K(cut, 'scale', 196, (0, 0, 0))
K(cut, 'scale', 200, (1, 1, 1))
K(front, 'location', 196, (0, 0, 0))
K(front, 'location', 206, (0, -0.35, 0))
K(front, 'scale', 202, (1, 1, 1))
K(front, 'scale', 208, (0, 0, 0))
K(front, 'scale', 640, (0, 0, 0))
K(front, 'location', 640, (0, -0.35, 0))
K(front, 'scale', 646, (1, 1, 1))
K(front, 'location', 654, (0, 0, 0))

dash_m = M((0.35, 0.55, 0.95), rough=0.4, coat=0.5, emit=0.3)
frame = C.empty('illus', None, (PC.x, PC.y - 0.2, PC.z + 0.24))
W_, H_ = 0.5, 0.56
pts = [(-W_ / 2, -H_ / 2), (W_ / 2, -H_ / 2), (W_ / 2, H_ / 2), (-W_ / 2, H_ / 2)]
for i in range(4):
    a, b = Vector((*pts[i], 0)), Vector((*pts[(i + 1) % 4], 0))
    for k in range(6):
        u0, u1 = k / 6 + 0.02, k / 6 + 0.11
        p0, p1 = a.lerp(b, u0), a.lerp(b, u1)
        C.tube('ds', [(p0.x, 0, p0.y), (p1.x, 0, p1.y)], 0.008, dash_m, frame)
pen = C.empty('pen', frame, (W_ / 2 - 0.02, -0.01, H_ / 2 - 0.02), (0, math.radians(-40), 0))
C.tube('pb', [(0, 0, 0), (0, 0, 0.12)], 0.016, M((1.0, 0.8, 0.3), rough=0.4, coat=0.5), pen)
C.tube('pt', [(0, 0, 0), (0, 0, -0.03)], 0.008, M((0.3, 0.3, 0.36), rough=0.5), pen)
T.pop_in(frame, 204, 1.0, 8)
T.pop_out(frame, 632, 1.0, 6)

drop_m = MA((0.3, 0.6, 1.0), 0.85, rough=0.05, emit=0.35)
rr = random.Random(7)
for k in range(9):
    d = C.empty('dr', None, (0, 0, 0))
    C.sphere('d', (0, 0, 0), (0.016, 0.016, 0.022), drop_m, d, 12)
    f0 = 384 + k * 9
    x = PC.x + rr.uniform(-0.12, 0.12)
    y = PC.y - 0.012 * 1.15 - 0.01
    z0, z1 = PC.z + HT - 0.04, PC.z + HT - 0.25 + rr.uniform(-0.04, 0.04)
    K(d, 'scale', 0, (0, 0, 0))
    K(d, 'scale', f0 - 1, (0, 0, 0))
    K(d, 'scale', f0, (1, 1, 1))
    K(d, 'location', f0, (x, y, z0))
    K(d, 'location', f0 + 30, (x * 0.4 + PC.x * 0.6, y, z1))
    K(d, 'scale', f0 + 30, (1, 1, 1))
    K(d, 'scale', f0 + 36, (0, 0, 0))
arrow_m = M((0.3, 0.6, 1.0), rough=0.3, coat=0.6, emit=0.4)
arrows = []
for k in range(2):
    o = C.empty('arr', None, (PC.x + (0.05 if k else -0.05), PC.y - 0.03, PC.z + HT - 0.2))
    C.tube('sh', [(0, 0, 0), (0, 0, 0.1)], 0.01, arrow_m, o)
    C.tube('hd', [(-0.025, 0, 0.075), (0, 0, 0.105), (0.025, 0, 0.075)], 0.01, arrow_m, o)
    arrows.append(o)
    T.pop_in(o, 450 + k * 6, 1.0, 6)
    K(o, 'location', 456 + k * 6, tuple(o.location))
    K(o, 'location', 520, tuple(o.location + Vector((0, 0, 0.1))))
    T.pop_out(o, 532, 1.0, 6)
for f in (564, 584, 604):
    K(roots, 'scale', f, (1, 1, 1))
    K(roots, 'scale', f + 8, (1.12, 1.12, 1.12))
    K(roots, 'scale', f + 16, (1, 1, 1))

soilw = C.empty('soilw', None, (PC.x, PC.y, PC.z + HT - 0.032))
C.sphere('sw', (0, 0, 0), (0.2, 0.2, 0.012), MA((0.35, 0.28, 0.24), 0.0 + 1.0, rough=0.3), soilw, 32)
K(soilw, 'scale', 0, (0, 0, 0))
K(soilw, 'scale', 300, (0, 0, 0))
K(soilw, 'scale', 330, (1, 1, 1))
K(soilw, 'scale', 600, (1, 1, 1))
K(soilw, 'scale', 680, (0.6, 0.6, 1))

can = spawn('watering_can', 2, 302, 'fresh', (0, 0, 0), 1.0, 0)
tip = next(o for o in can.children if o.name.startswith('tip'))
stream = C.empty('stream', tip, (0, 0, 0))
C.tube('st', [(0, 0, 0), (0.03, 0, -0.06), (0.04, 0, -0.18)], 0.012, MA((0.4, 0.7, 1.0), 0.7, emit=0.2), stream)
K(stream, 'scale', 0, (0, 0, 0))
CN0 = Vector((-0.55, -2.3, TOP + 0.35))
CN1 = Vector((-0.4, -2.08, PC.z + HT + 0.16))
T.pop_in(can, 270, 1.0, 8)
K(can, 'location', 270, tuple(CN0))
K(can, 'location', 290, tuple(CN1))
K(can, 'rotation_euler', 290, (0, 0, 0))
K(can, 'rotation_euler', 300, (0, math.radians(30), 0))
K(stream, 'scale', 299, (0, 0, 0))
K(stream, 'scale', 304, (1, 1, 1))
K(stream, 'scale', 334, (1, 1, 1))
K(stream, 'scale', 338, (0, 0, 0))
K(can, 'rotation_euler', 338, (0, math.radians(30), 0))
K(can, 'rotation_euler', 348, (0, 0, 0))
K(can, 'location', 348, tuple(CN1))
CN2 = Vector((0.42, -2.0, TOP))
K(can, 'location', 700, tuple(CN1))
for k in range(0, 17, 2):
    u = k / 16
    p = CN1.lerp(CN2, u)
    p.z += 0.15 * 4 * u * (1 - u)
    K(can, 'location', 700 + k, tuple(p))

cup = spawn('clear_cup', 0, 303, 'candy', (-0.32, -1.98, TOP), 1.1, 0)
cpiv = next(o for o in cup.children if o.name.startswith('water_pivot'))
cpiv.scale = (1, 1, 1)
straw = C.empty('straw', None, (0, 0, 0))
C.tube('s', [(0, 0, 0), (0, 0, 0.26), (0.05, 0, 0.32)], 0.012, M((0.98, 0.5, 0.55), rough=0.4, coat=0.6), straw)
T.pop_in(cup, 14, 1.1, 8)
T.pop_in(straw, 30, 1.0, 6)
SW0 = Vector((-0.32, -1.98, TOP + 0.04))
K(straw, 'location', 30, tuple(SW0))
K(straw, 'location', 690, tuple(SW0))
K(straw, 'location', 704, (-0.62, -1.9, TOP + 0.45))
K(straw, 'rotation_euler', 704, (0, math.radians(-20), 0))

lf = [o for o in plant.children if o.name.startswith('lf')]
for f in range(110, 180, 14):
    for o in lf:
        r0 = tuple(o.rotation_euler)
        K(o, 'rotation_euler', f, r0)
        K(o, 'rotation_euler', f + 7, (r0[0] + math.radians(6), r0[1], r0[2]))
K(plant, 'rotation_euler', 0, (0, 0, 0))

moki = make('moki', 1.3)
pimo = make('pimo', 1.3)
MO0 = Vector((-0.98, -1.45, Z0))
PI0 = Vector((0.95, -1.45, Z0))
T.place(moki, 0, MO0)
T.turn(moki, 0, 30)
T.place(pimo, 0, PI0)
T.turn(pimo, 0, -30)
T.arm(moki, 'R', 10, fwd=-70, out=20)
T.arm(moki, 'R', 40, fwd=-70, out=20)
T.rest_arm(moki, 'R', 50)
gesture(moki, 'sway', 112)
T.turn(pimo, 186, -45)
T.arm(pimo, 'L', 266, fwd=-70, out=25)
T.arm(pimo, 'L', 344, fwd=-70, out=25)
T.rest_arm(pimo, 'L', 354)
T.arm(pimo, 'L', 372, fwd=-50, out=40)
T.arm(pimo, 'L', 420, fwd=-50, out=40)
T.rest_arm(pimo, 'L', 430)
gesture(pimo, 'breathe', 480)
T.turn(moki, 556, 45)
gesture(moki, 'bounce', 600)
T.arm(moki, 'R', 686, fwd=-80, out=20)
T.arm(moki, 'R', 712, fwd=-80, out=20)
T.rest_arm(moki, 'R', 722)
gesture(moki, 'bounce', 740)
gesture(pimo, 'bounce', 746)

T.lines(EID, LINES)
T.blinks(moki, (60, 170, 300, 440, 590, 720))
T.blinks(pimo, (90, 240, 400, 520, 660, 780))
