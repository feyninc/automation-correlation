# Design

What is built and how it fits together.

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
| `professions/<name>/` | one profession: `overview.md` (the week in plain English, with citations, and what an ideal assistant does), `week.yaml` (job, people, policies, standing documents), `day1.yaml`..`day5.yaml` and `day1b.yaml`..`day5b.yaml` (what happens each day); `episode/` (compiled: `profession.json` plus one JSON per date) and `report.md` (build report), generated |
| `workweek/` | `schema.py` (Pydantic models), `compile.py` (forms to episodes, the audit), `apps.py` (the world as files), `world.py` (events, feed, ticks), `engine.py` (the Inspect AI task), `compaction.py` (conversation compaction), `checkpoint.py` (resume a week from its last tick), `prompts.py`, `checks.py` (the shared check evaluator), `grade.py` (offline grading), `config.py`, `creds.py`, `providers.py` (provider patches), `sandbox/` (Docker image) |
| `config/run.yaml` | models, routes, prices, context windows, judges and weights, the simulated worker, run settings |
| `scripts/` | `run.py` (run models x professions over a window), `smoke_models.py` (one tool call per route), `probe_reasoning.py`, `speed.py` (OpenRouter speed snapshot), `timeline.py` (release timeline and model set), `screen_occupations.py` |
| `data/` | O*NET 31.0, Economic Index tables, BLS wages via O*NET OnLine, ECEC June 2026 multipliers, the ECI factor, release timelines, probe outputs (`data/README.md`) |
| `logs/`, `results/` | run output (git-ignored) |

## 3. Professions

Eleven O*NET 31.0 occupations across observed exposure (0.07 to 0.70). Each is one working week, Monday 2026-11-02
to Friday 2026-11-06, at a fictional employer with real rules, regulators, standards and software.

| Profession (SOC) | Employer and arcs | Needs | Need minutes | Traps | Worker actions | Live calls | Inbound/day | Hours present | Needs' share of hours |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Customer service (43-4051) | fiber ISP: outage, credits batch error, cancellation script change | 554 | 972 | 81 | 576 | 174 | 85 | 45.8 | 35% |
| PR specialists (27-3031) | hospital system: embargoed gift, ER-death inquiry | 190 | 1,279 | 33 | 260 | 15 | 170 | 46.8 | 46% |
| Claims adjusters (13-1031) | Texas auto: Stowers demand, hail total loss, SIU, ~40 more claims | 180 | 1,440 | 28 | 284 | 20 | 80 | 44.8 | 54% |
| Admin assistants (43-6014) | engineering firm: ops review and site tour, travel, legal hold | 176 | 916 | 30 | 274 | 20 | 233 | 42.5 | 36% |
| Event planners (13-1121) | association: conference, attrition, event day, 2027 pipeline | 152 | 947 | 24 | 218 | 20 | 128 | 49.5 | 32% |
| Paralegals (23-2011) | law firm: federal discovery, deadlines, a trial, ~15 matters | 148 | 1,576 | 24 | 186 | 10 | 98 | 44.2 | 59% |
| Accountants (13-2011) | distributor: October close, bank rec, cutoff, bill-and-hold | 117 | 1,515 | 28 | 169 | 5 | 109 | 47.0 | 54% |
| Market research (13-1161) | B2B SaaS: survey cleaning to readout, launch, accruals | 117 | 1,598 | 29 | 175 | 0 | 89 | 45.0 | 59% |
| Operations managers (11-1021) | distribution center: OSHA, FLSA, FMLA, peak staffing | 110 | 742 | 21 | 190 | 15 | 272 | 48.0 | 26% |
| Budget analysts (13-2031) | state agency: allotments, fiscal notes, grant rates | 94 | 1,228 | 16 | 126 | 5 | 79 | 42.8 | 48% |
| Software developers (15-1252) | billing SaaS: DST bug, code reviews, CVE, incident | 84 | 1,385 | 18 | 163 | 0 | 143 | 43.9 | 53% |
| **Total** | | **1,922** | **13,598** | **332** | **2,621** | **284** | | | |

