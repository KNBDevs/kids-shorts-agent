from stage import *
from episodes.bopi_rueda_cuadrada_plan import *
import ep_tools as T
from props.basic import cart, wheel, apple, shake_cup, disc
EID = 'bopi_rueda_cuadrada'
T.hide_stage()
G = GROUND
C.rounded_box('path', (0, -4.0, -0.0), (18, 8.2, 0.04), 0.015, C.mat('path', (0.6, 0.42, 0.27), rough=0.85), None)
W0 = (-8.4, 1.3, -1.1, 0.95, 42)
CAM = [(0, -2.0) + W0, (74, -1.45) + W0, (84, -1.0) + W0, (222, -1.0) + W0, (300, -0.45) + W0, (330, -0.3) + W0,
       (436, -0.3) + W0, (452, 0.4, -7.4, 1.25, -1.6, 1.0, 42), (510, 0.4, -7.4, 1.25, -1.6, 1.0, 42),
       (530, -0.2) + W0, (546, -0.2) + W0, (630, 0.85) + W0, (680, 2.25) + W0, (736, 2.25) + W0,
       (754, 2.85, -6.4, 1.25, -1.2, 1.05, 45), (TOTAL - 1, 2.85, -6.4, 1.25, -1.2, 1.05, 45)]
for f, cx, cy, cz, ty, tz, lens in CAM:
    camkey(f, ((cx, cy, cz), (cx, ty, tz), lens))


def cam_x(f):
    for a, b in zip(CAM, CAM[1:]):
        if a[0] <= f <= b[0]:
            u = (f - a[0]) / max(b[0] - a[0], 1)
            return a[1] + (b[1] - a[1]) * u
    return CAM[-1][1]


hub = C.mat('hub', (0.95, 0.95, 0.9), rough=0.4)
col = {4: C.mat('w_sq', (0.95, 0.42, 0.05), rough=0.35, coat=0.4), 3: C.mat('w_tri', (0.9, 0.2, 0.55), rough=0.35, coat=0.4),
       0: C.mat('w_ci', (1.0, 0.78, 0.08), rough=0.35, coat=0.4)}
cA, handle = cart('cartA', (0.25, 0.6, 0.95), None)
W = {}
for n in (4, 3, 0):
    W[n] = [wheel(f'wA{n}{i}', n, WHEEL[n], cA, (sx * 0.3, sy * 0.33, 0), col[n], hub) for i, (sx, sy) in enumerate(((-1, -1), (1, -1), (-1, 1), (1, 1)))]
for w in W[4]:
    T.pop_out(w, 196)
for w in W[3]:
    T.pop_in(w, 204)
    T.pop_out(w, 428)
for w in W[0]:
    T.pop_in(w, 436)
ap = apple('apple', cA, (0.12, 0.02, 0.305))

bopi = make('bopi', 1.55)
ruki = make('ruki', 1.55)
gruno = make('gruno', 1.65)


def drive(root, wheels, name, follower=None, fx=-0.85, fy=0.0, hop=0.0, item=None, ws=1):
    f0, f1, n, x0, d, sgn = SEGS[name]
    prev = 0
    for f in range(f0, f1 + 1):
        x, z, th, k = seg_at(name, f)
        K(root, 'location', f, (x, LANE, G + z))
        for w in wheels:
            K(w, 'rotation_euler', f, (0, ws * th, 0))
        if follower and (f - f0) % 2 == 0:
            bob = 0.05 * abs(math.sin((f - f0) * math.pi / 9))
            T.place(follower, f, (x + fx, LANE + fy, G + bob))
        if k > prev and item is not None and hop:
            base = item.location.z if item.get('base') is None else item['base']
            item['base'] = base
            K(item, 'location', f - 1, (item.location.x, item.location.y, base))
            K(item, 'location', f + 4, (item.location.x, item.location.y, base + hop))
            K(item, 'location', f + 9, (item.location.x, item.location.y, base))
            K(item, 'rotation_euler', f + 4, (0, math.radians(14 * (-1) ** k), 0))
            K(item, 'rotation_euler', f + 10, (0, 0, 0))
        prev = k


K(ap, 'location', 0, tuple(ap.location))
K(ap, 'rotation_euler', 0, (0, 0, 0))
x, z, _, _ = seg_at('A', 0)
K(cA, 'location', 0, (x, LANE, G + z))
T.place(bopi, 0, (x - 0.85, LANE, G))
T.turn(bopi, 0, 55)
for s in 'LR':
    T.arm(bopi, s, 0, fwd=-70, out=12)
drive(cA, W[4], 'A', bopi, hop=0.1, item=ap)
T.turn(bopi, 80, 55)
T.turn(bopi, 90, 20)
for s in 'LR':
    T.arm(bopi, s, 80, fwd=-70, out=12)
    T.rest_arm(bopi, s, 90)
