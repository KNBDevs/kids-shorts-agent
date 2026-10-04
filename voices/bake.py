import os, sys, json, subprocess
import numpy as np
from scipy.io import wavfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path[:0] = [ROOT, HERE]
from cast import PROFILES, BASE_TEXT, lines, digest
OUT = os.path.join(ROOT, "assets", "vo")
TMP = os.path.join(ROOT, "_bake")
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
EQ = {
    "bright": "equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=3",
    "warm": "equalizer=f=220:t=q:w=1:g=1.5,equalizer=f=3000:t=q:w=1:g=1",
    "soft": "equalizer=f=3500:t=q:w=1:g=-1,lowpass=f=9000",
    "robot": "equalizer=f=1800:t=q:w=1:g=3",
    "nasal": "equalizer=f=1100:t=q:w=0.8:g=4,equalizer=f=180:t=q:w=1:g=2",
}


def write(p, sr, x):
    x = np.asarray(x, dtype=np.float32).flatten()
    x = x / (np.abs(x).max() + 1e-9) * 0.9
    wavfile.write(p, sr, (x * 32767).astype(np.int16))


def ff(src, dst, af):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", af, "-ac", "1", "-ar", "44100", dst], check=True)


def dur(p):
    sr, x = wavfile.read(p)
    return len(x) / sr


def main(chars):
    import torch
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    base = os.path.join(TMP, "base.wav")
    torch.manual_seed(7)
    write(base, m.sr, m.generate(BASE_TEXT, language_id="es", exaggeration=0.6, cfg_weight=0.45).squeeze().numpy())
    todo = {k: v for k, v in lines().items() if v["char"] in chars}
    man = {}
    for cid in chars:
        p = PROFILES[cid]
        ref = os.path.join(TMP, f"ref_{cid}.wav")
        ff(base, ref, f"rubberband=pitch={p['ref_pitch']}:formant=shifted:pitchq=quality")
        for key, e in todo.items():
            if e["char"] != cid:
                continue
            torch.manual_seed(sum(map(ord, key)))
            raw = os.path.join(TMP, f"{key}_raw.wav")
            w = m.generate(e["text"], language_id="es", audio_prompt_path=ref, exaggeration=p["exag"],
                           cfg_weight=p["cfg"], temperature=p["temp"])
            write(raw, m.sr, w.squeeze().numpy())
            trim = "silenceremove=start_periods=1:start_threshold=-42dB,areverse,silenceremove=start_periods=1:start_threshold=-42dB,areverse"
            mid = os.path.join(TMP, f"{key}_trim.wav")
            ff(raw, mid, trim)
            tempo = p["tempo"]
            d = dur(mid) / tempo
            if d > e["max"]:
                tempo = min(tempo * d / e["max"], tempo * 1.25)
            af = (f"rubberband=pitch={p['post_pitch']}:tempo={tempo:.3f}:formant=shifted:pitchq=quality,"
                  f"highpass=f=90,{EQ[p['eq']]},acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80,"
                  f"afade=t=in:d=0.01,areverse,afade=t=in:d=0.04,areverse")
            final = os.path.join(OUT, f"{key}.wav")
            ff(mid, final, af)
            man[key] = {"hash": digest(e), "dur": round(dur(final), 2), "text": e["text"]}
            print(key, man[key]["dur"], e["text"], flush=True)
    json.dump(man, open(os.path.join(OUT, f"manifest_{'_'.join(chars)}.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(sys.argv[1].split(","))
