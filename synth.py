import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
SR = 44100
FPS = 24
T = 0
rng = np.random.default_rng(3)

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
    N = len(buf)
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
