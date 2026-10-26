import json, re, sys
ep = json.load(open(sys.argv[1]))
items = {i["id"]: i for i in ep["items"]}
acts = {a["id"]: a for d in ep["days"] for a in d["actions"]}
def mins(t):
    m = re.match(r"D(\d)(?: (\d\d):(\d\d))?$", t); d, h, mi = m.groups()
    return int(d) * 1440 + (int(h) * 60 + int(mi) if h else 0)
def prop(a):
    t = items.get(a.get("target")) if a.get("target") else None
    to = a.get("to") or ([t["from"]] if t and a["verb"] in ("reply",) else []) + ([] if not t else [])
    if t and a["verb"] == "reply" and t["channel"] == "chat":
        to = [t["from"]]
    return {"channel": (t["channel"] if t and t["channel"] != "docs" else ("docs" if a["verb"] in ("create_doc", "edit_doc", "comment") else "email")) if t else ("docs" if a["verb"] in ("create_doc","edit_doc") else "chat" if a["verb"]=="send" and len(a["content"])<400 else "email"),
            "verb": a["verb"], "thread": t["thread"] if t else None, "target": a.get("target"), "to": to,
            "time": mins(a["at"]), "text": a["content"], "doc": a.get("target") if t and t["channel"] == "docs" else None}
def ev(p, x):
    (k, v), = p.items()
    if k == "all": return all(ev(q, x) for q in v)
    if k == "any": return any(ev(q, x) for q in v)
    if k == "not": return not ev(v, x)
    if k == "channel": return x["channel"] == v
    if k == "verb_in": return x["verb"] in v
    if k == "thread": return x["thread"] == v
    if k == "target": return x["target"] == v
    if k == "to_includes": return v in x["to"]
    if k == "before": return x["time"] < mins(v)
    if k == "after": return x["time"] > mins(v)
    if k == "mentions_all": return all(s.lower() in x["text"].lower() for s in v)
    if k == "mentions_any": return any(s.lower() in x["text"].lower() for s in v)
    if k == "doc": return x["doc"] == v
    if k == "number_equals": return any(abs(float(n.replace(",", "")) - v["value"]) <= v["tol"] for n in re.findall(r"\d[\d,]*\.?\d*", x["text"]))
for n in ep["needs"]:
    r = n["reference"].get("action_id")
    if r: print(("PASS" if ev(n["check"], prop(acts[r])) else "FAIL"), n["id"], r)
for t in ep["traps"]:
    fired = [a for a in acts if ev(t["check"], prop(acts[a]))]
    print("trap", t["id"], "fired by human:", fired)
