import colorsys, json, os, random
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
USAGE = os.path.join(ROOT, "catalog", "props_usage.json")
FAMILIES = {
    "pastel": [(0.95, 0.55, 0.65), (0.55, 0.75, 0.98), (0.98, 0.85, 0.45), (0.6, 0.88, 0.7), (0.78, 0.65, 0.95)],
    "autumn": [(0.75, 0.46, 0.27), (0.91, 0.74, 0.47), (0.51, 0.58, 0.52), (0.4, 0.32, 0.44), (0.91, 0.87, 0.81)],
    "fresh": [(0.35, 0.8, 0.75), (0.98, 0.6, 0.45), (0.98, 0.9, 0.55), (0.55, 0.7, 0.95), (0.95, 0.95, 0.9)],
    "candy": [(1.0, 0.45, 0.6), (0.45, 0.85, 0.95), (1.0, 0.8, 0.35), (0.7, 0.55, 1.0), (0.5, 0.9, 0.6)],
}
ENV_DEFAULT = {"plaza": "pastel", "patio": "fresh", "lab": "candy", "otono": "autumn", "casa": "pastel", "halloween": "autumn"}


def tint(rgb, rng, amount=0.06):
    h, s, v = colorsys.rgb_to_hsv(*rgb)
    h = (h + rng.uniform(-amount, amount)) % 1.0
    s = min(1, max(0, s + rng.uniform(-0.12, 0.12)))
    v = min(1, max(0.25, v + rng.uniform(-0.08, 0.08)))
    return colorsys.hsv_to_rgb(h, s, v)


def colors(rng, family, n):
    base = FAMILIES.get(family, FAMILIES["pastel"])[:]
    rng.shuffle(base)
    return [tint(base[i % len(base)], rng) for i in range(n)]


def load_usage():
    return json.load(open(USAGE)) if os.path.exists(USAGE) else {}


def recent(usage, n=6, exclude=None):
    items = [(v.get("order", 0), k, v) for k, v in usage.items() if k != exclude]
    items.sort()
    used = set()
    for _, _, v in items[-n:]:
        for d in v.get("decor", []) + v.get("hero", []):
            used.add((d["prop"], d["style"]))
    return used


def choose(eid, env, registry, count=6, seed=None, family=None):
    usage = load_usage()
    if eid in usage:
        return usage[eid]
    rng = random.Random(seed if seed is not None else sum(map(ord, eid)))
    family = family or ENV_DEFAULT.get(env, "pastel")
    blocked = recent(usage, exclude=eid)
    pool = [(n, s) for n, meta in registry.items() if (env in meta["envs"] or "any" in meta["envs"]) and meta.get("decor", True) for s in range(meta["styles"])]
    fresh = [p for p in pool if p not in blocked]
    rng.shuffle(fresh)
    picked, names = [], set()
    for n, s in fresh:
        if n in names:
            continue
        picked.append((n, s)); names.add(n)
        if len(picked) == count:
            break
    if len(picked) < count:
        rest = [p for p in pool if p[0] not in names]
        rng.shuffle(rest)
        for n, s in rest:
            if n in names:
                continue
            picked.append((n, s)); names.add(n)
            if len(picked) == count:
                break
    slots = layout(rng, len(picked))
    decor = [{"prop": n, "style": s, "seed": rng.randrange(10 ** 6), "loc": slots[i][0], "scale": slots[i][1], "rot": slots[i][2]}
             for i, (n, s) in enumerate(picked)]
    return {"env": env, "family": family, "decor": decor, "order": max([v.get("order", 0) for v in usage.values()] + [0]) + 1}


def layout(rng, n):
    out = []
    xs = [-3.4, 3.4, -2.2, 2.2, -4.6, 4.6, -1.1, 1.1]
    rng.shuffle(xs)
    for i in range(n):
        x = xs[i % len(xs)] + rng.uniform(-0.3, 0.3)
        y = rng.uniform(1.6, 4.5) if abs(x) < 2.5 else rng.uniform(0.2, 3.5)
        out.append(((round(x, 2), round(y, 2), 0.0), round(rng.uniform(0.85, 1.25), 2), round(rng.uniform(-35, 35), 1)))
    return out


def record(eid, env, registry, **kw):
    usage = load_usage()
    if eid not in usage:
        usage[eid] = choose(eid, env, registry, **kw)
        json.dump(usage, open(USAGE, "w"), ensure_ascii=False, indent=1)
    return usage[eid]
