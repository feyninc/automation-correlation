"""Main-line releases from 2026 Q1: the clean timeline and the candidate model set.

Reads data/releases/all.csv (written by scripts/timeline.py) and writes data/models.csv and
docs/model-timeline-2026.html.

    python3 -I scripts/timeline_2026.py <project root>
"""
import csv, datetime as dt, html, sys
from pathlib import Path

root = Path(sys.argv[1])
START, END, TODAY = dt.date(2026, 1, 1), dt.date(2026, 11, 10), dt.date(2026, 10, 25)
LABS = [("openai", "OpenAI", "GPT, Sol from 5.6"), ("anthropic", "Anthropic", "Opus"),
        ("moonshot", "Moonshot", "Kimi K"), ("deepseek", "DeepSeek", "Flash")]
NAME = {"GPT-5.2 (Thinking)": "GPT-5.2", "GPT-5.4 (Thinking)": "GPT-5.4", "GPT-5.5 (Thinking)": "GPT-5.5",
        "DeepSeek-V3.2": "V3.2", "DeepSeek-V4-Flash (Preview)": "V4 Flash", "DeepSeek-V4-Flash-0731": "V4 Flash 0731",
        "DeepSeek-V4.1-Flash": "V4.1 Flash", "DeepSeek-V4.1-Flash-1017": "V4.1 Flash 1017"}
def short(m):
    return NAME.get(m, m.replace("Claude ", "").replace("Kimi ", ""))

# In-place updates (same API name and price), kept because DeepSeek reports large agentic gains for them
# (Hugging Face model card for 0731, the Change Log for 1017).
UPDATE = {"DeepSeek-V4-Flash-0731", "DeepSeek-V4.1-Flash-1017"}
rows = [r for r in csv.DictReader(open(root / "data/releases/all.csv")) if r["main_line"] == "yes"]
for r in rows:
    r["date"] = dt.date.fromisoformat(r["release_date"])
lanes = {}
for lab, _, _ in LABS:
    mine = sorted((r for r in rows if r["lab"] == lab), key=lambda r: r["date"])
    before = [r for r in mine if r["date"] < START]
    # The set: the model in force on January 1, then every release since.
    lanes[lab] = (before[-2] if len(before) > 1 else None, before[-1:] + [r for r in mine if r["date"] >= START])

with open(root / "data/models.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["lab", "model", "release_date", "role", "days_since_previous", "previous", "openrouter_id",
                "launch_input_usd_per_m", "launch_output_usd_per_m"])
    for lab, _, _ in LABS:
        prev, rel = lanes[lab]
        for r in rel:
            role = "in force 2026-01-01" if r["date"] < START else ("in-place update" if r["model"] in UPDATE else "release")
            w.writerow([lab, r["model"], r["date"], role, (r["date"] - prev["date"]).days if prev else "",
                        prev["model"] if prev else "", r["openrouter_id"],
                        r["launch_input_usd_per_m"], r["launch_output_usd_per_m"]])
            prev = r

W, LEFT, RIGHT, TOP, LANE = 1240, 190, 40, 40, 132
H = TOP + LANE * len(LABS) + 40
def x(d):
    return LEFT + (d - START).days / (END - START).days * (W - LEFT - RIGHT)

s = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">',
     '<title id="t">Main-line model releases by lab, 2026</title>']
months = [dt.date(2026, m, 1) for m in range(1, 12)]
for m in months:
    s.append(f'<line x1="{x(m):.1f}" x2="{x(m):.1f}" y1="{TOP - 8}" y2="{H - 34}" class="{"q" if m.month in (1, 4, 7, 10) else "grid"}"/>')
    mid = m + dt.timedelta(days=15)
    if mid < END:
        s.append(f'<text x="{x(mid):.1f}" y="{H - 16}" class="tick" text-anchor="middle">{m.strftime("%b")}</text>')
for qd, ql in ((dt.date(2026, 1, 1), "Q1"), (dt.date(2026, 4, 1), "Q2"), (dt.date(2026, 7, 1), "Q3"), (dt.date(2026, 10, 1), "Q4")):
    s.append(f'<text x="{x(qd) + 4:.1f}" y="{TOP - 14}" class="qlab">{ql}</text>')