xa, za, _, _ = seg_at('A', 74)
xb, zb, _, _ = seg_at('B', 222)
K(cA, 'location', 196, (xa, LANE, G + za))
K(cA, 'location', 206, (xb, LANE, G + zb))
bx = xa - 0.85
for k, f in enumerate((180, 186, 192)):
    T.place(bopi, f, (bx, LANE, G))
    T.place(bopi, f + 3, (bx, LANE, G + 0.3))
    T.place(bopi, f + 6, (bx, LANE, G))
    land(bopi, f + 6)
T.place(bopi, 214, (bx, LANE, G))
T.turn(bopi, 212, 20)
T.turn(bopi, 220, 55)
for s in 'LR':
    T.rest_arm(bopi, s, 212)
    T.arm(bopi, s, 220, fwd=-70, out=12)
drive(cA, W[3], 'B', bopi, hop=0.2, item=ap)
T.turn(bopi, 300, 55)
T.turn(bopi, 308, 15)
for s in 'LR':
    T.arm(bopi, s, 300, fwd=-70, out=12)
    T.arm(bopi, s, 308, fwd=-20, out=70)
    T.arm(bopi, s, 340, fwd=-20, out=70)
    T.rest_arm(bopi, s, 348)
xc, zc, _, _ = seg_at('C', 546)
K(cA, 'location', 428, (xc, LANE, seg_at('B', 300)[1] + G))
K(cA, 'location', 438, (xc, LANE, G + zc))
T.place(bopi, 530, (xc - 0.85, LANE, G))
T.turn(bopi, 532, 15)
T.turn(bopi, 542, 55)
for s in 'LR':
    T.rest_arm(bopi, s, 532)
    T.arm(bopi, s, 542, fwd=-70, out=12)
drive(cA, W[0], 'C', bopi)
T.turn(bopi, 630, 55)
T.turn(bopi, 640, 35)
for s in 'LR':
    T.arm(bopi, s, 630, fwd=-70, out=12)
    T.rest_arm(bopi, s, 640)

R0 = Vector((0.15, -0.3, G))
RF = Vector((0.85, -2.0, G))
RB = Vector((-0.9, -0.2, G))
RE = Vector((0.85, -0.3, G))
RS = Vector((1.5, -0.3, G))
T.place(ruki, 0, RS)
T.place(ruki, 58, RS)
T.turn(ruki, 0, -60)
for k, f in enumerate(range(58, 82, 6)):
    p = RS.lerp(R0, (k + 1) / 4)
    T.place(ruki, f + 3, p + Vector((0, 0, 0.07)))
    T.place(ruki, f + 6, p)
T.turn(ruki, 80, -30)
T.arm(ruki, 'L', 86, 0, None)
T.arm(ruki, 'L', 92, fwd=-25, out=80)
T.arm(ruki, 'L', 124, fwd=-25, out=80)
T.rest_arm(ruki, 'L', 132)
T.place(ruki, 318, R0)
T.turn(ruki, 318, -30)
hop_to(ruki, 322, R0, RF, 20, apex=0.8)
T.turn(ruki, 342, -35)
dk = disc('dk', 0.25, 0.08, col[0], None)
C.sphere('dk.hub', (0, -0.05, 0), (0.06, 0.02, 0.06), hub, dk, 20)
D0 = 0.45
T.pop_in(dk, 360)
K(dk, 'location', 0, (D0, -2.3, G + 0.25))
K(dk, 'location', 378, (D0, -2.3, G + 0.25))
K(dk, 'rotation_euler', 378, (0, 0, 0))
for f in range(378, 421, 2):
    u = ease((f - 378) / 42)
    dd = 0.95 * u
    K(dk, 'location', f, (D0 - dd, -2.3, G + 0.25))
    K(dk, 'rotation_euler', f, (0, -dd / 0.25, 0))
T.pop_out(dk, 428, 1.0, 8)
T.arm(ruki, 'L', 368, 0, None)
T.arm(ruki, 'L', 374, fwd=-40, out=60)
T.arm(ruki, 'L', 384, fwd=-40, out=60)
T.rest_arm(ruki, 'L', 392)
T.turn(ruki, 440, -35)
T.turn(ruki, 450, -5)
T.arm(ruki, 'R', 452, 0, None)
T.arm(ruki, 'R', 458, fwd=-35, out=55)
T.arm(ruki, 'R', 500, fwd=-35, out=55)
T.rest_arm(ruki, 'R', 508)
T.place(ruki, 512, RF)
hop_to(ruki, 514, RF, RB, 24, apex=1.1)
T.turn(ruki, 536, -10)
T.turn(ruki, 560, 30)
T.place(ruki, 640, RB)
for k, f in enumerate(range(640, 664, 6)):
    p = RB.lerp(RE, (k + 1) / 4)
    T.place(ruki, f + 3, p + Vector((0, 0, 0.06)))
    T.place(ruki, f + 6, p)
