"""Calibrate the judge panel to the hand grades, and the headline numbers with it.

    uv run python scripts/calibrate.py results/final data/handgrades-2026-10-29.csv

The panel scores each proposal as the chance the worker sends it unchanged. A hand-graded sample (proposals that do
planned work, drawn by profession x panel-score band x lab) says what a person would actually do. This fits, with
the sample's design weights, two logistic curves from the panel score to the person's decision: "send as is", and
"use it" (send as is or after a small edit). It then reports:
- the curves, and a test that the panel is not more generous to newer models than the person (release date added
  to the curve: its coefficient should be about zero);
- the headline numbers on the calibrated scale (the press-enter rate of the newest models and of those in force on
  1 January, and the within-lab pace), with intervals from resampling the models and the hand grades together;
- a prediction-powered estimate of the same levels (Angelopoulos et al. 2023), which corrects the raw panel score
  by the design-weighted mean gap on the hand-graded sample and so does not rely on the curve's shape.
Writes <results>/calibration.json, which scripts/figures.py uses when it is present.
"""
import csv
import datetime as dt
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from workweek import config  # noqa: E402
from workweek.engine import load_episode  # noqa: E402

JAN1 = dt.date(2026, 1, 1)
BOOT = 1000


def band(score: float) -> int:
    return 0 if score < 35 else 1 if score < 70 else 2


def fit(X, y, w):
    """Weighted logistic regression by Newton's method."""
    b = np.zeros(X.shape[1])
    for _ in range(100):
        p = 1 / (1 + np.exp(-X @ b))
        step = np.linalg.solve(X.T @ (X * (w * p * (1 - p))[:, None]) + 1e-6 * np.eye(X.shape[1]), X.T @ (w * (y - p)))
        b += step
        if np.abs(step).max() < 1e-9:
            break
    return b


def curve(b, s):
    return 1 / (1 + np.exp(-(b[0] + b[1] * s)))


