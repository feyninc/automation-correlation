"""Offline grading of a run: code checks, the judge panel, edit effort, value.

    uv run python -m workweek.grade logs/<run> [--judges all|name,name] [--out results/<run>]

For each sample (one model on one profession): every proposal is matched against the needs and traps with the shared
check evaluator, graded by the judges, and valued; need outcomes and per-model summaries are written as JSONL and CSV.
"""
from __future__ import annotations

import argparse
import asyncio
import csv
import json
import re
from pathlib import Path

from inspect_ai.log import list_eval_logs, read_eval_log
from inspect_ai.model import ChatMessageUser, GenerateConfig, get_model

from . import checks, config as cfgmod, creds, prompts, providers  # noqa: F401
from .apps import document_file, render_world, thread_file
from .engine import ROOT, load_episode
from .schema import Episode, fmt, seconds

PROPOSALS_IN_FLIGHT = 8     # proposals judged at once (each by the whole panel)

# ---------- matching proposals to the world ----------


def path_index(ep: Episode) -> dict[str, tuple[str, str, str]]:
    """Sandbox file -> (app, path, id)."""
    idx = {}
    for t in ep.threads:
        idx[thread_file(t)] = (t.app, t.path, t.id)
    for d in ep.documents:
        idx[document_file(d)] = (d.app, d.path, d.id)
    return idx


def people(ep: Episode, text: str) -> list[str]:
    """Contact ids named in a free-text recipient field (by email, or by full name)."""
    text = (text or "").lower()
    out = []
    if ep.worker.email.lower() in text or ep.worker.name.lower() in text:
        out.append("worker")
    for c in ep.contacts:
        if (c.email and c.email.lower() in text) or c.name.lower() in text:
            out.append(c.id)
    return out


def to_prop(ep: Episode, idx, p: dict) -> checks.Prop:
    app, path, tid = idx.get(p["target"], ("", "", ""))
    drafts = [checks.Draft(text=str(d.get("text", "")), to=people(ep, d.get("to", "")), cc=people(ep, d.get("cc", "")),
                           subject=str(d.get("subject", "") or "")) for d in p["drafts"]]
    return checks.Prop(t=seconds(p["t"]), app=app, path=path, target=tid, action=checks.normalize_action(app, p["action"]),
                       drafts=drafts)


def outcomes(ep: Episode, props: list[checks.Prop]) -> tuple[list[dict], list[dict], dict[int, str]]:
    """Need outcomes (caught in window?), trap firings, and which need each proposal addresses."""
    addressed: dict[int, str] = {}
    needs = []
    for n in ep.needs:
        a, b = seconds(n.discoverable_at), seconds(n.deadline)
        hit = None
        for i, p in enumerate(props):
            if a <= p.t <= b and checks.matches(n.check, p) is not None:
                hit = i
                break
        if hit is not None:
            addressed.setdefault(hit, n.id)
        ref_t = None
        if n.reference.exchange_id:
            ref_t = next((seconds(x.at) for t in ep.threads for x in t.exchanges if x.id == n.reference.exchange_id), None)
        needs.append({"need": n.id, "task": n.onet_task_id, "caught": hit is not None, "proposal": hit,
                      "lead_minutes": (ref_t - props[hit].t) / 60 if hit is not None and ref_t is not None else None,
                      "worker_does_it": ref_t is not None})
    traps = []
    for tr in ep.traps:
        fired = [i for i, p in enumerate(props) if checks.matches(tr.check, p) is not None]
        traps.append({"trap": tr.id, "fired": bool(fired), "proposals": fired})
    return needs, traps, addressed


# ---------- judges ----------


CONTEXT_CHARS = 30000     # judge context budget
FILE_CHARS = 6000         # per file; longer files keep their head and the lines sharing an identifier with the drafts


def _excerpt(text: str, keys: set[str]) -> str:
    if len(text) <= FILE_CHARS:
        return text
    head, rest = text[:1500], text[1500:].splitlines()
    hits = [ln for ln in rest if keys & set(re.findall(r"[\w@.#-]*\d[\w@.#-]*", ln))]
    return head + "\n[... lines matching the drafts' identifiers:]\n" + "\n".join(hits)[:FILE_CHARS - 1500]


