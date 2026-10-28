"""Checkpoints, so a week that fails (or a batch that stops) resumes from its last tick instead of from Monday.

After every tick the engine saves, per model and profession, under `<WORKWEEK_CONTROL>/checkpoints/`: the
conversation, the simulation's records (proposals, questions, feed, counters), the clock position, the model's home
folder (`/home/assistant`, its notes) and the tokens spent so far. A restarted week loads it, restores the home
folder in its new sandbox, rewrites the world as of that moment and continues with the next tick; the tokens spent
before the restart are kept (`prior_usage`) and added to the week's cost. Without WORKWEEK_CONTROL (a plain
`scripts/run.py`), nothing is saved.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import asdict
from pathlib import Path

from inspect_ai.model import ChatMessage
from inspect_ai.util import sandbox
from pydantic import TypeAdapter

from .world import Event

VERSION = 1
_MESSAGES = TypeAdapter(list[ChatMessage])
SIM_FIELDS = ("last", "proposals", "questions", "ticks_run", "recovered", "measured", "compactions",
              "compaction_usage", "filtered", "call_retries", "long_usage", "read", "tick_index")


def path(model: str, sample_id: str, epoch: int = 1) -> Path | None:
    """One file per model, profession and run of the week (a second run of it is `<profession>-2.json`)."""
    control = os.environ.get("WORKWEEK_CONTROL")
    if not control:
        return None
    name = sample_id if epoch == 1 else f"{sample_id}-{epoch}"
    return Path(control) / "checkpoints" / re.sub(r"[^\w.-]+", "_", model) / f"{name}.json"


async def save(where: Path | None, sim, messages: list, *, day: int, t: int, resume: int, phase: str,
               usage: dict, window: tuple[int, int]) -> None:
    """phase "tick": tick t of day is done (resume after it, within the day); "night": the day and its overnight step
    are done (resume at the next day's start)."""
    if where is None:
        return
    r = await sandbox().exec(["bash", "-c", "tar czf - -C /home/assistant . | base64 -w0"], user="assistant")
    data = {"version": VERSION, "window": list(window), "day": day, "t": t, "resume": resume, "phase": phase,
            "messages": _MESSAGES.dump_python(messages, mode="json"),
            "sim": {k: getattr(sim, k) for k in SIM_FIELDS}, "call_done": sorted(sim.call_done),
            "feed": [asdict(e) for e in sim.feed], "usage": usage, "home": r.stdout if r.success else ""}
    where.parent.mkdir(parents=True, exist_ok=True)
    tmp = where.with_suffix(".tmp")
    tmp.write_text(json.dumps(data))
    tmp.replace(where)


async def load(where: Path | None, sim, window: tuple[int, int]) -> dict | None:
    """Restore sim and the home folder from a checkpoint for this window, or for one that starts at the same time and
    ends earlier (a run extended, e.g. Monday to Monday-Tuesday); returns the position and messages."""
    if where is None or not where.exists():
        return None
    data = json.loads(where.read_text())
    (a, b), (a2, b2) = data["window"], window
    if data.get("version") != VERSION or a != a2 or b > b2:
        return None
    for k, v in data["sim"].items():
        setattr(sim, k, tuple(v) if k == "measured" and v else v)
    sim.call_done = set(data["call_done"])
    sim.feed = [Event(**e) for e in data["feed"]]
    sim.written = {}                       # a new sandbox: the next sync writes the whole world
    if data["home"]:
        await sandbox().exec(["bash", "-c", "base64 -d | tar xzf - -C /home/assistant"], input=data["home"],
                             user="assistant")
    return {"day": data["day"], "t": data["t"], "resume": data["resume"], "phase": data["phase"],
            "messages": _MESSAGES.validate_python(data["messages"]), "usage": data["usage"]}
