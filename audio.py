import numpy as np, subprocess, os, json, sys
from scipy.signal import fftconvolve, butter, sosfilt
from scipy.io import wavfile
SR = 44100
DUR = 20.0
BPM = 120
BEAT = 60 / BPM
N = int(SR * DUR)
FPS = 24
HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = {'seed': 3, 'transpose': 0, 'words': ['ROJO', 'AZUL', 'AMARILLO', 'VERDE'], 'finale_word': '¡MUY BIEN!', 'outro': '¡Otra vez!'}
_p = os.environ.get('SPEC_FILE')
if _p:
    _s = json.load(open(_p))
    SPEC.update({k: v for k, v in _s.items() if k in SPEC})
    if 'colors' in _s:
        SPEC['words'] = [c['word'] for c in _s['colors']]
rng = np.random.default_rng(SPEC['seed'])
T = int(SPEC['transpose'])
L = [12 + 108 * i for i in range(4)]
J = [l + 84 for l in L[:-1]]
FINALE, J_FINAL = (L[-1] + 48, 444)
HOPS = [l + d for l in L for d in (36, 60)]

def ft(f):
    return f / FPS

def mtof(m):
    return 440 * 2 ** ((m + T - 69) / 12)

def env_adsr(n, a=0.005, d=0.1, s=0.6, r=0.1):
    t = np.arange(n) / SR
    e = np.ones(n) * s
    ai, di = (int(a * SR), int(d * SR))
    ri = int(r * SR)
    e[:ai] = np.linspace(0, 1, max(ai, 1))[:len(e[:ai])]
    e[ai:ai + di] = np.linspace(1, s, max(di, 1))[:len(e[ai:ai + di])]
    if ri:
        e[-ri:] *= np.linspace(1, 0, ri)
    return e

def add(buf, sig, t, gain=1.0, pan=0.0):
    i = int(t * SR) % N
    l, r = (gain * np.sqrt((1 - pan) / 2) * 1.414, gain * np.sqrt((1 + pan) / 2) * 1.414)
    for k in range(0, len(sig), N - i if i else N):
        pass
    idx = (np.arange(len(sig)) + i) % N
    np.add.at(buf[:, 0], idx, sig * l)
    np.add.at(buf[:, 1], idx, sig * r)

def lp(sig, fc, order=2):
    return sosfilt(butter(order, fc, 'low', fs=SR, output='sos'), sig)

def hp(sig, fc, order=2):
    return sosfilt(butter(order, fc, 'high', fs=SR, output='sos'), sig)

def glock(m, dur=0.6):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = mtof(m)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 12) + 0.15 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 25)
    return s * np.exp(-t * 4.5) * np.minimum(1, t * 800)

def marimba(m, dur=0.35):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = mtof(m)
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 40)
    return s * np.exp(-t * 9) * np.minimum(1, t * 600)

def pluck(m, dur=0.5, bright=0.5):
    f = mtof(m)
    p = int(SR / f)
    n = int(dur * SR)
    buf = rng.uniform(-1, 1, p)
    buf = lp(buf, 2000 + 4000 * bright)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.996 * 0.5 * (buf[i % p] + buf[(i + 1) % p])
    return out * np.minimum(1, np.arange(n) / 60)

def bass(m, dur=0.4):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = mtof(m)
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) + 0.12 * np.sign(np.sin(2 * np.pi * f * t))
    return lp(s * env_adsr(n, 0.004, 0.12, 0.55, 0.08), 900)

def kick():
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    f = 50 + 110 * np.exp(-t * 35)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)

def clap():
    n = int(0.22 * SR)
    t = np.arange(n) / SR
    nz = rng.uniform(-1, 1, n)
    e = np.exp(-t * 22) + 0.6 * np.exp(-np.maximum(t - 0.012, 0) * 60) * (t > 0.012)
    return hp(lp(nz, 6000), 900) * e

def shaker():
    n = int(0.07 * SR)
    t = np.arange(n) / SR
    return hp(rng.uniform(-1, 1, n), 6000) * np.exp(-t * 60) * np.minimum(1, t * 300)

