"""Offline grading of a run: code checks, the judge panel, edit effort, value.

    uv run python -m workweek.grade logs/<run> [--judges all|name,name] [--out results/<run>]

For each sample (one model on one profession): every proposal is matched against the needs and traps with the shared
check evaluator, graded by the judges, and valued; need outcomes and per-model summaries are written as JSONL and CSV.
"""
from __future__ import annotations

import argparse
import asyncio
import csv
import difflib
import json
import re
from pathlib import Path

from inspect_ai.log import list_eval_logs, read_eval_log
from inspect_ai.model import ChatMessageSystem, ChatMessageUser, GenerateConfig, get_model

from . import checks, config as cfgmod, creds, prompts, providers  # noqa: F401
from .apps import document_file, render_world, thread_file
from .engine import ROOT, load_episode
from .schema import Episode, seconds, show

PROPOSALS_IN_FLIGHT = 16    # proposals judged at once across all logs (each by the whole panel)

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


def speeds(run: cfgmod.RunConfig) -> dict[str, tuple[float, float]]:
    """Model name -> (p50 seconds to first token, p50 output tokens a second), from the run's speed file."""
    if not run.run.speed_file:
        return {}
    out = {}
    for r in csv.DictReader(open(ROOT / run.run.speed_file)):
        if r.get("ttft_p50_s") and r.get("tps_p50"):
            out[r["name"]] = (float(r["ttft_p50_s"]), float(r["tps_p50"]))
    return out


def call_timing(ep: Episode, p: dict, speed: tuple[float, float] | None) -> dict | None:
    """Would a line proposed on a call have reached the worker in time? Computed offline: the model's output tokens for
    the turn at its p50 speed, plus its tool time, plus the worker reading the line's first words, against the
    caller's patience (strict: from the end of the caller's line) and against the caller's line plus patience
    (streaming: as if the assistant heard the line as it was spoken)."""
    w = p.get("work") or {}
    if p["action"] != "say" or not w.get("answers"):
        return None
    x = next((x for th in ep.threads for x in th.exchanges if x.id == w["answers"]), None)
    mm = ep.economics.minutes_model
    read_s = min(len(str(p["drafts"][0].get("text", "")).split()), mm.call_read_words) / mm.read_wpm * 60
    patience = (x.meta.get("patience_s") if x else None) or w.get("patience_s") or 5
    speaking = len(x.body.split()) / 150 * 60 if x else 0.0
    if not speed:
        return {"latency_s": None, "read_s": round(read_s, 2), "patience_s": patience, "on_time": None,
                "on_time_streaming": None}
    ttft, tps = speed
    latency = sum(ttft + n / tps for n in w["output_tokens"]) + w.get("tool_s", 0.0)
    return {"latency_s": round(latency, 2), "read_s": round(read_s, 2), "patience_s": patience,
            "on_time": latency + read_s <= patience, "on_time_streaming": latency + read_s <= speaking + patience}


def outcomes(ep: Episode, props: list[checks.Prop], late: set[int] = frozenset()) -> tuple[
        list[dict], list[dict], dict[int, list[str]], dict[int, list[str]]]:
    """Need outcomes, trap firings, the needs each proposal earns, and the needs each proposal matches.

    A need is earned by the last proposal that matches it inside its window: later versions supersede earlier ones,
    as the worker would send the latest. One proposal can earn several needs (docs/design.md, section 6). A call line
    that would have arrived too late (`late`) earns nothing; traps still fire on it, as they measure what was proposed.
    """
    earned: dict[int, list[str]] = {}
    matched: dict[int, list[str]] = {}
    needs = []
    for n in ep.needs:
        a, b = seconds(n.discoverable_at), seconds(n.deadline)
        hits = [i for i, p in enumerate(props)
                if i not in late and a <= p.t <= b and checks.matches(n.check, p) is not None]
        for i in hits:
            matched.setdefault(i, []).append(n.id)
        last = max(hits, key=lambda i: (props[i].t, i)) if hits else None
        if last is not None:
            earned.setdefault(last, []).append(n.id)
        ref_t = None
        if n.reference.exchange_id:
            ref_t = next((seconds(x.at) for t in ep.threads for x in t.exchanges if x.id == n.reference.exchange_id), None)
        needs.append({"need": n.id, "task": n.onet_task_id, "caught": last is not None, "proposal": last,
                      "first_proposal": hits[0] if hits else None, "versions": len(hits),
                      "lead_minutes": (ref_t - props[last].t) / 60 if last is not None and ref_t is not None else None,
                      "worker_does_it": ref_t is not None})
    traps = []
    for tr in ep.traps:
        fired = [i for i, p in enumerate(props) if checks.matches(tr.check, p) is not None]
        traps.append({"trap": tr.id, "fired": bool(fired), "proposals": fired})
    return needs, traps, earned, matched


