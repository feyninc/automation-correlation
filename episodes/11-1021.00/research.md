# 11-1021.00 General and Operations Managers: research for the episode

Drafted 2026-10-26 for the week of Monday 2026-11-02. The worker is Marcus Bell, Operations Manager (the site lead) of
Calder Supply Co.'s Groveport distribution center near Columbus, Ohio. Calder Supply and every person in the episode are
fictional. The regulators, rules and software names are real.

Sources marked "(fetched 10-26)" were read on this date. A few primary pages refused this computer (osha.gov, ecfr.gov,
the ScienceDirect and ACM pages for the reading and typing papers). For those I cite the same regulation text on
law.cornell.edu, or the publication itself, and say so.

## 1. Economics

| Quantity | Value | Source |
| --- | --- | --- |
| Median hourly wage | $50.85 (2025); $105,770 a year | BLS OEWS May 2025 via O*NET OnLine: `data/wages-onetonline-2026-10-26.csv`; `data/onetonline/summary-11-1021.00.html` |
| Employment | 3,599,000 (2025) | same |
| Projection 2025-2035 | Faster than average (5% to 6%); 285,000 openings | same |
| Observed exposure (AEI) | 0.1378 | `data/aei/job_exposure.csv`, row 11-1021 (Anthropic Economic Index, labor market impacts, 2026-03-05) |
| Loaded-cost multiplier | 1.481 | BLS ECEC June 2026 (released 2026-09-09), Table 4, private industry, management, business and financial occupations: total compensation $88.63 / wages and salaries $59.85 per hour worked (wages are 67.5% of compensation). https://www.bls.gov/news.release/ecec.t04.htm (fetched 10-26) |
| Loaded hourly cost | $75.30 | 50.85 x 1.481 |

The occupational group is a better fit than the industry rows. Those are averages over all workers in an industry:
transportation and warehousing has a 1.513 multiplier ($49.86 / $32.95) and manufacturing 1.496 ($48.62 / $32.50), same
table. The all-private-industry multiplier is 1.429 ($46.89 / $32.82) (https://www.bls.gov/news.release/ecec.nr0.htm,
fetched 10-26).

**Per-task penetration.** From `data/aei/task_penetration.csv`, joined on exact task text with all 17 O*NET 31.0 tasks.
Only two tasks have nonzero penetration: 20699 "Review financial statements, sales or activity reports, or other
performance data..." at 0.9284, and 945 "Develop or implement product-marketing strategies..." at 0.8167. The other 15
tasks score 0.0, including all of scheduling (20701), budget (20703), personnel (20705), supplier monitoring (20702) and
directing operations (933, 20700). The episode therefore puts most of its needs in the zero-penetration tasks: the
low observed exposure (0.14) is what the study tests. The two exposed kinds of work in the week are the MBR numbers
(20699) and the variance (20703).

**Minutes model.** The rates:

- Reading speed is 238 words a minute for silent reading of non-fiction (Brysbaert 2019, "How many words do we read per
  minute?", *Journal of Memory and Language* 109:104047, https://doi.org/10.1016/j.jml.2019.104047; the default in
  `docs/episode-schema.md`; the publisher page refused this computer).
