"""Screen O*NET occupations for the office simulation: white-collar, desk-bound, email-heavy work."""
import csv, sys
from collections import defaultdict

onet = sys.argv[1]  # path to db_31_0_text
out = sys.argv[2]

def rows(name):
    with open(f"{onet}/{name}", encoding="utf-8") as f:
        yield from csv.DictReader(f, delimiter="\t")

title = {r["O*NET-SOC Code"]: r["Title"] for r in rows("Occupation Data.txt")}
zone = {r["O*NET-SOC Code"]: int(r["Job Zone"]) for r in rows("Job Zones.txt")}

ctx = defaultdict(dict)  # code -> element -> CX mean (1-5)
for r in rows("Work Context.txt"):
    if r["Scale ID"] == "CX" and r["Element ID"] in ("4.C.1.a.2.h", "4.C.1.a.2.l", "4.C.1.a.2.f"):
        ctx[r["O*NET-SOC Code"]][r["Element ID"]] = float(r["Data Value"])
computers = {r["O*NET-SOC Code"]: float(r["Data Value"]) for r in rows("Work Activities.txt")
             if r["Element ID"] == "4.A.3.b.1" and r["Scale ID"] == "IM"}

tasks = defaultdict(lambda: [0, 0])  # code -> [core, total]
for r in rows("Task Statements.txt"):
    t = tasks[r["O*NET-SOC Code"]]
    t[1] += 1
    t[0] += r["Task Type"] == "Core"

with open(out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["code", "title", "job_zone", "email_cx", "face_to_face_cx", "phone_cx", "computers_im", "core_tasks", "tasks"])
    for code, t in sorted(title.items()):
        c = ctx.get(code, {})
        if "4.C.1.a.2.h" not in c or code not in computers:
            continue  # no incumbent ratings (e.g. aggregate or new codes)
        w.writerow([code, t, zone.get(code, ""), c["4.C.1.a.2.h"], c.get("4.C.1.a.2.l", ""),
                    c.get("4.C.1.a.2.f", ""), computers[code], *tasks[code]])
