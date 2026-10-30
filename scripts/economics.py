"""The measured inputs of a Hulten-style back-of-envelope, and capability against observed use by task.

    uv run python scripts/economics.py results/final

Acemoglu ("The Simple Macroeconomics of AI", NBER w32487, 2024) puts the TFP gain from AI at the share of tasks
affected times the average cost saving on them: 20% of US labor tasks exposed x 23% profitable to automate = 4.6% of
tasks, with a 27% labor-cost saving on them (pp. 6, 30). This script measures the same two inputs for each job in
the run, on the calibrated scale (scripts/calibrate.py; it needs <results>/calibration.json):
- share of hours affected: the minutes of planned work a person would use (as is or after a small edit) over the
  worker's hours present;
- net labor-cost saving: net value per worker-week over the worker's weekly labor cost (loaded wage x hours present),
  and per affected hour (the saving divided by the share affected), which is the analogue of Acemoglu's 27%;
for each lab's newest models and for those in force on 1 January, by job and weighted by employment (BLS OEWS May
2025), with intervals from resampling the models and the hand grades together. It also compares, task by task, the
newest models' press-enter rate with observed AI use in the Anthropic Economic Index (task penetration, matched by
O*NET task statement). Writes <results>/economics.json.
"""
import csv
import datetime as dt
import difflib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from workweek import config  # noqa: E402
from workweek.engine import load_episode  # noqa: E402

JAN1 = dt.date(2026, 1, 1)
WEEKS_A_YEAR = 50
BOOT = 1000


def sig(b, s):
    return 1 / (1 + np.exp(-(b[0] + b[1] * s)))


def fit(X, y, w):
    b = np.zeros(X.shape[1])
    for _ in range(100):
        p = 1 / (1 + np.exp(-X @ b))
        step = np.linalg.solve(X.T @ (X * (w * p * (1 - p))[:, None]) + 1e-6 * np.eye(X.shape[1]), X.T @ (w * (y - p)))
        b += step
        if np.abs(step).max() < 1e-9:
            break
    return b


