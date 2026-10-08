from stage import *
from episodes.hw26_01_nombre_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, _font
from props.costumes import dress, flat, crescent_pts
from props import halloween as HW
from episodes.hw_look import autumn
EID = 'hw26_01_nombre'
Z0 = 0.08
autumn()
auto_dress(EID, ENV)

W0 = ((0, -5.7, 1.5), (0, -1.1, 0.98), 32)
WC = ((0, -4.0, 1.4), (0, -1.0, 1.2), 50)
camkey(0, W0)
camkey(300, W0)
camkey(318, WC)
camkey(612, WC)
camkey(630, W0)
camkey(TOTAL - 1, W0)

TY = -0.95
table = spawn('low_table', 1, 2601, 'autumn', (0, TY, Z0), 0.9, 0)
TOP = Z0 + 0.62 * 0.9
font = _font()

pimo = make('pimo', 1.3)
bopi = make('bopi', 1.35)
dress(pimo, 'pimo', COSTUME, 0)
dress(bopi, 'bopi', COSTUME, 0)
PP = Vector((-0.88, -1.4, Z0))
BP = Vector((0.88, -1.4, Z0))
T.place(pimo, 0, PP)
T.place(bopi, 0, BP)
T.turn(pimo, 0, 35)
T.turn(bopi, 0, -40)

CY = TY - 0.05
XL, XR = -0.26, 0.26
c31 = spawn('date_card', 2, 3101, 'autumn', (XR, CY, TOP), 1.35, 0, label=("31", "OCT"))
c1 = spawn('date_card', 2, 1101, 'autumn', (XL, CY, TOP), 1.35, 0, label=("1", "NOV"))

hand = BP + Vector((-0.45, 0.05, 0.75))
K(c1, 'location', 0, tuple(hand))
K(c1, 'location', 8, tuple(hand))
K(c1, 'location', 22, (XL, CY, TOP + 0.12))
K(c1, 'location', 28, (XL, CY, TOP))
K(c1, 'rotation_euler', 0, (0, math.radians(-12), 0))
K(c1, 'rotation_euler', 26, (0, 0, 0))
T.arm(bopi, 'R', 0, fwd=-60, out=20)
T.arm(bopi, 'R', 20, fwd=-50, out=30)
T.rest_arm(bopi, 'R', 34)
T.turn(bopi, 34, -40)
T.turn(bopi, 44, -15)

for f, a in ((14, 35), (22, 50), (60, 50), (68, 25)):
    T.turn(pimo, f, a)
K(pimo['spin'], 'rotation_euler', 10, (0, 0, math.radians(35)))
for f, tilt in ((10, 0), (18, 10), (48, 10), (56, 0)):
    K(pimo['sq'], 'rotation_euler', f, (0, math.radians(tilt), 0))

PS = PP + Vector((0.12, 0.3, 0))
hop_to(pimo, 112, PP, PS, 12, apex=0.25)
T.turn(pimo, 110, 25)
T.turn(pimo, 124, 15)
T.arm(pimo, 'R', 124, 0, None)
T.arm(pimo, 'R', 130, fwd=-70, out=20)
for o, a, b, f0, h in ((c1, XL, XR, 136, 0.32), (c31, XR, XL, 150, 0.22)):
    K(o, 'location', f0, (a, CY, TOP))
    for t in range(2, 19, 2):
        u = t / 18
        u = u * u * (3 - 2 * u)
        K(o, 'location', f0 + t, (a + (b - a) * u, CY - 0.12 * math.sin(math.pi * u), TOP + h * math.sin(math.pi * u)))
    K(o, 'location', f0 + 22, (b, CY, TOP))
T.rest_arm(pimo, 'R', 176)
hop_to(pimo, 186, PS, PP, 12, apex=0.25)
T.turn(pimo, 200, 30)
K(c31, 'scale', 196, (1.35, 1.35, 1.35))
K(c31, 'scale', 202, (1.5, 1.5, 1.5))
K(c31, 'scale', 210, (1.35, 1.35, 1.35))

lab_h = HW.card('lab_hw', 'Halloween', font, (XL, CY - 0.26, TOP + 0.06), w=0.44, h=0.12, bg=(0.95, 0.66, 0.3), ink=(0.2, 0.12, 0.24), rot=(math.radians(-14), 0, 0))
T.pop_in(lab_h, 214, 1.0, 10)
lab_s = HW.card('lab_ts', 'Todos los Santos', font, (XR, CY - 0.26, TOP + 0.06), w=0.48, h=0.12, bg=(0.93, 0.9, 0.82), ink=(0.2, 0.12, 0.24), rot=(math.radians(-14), 0, 0))
T.pop_in(lab_s, 420, 1.0, 10)

ZS = TOP + 0.86
moon_m = M((1.0, 0.86, 0.45), rough=0.3, coat=0.5, emit=0.35)
moon = C.empty('moon', None, (XL, CY - 0.02, ZS))
flat('moon_shape', crescent_pts(0.09), 0.03, moon_m, moon, rot=(0, 0, math.radians(25)))
night = C.empty('night', None, (XL, CY + 0.01, ZS - 0.02))
C.sphere('night_disc', (0, 0, 0), (0.15, 0.02, 0.15), M((0.24, 0.24, 0.52), rough=0.5, coat=0.3), night, 32)
for k, (dx, dz) in enumerate(((-0.08, 0.07), (0.09, 0.08), (0.07, -0.08))):
    C.sphere(f'night_star{k}', (dx, -0.025, dz), (0.014, 0.008, 0.014), moon_m, night, 12)
