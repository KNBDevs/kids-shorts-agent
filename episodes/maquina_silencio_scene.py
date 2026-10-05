from stage import *
from episodes.maquina_silencio_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, MA, M, _ring
EID = 'maquina_silencio'
Z0 = 0.08
auto_dress(EID, ENV)
spawn('gear_tower', 2, 9031, 'candy', (-3.3, 1.6, 0), 1.1, -12)
spawn('bunting', 0, 9032, 'candy', (2.6, 4.2, 0), 1.0, -8)

W0 = ((0, -7.0, 1.25), (0, -1.1, 1.0), 37)
WB = ((0.5, -6.1, 1.4), (0.5, -1.2, 1.25), 40)
WG = ((-0.45, -6.1, 1.35), (-0.45, -1.0, 1.2), 40)
camkey(0, W0)
camkey(380, W0)
camkey(396, WB)
camkey(612, WB)
camkey(628, WG)
camkey(736, WG)
camkey(752, W0)
camkey(TOTAL - 1, W0)

teal = M((0.3, 0.78, 0.82), rough=0.35, coat=0.7)
cream = M((0.98, 0.94, 0.86), rough=0.45, coat=0.4)
orange = M((1.0, 0.5, 0.18), rough=0.35, coat=0.8)
pink = M((1.0, 0.55, 0.72), rough=0.35, coat=0.7)
dark = M((0.12, 0.1, 0.2), rough=0.5)
MP = Vector((0.2, -0.15, Z0))
mach = C.empty('machine', None, tuple(MP))
for x in (-0.3, 0.3):
    for y in (-0.16, 0.16):
        C.sphere('mfoot', (x, y, 0.05), (0.07, 0.07, 0.05), orange, mach, 20)
C.rounded_box('mbody', (0, 0, 0.42), (0.78, 0.5, 0.64), 0.09, teal, mach)
C.rounded_box('mpanel', (0, -0.245, 0.42), (0.6, 0.04, 0.46), 0.03, cream, mach)
lamps = []
for k, x in enumerate((-0.17, 0.0, 0.17)):
    lm = C.mat(f'mlamp{k}', [(0.5, 0.95, 0.4), (1.0, 0.85, 0.3), (1.0, 0.45, 0.6)][k], rough=0.3, coat=0.8, emit=0.3)
    lamps.append(lm)
    C.sphere('mlamp', (x, -0.27, 0.58), (0.05, 0.03, 0.05), lm, mach, 20)
dial = C.empty('mdial', mach, (-0.12, -0.27, 0.34), (math.radians(90), 0, 0))
C.lathe('mdialface', [(0, 0.0), (0, 0.09), (0.015, 0.095), (0.025, 0.08), (0.03, 0.0)], M((1, 1, 1), rough=0.3, coat=0.6), dial, segs=40)
needle = C.empty('mneedle', dial, (0, 0, 0.032))
C.tube('mneedlebar', [(0, 0, 0), (0, 0.065, 0)], 0.008, dark, needle)
C.sphere('mbtn', (0.15, -0.27, 0.33), (0.075, 0.045, 0.075), orange, mach, 24)
hornp = C.empty('mhornp', mach, (-0.2, 0.0, 0.74), (math.radians(-35), math.radians(-30), 0))
C.lathe('mhorn', [(0.0, 0.055), (0.12, 0.06), (0.25, 0.09), (0.34, 0.16), (0.38, 0.22), (0.39, 0.235), (0.375, 0.215), (0.33, 0.14), (0.24, 0.07), (0.1, 0.04), (-0.02, 0.04)], pink, hornp, segs=48)
C.lathe('mhorncore', [(0.2, 0.0), (0.2, 0.055), (0.21, 0.0)], dark, hornp, segs=32)
C.tube('mwandstem', [(0.22, 0.0, 0.72), (0.24, 0.0, 0.92)], 0.02, orange, mach)
C.tube('mwand', [(0.24 + math.cos(k * 6.2832 / 40) * 0.09, 0.0, 1.01 + math.sin(k * 6.2832 / 40) * 0.09) for k in range(41)], 0.018, orange, mach)

