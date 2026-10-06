import os, sys, json, glob, subprocess
import numpy as np
from scipy.io import wavfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VO = os.path.join(ROOT, "assets", "vo")
PROFILES = os.path.join(HERE, "profiles.json")


def f0_track(y, sr):
    import librosa
    y = y.astype(np.float64)
    if y.ndim > 1:
        y = y.mean(1)
    y /= np.abs(y).max() + 1e-9
    if sr != 22050:
        y = librosa.resample(y, orig_sr=sr, target_sr=22050)
        sr = 22050
    f, v, _ = librosa.pyin(y, fmin=70, fmax=700, sr=sr)
    return f[v & ~np.isnan(f)]


def f0_file(path):
    sr, y = wavfile.read(path)
    return f0_track(y, sr)


def build(chars):
    prof = {}
    for c in chars:
        files = sorted(glob.glob(os.path.join(VO, f"hola_{c}_*.wav")))
        t = np.concatenate([f0_file(p) for p in files])
        prof[c] = {"ref": [os.path.basename(p) for p in files], "f0": round(float(np.median(t)), 1),
                   "p10": round(float(np.percentile(t, 10)), 1), "p90": round(float(np.percentile(t, 90)), 1)}
    json.dump(prof, open(PROFILES, "w"), indent=1)
    return prof


def profiles():
    return json.load(open(PROFILES))


def char_of(key):
    sys.path[:0] = [ROOT, HERE]
    from cast import lines
    e = lines().get(key)
    return e["char"] if e else None


if __name__ == "__main__":
    if sys.argv[1:] == ["build"]:
        print(json.dumps(build(["pimo", "ruki", "luma", "tuki", "moki", "bopi", "bolita", "gruno"]), indent=1))

