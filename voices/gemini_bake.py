import os, sys, json, base64, time, urllib.request, urllib.error, subprocess, difflib, re, unicodedata
import numpy as np
from scipy.io import wavfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path[:0] = [ROOT, HERE]
from cast import lines
KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = os.environ.get("TTS_MODEL", "gemini-2.5-flash-preview-tts")
B = "https://generativelanguage.googleapis.com/v1beta"
OUT = os.path.join(ROOT, "assets", "vo")
TMP = os.path.join(ROOT, "_bake")
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
from gvoices import ACC, VOICES, VERSION, digest
from lock import conform, profiles, LOCK


def reg(c):
    f = profiles()[c]["f0"]
    r = "agudo" if f > 240 else ("medio" if f > 170 else "grave")
    return f"siempre con el mismo tono {r} y el mismo timbre de su presentación, sin cambiar de registro"


BUDGET = [int(os.environ.get("MAX_REQ", "12"))]


def tts(prompt, voice, speakers=None):
    if BUDGET[0] <= 0:
        raise RuntimeError("budget")
    if speakers:
        sc = {"multiSpeakerVoiceConfig": {"speakerVoiceConfigs": [
            {"speaker": n, "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": v}}} for n, v in speakers]}}
    else:
        sc = {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": sc}}
    for attempt in range(3):
        BUDGET[0] -= 1
        r = urllib.request.Request(f"{B}/models/{MODEL}:generateContent", data=json.dumps(body).encode(),
                                   headers={"x-goog-api-key": KEY, "Content-Type": "application/json"})
        try:
            d = json.load(urllib.request.urlopen(r, timeout=180))
            pcm = base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
            time.sleep(21)
            return np.frombuffer(pcm, dtype=np.int16).astype(np.float64) / 32768, 24000
        except urllib.error.HTTPError as e:
            print("http", e.code, e.read()[:300], flush=True)
            if e.code == 429 and attempt >= 1:
                raise RuntimeError("quota")
            time.sleep(40 * (attempt + 1))
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
    for k, v in {"10": " diez ", "1": " uno ", "2": " dos ", "3": " tres ", "4": " cuatro ", "5": " cinco ", "6": " seis ", "7": " siete ", "8": " ocho ", "9": " nueve "}.items():
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
    h = int(sr2 * 0.01)
    en = np.array([np.sqrt(np.mean((y[i:i + h] / 32768.0) ** 2)) for i in range(0, len(y) - h, h)])
    on = np.where(en > en.max() * 0.06)[0]
    if len(on):
        y = y[max(0, (on[0] - 5) * h):min(len(y), (on[-1] + 20) * h)]
        wavfile.write(final, sr2, y)
    st = conform(final, e["char"])
    if st is None:
        print("pitch drift, reject", key, flush=True)
        sc = 0.0
    else:
        sr2, y = wavfile.read(final)
    return {"hash": digest(e["char"], e["text"]), "dur": round(len(y) / sr2, 2), "text": e["text"], "asr": round(sc, 2),
            "heard": heard.strip(), "engine": "gemini", "voice": VOICES[e["char"]][0], "lock": LOCK, "shift": st}


PAIRS = [("pimo", "luma"), ("ruki", "moki"), ("tuki", "bolita"), ("bopi", "gruno")]
NAMES = {"pimo": "Pimo", "luma": "Luma", "ruki": "Ruki", "moki": "Moki", "tuki": "Tuki", "bolita": "Bolita", "bopi": "Bopi", "gruno": "Gruno"}


def pending(man, allL, cid):
    todo = [(k, e) for k, e in allL.items() if e["char"] == cid and man.get(k, {}).get("hash") != digest(cid, e["text"])]
    uniq = []
    for k, e in todo:
        if e["text"] not in [u[1]["text"] for u in uniq]:
            uniq.append((k, e))
    return todo, uniq


def store(man, todo, results):
    for k, e in todo:
        if e["text"] not in results:
            continue
        src_k, res = results[e["text"]]
        if res["asr"] < 0.7:
            continue
        if src_k != k:
            subprocess.run(["cp", os.path.join(OUT, f"{src_k}.wav"), os.path.join(OUT, f"{k}.wav")], check=True)
        man[k] = dict(res)


def run_group(cids, man, allL, asr):
    jobs = {c: pending(man, allL, c) for c in cids}
    seq = [(c, k, e) for c in cids for k, e in jobs[c][1]]
    if not seq:
        return
    if len(cids) == 2:
        order = []
        a, b = [[x for x in seq if x[0] == c] for c in cids]
        while a or b:
            if a: order.append(a.pop(0))
            if b: order.append(b.pop(0))
        seq = order
        styles = " ".join(f"{NAMES[c]}: {VOICES[c][1]}, {reg(c)}." for c in cids)
        script = "\n".join(f"{NAMES[c]}: {e['text']}" for c, k, e in seq)
        prompt = (f"Lee este guion de un dibujo animado infantil. {styles} Cada frase con naturalidad y emoción, "
                  f"y una pausa de dos segundos entre frase y frase.\n\n{script}")
        x, sr = tts(prompt, None, [(NAMES[c], VOICES[c][0]) for c in cids])
    else:
        c = cids[0]
        script = "\n".join(f"{e['text']}" for _, k, e in seq)
        prompt = (f"{VOICES[c][1]}, {reg(c)}. Lee las siguientes frases en orden, con naturalidad y emoción, "
                  f"haciendo una pausa de dos segundos entre cada frase.\n\n{script}")
        x, sr = tts(prompt, VOICES[c][0])
    parts = split(x, sr, len(seq))
    if parts is None:
        print("split failed", cids, flush=True)
        return False
    results = {c: {} for c in cids}
    for (c, k, e), seg in zip(seq, parts):
        res = finish(seg, sr, k, e, asr)
        results[c][e["text"]] = (k, res)
        print(c, k, res["dur"], res["asr"], "|", e["text"], "|", res["heard"], flush=True)
    for c in cids:
        store(man, jobs[c][0], results[c])
    return all(r["asr"] >= 0.7 for c in cids for _, r in results[c].values())


def main(chars):
    from faster_whisper import WhisperModel
    asr = WhisperModel("small", device="cpu", compute_type="int8")
    mp = os.path.join(OUT, "manifest.json")
    man = json.load(open(mp)) if os.path.exists(mp) else {}
    allL = lines()
    groups = [p for p in PAIRS if p[0] in chars and p[1] in chars]
    done = {c for p in groups for c in p}
    groups += [(c,) for c in chars if c not in done]
    try:
        for g in groups:
            ok = run_group(list(g), man, allL, asr)
            json.dump(man, open(mp, "w"), ensure_ascii=False, indent=1)
            if ok is False and len(g) == 2:
                for c in g:
                    run_group([c], man, allL, asr)
                    json.dump(man, open(mp, "w"), ensure_ascii=False, indent=1)
    except RuntimeError as e:
        print("stopped:", e, flush=True)
    json.dump(man, open(mp, "w"), ensure_ascii=False, indent=1)
    missing = [k for k, e in allL.items() if man.get(k, {}).get("hash") != digest(e["char"], e["text"])]
    print("missing", len(missing), missing, flush=True)
    open(os.path.join(ROOT, "_missing.txt"), "w").write(str(len(missing)))


if __name__ == "__main__":
    main(sys.argv[1].split(","))
