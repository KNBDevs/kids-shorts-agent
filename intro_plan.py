FPS = 24
TOTAL = 720
HOOK = 0
S0 = 26
STEP = 64
CAST = [{'id': 'pimo', 'name': 'PIMO', 'line': '¡Hola! ¡Soy Pimo, el más preguntón!', 'voice': {'pitch': 1.45, 'tempo': 1.12}, 'gesture': 'wave', 'slot': (-2.7, 2.2)}, {'id': 'ruki', 'name': 'RUKI', 'line': 'Yo soy Ruki. Tranquilos... respirad.', 'voice': {'pitch': 1.15, 'tempo': 1.0}, 'gesture': 'breathe', 'slot': (-0.85, 2.2)}, {'id': 'luma', 'name': 'LUMA', 'line': '¡Soy Luma! ¡Sonreíd conmigo!', 'voice': {'pitch': 1.62, 'tempo': 1.15}, 'gesture': 'wave', 'slot': (0.85, 2.2)}, {'id': 'tuki', 'name': 'TUKI', 'line': '¡Soy Tuki! ¡A bailar!', 'voice': {'pitch': 1.5, 'tempo': 1.18}, 'gesture': 'spin', 'slot': (2.5, 2.2)}, {'id': 'moki', 'name': 'MOKI', 'line': 'Soy Moki... me encanta soñar.', 'voice': {'pitch': 1.42, 'tempo': 1.0}, 'gesture': 'sway', 'slot': (-1.7, -0.4)}, {'id': 'bopi', 'name': 'BOPI', 'line': 'Soy Bopi. ¡Todo en orden! ¡Bip!', 'voice': {'pitch': 1.3, 'tempo': 1.18, 'robot': True}, 'gesture': 'hops', 'slot': (0.0, -0.4)}, {'id': 'bolita', 'name': 'BOLITA', 'line': '¡Soy Bolita! ¡Yo primero!', 'voice': {'pitch': 1.58, 'tempo': 1.2}, 'gesture': 'bounce', 'slot': (1.7, -0.4)}]
for i, c in enumerate(CAST):
    c['start'] = S0 + i * STEP
GROUP = S0 + len(CAST) * STEP
GROUP_LINE = {'text': '¡Somos Pimoruki!', 'frame': GROUP + 20}
GRUNO = 606
GRUNO_LINE = {'text': 'Je, je... ¡Ya veréis, Pimoruki!', 'frame': GRUNO + 22, 'voice': {'pitch': 0.92, 'tempo': 0.95}}
SUBSCRIBE = 672
SUBSCRIBE_LINE = {'text': '¡Suscríbete!', 'frame': SUBSCRIBE + 6}
