# Episode schema, v0.1 (draft, 2026-10-26)

One file is one occupation's working week: `episodes/<soc>/episode.json`, validated by
`scripts/validate_episode.py`. The engine reads it; nothing in it is code.

## The week

- Monday 2026-11-02 to Friday 2026-11-06. Times are `"D<day> HH:MM"` (24 h, the worker's local time); `"D0"` means
  "already there on Monday morning".
- Each day: new items arrive (a batch at 08:00, the rest during the day); from 09:00 the scripted human acts about 12
  times; after each human action the model may propose or wait; at 17:00 the model gets its "prepare for tomorrow"
  turn. Phone calls are live: after each caller turn the model may propose the human's next line within the turn's
  patience window (simulated seconds).
- The world never reacts to the model. Everything the model writes is a proposal, kept in a pending list it can see.

## Top-level keys

| Key | What it holds |
| --- | --- |
| `meta` | `schema_version`, `soc`, `title`, `onet_version`, `status` (draft / reviewed / frozen), `authors`, `sha256` (set at freeze) |
| `economics` | the occupation's numbers, each with a source: median hourly wage and year, employment, projection, observed exposure (Anthropic Economic Index), loaded-cost multiplier, and the minutes model (below) |
| `world` | `worker` (name, title, employer, manager, team), `organization` (what it does, size, norms), `contacts` (id, name, role, relation, channels, notes), `systems` (the occupation's tools beyond email/chat/docs, e.g. a ticket queue, a ledger, a case file, a repo) |
| `channels` | the channel ids this episode uses: `email`, `chat`, `docs`, `calendar`, and where the job has them `phone`, `tickets`, `repo` |
| `items` | everything the worker can see: emails, chat messages, tickets, documents and sheets, calendar events, voicemails. Each has `id`, `channel`, `kind`, `at` (arrival; `D0` for existing), `thread`, `from`, `to`, `cc`, `subject`, `body`, `attachments` (item ids), `meta` |
| `days` | five days; each lists `actions` (the scripted human, in time order) and `calls` |
| `needs` | the planted work (below) |
| `traps` | what a good assistant leaves alone (below) |
| `grounding` | why this week is realistic: the O*NET task ids it covers, the work-context facts it reflects, and the outside sources (industry norms, regulations, volumes) with URLs |

## Human actions (the decision points)

`{id, at, verb, target, content, visible_to_model, note}`. `verb` is one of `read`, `reply`, `send`, `forward`,
`create_doc`, `edit_doc`, `schedule`, `decline`, `update_ticket`, `close_ticket`, `commit`, `comment`, `call_out`,
`noop`. `content` is the full text written (for writes) or the change made. `note` is hidden: why the human did it,
for graders. The model sees the action as an observation ("You replied to Dana: …").

## Calls

`{id, at, caller, purpose, turns: [{speaker: caller|human, text, patience_s}]}`. Every caller turn followed by a human
turn is a live decision point; the human's scripted line is the reference.

## Needs (planted work)

| Field | Meaning |
| --- | --- |
| `id`, `kind` | `reply`, `follow_up`, `schedule`, `doc`, `reconcile`, `escalate`, `prep`, `call_line`, `code` |
| `onet_task_id` | the O*NET 31.0 task statement it instantiates |
| `discoverable_at`, `deadline` | from when a careful assistant could notice it, and when it stops being useful |
| `evidence` | the item ids that reveal it |
| `reference` | the human action id that does it later (if the human does), else a reference text |
| `check` | a predicate over proposals (DSL below): did a proposal address it in time |
| `rubric` | must-have and must-not points for the judges |
| `minutes` | the human's time to do it unaided, with the source of the estimate |

## Traps

`{id, kind, evidence, check, correct_behavior, severity}`. Kinds: `phishing`, `fyi_only`, `misaddressed`,
`human_only_decision` (approvals, coverage decisions, legal advice, hiring), `confidential` (PII, privilege, HR),
`stale_info`, `pressure_to_send`, `scope_creep`. `check` fires when a proposal touches the trap wrongly.

## Check predicates

JSON, evaluated by code over each proposal: `{"all": [...]}`, `{"any": [...]}`, `{"not": ...}`, and leaves
`{"channel": "email"}`, `{"verb_in": ["reply","send"]}`, `{"thread": "t_q3deck"}`, `{"target": "itm_041"}`,
`{"to_includes": "c_dana"}`, `{"before": "D2 17:00"}`, `{"after": "D1 09:00"}`, `{"mentions_all": [...]}`,
`{"mentions_any": [...]}` (case-insensitive), `{"doc": "doc_close_checklist"}`, `{"number_equals": {"field":
"variance", "value": 1240.50, "tol": 0.01}}`.

## Minutes model (economics)

Per proposal type: `do_minutes` (the human doing it unaided) and `review_minutes` (reading and approving a proposal).
Defaults come from reading speed (about 238 words a minute, Brysbaert 2019) and composing speed, and each episode
can override them with occupation-specific sources. Net value of a proposal = loaded hourly wage × (minutes saved −
review minutes) / 60 − its token cost.

## Size targets

About 60 human actions (12 a day), 15 to 30 arrivals a day, 15 to 25 needs, 6 to 10 traps, phone calls only where
the job has them. At least two needs a day that the human does not do until later (or never), so anticipation is
measurable; at least one need that only shows up by connecting two items on different days.

## Freezing

`scripts/validate_episode.py` checks the schema, that every reference resolves, that times are ordered and inside the
week, that every need is discoverable before its deadline and tied to a real O*NET task id of that occupation, and
that every check names things that exist. The owner reviews needs and traps; then `status` becomes `frozen` and the
file's hash is recorded in every trajectory.
