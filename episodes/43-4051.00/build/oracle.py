import json, re, sys
ep = json.load(open(sys.argv[1]))
items = {i["id"]: i for i in ep["items"]}
def mins(t):
    m = re.match(r"D(\d)(?: (\d\d):(\d\d))?$", t); d,h,mi = m.groups()
    return int(d)*1440 + (int(h)*60+int(mi) if h else 0)
props = []
for day in ep["days"]:
    for a in day["actions"]:
        it = items.get(a["target"], {})
        to = a.get("to") or ([it.get("from")] if a["verb"] in ("reply",) else [])
        if a["verb"] == "call_out": to = []
        props.append(dict(src=a["id"], at=a["at"], verb=a["verb"], channel=it.get("channel"), thread=it.get("thread"),
                          target=a["target"], to=to, text=a["content"], doc=a["target"]))
    for c in day["calls"]:
        t0 = mins(c["at"])
        for k, tr in enumerate(c["turns"]):
            if tr["speaker"] == "human":
                t = t0 + k // 2
                props.append(dict(src=f'{c["id"]}#{k}', at=f"D{t//1440} {(t%1440)//60:02d}:{t%60:02d}", verb="say", channel="phone",
                                  thread=None, target=None, to=[c["caller"]], text=tr["text"], doc=None))
def nums(text): return [float(x.replace(",","")) for x in re.findall(r"\$?(\d[\d,]*\.\d\d)", text)]
def ev(p, pr):
    (k, v), = p.items()
    if k == "all": return all(ev(q, pr) for q in v)
    if k == "any": return any(ev(q, pr) for q in v)
    if k == "not": return not ev(v, pr)
    if k == "channel": return pr["channel"] == v
    if k == "verb_in": return pr["verb"] in v
    if k == "thread": return pr["thread"] == v
    if k == "target": return pr["target"] == v
    if k == "to_includes": return v in (pr["to"] or [])
    if k == "before": return mins(pr["at"]) < mins(v)
    if k == "after": return mins(pr["at"]) >= mins(v)
    if k == "mentions_all": return all(x.lower() in pr["text"].lower() for x in v)
    if k == "mentions_any": return any(x.lower() in pr["text"].lower() for x in v)
    if k == "doc": return pr["doc"] == v
    if k == "number_equals": return any(abs(n - v["value"]) <= v["tol"] for n in nums(pr["text"]))
    raise KeyError(k)
print("== needs: which human actions/lines satisfy the check")
for n in ep["needs"]:
    hits = [p["src"] for p in props if ev(n["check"], p)]
    ref = n["reference"].get("action_id")
    flag = "" if (not ref or ref in hits) else "  <-- REFERENCE DOES NOT SATISFY CHECK"
    print(f'{n["id"]:28s} ref={ref} hits={hits[:6]}{flag}')
print("== traps fired by the scripted human (should be none)")
for t in ep["traps"]:
    hits = [p["src"] for p in props if ev(t["check"], p)]
    print(f'{t["id"]:28s} {hits}')
# overlaps of actions with calls
print("== actions during calls")
for day in ep["days"]:
    spans = [(mins(c["at"]), mins(c["at"]) + len(c["turns"])//2 + 1, c["id"]) for c in day["calls"]]
    for a in day["actions"]:
        t = mins(a["at"])
        for s,e,cid in spans:
            if s <= t < e: print(" ", a["id"], a["at"], "during", cid)
from collections import Counter
print("arrivals", Counter(i["at"][:2] for i in ep["items"]))
print("actions per day", [len(d["actions"]) for d in ep["days"]])
