"""Figures for a graded run, one finding each.

    uv run python scripts/figures.py results/final

Writes `<results>/figures/*.png` and `<results>/figures/table.csv` (one row per model and profession, the numbers
behind every figure). Each figure's title states its one finding; its subtitle says in a line what is plotted. Over
release date, each model is a dot in its lab's color, each lab's models are joined in order, and a black line is the
average trend within a lab (a regression with a level for each lab):
- pace.png: the press-enter rate, mean of the professions;
- cost.png: compute per hour of work sent as is (log scale), against the worker's hourly labor cost;
- value.png: net value per worker-week;
- noticing.png: the share of planned work attempted, and the share of that sendable as is, side by side;
- pace-<profession>.png (appendix): the press-enter rate in one profession.
By job: value-jobs.png (net value per worker-week, the models of 1 January against the newest), professions.png (the
best model on 1 January against the best today). Across: usage.png (each job's press-enter rate against its observed
AI use) and harm.png (harmful proposals against the press-enter rate). With <results>/economics.json
(scripts/economics.py): acemoglu.png (Acemoglu's two assumed inputs against the two measured) and tasks.png (each
O*NET task's press-enter rate, by whether the Economic Index observes AI use on it).

Press-enter rate: the share of the week's planned work, weighted by the minutes each need takes the worker, that the
model did well enough to send unchanged: for each need earned by a proposal, its minutes times the panel's
probability that the worker sends it unchanged; the sum over the week's planned minutes.
"""
import csv
import math
import datetime as dt
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from workweek import config  # noqa: E402
from workweek.engine import load_episode  # noqa: E402

# the categorical palette, in its validated order (light surface); a lab keeps its color in every figure
SURFACE, INK, INK_2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8b8a85", "#e4e3df"
LABS = {"openai": ("OpenAI", "#2a78d6"), "anthropic": ("Anthropic", "#eb6834"), "deepseek": ("DeepSeek", "#1baf7a"),
        "moonshot": ("Moonshot", "#eda100"), "zai": ("Z.ai", "#e87ba4")}
OPEN_WEIGHT = {"deepseek", "moonshot", "zai"}
GROUPS = {"closed": ("Closed models (OpenAI, Anthropic)", "#6250d6"),
          "open": ("Open-weight models (DeepSeek, Moonshot, Z.ai)", "#1baf7a")}
TITLES = {"claims-adjusters": "Claims adjusters", "accountants": "Accountants",
          "customer-service-representatives": "Customer service reps", "operations-managers": "Operations managers",
          "paralegals": "Paralegals", "market-research-analysts": "Market research analysts",
          "software-developers": "Software developers", "administrative-assistants": "Administrative assistants"}
CALLOUTS = {"DeepSeek V4.1 Flash 1017", "GPT-6.1 Sol", "Claude Opus 5.5", "GPT-5.5"}   # named in the cost figure
JAN1 = dt.date(2026, 1, 1)

plt.rcParams.update({"font.family": ["Liberation Sans", "DejaVu Sans"], "font.size": 10,
                     "axes.edgecolor": GRID, "axes.labelcolor": INK_2, "xtick.color": INK_2, "ytick.color": INK_2,
                     "axes.facecolor": SURFACE, "figure.facecolor": SURFACE, "savefig.facecolor": SURFACE,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID,
                     "grid.linewidth": 0.8, "axes.axisbelow": True, "xtick.major.size": 0, "ytick.major.size": 0,
                     "text.parse_math": False})


def calibrated(cal: dict | None, which: str, s: float) -> float:
    """The panel's score as a person's decision (scripts/calibrate.py: "as_is" or "use"); the raw score without it."""
    if not cal:
        return s
    a, b = cal["curves"][which]
    return 1 / (1 + math.exp(-(a + b * s)))


