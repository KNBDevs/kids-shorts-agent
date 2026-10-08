import os, sys, math
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
os.environ.setdefault("TOTAL_FRAMES", "2")
from stage import *
from props.costumes import dress
MODE = os.environ.get("MODE", "halloween")
YAW = float(os.environ.get("YAW", "0"))
IDS = ["pimo", "ruki", "luma", "tuki", "moki", "bopi", "bolita", "gruno"][int(os.environ.get("SET", "0")) * 2:][:2]
for i, cid in enumerate(IDS):
    ch = make(cid, 1.0)
    dress(ch, cid, MODE)
    ch['hold'].location = ((i - 0.5) * 1.25, -1.6, 0.08)
    ch['spin'].rotation_euler = (0, 0, math.radians(YAW))
camkey(0, ((0, -6.4, 1.6), (0, -1.6, 0.6), 42))
if __name__ == "__main__":
    run()
