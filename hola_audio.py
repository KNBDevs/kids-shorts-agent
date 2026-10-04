import os
import numpy as np
from scipy.io import wavfile
import synth as S
from synth import SR, ft, add, glock, marimba, pluck, bass, kick, clap, shaker, slide_whistle, boing, splat, sparkle, pop, bip, popper, reverb
from voice import line
from hola_plan import *
HERE = os.path.dirname(os.path.abspath(__file__))
CID = current()
D = CHARS[CID]
G = CID == 'gruno'
DUR = TOTAL / FPS
N = int(SR * DUR)
BPM = 112 if CID in ('ruki', 'moki') else 124
BEAT = 60 / BPM
S.T = {'pimo': 0, 'ruki': -3, 'luma': 2, 'tuki': 4, 'moki': -2, 'bopi': 0, 'bolita': 5, 'gruno': -5}[CID]
chords = {'C': [60, 64, 67], 'G': [55, 59, 62], 'Am': [57, 60, 64], 'F': [53, 57, 60], 'Dm': [50, 53, 57], 'E': [52, 56, 59]}
roots = {'C': 36, 'G': 43, 'Am': 45, 'F': 41, 'Dm': 38, 'E': 40}
if G:
    prog = ['Am', 'Dm', 'E', 'Am'] * 4
    mel = {'Am': [(0, 69), (1, 72), (1.5, 71), (2, 69), (3, 64)], 'Dm': [(0, 65), (1, 69), (2, 74), (3, 72)], 'E': [(0, 68), (1, 71), (2, 74), (2.5, 72), (3, 71)]}
else:
    prog = [['C', 'G', 'Am', 'F'], ['C', 'F', 'G', 'C'], ['F', 'G', 'C', 'Am']][ORDER.index(CID) % 3] * 4
    mel = {'C': [(0, 79), (1, 76), (1.5, 77), (2, 79), (3, 84)], 'G': [(0, 83), (1, 79), (2, 74), (2.5, 76), (3, 77)], 'Am': [(0, 76), (0.5, 77), (1, 76), (2, 72), (3, 69)], 'F': [(0, 72), (1, 74), (1.5, 76), (2, 77), (3, 81)]}
music = np.zeros((N, 2))
drums = np.zeros((N, 2))
lead = marimba if CID in ('ruki', 'moki', 'gruno') else glock
for bar, ch in enumerate(prog):
    t0 = bar * 4 * BEAT
    if t0 >= DUR:
        break
    r = roots[ch]
    pat = [(0, r), (1, r + 7), (2, r + 12), (3, r + 7)] if G else [(0, r), (1.5, r), (2, r + 7), (3, r + 12), (3.5, r + 7)]
    for b, m in pat:
        add(music, bass(m, 0.3 if G else 0.35), t0 + b * BEAT, 0.4)
    for b in (0.5, 1.5, 2.5, 3.5):
        for k, m in enumerate(chords[ch]):
            add(music, pluck(m + 12, 0.42, 0.6), t0 + b * BEAT + k * 0.008, 0.08, pan=-0.3)
    for b, m in mel[ch]:
        add(music, lead(m, 0.5), t0 + b * BEAT, 0.13 if lead is glock else 0.2, pan=0.2)
    for b in range(4):
        add(drums, kick(), t0 + b * BEAT, 0.45 if b % 2 == 0 else 0.2)
        if b % 2:
            add(drums, clap(), t0 + b * BEAT, 0.12)
        if CID not in ('ruki', 'moki'):
            for h in (0, 0.5):
                add(drums, shaker(), t0 + (b + h) * BEAT + 0.01, 0.03 if h else 0.018, pan=0.4)
music = reverb(music, 1.3, 0.28) + drums
tt = np.arange(N) / SR
music *= (np.clip(tt / 0.05, 0, 1) * np.clip((DUR - tt) / 0.6, 0, 1))[:, None]
sfx = np.zeros((N, 2))
add(sfx, popper(), ft(2), 0.3)
add(sfx, sparkle(88), ft(3), 0.2)
add(sfx, boing(260, 0.35, up=True), ft(1), 0.25)
add(sfx, boing(170), ft(12), 0.35)
add(sfx, sparkle(96), ft(T_PRAISE), 0.18)
for f in (T_NAME, T_TRAIT + 2, T_BYE + 4):
    add(sfx, pop(), ft(f), 0.26)
add(sfx, sparkle(91), ft(T_TRAIT + 3), 0.16)
for k in range(5):
    add(sfx, bip(84 + 2 * k), ft(T_TRAIT + 20 + k * 22), 0.12)
if G:
    fp = T_ASK + 46
    add(sfx, bip(96), ft(fp - 4), 0.2)
    add(sfx, popper(), ft(fp), 0.45)
    add(sfx, splat(), ft(fp + 2), 0.3)
    add(sfx, slide_whistle(1400, 400, 0.5), ft(fp + 6), 0.18)
else:
    add(sfx, popper(), ft(T_BYE + 2), 0.28)
vo = np.zeros((N, 2))
v = VOICES[CID]
times = TIMES
limits = (1.6, 3.6, 6.5, 4.3, 2.0, 3.6)
for k, (f, text, lim) in enumerate(zip(times, D['lines'], limits)):
    s = line(f'hola_{CID}_{k}', text, CID, v['pitch'], v['tempo'], v.get('robot', False), max_len=lim)
    add(vo, s, ft(f), 0.9)
env = np.convolve(np.abs(vo[:, 0]), np.ones(2205) / 2205, 'same')
duck = 1 - 0.68 * np.clip(env / (env.max() + 1e-09) * 4, 0, 1)
mix = music * duck[:, None] * 0.62 + sfx * (0.55 + 0.45 * duck)[:, None] + vo * 1.25
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix /= np.abs(mix).max() / 0.89
wavfile.write(os.path.join(HERE, 'soundtrack.wav'), SR, (mix * 32767).astype(np.int16))
print('ok', CID, mix.shape)
