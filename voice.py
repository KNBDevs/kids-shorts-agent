import os, sys, subprocess
import numpy as np
from scipy.io import wavfile
from synth import SR, lp
HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.environ.get('VOICE_MODEL', os.path.join(HERE, 'es-carlfm-x-low.onnx'))
TMP = os.path.join(HERE, '_vo')
os.makedirs(TMP, exist_ok=True)

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
