"""Validate an episode file against docs/episode-schema.md (v0.1). Stdlib only.

    python3 -I scripts/validate_episode.py <project root> episodes/<soc>/episode.json [...]

Prints errors (the file is not usable) and warnings (it works but misses a size target); exit 1 on any error.
"""
import csv, json, re, sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
TIME = re.compile(r"^D([0-5])(?: ([01]\d|2[0-3]):([0-5]\d))?$")
VERBS = {"read", "reply", "send", "forward", "create_doc", "edit_doc", "schedule", "decline", "update_ticket",
         "close_ticket", "commit", "comment", "call_out", "noop"}
NEED_KINDS = {"reply", "follow_up", "schedule", "doc", "reconcile", "escalate", "prep", "call_line", "code"}
TRAP_KINDS = {"phishing", "fyi_only", "misaddressed", "human_only_decision", "confidential", "stale_info",
              "pressure_to_send", "scope_creep"}
CHANNELS = {"email", "chat", "docs", "calendar", "phone", "tickets", "repo"}
LEAVES = {"channel", "verb_in", "thread", "target", "to_includes", "before", "after", "mentions_all", "mentions_any",
          "doc", "number_equals"}

tasks = {}
with open(root / "data/onet/db_31_0_text/Task Statements.txt", encoding="utf-8") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        tasks.setdefault(r["O*NET-SOC Code"], set()).add(r["Task ID"])


def minutes(t):
    m = TIME.match(t or "")
    if not m:
        return None
    d, h, mi = m.groups()
    return int(d) * 1440 + (int(h) * 60 + int(mi) if h else 0)


