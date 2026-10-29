"""Figures for a graded run, one finding each.

    uv run python scripts/figures.py results/final

Writes `<results>/figures/*.png` and `<results>/figures/table.csv` (one row per model and profession, the numbers
behind every figure). Main figures:
- pace.png: the press-enter rate of each model, averaged over the professions, against its release date, a line
  per lab;
- professions.png: in each profession, the best model on 1 January against the best model now;
- usage.png: the frontier's press-enter rate in each profession against how much people already use AI there;
- value.png: net value per worker-week of the newest models, by profession;
- cost.png: compute per worker-week against the press-enter rate, closed and open-weight models;
- harm.png: harmful proposals per week against the press-enter rate.
Appendix: noticing.png (share of planned work attempted against the share of it done well) and one pace chart per
profession (pace-<profession>.png).

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
                     "grid.linewidth": 0.8, "axes.axisbelow": True, "xtick.major.size": 0, "ytick.major.size": 0})


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


def figure(title: str, subtitle: str, size=(7.2, 4.4)):
    fig, ax = plt.subplots(figsize=size)
    fig.text(0.02, 0.965, title, fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.02, 0.905, subtitle, fontsize=9.5, color=INK_2, va="top")
    return fig, ax


def save(fig, path: Path, top=0.80, legend=None, labels=None, lines=None, trend=None):
    if legend:      # one row above the plot; identity never rests on color alone (direct labels ride the marks)
        fig.legend(handles=legend, loc="upper left", bbox_to_anchor=(0.02, 0.86), ncol=len(legend), frameon=False,
                   fontsize=8.5, labelcolor=INK_2, handlelength=1.2, columnspacing=1.4)
        top -= 0.04
    fig.tight_layout(rect=(0, 0, 1, top))
    if labels:      # after the layout is final, so the free spots are measured where they will be
        place(fig, *labels)
    if lines:
        below_lines(fig, *lines)
    if trend:
        name_trend(fig, *trend)
    fig.savefig(path, dpi=200)
    plt.close(fig)


def dot(ax, x, y, color, size=46, **kw):
    ax.scatter(x, y, s=size, color=color, edgecolors=SURFACE, linewidths=2, zorder=3, **kw)


# where a label may sit around its point, in order of preference: below first, then the nearest free spot
SPOTS = [(0, -9, "center", "top"), (0, 9, "center", "bottom"), (8, 0, "left", "center"), (-8, 0, "right", "center"),
         (0, -22, "center", "top"), (0, 22, "center", "bottom"), (8, -10, "left", "top"), (-8, -10, "right", "top")]


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
    segment midpoint going back along the line; never over a mark, another line or another label."""
    from matplotlib.transforms import Bbox
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    blocked = [b for c in ax.collections for b in _dot_boxes(ax, c)]
    for xs, ys, _ in lines:                                   # every line, sampled along its length
        pts = ax.transData.transform(list(zip(xs, ys)))
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(2, int(max(abs(x1 - x0), abs(y1 - y0)) / 4))
            blocked += [Bbox([[x0 + (x1 - x0) * k / n - 2, y0 + (y1 - y0) * k / n - 2],
                              [x0 + (x1 - x0) * k / n + 2, y0 + (y1 - y0) * k / n + 2]]) for k in range(n + 1)]
    frame = ax.get_window_extent(r)
    for xs, ys, name in sorted(lines, key=lambda l: -l[1][-1]):
        spots = [(xs[-1], ys[-1])]
        for i in range(len(xs) - 1, 0, -1):
            spots += [((xs[i] + xs[i - 1]) / 2, (ys[i] + ys[i - 1]) / 2), (xs[i - 1], ys[i - 1])]
        for x, y in spots + [(xs[-1], ys[-1])]:
            a = ax.annotate(name, (x, y), xytext=(0, -9), textcoords="offset points", ha="center", va="top",
                            fontsize=8.5, color=INK_2, zorder=4)
            b = a.get_window_extent(r)
            inside = frame.x0 <= b.x0 and b.x1 <= frame.x1 and frame.y0 <= b.y0
            if inside and not any(b.overlaps(o) for o in blocked):
                blocked.append(b)
                break
            a.remove()
        else:                                                 # nowhere free: under the last point regardless
            blocked.append(ax.annotate(name, (xs[-1], ys[-1]), xytext=(0, -9), textcoords="offset points",
                                       ha="center", va="top", fontsize=8.5, color=INK_2).get_window_extent(r))


def _dot_boxes(ax, coll, pad=5):
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


