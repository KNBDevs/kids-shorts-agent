import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from props.select import record
from props.registry import REGISTRY
if __name__ == "__main__":
    eid, env = sys.argv[1], sys.argv[2]
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    print(json.dumps(record(eid, env, REGISTRY, count=count), ensure_ascii=False))