ped_m = M((0.75, 0.6, 1.0), rough=0.4, coat=0.6)
BL = Vector((0.45, -1.85, Z0))
DR = Vector((-0.3, -1.95, Z0))
C.lathe('ped1', [(0, 0.0), (0, 0.2), (0.16, 0.18), (0.2, 0.2), (0.2, 0.0)], ped_m, None, segs=40).location = tuple(BL)
C.lathe('ped2', [(0, 0.0), (0, 0.27), (0.12, 0.25), (0.15, 0.27), (0.15, 0.0)], M((1.0, 0.82, 0.4), rough=0.4, coat=0.6), None, segs=40).location = tuple(DR)
bell = spawn('desk_bell', 2, 4411, 'candy', tuple(BL + Vector((0, 0, 0.15))), 1.2, 0)
drum = spawn('toy_drum', 0, 4412, 'candy', tuple(DR + Vector((0, 0, 0.12))), 1.1, 15)
drum.rotation_euler = (math.radians(22), 0, math.radians(15))
bpiv = next(o for o in bell.children_recursive if o.name.startswith('bell_pivot'))
skin = next(o for o in drum.children_recursive if o.name.startswith('skin'))
BELLC = BL + Vector((0, -0.02, 0.15 + 0.52 * 1.2 - 0.12))
DRUMC = DR + Vector((0, -0.17, 0.12 + 0.36 * 1.1 * 0.93 + 0.1))


def ring_bell(f0, n=6, amp=22):
    K(bpiv, 'rotation_euler', f0, (0, 0, 0))
    for k in range(n):
        a = amp * (1 - k / n) * (1 if k % 2 == 0 else -1)
        K(bpiv, 'rotation_euler', f0 + 3 + k * 4, (0, math.radians(a), 0))
    K(bpiv, 'rotation_euler', f0 + 3 + n * 4, (0, 0, 0))


def stop_bell(f0):
    K(bpiv, 'rotation_euler', f0, (0, math.radians(14), 0))
    K(bpiv, 'rotation_euler', f0 + 3, (0, 0, 0))


def hit_drum(f0):
    K(skin, 'scale', f0 - 1, (1, 1, 1))
    K(skin, 'scale', f0 + 1, (1.04, 1.04, 0.2))
    K(skin, 'scale', f0 + 4, (0.98, 0.98, 1.6))
    K(skin, 'scale', f0 + 8, (1, 1, 1))
    K(drum, 'scale', f0 - 1, (1.1,) * 3)
    K(drum, 'scale', f0 + 2, (1.15, 1.15, 1.03))
    K(drum, 'scale', f0 + 7, (1.1,) * 3)


wave_m = C.mat('wave', (1.0, 0.92, 0.6), rough=0.3, emit=1.2)


def waves(center, f0, capture=None, n=3, big=0.5):
    for k in range(n):
        h = C.empty('wv', None, tuple(center))
        C.tube('wvr', [(math.cos(a * 6.2832 / 48), 0, math.sin(a * 6.2832 / 48)) for a in range(49)], 0.035, wave_m, h)
        s0 = f0 + k * 4
        K(h, 'scale', 0, (0, 0, 0))
        K(h, 'scale', s0 - 1, (0, 0, 0))
        K(h, 'scale', s0, (0.08,) * 3)
        if capture:
            K(h, 'scale', s0 + 8, ((0.2 + 0.07 * k),) * 3)
            K(h, 'scale', capture + 6, (0.06,) * 3)
            K(h, 'scale', capture + 8, (0, 0, 0))
        else:
            K(h, 'scale', s0 + 18, (big + 0.15 * k,) * 3)
            K(h, 'scale', s0 + 22, (0, 0, 0))


skin_m = MA((0.82, 0.92, 1.0), 0.26)
sheen_m = MA((1.0, 0.72, 0.95), 0.12)
hi_m = C.mat('bhi', (1, 1, 1), rough=0.2, emit=2.0)
arc_m = C.mat('barc', (1.0, 0.85, 0.45), rough=0.3, emit=1.5)


