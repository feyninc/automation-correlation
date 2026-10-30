"""Figures for a graded run, one finding each, in Feyn's chart style.

    uv run python scripts/figures.py results/final

Writes `<results>/figures/*.png` and `<results>/figures/table.csv` (one row per model and profession, the numbers
behind every figure). Each figure's title states its one finding; its subtitle says in a line what is plotted.

The style is the Feyn website's charts (feyn/website, the Pulpie article's charts and the design tokens in
src/styles/global.css): a raised-paper card in a 1px ink frame; a header (Archivo title, Lora subtitle, mono key)
and a footer (the source) set off by hairline rules; uppercase IBM Plex Mono for axis titles, keys and panel names;
warm-ink gridlines at 12%; orange for the measure the chart is about. A lab keeps its own brand color everywhere.

Over time, the charts use four dates: each lab's model in force on 1 January, 30 April and 31 July, and its newest
(config/run.yaml takes four models from each lab that way):
- pace.png: the press-enter rate, the five labs' mean and each lab on its own, as small multiples on one scale;
- cost.png: compute per hour of work sent as is, the five labs together, against the worker's own hour;
- value.png: net value per worker-week, as pace.png;
- noticing.png: the share of planned work attempted, with the share sent as is inside it;
- pace-jobs.png (appendix): the five labs' mean press-enter rate in each job.
By job: value-jobs.png (net value per worker-week, the models of 1 January against the newest), professions.png (the
best model on 1 January against the best today). Across: usage.png (each job's press-enter rate against its observed
AI use) and harm.png (harmful proposals against the press-enter rate, with the trend across models). With
<results>/economics.json (scripts/economics.py): acemoglu.png (the two numbers behind Acemoglu's productivity
estimate, as he assumed them and as measured) and tasks.png (each O*NET task's press-enter rate, by whether the
Economic Index records AI use on it).

Press-enter rate: the share of the week's planned work, weighted by the minutes each need takes the worker, that the
model did well enough to send unchanged: for each need earned by a proposal, its minutes times the panel's
probability that the worker sends it unchanged; the sum over the week's planned minutes.
"""
import csv
import datetime as dt
import json
import logging
import math
import sys
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)   # the fallback has no medium weight
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from workweek import config  # noqa: E402
from workweek.engine import load_episode  # noqa: E402

# Feyn's tokens (feyn/website/src/styles/global.css)
RAISED, INK, BODY, SOFT, FAINT = "#fbf7f0", "#1b1714", "#3f382f", "#756a5e", "#9a9081"
ORANGE, TINT, HAIR = "#c6531d", "#efd9c6", "#d7cbb6"
GRIDLINE = (27 / 255, 23 / 255, 20 / 255, 0.12)
SANS, SERIF, MONO, MONO_M = "Archivo SemiBold", "Lora", "IBM Plex Mono", "IBM Plex Mono Medium"   # fontsource names
FALLBACK = ["DejaVu Sans"]
# each lab's brand color: OpenAI's green, Anthropic's clay, DeepSeek's blue, Kimi's black; Z.ai's mark is black and
# white too, so it takes the violet of Zhipu's earlier mark to stay apart from Kimi
LABS = {"openai": ("OpenAI", "#10a37f"), "anthropic": ("Anthropic", "#d97757"), "deepseek": ("DeepSeek", "#4d6bfe"),
        "moonshot": ("Moonshot (Kimi)", "#1c1c1c"), "zai": ("Z.ai (GLM)", "#8e5bd6")}
TITLES = {"claims-adjusters": "Claims adjusters", "accountants": "Accountants",
          "customer-service-representatives": "Customer service reps", "operations-managers": "Operations managers",
          "paralegals": "Paralegals", "market-research-analysts": "Market research analysts",
          "software-developers": "Software developers", "administrative-assistants": "Administrative assistants"}
SNAPSHOTS = ["1 January", "30 April", "31 July", "Today"]      # each lab's model in force on each date (run.yaml)
SHORT = ["1 Jan", "30 Apr", "31 Jul", "Today"]
JAN1 = dt.date(2026, 1, 1)

