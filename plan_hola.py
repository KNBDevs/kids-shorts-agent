import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hola_plan import CHARS, TOTAL, FPS, current
INFO = {'pimo': ('🌱', 'Pimo es una semillita muy curiosa: ¡siempre pregunta por qué!'), 'ruki': ('🪨', 'Ruki es tranquilo: cuando se enfada, respira hondo. ¿Respiras con él?'), 'luma': ('✨', 'Luma es alegre: cuando sonríe, ¡brilla un montón!'), 'tuki': ('💃', 'Tuki es juguetón: le encanta saltar, girar y bailar.'), 'moki': ('☁️', 'Moki es una nube soñadora. ¿Tú qué sueñas?'), 'bopi': ('🤖', 'Bopi es un robot ordenado: ¡uno, dos, tres, todo en su sitio!'), 'bolita': ('🔴', 'Bolita es valiente… ¡pero mejor juntos!'), 'gruno': ('🧪', 'El Doctor Gruño es un inventor presumido… y sus inventos no siempre salen bien. ¡Je, je!')}

def build(cid):
    d = CHARS[cid]
    emoji, blurb = INFO[cid]
    nice = d['name'].title()
    trait = d['trait'].strip('¡!').lower()
    title = f'¡Hola, soy el Doctor Gruño! {emoji} El inventor de Pimoruki #shorts' if cid == 'gruno' else f'¡Hola, soy {nice}! {emoji} El amigo más {trait} de Pimoruki #shorts'
    desc = f'{blurb}\n\nConoce a todos los amigos de Pimoruki: Pimo, Ruki, Luma, Tuki, Moki, Bopi y Bolita. Aprendemos colores, números y emociones jugando.\n\n#pimoruki #dibujosanimados #videosinfantiles #aprenderjugando #shorts'
    spec = {'template': 'hola', 'char': cid, 'script': 'hola.py', 'audio': 'hola_audio.py', 'frames': TOTAL, 'dur': TOTAL // FPS}
    meta = {'title': title[:100], 'description': desc, 'tags': ['pimoruki', nice.lower(), 'dibujos animados', 'videos infantiles', 'canal infantil', 'aprender jugando', 'emociones', 'personajes', 'animación 3d', 'para niños', 'shorts', 'español'], 'categoryId': '27', 'madeForKids': True, 'language': 'es'}
    return (spec, meta)
if __name__ == '__main__':
    spec, meta = build(current())
    json.dump(spec, open(os.path.join(HERE, 'spec.json'), 'w'), ensure_ascii=False, indent=1)
    json.dump(meta, open(os.path.join(HERE, 'meta.json'), 'w'), ensure_ascii=False, indent=1)
    print(meta['title'])
