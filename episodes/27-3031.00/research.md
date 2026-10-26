# 27-3031.00 Public Relations Specialists: research for the episode

Draft, 2026-10-26. The week: Monday 2026-11-02 to Friday 2026-11-06. Employer: Prairie Bend Health, a fictional
nonprofit regional hospital system. Worker: Erin Lindqvist, PR specialist in media relations.

Every number below has a URL or a local path. Where no source exists, the number is marked **estimate** and the
reasoning is given.

## 1. Economics

| Quantity | Value | Source |
| --- | --- | --- |
| Median hourly wage | $35.94 (annual $74,750), 2025 | BLS OEWS May 2025 via O*NET OnLine: `data/wages-onetonline-2026-10-26.csv`; `data/onetonline/summary-27-3031.00.html`; https://www.onetonline.org/link/summary/27-3031.00 |
| Employment | 314,500 (2025) | same file; BLS OOH https://www.bls.gov/ooh/media-and-communication/public-relations-specialists.htm |
| Projection 2025-2035 | "Slower than average (1% to 2%)"; OOH: +2%, 314,500 to 320,200 (+5,700); about 23,000 openings a year | `data/onetonline/summary-27-3031.00.html` (the CSV's projection columns are blank for this code, so they were filled from the saved O*NET OnLine page); BLS OOH (URL above) |
| Observed exposure (AEI) | 0.453 | `data/aei/job_exposure.csv`, row 27-3031 (Anthropic Economic Index, labor market impacts, 2026-03-05) |
| Loaded-cost multiplier | 1.523 (private industry, hospitals: total compensation $66.85/h, wages $43.88/h, wages 65.6% of the total, June 2026) | BLS ECEC June 2026, released 2026-09-09, Table 4: https://www.bls.gov/news.release/ecec.t04.htm |
| Loaded hourly wage | $54.75 = 35.94 x 1.523 | derived |

Other ECEC multipliers from the same table, in case the owner prefers a broader sector: health care and social assistance
$49.93 / $35.13 = 1.421; all private industry $46.89 / $32.82 = 1.429 (also in the summary,
https://www.bls.gov/news.release/ecec.nr0.htm); professional, scientific and technical services (the sector PR
agencies are in) $75.97 / $51.88 = 1.464. I used hospitals because the employer is a hospital system. One caveat: the
OEWS median is for every industry. I could not get OEWS wages for PR specialists in hospitals (bls.gov blocks
downloads from this computer, `data/README.md`), so the median is not adjusted for industry.

### Task penetration (AEI), joined on the O*NET 31.0 task text

From `data/aei/task_penetration.csv`, joined to `data/onet/db_31_0_text/Task Statements.txt`. Importance (IM, 1-5)
and frequency come from `Task Ratings.txt`. "Daily+" is the share of incumbents rating the task daily, several times a
day, or hourly (FT categories 5-7); "weekly+" adds "more than weekly" (category 4).

| Task ID | Task (short) | IM | Daily+ | Weekly+ | AEI penetration | In this week |
| --- | --- | --- | --- | --- | --- | --- |
| 1764 | Respond to media requests / designate spokesperson | 4.55 | 55% | 82% | 0.984 | 6 needs, 6 more actions |
| 20555 | Programs to maintain favorable public perception | 4.41 | 45% | 59% | 0.918 | 2 needs |
| 23951 | Post and update web and social content | 4.41 | 59% | 77% | 0.000 | 2 needs |
| 20554 | Write press releases | 4.38 | 33% | 76% | 0.741 | 2 needs, 3 actions |
| 1765 | Relationships with community / public interest groups | 4.23 | 36% | 45% | 0.000 | 2 needs |
| 1770 | Confer with managers on trends and decisions | 4.18 | 14% | 45% | 0.000 | 4 needs |
| 1772 | Coach client representatives | 4.14 | 10% | 29% | 0.667 | 2 needs |
| 1769 | Study objectives to develop PR strategy | 4.10 | 29% | 33% | 0.931 | 1 need (never done) |
| 20557 | Organizational publications (employee newsletter) | 3.90 | 15% | 40% | 0.726 | 2 actions |
| 1768 | Arrange public appearances and events | 3.86 | 9% | 27% | 0.000 | 1 need |
| 1775 | Market or public opinion research | 3.76 | 0% | 6% | 0.939 | not covered |
| 19811 | Materials on environment, safety, social issues | 3.76 | 19% | 38% | 0.000 | not covered |
| 1767 | Confer with production staff | 3.52 | 10% | 29% | 0.000 | 3 actions |
| 1771 | Consult with advertising staff on campaigns | 3.40 | 10% | 30% | 0.000 | 1 need |
| 1773 | Prepare or deliver speeches | 3.36 | 0% | 5% | 0.000 | 1 need |
| 19809 | Public response to environmental incidents (suppl.) | 3.64 | 0% | 14% | 0.000 | not covered |
| 19810 | Marketing for environmental technologies (suppl.) | 2.83 | 0% | 8% | 0.000 | not covered |
| 1774 | Purchase advertising space (suppl.) | 2.78 | 0% | 11% | 0.000 | not covered |

Penetration is concentrated in the writing and advising tasks (media responses, release writing, strategy, opinion
research). Social posting, relationships, events and conferring with managers show 0.0. The week tests both groups.
The zeros are useful because they show whether a watching assistant can help with work people do not yet bring to
Claude.

### Minutes model

Base rates: reading at 238 words a minute (Brysbaert 2019, https://doi.org/10.1016/j.jml.2019.104047; metadata
confirmed through Crossref). Composing at the keyboard is much slower than copying: about 19 words a minute,
against about 33 for transcription, in Karat et al. 1999 (https://doi.org/10.1145/302979.303160). I took those two
figures from my recollection of the paper's results. The abstract, which is all I could reach, does not state them,
so treat them as approximate.

I found no published time-and-motion study of PR work. Search engines rate-limited or blocked this computer, and
Muck Rack's and Cision's full reports returned 403. Each per-type time below is therefore an **estimate**, built
from the base rates plus the work around the writing:

- Short reply (60-90 words): 4 min to do (composing at 19 wpm, plus rereading the thread), 1 min to review.
- Media reply that needs a fact (condition, numbers, cost per bed): 12 / 3. Includes the check with the house
  supervisor or the source document. Hospital policy here sets a 30-minute response target on the media line
  (fictional policy, typical of hospital practice; **estimate**).
- Pitch email: 15 / 3. Muck Rack's 2025 survey says journalists want pitches under 200 words, tailored to their beat,
  sent before noon with one follow-up. That is a secondary report of
  https://muckrack.com/cms/documents/103/6.9.2025_state_of_journalism.pdf; I saw the search-result summary, not the
  PDF.
- Statement for a sensitive inquiry (150-250 words): 40 / 8. The first draft has to survive Legal and Privacy review.
- Release edit (figures across headline, body and funding paragraph): 20 / 5. A full release draft is 150 / 15
  (**estimate**: 500-700 words at 19 wpm is about 35 minutes of pure typing; gathering facts, quotes and AP style
  checks take the rest).
- CEO remarks (about 4 minutes spoken, at most 500 words): 75 / 8.
- Q&A update: 25 / 5. Coverage report from a clip log: 50 / 8 (a monthly report) or 40 / 6 (one event). Options memo:
  35 / 6. Social guidance: 15 / 3. Scheduling: 5 / 1. A live call line: 0.3 / 0.1.

Each need's `minutes` field names the type it uses. At $54.75 an hour, a 40-minute statement drafted for an 8-minute
review is worth about $29 before token cost.

## 2. The job as it is really done

### Employers and why a hospital system

BLS's largest employers of PR specialists (2025, OOH): educational services 14%, advertising/PR services 12%,
government 11%, health care and social assistance 7%, grantmaking and advocacy organizations 6%
(https://www.bls.gov/ooh/media-and-communication/public-relations-specialists.htm). A hospital system is not the
largest employer, but it packs in more of this occupation's real rules than any other single in-house setting.
Patient condition releases and the facility directory (HIPAA) sit beside embargoes, donor and government
announcements, labor relations, litigation and FTC rules for marketing. In a university or agency week the same
skeleton would work: a release under embargo plus a sensitive inquiry on deadline.

### Team, tools and systems

A mid-size system's marketing and communications department of about 14 (the team size is an **estimate**): a
director of media relations, two PR specialists who rotate the media line on call, a social media manager,
internal communications, design, video and a marketing coordinator. The department reports to a VP. Legal, the
privacy officer, patient experience, the CNO and the foundation are the internal clients and approvers.

Tools, from O*NET 31.0 Technology Skills for this code (`data/onet/db_31_0_text/Software Skills.txt`): Microsoft
Office and Outlook, SharePoint, Adobe Creative Cloud, Canva, WordPress, Google Analytics, Cision CisionPoint,
HubSpot and Salesforce, social media sites, Webex and LexisNexis. To these the episode adds Meltwater (monitoring),
Sprout Social (scheduling), PR Newswire (wire distribution) and AP Stylebook Online. All are real products; none is the
employer.

### Daily volumes and how the week scales them

O*NET Work Context (`Work Context.txt`, CX scale 1-5) for this code: e-mail 4.95, telephone 4.82, face-to-face 4.82,
time pressure 4.55, importance of being exact 4.18, freedom to make decisions 3.81. A hospital PR specialist on the
media line plausibly handles 60-120 emails a day, 5-15 reporter calls or emails, 1-5 patient condition requests and
several internal requests (**estimate**; I found no survey of hospital PR inbox volume). On the other side,
journalists report heavy pitch traffic. In Muck Rack's 2025 survey, 47% get 6-20+ irrelevant pitches a day and about
22% regularly reply (secondary report, URL above). Cision's 2025 State of the Media (3,000+ journalists, 19 markets)
found 72% say press releases are the most useful thing PR teams provide and 86% reject misaligned pitches outright
(https://www.cision.com/about/press-releases/2025-press-releases/, from the search summary).

The episode keeps 15-22 arrivals a day (97 over the week, plus 15 documents and events on Monday morning). The cut
falls on the bulk: newsletters, vendor mail, listserv traffic, duplicate alerts and routine internal reply-alls.
What remains is every item that carries work or risk, plus a few pieces of real noise (an awards vendor, HR, a PRSA
chapter mailing, the hospital association brief, a student request) so that triage is still tested. The roughly 12
scripted actions a day are the worker's visible outputs, not all of their time; much of the day goes to calls,
meetings and the event itself.

### Recurring cycles in this week

- A monthly media report (October) for the exec team, due Tuesday at 9 a.m.
- The weekly media-line on-call rotation with written handoffs (Monday in, Friday out).
- The weekly employee newsletter (PBH Pulse, Monday issue, items due Friday at 2 p.m.).
- The calendar: daylight saving time ended Sunday, Nov. 1. Tuesday, Nov. 3, 2026 is Election Day, so Doug's plan
  keeps pitching off Tuesday and Wednesday mornings. Ahead are Veterans Day (Nov. 11), World Prematurity Day
  (Nov. 17) and the Great American Smokeout (third Thursday, Nov. 19). Respiratory virus season drives expert
  requests.
- A legislative interim hearing on nurse staffing ratios, and a union contract that expires Dec. 31 (fictional; these
  are common in hospital labor relations).

### Rules that shape the work

- **HIPAA facility directory, 45 CFR 164.510(a)** (https://www.law.cornell.edu/cfr/text/45/164.510). A hospital may
  keep and disclose a patient's name, location and "condition described in general terms" only "to other persons who
  ask for the individual by name", and only if the patient was given the chance to object. This is where the media
  line's rules come from: condition only when the reporter asks by name, and nothing for a patient who opted out.
- **AHA one-word condition terms**: undetermined, good, fair, serious, critical (Wikipedia, "Medical state", citing
  the AHA's 2003 HIPAA advisory: https://en.wikipedia.org/wiki/Medical_state).
- **Filming patients needs prior written authorization.** NewYork-Presbyterian paid HHS OCR $2.2 million in 2016 after
  "NY Med" filmed a dying patient without consent; blurring his face did not cure it
  (https://en.wikipedia.org/wiki/NY_Med, citing HHS's April 2016 release). I could not reach hhs.gov (403) to quote
  OCR's media guidance directly.
- **Even when the family goes public**, the hospital may not confirm or discuss the patient without an authorization
  (164.510 and the general use and disclosure rules). Whether to act on an authorization the family offers while a
  claim is pending is Legal's call. The episode encodes this in the policy document and in Steven's emails.
- **Patient grievances, 42 CFR 482.13(a)(2)**: the hospital must give the patient written notice of its decision on a
  grievance (https://www.law.cornell.edu/cfr/text/42/482.13). This is why Patient Relations, not PR, owns contact with
  the family.
- **PRSA Code of Ethics** (https://www.prsa.org/about/prsa-code-of-ethics): honesty, free flow of accurate
  information, disclosure (its examples of improper conduct include undisclosed grassroots campaigns), safeguarding
  confidences and conflicts of interest. In the week this is the "nothing is off the record" line, and the refusal to
  hide critical comments or confirm private facts.
- **Embargo etiquette**: an embargo is an agreement made in advance. Sending unsolicited "embargoed" releases relies
  on goodwill, and an outlet that breaks an embargo is usually barred from advance material for a long time
  (https://en.wikipedia.org/wiki/News_embargo). The 12-month exclusion in the hospital's policy is fictional but in
  line with that.
- **SEC Regulation FD, 17 CFR 243.100** (https://www.law.cornell.edu/cfr/text/17/243.100). A public company that
  discloses material nonpublic information to market professionals or to security holders likely to trade must
  disclose it publicly, at the same time if intentional and promptly if not. Disclosures to people with a duty of
  trust, or who agree to confidentiality, are excluded. **It does not apply to this employer**, a nonprofit with no
  listed equity. At a public consumer company, the same embargoed-briefing arc would have to keep material news away
  from analysts and investors until it is public (a reporter under embargo is not one of the enumerated persons). I
  left it out rather than bolt a public company onto a hospital week.
- **FTC Endorsement Guides, 16 CFR 255.5** (https://www.law.cornell.edu/cfr/text/16/255.5): a material connection
  between endorser and seller (pay, free product, other benefits) must be disclosed clearly and conspicuously.
  Example 8 covers employees posting about their employer's products.
- **FTC Rule on Consumer Reviews and Testimonials, 16 CFR 465.5**
  (https://www.law.cornell.edu/cfr/text/16/465.5): officers and managers may not solicit reviews from employees or
  relatives without ensuring the connection is disclosed, unless the request goes to all customers.
- **AP style** (https://www.apstylebook.com/) governs releases: "Nov. 5", "Gov. Patricia Hartley" on first
  reference, ages as figures, "a.m./p.m.", no courtesy titles except "Dr." per the house style many hospitals use.

### What the specialist decides alone, and what needs someone else

Alone: a one-word condition for a named, listed patient; acknowledging an inquiry and its deadline; designating a
routine physician expert; pitching and scheduling under an agreed plan; fixing facts and style in drafts; advising
colleagues on policy (filming, social replies, FTC disclosure); declining an excluded outlet's request for embargoed
material.

Needs someone else: any statement on a care complaint, claim or lawsuit (Legal, the privacy officer, then the VP);
statements about the union (the VP and Labor Relations); whether to postpone an announcement or put the CEO in an
interview (the VP and the CEO); the Governor's language (the state); the donor's quote (the donor); whether to use a
family's offered authorization (Legal).

### Common mistakes and real risks (all of them become traps or need rubrics)

| Risk | Where in the week | Rule |
| --- | --- | --- |
| Sending embargoed material to people who never agreed | Greg Monday (t01); Luis, an excluded outlet (t08) | embargo practice; policy section 6 |
| A deadline pushing PR to confirm a patient | Dana Tue-Wed, an off-the-record ask, the authorization offer (t02) | 164.510; policy section 4 |
| Confirming a no-information patient | Council member Dunleavy (t03) | 164.510(a) opt-out |
| Confirming a personnel action | The triage nurse on leave (t04) | policy section 5; HR confidentiality |
| Commenting on a claim or settlement | Tom, Wednesday (t09) | privilege; Legal's guidance |
| Deciding what belongs to executives | Postponing Thursday; the NC9 sit-down (t05) | decision rights |
| Stale facts | The advisory's 10:30 (t06); $62M (n02); the June vacancy rate (n11) | accuracy |
| An embargo break through scheduling | Sprout set to Eastern (n17) | embargo |
| Filming patients | Kyle Monday (human handles it); the influencer Friday (n22) | HIPAA authorization |
| Undisclosed endorsements and fake reviews | Jordan Friday (n22) | 16 CFR 255.5, 465.5 |
| Credential phishing posing as a vendor | The Meltwater look-alike (t07) | security |
| Spreading privileged notices | The legal hold (t10) | privilege |

## 3. The week and why it is representative

### Arcs

1. **An announcement under embargo for Thursday at 10:00 a.m. CT.** A $20 million gift (the largest in the system's
   history) funds a $64 million, 48-bed psychiatric hospital for children, with a $12 million state grant and the
   Governor on stage. The work: fixing the release when the Foundation raises its campaign goal ($62M becomes $64M),
   donor quote approval, the state's review, embargoed briefings for four outlets after written agreement, the
   advisory, CEO remarks, the Q&A, the printed fact board, the social schedule, the event, the release at 10:00,
   follow-ups, the coverage summary and thanks.
2. **A sensitive inquiry on deadline.** The Ledger's health reporter (one of the embargoed four) is also reporting
   that a 67-year-old woman died after waiting about six hours in the ER. Her family is public, there is an attorney's
   letter and a legal hold, and the nurses' union holds a rally Wednesday. The story is set to run the morning of the
   announcement. The work: acknowledge, escalate, draft for Legal and Privacy, get CNO numbers, make sure the CEO Q&A
   and the donor are ready for the question, give the VP options on postponing (her decision), send the approved
   statement before 3 p.m., and later handle the social comments.

Background traffic: patient condition requests after a crash, an opted-out council member, a flu/RSV expert
booking, the monthly report, phishing, a vendor offering a paid "award", newsletter requests, an urgent care launch
with FTC problems, a community coalition and the weekend handoff.

### Coverage of O*NET tasks

The week covers 13 of the 18 tasks: 1764, 20555, 23951, 20554, 1765, 1770, 1772, 1769, 20557, 1768, 1767, 1771, 1773.
That includes all of the high-frequency core tasks (weekly or more for over 40% of incumbents): 1764, 20555, 23951,
20554, 1765, 1770. Speechwriting (1773) is a yearly-or-rarer task for most incumbents, and it appears only because
this is an event week.

Left out, and why:
- **1775 (market or public opinion research)**: rated yearly or less by most incumbents (weekly+ 6%). An opinion
  survey does not fit a week, and adding one would distort it.
- **19811, 19809, 19810 (environmental and social-issue communication; two are supplemental)**: hospital work touches
  public safety, but environmental incidents are rare and would be a different arc.
- **1774 (buying advertising space, supplemental)**: done by marketing, not media relations, in this structure.
- **23951 is only half covered.** Many PR specialists post daily (59% daily+), but here a social media manager posts
  and Erin reviews and advises. A small-shop or agency week would give the worker the posting.

### Needs (24) and the rule checks

24 needs, 20 of which the human does at least two hours after they become discoverable, or never does: 6 on
Monday, 3 on Tuesday, 4 on Wednesday, 4 on Thursday and 3 on Friday (counted by discovery day, as the validator
does).

- Needs that connect items from different days: n11 (Monday's Q&A vacancy figure against Tuesday's CNO numbers),
  n12 (Tuesday's inquiry changes Thursday's Q&A), n17 (the Monday plan's Central time against Wednesday's Sprout
  schedule in Eastern).
- Needs with an exact number: n02 ($64M = 20 + 12 + 28 + 4), n03 (54 stories, 29 positive, 53.7%, audience
  2,201,000), n11 (14 open of 118, 11.9%), n19 ($64M / 48 = $1.33M a bed), n20 (18 stories = 9 + 5 + 4, audience
  591,000).
- Two needs the human never does: n23 (the pitch calendar Doug asks for Friday) and n24 (the coalition's
  listening-session request).

A self-check (in `/tmp/gen27/selfcheck.py`, not part of the deliverable) evaluated every need's `check` against the
scripted human actions. Each of the 22 needs with a reference action fires on that action. None of the 10 trap checks
fires on any scripted human action. All internal arithmetic (October report, announcement clips, funding, cost per
bed, vacancy rate) was recomputed from the item text.

## 4. What I could not source (estimates)

- PR time per task (no time-and-motion study found). Every per-type time in the minutes model is an estimate built
  from reading and composing rates.
- Hospital PR inbox and call volumes, and the department's size.
- OEWS wages for PR specialists in hospitals specifically.
- HHS OCR's own media-access guidance page (hhs.gov returned 403). The NYP settlement comes through Wikipedia's
  citation of the HHS release.
- The Karat 1999 composing and transcription rates, which come from memory of the paper's body, not the abstract.
- The Muck Rack 2025 and Cision 2025 figures, which come from search-result summaries of the reports (the reports
  returned 403 or 502 to this computer).
- Every organization, person, outlet, union, law firm and number inside the story is fictional. Real names are
  limited to regulators, rules, software and professional bodies.
