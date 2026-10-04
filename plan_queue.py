import json, os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
QUEUE = os.path.join(HERE, 'catalog', 'queue.json')
PUB = os.path.join(HERE, 'state', 'published.json')
READY = {'intro', 'hola'}

def out(k, v):
    p = os.environ.get('GITHUB_OUTPUT')
    if p:
        open(p, 'a').write(f'{k}={v}\n')
    print(f'{k}={v}')

def voices_ready(item):
    sys.path[:0] = [HERE, os.path.join(HERE, "voices")]
    from cast import lines
    from gvoices import digest
    mp = os.path.join(HERE, "assets", "vo", "manifest.json")
    man = json.load(open(mp)) if os.path.exists(mp) else {}
    pre = "intro_" if item["template"] == "intro" else f"hola_{item.get('char')}_"
    need = {k: e for k, e in lines().items() if k.startswith(pre)}
    return all(man.get(k, {}).get("hash") == digest(e["char"], e["text"]) for k, e in need.items())


def main():
    q = json.load(open(QUEUE))
    done = set(json.load(open(PUB))) if os.path.exists(PUB) else set()
    nxt = next((e for e in q if e['status'] == 'approved' and e['id'] not in done and e['template'] in READY and voices_ready(e)), None)
    if not nxt:
        out('skip', 'true')
        return
    env = dict(os.environ)
    if nxt['template'] == 'hola':
        env['CHAR'] = nxt['char']
    subprocess.run([sys.executable, os.path.join(HERE, f"plan_{nxt['template']}.py")], env=env, check=True)
    p = os.path.join(HERE, 'spec.json')
    spec = json.load(open(p))
    spec['episode'] = nxt['id']
    json.dump(spec, open(p, 'w'), ensure_ascii=False, indent=1)
    out('skip', 'false')
    out('episode', nxt['id'])
if __name__ == '__main__':
    main()