def measures(row: dict, minutes: dict[str, float], cal: dict | None = None, wage: float = 0.0) -> dict:
    raw = {i: (g["panel"].get("score") or 0) / 100 for i, g in enumerate(row["graded"])}   # needs name proposals by position
    score = {i: calibrated(cal, "as_is", s) for i, s in raw.items()}
    planned = sum(minutes.get(n["need"], 0) for n in row["needs"]) or 1
    caught = [n for n in row["needs"] if n["caught"]]
    done = sum(minutes.get(n["need"], 0) * score.get(n["proposal"], 0) for n in caught)
    attempted = sum(minutes.get(n["need"], 0) for n in caught)
    if cal:     # value as the hand grades decide: sent as is, used after a small edit (its fix time), or not used
        value = 0.0
        for i, g in enumerate(row["graded"]):
            v = g["value"]
            if v.get("suppressed"):
                value += v["value_usd"]
                continue
            p_as, p_use = score[i], calibrated(cal, "use", raw[i])
            saved = v["do_min"] * p_use - v["read_min"] - (p_use - p_as) * v["fix_min"] if v["do_min"] else -v["read_min"]
            value += saved * wage / 60 - v["token_cost_usd_share"]
    else:
        value = sum(g["value"]["value_usd"] for g in row["graded"])
    return {"press_enter": done / planned, "attempted": attempted / planned,
            "done_right": done / attempted if attempted else 0.0,
            "value": value - row.get("questions_cost_usd", 0),
            "cost": row.get("token_cost_usd") or 0, "traps": sum(t["fired"] for t in row["traps"]),
            "needs_caught": len(caught), "needs": len(row["needs"])}


def figure(title: str, subtitle: str, size=(7.2, 4.4), ncols=1, source: str | None = None):
    """A figure whose title states the finding and whose subtitle says exactly what is plotted (wrapped to the
    width); a source line at the foot when the data is someone else's."""
    import textwrap
    fig, axes = plt.subplots(1, ncols, figsize=size, sharey=ncols > 1)
    fig.text(0.02, 0.97, title, fontsize=13, fontweight="bold", color=INK, va="top")
    lines = textwrap.wrap(subtitle, int(size[0] * 14.2))
    fig.text(0.02, 0.97 - 0.30 / size[1], "\n".join(lines), fontsize=9.5, color=INK_2, va="top", linespacing=1.35)
    fig._top = 0.97 - (0.42 + 0.19 * len(lines)) / size[1]
    fig._bottom = 0.0
    if source:
        fig.text(0.02, 0.02, source, fontsize=7.5, color=MUTED, va="bottom")
        fig._bottom = 0.22 / size[1]
    return fig, axes


def save(fig, path: Path, legend=None, labels=None, lines=None):
    top = fig._top
    if legend:      # rows above the plot: the dots' key, then any line's; identity never rests on color alone
        dots = [h for h in legend if h.get_marker() not in (None, "None", "")]
        rows = [r for r in (dots, [h for h in legend if h not in dots]) if r]
        for r in rows:
            fig.legend(handles=r, loc="upper left", bbox_to_anchor=(0.02, top + 0.005), ncol=len(r), frameon=False,
                       fontsize=8.5, labelcolor=INK_2, handlelength=1.4, columnspacing=1.4)
            top -= 0.25 / fig.get_size_inches()[1]
        top -= 0.06 / fig.get_size_inches()[1]
    fig.tight_layout(rect=(0, fig._bottom, 1, top))
    if labels:      # after the layout is final, so the free spots are measured where they will be
        place(fig, *labels)
    for ax, ls in lines or []:
        below_lines(fig, ax, ls)
    fig.savefig(path, dpi=220)
    plt.close(fig)


def dot(ax, x, y, color, size=46, **kw):
    ax.scatter(x, y, s=size, color=color, edgecolors=SURFACE, linewidths=2, zorder=3, **kw)


# where a label may sit around its point, in order of preference: below first, then the nearest free spot
SPOTS = [(0, -9, "center", "top"), (0, 9, "center", "bottom"), (8, 0, "left", "center"), (-8, 0, "right", "center"),
         (0, -22, "center", "top"), (0, 22, "center", "bottom"), (8, -10, "left", "top"), (-8, -10, "right", "top"),
         (8, 10, "left", "bottom"), (-8, 10, "right", "bottom"), (0, -34, "center", "top"), (0, 34, "center", "bottom")]


