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
  unaided with their basis, and the worker's private intent (used only by the simulated worker).
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

A real worker sees about 117 emails and 153 chat messages a day (Microsoft Work Trend Index 2025); the weeks carry
roughly one-eighth to one-twelfth of that, keeping every item that carries work or risk plus some noise. Worker actions
are the visible outputs (25 to 115 a week), not every keystroke; calls and meetings the model cannot see appear as
`noop` actions in the feed.

## 4. The world (`workweek/apps.py`)

An app is a registered class; adding a service is one class. Thread apps: `mail`, `chat`, `tickets`, `phone`, `news`,
`reviews` (pull requests). Document apps: `docs`, `calendar`, `records`, `policies`, `contacts`, `repo`. Everything
renders to read-only files under `/world` at the current simulated time (ticket state as of that moment, the latest
version of each document; a call's turns, then the worker's case note), plus `/world/contacts.csv`,
`/world/inbox/new.md` (what changed since the last check, including what the worker did) and `/world/inbox/feed.md`
(the day so far). `/home/assistant` is writable and kept all week. The developer week's repository is runnable:
`python3 -m unittest` after copying it to `/home/assistant`.

## 5. The engine (`workweek/engine.py`, an Inspect AI task)

- **Clock:** simulated, 08:00 to 17:00 each day, a tick every `cadence_minutes` (default 5), the 17:00 tick an
  end-of-day turn. Before each tick the engine writes the world as of that moment.
- **Agent:** one conversation per day; each tick is a multi-turn tool loop ending at `wait` or after
  `max_tool_calls_per_tick` (25). Tool output older than 6 ticks is elided. Tools: `bash` (Docker, no network,
  non-root), `propose(target, action, drafts[1-3], note)` with actions reply, new, forward, edit, schedule, update,
  say and flag (a new or forwarded message must name its recipients); `ask_worker(question)`; `join_call(path)` /
  `leave_call()` (a turn after every caller line while joined; a model that joins before the worker answers the
  caller's last line gets that line first); `wait()`. A call ends at its last spoken turn; a case note written
  afterwards does not keep it live.
- **System prompt:** fixed harness instructions plus the profession's `profession_prompt` (`workweek/prompts.py`).
- **Simulated worker** (`user_model`, Gemini 4 Argon, owner 10-26): answers `ask_worker` in at most three sentences
  from the profession prompt, the private intents of needs already discoverable, and recent activity. Each question
  costs the worker reading plus `question_answer_s` (default 30 s).
- **Output:** proposals, questions and tick counts in the sample metadata of the Inspect log, with token usage per
  call.

## 6. Grading (`python -m workweek.grade logs/<run>`)

1. **Matching** with the shared evaluator (`workweek/checks.py`): whole words, case-insensitive; numbers normalized
   ($, thousands commas, trailing zeros; "320" does not match "3,200"); `number_equals` within a tolerance; a proposal
   matches if any draft does. Action names are normalized per app (anything added to a thread is a reply, a line on a
   call is say, anything changing a document is an edit; flag, new, forward and schedule keep their names). A need is
   earned by the last matching proposal inside its window, and one proposal can earn several needs (see "Crediting
   work" below); a trap fires on any matching proposal.
2. **Judges:** a panel of seven from seven families (weights in the config, summing to 1). The prompt carries the same
   profession prompt; as of the proposal's time, the target, the need's evidence and the last 12 files the model
   opened (long files keep their head and the lines sharing an identifier with the drafts; 30,000 characters in all);
   the identifiers and numbers in the drafts found nowhere in the world (computed or invented); every draft; and the
   rubric and the worker's own version for every need the proposal matches, superseded versions included. Output:
   score 0-100 (the probability the worker sends the best draft unchanged), best draft, harm, rubric hits and misses,
   two short reasons, and the minimal fix.
3. **Panel score:** weighted mean with the tested model's own family dropped (`report_with_dropout`); the full-panel
   mean and median are kept beside it.
4. **Edit effort:** word-level edit distance from the best draft to its minimal fix (the HTER count without block
   shifts), against the minimal sendable version, so acceptable wording costs nothing; fix time = edits / composing
   speed x friction (1.5), capped at writing from scratch; above an edit rate of 0.5 the worker rewrites. The best
   draft and the minimal fix are the heaviest remaining judge's after dropout.
5. **Value:** loaded wage x (minutes of the needs it earns x p - reading time - (1 - p) x fix time) minus the
   proposal's share of the tested model's token cost, with p = panel score / 100. Reading is every word of every
   draft, or for a revision only the words that changed; unplanned and superseded proposals cost their reading; each
   question costs its reading plus `question_answer_s` at the loaded wage. The simulated worker's tokens are recorded
   separately and not charged to the model.
6. **Latency (planned):** time to first token (p50) plus output tokens / throughput from OpenRouter's published stats,
   entered by hand in the config, to decide whether a call line would have arrived in time. The speed fields are not
   yet filled.

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

## 10. Open

- Need counts: 25 to 101 per week against the ~100 target; raising the analyst weeks to ~100 would mean either
  splitting big deliverables into many small needs (inflating counts without adding work) or writing more items. The
  owner should decide; minutes are reported either way.
- Speed fields (TTFT, throughput) for the latency analysis: owner to enter from OpenRouter.
- ECI factor on 2026-10-30.
- Hand grades (about 100 proposals) and judge agreement; the friction (1.5) and rewrite threshold (0.5) sensitivity.
- Seeds (3 planned) and the pilot that sizes the full run.
