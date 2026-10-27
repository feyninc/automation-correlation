# Design, v2 (2026-10-27)

What is built, how it fits together, and what is still open. v1 planned an LLM generator for the weeks; v2 replaces it
with hand-written weeks and a deterministic compiler (owner, 10-26: "I want you to write the episodes").

## 1. Question and measures

How much of a profession's ordinary work can an AI assistant, working unprompted next to the worker, do well enough
that the worker accepts it; what is that worth in dollars net of reading, fixes, mistakes, questions and tokens; and
how fast is it changing across model releases?

- **Pace, by profession:** net value per worker-week and press-enter rate against release date, per lab and pooled,
  with a doubling time fitted on log value against release date (bootstrap intervals), as in METR's time-horizon work.
- **Capability against usage, by task:** every need is tied to an O*NET task; its success rate is compared with the
  task's observed AI usage (Anthropic Economic Index task penetration), with profession as a grouping effect.

## 2. Repository

| Path | What it is |
| --- | --- |
| `professions/<name>/` | one profession: `week.yaml` (job, people, policies, standing documents) and `day1.yaml`..`day5.yaml` (what happens each day), written by hand; `episode/` (compiled: `profession.json` plus one JSON per date) and `report.md` (build report), generated |
| `workweek/` | `schema.py` (Pydantic models), `compile.py` (forms to episodes, the audit), `apps.py` (the world as files), `world.py` (events, feed, ticks), `engine.py` (the Inspect AI task), `prompts.py`, `checks.py` (the shared check evaluator), `grade.py` (offline grading), `config.py`, `creds.py`, `providers.py`, `sandbox/` (Docker image) |
| `config/run.yaml` | models, prices, judges and weights, the simulated worker, run settings |
| `scripts/` | `run.py` (run models x professions over a window), `smoke_models.py` (one tool call per route), `probe_reasoning.py`, `timeline.py` (release timeline and model set), `screen_occupations.py` |
| `data/` | O*NET 31.0, Economic Index tables, BLS wages via O*NET OnLine, ECEC June 2026 multipliers, the ECI factor, release timelines, probe outputs (`data/README.md`) |
| `logs/`, `results/` | run output (git-ignored) |

## 3. Professions

Eleven O*NET 31.0 occupations across observed exposure (0.07 to 0.70). Each is one working week, Monday 2026-11-02
to Friday 2026-11-06, at a fictional employer with real rules, regulators, standards and software.

| Profession (SOC) | Employer and arcs | Needs | Need minutes | Traps | Worker actions | Calls | Words |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Customer service (43-4051) | fiber ISP: outage, credits batch error, cancellation script change | 101 | 233 | 20 | 115 | 22 | 11,626 |
| Market research (13-1161) | B2B SaaS: survey cleaning to readout, launch, accruals | 73 | 971 | 21 | 103 | 0 | 9,079 |
| Admin assistants (43-6014) | engineering firm: ops review and site tour, travel, legal hold | 72 | 320 | 17 | 97 | 9 | 6,919 |
| PR specialists (27-3031) | hospital system: embargoed gift, ER-death inquiry | 65 | 573 | 17 | 101 | 3 | 7,793 |
| Accountants (13-2011) | distributor: October close, bank rec, cutoff, bill-and-hold | 47 | 563 | 17 | 77 | 1 | 5,347 |
| Paralegals (23-2011) | law firm: federal discovery, deadlines, privilege log | 45 | 419 | 10 | 58 | 5 | 4,924 |
| Software developers (15-1252) | billing SaaS: DST bug, review, CVE, incident | 40 | 752 | 12 | 74 | 0 | 5,230 |
| Event planners (13-1121) | association: conference guarantees, attrition, event day | 35 | 305 | 7 | 56 | 3 | 3,281 |
| Operations managers (11-1021) | distribution center: OSHA, FLSA, FMLA, peak staffing | 33 | 403 | 9 | 55 | 1 | 3,885 |
| Claims adjusters (13-1031) | Texas auto: Stowers demand, hail total loss, SIU | 31 | 362 | 7 | 49 | 3 | 3,393 |
| Budget analysts (13-2031) | state agency: allotments, fiscal note, grant rates | 25 | 474 | 7 | 42 | 0 | 3,063 |
| **Total** | | **567** | **5,375** | **144** | **827** | **47** | |