def previous_version(raw: list[dict], matched: dict[int, list[str]], i: int) -> int | None:
    """The latest earlier proposal this one revises: one matching a same need, or the same action on the same
    existing file. A line said on a call is a new turn, never a revision."""
    p = raw[i]
    if p["action"] == "say":
        return None
    for k in range(i - 1, -1, -1):
        q = raw[k]
        if q["action"] == "say":
            continue
        if set(matched.get(k, [])) & set(matched.get(i, [])):
            return k
        if p["target"] not in ("", "new") and q["target"] == p["target"] and q["action"] == p["action"]:
            return k
    return None


def changed_words(old: list[str], new: str) -> int:
    """Words of `new` that are not in the closest earlier draft: what a reader of a revision has to read."""
    nw = new.split()
    if not old:
        return len(nw)
    best = len(nw)
    for o in old:
        ops = difflib.SequenceMatcher(None, o.split(), nw, autojunk=False).get_opcodes()
        best = min(best, sum(j2 - j1 for tag, _, _, j1, j2 in ops if tag in ("replace", "insert")))
    return best


# ---------- judges ----------


CONTEXT_CHARS = 30000     # judge context budget
FILE_CHARS = 6000         # per file; longer files keep their head and the lines sharing an identifier with the drafts


def _excerpt(text: str, keys: set[str]) -> str:
    if len(text) <= FILE_CHARS:
        return text
    head, rest = text[:1500], text[1500:].splitlines()
    hits = [ln for ln in rest if keys & set(re.findall(r"[\w@.#-]*\d[\w@.#-]*", ln))]
    return head + "\n[... lines matching the drafts' identifiers:]\n" + "\n".join(hits)[:FILE_CHARS - 1500]


_ID = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+|\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b|\b\d{1,2}:\d{2}\b"
                 r"|\b(?=[\w#-]*\d)(?=[\w#-]*[A-Za-z])[\w#-]{4,}\b")
MAX_FACTS = 40
HISTORY_ROWS = 8


def facts_in(p: dict) -> tuple[list[str], list[float]]:
    """The checkable facts in a proposal's drafts: identifiers (ids, emails, dates, times) and amounts."""
    ids, nums = [], []
    for d in p["drafts"]:
        text = " ".join(str(d.get(k, "") or "") for k in ("to", "cc", "subject", "text"))
        found = [m.strip(".-") for m in _ID.findall(text)]
        ids += found
        rest = _ID.sub(" ", text)                       # numbers inside identifiers are not amounts
        nums += [abs(n) for n in checks.numbers(rest) if not (n.is_integer() and 0 <= abs(n) <= 31)]  # list items, days
    return list(dict.fromkeys(ids)), list(dict.fromkeys(nums))


def _locate(files: dict, order: list[str], fact, is_num: bool) -> str | None:
    paths = [x for x in order if x in files] + sorted(set(files) - set(order))
    for path in paths:
        for ln in files[path].data.decode(errors="replace").splitlines():
            hit = (any(abs(abs(n) - fact) < 0.005 for n in checks.numbers(ln)) if is_num
                   else re.search(r"(?<![\w/])" + re.escape(fact) + r"(?![\w/])", ln, re.I) is not None)
            if hit:
                return f"{path}: {ln.strip()[:160]}"
    return None


