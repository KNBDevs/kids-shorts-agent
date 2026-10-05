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
SONG = getattr(P, "SONG", None)
smel = {"C": [(0, 72), (0.5, 74), (1, 76), (2, 79), (3, 76)], "G": [(0, 74), (1, 71), (1.5, 74), (2, 79), (3, 74)],
        "Am": [(0, 72), (1, 76), (2, 81), (3, 79)], "F": [(0, 77), (0.5, 76), (1, 74), (2, 72), (3, 69)]}
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
    if SONG and SONG[0] / FPS - 0.01 <= t0 < SONG[1] / FPS:
        for b, m in smel.get(ch, mel[ch]):
            add(music, marimba(m, 0.45), t0 + b * BEAT, 0.24, pan=0.1)
            add(music, glock(m + 12, 0.4), t0 + b * BEAT, 0.05, pan=-0.1)
    else:
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


def _tail(sig, sec, fade=0.03):
    n = int(sec * SR)
    out = sig[:n].copy()
    k = int(fade * SR)
    out[-k:] *= np.linspace(1, 0, k)
    return out


def bell():
    n = int(1.8 * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for r, a, d in ((1, 1, 2.2), (2.0, 0.45, 3.2), (2.76, 0.32, 4.5), (4.07, 0.18, 6), (5.4, 0.1, 8)):
        s += a * np.sin(2 * np.pi * 1046 * r * t) * np.exp(-t * d)
    return s * np.minimum(1, t * 900) / 1.6


def drum():
    n = int(0.6 * SR)
    t = np.arange(n) / SR
    f = 92 + 80 * np.exp(-t * 30)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    s += 0.25 * S.lp(S.rng.uniform(-1, 1, n), 1200) * np.exp(-t * 45)
    return s * np.minimum(1, t * 1200)


def snore(soft=False):
    n = int(1.4 * SR)
    t = np.arange(n) / SR
    e = np.sin(np.pi * t / 1.4) ** 1.5
    puls = 0.55 + 0.45 * np.sin(2 * np.pi * 32 * t) ** 8
    s = S.lp(S.rng.uniform(-1, 1, n), 420) * 2.5 * puls + 0.5 * np.sin(2 * np.pi * np.cumsum(80 + 20 * t) / SR) * puls
    s *= e
    return S.lp(s, 260) * 0.5 if soft else s


def drip():
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    f = 900 + 900 * (t / 0.06).clip(0, 1)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 32) * np.minimum(1, t * 2000)


def rain():
    n = int(6.0 * SR)
    t = np.arange(n) / SR
    s = 0.18 * S.hp(S.lp(S.rng.uniform(-1, 1, n), 3500), 500)
    for k in range(140):
        i = int(S.rng.uniform(0, 5.85) * SR)
        m = int(S.rng.uniform(78, 92))
        g = marimba(m, 0.05) * S.rng.uniform(0.05, 0.16)
        s[i:i + len(g)] += g
    return s * np.clip(t / 0.5, 0, 1) * np.clip((6.0 - t) / 0.5, 0, 1)


def roar():
    n = int(1.1 * SR)
    t = np.arange(n) / SR
    f = 95 * (1 + 0.08 * np.sin(2 * np.pi * 5 * t)) * (1 - 0.15 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = sum(np.sin(k * ph) / k for k in range(1, 9))
    s = S.lp(s + 0.4 * S.lp(S.rng.uniform(-1, 1, n), 500), 700)
    return s * np.sin(np.pi * t / 1.1) ** 1.2 * 0.6


def meow():
    n = int(0.75 * SR)
    t = np.arange(n) / SR
    u = t / 0.75
    f = 520 + 380 * np.sin(np.pi * np.clip(u * 1.3, 0, 1)) ** 1.5 - 120 * u
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)
    return S.lp(s, 3000) * np.sin(np.pi * u) ** 0.8 * 0.6


SFX = {"pop": lambda: pop(), "boing": lambda: boing(170), "boing_up": lambda: boing(260, 0.35, up=True), "splat": lambda: splat(),
       "sparkle": lambda: sparkle(88), "popper": lambda: popper(), "bip": lambda: bip(88),
       "whistle_down": lambda: slide_whistle(1400, 400, 0.5), "whistle_up": lambda: slide_whistle(500, 1500, 0.5),
       "clonk": lambda: S.lp(kick(), 1500), "tock": lambda: tock(),
       "bell": lambda: bell(), "bell_cut": lambda: _tail(bell(), 0.48), "drum": lambda: drum(), "drum_cut": lambda: _tail(drum(), 0.16),
       "snore": lambda: snore(), "snore_soft": lambda: snore(True), "snore_cut": lambda: _tail(snore(), 0.85, 0.06), "drip": lambda: drip(), "rain": lambda: rain(),
       "roar": lambda: roar(), "meow": lambda: meow()}
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
