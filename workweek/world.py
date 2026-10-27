"""The world over time: what changed between two moments, as feed lines, and the tick schedule."""
from __future__ import annotations

from dataclasses import dataclass

from .apps import REGISTRY, document_file, thread_file
from .schema import Episode, fmt, seconds

DAY_START, DAY_END = 8 * 3600, 17 * 3600
DAYS = ["Monday 2026-11-02", "Tuesday 2026-11-03", "Wednesday 2026-11-04", "Thursday 2026-11-05", "Friday 2026-11-06"]


@dataclass
class Event:
    at: int
    path: str
    text: str


def _name(ep: Episode, pid: str) -> str:
    if pid == "worker":
        return ep.worker.name
    c = next((c for c in ep.contacts if c.id == pid), None)
    return c.name if c else pid


def events(ep: Episode, t0: int, t1: int) -> list[Event]:
    """Everything that became visible in (t0, t1]: new exchanges, new document versions, worker activity."""
    out: list[Event] = []
    produced = {a.produces for a in ep.worker_actions if a.produces}
    for t in ep.threads:
        app = REGISTRY[t.app]
        for i, x in enumerate(t.exchanges):
            s = seconds(x.at)
            if t0 < s <= t1 and x.id not in produced:
                if t.live and i == 0:
                    out.append(Event(s, thread_file(t), f"live {app.label} started: {t.title} ({_name(ep, x.author)})"))
                elif t.live:
                    continue  # call turns are only visible to an assistant that joined the call
                else:
                    what = x.subject or t.title
                    out.append(Event(s, thread_file(t), f"new {app.label} from {_name(ep, x.author)}: {what}"))
    for d in ep.documents:
        for i, v in enumerate(d.versions):
            s = seconds(v.at)
            if t0 < s <= t1 and f"{d.id}@{i}" not in produced:
                verb = "new" if i == 0 else "updated"
                out.append(Event(s, document_file(d), f"{verb} {REGISTRY[d.app].label} by {_name(ep, v.author)}: {d.title}"))
    for a in ep.worker_actions:
        s = seconds(a.at)
        if t0 < s <= t1:
            target = next((thread_file(t) for t in ep.threads if t.id == a.target), None) or \
                next((document_file(d) for d in ep.documents if d.id == a.target), a.target)
            out.append(Event(s, target, f"{ep.worker.name} {a.summary}"))
    return sorted(out, key=lambda e: (e.at, e.path))


def feed_lines(evs: list[Event]) -> str:
    return "\n".join(f"- [{fmt(e.at)[3:]}] {e.text}  ({e.path})" for e in evs)


def ticks(day: int, cadence_s: int, start: int = DAY_START, end: int = DAY_END) -> list[int]:
    base = (day - 1) * 86400
    out, s = [], start
    while s <= end:
        out.append(base + s)
        s += cadence_s
    if out[-1] != base + end:
        out.append(base + end)
    return out


def live_calls(ep: Episode):
    return [t for t in ep.threads if t.live]


def coverage(ep: Episode, cadence_s: int) -> dict:
    """Which need windows and live-call turns a model can reach at this cadence (calls are joined at a tick)."""
    reach, total = 0, 0
    for n in ep.needs:
        total += 1
        a, b = seconds(n.discoverable_at), seconds(n.deadline)
        day = a // 86400 + 1
        if any(a <= t <= b for d in range(day, 6) for t in ticks(d, cadence_s, 0, 86400 - cadence_s)):
            reach += 1
    call_turns, reachable_turns = 0, 0
    for t in live_calls(ep):
        start = seconds(t.exchanges[0].at)
        day = start // 86400 + 1
        first_tick = next((x for x in ticks(day, cadence_s, 0, 86400 - cadence_s) if x >= start), None)
        for x in t.exchanges:
            if x.author != "worker":
                call_turns += 1
                if first_tick is not None and seconds(x.at) >= first_tick:
                    reachable_turns += 1
    return {"needs": total, "needs_reachable": reach, "call_turns": call_turns,
            "call_turns_reachable": reachable_turns}
