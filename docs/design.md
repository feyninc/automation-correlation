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
| `professions/<name>/` | one profession: `overview.md` (the week in plain English, with citations, and what an ideal assistant does), `week.yaml` (job, people, policies, standing documents), `day1.yaml`..`day5.yaml` and `day1b.yaml`..`day5b.yaml` (what happens each day); `episode/` (compiled: `profession.json` plus one JSON per date) and `report.md` (build report), generated |
| `workweek/` | `schema.py` (Pydantic models), `compile.py` (forms to episodes, the audit), `apps.py` (the world as files), `world.py` (events, feed, ticks), `engine.py` (the Inspect AI task), `prompts.py`, `checks.py` (the shared check evaluator), `grade.py` (offline grading), `config.py`, `creds.py`, `providers.py`, `sandbox/` (Docker image) |
| `config/run.yaml` | models, prices, judges and weights, the simulated worker, run settings |
| `scripts/` | `run.py` (run models x professions over a window), `smoke_models.py` (one tool call per route), `probe_reasoning.py`, `speed.py` (OpenRouter speed snapshot for offline timing), `timeline.py` (release timeline and model set), `screen_occupations.py` |
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

### How the weeks were built

The first version of each week (10-26 to 10-27) was written by hand from primary sources. On 10-27 each was brought to
realistic volume (owner: "volume 100% needs fixing", hours to fill the day) by a subagent per profession (two for
customer service) working from one spec: daily email, chat and call targets from the volume research (section 10),
the time budget at 80-110% every day, about one new trap per eight needs, verified sources for every rule a need
turns on, every number computed and written in the day file's header, intents without hindsight. The new material is
in `day1b.yaml`..`day5b.yaml`; the first version is unchanged except for corrections. Each week was then reviewed
before commit: the audit (compile, time budget, volume, intents, placeholders, findability, source links), every
header figure recomputed, the rules a need turns on checked against the statute or regulation text, the code in the
developer week run (19 tests pass on Friday's repository), and checks that only accepted the worker's own wording
widened. The review found no arithmetic error in the new material except one deadline count (claims payments due
11/16, not 11/13); the builds and the review found errors in the first versions, now fixed: an indirect-cost base on
the pre-2024 2 CFR 200.1 rule, a fiscal note missing 2031-33, a UTC conversion after the DST change, PR numbers out of
order, a battery-backup reply that contradicted 47 CFR 9.20, a wrong Ins. Code subsection, unquoted "#" that cut
YAML values short, and several stale links.

Each week then got its `overview.md` (10-27), written from the reviewed forms: every count and claim checked against
the day files and policies, every link fetched (bls.gov, ftc.gov, pcma.org and FindLaw refuse scripted requests; those links are the pages' own
published addresses).

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
  answer (a 10-27 review removed five hindsight intents, one of which gave away a need's answer, and five computed
  credit amounts; 10 of 567 intents still contain a number a check needs, all facts the worker was told).
- **Traffic**: recurring low-information items (system notifications, digests, channel chatter) as templates
  (`traffic:`: app, path, sender, `per_day`, varied `items`), expanded deterministically over the worker's hours;
  real systems send templated mail, and machine-generated mail is over 60% of email traffic (Ailon et al. 2013).
- **Hours and time**: `worker.hours` per day and `lunch_minutes`; an action may carry `minutes` for timed work the
  assistant cannot help with (a meeting, a call it cannot see, an inspection).
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
5. a split/merge round trip that changes the episode (the per-day JSON must rebuild the same episode);
6. a missing `overview.md`, one that doesn't link every day file, or one whose stated need and trap counts ("N ...
   (needs)", "N ... (traps)") differ from the compiled week, so a new profession can't be added without its overview
   and an edited week can't drift from it.

The build report lists counts per day and app, the time budget per day (the needs the worker does, other timed work,
lunch and 20 s to skim each inbound item, against the minutes present; a warning outside 80-110%), the task mix
against O*NET frequency and importance, and warnings.
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

- **Clock:** simulated, around the clock from Monday 00:00 to Friday 23:55, a tick every `cadence_minutes` (default 5;
  owner, 10-27: "an agent never sleeps"). Each tick says whether the worker is at work (`worker.hours` per day) and
  when they are next in; mail and traffic that arrive overnight reach the assistant when they arrive, and what it
  proposes while the worker is away waits for them. The worker's departure tick is an end-of-day turn. A question
  asked while the worker is away is not answered (it costs the worker only its reading). Before each tick the engine
  writes the world as of that moment. Nothing waits on a model: the clock stops while it works, and every timing
  question (did a call line arrive in time?) is answered offline in grading from the tokens it used.
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
   its tools took; the grader converts tokens to seconds with the model's p50 time to first token and throughput:
   OpenRouter's week averages for 2026-10-20 to 2026-10-27, best provider, at the run's reasoning levels, read by the
   owner from the model pages (`run.speed_file`, `data/openrouter/speed-week-2026-10-20.csv`; `scripts/speed.py`
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
`scripts/timeline.py`. Routes: OpenAI's API for GPT; Bedrock for Claude, Kimi K3 and GLM-4.7/5; Azure Foundry for DeepSeek
and Kimi where offered; OpenRouter with a pinned provider and no fallback otherwise. Credits come first (owner, 10-27):
the 10-27 catalogs have no Kimi K2 Thinking, K3, K3.1 Pro, DeepSeek V4.1 Flash 1017 or any GLM on Azure; Bedrock has
Kimi K2 Thinking, K3 and GLM-5.3 but not K3.1 Pro, GLM-5.1, 5.2 or DeepSeek V4.1 Flash 1017. Kimi K2 Thinking stays on
OpenRouter: on Bedrock, every answer after a tool result (8 of 8 tries) came back with its reasoning as text, usually
an unclosed `<think>`, which cannot be separated from the answer. GLM-5.3 on Bedrock has a 0 quota and is refused
("not available for this account"). Kimi K3 moved to Bedrock after a tool-call test, the same prompt caching as
Moonshot's API (18,081 of 18,117 input tokens read from cache) and the reasoning setting passed through. Every model runs at its lab's
medium reasoning setting, set on every call (owner, 10-26), except DeepSeek, which has no medium and runs at high
(owner, 10-27):

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
| DeepSeek V4.1 Flash 1017 (OpenRouter, DeepInfra fp8) | thinks | `reasoning: {effort: "high"}` (no medium) |
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
- DeepSeek documents low, high and max for V4, no medium, so DeepSeek runs at high.
- Defaults differ even by host (DeepSeek V4.1 Flash thinks by default on DeepInfra, not on Azure), so a setting is
  always sent.
- Reasoning token counts are not comparable across routes: OpenAI and OpenRouter report them, Bedrock and Azure bill
  them inside output tokens.
- GLM-4.7 and GLM-5 on Bedrock sometimes write a tool call as text in GLM's own syntax instead of a structured call;
  `workweek/providers.py` recovers those, and each run records how many (`recovered_tool_calls`).

The judges are each provider's best model at medium (owner, 10-27): Claude Opus 5.5 (Bedrock), GPT-6 Astra (OpenAI,
through the Batch API), Gemini 4 Argon (OpenRouter, Google Vertex), Kimi K3.1 Pro (OpenRouter, Moonshot), DeepSeek
V4.1 Flash 1017 at high (OpenRouter, DeepInfra), Qwen3.8 Max Prime (OpenRouter, Alibaba) and GLM-5.3 (OpenRouter,
Z.ai). The simulated worker is Gemini 4 Argon at medium. A smoke test on 10-27 (`data/smoke-models.csv`) had every
tested model, judge and the simulated worker make its tool call on its route at these settings.

Who pays follows from the route (`workweek.config.billing`), and `scripts/run.py` and `workweek.grade` print each
run's cost split the same way:

| Billing | Tested models | Judges and the simulated worker |
| --- | --- | --- |
| Bedrock credits | Claude Opus 4.5, 4.6, 4.7, 4.8, 5, 5.5; Kimi K3; GLM-4.7, GLM-5 (9) | judge Claude Opus 5.5 |
| Azure credits | Kimi K2.5, K2.6; DeepSeek V3.2, V4 Flash, V4 Flash 0731, V4.1 Flash (6) | none |
| OpenAI credits | GPT-5.2, 5.4, 5.5, 5.6 Sol, 6 Sol, 6.1 Sol (6) | judge GPT-6 Astra (Batch API) |
| OpenRouter (paid) | Kimi K2 Thinking, K3.1 Pro; DeepSeek V4.1 Flash 1017; GLM-5.1, 5.2, 5.3 (6) | judges Gemini 4 Argon, Kimi K3.1 Pro, DeepSeek V4.1 Flash 1017, Qwen3.8 Max Prime, GLM-5.3; the simulated worker (Gemini 4 Argon) |

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

The full run is sized from the volume pilot (`logs/pilot-volume-d1`, 10-27): Claude Opus 4.8, GPT-6.1 Sol and
DeepSeek V4.1 Flash on the expanded budget-analyst and operations-manager weeks, Monday 00:00-23:55, the 24-hour clock.
Budget analysts are the lightest week (79 inbound items a day), operations managers the heaviest (272).

| Model | Profession | Calls | Input (cache share) | Output | Proposals | Cost | Wall clock |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Opus 4.8 | budget analysts | 495 | 26.7M (91%) | 77k | 26 | $29.61 | 48 min |
| Claude Opus 4.8 | operations managers | 636 | 46.7M (85%) | 100k | 56 | $64.88 | 60 min |
| GPT-6.1 Sol | budget analysts | 445 | 11.0M (92%) | 16k | 26 | $2.90 | 24 min |
| GPT-6.1 Sol | operations managers | 597 | 23.8M (84%) | 33k | 68 | $9.74 | 43 min |
| DeepSeek V4.1 Flash | budget analysts | 501 | 28.9M (96%) | 91k | 17 | $1.30 | 53 min |

- Tested models, one seed (27 models x 55 profession-days): about $29,000. Each model is priced on its family's
  pilot tokens (Claude on Opus 4.8's, GPT on GPT-6.1 Sol's, the rest on DeepSeek's budget day scaled by the 1.87
  budget-to-operations ratio the other two show), at its own prices, with full input price on the routes that do not
  cache (DeepSeek V3.2 on Azure, GLM-4.7 and GLM-5 on Bedrock). The six Claude models are $14,700 of it; GLM-5 and
  GLM-4.7 on Bedrock $3,700, because they do not cache.
- Judges: 38.6 proposals a profession-day, so about 57,000 a seed; at $0.16 a proposal about $9,200.
- Per seed in all: about $38,000, on the mean of the lightest and heaviest week; three seeds about $115,000. A
  batch of three professions is 3/11 of a seed, about $10,400.
- By billing, per seed: Bedrock credits about $23,000 (Claude, Kimi K3, GLM-4.7/5, the Opus judge), OpenAI credits
  $4,400, Azure credits $2,400, OpenRouter $8,300 (the only cash; $5,000 of it judging). Judge shares are from the
  claims grading (Opus 5.5 about 38%, GPT-6 Astra at its batch price about 8%, the five OpenRouter judges about 55%).
- The clock: 24-34% of a day's input tokens go to ticks before 7:00 and after 18:00, when the worker is away and a
  model mostly waits; each such tick is one call over the whole context, which is longest late in the day.
- Caveats: one day (Monday) of two professions; customer service, with 30-40 live calls a day, is not in the pilot;
  the judge cost per proposal is from the claims grading.
- Wall clock: a profession-day took 24-60 minutes; the batch's slowest model sets its pace.

## 10. Open

- Coverage: needs are 26-59% of the hours present (section 3); value is per benchmark week and the press-enter rate
  is over that work, not the whole job, unless scaled by task time shares.
- ECI factor on 2026-10-30.
- Hand grades (about 100 proposals) and judge agreement; the friction (1.5) and rewrite threshold (0.5) sensitivity.
- How many seeds: at about $38,000 a seed (section 9), the owner's decision.
