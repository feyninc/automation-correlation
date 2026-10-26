"""Model release timeline: merge the release files, pick the benchmark set, draw the chart.

Selection rule: for each lab, its main line only; at each calendar quarter's end, the newest main-line model that
OpenRouter still serves. A quarter with no new release repeats the previous model.

    python3 -I scripts/timeline.py <project root>
"""
import csv, datetime as dt, html, json, sys
from pathlib import Path

root = Path(sys.argv[1])
rel = root / "data" / "releases"

LABS = ["openai", "anthropic", "moonshot", "deepseek", "glm"]
LAB_NAME = {"openai": "OpenAI", "anthropic": "Anthropic", "moonshot": "Moonshot (Kimi)", "deepseek": "DeepSeek", "glm": "Z.ai (GLM)"}
LINE_NAME = {"openai": "GPT main line (Sol from 5.6)", "anthropic": "Opus", "moonshot": "Kimi K",
             "deepseek": "V3 line, then Flash", "glm": "GLM"}

# Main-line membership and short labels, by model name in the release files.
MAIN = {
    "openai": {"GPT-4 (8k)": "4", "GPT-4 Turbo preview (DevDay)": "4T preview", "GPT-4 Turbo preview update": "0125",
               "GPT-4 Turbo (GA, with vision)": "4 Turbo", "GPT-4o 2024-05-13": "4o", "GPT-4o 2024-08-06": "4o-0806",
               "GPT-4o 2024-11-20": "4o-1120", "GPT-4.1": "4.1", "GPT-5": "5",
               "GPT-5.1 (Thinking)": "5.1", "GPT-5.2 (Thinking)": "5.2", "GPT-5.4 (Thinking)": "5.4",
               "GPT-5.5 (Thinking)": "5.5", "GPT-5.6 Sol": "5.6 Sol", "GPT-6 Sol": "6 Sol", "GPT-6.1 Sol": "6.1 Sol"},
    "anthropic": {"Claude 3 Opus": "3 Opus", "Claude Opus 4": "4", "Claude Opus 4.1": "4.1", "Claude Opus 4.5": "4.5", "Claude Opus 4.6": "4.6",
                  "Claude Opus 4.7": "4.7", "Claude Opus 4.8": "4.8", "Claude Opus 5": "5", "Claude Opus 5.5": "5.5"},
    "moonshot": {"Kimi K2 (Kimi-K2-Instruct, Kimi-K2-Base)": "K2", "Kimi-K2-Instruct-0905": "K2-0905",
                 "Kimi K2 Thinking": "K2 Th.", "Kimi K2.5": "K2.5", "Kimi K2.6": "K2.6", "Kimi K3": "K3",
                 "Kimi K3.1 Pro": "K3.1 Pro"},
    "deepseek": {"DeepSeek-V3": "V3", "DeepSeek-V3-0324": "V3-0324", "DeepSeek-V3.1": "V3.1",
                 "DeepSeek-V3.1-Terminus": "Term.", "DeepSeek-V3.2-Exp": "3.2-Exp", "DeepSeek-V3.2": "V3.2",
                 "DeepSeek-V4-Flash (Preview)": "V4-Flash", "DeepSeek-V4-Flash-0731": "0731",
                 "DeepSeek-V4.1-Flash": "V4.1-Flash", "DeepSeek-V4.1-Flash-1017": "1017"},
    "glm": {"GLM-4.7": "4.7", "GLM-5": "5", "GLM-5.1": "5.1", "GLM-5.2": "5.2", "GLM-5.3": "5.3"},
}
# OpenRouter ids the release files left blank (the models are listed under these ids).
OR_ID = {"Kimi K2 (Kimi-K2-Instruct, Kimi-K2-Base)": "moonshotai/kimi-k2", "Kimi-K2-Instruct-0905": "moonshotai/kimi-k2-0905",
         "DeepSeek-V3.1-Terminus": "deepseek/deepseek-v3.1-terminus", "DeepSeek-V3.2-Exp": "deepseek/deepseek-v3.2-exp"}
FILE_LAB = {"openai": "openai", "anthropic": "anthropic", "kimi": "moonshot", "deepseek": "deepseek", "glm": "glm"}
PRE_LAB = {"gpt": "openai", "o3": "openai", "claude": "anthropic", "kimi": "moonshot", "deepseek": "deepseek"}
SKIP = {"GPT-4o (alias gpt-4o)"}  # the same model as the GPT-4o 2024-05-13 row
MIN_CONTEXT = 128_000  # an office week has to fit

catalog = {m["id"]: m.get("context_length") or 0
           for m in json.load(open(root / "data/openrouter/models-2026-10-25.json"))["data"]}

