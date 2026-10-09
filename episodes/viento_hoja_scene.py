from stage import *
from episodes.viento_hoja_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA
EID = 'viento_hoja'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0.0, -6.5, 2.05), (0.0, -1.4, 0.8), 31)
WT = ((0.0, -5.7, 2.6), (0.0, -1.85, 0.82), 29)
WS = ((0.18, -3.9, 2.25), (0.18, -2.0, 0.72), 27)
camkey(0, WT)
camkey(184, WT)
camkey(196, WS)
camkey(340, WS)
camkey(352, WT)
camkey(740, WT)
camkey(756, W0)
camkey(TOTAL - 1, W0)

TC = Vector((0.0, -2.0, Z0))
spawn('low_table', 1, 61, 'candy', tuple(TC), 1.05, 0)
TOP = Z0 + 0.62

paper = M((0.98, 0.97, 0.93), rough=0.7, coat=0.1)
ink = M((0.35, 0.72, 0.42), rough=0.5, coat=0.3)
sheet = C.empty('sheet', None, (0, 0, 0))
C.rounded_box('pg', (0, 0, 0.006), (0.3, 0.22, 0.008), 0.003, paper, sheet)
lp = [(0.11 * math.cos(2 * math.pi * k / 40) * (1 - 0.35 * abs(math.sin(2 * math.pi * k / 40))), 0.07 * math.sin(2 * math.pi * k / 40), 0.012) for k in range(41)]
C.tube('lf', lp, 0.005, ink, sheet)
C.tube('lv', [(-0.13, 0, 0.012), (0.1, 0, 0.012)], 0.004, ink, sheet)
for x in (-0.05, 0.03):
    C.tube('lv', [(x, 0, 0.012), (x + 0.04, 0.04, 0.012)], 0.003, ink, sheet)
    C.tube('lv', [(x, 0, 0.012), (x + 0.04, -0.04, 0.012)], 0.003, ink, sheet)

PX = [0.28, 0.12, -0.06, -0.06, -0.06, -0.22, -0.36]


