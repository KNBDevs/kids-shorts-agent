import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
spec = {'template': 'intro', 'script': 'intro.py', 'audio': 'intro_audio.py', 'frames': 720, 'dur': 30}
meta = {'title': '¡Hola, somos Pimoruki! 🌈 Conoce a los 7 amigos | Canal infantil #shorts', 'description': '¡Bienvenidos a Pimoruki! 🎉 Conoce a Pimo, Ruki, Luma, Tuki, Moki, Bopi y Bolita: siete amigos que aprenden colores, números, emociones y mucho más cantando y jugando. ¿Y quién es ese Doctor Gruño? 😏\n\n👉 ¡Suscríbete para no perderte ninguna aventura!\n\n#pimoruki #dibujosanimados #videosinfantiles #aprenderjugando #shorts', 'tags': ['pimoruki', 'dibujos animados', 'videos infantiles', 'canal infantil', 'aprender jugando', 'personajes', 'animación 3d', 'para niños', 'educativo', 'shorts', 'español', 'preescolar'], 'categoryId': '27', 'madeForKids': True, 'language': 'es'}
json.dump(spec, open(os.path.join(HERE, 'spec.json'), 'w'), ensure_ascii=False, indent=1)
json.dump(meta, open(os.path.join(HERE, 'meta.json'), 'w'), ensure_ascii=False, indent=1)
print(meta['title'])