s.append(f'<line x1="{x(TODAY):.1f}" x2="{x(TODAY):.1f}" y1="{TOP - 8}" y2="{H - 34}" class="today"/>')
s.append(f'<text x="{x(TODAY) + 4:.1f}" y="{H - 38}" class="tick">today</text>')

for i, (lab, title, line) in enumerate(LABS):
    yc = TOP + LANE * i + 70
    prev, rel = lanes[lab]
    s.append(f'<text x="14" y="{yc - 6}" class="lab">{title}</text>')
    s.append(f'<text x="14" y="{yc + 10}" class="sub">{line}</text>')
    s.append(f'<line x1="{LEFT}" x2="{x(TODAY):.1f}" y1="{yc}" y2="{yc}" class="axis"/>')
    last_x, below = None, False
    for j, r in enumerate(rel):
        cx = x(max(r["date"], START))
        gap = (r["date"] - (rel[j - 1]["date"] if j else prev["date"])).days if (j or prev) else None
        close = last_x is not None and cx - last_x < 70
        below = close and not below
        if j and not close:
            s.append(f'<text x="{(last_x + cx) / 2:.1f}" y="{yc + 16}" class="gap" text-anchor="middle">{gap} d</text>')
        if r["date"] < START:
            ny, dy = yc + 32, yc + 46
        elif below:
            ny, dy = yc + 26, yc + 40
        else:
            ny, dy = yc - 26, yc - 12
        tip = html.escape(f'{r["model"]} | released {r["date"]} | {gap} days after the previous'
                          + (f' | launch ${r["launch_input_usd_per_m"]} / ${r["launch_output_usd_per_m"]} per M'
                             if r["launch_input_usd_per_m"] else ""))
        s.append(f'<g class="pt" data-tip="{tip}"><circle cx="{cx:.1f}" cy="{yc}" r="14" class="hit"/>'
                 f'<circle cx="{cx:.1f}" cy="{yc}" r="5.5" class="{"inforce" if r["date"] < START else "dot"}"/></g>')
        s.append(f'<text x="{cx - (6 if r["date"] < START else 0):.1f}" y="{ny}" class="name" '
                 f'text-anchor="{"start" if r["date"] < START else "middle"}">{html.escape(short(r["model"]))}</text>')
        when = r["date"].strftime("%b %-d") + (", 2025" if r["date"] < START else "")
        when += " (update)" if r["model"] in UPDATE else ""
        anchor = "start" if r["date"] < START else "middle"
        s.append(f'<text x="{cx - (6 if anchor == "start" else 0):.1f}" y="{dy}" class="date" text-anchor="{anchor}">{when}</text>')
        last_x = cx
s.append("</svg>")

table = ['<table><thead><tr><th>Lab</th><th>Model</th><th>Released</th><th>Days since previous</th>'
         '<th>Launch $/M in / out</th></tr></thead><tbody>']
for lab, title, _ in LABS:
    prev, rel = lanes[lab]
    for r in rel:
        table.append(f'<tr><td>{title}</td><td>{html.escape(r["model"])}</td><td>{r["date"]}</td>'
                     f'<td class="n">{(r["date"] - prev["date"]).days if prev else ""}</td>'
                     f'<td class="n">{r["launch_input_usd_per_m"]} / {r["launch_output_usd_per_m"]}</td></tr>')
        prev = r
