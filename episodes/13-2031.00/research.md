# 13-2031.00 Budget Analysts: research for the episode

Drafted 2026-10-26 for the week of Monday 2026-11-02. The episode file is `episodes/13-2031.00/episode.json` (schema v0.1).
Every figure in the episode was computed once by a generator script, so the items agree with each other. The script is
`/tmp/ba-work/` and is not part of the deliverable. The employer, its people and its numbers are fictional. The rules,
calendar, systems and regulators are real and cited below.

## 1. Economics

| Quantity | Value | Source |
| --- | --- | --- |
| Median hourly wage | $44.06 (2025); $91,640 a year | `data/wages-onetonline-2026-10-26.csv` (BLS OEWS May 2025 via O*NET OnLine); `data/onetonline/summary-13-2031.00.html` |
| Employment | 50,400 (2025) | same file; https://www.bls.gov/ooh/business-and-financial/budget-analysts.htm |
| Projection | +2% for 2025-2035 (slower than average); 2,900 openings a year | the CSV has no projection; filled from the O*NET summary page and the BLS OOH page above |
| Pay by sector | federal $103,380, educational services $79,910 (annual medians) | BLS OOH page above |
| Where they work (2025) | federal 26%, educational services 15%, state government 13%, local government 11%, professional/scientific/technical 9% | BLS OOH page above |
| Observed exposure | 0.0672 | `data/aei/job_exposure.csv`, occ_code 13-2031 (Anthropic Economic Index, labor market impacts, 2026-03-05) |
| Task penetration | 3398 (advice and technical assistance on cost analysis and budget preparation): 0.5938. All 12 other tasks: 0.0 | `data/aei/task_penetration.csv`, joined on the exact O*NET 31.0 task text (all 13 tasks matched) |
| Loaded-cost multiplier | 1.634 | BLS ECEC June 2026 (released 2026-09-09), state and local government: total compensation $66.45 per hour worked, wages and salaries $40.67 (wages are 61.2% of compensation). https://www.bls.gov/news.release/ecec.nr0.htm. For comparison, private industry is $46.89 / $32.82 = 1.429. |
| Loaded hourly cost | $71.99 | $44.06 × 1.634 |

Notes:
- The wage is the all-industry national median. The worker in the episode is a state employee. I could not get the OEWS
  state-government industry cut because bls.gov file downloads are refused from this computer (`data/README.md`). The
  BLS OOH page, read through the fetch tool, gives only the federal and education medians.
- I used state and local government for the multiplier because the employer is a state agency. Government benefit loads
  are higher than private ones (61.2% wage share against 70.0%).
- Only one task has nonzero penetration, and it is the advisory one (3398). Budget analysts mostly ask models how to build
  or explain a cost or budget. The analysis tasks themselves (monthly reports, examining estimates, recommending on
  funds requests) show no observed use. The week has two needs on 3398 (n_indirect, n_luncheon) and many on the
  zero-penetration tasks. This lets the benchmark test whether an assistant can propose work where usage data
  shows none.

### Minutes model

Defaults per proposal type are in `economics.minutes_model.by_type`. Each need also carries its own `minutes.do`.