rows = []
def add(lab, r):
    if not r.get("release_date"):
        return
    name = r["model"].strip()
    oid = r.get("openrouter_id") or OR_ID.get(name, "")
    rows.append({"lab": lab, "model": name, "date": dt.date.fromisoformat(r["release_date"]),
                 "main": name in MAIN[lab], "short": MAIN[lab].get(name, ""), "openrouter_id": oid,
                 "served": oid in catalog, "context": catalog.get(oid, 0), "kind": r.get("kind", ""),
                 "price_in": r.get("launch_input_usd_per_m", ""), "price_out": r.get("launch_output_usd_per_m", ""),
                 "confidence": r.get("confidence", "")})

for f, lab in FILE_LAB.items():
    for r in csv.DictReader(open(rel / f"{f}.tsv"), delimiter="\t"):
        add(lab, r)
pre = rel / "pre-window.tsv"
if pre.exists():
    seen = {(r["lab"], r["model"]) for r in rows}
    for r in csv.DictReader(open(pre), delimiter="\t"):
        lab = next((v for k, v in PRE_LAB.items() if r["family"].strip().lower().startswith(k)), None)
        if lab and r["model"].strip() not in SKIP and (lab, r["model"].strip()) not in seen:
            add(lab, r)

rows.sort(key=lambda r: (LABS.index(r["lab"]), r["date"]))

# Days since the lab's previous main-line release.
for lab in LABS:
    prev = None
    for r in [r for r in rows if r["lab"] == lab and r["main"]]:
        r["gap_days"] = (r["date"] - prev).days if prev else ""
        prev = r["date"]