Need counts differ more than workload: call-heavy jobs have many one-line needs (a spoken answer is 0.3 minutes),
analyst jobs fewer, larger ones (a readout deck is 180 minutes). Need minutes, not counts, are the comparable size
measure; the planned ~100 needs per week was reached only for customer service (owner's target, 10-26; see section 10).

### The form

`week.yaml` holds the job and everything true on Monday morning; each `dayN.yaml` holds that day's documents,
threads, calls, the worker's actions, needs and traps. Lists from all files are concatenated. A later file can
continue an earlier thread (same id, new exchanges, optional state change) or add a version of an earlier document
(same id, `at` and `content`).

- **Threads** (`app`, `path`, `title`, `x`: exchanges with `at`, `from`, `to`, `cc`, `subject`, `body`, `att`).
- **Calls** (`turns`: speaker, line, the caller's patience in seconds); turn times follow from 150 spoken words a
  minute. A need for one of the worker's lines gets its window from the turns: from the caller turn it answers to just
  before the caller speaks again.
- **Worker actions** (`read`, `reply`, `new`, `forward`, `edit`, `update`, `noop`, ...): a reply or edit with a body
  becomes part of the world when it happens, so the model sees what the worker did; `update_state` changes a ticket's
  state at that time.
- **Needs**: id, O*NET task, window (`from`, `due`), evidence, a reference (`ref` to the worker's own action or call
  line, or `ref_text` when the worker never does it), the code check, the rubric (`must`, `must_not`), minutes to do it
  unaided with their basis, and the worker's private intent (used only by the simulated worker). An intent is what
  the worker thinks when the need appears: no hindsight about later days, and the method rather than a computed
  answer (a 10-27 review removed five hindsight intents, one of which gave away a need's answer, and five computed
  credit amounts; 10 of 567 intents still contain a number a check needs, all facts the worker was told).
- **Traps**: a check that fires on a harmful proposal, the correct behavior, severity, an optional dollar bound with
  its source, and `worker_mistakes` (the worker's own actions the trap is allowed to match).

No rule is planted to make a case decidable by lookup alone: the policies are the employer's ordinary ones, and the
cases turn on reading the facts against them (owner, 10-26).

### Compiler and audit (`python -m workweek.compile professions/<name>`)

Expansion adds O*NET tasks (importance, frequency), economics (OEWS median wage, the ECEC loaded-cost multiplier for
the form's `ecec_sector`, the ECI factor, observed exposure, per-task penetration) and resolves every reference. The
audit fails the build on:

1. a need's O*NET task not among the occupation's tasks; a check naming a missing thread or contact;
2. a need whose check does not pass on its own reference: the worker's action, the worker's call line, or (for the
   mention and number parts) its reference text;
3. a trap that fires on any worker action, except listed worker mistakes;
4. two threads or documents that render to the same file; a thread in a document app or the reverse;
5. a split/merge round trip that changes the episode (the per-day JSON must rebuild the same episode).

The build report lists counts per day and app, the task mix against O*NET frequency and importance, and warnings.
A separate findability check (run during the build-out) looked for identifiers and numbers a need's check expects that
appear nowhere the model could see before the deadline; it found one real gap (a deductible known only from the
worker's call), now fixed, and otherwise only derived figures.

### Where the facts come from

Every week was researched from primary sources (statutes, regulations, standards, vendor and regulator pages), listed
in `week.yaml` under `sources`. Facts a trap or need turns on were checked again while writing, for example: the IRS
mid-2026 mileage change (72.5 to 76 cents, irs.gov), GSA FY2027 per diem rates (api.gsa.gov), Texas Insurance Code
542.051-.057 and Government Code 662.003 (Veterans Day), the urllib3 advisory GHSA-vxq7-64xx-v4gw / CVE-2026-97689
(api.osv.dev), PyPI dependency ranges, and that `fastapi-idempotency-middleware` is not on PyPI. Code in the developer
week was run: the planted bugs fail the new tests and the fixes pass. Numbers inside each story (counts, sums,
prorations, deadlines) were computed by script and are shown in each day file's header comment.

### Realism and scale

A worker in Microsoft 365 receives about 117 emails and 153 chat messages a day (Microsoft Work Trend Index 2025).
The weeks carry 6 to 19 inbound items a day (mail, chat, tickets, calls and new or updated documents; claims adjusters
6.6, customer service 19.4, mean 11.4), about one-fifteenth to one-forty-fifth of that, keeping every item that
carries work or risk plus some noise. Worker actions are the visible outputs (8 to 23 a day, against the ~30 planned),
not every keystroke; calls and meetings the model cannot see appear as `noop` actions in the feed. The planned work is
0.8 to 3.2 hours of each 8-hour day, so value is per benchmark week, not per worker-week (section 10).

## 4. The world (`workweek/apps.py`)

An app is a registered class; adding a service is one class. Thread apps: `mail`, `chat`, `tickets`, `phone`, `news`,
`reviews` (pull requests). Document apps: `docs`, `calendar`, `records`, `policies`, `contacts`, `repo`. Everything
renders to read-only files under `/world` at the current simulated time (ticket state as of that moment, the latest
version of each document; a call's turns, then the worker's case note), plus `/world/contacts.csv`,
`/world/inbox/new.md` (what changed since the last check, including what the worker did) and `/world/inbox/feed.md`
(the day so far). `/home/assistant` is writable and kept all week. The developer week's repository is runnable:
`python3 -m unittest` after copying it to `/home/assistant`.

## 5. The engine (`workweek/engine.py`, an Inspect AI task)

- **Clock:** simulated, from the worker's arrival to departure each day (`worker.hours`, default 08:00 to 17:00), a
  tick every `cadence_minutes` (default 5), the departure tick an end-of-day turn. Before each tick the engine writes
  the world as of that moment. Nothing waits on a model: the clock stops while it works, and every timing question
  (did a call line arrive in time?) is answered offline in grading from the tokens it used.
- **Agent:** one conversation per day; each tick is a multi-turn tool loop ending at `wait` or after
  `max_tool_calls_per_tick` (25). Tool output older than 6 ticks is elided. Tools: `bash` (Docker, no network,
  non-root), `propose(target, action, drafts[1-3], note)` with actions reply, new, forward, edit, schedule, update,
  say and flag (a new or forwarded message must name its recipients); `ask_worker(question)`; `join_call(path)` /
  `leave_call()` (a turn after every caller line while joined; a model that joins before the worker answers the
  caller's last line gets that line first); `wait()`. A call ends at its last spoken turn; a case note written
  afterwards does not keep it live.
- **System prompt:** fixed harness instructions plus the profession's `profession_prompt` (`workweek/prompts.py`).
- **Simulated worker** (`user_model`, Gemini 4 Argon, owner 10-26): answers `ask_worker` in at most three sentences.
  A fixed system prompt (`WORKER_SYSTEM`: stay in character, answer only what was asked, use only what the case says,
  claim an action only if the activity shows it) and a case (`WORKER_CASE`: `<you>` the worker, employer, moment and
  profession prompt; `<your_views>` the intents of the needs discoverable by then; `<what_has_happened>` the last 25
  feed lines; `<question>`). Each question costs the worker reading plus `question_answer_s` (default 30 s).
- **Output:** proposals, questions and tick counts in the sample metadata of the Inspect log, with token usage per
  call.

## 6. Grading (`python -m workweek.grade logs/<run>`)

1. **Matching** with the shared evaluator (`workweek/checks.py`): whole words, case-insensitive; numbers normalized
   ($, thousands commas, trailing zeros; "320" does not match "3,200"); `number_equals` within a tolerance; a proposal
   matches if any draft does. Action names are normalized per app (anything added to a thread is a reply, a line on a
   call is say, anything changing a document is an edit; flag, new, forward and schedule keep their names). A need is
   earned by the last matching proposal inside its window, and one proposal can earn several needs (see "Crediting
   work" below); a trap fires on any matching proposal.
2. **Judges:** a panel of seven from seven families (weights in the config, summing to 1). Each judge gets a fixed
   system prompt (`JUDGE_SYSTEM`: what is graded and how, the parts of the case, the checklist, the score bands, the
   reply format) and one case per proposal (`JUDGE_CASE`), in labeled parts so judging is reading, not searching (see
   "Making judging easy" below): `<job>` the person, moment and profession prompt; `<proposal>` the target, action and
   drafts; `<planned_work>` for every need the proposal matches, its must and must-not and the worker's own version;
   `<open_work>` the planned work open then and whether the worker had done it; `<already_done>` what the worker and
   the assistant had done on the matter; `<draft_facts>` every number, identifier, date, email and named person in the
   drafts, looked up in the world as of that moment; `<files>` the target, evidence and the last 12 files the model
   opened (long files keep their head and the lines sharing an identifier with the drafts; 30,000 characters). No
   tools: one call per judge per proposal. Output: a checklist (needed, right place, facts correct, within authority,
   complete), then score 0-100 (the probability the worker sends the best draft unchanged) bounded by the checklist,
   best draft, harm, rubric hits and misses, two short reasons, the minimal fix.
3. **Panel score:** each judge's score less its offset (its mean deviation from the other judges on the same
   proposals, over the whole run), then the weighted mean with the tested model's own family left out
   (`report_with_dropout`). The uncalibrated and full-panel means and the median are kept beside it; offsets are
   written to `results/<run>/judge_offsets.json`.
4. **Edit effort:** word-level edit distance from the best draft to its minimal fix (the HTER count without block
   shifts), against the minimal sendable version, so acceptable wording costs nothing; fix time = edits / composing
   speed x friction (1.5), capped at writing from scratch; above an edit rate of 0.5 the worker rewrites. The best
   draft and the minimal fix are the heaviest remaining judge's after dropout.
5. **Value:** loaded wage x (minutes of the needs it earns x p - reading time - (1 - p) x fix time) minus the
   proposal's share of the tested model's token cost, with p = panel score / 100. Reading is every word of every
   draft, or for a revision only the words that changed, plus an attention cost for every proposal shown (10 s for a
   written proposal, 3 s for a call line; below); unplanned and superseded proposals cost their reading and attention;
   each question costs its reading plus `question_answer_s` at the loaded wage. The simulated worker's tokens are
   recorded separately and not charged to the model.
6. **Call timing (offline):** a line proposed on a call counts only if it would have reached the worker in time. The
   engine records, with each proposal, the output tokens of every model call since the caller's line and the time
   its tools took; the grader converts tokens to seconds with the model's p50 time to first token and throughput on
   its route (`scripts/speed.py`, OpenRouter's endpoint stats, `data/openrouter/speed-<date>.csv`), adds the worker
   reading the line's first 10 words, and compares with the caller's patience (strict) or the caller's line plus
   patience (streaming, as if the assistant heard the line as it was spoken: an upper bound). A late line is dropped
   before the worker sees it, as any assistant would once the worker has started answering: it earns no need and
   costs nothing but its tokens (`value_if_shown` keeps what it would have cost if shown anyway, for sensitivity);
   traps still fire on it, since they measure what was proposed. Provider-neutral speeds rather than our own
   wall clock keep queueing and retries on our routes (Bedrock's 503s, Azure's slow DeepSeek) out of the measure.
7. **Attention:** every proposal shown costs time beyond reading it, whether accepted or not (agents ignored 62% of
   AI suggestions in Brynjolfsson, Li and Raymond 2023). Written proposal: 10 s (4-60 s for sensitivity), from about
   2 s to notice and switch to the mail client (Iqbal and Horvitz 2007: 2.35 s to Outlook after an alert), 2-6 s to
   decide beyond reading (Mozannar et al., AI-assisted programming: 6.11 s from a suggestion to accepting or rejecting
   it; 6.48 s median with later verification) and 2-4 s to resume the interrupted task (Altmann and Trafton 2004:
   resumption lag 3.8 s against 1.9 s between actions). Call line: 3 s (1-8 s), no switch (the worker is watching the
   panel) but a decision inside turn gaps of about 200 ms (Levinson and Torreira 2015). The popular "23 minutes to
   refocus" is in neither of Mark's papers; Mark, Gonzalez and Harris 2005 measured 25 minutes until people returned to
   an interrupted task, doing other work meanwhile.

### Making judging easy, and what it bought

Judges do not see the episode's history or the model's notes, and should not have to: a draft is right or wrong
against the world, whatever the model's process. So the packet hands them what checking needs.

- **Draft facts:** every identifier (claim and account numbers, emails, dates, times), amount and person in the drafts,
  located deterministically in the world as of the proposal (file and line), or marked as in the worker's own version
  (computed), or as found nowhere (computed from other figures, or invented). Where a fact came from (a file read days
  earlier, the model's notes) no longer matters.
- **Open work and history:** the planned work open at that moment with whether the worker had done it, and what the
  worker and the assistant had already done on the matter, so "already done" and "duplicate" can be judged at all.
- **Checklist before the score**, with the score bounded by it (not needed: 0-9; wrong place, facts or authority: at
  most 49 unless the fix is a few words).

Measured on the same proposals graded with the old and the new prompt (63 from the claims sample, 40 from six models
in the customer-service sample): agreement on accept (score at least 50) stayed at Fleiss kappa 0.34-0.44 and the
typical spread across judges barely moved, while judges became 4-8 points stricter. Where old and new grades differed
most, the new ones were right: a draft naming a caller with an email the draft-facts lookup located on another
customer's account fell from 60 to 2; a QA dispute that was Marisol's planned work rose from 27 to 69. So the packet
buys validity, not agreement, at about 60% more judge cost ($0.16 a proposal against $0.10).

The disagreement that remains is mostly in level, not ranking: each judge correlates 0.72-0.94 with the mean of the
other six, and with judges' offsets removed the seven-judge panel's reliability is ICC(3,k) 0.90-0.94. The offsets
are large (Claude Opus 5.5 about -12 points, Kimi K3 +8, GLM-5.3 +6), which made leaving out the tested family shift
scores by family: Claude models +1.8 points, Kimi -1.4, GLM -1.0. Calibrating offsets over the run removes it
(-0.2, -0.1, 0.0). Remaining checks: hand grades for accuracy, and agreement on the full run.

### Crediting work, and why

A large need (a variance report, a readout deck) is open for days, and the model has a turn every 5 minutes, so it
can draft, come back and revise. How proposals are credited decides whether that is rewarded, so the rules are
stated here with their reasons.

1. **The last version before the deadline earns the need.** Earlier matching proposals are superseded: they still
   cost the worker their reading and are judged (so improvement across versions can be measured), but earn nothing.
   - *Not the first match:* that rewards a fast rough draft and penalizes revision, which is how people produce
     large deliverables. Under first-match, a model that sends a thin letter at 11:10 and the full one at 11:40 is
     valued on the thin one.
   - *Not the best match:* picking the best by the judges' scores is hindsight the worker does not have. It would
     let a model hedge by proposing many variants and be credited with the luckiest, while the worker cannot tell
     which to send without reading them all.
   - *The last version* is what a worker would act on: a newer draft of the same thing replaces the older one. The
     model is responsible for its own final answer, so a late regression costs it. Revising is not free: every
     version is read.
   - The first and the earning version are both recorded (`first_proposal`, `proposal`, `versions`), so lead time can
     be reported for either.
2. **One proposal can earn several needs.** Needs are units of work, not of messages. Maribel's one escalation email
   both escalates the demand and requests the reserve increase, two needs. Crediting one need per proposal would
   reward splitting the same work into more messages, a formatting choice rather than more help. The proposal's
   value adds the minutes of every need it earns; its reading and fix time count once, since there is one draft.
3. **A revision costs only the reading of what changed.** A worker re-reading a revised draft reads the changes, as
   with tracked changes. Charging a full re-read for every version would over-penalize revision. A proposal revises
   the latest earlier one that matches a same need, or that takes the same action on the same file; its reading is
   the words of each draft not found in the closest earlier draft (inserted or replaced words in a word-level diff).
4. **Large items stay whole.** They are not split into milestones. The value of a deliverable is realized when the
   worker can send it; a milestone no one can send has no value of its own, and splitting would inflate need counts
   without adding work. Partial progress still counts through the fix time: a draft that needs work earns the need's
   minutes x p minus the expected fixing, and above an edit rate of 0.5 the worker rewrites.

Limits: the model cannot mark a version as final, so a revision proposed only to explore an alternative supersedes
the earlier one. A line said on a call is never a revision: each is a new turn in the conversation, read in full.

Outputs: `results/<run>/graded.jsonl` (every proposal, need outcome, judgment and value) and `summary.csv` (per model
and profession: ticks, proposals, questions, needs caught, traps fired, press-enter rate, value, token cost).

## 7. Models, routes and reasoning (`config/run.yaml`)

27 models: each lab's main line, the model in force on 2026-01-01 and every release since (OpenAI GPT-5.2 to 6.1 Sol;
Claude Opus 4.5 to 5.5; Kimi K2 Thinking to K3.1 Pro; DeepSeek V3.2 to V4.1 Flash 1017; GLM-4.7 to 5.3), from
`scripts/timeline.py`. Routes: OpenAI's API for GPT; Bedrock for Claude and GLM-4.7/5; Azure Foundry for DeepSeek and
Kimi where offered; OpenRouter with a pinned provider and no fallback otherwise. Every model runs at its lab's
medium reasoning setting, set on every call (owner, 10-26):

| Model (route) | Default, observed | Medium is sent as |
| --- | --- | --- |
| GPT-5.2, 5.4 (OpenAI) | no reasoning | `reasoning_effort: "medium"` |
| GPT-5.5, 5.6 Sol, 6 Sol, 6.1 Sol, 6 Astra (OpenAI) | reasoning | same |
| Opus 4.5 (Bedrock) | no thinking | effort beta, `effort: "medium"`, thinking with an 8,000-token budget |
| Opus 4.6 to 5.5 (Bedrock) | 4.6-4.8 no thinking; 5, 5.5 adaptive | adaptive thinking, `effort: "medium"` |
| DeepSeek V3.2 to V4.1 Flash (Azure) | no thinking | `reasoning_effort: "medium"` |
| Kimi K2.5, K2.6 (Azure) | thinks | `reasoning_effort: "medium"` |
| Kimi K2 Thinking, K3, K3.1 Pro; DeepSeek V4.1 Flash 1017 (OpenRouter) | thinks | `reasoning: {effort: "medium"}` |
| GLM-4.7, GLM-5 (Bedrock) | thinks only at high | `reasoning_effort: "high"` (GLM thinking is on/off; `workweek/providers.py` passes it, which Inspect's Bedrock route did not) |
| GLM-5.1 to 5.3, Gemini 4 Argon, Qwen3.8 Max Prime (OpenRouter) | varies | `reasoning: {effort: "medium"}` |

Evidence: `scripts/probe_reasoning.py` asked each model one short scheduling question on its own route with no setting
and at low, medium and high (`data/reasoning-probe*.csv`). That shows whether thinking is on and the setting accepted;
it does not measure how much a model thinks on real work. Caveats:

- "Medium" is each lab's own word, not a common unit. Anthropic's effort default is high, so medium is a step below
  Anthropic's default but OpenAI's default from GPT-5.5 on.
- Adaptive thinking decides per call: at medium Opus 4.6 thought on the probe, Opus 4.7 did not at any level.
- GLM has only thinking on or off (Z.ai's API), so its "medium" is "thinking on". On Bedrock `reasoning_effort` low and
  medium leave it off and high turns it on (`data/reasoning-probe-glm.csv`); Z.ai's own `thinking: {type: enabled}`
  is ignored there.
- DeepSeek documents low, high and max for V4; what Azure does with medium is not documented.
- Defaults differ even by host (DeepSeek V4.1 Flash thinks by default on DeepInfra, not on Azure), so a setting is
  always sent.
- Reasoning token counts are not comparable across routes: OpenAI and OpenRouter report them, Bedrock and Azure bill
  them inside output tokens.
- GLM-4.7 and GLM-5 on Bedrock sometimes write a tool call as text in GLM's own syntax instead of a structured call;
  `workweek/providers.py` recovers those, and each run records how many (`recovered_tool_calls`).

`workweek.config.load()` refuses duplicate names, unknown families, a model string without a provider prefix, a
missing price, judge weights that do not sum to 1, two judges from one family, a dropout that leaves no weight, and a
non-positive cadence; `missing_credentials()` lists routes without keys.

## 8. Economics

Wages: BLS OEWS May 2025 medians via O*NET OnLine (the newest OEWS, released 2026-05-15). Loaded cost: BLS ECEC June
2026 total compensation over wages for the employer's sector or occupational group (`data/ecec-2026-06.csv`).
Ageing to the run quarter: the ECI factor in `data/eci.yaml`, a placeholder of 1.0 until the Q3 2026 release on
2026-10-30. Composing speed 18-25 words a minute by profession (Karat et al. 1999 measured about 19 for composition);
reading 238 (Brysbaert 2019). Each need's minutes are estimates with their basis stated; no time-use study exists for
most of these tasks.

## 9. Status (2026-10-27)

- All 11 weeks compile with 0 audit errors; all 27 routes pass a tool-call smoke test (`data/smoke-models.csv`).
- Three samples of 10 simulated minutes on all 27 models: customer service D1 13:15-13:25 and 09:15-09:25 (with a
  live call), claims D1 11:00-11:10 (a live call, then the written offer). Every model completed every sample.
- Questions: in the first sample four models asked six (GPT-6.1 Sol, Claude Opus 5, DeepSeek V3.2 three, GLM-5); the
  simulated worker (Gemini 4 Argon) answered each from the worker's intents, once claiming an action the worker had
  not taken, which its prompt now forbids.
- The claims sample, graded with all seven judges: 497 judge calls, no errors; 15 models caught each of the three
  needs in the window (both call lines and the written offer); mean panel score 0.43 to 0.92 by model; token cost
  $0.003 to $0.50 a model for the 10 minutes.
- The samples found and fixed: calls kept live by their case notes; a joined model missing the caller's opening
  line; 65 call-line windows that disagreed with the compiled turn times (now derived); GLM tool calls written as
  text on Bedrock (recovered); judges given too little context (median spread across judges fell from over 80 points
  to 29 with the files the model opened); token cost charging the simulated worker and double-counting cache reads;
  phishing traps firing on correct reports; new messages without recipients (now refused).

### Cost

Spent on 2026-10-27: about $17 on tested models for the three samples, under $0.05 on the simulated worker, and about
$7 to $11 per full grading of the claims sample (several gradings while fixing the grader); about $60 in all.

The full run is extrapolated from the claims sample (27 models, 10 minutes) and a one-day pilot (Claude Opus 4.8 and
GPT-6.1 Sol, DeepSeek V4.1 Flash; claims and customer service, D1 08:00-17:00; `logs/pilot-day1`):

- A full day costs 15-20 times a 10-minute window, not 54: after the first look a model makes about 1.5 calls a tick,
  and prompt caching covers most input (90-95% of input tokens read from cache on Bedrock and OpenAI). Input
  per call grows through the day (Opus 4.8: 9k tokens a call in the first quarter of the day, 27k in the last).
- Cost rises with the day's inbound items, with an elasticity of 0.6 (Opus 4.8) to 1.2 (DeepSeek V4.1 Flash)
  between claims (6.6 items a day) and customer service (19.4). Realistic volume (section 3) multiplies the inbound
  items, so it multiplies cost by about that factor to the power 0.6-1.2.
- Tested models, one seed (27 models x 11 professions x 5 days), at today's volume: $3,200-5,800 (mid $4,400). Routes
  without prompt caching (DeepSeek V3.2 on Azure, GLM-4.7 and GLM-5 on Bedrock) cost more than their prices suggest.
- Judges: 11-27 proposals a profession-day (pilot), so 16,000-40,000 a seed; at $0.16 a proposal (seven judges, the
  packet) $2,600-6,400 (mid $4,500). GPT-6 Astra now judges through OpenAI's Batch API at half price, about a sixth
  off the judge cost; Inspect batches only OpenAI's, Anthropic's own and Google's own APIs, so the Bedrock, Azure and
  OpenRouter judges cannot.
- Per seed in all, at today's volume: $5,800-12,200 (mid about $8,900); three seeds $17,000-37,000. About $2,300 a
  seed runs through OpenRouter (8 tested models, 4 judges, the simulated worker); its credit tops up automatically.
- Wall clock: a day took 11-14 minutes for GPT-6.1 Sol and Opus 4.8 (both professions in parallel) and 79 minutes for
  DeepSeek V4.1 Flash on Azure, which sets the pace of a full run.

## 10. Open

- Need counts: 25 to 101 per week against the ~100 target; raising the analyst weeks to ~100 would mean either
  splitting big deliverables into many small needs (inflating counts without adding work) or writing more items. The
  owner should decide; minutes are reported either way.
- Volume: inbound items are 1/15 to 1/45 of a Microsoft 365 worker's mail and chat, which makes noticing easier and
  runs cheaper; a templated low-information noise arm (newsletters, notifications, cc's, calendar replies) would test
  how much recall depends on it.
- Coverage: planned work is 0.8-3.2 hours of each day; value is per benchmark week and the press-enter rate is over
  planned work, not the whole job, unless scaled by task time shares.
- ECI factor on 2026-10-30.
- Hand grades (about 100 proposals) and judge agreement; the friction (1.5) and rewrite threshold (0.5) sensitivity.
- Seeds (3 planned) and the pilot that sizes the full run.
