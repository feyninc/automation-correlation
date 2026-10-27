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
  real rules, regulators and software, written by hand from primary sources: 25 to 101 needs (567 in all, 5,375
  minutes of work, each tied to an O*NET task with a window, a code check, a rubric, the minutes it takes and the
  worker's own version) and 7 to 21 traps (144) drawn from the job's real risks. A compiler audits every week: each
  need's check passes on the worker's own version, no trap fires on what the worker did, and the files round-trip.
- **The loop.** An Inspect AI task on a simulated clock: every 5 minutes the model sees the world as files (mail,
  chat, tickets, calls, documents, what the worker just did) and may read, propose up to three drafts, ask the worker
  (a simulated worker answers), join a live call or wait. Nothing it writes is delivered, so the week is identical
  for every model.
- **Grading.** Code checks match proposals to needs and traps; a panel of seven judges from seven model families
  scores each proposal 0-100 (the chance the worker sends it unchanged) and writes the minimal fix. The tested
  model's own family is left out of the weighted mean. The edit distance to that fix gives the worker's fix time.
- **Value.** Loaded wage times (minutes saved x score - reading - expected fixing) minus token cost, per worker-week.
- **Models.** Each lab's main line, the model in force on 2026-01-01 and every release since: OpenAI GPT-5.2 to
  GPT-6.1 Sol, Claude Opus 4.5 to 5.5, Kimi K2 Thinking to K3.1 Pro, DeepSeek V3.2 to V4.1 Flash, GLM-4.7 to GLM-5.3
  (27 models), each at its lab's medium reasoning setting.

## Status (2026-10-27)

All 11 weeks are written and compile with 0 audit errors; the engine and grader run end to end on all 27 models. Next:
hand grades for judge agreement, the pilot that sizes the full run, then the full run.

## Layout

| Path | What it is |
| --- | --- |
| `professions/<name>/` | one week: `week.yaml` and `day1.yaml`..`day5.yaml` (hand-written), `episode/` and `report.md` (compiled) |
| `workweek/` | schema, compiler and audit, the world, the engine (Inspect AI task), checks, grader, config, provider patches, sandbox image |
| `config/run.yaml` | models, routes, prices, judges, the simulated worker, run settings |
| `scripts/` | `run.py`, `smoke_models.py`, `probe_reasoning.py`, `speed.py`, `timeline.py`, `screen_occupations.py` |
| `data/` | O*NET, Economic Index, wages, ECEC, ECI, release timelines, probe outputs; see `data/README.md` |
| `docs/` | `design.md`, the model timeline chart |

Credentials live outside the repository (`~/.config/automation-correlation/`).

## Commands

    uv sync
    unzip data/onet/db_31_0_text.zip -d data/onet
    docker build -t workweek-sandbox:1 workweek/sandbox
    uv run python -m workweek.compile professions/claims-adjusters        # compile and audit one week
    uv run python scripts/run.py --models "GPT-5.5" --professions claims-adjusters \
        --start "D1 09:00" --end "D1 09:30" --log-dir logs/try                # run a window
    uv run python -m workweek.grade logs/try                                 # grade it into results/