sun_g = C.empty('day', None, (XR, CY, ZS - 0.02))
C.sphere('day_disc', (0, 0, 0), (0.15, 0.02, 0.15), M((0.62, 0.82, 1.0), rough=0.5, coat=0.3), sun_g, 32)
C.sphere('sun_core', (0, -0.025, 0), (0.06, 0.012, 0.06), M((1.0, 0.8, 0.25), rough=0.3, coat=0.5, emit=0.3), sun_g, 24)
for k in range(8):
    a = k * math.pi / 4
    C.sphere(f'sun_ray{k}', (0.095 * math.cos(a), -0.025, 0.095 * math.sin(a)), (0.016, 0.008, 0.016), M((1.0, 0.8, 0.25), rough=0.3, coat=0.5, emit=0.3), sun_g, 10)
T.pop_in(night, 352, 1.0, 10)
T.pop_in(moon, 356, 1.0, 10)
T.pop_in(sun_g, 392, 1.0, 10)
dots = []
for k in range(7):
    u = (k + 1) / 8
    x = XL + (XR - XL) * u
    z = ZS + 0.17 + 0.1 * math.sin(math.pi * u)
    d = C.empty(f'arc{k}', None, (x, CY - 0.03, z))
    C.sphere(f'arcs{k}', (0, 0, 0), (0.022,) * 3, M((0.5, 0.28, 0.52), rough=0.4, coat=0.5), d, 12)
    T.pop_in(d, 440 + k * 5, 1.0, 6)
    dots.append(d)
tip = C.empty('arc_tip', None, (XR - 0.03, CY - 0.03, ZS + 0.15))
for sx in (-1, 1):
    C.tube(f'tip{sx}', [(0, 0, 0), (-0.04, 0, 0.035 * sx)], 0.012, M((0.5, 0.28, 0.52), rough=0.4, coat=0.5), tip)
T.pop_in(tip, 478, 1.0, 6)
banner = HW.card('lab_na', 'la noche de antes', font, (0, CY - 0.03, ZS + 0.36), w=0.62, h=0.13, bg=(0.5, 0.28, 0.52), ink=(1.0, 0.9, 0.7))
T.pop_in(banner, 484, 1.0, 10)
for o in [night, moon, sun_g, tip, banner] + dots:
    T.pop_out(o, 612, 1.0, 8)

T.turn(pimo, 330, 30)
T.turn(pimo, 338, 10)
T.turn(bopi, 330, -15)
T.turn(bopi, 338, -5)
gesture(pimo, 'breathe', 400)
gesture(bopi, 'breathe', 520)
for f, a in ((440, 10), (448, 40), (500, 40), (508, 10)):
    T.turn(pimo, f, a)

BS = BP + Vector((-0.35, 0.15, 0))
hop_to(bopi, 624, BP, BS, 10, apex=0.2)
T.turn(bopi, 622, -15)
T.turn(bopi, 634, -35)
T.arm(bopi, 'R', 632, 0, None)
T.arm(bopi, 'R', 640, fwd=-75, out=25)
K(c1, 'rotation_euler', 640, (0, 0, 0))
K(c1, 'rotation_euler', 654, (0, 0, math.radians(-70)))
K(c1, 'rotation_euler', 660, (0, 0, math.radians(-62)))
K(c1, 'rotation_euler', 672, (0, 0, math.radians(-62)))
T.arm(pimo, 'L', 640, 0, None)
T.arm(pimo, 'L', 646, fwd=-40, out=80)
T.arm(pimo, 'L', 676, fwd=-40, out=80)
T.rest_arm(pimo, 'L', 686)
T.turn(pimo, 636, 10)
T.turn(pimo, 642, 45)
S(pimo, 640, (1, 1, 1))
S(pimo, 644, (1.06, 1.06, 0.94))
S(pimo, 650, (1, 1, 1))
K(c1, 'rotation_euler', 690, (0, 0, math.radians(-62)))
K(c1, 'rotation_euler', 704, (0, 0, math.radians(6)))
K(c1, 'rotation_euler', 710, (0, 0, 0))
T.rest_arm(bopi, 'R', 712)
S(bopi, 704, (1, 1, 1))
S(bopi, 708, (1.08, 1.08, 0.92))
S(bopi, 714, (1, 1, 1))
hop_to(bopi, 722, BS, BP, 10, apex=0.2)
T.turn(bopi, 734, -40)
T.turn(bopi, 744, -10)
T.turn(pimo, 744, 45)
T.turn(pimo, 752, 15)
C.wave(pimo, 'R', 800, cycles=2, period=8)
C.wave(bopi, 'L', 806, cycles=2, period=8)

T.lines(EID, LINES)
T.blinks(pimo, (40, 150, 260, 380, 500, 610, 720, 830))
T.blinks(bopi, (70, 190, 310, 430, 560, 690, 790))