def _context(ep: Episode, p: dict, t: int, need) -> str:
    """What the assistant could see, as of the proposal: the target, the need's evidence, the files it read."""
    files = render_world(ep, t)
    keys = {k for d in p["drafts"] for k in re.findall(r"[\w@.#-]*\d[\w@.#-]*", " ".join(str(v) for v in d.values()))
            if len(k) >= 3}
    paths = [p["target"]]
    for e in (need.evidence if need else []):
        paths += [thread_file(th) for th in ep.threads if th.id == e or any(x.id == e for x in th.exchanges)]
        paths += [document_file(d) for d in ep.documents if d.id == e]
    paths += reversed(p.get("read", []))
    parts, used, seen = [], 0, set()
    for path in paths:
        f = files.get(path)
        if not f or path in seen or path.endswith(".xlsx"):
            continue
        seen.add(path)
        block = f"### {path}\n" + _excerpt(f.data.decode(errors="replace"), keys)
        if used + len(block) > CONTEXT_CHARS:
            continue
        parts.append(block)
        used += len(block)
    world = " ".join(f.data.decode(errors="replace") for f in files.values()) + " " + " ".join(
        x.body for th in ep.threads for x in th.exchanges if seconds(x.at) <= t)
    unseen = sorted(k for k in keys if k.strip(".-") and k.strip(".-") not in world)
    note = ("\n\nIdentifiers and numbers in the drafts found nowhere in the world at this time (they may be computed, "
            "or invented): " + ", ".join(unseen[:40])) if unseen else ""
    return ("\n\n".join(parts) or "(no file context)") + note


def judge_prompt(ep: Episode, p: dict, need) -> str:
    t = seconds(p["t"])
    drafts = "\n".join(f"### Draft {i + 1}: {d.get('label', '')}\nTo: {d.get('to', '')}  Cc: {d.get('cc', '')}  "
                       f"Subject: {d.get('subject', '')}\n{d.get('text', '')}" for i, d in enumerate(p["drafts"]))
    rubric = ""
    if need:
        ref = ""
        if need.reference.exchange_id:
            x = next((x for th in ep.threads for x in th.exchanges if x.id == need.reference.exchange_id), None)
            ref = f"What {ep.worker.name.split()[0]} actually did (for reference; other good versions exist):\n{x.body}" if x else ""
        elif need.reference.text:
            ref = f"A good version (for reference; other good versions exist):\n{need.reference.text}"
        rubric = prompts.RUBRIC.format(title=need.title, must="; ".join(need.rubric.must),
                                       must_not="; ".join(need.rubric.must_not) or "(none)", reference=ref)
    return prompts.JUDGE.format(worker_name=ep.worker.name, worker_title=ep.worker.title, employer=ep.employer.name,
                                first_name=ep.worker.name.split()[0], when=fmt(t),
                                profession_prompt=ep.profession_prompt, rubric_block=rubric,
                                context=_context(ep, p, t, need), target=p["target"], action=p["action"], drafts=drafts)


def parse_judgement(text: str) -> dict | None:
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        return None
    try:
        j = json.loads(m.group(0))
    except ValueError:
        return None
    try:
        j["score"] = max(0.0, min(100.0, float(j.get("score", 0))))
        j["best_draft"] = int(j.get("best_draft", 1) or 1)
    except (TypeError, ValueError):
        return None
    j["harm"] = bool(j.get("harm", False))
    j["minimal_fix"] = str(j.get("minimal_fix", "") or "")
    j["reasons"] = [str(r)[:220] for r in (j.get("reasons") or [])][:2]
    return j


async def judge_all(run: cfgmod.RunConfig, judges, prompt: str) -> dict[str, dict]:
    async def one(j):
        model = get_model(j.model, config=GenerateConfig(**{**run.generate_for(j), "max_tokens": 16000}), **j.model_args)
        for _ in range(2):
            out = await model.generate([ChatMessageUser(content=prompt)])
            parsed = parse_judgement(out.completion)
            if parsed:
                parsed["usage"] = out.usage.model_dump() if out.usage else None
                return j.name, parsed
        return j.name, {"error": "unparseable", "raw": (out.completion or "")[:500]}
    return dict(await asyncio.gather(*(one(j) for j in judges)))


