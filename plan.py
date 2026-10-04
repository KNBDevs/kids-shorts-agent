import json, os, random, sys, time, urllib.request, hashlib, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, 'state', 'history.json')
COLORS = {'ROJO': [0.9, 0.05, 0.06], 'AZUL': [0.03, 0.22, 0.95], 'AMARILLO': [1.0, 0.72, 0.02], 'VERDE': [0.06, 0.7, 0.12], 'NARANJA': [1.0, 0.3, 0.02], 'MORADO': [0.38, 0.08, 0.85], 'ROSA': [1.0, 0.28, 0.55], 'CELESTE': [0.25, 0.7, 1.0]}
FINALES = ['¡MUY BIEN!', '¡GENIAL!', '¡BRAVO!', '¡SÚPER!', '¡QUÉ BIEN!']
ENVS = {'dia': {'sky_top': [0.1, 0.42, 1.0], 'sky_bottom': [1.0, 0.62, 0.7], 'ground': [0.28, 0.8, 0.42]}, 'atardecer': {'sky_top': [0.45, 0.25, 0.9], 'sky_bottom': [1.0, 0.55, 0.3], 'ground': [0.55, 0.85, 0.4]}, 'caramelo': {'sky_top': [0.95, 0.45, 0.8], 'sky_bottom': [1.0, 0.85, 0.6], 'ground': [0.45, 0.85, 0.8]}, 'menta': {'sky_top': [0.2, 0.75, 0.85], 'sky_bottom': [0.85, 1.0, 0.85], 'ground': [0.95, 0.8, 0.45]}}
ACCENTS = [[1, 0.75, 0.1], [1, 0.35, 0.6], [0.3, 0.8, 1], [0.6, 0.4, 1], [1, 0.5, 0.15]]

def load_history():
    try:
        return json.load(open(STATE))
    except Exception:
        return []

def gemini(prompt, key):
    body = json.dumps({'contents': [{'parts': [{'text': prompt}]}], 'generationConfig': {'responseMimeType': 'application/json', 'temperature': 1.0}}).encode()
    for model in ('gemini-flash-latest', 'gemini-2.5-flash', 'gemini-2.0-flash'):
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'
        req = urllib.request.Request(url, body, {'Content-Type': 'application/json', 'x-goog-api-key': key})
        for attempt in range(2):
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = json.load(r)
                return json.loads(data['candidates'][0]['content']['parts'][0]['text'])
            except Exception as e:
                print(f'[plan] {model} attempt {attempt}: {e}', file=sys.stderr)
                time.sleep(3)
    return None

def fallback_copy(words):
    emo = {'ROJO': '🔴', 'AZUL': '🔵', 'AMARILLO': '🟡', 'VERDE': '🟢', 'NARANJA': '🟠', 'MORADO': '🟣', 'ROSA': '🩷', 'CELESTE': '🩵'}
    icons = ''.join((emo.get(w, '') for w in words))
    title = f'¡Aprende los colores con Pip! {icons} #Shorts'
    desc = f"¡Salta con Pip y aprende los colores! {', '.join((w.lower() for w in words))} en una animación 3D alegre para peques.\n\n¿Cuál es tu color favorito? 🌈\n¡Suscríbete a Pimoruki para más! 💫\n\n#aprendecolores #pimoruki #coloresparaniños #videosinfantiles #shorts #educacioninfantil"
    tags = ['colores para niños', 'aprende los colores', 'videos para niños', 'colores en español', 'animación infantil', 'educación infantil', 'shorts infantiles'] + [f'color {w.lower()}' for w in words]
    return {'title': title, 'description': desc, 'tags': tags}

def main():
    hist = load_history()
    seed = int(os.environ.get('SEED') or int(time.time()) % 100000)
    rnd = random.Random(seed)
    recent = {tuple(h['words']) for h in hist[-40:]}
    for _ in range(50):
        words = rnd.sample(list(COLORS), 4)
        if tuple(words) not in recent:
            break
    env_name = rnd.choice(list(ENVS))
    finale = rnd.choice(FINALES)
    copy = None
    key = os.environ.get('GEMINI_API_KEY')
    if key:
        recent_titles = [h.get('title', '') for h in hist[-15:]]
        prompt = f"""Eres experto en SEO de YouTube Shorts infantiles en español (España y Latinoamérica).\nVídeo: animación 3D de 20 s en bucle. Un personaje adorable llamado Pip salta sobre botones gigantes y cambia\nde color; una voz dice cada color: {', '.join(words)}. Público: niños de 1 a 5 años y sus padres. Canal: Pimoruki (incluye una invitación breve a suscribirse a Pimoruki en la descripción y #pimoruki entre los hashtags).\nDevuelve SOLO JSON con: "title" (máx 70 caracteres, atractivo, con 1-4 emojis, termina en #Shorts, sin mayúsculas\nexcesivas, distinto de estos recientes: {recent_titles}), "description" (3-5 líneas, natural, pregunta al\nespectador, 4-6 hashtags al final, sin promesas engañosas), "tags" (10-15 etiquetas en español, búsquedas reales).\nNo menciones IA. Contenido apto para niños."""
        copy = gemini(prompt, key)
        if copy and (not all((k in copy for k in ('title', 'description', 'tags')))):
            copy = None
        if copy:
            copy['title'] = copy['title'][:95]
            copy['tags'] = [t[:30] for t in copy['tags']][:15]
    if not copy:
        copy = fallback_copy(words)
    spec = {'seed': seed, 'transpose': rnd.choice([0, 2, -1, 3, -3]), 'colors': [{'word': w, 'rgb': COLORS[w]} for w in words], 'finale_word': finale, **ENVS[env_name], 'antenna': rnd.choice(ACCENTS), 'band': rnd.choice(ACCENTS), 'body_shape': [round(rnd.uniform(0.96, 1.04), 3), round(rnd.uniform(0.89, 0.94), 3), 1.1], 'trees': rnd.sample(ACCENTS, 4)}
    meta = {**copy, 'categoryId': '27', 'madeForKids': True, 'language': 'es'}
    json.dump(spec, open(os.path.join(HERE, 'spec.json'), 'w'), ensure_ascii=False, indent=1)
    json.dump(meta, open(os.path.join(HERE, 'meta.json'), 'w'), ensure_ascii=False, indent=1)
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    hist.append({'date': datetime.date.today().isoformat(), 'seed': seed, 'words': words, 'env': env_name, 'title': meta['title']})
    json.dump(hist[-200:], open(STATE, 'w'), ensure_ascii=False, indent=0)
    print(json.dumps({'words': words, 'env': env_name, 'title': meta['title']}, ensure_ascii=False))
if __name__ == '__main__':
    main()
