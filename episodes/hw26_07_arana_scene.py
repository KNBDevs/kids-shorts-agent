from stage import *
from episodes.hw26_07_arana_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, glyph, _font
from props.costumes import dress
from props import halloween as HW
from episodes.hw_look import autumn
EID = 'hw26_07_arana'
Z0 = 0.08
autumn()
auto_dress(EID, ENV)

W0 = ((0, -5.6, 1.55), (0, -1.15, 0.85), 32)
WC = ((0, -2.55, 3.7), (0, -1.22, 0.2), 30)
camkey(0, W0)
camkey(136, W0)
camkey(150, WC)
camkey(486, WC)
camkey(500, W0)
camkey(TOTAL - 1, W0)

PAD = Vector((0, -1.3, Z0))
PS = 1.5
pad = spawn('leaf_pad', 0, 707, 'autumn', tuple(PAD), PS, 0)
seda = HW.spider('Seda', span=1.45)
seda['root'].location = PAD + Vector((0, 0, 0.065 * PS + 0.005))
body = seda['body']
legs = seda['legs']

bopi = make('bopi', 1.3)
ruki = make('ruki', 1.35)
dress(bopi, 'bopi', COSTUME, 1)
dress(ruki, 'ruki', COSTUME, 0)
BP = Vector((-1.12, -0.75, Z0))
RP = Vector((1.12, -0.75, Z0))
T.place(bopi, 0, BP)
T.place(ruki, 0, RP)
T.turn(bopi, 0, 30)
T.turn(ruki, 0, -30)

wl = legs['leg_L_1']
r0 = tuple(wl.rotation_euler)
K(wl, 'rotation_euler', 0, r0)
K(wl, 'rotation_euler', 4, r0)
up = (r0[0], r0[1] + math.radians(48), r0[2])
K(wl, 'rotation_euler', 12, up)
for k, f in enumerate(range(16, 96, 8)):
    K(wl, 'rotation_euler', f, (up[0], up[1], up[2] + math.radians(14 if k % 2 else -14)))
K(wl, 'rotation_euler', 100, up)
K(wl, 'rotation_euler', 480, up)
K(wl, 'rotation_euler', 494, r0)
for f, a in ((0, 0), (10, -6), (40, 6), (70, -6), (100, 0)):
    K(body, 'rotation_euler', f, (0, 0, math.radians(a)))
for f, z in ((0, 0.0), (6, 0.03), (12, 0.0)):
    K(seda['root'], 'location', f, tuple(seda['root'].location + Vector((0, 0, z))))

T.turn(bopi, 8, 30)
T.turn(bopi, 16, 15)
for f, tilt in ((10, 0), (18, 12), (60, 12), (68, 0)):
    K(bopi['sq'], 'rotation_euler', f, (0, math.radians(tilt), 0))

bpy.context.scene.frame_set(300)
bpy.context.view_layer.update()
ORDER = [('L', 1), ('L', 2), ('L', 3), ('L', 4), ('R', 1), ('R', 2), ('R', 3), ('R', 4)]
glow = M((1.0, 0.82, 0.35), rough=0.3, coat=0.5, emit=0.6)
ink = M((0.3, 0.16, 0.36), rough=0.35, coat=0.5)
dot_m = M((1.0, 0.84, 0.5), rough=0.4, coat=0.5)
nodes = []
for k, (side, i) in enumerate(ORDER):
    toe = bpy.data.objects[f'Seda.toe_{side}_{i}']
    leg = legs[f'leg_{side}_{i}']
    p = Vector(toe.location)
    pw = toe.matrix_world.translation.copy()
    f0 = 150 + 42 * k
    ring = C.empty(f'node{k}', leg, tuple(p + Vector((0, 0, 0.012))))
    C.tube(f'nodering{k}', [(0.06 * math.cos(2 * math.pi * j / 32), 0.06 * math.sin(2 * math.pi * j / 32), 0) for j in range(33)], 0.012, glow, ring)
    T.pop_in(ring, f0, 1.0, 8)
    sx = -1 if side == 'L' else 1
    dv = (pw - PAD)
    dv.z = 0
    dv.normalize()
    tag = C.empty(f'tag{k}', None, tuple(pw + dv * 0.2 + Vector((0, 0, 0.12))), (math.radians(-70), 0, 0))
    C.sphere(f'tagbg{k}', (0, 0.012, 0), (0.11, 0.02, 0.11), dot_m, tag, 24)
    glyph(str(k + 1), 0.17, 0.012, ink, tag, (0, -0.012, -0.004))
    T.pop_in(tag, f0 + 2, 1.0, 8)
    nodes.append((ring, tag))
    rr = tuple(leg.rotation_euler)
    if (side, i) == ('L', 1):
        continue
    K(leg, 'rotation_euler', f0, rr)
    K(leg, 'rotation_euler', f0 + 5, (rr[0], rr[1] - sx * math.radians(8), rr[2]))
    K(leg, 'rotation_euler', f0 + 11, rr)