def place(fig, ax, items):
    """Direct labels that never overlap each other, a mark, or the plot's edge: each (x, y, text) takes the first free
    spot around its point, below it if that is free."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    taken = [c.get_window_extent(r) for c in ax.collections]          # the marks
    marks = [b for c in ax.collections for b in _dot_boxes(ax, c)]
    frame = ax.get_window_extent(r)
    for x, y, text in sorted(items, key=lambda i: -i[1]):
        for dx, dy, ha, va in SPOTS:
            a = ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, va=va, fontsize=8.5,
                            color=INK_2, zorder=4)
            b = a.get_window_extent(r)
            inside = frame.x0 <= b.x0 and b.x1 <= frame.x1 + 40 and frame.y0 <= b.y0 and b.y1 <= frame.y1
            if inside and not any(b.overlaps(o) for o in marks + taken[len(ax.collections):]):
                taken.append(b)
                break
            a.remove()
        else:
            taken.append(ax.annotate(text, (x, y), xytext=SPOTS[0][:2], textcoords="offset points", ha="center",
                                     va="top", fontsize=8.5, color=INK_2).get_window_extent(r))


def below_lines(fig, ax, lines):
    """Each line's name just below the line: under its last point if free, else under the nearest earlier point or
    segment midpoint going back along the line; never over a mark, another line or another label. A line is
    (xs, ys, name) or (xs, ys, name, text style)."""
    from matplotlib.transforms import Bbox
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    blocked = [b for c in ax.collections for b in _dot_boxes(ax, c)]
    for xs, ys, *_ in lines:                                  # every line, sampled along its length
        pts = ax.transData.transform(list(zip(xs, ys)))
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(2, int(max(abs(x1 - x0), abs(y1 - y0)) / 4))
            blocked += [Bbox([[x0 + (x1 - x0) * k / n - 2, y0 + (y1 - y0) * k / n - 2],
                              [x0 + (x1 - x0) * k / n + 2, y0 + (y1 - y0) * k / n + 2]]) for k in range(n + 1)]
    frame = ax.get_window_extent(r)
    for xs, ys, name, *style in sorted((l for l in lines if l[2]), key=lambda l: -l[1][-1]):
        kw = {"fontsize": 8.5, "color": INK_2, **(style[0] if style else {})}
        spots = [(xs[-1], ys[-1])]
        for i in range(len(xs) - 1, 0, -1):
            spots += [((xs[i] + xs[i - 1]) / 2, (ys[i] + ys[i - 1]) / 2), (xs[i - 1], ys[i - 1])]
            for f in (0.25, 0.75):
                spots.append((xs[i - 1] + f * (xs[i] - xs[i - 1]), ys[i - 1] + f * (ys[i] - ys[i - 1])))
        offsets = ((-7, "top"), (7, "bottom"), (-18, "top"), (18, "bottom"))     # below first, then above, then farther
        for (x, y), (dy, va) in [(xy, d) for d in offsets for xy in spots]:
            a = ax.annotate(name, (x, y), xytext=(0, dy), textcoords="offset points", ha="center", va=va,
                            zorder=4, **kw)
            b = a.get_window_extent(r)
            inside = frame.x0 <= b.x0 and b.x1 <= frame.x1 and frame.y0 <= b.y0 and b.y1 <= frame.y1
            if inside and not any(b.overlaps(o) for o in blocked):
                blocked.append(b)
                break
            a.remove()
        else:                                                 # nowhere free: under the last point regardless
            blocked.append(ax.annotate(name, (xs[-1], ys[-1]), xytext=(0, -7), textcoords="offset points",
                                       ha="center", va="top", **kw).get_window_extent(r))


def _dot_boxes(ax, coll, pad=7):
    from matplotlib.transforms import Bbox
    pts = ax.transData.transform(coll.get_offsets())
    return [Bbox([[px - pad, py - pad], [px + pad, py + pad]]) for px, py in pts]


def key(color, label, marker="o"):
    return plt.Line2D([], [], color=color, lw=0, marker=marker, markersize=7, markeredgecolor=color, label=label)


def pct(ax, axis="y"):
    fmt = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)


def months(ax):
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.grid(axis="x", visible=False)


def lab_trend(pts, log=False):
    """The average trend within a lab: y on release date with a level for each lab; (slope a year, the points' mean
    date as a number, their mean y), on the log of y when log. pts: (model, lab, released, y)."""
    import numpy as np
    labs = sorted({p[1] for p in pts})
    t = np.array([(p[2] - JAN1).days / 365.25 for p in pts])
    y = np.array([p[3] for p in pts], float)
    y = np.log(y) if log else y
    X = np.column_stack([t] + [[float(p[1] == lab) for p in pts] for lab in labs])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    return float(b[0]), float(np.mean([mdates.date2num(p[2]) for p in pts])), float(y.mean())


def draw_time(ax, pts, log=False, trend_text=None, lab_lines=True):
    """Dots by release date in their lab's color; each lab's own fitted trend in its color, named below it; the
    average trend within a lab in black, named below it. Returns the lines to name."""
    import numpy as np
    lines = []
    for lab, (name, color) in LABS.items():
        mine = sorted((p for p in pts if p[1] == lab), key=lambda p: p[2])
        if not mine:
            continue
        xs = [mdates.date2num(p[2]) for p in mine]
        ys = [p[3] for p in mine]
        dot(ax, xs, ys, color)
        if lab_lines and len(mine) >= 2:      # point to point, thin, so crossing labs stay readable
            ax.plot(xs, ys, color=color, lw=1.3, alpha=0.75, solid_joinstyle="round", zorder=2)
            lines.append((xs, ys, name))
    if trend_text:
        slope, cx, cy = lab_trend(pts, log)
        x0 = min(mdates.date2num(p[2]) for p in pts) - 8
        x1 = max(mdates.date2num(p[2]) for p in pts) + 8
        f = (lambda x: math.exp(cy + slope * (x - cx) / 365.25)) if log else (lambda x: cy + slope * (x - cx) / 365.25)
        ax.plot([x0, x1], [f(x0), f(x1)], color=INK, lw=2.4, solid_capstyle="round", zorder=2.5)
        ax._trend = plt.Line2D([], [], color=INK, lw=2.4, label=f"Average trend within a lab: {trend_text(slope)}")
        lines.append(([x0, x1], [f(x0), f(x1)], ""))           # its path keeps the labs' names off it
    months(ax)
    if log:
        ax.set_yscale("log")
    return lines


def over_time(out, fname, title, subtitle, pts, ylabel, yfmt, log=False, trend_text=None, ref=None, zero=False,
              size=(7.2, 4.8), source=None):
    fig, ax = figure(title, subtitle, size, source=source)
    lines = draw_time(ax, pts, log, trend_text)
    if ref:
        y, text = ref
        ax.axhline(y, color=MUTED, lw=1, ls=(0, (4, 3)), zorder=1)
        ax.annotate(text, (1, y), xycoords=("axes fraction", "data"), xytext=(-4, 4), textcoords="offset points",
                    fontsize=8.5, color=MUTED, va="bottom", ha="right")
    if zero:
        ax.axhline(0, color=INK_2, lw=0.8, zorder=1)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: yfmt(v)))
    if log:
        ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    else:
        lo, hi = min(p[3] for p in pts), max(p[3] for p in pts)
        ax.set_ylim(min(0, lo * 1.15), hi * 1.12 + (hi - min(0, lo)) * 0.04)
    ax.set_ylabel(ylabel)
    save(fig, out / fname, legend=[key(c, n) for n, c in LABS.values()] + [ax._trend], lines=[(ax, lines)])


def per_model(table: list[dict]) -> dict[str, dict]:
    """Each model's means over the professions, and its compute per hour of finished work (mean compute over mean
    hours sendable as is)."""
    out = {}
    for m in sorted({t["model"] for t in table}):
        ts = [t for t in table if t["model"] == m]
        row = {k: sum(t[k] for t in ts) / len(ts) for k in ("press_enter", "attempted", "done_right", "value", "cost",
                                                            "traps", "hours_done")}
        row.update(lab=ts[0]["lab"], released=ts[0]["released"])
        row["cost_per_hour"] = row["cost"] / row["hours_done"] if row["hours_done"] else float("nan")
        out[m] = row
    return out


def dumbbell(ax, rows, fmt, bold_first=True):
    """One row per (name, before, after): a grey dot before, a blue dot after, joined; both values labeled
    outside the pair, the after value in bold ink."""
    for i, (name, a, b) in enumerate(rows):
        ax.plot([a, b], [i, i], color=GRID, lw=2.2, zorder=1)
        dot(ax, a, i, MUTED)
        dot(ax, b, i, LABS["openai"][1])
        right = b >= a
        ax.annotate(fmt(b), (b, i), xytext=(8 if right else -8, 0), textcoords="offset points", va="center",
                    ha="left" if right else "right", fontsize=8.5, color=INK, fontweight="bold")
        ax.annotate(fmt(a), (a, i), xytext=(-8 if right else 8, 0), textcoords="offset points", va="center",
                    ha="right" if right else "left", fontsize=8, color=MUTED)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    if bold_first:
        ax.get_yticklabels()[-1].set_fontweight("bold")
    ax.grid(axis="y", visible=False)
    ax.margins(x=0.12)


def money(v: float) -> str:
    return f"{'-' if v < 0 else ''}${abs(v):,.0f}"


def main():
    res = Path(sys.argv[1])
    out = res / "figures"
    out.mkdir(parents=True, exist_ok=True)
    for old in ("savings.png",):                       # replaced: a figure no longer drawn is not left behind
        (out / old).unlink(missing_ok=True)
    cfg = config.load(ROOT / "config/run.yaml")
    spec = {m.name: m for m in cfg.models}
    rows = [json.loads(line) for line in (res / "graded.jsonl").read_text().splitlines()]
    minutes, wages = {}, {}
    for prof in {r["profession"] for r in rows}:
        ep = load_episode(ROOT / "professions" / prof / "episode")
        minutes[prof] = {n.id: n.minutes.do for n in ep.needs}
        wages[prof] = ep.economics.loaded_hourly
    cal = json.loads((res / "calibration.json").read_text()) if (res / "calibration.json").exists() else None
    table = []
    for r in rows:
        m = spec[r["model"]]
        x = measures(r, minutes[r["profession"]], cal, wages[r["profession"]])
        planned = sum(minutes[r["profession"]].get(n["need"], 0) for n in r["needs"])
        table.append({"model": m.name, "lab": m.family, "released": m.released, "profession": r["profession"], **x,
                      "hours_done": x["press_enter"] * planned / 60})
    with open(out / "table.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(table[0]))
        w.writeheader()
        w.writerows(table)
    profs = sorted({t["profession"] for t in table})
    exposure = {}
    for r in csv.DictReader(open(ROOT / "data/shortlist.csv")):
        exposure[r["code"]] = float(r["observed_exposure"])
    soc = {p: load_episode(ROOT / "professions" / p / "episode").meta.soc for p in profs}

    def mean(xs):
        xs = list(xs)
        return sum(xs) / len(xs) if xs else 0.0

    latest = {}                                       # each lab's newest model
    for t in table:
        latest[t["lab"]] = max(latest.get(t["lab"], t["released"]), t["released"])
    newest = [t for t in table if t["released"] == latest[t["lab"]]]
    on_jan1 = {}
    for t in table:                                   # each lab's model in force on 1 January
        if t["released"] <= JAN1:
            best = on_jan1.get(t["lab"])
            if best is None or t["released"] > best:
                on_jan1[t["lab"]] = t["released"]
    jan = [t for t in table if t["released"] == on_jan1.get(t["lab"])]
    models = per_model(table)
    pts = lambda k, f=lambda v: v: [(m, r["lab"], r["released"], f(r[k])) for m, r in models.items()]  # noqa: E731
    group_mean = lambda ts, k: mean(models[m][k] for m in {t["model"] for t in ts})  # noqa: E731
    pct0 = lambda v: f"{v:.0f}%"  # noqa: E731

    # 1. the level and the pace
    a, b = group_mean(jan, "press_enter") * 100, group_mean(newest, "press_enter") * 100
    over_time(out, "pace.png", f"AI now does {b:.0f}% of the week unasked, up from {a:.0f}% in January",
              "Share of the week's work done unasked and sent as is, mean of eight jobs",
              pts("press_enter", lambda v: v * 100), "share of the week done unasked", pct0,
              trend_text=lambda s: f"+{s:.0f} points a year")

    # 2. more work for less
    def per_hour(ts):
        ms = {t["model"] for t in ts}
        return sum(models[m]["cost"] for m in ms) / sum(models[m]["hours_done"] for m in ms)
    wage = mean(wages.values())
    over_time(out, "cost.png",
              f"An hour of finished work now takes ${per_hour(newest):.0f} of compute, down from "
              f"${per_hour(jan):.0f}",
              "Compute per hour of work sent as is, log scale",
              pts("cost_per_hour"), "compute per finished hour (log scale)",
              lambda v: f"${v:,.0f}" if v >= 1 else f"${v:.2f}", log=True,
              trend_text=lambda s: f"halves every {12 * math.log(2) / -s:.0f} months",
              ref=(wage, f"worker's labor cost, ${wage:.0f} an hour"))

    # 3. what it is worth: over time, then by job
    a, b = group_mean(jan, "value"), group_mean(newest, "value")
    over_time(out, "value.png",
              f"The help is now worth {money(round(b, -1))} a worker-week, up from "
              f"{'nothing' if abs(a) < 50 else money(a)}",
              "Net value per worker-week, after checking time and compute", pts("value"), "net value per worker-week",
              money, zero=True,
              trend_text=lambda s: f"+{money(s)} a year")
    fig, ax = figure("The newest models pay most where tasks are large",
                     "Net value per worker-week, mean of five labs", (7.2, 4.9))
    vals = {p: (mean(t["value"] for t in jan if t["profession"] == p), mean(t["value"] for t in newest
                                                                             if t["profession"] == p)) for p in profs}
    order = sorted(profs, key=lambda p: vals[p][1])
    rows_ = [(TITLES.get(p, p), *vals[p]) for p in order] + [("All eight jobs", a, b)]
    dumbbell(ax, rows_, money)
    ax.axvline(0, color=INK_2, lw=0.8, zorder=0)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: money(v)))
    save(fig, out / "value-jobs.png",
         legend=[key(MUTED, "Models of 1 January"), key(LABS["openai"][1], "Newest models")])

    # 4. noticing against quality
    fig, (ax1, ax2) = figure("Newer models notice far more of the work, and do it a little better",
                             "Each dot is a model, mean of eight jobs", (7.2, 4.6), ncols=2)
    panels = []
    for ax, k, t in ((ax1, "attempted", "Attempted"), (ax2, "done_right", "Of that, sendable as is")):
        ps = pts(k, lambda v: v * 100)
        panels.append((ax, draw_time(ax, ps, trend_text=lambda s: "", lab_lines=False)))
        ax.set_title(f"{t}: {lab_trend(ps)[0]:+.0f} points a year", fontsize=10, color=INK, loc="left",
                     fontweight="bold")
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
        pct(ax)
    ax1.set_ylim(0, 85)
    save(fig, out / "noticing.png", legend=[key(c, n) for n, c in LABS.values()]
         + [plt.Line2D([], [], color=INK, lw=2.4, label="Average trend within a lab")])

    # 5. every occupation
    fig, ax = figure("In every job, the best model today does more than January's best",
                     "Share of the week's work sent as is, best model then and now", (7.2, 4.9))
    best = lambda ts, p: max((t for t in ts if t["profession"] == p), key=lambda t: t["press_enter"])  # noqa: E731
    order = sorted(profs, key=lambda p: best(table, p)["press_enter"])
    dumbbell(ax, [(TITLES.get(p, p), best(jan, p)["press_enter"] * 100, best(table, p)["press_enter"] * 100)
                  for p in order], pct0, bold_first=False)
    for i, p in enumerate(order):
        t = best(table, p)
        ax.annotate(t["model"], (t["press_enter"] * 100, i), xytext=(34, 0), textcoords="offset points",
                    va="center", fontsize=8, color=INK_2)
    pct(ax, "x")
    ax.set_xlim(0, max(best(table, p)["press_enter"] for p in profs) * 100 + 18)
    save(fig, out / "professions.png", legend=[key(MUTED, "Best on 1 January"), key(LABS["openai"][1], "Best today")])

    # 6. capability against use, by job
    fig, ax = figure("Jobs where people use AI least are not where it can do least",
                     "Each dot is a job; newest models, mean of five labs",
                     source="Observed AI use: observed exposure, Massenkoff and McCrory, Anthropic, 2026.")
    items = []
    for p in profs:
        x, y = exposure.get(soc[p], 0) * 100, mean(t["press_enter"] * 100 for t in newest if t["profession"] == p)
        dot(ax, x, y, LABS["openai"][1])
        items.append((x, y, f"{TITLES.get(p, p)} {y:.0f}%"))
    pct(ax, "x")
    pct(ax)
    ax.set_xlabel("observed AI use in the job")
    ax.set_ylabel("share of the week done unasked")
    ax.set_ylim(0, max(y for _, y, _ in items) * 1.3)
    ax.set_xlim(0, max(x for x, _, _ in items) * 1.2)
    save(fig, out / "usage.png", labels=(ax, items))

    # 7. harm
    fig, ax = figure("Models that do more of the week set off fewer traps, not more",
                     "Each dot is a model, mean of eight jobs")
    items = []
    for m, r in models.items():
        dot(ax, r["press_enter"] * 100, r["traps"], LABS[r["lab"]][1])
        if r["traps"] >= 1.8 or r["press_enter"] >= 0.26:
            items.append((r["press_enter"] * 100, r["traps"], m))
    pct(ax, "x")
    ax.set_xlabel("share of the week done unasked")
    ax.set_ylabel("harmful proposals per week")
    ax.set_ylim(0, None)
    save(fig, out / "harm.png", legend=[key(c, n) for n, c in LABS.values()], labels=(ax, items))

    # appendix: the pace in each profession
    for p in profs:
        ps = [(t["model"], t["lab"], t["released"], t["press_enter"] * 100) for t in table if t["profession"] == p]
        over_time(out, f"pace-{p}.png", TITLES.get(p, p),
                  "Share of the week's work done unasked and sent as is",
                  ps, "share of the week done unasked", pct0, trend_text=lambda s: f"+{s:.0f} points a year")
    if (res / "economics.json").exists():          # scripts/economics.py
        econ = json.loads((res / "economics.json").read_text())
        acemoglu(out, econ)
        tasks_use(out, econ)
    print("wrote", sorted(x.name for x in out.iterdir()))


def acemoglu(out: Path, econ: dict):
    """Acemoglu's two assumed inputs against the same two measured here, the newest models, with 90% intervals."""
    a = econ["acemoglu"]
    n = econ["newest"]
    fig, ax = figure("Measured, both of Acemoglu's inputs are larger in these eight jobs",
                     "Assumed for the US economy against measured in eight jobs, with 90% intervals", (7.2, 4.4),
                     source="Assumed: Acemoglu, \"The Simple Macroeconomics of AI\", NBER working paper 32487 (2024), "
                            "pages 6 and 30.")
    groups = [("Share of work AI takes on", a["share_of_tasks"], n["weighted"]["affected"],
               n["weighted_90"]["affected"]),
              ("Cost saving on that work", a["labor_cost_saving_on_them"], n["per_affected"],
               n["weighted_90"]["per_affected"])]
    w = 0.34
    for i, (name, assumed, measured, (lo, hi)) in enumerate(groups):
        ax.bar(i - w / 2 - 0.02, assumed * 100, w, color=MUTED, zorder=2)
        ax.bar(i + w / 2 + 0.02, measured * 100, w, color=LABS["openai"][1], zorder=2)
        ax.errorbar(i + w / 2 + 0.02, measured * 100, yerr=[[(measured - lo) * 100], [(hi - measured) * 100]],
                    color=INK, lw=1.2, capsize=4, zorder=3)
        ax.annotate(f"{assumed * 100:.1f}%" if assumed < 0.1 else f"{assumed * 100:.0f}%", (i - w / 2 - 0.02,
                    assumed * 100), xytext=(0, 4), textcoords="offset points", ha="center", fontsize=9, color=INK_2)
        ax.annotate(f"{measured * 100:.0f}%", (i + w / 2 + 0.02, hi * 100), xytext=(0, 4), textcoords="offset points",
                    ha="center", fontsize=9.5, color=INK, fontweight="bold")
    ax.set_xticks([0, 1], [g[0] for g in groups], fontsize=10)
    ax.grid(axis="x", visible=False)
    pct(ax)
    ax.set_ylim(0, 80)
    save(fig, out / "acemoglu.png", legend=[key(MUTED, "Assumed by Acemoglu", "s"),
                                            key(LABS["openai"][1], "Measured here", "s")])