def panel(run: cfgmod.RunConfig, judgements: dict[str, dict], tested_family: str) -> dict:
    ok = {j.name: (j, judgements[j.name]) for j in run.judges if j.name in judgements and "score" in judgements[j.name]}

    def mean(items):
        w = sum(j.weight for j, _ in items)
        return sum(j.weight * r["score"] for j, r in items) / w if w else None

    full = list(ok.values())
    drop = [(j, r) for j, r in full if not (j.report_with_dropout and j.family == tested_family)]
    scores = sorted(r["score"] for _, r in full)
    median = scores[len(scores) // 2] if scores else None
    return {"score": mean(drop), "score_all": mean(full), "median_all": median,
            "harm": sum(j.weight for j, r in drop if r["harm"]) / max(sum(j.weight for j, _ in drop), 1e-9) >= 0.5}


def fix_judge(run: cfgmod.RunConfig, judgements: dict[str, dict], tested_family: str) -> dict:
    """The judgement whose best draft and minimal fix set the edit effort: the heaviest judge left after dropout."""
    ok = [(j, judgements[j.name]) for j in run.judges if "score" in judgements.get(j.name, {})
          and not (j.report_with_dropout and j.family == tested_family)]
    return max(ok, key=lambda x: x[0].weight)[1] if ok else {}


# ---------- edit effort and value ----------


def word_edits(a: str, b: str) -> int:
    """Word-level edit distance (insertions, deletions, substitutions); the HTER count without block shifts."""
    x, y = a.split(), b.split()
    prev = list(range(len(y) + 1))
    for i, wx in enumerate(x, 1):
        cur = [i] + [0] * len(y)
        for k, wy in enumerate(y, 1):
            cur[k] = min(prev[k] + 1, cur[k - 1] + 1, prev[k - 1] + (wx != wy))
        prev = cur
    return prev[-1]


def value(ep: Episode, p: dict, j: dict | None, need, price, usage: dict | None) -> dict:
    mm = ep.economics.minutes_model
    wage_min = ep.economics.loaded_hourly / 60
    words_all = sum(len(str(d.get("text", "")).split()) for d in p["drafts"])
    read_min = words_all / mm.read_wpm
    best = p["drafts"][max(1, min(len(p["drafts"]), (j or {}).get("best_draft", 1))) - 1] if p["drafts"] else {}
    best_text = str(best.get("text", ""))
    score = (j or {}).get("score")
    fix_min = 0.0
    edits = 0
    if j and j.get("minimal_fix"):
        edits = word_edits(best_text, j["minimal_fix"])
        rate = edits / max(len(j["minimal_fix"].split()), 1)
        write_min = len(j["minimal_fix"].split()) / mm.compose_wpm
        fix_min = write_min if rate > mm.rewrite_threshold else min(write_min, edits / mm.compose_wpm * mm.friction)
    do_min = need.minutes.do if need else 0.0
    p_acc = (score or 0) / 100
    minutes_saved = do_min * p_acc - read_min - (1 - p_acc) * fix_min if need else -read_min
    tok_cost = price.cost(usage) if usage and price else 0.0
    return {"read_min": round(read_min, 3), "fix_min": round(fix_min, 3), "edits": edits, "do_min": do_min,
            "minutes_saved": round(minutes_saved, 3), "value_usd": round(minutes_saved * wage_min - tok_cost, 4),
            "token_cost_usd_share": round(tok_cost, 5)}


# ---------- driver ----------


async def grade_log(log_path: str, run: cfgmod.RunConfig, judges, out_dir: Path) -> list[dict]:
    log = read_eval_log(log_path)
    model_name = log.eval.model
    spec = next((m for m in run.models if m.model == model_name or model_name.endswith(m.model.split("/", 1)[-1])), None)
    family = spec.family if spec else ""
    rows = []
    for s in log.samples or []:
        ep = load_episode(ROOT / s.metadata["episode"])
        idx = path_index(ep)
        props_raw = s.metadata.get("proposals", [])
        props = [to_prop(ep, idx, p) for p in props_raw]
        needs, traps, addressed = outcomes(ep, props)
        u = (s.model_usage or {}).get(model_name)     # the tested model only, not the simulated worker
        usage = u.model_dump() if u else None
        n_props = max(len(props_raw), 1)
        share = {k: (v / n_props if isinstance(v, (int, float)) else v) for k, v in (usage or {}).items()}
        gate = asyncio.Semaphore(PROPOSALS_IN_FLIGHT)

        async def grade_one(i, p):
            need = next((n for n in ep.needs if n.id == addressed.get(i)), None)
            async with gate:
                js = await judge_all(run, judges, judge_prompt(ep, p, need)) if judges else {}
            pn = panel(run, js, family) if js else {"score": None}
            lead = fix_judge(run, js, family)
            j_for_value = {"score": pn["score"], "best_draft": lead.get("best_draft", 1),
                           "minimal_fix": lead.get("minimal_fix", "")} if js else None
            v = value(ep, p, j_for_value, need, spec.price if spec else None, share)
            return {"model": spec.name if spec else model_name, "profession": s.id, "epoch": s.epoch,
                    "proposal": p, "need": need.id if need else None, "panel": pn, "judges": js, "value": v}
        graded = list(await asyncio.gather(*(grade_one(i, p) for i, p in enumerate(props_raw))))
        tot_cost = spec.price.cost(usage) if usage and spec and spec.price else 0.0
        mm = ep.economics.minutes_model
        qs = s.metadata.get("questions", [])
        q_min = sum(len(q["question"].split()) / mm.read_wpm + mm.question_answer_s / 60 for q in qs)
        rows.append({"model": spec.name if spec else model_name, "profession": s.id, "epoch": s.epoch,
                     "ticks": s.metadata.get("ticks"), "proposals": len(props_raw),
                     "questions": len(qs), "questions_cost_usd": round(q_min * ep.economics.loaded_hourly / 60, 4),
                     "recovered_tool_calls": s.metadata.get("recovered_tool_calls", 0), "needs": needs, "traps": traps,
                     "graded": graded, "usage": usage, "token_cost_usd": round(tot_cost, 4)})
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "graded.jsonl", "a") as f:
        for r in rows:
            f.write(json.dumps(r, default=str) + "\n")
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logs")
    ap.add_argument("--judges", default="all")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    creds.load()
    run = cfgmod.load(ROOT / "config/run.yaml")
    judges = [] if a.judges == "none" else [j for j in run.judges if a.judges == "all" or j.name in a.judges.split(",")]
    out = Path(a.out or ROOT / "results" / Path(a.logs).name)
    if (out / "graded.jsonl").exists():
        (out / "graded.jsonl").unlink()
    logs = [l.name for l in list_eval_logs(a.logs)]
    summary = []
    for lp in logs:
        for r in asyncio.run(grade_log(lp, run, judges, out)):
            sc = [g["panel"]["score"] for g in r["graded"] if g["panel"].get("score") is not None]
            summary.append({"model": r["model"], "profession": r["profession"], "epoch": r["epoch"], "ticks": r["ticks"],
                            "proposals": r["proposals"], "questions": r["questions"],
                            "needs_caught": sum(n["caught"] for n in r["needs"]), "needs": len(r["needs"]),
                            "traps_fired": sum(t["fired"] for t in r["traps"]),
                            "press_enter": round(sum(sc) / len(sc) / 100, 3) if sc else "",
                            "value_usd": round(sum(g["value"]["value_usd"] for g in r["graded"])
                                               - r["questions_cost_usd"], 2),
                            "token_cost_usd": r["token_cost_usd"]})
    with open(out / "summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0]) if summary else ["model"])
        w.writeheader()
        w.writerows(summary)
    for s in summary:
        print(s)


if __name__ == "__main__":
    main()