table.append("</tbody></table>")

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Main-line releases, 2026</title><style>
.viz-root {{ color-scheme: light; --surface-1:#fcfcfb; --page:#f9f9f7; --text-primary:#0b0b0b; --text-secondary:#52514e;
  --muted:#898781; --grid:#e1e0d9; --axis:#c3c2b7; --series-1:#2a78d6; --border:rgba(11,11,11,0.10); }}
@media (prefers-color-scheme: dark) {{ :root:where(:not([data-theme="light"])) .viz-root {{ color-scheme: dark;
  --surface-1:#1a1a19; --page:#0d0d0d; --text-primary:#f0efec; --text-secondary:#c3c2b7; --grid:#2c2c2a; --axis:#383835;
  --series-1:#3987e5; --border:rgba(255,255,255,0.10); }} }}
body {{ margin:0; background:var(--page); font-family:system-ui,-apple-system,"Segoe UI",sans-serif; }}
.viz-root {{ background:var(--page); color:var(--text-primary); padding:24px; }}
.card {{ background:var(--surface-1); border:1px solid var(--border); border-radius:8px; padding:20px 20px 8px; max-width:{W}px; }}
h1 {{ font-size:18px; font-weight:600; margin:0 0 4px; }} p.sub {{ margin:0 0 8px; color:var(--text-secondary); font-size:13px; }}
svg text {{ font-family:inherit; }} .grid {{ stroke:var(--grid); stroke-width:1; }} .q {{ stroke:var(--axis); stroke-width:1; }}
.axis {{ stroke:var(--axis); stroke-width:1; }} .today {{ stroke:var(--text-secondary); stroke-width:1; }}
.tick {{ fill:var(--muted); font-size:11px; }} .qlab {{ fill:var(--text-secondary); font-size:11px; font-weight:600; }}
.lab {{ fill:var(--text-primary); font-size:14px; font-weight:600; }} .sub {{ fill:var(--muted); font-size:11px; }}
.dot {{ fill:var(--series-1); stroke:var(--surface-1); stroke-width:2; }} .hit {{ fill:transparent; }}
.inforce {{ fill:var(--surface-1); stroke:var(--series-1); stroke-width:2.5; }}
.upd {{ fill:var(--surface-1); stroke:var(--muted); stroke-width:1.5; }}
.pt:hover .dot, .pt:focus .dot {{ stroke:var(--text-primary); }}
.name {{ fill:var(--text-primary); font-size:12px; font-weight:600; }} .date {{ fill:var(--text-secondary); font-size:11px; }}
.name, .date {{ paint-order:stroke; stroke:var(--surface-1); stroke-width:4px; stroke-linejoin:round; }}
.gap {{ fill:var(--muted); font-size:10.5px; font-variant-numeric:tabular-nums; }}
#tip {{ position:fixed; pointer-events:none; background:var(--surface-1); color:var(--text-primary); border:1px solid var(--border);
  border-radius:6px; padding:6px 8px; font-size:12px; display:none; max-width:380px; }}
table {{ border-collapse:collapse; font-size:12px; margin-top:12px; background:var(--surface-1); }}
th, td {{ text-align:left; padding:4px 10px; border-bottom:1px solid var(--grid); }} td.n {{ font-variant-numeric:tabular-nums; }}
th {{ color:var(--text-secondary); font-weight:600; }} details {{ margin-top:16px; color:var(--text-secondary); font-size:13px; }}
</style></head><body><div class="viz-root"><div class="card">
<h1>Main-line model releases by lab, 2026</h1>
<p class="sub">Each lab's main line: the model in force on January 1 (ring, labelled below), then every release since,
with the days between them.
DeepSeek's two in-place updates are included for their reported agentic gains.
Release dates are first public availability, from each lab's own announcements.</p>
{''.join(s)}</div><details><summary>Table view</summary>{''.join(table)}</details><div id="tip"></div></div>
<script>const tip=document.getElementById('tip');
document.querySelectorAll('.pt').forEach(g=>{{ g.setAttribute('tabindex','0');
 const show=()=>{{ tip.textContent=g.dataset.tip; tip.style.display='block'; const r=g.getBoundingClientRect();
  tip.style.left=Math.min(r.left, innerWidth-400)+'px'; tip.style.top=(r.bottom+6)+'px'; }};
 g.addEventListener('mouseenter',show); g.addEventListener('focus',show);
 g.addEventListener('mouseleave',()=>tip.style.display='none'); g.addEventListener('blur',()=>tip.style.display='none'); }});
</script></body></html>"""
(root / "docs/model-timeline-2026.html").write_text(page)
print(sum(len(v[1]) for v in lanes.values()), "releases since", START)
