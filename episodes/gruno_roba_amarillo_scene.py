from stage import *
from episodes.gruno_roba_amarillo_plan import *
import ep_tools as T
from props.basic import potted_flower, flower_head, banana, color_vacuum, anim_color
EID = 'gruno_roba_amarillo'
Z0 = 0.08
YEL = (1.0, 0.78, 0.04)
GREY = (0.42, 0.42, 0.42)
W0 = ((0, -7.3, 1.15), (0, -1.1, 0.95), 37)
camkey(0, ((0, -6.9, 1.15), (0, -1.1, 0.95), 37))
camkey(20, W0)
camkey(204, W0)
camkey(222, ((-0.55, -6.3, 1.15), (-0.55, -1.2, 1.0), 40))
camkey(300, ((-0.55, -6.3, 1.15), (-0.55, -1.2, 1.0), 40))
camkey(318, W0)
camkey(470, W0)
camkey(500, ((0.6, -6.4, 1.2), (0.6, -1.0, 1.05), 40))
camkey(540, ((0.6, -6.4, 1.2), (0.6, -1.0, 1.05), 40))
camkey(560, ((0.25, -6.6, 1.15), (0.25, -1.1, 1.0), 38))
camkey(TOTAL - 1, ((0.25, -6.4, 1.15), (0.25, -1.1, 1.0), 38))

petal_m = C.mat('petal', YEL, rough=0.45, sss=0.1)
ban_m = C.mat('banana', YEL, rough=0.45)
for m in (petal_m, ban_m):
    anim_color(m, 0, YEL)
anim_color(petal_m, 8, YEL)
anim_color(petal_m, 40, GREY)
anim_color(petal_m, 404, GREY)
anim_color(petal_m, 438, YEL)
anim_color(ban_m, 168, YEL)
anim_color(ban_m, 204, GREY)
anim_color(ban_m, 410, GREY)
anim_color(ban_m, 444, YEL)
FL = Vector((-0.45, -1.55, Z0))
fl, fhead = potted_flower('flower', tuple(FL), petal_m)
BA = Vector((0.08, -1.8, Z0))
stool_m = C.mat('stool', (0.95, 0.9, 0.82), rough=0.5, coat=0.2)
C.lathe('stool', [(0.0, 0.0), (0.0, 0.1), (0.16, 0.08), (0.2, 0.16), (0.23, 0.16), (0.23, 0.0)], stool_m, None, segs=48).location = tuple(BA)
ban = banana('banana', None, tuple(BA + Vector((0, 0, 0.28))), ban_m)
ban.rotation_euler = (0, math.radians(-8), math.radians(8))

vac = color_vacuum('vac', (0.0, -0.55, Z0))
aim = C.empty('aim')
dt = vac['arm'].constraints.new('DAMPED_TRACK')
dt.target = aim
dt.track_axis = 'TRACK_NEGATIVE_Y'
P_FL = FL + Vector((0, -0.02, 0.7))
P_BA = BA + Vector((0, 0, 0.33))
K(aim, 'location', 0, tuple(P_FL))
K(aim, 'location', 150, tuple(P_FL))
K(aim, 'location', 164, tuple(P_BA))
K(aim, 'location', 396, tuple(P_BA))
K(aim, 'location', 402, tuple(P_FL))
K(aim, 'location', 420, tuple(P_FL))
K(aim, 'location', 426, tuple(P_BA))
K(aim, 'location', 450, tuple(P_BA))
K(aim, 'location', 470, tuple(Vector((0.0, -1.6, 1.4))))
ARM0 = Vector((0.0, -0.73, Z0 + 0.42))


def tip(p):
    return ARM0 + (p - ARM0).normalized() * 0.5


lvl = vac['level']
for f, z in ((0, 0.001), (8, 0.001), (40, 0.15), (168, 0.15), (204, 0.32), (400, 0.32), (440, 0.1), (446, 0.001)):
    K(lvl, 'scale', f, (1, 1, z))
ball_m = C.mat('yball', (1.0, 0.8, 0.05), rough=0.3, emit=0.6)


def stream(a, b, f0, f1, n=9, arc=0.18):
    for k in range(n):
        o = C.sphere('yb', tuple(a), (1, 1, 1), ball_m, None, 16)
        s0 = f0 + int((f1 - f0 - 12) * k / max(n - 1, 1))
        K(o, 'scale', 0, (0, 0, 0))
        K(o, 'scale', s0 - 1, (0, 0, 0))
        K(o, 'scale', s0 + 2, (0.04, 0.04, 0.04))
        K(o, 'scale', s0 + 11, (0.035, 0.035, 0.035))
        K(o, 'scale', s0 + 13, (0, 0, 0))
        for t in range(0, 13, 2):
            u = t / 12
            p = a.lerp(b, u) + Vector((0, 0, arc * 4 * u * (1 - u)))
            K(o, 'location', s0 + t, tuple(p))