def scoot(f0, x0, x1, n=3, step=10):
    for k in range(n + 1):
        u = k / n
        x = x0 + (x1 - x0) * u
        f = f0 + k * step
        K(sheet, 'location', f, (x, -2.0, TOP))
        K(sheet, 'rotation_euler', f, (0, 0, math.radians(4 * math.sin(k * 1.7))))
        if k < n:
            K(sheet, 'location', f + step // 2, (x + (x1 - x0) / n * 0.5, -2.0, TOP + 0.03))
            K(sheet, 'rotation_euler', f + step // 2, (0, math.radians(-6), 0))


K(sheet, 'location', 0, (0.3, -2.0, TOP))
scoot(14, 0.3, 0.12, 3, 10)
scoot(70, 0.12, 0.0, 2, 10)
scoot(120, 0.0, -0.08, 2, 10)
K(sheet, 'location', 200, (-0.08, -2.0, TOP))
scoot(282, -0.08, -0.22, 3, 12)
scoot(430, -0.22, -0.34, 3, 12)
K(sheet, 'location', 600, (-0.34, -2.0, TOP))

luma = make('luma', 1.45)
moki = make('moki', 1.4)
LU0 = Vector((1.05, -1.7, Z0))
MO0 = Vector((-1.0, -1.42, Z0))
T.place(luma, 0, LU0)
T.turn(luma, 0, -55)
T.place(moki, 0, MO0)
T.turn(moki, 0, 30)

fan = spawn('hand_fan', 0, 71, 'candy', (0.58, -2.18, TOP - 0.1), 1.25, 0)
fbase = (0, 0, math.radians(38))
fan.rotation_euler = fbase
T.arm(luma, 'R', 0, fwd=-35, out=55)
T.arm(luma, 'L', 0, fwd=-35, out=55)


def wave(f0, f1, amp=26, per=12):
    f = f0
    s = 1
    while f < f1:
        K(fan, 'rotation_euler', f, (math.radians(s * amp), 0, fbase[2]))
        s = -s
        f += per // 2
    K(fan, 'rotation_euler', f1, fbase)


K(fan, 'rotation_euler', 0, fbase)
wave(6, 150, 22, 10)
K(fan, 'rotation_euler', 200, fbase)
K(fan, 'rotation_euler', 262, fbase)
wave(276, 340, 26, 12)
wave(424, 480, 26, 12)

air = MA((1.0, 1.0, 1.0), 0.45, emit=0.6)
streaks = []
for k in range(3):
    o = C.empty('air', None, (0.45, -2.08 - 0.05 * (k - 1), TOP + 0.08 + 0.06 * k))
    pts = [(-0.18 * j / 12, 0, 0.025 * math.sin(j * 0.9 + k)) for j in range(13)]
    C.tube('st', pts, 0.008, air, o)
    o.scale = (0, 0, 0)
    streaks.append(o)


def blow(f0, f1, x0, x1):
    for k, o in enumerate(streaks):
        d = k * 4
        K(o, 'scale', f0 + d - 1, (0, 0, 0))
        K(o, 'scale', f0 + d + 4, (1, 1, 1))
        K(o, 'scale', f1 - 4, (1, 1, 1))
        K(o, 'scale', f1, (0, 0, 0))
        y, z = o.location.y, o.location.z
        K(o, 'location', f0 + d, (x0, y, z))
        K(o, 'location', f1, (x1, y, z))


blow(280, 340, 0.55, 0.0)
blow(350, 410, 0.55, -0.05)
blow(426, 484, 0.5, -0.2)
word3d('¡AIRE!', (0.32, 0.62, 0.98), (0.0, -2.2, 1.32), 356, 414, 0.24, 1.0)

pw = spawn('pinwheel', 1, 81, 'candy', (-0.36, -2.16, TOP), 1.35, -35)
rotor = next(o for o in pw.children_recursive if o.name.startswith('rotor'))
T.pop_in(pw, 600, 1.35, 8)
T.arm(moki, 'R', 596, fwd=-10, out=None)
T.arm(moki, 'R', 606, fwd=-60, out=30)
K(rotor, 'rotation_euler', 0, (math.radians(90), 0, 0))
K(rotor, 'rotation_euler', 690, (math.radians(90), 0, 0))
rotor.rotation_mode = 'XYZ'
K(rotor, 'rotation_euler', 760, (math.radians(90), 0, math.radians(-900)))
K(rotor, 'rotation_euler', TOTAL - 1, (math.radians(90), 0, math.radians(-1200)))
wave(682, TOTAL - 1, 24, 12)

T.turn(moki, 20, 10)
for f, dz in ((24, -0.15), (40, 0.0), (58, -0.15), (74, 0.0)):
    K(moki['spin'], 'rotation_euler', f, (math.radians(-dz * 120), 0, math.radians(10)))
K(moki['spin'], 'rotation_euler', 90, (0, 0, math.radians(10)))
hop_to(moki, 104, MO0, MO0 + Vector((0.18, -0.05, 0)), 12, 0.3)
T.place(moki, 118, MO0 + Vector((0.18, -0.05, 0)))
T.turn(moki, 118, 20)
gesture(moki, 'sway', 140)
T.turn(moki, 186, 45)
T.turn(luma, 186, -40)
T.arm(luma, 'R', 196, fwd=-35, out=55)
T.turn(moki, 300, 25)
T.turn(moki, 420, 30)
gesture(luma, 'breathe', 500)
T.turn(moki, 516, 40)
gesture(moki, 'bounce', 530)
T.turn(moki, 600, 50)
T.turn(luma, 600, -50)
hop_to(moki, 610, MO0 + Vector((0.18, -0.05, 0)), Vector((-0.95, -1.55, Z0)), 14, 0.3)
T.place(moki, 700, Vector((-0.95, -1.55, Z0)))
gesture(moki, 'bounce', 712)
gesture(luma, 'bounce', 716)
confetti(740, (0.0, -1.9, 1.3), 18, 0.8)

T.lines(EID, LINES)
T.blinks(moki, (60, 170, 260, 400, 560, 690))
T.blinks(luma, (90, 230, 380, 520, 650))
