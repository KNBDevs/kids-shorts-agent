FPS = 24
TOTAL = 780
MOOD = 'happy'
ENV = 'patio'
JUMPS0 = [(4, 1), (22, 2), (40, 4)]
JUMPS = [(192, 1), (232, 2), (272, 3), (312, 4)]
PULSE = [404, 413, 422, 431]
BIG = 560
LINES = [
    ('a1', 'tuki', '¡Uno!', 6, 1.0),
    ('a2', 'tuki', '¡Dos!', 24, 1.0),
    ('a4', 'tuki', '¡Cuatro!', 42, 1.0),
    ('r1', 'ruki', '¿Y el tres?', 76, 1.4),
    ('r2', 'ruki', 'Contamos despacio: un salto, una ficha.', 106, 2.9),
    ('c1', 'tuki', '¡Uno!', 194, 1.0),
    ('c2', 'tuki', '¡Dos!', 234, 1.0),
    ('c3', 'tuki', '¡Tres!', 274, 1.0),
    ('c4', 'tuki', '¡Cuatro!', 314, 1.0),
    ('r3', 'ruki', '¿Cuántas fichas hay?', 356, 1.8),
    ('t5', 'tuki', '¡Cuatro!', 442, 1.0),
    ('r4', 'ruki', '¡Cuatro saltos, cuatro fichas!', 472, 2.4),
    ('t6', 'tuki', '¡Y otro más!', 536, 1.3),
    ('t7', 'tuki', '¡Cinco!', 600, 1.0),
    ('r5', 'ruki', '¡Cinco saltos, cinco fichas!', 636, 2.4),
]
SFX = [(f + 12, 'boing', 0.18) for f, _ in JUMPS0]
SFX += [(f + 14, 'pop', 0.4) for f, _ in JUMPS]
SFX += [(f, 'bip', 0.16) for f in PULSE]
SFX += [(70, 'whistle_up', 0.12), (BIG - 2, 'boing_up', 0.25), (586, 'boing', 0.25), (604, 'pop', 0.4), (606, 'sparkle', 0.35), (690, 'popper', 0.2)]
META = {
    'title': 'Tuki cuenta sus saltos 🔢 ¡Un salto, una ficha! #shorts',
    'description': 'Tuki salta y cuenta: «uno, dos, cuatro»... ¡se ha saltado el tres! Ruki coloca una ficha por cada salto y cuentan despacio hasta cinco. Aprende a contar del 1 al 5 jugando.\n\n#pimoruki #dibujosanimados #videosinfantiles #aprenderjugando #shorts',
    'tags': ['pimoruki', 'dibujos animados', 'videos infantiles', 'aprender jugando', 'contar', 'números',
             'contar hasta cinco', 'aprender a contar', 'educación infantil', 'preescolar', 'tuki', 'shorts'],
}