T.turn(ruki, 664, 30)

gA, _ = cart('cartG', (0.45, 0.65, 0.04), None)
GW = [wheel(f'wG{i}', 4, WHEEL[4], gA, (sx * 0.3, sy * 0.33, 0), C.mat(f'wg{i}', (0.35, 0.1, 0.55), rough=0.4, coat=0.3), hub)
      for i, (sx, sy) in enumerate(((-1, -1), (1, -1), (-1, 1), (1, 1)))]
gA.rotation_euler = (0, 0, math.radians(180))
cup, pink = shake_cup('cup', gA, (-0.22, 0.0, 0.305))
x, z, _, _ = seg_at('G1', 0)
K(gA, 'location', 0, (x, LANE, G + z))
T.place(gruno, 0, (x + 0.8, LANE + 0.1, G))
T.turn(gruno, 0, -60)
drive(gA, GW, 'G1', gruno, fx=0.8, fy=0.1, hop=0.06, item=cup, ws=-1)
for w in GW:
    K(w, 'rotation_euler', 676, w.rotation_euler)
T.turn(gruno, 676, -60)
T.turn(gruno, 684, -20)
T.turn(gruno, 722, -20)
T.turn(gruno, 728, -55)
drive(gA, GW, 'G2', gruno, fx=0.8, fy=0.1, ws=-1)
T.turn(gruno, 746, -55)
sc.frame_set(746)
bpy.context.view_layer.update()
c0 = cup.matrix_world.translation + Vector((0, 0, 0.3))
sc.frame_set(760)
bpy.context.view_layer.update()
gogs = [o for o in bpy.data.objects if o.name.startswith('Gruno.goggle.') and o.type == 'EMPTY']
g_mid = sum((o.matrix_world.translation for o in gogs), Vector()) / max(len(gogs), 1)
blob = C.sphere('blob', tuple(c0), (1, 1, 1), pink, None, 24)
K(blob, 'scale', 0, (0, 0, 0))
K(blob, 'scale', 746, (0, 0, 0))
K(blob, 'scale', 749, (0.1, 0.1, 0.13))
K(blob, 'scale', 758, (0.11, 0.11, 0.11))
K(blob, 'scale', 760, (0, 0, 0))
for f in range(746, 761):
    u = (f - 746) / 14
    p = c0.lerp(g_mid + Vector((0, -0.12, 0)), u) + Vector((0, 0, 0.55 * 4 * u * (1 - u)))
    K(blob, 'location', f, tuple(p))
for o in gogs:
    sp = C.sphere(o.name + '.splat', (0, -0.09, 0.0), (1, 1, 1), pink, o, 24)
    K(sp, 'scale', 0, (0, 0, 0))
    K(sp, 'scale', 759, (0, 0, 0))
    K(sp, 'scale', 762, (0.17, 0.035, 0.15))
    K(sp, 'scale', 766, (0.15, 0.03, 0.14))
    dr = C.sphere(o.name + '.drip', (0, -0.1, -0.08), (1, 1, 1), pink, o, 16)
    K(dr, 'scale', 0, (0, 0, 0))
    K(dr, 'scale', 764, (0, 0, 0))
    K(dr, 'scale', 770, (0.035, 0.03, 0.05))
    K(dr, 'location', 770, (0, -0.1, -0.08))
    K(dr, 'location', 800, (0, -0.1, -0.2))
S(gruno, 760, (1, 1, 1))
S(gruno, 763, (1.1, 1.1, 0.9))
S(gruno, 768, (0.97, 0.97, 1.03))
S(gruno, 772, (1, 1, 1))
T.turn(gruno, 764, -55)
T.turn(gruno, 772, -15)
for ch, f in ((bopi, 772), (ruki, 776)):
    p = ch['hold'].location.copy()
    for k in range(3):
        T.place(ch, f + k * 8, p)
        T.place(ch, f + k * 8 + 4, p + Vector((0, 0, 0.12)))
    T.place(ch, f + 24, p)
T.turn(bopi, 770, 35)
T.turn(bopi, 778, 50)
T.turn(ruki, 770, 30)
T.turn(ruki, 778, 45)

T.lines(EID, LINES)
T.blinks(bopi, (60, 170, 260, 400, 520, 660, 790))
T.blinks(ruki, (40, 150, 240, 330, 480, 600, 720))
T.blinks(gruno, (700, 785, 805))
tx = cam_x(640)
h = word3d('¡EL CÍRCULO RUEDA!', (1.0, 0.65, 0.05), (0, 0, 0), 596, 690, size=0.9, max_w=2.5)
h.parent = cam
h.location = (0, 1.25, -7.0)
h.rotation_euler = (0, 0, 0)