def bubble(name, R=0.24, inner='arcs'):
    root = C.empty(name)
    C.sphere(name + '.skin', (0, 0, 0), (R, R, R), skin_m, root, 40)
    C.sphere(name + '.sheen', (0, 0, 0), (R * 1.03,) * 3, sheen_m, root, 40)
    C.sphere(name + '.hi', (-R * 0.38, -R * 0.82, R * 0.42), (R * 0.15, R * 0.06, R * 0.1), hi_m, root, 16)
    if inner == 'arcs':
        for k in range(3):
            rr = R * (0.22 + 0.2 * k)
            C.tube(name + '.arc', [(-R * 0.3 + rr * math.cos(math.radians(a)), 0, rr * math.sin(math.radians(a))) for a in range(-50, 51, 10)], 0.012, arc_m, root)
        C.sphere(name + '.dot', (-R * 0.3, 0, 0), (0.025,) * 3, arc_m, root, 12)
    else:
        for k, (dx, dz, sz) in enumerate(((-0.06, -0.05, 0.11), (0.05, 0.04, 0.08), (0.11, 0.11, 0.06))):
            zc = bpy.data.curves.new('zz', 'FONT')
            zc.body = 'z'
            zc.font = font
            zc.align_x = 'CENTER'
            zc.align_y = 'CENTER'
            zc.size = sz * 1.6
            zc.extrude = 0.01
            zo = bpy.data.objects.new('zz', zc)
            sc.collection.objects.link(zo)
            zo.data.materials.append(arc_m)
            zo.parent = root
            zo.location = (dx, 0, dz)
            zo.rotation_euler = (math.radians(90), 0, 0)
    return root


def flash(f0, n=4):
    for m in lamps:
        inp = m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
        for k in range(n):
            inp.default_value = 0.3
            inp.keyframe_insert('default_value', frame=f0 + k * 6)
            inp.default_value = 3.0
            inp.keyframe_insert('default_value', frame=f0 + k * 6 + 3)
        inp.default_value = 0.3
        inp.keyframe_insert('default_value', frame=f0 + n * 6)
    K(needle, 'rotation_euler', f0, (0, 0, 0))
    K(needle, 'rotation_euler', f0 + 6, (0, 0, math.radians(-70)))
    K(needle, 'rotation_euler', f0 + n * 6 + 6, (0, 0, 0))
    K(hornp, 'scale', f0, (1, 1, 1))
    K(hornp, 'scale', f0 + 5, (0.9, 0.9, 1.15))
    K(hornp, 'scale', f0 + 12, (1.08, 1.08, 0.95))
    K(hornp, 'scale', f0 + 18, (1, 1, 1))


HB1 = Vector((-0.28, -0.4, 1.85))
HB2 = Vector((0.48, -0.4, 1.9))


def fly(o, pts, frames):
    for (a, b), (fa, fb) in zip(zip(pts, pts[1:]), zip(frames, frames[1:])):
        for f in range(fa, fb + 1, 2):
            u = (f - fa) / (fb - fa)
            u = u * u * (3 - 2 * u)
            p = a.lerp(b, u) + Vector((0, 0, 0.18 * 4 * u * (1 - u)))
            K(o, 'location', f, tuple(p))


