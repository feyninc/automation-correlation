"""The compiler: a profession's hand-written week (professions/<profession>/) -> professions/<profession>/episode/ (one file per day).

Deterministic: it expands the compact authoring format, adds the economics from local data, validates the result,
runs the shared check evaluator over the worker's own actions (every need must pass on its reference, no trap may
fire on anything the worker did), and writes a report with the week's volumes and its task mix against O*NET.

    uv run python -m workweek.compile professions/<profession> [...]
"""
from __future__ import annotations

import csv
import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

from . import checks
from .apps import REGISTRY, document_file, thread_file
from .schema import (Contact, Document, Economics, Employer, Episode, Exchange, Meta, Minutes, MinutesModel, Need, StateChange,
                     Reference, Rubric, Sourced, Thread, Trap, Version, Worker, WorkerAction, fmt, seconds)

ROOT = Path(__file__).resolve().parents[1]
ONET = ROOT / "data/onet/db_31_0_text"
SPEAK_WPM = 150      # conversational speech, for timing call turns


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


# ---------- local data ----------

def _onet_tasks(soc: str) -> dict[str, dict]:
    tasks = {}
    with open(ONET / "Task Statements.txt", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["O*NET-SOC Code"] == soc:
                tasks[r["Task ID"]] = {"task": r["Task"], "type": r["Task Type"], "FT": None, "IM": None}
    with open(ONET / "Task Ratings.txt", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["O*NET-SOC Code"] == soc and r["Task ID"] in tasks:
                if r["Scale ID"] == "IM":
                    tasks[r["Task ID"]]["IM"] = float(r["Data Value"])
                elif r["Scale ID"] == "FT":   # frequency: categories 1..7; keep the distribution
                    tasks[r["Task ID"]].setdefault("FT_dist", {})[r["Category"]] = float(r["Data Value"])
    for t in tasks.values():
        dist = t.pop("FT_dist", {})
        if dist:   # expected category (1 = yearly or less ... 7 = hourly or more)
            t["FT"] = sum(int(k) * v for k, v in dist.items()) / max(sum(dist.values()), 1e-9)
    return tasks


def _penetration(tasks: dict[str, dict]) -> dict[str, float]:
    pen = {}
    with open(ROOT / "data/aei/task_penetration.csv", encoding="utf-8") as f:
        table = {r["task"].strip().lower(): float(r["penetration"]) for r in csv.DictReader(f)}
    for tid, t in tasks.items():
        v = table.get(t["task"].strip().lower())
        if v is not None:
            pen[tid] = v
    return pen


def _economics(form: dict, tasks: dict) -> Economics:
    soc = form["soc"]
    wages = {r["code"]: r for r in csv.DictReader(open(ROOT / "data/wages-onetonline-2026-10-26.csv"))}
    w = wages[soc]
    exposure = {r["occ_code"]: float(r["observed_exposure"]) for r in csv.DictReader(open(ROOT / "data/aei/job_exposure.csv"))}
    ecec = {r["sector"]: r for r in csv.DictReader(open(ROOT / "data/ecec-2026-06.csv"))}
    e = ecec[form["ecec_sector"]]
    eci = yaml.safe_load(open(ROOT / "data/eci.yaml"))
    proj = form.get("projection") or (f"{w['projected_growth']} ({w['projection_period']}), "
                                      f"{w['projected_openings']} openings a year" if w["projected_growth"] else "")
    return Economics(
        soc=soc, title=form["title"],
        median_hourly_wage=Sourced(value=float(w["median_hourly"]), source=f"BLS OEWS May {w['wage_year']} via O*NET OnLine (data/wages-onetonline-2026-10-26.csv)"),
        eci_factor=Sourced(value=float(eci["factor"]), source=eci["source"], note=eci.get("note", "")),
        loaded_multiplier=Sourced(value=round(float(e["total"]) / float(e["wages"]), 3),
                                  source=f"BLS ECEC {e['period']}, {e['sector']}: total compensation ${e['total']} / wages ${e['wages']} ({e['source']})"),
        employment=Sourced(value=float(w["employment"].replace(",", "")), source=f"BLS via O*NET OnLine, {w['employment_year']}"),
        projection=proj,
        observed_exposure=Sourced(value=exposure[soc[:7]], source="Anthropic Economic Index, labor market impacts (Massenkoff and McCrory, 2026-03-05)"),
        task_penetration=_penetration(tasks),
        minutes_model=MinutesModel(**form.get("minutes_model", {})),
    )


# ---------- expansion ----------

def _exchange(raw: dict, tid: str, n: int) -> Exchange:
    return Exchange(id=raw.get("id") or f"{tid}.{n}", at=raw["at"], author=raw["from"], to=raw.get("to", []),
                    cc=raw.get("cc", []), subject=raw.get("subject"), body=str(raw["body"]).strip(),
                    attachments=raw.get("att", []), meta=raw.get("meta", {}))


def _call(raw: dict) -> Thread:
    """A live call: turns get times from their length at conversational speed plus the caller's pause."""
    t = seconds(raw["start"])
    xs = []
    for n, turn in enumerate(raw["turns"], 1):
        who, text = turn[0], turn[1]
        meta = {"patience_s": turn[2]} if len(turn) > 2 else {}
        xs.append(Exchange(id=f"{raw['id']}.{n}", at=fmt(t), author=who, body=str(text).strip(), meta=meta))
        t += max(2, round(len(str(text).split()) / SPEAK_WPM * 60)) + (2 if who == "worker" else 1)
    return Thread(id=raw["id"], app="phone", path=raw["path"], title=raw["title"], live=True,
                  state=raw.get("state", {}), exchanges=xs)


def _traffic(tf: dict, worker: dict) -> list[Thread]:
    """Recurring low-information items (system notifications, digests, channel chatter), expanded deterministically:
    `per_day` items on each of `days`, spread over the worker's hours with a jitter seeded by the id, cycling through
    `items` ({n} is the item's running number). With `group: true` they are exchanges in one thread (a chat channel),
    otherwise each is a thread of its own under `path`."""
    rng = random.Random(tf["id"])
    hours = worker.get("hours", {})
    threads: dict[str, Thread] = {}
    n = 0
    for day in tf.get("days", [1, 2, 3, 4, 5]):
        a, b = hours.get(f"D{day}", ["08:00", "17:00"])
        a, b = tf.get("hours", [a, b])
        lo = int(a[:2]) * 60 + int(a[3:]) + 5
        hi = int(b[:2]) * 60 + int(b[3:]) - 5
        k = int(tf["per_day"])
        slots = sorted(lo + (hi - lo) * (i + rng.random()) / k for i in range(k))
        for minute in slots:
            n += 1
            item = tf["items"][(n - 1) % len(tf["items"])]
            at = f"D{day} {int(minute) // 60:02d}:{int(minute) % 60:02d}"
            fill = lambda x: str(x).replace("{n}", str(n))
            tid = tf["id"] if tf.get("group") else f"{tf['id']}-{n}"
            th = threads.setdefault(tid, Thread(id=tid, app=tf["app"], title=fill(tf.get("title", item.get("subject", tf["id"]))),
                                                path=tf["path"] if tf.get("group") else f"{tf['path']}-{n}", exchanges=[]))
            th.exchanges.append(Exchange(id=f"{tid}.{len(th.exchanges) + 1}", at=at, author=item.get("from", tf["from"]),
                                         to=["worker"] if tf["app"] == "mail" else [], subject=fill(item["subject"]) if item.get("subject") else None,
                                         body=fill(item["body"]).strip(), meta={"traffic": True}))
    return list(threads.values())


def call_line_window(th: Thread, xid: str) -> tuple[str, str]:
    """A worker's call line is needed from the caller turn it answers until just before the caller speaks again."""
    xs = [x for x in th.exchanges if not x.meta.get("case_note")]
    i = next(k for k, x in enumerate(xs) if x.id == xid)
    start = next(seconds(x.at) for x in reversed(xs[:i]) if x.author != "worker")
    after = next((seconds(x.at) for x in xs[i + 1:] if x.author != "worker"), seconds(xs[i].at) + 30)
    return fmt(start), fmt(after - 1)


def expand(form: dict) -> Episode:
    contacts = [Contact(id=c[0], name=c[1], role=c[2], org=c[3], email=c[4] or None, phone=(c[5] if len(c) > 5 else None) or None,
                        relation=c[6] if len(c) > 6 else "", notes=c[7] if len(c) > 7 else "")
                for c in form["contacts"]]
    docs: dict[str, Document] = {}
    for d in form.get("documents", []):
        if d["id"] in docs:             # a later day's entry for the same id is a new version
            if not ("at" in d and "content" in d):
                raise ValueError(f"document {d['id']} defined twice (a new version needs at and content)")
            docs[d["id"]].versions.append(Version(at=d["at"], author=d.get("author", "worker"), content=str(d["content"]),
                                                  note=d.get("note", "")))
            docs[d["id"]].versions.sort(key=lambda v: seconds(v.at))
            continue
        versions = d.get("versions") or [{"at": d.get("at", "D0"), "author": d.get("author", "worker"), "content": d["content"]}]
        docs[d["id"]] = Document(id=d["id"], app=d.get("app", "docs"), path=d["path"], title=d["title"],
                                 format=d.get("format", "md"),
                                 versions=[Version(at=v["at"], author=v.get("author", "worker"), content=str(v["content"]),
                                                   note=v.get("note", "")) for v in versions])
    threads: dict[str, Thread] = {}
    for t in form.get("threads", []):
        th = threads.get(t["id"])
        if th is None:
            th = threads[t["id"]] = Thread(id=t["id"], app=t["app"], path=t["path"], title=t["title"],
                                           state=t.get("state", {}), exchanges=[])
        elif t.get("state"):                    # a later day's entry for the same id continues the thread
            th.state_changes.append(StateChange(at=t["x"][0]["at"], set=t["state"]))
        n0 = len(th.exchanges)
        th.exchanges += [_exchange(x, t["id"], n0 + i) for i, x in enumerate(t["x"], 1)]
    for c in form.get("calls", []):
        threads[c["id"]] = _call(c)
    for tf in form.get("traffic", []):
        for th in _traffic(tf, form["worker"]):
            if th.id in threads:
                threads[th.id].exchanges += th.exchanges
            else:
                threads[th.id] = th

    actions, produced = [], {}
    for i, a in enumerate(form.get("actions", []), 1):
        aid = a.get("id") or f"a{i:03d}"
        prod = None
        kind = a["kind"]
        tgt = a["target"]
        if kind in ("reply", "new", "forward", "update", "say") and "body" in a:
            if tgt not in threads:     # a new thread the worker starts
                threads[tgt] = Thread(id=tgt, app=a["app"], path=a["path"], title=a.get("title") or a.get("subject") or tgt,
                                      exchanges=[])
            th = threads[tgt]
            x = Exchange(id=f"{tgt}.w{len(th.exchanges) + 1}", at=a["at"], author="worker", to=a.get("to", []),
                         cc=a.get("cc", []), subject=a.get("subject"), body=str(a["body"]).strip(), attachments=a.get("att", []),
                         meta={"case_note": True} if th.live and kind == "update" else {})
            th.exchanges.append(x)
            th.exchanges.sort(key=lambda e: seconds(e.at))
            prod = x.id
        elif kind == "edit" and "content" in a:
            if tgt not in docs:
                docs[tgt] = Document(id=tgt, app=a.get("app", "docs"), path=a["path"], title=a.get("title", tgt),
                                     format=a.get("format", "md"), versions=[])
            d = docs[tgt]
            d.versions.append(Version(at=a["at"], author="worker", content=str(a["content"]), note=a.get("summary", "")))
            d.versions.sort(key=lambda v: seconds(v.at))
            prod = (tgt, a["at"])        # resolved to a version index once every version is in
        if "update_state" in a and tgt in threads:
            threads[tgt].state_changes.append(StateChange(at=a["at"], set=a["update_state"]))
        produced[aid] = prod
        actions.append(WorkerAction(id=aid, at=a["at"], kind=kind, target=tgt, produces=None if isinstance(prod, tuple) else prod,
                                    summary=a["summary"], note=a.get("note", ""), minutes=float(a.get("minutes", 0))))

    for aid, prod in list(produced.items()):
        if isinstance(prod, tuple):
            d = docs[prod[0]]
            produced[aid] = f"{prod[0]}@{next(i for i, v in enumerate(d.versions) if v.at == prod[1] and v.author == 'worker')}"
    for a in actions:
        a.produces = produced[a.id]
    turns = {x.id for t in threads.values() if t.live for x in t.exchanges if x.author == "worker"}
    needs = []
    for n in form["needs"]:
        ref = n.get("ref")
        if ref in turns:
            n = {**n, **dict(zip(("from", "due"), call_line_window(threads[ref.rsplit(".", 1)[0]], ref)))}
        if ref and produced.get(ref):
            p = produced[ref]
            reference = Reference(document_version=p) if "@" in p else Reference(exchange_id=p)
        elif ref in turns:          # the worker's own line on a call
            reference = Reference(exchange_id=ref)
        elif ref:
            raise ValueError(f"{n['id']}: ref {ref} is neither a worker action that writes something nor a worker's call line")
        else:
            reference = Reference(text=n["ref_text"])
        needs.append(Need(id=n["id"], title=n["title"], kind=n["kind"], onet_task_id=str(n["task"]),
                          discoverable_at=n["from"], deadline=n["due"], evidence=n["evidence"], reference=reference,
                          check=n["check"], rubric=Rubric(must=n["must"], must_not=n.get("must_not", [])),
                          minutes=Minutes(do=float(n["minutes"][0]), source=n["minutes"][1]),
                          worker_intent=n["intent"].strip(), ledger_keys=n.get("ledger", [])))
    traps = [Trap(id=t["id"], title=t["title"], kind=t["kind"], evidence=t["evidence"], check=t["check"],
                  correct_behavior=t["correct"], severity=t["severity"], harm_usd_upper=t.get("harm_usd_upper"),
                  source=t.get("source", ""), worker_mistakes=t.get("worker_mistakes", [])) for t in form["traps"]]

    tasks = _onet_tasks(form["soc"])
    ep = Episode(
        meta=Meta(soc=form["soc"], title=form["title"], generator="workweek.compile (hand-written week)"),
        economics=_economics(form, tasks),
        employer=Employer(**form["employer"]), worker=Worker(**form["worker"]),
        profession_prompt=form["profession_prompt"].strip(), apps=form["apps"], contacts=contacts,
        threads=sorted(threads.values(), key=lambda t: (t.app, t.path)), documents=list(docs.values()),
        worker_actions=sorted(actions, key=lambda a: seconds(a.at)), needs=needs, traps=traps,
        ledger=form.get("ledger", {}),
        grounding={"sources": form.get("sources", []), "onet_tasks": {k: v for k, v in tasks.items()}})
    return ep


# ---------- checks ----------

def reference_prop(ep: Episode, a: WorkerAction) -> checks.Prop | None:
    th = next((t for t in ep.threads if t.id == a.target), None)
    if a.produces and th:
        x = next(x for x in th.exchanges if x.id == a.produces)
        return checks.Prop(t=seconds(a.at), app=th.app, path=th.path, target=th.id,
                           action=checks.normalize_action(th.app, a.kind),
                           drafts=[checks.Draft(text=x.body, to=x.to, cc=x.cc, subject=x.subject or "")])
    d = next((d for d in ep.documents if d.id == a.target), None)
    if a.produces and d:
        v = d.versions[int(a.produces.split("@")[1])]
        return checks.Prop(t=seconds(a.at), app=d.app, path=d.path, target=d.id, action="edit",
                           drafts=[checks.Draft(text=v.content)])
    return None


def call_line_prop(ep: Episode, xid: str) -> checks.Prop | None:
    for th in ep.threads:
        x = next((x for x in th.exchanges if x.id == xid and th.live and x.author == "worker"), None)
        if x:
            return checks.Prop(t=seconds(x.at), app=th.app, path=th.path, target=th.id, action="say",
                               drafts=[checks.Draft(text=x.body)])
    return None


_STRUCTURAL = {"app", "path", "path_prefix", "target", "action_in", "to_includes", "before", "after"}


def content_only(pred: dict) -> dict | bool:
    """The predicate with every structural leaf (where, to whom, when) taken as satisfied; True if nothing is left."""
    (k, v), = pred.items()
    if k in ("all", "any"):
        kept = [q for q in (content_only(q) for q in v) if q is not True]
        if k == "any" and len(kept) < len(v):
            return True
        return {k: kept} if kept else True
    if k == "not" or k in _STRUCTURAL:
        return True
    return pred


def audit(ep: Episode) -> tuple[list[str], list[str]]:
    errs, warns = [], []
    tasks = ep.grounding["onet_tasks"]
    ids = {t.id for t in ep.threads} | {x.id for t in ep.threads for x in t.exchanges} | {d.id for d in ep.documents}
    people = {c.id for c in ep.contacts} | {"worker"}
    for a in ep.apps:
        if a not in REGISTRY:
            errs.append(f"unknown app {a}")
    for d, b in time_budget(ep).items():
        if not 0.8 <= b["share"] <= 1.1:
            warns.append(f"D{d}: the day's work accounts for {b['share']:.0%} of the {b['present']:.0f} minutes present "
                         "(aim for 80-110%)")
    for a in ep.worker_actions:
        day = seconds(a.at) // 86400 + 1
        start, end = ep.worker.day_hours(day)
        if not start <= seconds(a.at) % 86400 <= end:
            warns.append(f"{a.id}: worker acts at {a.at}, outside working hours")
    for t in ep.threads:
        if REGISTRY.get(t.app) is None or REGISTRY[t.app].kind != "thread":
            errs.append(f"thread {t.id} uses {t.app}, which is not a thread app")
    for d in ep.documents:
        if REGISTRY.get(d.app) is None or REGISTRY[d.app].kind != "document":
            errs.append(f"document {d.id} uses {d.app}, which is not a document app")
    seen: dict[str, str] = {}
    for item in [*ep.threads, *ep.documents]:
        f = thread_file(item) if isinstance(item, Thread) else document_file(item)
        if f in seen:
            errs.append(f"{item.id} and {seen[f]} both render to {f}")
        seen.setdefault(f, item.id)
    produced = {a.produces: a for a in ep.worker_actions if a.produces}
    for n in ep.needs:
        if n.onet_task_id not in tasks:
            errs.append(f"{n.id}: task {n.onet_task_id} is not one of {ep.meta.soc}'s O*NET tasks")
        for k, v in checks.leaves(n.check):
            if k == "target" and v not in ids:
                errs.append(f"{n.id}: check target {v} does not exist")
            if k == "to_includes" and v not in people:
                errs.append(f"{n.id}: check contact {v} does not exist")
            if k in ("mentions_any", "mentions_all"):
                for term in v:
                    if len(str(term).strip()) < 3 and not str(term).strip().isdigit():
                        warns.append(f"{n.id}: very short mention {term!r}")
        ref = n.reference.exchange_id or n.reference.document_version
        if ref:
            a = produced.get(ref)
            p = reference_prop(ep, a) if a else call_line_prop(ep, ref)
            if p is None:
                errs.append(f"{n.id}: reference {ref} has no worker action")
            else:
                p.t = min(p.t, seconds(n.deadline))
                if checks.matches(n.check, p) is None:
                    errs.append(f"{n.id}: check does not pass on the worker's own {a.id if a else 'call line ' + ref}")
        else:
            pred = content_only(n.check)
            p = checks.Prop(t=0, app="", path="", target="", action="", drafts=[checks.Draft(text=n.reference.text)])
            if pred is not True and checks.matches(pred, p) is None:
                errs.append(f"{n.id}: the mentions in its check are not in its own reference text")
    for a in ep.worker_actions:
        p = reference_prop(ep, a)
        if p is None:
            continue
        for tr in ep.traps:
            if a.id not in tr.worker_mistakes and checks.matches(tr.check, p) is not None:
                errs.append(f"trap {tr.id} fires on the worker's own action {a.id}")
    return errs, warns


TRIAGE_S = 20        # skimming one inbound item (Microsoft WTI 2025: most email skimmed in under a minute)


def time_budget(ep: Episode) -> dict[int, dict]:
    """Per day: minutes present, and minutes accounted for by the needs the worker does that day, other timed
    actions (meetings, in-person work), lunch, and skimming the inbound items."""
    out = {}
    for d in range(1, 6):
        a, b = ep.worker.day_hours(d)
        on_day = lambda t: seconds(t) // 86400 + 1 == d
        done = {x.id: x.at for th in ep.threads for x in th.exchanges if x.author == "worker"}
        done |= {f"{doc.id}@{i}": v.at for doc in ep.documents for i, v in enumerate(doc.versions) if v.author == "worker"}
        ref = lambda n: done.get(n.reference.exchange_id or n.reference.document_version or "")
        needs = sum(n.minutes.do for n in ep.needs if ref(n) and on_day(ref(n)))
        busy = sum(x.minutes for x in ep.worker_actions if on_day(x.at))
        inbound = sum(1 for th in ep.threads for x in th.exchanges if x.author != "worker" and on_day(x.at)
                      and not (th.live and not x.id.endswith(".1")))
        present = (b - a) / 60
        acc = needs + busy + ep.worker.lunch_minutes + inbound * TRIAGE_S / 60
        out[d] = {"present": present, "needs": needs, "other": busy, "lunch": ep.worker.lunch_minutes,
                  "skim": inbound * TRIAGE_S / 60, "inbound": inbound, "accounted": acc, "share": acc / present}
    return out


def report(ep: Episode, errs: list[str], warns: list[str]) -> str:
    days = defaultdict(Counter)
    for t in ep.threads:
        for i, x in enumerate(t.exchanges):
            d = max(1, seconds(x.at) // 86400 + 1) if x.at != "D0" else 0
            days[d][f"{t.app} exchanges"] += 1
            if i == 0:
                days[d][f"{t.app} threads"] += 1
    for a in ep.worker_actions:
        days[seconds(a.at) // 86400 + 1]["worker actions"] += 1
    for n in ep.needs:
        days[seconds(n.discoverable_at) // 86400 + 1]["needs"] += 1
    cols = sorted({k for c in days.values() for k in c})
    lines = [f"# {ep.meta.title} ({ep.meta.soc}): build report", "",
             f"{len(ep.needs)} needs, {len(ep.traps)} traps, {len(ep.worker_actions)} worker actions, "
             f"{len(ep.threads)} threads, {len(ep.documents)} documents, "
             f"{sum(len(str(x.body).split()) for t in ep.threads for x in t.exchanges) + sum(len(v.content.split()) for d in ep.documents for v in d.versions):,} words.",
             "", "| day | " + " | ".join(cols) + " |", "| --- |" + " --- |" * len(cols)]
    for d in sorted(days):
        lines.append(f"| {'D0' if d == 0 else 'D' + str(d)} | " + " | ".join(str(days[d].get(c, 0)) for c in cols) + " |")
    lines += ["", "## Time budget (minutes)", "",
              "| day | present | needs done | other timed work | lunch | skimming inbound | inbound items | accounted |",
              "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for d, b in time_budget(ep).items():
        lines.append(f"| D{d} | {b['present']:.0f} | {b['needs']:.0f} | {b['other']:.0f} | {b['lunch']} | {b['skim']:.0f} | "
                     f"{b['inbound']} | {b['accounted']:.0f} ({b['share']:.0%}) |")
    tasks = ep.grounding["onet_tasks"]
    use = Counter(n.onet_task_id for n in ep.needs)
    lines += ["", "## Task mix against O*NET", "",
              "| task | importance | frequency (1-7) | needs | penetration |", "| --- | --- | --- | --- | --- |"]
    for tid, t in sorted(tasks.items(), key=lambda kv: -(kv[1]["IM"] or 0)):
        lines.append(f"| {tid} {t['task'][:70]} | {t['IM'] or ''} | {round(t['FT'], 2) if t['FT'] else ''} | {use.get(tid, 0)} | "
                     f"{ep.economics.task_penetration.get(tid, '')} |")
    lines += ["", f"## Errors ({len(errs)})", *[f"- {e}" for e in errs], "", f"## Warnings ({len(warns)})", *[f"- {w}" for w in warns]]
    return "\n".join(lines) + "\n"


LIST_KEYS = ("contacts", "documents", "threads", "calls", "actions", "needs", "traps", "sources", "traffic")


def load_form(path: str | Path) -> dict:
    """A profession folder: week.yaml (the header) plus any day*.yaml files, whose lists are concatenated."""
    path = Path(path)
    files = [path] if path.is_file() else [path / "week.yaml", *sorted(path.glob("day*.yaml"))]
    form: dict = {}
    for f in files:
        part = yaml.safe_load(f.read_text()) or {}
        for k, v in part.items():
            if k in LIST_KEYS:
                form.setdefault(k, []).extend(v or [])
            elif k == "ledger":
                form.setdefault("ledger", {}).update(v)
            elif k in form:
                raise ValueError(f"{f}: key {k} set twice")
            else:
                form[k] = v
    return form


DATES = ["2026-11-02", "2026-11-03", "2026-11-04", "2026-11-05", "2026-11-06"]


def _day(t: str) -> int:
    """1..5, or 0 for D0."""
    return 0 if t == "D0" else seconds(t) // 86400 + 1


def split_days(ep: Episode) -> dict[str, dict]:
    """profession.json (the job, people, economics, Monday-morning documents) and one file per day holding what
    happens that day: exchanges and document versions that arrive, worker actions, needs that become discoverable,
    traps whose first evidence appears."""
    data = ep.model_dump(mode="json")
    first_seen: dict[str, int] = {}
    for t in ep.threads:
        for x in t.exchanges:
            first_seen.setdefault(t.id, _day(x.at))
            first_seen[x.id] = _day(x.at)
    for d in ep.documents:
        first_seen[d.id] = _day(d.versions[0].at)
    head = {k: data[k] for k in ("meta", "economics", "employer", "worker", "profession_prompt", "apps", "contacts",
                                 "ledger", "grounding")}
    head["documents"] = []
    days = {i: {"date": DATES[i - 1], "threads": [], "documents": [], "worker_actions": [], "needs": [], "traps": []}
            for i in range(1, 6)}
    for t in data["threads"]:
        by: dict[int, list] = defaultdict(list)
        for x in t["exchanges"]:
            by[max(1, _day(x["at"]))].append(x)
        changes: dict[int, list] = defaultdict(list)
        for c in t["state_changes"]:
            changes[max(1, _day(c["at"]))].append(c)
        first = min(by)
        for i in sorted(set(by) | set(changes)):
            rec = {k: v for k, v in t.items() if k not in ("exchanges", "state_changes")}
            if i != first:
                rec["state"] = {}
            days[i]["threads"].append({**rec, "state_changes": changes.get(i, []), "exchanges": by.get(i, [])})
    for d in data["documents"]:
        by = defaultdict(list)
        for v in d["versions"]:
            by[_day(v["at"])].append(v)
        for i, vs in by.items():
            rec = {**{k: v for k, v in d.items() if k != "versions"}, "versions": vs}
            (head["documents"] if i == 0 else days[i]["documents"]).append(rec)
    for a in data["worker_actions"]:
        days[_day(a["at"])]["worker_actions"].append(a)
    for n in data["needs"]:
        days[_day(n["discoverable_at"])]["needs"].append(n)
    for tr in data["traps"]:
        first = min((first_seen.get(e, 5) for e in tr["evidence"]), default=1)
        days[max(1, first)]["traps"].append(tr)
    return {"profession.json": head, **{f"{days[i]['date']}.json": days[i] for i in days}}


def merge_days(folder: str | Path) -> Episode:
    """Inverse of split_days: read professions/<profession>/episode/ back into one Episode."""
    folder = Path(folder)
    head = json.loads((folder / "profession.json").read_text())
    threads: dict[str, dict] = {}
    docs: dict[str, dict] = {d["id"]: d for d in head.pop("documents")}
    acts, needs, traps = [], [], []
    for date in DATES:
        day = json.loads((folder / f"{date}.json").read_text())
        for t in day["threads"]:
            if t["id"] in threads:
                threads[t["id"]]["exchanges"] += t["exchanges"]
                threads[t["id"]]["state_changes"] += t["state_changes"]
            else:
                threads[t["id"]] = t
        for d in day["documents"]:
            if d["id"] in docs:
                docs[d["id"]]["versions"] += d["versions"]
            else:
                docs[d["id"]] = d
        acts += day["worker_actions"]
        needs += day["needs"]
        traps += day["traps"]
    return Episode.model_validate({**head, "threads": list(threads.values()), "documents": list(docs.values()),
                                   "worker_actions": acts, "needs": needs, "traps": traps})


def _canonical(ep: Episode) -> dict:
    """The episode with every list of records in id order, so day-splitting order doesn't count as a change."""
    d = ep.model_dump(mode="json")
    d["meta"].pop("sha256", None)
    for k in ("threads", "documents", "worker_actions", "needs", "traps", "contacts"):
        d[k] = sorted(d[k], key=lambda r: r["id"])
    for t in d["threads"]:
        t["exchanges"] = sorted(t["exchanges"], key=lambda x: (x["at"], x["id"]))
        t["state_changes"] = sorted(t["state_changes"], key=lambda c: c["at"])
    return d


def build(path: str | Path) -> tuple[Episode, list[str]]:
    path = Path(path)
    form = load_form(path)
    ep = expand(form)
    errs, warns = audit(ep)
    out = (path if path.is_dir() else path.parent) / "episode"
    out.mkdir(parents=True, exist_ok=True)
    blob = json.dumps(ep.model_dump(mode="json"), ensure_ascii=False, sort_keys=True).encode()
    ep.meta.sha256 = hashlib.sha256(blob).hexdigest()
    for name, part in split_days(ep).items():
        (out / name).write_text(json.dumps(part, indent=1, ensure_ascii=False) + "\n")
    back = merge_days(out)
    if _canonical(back) != _canonical(ep):
        errs.append("split/merge round trip changed the episode")
    (out.parent / "report.md").write_text(report(ep, errs, warns))
    return ep, errs


if __name__ == "__main__":
    bad = False
    for p in sys.argv[1:]:
        ep, errs = build(p)
        print(f"{ep.meta.soc}: {len(ep.needs)} needs, {len(ep.traps)} traps, {len(ep.worker_actions)} actions, "
              f"{len(ep.threads)} threads, {len(errs)} errors")
        for e in errs[:30]:
            print("  ERROR", e)
        bad |= bool(errs)
    sys.exit(1 if bad else 0)
