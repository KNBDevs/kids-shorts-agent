import os, sys, json, base64, time, urllib.request, urllib.error, subprocess, difflib, re, unicodedata
import numpy as np
from scipy.io import wavfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path[:0] = [ROOT, HERE]
from cast import lines
KEY = os.environ["GEMINI_API_KEY"]
MODEL = os.environ.get("TTS_MODEL", "gemini-2.5-flash-preview-tts")
B = "https://generativelanguage.googleapis.com/v1beta"
OUT = os.path.join(ROOT, "assets", "vo")
TMP = os.path.join(ROOT, "_bake")
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
ACC = "con acento castellano de España (nada latinoamericano), dicción clara y natural, para un dibujo animado infantil"
VOICES = {
    "pimo": ("Puck", "Voz de niño pequeño, curioso y alegre, " + ACC),
    "ruki": ("Umbriel", "Voz de niño tranquilo y sereno, habla pausado y amable, " + ACC),
    "luma": ("Leda", "Voz de niña pequeña muy alegre y risueña, cálida y expresiva, " + ACC),
    "tuki": ("Fenrir", "Voz de niño travieso y lleno de energía, rápido y juguetón, " + ACC),
    "moki": ("Enceladus", "Voz de niño soñador, suave, dulce y algo soñolienta, " + ACC),
    "bopi": ("Iapetus", "Voz de robot pequeño y simpático, precisa, ordenada y algo entrecortada, " + ACC),
    "bolita": ("Zephyr", "Voz de niña valiente, impulsiva y entusiasta, muy enérgica, " + ACC),
    "gruno": ("Algenib", "Voz de villano cómico de dibujos animados, presumido, teatral y pícaro, nunca aterrador, " + ACC),
}
VERSION = "g1"


def digest(cid, text):
    import hashlib
    return hashlib.sha1((VERSION + cid + VOICES[cid][0] + VOICES[cid][1] + text).encode()).hexdigest()[:12]


def tts(prompt, voice):
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    for attempt in range(6):
        r = urllib.request.Request(f"{B}/models/{MODEL}:generateContent", data=json.dumps(body).encode(),
                                   headers={"x-goog-api-key": KEY, "Content-Type": "application/json"})
        try:
            d = json.load(urllib.request.urlopen(r, timeout=180))
            pcm = base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
            time.sleep(21)
            return np.frombuffer(pcm, dtype=np.int16).astype(np.float64) / 32768, 24000
        except urllib.error.HTTPError as e:
            print("http", e.code, e.read()[:300], flush=True)
            time.sleep(30 * (attempt + 1))
        except Exception as e:
            print("err", e, flush=True)
            time.sleep(20)
    raise RuntimeError("tts failed")


def split(x, sr, n):
    hop = int(0.02 * sr)
    e = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2) + 1e-12) for i in range(0, len(x) - hop, hop)])
    th = max(e.max() * 0.03, 1e-4)
    sil = e < th
    gaps, i = [], 0
    while i < len(sil):
        if sil[i]:
            j = i
            while j < len(sil) and sil[j]:
                j += 1
            if i > 0 and j < len(sil):
                gaps.append((j - i, i, j))
            i = j
        else:
            i += 1
    gaps = sorted(sorted(gaps, reverse=True)[:n - 1], key=lambda g: g[1])
    if len(gaps) != n - 1 or any(g[0] * 0.02 < 0.3 for g in gaps):
        return None
    cuts = [0] + [((g[1] + g[2]) // 2) * hop for g in gaps] + [len(x)]
    return [x[cuts[k]:cuts[k + 1]] for k in range(n)]


def norm(t):
    t = t.lower()
    for k, v in {"1": " uno ", "2": " dos ", "3": " tres "}.items():
        t = t.replace(k, v)
    t = "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-zñ ]+", " ", t).split()


def finish(seg, sr, key, e, asr):
    raw = os.path.join(TMP, f"{key}.wav")
    wavfile.write(raw, sr, (seg / (np.abs(seg).max() + 1e-9) * 0.9 * 32767).astype(np.int16))
    segs, _ = asr.transcribe(raw, language="es", beam_size=3, word_timestamps=True)
    segs = list(segs)
    heard = " ".join(s.text for s in segs)
    words = [w for s in segs for w in (s.words or [])]
    sc = difflib.SequenceMatcher(None, norm(e["text"]), norm(heard)).ratio()
    a0, a1 = (max(0, words[0].start - 0.08), words[-1].end + 0.25) if words else (0, len(seg) / sr)
    d = a1 - a0
    tempo = min(max(d / e["max"], 1.0), 1.2)
    af = (f"atrim={a0:.3f}:{a1:.3f},asetpts=PTS-STARTPTS,atempo={tempo:.3f},highpass=f=80,"
          f"acompressor=threshold=-20dB:ratio=2:attack=5:release=90,afade=t=in:d=0.01,areverse,afade=t=in:d=0.05,areverse")
    final = os.path.join(OUT, f"{key}.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", af, "-ar", "44100", "-ac", "1", final], check=True)
    sr2, y = wavfile.read(final)
    return {"hash": digest(e["char"], e["text"]), "dur": round(len(y) / sr2, 2), "text": e["text"], "asr": round(sc, 2),
            "heard": heard.strip(), "engine": "gemini", "voice": VOICES[e["char"]][0]}


def main(chars):
    from faster_whisper import WhisperModel
    asr = WhisperModel("small", device="cpu", compute_type="int8")
    mp = os.path.join(OUT, "manifest.json")
    man = json.load(open(mp)) if os.path.exists(mp) else {}
    allL = lines()
    for cid in chars:
        voice, style = VOICES[cid]
        todo = [(k, e) for k, e in allL.items() if e["char"] == cid and man.get(k, {}).get("hash") != digest(cid, e["text"])]
        uniq = []
        for k, e in todo:
            if e["text"] not in [u[1]["text"] for u in uniq]:
                uniq.append((k, e))
        if not uniq:
            continue
        script = "\n".join(f"{i + 1}. {e['text']}" for i, (k, e) in enumerate(uniq))
        prompt = (f"{style}. Lee las siguientes frases en orden, con naturalidad y emoción, "
                  f"haciendo una pausa de dos segundos entre cada frase. No leas los números.\n\n{script}")
        x, sr = tts(prompt, voice)
        parts = split(x, sr, len(uniq))
        results = {}
        for i, (k, e) in enumerate(uniq):
            seg = parts[i] if parts else None
            res = finish(seg, sr, k, e, asr) if seg is not None else None
            if res is None or res["asr"] < 0.7:
                print("retry single", k, res and res["heard"], flush=True)
                y, sr1 = tts(f"{style}. Di con naturalidad y emoción: {e['text']}", voice)
                res = finish(y, sr1, k, e, asr)
            results[e["text"]] = (k, res)
            print(cid, k, res["dur"], res["asr"], "|", e["text"], "|", res["heard"], flush=True)
        for k, e in todo:
            src_k, res = results[e["text"]]
            if src_k != k:
                subprocess.run(["cp", os.path.join(OUT, f"{src_k}.wav"), os.path.join(OUT, f"{k}.wav")], check=True)
            man[k] = dict(res)
        json.dump(man, open(mp, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(sys.argv[1].split(","))