# Quarter-end selection.
def quarter_ends(start, end):
    q = []
    y, m = start.year, ((start.month - 1) // 3 + 1) * 3
    while True:
        d = dt.date(y, m, 1)
        d = (d.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
        if d > end:
            return q
        q.append(d)
        m += 3
        if m > 12:
            y, m = y + 1, 3

def qlabel(d):
    return f"{d.year} Q{(d.month - 1) // 3 + 1}"

QUARTERS = quarter_ends(dt.date(2024, 4, 1), dt.date(2026, 9, 30))
picks = []  # (quarter end, lab, row)
for lab in LABS:
    main = [r for r in rows if r["lab"] == lab and r["main"] and r["served"] and r["context"] >= MIN_CONTEXT]
    for q in QUARTERS:
        cand = [r for r in main if r["date"] <= q]
        if cand:
            picks.append((q, lab, cand[-1]))
for r in rows:
    r["quarters"] = [qlabel(q) for q, _, p in picks if p is r]

with open(root / "data/releases/all.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["lab", "model", "release_date", "main_line", "days_since_previous_main", "openrouter_id",
                "on_openrouter", "benchmark_quarters", "launch_input_usd_per_m", "launch_output_usd_per_m", "confidence"])
    for r in rows:
        w.writerow([r["lab"], r["model"], r["date"], "yes" if r["main"] else "no", r.get("gap_days", ""),
                    r["openrouter_id"], "yes" if r["served"] else "no", " ".join(r["quarters"]),
                    r["price_in"], r["price_out"], r["confidence"]])

with open(root / "data/models-quarterly.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["quarter", "quarter_end", "lab", "line", "model", "openrouter_id", "release_date", "age_days_at_quarter_end"])
    for q, lab, r in sorted(picks, key=lambda p: (p[0], LABS.index(p[1]))):
        w.writerow([qlabel(q), q, lab, LINE_NAME[lab], r["model"], r["openrouter_id"], r["date"], (q - r["date"]).days])

# ---- chart ----
X0, X1 = dt.date(2024, 2, 1), dt.date(2026, 11, 15)
W, LEFT, RIGHT = 1240, 170, 30
LANE, TOP = 118, 70
H = TOP + LANE * len(LABS) + 46
def x(d):
    return LEFT + (d - X0).days / (X1 - X0).days * (W - LEFT - RIGHT)

svg = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">',
       '<title id="t">Model releases by lab, 2024 to 2026</title>',
       '<desc id="d">Each lab\'s releases on one time axis; the main line filled, other tiers hollow; the benchmark set larger.</desc>']
for q in QUARTERS + [dt.date(2024, 3, 31), dt.date(2023, 12, 31)]:
    if X0 <= q <= X1:
        svg.append(f'<line x1="{x(q):.1f}" x2="{x(q):.1f}" y1="{TOP - 10}" y2="{H - 40}" class="grid"/>')
for q in QUARTERS:
    mid = q - dt.timedelta(days=45)
    svg.append(f'<text x="{x(mid):.1f}" y="{H - 24}" class="tick" text-anchor="middle">Q{(q.month - 1) // 3 + 1}</text>')
for y in (2024, 2025, 2026):
    d = max(dt.date(y, 1, 1), X0)
    svg.append(f'<text x="{x(d) + 4:.1f}" y="{H - 8}" class="year">{y}</text>')
svg.append(f'<text x="{x(dt.date(2026, 10, 25)):.1f}" y="{TOP - 16}" class="tick" text-anchor="middle">today</text>')
svg.append(f'<line x1="{x(dt.date(2026, 10, 25)):.1f}" x2="{x(dt.date(2026, 10, 25)):.1f}" y1="{TOP - 10}" y2="{H - 40}" class="axis"/>')

for i, lab in enumerate(LABS):
    yc = TOP + LANE * i + 44
    svg.append(f'<text x="12" y="{yc + 4}" class="lab">{LAB_NAME[lab]}</text>')
    svg.append(f'<text x="12" y="{yc + 20}" class="sub">{html.escape(LINE_NAME[lab])}</text>')
    svg.append(f'<line x1="{LEFT}" x2="{W - RIGHT}" y1="{yc}" y2="{yc}" class="axis"/>')
    svg.append(f'<text x="{LEFT - 8}" y="{yc + 40}" class="sub" text-anchor="end">other tiers</text>')
    k = 0
    for r in [r for r in rows if r["lab"] == lab]:
        if r["date"] < X0:
            continue
        tip = html.escape(f'{r["model"]} | {r["date"]} | {"main line" if r["main"] else "other tier"}'
                          f'{" | not on OpenRouter" if not r["served"] else ""}'
                          f'{" | benchmark: " + ", ".join(r["quarters"]) if r["quarters"] else ""}'
                          f'{" | launch $" + r["price_in"] + " / $" + r["price_out"] + " per M" if r["price_in"] else ""}')
        cx = x(r["date"])
        if not r["main"]:
            svg.append(f'<g class="pt" data-tip="{tip}"><circle cx="{cx:.1f}" cy="{yc + 36}" r="12" class="hit"/>'
                       f'<circle cx="{cx:.1f}" cy="{yc + 36}" r="3" class="other"/></g>')
            continue
        sel = bool(r["quarters"])
        cls = "sel" if sel else ("main" if r["served"] and r["context"] >= MIN_CONTEXT else "gone")
        rad = 6 if sel else 4.5
        ly = yc - 13 if k % 2 == 0 else yc + 21
        k += 1
        svg.append(f'<g class="pt" data-tip="{tip}"><circle cx="{cx:.1f}" cy="{yc}" r="14" class="hit"/>'
                   f'<circle cx="{cx:.1f}" cy="{yc}" r="{rad}" class="{cls}"/></g>')
        svg.append(f'<text x="{cx:.1f}" y="{ly}" text-anchor="middle" class="{"lbl-sel" if sel else "lbl"}">'
                   f'{html.escape(r["short"])}</text>')
svg.append("</svg>")

table = ["<table><thead><tr><th>Lab</th><th>Model</th><th>Released</th><th>Line</th><th>Days since previous</th>"
         "<th>Benchmark quarters</th><th>On OpenRouter</th><th>Launch $/M in / out</th></tr></thead><tbody>"]
for r in rows:
    table.append(f'<tr><td>{LAB_NAME[r["lab"]]}</td><td>{html.escape(r["model"])}</td><td>{r["date"]}</td>'
                 f'<td>{"main" if r["main"] else "other"}</td><td class="n">{r.get("gap_days", "")}</td>'
                 f'<td>{", ".join(r["quarters"])}</td><td>{"yes" if r["served"] else "no"}</td>'
                 f'<td class="n">{r["price_in"]}{" / " + r["price_out"] if r["price_in"] else ""}</td></tr>')
table.append("</tbody></table>")

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Model releases</title>
<style>
.viz-root {{ color-scheme: light; --surface-1:#fcfcfb; --page:#f9f9f7; --text-primary:#0b0b0b; --text-secondary:#52514e;
  --muted:#898781; --grid:#e1e0d9; --axis:#c3c2b7; --series-1:#2a78d6; --series-2:#eb6834; --border:rgba(11,11,11,0.10); }}
@media (prefers-color-scheme: dark) {{ :root:where(:not([data-theme="light"])) .viz-root {{ color-scheme: dark;
  --surface-1:#1a1a19; --page:#0d0d0d; --text-primary:#f0efec; --text-secondary:#c3c2b7; --grid:#2c2c2a; --axis:#383835;
  --series-1:#3987e5; --series-2:#d95926; --border:rgba(255,255,255,0.10); }} }}
body {{ margin:0; background:var(--page); font-family:system-ui,-apple-system,"Segoe UI",sans-serif; }}
.viz-root {{ background:var(--page); color:var(--text-primary); padding:24px; }}
.card {{ background:var(--surface-1); border:1px solid var(--border); border-radius:8px; padding:20px 20px 8px; max-width:{W}px; }}
h1 {{ font-size:18px; font-weight:600; margin:0 0 4px; }} p.sub {{ margin:0 0 12px; color:var(--text-secondary); font-size:13px; }}
.legend {{ display:flex; gap:20px; font-size:12px; color:var(--text-secondary); margin:0 0 4px; }}
.legend span {{ display:inline-flex; align-items:center; gap:6px; }}
.sw {{ width:10px; height:10px; border-radius:50%; display:inline-block; }}
svg text {{ font-family:inherit; }}
.grid {{ stroke:var(--grid); stroke-width:1; }} .axis {{ stroke:var(--axis); stroke-width:1; }}
.tick {{ fill:var(--muted); font-size:11px; }} .year {{ fill:var(--text-secondary); font-size:11px; font-weight:600; }}
.lab {{ fill:var(--text-primary); font-size:13px; font-weight:600; }} .sub {{ fill:var(--muted); font-size:11px; }}
.sel {{ fill:var(--series-2); stroke:var(--surface-1); stroke-width:2; }}
.main {{ fill:var(--series-1); stroke:var(--surface-1); stroke-width:2; }}
.gone {{ fill:var(--surface-1); stroke:var(--series-1); stroke-width:1.5; }}
.other {{ fill:none; stroke:var(--muted); stroke-width:1.2; }}
.hit {{ fill:transparent; }} .pt:hover circle:not(.hit), .pt:focus circle:not(.hit) {{ stroke:var(--text-primary); }}
.lbl {{ fill:var(--text-secondary); font-size:10.5px; }} .lbl-sel {{ fill:var(--text-primary); font-size:11px; font-weight:600; }}
#tip {{ position:fixed; pointer-events:none; background:var(--surface-1); color:var(--text-primary); border:1px solid var(--border);
  border-radius:6px; padding:6px 8px; font-size:12px; display:none; max-width:360px; box-shadow:0 2px 8px rgba(0,0,0,.08); }}
table {{ border-collapse:collapse; font-size:12px; margin-top:20px; background:var(--surface-1); }}
th, td {{ text-align:left; padding:4px 10px; border-bottom:1px solid var(--grid); }} td.n {{ font-variant-numeric:tabular-nums; }}
th {{ color:var(--text-secondary); font-weight:600; }} details {{ margin-top:16px; color:var(--text-secondary); font-size:13px; }}
</style></head><body><div class="viz-root">
<div class="card"><h1>Model releases by lab, 2024 to 2026</h1>
<p class="sub">Each lab's main line on its lane; other tiers below it. Larger orange dots: the benchmark set, the newest
main-line model OpenRouter serves at each quarter's end. Vertical rules are quarter ends.</p>
<div class="legend"><span><i class="sw" style="background:var(--series-2)"></i>Benchmark set</span>
<span><i class="sw" style="background:var(--series-1)"></i>Main line, not selected</span>
<span><i class="sw" style="border:1.5px solid var(--series-1)"></i>Main line, not servable (retired, or context under 128k)</span>
<span><i class="sw" style="border:1.2px solid var(--muted)"></i>Other tier</span></div>
{''.join(svg)}</div>
<details><summary>Table view</summary>{''.join(table)}</details>
<div id="tip"></div></div>
<script>
const tip=document.getElementById('tip');
document.querySelectorAll('.pt').forEach(g=>{{ g.setAttribute('tabindex','0');
  const show=e=>{{ tip.textContent=g.dataset.tip; tip.style.display='block';
    const r=g.getBoundingClientRect(); tip.style.left=Math.min(r.left, innerWidth-380)+'px'; tip.style.top=(r.bottom+6)+'px'; }};
  g.addEventListener('mouseenter',show); g.addEventListener('focus',show);
  g.addEventListener('mouseleave',()=>tip.style.display='none'); g.addEventListener('blur',()=>tip.style.display='none'); }});
</script></body></html>"""
(root / "docs").mkdir(exist_ok=True)
(root / "docs/model-timeline.html").write_text(page)
print(len(rows), "releases;", len({id(p[2]) for p in picks}), "benchmark models over", len(QUARTERS), "quarters")
