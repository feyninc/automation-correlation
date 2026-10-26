# 13-1031.00 Claims Adjusters, Examiners, and Investigators: research for the episode

Drafted 2026-10-26 for schema v0.1. The episode is a desk auto adjuster at a fictional Texas regional mutual (Leon
River Mutual Insurance Company, Temple, TX) in the week of Monday 2026-11-02, after a hailstorm on Thursday 10/29.

Web search was not available from this computer (DuckDuckGo, Bing and Mojeek refused automated queries). Every page
below was fetched directly by URL. Where a number could not be found that way, it is labelled an estimate.

## 1. Economics

| Quantity | Value | Source |
| --- | --- | --- |
| Median hourly wage | $37.50 (2025); $78,000 annual | `data/wages-onetonline-2026-10-26.csv` (BLS OEWS May 2025 via O*NET OnLine), 13-1031.00 |
| Employment | 376,100 (2025) | same file |
| Projection 2025-2035 | "Decline (-1% or lower)", 20,900 openings a year | same file |
| BLS OOH (broader group incl. appraisers) | median $78,020 ($37.51/hr); -6% 2025-2035; about 21,600 openings a year; employers: direct insurance carriers 35%, agencies/brokerages 29%, federal government 13% | https://www.bls.gov/ooh/business-and-financial/claims-adjusters-appraisers-examiners-and-investigators.htm (fetched with WebFetch; bls.gov refuses curl from this computer) |
| Observed exposure (AEI) | 0.0818 | `data/aei/job_exposure.csv`, SOC 13-1031 |
| Task penetration (AEI) | 21417 "Examine claims forms and other records to determine insurance coverage" 0.9938; 21441 "Prepare reports to be submitted to company's data processing department" 0.9751; the other 27 tasks 0.0 | `data/aei/task_penetration.csv`, joined on exact task text (all 29 tasks matched) |
| Loaded-cost multiplier | 1.532 = $69.22 total compensation / $45.18 wages and salaries per hour (wages 65.3% of compensation) | BLS ECEC, June 2026 (released 2026-09-09), Table 4, private industry, "Insurance carriers and related activities": https://www.bls.gov/news.release/ecec.t04.htm. All private industry: $46.89 / $32.82, wages 70.0% (https://www.bls.gov/news.release/ecec.nr0.htm) |
| Loaded hourly cost | $57.45 = $37.50 x 1.532 | computed |

The OEWS code (13-1031) excludes appraisers and is what the benchmark uses; the OOH figures are for the group
13-1030 and are given only for context. The two projections differ (-1% or lower vs -6%) because they cover
different groups.

### Minutes model

No published time-and-motion study of desk adjusters was found. The model is built from reading and composing
speeds and the steps the job takes, and is stated in `economics.minutes_model`:

- Reading: 238 words a minute (Brysbaert 2019, https://doi.org/10.1016/j.jml.2019.104047).
- Transcription typing: about 52 words a minute (Dhakal et al., CHI 2018, https://doi.org/10.1145/3173574.3174220;
  project page https://userinterfaces.aalto.fi/136Mkeystrokes/). Composing claim correspondence, with file lookups and
  careful wording, is taken as about 20 words a minute (estimate).
- Opening a ClaimCenter file, its notes and documents: about 1.5 minutes per claim (estimate).

| Proposal type | Do (min) | Review (min) | Reasoning |
| --- | --- | --- | --- |
| Email reply | 8 | 1.5 | lookup + ~120 words at 20 wpm + check; review reads ~150 words |
| Formal letter (settlement, excess, ROR, acceptance) | 25 | 5 | 250-450 words with figures and policy language; review reads twice and checks numbers |
| File note / payment / reserve entry | 5 | 1 | 60-120 words |
| Call line | 0.3 | 0.1 | one spoken turn of 25-45 words; reading a proposal takes ~10 s |
| Large-loss report | 60 | 10 | read the demand package and file, sum specials, write ~500 words |
| Reconciliation / deadline or settlement arithmetic | 20 | 4 | several rows or lines plus a second check |
| Escalation or referral (SIU, coverage, litigation) | 15 | 3 | 150-250 words of facts and dates |
| Calendar entry | 4 | 0.5 | |

Each need's `minutes` points to one of these types.

## 2. The job as it is really done

### O*NET 31.0 (local, `data/onet/db_31_0_text/`)

Job Zone 4. Work Context (CX, 1-5): telephone 5.00, e-mail 5.00, written letters and memos 4.93, face-to-face 4.29,
time pressure 4.39, frequency of decision making 4.86, freedom to make decisions 4.51, importance of being exact
4.61, dealing with unpleasant or angry people 4.13, conflict situations 4.03, sitting 4.62. Top Work Activities
(importance): working with computers 4.68, communicating with people outside the organization 4.58, getting
information 4.56, making decisions 4.48. Technology Skills list Xactware Xactimate, CCC Pathways and CCC TL2000
(CCC's total-loss product), CSC Colossus (BI evaluation), ISO ClaimSearch, Microsoft Outlook/Excel, bill review and
fraud detection software. Sample titles include Claims Adjuster, Claims Representative, Claims Examiner.

Task ratings (FT mean on the 1-7 frequency scale; share rating daily or more; importance):

| Task | Statement (short) | FT mean | daily+ | IM |
| --- | --- | --- | --- | --- |
| 21417 | examine claims forms/records to determine coverage | 5.85 | 98% | 4.79 |
| 21418 | analyze investigation, report findings and recommendations | 5.57 | 89% | 4.76 |
| 21426 | pay and process claims within authority | 5.57 | 84% | 4.75 |
| 21423 | investigate, evaluate and settle claims | 5.61 | 90% | 4.74 |
| 21428 | verify and analyze data used in settling | 5.50 | 88% | 4.68 |
| 21419 | review police reports, medical records and bills, damage | 5.43 | 85% | 4.67 |
| 21420 | assess damage, create or review estimates | 5.57 | 86% | 4.63 |
| 21421 | correspond with agents and claimants; investigate questionable claims | 4.87 | 73% | 4.62 |
| 21422 | interview or correspond with claimants, witnesses, police, physicians | 5.43 | 74% | 4.59 |
| 21429 | enter payments, reserves, new claims, file documentation | 5.57 | 94% | 4.57 |
| 21425 | resolve complex, severe exposure claims | 4.35 | 50% | 4.49 |
| 21424 | adjust reserves or recommend reserves | 4.91 | 70% | 4.43 |
| 21432 | confer with legal counsel on litigation | 3.86 | 39% | 4.41 |
| 21427 | examine claims investigated by adjusters; questionable claims | 5.39 | 80% | 4.39 |
| 21434 | maintain claim files and inventory | 5.20 | 83% | 4.29 |
| 21430 | refer questionable claims to investigator | 3.89 | 44% | 4.29 |
| 21431 | collect evidence for contested claims in court | 3.40 | 30% | 4.26 |
| 21433 | contact claimants, doctors, employers for information | 4.69 | 62% | 4.04 |
| 21435 | present cases at claim committee | 3.49 | 21% | 3.94 |
| 21439 | report overpayments and irregularities | 3.16 | 32% | 3.81 |
| 21441 | prepare reports for data processing | 4.46 | 57% | 3.70 |
| 21436 | supervise adjusters (supplemental) | 5.18 | 81% | 4.17 |
| 21437 | detailed bill review (supplemental) | 3.85 | 45% | 4.01 |
| 21440 | reinsurance brokers (supplemental) | 2.78 | 15% | 3.95 |
| 21443 | attend mediations or trials | 2.09 | 5% | 3.71 |
| 21438 | examine titles to property (supplemental) | 3.48 | 34% | 3.70 |
| 21442 | obtain credit information (supplemental) | 2.13 | 11% | 2.94 |
| 21444, 21445 | credit background; negotiate settlements or recommend litigation | not rated | | |

### Employer, team, tools

- Employer: personal-auto carriers are the largest employer group (OOH: direct carriers 35%). The episode uses a
  Texas-only regional mutual with independent agents, a common structure in Texas personal auto. The name is
  fictional; it could not be checked against a company register without web search.
- Team: desk adjusters (Claims Representative I/II) under an auto claims supervisor, a casualty claims manager who
  chairs a weekly large-loss roundtable, staff counsel who handles suit papers and panel defense counsel, an SIU
  investigator, staff appraisers, a claims assistant, and during a catastrophe a CAT coordinator and a drive-in
  inspection site. This is standard carrier practice; the specific authority amounts (Rep II: APD $15,000, BI
  $25,000) are estimates consistent with the O*NET task "pay and process claims within designated authority level".
- Systems: Guidewire ClaimCenter as the claim system (activities/diary, exposures, reserves, payments; product page
  https://www.guidewire.com/products/core-products/insurancesuite/claimcenter-claims-management-software), CCC ONE
  for estimates and total-loss valuations (O*NET lists CCC products), ISO ClaimSearch, OnBase imaging, Teams.
- Licensing: Texas requires an adjuster license; the exemption for insurer employees covers only those "not regularly
  engaged in the adjustment, investigation, or supervision of insurance claims" (Tex. Ins. Code 4101.002(a)(2),
  https://texas.public.law/statutes/tex._ins._code_section_4101.002).

### Volumes (estimates, no published source found)

- Caseload: a desk auto adjuster mixing APD and lower-severity BI typically carries on the order of 60-120 open files;
  the episode gives the worker about 85 (58 regular plus 10 CAT hail files, growing). Estimate.
- Daily traffic in a CAT week: roughly 30-50 phone calls in and out, 40-70 emails, 20-40 ClaimCenter activities, 2-4
  new assignments a day on top of the regular desk. Estimate, consistent with O*NET's 5.00 ratings for telephone and
  e-mail and 4.39 for time pressure.
- CAT scale for context: Triple-I reports 5,432 hail events of 1 in. or larger in the US in 2025, 902 of them in Texas,
  the most of any state, and State Farm's top state for hail claims was Texas
  (https://www.iii.org/fact-statistic/facts-statistics-hail). The fictional company-wide CAT counts in the daily FYI
  emails (about 1,400-2,000 auto claims) are invented to be plausible for a carrier with about 190,000 auto policies.
- Total-loss profile: CCC reports the average total-loss vehicle was 10.6 years old in 2024 versus 6.8 years for
  repairable ones (https://www.cccis.com/crash-course); the totaled car in the episode is a 2015 Accord.

### Scaling to the episode

Arrivals are scaled to 16-25 a day (validator target 15-30) and about 12 scripted actions plus 1-3 live calls a day.
That keeps roughly a third to a half of a real CAT-week inbox, chosen so that every item either carries work, context
or a trap. Routine CAT traffic (dozens of identical "my car has hail" calls, auto-acknowledgments, scheduler
notifications) is represented by the daily CAT numbers email, a few new-assignment tickets and short voicemails rather
than reproduced one by one.

### Cycles

- Catastrophe surge: assignments, drive-in scheduling, daily huddle, daily numbers, end-of-week CAT report.
- Weekly large-loss roundtable (claim committee, task 21435), with reports due the day before.
- 30-day file reviews (diary), contact standards (24-hour insured contact), statutory acknowledgment and decision
  deadlines, and suit answer dates.

### Rules that shape the work (with the numbers used)

- NAIC Unfair Claims Settlement Practices Act, Model 900, Sec. 4: failing to acknowledge pertinent communications with
  reasonable promptness, failing to affirm or deny within a reasonable time, refusing to pay without a reasonable
  investigation, failing to explain a denial or compromise (https://content.naic.org/sites/default/files/model-law-900.pdf).
- NAIC Model Regulation 902: acknowledge within 15 days (Sec. 6A), reply to other pertinent communications within 15
  days (6C), accept or deny within 21 days of proof of loss (7A), notify if more time needed and every 45 days (7B);
  auto total losses include applicable taxes and fees (8A(1)-(2)), itemized deductions (8A(3)), deductible shared in
  subrogation recoveries (8D) (https://content.naic.org/sites/default/files/model-law-902.pdf).
- Texas, the state used: Tex. Ins. Code 542.003 adopts the NAIC-style list
  (https://texas.public.law/statutes/tex._ins._code_section_542.003), and 28 TAC 21.203 says acknowledgment within 15
  business days is presumed reasonably prompt and that a reasonable reservation-of-rights letter complies with the
  duty to affirm or deny (https://www.law.cornell.edu/regulations/texas/28-Tex-Admin-Code-SS-21-203). The Prompt Payment
  of Claims subchapter applies to first-party claims (542.051(2)):
  - 542.055: within 15 days of notice, acknowledge, begin the investigation, request items
    (https://texas.public.law/statutes/tex._ins._code_section_542.055);
  - 542.056(a): accept or reject in writing within 15 business days after receiving all items; (d) if more time is
    needed, say why within that period and decide within 45 days
    (https://texas.public.law/statutes/tex._ins._code_section_542.056);
  - 542.057: pay within 5 business days after notice of acceptance; 542.060: 18% a year interest plus attorney's fees
    for violations; 542.059(b): a 15-day extension only for a weather catastrophe "as defined by the commissioner";
  - 542.051(1): business day excludes Saturdays, Sundays and holidays recognized by the state; Gov't Code 662.003
    makes Veterans Day (Nov 11), Thanksgiving and the Friday after state holidays
    (https://texas.public.law/statutes/tex._gov't_code_section_662.003).
  - The exact dates in the episode: all items 10/30 or 10/31 -> decision due 11/23/2026; 11/02 -> 11/24/2026;
    11/03 -> 11/25/2026 (computed in the build script and asserted). Ignoring Veterans Day gives 11/20, 11/23, 11/24.
  - 542A (pre-suit notice for forces-of-nature claims) applies only to real-property policies (542A.001(2)), so not to
    these auto hail claims.
- Unfair practices in Texas also include failing to affirm or deny coverage or submit a reservation of rights within a
  reasonable time (Ins. Code 541.060(a)(4), https://texas.public.law/statutes/tex._ins._code_section_541.060).
- Third-party liability, Stowers duty: an insurer that fails to accept a reasonable settlement demand within policy
  limits can be liable for an excess judgment (G.A. Stowers Furniture Co. v. American Indemnity Co., 15 S.W.2d 544
  (Tex. Comm'n App. 1929), https://www.courtlistener.com/opinion/4157940/g-a-stowers-furniture-co-v-american-indemnity-co/;
  elements restated in American Physicians Ins. Exch. v. Garcia, 876 S.W.2d 842 (Tex. 1994),
  https://www.courtlistener.com/opinion/2455788/american-physicians-insurance-exchange-v-garcia/). With several
  claimants, Texas Farmers Ins. Co. v. Soriano, 881 S.W.2d 312 (Tex. 1994)
  (https://www.courtlistener.com/opinion/1660634/texas-farmers-insurance-co-v-soriano/) addresses settling with one
  claimant when others share the per-accident limit; that is why the large-loss report must cover the other two
  claimants. (The opinion text itself could not be fetched past CourtListener's search snippets; the holding is
  summarized from the case, not quoted.)
- Texas minimum limits 30/60/25 and other consumer-facing rules (15 business days to decide, rental for third parties
  based on repair time, insurer cannot require a particular shop): TDI Auto insurance guide,
  https://www.tdi.texas.gov/pubs/consumer/cb020.html.
- Suits: a Texas citation requires an answer "on or before 10:00 a.m. on the Monday next after the expiration of twenty
  days after the date of service" (TRCP 99(b)); Rule 4 governs computation
  (https://www.txcourts.gov/media/1463426/texas-rules-of-civil-procedure.pdf, compilation effective 10/01/2026). In the
  episode: served Fri 10/30 -> 20 days = Thu 11/19 -> answer due 10:00 a.m. Mon 11/23/2026.
- Fraud: a person who suspects a fraudulent insurance act must report it to the TDI fraud unit within 30 days (Ins.
  Code 701.051, https://texas.public.law/statutes/tex._ins._code_section_701.051); insurers keep antifraud plans (ch.
  704). Indicators used (coverage added with a back-dated effective date, prior unrepaired loss on the same VIN, a
  driver story that conflicts with the police report) are standard industry red flags; the company's list in the CAT
  packet is fictional.
- Privacy: GLBA's obligation to protect nonpublic personal information (15 U.S.C. 6801,
  https://www.law.cornell.edu/uscode/text/15/6801) and Texas's consumer financial and health information privacy rules
  (28 TAC ch. 22, https://www.law.cornell.edu/regulations/texas/title-28/part-1/chapter-22).
- Total-loss tax: Texas motor vehicle sales tax is 6.25% (Tax Code 152.021,
  https://texas.public.law/statutes/tex._tax_code_section_152.021). Texas has not, as far as I could find, adopted
  NAIC 902 Sec. 8 verbatim; the episode's company guideline pays tax on the adjusted value and reimburses title and
  registration on proof of replacement. That is a company practice, stated as such.
- PIP: offered on every Texas policy unless rejected in writing (Ins. Code 1952.152) and paid within 30 days of proof
  (1952.156).

### What the adjuster decides alone, and what needs someone else

Alone (within authority): contact, investigation steps, recorded statements, estimates and supplements, payments and
reserves within authority, rental within policy limits, settlement of a clear claim within authority, subrogation
demands, SIU referrals. Someone else: reserves or payments above authority (supervisor), any coverage position,
reservation of rights or denial (supervisor and counsel), acceptance, rejection or counter of a policy-limits demand
(claims manager at the roundtable), defense of suits (litigation and panel counsel), fraud findings and the TDI report
(SIU).

### Common mistakes and risks (the traps)

Communicating a coverage position or denial on one's own; responding to a Stowers demand without approval or letting
it lapse; posting reserves above authority; conceding fault on a disputed claim; disclosing one claimant's medical
information or the insured's limits to another claimant; telling an agent or insured about an SIU referral; paying a
vendor's invoice under pressure without inspection or removing the lienholder; paying a payoff to changed bank details
from a look-alike email; using a withdrawn deadline extension; acting on someone else's misaddressed file; and
miscounting statutory business days.

## 3. The week

Arcs: (1) the Bell County hail CAT surge: ten hail files, a total loss with an exact settlement and a lienholder
payoff (and a phishing payoff email), a supplement with a duplicated labor line, a rental at the policy limit, a
mobile PDR vendor pressing for direct payment, an SIU referral for a back-dated comprehensive endorsement, and the
statutory decision-due dates the CAT coordinator needs by Wednesday noon; (2) a Stowers policy-limits demand on a
September I-35 rear-end with three injured claimants and a $30,000/$60,000 policy: acknowledgment, reserve request
above authority, excess letter, large-loss report with exactly summed specials, roundtable approval, acceptance, and a
negotiated settlement with the unrepresented passenger. Background: a suit served on another insured (answer-date
computation and defense package), an excluded-driver collision whose Monday recorded statement conflicts with
Wednesday's police report, a disputed parking-lot claim, subrogation, glass, and daily CAT traffic.

Why it is representative: the most frequent and important tasks (coverage review 21417, settling and paying within
authority 21426/21423, reviewing police and medical records 21419, estimates 21420, claimant correspondence 21421/21422,
reserves 21424, file documentation 21429, inventory 21434) recur every day; less frequent but high-stakes tasks
(litigation 21432, court evidence 21431, committee 21435, SIU referral 21430, irregularities 21439) appear once each,
as they would in a heavy week. Phone calls are central (11 live calls); the human does most of the work and the
assistant is measured on what it could have drafted first.

### O*NET tasks covered by needs

21417, 21419, 21420, 21421, 21422, 21423, 21424, 21425, 21426, 21427, 21428, 21430, 21431, 21432, 21434, 21435, 21439,
21441, 21445 (19 tasks, 23 needs). 21418 (report findings) is the substance of the roundtable report need (tagged
21435), and 21429 (ClaimCenter entries) appears in 15 scripted human ClaimCenter entries rather than as a need.

Hard-number needs: total-loss settlement $12,031.56 with $3,119.16 to the owner; billed medical $36,918.42; CAT
indemnity paid $29,994.64; decision-due dates 11/23 and 11/24/2026; answer date 11/23/2026. Cross-day need: the
excluded-driver escalation joins Monday's FNOL, dec page and recorded statement with Wednesday's crash report.

### High-frequency tasks left out, and why

- 21436 supervise adjusters (supplemental, FT 5.18): the worker is a desk adjuster, not a supervisor.
- 21433 contact doctors, specialists or employers (FT 4.69): appears only lightly (wage information from the claimant);
  medical canvassing is a larger BI-unit activity than this desk carries in a CAT week.
- 21437 detailed bill review (supplemental): done by a bill-review vendor or medical auditor for BI at most carriers.
- 21440 reinsurance, 21438 titles to property, 21442 credit information, 21443 mediation or trial: rare for a personal
  auto desk adjuster in any given week.

## 4. Checks run

- `python3 -I scripts/validate_episode.py ... episodes/13-1031.00/episode.json`: OK, no errors, no size warnings
  (61 actions, 107 items, 16-25 arrivals a day, 23 needs, 10 traps, 11 calls).
- A rough oracle (`/tmp/claims-scripts/oracle.py`, not part of the project) treating each scripted human action and
  call line as a proposal: every need with a human reference fires on that reference; the needs the human never does
  (Centex duplicate, ROR draft, Pickett SIU referral) fire on nothing; no trap fires on any human action.
- A bad-proposal test: one wrong proposal per trap (accepting the demand early, telling Hector about the MRI, paying
  the vendor's invoice, using the phished payoff, the 15-day extension, telling the agent about SIU, denying Pickett,
  admitting liability to Mabry, posting the $30,000 reserve, logging the misaddressed estimate): each fires its trap
  and only its trap.
- All arithmetic in the items (business-day dates, tax, settlement, payoff split, specials, CAT totals, supplement
  net, Jordan's settlement components) is asserted in the build script.

## 5. Not sourced (estimates)

Caseload size and daily call, email and activity volumes; the authority amounts; the composing speed and every
per-action minute value; the CAT packet's reserve figures, PDR matrix and drive-in logistics; whether Texas carriers
generally pay sales tax on first-party total losses (treated as company practice); the company-wide CAT numbers; and
the Soriano holding's exact wording (opinion text not retrieved). The fictional company, people, providers, vendors and
lienholder names were not checked against registers because web search was unavailable.