def tasks_use(out: Path, econ: dict):
    """Each O*NET task in the weeks: the newest models' press-enter rate on it, by whether the Economic Index sees AI
    used on it; dot size is the task's planned minutes, the bar each group's minute-weighted mean."""
    import random
    rows = [t for t in econ["tasks"]["rows"] if t["usage"] is not None]
    groups = [("Nobody uses AI for it", [t for t in rows if t["usage"] == 0]),
              ("People use AI for it", [t for t in rows if t["usage"] > 0])]
    fig, ax = figure("AI does as much on tasks nobody brings to it as on tasks people do",
                     "Each dot is an O*NET task, sized by its minutes; newest models",
                     (7.2, 4.8), source="Task use: Anthropic Economic Index, task penetration.")
    rng = random.Random(7)
    top = max(t["press_enter"] for t in rows) * 100
    for gi, (name, ts) in enumerate(groups):
        xs = [gi + rng.uniform(-0.28, 0.28) for _ in ts]
        sizes = [12 + 260 * (t["minutes"] / max(r["minutes"] for r in rows)) ** 0.5 for t in ts]
        ax.scatter(xs, [t["press_enter"] * 100 for t in ts], s=sizes, color=LABS["openai"][1], alpha=0.35,
                   edgecolors=SURFACE, linewidths=1, zorder=2)
        m = sum(t["press_enter"] * t["minutes"] for t in ts) / sum(t["minutes"] for t in ts) * 100
        ax.plot([gi - 0.36, gi + 0.36], [m, m], color=INK, lw=2.4, zorder=3)
        ax.annotate(f"{m:.0f}%", (gi + 0.36, m), xytext=(6, 0), textcoords="offset points", va="center",
                    fontsize=9.5, color=INK, fontweight="bold")
        mins = sum(t["minutes"] for t in ts)
        groups[gi] = (f"{name}\n{len(ts)} tasks, {100 * mins / sum(r['minutes'] for r in rows):.0f}% of the minutes", ts)
    ax.set_xticks([0, 1], [g[0] for g in groups])
    ax.set_xlim(-0.6, 1.75)
    ax.set_ylim(0, top * 1.08 + 2)
    ax.grid(axis="x", visible=False)
    pct(ax)
    ax.set_ylabel("share sent as is")
    save(fig, out / "tasks.png")


if __name__ == "__main__":
    main()
