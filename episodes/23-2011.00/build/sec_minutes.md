Two published anchors: silent reading of non-fiction at about 238 words a minute (Brysbaert 2019,
https://doi.org/10.1016/j.jml.2019.104047) and mean typing speed of 51.56 words a minute across 168,000 volunteers
(Dhakal et al., CHI 2018, https://userinterfaces.aalto.fi/136Mkeystrokes/resources/chi-18-analysis.pdf). Typing
speed is transcription; composing legal correspondence includes deciding what to say and checking names, dates and
numbers, so the model uses **40 words a minute composed** (an estimate, about 78% of typing speed). Document review
in e-discovery runs 31 to 100 documents an hour (RAND MG-1208, Pace and Zakaras 2012, p. 77 of the PDF:
https://www.rand.org/content/dam/rand/pubs/monographs/2012/RAND_MG1208.pdf), which bounds the privilege QC work.

| Proposal type | Do (min) | Review (min) | Reasoning |
| --- | --- | --- | --- |
| Short reply (60-100 words) | 4 | 1 | ~2.5 min composing at 40 wpm plus reading the source; review reads both at 238 wpm |
| Substantive e-mail (120-200 words, facts from 1-3 items) | 10 | 2 | ~4-5 min composing plus looking up facts |
| Docketing request with a computed deadline | 12 | 2 | reading the certificate of service and Rules 6(a)/6(d), counting on a calendar, writing ~150 words; review re-counts |
| Scheduling (calendar check and invite or vendor booking) | 8 | 1.5 | two calendars and a short message |
| Short document from a template (notice, cover letter, verification) | 30 | 6 | 1-2 pages adapted, caption and service details checked |
| Long document (20-entry privilege log, exhibit list) | 60 | 12 | about 3 minutes an entry from an export (estimate; see section 5) |
| Cite-check of a short motion with exhibits | 75 | 10 | every record cite, name, date, case number and the TOA checked against the exhibits |
| Pre-bill scrub (16 entries) | 30 | 5 | about 1.5 minutes an entry against a 3-section guideline, plus a summary |
| Weekly time entries | 20 | 4 | reconstructing a week's entries from the record |
| Call line (one spoken turn) | 0.3 | 0.1 | the value is the content, not the time |

Each need in `episode.json` carries its own `minutes` (do, review, and the source line); they follow this table.
At the loaded rate of $43.52 an hour, a 60-minute privilege log drafted well enough to accept after 12 minutes of
review is worth about $34.82 of the worker's time; a 4-minute reply reviewed in 1 minute is worth about $2.18.

Billable-time context: paralegals in NALA's 2020 survey reported working 40 hours a week, "where 29 of those hours
are billable," and "slightly over half of paralegals are not expected to produce a set number of billable hours per
week" (https://nala.org/wp-content/uploads/2023/02/NALA_2020_Utilization_and_Compensation_Survey.pdf). For lawyers,
Clio reports an average utilization rate of 37%, "2.9 hours of billable work in an average 8-hour work day"
(https://web.archive.org/web/20260516091805/https://www.clio.com/blog/how-to-calculate-utilization-rate/). The
worker's released week here (12.8 billable hours out of about 40) is light against NALA's 29 because the episode
models two matters, not her whole caseload (section 4).