plt.rcParams.update({"font.family": [SANS] + FALLBACK, "font.size": 9, "text.parse_math": False,
                     "figure.facecolor": RAISED, "savefig.facecolor": RAISED, "axes.facecolor": RAISED,
                     "axes.edgecolor": SOFT, "axes.linewidth": 0.8, "axes.labelcolor": SOFT,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "axes.axisbelow": True,
                     "grid.color": GRIDLINE, "grid.linewidth": 0.8, "xtick.major.size": 0, "ytick.major.size": 0,
                     "xtick.color": SOFT, "ytick.color": SOFT, "xtick.major.pad": 6, "ytick.major.pad": 6})


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


# --- the card: header, footer, frame -------------------------------------------------------------------------------

def figure(title: str, subtitle: str, size=(7.2, 4.6), ncols=1, nrows=1, source: str | None = None):
    """A chart card: the title states the finding, the subtitle says in a line what is plotted; the source, when the
    data is someone else's, sits in a footer. The key and the header's rule are added by save()."""
    w, h = size
    fig, axes = plt.subplots(nrows, ncols, figsize=size, sharey=nrows * ncols > 1)
    px = 0.26 / w
    y = 1 - 0.26 / h
    fig.text(px, y, title, fontfamily=[SANS] + FALLBACK, fontweight=700, fontsize=13.5, color=INK, va="top")
    lines = textwrap.wrap(subtitle, int(w * 13.5))
    y -= 0.36 / h
    fig.text(px, y, "\n".join(lines), fontfamily=[SERIF] + FALLBACK, fontsize=9.5, color=BODY, va="top",
             linespacing=1.4)
    fig._px, fig._head = px, y - (0.19 * len(lines) + 0.06) / h
    fig._foot = 0.12 / h
    if source:
        rule = 0.36 / h
        fig.add_artist(Line2D([0, 1], [rule, rule], transform=fig.transFigure, color=HAIR, lw=0.8))
        fig.text(px, 0.13 / h, source, fontfamily=[SERIF] + FALLBACK, fontstyle="italic", fontsize=7.5, color=SOFT,
                 va="bottom")
        fig._foot = rule + 0.08 / h
    fig.add_artist(Rectangle((0, 0), 1, 1, transform=fig.transFigure, fill=False, edgecolor=INK, lw=1.6, zorder=10))
    return fig, axes


def save(fig, path: Path, legend=None, labels=None):
    h = fig.get_size_inches()[1]
    top = fig._head
    if legend:      # the key under the subtitle: the marks' row, then any line's
        marks = [k for k in legend if k.get_marker() not in (None, "None", "")]
        for row in (r for r in (marks, [k for k in legend if k not in marks]) if r):
            fig.legend(handles=row, loc="upper left", bbox_to_anchor=(fig._px - 0.008, top), ncol=len(row),
                       frameon=False, prop={"family": [MONO] + FALLBACK, "size": 7.5}, labelcolor=SOFT,
                       handlelength=1.3, handletextpad=0.6, columnspacing=1.8, borderaxespad=0)
            top -= 0.22 / h
    rule = top - (0.08 if legend else 0.02) / h
    fig.add_artist(Line2D([0, 1], [rule, rule], transform=fig.transFigure, color=HAIR, lw=0.8))
    fig.tight_layout(rect=(0.015, fig._foot, 0.985, rule - 0.1 / h))
    if labels:      # after the layout is final, so the free spots are measured where they will be
        place(fig, *labels)
    fig.savefig(path, dpi=220)
    plt.close(fig)


def key(color, label, marker="o"):
    return Line2D([], [], color=color, lw=0, marker=marker, markersize=6.5, markeredgecolor=color, label=label.upper())


def line_key(color, label, **kw):
    return Line2D([], [], color=color, label=label.upper(), **kw)


def style(ax, cats: str | None = None):
    """Numbers on the axes in mono; category names (jobs, groups) in the sans, in body ink."""
    for axis in ("x", "y"):
        for t in (ax.get_xticklabels() if axis == "x" else ax.get_yticklabels()):
            if axis == cats:
                t.set_fontfamily([SANS] + FALLBACK)
                t.set_fontsize(9)
                t.set_color(BODY)
            else:
                t.set_fontfamily([MONO] + FALLBACK)
                t.set_fontsize(7.5)
                t.set_color(SOFT)


def axis_title(ax, x: str | None = None, y: str | None = None):
    kw = {"fontfamily": [MONO] + FALLBACK, "fontsize": 7.5, "color": SOFT}
    if x:
        ax.set_xlabel(x.upper(), labelpad=8, **kw)
    if y:
        ax.set_ylabel(y.upper(), labelpad=8, **kw)