- Typing speed averages 52 words a minute (Dhakal, Feit, Kristensson and Oulasvirta 2018, "Observations on Typing from 136
  Million Keystrokes", CHI '18, https://doi.org/10.1145/3173574.3174220). The project page
  https://userinterfaces.aalto.fi/136Mkeystrokes/ confirms the citation but not the figure; the 52 wpm is from the
  paper's abstract.
- Composing speed is about 25 words a minute. This is **my estimate** (half of typing speed, to allow for deciding what to
  say). I found no source that measures how fast managers compose.
- Volume: the average Microsoft 365 user receives 117 emails and 153 Teams messages a day, most emails skimmed in under a
  minute (Microsoft Work Trend Index, 2025-06-17,
  https://www.microsoft.com/en-us/worklab/work-trend-index/breaking-down-infinite-workday, fetched 10-26). O*NET Work
  Context: 88% of these managers use email every day and 88% talk on the phone every day (`Work Context.txt`, CXP
  category 5).

| Kind | do (min) | review (min) | Reasoning |
| --- | --- | --- | --- |
| reply | 6 | 1.5 | read a 200-word thread (1 min) + compose 100 words at 25 wpm (4 min) + decide (1 min); review 100 words at 238 wpm + 30 s |
| follow_up | 8 | 2 | as reply plus looking something up |
| escalate | 12 | 2.5 | 150-200 words with facts gathered from 2-3 items |
| doc | 45 | 8 | a page of analysis or a plan (compute + write + check); review reads about 500 words and checks the numbers |
| reconcile | 25 | 4 | compare two documents line by line, find the cause, write the dispute |
| prep | 20 | 4 | meeting or interview prep |
| call_line | 0.3 | 0.1 | one spoken turn; the saving is thinking time only |
| schedule | 4 | 1 | invite or reschedule |

Needs override these where the item is bigger or smaller, and each states its basis: the MBR pages are 60 min, the
staffing plan 40, the CER 30. All of these values are estimates. I found no time-and-motion study of how long operations
managers spend on email or document tasks. The size of the MBR is set by practitioner norms: an MBR is the standard
monthly operating review in multi-site operations, and its ops pages carry the KPIs listed in section 2.

## 2. The job as it is really done

**Who employs them.** General and operations managers "oversee activities that are too diverse to be classified into one
area of management". The largest employers are retail trade (12%), professional, scientific and technical services
(12%), construction, wholesale trade and manufacturing (7% each). Most work full time and many work more than 40 hours
(BLS OOH, https://www.bls.gov/ooh/management/top-executives.htm, fetched 10-26). O*NET: 69.9% of incumbents work more
than 40 hours a week, and Freedom to Make Decisions is 4.81 of 5. O*NET's sample job titles include Operations Manager,
General Manager, Center Manager and Plant Superintendent (`summary-11-1021.00.html`).

**The employer chosen.** The site lead of a wholesale distributor's regional DC. This is wholesale trade, one of the five
largest employing industries. It also exercises the whole O*NET core list: operations (933, 20700), schedules (20701),
budget (20703), suppliers (20702), personnel (20705), policies (20704) and performance data (20699). The site is a
412,000 sq ft DC with two shifts, 148 permanent hourly associates plus about 32 agency associates, about 11,500 order
lines a day, and 38 branches as internal customers. These size figures are a plausible fictional site, not sourced
statistics.

**The team and tools.** Two shift supervisors, an inventory control supervisor, an EHS coordinator, a maintenance lead
and a transportation coordinator report to the site lead. Corporate partners are the VP (his manager), FP&A, the HR
business partner and the EHS director. Systems are a WMS, UKG timekeeping, an ERP general ledger, Coupa purchasing,
Workday HR, and Excel/SharePoint for the 300 log. O*NET 31.0 `Software Skills.txt` lists Microsoft Excel, Outlook,
PowerPoint, SharePoint, Kronos Workforce Timekeeper, Oracle JD Edwards, SAP, NetSuite and personnel scheduling software
for this occupation. Manhattan Active WM and Coupa are typical of the industry, not taken from that list.

**Daily and weekly volumes in the episode, and how they were scaled.** A real site lead's inbox is about 117 emails and
150 chats a day (WTI above). The episode has 16 to 24 arrivals a day, a scale of about 1:12. What was cut is the bulk:
CCs, system notifications beyond one daily summary, calendar churn, vendor marketing, and the many chat lines that are
only acknowledgements. Each day keeps what a site lead actually acts on, plus 1-2 FYI items so that knowing when to do
nothing is tested. Three phone calls stand in for many (O*NET: daily phone use 88%). The floor time (face to face with
individuals, 86% daily) appears as meetings and walks the model cannot see (noop actions).

**The recurring cycles in the week.** These are the Monday ops review; the monthly close (GL closed 11/03); the MBR
(Thursday, ops pages due Wednesday); the start of Q4 peak (an agency class starting 11/09); weekly vendor and carrier
reviews; the monthly safety walk; and the regional safety roll-up (Friday).

**Rules that shape the work (all fetched 10-26 unless noted).**

- OSHA recordkeeping, 29 CFR 1904 (Ohio private employers fall under federal OSHA):
  - A recordable case must go on the 300 log and a 301 "within seven (7) calendar days of receiving information"
    (1904.29(b)(3), https://www.law.cornell.edu/cfr/text/29/1904.29).
  - Medical treatment beyond first aid makes a case recordable. A non-prescription medication recommended at prescription
    strength is medical treatment (1904.7(b)(5)(ii)(A), https://www.law.cornell.edu/cfr/text/29/1904.7). The episode
    turns on a prescription for ibuprofen 800 mg. OSHA's recordkeeping FAQ puts prescription-strength ibuprofen at over
    467 mg; osha.gov refused this computer, so that threshold is from OSHA's published FAQ and was not re-read today.
  - An elastic wrap is first aid.
  - Restricted work means the employer or the provider keeps the employee from routine functions, meaning those done at
    least once a week (1904.7(b)(4)).
  - Report a fatality within 8 hours; an in-patient hospitalization, amputation or loss of an eye within 24 hours
    (1904.39).
  - Agency workers supervised day to day go on the host's log (1904.31(b)(2)), so their hours count in the site's TRIR.
  - The annual summary is certified by a company executive and posted from February 1 to April 30 (1904.32).
  - No retaliation for reporting an injury; a reporting procedure must not deter reporting (1904.35).
  - Benchmark: the 2024 TRC rate is 4.9 per 100 FTE for general warehousing (DART 4.3) against 2.3 for all private
    industry (https://www.bls.gov/web/osh/table-1-industry-rates-national.htm). The fictional site's YTD TRIR of 2.55 is
    therefore a good but believable warehouse.
- Forklifts, 29 CFR 1910.178(l)(4): refresher training and an evaluation are required when an operator "has been involved
  in an accident or near-miss incident"; operators are evaluated at least every three years
  (https://www.law.cornell.edu/cfr/text/29/1910.178).
- FLSA overtime: 1.5 times the regular rate over 40 hours in a fixed 168-hour workweek. "Averaging of hours over two or
  more weeks is not permitted." Overtime worked without authorization still has to be paid (WHD Fact Sheet 23,
  https://www.dol.gov/agencies/whd/fact-sheets/23-flsa-overtime-pay). Ohio has no daily overtime rule.
- FMLA: the employee need not mention the FMLA; the employer is expected to inquire (29 CFR 825.303(b),
  https://www.law.cornell.edu/cfr/text/29/825.303). The eligibility notice is due within five business days of the
  employer learning that leave may qualify (825.300(b)(1), https://www.law.cornell.edu/cfr/text/29/825.300). A
  supervisor who knew about absences to take a parent to dialysis is the employer knowing.
- ADA: an accommodation request can be made in plain English, and the employer then engages in an interactive process
  (EEOC guidance,
  https://www.eeoc.gov/laws/guidance/enforcement-guidance-reasonable-accommodation-and-undue-hardship-under-ada). This
  is background for the HR routing rules; no ADA case is planted.
- Ohio R.C. 3599.06: no employer may discharge or threaten an elector "for taking a reasonable amount of time to vote on
  election day" (https://codes.ohio.gov/ohio-revised-code/section-3599.06). Tuesday 11/03/2026 is Election Day, so the
  week includes a request to come in late to vote.

**What the site lead may decide alone, and what needs someone else.** The authority structure (fictional FIN-104,
EHS-301, HR-210, written to typical corporate practice) works like this:

- Alone: operating spend up to $25,000; overtime within budget; service agreements of 12 months or less and $50,000 or
  less on standard terms; daily scheduling; recovery for customers; and the recordability determination, with EHS facts
  and the corporate EHS director for questionable cases.
- Needs the VP, or the VP and CFO with Legal: all capital, all leases, multi-year or auto-renewing contracts, and
  overtime that puts labor more than 2% over forecast.
- Needs HR: final warnings, terminations, offers, pay data, and FMLA or ADA determinations.

Delegation-of-authority matrices with tiered dollar limits are standard internal control. The specific limits here are
**my estimate** of a mid-size distributor's; I found no survey of DOA limits.

**Common mistakes and risks that the traps and needs draw on.**

- Classifying from a work status form ("full duty") without reading the visit summary, which lists the prescription.
- Disciplining an employee right after an injury report.
- Terminating on attendance points that include FMLA-qualifying absences.
- Signing a multi-year lease under a vendor's price deadline.
- Approving capital through an operating PO, or splitting it.
- Paying an agency invoice that does not match approved timecards.
- Reporting against a stale budget.
- Vendor bank-change fraud (business email compromise).
- Sharing pay data.
- Acting on a misaddressed HR document.

## 3. The week and why it is representative

**The arcs.**

1. The October MBR on Thursday. The ops pages are due Wednesday at 17:00. October actuals arrive Wednesday morning, and the
   reforecast arrives Tuesday and replaces the AOP, which is still printed in the deck.
2. A safety case. A reach-truck incident on 10/29 was logged as first aid. The clinic's visit summary (Monday) shows a
   prescription, which makes it recordable. The safety page and the region's numbers are wrong until someone connects
   the clinic summary (D1), the KPI sheet (D0) and the EHS director's request (D3).
3. Peak staffing. The agency fills 14 of 22 seats for 11/09. The 320-hour gap is covered by volunteer overtime that
   needs the VP's advance approval.

Around these run the ordinary work: a customer mis-ship escalation and its root cause, a vendor pressing to sign a
lease, a capital request, an attendance termination that HR must review, an interview, an agency invoice, a carrier
missing pickups, the recycling rebate, and a voting-time request.

**The numbers add up. They were computed and asserted by the generator script (`/tmp/gm_build/build.py`, scratch, not kept):**

- October: 250,500 lines on 31,448 paid hours gives LPH 7.97. Accuracy 99.68% (812 errors), on-time 99.03% (337 late of
  34,850), OT 6.04%.
- GL direct labor is $669,590.20 ($552,299.40 wages plus $117,290.80 agency accrued at the invoice). Against the $655,800
  reforecast that is $13,790.20 (2.1%) over; against the stale $684,000 AOP it would look favorable.
- The agency invoice bills 5,368.0 h against 5,324.0 h approved in UKG: 44.0 h x $21.85 = $961.40.
- TRIR is 4 x 200,000 / 313,400 hours = 2.55 (1.91 if the case is left out).
- The recycling rebate: 22.05 t against 19.60 t at $85 is short $208.25.
- The staffing gap: 8 x 40 = 320 h = 192 (Saturday) + 128 (10-hour days). At $30.60 that is $9,792, against $6,992 for
  agency labor, a $2,800 premium.

**O*NET tasks covered.** Frequency is the mean of the FT categories (1 = yearly or less, 5 = daily, 7 = hourly or more)
and importance is IM, from `Task Ratings.txt`.

| Task | Freq | Imp | Needs |
| --- | --- | --- | --- |
| 20699 review performance data | 4.15 | 4.18 | ops review prep, MBR KPIs, MBR safety |
| 933 direct production/sales/distribution | 4.88 | 4.14 | Hollister recovery |
| 20700 direct administrative activities | 4.68 | 4.01 | OSHA recordability flag, 301 to EHS |
| 20701 staff schedules and duties | 4.71 | 3.98 | FLSA averaging reply, peak staffing plan, OT notice, agency call |
| 20703 financial/budget activities | 3.30 | 3.90 | leveler CER, labor variance |
| 20706 coordination with other managers | 4.24 | 3.83 | branch manager call |
| 20705 personnel (selection, training, evaluation) | 3.22 | 3.79 | termination to HR, PIT refresher, interview guide |
| 20704 policies, goals, procedures | 3.35 | 3.74 | MBR follow-up |
| 20702 monitor suppliers | 3.22 | 3.44 | agency invoice, lease routing, carrier escalation, vendor call |
| 20708 movement of goods | 4.68 | 4.03 | mis-pick root cause |
| 19501 environmental/sustainability programs | 2.79 | 3.10 | recycling rebate |

**Left out, and why.**

- 20707, set prices or credit terms (freq 4.54): in a distributor this sits with branch sales and credit, not the DC.
- 944, sales floor work (4.81): there is no sales floor in a DC.
- 945, marketing (2.90), 947, non-merchandising departments (3.95), 949, store layouts (2.84), and 948, facility
  locations (1.85): these belong to retail or HQ variants of the job. The leveler CER touches 948 only lightly.

The high-frequency 933, 20700 and 20701 also happen on the floor, face to face. That part of the job cannot be
observed, so it appears only as noop actions (the ops review, the safety walk, the MBR).

**Anticipation and connection.** Each day has at least two needs the human leaves for two hours or more, or never does:

- D1: root cause, invoice, OSHA flag, PIT refresher, lease routing, call.
- D2: HR escalation, CER, carrier, interview guide.
- D3: MBR KPIs, variance, safety, recycling, call.
- D4: staffing plan, MBR follow-up, call.
- D5: OT notice, the 301 to EHS.

The cross-day needs are:

- The safety page (D0 KPI sheet + D1 clinic summary + D3 EHS request).
- The OSHA flag (D0 incident report + D1 summary).
- The agency invoice (D1 invoice + D1 UKG report, which matters later through the D3 GL accrual and the D5 AP request).

The hard numbers checked exactly are $961.40, LPH 7.97, the $13,790.20 variance, TRIR 2.55 and $208.25.

## 4. What I could not source

- The authority limits ($25k operating spend, 12-month/$50k contracts, a 2% OT threshold), the attendance point scale
  and the site's size, wages ($20.40 average) and agency bill rate ($21.85). These are realistic estimates, not
  statistics. I did not fetch a Columbus-area warehouse wage to check the $20.40.
- KPI targets (LPH 8.0, accuracy 99.70%, on-time 98.50%, OT 6%) and the carrier SLA. These are typical of the WERC DC
  Measures metrics, but werc.org refused this computer, so no benchmark value is cited.
- Composing speed (25 wpm) and all per-kind minutes. These are estimates from the reading and typing rates above.
- OSHA's 467 mg ibuprofen threshold is from OSHA's recordkeeping FAQ, which I could not re-read today (osha.gov 403). The
  rule that prescription strength is medical treatment is verified at law.cornell.edu.
