# Design, v1 (2026-10-27)

This replaces `architecture.md` and `episode-schema.md` (kept for history). It is the design the code is being
built to. Decisions are marked with who made them; open defaults are listed at the end.

## 1. Question and measures

How much of a profession's ordinary work can an AI assistant, working unprompted next to the worker, do well enough
that the worker accepts it, what is that worth in dollars net of review, fixes, mistakes and tokens, and how fast is
it changing across model releases? Two analyses:

- **Pace, by profession:** net value per worker-week and press-enter rate against release date, per lab and pooled;
  a doubling time fitted as in METR's time-horizon work (log metric on release date, bootstrap intervals).
- **Capability against usage, by task:** every need is tied to an O*NET task; its success rate is compared with
  that task's observed AI usage (Anthropic Economic Index task penetration), with profession as a grouping effect.

## 2. Pipeline

```
professions/<soc>/profession.yaml   (written by a person: job, employer, storyline, scale)
        |  workweek.compile
        v
build/<soc>/episode.json             (generated, validated, frozen by hash)
        |  workweek.engine (Inspect AI task)      config/run.yaml (models, judges, user model, cadence)
        v
logs/<run>/                          (Inspect transcripts + proposals.jsonl)
        |  workweek.grade
        v
results/<run>/                       (graded proposals, need outcomes, value, tables, figures)
```

Human-written inputs are YAML (the profession form, the run config). Generated artifacts are JSON validated by
Pydantic models (`workweek/schema.py`), which also export a JSON Schema.

## 3. The profession form (`professions/<soc>/profession.yaml`)

```yaml
soc: 43-4051.00
employer: {name: Northbeam Fiber, industry: telecommunications, size: 900, location: "Salem, OR", timezone: America/Los_Angeles}
worker:   {name: Marisol Ortega, title: Customer Care Specialist II, manager: Dana Pruitt, team: Residential Care}
profession_prompt: |      # what good help looks like in this job; goes to the assistant and to the judges
  ...
apps: [mail, chat, calendar, docs, phone, tickets, records, contacts]
scale: {needs_per_day: 20, human_actions_per_day: 30, threads_per_day: {mail: 12, chat: 10, tickets: 18, phone: 14}}
storyline:
  arcs: [...]               # the week's one or two arcs
  days: {mon: ..., tue: ..., wed: ..., thu: ..., fri: ...}
policies: [identity verification, credits and refunds authority, cancellations, outages, escalation tiers]
sources: [ ... ]            # URLs the storyline rests on
```

The 11 existing drafts become the first 11 forms: their arcs, worlds and `research.md` are the storyline and sources.

## 4. Compiler (`workweek/compile`)

One function, `compile_profession(form) -> Episode`, the same for every profession:

1. **Enrich** (no LLM): O*NET 31.0 task statements with frequency and importance ratings and work context; BLS
   wages (OEWS May 2025 via O*NET OnLine) aged to the run quarter with the ECI; the loaded-cost multiplier from ECEC
   for the employer's sector; observed exposure and per-task penetration (Economic Index); reading and composing
   speeds.
2. **Plan** (no LLM): allocate the week's needs to O*NET tasks in proportion to frequency x importance, and to days
   and apps by the form's scale; place traps; lay out thread and call slots, human-action slots and arrival times.
   Because the allocation is computed from O*NET ratings, the task-mix part of the realism check is true by
   construction and reported.
3. **Numbers** (no LLM): a ledger of every figure a need's check depends on, computed in code (sums, dates, deadlines
   with business-day and holiday rules), so the prose cannot contradict the check.
4. **Draft** (LLM, `generator_model` in the run config): fills each slot, day by day and app by app, with structured
   output into the schema, given the form, the plan, the ledger and a running world bible (people, threads, facts so
   far). Each need also gets the worker's private intent ("what I would do and why"), used by the simulated worker.
5. **Validate and self-test:** schema; every reference resolves; times ordered; needs discoverable before deadline;
   O*NET ids belong to the profession; ledger figures appear where they must; the shared check evaluator passes every
   need on its reference action and fires no trap on any human action.
6. **Realism report** ((a) and (b), owner 10-26): a sample of 20 cited claims per profession for a source audit, and
   the week's volumes and task mix next to outside references (O*NET ratings, Microsoft Work Trend Index, job
   benchmarks such as handle time, the Enron corpus's arrival rhythm).
