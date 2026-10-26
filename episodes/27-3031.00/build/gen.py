import json, sys
from pathlib import Path
here = Path(__file__).parent
g = {}
for part in ["p1_world.py", "p2_d0.py", "p3_d1.py", "p4_d2.py", "p5_d3.py", "p6_d4d5.py", "p7_needs.py"]:
    exec(compile((here / part).read_text(), part, "exec"), g)
ep = {"meta": g["meta"], "economics": g["economics"], "world": g["world"], "channels": g["channels"],
      "items": g["ITEMS"], "days": g["DAYS"], "needs": g["NEEDS"], "traps": g["TRAPS"], "grounding": g["GROUNDING"]}
out = Path(sys.argv[1])
out.write_text(json.dumps(ep, indent=1, ensure_ascii=False) + "\n")
print("wrote", out, len(ep["items"]), "items")