def slide_whistle(f0, f1, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / dur) * (1 + 0.01 * np.sin(2 * np.pi * 6 * t))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.1 * rng.uniform(-1, 1, n)
    return lp(s, 4000) * env_adsr(n, 0.02, 0.05, 0.9, 0.05)

def boing(f0=180, dur=0.45, up=False):
    n = int(dur * SR)
    t = np.arange(n) / SR
    if up:
        f = f0 * (1 + 2.2 * (t / dur) ** 0.6)
    else:
        f = f0 * (1 + 0.6 * np.exp(-t * 6)) * (1 + 0.12 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 4))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return s * np.exp(-t * (5 if not up else 6)) * np.minimum(1, t * 400)

def splat():
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    s = lp(rng.uniform(-1, 1, n), 1800) * np.exp(-t * 18)
    for k in range(5):
        d = rng.uniform(0.02, 0.2)
        fb = rng.uniform(600, 1400)
        m = t > d
        s += 0.35 * m * np.sin(2 * np.pi * fb * (1 + 3 * (t - d)) * (t - d)) * np.exp(-(t - d) * 60)
    return s

def sparkle(root=84):
    out = np.zeros(int(0.9 * SR))
    for k, m in enumerate([root, root + 4, root + 7, root + 12, root + 16]):
        g = glock(m, 0.6)
        i = int(k * 0.045 * SR)
        out[i:i + len(g)] += g * (0.9 - k * 0.1)
    return out

def pop():
    n = int(0.08 * SR)
    t = np.arange(n) / SR
    f = 900 * np.exp(-t * 30) + 300
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 50)

def bip(m=88):
    return marimba(m, 0.18)

def popper():
    n = int(0.5 * SR)
    t = np.arange(n) / SR
    return hp(rng.uniform(-1, 1, n), 1500) * (np.exp(-t * 40) + 0.2 * np.exp(-t * 6))

def reverb(sig, size=1.2, mix=0.22):
    n = int(size * SR)
    t = np.arange(n) / SR
    ir = rng.uniform(-1, 1, (n, 2)) * np.exp(-t * 5)[:, None]
    ir[:, 0] = lp(ir[:, 0], 5000)
    ir[:, 1] = lp(ir[:, 1], 5000)
    wet = np.stack([fftconvolve(sig[:, c], ir[:, c])[:len(sig) + n] for c in range(2)], 1)
    out = np.zeros_like(sig)
    out += sig * (1 - mix)
    w = wet[:len(sig)] * mix * 0.12
    out += w
    tail = wet[len(sig):] * mix * 0.12
    out[:len(tail)] += tail
    return out
music = np.zeros((N, 2))
drums = np.zeros((N, 2))
PROGS = [['C', 'G', 'Am', 'F', 'C', 'F', 'G', 'C', 'F', 'G'], ['C', 'F', 'G', 'C', 'Am', 'F', 'G', 'C', 'F', 'G'], ['C', 'Am', 'F', 'G', 'C', 'Am', 'F', 'G', 'F', 'G']]
prog = PROGS[SPEC['seed'] % len(PROGS)]
chords = {'C': [60, 64, 67], 'G': [55, 59, 62], 'Am': [57, 60, 64], 'F': [53, 57, 60]}
roots = {'C': 36, 'G': 43, 'Am': 45, 'F': 41}
motif_a = [(0, 76), (0.5, 76), (1, 79), (2, 76), (2.5, 74), (3, 72)]
motif_b = [(0, 74), (0.5, 74), (1, 77), (2, 74), (2.5, 72), (3, 71)]
mel_bar = {'C': motif_a, 'G': motif_b, 'Am': [(0, 76), (0.5, 72), (1, 69), (2, 72), (3, 76)], 'F': [(0, 77), (0.5, 76), (1, 74), (2, 72), (2.5, 74), (3, 77)]}
for bar, ch in enumerate(prog):
    t0 = bar * 4 * BEAT
    r = roots[ch]
    for b, m in [(0, r), (1.5, r), (2, r + 7), (3, r + 12), (3.5, r + 7)]:
        add(music, bass(m, 0.35), t0 + b * BEAT, 0.42)
    for b in (0.5, 1.5, 2.5, 3.5):
        for k, m in enumerate(chords[ch]):
            add(music, pluck(m + 12, 0.45, 0.6), t0 + b * BEAT + k * 0.008, 0.1, pan=-0.3)
    for b, m in mel_bar[ch]:
        add(music, glock(m, 0.7), t0 + b * BEAT, 0.2, pan=0.2)
        add(music, marimba(m - 12, 0.3), t0 + b * BEAT, 0.1, pan=-0.1)
    for b in range(4):
        add(drums, kick(), t0 + b * BEAT, 0.55 if b % 2 == 0 else 0.25)
        if b % 2:
            add(drums, clap(), t0 + b * BEAT, 0.15)
        for h in (0, 0.5):
            add(drums, shaker(), t0 + (b + h) * BEAT + 0.01, 0.035 if h else 0.02, pan=0.4)
