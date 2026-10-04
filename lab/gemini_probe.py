import os, json, base64, urllib.request, wave, time, sys
KEY = os.environ["GEMINI_API_KEY"]
B = "https://generativelanguage.googleapis.com/v1beta"
req = urllib.request.Request(f"{B}/models?pageSize=200", headers={"x-goog-api-key": KEY})
models = [m["name"] for m in json.load(urllib.request.urlopen(req))["models"] if "tts" in m["name"]]
print("TTS models:", models)
os.makedirs("lab_out", exist_ok=True)
TESTS = {
    "pimo": ("Puck", "Voz de niño pequeño, curioso y alegre, con acento castellano de España, natural y expresivo"),
    "luma": ("Leda", "Voz de niña pequeña muy alegre y risueña, acento castellano de España, cálida y expresiva"),
    "gruno": ("Algenib", "Voz de villano cómico de dibujos animados, presumido y teatral, nada aterrador, acento castellano de España"),
}
LINES = {
    "pimo": "¡Hola! ¡Soy Pimo! ¡Encantado! ¿Sabes qué me encanta? ¡Preguntar! ¿Por qué? ¿Y por qué?",
    "luma": "¡Hola a todos! ¡Soy Luma, encantada! Cuando sonrío... ¡brillo muchísimo! ¿Lo ves?",
    "gruno": "Vaya, vaya, vaya... ¡Soy el Doctor Gruño! ¡El inventor más genial del mundo mundial!",
}
for model in [m.split("/")[-1] for m in models][:2]:
    for c, (voice, style) in TESTS.items():
        body = {"contents": [{"parts": [{"text": f"{style}. Lee esto:\n{LINES[c]}"}]}],
                "generationConfig": {"responseModalities": ["AUDIO"],
                                     "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
        r = urllib.request.Request(f"{B}/models/{model}:generateContent", data=json.dumps(body).encode(),
                                   headers={"x-goog-api-key": KEY, "Content-Type": "application/json"})
        try:
            d = json.load(urllib.request.urlopen(r, timeout=120))
            pcm = base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
            with wave.open(f"lab_out/{model}_{c}.wav", "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
            print("ok", model, c, len(pcm) / 48000)
        except urllib.error.HTTPError as e:
            print("ERR", model, c, e.code, e.read()[:400])
        time.sleep(22)
