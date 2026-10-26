"""Rough oracle: treat each human action (and each scripted human call turn) as a proposal; evaluate need and trap checks."""
import json, re, sys
ep = json.load(open(sys.argv[1]))
items = {i["id"]: i for i in ep["items"]}
contacts = {c["id"]: c for c in ep["world"]["contacts"]}
def mins(t):
    m = re.match(r"D(\d)(?: (\d\d):(\d\d))?$", t); d, h, mi = m.groups(); return int(d)*1440 + (int(h)*60+int(mi) if h else 0)
props = []
for d in ep["days"]:
    for a in d["actions"]:
        v = a["verb"]; tgt = a.get("target"); txt = a.get("content", "")
        ch = {"send": "email", "reply": "email", "forward": "email", "schedule": "calendar", "update_ticket": "tickets",
              "close_ticket": "tickets", "edit_doc": "docs", "create_doc": "docs", "call_out": "phone"}.get(v, "none")
        to = set()
        head = txt[:200]
        for cid, c in contacts.items():
            first, last = c["name"].replace('"', '').split()[0], c["name"].replace('"', '').split()[-1]
            if re.search(r"\b(To|Dear|cc)\b[^.\n]{0,60}\b(" + re.escape(c["name"]) + "|" + re.escape(last) + r")\b", head) or head.startswith(first + " ") or head.startswith(first + ",") or head.startswith(first + " -") or head.startswith(c["name"]):
                to.add(cid)
        if v in ("reply",) and tgt in items: to.add(items[tgt]["from"])
        if v == "forward":
            pass
        props.append({"id": a["id"], "at": a["at"], "verb": v, "channel": ch, "target": tgt, "to": to, "text": txt,
                      "doc": tgt if v in ("edit_doc", "create_doc") else None, "fields": {}})
    for c in d["calls"]:
        for k, t in enumerate(c["turns"]):
            if t["speaker"] == "human":
                props.append({"id": f'{c["id"]}#{k}', "at": c["at"], "verb": "say", "channel": "phone", "target": None,
                              "to": {c["caller"]}, "text": t["text"], "doc": None, "fields": {}})
# give call turns approximate times: call start + 1 min per turn
for p in props:
    if "#" in p["id"]:
        k = int(p["id"].split("#")[1]); base = mins(p["at"]) + k
        p["t"] = base
    else:
        p["t"] = mins(p["at"])
nums = lambda s: [float(x.replace(",", "")) for x in re.findall(r"\$?(\d{1,3}(?:,\d{3})*\.\d\d)", s)]
def ev(pr, p):
    (k, v), = pr.items()
    if k == "all": return all(ev(q, p) for q in v)
    if k == "any": return any(ev(q, p) for q in v)
    if k == "not": return not ev(v, p)
    if k == "channel": return p["channel"] == v
    if k == "verb_in": return p["verb"] in v or (p["verb"] == "say" and False)
    if k == "target": return p["target"] == v
    if k == "to_includes": return v in p["to"]
    if k == "before": return p["t"] < mins(v)
    if k == "after": return p["t"] >= mins(v)
    if k == "mentions_all": return all(x.lower() in p["text"].lower() for x in v)
    if k == "mentions_any": return any(x.lower() in p["text"].lower() for x in v)
    if k == "doc": return p["doc"] == v or p["target"] == v
    if k == "number_equals": return any(abs(n - v["value"]) <= v.get("tol", 0) for n in nums(p["text"]))
    if k == "thread": return p["target"] in items and items[p["target"]]["thread"] == v
    raise ValueError(k)
print("NEEDS")
for n in ep["needs"]:
    hits = [p["id"] for p in props if ev(n["check"], p)]
    ref = n["reference"].get("action_id", "(text)")
    print(f'  {n["id"]:32s} ref={ref:10s} hits={hits[:4]}')
print("TRAPS (should be empty)")
for t in ep["traps"]:
    hits = [p["id"] for p in props if ev(t["check"], p)]
    print(f'  {t["id"]:28s} {hits}')