def panel_title(ax, text: str):
    ax.set_title(text.upper(), loc="left", fontfamily=[MONO_M] + FALLBACK, fontweight=500, fontsize=7.5, color=INK, pad=8)


def value_label(ax, x, y, text, big=False, color=INK, below=False):
    ax.annotate(text, (x, y), xytext=(0, -3 if below else 3), textcoords="offset points", ha="center",
                va="top" if below else "bottom", fontfamily=[MONO_M if big else MONO] + FALLBACK, fontweight=500 if big else 400,
                fontsize=8.5 if big else 7.5, color=color, zorder=4)


def dot(ax, x, y, color, size=44, **kw):
    ax.scatter(x, y, s=size, color=color, edgecolors=RAISED, linewidths=1.6, zorder=3, **kw)


def pct(ax, axis="y"):
    fmt = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)


def money(v: float) -> str:
    return f"{'-' if v < 0 else ''}${abs(v):,.0f}"


# --- direct labels ------------------------------------------------------------------------------------------------

# where a label may sit around its point: right beside it first, then left, below, above; then farther out in eight
# directions, joined to its point by a hairline so it is never read as another point's
NEAR = [(8, 0, "left", "center"), (-8, 0, "right", "center"), (0, -9, "center", "top"), (0, 9, "center", "bottom")]
FAR = [(dx * d, dy * d, ha, va) for d in (20, 32, 46) for dx, dy, ha, va in
       ((1, 0, "left", "center"), (-1, 0, "right", "center"), (0, -1, "center", "top"), (0, 1, "center", "bottom"),
        (0.8, -0.8, "left", "top"), (-0.8, -0.8, "right", "top"), (0.8, 0.8, "left", "bottom"),
        (-0.8, 0.8, "right", "bottom"))]


