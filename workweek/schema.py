"""The episode: one profession's simulated working week, as the compiler writes it and the engine reads it.

Times are "D<day> HH:MM" or "D<day> HH:MM:SS" (day 1 = Monday 2026-11-02; seconds are used inside live calls);
"D0" means already there on Monday morning. Paths use "/" to bucket threads and documents inside an app.
"""
from __future__ import annotations

import re
from typing import Annotated, Any, Literal

from pydantic import AfterValidator, BaseModel, field_validator, model_validator

SCHEMA_VERSION = "1.0"
_TIME = re.compile(r"^D([0-5])(?: ([01]\d|2[0-3]):([0-5]\d)(?::([0-5]\d))?)?$")


def seconds(t: str) -> int:
    """Simulated seconds since Monday 00:00 of week day 0; D0 sorts before everything."""
    m = _TIME.match(t)
    if not m:
        raise ValueError(f"bad time {t!r}")
    d, h, mi, s = m.groups()
    if not h:
        return -1 if d == "0" else (int(d) - 1) * 86400
    return (int(d) - 1) * 86400 + int(h) * 3600 + int(mi) * 60 + int(s or 0)


def fmt(sec: int) -> str:
    if sec < 0:
        return "D0"
    d, r = divmod(sec, 86400)
    h, r = divmod(r, 3600)
    m, s = divmod(r, 60)
    return f"D{d + 1} {h:02d}:{m:02d}" + (f":{s:02d}" if s else "")


def _check_time(v: str) -> str:
    seconds(v)
    return v


Time = Annotated[str, AfterValidator(_check_time)]


class _M(BaseModel):
    model_config = {"extra": "forbid"}


class Contact(_M):
    id: str
    name: str
    role: str
    org: str
    email: str | None = None
    phone: str | None = None
    relation: str = ""          # manager, peer, customer, vendor, regulator, ...
    notes: str = ""


class Worker(_M):
    id: str = "worker"
    name: str
    title: str
    manager: str                # contact id
    team: str
    email: str
    signature: str = ""


class Employer(_M):
    name: str
    industry: str
    size: int
    location: str
    timezone: str
    description: str = ""


class Exchange(_M):
    """One message in a thread: an email, a chat message, a ticket update, a call turn, a PR comment."""
    id: str
    at: Time
    author: str                 # contact id or "worker"
    to: list[str] = []
    cc: list[str] = []
    subject: str | None = None
    body: str
    attachments: list[str] = []  # document ids
    meta: dict[str, Any] = {}


class StateChange(_M):
    at: Time
    set: dict[str, Any]


class Thread(_M):
    id: str
    app: str
    path: str                   # bucketed name inside the app, e.g. "#ops/peak-staffing"
    title: str
    live: bool = False          # a phone call: exchanges arrive faster than the tick
    state: dict[str, Any] = {}  # ticket status, priority, ... when the thread first appears
    state_changes: list[StateChange] = []   # later changes (a reply marks it solved, a customer reopens it)
    exchanges: list[Exchange]

    def call_end(self) -> int:
        """When a call's last spoken turn is; case notes written afterwards don't extend it."""
        return max(seconds(x.at) for x in self.exchanges if not x.meta.get("case_note"))

    def state_at(self, t: int) -> dict[str, Any]:
        out = dict(self.state)
        for c in sorted(self.state_changes, key=lambda c: seconds(c.at)):
            if seconds(c.at) <= t:
                out.update(c.set)
        return out

    @field_validator("path")
    @classmethod
    def _path(cls, v: str) -> str:
        if v.startswith("/") or "//" in v or not re.fullmatch(r"[#@A-Za-z0-9._\-/ ]+", v):
            raise ValueError(f"bad path {v!r}")
        return v


class Version(_M):
    at: Time
    author: str
    content: str                # md/csv/json text; xlsx is written from csv content
    note: str = ""


class Document(_M):
    id: str
    app: str                    # docs, calendar, records, contacts, policies, repo
    path: str
    title: str
    format: Literal["md", "csv", "xlsx", "json", "txt", "py", "sql", "yaml", "ics"] = "md"
    versions: list[Version]


class WorkerAction(_M):
    """Something the worker does: shows up in the assistant's feed as worker activity.

    A write (reply, new, edit, ...) points at the exchange or document version it produced; a read just records
    what the worker looked at.
    """
    id: str
    at: Time
    kind: Literal["read", "reply", "new", "forward", "edit", "schedule", "update", "say", "call", "noop"]
    target: str                 # thread id or document id
    produces: str | None = None  # exchange id or "<doc id>@<version index>"
    summary: str                # one line shown in the feed
    note: str = ""              # hidden: why (for graders and the realism review)


Predicate = dict[str, Any]
PREDICATE_LEAVES = {"app", "path", "path_prefix", "target", "action_in", "to_includes", "before", "after",
                    "mentions_all", "mentions_any", "number_equals"}


class Minutes(_M):
    do: float                   # the worker doing it unaided
    source: str


class Rubric(_M):
    must: list[str]
    must_not: list[str] = []


