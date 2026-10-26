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

- **Occupations.** 11 white-collar O*NET 31.0 occupations whose work runs through email, chat and documents, spread
  across observed exposure from 0.07 (budget analysts) to 0.70 (customer service representatives), from general and
  operations managers to software developers. Wages and employment are BLS OEWS May 2025 (via O*NET OnLine), to be
  aged with the Employment Cost Index; loaded labor cost uses BLS Employer Costs for Employee Compensation (June 2026).
- **Episodes.** For each occupation, one simulated working week (Monday 2026-11-02 to Friday 11-06): a fictional
  employer, contacts and systems, about 110 items (emails, chats, tickets, documents, sheets, calendar, calls), and
  about 60 scripted actions by the human worker. Each week is researched from O*NET task statements and work context,
  regulators, professional standards and industry benchmarks, with its sources in `research.md`.
- **The loop.** After each human action the model sees what happened and may read, propose or wait; at 5 PM it gets a
  turn to prepare for the next day; on phone calls it may propose the worker's next line within the caller's
  patience, on a simulated clock. Nothing the model writes is delivered: every action is a proposal, so the week stays
  identical for every model. An optional arm exposes a send command under an instruction to only draft, to count
  overstepping.
- **Ground truth.** Each week plants 23 to 25 needs (work that should get done, each tied to an O*NET task, with a
  deadline, a code-checkable condition, a rubric and the minutes it saves) and 9 to 10 traps drawn from the job's real
  risks (phishing, confidential data, decisions only the worker may make, pressure to send).
- **Grading.** Code checks first (recall of needs, traps triggered); then a panel of seven judges from seven model
  families grades each proposal as accept, edit or reject. The primary grade leaves out the judge from the tested
  model's own family (six judges; ties go to the stricter grade); the full panel's median is reported beside it,
  along with self-preference and agreement, and a hand-graded sample measures judge accuracy.
- **Models.** Each lab's main line, the model in force on 2026-01-01 and every release since: OpenAI GPT-5.2 to
  GPT-6.1 Sol, Claude Opus 4.5 to 5.5, Kimi K2 Thinking to K3.1 Pro, DeepSeek V3.2 to V4.1 Flash, GLM-4.7 to GLM-5.3 (27 models), each at
  its lab's medium reasoning setting. Release dates and the gaps between them are recorded from the labs' own
  announcements.
- **Economics.** The value of a proposal is the loaded wage times the minutes it saves minus the minutes to review it,
  minus its token cost. Prices are recorded both at launch and at run time.

## Status

Design, data, model selection and the 11 drafted weeks are in place; the engine, the grader and a pilot run are next.
The drafts still need review of their needs and traps before they are frozen.

## Layout

| Path | What it is |
| --- | --- |
| `docs/` | `architecture.md`, `episode-schema.md`, `episode-brief.md` (how the weeks were drafted), `episode-review.md`, `reasoning.md`, model timeline charts |
| `episodes/<soc>/` | the week (`episode.json`), its sources (`research.md`) and the scripts that built it (`build/`) |
| `scripts/` | `validate_episode.py`, `cost_estimate.py`, `probe_reasoning.py`, `timeline.py`, `timeline_2026.py`, `screen_occupations.py` |
| `data/` | O*NET 31.0 (zipped), Anthropic Economic Index tables, BLS wages via O*NET OnLine, release timelines, OpenRouter catalog snapshots, probe and cost outputs; see `data/README.md` |

Credentials and account details live outside the repository (`~/.config/automation-correlation/`).

    unzip data/onet/db_31_0_text.zip -d data/onet
    python3 -I scripts/validate_episode.py . episodes/*/episode.json
