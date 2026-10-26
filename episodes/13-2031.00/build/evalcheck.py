import json, re, sys
ep = json.load(open(sys.argv[1]))
items = {i["id"]: i for i in ep["items"]}
acts = {a["id"]: a for d in ep["days"] for a in d["actions"]}
def mins(t):
    m = re.match(r"D(\d)(?: (\d\d):(\d\d))?", t); d, h, mi = m.groups()
    return int(d)*1440 + (int(h)*60+int(mi) if h else 0)
def prop_of(a):
    tgt = a.get("target"); it = items.get(tgt) or {}
    if tgt in acts: it = items.get(acts[tgt].get("target"), {})
    ch = "docs" if a["verb"] in ("create_doc","edit_doc") else it.get("channel","email")
    to = set()
    for c in ep["world"]["contacts"]:
        if c["name"].split()[0] in a["content"][:400]: to.add(c["id"])
    if it.get("from"): to.add(it["from"])
    return dict(text=a["content"], at=mins(a["at"]), thread=it.get("thread"), target=tgt, channel=ch, verb=a["verb"], to=to)
def ev(p, P):
    (k, v), = p.items()
    if k=="all": return all(ev(q,P) for q in v)
    if k=="any": return any(ev(q,P) for q in v)
    if k=="not": return not ev(v,P)
    t=P["text"].lower()
    return {"channel": lambda: P["channel"]==v, "verb_in": lambda: P["verb"] in v, "thread": lambda: P["thread"]==v,
            "target": lambda: P["target"]==v, "to_includes": lambda: v in P["to"], "before": lambda: P["at"]<mins(v),
            "after": lambda: P["at"]>mins(v), "mentions_all": lambda: all(x.lower() in t for x in v),
            "mentions_any": lambda: any(x.lower() in t for x in v), "doc": lambda: True, "number_equals": lambda: False}[k]()
for n in ep["needs"]:
    r = n["reference"].get("action_id")
    if r: print(n["id"], r, "OK" if ev(n["check"], prop_of(acts[r])) else "FAIL")
print("--- traps firing on human actions (to_includes ignored)")
for tr in ep["traps"]:
    for a in acts.values():
        if ev(tr["check"], prop_of(a)): print(tr["id"], "fires on", a["id"])
