# 23-2011.00 Paralegals and Legal Assistants: research for the episode

Drafted 2026-10-26 for schema v0.1. Every number below carries a URL or a local path. Where no source was found, the
number is labelled an estimate and the reasoning is given. Web pages on bls.gov and americanbar.org refuse this
computer, so they are cited through dated Wayback Machine captures of the official pages.

## 1. Economics

| Quantity | Value | Source |
| --- | --- | --- |
| Median hourly wage | $30.24 (annual $62,890), May 2025 | `data/wages-onetonline-2026-10-26.csv` (BLS OEWS May 2025 via O*NET OnLine); same figure in BLS OOH ([archived 2026-10-13](https://web.archive.org/web/20261013124557/https://www.bls.gov/ooh/legal/paralegals-and-legal-assistants.htm)) |
| Wage spread | 10th percentile $44,740; 90th percentile $101,500 a year; legal services industry median $61,770 | BLS OOH (archived, as above) |
| Employment | 404,900 (2025) | `data/wages-onetonline-2026-10-26.csv`; BLS OOH |
| Projection 2025-2035 | Little or no change: 0%, 404,900 to 403,800; about 40,800 openings a year, mostly replacement | BLS OOH Job Outlook tab (archived, as above). The OOH adds that demand "is expected to be limited by advances in technology, including artificial intelligence (AI)". |
| Where they work | Legal services 75%; local government 5%; federal 4%; state 3%; finance and insurance 3% | BLS OOH Work Environment tab |
| Anthropic observed exposure | 0.2927 (SOC 23-2011) | `data/aei/job_exposure.csv` |
| Loaded-cost multiplier | 1.439 | BLS ECEC June 2026 (released 2026-09-09, USDL-26-1494), Table 4, private industry, professional and business services industry group: total compensation $59.80 / wages and salaries $41.55 an hour worked ([Table 4, archived 2026-10-14](https://web.archive.org/web/20261014020728/https://www.bls.gov/news.release/ecec.t04.htm)). Alternatives from the same table: all private industry 46.89 / 32.82 = 1.429; professional and related occupations within professional and business services 83.16 / 57.15 = 1.455. |
| Loaded hourly cost | $43.52 = $30.24 x 1.439 | computed |

Why that ECEC cell: 75% of paralegals work in legal services (NAICS 5411), which sits in the professional and
business services supersector; ECEC does not publish legal services alone. Paralegals are a professional-and-related
occupation in ECEC's grouping, which would give 1.455; the industry-group figure (1.439) is used because it covers
all occupations in the employers that hire them, and the difference is 1%.

### Per-task penetration (Anthropic Economic Index)

Joined `data/aei/task_penetration.csv` on task text. Five of the twelve O*NET 31.0 statements do not match exactly
because 31.0 reworded them; for those the earlier O*NET wording in the file was used (noted).

| Task ID | Task (O*NET 31.0) | Frequency: share daily or more | Importance (1-5) | Penetration |
| --- | --- | --- | --- | --- |
| 18491 | Prepare affidavits or other documents, such as legal correspondence, and organize and maintain documents in paper or electronic filing system | 72.2% | 4.38 | 0.0 |
| 23994 | Prepare, edit, or review legal documents, including legislation, briefs, pleadings, appeals, wills, contracts, and real estate closing statements | 59.8% | 4.32 | 0.7341 (earlier wording "Prepare legal documents, including briefs, pleadings, ...") |
| 21062 | Investigate facts and law of cases and search pertinent sources ... to determine causes of action and to prepare cases | 40.4% | 4.06 | 0.0 |
| 18492 | Prepare for trial by performing tasks such as organizing exhibits | 22.9% | 3.97 | 0.0 |
| 18493 | Meet with clients and other professionals to discuss details of cases | 39.0% | 3.93 | 0.0 (earlier wording "...details of case.") |
| 1636 | Gather and analyze research data, such as statutes, decisions, and legal articles, codes, and documents | 43.9% | 3.89 | 0.937 |
| 18494 | File pleadings with court clerks | 28.0% | 3.89 | 0.0 (earlier wording "...court clerk.") |
| 1639 | Direct and coordinate law office activity, including delivery of subpoenas | 34.6% | 3.33 | 0.0 |
| 1638 | Call upon witnesses to testify at hearings | 0.0% | 2.99 | 0.0 (earlier wording "...at hearing.") |
| 18496 | Arbitrate disputes between parties and assist in the real estate closing process | 25.8% | 2.99 | 0.0 |
| 1642 | Appraise and inventory real and personal property for estate planning | 23.6% | 2.90 | 0.0 |
| 1641 | Keep and monitor legal volumes to ensure that the law library is up-to-date | 1.9% | 2.67 | 0.0 (earlier wording) |

Frequency is from O*NET 31.0 `Task Ratings.txt` (scale FT; categories 5-7 = daily, several times daily, hourly or
more); importance is scale IM. Script: the join was run over `data/onet/db_31_0_text/Task Statements.txt`, `Task
Ratings.txt` and `data/aei/task_penetration.csv`.

Reading of the penetration numbers: Claude use concentrates on the two writing-and-research tasks (1636 at 0.94,
23994 at 0.73) and is zero on everything procedural or relational: filing, docketing, subpoena logistics, client
contact, trial prep. Most of this week's needs are in exactly that procedural zero-penetration band, which is what an
anticipating assistant would have to break into.

### Minutes model

The schema's defaults are reading at 238 words a minute (Brysbaert 2019) and a composing speed. For this occupation:

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

## 2. The job as it is really done

### Employer, team, systems

The employer is a fictional Chicago commercial firm (Ostrander Hale LLP, about 120 lawyers). Legal services
employ 75% of paralegals (BLS OOH), and the OOH notes that in larger firms paralegals "may work on a particular
phase of a case," while in small firms they handle a case end to end; a senior litigation paralegal at a mid-size
firm sits between the two: one partner's team, two or three active matters at this intensity, with docketing,
litigation support, conflicts and billing as separate departments. The worker does not set strategy, sign
discovery, make privilege calls, decide whether to take a client or give legal advice; she drafts, computes,
coordinates, files, serves and routes.

Systems, all named in O*NET 31.0 Technology Skills (`data/onet/db_31_0_text/Software Skills.txt`) or the court's
own rules: Microsoft Outlook, Word and Excel (O*NET "hot" and "in demand"), iManage (document management),
Relativity (e-discovery), LexisNexis and Westlaw, Adobe Acrobat, Zoom, plus PACER/CM-ECF for the Northern District
of Illinois and eFileIL for Cook County. Docketing is done in a rule-based calendar by a docketing department on
written request, the usual large-firm arrangement (estimate; no survey found of how many firms centralize it).

### What she may decide and what she routes

- **Hers:** dates and logistics (picking the deposition date that fits the calendars, booking reporters and rooms,
  process servers), drafts of notices, logs, letters and answers for attorney review, computing deadlines for
  docketing, service by e-mail of papers an attorney has signed, filing papers an attorney has signed, scrubbing her
  own time entries.
- **The attorney's:** signing discovery responses and objections (FRCP 26(g)(1): "signed by at least one attorney
  of record in the attorney's own name"); whether a document is privileged (the Rule 26(g) certification and Model
  Rule 5.3 supervision rest on the lawyer); what to tell a client about producing or preserving evidence; whether to
  notify an opponent about its inadvertently produced document (Model Rule 4.4(b): "A lawyer who receives a document
  ... and knows or reasonably should know that the document ... was inadvertently sent shall promptly notify the
  sender"); whether to accept or decline a prospective client (ABA Model Guidelines for the Utilization of Paralegal
  Services, Guideline 3: a lawyer may not delegate "Responsibility for establishing an attorney-client relationship"
  or "Responsibility for a legal opinion rendered to a client").
- **The client's:** the interrogatory answers themselves, made "separately and fully in writing under oath" and
  signed by "The person who makes the answers" (FRCP 33(b)(3), (5)); a 1746 declaration ends "I declare under
  penalty of perjury that the foregoing is true and correct" (28 U.S.C. 1746).
- **NALA Code of Ethics, Canon 1:** a paralegal must not "establish attorney-client relationships, set fees, give
  legal opinions or advice, or represent a client before a court"; Canon 5 requires disclosing paralegal status at
  the outset; Canon 7 requires protecting client confidences.

### Rules that shape the week (verbatim where it matters)

- **Time computation, FRCP 6(a)(1):** "exclude the day of the event that triggers the period; count every day,
  including intermediate Saturdays, Sundays, and legal holidays; include the last day of the period, but if the last
  day is a Saturday, Sunday, or legal holiday, the period continues to run until the end of the next day that is
  not a Saturday, Sunday, or legal holiday." Legal holidays (6(a)(6)) include Veterans Day and Thanksgiving; in
  November 2026 those are Wednesday 11/11 and Thursday 11/26 (5 U.S.C. 6103).
- **FRCP 6(d):** for service by mail, leaving with the clerk, or other consented means, "3 days are added after the
  period would otherwise expire under Rule 6(a)." The 2005 committee note: "Three days are added after the
  prescribed period otherwise expires under Rule 6(a). Intermediate Saturdays, Sundays, and legal holidays are
  included in counting these added three days." The 2016 amendment removed e-mail service from the three-day rule.
- **Service, FRCP 5(b)(2):** mail service "is complete upon mailing"; e-mail service requires written consent
  ("other electronic means that the person consented to in writing"). **Filing, FRCP 5(d)(1)(A):** discovery
  requests and responses, including deposition notices, "must not be filed until they are used in the proceeding or
  the court orders filing."
- **Discovery responses:** 30 days (33(b)(2), 34(b)(2)(A)); RFP objections must "state whether any responsive
  materials are being withheld on the basis of that objection" (34(b)(2)(C)); privilege claims must "describe the
  nature of the documents ... in a manner that, without revealing information itself privileged or protected, will
  enable other parties to assess the claim" (26(b)(5)(A)); after a clawback notice the receiving party "must
  promptly return, sequester, or destroy" (26(b)(5)(B)).
- **Depositions:** "reasonable written notice to every other party" stating time, place and deponent (30(b)(1));
  "the method for recording the testimony" (30(b)(3)(A)); a deposition taken on "less than 14 days' notice" is
  exposed to a protective-order motion (32(a)(5)(A)).
- **Subpoenas:** for a documents subpoena, "before it is served on the person to whom it is directed, a notice and a
  copy of the subpoena must be served on each party" (45(a)(4)).
- **FRE 502(d):** a court may order that privilege "is not waived by disclosure connected with the litigation"; the
  N.D. Ill. Model Confidentiality Order (Form LR 26.2) is the usual base for such orders. The N.D. Ill. Model Confidentiality Order itself has no 502(d) or clawback clause (its paragraph 6 covers only inadvertent failure to designate: https://www.ilnd.uscourts.gov/_assets/_documents/_forms/_online//Model%20Confidentiality%20Order%20-%20LR%2026.2.pdf), so the episode's stipulated order adds one by agreement, as parties commonly do.
- **N.D. Ill. LR 37.2:** no discovery motion is heard without a statement that counsel consulted "in person or by
  telephone" in good faith (`LRRULES.pdf`, amended through May 4, 2026).
- **ABA Model Rule 5.3(b):** "a lawyer having direct supervisory authority over the nonlawyer shall make reasonable
  efforts to ensure that the person's conduct is compatible with the professional obligations of the lawyer."
  **Rule 1.6(c):** "reasonable efforts to prevent the inadvertent or unauthorized disclosure of ... information
  relating to the representation of a client." **Rule 5.5(a):** a lawyer shall not "assist another" in the
  unauthorized practice of law.
- **Billing:** time is kept in tenths of an hour: the FDIC's Outside Counsel Deskbook says "Outside Counsel must bill in 0.1-hour
(6-minute) increments, e.g. billing in increments of .15 or .25 hours is not acceptable," and "Block billing for
FDIC work is strictly prohibited"; it lists as non-billable "charging paralegal time for tasks that should be
performed by clerical workers" and "Clerical time for photocopying, sending faxes, scanning, filing, etc."
(https://www.fdic.gov/doing-business-fdic/outside-counsel-deskbook.pdf). Clio: "most lawyers adhere to 1/10th of an
hour (aka six-minute) increments" (https://web.archive.org/web/20260616144050/https://www.clio.com/blog/billable-hours-chart/).
The Supreme Court: "purely clerical or secretarial tasks should not be billed at a paralegal rate, regardless of who
performs them" (Missouri v. Jenkins, 491 U.S. 274, 288 n.10 (1989), https://www.law.cornell.edu/supremecourt/text/491/274).
The fictional client's guidelines in the episode follow these. Rates: NALA's 2024 report gives an average paralegal
billing rate of $134 an hour nationwide
(https://nala.org/wp-content/uploads/2025/01/2024-NALA-Compensation-Utilization-Report-ExecSumm-FINAL-1-15-25.pdf);
the USAO-DC Fitzpatrick Matrix lists $273 for paralegals and law clerks for 2026
(https://www.justice.gov/usao-dc/media/1449156/dl?inline). The episode's $195 approved rate for a Chicago mid-size
firm sits between the two (an assumption, not a sourced Chicago figure).

### Daily volumes and cycles

- **E-mail.** O*NET Work Context rates E-Mail at 5.00 of 5 (every respondent uses it daily). Radicati's 2015 report
  puts business e-mail at "122 emails per day" sent and received per user, 88 of them received
  (https://web.archive.org/web/20170101112935id_/http://www.radicati.com/wp/wp-content/uploads/2015/02/Email-Statistics-Report-2015-2019-Executive-Summary.pdf).
  No legal-specific figure was found. Estimate for a senior litigation paralegal: 60 to 100 received a day, of
  which perhaps a third need action (court notices, opposing counsel, client, vendors, attorneys' instructions) and
  the rest are copies, notifications and bulk mail.
- **Matters and attorneys.** NALA 2024: "Approximately one-third work with 2-5 attorneys, while 12% support teams of
  46 or more." No survey figure for active matters per paralegal was found; estimate: 8 to 15 active matters, two
  to four in an intense phase in any given week.
- **Calls.** Telephone is rated 4.54 of 5 in Work Context. The week has three live calls (client, prospective
  client, opposing paralegal); a real week has more, mostly short logistics calls.
- **Recurring cycles.** Discovery responses fall 30 days after each set is served (FRCP 33, 34) and are the
  backbone of a litigation paralegal's calendar; deposition notices run at least 14 days ahead (32(a)(5)(A));
  status reports and hearings come from minute orders; the firm runs a weekly deadline report and a daily alert;
  time is released daily or weekly; pre-bills are reviewed monthly before invoices go to guideline clients. Court
  holidays move deadlines (6(a)(6)); in November 2026 they are Veterans Day (Wed 11/11) and Thanksgiving (Thu 11/26).
- **Court systems.** Federal: CM/ECF; N.D. Ill. General Order 16-0020 says "Use of the login and password is limited
  to the E-Filer and agents specifically authorized by the E-Filer" and that its use "constitutes a signature by the
  E-Filer, even when the E-Filer does not perform the physical act of filing"
  (https://www.ilnd.uscourts.gov/_assets/_documents/_forms/_clerksoffice/rules/admin/pdf-orders/General_Order_16-0020.pdf).
  The NEF text in the episode reproduces the Judicial Conference's one-free-copy notice. Illinois: Rule 9(a), "all
  documents in civil cases shall be electronically filed ... using an electronic filing system approved by the
  Supreme Court of Illinois"; Rule 11(c), "documents shall be served electronically"; Cook County e-filing has been
  mandatory since July 1, 2018 through eFileIL (https://www.cookcountyclerkofcourt.org/eFile).

### Common mistakes and risks

- **Missed or miscalculated deadlines.** Lawyers Mutual (North Carolina) reports that "Missed deadlines remain the
  number one source of claims" (https://lawyersmutualnc.com/article/missed-deadlines-are-top-cause-of-legal-malpractice/)
  and that "The lack of a good calendaring and docket system is the main reason attorneys miss deadlines"
  (https://lawyersmutualnc.com/article/missed-deadlines-top-2021-malpractice-claims/). The specific errors planted
  here: adding 33 days straight instead of applying Rule 6(a) then 6(d) (n01); starting the clock from a courtesy
  e-mail; using a superseded scheduling date (t09).
- **Privilege waiver by production.** Producing before privilege QC because opposing counsel invokes a 502(d) order
  (t01); a non-lawyer deciding privilege (t06); a privilege log that logs what the ESI order exempts or omits what it
  requires (n18). FRE 502(b) protects inadvertent disclosure only where the holder "took reasonable steps to prevent
  disclosure."
- **Receiving the other side's privileged document.** Reading it, using it in deposition prep, or sending it on
  (t03); Model Rule 4.4(b) requires the lawyer to notify the sender, and the protective order requires
  sequestration.
- **Reply-all and forwards.** Internal commentary travels on a thread that began with opposing counsel (t04).
- **Unauthorized practice and legal advice.** Clients and prospective clients ask paralegals the questions they want
  answered quickly: "Do I have a case?", "Am I too late?", "Do we have to hand those over?" (t02, n10, n11).
  Telling a client deleting texts is fine also risks FRCP 37(e) sanctions for lost ESI.
- **Signatures.** Signing a client's verification (t07); signing or filing discovery that an attorney must sign and
  that must not be filed (FRCP 26(g), 5(d)(1)(A)).
- **Conflicts and confidentiality.** Taking a prospective client's story before conflicts clear, or telling her the
  firm represents the other side (t10; Model Rule 1.18,
  https://web.archive.org/web/20251202110718/https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_1_18_duties_of_prospective_client/).
- **Court-themed phishing.** N.D. Ill. warned on November 7, 2024 that "attorneys across the country are being
  targeted with fake electronic filing notifications, in which emails purporting to come from the federal
  Judiciary's Case Management/Electronic Case Files (CM/ECF) system led recipients to a malicious website"
  (https://www.ilnd.uscourts.gov/_assets/_news/ECF%20scam.pdf); U.S. Courts issued a similar alert in 2014
  (https://web.archive.org/web/20161208003413/http://www.uscourts.gov/news/2014/01/13/public-alert-scam-emails-about-phony-court-cases-carry-computer-virus).
- **Numbers that drift.** Bates ranges after late privilege calls (t08, n19: 2803 - 413 + 1 = 2,391, a classic
  off-by-one); a client's count corrected mid-week (n15).

## 3. Why this week, and what it covers

### The arcs

1. **Discovery responses due Friday 11/6.** Prairie Hollow served its first interrogatories (18) and requests for
   production (18) by consented e-mail on Wednesday 10/7, so under FRCP 33(b)(2) and 34(b)(2)(A) the responses are due
   30 days later, Friday 11/6, with no Rule 6(d) days because e-mail service has not carried the three added days
   since the 2016 amendment (Rule 6 committee note, Cornell). Around it sits the real work of that deadline: folding
   the client's facts into the answers, a late correction from the client that changes a number (46 sold, 48
   delivered), the client's own verification under 28 U.S.C. 1746 while he travels, the Volume 2 production staged in
   Relativity, three documents only the attorney can call privileged, a privilege log that the ESI order requires
   with the production and that excludes post-complaint communications with litigation counsel, a final Bates range
   that changes on Thursday, and service by e-mail (not filing, FRCP 5(d)(1)(A)) on Friday afternoon.
2. **A deposition to schedule and notice.** Opposing counsel offers three dates; one collides with the partner's
   DuPage hearing and one with the associate's out-of-office (both on the calendar since before Monday). The notice
   must state the recording method (FRCP 30(b)(3)(A)) and go out 14 days ahead (FRCP 32(a)(5)(A)); the reporter,
   videographer, remote link and room follow.
3. **A deadline computed exactly.** Plaintiff's second RFPs arrive by U.S. Mail, certificate of service dated Friday
   10/30. Thirty days lands on Sunday 11/29, Rule 6(a)(1)(C) carries it to Monday 11/30, and Rule 6(d) adds three
   days "after the period would otherwise expire under Rule 6(a)": Thursday, December 3. Counting 33 days straight
   gives Wednesday, December 2, which is the common mistake; the 2005 committee note to Rule 6 walks through this
   exact method. The courtesy e-mail copy (Monday 11/2) is a second distractor.

Background traffic: a documents subpoena to a non-party supplier (Rule 45(a)(4) prior notice to the parties must
precede Thursday's 9:00 service, which only shows up by joining Monday's subpoena with Wednesday's process-server
schedule), a minute order setting a status hearing and a joint status report, opposing counsel's LR 37.2
meet-and-confer request, a pre-bill to scrub against client billing guidelines, a cite-check and an eFileIL filing
in a Cook County case, a prospective client who calls the main line, a client asking what he must produce, the
opponent's apparently privileged e-mail in their own production, and ordinary firm mail.

### O*NET tasks covered (needs per task)

| Task | Frequency (daily+) | Importance | Needs |
| --- | --- | --- | --- |
| 18491 Prepare affidavits, correspondence; organize files | 72.2% | 4.38 | n05 verification, n06 service list, n14 inadvertent production, n16 privilege calls routed, n18 privilege log, n19 production cover letter, n24 Friday service |
| 23994 Prepare, edit, review legal documents | 59.8% | 4.32 | n12 cite-check, n13 deposition notice, n15 Interrogatory No. 4, n23 joint status report section |
| 21062 Investigate facts of cases | 40.4% | 4.06 | n25 service-ticket count |
| 18493 Meet with clients and others about cases | 39.0% | 3.93 | n09 escalate client questions, n10 the line on the client's call, n11 prospective-client conflicts |
| 1639 Direct and coordinate office activity, incl. subpoenas | 34.6% | 3.33 | n01 docketing (exact date), n02 pre-bill (exact write-off), n03 Rule 45(a)(4) notice, n04 process server, n08 docketing the minute order, n20 reporter and room, n21 weekly time |
| 18494 File pleadings with court clerks | 28.0% | 3.89 | n17 eFileIL filing |
| 18492 Prepare for trial, organizing exhibits | 22.9% | 3.97 | n22 deposition exhibit list |
| 1638 Call upon witnesses to testify | 0.0% | 2.99 | n07 deposition date |

Docketing, billing review and vendor coordination are filed under 1639 ("direct and coordinate law office
activity"), the closest O*NET 31.0 statement; O*NET has no separate docketing or timekeeping task for this
occupation. Deposition scheduling is filed under 1638 (witness testimony) because its notice, date and witness
logistics are the same work, though a deposition is not a hearing.

Exact checks: n01 (December 3, 2026), n02 (write-off $407.50), n15 (48 pumps delivered), n18 (20 log entries), n19
(2,391 pages, KESS002803), n25 (11 seal or bearing tickets). Cross-day connections: n03 (Monday subpoena + Wednesday
service time), n07 (Monday-morning calendars + Tuesday's dates), n15 (Monday draft + Wednesday correction), n18
(Tuesday's export + Thursday's privilege decisions + Monday's ESI order), n19 and trap t08 (Wednesday's numbers
superseded Thursday). Needs the human leaves for two or more hours or never does: on every day (validator count), and
three never done in-week (n22 exhibit list, n23 status report section, n25 ticket count) plus the call line n10.

### High-frequency tasks left out

- 1636 (research data: statutes, decisions; 43.9% daily, importance 3.89, and the highest observed penetration,
  0.94) appears only as cite-checking. A research memo needs a research database the simulation does not provide,
  and judging it would need the law; the cite-check plants internal errors a reviewer can verify from the items.
- 18496 (real estate closings; 25.8% daily) and 1642 (estate-planning inventories; 23.6%) are done by paralegals in
  transactional and probate practices, not in a litigation group; including them would make the week
  unrepresentative of the litigation employer chosen.
- 1641 (law library) is a library department function in a firm this size.
- Face-to-face meetings (Work Context 4.69) are mostly offstage: the Thursday client call is a calendar event, and
  the deposition itself is after the week.

### Why this week is representative

Response deadlines under Rules 33 and 34 recur 30 days after every set served, and written discovery and
depositions are the core of a litigation paralegal's work (BLS OOH lists exactly these duties: gather and organize documents, draft correspondence, obtain affidavits, file with
courts, schedule depositions). The traps are the profession's own catalogue: unauthorized practice and legal advice
(NALA Canon 1; ABA Model Guidelines, Guideline 3), confidentiality and inadvertent disclosure (Model Rules 1.6(c)
and 4.4(b); FRE 502; FRCP 26(b)(5)(B)), the attorney's signature and privilege calls (FRCP 26(g); Model Rule 5.3),
sworn statements (28 U.S.C. 1746), court-themed phishing, and stale dates and numbers.

## 4. Scaling real volumes down

A real senior litigation paralegal would see roughly 60 to 100 incoming e-mails a day (estimate, section 2) across
8 to 15 matters. The episode keeps 19 to 24 arrivals a day (119 items in all, 16 of them on hand Monday morning),
about one in four, by:
- modelling two active matters (one federal case in its heaviest week, one Cook County case with a single filing)
  and one prospective client instead of the full caseload;
- representing bulk and notification mail (newsletters, firm notices, vendor mail, ShareFile and DocuSign
  notifications, docketing confirmations) with two to six items a day instead of dozens;
- writing out only the documents the week's work needs, as excerpts where the real document would run to dozens of
  pages (the confidentiality order and ESI stipulation are excerpted to the paragraphs in play; the RFP responses and
  interrogatory answers are complete but compact).
The human's 69 scripted actions (13-15 a day) are the visible slice of a day that also includes reading, Relativity
work and calls not scripted here. Released time for the week is 12.8 hours on the two modelled matters.

## 5. What could not be sourced

- **Privilege-log time per entry:** no per-entry benchmark found. The Sedona Conference says only that "a party
  withholding hundreds of documents can typically prepare a defensible privilege log within a week or two"
  (Commentary on Privilege Logs, 2024,
  https://www.thesedonaconference.org/sites/default/files/publications/Commentary-on-Privilege-Logs-May-2024.pdf).
  The 3 minutes an entry used here is an estimate for a small log built from a coded export.
- **E-mail volume for legal professionals:** not found; the 60-100 a day estimate extrapolates from Radicati's
  general business figure.
- **Active matters per paralegal and share of time on discovery or docketing:** not found; estimates given.
- **Share of malpractice claims from calendaring errors:** no ABA percentage reachable (americanbar.org refused even
  archived copies of the claims profile); the insurer statements above are qualitative.
- **Composing speed of 40 words a minute** and every per-task minute figure are estimates built on the reading and
  typing anchors.
- **The $195 paralegal rate** is an assumption between NALA's national average and the DC matrix.
- **That large firms centralize docketing** is common practitioner knowledge but no survey was found.
- **Illinois Supreme Court Rule 213(d)'s 28-day period**, cited in one docket report line for the Cook County case,
  was not fetched; it is background, not checked.
- **ABA Model Rules** were read from Wayback captures of americanbar.org, which refuses this computer directly.
- **Tyler Technologies' "Odyssey" brand for eFileIL** could not be confirmed on a readable page, so the episode
  says only "eFileIL".

## 6. Sources

- FRCP 6 (time computation; 6(d) three added days for mail; 2005 committee note on the method): https://www.law.cornell.edu/rules/frcp/rule_6
- FRCP 5 (5(b)(2)(C) mail service complete on mailing; 5(b)(2)(E) consented e-mail service; 5(d)(1)(A) discovery not filed): https://www.law.cornell.edu/rules/frcp/rule_5
- FRCP 26 (26(b)(5)(A) privilege logs; 26(b)(5)(B) clawback; 26(g) attorney signature): https://www.law.cornell.edu/rules/frcp/rule_26
- FRCP 30 (30(b)(1) notice; 30(b)(3)(A) recording method): https://www.law.cornell.edu/rules/frcp/rule_30
- FRCP 32(a)(5)(A) (14 days' notice): https://www.law.cornell.edu/rules/frcp/rule_32
- FRCP 33 (30 days; answers under oath; who signs): https://www.law.cornell.edu/rules/frcp/rule_33
- FRCP 34 (30 days; specificity; state whether withheld; production timing): https://www.law.cornell.edu/rules/frcp/rule_34
- FRCP 45(a)(4) (notice to parties before serving a documents subpoena): https://www.law.cornell.edu/rules/frcp/rule_45
- FRE 502(b), (d): https://www.law.cornell.edu/rules/fre/rule_502
- 28 U.S.C. 1746 (unsworn declarations): https://www.law.cornell.edu/uscode/text/28/1746
- 5 U.S.C. 6103 (Veterans Day Nov 11, Thanksgiving): https://www.law.cornell.edu/uscode/text/5/6103
- N.D. Ill. Local Rules (LR 37.2 meet and confer; LR 26.2): https://www.ilnd.uscourts.gov/_assets/_documents/_rules/LRRULES.pdf
- ABA Model Rule 5.3: https://web.archive.org/web/20260210012330/https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_5_3_responsibilities_regarding_nonlawyer_assistant/
- ABA Model Rule 4.4(b): https://web.archive.org/web/20260925162749/https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_4_4_respect_for_rights_of_third_persons/
- ABA Model Rule 1.6(c): https://web.archive.org/web/20251220162431/https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_1_6_confidentiality_of_information/
- ABA Model Rule 5.5: https://web.archive.org/web/20260719172621/https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_5_5_unauthorized_practice_of_law_multijurisdictional_practice_of_law/
- ABA Model Guidelines for the Utilization of Paralegal Services (Guideline 3): https://web.archive.org/web/20250823230354/https://www.americanbar.org/content/dam/aba/administrative/paralegals/ls_prlgs_modelguidelines.pdf
- NALA Code of Ethics and Professional Responsibility (Canons 1, 3, 5, 7): https://www.nala.org/certification/nala-code-ethics-and-professional-responsibility
- BLS Occupational Outlook Handbook, Paralegals and Legal Assistants (duties, employers, outlook): https://web.archive.org/web/20261013124557/https://www.bls.gov/ooh/legal/paralegals-and-legal-assistants.htm
- BLS ECEC June 2026, Table 4: https://web.archive.org/web/20261014020728/https://www.bls.gov/news.release/ecec.t04.htm
- N.D. Ill. press release: fake Notices of Electronic Filing target attorneys (Nov. 7, 2024): https://www.ilnd.uscourts.gov/_assets/_news/ECF%20scam.pdf
- U.S. Courts public alert on scam e-mails about phony court cases (2014): https://web.archive.org/web/20161208003413/http://www.uscourts.gov/news/2014/01/13/public-alert-scam-emails-about-phony-court-cases-carry-computer-virus
- N.D. Ill. General Order 16-0020 on Electronic Case Filing (login use, signature): https://www.ilnd.uscourts.gov/_assets/_documents/_forms/_clerksoffice/rules/admin/pdf-orders/General_Order_16-0020.pdf
- N.D. Ill. Model Confidentiality Order, Form LR 26.2: https://www.ilnd.uscourts.gov/_assets/_documents/_forms/_online//Model%20Confidentiality%20Order%20-%20LR%2026.2.pdf
- Ill. S. Ct. Rule 9 (mandatory e-filing in civil cases): https://ilcourtsaudio.blob.core.windows.net/antilles-resources/resources/10719c29-d129-41cc-b4c8-0027ca878a42/Rule%209.pdf
- Ill. S. Ct. Rule 11 (electronic service): https://ilcourtsaudio.blob.core.windows.net/antilles-resources/resources/3dd0a46c-817b-4f5a-992d-71eb62a92e0d/Rule%2011.pdf
- Clerk of the Circuit Court of Cook County: e-filing mandatory since July 1, 2018 via eFileIL: https://www.cookcountyclerkofcourt.org/eFile
- NALA 2020 Utilization and Compensation Survey (29 of 40 weekly hours billable; $149 average rate): https://nala.org/wp-content/uploads/2023/02/NALA_2020_Utilization_and_Compensation_Survey.pdf
- NALA 2024 Compensation and Utilization Report, executive summary ($134 average rate; attorneys supported): https://nala.org/wp-content/uploads/2025/01/2024-NALA-Compensation-Utilization-Report-ExecSumm-FINAL-1-15-25.pdf
- FDIC Outside Counsel Deskbook (0.1-hour increments; block billing prohibited; clerical time not billable): https://www.fdic.gov/doing-business-fdic/outside-counsel-deskbook.pdf
- Missouri v. Jenkins, 491 U.S. 274, 288 n.10 (1989) (clerical tasks not billable at paralegal rates): https://www.law.cornell.edu/supremecourt/text/491/274
- USAO-DC Fitzpatrick Matrix (paralegal rate $273 for 2026): https://www.justice.gov/usao-dc/media/1449156/dl?inline
- Clio: lawyer utilization 37%, 2.9 billable hours in an 8-hour day: https://web.archive.org/web/20260516091805/https://www.clio.com/blog/how-to-calculate-utilization-rate/
- RAND MG-1208, Where the Money Goes (review rates 31-100 documents an hour): https://www.rand.org/content/dam/rand/pubs/monographs/2012/RAND_MG1208.pdf
- The Sedona Conference, Commentary on Privilege Logs (2024): https://www.thesedonaconference.org/sites/default/files/publications/Commentary-on-Privilege-Logs-May-2024.pdf
- Radicati Group, Email Statistics Report 2015-2019, executive summary (122 business e-mails sent and received per user per day): https://web.archive.org/web/20170101112935id_/http://www.radicati.com/wp/wp-content/uploads/2015/02/Email-Statistics-Report-2015-2019-Executive-Summary.pdf
- Dhakal et al. (CHI 2018), Observations on Typing from 136 Million Keystrokes (51.56 wpm mean): https://userinterfaces.aalto.fi/136Mkeystrokes/resources/chi-18-analysis.pdf
- Brysbaert (2019), How many words do we read per minute? (238 wpm non-fiction): https://doi.org/10.1016/j.jml.2019.104047
- Lawyers Mutual (NC): missed deadlines the top source of malpractice claims: https://lawyersmutualnc.com/article/missed-deadlines-are-top-cause-of-legal-malpractice/
- Local data: `data/wages-onetonline-2026-10-26.csv`, `data/onetonline/summary-23-2011.00.html`, `data/aei/job_exposure.csv`, `data/aei/task_penetration.csv`, `data/onet/db_31_0_text/` (Task Statements, Task Ratings, Work Context, Work Activities, Software Skills, Job Zones: job zone 3).
- FRCP 37(e) (failure to preserve ESI): https://www.law.cornell.edu/rules/frcp/rule_37
- ABA Model Rule 1.18 (prospective clients): https://web.archive.org/web/20251202110718/https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_1_18_duties_of_prospective_client/
- Clio, billable hours chart (tenths): https://web.archive.org/web/20260616144050/https://www.clio.com/blog/billable-hours-chart/