def within_lab_slope(rows: list[dict]) -> float | None:
    """Points a year: the press-enter rate on release date, each lab (and profession) with its own level."""
    import numpy as np
    if len({t["model"] for t in rows}) < 3:
        return None
    labs, profs = sorted({t["lab"] for t in rows}), sorted({t["profession"] for t in rows})
    X = np.array([[(t["released"] - JAN1).days / 365.25] + [t["lab"] == l for l in labs]
                  + [t["profession"] == q for q in profs[1:]] for t in rows], float)
    return float(np.linalg.lstsq(X, np.array([t["press_enter"] * 100 for t in rows]), rcond=None)[0][0])


def pace(out: Path, table: list[dict], fname: str, title: str, subtitle: str, prof: str | None = None):
    """One dot per model (its mean over the professions shown), its lab's color; one line: the within-lab trend,
    drawn through the dots' center, named just below it."""
    fig, ax = figure(title, subtitle)
    rows = [t for t in table if prof is None or t["profession"] == prof]
    pts = {}
    for t in rows:
        pts.setdefault((t["model"], t["lab"], t["released"]), []).append(t["press_enter"] * 100)
    xs = [mdates.date2num(r) for (_, _, r) in pts]
    ys = [sum(v) / len(v) for v in pts.values()]
    for ((m, lab, r), v), x, y in zip(pts.items(), xs, ys):
        dot(ax, [x], [y], LABS[lab][1])
    slope = within_lab_slope(rows)
    if slope is not None:
        cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
        x0, x1 = min(xs) - 10, max(xs) + 10
        line_x = [x0, x1]
        line_y = [cy + slope * (x - cx) / 365.25 for x in line_x]
        ax.plot(line_x, line_y, color=INK, lw=2, solid_capstyle="round", zorder=2)
        trend = (x0, x1, cx, cy, slope)
    months(ax)
    pct(ax)
    ax.set_ylim(0, max(ys) * 1.12 + 4)
    ax.set_ylabel("share of the week's work done unasked")
    save(fig, out / fname, legend=[key(c, n) for n, c in LABS.values()], trend=(ax, trend) if slope is not None else None)


def name_trend(fig, ax, trend):
    """The trend's name just below its line, at the first spot from the right that covers no dot."""
    x0, x1, cx, cy, slope = trend
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    marks = [b for c in ax.collections for b in _dot_boxes(ax, c)]
    for f in (0.82, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.9):
        tx = x0 + f * (x1 - x0)
        a = ax.annotate(f"+{slope:.0f} points a year", (tx, cy + slope * (tx - cx) / 365.25), xytext=(0, -10),
                        textcoords="offset points", ha="center", va="top", fontsize=9, color=INK, fontweight="bold",
                        zorder=4)
        if not any(a.get_window_extent(r).overlaps(m) for m in marks):
            return
        a.remove()
    ax.annotate(f"+{slope:.0f} points a year", (x0 + 0.82 * (x1 - x0), cy + slope * (0.32 * (x1 - x0)) / 365.25),
                xytext=(0, -10), textcoords="offset points", ha="center", va="top", fontsize=9, color=INK,
                fontweight="bold")


