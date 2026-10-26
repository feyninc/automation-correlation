import json, sys
from pathlib import Path
here = Path(__file__).parent
g = {}
for part in ("gen_part1.py", "gen_part2.py", "gen_part3.py", "gen_part4.py"):
    exec(compile((here / part).read_text(), part, "exec"), g)
out = Path(sys.argv[1])
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(g["EPISODE"], indent=1, ensure_ascii=False) + "\n")
print("wrote", out, out.stat().st_size, "bytes")
