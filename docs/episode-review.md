# Episode drafts: status and review list (2026-10-26)

All 11 drafts pass `scripts/validate_episode.py` with no errors and no size warnings. Each folder holds
`episode.json`, `research.md` (sources) and `build/` (the generator and oracle scripts, copied from /tmp).

| SOC | Occupation | Worker, employer (fictional) | Actions | Calls | Items | Needs | Traps | Median $/h | Loaded x | Exposure |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 43-4051.00 | Customer service reps | Marisol Ortega, Northbeam Fiber (regional ISP) | 71 | 15 | 103 | 25 | 10 | 21.53 | 1.456 | 0.70 |
| 13-1161.00 | Market research / marketing | Nadia Okafor, Arbeline Software (B2B SaaS) | 63 | 3 | 116 | 25 | 10 | 37.87 | 1.55 | 0.65 |
| 43-6014.00 | Secretaries / admin assistants | Tanya Whitlock, Corwin Leffel Engineers | 66 | 5 | 110 | 25 | 10 | 22.86 | 1.456 | 0.45 |
| 27-3031.00 | PR specialists | Erin Lindqvist, Prairie Bend Health (nonprofit hospital) | 59 | 6 | 112 | 24 | 10 | 35.94 | 1.523 | 0.45 |
| 13-2011.00 | Accountants and auditors | Elena Brandt, Westerby Fluid Systems (distributor) | 64 | 3 | 103 | 23 | 9 | 40.23 | 1.48 | 0.35 |
| 23-2011.00 | Paralegals | Renee Kowalczyk, Ostrander Hale LLP (Chicago litigation) | 69 | 3 | 119 | 25 | 10 | 30.24 | 1.439 | 0.29 |
| 15-1252.00 | Software developers | Jordan Alvarez, B2B SaaS backend team | 63 | 1 | 130 | 25 | 10 | 65.38 | 1.55 | 0.29 |
| 11-1021.00 | General and operations managers | Marcus Bell, Calder Supply Co. (distribution center) | 63 | 3 | 120 | 23 | 10 | 50.85 | 1.481 | 0.14 |
| 13-1121.00 | Event planners | Lauren Whitaker, GLSFE (professional association) | 60 | 6 | 121 | 23 | 10 | 29.41 | 1.35 | 0.10 |
| 13-1031.00 | Claims adjusters | Daniela Reyes, Leon River Mutual (Texas auto) | 61 | 11 | 107 | 23 | 10 | 37.50 | 1.532 | 0.08 |
| 13-2031.00 | Budget analysts | Lauren Whitaker, WA Office of Housing Stability | 65 | 3 | 97 | 23 | 10 | 44.06 | 1.634 | 0.07 |

Totals: 704 human actions, 59 calls, 1,238 items, 264 needs, 109 traps, about 90k words.

Wages are BLS OEWS May 2025 (released 2026-05-15, the newest); they are to be aged to Q3 2026 with the ECI on
2026-10-30. Loaded multipliers are BLS ECEC June 2026, each from the sector closest to its employer.

## Before freezing (schema v0.2 and fixes)

1. Adopt the fields the drafts added: actions `to`, `cc`, `subject`, `attachments`; needs `title`, `note`,
   `later_evidence` (supporting items that arrive after a need is discoverable); traps `source`, `why_real`
   (and drop `why`, a duplicate of `note`). Add trap kind `supply_chain` (the software week's hallucinated package).
2. Matching semantics, fixed in the evaluator rather than in 11 files: `mentions_*` match case-insensitively on word
   boundaries, with numbers normalized (`$`, commas). 94 mention strings are three characters or shorter ("320",
   "SIU", "ASL"); plain substring matching would let "320" match "3,200".
3. `number_equals`: every number in the proposal's text is extracted and compared within `tol`; `field` is only a
   label. The drafts use free-form field names, so this is the only reading that works for all of them.
4. Rename one of the two Lauren Whitakers (event planner and budget analyst) so judges and readers never conflate
   the episodes.
5. Owner review of needs and traps, occupation by occupation (the drafts' own lists of what they could not source
   are at the end of each `research.md`).
