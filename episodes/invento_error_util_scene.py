from stage import *
from episodes.invento_error_util_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA
EID = 'invento_error_util'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0, -7.0, 1.4), (0, -1.1, 1.1), 37)
WF = ((-0.08, -6.3, 1.6), (-0.06, -1.0, 1.3), 35)
camkey(0, W0)
camkey(330, W0)
camkey(346, WF)
camkey(470, WF)
camkey(486, W0)
camkey(TOTAL - 1, W0)

MB = Vector((-0.15, -1.85, Z0))
mach = spawn('bubble_blower', 0, 8801, 'candy', tuple(MB), 1.0, 10)
noz = next(o for o in mach.children_recursive if o.name.startswith('nozzle'))
NZ = MB + Vector((0.0, -0.3, 0.62))
for k, f in enumerate(range(60, 100, 4)):
    K(mach, 'rotation_euler', f, (0, math.radians(3 if k % 2 else -3), math.radians(10)))
K(mach, 'rotation_euler', 102, (0, 0, math.radians(10)))
K(noz, 'rotation_euler', 60, (math.radians(90), 0, 0))
K(noz, 'rotation_euler', 100, (math.radians(90), math.radians(720), 0))
K(noz, 'rotation_euler', 640, (math.radians(90), math.radians(720), 0))
K(noz, 'rotation_euler', 670, (math.radians(90), math.radians(1080), 0))

skin_m = MA((0.82, 0.92, 1.0), 0.15)
sheen_m = MA((1.0, 0.72, 0.95), 0.06)
hi_m = C.mat('bhi', (1, 1, 1), rough=0.2, emit=2.0)


def bubble(name, R):
    root = C.empty(name)
    C.sphere(name + '.skin', (0, 0, 0), (R, R, R), skin_m, root, 48)
    C.sphere(name + '.sheen', (0, 0, 0), (R * 1.02,) * 3, sheen_m, root, 48)
    C.sphere(name + '.hi', (-R * 0.4, -R * 0.82, R * 0.4), (R * 0.13, R * 0.05, R * 0.09), hi_m, root, 16)
    return root


BR = 0.42
big = bubble('big', BR)
B1 = Vector((0.25, -1.75, 1.35))
K(big, 'scale', 0, (0, 0, 0))
K(big, 'scale', 63, (0, 0, 0))
K(big, 'location', 63, tuple(NZ))
for f, sc_ in ((70, 0.3), (80, 0.6), (90, 0.95), (96, 1.08), (100, 1.0)):
    K(big, 'scale', f, (sc_,) * 3)
K(big, 'location', 100, tuple(NZ + Vector((0.1, -0.05, 0.25))))
K(big, 'location', 130, tuple(B1))
for k, f in enumerate(range(140, 330, 16)):
    K(big, 'location', f, tuple(B1 + Vector((0.03 * math.sin(k), 0, 0.04 * (1 if k % 2 else -1)))))
K(big, 'location', 330, tuple(B1))

ball = spawn('play_ball', 1, 8802, (0.92, 0.2, 0.3), (0, 0, 0), 1.45, 0)
BALL_R = 0.11 * 1.45
P0 = Vector((1.0, -1.15, Z0))
HAND = P0 + Vector((-0.42, -0.35, 0.55))
T.pop_in(ball, 242, 1.45)
K(ball, 'location', 0, tuple(HAND))
K(ball, 'location', 312, tuple(HAND))
IN = B1 + Vector((0, 0, -BALL_R))
for f in range(312, 329, 2):
    u = (f - 312) / 16
    K(ball, 'location', f, tuple(HAND.lerp(IN, u) + Vector((0, 0, 0.35 * 4 * u * (1 - u)))))
K(ball, 'rotation_euler', 312, (0, 0, 0))
K(ball, 'rotation_euler', 328, (math.radians(200), 0, 0))
for f, sc_ in ((326, (1, 1, 1)), (330, (1.12, 1.12, 0.88)), (334, (0.92, 0.92, 1.1)), (340, (1, 1, 1))):
    K(big, 'scale', f, sc_)
PATH = [B1, Vector((0.15, -1.2, 1.95)), Vector((0.3, -0.6, 2.05)), Vector((0.35, -0.25, 1.5))]
FR = [340, 380, 420, 452]
for (a, b), (fa, fb) in zip(zip(PATH, PATH[1:]), zip(FR, FR[1:])):
    for f in range(fa, fb + 1, 2):
        u = (f - fa) / (fb - fa)
        u = u * u * (3 - 2 * u)
        p = a.lerp(b, u)
        K(big, 'location', f, tuple(p))
        K(ball, 'location', f, tuple(p + Vector((0, 0, -BALL_R))))
        K(ball, 'rotation_euler', f, (math.radians(200 + (f - 340) * 2), 0, 0))
T.pop_out(big, 454, 1.0, 6)
BK = Vector((0.35, -0.25, Z0))
bas = spawn('ball_basket', 1, 8803, (0.98, 0.75, 0.4), tuple(BK), 1.2, 0)
for f in range(454, 470, 2):
    u = (f - 454) / 14
    K(ball, 'location', f, tuple(Vector((0.35, -0.25, 1.5 - BALL_R)).lerp(BK + Vector((0, 0, 0.2)), u * u)))
