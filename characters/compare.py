import sys
from PIL import Image
U = "/root/.claude/uploads/351725bd-2a89-5b50-868a-9a93c20278f1/"
REF = {"pimo": "6b2ad09b", "ruki": "79511248", "luma": "bc2662d2", "tuki": "d96f809c", "moki": "b04bf85b", "bopi": "ac601686", "bolita": "a72ad1aa", "gruno": "16f63fc9"}
for n in sys.argv[1:]:
    ref = Image.open(U + REF[n] + "-image.png").convert("RGB").crop((0, 150, 1536, 940))
    W = 1920; ref = ref.resize((W, int(ref.height * W / ref.width)))
    ims = [Image.open(f"inspect/{n}_{v}.png").convert("RGB") for v in ("front", "left_side", "back", "three_quarter")]
    row = Image.new("RGB", (1920, 560)); [row.paste(im, (i * 480, 0)) for i, im in enumerate(ims)]
    c = Image.new("RGB", (W, ref.height + 560)); c.paste(ref, (0, 0)); c.paste(row, (0, ref.height))
    c.save(f"inspect/{n}_compare.jpg", quality=85)
