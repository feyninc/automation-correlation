# 43-4051.00 Customer Service Representatives: research for the episode (draft, 2026-10-26)

Week drafted: Monday 2026-11-02 to Friday 2026-11-06. Worker: Marisol Ortega, Customer Care Representative II (Tier 1,
blended phone and digital) at Northbeam Fiber, a fictional regional fiber internet and Home Phone (interconnected VoIP)
provider in the Willamette Valley, southwest Washington and Siskiyou County, California. Pacific time; daylight saving
time ends Sunday 2026-11-01, so every time in the week is PST.

Sources fetched on 2026-10-26 unless noted. Local files are relative to the project root.

## 1. Economics

| Quantity | Value | Source |
| --- | --- | --- |
| Median hourly wage | $21.53 (2025); annual $44,770 | `data/wages-onetonline-2026-10-26.csv` (BLS OEWS May 2025 via O*NET OnLine); same figures in `data/onetonline/summary-43-4051.00.html` and the [BLS OOH page](https://www.bls.gov/ooh/office-and-administrative-support/customer-service-representatives.htm) |
| Employment | 2,666,000 (2025) | `data/wages-onetonline-2026-10-26.csv` |
| Projection 2025-2035 | Decline (-1% or lower); 289,500 openings. BLS OOH: -5%, -141,800 jobs, because "self-service systems, social media, and mobile applications enable customers to do simple tasks" | `data/wages-onetonline-2026-10-26.csv`; [BLS OOH](https://www.bls.gov/ooh/office-and-administrative-support/customer-service-representatives.htm) |
| Observed exposure (AEI) | 0.7011 | `data/aei/job_exposure.csv`, row 43-4051 |
| Loaded-cost multiplier | 1.456 = $36.73 / $25.22 | [BLS ECEC June 2026, Table 4](https://www.bls.gov/news.release/ecec.t04.htm) (released 2026-09-09): private industry, office and administrative support occupations, total compensation $36.73/h, wages and salaries $25.22/h (68.7%). For comparison, all private-industry workers: $46.89 / $32.82 = 1.429 ([summary](https://www.bls.gov/news.release/ecec.nr0.htm)). |
| Loaded hourly cost | $31.36 = $21.53 x 1.456 | computed |

Why office and administrative support rather than all private industry: SOC 43-4051 sits in the office and
administrative support major group (43-0000), and that group's benefit share (31.3%) is what an employer of CSRs pays.

### Task penetration (AEI), joined on task text

From `data/aei/task_penetration.csv`; every one of the 13 task statements matched exactly.

| Task ID | Task (short) | Penetration |
| --- | --- | --- |
| 18565 | Confer with customers by telephone ... cancel accounts, obtain details of complaints | 0.991 |
| 2578 | Keep records of customer interactions | 0.9951 |
| 2580 | Check that changes were made to resolve problems | 0.0 |
| 2581 | Contact customers to respond to inquiries or notify of results/adjustments | 0.9913 |
| 2583 | Determine charges, collect payments, arrange billing | 0.0 |
| 2584 | Complete contract forms, change of address, discontinuance orders | 0.0 |
| 2582 | Refer unresolved grievances to designated departments | 1.0 |
| 2579 | Resolve complaints: exchange, refund, adjust bills | 0.9872 |
| 2587 | Review insurance policy terms | 0.0 |
| 2586 | Solicit sales of new or additional services | 1.0 |
| 2589 | Compare disputed merchandise with requisitions and invoices | 0.0 |
| 2585 | Obtain and examine information to assess complaint validity and causes | 0.0 |
| 2591 | Recommend improvements to prevent future problems | 0.0 |

The values are close to binary (observed in Claude usage or not). The week deliberately includes needs on the
zero-penetration tasks (2580, 2583, 2584, 2585, 2589, 2591), since the benchmark asks whether an assistant can do them
when watching the worker, not whether people already ask Claude for them.

### Minutes model

Inputs:
- Reading speed 238 words/minute for silent reading of non-fiction (Brysbaert 2019,
  [doi:10.1016/j.jml.2019.104047](https://doi.org/10.1016/j.jml.2019.104047)).
- Typing speed: mean 52 words/minute across 168,000 typists (Dhakal et al. 2018,
  [doi:10.1145/3173574.3174220](https://doi.org/10.1145/3173574.3174220)). Composing a customer reply is slower than
  typing: you look things up and choose words. **Estimate:** about 20 words/minute for a reply, including lookups.
- Contact-center norms ([Call Centre Helper, industry standard metrics](https://www.callcentrehelper.com/industry-standards-metrics-125584.htm),
  modified 2026-01-23): average handling time 6 min 3 s (190,702 entries in their Erlang calculator), maximum occupancy
  83.3%, shrinkage 30%, service level 80% of calls in 20 seconds, email 100% answered within 24 hours, chat 80% within
  20 seconds, QA "random scoring of four advisor calls per month" with scores normally 75-90%, FCR 70-75%.
- AHT is talk + hold + after-call work ([Call Centre Helper, What is AHT](https://www.callcentrehelper.com/what-is-average-handling-time-aht-91340.htm)).

Per proposal type (also in `episode.json` `economics.minutes_model`). All of these are estimates built from the inputs
above; I found no published time study for individual CSR actions.

| Type | Do (min) | Review (min) | Reasoning |
| --- | --- | --- | --- |
| Ticket reply (email/chat) | 5.0 | 1.0 | About 100 words at about 20 wpm, plus an account lookup. Review: reading 100 words at 238 wpm takes 0.4 min, plus checking the facts against the account. |
| Case note (after-call work) | 1.5 | 0.4 | ACW is part of the 6:03 AHT; a 60-word note at 52 wpm plus reason codes. |
| Internal chat | 1.0 | 0.2 | One or two lines. |
| Escalation to Tier 2 / Security | 6.0 | 1.5 | Gathering confirmation numbers, amounts, tracking and dates, and writing about 120 words. |
| Document (letter, order form) | 10.0 | 2.5 | Filling a template from several lookups. |
| Reconcile (call detail, returns log) | 10.0 | 3.0 | Comparing two records line by line. |
| Outbound callback | 4.0 | 0.5 | Dialing, a 2-3 minute conversation and a note. The review covers only the plan or script. |
| Call line (live call) | 0.3 | 0.1 | The rep speaks anyway. A 25-word suggested line takes about 6 s to read at 238 wpm. On calls the value is accuracy (the right policy, the right amount) and the hold time avoided, not typing saved. |
| Calendar | 1.0 | 0.2 | |

Each need's `minutes.do_minutes` in the episode uses these, with the need's own adjustment (for example, the six
remaining callbacks are 6 x 4 = 24 minutes).

Patience windows on calls (`patience_s`) are 3 to 10 seconds. In ordinary conversation the typical gap between turns
is about 0 to 200 ms in every language studied (Stivers et al. 2009, PNAS,
[doi:10.1073/pnas.0903616106](https://doi.org/10.1073/pnas.0903616106)). A rep can buy time with "let me check that",
so I set **estimates** by situation: 3-4 s for angry callers or demands, 5-6 s for routine turns, and 8-10 s where the
caller is doing something (reading a code, power-cycling a box) or is elderly. I found no published measure of how much
silence callers tolerate.

## 2. The job as it is really done

### Employer, team, tools

- Who employs CSRs: retail trade 15%, insurance 12%, business support services (call-center outsourcers) 8%
  ([BLS OOH](https://www.bls.gov/ooh/office-and-administrative-support/customer-service-representatives.htm)). O*NET
  OnLine lists finance and insurance and retail trade as the top industries (`data/onetonline/summary-43-4051.00.html`).
  I chose a telecom/ISP employer instead because it gives the job's full regulatory load in one week: card payments
  (PCI DSS), account authentication with a legal basis (FCC CPNI rules, which apply to interconnected VoIP), recurring
  subscription cancellations (ROSCA, California's automatic renewal law), outbound callbacks (TCPA) and network
  outages that produce contact spikes. It is also the hardest vertical for first-contact resolution: SQM Group puts the
  industry FCR average at 71% and telecom lowest at 56%
  ([SQM Group, FCR benchmark](https://www.sqmgroup.com/resources/library/blog/fcr-metric-operating-philosophy), updated 2026-08-20).
- Training: usually 2 to 4 weeks on the job (BLS OOH). The episode has a 6-week new hire (Omar) who asks the team questions.
- Schedules: mostly full time; evenings, weekends and holidays are common (BLS OOH). The episode has a holiday shift bid.
- Tools (O*NET 31.0 Software Skills for 43-4051.00, `data/onet/db_31_0_text/Software Skills.txt`): Salesforce CRM,
  "customer complaint ticketing management software", "multi-channel contact center software", Microsoft Teams/Slack,
  VoIP softphones, Microsoft Outlook. The episode uses Genesys Cloud CX (ACD and softphone with screen pop, Secure Pay
  IVR transfer and recording pause), a billing/account console (Beam360, fictional), Zendesk (ticket queue with
  Redact), Slack and a Guru knowledge base. These are real product names; the employer and its console are fictional.
- Structure: Tier 1 generalists (phone plus scheduled "digital blocks" for email/chat tickets), Tier 2 Billing and
  Tier 2 Technical escalation groups, a Loyalty (retention) queue, Account Security, NOC, field dispatch, QA, WFM and
  a knowledge manager. This is the standard tiered model. I did not find one public source that describes a
  representative org chart, so the specific team names and response times are my **estimates**.

### Work context (O*NET 31.0, `Work Context.txt`, CX scale 1-5)

Telephone conversations 5.00 (the highest possible); deal with external customers 4.79; e-mail 4.33; time pressure
4.55; importance of being exact 4.53; repeating the same tasks 4.45; dealing with unpleasant or angry people 4.21;
face-to-face 3.61; freedom to make decisions 3.05; consequence of error 2.16. Top work activities by importance:
communicating with supervisors and peers 4.59, working with computers 4.54, communicating with people outside the
organization 4.51, performing for or working directly with the public 4.37.

The week reflects this: 15 live calls carry most of the decision points, with tickets and internal chat around them.
Every customer touch needs an exact number or policy, several callers are angry, and freedom is bounded by authority
limits.

### Daily volumes and how the week scales them

- Calls per day. **Estimate** from the Call Centre Helper standards: an 8-hour shift x (1 - 0.30 shrinkage) = 5.6 h
  available; x 0.833 occupancy = 4.7 h handling; at 6:03 AHT that is about 46 calls. A blended rep who spends two
  hours a day in digital blocks takes about 35. The episode scripts 3 calls a day (15 for the week), about 1 in 12. I
  picked calls that each turn on a rule (verification, a credit formula, PCI, the cancellation script, an add-on
  sale, a payment arrangement) and left out the routine ones.
- Tickets. With email answered within 24 hours and two one-hour digital blocks at about 5 minutes a ticket, a rep
  clears roughly 20-25 tickets a day (**estimate**). The episode has 4 to 8 ticket arrivals a day, plus screen pops,
  internal chat, NOC posts, policy emails and documents. That gives 16 to 20 arrivals a day (validator target 15 to 30)
  and 71 scripted actions (16, 14, 15, 14, 12 a day), about a fifth of a real week's contacts.
- Outage spike. Priya's email says 9,412 calls on Tuesday, three times a normal Tuesday. That number is fictional. I
  found no public statistic for how much contact volume rises during an ISP outage. In the episode the spike shows up
  as cancelled digital blocks, longer hold times in callers' complaints, and an AHT of 7:48 for the week.

### Recurring cycles in the week

- Billing: statements on the 1st, due on the 18th, billed a month in advance. Monday brings "why is my bill higher"
  calls after a 12-month promotion ends. Payment arrangements, late fees 15 days after the due date, and final bills
  with prorated credits come up through the week.
- QA: evaluations of about 4 calls a month, with a dispute window, and a monthly calibration session (Call Centre
  Helper's QA standard). The episode has a disputed QA score and a Wednesday calibration session.
- WFM: overtime sign-ups during the incident, a holiday shift bid that closes Friday at 5 pm, and next week's
  published schedule.
- Knowledge base: a weekly note, and a script version published Tuesday that takes effect Thursday.

### Rules that shape the work (cited)

- **Account verification / CPNI.** Carriers must authenticate a caller before disclosing call detail on a
  customer-initiated call. That means a password "not prompted by the carrier asking for readily available biographical
  information". Without one, call detail can only be sent to the address of record or given by calling the telephone
  number of record. Carriers must also notify customers immediately when a password or address of record changes
  ([47 CFR 64.2010](https://www.law.cornell.edu/cfr/text/47/64.2010)). "Telecommunications carrier" includes
  interconnected VoIP providers. "Readily available biographical information" includes SSN or its last four digits,
  mother's maiden name, home address and date of birth. An address becomes an address of record after 30 days on the
  account ([47 CFR 64.2003](https://www.law.cornell.edu/cfr/text/47/64.2003)). Obtaining confidential phone records by
  false statements to a carrier's employee is a federal crime with up to 10 years' imprisonment
  ([18 U.S.C. 1039](https://www.law.cornell.edu/uscode/text/18/1039)). Northbeam's Verification Standard applies the
  same rule to internet-only accounts. That extension is company policy, not law: since the 2017 repeal of the
  broadband privacy rules, CPNI rules bind broadband-only service only where state law says so. I did not research
  state law further.
- **PCI DSS for card payments.** Sensitive authentication data, such as the card verification code, "must not be
  stored after authorization, even if encrypted". If a recording captures it, it must be deleted. The PAN may be
  displayed only up to the first six and last four digits. Pause-and-resume, DTMF masking and secure IVR transfer are
  the recognised ways to keep card data out of recordings, and agent-initiated pause-and-resume needs regular checks
  ([PCI SSC Information Supplement, Protecting Telephone-Based Payment Card Data v3.0, Nov 2018](https://www.pcisecuritystandards.org/documents/Protecting_Telephone_Based_Payment_Card_Data_v3-0_nov_2018.pdf),
  pp. on SAD storage and section 6.5.1). The episode's card-data policy, a caller who starts reading digits aloud, and
  a chat customer who pastes the card, expiry and CVV all come from this.
- **Cancellations.**
  - Federal: ROSCA requires "simple mechanisms for a consumer to stop recurring charges"
    ([15 U.S.C. 8403](https://www.law.cornell.edu/uscode/text/15/8403)).
  - The FTC's 2024 "click-to-cancel" amendments are no longer in force. In light of court decisions, the FTC
    recodified the Negative Option Rule as it stood before the 2024 rule, effective 2026-02-12
    ([FR doc. 2026-02866](https://www.federalregister.gov/documents/2026/02/12/2026-02866/revision-of-the-negative-option-rule-withdrawal-of-the-cars-rule-removal-of-the-non-compete-rule-to)).
    It then opened a new advance notice of proposed rulemaking on 2026-03-13, with comments due 2026-04-13
    ([2026-04952](https://www.federalregister.gov/documents/2026/03/13/2026-04952/rule-concerning-the-use-of-prenotification-negative-option-plans)).
  - California's automatic renewal law ([Cal. Bus. & Prof. Code 17602, via FindLaw](https://codes.findlaw.com/ca/business-and-professions-code/bpc-sect-17602/))
    has four provisions that matter here:
    - cancellation must be possible in the medium the consumer used;
    - a voicemail cancellation request must be processed or called back "within one business day" (subdivision (c));
    - by telephone, a business may present a retention offer only "provided that the business first clearly and
      conspicuously informs the consumer that they may complete the cancellation process at any time by stating that
      they want to 'cancel'" (subdivision (e));
    - price changes need 7 to 30 days' notice (subdivision (g)).
  - The episode's mid-week policy change (v7, every state from Thursday) applies these rules company-wide. That is a
    plausible compliance decision for a provider that already has California customers.
  - I could not open the official leginfo.legislature.ca.gov text from this computer (HTTP 403), so the quotes come
    from FindLaw's copy.
- **TCPA, for outbound calls.**
  - A telemarketing call using an artificial or prerecorded voice needs the called party's prior express written
    consent: paragraph (a)(2) for wireless numbers, (a)(3) for residential lines. An established business relationship
    does not exempt prerecorded telemarketing to residential lines.
  - Telephone solicitations are barred before 8 a.m. and after 9 p.m. local time ((c)(1)).
  - Consent may be revoked "by using any reasonable method" and must be honored "within a reasonable time not to exceed
    ten business days" ((a)(10)).
  - Telemarketers must keep company-specific do-not-call lists ((d)).
  - All from [47 CFR 64.1200](https://www.law.cornell.edu/cfr/text/47/64.1200).
  - The Thursday sales-manager push (call outage callback lists until 9:30 pm, and load non-answers into a prerecorded
    upgrade campaign) breaks several of these at once. The callback list's internal do-not-call flag comes from (d).
- **One-ring (wangiri) scam.** Autodialers leave one-ring missed calls hoping the victim calls back. One variant uses
  Caribbean numbers such as 1-473 (Grenada) "which look like North American domestic calls"
  ([Wikipedia, Phone fraud](https://en.wikipedia.org/wiki/Phone_fraud), citing KSL 2014). The FCC's consumer page on
  the scam returned HTTP 403 from this computer, so I could not cite it directly. The Thursday usage dispute is built
  on this pattern, and the Grenada rate ($0.58/min) is fictional.

### What a Tier 1 rep decides alone, and what needs someone else

Decides alone (episode authority matrix, items 1-4 and 8):
- goodwill credits up to $40 per account per 30 days;
- outage credits by formula;
- one late-fee waiver a year;
- a one-time usage courtesy credit up to $40;
- payment arrangements up to $250 in two installments within 30 days;
- add-on sales, moves, cancellations and downgrades;
- what to say on the call.

Needs someone else:
- refunds of payments and equipment-fee reversals (Tier 2 Billing);
- promotions and retention offers outside the Offer Library (Loyalty);
- technical problems outside a known incident (Tier 2 Technical or dispatch);
- suspected pretexting (Account Security);
- incident credit policy (Billing Operations);
- anything legal or compliance-related (Compliance).

The dollar limits are my **estimates**. Companies keep these limits internal, and I found no published survey of CSR
credit authority, only the general practice of tiered approval limits. They were chosen so that the week's amounts land
on both sides of the line: $34.80 is within Tier 1 authority, while $80.00 and $150.00 are not.

### Common mistakes and risks (the traps and needs come from these)

- Giving account information to someone who has not been verified, or verifying with biographical data (CPNI).
- Repeating or recording card data (PCI DSS).
- Promising credits, refunds or fee removals beyond the rep's authority, especially under pressure or threats ("I'm
  filing with the Attorney General").
- Using a stale policy or a stale ETR after the incident notice changed.
- Using the outage macro for a customer who is not in the outage area (a different fault).
- Losing track of follow-ups: callbacks, "I'll let you know when Billing confirms", pending tickets.
- Being hooked by phishing during an incident.
- Acting on a misaddressed internal email that contains customer data.
- Sales pressure that runs into the TCPA.
- Telling customers whose 911 depends on a VoIP line during an outage about it too late.

## 3. Why this week is representative

- One or two arcs a real rep could meet in a single week:
  - A **service incident on Tuesday**: a contractor cuts fiber in north Keizer, about 4,800 customers are out, the ETR
    is revised twice, part of the area takes longer to restore, some damage follows on afterwards, and customers ask for
    callbacks.
  - A **policy change on Wednesday** that the incident causes: Billing makes outage credits automatic, forbids manual
    credits from 10:00, and handles errors with a correction form. Friday's batch then shortchanges a customer in the
    slower-restored segment.
  - A second, **regulatory policy change**: the cancellation script v7, published Tuesday and live Thursday.
  - Around these runs ordinary background: promotion roll-off calls after the 1st's statements, a duplicate-payment
    refund, a move order, an equipment-fee dispute, an add-on sale, a payment arrangement, the QA dispute, the holiday
    bid and peer questions.
- The human does most of the work (71 actions, 15 calls) and makes realistic mistakes under load:
  - sends the outage macro to a Monmouth customer;
  - never makes the Monday follow-up call;
  - calls back only one of seven customers on the callback list;
  - does not check the returns log and asks the customer for evidence instead;
  - forgets to tell a customer his refund was approved until he chases it;
  - answers the takeover email safely but never refers it to Account Security;
  - never works the voicemail cancellation;
  - never sends the outage feedback.
  These gaps are the needs that wait until later or are never done (2 or more each day, as the validator counts them).
- Needs that only show up by connecting items from different days:
  - n12: Tuesday's ticket, plus Wednesday's NOC post, plus Wednesday's billing rule, gives the $7.00 credit.
  - n04: Monday's dispute, plus the Monday-morning returns sheet, plus Thursday's question from Tier 2, shows the serial
    was transposed.
  - n17: Wednesday's pretext call, plus Thursday's email from the same mobile number.
  - n22: Wednesday's rule applied to Friday's batch error.
- Hard numbers that are checked exactly:
  - n12: $7.00 = 2 x $105.00 / 30;
  - n20: $34.80 = 60 min x $0.58;
  - n22: $2.50 = $5.00 - $2.50;
  - plus call lines with $72.49 and $77.49, and the final-bill prorations $25.00, $41.67, $16.00 in human lines.

### O*NET tasks covered (ids, frequency = share rating daily or more often, importance 1-5)

From `Task Statements.txt` and `Task Ratings.txt` (FT categories 5-7 = daily, several times daily, hourly or more).

| Task | Daily+ | Imp. | Needs |
| --- | --- | --- | --- |
| 18565 Confer by telephone ... cancel accounts, complaints | 86.1% (hourly+ 55.2%) | 4.67 | n08, n18, n21; all 15 calls |
| 2578 Keep records of interactions | 77.6% | 4.53 | the human's after-call case note on every call; n19 draws on the records |
| 2580 Check changes resolved the problem | 73.5% | 4.39 | n02, n13 |
| 2581 Contact customers re inquiries, results, adjustments | 56.4% | 4.22 | n10, n11, n12, n14, n23, n24 |
| 2583 Determine charges, collect payments, arrange billing | 71.9% | 4.18 | n07, n16, n25 |
| 2584 Contract forms, change of address, discontinuance orders | 74.7% | 4.10 | n05 (and three disconnects done by the human) |
| 2582 Refer unresolved grievances to departments | 38.4% | 4.07 | n03, n09, n15, n17 |
| 2579 Resolve complaints: refund, adjust bills | 66.9% | 4.19 | n01, n22 |
| 2586 Solicit sales of additional services | 77.1% | 3.87 | n06 |
| 2589 Compare disputed merchandise with records | 41.9% | 3.64 | n04 |
| 2585 Examine information to assess complaint validity and cause | 52.4% | 3.63 | n20 |
| 2591 Recommend improvements | 28.1% | 3.16 | n19 |

Left out: **2587** "Review insurance policy terms to determine whether a particular loss is covered by insurance"
(daily+ 51.1%, importance 4.05, but only 14 respondents). It belongs to CSRs at insurance carriers and cannot happen at
an internet provider. A sibling episode with an insurance employer would cover it. Among the high-frequency tasks, 2578
(record keeping) has no planted need of its own: the scripted human writes every case note, so an assistant's notes
would only duplicate references. Sales (2586, daily+ 77.1%) is under-sampled, with one planted need. At a retention-
or sales-heavy employer it would be a larger share of calls.

## 4. What I could not source (estimates in the episode)

- Tier 1 dollar authority ($40 discretionary, $40 usage courtesy, $250 payment arrangements, Tier 2 refunds up to $150)
  and the outage-credit formula (1/30 of monthly service per started 24 hours, 4-hour minimum). These are plausible
  company policy. I found no public survey or regulation that sets them for broadband.
- Per-action do and review minutes (section 1). No time-and-motion study for CSR actions was found; the figures are
  built from reading and typing speeds and the AHT standard.
- Callers' tolerance for silence (patience windows).
- Ticket throughput per digital hour, the multiplier for contacts during an outage, and the 5-7 business days for a card
  refund to appear (a common merchant statement, not sourced).
- The FCC one-ring scam page and the official California leginfo text could not be fetched (HTTP 403); I used
  Wikipedia and FindLaw's copy instead.
- Whether CPNI rules reach broadband-only accounts under any state law (not researched; the episode treats the
  extension as company policy).

All people, the employer, account numbers, addresses (fictional house numbers on real Salem/Keizer street names),
phone numbers (555-01xx), tracking numbers and card numbers are invented. The pasted card number is Luhn-valid so that
it looks real, but it is not issued.
