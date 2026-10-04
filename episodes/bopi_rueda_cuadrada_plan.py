import math
FPS = 24
TOTAL = 816
MOOD = 'silly'
LANE = -1.25
GROUND = 0.02
WHEEL = {4: 0.21, 3: 0.24, 0: 0.18}
SEGS = {
    'A': (2, 74, 4, -2.0, 0.9, 1),
    'B': (222, 300, 3, -1.1, 1.25, 1),
    'C': (546, 630, 0, 0.15, 1.45, 1),
    'G1': (636, 676, 4, 3.94, 0.891, -1),
    'G2': (728, 746, 4, 3.049, 0.297, -1),
}
LINES = [
    ('l1', 'ruki', '¿Una rueda cuadrada?', 84, 1.8),
    ('l2', 'bopi', '¡Bip! ¡Pues probaré con triángulos!', 136, 2.2),
    ('l3', 'bopi', '¡Uy! ¡Da más saltos!', 308, 1.6),
    ('l4', 'ruki', 'Probemos un círculo.', 356, 1.8),
    ('l5', 'ruki', '¿Tú qué crees? ¿Rodará mejor?', 452, 2.4),
    ('l6', 'bopi', '¡El círculo rueda!', 590, 1.6),
    ('l7', 'gruno', '¡El mío es mejor!', 684, 1.6),
]


def ease(u):
    return u * u * (3 - 2 * u)


def roll(n, x0, d, sgn=1):
    R = WHEEL[n]
    if n == 0:
        return x0 + sgn * d, R, sgn * d / R, 0
    L = 2 * R * math.sin(math.pi / n)
    k = int(d / L + 1e-09)
    phi = (d - k * L) / L * 2 * math.pi / n
    x = k * L + L / 2 - R * math.sin(math.pi / n - phi)
    z = R * math.cos(math.pi / n - phi)
    return x0 + sgn * x, z, sgn * (k * 2 * math.pi / n + phi), k


def seg_at(name, f):
    f0, f1, n, x0, d, sgn = SEGS[name]
    u = min(max((f - f0) / (f1 - f0), 0), 1)
    return roll(n, x0, d * ease(u), sgn)


def landings(name):
    f0, f1, n, x0, d, sgn = SEGS[name]
    out, prev = [], 0
    for f in range(f0, f1 + 1):
        k = seg_at(name, f)[3]
        if k > prev:
            out.append(f)
        prev = k
    return out


SFX = [(f, 'clonk', 0.5) for s in ('A', 'G1', 'G2') for f in landings(s)]
SFX += [(f, 'tock', 0.45) for f in landings('B')]
SFX += [(196, 'pop', 0.4), (206, 'sparkle', 0.3), (360, 'pop', 0.35), (378, 'whistle_down', 0.12),
        (428, 'pop', 0.4), (436, 'sparkle', 0.35), (594, 'sparkle', 0.25), (747, 'boing_up', 0.25), (760, 'splat', 0.5)]
META = {
    'title': 'Bopi y la rueda cuadrada 🟧🔺⚪ ¿Qué forma rueda mejor? #shorts',
    'description': 'Bopi tiene un carrito con ruedas cuadradas y todo da saltos. ¿Y con triángulos? Ruki propone probar un círculo... ¡y el carrito va suave! Aprende jugando qué forma rueda mejor sobre un suelo plano.\n\n#pimoruki #dibujosanimados #videosinfantiles #aprenderjugando #shorts',
    'tags': ['pimoruki', 'dibujos animados', 'videos infantiles', 'aprender jugando', 'formas geométricas', 'círculo',
             'cuadrado', 'triángulo', 'ruedas', 'educación infantil', 'preescolar', 'shorts'],
}
