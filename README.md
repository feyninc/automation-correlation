# Automation correlation

How much of a real job's ordinary work can an AI assistant do without being asked, well enough that the worker only
has to press enter, and how fast is that share growing as models improve?

## Why this question

Most benchmarks hand a model a task and score the answer. Real work does not arrive as tasks: it arrives as an inbox,
a queue, a calendar and a few half-finished documents, and most of the skill is noticing what needs doing. An
assistant that can do a task when told is augmentation; one that notices the task, drafts the right thing at the
right time and leaves alone what it should not touch is the beginning of automation. The share of a week's work that
reaches "accept as is" is a direct, economically legible measure of that shift, and tracking it model by model shows
its pace, not just its level.

The second question is how that pace lines up with what is already observed in the labor market. Occupations differ
widely in how much of their work already shows up in real AI usage (observed exposure, Massenkoff and McCrory, 2026).
If proactive capability is high where observed exposure is low, adoption is lagging capability; if the two move
together, usage is tracking what models can do. Hence the name: does automation capability correlate with exposure,
and with time?

## Method

The full design is [`docs/design.md`](docs/design.md).

- **Occupations.** 11 O*NET 31.0 occupations whose work runs through email, chat, calls and documents, spread across
  observed exposure from 0.07 (budget analysts) to 0.70 (customer service representatives). Wages are BLS OEWS May
  2025 medians, loaded with BLS ECEC (June 2026) and aged with the Employment Cost Index.
- **Weeks.** For each occupation, one working week (Monday 2026-11-02 to Friday 11-06) at a fictional employer with
  real rules, regulators and software, built from primary sources: 84 to 554 needs (1,922 in all, 13,598 minutes of
  work, each tied to an O*NET task with a window, a code check, a rubric, the minutes it takes and the worker's own
  version) and 16 to 81 traps (332) drawn from the job's real risks. Each week's `overview.md` explains it in plain
  English, with citations, and says what an ideal assistant would do. A compiler audits every week: each need's check
  passes on the worker's own version, no trap fires on what the worker did, the files round-trip, and the overview
  is there and agrees with the week.
- **The loop.** An Inspect AI task on a simulated clock that ticks every 5 minutes around the clock, Monday to
  Friday: at each tick the model sees the world as files (mail, chat, tickets, calls, documents, what the worker just
  did) and may read, propose up to three drafts, ask the worker (a simulated worker answers), join a live call or
  wait. Nothing it writes is delivered, so the week is identical for every model. The model keeps one conversation
  for the week at its largest context window, compacted in OpenCode's style at 80% of the window and at midnight.
- **Grading.** Code checks match proposals to needs and traps; a panel of six judges from six model families
  scores each proposal 0-100 (the chance the worker sends it unchanged) and writes the minimal fix. The tested
  model's own family is left out of the weighted mean. The edit distance to that fix gives the worker's fix time.
- **Value.** Loaded wage times (minutes saved x score - reading - expected fixing) minus token cost, per worker-week.
- **Models.** For each of five labs, its newest model on 1 January, 30 April and 31 July 2026 and its latest: 20
  models, each at its lab's medium reasoning setting (DeepSeek at high, which has no medium).

  | In force on | OpenAI | Anthropic | Moonshot | DeepSeek | Z.ai |
  | --- | --- | --- | --- | --- | --- |
  | 2026-01-01 | GPT-5.2 | Claude Opus 4.5 | Kimi K2 Thinking | DeepSeek V3.2 | GLM-4.7 |
  | 2026-04-30 | GPT-5.5 | Claude Opus 4.7 | Kimi K2.6 | DeepSeek V4 Flash | GLM-5.1 |
  | 2026-07-31 | GPT-5.6 Sol | Claude Opus 5 | Kimi K3 | DeepSeek V4 Flash 0731 | GLM-5.2 |
  | Latest | GPT-6.1 Sol | Claude Opus 5.5 | Kimi K3.1 Pro | DeepSeek V4.1 Flash 1017 | GLM-5.3 |

## Status

All 11 weeks are written and compile with 0 audit errors; the engine, compaction and grader run end to end, and every
model route passes a tool-call smoke test. Next: hand grades
for judge accuracy, then the full run in batches of three professions.

## Layout

| Path | What it is |
| --- | --- |
| `professions/<name>/` | one week: `overview.md` (start here), `week.yaml`, `day1.yaml`..`day5.yaml` and `day1b.yaml`..`day5b.yaml` (the forms), `episode/` and `report.md` (compiled) |
| `workweek/` | schema, compiler and audit, the world, the engine (Inspect AI task), checks, grader, config, provider patches, sandbox image |
| `config/run.yaml` | models, routes, prices, context windows, judges, the simulated worker, run settings (cadence, compaction, snapshot dates) |
| `scripts/` | `run.py`, `batch.py`, `calibrate.py`, `economics.py`, `figures.py`, `smoke_models.py`, `probe_reasoning.py`, `speed.py`, `timeline.py`, `screen_occupations.py` |
| `data/` | O*NET, Economic Index, wages, ECEC, ECI, release timelines, probe outputs; see `data/README.md` |
| `docs/` | `design.md`, `grading-audit.md` (every check changed or need voided in the first three weeks), the model timeline chart |

Credentials live outside the repository (`~/.config/automation-correlation/`).

## Commands

    uv sync
    unzip data/onet/db_31_0_text.zip -d data/onet
    docker build -t workweek-sandbox:1 workweek/sandbox
    uv run python -m workweek.compile professions/claims-adjusters        # compile and audit one week
    uv run python scripts/run.py --models "GPT-5.5" --professions claims-adjusters \
        --start "D1 09:00" --end "D1 09:30" --log-dir logs/try                # run a window
    uv run python scripts/run.py --professions claims-adjusters,paralegals,accountants \
        --log-dir logs/batch-1                                                # the 20 run models, a full week
    uv run python -m workweek.grade logs/try                                 # grade it into results/
    uv run python scripts/calibrate.py results/final data/handgrades-2026-10-29.csv   # the panel to the hand grades
    uv run python scripts/economics.py results/final                         # Acemoglu's inputs, measured; tasks vs use
    uv run python scripts/figures.py results/final                           # the figures (calibrated if it ran)