K(ball, 'location', 474, tuple(BK + Vector((0, 0, 0.26))))
K(ball, 'location', 478, tuple(BK + Vector((0, 0, 0.2))))

gruno = make('gruno', 1.5)
pimo = make('pimo', 1.7)
G0 = Vector((-0.8, -0.95, Z0))
T.place(gruno, 0, G0)
T.turn(gruno, 0, 25)
T.place(pimo, 0, P0)
T.turn(pimo, 0, -25)

C.wave(gruno, 'R', 14, cycles=2, period=8)
T.arm(gruno, 'L', 54, 0, None)
T.arm(gruno, 'L', 58, fwd=-45, out=None)
T.arm(gruno, 'L', 62, fwd=-45, out=None)
T.arm(gruno, 'L', 68, 0, None)
T.turn(gruno, 66, 25)
T.turn(gruno, 74, 40)
T.turn(gruno, 106, 40)
T.turn(gruno, 112, 15)
S(gruno, 110, (1, 1, 1))
S(gruno, 116, (1.1, 1.1, 0.88))
S(gruno, 150, (1.1, 1.1, 0.88))
S(gruno, 158, (1, 1, 1))
for k, f in enumerate(range(118, 150, 8)):
    T.turn(gruno, f, 15 + (12 if k % 2 else -12))
T.turn(pimo, 170, -25)
T.turn(pimo, 178, -55)
T.arm(pimo, 'R', 182, 0, None)
T.arm(pimo, 'R', 188, fwd=-40, out=110)
T.arm(pimo, 'R', 220, fwd=-40, out=110)
T.rest_arm(pimo, 'R', 228)
T.turn(pimo, 236, -55)
T.turn(pimo, 242, -40)
T.arm(pimo, 'R', 240, 0, None)
T.arm(pimo, 'R', 246, fwd=-50, out=45)
T.arm(pimo, 'R', 308, fwd=-50, out=45)
T.arm(pimo, 'R', 316, fwd=-110, out=45)
T.rest_arm(pimo, 'R', 326)
T.turn(pimo, 340, -40)
T.turn(pimo, 348, 10)
T.turn(pimo, 420, 10)
T.turn(pimo, 428, 40)
T.turn(gruno, 340, 15)
T.turn(gruno, 348, 45)
T.turn(gruno, 460, 45)
T.turn(gruno, 468, 15)
gesture(gruno, 'bounce', 474)
T.turn(pimo, 550, 40)
T.turn(pimo, 558, -10)

sc.frame_set(682)
bpy.context.view_layer.update()
rem = bpy.data.objects['Gruno.remote']
RP = rem.matrix_world.translation.copy()
sc.frame_set(0)
K(rem, 'scale', 0, (1, 1, 1))
K(rem, 'scale', 683, (1, 1, 1))
K(rem, 'scale', 684, (0, 0, 0))
fake = C.empty('fake_remote', None, tuple(RP))
H = 1.3
C.sphere('fr_body', (0, 0, 0), (0.07 * H, 0.05 * H, 0.1 * H), bpy.data.materials['gruno_orange'], fake, 32)
C.sphere('fr_btn', (0, -0.045 * H, 0.015 * H), (0.035 * H, 0.015 * H, 0.035 * H), bpy.data.materials['gruno_btn'], fake, 24)
s_ = gruno['s']
fake.scale = (s_, s_, s_)
fake.rotation_euler = (0, math.radians(-30), 0)
small = bubble('small', 0.22)
K(small, 'scale', 0, (0, 0, 0))
K(small, 'scale', 641, (0, 0, 0))
K(small, 'location', 641, tuple(NZ))
K(small, 'scale', 652, (1, 1, 1))
K(small, 'location', 680, tuple(RP))
K(fake, 'scale', 0, (0, 0, 0))
K(fake, 'scale', 683, (0, 0, 0))
K(fake, 'scale', 684, (s_, s_, s_))
TOPP = RP + Vector((0.75, -0.15, 1.0))
for f in range(684, TOTAL, 4):
    u = min(1.0, (f - 684) / 120)
    p = RP.lerp(TOPP, u) + Vector((0.05 * math.sin(f / 9), 0, 0))
    K(small, 'location', f, tuple(p))
    K(fake, 'location', f, tuple(p))
    K(fake, 'rotation_euler', f, (0, math.radians(-30 + 10 * math.sin(f / 7)), 0))
T.turn(gruno, 630, 15)
T.turn(gruno, 640, 50)
S(gruno, 684, (1, 1, 1))
S(gruno, 688, (0.94, 0.94, 1.08))
S(gruno, 694, (1, 1, 1))
gruno['hold'].location = G0
gesture(gruno, 'hops', 712)
T.arm(gruno, 'R', 712, 0, None)
T.arm(gruno, 'R', 718, fwd=-30, out=150)
T.arm(gruno, 'R', 760, fwd=-30, out=150)
T.rest_arm(gruno, 'R', 768)
T.turn(pimo, 690, -10)
T.turn(pimo, 698, -40)
pimo['hold'].location = P0
gesture(pimo, 'bounce', 780)

T.lines(EID, LINES)
T.blinks(gruno, (90, 200, 300, 420, 560, 700, 800))
T.blinks(pimo, (60, 160, 280, 400, 520, 650, 760))
