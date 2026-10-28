"""Figures for a graded run: one simple message each, one panel per profession.

    uv run python scripts/figures.py results/batch-1

Writes `<results>/figures/*.png` and `<results>/figures/table.csv` (the numbers behind them):
- press_enter.png: press-enter rate against release date, one line per lab;
- net_value.png: net value per worker-week against release date;
- cost_quality.png: compute cost per worker-week against press-enter rate;
- noticing_doing.png: share of planned work attempted against the share of it done to send-as-is quality;
- harm.png: traps fired per model.

Press-enter rate: the share of the week's planned work, weighted by the minutes each need takes the worker, that the
model did well enough to send unchanged: for each need earned by a proposal, its minutes times the panel's
probability that the worker sends it unchanged; the sum over the week's planned minutes.
"""
import csv
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

LABS = {"openai": ("OpenAI", "#1f77b4"), "anthropic": ("Anthropic", "#d4673a"), "moonshot": ("Moonshot", "#6a3d9a"),
        "deepseek": ("DeepSeek", "#2ca02c"), "zai": ("Z.ai", "#7f7f7f")}
TITLES = {"claims-adjusters": "Claims adjusters", "accountants": "Accountants",
          "customer-service-representatives": "Customer service"}


def measures(row: dict, minutes: dict[str, float]) -> dict:
    score = {i: (g["panel"].get("score") or 0) / 100 for i, g in enumerate(row["graded"])}   # needs name proposals by position
    planned = sum(minutes.get(n["need"], 0) for n in row["needs"]) or 1
    caught = [n for n in row["needs"] if n["caught"]]
    done = sum(minutes.get(n["need"], 0) * score.get(n["proposal"], 0) for n in caught)
    attempted = sum(minutes.get(n["need"], 0) for n in caught)
    return {"press_enter": done / planned, "attempted": attempted / planned,
            "done_right": done / attempted if attempted else 0.0,
            "value": sum(g["value"]["value_usd"] for g in row["graded"]) - row.get("questions_cost_usd", 0),
            "cost": row.get("token_cost_usd") or 0, "traps": sum(t["fired"] for t in row["traps"]),
            "needs_caught": len(caught), "needs": len(row["needs"])}


def main():
    res = Path(sys.argv[1])
    out = res / "figures"
    out.mkdir(parents=True, exist_ok=True)
    cfg = config.load(ROOT / "config/run.yaml")
    spec = {m.name: m for m in cfg.models}
    rows = [json.loads(line) for line in (res / "graded.jsonl").read_text().splitlines()]
    minutes = {}
    for prof in {r["profession"] for r in rows}:
        ep = load_episode(ROOT / "professions" / prof / "episode")
        minutes[prof] = {n.id: n.minutes.do for n in ep.needs}
    table = []
    for r in rows:
        m = spec[r["model"]]
        table.append({"model": m.name, "lab": m.family, "released": m.released, "profession": r["profession"],
                      **measures(r, minutes[r["profession"]])})
    with open(out / "table.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(table[0]))
        w.writeheader()
        w.writerows(table)
    present = sorted({t["profession"] for t in table})
    profs = [p for p in TITLES if p in present] + [p for p in present if p not in TITLES]

    def panels(title: str):
        fig, axes = plt.subplots(1, len(profs), figsize=(4.6 * len(profs), 3.9), sharey=True, squeeze=False)
        fig.suptitle(title, x=0.01, ha="left", fontsize=13)
        for ax, p in zip(axes[0], profs):
            ax.set_title(TITLES.get(p, p.replace("-", " ").capitalize()), loc="left", fontsize=11)
            ax.spines[["top", "right"]].set_visible(False)
        return fig, axes[0]

    def by_release(key: str, title: str, ylabel: str, fname: str, percent: bool):
        fig, axes = panels(title)
        for ax, p in zip(axes, profs):
            for lab, (label, color) in LABS.items():
                pts = sorted((t["released"], t[key]) for t in table if t["profession"] == p and t["lab"] == lab)
                if not pts:
                    continue
                xs, ys = [x for x, _ in pts], [y * (100 if percent else 1) for _, y in pts]
                ax.plot(xs, ys, "-o", color=color, lw=1.8, ms=4)
                ax.annotate(label, (xs[-1], ys[-1]), xytext=(5, 0), textcoords="offset points", color=color,
                            fontsize=8, va="center")
            ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
            ax.tick_params(labelsize=8)
            if key == "value":
                ax.axhline(0, color="black", lw=0.6)
            else:
                ax.set_ylim(bottom=0)
        axes[0].set_ylabel(ylabel)
        fig.tight_layout()
        fig.savefig(out / fname, dpi=160)
        plt.close(fig)

    by_release("press_enter", "Share of the week's planned work done well enough to send unchanged",
               "press-enter rate (% of planned minutes)", "press_enter.png", True)
    by_release("value", "Net value per worker-week, after checking time and compute",
               "dollars per worker-week", "net_value.png", False)

    fig, axes = panels("Compute cost against quality, one point per model")
    for ax, p in zip(axes, profs):
        for t in table:
            if t["profession"] == p:
                ax.scatter(max(t["cost"], 0.01), t["press_enter"] * 100, color=LABS[t["lab"]][1], s=26)
        ax.set_xscale("log")
        ax.set_ylim(0, max(10, max(t["press_enter"] * 100 for t in table) * 1.15))
        ax.set_xlabel("compute cost per worker-week ($, log scale)", fontsize=8)
        ax.tick_params(labelsize=8)
    axes[0].set_ylabel("press-enter rate (%)")
    for lab, (label, color) in LABS.items():
        axes[-1].scatter([], [], color=color, label=label, s=26)
    axes[-1].legend(frameon=False, fontsize=8, loc="best")
    fig.tight_layout()
    fig.savefig(out / "cost_quality.png", dpi=160)
    plt.close(fig)

    fig, axes = panels("Noticing the work against doing it right")
    for ax, p in zip(axes, profs):
        for t in table:
            if t["profession"] == p:
                ax.scatter(t["attempted"] * 100, t["done_right"] * 100, color=LABS[t["lab"]][1], s=26)
        ax.set_xlabel("planned work attempted (% of minutes)", fontsize=8)
        ax.set_xlim(0, max(10, max(t["attempted"] * 100 for t in table) * 1.15))
        ax.set_ylim(0, 100)
        ax.tick_params(labelsize=8)
    axes[0].set_ylabel("attempted work sendable as is (%)")
    for lab, (label, color) in LABS.items():
        axes[-1].scatter([], [], color=color, label=label, s=26)
    axes[-1].legend(frameon=False, fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(out / "noticing_doing.png", dpi=160)
    plt.close(fig)

    fig, axes = panels("Traps fired: harmful proposals in the week")
    for ax, p in zip(axes, profs):
        ts = sorted((t for t in table if t["profession"] == p), key=lambda t: (t["lab"], t["released"]))
        ax.barh([t["model"] for t in ts], [t["traps"] for t in ts], color=[LABS[t["lab"]][1] for t in ts])
        ax.invert_yaxis()
        ax.tick_params(labelsize=7)
        ax.set_xlabel("traps fired", fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "harm.png", dpi=160)
    plt.close(fig)
    print("wrote", sorted(x.name for x in out.iterdir()))


if __name__ == "__main__":
    main()
