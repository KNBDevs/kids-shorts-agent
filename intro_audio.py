import os, sys, subprocess
import numpy as np
from scipy.io import wavfile
import synth as S
from synth import SR, ft, add, glock, marimba, pluck, bass, kick, clap, shaker, slide_whistle, boing, splat, sparkle, pop, bip, popper, reverb, lp, hp, env_adsr
from intro_plan import *
HERE = os.path.dirname(os.path.abspath(__file__))
DUR = TOTAL / FPS
N = int(SR * DUR)
BPM = 120
BEAT = 60 / BPM
MODEL = os.environ.get('VOICE_MODEL', os.path.join(HERE, 'es-carlfm-x-low.onnx'))
TMP = os.path.join(HERE, '_vo')
os.makedirs(TMP, exist_ok=True)
MAX_LINE = 2.45

def tts(text, key, pitch=1.4, tempo=1.08, robot=False, max_len=None):
    src = os.path.join(TMP, f'{key}.wav')
    dst = os.path.join(TMP, f'{key}_c.wav')
    subprocess.run([sys.executable, '-m', 'piper', '-m', MODEL, '-f', src], input=text.encode(), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sr0, raw = wavfile.read(src)
    raw_len = len(raw) / sr0
    if max_len:
        tempo = max(tempo, raw_len / max_len)
    af = f'silenceremove=start_periods=1:start_threshold=-45dB,rubberband=pitch={pitch}:tempo={tempo:.3f},highpass=f=130,acompressor=threshold=-18dB:ratio=3,aresample={SR}'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-af', af, '-ac', '1', dst], check=True)
    _, v = wavfile.read(dst)
    v = v.astype(np.float64) / 32768
    if robot:
        t = np.arange(len(v)) / SR
        v = 0.55 * v + 0.45 * v * np.sin(2 * np.pi * 70 * t)
        v = np.round(v * 24) / 24
        v = lp(v, 6000)
    return v / (np.abs(v).max() + 1e-09)

def chorus(text, key, pitches, tempo=1.1):
    parts = [tts(text, f'{key}{i}', p, tempo) for i, p in enumerate(pitches)]
    n = max((len(p) for p in parts))
    out = np.zeros(n)
    for p in parts:
        out[:len(p)] += p
    return out / (np.abs(out).max() + 1e-09)
music = np.zeros((N, 2))
drums = np.zeros((N, 2))
chords = {'C': [60, 64, 67], 'G': [55, 59, 62], 'Am': [57, 60, 64], 'F': [53, 57, 60], 'Dm': [50, 53, 57]}
roots = {'C': 36, 'G': 43, 'Am': 45, 'F': 41, 'Dm': 38}
prog = ['C', 'G', 'Am', 'F'] * 3 + ['Dm', 'G', 'C']
mel = {'C': [(0, 79), (1, 76), (1.5, 77), (2, 79), (3, 84)], 'G': [(0, 83), (1, 79), (2, 74), (2.5, 76), (3, 77)], 'Am': [(0, 76), (0.5, 77), (1, 76), (2, 72), (3, 69)], 'F': [(0, 72), (1, 74), (1.5, 76), (2, 77), (3, 81)], 'Dm': [(0, 77), (1, 74), (2, 72), (3, 74)]}
GRU_T0, GRU_T1 = (ft(GRUNO - 4), ft(GRUNO + 30))
for bar, ch in enumerate(prog):
    t0 = bar * 4 * BEAT
    if t0 >= DUR:
        break
    r = roots[ch]
    for b, m in [(0, r), (1.5, r), (2, r + 7), (3, r + 12), (3.5, r + 7)]:
        add(music, bass(m, 0.35), t0 + b * BEAT, 0.4)
    for b in (0.5, 1.5, 2.5, 3.5):
        for k, m in enumerate(chords[ch]):
            add(music, pluck(m + 12, 0.42, 0.6), t0 + b * BEAT + k * 0.008, 0.09, pan=-0.3)
    for b, m in mel[ch]:
        add(music, glock(m, 0.6), t0 + b * BEAT, 0.13, pan=0.2)
    for b in range(4):
        add(drums, kick(), t0 + b * BEAT, 0.5 if b % 2 == 0 else 0.22)
        if b % 2:
            add(drums, clap(), t0 + b * BEAT, 0.14)
        for h in (0, 0.5):
            add(drums, shaker(), t0 + (b + h) * BEAT + 0.01, 0.03 if h else 0.018, pan=0.4)
music = reverb(music, 1.3, 0.28) + drums
tt = np.arange(N) / SR
gate = np.clip(np.minimum((GRU_T0 - tt) / 0.15 + 1, (tt - GRU_T1) / 0.4), 0.12, 1)
gate[tt < GRU_T0 - 0.2] = 1
music *= gate[:, None]
music *= np.clip((DUR - tt) / 0.6, 0, 1)[:, None]
sfx = np.zeros((N, 2))
add(sfx, popper(), ft(2), 0.32)
add(sfx, sparkle(88), ft(3), 0.22)
for i, c in enumerate(CAST):
    s0 = c['start']
    add(sfx, slide_whistle(1600, 500, ft(9)), ft(s0), 0.16)
    add(sfx, boing(150 + 18 * i), ft(s0 + 8), 0.4)
    add(sfx, splat(), ft(s0 + 8), 0.2)
    add(sfx, pop(), ft(s0 + 10), 0.28)
    add(sfx, sparkle(84 + [0, 2, 4, 5, 7, 9, 11][i]), ft(s0 + 11), 0.14, pan=0.15)
    add(sfx, boing(260, 0.35, up=True), ft(s0 + 53), 0.22)
    add(sfx, bip(84 + i % 5), ft(s0 + 66), 0.15)
add(sfx, popper(), ft(GROUP + 16), 0.38)
add(sfx, sparkle(91), ft(GROUP + 16), 0.25)
for i in range(len(CAST)):
    add(sfx, bip(84 + 2 * i), ft(GROUP + 18 + i * 3), 0.1)

def sting():
    out = np.zeros(int(2.0 * SR))
    for k, (m, d) in enumerate([(41, 0.28), (40, 0.28), (39, 0.9)]):
        n = int(d * SR)
        t = np.arange(n) / SR
        f = S.mtof(m)
        s = np.sign(np.sin(2 * np.pi * f * t)) * 0.4 + np.sin(2 * np.pi * f * t) + 0.5 * np.sin(4 * np.pi * f * t)
        s = lp(s, 1200) * env_adsr(n, 0.01, 0.08, 0.8, 0.12) * (1 + 0.15 * np.sin(2 * np.pi * 6 * t) * (k == 2))
        i0 = int(k * 0.3 * SR)
        out[i0:i0 + n] += s
    return out
add(sfx, slide_whistle(300, 900, 0.45), ft(GRUNO), 0.15)
add(sfx, sting(), ft(GRUNO + 4), 0.45)
for k in range(3):
    add(sfx, boing(240 + 30 * k, 0.3), ft(GRUNO + 34 + k), 0.12)
add(sfx, pop(), ft(SUBSCRIBE), 0.3)
add(sfx, sparkle(96), ft(SUBSCRIBE + 1), 0.22)
voice = np.zeros((N, 2))
pans = [-0.25, -0.1, 0.1, 0.25, -0.18, 0.0, 0.18]
add(voice, chorus('¡Hola!', 'hook', [1.35, 1.55, 1.7], 1.0), ft(4), 0.75)
for i, c in enumerate(CAST):
    v = c['voice']
    s = tts(c['line'], c['id'], v['pitch'], v['tempo'], v.get('robot', False), max_len=MAX_LINE)
    add(voice, s, ft(c['start'] + 12), 0.85, pan=pans[i])
add(voice, chorus(GROUP_LINE['text'], 'group', [1.3, 1.45, 1.6, 1.75], 1.1), ft(GROUP_LINE['frame']), 0.85)
gv = GRUNO_LINE['voice']
add(voice, tts(GRUNO_LINE['text'], 'gruno', gv['pitch'], gv['tempo'], max_len=1.9), ft(GRUNO_LINE['frame']), 0.9, pan=0.15)
add(voice, chorus(SUBSCRIBE_LINE['text'], 'sub', [1.4, 1.62], 1.1), ft(SUBSCRIBE_LINE['frame']), 0.85)
env = np.convolve(np.abs(voice[:, 0]), np.ones(2205) / 2205, 'same')
duck = 1 - 0.68 * np.clip(env / (env.max() + 1e-09) * 4, 0, 1)
mix = music * duck[:, None] * 0.62 + sfx * (0.55 + 0.45 * duck)[:, None] + voice * 1.25
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix /= np.abs(mix).max() / 0.89
wavfile.write(os.path.join(HERE, 'soundtrack.wav'), SR, (mix * 32767).astype(np.int16))
print('ok', mix.shape)
