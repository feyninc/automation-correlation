# 13-2011.00 Accountants and Auditors: research for the episode

Drafted 2026-10-26 for the week of Monday 2026-11-02 to Friday 2026-11-06. The worker is Elena Brandt, CPA, Senior
Accountant at Westerby Fluid Systems, Inc. (fictional), a 642-person private industrial distributor in Grove City, Ohio,
closing October. Every number below has a source, or is labelled an estimate.

## 1. Economics

| Quantity | Value | Source |
| --- | --- | --- |
| Median hourly wage | $40.23 (2025); $83,680 annual | `data/wages-onetonline-2026-10-26.csv` (BLS OEWS May 2025 via O*NET OnLine); BLS OOH, https://www.bls.gov/ooh/business-and-financial/accountants-and-auditors.htm |
| Employment | 1,595,200 (2025) | same CSV; OOH says "about 1.6 million" |
| Projection | +5% 2025-2035 (faster than average), 115,300 openings a year | same CSV; OOH |
| Observed exposure (AEI) | 0.3478 (SOC 13-2011) | `data/aei/job_exposure.csv` |
| Loaded-cost multiplier | 1.48 | BLS ECEC, June 2026, released 2026-09-09, Table 4: private industry, management, business, and financial occupations, total compensation $88.63/h, wages and salaries $59.85/h (67.5%); 88.63 / 59.85 = 1.481. https://www.bls.gov/news.release/ecec.t04.htm |
| Loaded hourly cost | $59.58 | 40.23 x 1.481 |