stream(P_FL, tip(P_FL), 8, 42)
stream(P_BA, tip(P_BA), 168, 206)
stream(tip(P_FL), P_FL, 404, 438, n=7)
stream(tip(P_BA), P_BA, 410, 444, n=7)
tank = vac['tank']
K(tank, 'rotation_euler', 0, (0, 0, 0))
K(vac['root'], 'location', 0, (0.0, -0.55, Z0))
for k, f in enumerate(range(206, 262, 4)):
    a = 4 if k % 2 else -4
    K(tank, 'rotation_euler', f, (0, math.radians(a), 0))
K(tank, 'rotation_euler', 262, (0, 0, 0))
for k, f in enumerate(range(340, 404, 3)):
    a = 9 if k % 2 else -9
    K(tank, 'rotation_euler', f, (0, math.radians(a), 0))
    K(vac['root'], 'location', f, (0.03 * (1 if k % 2 else -1), -0.55, Z0 + (0.03 if k % 3 == 0 else 0)))
K(tank, 'rotation_euler', 404, (0, 0, 0))
K(vac['root'], 'location', 404, (0.0, -0.55, Z0))
for f, sc3 in ((442, (1, 1, 1)), (446, (1.25, 1.25, 0.8)), (450, (0.9, 0.9, 1.15)), (456, (1, 1, 1))):
    K(tank, 'scale', f, sc3)

pimo = make('pimo', 1.85)
gruno = make('gruno', 1.9)
PP = Vector((-0.92, -1.0, Z0))
GP = Vector((0.98, -0.9, Z0))
T.place(pimo, 0, PP)
T.turn(pimo, 0, 35)
T.place(gruno, 0, GP)
T.turn(gruno, 0, -35)
T.turn(pimo, 60, 35)
T.turn(pimo, 66, 15)
T.arm(pimo, 'R', 70, 0, None)
T.arm(pimo, 'R', 76, fwd=-30, out=75)
T.arm(pimo, 'R', 110, fwd=-30, out=75)
T.rest_arm(pimo, 'R', 118)
gesture(gruno, 'bounce', 126)
T.turn(pimo, 160, 15)
T.turn(pimo, 168, 30)
T.turn(pimo, 208, 30)
T.turn(pimo, 214, 0)
T.turn(pimo, 286, 0)
T.turn(pimo, 292, 15)
for f, side in ((296, 'R'), (318, 'L')):
    T.arm(pimo, side, f - 2, 0, None)
    T.arm(pimo, side, f + 4, fwd=-35, out=80)
    T.arm(pimo, side, f + 22, fwd=-35, out=80)
    T.rest_arm(pimo, side, f + 30)
gesture(pimo, 'hops', 300)
S(gruno, 346, (1, 1, 1))
for k, f in enumerate(range(350, 396, 6)):
    T.turn(gruno, f, -35 + (8 if k % 2 else -8))
T.turn(gruno, 400, -35)
T.turn(pimo, 330, 15)
T.turn(pimo, 340, 40)

cloud_m = C.mat('ycloud', (1.0, 0.84, 0.25), rough=0.8, sss=0.2, emit=0.15)
cl = C.empty('ycloud')
for dx, dz, r in ((0, 0, 0.22), (0.2, 0.03, 0.17), (-0.2, 0.02, 0.16), (0.07, 0.14, 0.15), (-0.09, 0.12, 0.13)):
    C.sphere('yc', (dx, 0, dz), (r, r * 0.8, r), cloud_m, cl, 24)
C0 = Vector((0.0, -0.55, Z0 + 0.95))
GH = GP + Vector((0, 0, 2.25))
K(cl, 'scale', 0, (0, 0, 0))
K(cl, 'scale', 445, (0, 0, 0))
K(cl, 'scale', 452, (1.25, 1.25, 1.25))
K(cl, 'scale', 458, (1, 1, 1))
K(cl, 'location', 446, tuple(C0))
K(cl, 'location', 470, tuple(GH))
GH2 = Vector((0.82, -0.98, Z0 + 2.25))
for k, f in enumerate(list(range(480, 520, 20)) + list(range(536, TOTAL, 24))):
    base = GH if f < 520 else GH2
    K(cl, 'location', f, tuple(base + Vector((0.04 * (-1) ** k, 0, 0.05 * (-1) ** k))))
