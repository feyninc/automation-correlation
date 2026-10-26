# Data

- `onet/db_31_0_text/`: O*NET 31.0 database (text release), from onetcenter.org.
- `aei/job_exposure.csv`: "observed exposure" by 6-digit SOC, Anthropic Economic Index `labor_market_impacts/`
  (Massenkoff and McCrory, "Labor market impacts", 2026-03-05). `aei/wage_data.csv` is the 2025-02-10 release's wage table;
  its salaries are older and patchy (none for computer occupations), so wages for the paper come from BLS OEWS instead.
- `wages-onetonline-2026-10-26.csv`: BLS OEWS May 2025 medians (released 2026-05-15, the newest OEWS; May 2026
  data comes out in spring 2027) and the 2025-35 projections, read from O*NET OnLine's summary pages.
- `oews/`: empty. bls.gov and api.bls.gov refuse this computer (403/503), so the OEWS national file has to be
  downloaded from a browser and copied in.
- `occupations_screen.csv`: `scripts/screen_occupations.py` over O*NET 31.0: job zone, Work Context ratings
  (E-Mail, Face-to-Face, Telephone; 1-5), Working with Computers importance (1-5), task counts.
- `shortlist.csv`: the 20 candidate occupations, banded by observed exposure, with the 11 chosen (`chosen` = 1).
