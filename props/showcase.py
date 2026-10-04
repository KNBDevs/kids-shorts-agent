import os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
os.environ.setdefault("TOTAL_FRAMES", "2")
from stage import *
from props.lib import spawn
from props.registry import REGISTRY
STYLE = int(os.environ.get("STYLE", "0"))
FAM = os.environ.get("FAM", "pastel")
names = list(REGISTRY)
for i, n in enumerate(names):
    col, row = i % 3, i // 3
    spawn(n, STYLE, 7 + i, FAM, ((col - 1) * 1.25, -1.2 + row * 0.9, 0), 1.0, 15)
camkey(0, ((0, -7.5, 3.2), (0, 0.2, 0.6), 40))
if __name__ == "__main__":
    run()
