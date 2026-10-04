import os
import numpy as np
from scipy.io import wavfile
import synth as S
from synth import SR, ft, add, glock, marimba, pluck, bass, kick, clap, shaker, slide_whistle, boing, splat, sparkle, pop, bip, popper, reverb
from voice import line
from episode_lib import current_id, plan, FPS
HERE = os.path.dirname(os.path.abspath(__file__))
EID = current_id()
P = plan(EID)
DUR = P.TOTAL / FPS
N = int(SR * DUR)
MOOD = getattr(P, "MOOD", "happy")
BPM = {"happy": 124, "calm": 108, "silly": 132, "mystery": 112}[MOOD]
BEAT = 60 / BPM
S.T = getattr(P, "TRANSPOSE", 0)
chords = {"C": [60, 64, 67], "G": [55, 59, 62], "Am": [57, 60, 64], "F": [53, 57, 60], "Dm": [50, 53, 57], "E": [52, 56, 59]}
roots = {"C": 36, "G": 43, "Am": 45, "F": 41, "Dm": 38, "E": 40}
if MOOD == "mystery":
    prog = ["Am", "Dm", "E", "Am"] * 6
    mel = {"Am": [(0, 69), (1, 72), (2, 69), (3, 64)], "Dm": [(0, 65), (1, 69), (2, 74), (3, 72)], "E": [(0, 68), (1, 71), (2, 74), (3, 71)]}
else:
    prog = ["C", "G", "Am", "F"] * 6
    mel = {"C": [(0, 79), (1, 76), (1.5, 77), (2, 79), (3, 84)], "G": [(0, 83), (1, 79), (2, 74), (2.5, 76), (3, 77)],
           "Am": [(0, 76), (0.5, 77), (1, 76), (2, 72), (3, 69)], "F": [(0, 72), (1, 74), (1.5, 76), (2, 77), (3, 81)]}
lead = marimba if MOOD in ("calm", "mystery", "silly") else glock
music = np.zeros((N, 2)); drums = np.zeros((N, 2))
for bar, ch in enumerate(prog):
    t0 = bar * 4 * BEAT
    if t0 >= DUR:
        break
    r = roots[ch]
    for b, m in [(0, r), (1.5, r), (2, r + 7), (3, r + 12), (3.5, r + 7)]:
        add(music, bass(m, 0.35), t0 + b * BEAT, 0.4)
    for b in (0.5, 1.5, 2.5, 3.5):
        for k, m in enumerate(chords[ch]):
            add(music, pluck(m + 12, 0.42, 0.6), t0 + b * BEAT + k * 0.008, 0.08, pan=-0.3)
    for b, m in mel[ch]:
        add(music, lead(m, 0.5), t0 + b * BEAT, 0.13 if lead is glock else 0.2, pan=0.2)
    for b in range(4):
        add(drums, kick(), t0 + b * BEAT, 0.45 if b % 2 == 0 else 0.2)
        if b % 2:
            add(drums, clap(), t0 + b * BEAT, 0.12)
        if MOOD != "calm":
            for h in (0, 0.5):
                add(drums, shaker(), t0 + (b + h) * BEAT + 0.01, 0.03 if h else 0.018, pan=0.4)
music = reverb(music, 1.3, 0.28) + drums
tt = np.arange(N) / SR
music *= (np.clip(tt / 0.05, 0, 1) * np.clip((DUR - tt) / 0.6, 0, 1))[:, None]
def tock():
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 820 * t) + 0.4 * np.sin(2 * np.pi * 1730 * t)) * np.exp(-t * 45) * np.minimum(1, t * 900)


SFX = {"pop": lambda: pop(), "boing": lambda: boing(170), "boing_up": lambda: boing(260, 0.35, up=True), "splat": lambda: splat(),
       "sparkle": lambda: sparkle(88), "popper": lambda: popper(), "bip": lambda: bip(88),
       "whistle_down": lambda: slide_whistle(1400, 400, 0.5), "whistle_up": lambda: slide_whistle(500, 1500, 0.5),
       "clonk": lambda: S.lp(kick(), 1500), "tock": lambda: tock()}
sfx = np.zeros((N, 2))
for f, kind, g in getattr(P, "SFX", []):
    add(sfx, SFX[kind](), ft(f), g)
vo = np.zeros((N, 2))
for key, char, text, frame, mx in P.LINES:
    add(vo, line(f"ep_{EID}_{key}", text, char, max_len=mx), ft(frame), 0.9)
env = np.convolve(np.abs(vo[:, 0]), np.ones(2205) / 2205, "same")
duck = 1 - 0.68 * np.clip(env / (env.max() + 1e-09) * 4, 0, 1)
mix = music * duck[:, None] * 0.62 + sfx * (0.55 + 0.45 * duck)[:, None] + vo * 1.25
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix /= np.abs(mix).max() / 0.89
wavfile.write(os.path.join(HERE, "soundtrack.wav"), SR, (mix * 32767).astype(np.int16))
print("ok", EID, mix.shape)
