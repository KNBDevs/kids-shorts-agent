import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hola_plan import *
os.environ['TOTAL_FRAMES'] = str(TOTAL)
from stage import *
from mathutils import Vector
CID = current()
D = CHARS[CID]
L = D['lines']
G = CID == 'gruno'
FAR = ((0, -8.2, 2.3), (0, -1.2, 1.25), 45)
NEAR = ((0, -6.0, 2.05), (0, -1.2, 1.4), 45)
camkey(0, ((0, -7.4, 2.0), (0, -1.2, 1.3), 45))
camkey(14, FAR)
camkey(T_ASK - 8, FAR)
camkey(T_ASK + 10, NEAR)
camkey(T_BYE - 10, NEAR)
camkey(T_BYE + 8, FAR)
camkey(TOTAL - 12, FAR)
camkey(TOTAL - 1, ((0, -7.4, 2.0), (0, -1.2, 1.3), 45))
ch = make(CID, target_h=2.1 if G else 2.0)
acc = ch['accent']
under = CENTER + Vector((0, 0, -2.6))
K(ch['hold'], 'location', 0, tuple(under))
K(ch['hold'], 'location', 1, tuple(under))
K(ch['hold'], 'location', 7, tuple(CENTER + Vector((0, 0, 0.9))))
K(ch['hold'], 'location', 12, tuple(CENTER))
land(ch, 12)
if G:
    K(ch['spin'], 'rotation_euler', 0, (0, 0, math.radians(-12)))

import json
try:
    MAN = json.load(open(os.path.join(HERE, 'assets', 'vo', 'manifest.json')))
except Exception:
    MAN = {}

def say(f, text, key):
    d = MAN.get(key, {}).get('dur')
    n = round(d * FPS / 4) if d else len(text) // 4
    C.talk(ch, f, syllables=max(3, n), step=4)
for k, (f, t) in enumerate(zip(TIMES, L)):
    say(f, t, f'hola_{CID}_{k}')
for f in (40, 120, 230, 300, 470, 540, 585):
    C.blink(ch, f)
confetti(2, (0, -1.2, 1.8), 30)
word3d('¡HOLA!', (0.2, 0.55, 1.0), (0, -1.6, 2.95), 3, T_NAME - 4, size=1.2, max_w=2.3)
word3d(D['name'], acc, (0, -1.6, 2.95), T_NAME, T_TRAIT - 6, size=1.0, max_w=2.2)
word3d(D['trait'], acc, (0, -1.6, 2.95), T_TRAIT + 2, T_ASK - 10, size=1.0, max_w=2.2)
word3d('PIMORUKI', (1.0, 0.3, 0.6), (0, -1.6, 2.95), T_BYE + 4, TOTAL - 8, size=1.0, max_w=2.2)
C.wave(ch, 'R', T_HOLA + 2, cycles=2, period=8)
gesture(ch, D['gesture'], T_TRAIT + 10)
gesture(ch, D['gesture'], T_ASK + 30)
C.wave(ch, 'R', T_BYE + 4, cycles=3, period=8)
glow = C.mat('glow', (1, 0.78, 0.15), rough=0.2, coat=0.8, emit=0.7)
bub = C.mat('bub', (0.75, 0.9, 1.0), rough=0.05, coat=1.0, emit=0.2)

def floater(obj, f0, x, life=60, rise=1.6):
    K(obj, 'location', f0, (x, -1.4, 1.6))
    K(obj, 'location', f0 + life, (x * 1.3, -1.4, 1.6 + rise))
    set_interp(obj, 'LINEAR')
emote = D['emote']
random.seed(5)
for k in range(5):
    f0 = T_TRAIT + 20 + k * 22
    x = (-1 if k % 2 else 1) * random.uniform(0.7, 1.15)
    if emote in ('bubble', 'spark'):
        o = C.sphere('em', (0, 0, 0), (1, 1, 1), bub if emote == 'bubble' else glow, None, 24)
        r0 = 0.13
        K(o, 'scale', 0, (0, 0, 0))
        K(o, 'scale', f0 - 1, (0, 0, 0))
        K(o, 'scale', f0 + 6, (r0, r0, r0))
        K(o, 'scale', f0 + 54, (r0, r0, r0))
        K(o, 'scale', f0 + 60, (0, 0, 0))
        floater(o, f0, x)
    elif emote == 'poof':
        continue
    else:
        txt = emote if emote != '123' else '123'[k % 3]
        h = word3d(txt, acc, (x, -1.4, 1.6), f0, f0 + 56, size=0.55, max_w=1.0)
        floater(h, f0, x)
if G:
    fp = T_ASK + 46
    confetti(fp, (0.2, -1.6, 2.2), 40, 2.2)
    S(ch, fp, (1, 1, 1))
    S(ch, fp + 3, (1.15, 1.15, 0.85))
    S(ch, fp + 8, (0.95, 0.95, 1.06))
    S(ch, fp + 12, (1, 1, 1))
    K(ch['spin'], 'rotation_euler', fp, (0, 0, math.radians(-12)))
    K(ch['spin'], 'rotation_euler', fp + 6, (0, 0, math.radians(14)))
    K(ch['spin'], 'rotation_euler', fp + 14, (0, 0, math.radians(-12)))
else:
    confetti(T_PRAISE, (0, -1.2, 2.2), 30, 2.4)
    confetti(T_BYE + 2, (0, -1.2, 2.4), 26, 2.4)
if __name__ == '__main__':
    run()
