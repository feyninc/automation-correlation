# Data

- `onet/db_31_0_text.zip`: O*NET 31.0 database (text release), from onetcenter.org. Unzip in place to
  `onet/db_31_0_text/` (git-ignored); the compiler reads task statements, ratings and the occupation list from it.
- `aei/job_exposure.csv`: "observed exposure" by 6-digit SOC, Anthropic Economic Index `labor_market_impacts/`
  (Massenkoff and McCrory, "Labor market impacts", 2026-03-05). `aei/task_penetration.csv`: observed usage by O*NET
  task, from the same release (only 1,354 of its 17,998 tasks have any usage above 0). `aei/wage_data.csv` is the
  2025-02-10 release's wage table; its salaries are older and patchy (none for computer occupations), so wages come
  from BLS OEWS instead. See `aei/README.md`.
- `wages-onetonline-2026-10-26.csv`: BLS OEWS May 2025 medians (released 2026-05-15, the newest OEWS) and the
  2025-35 projections, read from O*NET OnLine's summary pages, saved in `onetonline/` (bls.gov refuses scripted
  requests, so the figures come through O*NET OnLine).
- `ecec-2026-06.csv`: BLS Employer Costs for Employee Compensation, June 2026: total compensation over wages and
  salaries by sector and occupational group (the loaded-cost multiplier).
- `eci.yaml`: the Employment Cost Index factor that ages OEWS wages to the run quarter (1.0 until the Q3 2026 release
  on 2026-10-30).
- `occupations_screen.csv`: `scripts/screen_occupations.py` over O*NET 31.0: job zone, Work Context ratings
  (E-Mail, Face-to-Face, Telephone; 1-5), Working with Computers importance (1-5), task counts.
- `shortlist.csv`: the 20 candidate occupations, banded by observed exposure, with the 11 chosen (`chosen` = 1).
- `releases/`: each lab's release history (`<lab>.tsv`, from the labs' own announcements; `pre-window.tsv` for the
  models before 2026; `deepseek-updates.csv` for DeepSeek's dated checkpoints), merged by `scripts/timeline.py` into
  `releases/all.csv`. `models.csv` is the 27-model set it selects (every main-line model from the one in force on
  2026-01-01), which `config/run.yaml` lists; the run takes 20 of them by snapshot date. The chart is
  `docs/model-timeline-2026.html`.
- `openrouter/`: OpenRouter catalog snapshots of 2026-10-25 (models, families, per-model endpoints), used for model ids,
  prices, providers and context windows. `speed-week-2026-10-20.csv`: each model's p50 time to first token and
  throughput, OpenRouter's week averages for 2026-10-20 to 2026-10-27 at the run's reasoning levels, best provider,
  which the grader uses for offline call timing; `speed-snapshot-2026-10-27.csv` (`scripts/speed.py`): the last 30
  minutes per route, a cross-check.
- `reasoning-probe.csv`, `reasoning-probe-glm.csv`, `reasoning-probe-glm-5.3.csv`: `scripts/probe_reasoning.py`, each
  model with no reasoning setting and at low, medium and high (`docs/design.md`, section 7).
- `smoke-models.csv`: `scripts/smoke_models.py`, one tool call per model on its route.