7. **Freeze:** the episode's sha256 goes into every run log.

## 5. The world: apps, threads, documents

An app is a plug-in class registered by name (`workweek/apps/`); adding a service is one new class.

- **Thread apps** (mail, chat, phone, tickets, news, repo pull requests): an app holds threads; a thread holds
  exchanges (author, time, body, attachments); threads are addressed by a path whose `/` segments bucket them
  (`chat/#ops/peak-staffing`, `mail/inbox/billhold-po-77412`). Thread ids are slugs, separate from display names.
  `live: true` marks a thread whose exchanges arrive faster than the tick (a phone call).
- **Document apps** (docs and sheets, calendar, records, contacts, repo files, policies): an app holds documents with
  a state and versions.
- Every app renders to files in the sandbox, so the model uses ordinary commands:

```
/inbox/unread.md            unified feed: new items and worker activity since the model last listed it, each with its path
/mail/<path>/<thread>.md    /chat/<path>/<thread>.md    /tickets/<queue>/<id>.md    /news/<source>/<id>.md
/phone/<call>/transcript.md (live while the call runs)  /calendar/<yyyy-mm-dd>.md   /docs/<path>  (md, csv, xlsx)
/records/<system>/<id>.json /contacts.csv               /policies/*.md              /repo (a real git repository)
/home/assistant/            writable: memory and scratch files, kept across days
```

Size per day (defaults, scaled per profession by the form): about 30 mail threads (2.5 messages on average, at least
1), 15 chat threads (at least 2 messages), 6 calendar events, 3 to 6 documents changed, tickets and calls where the job
has them (a call has at least 6 turns), about 30 worker actions and 20 needs; most threads and most ticks are no-op
opportunities.

## 6. The engine (`workweek/engine`, an Inspect AI task)

- **Clock:** simulated. Days run 08:00 to 17:00 plus a 17:00 "end of day" tick; the model gets a tick every
  `cadence_minutes` (config, default 5). Each tick: the engine applies arrivals and worker actions up to the tick
  time, writes them into the sandbox, and runs the agent. Between ticks nothing calls the model.
- **Agent:** a multi-turn tool-using agent per tick, ending at `wait()` or after `max_tool_calls_per_tick`.
  Tools:
  - `bash(cmd)`: a Docker sandbox, network off, the world mounted read-only and `/home/assistant` writable; `python3`
    available (with csv and openpyxl) for arithmetic and sheets.
  - `propose(target, action, drafts, note)`: the only way to reach the worker. `target` is a path; `action` is
    reply, new, edit, schedule, update or say; `drafts` holds 1 to 3 alternatives in the model's order of preference.
    Nothing is delivered; the proposal is stored with its time.
  - `ask_worker(question)`: answered by the simulated worker (below).
  - `join_call(path)` / `leave_call()`: while joined, the model gets a turn after every caller exchange of that
    call instead of waiting for the tick; outside calls the cadence applies.
  - `wait()`: ends the tick.
  - `send(...)`: only in the optional overreach arm, where the instructions say to draft only; intercepted.
- **System prompt:** our fixed harness instructions (how the world is laid out, the tools, that proposals are the
  only output, that memory persists, that waiting is a normal and good choice) followed by the form's
  `profession_prompt`.
- **Context:** one conversation per day; each morning starts from the system prompt plus a short summary of the
  date; whatever the model wants to keep it keeps in `/home/assistant/`.
- **Simulated worker (`user_model`, owner 10-26: Gemini 4 Argon):** answers `ask_worker` in character, from the
  worker's persona, the visible world and the private intent notes, briefly, as a busy colleague would; it does not
  volunteer more than asked. Every exchange costs the worker's attention (reading the question plus writing the
  answer) in net value.
- **Coverage report (before a run):** for the chosen cadence, the share of need windows and call turns the model can
  reach; a warning below a threshold; grading uses only reachable opportunities.
- **Logs:** Inspect's transcripts (every tool call, every model message, token usage per call) plus
  `proposals.jsonl` (proposal, time, the world state version it saw).

## 7. Grading (`workweek/grade`, offline)

1. **Code checks** with one shared evaluator: whole-word, case-insensitive, numbers normalized (`$`, commas,
   trailing zeros); `number_equals` compares every number in the draft with the value within `tol`. A need is met
   when a matching proposal (any draft) lands inside its window; a trap fires when a matching proposal exists.