Why that ECEC row: accountants are classed in "management, business, and financial" occupations. The industry rows
give similar shares (manufacturing 66.9% wages, so 1.50; professional and business services 69.5%, so 1.44); the
occupational row fits a company accountant best. All private industry: 70.0% (1.43).
(https://www.bls.gov/news.release/ecec.nr0.htm, https://www.bls.gov/news.release/ecec.t04.htm)

### Task penetration (AEI), joined on the O*NET 31.0 task text

From `data/aei/task_penetration.csv`. Frequency is the O*NET 31.0 Task Ratings FT mean (1 = yearly or less, 5 = daily,
7 = hourly or more) and the share rating it daily or more; importance is IM (1-5). `Task Ratings.txt`, `Task
Categories.txt` in `data/onet/db_31_0_text/`.

| Task ID | Task (short) | IM | FT mean | % daily+ | AEI penetration | In the week |
| --- | --- | --- | --- | --- | --- | --- |
| 21533 | Process invoices for payment | 4.54 | 4.54 | 46.1 | 0.000 | n11 |
| 21529 | Direct personnel filing, recording, transmitting records | 3.47 | 3.80 | 26.7 | 0.000 | n13 |
| 21514 | Prepare, examine, analyze accounting records and reports | 4.60 | 3.75 | 31.2 | 0.893 | n06, n07, n12, n23 |
| 21516 | Review accounts for discrepancies and reconcile | 4.47 | 3.47 | 17.6 | 0.000 | n01, n02, n19 |
| 21508 | Inspect books and systems for efficiency, accepted procedures | 4.18 | 3.47 | 23.5 | 0.000 | background only (see section 4) |
| 21515 | Prepare adjusting journal entries | 4.29 | 3.35 | 17.6 | 0.000 | n03, n04, n08, n16 |
| 21517 | Establish tables of accounts, assign entries | 3.75 | 3.25 | 12.5 | 0.937 | inside n11 (GL coding) |
| 21512 | Inspect cash, notes, securities, canceled checks | 3.71 | 3.21 | 14.3 | 0.000 | n14 |
| 21521 | Develop and document recordkeeping systems | 3.86 | 3.14 | 35.7 | 0.911 | left out |
| 21520 | Report to management on finances | 3.93 | 3.07 | 21.4 | 0.000 | n17, n18, n20 |
| 21509 | Supervise audits, determine scope | 3.86 | 3.00 | 28.6 | 0.000 | left out (auditor side) |
| 21534 | Review data on assets, liabilities, income | 3.94 | 2.88 | 17.6 | 0.000 | inside n01, n17 |
| 21510 | Confer with officials on financial and regulatory matters | 3.81 | 2.75 | 12.5 | 0.000 | n05, n21 |
| 21526 | Compute taxes owed, prepare returns | 4.29 | 2.71 | 11.8 | 0.000 | n10, n22 |
| 21507 | Detect deficient controls, fraud, non-compliance | 4.00 | 2.20 | 6.7 | 0.910 | n09, n15 |

The penetration column is bimodal for this occupation (0 or about 0.9), which reads as a matching artefact of the
task-level data rather than a measured share; the episode does not depend on it.

### Minutes model

No published time-and-motion study of a corporate senior accountant's close tasks was found. The model uses:

- Reading: 238 words a minute for non-fiction (Brysbaert 2019, https://doi.org/10.1016/j.jml.2019.104047).
- Typing: about 52 words a minute (Dhakal et al., CHI 2018, 136 million keystrokes,
  https://doi.org/10.1145/3173574.3174220); composing business prose runs at roughly a third of typing speed
  (estimate), so a 120-word reply is about 7 minutes plus a lookup.
- Accounting tasks (estimates, reasoned): a formula accrual with new inputs 15 min; a 10-line prepaid review 15 min;
  a technical memo of one page 35 min; tying a high-volume operating bank account from summary categories and three
  days of detail 60-75 min; tracing one receipt across GL, bank file and aging 25 min; a flux of 8 explained lines from
  known drivers 45 min; reviewing a drafted item takes about a fifth of doing it for workpapers (re-footing, tracing
  the items) and 1-2 minutes for a short email (reading at 238 wpm plus a check of one fact).

Per-kind defaults are in `economics.minutes_model.per_kind`; each need carries its own `minutes` with its basis.

## 2. The job as it is really done

### Employer, team, tools

BLS: 21% of accountants and auditors work in accounting, tax preparation, bookkeeping and payroll services, 8% in
finance and insurance, 8% in government (OOH, above); the rest, the largest group, are in company accounting
departments like this one. O*NET 31.0 reported titles include General Accountant, Financial Reporting Accountant and
Cost Accountant (`Sample of Reported Titles.txt`); job zone 4 (`Job Zones.txt`).

The fictional employer is a 642-person private distributor and assembler of hydraulic components, owned since 2023 by
a private equity fund, financed by an asset-based revolver and term loan, audited annually. Its finance team (CFO,
Controller, Assistant Controller, one Senior Accountant, two Staff Accountants, AP Lead plus two specialists, two AR
and credit specialists, a Payroll Manager, an FP&A Manager) is the author's estimate of a typical structure for a
$200-250 million company; no staffing benchmark was retrieved.

Tools: O*NET 31.0 Technology Skills for 13-2011.00 list as hot and in-demand technologies Microsoft Excel, Outlook, Office,
PowerPoint, SAP and Intuit QuickBooks, and include NetSuite ERP, Microsoft Dynamics, Workday, SAP Concur, Avalara AvaTax,
ADP Workforce Now and CaseWare (`Software Skills.txt`). The week uses NetSuite (GL, AP, AR, JE approval workflow),
FloQast (close checklist and reconciliations), the bank's treasury portal (statements, account analysis, payee
positive pay), Avalara AvaTax and Returns, ADP Workforce Now, Suralink (the auditors' request portal), Excel, Outlook
and Teams. NetSuite, FloQast, Suralink and Avalara are real products named for realism; their screens are described
generically.

### Daily volumes and how they were scaled

- O*NET Work Context (1-5 scale): E-Mail 4.97, Telephone Conversations 4.72, Face-to-Face 4.48, Importance of Being
  Exact or Accurate 4.66, Importance of Repeating Same Tasks 4.03, Time Pressure 3.90, Freedom to Make Decisions 3.76;
  50.0% report more than 40 hours a week, 46.4% exactly 40 (`Work Context.txt`).
- Microsoft Work Trend Index (2025-06-17): the average worker receives 117 emails and 153 Teams messages a weekday
  (https://www.microsoft.com/en-us/worklab/work-trend-index/breaking-down-infinite-workday). No accountant-specific
  count was found; during close a senior accountant plausibly sees 60-120 emails and system notifications a day
  (estimate).
- Scaled down: 16-18 arrivals a day (86 over the week, plus 17 documents, emails and calendar events already there on Monday morning), keeping every
  item that carries work and a sample of the routine traffic (NetSuite and FloQast notifications, IT and HR notices, an
  all-company email). Phone is kept at three calls because the job is phone-heavy (4.72) but most calls are short.

### The recurring cycle: the month-end close

The close calendar in the episode (`doc_close_calendar`) runs WD-1 to WD5: AP cutoff, bank recs and cash entries,
prepaids and depreciation (WD1); accruals and the shipping log (WD2); revenue cutoff, all entries approved and recs
prepared (WD3); flux and rec reviews (WD4); close review (WD5); package to the sponsor and lender on WD7. A
five-business-day close is a common target in practice. I could not retrieve a benchmark figure: APQC's and
NetSuite's pages returned 403 to this computer and no search engine was usable, so the length of the close is an
estimate here, not a sourced number.

Other dates that shape the week:

- Ohio sales tax: a vendor files the monthly UST-1 return on or before the 23rd (ORC 5739.12,
  https://codes.ohio.gov/ohio-revised-code/section-5739.12); consumer's use tax on purchases where no tax was charged
  is also due on or before the 23rd (ORC 5741.12, https://codes.ohio.gov/ohio-revised-code/section-5741.12). So
  October's returns are due Monday 11/23.
- Franklin County combined rate 8.0% (state 5.75%, county 1.25%, COTA 1.0%), Avalara 2026 rate page
  (https://www.avalara.com/taxrates/en/state-rates/ohio/counties/franklin-county.html). Ohio's own rate table
  (tax.ohio.gov) refused this computer.
- External audit: interim fieldwork in November for a December year end, with a client-prepared (PBC) list, is
  standard practice; the dates are invented.
- Biweekly payroll; the accrual formula is the company's (policy 3.2).
- Borrowing base certificate on the 20th, monthly package on WD7: typical ABL and sponsor terms, invented here.

### Rules that shape the work

- Revenue: ASC 606. Control transfers at shipment or delivery per the terms (606-10-25-30). Bill-and-hold needs all
  four criteria of 606-10-55-83: (a) a substantive reason, such as the customer's request; (b) the product identified
  separately as the customer's; (c) ready for physical transfer; (d) the entity cannot use it or direct it to another
  customer. 606-10-55-84 requires considering a custodial service obligation. Quoted from FASB ASU 2014-09, Section A,
  pp. 72-73 (https://storage.fasb.org/ASU%202014-09_Section%20A.pdf).
- Internal control: COSO's Internal Control - Integrated Framework (https://www.coso.org/guidance-on-ic). Segregation
  of duties (preparer never approves), reconciliation and review, and approval limits are the company policies in
  `doc_je_policy`. Westerby is private and not an SEC registrant, so SOX 404 management assessment does not apply; the
  lender's and sponsor's audit requirement and the company policy do the same job. NetSuite's standard Journal
  Approval permission does not by itself stop a user approving an entry they created, which is why self-approval is a
  real risk (this is the author's understanding of NetSuite, not a sourced statement).
- Payment fraud: business email compromise is the costliest fraud type in FBI IC3 data, 21,442 complaints and
  $2,770,151,146 adjusted losses in 2024 (IC3 2024 Internet Crime Report, pp. 10 and 18-19,
  https://www.ic3.gov/AnnualReport/Reports/2024_IC3Report.pdf). AFP's 2026 Payments Fraud and Control Survey: 76% of
  organizations had attempted or actual payments fraud in 2025, check fraud the most common at 58%
  (https://financialprofessionals.org/training-resources/resources/survey-research-economic-data/Details/payments-fraud).
  Nacha's fraud monitoring rule (Phase 2 effective 2026-06-19, practically 06-22) requires every non-consumer
  originator to have risk-based processes "reasonably intended to identify ACH Entries initiated due to fraud", and
  defines False Pretenses as inducing a payment by misrepresenting identity
  (https://www.nacha.org/rules/risk-management-topics-fraud-monitoring-phase-2). The vendor callback rule
  (verify at the number in the vendor master, never the one in the request) is standard practice, encoded as policy 6.1.
- Confidential data: payroll registers with SSNs go to auditors only through the audit portal (policy 7.1).

### What the worker decides alone, and what needs someone else

Alone: GL coding under the capitalization policy; approving staff entries up to $50,000; returning a positive pay
exception; how to document a rec; what to say to an internal requester while a decision is pending.
Needs someone else: approval of her own entries (Assistant Controller or Controller); bill-and-hold and other revenue
judgments (Controller); any write-off or plug of a reconciling difference (Controller); vendor bank changes (AP Lead,
after callback, with a second approver); anything that sends results outside the company (Controller or CFO);
customer refunds (AR and the Controller).

### Common mistakes and risks, as used in the week

Plugging an unreconciled difference to suspense; double-counted receipts when a manual wire entry and a prior-day bank
file import both post (the BAI2 import duplicating a manual entry is a known pattern in bank-feed matching, stated here
as practitioner knowledge, not sourced); FOB Destination shipments recognized at shipment; prepaid schedules rolled
forward with an expired line; accruing a known liability in the wrong month; missing use tax on an out-of-state
vendor's invoice; self-approval when approvers are away; refunding a credit that is the company's own posting error;
vendor bank-change email from a lookalike domain; altered-payee checks stolen from the mail; emailing PII; sending
unreviewed numbers to an owner or lender under time pressure.

## 3. The week

Two arcs plus background:

1. October close with a bank reconciliation that does not tie. GL 1010 is 3,185,586.02, the adjusted bank balance
   3,165,821.02, a difference of exactly 19,765.00 = 1,245.00 (unrecorded account analysis charge) + 90.00 (merchant
   fee keyed 4,560.00 instead of 4,650.00) + 18,430.00 (Hartline's 10/29 wire entered manually and again by the 10/30
   bank-file import). The first two are findable Monday; the third only by joining Monday's GL and bank detail with
   Tuesday's AR aging (an unapplied credit of 18,430.00 dated 10/30) and Wednesday's chat from AR. Around it: the
   prepaid review (41,766.67, not 44,266.67), payroll accrual (821,821.63), the Northfield cutoff accrual (27,300.00),
   use tax missed by the human (3,072.00), revenue cutoff (80,819.75 of FOB Destination sales, cost 58,420.00), the
   accrued expenses JE that NetSuite routes back to its own preparer, and the flux due Thursday noon.
2. Revenue pressure and the auditors: the VP Sales wants a $212,400 bill-and-hold order in October, the sponsor's
   associate asks for unreviewed October numbers for a board deck, and the auditors' interim PBC list, with an
   associate asking for the payroll register by email.

Background: AP coding questions, a vendor bank-change phishing email and its "URGENT" follow-up, a positive pay
exception on an altered-payee check (live call), a misaddressed customer-quote request, IT, HR and system notices.

All the numbers are generated by one script so that every item agrees: Sept 30 rec (bank 2,412,906.33 + DIT
54,118.62 - outstanding checks 131,406.27 = GL 2,335,618.68), the October statement and GL activity, the outstanding
check list (212,880.65), the TB (balances to the cent), the P&L (lines and totals) and the AR aging (columns foot).

Exact checks: n01 (19,765.00), n03 (41,766.67), n04 (821,821.63), n10 (3,072.00), n12 (80,819.75). Cross-day: n02
(D1 + D2 + D3) and n22 (D2 invoice + D5 Avalara note). Never done by the human: n10, n19, n22 (and the n14 call line is
a text reference).

## 4. Why it is representative, and what it leaves out

It covers 10 of the 30 O*NET tasks directly (table above), including six of the eight most frequent (21533, 21529,
21514, 21516, 21515, 21512) and the highest-importance one (21514, IM 4.60). Close week is when a company accountant's
frequent tasks cluster; a mid-month week would carry more AP and analysis and less reconciliation.

High-frequency tasks it leaves out:

- 21508 (inspect books and systems for efficiency; FT 3.47) and 21521 (develop and document recordkeeping systems;
  FT 3.14, 35.7% daily+): touched only in the status email's note that the NetSuite approval workflow should be
  fixed and Monique switching off auto-match. A systems project does not fit a close week.
- 21509 (supervise audits, scope) and 21505, 21525, 21528: the auditor's and tax examiner's side of the occupation.
  This occupation mixes company accountants with public-accounting and government auditors; the episode takes the
  company side and shows the audit from the client's chair.
- 21522, 21527, 21524: tax planning and advisory for clients, payroll audits for insurance premiums; public practice.
- 21531 (budgets): FP&A owns the budget here; the flux compares to it.

## 5. Not sourced (estimates or author's practice knowledge)

- Length of a typical monthly close (APQC and NetSuite pages refused; no search engine available).
- Accountant-specific daily email and chat volumes; the per-task minutes.
- Finance team size for a company of this size.
- That NetSuite's Journal Approval permission alone does not prevent self-approval.
- That a prior-day BAI2 import commonly duplicates manually entered wires.
- Indiana and Pennsylvania return due dates (deliberately left out of the items).
- Bank analysis, positive pay cutoff (2:00 p.m. ET) and default decision are typical bank terms, not a cited bank's.