def bob(o, base, f0, f1, amp=0.05, per=24, ph=0):
    for f in range(f0, f1, per // 2):
        k = (f - f0) // (per // 2)
        K(o, 'location', f, tuple(base + Vector((0, 0, amp * (1 if (k + ph) % 2 else -1)))))


gruno = make('gruno', 1.6)
bopi = make('bopi', 1.5)
G0 = Vector((-0.85, -1.0, Z0))
P0 = Vector((1.0, -1.25, Z0))
PD = Vector((0.0, -1.45, Z0))
B1P = P0 + Vector((0, 0, 1.9))
T.place(gruno, 0, G0)
T.turn(gruno, 0, 15)
T.place(bopi, 0, P0)
T.turn(bopi, 0, -20)


def press(f):
    T.arm(gruno, 'L', f - 4, 0, None)
    T.arm(gruno, 'L', f, fwd=-45, out=None)
    T.arm(gruno, 'L', f + 3, fwd=-45, out=None)
    T.arm(gruno, 'L', f + 9, 0, None)
    S(gruno, f - 2, (1, 1, 1))
    S(gruno, f + 1, (1.04, 1.04, 0.96))
    S(gruno, f + 6, (1, 1, 1))


def tap(ch, side, f, fwd=-80):
    T.arm(ch, side, f - 6, 0, None)
    T.arm(ch, side, f, fwd=fwd, out=10)
    T.arm(ch, side, f + 4, fwd=fwd * 0.6, out=10)
    T.rest_arm(ch, side, f + 10)


C.wave(gruno, 'R', 14, cycles=3, period=8)
T.turn(gruno, 40, 15)
T.turn(gruno, 48, 35)
T.turn(bopi, 54, -20)
T.turn(bopi, 60, -42)
tap(bopi, 'R', 66)
ring_bell(66)
waves(BELLC, 68, capture=80)
press(76)
flash(78)
stop_bell(84)

b1 = bubble('bub1')
K(b1, 'scale', 0, (0, 0, 0))
K(b1, 'scale', 79, (0, 0, 0))
K(b1, 'scale', 86, (1.15,) * 3)
K(b1, 'scale', 90, (1,) * 3)
K(b1, 'location', 79, tuple(BELLC))
K(b1, 'location', 92, tuple(BELLC))
fly(b1, [BELLC, HB1], [92, 112])
bob(b1, HB1, 114, 392, ph=0)
fly(b1, [HB1, B1P], [392, 404])
T.pop_out(b1, 406, 1.0, 4)
waves(B1P, 406, big=0.5)

T.turn(gruno, 104, 35)
T.turn(gruno, 110, 10)
gesture(gruno, 'bounce', 114)
tap(bopi, 'R', 152)
ring_bell(152, n=3, amp=12)
T.turn(bopi, 162, -42)
for k, f in enumerate(range(170, 222, 13)):
    T.turn(bopi, f, (-35 if k % 2 == 0 else 25))
T.turn(bopi, 228, -20)
S(bopi, 166, (1, 1, 1))
S(bopi, 170, (1.06, 1.06, 0.94))
S(bopi, 176, (1, 1, 1))

T.turn(gruno, 222, 10)
T.turn(gruno, 230, 30)
C.wave(gruno, 'R', 226, cycles=2, period=8)
T.turn(bopi, 252, -20)
T.turn(bopi, 258, -80)
hop_to(bopi, 262, P0, PD, 14, apex=0.35)
T.turn(bopi, 276, -80)
T.turn(bopi, 280, -31)
tap(bopi, 'R', 280, fwd=-65)
hit_drum(280)
tap(bopi, 'L', 290, fwd=-65)
hit_drum(290)
waves(DRUMC, 282, capture=294)
press(290)
flash(292)

b2 = bubble('bub2')
K(b2, 'scale', 0, (0, 0, 0))
K(b2, 'scale', 291, (0, 0, 0))
K(b2, 'scale', 298, (1.15,) * 3)
K(b2, 'scale', 302, (1,) * 3)
K(b2, 'location', 291, tuple(DRUMC))
K(b2, 'location', 304, tuple(DRUMC))
fly(b2, [DRUMC, HB2], [304, 324])
bob(b2, HB2, 326, 516, ph=1)
fly(b2, [HB2, B1P], [516, 528])
T.pop_out(b2, 530, 1.0, 4)
waves(B1P, 530, big=0.5)
waves(B1P, 542, big=0.5, n=2)

T.turn(bopi, 310, -31)
T.turn(bopi, 318, 100)
hop_to(bopi, 322, PD, P0, 14, apex=0.35)
T.turn(bopi, 338, 100)
T.turn(bopi, 346, -20)
T.arm(bopi, 'R', 348, 0, None)
T.arm(bopi, 'R', 354, fwd=-30, out=140)
T.arm(bopi, 'R', 384, fwd=-30, out=140)
T.rest_arm(bopi, 'R', 392)
T.turn(bopi, 392, 0)
S(bopi, 403, (1, 1, 1))
S(bopi, 406, (1.1, 1.1, 0.9))
S(bopi, 412, (1, 1, 1))
T.turn(bopi, 428, 0)
T.turn(bopi, 436, -42)
ring_bell(434, n=5, amp=14)
T.turn(gruno, 404, 10)
T.turn(gruno, 412, 30)
T.turn(bopi, 470, -42)
T.turn(bopi, 478, -10)
T.arm(bopi, 'L', 480, 0, None)
T.arm(bopi, 'L', 486, fwd=-30, out=140)
T.arm(bopi, 'L', 512, fwd=-30, out=140)
T.rest_arm(bopi, 'L', 520)
T.turn(bopi, 516, 0)
S(bopi, 527, (1, 1, 1))
S(bopi, 530, (1.1, 1.1, 0.9))
S(bopi, 536, (1, 1, 1))
T.turn(bopi, 572, 0)
T.turn(bopi, 580, -55)
hit_drum(578)
T.turn(bopi, 600, -55)
T.turn(bopi, 606, -10)
gesture(bopi, 'hops', 608)
T.turn(gruno, 528, 30)
T.turn(gruno, 536, 10)

T.turn(gruno, 618, 10)
T.turn(gruno, 626, 0)
mouth = gruno['mouth']
mb = tuple(mouth.scale)
K(mouth, 'scale', 680, mb)
K(mouth, 'scale', 688, (mb[0] * 1.3, mb[1], mb[2] * 3.2))
K(mouth, 'scale', 700, (mb[0] * 1.3, mb[1], mb[2] * 3.2))
K(mouth, 'scale', 706, mb)
for e in gruno['eyes']:
    if e is None:
        continue
    K(e, 'scale', 694, (1, 1, 1))
    K(e, 'scale', 702, (1, 1, 0.08))
    K(e, 'scale', TOTAL - 1, (1, 1, 0.08))
S(gruno, 700, (1, 1, 1))
for f in range(708, TOTAL - 1, 28):
    S(gruno, f, (1.0, 1.0, 1.0))
    S(gruno, f + 14, (1.04, 1.04, 0.96))
for k, f in enumerate(range(704, TOTAL - 1, 28)):
    K(gruno['spin'], 'rotation_euler', f, (0, math.radians(4 if k % 2 else -2), 0))

b3 = bubble('bub3', R=0.2, inner='zzz')
GH = G0 + Vector((0.5, -0.35, 1.7))
K(b3, 'scale', 0, (0, 0, 0))
K(b3, 'scale', 716, (0, 0, 0))
K(b3, 'scale', 724, (1.15,) * 3)
K(b3, 'scale', 728, (1,) * 3)
K(b3, 'location', 716, tuple(G0 + Vector((0.15, -0.7, 0.95))))
K(b3, 'location', 734, tuple(GH))
bob(b3, GH, 742, TOTAL - 1, amp=0.06, per=28)

T.turn(bopi, 700, -10)
T.turn(bopi, 708, -45)
T.turn(bopi, 742, -45)
T.turn(bopi, 750, -20)
gesture(bopi, 'bounce', 800)
C.wave(bopi, 'R', 806, cycles=2, period=8)

T.lines(EID, LINES)
T.blinks(gruno, (90, 200, 300, 420, 560, 640))
T.blinks(bopi, (40, 140, 260, 360, 470, 560, 660, 780))
word3d('CAMPANA', (0.95, 0.2, 0.45), (0.5, -1.6, 2.5), 434, 518, size=0.5, max_w=1.5)
word3d('TAMBOR', (0.15, 0.35, 0.95), (0.3, -1.6, 2.5), 578, 640, size=0.5, max_w=1.3)
