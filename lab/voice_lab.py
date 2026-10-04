import os, sys, subprocess, json, traceback
import numpy as np
from scipy.io import wavfile
ENGINE = sys.argv[1]
OUT = os.path.join("lab_out", ENGINE)
os.makedirs(OUT, exist_ok=True)
LINES = [
    ("pimo", "¡Hola! Soy Pimo. ¡Me encanta preguntar! ¿Por qué? ¿Y por qué?"),
    ("luma", "¡Hola, hola! ¡Soy Luma! ¡Cuando sonrío, brillo un montón!"),
    ("ruki", "Hola, soy Ruki. Cuando me enfado, respiro hondo... ¡así!"),
    ("gruno", "¡Je, je! ¡Soy el Doctor Gruño! ¡Ya veréis, Pimoruki!"),
]


def save(name, sr, x):
    x = np.asarray(x, dtype=np.float32).flatten()
    x = x / (np.abs(x).max() + 1e-9) * 0.9
    wavfile.write(os.path.join(OUT, f"{name}.wav"), sr, (x * 32767).astype(np.int16))


if ENGINE.startswith("piper"):
    model, spk = {"piper_sharvard_f": ("es_ES-sharvard-medium.onnx", "1"), "piper_sharvard_m": ("es_ES-sharvard-medium.onnx", "0"),
                  "piper_davefx": ("es_ES-davefx-medium.onnx", "0")}[ENGINE]
    for n, t in LINES:
        p = os.path.join(OUT, f"{n}.wav")
        subprocess.run([sys.executable, "-m", "piper", "-m", model, "-s", spk, "-f", p, "--length-scale", "0.95"], input=t.encode(), check=True)
elif ENGINE.startswith("kokoro"):
    from kokoro import KPipeline
    voice = {"kokoro_dora": "ef_dora", "kokoro_alex": "em_alex", "kokoro_santa": "em_santa"}[ENGINE]
    pipe = KPipeline(lang_code="e")
    for n, t in LINES:
        parts = [a for _, _, a in pipe(t, voice=voice, speed=1.05)]
        save(n, 24000, np.concatenate([np.asarray(a) for a in parts]))
elif ENGINE.startswith("chatterbox"):
    import torch, torchaudio
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    ex = 0.75 if ENGINE == "chatterbox_expr" else 0.5
    for n, t in LINES:
        w = m.generate(t, language_id="es", exaggeration=ex, cfg_weight=0.35)
        save(n, m.sr, w.squeeze().cpu().numpy())
print("done", ENGINE)