def draft_facts(ep: Episode, p: dict, t: int, needs: list, files: dict, order: list[str]) -> str:
    """Each number, identifier, date, email and person in the drafts, looked up in the world as of t."""
    ids, nums = facts_in(p)
    key = " ".join(need.reference.text or next((x.body for th in ep.threads for x in th.exchanges
                                                 if x.id == need.reference.exchange_id), "") for need in needs)
    rows = []
    for fact, is_num in [(i, False) for i in ids] + [(n, True) for n in nums]:
        where = _locate(files, order, fact, is_num)
        shown = (str(int(fact)) if is_num and fact.is_integer() and 1900 <= fact <= 2100
                 else f"{fact:,.2f}".rstrip("0").rstrip(".") if is_num else fact)
        if where:
            path, line = where.split(": ", 1)
            rows.append(f"- {shown}: in {path}: \"{line}\"")
        elif (any(abs(abs(n) - fact) < 0.005 for n in checks.numbers(key)) if is_num else fact.lower() in key.lower()):
            rows.append(f"- {shown}: not in the world; in {ep.worker.name.split()[0]}'s own version (computed)")
        else:
            rows.append(f"- {shown}: appears nowhere (computed from other figures, or invented)")
    text = " ".join(str(d.get(k, "") or "") for d in p["drafts"] for k in ("to", "cc", "text"))
    for c in ep.contacts:
        local = (c.email or "").split("@")[0].lower()      # a name word counts if it is in the contact's own address
        words = [w for w in {c.name.split()[0], c.name.split()[-1]} if len(w) >= 3 and w.lower() in local]
        if re.search(rf"\b{re.escape(c.name)}\b", text) or any(re.search(rf"\b{re.escape(w)}\b", text) for w in words):
            rows.append(f"- {c.name}: in /world/contacts.csv: {c.role}, {c.org}" + (f", {c.email}" if c.email else ""))
    return "\n".join(rows[:MAX_FACTS]) or "(no identifiers, amounts or people)"


def open_work(ep: Episode, t: int, needs: list) -> str:
    """The planned work open at t, and whether the worker had already done it."""
    rows = []
    for n in ep.needs:
        if not seconds(n.discoverable_at) <= t <= seconds(n.deadline):
            continue
        done = next((seconds(x.at) for th in ep.threads for x in th.exchanges if x.id == n.reference.exchange_id), None)
        status = f"done by {ep.worker.name.split()[0]} at {show(done)}" if done is not None and done <= t else "not done yet"
        mark = " [the proposal does this work]" if n in needs else ""
        rows.append(f"- {n.title} (due {show(n.deadline)}; {status}){mark}")
    return "\n".join(rows) or "(none)"


def history(ep: Episode, p: dict, t: int, needs: list, earlier: list[dict]) -> str:
    """What the worker and the assistant had already done on this matter by t."""
    first = ep.worker.name.split()[0]
    idx = path_index(ep)
    ids = {idx[p["target"]][2]} if p["target"] in idx else set()
    ids |= {e for n in needs for e in n.evidence}
    rows = []
    for a in ep.worker_actions:
        if seconds(a.at) <= t and (a.target in ids or any(n.reference.exchange_id == a.produces for n in needs)):
            body = next((x.body for th in ep.threads for x in th.exchanges if x.id == a.produces), "")
            rows.append(f"- {show(a.at)} {first} {a.summary}" + (f": \"{body[:400]}\"" if body else ""))
    for q in earlier:
        text = str(q["drafts"][0].get("text", "")) if q["drafts"] else ""
        rows.append(f"- {show(q['t'])} the assistant already proposed ({q['action']} on {q['target']}): \"{text[:300]}\"")
    return "\n".join(rows[-HISTORY_ROWS:]) or "(nothing yet)"


def _draft(i: int, d: dict) -> str:
    head = [f"{k.capitalize()}: {d[k]}" for k in ("to", "cc", "subject") if d.get(k)]
    label = f" ({d['label']})" if d.get("label") else ""
    return f"<draft n=\"{i}\">{label}\n" + "".join(h + "\n" for h in head) + ("\n" if head else "") + \
        f"{d.get('text', '')}\n</draft>"


def judge_prompt(ep: Episode, p: dict, needs: list, earlier: list[dict] = ()) -> tuple[str, str]:
    """The judge's system prompt (the same for every proposal) and the case for this proposal."""
    t = seconds(p["t"])
    first = ep.worker.name.split()[0]
    files = render_world(ep, t)
    order = [p["target"]] + [thread_file(th) for n in needs for e in n.evidence for th in ep.threads if th.id == e] \
        + [document_file(d) for n in needs for e in n.evidence for d in ep.documents if d.id == e] \
        + list(reversed(p.get("read", [])))
    planned = ""
    for need in needs:
        x = next((x for th in ep.threads for x in th.exchanges if x.id == need.reference.exchange_id), None)
        planned += prompts.PLANNED_WORK.format(
            title=need.title, must="; ".join(need.rubric.must), must_not="; ".join(need.rubric.must_not) or "nothing listed",
            first_name=first, reference=x.body if x else need.reference.text or "(none)",
            reference_label=f"What {first} actually did" if x else f"A good version ({first} did not do it)")
    case = prompts.JUDGE_CASE.format(
        worker_name=ep.worker.name, worker_title=ep.worker.title, employer=ep.employer.name, when=show(t),
        profession_prompt=ep.profession_prompt, target=p["target"], action=p["action"],
        drafts="\n\n".join(_draft(i, d) for i, d in enumerate(p["drafts"], 1)), planned_work=planned,
        open_work=open_work(ep, t, needs), history=history(ep, p, t, needs, list(earlier)),
        facts=draft_facts(ep, p, t, needs, files, order), context=_context(ep, p, t, needs, files, order))
    return prompts.JUDGE_SYSTEM, case