def main():
    res = Path(sys.argv[1])
    out = res / "figures"
    out.mkdir(parents=True, exist_ok=True)
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
        table.append({"model": m.name, "lab": m.family, "released": m.released, "profession": r["profession"],
                      **measures(r, minutes[r["profession"]], cal, wages[r["profession"]])})
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

    # 1. pace
    pace(out, table, "pace.png", "AI assistants do far more of the week unasked than they did in January",
         "Share of a week's planned work done without being asked, well enough to send as is. Mean of eight jobs")

    # 2. every profession
    fig, ax = figure("The rise shows up in every occupation",
                     "Best model in force on 1 January against the best model today, same week of work", (7.2, 4.8))
    best = lambda ts, p: max((t["press_enter"] * 100 for t in ts if t["profession"] == p), default=0)  # noqa: E731
    order = sorted(profs, key=lambda p: best(table, p))   # today: every model released so far is available
    for i, p in enumerate(order):
        a, b = best(jan, p), best(table, p)
        ax.plot([a, b], [i, i], color=GRID, lw=2, zorder=1)
        dot(ax, a, i, MUTED)
        dot(ax, b, i, LABS["openai"][1])
        ax.annotate(f"{b:.0f}%", (b, i), xytext=(8, 0), textcoords="offset points", va="center", fontsize=8.5,
                    color=INK_2)
    ax.set_yticks(range(len(order)), [TITLES.get(p, p) for p in order])
    ax.grid(axis="y", visible=False)
    pct(ax, "x")
    ax.set_xlim(0, max(best(table, p) for p in profs) + 10)
    save(fig, out / "professions.png", legend=[key(MUTED, "Best on 1 January"), key(LABS["openai"][1], "Best today")])

    # 3. capability against usage
    fig, ax = figure("AI can do as much in jobs where few use it as where many do",
                     "Newest models' share of the week done unasked, against how much of the job's work people "
                     "already bring to AI")
    items = []
    for p in profs:
        x, y = exposure.get(soc[p], 0) * 100, mean(t["press_enter"] * 100 for t in newest if t["profession"] == p)
        dot(ax, x, y, LABS["openai"][1])
        items.append((x, y, TITLES.get(p, p)))
    pct(ax, "x")
    pct(ax)
    ax.set_xlabel("observed AI use in the occupation (Anthropic Economic Index)")
    ax.set_ylabel("share of the week done unasked")
    ax.set_ylim(0, max(y for _, y, _ in items) * 1.25)
    ax.set_xlim(0, max(x for x, _, _ in items) * 1.15)
    save(fig, out / "usage.png", labels=(ax, items))

    # 4. net value
    fig, ax = figure("It pays where the work is substantial, and costs money on small tasks",
                     "Newest models' mean net value per worker-week: time saved, less checking and fixing time and "
                     "compute", (7.2, 4.8))
    vals = {p: mean(t["value"] for t in newest if t["profession"] == p) for p in profs}
    order = sorted(profs, key=vals.get)
    ax.barh(range(len(order)), [vals[p] for p in order], height=0.55, color=LABS["openai"][1], zorder=2)
    for i, p in enumerate(order):
        v = vals[p]
        ax.annotate(f"{'-' if v < 0 else ''}${abs(v):,.0f}", (v, i), xytext=(6 if v >= 0 else -6, 0),
                    textcoords="offset points", va="center", ha="left" if v >= 0 else "right", fontsize=8.5,
                    color=INK_2)
    ax.axvline(0, color=INK_2, lw=1)
    ax.set_yticks(range(len(order)), [TITLES.get(p, p) for p in order])
    ax.grid(axis="y", visible=False)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.margins(x=0.15)
    save(fig, out / "value.png")

    # 5. cost
    fig, ax = figure("Open-weight models come close at a sliver of the compute",
                     "Each model's compute per worker-week against its share of the week done unasked, mean over "
                     "the professions")
    items = []
    for g, (name, color) in GROUPS.items():
        ms = sorted({t["model"] for t in table if (t["lab"] in OPEN_WEIGHT) == (g == "open")})
        for m in ms:
            ts = [t for t in table if t["model"] == m]
            x, y = max(mean(t["cost"] for t in ts), 0.01), mean(t["press_enter"] * 100 for t in ts)
            dot(ax, x, y, color)
            if m in CALLOUTS:
                items.append((x, y, m))
    ax.set_xscale("log")
    ax.set_xlim(0.5, None)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"${v:,.0f}" if v >= 1 else f"${v:.2f}"))
    pct(ax)
    ax.set_xlabel("compute per worker-week (log scale)")
    ax.set_ylabel("share of the week done unasked")
    ax.set_ylim(0, None)
    save(fig, out / "cost.png", legend=[key(c, n) for n, c in GROUPS.values()], labels=(ax, items))

    # 6. harm
    fig, ax = figure("Doing more did not mean more harm",
                     "Harmful proposals a week (a trap set off and judged harmful), each model's mean over the "
                     "professions")
    for m in sorted({t["model"] for t in table}):
        ts = [t for t in table if t["model"] == m]
        dot(ax, mean(t["press_enter"] * 100 for t in ts), mean(t["traps"] for t in ts), LABS[ts[0]["lab"]][1])
    pct(ax, "x")
    ax.set_xlabel("share of the week done unasked")
    ax.set_ylabel("harmful proposals per week")
    ax.set_ylim(0, None)
    save(fig, out / "harm.png", legend=[key(c, n) for n, c in LABS.values()])

    # appendix: noticing against doing, and the pace in each profession
    fig, ax = figure("Newer models notice more of the work; how well they do it changes less",
                     "Share of the planned work each model attempted, and how much of that it did well enough to send")
    for m in sorted({t["model"] for t in table}):
        ts = [t for t in table if t["model"] == m]
        dot(ax, mean(t["attempted"] * 100 for t in ts), mean(t["done_right"] * 100 for t in ts), LABS[ts[0]["lab"]][1])
    pct(ax, "x")
    pct(ax)
    ax.set_xlabel("planned work attempted")
    ax.set_ylabel("of that, done well enough to send")
    save(fig, out / "noticing.png", legend=[key(c, n) for n, c in LABS.values()])
    for p in profs:
        pace(out, table, f"pace-{p}.png", TITLES.get(p, p),
             "Share of the week's planned work done unasked, sendable as is, by release date", prof=p)
    print("wrote", sorted(x.name for x in out.iterdir()))


if __name__ == "__main__":
    main()