for k in range(16):
    o = C.sphere('ydrop', (0, 0, 0), (1, 1, 1), ball_m, None, 12)
    x = GH.x + random.uniform(-0.35, 0.35)
    y = GH.y + random.uniform(-0.2, 0.15)
    f0 = 472 + k * 2
    K(o, 'scale', 0, (0, 0, 0))
    K(o, 'scale', f0 - 1, (0, 0, 0))
    K(o, 'scale', f0, (0.025, 0.025, 0.035))
    K(o, 'location', f0, (x, y, GH.z - 0.15))
    K(o, 'location', f0 + 14, (x, y, GH.z - 0.75))
    K(o, 'scale', f0 + 14, (0.025, 0.025, 0.035))
    K(o, 'scale', f0 + 16, (0, 0, 0))

body = gruno['body']
bpy.context.view_layer.update()
surf = C.Surface(body)
inv = body.matrix_world.inverted()
s = gruno['s']
random.seed(4)
spots = []
tries = 0
while len(spots) < 16 and tries < 400:
    tries += 1
    x = random.uniform(-0.62, 0.62) * s
    z = random.uniform(0.25, 1.35) * s
    if abs(x) < 0.42 * s and 0.62 * s < z < 1.3 * s:
        continue
    p, n = surf.hit(GP.x + x, Z0 + z)
    if p is None:
        continue
    if any((p - q).length < 0.12 for q in spots):
        continue
    spots.append(p)
    lp = inv @ (p + n * 0.01)
    o = C.sphere('yspot', tuple(lp), (1, 1, 1), ball_m, body, 16)
    f0 = 480 + len(spots)
    K(o, 'scale', 0, (0, 0, 0))
    K(o, 'scale', f0, (0, 0, 0))
    K(o, 'scale', f0 + 4, (0.05, 0.05, 0.05))
    K(o, 'scale', f0 + 7, (0.04, 0.04, 0.04))
for f in (482, 500):
    C.blink(gruno, f)
S(gruno, 480, (1, 1, 1))
S(gruno, 484, (1.08, 1.08, 0.92))
S(gruno, 490, (1, 1, 1))
T.turn(gruno, 476, -35)
T.turn(gruno, 486, -10)

P2 = Vector((0.12, -2.15, Z0))
PM = Vector((-0.62, -2.2, Z0))
GP2 = Vector((0.82, -0.98, Z0))
T.place(gruno, 514, GP)
hop_to(gruno, 516, GP, GP2, 14, apex=0.3)
T.place(pimo, 516, PP)
hop_to(pimo, 518, PP, PM, 14, apex=0.45)
hop_to(pimo, 536, PM, P2, 12, apex=0.35)
T.turn(pimo, 516, 35)
T.turn(pimo, 530, 0)
T.turn(pimo, 546, 50)
T.arm(pimo, 'R', 546, 0, None)
T.arm(pimo, 'R', 554, fwd=-55, out=55)
T.arm(pimo, 'R', 600, fwd=-55, out=55)
T.rest_arm(pimo, 'R', 610)
T.turn(pimo, 604, 45)
T.turn(pimo, 612, 20)
T.turn(gruno, 530, -35)
T.turn(gruno, 612, -20)
T.turn(gruno, 640, -20)
T.turn(gruno, 652, -5)
fc = C.mat('pfc', (0.55, 0.28, 0.06), rough=0.6)
ph = flower_head('pflower', None, (0, 0, 0), 0.1, petal_m, fc)
C.tube('pfstem', [(0, 0.01, -0.02), (0, 0.01, -0.28)], 0.013, C.mat('pfs', (0.15, 0.55, 0.18), rough=0.5), ph)
sc.frame_set(620)
bpy.context.view_layer.update()
gg = [o for o in bpy.data.objects if o.name.startswith('Gruno.goggle.') and o.type == 'EMPTY']
top = sum((o.matrix_world.translation for o in gg), Vector()) / len(gg) + Vector((0.02, 0.08, 0.2))
HAND = P2 + Vector((0.48, -0.15, 0.7))
T.pop_in(ph, 548, 1.0)
K(ph, 'location', 0, tuple(HAND))
K(ph, 'location', 600, tuple(HAND))
K(ph, 'rotation_euler', 600, (0, 0, 0))
for f in range(600, 615, 2):
    u = (f - 600) / 14
    K(ph, 'location', f, tuple(HAND.lerp(top, u) + Vector((0, 0, 0.35 * 4 * u * (1 - u)))))
K(ph, 'location', 614, tuple(top))
K(ph, 'rotation_euler', 614, (0, math.radians(-25), 0))
K(ph, 'scale', 606, (1, 1, 1))
K(ph, 'scale', 614, (1.4, 1.4, 1.4))
K(ph, 'scale', 617, (1.7, 1.7, 1.7))
K(ph, 'scale', 621, (1.4, 1.4, 1.4))

T.lines(EID, LINES)
T.blinks(pimo, (50, 150, 260, 380, 470, 590, 690))
T.blinks(gruno, (90, 190, 300, 420, 560, 700))
word3d('AMARILLO', YEL, (0, -1.6, 2.2), 300, 392, size=0.9, max_w=2.0)