2. **Judges.** Each proposal is graded by every judge in the panel. The prompt is our fixed base instructions, the
   same `profession_prompt` the assistant saw, the context visible at the proposal's time, all drafts, and the
   need's rubric and the worker's own version when the proposal matched a need. Output:

   ```json
   {"score": 0-100,            // probability a competent worker would send the best draft unchanged
    "best_draft": 1,
    "harm": false,             // acts on a trap, leaks, oversteps authority
    "rubric_hits": [], "rubric_misses": [],
    "reasons": ["at most two, at most 25 words each"],
    "minimal_fix": "..."}       // the smallest edit of the best draft that makes it sendable; empty if none needed
   ```

3. **Panel score:** the weighted mean of judges' scores (weights in the config, summing to 1); with
   `report_with_dropout`, the tested model's own family's judge is dropped and the weights renormalized. The median
   is reported as a robustness check, with Krippendorff's alpha, the pairwise matrix and self-preference.
4. **Edit effort:** word-level edit distance between the best draft and its minimal fix (insertions, deletions,
   substitutions, block shifts), as in HTER, but against the *minimal sendable* version, not against what the worker
   would have written, so "kinda the same" costs nothing. Fix time = edits / composing speed x friction, capped at the
   time to write from scratch; above an edit rate of 0.5 the worker is assumed to rewrite. Friction (default 1.5)
   and the 0.5 threshold are assumptions with a sensitivity analysis. Validated against the owner's own edits on
   about 30 proposals.
5. **Value:** per proposal, loaded wage x (need minutes x p - reading time of every draft - (1 - p) x fix time) -
   token cost, with p the panel score / 100; a fired trap costs at least reading plus fixing (a severity-weighted
   upper bound in a sensitivity table); questions cost the worker's attention; unplanned proposals earn nothing but
   cost their reading (their usefulness is reported separately).
6. **Latency (offline):** per model, time to first token (p50) + output tokens / throughput, from OpenRouter's
   published stats entered in the run config. Used to decide whether a call line would have arrived in time.
7. **Hand grades:** about 100 proposals stratified by profession, family and judge disagreement, graded in the same
   format; agreement (Cohen's kappa on thresholded scores, correlation on scores) for each judge and the panel.

## 8. Metrics and figures

Per model and profession: net value per worker-week; press-enter rate (mean p) on the best draft and on the first
draft; drafts per proposal; recall of needs and anticipation (hours before the worker); traps fired; questions and
their cost; wasted tokens and dollars on ticks that end in no proposal; token cost per accepted proposal; policy
consultation (opened a relevant `/policies` file before proposing); day-over-day improvement; pass^k across seeds;
call lines in time.

Figures: value per worker-week against release date by lab with the doubling time; task-level success against
observed usage; traps against capability; cost against value by release date; anticipation lead times.

## 9. Run config (`config/run.yaml`)

```yaml
run: {cadence_minutes: 5, seeds: 3, max_tool_calls_per_tick: 25, send_arm: false, professions: all, eci_factor: 1.034}
generator_model: {model: "openrouter/google/gemini-4-argon", reasoning_effort: medium}
user_model:      {model: "openrouter/google/gemini-4-argon", reasoning_effort: medium}
models:
  - name: Claude Opus 5.5
    model: "bedrock/global.anthropic.claude-opus-5-5"   # passed to Inspect as is
    family: anthropic
    released: 2026-09-22
    generate: {reasoning_effort: medium}
    price: {input: 4.00, output: 20.00, cache_read: 0.20, cache_write: 5.00}   # USD per million tokens
    speed: {ttft_p50_s: null, throughput_tps: null}                            # from OpenRouter, entered by hand
judges:
  - {model: "openrouter/google/gemini-4-argon", family: google, weight: 0.142857, report_with_dropout: true}
```

`workweek.config.load()` refuses a config whose judge weights do not sum to 1, whose families are unknown, where a
dropout leaves no weight, where a model string has no provider prefix, where prices or speeds are missing, or where
a route's credentials are absent.

## 10. Defaults still open (owner can change any)

- Seeds: 3 (the pilot decides).
- `max_tool_calls_per_tick`: 25; per-tick output cap 16k tokens.
- Generator model: Gemini 4 Argon (outside every tested family).
- Rewrite threshold 0.5 and edit friction 1.5.
- Unplanned proposals: zero value (conservative), usefulness reported separately.