def place(fig, ax, items):
    """Direct labels that never overlap each other, a mark, or the plot's edge: each (x, y, text) takes the first free
    spot around its point, beside it if that is free; a label set farther out gets a hairline to its point."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    marks = [b for c in ax.collections for b in _dot_boxes(ax, c)]
    taken = []
    frame = ax.get_window_extent(r)
    for x, y, text in sorted(items, key=lambda i: -i[1]):
        for dx, dy, ha, va in NEAR + FAR:
            far = abs(dx) + abs(dy) > 12
            a = ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, va=va, fontsize=8,
                            color=BODY, zorder=4, bbox=dict(boxstyle="square,pad=0.12", fc=RAISED, ec="none"),
                            arrowprops=dict(arrowstyle="-", color=FAINT, lw=0.6, shrinkA=1, shrinkB=4) if far else None)
            a.update_positions(r)
            b = matplotlib.text.Text.get_window_extent(a, r)          # the text alone, not its hairline
            inside = frame.x0 <= b.x0 and b.x1 <= frame.x1 and frame.y0 <= b.y0 and b.y1 <= frame.y1
            if inside and not any(b.overlaps(o) for o in marks + taken):
                taken.append(b)
                break
            a.remove()
        else:
            taken.append(ax.annotate(text, (x, y), xytext=(0, -9), textcoords="offset points", ha="center",
                                     va="top", fontsize=8, color=BODY).get_window_extent(r))


def _dot_boxes(ax, coll, pad=7):
    from matplotlib.transforms import Bbox
    pts = ax.transData.transform(coll.get_offsets())
    return [Bbox([[px - pad, py - pad], [px + pad, py + pad]]) for px, py in pts]


# --- the shapes ---------------------------------------------------------------------------------------------------

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


def snapshot_of(models: dict[str, dict]) -> dict[str, int]:
    """Each model's date: its rank among its lab's models by release (the run takes four from each lab)."""
    out = {}
    for lab in {r["lab"] for r in models.values()}:
        for i, m in enumerate(sorted((m for m, r in models.items() if r["lab"] == lab),
                                     key=lambda m: models[m]["released"])):
            out[m] = i
    return out


def date_axis(ax, labels=SHORT):
    ax.set_xticks(range(len(labels)), labels)
    ax.grid(axis="x", visible=False)
    ax.axhline(0, color=SOFT, lw=0.8, zorder=2.5)
    ax.spines["bottom"].set_visible(False)


def lab_panels(axes, models, snap, value, fmt):
    """Small multiples on one scale: the five labs' mean first, in orange with its values in bold, then one panel per
    lab in its color; four bars each, one per date."""
    by = {(models[m]["lab"], snap[m]): value(models[m]) for m in models}
    panels = [("All five labs, mean", ORANGE, [sum(by[(lab, i)] for lab in LABS) / len(LABS) for i in range(4)])]
    panels += [(name, color, [by[(lab, i)] for i in range(4)]) for lab, (name, color) in LABS.items()]
    lo = min(min(ys) for _, _, ys in panels)
    hi = max(max(ys) for _, _, ys in panels)
    for k, (ax, (name, color, ys)) in enumerate(zip(axes.flat, panels)):
        ax.bar(range(4), ys, 0.62, color=color, zorder=2)
        for i, y in enumerate(ys):
            value_label(ax, i, y, fmt(y), big=k == 0, below=y < 0)
        panel_title(ax, name)
        date_axis(ax)
        style(ax)
    pad = (hi - min(0, lo)) * 0.14
    axes.flat[0].set_ylim(min(0, lo) - (pad if lo < 0 else 0), hi + pad)


def dumbbell(ax, rows, fmt, bold_last=True):
    """One row per (name, before, after): the before dot in warm grey, the after dot in orange, joined by a soft
    hairline; the before value outside on its side, the after value in bold mono."""
    for i, (name, a, b) in enumerate(rows):
        ax.plot([a, b], [i, i], color=HAIR, lw=2.2, zorder=1, solid_capstyle="butt")
        dot(ax, a, i, FAINT)
        dot(ax, b, i, ORANGE)
        right = b >= a
        ax.annotate(fmt(b), (b, i), xytext=(8 if right else -8, 0), textcoords="offset points", va="center",
                    ha="left" if right else "right", fontfamily=[MONO_M] + FALLBACK, fontweight=500, fontsize=8.5, color=INK)
        ax.annotate(fmt(a), (a, i), xytext=(-8 if right else 8, 0), textcoords="offset points", va="center",
                    ha="right" if right else "left", fontfamily=[MONO] + FALLBACK, fontsize=7.5, color=SOFT)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    ax.margins(x=0.12)
    style(ax, cats="y")
    if bold_last:
        ax.get_yticklabels()[-1].set_fontweight(700)
        ax.get_yticklabels()[-1].set_color(INK)


def main():
    res = Path(sys.argv[1])
    out = res / "figures"
    out.mkdir(parents=True, exist_ok=True)
    for old in ["savings.png"] + [p.name for p in out.glob("pace-*.png") if p.name != "pace-jobs.png"]:
        (out / old).unlink(missing_ok=True)            # replaced: a figure no longer drawn is not left behind
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
    snap = snapshot_of(models)
    at = lambda i: [m for m in models if snap[m] == i]  # noqa: E731
    group_mean = lambda ts, k: mean(models[m][k] for m in {t["model"] for t in ts})  # noqa: E731
    pct0 = lambda v: f"{v:.0f}%"  # noqa: E731

    # 1. the level and the pace: the five labs' mean, then each lab, on the four dates
    a, b = group_mean(jan, "press_enter") * 100, group_mean(newest, "press_enter") * 100
    fig, axes = figure(f"AI now does {b:.0f}% of the week unasked, up from {a:.0f}% in January",
                       "Share of the week's work sent as is, by the model in force on each date", (7.2, 5.4),
                       ncols=3, nrows=2)
    lab_panels(axes, models, snap, lambda r: r["press_enter"] * 100, pct0)
    for ax in axes.flat:
        pct(ax)
    save(fig, out / "pace.png")

    # 2. more work for less: all five labs' compute over all five labs' finished hours, on each date
    def per_hour(ms):
        return sum(models[m]["cost"] for m in ms) / sum(models[m]["hours_done"] for m in ms)
    wage = mean(wages.values())
    hours = [per_hour(at(i)) for i in range(len(SNAPSHOTS))]
    fig, ax = figure(f"An hour of finished work now takes ${hours[-1]:.0f} of compute, down from ${hours[0]:.0f}",
                     "Compute per hour of work sent as is, the five labs' models on each date")
    ax.bar(range(4), hours, 0.56, color=ORANGE, zorder=2)
    for i, y in enumerate(hours):
        value_label(ax, i, y, f"${y:,.0f}", big=True)
    ax.axhline(wage, color=SOFT, lw=0.9, ls=(0, (4, 3)), zorder=1.5)
    ax.annotate(f"the worker's own hour, ${wage:.0f}".upper(), (1, wage), xycoords=("axes fraction", "data"),
                xytext=(0, 5), textcoords="offset points", ha="right", va="bottom", fontfamily=[MONO] + FALLBACK,
                fontsize=7.5, color=SOFT)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.set_ylim(0, max(max(hours), wage) * 1.18)
    date_axis(ax, SNAPSHOTS)
    style(ax, cats="x")
    save(fig, out / "cost.png")

    # 3. what it is worth: on each date, then by job
    a, b = group_mean(jan, "value"), group_mean(newest, "value")
    fig, axes = figure(f"The help is now worth {money(round(b, -1))} a worker-week, up from "
                       f"{'nothing' if abs(a) < 50 else money(a)}",
                       "Net value per worker-week after checking and compute, by the model in force on each date",
                       (7.2, 5.4), ncols=3, nrows=2)
    lab_panels(axes, models, snap, lambda r: r["value"], money)
    for ax in axes.flat:
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: money(v)))
    save(fig, out / "value.png")

    fig, ax = figure("The newest models pay most where tasks are large",
                     "Net value per worker-week, mean of the five labs' models", (7.2, 5.0))
    vals = {p: (mean(t["value"] for t in jan if t["profession"] == p), mean(t["value"] for t in newest
                                                                             if t["profession"] == p)) for p in profs}
    order = sorted(profs, key=lambda p: vals[p][1])
    dumbbell(ax, [(TITLES.get(p, p), *vals[p]) for p in order] + [("All eight jobs", a, b)], money)
    ax.axvline(0, color=SOFT, lw=0.8, zorder=0.5)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: money(v)))
    style(ax, cats="y")
    ax.get_yticklabels()[-1].set_fontweight(700)
    save(fig, out / "value-jobs.png", legend=[key(FAINT, "Models of 1 January"), key(ORANGE, "Newest models")])

    # 4. noticing against quality: what the models attempted, and inside it what was sent as is
    att = [mean(models[m]["attempted"] * 100 for m in at(i)) for i in range(len(SNAPSHOTS))]
    done = [mean(models[m]["press_enter"] * 100 for m in at(i)) for i in range(len(SNAPSHOTS))]
    right = [mean(models[m]["done_right"] * 100 for m in at(i)) for i in range(len(SNAPSHOTS))]
    fig, ax = figure("Newer models attempt twice as much of the week, and do it a little better",
                     "Share of the week's work, mean of the five labs' models on each date", (7.2, 4.8))
    for i in range(len(SNAPSHOTS)):
        ax.bar(i, att[i], 0.56, color=TINT, zorder=2)
        ax.bar(i, done[i], 0.56, color=ORANGE, zorder=2.2)
        value_label(ax, i, att[i], f"{att[i]:.0f}%", big=True)
        value_label(ax, i, done[i], f"{done[i]:.0f}%", big=True, color=ORANGE)
    date_axis(ax, [f"{d}\n{r:.0f}% of attempts sendable" for d, r in zip(SNAPSHOTS, right)])
    style(ax, cats="x")
    pct(ax)
    ax.set_ylim(0, max(att) * 1.15)
    save(fig, out / "noticing.png", legend=[key(TINT, "Attempted", "s"), key(ORANGE, "Sent as is", "s")])

    # 5. every occupation: the best model then and now; today's named
    fig, ax = figure("In every job, the best model today does more than January's best",
                     "Share of the week's work sent as is, best model then and now", (7.2, 5.3))
    best = lambda ts, p: max((t for t in ts if t["profession"] == p), key=lambda t: t["press_enter"])  # noqa: E731
    order = sorted(profs, key=lambda p: best(table, p)["press_enter"])
    dumbbell(ax, [(TITLES.get(p, p), best(jan, p)["press_enter"] * 100, best(table, p)["press_enter"] * 100)
                  for p in order], pct0, bold_last=False)
    for i, p in enumerate(order):
        t = best(table, p)
        ax.annotate(t["model"], (t["press_enter"] * 100, i), xytext=(0, 7), textcoords="offset points",
                    ha="center", va="bottom", fontsize=7.5, color=BODY)
    jan_best = sorted({best(jan, p)["model"] for p in profs})
    pct(ax, "x")
    ax.set_xlim(0, max(best(table, p)["press_enter"] for p in profs) * 100 + 8)
    ax.set_ylim(-0.6, len(order) - 0.3)
    style(ax, cats="y")
    jan_label = (f"Best on 1 January ({jan_best[0]} in every job)" if len(jan_best) == 1
                 else "Best on 1 January (" + ", ".join(jan_best) + ")")
    save(fig, out / "professions.png", legend=[key(FAINT, jan_label), key(ORANGE, "Best today, named")])

    # 6. capability against use, by job
    fig, ax = figure("AI can do a similar share of each job, however much it is used there",
                     "Each dot is a job; newest models, mean of the five labs",
                     source="Observed AI use: observed exposure, Massenkoff and McCrory, Anthropic, 2026.")
    items = []
    for p in profs:
        x, y = exposure.get(soc[p], 0) * 100, mean(t["press_enter"] * 100 for t in newest if t["profession"] == p)
        dot(ax, x, y, ORANGE, size=52)
        items.append((x, y, f"{TITLES.get(p, p)} {y:.0f}%"))
    pct(ax, "x")
    pct(ax)
    axis_title(ax, "share of the job's work already done with AI", "share of the week done unasked")
    ax.set_ylim(0, max(y for _, y, _ in items) * 1.3)
    ax.set_xlim(-4, max(x for x, _, _ in items) * 1.2)       # off the corner, so the two 0% labels stay apart
    style(ax)
    save(fig, out / "usage.png", labels=(ax, items))

    # 7. harm: each lab's newest model is named, and the extremes on either axis
    import numpy as np
    fig, ax = figure("Models that do more of the week set off fewer traps, not more",
                     "Each dot is a model; named: each lab's newest, and the extremes")
    named = {t["model"] for t in newest}
    named |= {max(models, key=lambda m: models[m]["traps"]), max(models, key=lambda m: models[m]["press_enter"]),
              min(models, key=lambda m: models[m]["press_enter"])}
    items = []
    for m, r in models.items():
        dot(ax, r["press_enter"] * 100, r["traps"], LABS[r["lab"]][1])
        if m in named:
            items.append((r["press_enter"] * 100, r["traps"], m))
    xs = np.array([r["press_enter"] * 100 for r in models.values()])   # the trend across models, least squares
    k, c = np.polyfit(xs, [r["traps"] for r in models.values()], 1)
    ax.plot([xs.min(), xs.max()], [k * xs.min() + c, k * xs.max() + c], color=SOFT, lw=0.9, ls=(0, (5, 3)), zorder=1.5)
    pct(ax, "x")
    axis_title(ax, "share of the week done unasked", "harmful proposals per week")
    ax.set_ylim(-0.45, max(r["traps"] for r in models.values()) * 1.12)
    ax.set_yticks([0, 0.5, 1, 1.5, 2, 2.5])
    style(ax)
    save(fig, out / "harm.png", legend=[key(c, n) for n, c in LABS.values()]
         + [line_key(SOFT, "Trend across the 20 models", lw=0.9, ls=(0, (5, 3)))], labels=(ax, items))

    # appendix: the pace in every job, the five labs' mean on each date
    fig, axes = figure("The rise shows up in every job",
                       "Share of the week's work sent as is, mean of the five labs' models on each date", (7.2, 6.6),
                       ncols=4, nrows=2)
    for ax, p in zip(axes.flat, sorted(profs, key=lambda p: -mean(t["press_enter"] for t in newest
                                                                    if t["profession"] == p))):
        ys = [mean(t["press_enter"] * 100 for t in table if t["profession"] == p and snap[t["model"]] == i)
              for i in range(len(SNAPSHOTS))]
        ax.bar(range(4), ys, 0.62, color=ORANGE, zorder=2)
        for i, y in enumerate(ys):
            value_label(ax, i, y, f"{y:.0f}%")
        panel_title(ax, TITLES.get(p, p).replace("Administrative", "Admin."))
        date_axis(ax)
        pct(ax)
        style(ax)
        for t in ax.get_xticklabels():
            t.set_fontsize(6.5)
    save(fig, out / "pace-jobs.png")

    if (res / "economics.json").exists():          # scripts/economics.py
        econ = json.loads((res / "economics.json").read_text())
        acemoglu(out, econ)
        tasks_use(out, econ)
    print("wrote", sorted(x.name for x in out.iterdir()))


def acemoglu(out: Path, econ: dict):
    """The two numbers behind Acemoglu's productivity estimate (the share of work AI takes on, the cost saving on it),
    as he assumed them and as measured here with the newest models, with 90% intervals."""
    a = econ["acemoglu"]
    n = econ["newest"]
    fig, ax = figure("Both numbers behind the leading productivity estimate are larger here",
                     "Assumed for the US economy against measured in eight jobs, with 90% intervals", (7.2, 4.6),
                     source="Assumed: Acemoglu, \"The Simple Macroeconomics of AI\", NBER working paper 32487 (2024), "
                            "pages 6 and 30.")
    groups = [("Share of work AI takes on", a["share_of_tasks"], n["weighted"]["affected"],
               n["weighted_90"]["affected"]),
              ("Cost saving on that work", a["labor_cost_saving_on_them"], n["per_affected"],
               n["weighted_90"]["per_affected"])]
    w = 0.32
    for i, (name, assumed, measured, (lo, hi)) in enumerate(groups):
        ax.bar(i - w / 2 - 0.02, assumed * 100, w, color=FAINT, zorder=2)
        ax.bar(i + w / 2 + 0.02, measured * 100, w, color=ORANGE, zorder=2)
        ax.errorbar(i + w / 2 + 0.02, measured * 100, yerr=[[(measured - lo) * 100], [(hi - measured) * 100]],
                    color=INK, lw=1, capsize=4, capthick=1, zorder=3)
        value_label(ax, i - w / 2 - 0.02, assumed * 100,
                    f"{assumed * 100:.1f}%" if assumed < 0.1 else f"{assumed * 100:.0f}%", big=True, color=SOFT)
        value_label(ax, i + w / 2 + 0.02, hi * 100, f"{measured * 100:.0f}%", big=True)
    ax.set_xticks([0, 1], [g[0] for g in groups])
    ax.grid(axis="x", visible=False)
    ax.axhline(0, color=SOFT, lw=0.8, zorder=2.5)
    ax.spines["bottom"].set_visible(False)
    pct(ax)
    ax.set_ylim(0, 80)
    style(ax, cats="x")
    save(fig, out / "acemoglu.png", legend=[key(FAINT, "Assumed in the estimate", "s"),
                                            key(ORANGE, "Measured in these eight jobs", "s")])


def tasks_use(out: Path, econ: dict):
    """Each O*NET task in the weeks: the newest models' press-enter rate on it, by whether the Economic Index records
    AI use on it; dot size is the task's planned minutes, the line each group's minute-weighted mean."""
    import random
    rows = [t for t in econ["tasks"]["rows"] if t["usage"] is not None]
    groups = [("No recorded AI use", [t for t in rows if t["usage"] == 0]),
              ("Some recorded AI use", [t for t in rows if t["usage"] > 0])]
    fig, ax = figure("AI does as much on tasks with no recorded AI use as on tasks with some",
                     "Each dot is an O*NET task, sized by its minutes; newest models", (7.2, 5.0),
                     source="Recorded AI use: the Anthropic Economic Index, which maps Claude conversations to O*NET "
                            "tasks.")
    rng = random.Random(7)
    top = max(t["press_enter"] for t in rows) * 100
    for gi, (name, ts) in enumerate(groups):
        xs = [gi + rng.uniform(-0.28, 0.28) for _ in ts]
        sizes = [12 + 260 * (t["minutes"] / max(r["minutes"] for r in rows)) ** 0.5 for t in ts]
        ax.scatter(xs, [t["press_enter"] * 100 for t in ts], s=sizes, color=ORANGE, alpha=0.28, edgecolors=RAISED,
                   linewidths=0.8, zorder=2)
        m = sum(t["press_enter"] * t["minutes"] for t in ts) / sum(t["minutes"] for t in ts) * 100
        ax.plot([gi - 0.36, gi + 0.36], [m, m], color=INK, lw=1.4, zorder=3)
        ax.annotate(f"{m:.0f}%", (gi + 0.36, m), xytext=(6, 0), textcoords="offset points", va="center",
                    fontfamily=[MONO_M] + FALLBACK, fontweight=500, fontsize=9, color=INK)
        groups[gi] = (f"{name}\n{len(ts)} tasks", ts)
    ax.set_xticks([0, 1], [g[0] for g in groups])
    ax.set_xlim(-0.6, 1.75)
    ax.set_ylim(0, top * 1.08 + 2)
    ax.grid(axis="x", visible=False)
    pct(ax)
    axis_title(ax, y="share sent as is")
    style(ax, cats="x")
    save(fig, out / "tasks.png")


if __name__ == "__main__":
    main()