def norm(t: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", t.lower())


def main():
    res = Path(sys.argv[1])
    cfg = config.load(ROOT / "config/run.yaml")
    spec = {m.name: m for m in cfg.models}
    cal = json.loads((res / "calibration.json").read_text())
    rows = [json.loads(line) for line in (res / "graded.jsonl").read_text().splitlines()]

    latest, on_jan1 = {}, {}
    for r in rows:
        m = spec[r["model"]]
        latest[m.family] = max(latest.get(m.family, m.released), m.released)
        if m.released <= JAN1:
            on_jan1[m.family] = max(on_jan1.get(m.family, m.released), m.released)
    group = {n: ("newest" if m.released == latest.get(m.family) else "jan1" if m.released == on_jan1.get(m.family) else "")
             for n, m in spec.items()}

    # O*NET task statements and the Economic Index's task penetration (matched by text; close wording counts)
    statements = {}
    with open(ROOT / "data/onet/db_31_0_text/Task Statements.txt", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            statements[r["Task ID"]] = r["Task"]
    pen = {norm(r["task"]): float(r["penetration"]) for r in csv.DictReader(open(ROOT / "data/aei/task_penetration.csv"))}
    pen_keys = list(pen)

    def usage(task_id):
        t = statements.get(str(task_id))
        if not t:
            return None
        k = norm(t)
        if k in pen:
            return pen[k]
        close = difflib.get_close_matches(k, pen_keys, n=1, cutoff=0.93)
        return pen[close[0]] if close else None

    employment, eps = {}, {}
    for r in csv.DictReader(open(ROOT / "data/wages-onetonline-2026-10-26.csv")):
        employment[r["code"]] = float(r["employment"].replace(",", "")) if r["employment"] else 0.0

    # per week: the arrays the calibrated measures need
    weeks = []
    for r in rows:
        p = r["profession"]
        if p not in eps:
            ep = load_episode(ROOT / "professions" / p / "episode")
            present = sum(b - a for a, b in (ep.worker.day_hours(d) for d in range(1, 6))) / 60
            needs = {n.id: n for n in ep.needs}
            eps[p] = {"ep": ep, "present_min": present, "wage": ep.economics.loaded_hourly, "needs": needs,
                      "usage": {n.id: usage(n.onet_task_id) for n in ep.needs}, "soc": ep.meta.soc}
        e = eps[p]
        sc = np.array([(g["panel"].get("score") or 0) / 100 for g in r["graded"]])
        v = [g["value"] for g in r["graded"]]
        caught = [(n["need"], n["proposal"]) for n in r["needs"] if n["caught"]]
        weeks.append({
            "model": r["model"], "profession": p, "group": group[r["model"]],
            "planned": sum(e["needs"][n["need"]].minutes.do for n in r["needs"]),
            "need_ids": [n["need"] for n in r["needs"]],
            "caught_min": np.array([e["needs"][i].minutes.do for i, _ in caught]),
            "caught_s": np.array([sc[j] for _, j in caught]), "caught_ids": [i for i, _ in caught],
            "s": sc, "do": np.array([x["do_min"] for x in v], float), "read": np.array([x["read_min"] for x in v], float),
            "fix": np.array([x["fix_min"] for x in v], float), "tok": np.array([x["token_cost_usd_share"] for x in v], float),
            "supp": np.array([bool(x.get("suppressed")) for x in v]), "supp_val": np.array([x["value_usd"] for x in v], float),
            "questions": r.get("questions_cost_usd", 0.0)})

    def week_measures(w, b_as, b_use):
        e = eps[w["profession"]]
        p_as, p_use = sig(b_as, w["s"]), sig(b_use, w["s"])
        saved = np.where(w["do"] > 0, w["do"] * p_use - w["read"] - (p_use - p_as) * w["fix"], -w["read"])
        value = np.where(w["supp"], w["supp_val"], saved * e["wage"] / 60 - w["tok"]).sum() - w["questions"]
        used_min = (w["caught_min"] * sig(b_use, w["caught_s"])).sum()
        cost = e["wage"] * e["present_min"] / 60
        return {"affected": used_min / e["present_min"], "saving": value / cost, "value": value,
                "press_enter": (w["caught_min"] * sig(b_as, w["caught_s"])).sum() / max(w["planned"], 1e-9)}

    profs = sorted(eps)
    emp = {p: employment.get(eps[p]["soc"], 0.0) for p in profs}
    bill = {p: emp[p] * eps[p]["wage"] * eps[p]["present_min"] / 60 * WEEKS_A_YEAR for p in profs}

    def summarize(b_as, b_use, ws):
        out = {}
        for grp in ("newest", "jan1"):
            by = defaultdict(list)
            for w in ws:
                if w["group"] == grp:
                    by[w["profession"]].append(week_measures(w, b_as, b_use))
            jobs = {p: {k: float(np.mean([x[k] for x in v])) for k in v[0]} for p, v in by.items()}
            tot = sum(bill[p] for p in jobs)
            out[grp] = {"jobs": jobs,
                        "weighted": {k: sum(bill[p] * jobs[p][k] for p in jobs) / tot for k in ("affected", "saving")},
                        "annual_usd": sum(emp[p] * jobs[p]["value"] * WEEKS_A_YEAR for p in jobs)}
        return out

    b_as, b_use = np.array(cal["curves"]["as_is"]), np.array(cal["curves"]["use"])
    point = summarize(b_as, b_use, weeks)

    # the joint bootstrap: models (with all their weeks) and the hand grades, as in scripts/calibrate.py
    hg = [h for h in csv.DictReader(open(ROOT / cal["hand_grades"])) if not h["repeat_of"]]
    x = np.array([float(h["panel_score"]) / 100 for h in hg])
    y_as = np.array([h["verdict"] == "Send as is" for h in hg], float)
    y_use = np.array([h["verdict"] in ("Send as is", "Small edit") for h in hg], float)
    band = lambda s: 0 if s < 35 else 1 if s < 70 else 2  # noqa: E731
    cand = defaultdict(int)
    for r in rows:
        for g in r["graded"]:
            sc = g["panel"].get("score")
            if sc is not None and g["matches"] and not (g.get("value") or {}).get("suppressed"):
                cand[(r["profession"], band(sc), spec[r["model"]].family)] += 1
    taken = defaultdict(int)
    for h in hg:
        taken[(h["profession"], band(float(h["panel_score"])), h["lab"])] += 1
    wt = np.array([cand[(h["profession"], band(float(h["panel_score"])), h["lab"])] /
                   taken[(h["profession"], band(float(h["panel_score"])), h["lab"])] for h in hg])
    X = np.column_stack([np.ones_like(x), x])
    rng = np.random.default_rng(20261030)
    models = sorted({w["model"] for w in weeks})
    draws = defaultdict(list)
    for _ in range(BOOT):
        ms = rng.choice(models, len(models))
        ws = [w for m in ms for w in weeks if w["model"] == m]
        if not any(w["group"] == "newest" for w in ws) or not any(w["group"] == "jan1" for w in ws):
            continue
        i = rng.integers(0, len(hg), len(hg))
        o = summarize(fit(X[i], y_as[i], wt[i]), fit(X[i], y_use[i], wt[i]), ws)
        for grp in ("newest", "jan1"):
            for k in ("affected", "saving"):
                draws[(grp, k)].append(o[grp]["weighted"][k])
            draws[(grp, "per_affected")].append(o[grp]["weighted"]["saving"] / o[grp]["weighted"]["affected"])

    def ci(key):
        a = np.array(draws[key])
        return [round(float(np.percentile(a, 5)), 4), round(float(np.percentile(a, 95)), 4)]

    # task by task: the newest models' press-enter rate on each O*NET task against its observed use
    task_rows = defaultdict(lambda: {"planned": 0.0, "done": 0.0, "usage": None, "job": None})
    for w in weeks:
        if w["group"] != "newest":
            continue
        e = eps[w["profession"]]
        caught = dict(zip(w["caught_ids"], sig(b_as, w["caught_s"]) * w["caught_min"]))
        for nid in w["need_ids"]:
            n = e["needs"][nid]
            t = task_rows[(w["profession"], n.onet_task_id)]
            t["planned"] += n.minutes.do
            t["done"] += caught.get(nid, 0.0)
            t["usage"], t["job"] = e["usage"][nid], w["profession"]
    tasks = [{"job": k[0], "task_id": k[1], "statement": statements.get(str(k[1]), ""), "minutes": v["planned"],
              "press_enter": v["done"] / v["planned"] if v["planned"] else 0.0, "usage": v["usage"]}
             for k, v in task_rows.items()]
    known = [t for t in tasks if t["usage"] is not None]
    zero = [t for t in known if t["usage"] == 0]
    used = [t for t in known if t["usage"] > 0]

    def wmean(ts, k="press_enter"):
        m = sum(t["minutes"] for t in ts)
        return sum(t[k] * t["minutes"] for t in ts) / m if m else None

    # within jobs: the same comparison with each job's own mean removed
    within = []
    for p in profs:
        a = [t for t in zero if t["job"] == p]
        b = [t for t in used if t["job"] == p]
        if a and b:
            within.append({"job": p, "no_use": wmean(a), "use": wmean(b),
                           "minutes_no_use": sum(t["minutes"] for t in a), "minutes_use": sum(t["minutes"] for t in b)})

    out = {
        "acemoglu": {"share_of_tasks": 0.046, "labor_cost_saving_on_them": 0.27, "labor_share": 0.535,
                     "tfp_10_years": 0.0066, "source": "Acemoglu 2024, NBER w32487, pp. 6, 30-31"},
        "weeks_a_year": WEEKS_A_YEAR,
        "employment": emp,
        "newest": {**point["newest"], "weighted_90": {k: ci(("newest", k)) for k in ("affected", "saving", "per_affected")},
                   "per_affected": point["newest"]["weighted"]["saving"] / point["newest"]["weighted"]["affected"]},
        "jan1": {**point["jan1"], "weighted_90": {k: ci(("jan1", k)) for k in ("affected", "saving", "per_affected")},
                 "per_affected": point["jan1"]["weighted"]["saving"] / point["jan1"]["weighted"]["affected"]},
        "tasks": {"n": len(tasks), "matched": len(known), "no_use": len(zero), "use": len(used),
                  "minutes_no_use": sum(t["minutes"] for t in zero), "minutes_use": sum(t["minutes"] for t in used),
                  "press_enter_no_use": wmean(zero), "press_enter_use": wmean(used), "within_jobs": within,
                  "rows": sorted(tasks, key=lambda t: (t["job"], -t["minutes"]))},
    }
    (res / "economics.json").write_text(json.dumps(out, indent=1, default=float) + "\n")
    s = {k: out[k] for k in ("newest", "jan1")}
    print(json.dumps({k: {"weighted": v["weighted"], "weighted_90": v["weighted_90"], "per_affected": v["per_affected"],
                          "annual_usd_bn": v["annual_usd"] / 1e9,
                          "jobs": {p: {kk: round(vv, 3) for kk, vv in j.items() if kk != "value"} for p, j in v["jobs"].items()}}
                      for k, v in s.items()}, indent=1))
    print(json.dumps({k: v for k, v in out["tasks"].items() if k != "rows"}, indent=1))


if __name__ == "__main__":
    main()
