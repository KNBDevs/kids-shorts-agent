import os, sys, json, glob, subprocess
import numpy as np
from scipy.io import wavfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VO = os.path.join(ROOT, "assets", "vo")
PROFILES = os.path.join(HERE, "profiles.json")
LOCK = "L1"
MAX_SHIFT = 7.0
TOL = 0.4


def f0_track(y, sr):
    y = y.astype(np.float64)
    if y.ndim > 1:
        y = y.mean(1)
    y /= np.abs(y).max() + 1e-9
    n, hop = int(0.04 * sr), int(0.01 * sr)
    lo, hi = int(sr / 600), int(sr / 70)
    w = np.hanning(n)
    out = []
    for i in range(0, len(y) - n, hop):
        f = y[i:i + n] * w
        if np.sqrt(np.mean(f ** 2)) < 0.05:
            continue
        ac = np.correlate(f, f, "full")[n - 1:]
        ac /= ac[0] + 1e-9
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] > 0.5:
            out.append(sr / k)
    return np.array(out)


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


def conform(path, char):
    """Shift a baked line so its median pitch matches the character's locked reference.
    Returns semitone offset measured before correction, or None if out of range (reject)."""
    ref = profiles()[char]["f0"]
    t = f0_file(path)
    if len(t) < 5:
        return 0.0
    st = 12 * np.log2(np.median(t) / ref)
    if abs(st) > MAX_SHIFT:
        return None
    cur = st
    for _ in range(2):
        if abs(cur) <= TOL:
            break
        ratio = 2 ** (-cur / 12)
        tmp = path + ".tmp.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-af",
                        f"rubberband=pitch={ratio:.5f}:formant=preserved:pitchq=quality", "-ac", "1", tmp], check=True)
        os.replace(tmp, path)
        t = f0_file(path)
        cur = 12 * np.log2(np.median(t) / ref) if len(t) >= 5 else 0.0
    return round(float(st), 2)


def apply_all():
    mp = os.path.join(VO, "manifest.json")
    man = json.load(open(mp))
    prof = profiles()
    for k, e in sorted(man.items()):
        if k.startswith("hola_") or e.get("lock") == LOCK:
            continue
        p = os.path.join(VO, f"{k}.wav")
        c = char_of(k)
        if not c or not os.path.exists(p):
            continue
        st = conform(p, c)
        if st is None:
            print("REJECT", k, flush=True)
            e["hash"] = "rejected"
            continue
        e["lock"] = LOCK
        e["shift"] = st
        print(k, c, st, flush=True)
    json.dump(man, open(mp, "w"), ensure_ascii=False, indent=1)


def char_of(key):
    sys.path[:0] = [ROOT, HERE]
    from cast import lines
    e = lines().get(key)
    return e["char"] if e else None


if __name__ == "__main__":
    if sys.argv[1:] == ["build"]:
        print(json.dumps(build(["pimo", "ruki", "luma", "tuki", "moki", "bopi", "bolita", "gruno"]), indent=1))
    else:
        apply_all()