def _context(ep: Episode, p: dict, t: int, needs: list, files: dict, order: list[str]) -> str:
    """The files themselves, as of the proposal: the target, the need's evidence, the files the assistant opened."""
    ids, _ = facts_in(p)
    keys = set(ids) | {k for d in p["drafts"] for k in re.findall(r"[\w@.#-]*\d[\w@.#-]*", str(d.get("text", "")))
                       if len(k) >= 3}
    parts, used, seen = [], 0, set()
    for path in order:
        f = files.get(path)
        if not f or path in seen or path.endswith(".xlsx"):
            continue
        seen.add(path)
        block = f"### {path}\n" + _excerpt(f.data.decode(errors="replace"), keys)
        if used + len(block) > CONTEXT_CHARS:
            continue
        parts.append(block)
        used += len(block)
    return "\n\n".join(parts) or "(no file context)"


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
    j["checklist"] = {k: j.get(k) for k in ("needed", "right_place", "facts_correct", "within_authority", "complete")}
    j["minimal_fix"] = str(j.get("minimal_fix", "") or "")
    j["reasons"] = [str(r)[:220] for r in (j.get("reasons") or [])][:2]
    return j


NO_BATCH = False            # --no-batch: skip batch APIs (quick checks)
JUDGE_ATTEMPTS = 4          # per judge and proposal: API errors and unparseable replies are retried with backoff


async def judge_all(run: cfgmod.RunConfig, judges, prompt: tuple[str, str]) -> dict[str, dict]:
    async def one(j):
        gen = {**run.generate_for(j), "max_tokens": 16000}
        if NO_BATCH:
            gen.pop("batch", None)
        model = get_model(j.model, config=GenerateConfig(**gen), **j.model_args)
        last = {"error": "no attempt"}
        for attempt in range(JUDGE_ATTEMPTS):
            if attempt:
                await asyncio.sleep(5 * 2 ** (attempt - 1))
            try:
                out = await model.generate([ChatMessageSystem(content=prompt[0]), ChatMessageUser(content=prompt[1])])
            except Exception as e:  # noqa: BLE001  (any provider error: retry, then record it)
                last = {"error": f"{type(e).__name__}: {str(e)[:300]}"}
                continue
            parsed = parse_judgement(out.completion)
            if parsed:
                parsed["usage"] = out.usage.model_dump() if out.usage else None
                return j.name, parsed
            last = {"error": "unparseable", "raw": (out.completion or "")[:500]}
        return j.name, last
    return dict(await asyncio.gather(*(one(j) for j in judges)))


