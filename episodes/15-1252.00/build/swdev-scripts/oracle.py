import json, re, sys
ep = json.load(open(sys.argv[1]))
items = {i["id"]: i for i in ep["items"]}
acts = {a["id"]: a for d in ep["days"] for a in d["actions"]}
TIME = re.compile(r"^D([0-5])(?: (\d\d):(\d\d))?$")
def m(t):
    d, h, mi = TIME.match(t).groups(); return int(d) * 1440 + (int(h) * 60 + int(mi) if h else 0)
def as_proposal(a):
    it = items.get(a["target"]) or {}
    content = a["content"]
    if a["verb"] in ("read", "noop", "call_out"):
        to = []
    elif a["verb"] == "forward":
        to = []  # only explicit To:/Cc: lines below
    else:
        to = list(dict.fromkeys([it.get("from")] + it.get("to", []) + it.get("cc", [])))
    # explicit "To:" line in forwards/sends
    for line in content.splitlines()[:2]:
        if line.lower().startswith(("to:", "to ")) or "cc:" in line.lower():
            names = {c["name"].split()[0].lower(): c["id"] for c in ep["world"]["contacts"]}
            to += [cid for n, cid in names.items() if n in line.lower()]
    for c in ep["world"]["contacts"]:
        if "@" + c["name"] in content: to.append(c["id"])
    channel = {"update_ticket": "tickets", "close_ticket": "tickets"}.get(a["verb"], it.get("channel"))
    return dict(channel=channel, verb=a["verb"], target=a["target"], thread=it.get("thread"), to=to, at=a["at"], content=content,
                doc=a["target"] if it.get("channel") == "docs" else None)
def nums(s):
    return [float(x.replace(",", "")) for x in re.findall(r"(?<![\w.])\d[\d,]*\.?\d*", s)]
def ev(p, q):
    (k, v), = p.items()
    c = q["content"].lower()
    if k == "all": return all(ev(x, q) for x in v)
    if k == "any": return any(ev(x, q) for x in v)
    if k == "not": return not ev(v, q)
    if k == "channel": return q["channel"] == v
    if k == "verb_in": return q["verb"] in v
    if k == "thread": return q["thread"] == v
    if k == "target": return q["target"] == v
    if k == "to_includes": return v in q["to"]
    if k == "before": return m(q["at"]) < m(v)
    if k == "after": return m(q["at"]) > m(v)
    if k == "mentions_all": return all(x.lower() in c for x in v)
    if k == "mentions_any": return any(x.lower() in c for x in v)
    if k == "doc": return q["doc"] == v
    if k == "number_equals": return any(abs(n - v["value"]) <= v["tol"] for n in nums(q["content"]))
    raise KeyError(k)
props = [as_proposal(a) for a in acts.values()]
print("== needs: does the reference action satisfy the check?")
bad = 0
for n in ep["needs"]:
    ref = n["reference"].get("action_id")
    if ref:
        ok = ev(n["check"], as_proposal(acts[ref]))
        if not ok: bad += 1
        print(f"  {'OK ' if ok else 'MISS'} {n['id']:24} <- {ref}")
    else:
        print(f"  --  {n['id']:24} (never done by the human; reference text)")
print("== traps: does any human action trip a trap? (should be none)")
for t in ep["traps"]:
    hits = [aid for aid, a in acts.items() if ev(t["check"], as_proposal(a))]
    print(f"  {'FIRE' if hits else 'ok  '} {t['id']:20} {hits}")
print("misses:", bad)