def main():
    res, grades_csv = Path(sys.argv[1]), Path(sys.argv[2])
    cfg = config.load(ROOT / "config/run.yaml")
    spec = {m.name: m for m in cfg.models}
    rows = [json.loads(line) for line in (res / "graded.jsonl").read_text().splitlines()]
    latest, on_jan1 = {}, {}
    for m in spec.values():
        if any(r["model"] == m.name for r in rows):
            latest[m.family] = max(latest.get(m.family, m.released), m.released)
            if m.released <= JAN1:
                on_jan1[m.family] = max(on_jan1.get(m.family, m.released), m.released)
    group = {m.name: ("newest" if m.released == latest.get(m.family) else "jan1" if m.released == on_jan1.get(m.family)
                      else "") for m in spec.values()}

    # the weeks, as the press-enter rate needs them: each caught need's minutes and its proposal's panel score
    minutes, weeks, cand, by_prop = {}, [], Counter(), {}
    for r in rows:
        p = r["profession"]
        if p not in minutes:
            minutes[p] = {n.id: n.minutes.do for n in load_episode(ROOT / "professions" / p / "episode").needs}
        sc = [(g["panel"].get("score") or 0) / 100 for g in r["graded"]]
        caught = [(minutes[p].get(n["need"], 0), n["proposal"]) for n in r["needs"] if n["caught"]]
        weeks.append({"model": r["model"], "profession": p, "planned": sum(minutes[p].get(n["need"], 0) for n in r["needs"]) or 1,
                      "w": np.array([w for w, _ in caught]), "s": np.array([sc[i] for _, i in caught])})
        for i, g in enumerate(r["graded"]):
            s = g["panel"].get("score")
            if s is None or not g["matches"] or (g.get("value") or {}).get("suppressed"):
                continue
            cand[(p, band(s), spec[r["model"]].family)] += 1
            by_prop[(r["model"], p, r["epoch"], g["proposal"]["id"])] = sum(w for w, j in caught if j == i)

    # the hand grades (first sight of each proposal only) and their design weights
    hg = [h for h in csv.DictReader(open(grades_csv)) if not h["repeat_of"]]
    for h in hg:
        h["s"] = float(h["panel_score"]) / 100
        h["cell"] = (h["profession"], band(float(h["panel_score"])), h["lab"])
    taken = Counter(h["cell"] for h in hg)
    x = np.array([h["s"] for h in hg])
    asis = np.array([h["verdict"] == "Send as is" for h in hg], float)
    use = np.array([h["verdict"] in ("Send as is", "Small edit") for h in hg], float)
    wt = np.array([cand[h["cell"]] / taken[h["cell"]] for h in hg])
    years = np.array([(spec[h["model"]].released - JAN1).days / 365.25 for h in hg])
    X = np.column_stack([np.ones_like(x), x])
    b_asis, b_use = fit(X, asis, wt), fit(X, use, wt)

    rng = np.random.default_rng(20261029)
    Xr = np.column_stack([X, years])
    b_rel = fit(Xr, asis, wt)
    rel_boot = sorted(fit(Xr[i], asis[i], wt[i])[2] for i in (rng.integers(0, len(hg), len(hg)) for _ in range(BOOT)))

    labs = sorted({spec[w["model"]].family for w in weeks})
    profs = sorted({w["profession"] for w in weeks})
    models = sorted({w["model"] for w in weeks})

    def design(ws):
        return np.array([[(spec[w["model"]].released - JAN1).days / 365.25] + [spec[w["model"]].family == lab for lab in labs]
                         + [w["profession"] == q for q in profs[1:]] for w in ws], float)

    def headline(b, ws):
        pe = np.array([100 * (w["w"] * curve(b, w["s"])).sum() / w["planned"] for w in ws])
        g = np.array([group[w["model"]] for w in ws])
        return pe[g == "newest"].mean(), pe[g == "jan1"].mean(), np.linalg.lstsq(design(ws), pe, rcond=None)[0][0]

    point = headline(b_asis, weeks)
    point_use = headline(b_use, weeks)
    boot, boot_use = [], []
    for _ in range(BOOT):         # the models (each with all its weeks) and the hand grades, resampled together
        ms = rng.choice(models, len(models))
        ws = [w for m in ms for w in weeks if w["model"] == m]
        if not any(group[w["model"]] == "newest" for w in ws) or not any(group[w["model"]] == "jan1" for w in ws):
            continue
        i = rng.integers(0, len(hg), len(hg))
        boot.append(headline(fit(X[i], asis[i], wt[i]), ws))
        boot_use.append(headline(fit(X[i], use[i], wt[i]), ws))
    boot, boot_use = np.array(boot), np.array(boot_use)

    # prediction-powered levels: the panel's minute-weighted mean, plus the design-weighted mean gap between the
    # person and the panel on the hand-graded proposals that earn needs, weighted by the minutes they earn (one gap
    # for all models: the release-date test above finds no difference between older and newer models)
    def ppi(grp):
        allw = [(w["w"], w["s"], w["planned"]) for w in weeks if group[w["model"]] == grp]
        planned = sum(p for _, _, p in allw)
        panel = sum((ww * s).sum() for ww, s, _ in allw) / planned
        lab = [(by_prop.get((h["model"], h["profession"], int(h["epoch"]), h["proposal"]), 0), wt[k], asis[k] - h["s"])
               for k, h in enumerate(hg)]
        lab = [(m, w_, d) for m, w_, d in lab if m > 0]
        gap = sum(m * w_ * d for m, w_, d in lab) / sum(m * w_ for m, w_, _ in lab)
        share = sum((ww).sum() for ww, _, _ in allw) / planned          # caught minutes over planned minutes
        return 100 * panel, 100 * (panel + share * gap)
    ppi_new, ppi_jan = ppi("newest"), ppi("jan1")

    def interval(a, j):
        return [round(float(np.percentile(a[:, j], 5)), 2), round(float(np.percentile(a[:, j], 95)), 2)]
    out = {
        "hand_grades": str(grades_csv.relative_to(ROOT) if grades_csv.is_absolute() else grades_csv), "n": len(hg),
        "curves": {"as_is": [round(float(v), 4) for v in b_asis], "use": [round(float(v), 4) for v in b_use]},
        "curve_form": "P(decision) = 1 / (1 + exp(-(a + b * panel_score / 100))), design-weighted logistic fit",
        "release_date_term": {"log_odds_per_year": round(float(b_rel[2]), 3),
                              "interval_90": [round(rel_boot[int(.05 * BOOT)], 3), round(rel_boot[int(.95 * BOOT)], 3)]},
        "as_is": {"newest": round(point[0], 2), "newest_90": interval(boot, 0), "jan1": round(point[1], 2),
                  "jan1_90": interval(boot, 1), "pace_points_a_year": round(point[2], 2), "pace_90": interval(boot, 2),
                  "ratio": round(point[0] / point[1], 2),
                  "ratio_90": [round(float(np.percentile(boot[:, 0] / boot[:, 1], q)), 2) for q in (5, 95)]},
        "use": {"newest": round(point_use[0], 2), "newest_90": interval(boot_use, 0), "jan1": round(point_use[1], 2),
                "jan1_90": interval(boot_use, 1), "pace_points_a_year": round(point_use[2], 2),
                "pace_90": interval(boot_use, 2)},
        "prediction_powered": {"newest": {"panel": round(ppi_new[0], 2), "corrected": round(ppi_new[1], 2)},
                               "jan1": {"panel": round(ppi_jan[0], 2), "corrected": round(ppi_jan[1], 2)}},
        "bootstrap": {"draws": len(boot), "resampled": "models (with all their weeks) and hand grades, together"},
    }
    (res / "calibration.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
