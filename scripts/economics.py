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
O*NET task statement). Writes <results>/economics.json, and <results>/post/ with every other number the write-up
quotes (post.json, workweek-tasks.csv, intervals.md): the five labs' means on the four dates, the within-lab pace with
each lab left out, the halving time of inference cost per finished hour, the worked example, late call lines, and
Acemoglu's own exposure rule applied to the run's jobs (data/eloundou/).
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
EXPOSED_US, PROFITABLE = 0.199, 0.23    # Acemoglu's two factors of his 4.6%: Eloundou et al. x Svanberg et al. (p. 24)


# O*NET 31.0 task statements the Economic Index holds under their older wording, too far apart for the fuzzy match
RENAMED = {
    "23994": "Prepare legal documents, including briefs, pleadings, appeals, wills, contracts, and real estate closing "
             "statements.",   # 31.0 adds "edit, or review" and "legislation"
}


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
        t = RENAMED.get(str(task_id)) or statements.get(str(task_id))
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
            "lab": spec[r["model"]].family, "released": spec[r["model"]].released,
            "cost_usd": r.get("token_cost_usd") or 0.0, "proposals": r["proposals"],
            "traps": len(r["traps"]), "fired": sum(t["fired"] for t in r["traps"]),
            "on_time": [g["timing"]["on_time_streaming"] for g in r["graded"]
                        if (g.get("timing") or {}).get("on_time_streaming") is not None],
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
        done_min = (w["caught_min"] * sig(b_as, w["caught_s"])).sum()
        cost = e["wage"] * e["present_min"] / 60
        return {"affected": used_min / e["present_min"], "saving": value / cost, "value": value,
                "press_enter": done_min / max(w["planned"], 1e-9), "finished": done_min / e["present_min"]}

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
                        "weighted": {k: sum(bill[p] * jobs[p][k] for p in jobs) / tot
                                     for k in ("affected", "saving", "finished")},
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
            for k in ("affected", "saving", "finished"):
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
        "newest": {**point["newest"],
                   "weighted_90": {k: ci(("newest", k)) for k in ("affected", "saving", "finished", "per_affected")},
                   "per_affected": point["newest"]["weighted"]["saving"] / point["newest"]["weighted"]["affected"]},
        "jan1": {**point["jan1"],
                 "weighted_90": {k: ci(("jan1", k)) for k in ("affected", "saving", "finished", "per_affected")},
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
    post(res, cal, out, weeks, eps, bill, b_as, lambda w: week_measures(w, b_as, b_use))


def eloundou_exposed(socs: dict[str, str]) -> tuple[dict[str, float], float]:
    """Acemoglu's exposure rule (NBER w32487, p. 24: a task is exposed when Eloundou et al.'s automation index puts
    more than 50% of its activities within reach) applied to each job's O*NET tasks, as a share of the job's tasks;
    and the unweighted mean over every occupation, a check against his wage-bill-weighted 19.9%."""
    by = defaultdict(list)
    with open(ROOT / "data/eloundou/full_labelset.tsv", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            by[r["O*NET-SOC Code"]].append(float(r["automation"]) > 0.5)
    share = {p: float(np.mean(by[soc])) for p, soc in socs.items()}
    return share, float(np.mean([np.mean(v) for k, v in by.items() if k.endswith(".00")]))


def post(res: Path, cal: dict, econ: dict, weeks: list[dict], eps: dict, bill: dict, b_as, measure) -> None:
    """Every number the write-up quotes that the other outputs do not hold, in <results>/post/: post.json (the five
    labs' means on the four dates, the within-lab pace with each lab left out, the halving time of inference cost per
    finished hour, the worked example, late call lines, Acemoglu's rule on the run's jobs, the press-enter rate with
    every piece of work counted once, the panel's rank correlation with the hand grades), workweek-tasks.csv (the
    task scatter) and intervals.md (the headline intervals)."""
    out = res / "post"
    out.mkdir(exist_ok=True)
    rank = {}                                         # each lab's models by release: the four dates
    for lab in {w["lab"] for w in weeks}:
        for i, (_, m) in enumerate(sorted({(w["released"], w["model"]) for w in weeks if w["lab"] == lab})):
            rank[m] = i
    per = defaultdict(list)
    for w in weeks:
        x = measure(w)
        att = w["caught_min"].sum() / max(w["planned"], 1e-9)
        per[w["model"]].append({**x, "attempted": att, "finished_h": x["press_enter"] * w["planned"] / 60,
                                "usable": x["affected"] * eps[w["profession"]]["present_min"] / max(w["planned"], 1e-9),
                                "cost": w["cost_usd"], "read_h": w["read"].sum() / 60, "proposals": w["proposals"],
                                "fired": w["fired"], "trap_share": w["fired"] / max(w["traps"], 1),
                                # robustness: every piece of planned work counted once, not by its minutes
                                "press_enter_equal": float(sig(b_as, w["caught_s"]).sum()) / max(len(w["need_ids"]), 1)})
    models = {m: {k: float(np.mean([x[k] for x in v])) for k in v[0]} for m, v in per.items()}
    for m, v in per.items():
        models[m]["proposals_range"] = [min(x["proposals"] for x in v), max(x["proposals"] for x in v)]
        models[m]["cost_per_finished_h"] = models[m]["cost"] / models[m]["finished_h"]
    dates = []
    for i in range(4):
        ms = [models[m] for m in models if rank[m] == i]
        mean = lambda k: float(np.mean([x[k] for x in ms]))  # noqa: E731
        dates.append({"models": sorted(m for m in models if rank[m] == i),
                      **{k: mean(k) for k in ("press_enter", "press_enter_equal", "usable", "attempted", "value",
                                              "finished_h", "cost", "read_h", "fired", "trap_share")},
                      "quality": mean("press_enter") / mean("attempted"),
                      "cost_per_finished_h": sum(x["cost"] for x in ms) / sum(x["finished_h"] for x in ms)})

    # within-lab pace: each week's press-enter rate on release date, a level for each lab and each job; then each lab
    # left out. The halving time: each model's log inference cost per finished hour on release date, a level per lab.
    labs, profs = sorted({w["lab"] for w in weeks}), sorted({w["profession"] for w in weeks})
    years = lambda w: (w["released"] - JAN1).days / 365.25  # noqa: E731

    def pace(ws):
        ls = sorted({w["lab"] for w in ws})
        X = np.array([[years(w)] + [w["lab"] == lab for lab in ls] + [w["profession"] == q for q in profs[1:]]
                      for w in ws], float)
        return float(np.linalg.lstsq(X, np.array([100 * measure(w)["press_enter"] for w in ws]), rcond=None)[0][0])
    first = {m: next(w for w in weeks if w["model"] == m) for m in models}
    X = np.array([[years(first[m])] + [first[m]["lab"] == lab for lab in labs] for m in models], float)
    slope = np.linalg.lstsq(X, np.log([models[m]["cost_per_finished_h"] for m in models]), rcond=None)[0][0]

    # how the panel ranks the hand-graded proposals against the person: Spearman's rho of the panel score and the
    # verdict (do not use < rewrite < small edit < send as is), each distinct proposal once, ties at their mean rank
    order = {"Don't send": 0, "Rewrite": 1, "Small edit": 2, "Send as is": 3}
    hg = [h for h in csv.DictReader(open(ROOT / cal["hand_grades"])) if not h["repeat_of"]]

    def ranks(a):
        a = np.asarray(a, float)
        r = np.empty(len(a))
        r[a.argsort(kind="stable")] = np.arange(len(a))
        for v in np.unique(a):
            r[a == v] = r[a == v].mean()
        return r
    rho = float(np.corrcoef(ranks([float(h["panel_score"]) for h in hg]),
                            ranks([order[h["verdict"]] for h in hg]))[0, 1])

    # Claude Opus 5.5 in the claims adjuster's week, piece by piece
    w = next(w for w in weeks if w["model"] == "Claude Opus 5.5" and w["profession"] == "claims-adjusters")
    chance = dict(zip(w["caught_ids"], sig(b_as, w["caught_s"])))
    needs = eps[w["profession"]]["needs"]
    example = [{"need": i, "title": needs[i].title, "minutes": needs[i].minutes.do,
                "chance_unchanged": float(chance[i]) if i in chance else None,
                "finished_minutes": needs[i].minutes.do * float(chance.get(i, 0.0))} for i in w["need_ids"]]

    # call lines that reach the worker in time, the latest models in the customer service week
    calls = {m: [x for w in weeks if w["model"] == m and w["profession"] == "customer-service-representatives"
                 for x in w["on_time"]] for m in models if rank[m] == 3}

    # Acemoglu's own rule on the run's jobs: Eloundou et al.'s exposed share of each job's tasks, weighted as the
    # measured shares are, times Svanberg et al.'s 23% and his 27% saving
    exposed, all_occupations = eloundou_exposed({p: eps[p]["soc"] for p in profs})
    tot = sum(bill.values())
    exp_w = sum(bill[p] * exposed[p] for p in profs) / tot
    a, n = econ["acemoglu"], econ["newest"]
    his_share = exp_w * PROFITABLE
    his_saving = his_share * a["labor_cost_saving_on_them"]
    acem = {"exposed_by_job": exposed, "exposed_weighted": exp_w, "exposed_all_occupations_unweighted": all_occupations,
            "his_method_share": his_share, "his_method_saving": his_saving,
            "multiple_economy": n["weighted"]["saving"] / (a["share_of_tasks"] * a["labor_cost_saving_on_them"]),
            "multiple_same_jobs": n["weighted"]["saving"] / his_saving,
            "multiple_same_jobs_90": [x / his_saving for x in n["weighted_90"]["saving"]],
            "factors": {"job_selection": exp_w / EXPOSED_US, "share": n["weighted"]["affected"] / his_share,
                        "saving_per_hour": n["per_affected"] / a["labor_cost_saving_on_them"]}}

    summary = {"dates": dates, "models": models,
               "pace_points_a_year": pace(weeks), "pace_without_lab": {lab: pace([w for w in weeks if w["lab"] != lab])
                                                                       for lab in labs},
               "cost_per_finished_h_halving_months": float(12 * np.log(2) / -slope),
               "example": {"model": w["model"], "profession": w["profession"], "pieces": example,
                           "week_minutes": float(w["planned"]),
                           "finished_minutes": float(sum(x["finished_minutes"] for x in example))},
               "late_call_lines": {**{m: 1 - float(np.mean(v)) for m, v in calls.items()},
                                   "pooled": 1 - float(np.mean([x for v in calls.values() for x in v]))},
               "acemoglu_same_jobs": acem,
               "hand_grades": {"n": len(hg), "spearman_panel_vs_verdict": rho}}
    (out / "post.json").write_text(json.dumps(summary, indent=1, default=float) + "\n")

    with open(out / "workweek-tasks.csv", "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["job", "onet_task_id", "task_statement", "planned_minutes",
                     "share_accepted_unchanged_latest_models", "ai_use_recorded", "economic_index_usage"])
        for t in econ["tasks"]["rows"]:
            wr.writerow([t["job"], t["task_id"], t["statement"], t["minutes"], round(t["press_enter"], 4),
                         "unknown" if t["usage"] is None else "yes" if t["usage"] else "no", t["usage"]])

    c, j = cal, econ["jan1"]
    pct = lambda v: f"{v * 100:.1f}%"  # noqa: E731
    span = lambda lo_hi, f=pct: f"[{f(lo_hi[0])}, {f(lo_hi[1])}]"  # noqa: E731
    pts = lambda v: f"{v:.1f}%"  # noqa: E731
    lines = ["# Headline estimates and 90% intervals", "",
             f"Intervals: {c['bootstrap']['draws']} bootstrap draws resampling the 20 models (with all their weeks) "
             "and the hand grades together.", "",
             "| Measure | Models of 1st January | Latest models |", "| --- | --- | --- |",
             f"| Press-enter rate (accepted unchanged, share of planned hours) | {pts(c['as_is']['jan1'])} "
             f"{span(c['as_is']['jan1_90'], pts)} | {pts(c['as_is']['newest'])} {span(c['as_is']['newest_90'], pts)} |",
             f"| Usable (unchanged or after a small edit), share of planned hours | {pts(c['use']['jan1'])} "
             f"{span(c['use']['jan1_90'], pts)} | {pts(c['use']['newest'])} {span(c['use']['newest_90'], pts)} |",
             f"| Latest over January press-enter rate | | {c['as_is']['ratio']:.2f}x [{c['as_is']['ratio_90'][0]:.2f}, "
             f"{c['as_is']['ratio_90'][1]:.2f}] |",
             f"| Pace within a lab, press-enter rate | | {c['as_is']['pace_points_a_year']:.1f} points a year "
             f"[{c['as_is']['pace_90'][0]:.1f}, {c['as_is']['pace_90'][1]:.1f}] |"]
    for k, name in (("affected", "Usable work, share of all labor hours"),
                    ("finished", "Finished hours, share of all labor hours"),
                    ("saving", "Net value, share of weekly labor cost")):
        lines.append(f"| {name} (labor-cost weighted) | {pct(j['weighted'][k])} {span(j['weighted_90'][k])} | "
                     f"{pct(n['weighted'][k])} {span(n['weighted_90'][k])} |")
    lines += [f"| Net saving per usable hour | | {pct(n['per_affected'])} {span(n['weighted_90']['per_affected'])} |",
              f"| Multiple of the 1.24% Acemoglu's economy-wide inputs imply | | {acem['multiple_economy']:.1f}x |",
              f"| Multiple of his inputs for the same 8 jobs ({pct(his_saving)}) | | {acem['multiple_same_jobs']:.1f}x "
              f"[{acem['multiple_same_jobs_90'][0]:.1f}, {acem['multiple_same_jobs_90'][1]:.1f}] |",
              f"| Hand-graded calibration | n = {c['n']} distinct proposals | release-date term "
              f"{c['release_date_term']['log_odds_per_year']} log-odds a year {c['release_date_term']['interval_90']} |"]
    (out / "intervals.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"dates": [{k: d[k] for k in d if k != "models"} for d in dates], "spearman": rho,
                      "pace_without_lab": summary["pace_without_lab"],
                      "halving_months": summary["cost_per_finished_h_halving_months"],
                      "late_call_lines": summary["late_call_lines"], "acemoglu_same_jobs": acem}, indent=1, default=float))


if __name__ == "__main__":
    main()