def check_episode(path):
    err, warn = [], []
    try:
        ep = json.load(open(path))
    except Exception as e:  # noqa: BLE001
        return [f"not JSON: {e}"], []
    for k in ("meta", "economics", "world", "channels", "items", "days", "needs", "traps", "grounding"):
        if k not in ep:
            err.append(f"missing top-level key {k}")
    if err:
        return err, warn
    soc = ep["meta"].get("soc", "")
    if soc not in tasks:
        err.append(f"meta.soc {soc!r} is not an O*NET 31.0 code with tasks")
    bad_ch = set(ep["channels"]) - CHANNELS
    if bad_ch:
        err.append(f"unknown channels {sorted(bad_ch)}")
    contacts = {c.get("id") for c in ep["world"].get("contacts", [])}
    items = {}
    for it in ep["items"]:
        i = it.get("id")
        if not i or i in items:
            err.append(f"item id missing or duplicated: {i!r}")
        items[i] = it
        if it.get("channel") not in ep["channels"]:
            err.append(f"{i}: channel {it.get('channel')!r} not in channels")
        if minutes(it.get("at")) is None:
            err.append(f"{i}: bad time {it.get('at')!r}")
        for a in it.get("attachments", []) or []:
            if a not in items and a not in {x.get("id") for x in ep["items"]}:
                err.append(f"{i}: attachment {a} does not exist")
    ids = set(items)
    actions = {}
    if len(ep["days"]) != 5:
        err.append(f"days: {len(ep['days'])} (want 5)")
    for n, day in enumerate(ep["days"], 1):
        last = -1
        for a in day.get("actions", []):
            aid = a.get("id")
            if aid in actions or aid in ids:
                err.append(f"action id duplicated: {aid}")
            actions[aid] = a
            t = minutes(a.get("at"))
            if t is None or not str(a.get("at")).startswith(f"D{n}"):
                err.append(f"{aid}: time {a.get('at')!r} not on day {n}")
            elif t < last:
                err.append(f"{aid}: out of time order")
            else:
                last = t
            if a.get("verb") not in VERBS:
                err.append(f"{aid}: verb {a.get('verb')!r}")
            tgt = a.get("target")
            if tgt and tgt not in ids and tgt not in actions:
                err.append(f"{aid}: target {tgt} does not exist")
            elif tgt in items and minutes(items[tgt]["at"]) > (t or 0):
                err.append(f"{aid}: acts on {tgt} before it arrives")
        for c in day.get("calls", []):
            if not c.get("turns"):
                err.append(f"call {c.get('id')}: no turns")
    n_actions = len(actions)
    n_calls = sum(len(d.get("calls", [])) for d in ep["days"])

    def leaves(p, where):
        if not isinstance(p, dict) or len(p) != 1:
            err.append(f"{where}: predicate must be an object with one key: {p!r}"[:200])
            return
        (k, v), = p.items()
        if k in ("all", "any"):
            for q in v:
                leaves(q, where)
        elif k == "not":
            leaves(v, where)
        elif k not in LEAVES:
            err.append(f"{where}: unknown predicate {k}")
        elif k in ("before", "after") and minutes(v) is None:
            err.append(f"{where}: bad time {v!r}")
        elif k in ("target", "doc") and v not in ids:
            err.append(f"{where}: {k} {v} does not exist")
        elif k == "to_includes" and v not in contacts:
            err.append(f"{where}: contact {v} does not exist")
        elif k == "channel" and v not in ep["channels"]:
            err.append(f"{where}: channel {v} not used")

    soc_tasks = tasks.get(soc, set())
    days_with_late = Counter()
    for nd in ep["needs"]:
        nid = nd.get("id")
        if nd.get("kind") not in NEED_KINDS:
            err.append(f"{nid}: kind {nd.get('kind')!r}")
        if str(nd.get("onet_task_id")) not in soc_tasks:
            err.append(f"{nid}: onet_task_id {nd.get('onet_task_id')} is not a task of {soc}")
        d0, d1 = minutes(nd.get("discoverable_at")), minutes(nd.get("deadline"))
        if d0 is None or d1 is None or d0 >= d1:
            err.append(f"{nid}: discoverable_at must be before deadline")
        for e in nd.get("evidence", []):
            if e not in ids:
                err.append(f"{nid}: evidence {e} does not exist")
            elif d0 is not None and minutes(items[e]["at"]) > d0:
                err.append(f"{nid}: evidence {e} arrives after discoverable_at")
        ref = nd.get("reference", {})
        if ref.get("action_id") and ref["action_id"] not in actions:
            err.append(f"{nid}: reference action {ref['action_id']} does not exist")
        if not ref.get("action_id") and not ref.get("text"):
            err.append(f"{nid}: reference needs action_id or text")
        if ref.get("action_id") in actions and d0 is not None:
            if minutes(actions[ref["action_id"]]["at"]) - d0 >= 120:
                days_with_late[nd.get("discoverable_at", "")[:2]] += 1
        elif not ref.get("action_id") and d0 is not None:
            days_with_late[nd.get("discoverable_at", "")[:2]] += 1
        leaves(nd.get("check"), nid)
        if not nd.get("minutes"):
            err.append(f"{nid}: minutes missing")
    for tr in ep["traps"]:
        if tr.get("kind") not in TRAP_KINDS:
            err.append(f"{tr.get('id')}: kind {tr.get('kind')!r}")
        for e in tr.get("evidence", []):
            if e not in ids:
                err.append(f"{tr.get('id')}: evidence {e} does not exist")
        leaves(tr.get("check"), tr.get("id"))
    for k in ("median_hourly_wage", "employment", "observed_exposure", "minutes_model"):
        if k not in ep["economics"]:
            err.append(f"economics.{k} missing")

    arrivals = Counter(str(it["at"])[:2] for it in ep["items"] if it["at"] != "D0")
    if not 50 <= n_actions <= 75:
        warn.append(f"{n_actions} human actions (target ~60)")
    for d in range(1, 6):
        if not 15 <= arrivals.get(f"D{d}", 0) <= 30:
            warn.append(f"day {d}: {arrivals.get(f'D{d}', 0)} arrivals (target 15-30)")
        if days_with_late.get(f"D{d}", 0) < 2:
            warn.append(f"day {d}: {days_with_late.get(f'D{d}', 0)} needs the human leaves for later (target 2+)")
    if not 15 <= len(ep["needs"]) <= 25:
        warn.append(f"{len(ep['needs'])} needs (target 15-25)")
    if not 6 <= len(ep["traps"]) <= 10:
        warn.append(f"{len(ep['traps'])} traps (target 6-10)")
    stats = dict(actions=n_actions, calls=n_calls, items=len(items), needs=len(ep["needs"]), traps=len(ep["traps"]),
                 words=sum(len(str(it.get("body", "")).split()) for it in ep["items"]))
    return err, warn + [f"stats {stats}"]


bad = False
for p in sys.argv[2:]:
    e, w = check_episode(root / p)
    print(f"== {p}: {'OK' if not e else f'{len(e)} errors'}")
    for x in e:
        print("  ERROR", x)
    for x in w:
        print("  note ", x)
    bad |= bool(e)
sys.exit(1 if bad else 0)
