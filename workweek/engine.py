"""The simulator: one Inspect AI task that runs an assistant model through a profession's week.

The clock is simulated. At every tick (config cadence) the world up to that moment is written into the sandbox and the
model runs as a multi-turn tool-using agent until it calls wait. Live calls the model joins are followed turn by turn.
Nothing the model proposes reaches the world; proposals and questions are recorded in the sample's store.

The model keeps one conversation for the whole week. Nothing in it is trimmed; it is compacted (workweek/compaction.py,
after OpenCode) when the input reaches `compact_at` of the model's context window (config `context_window`, the
largest variant on its route) and at midnight after each day. Compaction's tokens are recorded apart and not charged
to the model.
"""
from __future__ import annotations

import asyncio
import json
import os
import time
from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.model import ChatMessageSystem, ChatMessageTool, ChatMessageUser, GenerateConfig, Model, get_model
from inspect_ai.solver import Generate, TaskState, solver
from inspect_ai.tool import ToolInfo, ToolParam, ToolParams
from inspect_ai.util import sandbox, store

from . import config as cfgmod
from . import compaction, prompts, providers  # importing providers also patches Inspect
from .apps import FileOut, render_world, thread_file
from .schema import WEEKDAYS, Episode, fmt, seconds, show
from .world import DAYS, Event, events, feed_lines, ticks

ROOT = Path(__file__).resolve().parents[1]
SANDBOX = ("docker", str(ROOT / "workweek/sandbox/compose.yaml"))
MAX_TOOL_OUTPUT = 12000
FILTER_ATTEMPTS = 3           # tries of a call a content filter blocks before the turn is given up
READ_KEPT = 12                 # most recent world files read, kept with each proposal for the judges

TOOLS = [
    ToolInfo(name="bash", description="Run a shell command in your workspace (read-only /world, writable /home/assistant). Returns stdout and stderr.",
             parameters=ToolParams(properties={"command": ToolParam(type="string", description="The command to run.")},
                                   required=["command"])),
    ToolInfo(name="propose",
             description="Propose something for the worker to approve: a reply, a new message, a document edit, a calendar change, a ticket update, or a line to say on a call. Nothing is sent until the worker approves.",
             parameters=ToolParams(properties={
                 "target": ToolParam(type="string", description="The file this concerns (e.g. /world/mail/inbox/x.md), or 'new' for a new item."),
                 "action": ToolParam(type="string", enum=["reply", "new", "forward", "edit", "schedule", "update", "say", "flag"],
                                     description="reply/forward in a thread; new message; edit a document; schedule on the calendar; update a ticket or case; say a line on a joined call; flag = a heads-up note for the worker with nothing to send."),
                 "drafts": ToolParam(type="array", description="One to three alternative drafts, best first.",
                                     items=ToolParam(type="object", properties={
                                         "label": ToolParam(type="string", description="A short name for this alternative."),
                                         "to": ToolParam(type="string", description="Recipients, comma-separated (messages only)."),
                                         "cc": ToolParam(type="string", description="Cc, comma-separated (optional)."),
                                         "subject": ToolParam(type="string", description="Subject (new messages only)."),
                                         "text": ToolParam(type="string", description="The full text: the message, the new document content or the change, or the line to say."),
                                     }, required=["text"])),
                 "note": ToolParam(type="string", description="Optional one-line note to the worker about why."),
             }, required=["target", "action", "drafts"])),
    ToolInfo(name="ask_worker", description="Ask the worker a short question. It interrupts them; use it only when it matters.",
             parameters=ToolParams(properties={"question": ToolParam(type="string")}, required=["question"])),
    ToolInfo(name="join_call", description="Follow a live call turn by turn.",
             parameters=ToolParams(properties={"path": ToolParam(type="string", description="The call's file under /world/phone.")},
                                   required=["path"])),
    ToolInfo(name="leave_call", description="Stop following the current call.", parameters=ToolParams()),
    ToolInfo(name="wait", description="Nothing more to do for now; resume at the next check-in.", parameters=ToolParams()),
]


def load_episode(folder: str | Path) -> Episode:
    from .compile import merge_days
    return merge_days(folder)


