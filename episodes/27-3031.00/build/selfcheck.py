import json, re, sys
ep = json.load(open(sys.argv[1]))
items = {i["id"]: i for i in ep["items"]}
def mins(t):
    m = re.match(r"^D(\d)(?: (\d\d):(\d\d))?$", t); d, h, mi = m.groups()
    return int(d) * 1440 + (int(h) * 60 + int(mi) if h else 0)
acts = [a for d in ep["days"] for a in d["actions"]]
def prop(a):
    tgt = items.get(a.get("target"))
    if a["verb"] in ("create_doc", "edit_doc", "comment") and (not tgt or tgt["channel"] == "docs"):
        ch = "docs"
    elif tgt:
        ch = tgt["channel"]
    else:
        ch = "email"
    if tgt and tgt["channel"] == "docs" and a["verb"] == "comment":
        ch = "docs"
    return {"channel": ch, "verb": a["verb"], "target": a.get("target"), "thread": tgt["thread"] if tgt else None,
            "to": a.get("to", []), "at": mins(a["at"]), "text": a["content"] + " " + a.get("subject", "") ,
            "doc": a.get("target") if ch == "docs" else None}
def ev(p, q):
    (k, v), = q.items()
    if k == "all": return all(ev(p, x) for x in v)
    if k == "any": return any(ev(p, x) for x in v)
    if k == "not": return not ev(p, v)
    t = p["text"].lower()
    return {"channel": lambda: p["channel"] == v, "verb_in": lambda: p["verb"] in v, "thread": lambda: p["thread"] == v,
            "target": lambda: p["target"] == v, "to_includes": lambda: v in p["to"],
            "before": lambda: p["at"] < mins(v), "after": lambda: p["at"] > mins(v),
            "mentions_all": lambda: all(x.lower() in t for x in v), "mentions_any": lambda: any(x.lower() in t for x in v),
            "doc": lambda: p["doc"] == v, "number_equals": lambda: False}[k]()
P = {a["id"]: prop(a) for a in acts}
print("NEEDS: reference fires?")
for n in ep["needs"]:
    r = n["reference"].get("action_id")
    hits = [aid for aid, p in P.items() if ev(p, n["check"])]
    print(f"  {n['id']:24s} ref={r} fires_on_ref={r in hits if r else '-'} other_hits={[h for h in hits if h != r]}")
print("TRAPS: fire on any human action?")
for t in ep["traps"]:
    hits = [aid for aid, p in P.items() if ev(p, t["check"])]
    print(f"  {t['id']:24s} {hits}")