def panel(run: cfgmod.RunConfig, judgements: dict[str, dict], tested_family: str,
          offsets: dict[str, float] | None = None) -> dict:
    """The panel score: each judge's score less its offset (its average lean over the whole run), weighted, with the
    tested model's own family left out. The uncalibrated means are kept beside it."""
    offsets = offsets or {}
    ok = {j.name: (j, judgements[j.name]) for j in run.judges if j.name in judgements and "score" in judgements[j.name]}

    def mean(items, calibrated=True):
        w = sum(j.weight for j, _ in items)
        if not w:
            return None
        return sum(j.weight * (min(100.0, max(0.0, r["score"] - offsets.get(j.name, 0.0))) if calibrated else r["score"])
                   for j, r in items) / w

    full = list(ok.values())
    drop = [(j, r) for j, r in full if not (j.report_with_dropout and j.family == tested_family)]
    scores = sorted(r["score"] for _, r in full)
    median = scores[len(scores) // 2] if scores else None
    return {"score": mean(drop), "score_all": mean(full), "score_raw": mean(drop, False),
            "score_all_raw": mean(full, False), "median_all_raw": median,
            "harm": sum(j.weight for j, r in drop if r["harm"]) / max(sum(j.weight for j, _ in drop), 1e-9) >= 0.5}


def judge_offsets(graded: list[dict]) -> dict[str, float]:
    """Each judge's average lean: its score minus the mean of all judges on the same proposal, over the run."""
    devs: dict[str, list[float]] = {}
    for g in graded:
        sc = {k: v["score"] for k, v in g["judges"].items() if "score" in v}
        if len(sc) < 2:
            continue
        m = sum(sc.values()) / len(sc)
        for k, v in sc.items():
            devs.setdefault(k, []).append(v - m)
    return {k: sum(v) / len(v) for k, v in devs.items()}


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


def value(ep: Episode, p: dict, j: dict | None, earned: list, price, usage: dict | None,
          read_words: int | None = None) -> dict:
    """Minutes and dollars for one proposal. `earned` are the needs it earns (none if unplanned or superseded);
    `read_words` is what the worker reads (all drafts, or only what changed for a revision)."""
    mm = ep.economics.minutes_model
    wage_min = ep.economics.loaded_hourly / 60
    words_all = sum(len(str(d.get("text", "")).split()) for d in p["drafts"])
    read_min = (words_all if read_words is None else read_words) / mm.read_wpm
    read_min += (mm.call_glance_s if p["action"] == "say" else mm.triage_s) / 60    # attention, beyond reading
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
    do_min = sum(n.minutes.do for n in earned)
    p_acc = (score or 0) / 100
    minutes_saved = do_min * p_acc - read_min - (1 - p_acc) * fix_min if earned else -read_min
    tok_cost = price.cost(usage) if usage and price else 0.0
    return {"read_min": round(read_min, 3), "fix_min": round(fix_min, 3), "edits": edits, "do_min": do_min,
            "minutes_saved": round(minutes_saved, 3), "value_usd": round(minutes_saved * wage_min - tok_cost, 4),
            "token_cost_usd_share": round(tok_cost, 5)}


# ---------- driver ----------


async def grade_log(log, run: cfgmod.RunConfig, judges, gate: asyncio.Semaphore) -> list[dict]:
    speed = speeds(run)
    model_name = log.eval.model
    spec = next((m for m in run.models if m.model == model_name or model_name.endswith(m.model.split("/", 1)[-1])), None)
    family = spec.family if spec else ""
    rows = []
    for s in log.samples or []:
        ep = load_episode(ROOT / s.metadata["episode"])
        idx = path_index(ep)
        props_raw = s.metadata.get("proposals", [])
        props = [to_prop(ep, idx, p) for p in props_raw]
        timing = [call_timing(ep, p, speed.get(spec.name) if spec else None) for p in props_raw]
        late = {i for i, tm in enumerate(timing) if tm and tm["on_time"] is False}
        needs, traps, earned, matched = outcomes(ep, props, late)
        by_id = {n.id: n for n in ep.needs}
        u = (s.model_usage or {}).get(model_name)     # the tested model only, not the simulated worker
        # compaction is the harness's, not the model's: its tokens are not charged (owner, 10-27)
        usage = cfgmod.net_usage(u.model_dump(), s.metadata.get("compaction_usage", {}).get(model_name)) if u else None
        n_props = max(len(props_raw), 1)
        share = {k: (v / n_props if isinstance(v, (int, float)) else v) for k, v in (usage or {}).items()}
        async def grade_one(i, p):
            relevant = [by_id[x] for x in matched.get(i, [])]      # judged against every need it does
            gets = [by_id[x] for x in earned.get(i, [])]           # valued for the needs it earns
            prev = previous_version(props_raw, matched, i)
            read_words = None if prev is None else sum(
                changed_words([str(d.get("text", "")) for d in props_raw[prev]["drafts"]], str(d.get("text", "")))
                for d in p["drafts"])
            earlier = [props_raw[k] for k in range(i) if props_raw[k]["target"] == p["target"] and p["target"] != "new"
                       or set(matched.get(k, [])) & set(matched.get(i, []))]
            async with gate:
                js = await judge_all(run, judges, judge_prompt(ep, p, relevant, earlier)) if judges else {}
            return {"model": spec.name if spec else model_name, "profession": s.id, "epoch": s.epoch,
                    "proposal": p, "needs": [n.id for n in gets], "matches": [n.id for n in relevant],
                    "revises": props_raw[prev]["id"] if prev is not None else None, "timing": timing[i],
                    "judges": js,
                    "_value_args": (ep, gets, spec.price if spec else None, share, read_words, family)}
        graded = list(await asyncio.gather(*(grade_one(i, p) for i, p in enumerate(props_raw))))
        tot_cost = spec.price.cost(usage, s.metadata.get("long_context_usage")) if usage and spec and spec.price else 0.0
        mm = ep.economics.minutes_model
        qs = s.metadata.get("questions", [])
        q_min = sum(len(q["question"].split()) / mm.read_wpm + (0 if q.get("away") else mm.question_answer_s / 60)
                    for q in qs)                                  # a question asked while the worker is away is only read
        rows.append({"model": spec.name if spec else model_name, "profession": s.id, "epoch": s.epoch,
                     "ticks": s.metadata.get("ticks"), "proposals": len(props_raw),
                     "questions": len(qs), "questions_cost_usd": round(q_min * ep.economics.loaded_hourly / 60, 4),
                     "recovered_tool_calls": s.metadata.get("recovered_tool_calls", 0), "needs": needs, "traps": traps,
                     "graded": graded, "usage": usage, "token_cost_usd": round(tot_cost, 4)})
    return rows


def finish(run: cfgmod.RunConfig, rows: list[dict], offsets: dict[str, float]) -> None:
    """Panel scores and value for every graded proposal, once the judges' offsets over the run are known."""
    for r in rows:
        for g in r["graded"]:
            ep, gets, price, share, read_words, family = g.pop("_value_args")
            js = g["judges"]
            g["panel"] = panel(run, js, family, offsets) if js else {"score": None}
            lead = fix_judge(run, js, family)
            j_for_value = {"score": g["panel"]["score"], "best_draft": lead.get("best_draft", 1),
                           "minimal_fix": lead.get("minimal_fix", "")} if js else None
            g["value"] = value(ep, g["proposal"], j_for_value, gets, price, share, read_words)
            if g.get("timing") and g["timing"]["on_time"] is False:
                # a late call line is dropped before the worker sees it, as any assistant would once the worker has
                # started answering; what it would have cost if shown anyway is kept for the sensitivity analysis
                g["value_if_shown"] = g["value"]
                tok = g["value"]["token_cost_usd_share"]
                g["value"] = {"read_min": 0.0, "fix_min": 0.0, "edits": 0, "do_min": 0.0, "minutes_saved": 0.0,
                              "value_usd": round(-tok, 4), "token_cost_usd_share": tok, "suppressed": True}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logs")
    ap.add_argument("--judges", default="all")
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-batch", action="store_true", help="call batch-enabled judges directly (quick checks)")
    a = ap.parse_args()
    global NO_BATCH
    NO_BATCH = a.no_batch
    creds.load()
    run = cfgmod.load(ROOT / "config/run.yaml")
    judges = [] if a.judges == "none" else [j for j in run.judges if a.judges == "all" or j.name in a.judges.split(",")]
    out = Path(a.out or ROOT / "results" / Path(a.logs).name)
    logs = [read_eval_log(l.name) for l in list_eval_logs(a.logs)]   # read before the event loop starts

    async def grade_all():
        gate = asyncio.Semaphore(PROPOSALS_IN_FLIGHT)
        return [r for rows in await asyncio.gather(*(grade_log(lg, run, judges, gate) for lg in logs)) for r in rows]

    rows = sorted(asyncio.run(grade_all()), key=lambda r: (r["model"], r["profession"], r["epoch"]))
    offsets = judge_offsets([g for r in rows for g in r["graded"]])
    finish(run, rows, offsets)
    out.mkdir(parents=True, exist_ok=True)
    (out / "judge_offsets.json").write_text(json.dumps(offsets, indent=1) + "\n")
    with open(out / "graded.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, default=str) + "\n")
    summary = []
    for r in rows:
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
    judges = {j.name: j for j in run.judges}
    spent = dict.fromkeys(cfgmod.BILLED, 0.0)
    for r in rows:
        for g in r["graded"]:
            for k, v in g["judges"].items():
                if v.get("usage") and k in judges and judges[k].price:
                    spent[cfgmod.billing(judges[k].model)] += judges[k].price.cost(v["usage"])
    print(f"cost: judges ${sum(spent.values()):.2f} for {sum(len(r['graded']) for r in rows)} proposals; by billing: "
          + ", ".join(f"{b} ${v:.2f}" for b, v in spent.items()))


if __name__ == "__main__":
    main()
