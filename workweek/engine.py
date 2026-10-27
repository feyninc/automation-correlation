"""The simulator: one Inspect AI task that runs an assistant model through a profession's week.

The clock is simulated. At every tick (config cadence) the world up to that moment is written into the sandbox and the
model runs as a multi-turn tool-using agent until it calls wait. Live calls the model joins are followed turn by turn.
Nothing the model proposes reaches the world; proposals and questions are recorded in the sample's store.
"""
from __future__ import annotations

import json
from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.model import (ChatMessageSystem, ChatMessageTool, ChatMessageUser, GenerateConfig, Model,
                              get_model)
from inspect_ai.solver import Generate, TaskState, solver
from inspect_ai.tool import ToolInfo, ToolParam, ToolParams
from inspect_ai.util import sandbox, store

from . import config as cfgmod
from . import prompts, providers  # importing providers also patches Inspect
from .apps import FileOut, render_world, thread_file
from .schema import Episode, fmt, seconds
from .world import DAYS, Event, events, feed_lines, ticks

ROOT = Path(__file__).resolve().parents[1]
SANDBOX = ("docker", str(ROOT / "workweek/sandbox/compose.yaml"))
MAX_TOOL_OUTPUT = 12000
KEEP_TOOL_OUTPUT_TICKS = 6
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
        self.read: list[str] = []   # world files named in bash commands, most recent last (the judges see them)
        self.feed: list[Event] = []
        self.last = -1
        self.proposals: list[dict] = []
        self.questions: list[dict] = []
        self.call: str | None = None          # thread id of the joined call
        self.call_done: set[str] = set()
        self.ticks_run = 0
        self.recovered = 0          # tool calls recovered from GLM-syntax text
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

    async def ask(self, question: str, t: int) -> str:
        visible = [n for n in self.ep.needs if seconds(n.discoverable_at) <= t]
        intents = "\n".join(f"- {n.title}: {n.worker_intent}" for n in visible) or "- (nothing specific yet)"
        recent = feed_lines(self.feed[-25:]) or "(nothing yet)"
        msg = prompts.WORKER_SIM.format(worker_name=self.ep.worker.name, worker_title=self.ep.worker.title,
                                        employer=self.ep.employer.name, profession_prompt=self.ep.profession_prompt,
                                        intents=intents, recent=recent, when=fmt(t), question=question)
        out = await self.user_model.generate([ChatMessageUser(content=msg)])
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
        r = await sandbox().exec(["bash", "-lc", str(a.get("command", ""))], user="assistant",
                                 cwd="/home/assistant", timeout=60)
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
                              "in_call": sim.call, "read": sim.read[-READ_KEPT:]})
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


def elide(messages: list, keep_from: int) -> None:
    """Shorten tool outputs older than the last few ticks to bound context; the model can rerun commands."""
    for m in messages[:keep_from]:
        if isinstance(m, ChatMessageTool) and isinstance(m.content, str) and len(m.content) > 400 \
                and not m.content.startswith("[elided"):
            m.content = "[elided: older output; rerun the command if you need it]\n" + m.content[:200]


async def agent_turn(sim: Sim, model: Model, messages: list, t: int, budget: int) -> None:
    for _ in range(budget):
        out = await model.generate(messages, tools=TOOLS)
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
        messages.append(ChatMessageUser(content=prompts.CALL_TURN.format(
            when=fmt(s), path=path, speaker=speaker, text=x.body, first_name=sim.first)))
        await agent_turn(sim, model, messages, s, budget=4)
        if sim.call is None:
            return s
    sim.call_done.add(th.id)
    sim.call = None
    return min(th.call_end(), sim.end)


@solver
def workweek_agent(run_path: str = "config/run.yaml", start: str = "D1 08:00", end: str = "D5 17:00"):
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        run = cfgmod.load(ROOT / run_path)
        ep = load_episode(ROOT / state.metadata["episode"])
        s0, s1 = seconds(start), seconds(end)
        sim = Sim(ep, run, s0, s1)
        model = get_model()
        cadence = int(run.run.cadence_minutes * 60)
        budget = run.run.max_tool_calls_per_tick
        system = prompts.HARNESS.format(worker_name=ep.worker.name, worker_title=ep.worker.title,
                                        employer=ep.employer.name, first_name=sim.first,
                                        profession_prompt=ep.profession_prompt.strip())
        for day in range(1, 6):
            day_ticks = [x for x in ticks(day, cadence) if s0 <= x <= s1]
            if not day_ticks:
                continue
            messages: list = [ChatMessageSystem(content=system),
                              ChatMessageUser(content=prompts.DAY_START.format(date=DAYS[day - 1]))]
            tick_starts: list[int] = []
            resume = -1
            for t in day_ticks:
                if t < resume:
                    continue
                new = events(ep, sim.last, t)
                await sim.sync(t, new)
                sim.last = t
                live = [e for e in sim.feed if e.text.startswith("live ") and e.at <= t]
                call_note = ""
                if any(sim.call_thread(e.path) and sim.call_thread(e.path).call_end() >= t for e in live):
                    call_note = " A live call is in progress (see the feed)."
                end_of_day = t % 86400 == 17 * 3600
                text = (prompts.END_OF_DAY.format(when=fmt(t), first_name=sim.first, n_new=len(new)) if end_of_day else
                        prompts.TICK.format(when=fmt(t), n_new=len(new), call_note=call_note))
                tick_starts.append(len(messages))
                if len(tick_starts) > KEEP_TOOL_OUTPUT_TICKS:
                    elide(messages, tick_starts[-KEEP_TOOL_OUTPUT_TICKS - 1])
                messages.append(ChatMessageUser(content=text))
                sim.ticks_run += 1
                await agent_turn(sim, model, messages, t, budget)
                if sim.call:
                    resume = await follow_call(sim, model, messages, t)
        store().set("proposals", sim.proposals)
        store().set("questions", sim.questions)
        store().set("ticks", sim.ticks_run)
        state.metadata["proposals"] = sim.proposals
        state.metadata["questions"] = sim.questions
        state.metadata["ticks"] = sim.ticks_run
        state.metadata["recovered_tool_calls"] = sim.recovered
        state.completed = True
        return state

    return solve


@task
def workweek(professions: str = "all", start: str = "D1 08:00", end: str = "D5 17:00",
             run_path: str = "config/run.yaml", epochs: int = 1):
    paths = sorted(p.parent for p in (ROOT / "professions").glob("*/episode/profession.json"))
    if professions != "all":
        keep = set(professions.split(","))
        paths = [p for p in paths if p.parent.name in keep]
    samples = [Sample(id=p.parent.name, input=f"Simulate {p.parent.name}", metadata={"episode": str(p.relative_to(ROOT))})
               for p in paths]
    return Task(dataset=samples, solver=workweek_agent(run_path=run_path, start=start, end=end), sandbox=SANDBOX,
                epochs=epochs)
