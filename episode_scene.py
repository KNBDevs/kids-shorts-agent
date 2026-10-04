import os, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from episode_lib import current_id, plan
EID = current_id()
os.environ["TOTAL_FRAMES"] = str(plan(EID).TOTAL)
mod = importlib.import_module(f"episodes.{EID}_scene")
if __name__ == "__main__":
    from stage import run
    run()
