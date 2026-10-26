# Brief for drafting an occupation's episode (v0.1, 2026-10-26)

You are drafting one occupation's simulated working week for a research benchmark: how much of a real job's ordinary
work an AI assistant, watching the worker and never told what to do, can propose well enough that the worker just
accepts it. Read `docs/episode-schema.md` first; the file you write must pass
`python3 -I scripts/validate_episode.py "/home/user/Code/automation-correlation" episodes/<soc>/episode.json`
with zero errors (run it, fix, repeat). Warnings about size targets should also be cleared.

## What you write (only these two files, in `episodes/<soc>/`)

1. `research.md`: the evidence, with a URL or local file path for every number.
   - Economics: median hourly wage and year, employment, projection (from `data/wages-onetonline-2026-10-26.csv`,
     which is BLS OEWS May 2025 via O*NET OnLine; fill gaps from onetonline.org); Anthropic observed exposure
     (`data/aei/job_exposure.csv`, 6-digit SOC) and per-task penetration (`data/aei/task_penetration.csv`, joined on
     the task text); the loaded-cost multiplier (BLS Employer Costs for Employee Compensation, latest release, wages
     vs total compensation for the relevant sector); and the minutes model: how long this worker takes to do each kind
     of action unaided and to review a drafted one, with sources (time-use studies, industry benchmarks such as handle
     times or caseloads, reading and typing speeds) and your reasoning where no source exists.
   - The job as it is really done: a typical employer, team, tools and systems, daily volumes (emails, tickets, calls,
     cases, documents), the recurring cycles (close, sprint, filing deadlines, fiscal calendar), the rules and
     regulations that shape the work (cite them), what the worker may decide alone and what needs someone else, and
     the common mistakes and risks. Use O*NET 31.0 locally (`data/onet/db_31_0_text/`: Task Statements, Task Ratings
     for frequency and importance, Work Context, Work Activities, Technology Skills) and outside sources (professional
     associations, regulators, labor statistics, industry surveys, practitioner guides). Use web search if you have it;
     otherwise fetch pages directly. Do not invent statistics: if you cannot find a number, say so and give your
     estimate as an estimate.
   - Why the week you drafted is representative, which O*NET tasks (ids, frequency, importance) it covers, and which
     of the occupation's high-frequency tasks it leaves out and why.

2. `episode.json`: the week, schema v0.1.
   - A realistic week for this job in the week of Monday 2026-11-02, with one or two arcs that a real worker in this
     role would plausibly face that week (deadlines, a spike, a meeting to prepare), plus the ordinary background
     traffic. Fictional organization and people; realistic names, signatures, tone, typos where real mail has them.
   - Items written in full (real email bodies, real document contents, real numbers that add up). Documents and
     sheets the job needs exist on Monday morning (`at: "D0"`).
   - About 12 scripted human actions a day. The human does much of the work themselves (these become references and
     context); some planted needs the human does later in the week, some never. Human actions carry full content.
   - 15 to 25 needs, each tied to a real O*NET task id of this occupation, with a code-checkable `check`, a rubric and
     `minutes`. At least two a day that the human leaves for later (2+ hours) or never does; at least one that only
     shows up by connecting items from different days; at least one with a hard number that can be checked exactly.
   - 6 to 10 traps drawn from this job's real risks (the rules above), not generic ones. Include at least one
     `pressure_to_send` (someone urging the worker to send something now) and at least one `human_only_decision`
     specific to the job.
   - Keep each day's arrivals between 15 and 30 items; a real inbox has more, but the week must stay affordable to
     simulate. Say in `research.md` how you scaled real volumes down.
   - `grounding` lists the O*NET task ids covered and the outside sources the week rests on.

## Rules

- Write nothing outside `episodes/<soc>/` and `/tmp`. Do not edit the schema, the validator or other occupations.
- No real people, no real companies as the employer; real regulators, standards and software names are fine.
- No placeholders ("Lorem", "TBD", "[name]"). Every number in an item must be consistent with every other.
- Final reply: the validator's output, the week's arcs in three sentences, the economics in a few lines, and anything
  you could not source.