class Sim:
    """Per-sample simulator state."""

    def __init__(self, ep: Episode, run: cfgmod.RunConfig, start: int, end: int):
        self.ep, self.run = ep, run
        self.start, self.end = start, end
        self.written: dict[str, bytes] = {}
        self.work = {"output_tokens": [], "tool_s": 0.0}   # since the prompt being answered: for offline timing
        self.read: list[str] = []   # world files named in bash commands, most recent last (the judges see them)
        self.feed: list[Event] = []
        self.last = -1
        self.proposals: list[dict] = []
        self.questions: list[dict] = []
        self.call: str | None = None          # thread id of the joined call
        self.call_done: set[str] = set()
        self.ticks_run = 0
        self.recovered = 0          # tool calls recovered from GLM-syntax text
        self.window = 0             # the tested model's context window (tokens)
        self.measured: tuple[int, int] | None = None   # input tokens of the last call, and len(messages) it covered
        self.compactions = 0
        self.compaction_usage: dict[str, dict] = {}   # per model string: tokens spent compacting (not charged)
        self.filtered: list[dict] = []    # calls a provider's content filter blocked, after retries
        self.price = None                 # the tested model's Price
        self.long_usage: dict = {}        # usage of calls over price.long_above (priced at the long-context rate)
        self.tick_index = 0
        self.first = ep.worker.name.split()[0]
        self.user_model: Model = get_model(run.user_model.model, config=GenerateConfig(**run.generate_for(run.user_model)),
                                           **run.user_model.model_args)

    async def sync(self, t: int, new: list[Event]) -> None:
        sb = sandbox()
        files = render_world(self.ep, t)
        self.feed += new
        day0 = (t // 86400) * 86400
        today = [e for e in self.feed if e.at >= day0]
        files["/world/inbox/new.md"] = FileOut("/world/inbox/new.md",
                                               ("# New since your last check\n\n" + (feed_lines(new) or "(nothing new)") + "\n").encode())
        files["/world/inbox/feed.md"] = FileOut("/world/inbox/feed.md",
                                                ("# Today so far\n\n" + (feed_lines(today) or "(nothing yet)") + "\n").encode())
        for p, f in files.items():
            if self.written.get(p) != f.data:
                await sb.write_file(p, f.data)
                self.written[p] = f.data
        await sb.exec(["chmod", "-R", "a+rX", "/world"])

    def note_reads(self, command: str) -> None:
        """Remember which world files a command names, by full path or by their last two path parts."""
        for f in self.written:
            if f.startswith("/world/inbox/"):
                continue
            if f in command or "/".join(f.split("/")[-2:]) in command:
                if f in self.read:
                    self.read.remove(f)
                self.read.append(f)

    def call_thread(self, path: str):
        for t in self.ep.threads:
            if t.live and (thread_file(t) == path or t.id == path or t.path == path):
                return t
        return None

    def presence(self, t: int) -> str:
        """Whether the worker is at work at t, and if not, when they are next in."""
        day, sec = t // 86400 + 1, t % 86400
        a, b = self.ep.worker.day_hours(day)
        hm = lambda x: f"{x // 3600:02d}:{x % 3600 // 60:02d}"
        if a <= sec < b:
            return f"{self.first} is at work until {hm(b)}."
        if sec < a:
            return f"{self.first} is not at work yet; in at {hm(a)}."
        if day < 5:
            return f"{self.first} has left for the day; back {WEEKDAYS[day]} {hm(self.ep.worker.day_hours(day + 1)[0])}."
        return f"{self.first} has left for the week."

    def at_work(self, t: int) -> bool:
        a, b = self.ep.worker.day_hours(t // 86400 + 1)
        return a <= t % 86400 < b

    async def ask(self, question: str, t: int) -> str:
        if not self.at_work(t):
            self.questions.append({"t": fmt(t), "question": question, "answer": "", "away": True, "usage": None})
            return f"{self.presence(t)} The question waits until then; nobody can answer it now."
        visible = [n for n in self.ep.needs if seconds(n.discoverable_at) <= t]
        intents = "\n".join(f"- {n.title}: {n.worker_intent}" for n in visible) or "- (nothing specific yet)"
        recent = feed_lines(self.feed[-25:]) or "(nothing yet)"
        case = prompts.WORKER_CASE.format(worker_name=self.ep.worker.name, worker_title=self.ep.worker.title,
                                          employer=self.ep.employer.name, profession_prompt=self.ep.profession_prompt,
                                          intents=intents, recent=recent, when=show(t), question=question)
        out = await self.user_model.generate([ChatMessageSystem(content=prompts.WORKER_SYSTEM),
                                              ChatMessageUser(content=case)])
        answer = (out.completion or "").strip()
        u = out.usage
        self.questions.append({"t": fmt(t), "question": question, "answer": answer,
                               "usage": u.model_dump() if u else None})
        return answer


async def run_tool(sim: Sim, call, t: int) -> tuple[str, bool]:
    """Execute one tool call; returns (output, ends_turn)."""
    a = call.arguments or {}
    name = call.function
    if name == "bash":
        sim.note_reads(str(a.get("command", "")))
        t0 = time.monotonic()
        r = await sandbox().exec(["bash", "-lc", str(a.get("command", ""))], user="assistant",
                                 cwd="/home/assistant", timeout=60)
        sim.work["tool_s"] += time.monotonic() - t0
        out = (r.stdout or "") + (("\n[stderr]\n" + r.stderr) if r.stderr else "")
        if len(out) > MAX_TOOL_OUTPUT:
            out = out[:MAX_TOOL_OUTPUT] + f"\n[... output truncated at {MAX_TOOL_OUTPUT} characters]"
        return out or "(no output)", False
    if name == "propose":
        drafts = a.get("drafts") or []
        if isinstance(drafts, str):
            try:
                drafts = json.loads(drafts)
            except ValueError:
                drafts = [{"text": drafts}]
        drafts = [d if isinstance(d, dict) else {"text": str(d)} for d in drafts][:3]
        if not drafts:
            return "A proposal needs at least one draft.", False
        if a.get("action") in ("new", "forward") and not all(d.get("to") for d in drafts):
            return "Nothing saved: a new or forwarded message needs a recipient (to) in every draft.", False
        pid = f"p{len(sim.proposals) + 1:04d}"
        sim.proposals.append({"id": pid, "t": fmt(t), "tick": sim.ticks_run, "target": a.get("target", ""),
                              "action": a.get("action", ""), "drafts": drafts, "note": a.get("note", ""),
                              "in_call": sim.call, "read": sim.read[-READ_KEPT:],
                              "work": {**sim.work, "output_tokens": list(sim.work["output_tokens"]),
                                       "tool_s": round(sim.work["tool_s"], 2)}})
        return f"Saved proposal {pid} with {len(drafts)} draft(s). {sim.first} will review it; nothing was sent.", False
    if name == "ask_worker":
        q = str(a.get("question", "")).strip()
        if not q:
            return "Empty question.", False
        return f"{sim.first}: {await sim.ask(q, t)}", False
    if name == "join_call":
        th = sim.call_thread(str(a.get("path", "")))
        if not th:
            return "No live call at that path.", False
        if th.id in sim.call_done or th.call_end() < t:
            return "That call has ended.", False
        if seconds(th.exchanges[0].at) > t:
            return "That call has not started.", False
        sim.call = th.id
        return f"Joined the call {thread_file(th)}. You will get each new turn as it happens.", True
    if name == "leave_call":
        sim.call = None
        return "Left the call.", False
    if name == "wait":
        return "OK.", True
    return f"Unknown tool {name}.", False


async def pause_point() -> None:
    """Wait while the batch's PAUSE file exists (scripts/batch.py sets WORKWEEK_CONTROL to the batch's log directory).
    The simulated clock stops with it, so a pause changes nothing in the week; one over a provider's cache lifetime
    (about five minutes on Bedrock) costs one cache rewrite of the conversation when it resumes."""
    control = os.environ.get("WORKWEEK_CONTROL")
    while control and (Path(control) / "PAUSE").exists():
        await asyncio.sleep(15)


async def compact_if_due(sim: Sim, model: Model, messages: list, force: bool = False) -> None:
    """Compact the conversation once its input reaches compact_at of the window, or now (midnight)."""
    if len(messages) <= 2:
        return
    threshold = sim.run.run.compact_at * sim.window
    # the model's own characters per token, from its last measured call (tool definitions make it conservative)
    cpt = (max(1.0, compaction.chars(messages[:sim.measured[1]]) / sim.measured[0]) if sim.measured
           else compaction.CHARS_PER_TOKEN)
    if not force:
        tokens = (sim.measured[0] + compaction.estimate(messages[sim.measured[1]:], cpt) if sim.measured
                  else compaction.estimate(messages, cpt))
        if tokens < threshold:
            return
    keep = min(compaction.KEEP_TOKENS, int(compaction.TAIL_SHARE * threshold))

    async def fn(model, messages, tools, usage):
        return await compaction.compact(model, messages, tools, usage, keep=keep, chars_per_token=cpt)
    await replace(sim, model, messages, fn)


async def overnight(sim: Sim, model: Model, messages: list) -> None:
    """Between days, as config `overnight` says: compact, clear, or the custom function."""
    how = sim.run.run.overnight
    if how == "clear":
        messages[:] = compaction.clear(messages)
        sim.measured = None
    elif how == "compact":
        await compact_if_due(sim, model, messages, force=True)
    else:
        await replace(sim, model, messages, compaction.load(sim.run.run.overnight_function))


async def replace(sim: Sim, model: Model, messages: list, fn) -> None:
    """Replace the conversation with fn's; its calls' tokens are tallied apart and not charged."""
    usage: list[dict] = []
    for attempt in range(FILTER_ATTEMPTS):      # a summary call can meet a content filter too
        try:
            messages[:] = await fn(model, messages, TOOLS, usage)
            break
        except Exception as e:
            if not providers.content_filtered(e) or attempt == FILTER_ATTEMPTS - 1:
                raise
    sim.measured = None
    sim.compactions += 1
    tally = sim.compaction_usage.setdefault(str(model), {})
    for u in usage:
        for f, v in u.items():
            if isinstance(v, (int, float)):
                tally[f] = tally.get(f, 0) + v


async def agent_turn(sim: Sim, model: Model, messages: list, t: int, budget: int) -> None:
    for _ in range(budget):
        await compact_if_due(sim, model, messages)
        out = None
        for attempt in range(FILTER_ATTEMPTS):
            try:
                out = await model.generate(messages, tools=TOOLS)
                break
            except Exception as e:     # a content-filter block ends this turn, not the sample
                if not providers.content_filtered(e):
                    raise
                if attempt == FILTER_ATTEMPTS - 1:
                    sim.filtered.append({"at": fmt(t), "error": str(e)[-300:]})
                    return
        u = out.usage
        prompt_tokens = u.input_tokens + (u.input_tokens_cache_read or 0) + (u.input_tokens_cache_write or 0) if u else 0
        if u:
            sim.measured = (prompt_tokens, len(messages))
        if u and sim.price and sim.price.long_above and prompt_tokens > sim.price.long_above:
            for f, v in u.model_dump().items():
                if isinstance(v, (int, float)):
                    sim.long_usage[f] = sim.long_usage.get(f, 0) + v
        sim.work["output_tokens"].append(out.usage.output_tokens if out.usage else 0)
        calls = out.message.tool_calls or []
        if not calls:
            calls = providers.recover_tool_calls(out.message.text, {t.name for t in TOOLS})
            if calls:
                out.message.tool_calls = calls
                sim.recovered += len(calls)
        messages.append(out.message)
        if not calls:
            messages.append(ChatMessageUser(content=prompts.NO_TOOL.format(first_name=sim.first)))
            return
        done = False
        for c in calls:
            text, ends = await run_tool(sim, c, t)
            messages.append(ChatMessageTool(content=text, tool_call_id=c.id, function=c.function))
            done = done or ends
        if done:
            return


async def follow_call(sim: Sim, model: Model, messages: list, t: int) -> int:
    """Run a joined call turn by turn from time t; returns the time the call ended or was left."""
    th = next(x for x in sim.ep.threads if x.id == sim.call)
    path = thread_file(th)
    xs = [x for x in th.exchanges if not x.meta.get("case_note")]
    # a caller turn spoken at or before joining that the worker has not answered yet is still the model's to answer
    pending = next((i for i in range(len(xs) - 1, -1, -1) if xs[i].author != "worker" and seconds(xs[i].at) <= t
                    and (i + 1 == len(xs) or seconds(xs[i + 1].at) > t)), None)
    for i, x in enumerate(xs):
        s = seconds(x.at)
        if x.author == "worker" or (s <= t and i != pending):
            continue
        s = max(s, t)
        if s > sim.end:
            break
        await sim.sync(s, events(sim.ep, sim.last, s))
        sim.last = s
        speaker = next((c.name for c in sim.ep.contacts if c.id == x.author), x.author)
        sim.work = {"output_tokens": [], "tool_s": 0.0, "answers": x.id, "patience_s": x.meta.get("patience_s")}
        messages.append(ChatMessageUser(content=prompts.CALL_TURN.format(
            when=show(s), path=path, speaker=speaker, text=x.body, first_name=sim.first)))
        await agent_turn(sim, model, messages, s, budget=4)
        if sim.call is None:
            return s
    sim.call_done.add(th.id)
    sim.call = None
    return min(th.call_end(), sim.end)


@solver
def workweek_agent(run_path: str = "config/run.yaml", start: str = "D1 00:00", end: str = "D5 23:59"):
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        run = cfgmod.load(ROOT / run_path)
        ep = load_episode(ROOT / state.metadata["episode"])
        s0, s1 = seconds(start), seconds(end)
        sim = Sim(ep, run, s0, s1)
        model = get_model()
        sim.window = run.spec(str(model)).context_window
        sim.price = run.spec(str(model)).price
        cadence = int(run.run.cadence_minutes * 60)
        budget = run.run.max_tool_calls_per_tick
        system = prompts.HARNESS.format(worker_name=ep.worker.name, worker_title=ep.worker.title,
                                        overnight=prompts.OVERNIGHT[run.run.overnight],
                                        employer=ep.employer.name, first_name=sim.first,
                                        profession_prompt=ep.profession_prompt.strip())
        days = [d for d in range(1, 6) if any(s0 <= x <= s1 for x in ticks(d, cadence, 0, 86400 - cadence))]
        messages: list = [ChatMessageSystem(content=system)]     # one conversation for the week
        for day in days:
            day_start, day_end = ep.worker.day_hours(day)
            day_ticks = [x for x in ticks(day, cadence, 0, 86400 - cadence) if s0 <= x <= s1]   # around the clock
            messages.append(ChatMessageUser(content=prompts.DAY_START.format(
                date=DAYS[day - 1], time=show(day_ticks[0]).split()[1], first_name=sim.first,
                arrive=f"{day_start // 3600:02d}:{day_start % 3600 // 60:02d}",
                leave=f"{day_end // 3600:02d}:{day_end % 3600 // 60:02d}")))
            resume = -1
            for t in day_ticks:
                if t < resume:
                    continue
                await pause_point()
                new = events(ep, sim.last, t)
                await sim.sync(t, new)
                sim.last = t
                live = [e for e in sim.feed if e.text.startswith("live ") and e.at <= t]
                call_note = ""
                if any(sim.call_thread(e.path) and sim.call_thread(e.path).call_end() >= t for e in live):
                    call_note = " A live call is in progress (see the feed)."
                end_of_day = t % 86400 == day_end
                text = (prompts.END_OF_DAY.format(when=show(t), first_name=sim.first, n_new=len(new)) if end_of_day else
                        prompts.TICK.format(when=show(t), n_new=len(new), call_note=call_note,
                                            presence=sim.presence(t)))
                messages.append(ChatMessageUser(content=text))
                sim.ticks_run += 1
                sim.work = {"output_tokens": [], "tool_s": 0.0}
                await agent_turn(sim, model, messages, t, budget)
                if sim.call:
                    resume = await follow_call(sim, model, messages, t)
            if day != days[-1]:
                await overnight(sim, model, messages)
        store().set("proposals", sim.proposals)
        store().set("questions", sim.questions)
        store().set("ticks", sim.ticks_run)
        state.metadata["proposals"] = sim.proposals
        state.metadata["questions"] = sim.questions
        state.metadata["ticks"] = sim.ticks_run
        state.metadata["recovered_tool_calls"] = sim.recovered
        state.metadata["compactions"] = sim.compactions
        state.metadata["filtered_calls"] = sim.filtered
        state.metadata["long_context_usage"] = sim.long_usage
        state.metadata["compaction_usage"] = sim.compaction_usage
        state.completed = True
        return state

    return solve


@task
def workweek(professions: str = "all", start: str = "D1 00:00", end: str = "D5 23:59",
             run_path: str = "config/run.yaml", epochs: int = 1):
    paths = sorted(p.parent for p in (ROOT / "professions").glob("*/episode/profession.json"))
    if professions != "all":
        keep = set(professions.split(","))
        paths = [p for p in paths if p.parent.name in keep]
    samples = [Sample(id=p.parent.name, input=f"Simulate {p.parent.name}", metadata={"episode": str(p.relative_to(ROOT))})
               for p in paths]
    return Task(dataset=samples, solver=workweek_agent(run_path=run_path, start=start, end=end), sandbox=SANDBOX,
                epochs=epochs)
