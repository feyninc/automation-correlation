import json, re, sys
ep = json.load(open(sys.argv[1]))
items = {i["id"]: i for i in ep["items"]}
acts = [a for d in ep["days"] for a in d["actions"]]
calls = [c for d in ep["days"] for c in d["calls"]]
def m(t):
    d = int(t[1]); hm = t[3:] if len(t) > 2 else "00:00"; h, mi = hm.split(":"); return d*1440+int(h)*60+int(mi)
def prop(a):
    tgt = a.get("target"); it = items.get(tgt, {})
    ch = a.get("channel") or it.get("channel") or ("email" if a["verb"] in ("send",) else "docs")
    return {"channel": ch, "verb": a["verb"], "target": tgt, "thread": it.get("thread"), "to": a.get("to", []) + a.get("cc", []),
            "at": a["at"], "text": a["content"]}
def nums(text):
    return [float(x.replace(",", "")) for x in re.findall(r"-?\d[\d,]*\.?\d*", text) if x.replace(",", "").replace(".", "").lstrip("-").isdigit()]
def ev(p, P):
    (k, v), = p.items()
    if k == "all": return all(ev(q, P) for q in v)
    if k == "any": return any(ev(q, P) for q in v)
    if k == "not": return not ev(v, P)
    if k == "channel": return P["channel"] == v
    if k == "verb_in": return P["verb"] in v
    if k == "thread": return P["thread"] == v
    if k == "target": return P["target"] == v
    if k == "doc": return P["target"] == v
    if k == "to_includes": return v in P["to"]
    if k == "before": return m(P["at"]) <= m(v)
    if k == "after": return m(P["at"]) >= m(v)
    if k == "mentions_all": return all(s.lower() in P["text"].lower() for s in v)
    if k == "mentions_any": return any(s.lower() in P["text"].lower() for s in v)
    if k == "number_equals": return any(abs(x - v["value"]) <= v["tol"] for x in nums(P["text"]))
    raise KeyError(k)
byid = {a["id"]: a for a in acts}
for n in ep["needs"]:
    r = n["reference"].get("action_id")
    if r: print(("PASS" if ev(n["check"], prop(byid[r])) else "FAIL"), n["id"], r)
# call lines as proposals
callprops = []
for c in calls:
    for t in c["turns"]:
        if t["speaker"] == "human":
            callprops.append({"channel": "phone", "verb": "call_line", "target": None, "thread": None, "to": [c["caller"]], "at": c["at"], "text": t["text"]})
k = [n for n in ep["needs"] if n["id"].startswith("n17")][0]
print("n17 via kyle call lines:", any(ev(k["check"], P) for P in callprops if "c_kyle" in P["to"]))
k = [n for n in ep["needs"] if n["id"].startswith("n16")][0]
print("n16 via tess call:", any(ev(k["check"], P) for P in callprops if "c_tess" in P["to"]))
for t in ep["traps"]:
    fired = [a["id"] for a in acts if ev(t["check"], prop(a))] + [P["at"] for P in callprops if ev(t["check"], P)]
    print("trap", t["id"], "fires on human:", fired)