music = reverb(music, 1.3, 0.3)
music += drums
sfx = np.zeros((N, 2))
add(sfx, slide_whistle(1500, 520, 0.48), ft(0), 0.2)
for i, l in enumerate(L):
    add(sfx, boing(150 + 20 * i), ft(l), 0.45)
    add(sfx, splat(), ft(l), 0.28)
    add(sfx, sparkle(84 + [0, 2, 4, 5][i]), ft(l + 1), 0.22, pan=0.15)
    add(sfx, pop(), ft(l + 2), 0.3)
for j in J:
    add(sfx, boing(260, 0.35, up=True), ft(j - 1), 0.3)
for h in HOPS:
    add(sfx, bip(84 + h // 12 % 5), ft(h), 0.18)
for f in range(FINALE, FINALE + 36, 4):
    add(sfx, marimba(84 + (f - FINALE) // 4 * 2, 0.25), ft(f), 0.16)
add(sfx, popper(), ft(FINALE + 38), 0.35)
add(sfx, sparkle(91), ft(FINALE + 38), 0.25)
add(sfx, slide_whistle(500, 1700, 0.6), ft(J_FINAL), 0.22)
voice = np.zeros((N, 2))

def say(txt):
    return '¡' + txt.strip('¡!').capitalize() + '!' if txt.isupper() or not txt.startswith('¡') else txt
model = os.environ.get('VOICE_MODEL', os.path.join(HERE, 'es-carlfm-x-low.onnx'))
lines = [(say(w), L[i] + 3) for i, w in enumerate(SPEC['words'])]
lines += [(say(SPEC['finale_word']), FINALE + 40), (SPEC['outro'], J_FINAL + 14)]
for k, (text, f) in enumerate(lines):
    src = os.path.join(HERE, f'v_{k}.wav')
    dst = os.path.join(HERE, f'vc_{k}.wav')
    subprocess.run([sys.executable, '-m', 'piper', '-m', model, '-f', src], input=text.encode(), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-af', 'silenceremove=start_periods=1:start_threshold=-45dB,rubberband=pitch=1.42:tempo=1.08,highpass=f=140,acompressor=threshold=-18dB:ratio=3,aresample=44100', '-ac', '1', dst], check=True)
    sr, v = wavfile.read(dst)
    v = v.astype(np.float64) / 32768
    v /= np.abs(v).max() + 1e-09
    add(voice, v, ft(f), 0.8)
voice = reverb(voice, 0.6, 0.15)
env = np.abs(voice[:, 0])
env = np.convolve(env, np.ones(2205) / 2205, 'same')
duck = 1 - 0.45 * np.clip(env / (env.max() + 1e-09) * 3, 0, 1)
mix = music * duck[:, None] * 0.85 + sfx + voice
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix /= np.abs(mix).max() / 0.89
wavfile.write(os.path.join(HERE, 'soundtrack.wav'), SR, (mix * 32767).astype(np.int16))
print('ok', mix.shape)