Each day's work fills 81-101% of the hours present (the build report's time budget: the needs the worker does, other
timed work such as meetings and calls the assistant cannot join, lunch, and 20 s to skim each inbound item). Needs are
26-59% of the hours present: the rest of the day is meetings, calls, in-person work and reading. So the value the
benchmark can find is bounded by that share; value per worker-week is reported against the hours present, and the
press-enter rate is over the planned work. Need counts differ more than workload: call-heavy jobs have many one-line
needs (a spoken answer is 0.3 minutes), analyst jobs fewer, larger ones.

### How the weeks are built and checked

Each week is written from primary sources. The day files carry the week's main cases (`dayN.yaml`) and its realistic
volume (`dayNb.yaml`: the rest of the day's mail, chat, calls, meetings and smaller needs), built to one spec: daily
email, chat and call targets from the volume research, the time budget at 80-110% of every day, about one trap per
eight needs, a verified source for every rule a need turns on, every number computed and written in the day file's
header, intents without hindsight. Every week passes the audit (below) and was reviewed: header figures recomputed,
the rules a need turns on checked against the statute or regulation text, the developer week's code run (19 tests
pass on Friday's repository), checks widened where they accepted only the worker's own wording. Each `overview.md`
is written from the forms, with every count and claim checked against the day files and policies and every link
opened.

Known simplifications: HB 1214 has a bill number on 11/2, before Washington's pre-filing would give it one; market
research and software development have no phone app, so their calls are timed activity only; traffic is about half of
email, below the 60% machine-generated share measured in consumer mail.

### The form

`week.yaml` holds the job and everything true on Monday morning; each `dayN.yaml` and `dayNb.yaml` holds that day's
documents, threads, calls, the worker's actions, needs and traps. Lists from all files are concatenated.
`overview.md` is the account for a human reader: who the worker is, the rules that govern the work (each linked to
its source), how the week unfolds day by day (linking the day files), and what an ideal assistant would do at the
week's decision points. A later file can
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
  answer; a number a check needs appears in an intent only when the worker was told it.
- **Traffic**: recurring low-information items (system notifications, digests, channel chatter) as templates
  (`traffic:`: app, path, sender, `per_day`, varied `items`), expanded deterministically over the worker's hours;
  real systems send templated mail, and machine-generated mail is over 60% of email traffic (Ailon et al. 2013).
- **Hours and time**: `worker.hours` per day and `lunch_minutes`; an action may carry `minutes` for timed work the
  assistant cannot help with (a meeting, a call it cannot see, an inspection).
- **Traps**: a check that fires on a harmful proposal, the correct behavior, severity, an optional dollar bound with
  its source, and `worker_mistakes` (the worker's own actions the trap is allowed to match).

No rule is planted to make a case decidable by lookup alone: the policies are the employer's ordinary ones, and the
cases turn on reading the facts against them.

### Compiler and audit (`python -m workweek.compile professions/<name>`)

Expansion adds O*NET tasks (importance, frequency), economics (OEWS median wage, the ECEC loaded-cost multiplier for
the form's `ecec_sector`, the ECI factor, observed exposure, per-task penetration) and resolves every reference. The
audit fails the build on:

1. a need's O*NET task not among the occupation's tasks; a check naming a missing thread or contact;
2. a need whose check does not pass on its own reference: the worker's action, the worker's call line, or (for the
   mention and number parts) its reference text;
3. a trap that fires on any worker action, except listed worker mistakes;
4. two threads or documents that render to the same file; a thread in a document app or the reverse;
5. a split/merge round trip that changes the episode (the per-day JSON must rebuild the same episode);
6. a missing `overview.md`, one that doesn't link every day file, or one whose stated need and trap counts ("N ...
   (needs)", "N ... (traps)") differ from the compiled week, so a new profession can't be added without its overview
   and an edited week can't drift from it.

The build report lists counts per day and app, the time budget per day (the needs the worker does, other timed work,
lunch and 20 s to skim each inbound item, against the minutes present; a warning outside 80-110%), the task mix
against O*NET frequency and importance, and warnings.
Every identifier and number a need's check expects appears somewhere the model can see before the deadline, except
figures the work itself derives (checked by script across all weeks).

### Where the facts come from

Every week was researched from primary sources (statutes, regulations, standards, vendor and regulator pages), listed
in `week.yaml` under `sources`. Facts a trap or need turns on were checked again while writing, for example: the IRS
mid-2026 mileage change (72.5 to 76 cents, irs.gov), GSA FY2027 per diem rates (api.gsa.gov), Texas Insurance Code
542.051-.057 and Government Code 662.003 (Veterans Day), the urllib3 advisory GHSA-vxq7-64xx-v4gw / CVE-2026-97689
(api.osv.dev), PyPI dependency ranges, and that `fastapi-idempotency-middleware` is not on PyPI. Code in the developer
week was run: the planted bugs fail the new tests and the fixes pass. Numbers inside each story (counts, sums,
prorations, deadlines) were computed by script and are shown in each day file's header comment.

### Realism and scale

Everything a model, judge or the simulated worker reads gives times as the weekday and clock time ("Monday 11:05");
the week runs from Monday 2026-11-02, the first day, to Friday 2026-11-06, the last. Internally times are "D1 11:05".

A worker in Microsoft 365 receives about 117 emails and 153 chat messages a day (Microsoft Work Trend Index 2025). The
weeks carry 79 to 272 inbound items a day by profession (mail, chat, tickets and calls), from the per-occupation
targets of the volume research (contact centers 24-46 calls a day; claims caseloads of 100-140; Google's median of four
code reviews a week; the rest judgment calls bounded by the Microsoft figures). Recurring automated mail is templated
(`traffic:`), human mail and chat are written. Calls and meetings the assistant cannot join appear as timed `noop`
actions in the feed.

## 4. The world (`workweek/apps.py`)

An app is a registered class; adding a service is one class. Thread apps: `mail`, `chat`, `tickets`, `phone`, `news`,
`reviews` (pull requests). Document apps: `docs`, `calendar`, `records`, `policies`, `contacts`, `repo`. Everything
renders to read-only files under `/world` at the current simulated time (ticket state as of that moment, the latest
version of each document; a call's turns, then the worker's case note), plus `/world/contacts.csv`,
`/world/inbox/new.md` (what changed since the last check, including what the worker did) and `/world/inbox/feed.md`
(the day so far). `/home/assistant` is writable and kept all week. The developer week's repository is runnable:
`python3 -m unittest` after copying it to `/home/assistant`.

## 5. The engine (`workweek/engine.py`, an Inspect AI task)

- **Clock:** simulated, around the clock from Monday 00:00 to Friday 23:55, a tick every `cadence_minutes` (5), since
  an assistant does not sleep. Each tick says whether the worker is at work (`worker.hours` per day) and when they
  are next in; mail and traffic that arrive overnight reach the assistant when they arrive, and what it proposes
  while the worker is away waits for them. The worker's departure tick is an end-of-day turn. A question asked while
  the worker is away is not answered (it costs the worker only its reading). Before each tick the engine writes the
  world as of that moment. Nothing waits on a model: the clock stops while it works, and every timing question (did
  a call line arrive in time?) is answered offline in grading from the tokens it used.
- **Agent:** one conversation for the week; each tick is a multi-turn tool loop ending at `wait` or after
  `max_tool_calls_per_tick` (25). Each model runs at the largest context window its route serves (`context_window`),
  and nothing in the conversation is trimmed: editing earlier turns would break the prompt cache and make every call
  rewrite it (on a pilot day with per-tick trimming, cache writes were 61% of Opus 4.8's cost).
- **Compaction** (`workweek/compaction.py`): when the input reaches `compact_at` (0.8) of the window, and between
  days as `overnight` says: `compact` (a checkpoint at midnight; the default), `clear` (a fresh conversation each
  morning) or `custom` (a function named in `overnight_function`, `"module:function"`, with the signature of
  `compaction.compact`). The procedure is OpenCode's default (anomalyco/opencode,
  `packages/core/src/session/compaction.ts`), the same for every model:
  - the model writes its own summary in a fixed template (the worker's week, open work, proposals and promises,
    decisions and rules, facts and figures, done, next, relevant files) under OpenCode's rules (terse bullets, exact
    identifiers, only what is still open, no mention of compaction);
  - the newest 15,000 tokens (at most a quarter of the compaction threshold, sized with the model's own characters
    per token from its last call) are kept word for word beside it; later requests open with one
    `<conversation-checkpoint>` message holding both;
  - the summary request is the conversation unchanged plus the prompt, so it reads the prompt cache; a later
    compaction updates the checkpoint; a reply that skips the template gets one reminder; a request the provider
    rejects as too long is resent as a transcript with tool outputs cut.

  Native compaction is not used: OpenAI's returns an encrypted item only OpenAI models can read ("opaque and not
  intended to be human-interpretable"), and OpenCode uses native compaction only where a user opts in. Compaction is
  the harness's: its tokens are recorded in the sample (`compaction_usage`) and not charged to the model.
- **Failed calls:** a call a provider's filter blocks is tried three times, then recorded (`filtered_calls`) and the
  turn ends; the sample goes on. A call that fails otherwise (an outage, throttling) is retried within the turn, up
  to seven tries with waits of 5 s doubling to 160 s (`call_retries`), so a brief outage does not restart the week;
  Bedrock's client gets 10 attempts (`AWS_MAX_ATTEMPTS`). A week that still fails, or a batch that stops, resumes
  from its last tick (`workweek/checkpoint.py`): after every tick the engine saves the conversation, the records,
  the clock position, the model's home folder and the tokens spent so far under the batch's `checkpoints/`; a
  restart restores them in a new sandbox and continues, and the tokens spent before it (`prior_usage`) are added to
  the week's cost. The restored conversation is identical, so the provider's cache still matches. GPT models from GPT-5.4 on compact at 270k tokens
  (`compact_tokens`), below the 272k at which OpenAI doubles the input price. Tools: `bash` (Docker, no network,
  non-root), `propose(target, action, drafts[1-3], note)` with actions reply, new, forward, edit, schedule, update,
  say and flag (a new or forwarded message must name its recipients); `ask_worker(question)`; `join_call(path)` /
  `leave_call()` (a turn after every caller line while joined; a model that joins before the worker answers the
  caller's last line gets that line first); `wait()`. A call ends at its last spoken turn; a case note written
  afterwards does not keep it live.
- **System prompt:** fixed harness instructions plus the profession's `profession_prompt` (`workweek/prompts.py`).
- **Simulated worker** (`user_model`, Gemini 4 Argon): answers `ask_worker` in at most three sentences.
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
2. **Judges:** a panel of six from six families (equal weights in the config, summing to 1). Each judge gets a fixed
   system prompt (`JUDGE_SYSTEM`: what is graded and how, the parts of the case, the checklist, the score bands, the
   reply format; then `<job>`, the person and profession prompt, and `<policies>`, the employer's policies as of
   Monday morning: the same for every proposal in a profession, so it is the cached prefix of every judge request)
   and one case per proposal (`JUDGE_CASE`), in labeled parts so judging is reading, not searching (see "Making
   judging easy" below): `<moment>`; `<policy_changes>` any policy added or changed since Monday, as of the moment;
   `<proposal>` the target, action and
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
   its tools took; the grader converts tokens to seconds with the model's p50 time to first token and throughput:
   OpenRouter's week averages for 2026-10-20 to 2026-10-27, best provider, at the run's reasoning levels, read from
   the model pages (`run.speed_file`, `data/openrouter/speed-week-2026-10-20.csv`; `scripts/speed.py`
   snapshots the last 30 minutes per route as a cross-check, `speed-snapshot-2026-10-27.csv`), adds the worker
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

### Making judging easy, and what it buys

Judges do not see the episode's history or the model's notes, and should not have to: a draft is right or wrong
against the world, whatever the model's process. So the packet hands them what checking needs.

- **Draft facts:** every identifier (claim and account numbers, emails, dates, times), amount and person in the drafts,
  located deterministically in the world as of the proposal (file and line), or marked as in the worker's own version
  (computed), or as found nowhere (computed from other figures, or invented). Where a fact came from (a file read days
  earlier, the model's notes) does not matter.
- **Open work and history:** the planned work open at that moment with whether the worker had done it, and what the
  worker and the assistant had already done on the matter, so "already done" and "duplicate" can be judged at all.
- **Checklist before the score**, with the score bounded by it (not needed: 0-9; wrong place, facts or authority: at
  most 49 unless the fix is a few words).

Measured against a bare packet (the proposal and the files only) on the same proposals (63 from the claims sample,
40 from six models in the customer-service sample): agreement on accept (score at least 50) is Fleiss kappa
0.34-0.44 with either, and the typical spread across judges is about the same, while judges are 4-8 points
stricter with the full packet. Where the two grades differ most, the full packet's are right: a draft naming a
caller with an email the draft-facts lookup locates on another customer's account scores 2 rather than 60; a QA
dispute that was Marisol's planned work scores 69 rather than 27. So the packet buys validity, not agreement, at
about 60% more judge cost ($0.16 a proposal against $0.10).

The disagreement that remains is mostly in level, not ranking: each judge correlates 0.72-0.94 with the mean of the
others, and with judges' offsets removed the panel's reliability is ICC(3,k) 0.90-0.94 (0.93 for the six judges on
the claims sample's 71 proposals, against 0.95 for seven with Qwen3.8 Max Prime, which is left out because it was a
quarter of the judging cost and among the slowest). The offsets
are large (Claude Opus 5.5 about -12 points, Kimi K3 +8, GLM-5.3 +6); without calibration, leaving out the tested
family would shift scores by family (Claude models +1.8 points, Kimi -1.4, GLM -1.0), and with offsets calibrated
over the run the shift is -0.2, -0.1 and 0.0.

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

Grading runs as the weeks do: `--watch` grades each log as it finishes; concurrency is live
(`results/<run>/control.json`), `results/<run>/PAUSE` holds new judging, each judge call is retried up to seven
times (waits doubling from 5 s to 160 s), and every judgement is saved as it arrives (`judgements.jsonl`), so a
rerun of the grader pays only for what is missing. A week that ended in an error is left out
(`failed_weeks.json` lists any without a successful rerun); a week run more than once counts once.

Outputs: `results/<run>/graded.jsonl` (every proposal, need outcome, judgment and value) and `summary.csv` (per model
and profession: ticks, proposals, questions, needs caught, traps fired, press-enter rate, value, token cost).

## 7. Models, routes and reasoning (`config/run.yaml`)

The config holds each lab's main line from the model in force on 2026-01-01 through every release since (27 models,
from `scripts/timeline.py`). The run uses 20 of them (`run.snapshots`, `config.run_models()`, the default of
`scripts/run.py --models`): for each lab, its newest model released on or before 1 January, 30 April and 31 July
2026, and its latest model as of the run.

| In force on | OpenAI | Anthropic | Moonshot | DeepSeek | Z.ai |
| --- | --- | --- | --- | --- | --- |
| 2026-01-01 | GPT-5.2 | Claude Opus 4.5 | Kimi K2 Thinking | DeepSeek V3.2 | GLM-4.7 |
| 2026-04-30 | GPT-5.5 | Claude Opus 4.7 | Kimi K2.6 | DeepSeek V4 Flash | GLM-5.1 |
| 2026-07-31 | GPT-5.6 Sol | Claude Opus 5 | Kimi K3 | DeepSeek V4 Flash 0731 | GLM-5.2 |
| Latest | GPT-6.1 Sol | Claude Opus 5.5 | Kimi K3.1 Pro | DeepSeek V4.1 Flash 1017 | GLM-5.3 |

The rule is fixed in advance and the same for every lab: the best model a customer of each lab could use on each
date. A slope against release date is set mostly by the spread of dates, so releases weeks apart add little; four
points a lab span the period and show its shape. The analysis places each model at its own release date, so the
uneven gaps between snapshot dates (four months, then three and three) do not matter. The other seven configured
models (GPT-5.4, GPT-6 Sol, Claude Opus 4.6 and 4.8, Kimi K2.5, DeepSeek V4.1 Flash, GLM-5) can be run as a side
check with `--models` naming them.

Routes: OpenAI's API for GPT; Bedrock for Claude, Kimi K3 and GLM-4.7/5; Azure Foundry for DeepSeek V3.2 to V4.1
Flash and Kimi K2.5/K2.6; OpenRouter with a pinned provider and no fallback for the rest. Credits are used wherever a
route offers the model: Azure's catalog has no Kimi K2 Thinking, K3 or K3.1 Pro, no DeepSeek V4.1 Flash 1017 and no
GLM; Bedrock has no Kimi K3.1 Pro, GLM-5.1, GLM-5.2 or DeepSeek V4.1 Flash 1017. Kimi K2 Thinking runs on
OpenRouter because on Bedrock its answers after a tool result carry its reasoning as text, usually an unclosed
`<think>` (8 of 8 tries), which cannot be separated from the answer. GLM-5.3 runs on OpenRouter because Bedrock lists
it but refuses calls for this account. Kimi K3 on Bedrock makes structured tool calls, caches prompts as Moonshot's
API does (18,081 of 18,117 input tokens read from cache on a repeat) and takes the reasoning setting.

Context windows are the largest each route serves, checked with long prompts where no catalog gives the route's own
limit: Opus 4.6 to 5.5 1M on Bedrock with no beta setting (Opus 4.6 answers a 505,023-token prompt), Opus 4.5 200k;
GPT-5.4 and later 1.05M, GPT-5.2 400k (OpenAI prices prompts over 272k at twice the input rate and 1.5 times the
output rate; calls over that are recorded in `long_context_usage` and priced so); Kimi K3 and K3.1 Pro, DeepSeek V4
and V4.1, GLM-5.2 and 5.3 about 1M (K3 on Bedrock and DeepSeek V4 and V4.1 on Azure each answer a 398,000-token
prompt); Kimi K2 Thinking, K2.5 and K2.6 262,144 (K2.5 on Azure takes 251,722); GLM-4.7, GLM-5 and GLM-5.1 202,752
(Bedrock refuses 200,753 input tokens plus 2,000 output); DeepSeek V3.2 on Azure 131,072 (it refuses 156,721).

Content filters are off wherever they can be turned off. The weeks carry phishing and social-engineering messages by
design, which Azure's default filter (`Microsoft.DefaultV2`) blocks as jailbreaks. The six Azure deployments use
`benchmark-minimal-filters`: jailbreak, indirect-attack and protected-material checks off, and the four harm
categories at their most permissive setting, blocking only high severity; turning those off needs Microsoft's
approval for modified content filtering (aka.ms/oai/rai/exceptions). Bedrock applies no guardrail unless a request
names one, and none does; OpenAI's API and OpenRouter have no filter to configure.

Every model runs at its lab's medium reasoning setting, set on every call, except DeepSeek, which has no medium and
runs at high:

| Model (route) | Default, observed | Medium is sent as |
| --- | --- | --- |
| GPT-5.2, 5.4 (OpenAI) | no reasoning | `reasoning_effort: "medium"` |
| GPT-5.5, 5.6 Sol, 6 Sol, 6.1 Sol, 6 Astra (OpenAI) | reasoning | same |
| Opus 4.5 (Bedrock) | no thinking | effort beta, `effort: "medium"`, thinking with an 8,000-token budget |
| Opus 4.6 to 5.5 (Bedrock) | 4.6-4.8 no thinking; 5, 5.5 adaptive | adaptive thinking, `effort: "medium"` |
| DeepSeek V3.2 to V4.1 Flash (Azure) | no thinking | `reasoning_effort: "high"` (no medium) |
| Kimi K2.5, K2.6 (Azure) | thinks | `reasoning_effort: "medium"` |
| Kimi K3 (Bedrock) | thinks | `reasoning_effort: "medium"` (passed by `workweek/providers.py`; K3 thinks at every setting, on Moonshot's API too) |
| Kimi K2 Thinking, K3.1 Pro (OpenRouter) | thinks | `reasoning: {effort: "medium"}` |
| DeepSeek V4.1 Flash 1017 (OpenRouter, fp8: Morph, then inference.net, then SiliconFlow) | thinks | `reasoning: {effort: "high"}` (no medium) |
| GLM-4.7, GLM-5 (Bedrock) | thinks only at high | `reasoning_effort: "high"` (GLM thinking is on/off; `workweek/providers.py` passes it, which Inspect's Bedrock route did not) |
| GLM-5.1 to 5.3, Gemini 4 Argon (OpenRouter) | varies | `reasoning: {effort: "medium"}` |

Evidence: `scripts/probe_reasoning.py` asked each model one short scheduling question on its own route with no setting
and at low, medium and high (`data/reasoning-probe*.csv`). That shows whether thinking is on and the setting accepted;
it does not measure how much a model thinks on real work. Caveats:

- "Medium" is each lab's own word, not a common unit. Anthropic's effort default is high, so medium is a step below
  Anthropic's default but OpenAI's default from GPT-5.5 on.
- Adaptive thinking decides per call: at medium Opus 4.6 thought on the probe, Opus 4.7 did not at any level.
- GLM has only thinking on or off (Z.ai's API), so its "medium" is "thinking on". On Bedrock `reasoning_effort` low and
  medium leave it off and high turns it on (`data/reasoning-probe-glm.csv`); Z.ai's own `thinking: {type: enabled}`
  is ignored there.
- DeepSeek documents low, high and max for V4, no medium, so DeepSeek runs at high.
- Defaults differ even by host (DeepSeek V4.1 Flash thinks by default on DeepInfra, not on Azure), so a setting is
  always sent.
- Reasoning token counts are not comparable across routes: OpenAI and OpenRouter report them, Bedrock and Azure bill
  them inside output tokens.
- GLM-4.7 and GLM-5 on Bedrock sometimes write a tool call as text in GLM's own syntax instead of a structured call;
  `workweek/providers.py` recovers those, and each run records how many (`recovered_tool_calls`).

The judges are each provider's best model at medium: Claude Opus 5.5 (Bedrock), GPT-6 Astra (OpenAI), Gemini 4
Argon (OpenRouter, Google Vertex), Kimi K3.1 Pro (OpenRouter, Moonshot), DeepSeek V4.1 Flash 1017 at high
(OpenRouter, fp8) and GLM-5.3 (OpenRouter, Z.ai). Gemini is the panel's one family not under test. Astra is called
directly: Inspect sends batch requests one or two at a time, each taking 1-3 minutes, which stalls grading. On the
107 operations-manager proposals, GPT-6.1 Sol as a judge agrees with Astra (r 0.90, same mean, 93% agreement on
accept) at a third of the cost; Astra stays as OpenAI's strongest model, the saving being about $280 a seed of
OpenAI credits. DeepSeek 1017 runs on the fastest fp8 providers (Morph about 150 tokens a second, against 47 on
DeepInfra), which sets the pace of grading.
The simulated worker is Gemini 4 Argon at medium. The smoke test (`data/smoke-models.csv`) has every model, judge and
the simulated worker make its tool call on its route at these settings.

Who pays follows from the route (`workweek.config.billing`), and `scripts/run.py` and `workweek.grade` print each
run's cost split the same way:

| Billing | Run models | Judges and the simulated worker |
| --- | --- | --- |
| Bedrock credits | Claude Opus 4.5, 4.7, 5, 5.5; Kimi K3; GLM-4.7 (6) | judge Claude Opus 5.5 |
| Azure credits | Kimi K2.6; DeepSeek V3.2, V4 Flash, V4 Flash 0731 (4) | none |
| OpenAI credits | GPT-5.2, 5.5, 5.6 Sol, 6.1 Sol (4) | judge GPT-6 Astra |
| OpenRouter (paid) | Kimi K2 Thinking, K3.1 Pro; DeepSeek V4.1 Flash 1017; GLM-5.1, 5.2, 5.3 (6) | judges Gemini 4 Argon, Kimi K3.1 Pro, DeepSeek V4.1 Flash 1017, GLM-5.3; the simulated worker (Gemini 4 Argon) |

`workweek.config.load()` refuses duplicate names, unknown families, a model string without a provider prefix, a
model without a release date, price or context window, judge weights that do not sum to 1, two judges from one
family, a dropout that leaves no weight, a non-positive cadence, a `compact_at` outside (0, 1], and an `overnight`
of `custom` without `overnight_function` (or the reverse); `missing_credentials()` lists routes without keys.

## 8. Economics

Wages: BLS OEWS May 2025 medians via O*NET OnLine (the newest OEWS, released 2026-05-15). Loaded cost: BLS ECEC June
2026 total compensation over wages for the employer's sector or occupational group (`data/ecec-2026-06.csv`).
Ageing to the run quarter: the ECI factor in `data/eci.yaml`, a placeholder of 1.0 until the Q3 2026 release on
2026-10-30. Composing speed 18-25 words a minute by profession (Karat et al. 1999 measured about 19 for composition);
reading 238 (Brysbaert 2019). Each need's minutes are estimates with their basis stated; no time-use study exists for
most of these tasks.

## 9. Status

- All 11 weeks compile with 0 audit errors; every route passes the tool-call smoke test (`data/smoke-models.csv`).
- Three samples of 10 simulated minutes on all 27 models (customer service Monday 13:15-13:25 and 09:15-09:25, with a
  live call; claims Monday 11:00-11:10, a live call and then the written offer): every model completed every sample.
  In the first, four models asked six questions (GPT-6.1 Sol, Claude Opus 5, DeepSeek V3.2 three, GLM-5); the
  simulated worker answered each from the worker's intents.
- The claims sample, graded with seven judges (the six plus Qwen3.8 Max Prime): 497 judge calls, no errors; 15 models caught each of the three
  needs in the window (both call lines and the written offer); mean panel score 0.43 to 0.92 by model; token cost
  $0.003 to $0.50 a model for the 10 minutes.
- Compaction runs end to end: with the window set to 30,000 tokens, budget analysts Monday 16:00 to Tuesday 08:30,
  GPT-6.1 Sol compacts at midnight and at 04:55 and Claude Opus 4.8 at 19:35, midnight and 08:30; each summary
  request reads 95-98% of its input from the cache, and each checkpoint is about 10,000 tokens.

### Cost

A full day in the current harness (`logs/cost-check-ops-d1`: operations managers, the heaviest week with 272 inbound
items a day, Monday 00:00-23:55, full context windows), beside the same day with per-tick trimming of tool outputs
older than six ticks (`logs/pilot-volume-d1`):

| Model | Harness | Calls | Largest context | Input (from cache) | Cache writes | Proposals | Cost | Wall clock |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Opus 4.8 | current | 635 | 177k | 59.3M (100%) | 0.18M ($1.11) | 50 | $33.24 | 40 min |
| Claude Opus 4.8 | trimmed | 636 | 138k | 46.7M (85%) | 6.79M ($42.42) | 56 | $64.88 | 60 min |
| GPT-6.1 Sol | current | 584 | 101k | 31.4M (100%) | 0.10M ($0.20) | 57 | $3.64 | 39 min |
| GPT-6.1 Sol | trimmed | 597 | 76k | 23.8M (84%) | 3.70M ($7.40) | 68 | $9.74 | 43 min |

Neither model compacts during the day: the largest context is under a fifth of a 1M window and under the 272k at
which OpenAI's long-context price starts. Models with windows near 200k (Opus 4.5, GLM-4.7, GLM-5.1) or 131k
(DeepSeek V3.2) compact on heavy days.

One seed of the 20-model run (20 models x 55 profession-days) is about $16,000-19,000:

- Tested models about $13,400: each model on its family's token profile (from the 27-model samples and a full-day
  pilot on budget analysts and operations managers), at its own prices, scaled to the current harness by the change
  measured on the same day (Claude x0.51, GPT x0.37; the other caching routes taken at about x0.45, up to x1.0 for
  the upper figure), with the two routes that do not cache (DeepSeek V3.2 on Azure, GLM-4.7 on Bedrock) at about
  x1.3 for the larger context. Claude is about $6,600 of it.
- Judges about $3,000: about 36,600 proposals (33 a profession-day) at about $0.08 each with the six judges, the
  shared cached prefix and Astra called directly (Astra measured at $0.012 a proposal; Opus 5.5 about $0.033,
  Gemini $0.020, Kimi $0.010, GLM-5.3 $0.005, DeepSeek $0.003).
- By billing: Bedrock credits about $10,100, Azure credits $2,000, OpenAI credits $1,400, OpenRouter $2,900 (the
  only cash; $1,400 of it judging). A batch of three professions is 3/11 of a seed: about $4,500, $800 of it cash.
- The clock: about a quarter to a third of a day's input goes to ticks before 7:00 and after 18:00, when the worker
  is away and a model mostly waits.
- Wall clock: a profession-day takes 39-97 minutes by model (DeepSeek on Azure is the slowest); the batch's slowest
  model sets its pace.

## 10. Open

- Coverage: needs are 26-59% of the hours present (section 3); value is per benchmark week and the press-enter rate
  is over that work, not the whole job, unless scaled by task time shares.
- ECI factor on 2026-10-30.
- Hand grades (about 100 proposals) for judge accuracy; judge agreement on the full run; the friction (1.5) and
  rewrite threshold (0.5) sensitivity.
- How many seeds.