class Reference(_M):
    exchange_id: str | None = None   # the worker's own version, when the worker does it
    document_version: str | None = None
    text: str | None = None          # otherwise a reference text

    @model_validator(mode="after")
    def _one(self):
        if not (self.exchange_id or self.document_version or self.text):
            raise ValueError("reference needs exchange_id, document_version or text")
        return self


class Need(_M):
    id: str
    title: str
    kind: Literal["reply", "follow_up", "schedule", "doc", "reconcile", "escalate", "prep", "call_line", "code", "update", "flag"]
    onet_task_id: str
    discoverable_at: Time
    deadline: Time
    evidence: list[str]              # item ids that reveal it (threads, exchanges, documents)
    reference: Reference
    check: Predicate
    rubric: Rubric
    minutes: Minutes
    worker_intent: str               # private: what the worker would decide and why (for the simulated worker)
    ledger_keys: list[str] = []      # figures this need depends on

    @model_validator(mode="after")
    def _window(self):
        if seconds(self.discoverable_at) >= seconds(self.deadline):
            raise ValueError(f"{self.id}: discoverable_at must be before deadline")
        return self


class Trap(_M):
    id: str
    title: str
    kind: Literal["phishing", "fyi_only", "misaddressed", "human_only_decision", "confidential", "stale_info",
                  "pressure_to_send", "scope_creep", "supply_chain"]
    evidence: list[str]
    check: Predicate
    correct_behavior: str
    severity: Literal["low", "medium", "high"]
    harm_usd_upper: float | None = None   # sourced upper bound for the sensitivity table
    source: str = ""
    worker_mistakes: list[str] = []       # worker actions that deliberately fall for it (the script's own errors)


class Sourced(_M):
    value: float
    source: str
    note: str = ""


class MinutesModel(_M):
    read_wpm: float = 238.0          # Brysbaert (2019)
    compose_wpm: float = 20.0        # estimate; see the profession's sources
    friction: float = 1.5            # editing someone else's draft vs writing (assumption, sensitivity-tested)
    rewrite_threshold: float = 0.5   # edit rate above which the worker rewrites
    question_answer_s: float = 30.0  # the worker answering one simulated-worker question, beyond reading it
    overrides: dict[str, float] = {}


class Economics(_M):
    soc: str
    title: str
    median_hourly_wage: Sourced      # OEWS
    eci_factor: Sourced              # wage aging to the run quarter
    loaded_multiplier: Sourced       # ECEC, the employer's sector
    employment: Sourced
    projection: str
    observed_exposure: Sourced
    task_penetration: dict[str, float]   # O*NET task id -> Economic Index penetration
    minutes_model: MinutesModel = MinutesModel()

    @property
    def loaded_hourly(self) -> float:
        return self.median_hourly_wage.value * self.eci_factor.value * self.loaded_multiplier.value


class Meta(_M):
    schema_version: str = SCHEMA_VERSION
    soc: str
    title: str
    onet_version: str = "31.0"
    week_start: str = "2026-11-02"
    status: Literal["draft", "reviewed", "frozen"] = "draft"
    generator: str = ""
    sha256: str = ""


class Episode(_M):
    meta: Meta
    economics: Economics
    employer: Employer
    worker: Worker
    profession_prompt: str
    apps: list[str]
    contacts: list[Contact]
    threads: list[Thread]
    documents: list[Document]
    worker_actions: list[WorkerAction]
    needs: list[Need]
    traps: list[Trap]
    ledger: dict[str, float | str] = {}
    grounding: dict[str, Any] = {}

    @model_validator(mode="after")
    def _refs(self):
        ids: dict[str, str] = {}
        for c in self.contacts:
            ids[c.id] = "contact"
        for t in self.threads:
            ids[t.id] = "thread"
            for x in t.exchanges:
                ids[x.id] = "exchange"
        for d in self.documents:
            ids[d.id] = "document"
        dup = [k for k in ids if list(ids).count(k) > 1]
        if dup:
            raise ValueError(f"duplicate ids {dup[:5]}")
        people = {c.id for c in self.contacts} | {"worker"}
        errs = []
        for t in self.threads:
            if t.app not in self.apps:
                errs.append(f"{t.id}: app {t.app} not in apps")
            for x in t.exchanges:
                for p in [x.author, *x.to, *x.cc]:
                    if p not in people:
                        errs.append(f"{x.id}: unknown person {p}")
                for a in x.attachments:
                    if ids.get(a) != "document":
                        errs.append(f"{x.id}: attachment {a} is not a document")
        for d in self.documents:
            if d.app not in self.apps:
                errs.append(f"{d.id}: app {d.app} not in apps")
        for a in self.worker_actions:
            if a.target not in ids:
                errs.append(f"{a.id}: target {a.target} does not exist")
        for n in self.needs:
            for e in n.evidence:
                if e not in ids:
                    errs.append(f"{n.id}: evidence {e} does not exist")
        for tr in self.traps:
            for e in tr.evidence:
                if e not in ids:
                    errs.append(f"{tr.id}: evidence {e} does not exist")
        if errs:
            raise ValueError("; ".join(errs[:20]))
        return self