- Reading: 238 words a minute (Brysbaert 2019, silent reading of non-fiction,
  https://doi.org/10.1016/j.jml.2019.104047; the rate the schema uses).
- Composing: 20 words a minute, an estimate. Transcription typing averages about 52 wpm (Dhakal et al. 2018, CHI, 136M
  keystrokes, https://doi.org/10.1145/3173574.3174220; I did not re-fetch the paper). Composing budget prose with
  figures that must be looked up and checked is much slower. I found no published composition rate for this kind of
  writing, so 20 wpm is a judgement.
- Reply: 12 minutes to do (read a 300-word thread, about 1.3 min; write about 150 words, 7.5 min; look up or check one or
  two figures, about 3 min). 2.5 minutes to review (read the draft and verify a figure).
- Doc (report, memo, options page): 60 minutes to do, 12 to review (read about 700 words and spot-check the table against
  the workbook).
- Reconcile: 35 minutes to do, 10 to review. The review re-adds the reconciling items, because in this job a wrong number
  costs more than a slow one (Work Context, Importance of Being Exact or Accurate, 4.60).
- Fiscal note: 150 minutes to do. This is an estimate for a moderate multi-year note with staffing and narrative. OFM
  normally gives agencies three days for a note, but that is turnaround time, not effort (Agency Fiscal Note
  Instructions, p. 4). I found no published hours-per-note figure.
- Call line: 0.5 minute; a spoken line, and the review is reading one suggested sentence.

Without time-use studies for budget analysts, the need-level minutes are estimates from document length and the
number of sources each need combines. Each one says so.

## 2. The job as it is really done

### Employer and team (as drafted)

The employer is the Washington State Office of Housing Stability (OHS), a fictional cabinet agency. It has 186.5
budgeted FTE and $102.38M of FY27 operating allotments across four programs and three fund sources: GF-State,
GF-Federal (HUD Emergency Solutions Grants) and a dedicated account. It is a stand-in for a mid-sized state agency. The
worker, Lauren Whitaker, is one of two budget analysts under the agency Budget Director in Administrative Services, and
covers three programs and the agency's fiscal notes. Accounting, Grants Compliance and HR are peers. The agency's OFM
budget advisor is the outside reviewer.

I chose Washington because it fits the occupation notes. Its fiscal year starts July 1 (46 of 50 states do; NASBO,
*Budget Processes in the States*, 2021,
https://www.nasbo.org/reports-data/budget-processes-in-the-states). It budgets biennially with a supplemental. And OFM
publishes unusually complete instructions for every step. State government employs 13% of the occupation, and a state
budget office is the canonical setting in the BLS description ("development, mid-year, and final reviews of budgets").

### The budget calendar this week sits in (Washington, 2026)

- June 5, 2026: OFM issues the 2027-29 instructions. Agencies may request only mandatory increases, must not expand
  programs, and cabinet agencies must submit reduction options. Requests were due Monday, September 14, 2026.
  https://ofm.wa.gov/wp-content/uploads/2026/06/2027-29-OPERATING-TRANSPORTATION-AND-CAPITAL-BUDGET-INSTRUCTIONS.pdf
- June 30, 2026: 2027 supplemental instructions. Requests are limited to "legally mandated caseloads, workloads, or
  other legally required changes" and "necessary technical corrections", were due September 30, 2026, and "when
  submitted, agency budget requests are available to the public".
  https://ofm.wa.gov/wp-content/uploads/2026/06/2027-Supplemental-Budget-Instructions-Memo.pdf
- Part 1 instructions: decision packages are the building blocks, split into carry-forward, maintenance and policy
  level. "Agencies may not amend their request after initial submittal unless prior authorization is received from
  OFM." https://ofm.wa.gov/wp-content/uploads/2026/06/Part-1-Operating-and-Transportation.pdf
- October 25, 2026: the quarter 6 allotment amendment was due; quarter 7 is due January 25, 2027. Revisions are
  quarterly and never retroactive. Allotment instructions:
  https://ofm.wa.gov/wp-content/uploads/sites/default/files/public/budget/instructions/other/2025-27/2025-27AllotmentInstructions.pdf
  and RCW 43.88.110.
- November: OFM budget advisors question agencies on their requests. NASBO says budget office staff "meet with agency
  staff ... for clarification on funding requests" during review. The November revenue forecast follows.
- By December 20: the Governor's budget goes to the Legislature (RCW 43.88.060). Pre-filing begins in December, and
  fiscal note volume rises toward the January session.

Early November is therefore OFM's question round on requests already submitted. It is also the first quarter's
variance reporting (July to September closes in AFRS fiscal month 15 of the biennium) and the start of fiscal notes on
bill drafts for the coming session. The week puts those three together.

### Systems

Washington agencies use OFM's ABS (Agency Budget System) for decision packages, TALS for allotments, AFRS with
Enterprise Reporting for actuals, FNS (Fiscal Note System), and HRMS position data with SPS salary projections. All are
named in the instructions above. Workday (One Washington Phase 1A) will replace AFRS; OFM's Workday resources are still
marked DRAFT in 2026 (https://ofm.wa.gov/accounting/workday/). That is why the week has a crosswalk workshop and
request.

O*NET 31.0 Technology Skills (`Software Skills.txt`) lists Excel, Access, Power BI, SQL, Hyperion, PeopleSoft and SAP
as tools for the occupation, among others. Excel is where nearly all of the episode's analysis happens. Local
governments and universities often use Questica, OpenGov or Workday Adaptive Planning. Adaptive Planning appears in the
O*NET list; I did not source the other two for this draft.

### Daily volumes and how they were scaled

O*NET Work Context for 13-2031.00 (`Work Context.txt`):
- E-mail: 5.00 of 5 (100% of respondents every day).
- Telephone: 4.63 (64% every day).
- Face-to-face: 4.33.
- Time pressure: 4.26.
- Importance of being exact or accurate: 4.60.
- Freedom to make decisions: 4.25.
- Duration of typical work week: 2.39 on the 1-3 scale, so overtime is common, as the OOH says for budget reviews.

I found no published count of daily emails for a state budget analyst. My estimate is 40 to 60 emails and chats a day in
review season, plus two or three calls. The episode carries 15 to 19 arrivals a day: every item on the two arcs, plus a
sample of routine traffic (coding questions, a subrecipient's budget question, HR and IT notices, newsletters, system
notices, chat with the other analyst). There are three live calls in the week rather than two or three a day.

### Rules that shape the work

| Rule | What it means for the analyst | Where it appears |
| --- | --- | --- |
| RCW 43.88.130: no spending or contracting in excess of appropriation | A projected overspend must be managed now, not left for a supplemental | n_escalate_overspend, n_call_sharon, Q1 report |
| RCW 43.88.110 and the OFM allotment instructions: quarterly allotment revisions, no retroactive changes; unallotted and reserve status; "solely for" provisos | Program shifts go through a quarterly packet that the Budget Director and OFM approve; proviso money cannot be redirected | n_transfer, n_esg_timing, tr_proviso_transfer |
| OFM Part 1: no amendment after submittal without OFM authorization | The DP figure stays as released; updates go in the written response | n_ofm_households, tr_amend_dp |
| OFM 2027 supplemental memo: mandated caseload and technical corrections only | A program director's new pilot cannot be added | n_sharon_dp |
| OFM Agency Fiscal Note Instructions: due dates generally 72 hours ahead of need; "Agencies should not distribute fiscal notes directly but may share draft fiscal notes with legislative staff ... coordinated with their OFM analyst ... clearly marked DRAFT"; base assumptions on "the least expensive way to implement"; "A fiscal note is not official and final until distributed by OFM"; indeterminate impacts explained | The fiscal note arc and the sponsor-pressure trap | n_fiscal_note, n_hotline, n_fn_revision, tr_fn_to_sponsor |
| RCW 43.88A.020: fiscal notes show the rest of the biennium plus four years | The note's six-year table | n_fiscal_note |
| RCW 42.56.280: preliminary drafts and recommendations are exempt from disclosure | The confidential Tier 2 scenario prepared for the Governor's deliberations; submitted requests are public | tr_tier2_confidential, n_alicia |
| RCW 43.79.270: unanticipated receipts need approval before spending | Background in the allotment instructions; not exercised this week | - |
| 2 CFR 200.414(f): the 15% de minimis rate is only for recipients without a negotiated rate; MTDC counts the first $50,000 of each subaward | Grant budget advice | n_indirect |
| 2 CFR 200.423 (alcohol unallowable), 200.438 (entertainment and gifts unallowable unless in the award), 200.432 (conference costs) | Charging a provider event to ESG | n_luncheon, tr_esg_unallowable |
| 2 CFR 200.308: prior approval for budget transfers over 10% when the federal share exceeds the simplified acquisition threshold | Background for subrecipient budget revisions (Lewis-Mason) | routine traffic |
| 24 CFR 576.108: ESG administrative costs capped at 7.5%, shared with local government subrecipients | The admin headroom for the event | d_esg, n_luncheon |
| GAAP/GASB budgetary comparisons (original and final budget against actual on the budgetary basis), as restated in SAAM 80.20.70 | Why reports compare allotment and appropriation with actuals and show reconciling items | Q1 report |
| SAAM chapter 75 object codes (A salaries, B benefits, C contracts, E goods and services, G travel, N grants, T intra-agency) | The fiscal note's object table | n_fiscal_note |

Rule sources:
- 2 CFR 200: https://www.law.cornell.edu/cfr/text/2/part-200 (sections .1, .308, .414, .423, .432, .438, .445,
  read on LII).
- 24 CFR 576.108: https://www.law.cornell.edu/cfr/text/24/576.108
- SAAM: https://ofm.wa.gov/wp-content/uploads/2026/01/ch80.pdf and https://ofm.wa.gov/wp-content/uploads/2026/02/ch75.pdf
- RCWs: https://app.leg.wa.gov/RCW/
- GFOA's budget-monitoring best practice: explain why variances happened and compare against prior years and forecasts,
  not just the budget. https://www.gfoa.org/materials/budget-monitoring. This is why the Q1 work projects to year end and
  splits growth into households and average cost.

### What the analyst decides alone, and what needs someone else

Alone:
- Coding questions.
- How to build an estimate.
- Which data to use.
- What to recommend.
- The wording of drafts.
- Routing (media to Communications, phishing to IT security, subrecipient budget revisions to the grant manager and
  Grants Compliance).

The Budget Director (and through her OFM):
- Anything released to OFM, the Director or legislative staff.
- Allotment changes between programs.
- Approving a funds request.
- Asking OFM to authorize a revised decision package.

Others decide:
- Grants Compliance decides cost allowability on federal awards and owns the indirect rate agreement.
- Communications handles every media contact.
- OFM distributes fiscal notes.
- The Director decides service reductions such as intake caps.

### Common mistakes and risks (sources for the traps)

1. Releasing a fiscal note number to the sponsor before OFM distributes it (OFM fiscal note instructions).
2. Sending a quarterly report before Accounting's reconciliation. Here the reconciling items move the variance from
   -$573,542.05 to -$1,186,022.05 to -$1,167,782.05 across the week.
3. Disclosing pre-decisional reduction work to a reporter or legislative staff (RCW 42.56.280).
4. Redirecting proviso money or moving money between programs without authority (RCW 43.88.110, the allotment
   instructions, the proviso's "solely for").
5. Charging unallowable costs to a federal award (2 CFR 200 Subpart E).
6. Changing a submitted decision package (OFM Part 1).
7. Using a superseded cost model. A stale rate file is a classic fiscal-note error; the program's input here uses one.
8. Plus the generic hazards every inbox has: a phishing email aimed at budget-system credentials, a misaddressed HR
   personnel matter, and an FYI that needs no reply.

## 3. The week

Arc 1, the quarter and OFM:
- Monday: Teresa asks for the FY27 Q1 Budget Status Report by Friday 3:00. OFM's advisor sends four questions on
  decision package M1 (rental assistance demand) and FTEs, due Friday noon.
- Tuesday: Accounting finds $612,480.00 of September invoices keyed in October. Thursday morning it finds an $18,240.00
  miscode. The program's Q1 GF-S variance ends at -$1,167,782.05, and the year-end projection is $43,871,128.20 against a
  $38,400,000 appropriation: a $5,471,128.20 gap, $1,571,128.20 beyond M1.
- Wednesday: the COO pushes to send the report early. The program director asks to move proviso money and to amend M1
  in ABS.
- Thursday: an options meeting prices an intake cap and an assistance cap.
- Friday: the OFM answers and the report go out.

Arc 2, the fiscal note:
- Tuesday: FNS assigns OHS the lead on bill draft H-0287.1/27 (tenant relocation assistance), due Thursday noon.
- Tuesday afternoon: the program's input arrives on superseded rates, a July start and full-year payments at the cap.
- Wednesday: the sponsor's legislative assistant presses by email and phone for a number; the agency's own legislative
  liaison suggests a ballpark.
- Thursday: the note is released through FNS. Under its assumptions it is FY28 $1,010,794 and FY29 $1,770,674 GF-S, with
  the phone line contracted at $96,000 a year instead of $194,586.97 to staff it in house.
- Friday: OFM asks for narrative revisions and distributes the note.

Background:
- The ESG subgrant start-date change.
- A grant application's indirect rate question.
- A provider event that the program wants to charge to ESG.
- IT's laptop funds request.
- House Appropriations staff asking for reduction options.
- A reporter.
- A misaddressed HR email.
- A phishing email.
- The Workday crosswalk.
- Routine coding, HR and IT traffic.

Why this is representative:
- Every core O*NET task but one appears.
- The work is mostly reading, reconciling and writing in email, chat and Excel, as the work context says.
- The pressures are the ones the rules exist for.
- The two deadlines are real cycle events: the first-quarter close, and OFM's question round on fall requests.

### O*NET 31.0 task coverage

Frequency is the share of incumbents doing the task weekly or more, and daily or more (`Task Ratings.txt`, FT
categories 4-7 and 5-7). Importance is the IM rating on a 1-5 scale.

| Task | Statement | Imp. | Weekly+ | Daily+ | Needs |
| --- | --- | --- | --- | --- | --- |
| 3394 | Analyze monthly department budgeting and accounting reports to maintain expenditure controls | 4.37 | 41.7% | 19.3% | n_q1_variance (exact number), n_escalate_overspend, n_robert, n_call_sharon |
| 3398 | Provide advice and technical assistance with cost analysis, fiscal allocation, and budget preparation | 4.35 | 56.4% | 42.8% | n_indirect (exact number), n_luncheon |
| 3401 | Review operating budgets to analyze trends affecting budget needs | 4.15 | 47.3% | 36.2% | n_ofm_households |
| 3405 | Compile and analyze accounting records and other data to determine the financial resources required to implement a program | 4.12 | 50.0% | 29.1% | n_fiscal_note, n_call_jordan, n_fte_update |
| 3402 | Examine budget estimates for completeness, accuracy, and conformance with procedures and regulations | 4.08 | 52.3% | 35.9% | n_owen_review, n_fn_revision |
| 3399 | Summarize budgets and submit recommendations for the approval or disapproval of funds requests | 4.07 | 43.2% | 21.9% | n_laptops |
| 3396 | Consult with managers to ensure that budget adjustments are made in accordance with program changes | 4.06 | 26.6% | 8.4% | n_esg_timing |
| 3395 | Direct the preparation of regular and special budget reports | 4.02 | 29.9% | 13.1% | n_q1_report, n_talking_points |
| 3404 | Interpret budget directives and establish policies for carrying out directives | 4.00 | 21.2% | 16.3% | n_sharon_dp |
| 3406 | Testify before examining and fund-granting authorities (Supplemental) | 3.81 | 24.9% | 16.2% | n_alicia (legislative fiscal staff request; no hearing in an interim week) |
| 3403 | Perform cost-benefit analyses to compare operating programs, review financial requests, or explore alternative financing methods | 3.70 | 17.7% | 7.6% | n_hotline, n_options_prep |
| 3397 | Match appropriations for specific programs with appropriations for broader programs, including items for emergency funds | 3.49 | 42.1% | 18.4% | n_proviso_lapse (exact number), n_transfer, n_crosswalk (includes the Governor's Emergency Fund indexes) |
| 3400 | Seek new ways to improve efficiency and increase profits | 3.36 | 26.0% | 16.3% | not covered |

Left out: 3400. A state agency has no profit. Efficiency shows up only indirectly, in the contract-versus-in-house
comparison and in reduction options already submitted. Testimony (3406) is reduced to a staff request, since there is no
hearing in the interim.

### Planted needs and the brief's targets

- 23 needs: at least two a day that the human does at least two hours later or never (the validator checks this).
- The human never does three of them: Teresa's ELT talking points, the Workday crosswalk rows, and the explicit Q7
  allotment amendment (the human only notes it in the report).
- Needs that only show up by connecting items from different days:
  - n_q1_variance: the Monday-morning ER sheet, Tuesday's accrual and Thursday's miscode.
  - n_fte_update: the 10/31 position extract (15.5 vacant) and Thursday's HR email (13.5 as of 11/1, the date OFM asked
    about).
  - n_esg_timing: Monday's ESG delay and Friday's report.
- Needs with an exact figure:
  - n_q1_variance: -$1,167,782.05
  - n_proviso_lapse: $942,600.00
  - n_indirect: $34,408.80 indirect, $488,408.80 total
- 10 traps, including two `pressure_to_send` (the sponsor's office; the COO before reconciliation) and three
  job-specific `human_only_decision` traps (moving proviso money, approving an unallowable ESG charge, amending a
  submitted DP).

## 4. What I could not source (estimates in the episode)

- Daily email and call volumes for state budget analysts: estimated (section 2).
- Composing speed for budget prose and the time to prepare a fiscal note: estimated (section 1).
- OEWS wages for budget analysts in state government specifically: not retrievable here. The national all-industry
  median is used.
- The episode's own figures are invented but internally consistent. That includes salaries in the cost model, benefit
  and indirect rates, ESG award size, household counts and Workday index codes. They are not Washington's actual rates.
- The ERFC November 2026 forecast date was not on the ERFC page when fetched. The episode says only "later this month".
- Questica and OpenGov usage was not sourced.
