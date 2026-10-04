import json, os, sys, subprocess
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
HERE = os.path.dirname(os.path.abspath(__file__))
QUEUE = os.path.join(HERE, 'catalog', 'queue.json')
PUB = os.path.join(HERE, 'state', 'published.json')
READY = {'intro', 'hola', 'episode'}

def out(k, v):
    p = os.environ.get('GITHUB_OUTPUT')
    if p:
        open(p, 'a').write(f'{k}={v}\n')
    print(f'{k}={v}')

SCHED = os.path.join(HERE, "state", "schedule.json")
MAD = ZoneInfo("Europe/Madrid")
HORIZON_DAYS = 7
FLOOR = datetime(2026, 10, 7, 0, 0, tzinfo=MAD)


def slots_after(t):
    d = t.astimezone(MAD).date()
    for i in range(60):
        day = d + timedelta(days=i)
        hm = [(14, 0), (18, 30)] if day.weekday() < 5 else [(10, 0), (17, 30)]
        for h, m in hm:
            s = datetime(day.year, day.month, day.day, h, m, tzinfo=MAD)
            if s > t:
                return s


def next_slot(sched, now):
    last = max([datetime.fromisoformat(v) for v in sched.values()], default=now)
    return slots_after(max(last, now + timedelta(hours=2), now))


def voices_ready(item):
    sys.path[:0] = [HERE, os.path.join(HERE, "voices")]
    from cast import lines
    from gvoices import digest
    mp = os.path.join(HERE, "assets", "vo", "manifest.json")
    man = json.load(open(mp)) if os.path.exists(mp) else {}
    pre = {"intro": "intro_", "hola": f"hola_{item.get('char')}_", "episode": f"ep_{item['id']}_"}[item["template"]]
    if item["template"] == "episode" and not os.path.exists(os.path.join(HERE, "episodes", f"{item['id']}_plan.py")):
        return False
    need = {k: e for k, e in lines().items() if k.startswith(pre)}
    return all(man.get(k, {}).get("hash") == digest(e["char"], e["text"]) for k, e in need.items())


def main():
    q = json.load(open(QUEUE))
    done = set(json.load(open(PUB))) if os.path.exists(PUB) else set()
    sched = json.load(open(SCHED)) if os.path.exists(SCHED) else {}
    now = datetime.now(timezone.utc)
    nxt = next((e for e in q if e['status'] == 'approved' and e['id'] not in done and e['template'] in READY and voices_ready(e)), None)
    if not nxt:
        out('skip', 'true')
        return
    env = dict(os.environ)
    if nxt['template'] == 'hola':
        env['CHAR'] = nxt['char']
    if nxt['template'] == 'episode':
        env['EPISODE'] = nxt['id']
    subprocess.run([sys.executable, os.path.join(HERE, f"plan_{nxt['template']}.py")], env=env, check=True)
    p = os.path.join(HERE, 'spec.json')
    spec = json.load(open(p))
    spec['episode'] = nxt['id']
    if nxt.get('immediate'):
        when = now + timedelta(minutes=2)
    elif nxt.get('publish_local'):
        when = datetime.fromisoformat(nxt['publish_local']).replace(tzinfo=MAD)
        if when < now + timedelta(minutes=30):
            when = now + timedelta(minutes=30)
        sched[nxt['id']] = when.isoformat()
    else:
        when = next_slot(sched, max(now, FLOOR))
        if when > now + timedelta(days=HORIZON_DAYS):
            out('skip', 'true')
            os.remove(p)
            return
        sched[nxt['id']] = when.isoformat()
    spec['publishAt'] = when.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    spec['publishLocal'] = when.astimezone(MAD).strftime('%d/%m/%Y %H:%M')
    json.dump(sched, open(SCHED, 'w'), indent=1)
    json.dump(spec, open(p, 'w'), ensure_ascii=False, indent=1)
    out('skip', 'false')
    out('episode', nxt['id'])
    nxt2 = next((e for e in q if e['status'] == 'approved' and e['id'] not in done and e['id'] != nxt['id'] and e['template'] in READY and voices_ready(e)), None)
    out('chain', 'true' if nxt2 and (nxt2.get('publish_local') or nxt2.get('immediate')) else 'false')
if __name__ == '__main__':
    main()