for ring, tag in nodes:
    T.pop_out(tag, 700, 1.0, 8)
    T.pop_out(ring, 840, 1.0, 8)

BB = BP + Vector((-0.15, 0.55, 0))
RB = RP + Vector((0.15, 0.55, 0))
hop_to(bopi, 126, BP, BB, 12, apex=0.25)
hop_to(ruki, 130, RP, RB, 12, apex=0.25)
hop_to(bopi, 490, BB, BP, 12, apex=0.25)
hop_to(ruki, 494, RB, RP, 12, apex=0.25)
for f, a in ((150, -30), (156, -15)):
    T.turn(ruki, f, a)
gesture(ruki, 'breathe', 300)
T.arm(ruki, 'R', 160, 0, None)
T.arm(ruki, 'R', 166, fwd=-50, out=30)
T.arm(ruki, 'R', 470, fwd=-50, out=30)
T.rest_arm(ruki, 'R', 478)
gesture(bopi, 'breathe', 360)

word3d('8 PATAS', (0.98, 0.62, 0.22), (0, -1.5, 2.35), 500, 700, size=0.42, max_w=1.4)
lab = HW.card('lab_ni', 'no es un insecto', _font(), (0, -1.5, 1.85), w=1.05, h=0.2, bg=(0.5, 0.28, 0.52), ink=(1.0, 0.9, 0.7), rot=(math.radians(-6), 0, 0))
T.pop_in(lab, 600, 1.0, 10)
T.pop_out(lab, 700, 1.0, 8)

T.turn(bopi, 700, 30)
T.turn(bopi, 708, 5)
for side in ('L', 'R'):
    T.arm(bopi, side, 700, 0, None)
    T.arm(bopi, side, 708, fwd=-150, out=40)
for k, f in enumerate(range(708, 760, 8)):
    K(bopi['spin'], 'rotation_euler', f, (0, math.radians(10 if k % 2 else -10), math.radians(5)))
K(bopi['spin'], 'rotation_euler', 764, (0, 0, math.radians(5)))
for side in ('L', 'R'):
    T.arm(bopi, side, 760, fwd=-150, out=40)
    T.rest_arm(bopi, side, 770)
S(bopi, 762, (1, 1, 1))
S(bopi, 766, (1.1, 1.1, 0.9))
S(bopi, 772, (1, 1, 1))
C.wave(bopi, 'R', 790, cycles=2, period=8)
for f, z in ((790, 0.0), (796, 0.04), (802, 0.0)):
    K(seda['root'], 'location', f, tuple(PAD + Vector((0, 0, 0.065 * PS + 0.005 + z))))
T.turn(ruki, 760, -15)
T.turn(ruki, 768, -35)

T.lines(EID, LINES)
T.blinks(bopi, (60, 200, 330, 470, 600, 740, 830))
T.blinks(ruki, (90, 230, 380, 520, 650, 800))
