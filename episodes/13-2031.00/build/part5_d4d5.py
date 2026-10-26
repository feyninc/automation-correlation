from part4_d3 import *

doc("d_proviso", "D0", "FY27 proviso tracking - Program 040 landlord mitigation (through September).xlsx", f"""
Proviso: 2026 supplemental operating budget Sec. 131(4), $1,800,000 FY27 GF-S provided solely for the landlord mitigation program. Unspent amounts lapse June 30, 2027.

Month | Claims paid | Allotment
""" + "\n".join(f"{mo} | {m(a)} | $150,000.00" for mo, a in PROVISO_MONTHS) + f"""
Q1 | {m(PROVISO_Q1)} | {m(PROVISO_Q1_ALLOT)}
FY27 proviso amount | | {m(PROVISO, False)}

Claims are landlord reimbursements for unpaid rent or damage under the program's rules; volume has run below plan since FY26 (FY26 lapse $241,880).
""", kind="sheet", meta={"format": "xlsx"})

Q1_FINAL_TABLE, _ = q1_table(adjusted=True)

OPTIONS_DOC = f"""
HSRA FY27 spending options - for discussion, Thu 11/5 10:00 (preliminary: Accounting's September sign-off is due today at noon)

The problem
- Q1 020 GF-S spending was {m(PRELIM_ADJ)} against a {m(ROWS[2][4], False)} allotment, counting Accounting's {m(ACCRUAL, False)} of September invoices.
- At the Q1 pace FY27 GF-S would be about {m(PRELIM_PROJ, False)} against a {m(ROWS[2][3], False)} appropriation, a gap of about {m(PRELIM_GAP, False)}. M1 asked OFM for {m(DP_M1, False)}.
- Drivers (grantee data): {Q1_HH_MO.quantize(D('1')):,} households a month against {int(FY26_HH_MO):,} in FY26 (+{r2(HH_GROWTH)}%), and {m(Q1_AVG)} average assistance against {m(FY26_AVG)} (+{r2(AVG_GROWTH)}%). Pierce and Spokane account for most of the household growth (intake sheet).
- We cannot spend past the appropriation (RCW 43.88.130). A supplemental would not be enacted before March at the earliest.

Options (savings for the nine months October-June; GF-S is {r2(GFS_SHARE * 100)}% of 020 spending)
A. Cap new intake at the FY26 average of {int(FY26_HH_MO):,} households a month from December, allocated to grantees by their FY26 share. Saves about {m(OPT_A_ALL, False)} all funds / {m(OPT_A_GFS, False)} GF-S if applied for nine months; about {OPT_A_HH.quantize(D('1')):,} fewer households over nine months. Prorate if it starts in December.
B. Cap average assistance per household at the FY26 level ({m(FY26_AVG)}) by limiting months of arrears paid. Saves about {m(OPT_B_ALL, False)} all funds / {m(OPT_B_GFS, False)} GF-S; same households served, less paid per household.
A and B together: about {m(OPT_AB_ALL, False)} all funds / {m(OPT_AB_GFS, False)} GF-S (not the sum of A and B, because the two overlap).
C. Reallot part of 040's non-proviso GF-S ({m(P040_NONPROVISO_ANNUAL, False)} for FY27, mostly committed to navigation contracts) in the Q7 amendment. Small, and Teresa's and OFM's decision. The {m(PROVISO, False)} landlord mitigation proviso cannot be used.
D. Ask OFM about Governor's budget treatment of M1. That is a decision for the Director, not a spending fix.

What each means against the gap
- If M1 is funded in full: the remaining gap is about {m(PRELIM_GAP - DP_M1, False)}, which A or B alone covers.
- If M1 is not funded: the gap is about {m(PRELIM_GAP, False)}, more than A and B together save; grantee contracts would also have to be cut for the rest of the year, as M1's narrative warned.

Decision needed from Teresa / the Director: which option, starting when, and how we tell grantees (30 days' notice under the grant agreements).
"""

Q1_REPORT = f"""
OHS Quarterly Budget Status Report - FY27 Q1 (July-September 2026)
To: Monica Ferrante, Director | From: Budget Office (L. Whitaker, T. Lindqvist) | For: Executive Leadership Team, 11/9/2026

1. Bottom line
HSRA (Program 020) is on track to overspend its FY27 GF-S appropriation. Q1 020 GF-S spending was {m(P020_GFS_ADJ)}, {m(-P020_GFS_VAR)} over its {m(ROWS[2][4], False)} allotment. At the Q1 pace FY27 020 GF-S spending would reach {m(P020_PROJ)} against {m(ROWS[2][3], False)}, a {m(P020_GAP)} gap, {m(GAP_BEYOND_DP)} more than the {m(DP_M1, False)} requested in M1. We cannot spend past the appropriation (RCW 43.88.130), so a management decision is needed this month. 020 HSA-S is slightly over ({m(ROWS[3][4] - ROWS[3][5])}); every other program and fund is within its allotment.

2. By program and fund, Q1 (after Accounting's reconciliation, signed off 11/5)
{Q1_FINAL_TABLE}
GF-S overall: {m(GFS_Q1_ADJ)} against {m(GFS_Q1_ALLOT, False)} allotted ({m(GFS_Q1_VAR)}).

3. Reconciling items against the 10/12 ER report
- +{m(ACCRUAL)} 020 GF-S: three September grantee invoices keyed in FM16 (accrual JV, September service dates).
- -{m(MISCODE)} 020 GF-S / +{m(MISCODE)} 030 GF-S: a shelter grant payment miscoded to 020 (corrected in FM16).
Accounting (D. Kalama) signed off the September reconciliation 11/5.

4. Issues
- HSRA demand: {Q1_HH_MO.quantize(D('1')):,} households a month (+{r2(HH_GROWTH)}% over FY26) and {m(Q1_AVG)} average assistance (+{r2(AVG_GROWTH)}%). Options (intake cap, assistance cap) were reviewed 11/5 and are with the Director for decision; either one closes the gap beyond M1 if M1 is funded. If M1 is not funded, both together (about {m(OPT_AB_GFS, False)} GF-S over nine months, less from a later start) still fall short of the gap, and grantee contracts would have to be reduced for the rest of the year.
- Landlord mitigation proviso (040): {m(PROVISO_Q1)} of claims in Q1; at that pace {m(PROVISO_PROJ)} for the year and a projected lapse of {m(PROVISO_LAPSE)}. The money is "solely for" this program and cannot be moved to HSRA.
- Administration (010): {m(P010_Q1_UNDER)} under in Q1 from vacancies. {FTE_FILLED_NOV1} of {FTE_BUDGET} FTE filled as of 11/1 (4.0 held vacant for reduction option R3).
- ESG (030 GF-F): Q1 draws {m(ROWS[5][4] - ROWS[5][5])} under allotment from reimbursement timing.

5. What OFM has been told
Responses to OFM's M1 questions (due to OFM 11/6 at noon) give the updated projection; M1 itself was not changed in ABS.
"""

# =============================================================== DAY 4 (Thu 11/5) items
chat("chat_teresa4", "D4 08:15", "c_teresa", ["c_lauren"], "FN: add one sentence on why the AAG cost is FY28 only, otherwise fine to release. send Jordan the draft for Alicia.", "t_teresa_chat")

email("e_hoang_lunch", "D4 08:40", "c_hoang", ["c_lauren", "c_kevin"], "RE: Coding for the 11/19 provider training and appreciation day", f"""
Agree with Lauren. Kevin, send me the agenda. If the day is mainly the HMIS and ESG training, the venue, lunch and AV ({m(LUNCH_MAYBE)}) can go to ESG admin as conference costs. The reception and gift cards ({m(LUNCH_NO)}) can't be charged to ESG at all, and talk to Denise before assuming state funds can cover them. Don't sign the venue contract until I've coded it.

Hoang

{SIG['c_hoang']}
""", "t_luncheon")

email("e_kevin_lunch2", "D4 09:10", "c_kevin", ["c_lauren", "c_hoang"], "RE: Coding for the 11/19 provider training and appreciation day", """
Understood - dropping the reception and the gift cards. Agenda to Hoang this morning. Thanks for catching it before I signed.

Kevin
""", "t_luncheon")

email("e_jenna_pc", "D4 09:20", "c_jenna", ["c_lauren", "c_marcus"], "Position control update - 11/1 starts", f"""
Hi Lauren and Marcus,

Both Fiscal Analyst 3 hires in Program 010 are effective 11/1 in HRMS (first day was Monday). That brings filled FTE to {FTE_FILLED_NOV1} of {FTE_BUDGET}, so {FTE_VACANT_NOV1} vacant as of 11/1. The 10/31 extract you have still shows them vacant. No other changes this pay period.

Jenna

{SIG['c_jenna']}
""", "t_positions")

email("e_jordan_draft_ack", "D4 09:25", "c_jordan", ["c_lauren"], "RE: H-0287.1 - OFM analyst", """
Got the DRAFT, thanks - passed it to Alicia marked as a draft. Release it in FNS when you're ready.

Jordan
""", "t_fn")

email("e_alicia_ask", "D4 09:45", "c_alicia", ["c_lauren"], "Interim briefing - OHS budget information", """
Hi Lauren,

I'm preparing an interim budget briefing for the Housing Committee chair for November 18. Could you send me:
1. The reduction options OHS submitted with its 2027-29 request;
2. Any additional reduction options OFM asked agencies to identify this fall;
3. Q1 HSRA spending against allotment.

Thanks very much,
Alicia Brandt
Fiscal Analyst, House Appropriations Committee
Washington State House of Representatives
""", "t_alicia")

email("e_denise_recon", "D4 10:55", "c_denise", ["c_lauren", "c_teresa"], "September (FM15) reconciliation - signed off", f"""
Lauren, Teresa,

September is reconciled and signed off. Two items for the Q1 report against the 10/12 ER run:

1. The {m(ACCRUAL)} of September HSRA invoices (020 GF-S) - accrual JV posted in FM16. No change from Tuesday.
2. A {m(MISCODE)} Walla Walla Valley Family Shelter grant payment was coded to the 020 GF-S grants index instead of 030 GF-S. Corrected in FM16. So 020 GF-S goes down {m(MISCODE)} and 030 GF-S goes up the same.

Payroll ties to HRMS for July-September. No other items.

Denise

{SIG['c_denise']}
""", "t_recon")

email("e_cfd_reminder", "D4 11:00", "c_nora", ["c_lauren"], "Bake sale starts in 30 min!", """
2nd floor break room, 11:30. Lemon bars are going fast.

Nora
""", "t_cfd")

email("e_sharon_after", "D4 11:20", "c_sharon", ["c_lauren", "c_teresa"], "After this morning", f"""
Thanks both. To confirm what we agreed: I'll get grantee input on options A and B by next Wednesday, and Teresa will take them to Monica after ELT. No changes to grantee contracts until Monica decides. Lauren, please keep the options as "under consideration" in the Q1 report.

Sharon

{SIG['c_sharon']}
""", "t_hsra_options")

email("e_fns_confirm", "D4 11:32", "c_fns", ["c_lauren"], "FNS: Fiscal note 27-0142 released to OFM", """
Your agency's fiscal note on H-0287.1/27 (request 27-0142) has been released to OFM for review. You will be notified when OFM distributes the note.

This is an automated message from the OFM Fiscal Note System.
""", "t_fn")

email("e_hr_ethics", "D4 12:30", "c_hr", ["c_lauren"], "Reminder: annual ethics training due November 30", """
All staff: the Executive Ethics Board annual training module is due by November 30 in the Learning Center. It takes about 30 minutes.

OHS Human Resources
""", "t_hr_ethics")

email("e_kim_followup", "D4 14:00", "c_kim", ["c_lauren", "c_marcus"], "Crosswalk owner for OHS?", """
Hi both - thanks for joining yesterday. Can you tell me who owns the OHS crosswalk submission, and please make sure provisos that need separate tracking are listed with their appropriation and program index? Due 11/20.

Kim
""", "t_workday")

email("e_jordan_fnq", "D4 15:00", "c_jordan", ["c_lauren"], "27-0142 - two revisions before I distribute", f"""
Lauren,

The note is in good shape. Before I distribute, please:
1. Put the phone line comparison in the narrative (contract vs in-house, annual cost of each), so readers see why you chose the contract.
2. Explain the January 1, 2028 start for the second Program Specialist 3 with the workload numbers, and reference Commerce's local government note, which assumes code enforcement offices will refer displaced households.

Numbers don't need to change. Can you re-release by 10:00 tomorrow?

Jordan
""", "t_fn")

chat("chat_marcus5", "D4 15:30", "c_marcus", ["c_lauren"], "I'm out tomorrow (kid's school thing). 010 numbers in the Q1 table are good from my side. Kim wants a crosswalk owner - you or me?", "t_marcus_chat")

email("e_darnell_followup", "D4 16:20", "c_darnell", ["c_lauren"], "RE: Funds request: laptop replacement FY27", """
Any word on the laptops? I need to order by 11/20.

Darnell
""", "t_laptops")

email("e_gfoa2", "D4 16:45", "c_gfoa", ["c_lauren"], "GFOA Weekly: fiscal notes that hold up", """
This week: how legislative fiscal offices review agency fiscal notes (state your assumptions, prorate partial years, separate one-time from ongoing costs), plus a new GFOA paper on multi-year forecasting for small governments.

Government Finance Officers Association
""", "t_gfoa")

# =============================================================== DAY 4 calls
call(4, "call_jordan", "D4 13:30", "c_jordan", "OFM's analyst calls with questions on the fiscal note before he writes up his review.", [
    ("caller", "Hi Lauren, Jordan. Quick questions on 27-0142. Where does the 650 households a year come from?", 25),
    ("human", "It's from the program's survey of local code enforcement offices, the ones that issue the condemnation and unfit-to-occupy orders. They reported about 650 displaced tenant households a year statewide. The $1,850 average is from our 2025 relocation pilot, which is under the bill's $2,000 cap.", None),
    ("caller", "Okay. And the AAG cost is only in FY28?", 20),
    ("human", "Yes. It's the $18,000 the Attorney General's Office charges for a new rule chapter, and Sec. 7 rules have to be adopted before applications open in January 2028. After that the program runs on staff costs, the phone line contract and the payments.", None),
    ("caller", "Good. Last one: recoveries from landlords, you have them indeterminate. Any order of magnitude?", 20),
    ("human", "We genuinely don't know. Many of these buildings are abandoned or the owners are in foreclosure, and we have no recovery history. I'd rather say indeterminate and explain why than put a number in that offsets the GF-S cost. Recoveries go to the new nonappropriated account anyway, not back to the general fund.", None),
    ("caller", "That works. I'll send you a couple of narrative edits this afternoon.", 10),
    ("human", "Sounds good, I'll turn them around first thing tomorrow.", None),
])

# =============================================================== DAY 4 actions
act(4, "a4_01", "D4 09:00", "create_doc", "cal_ra_options", OPTIONS_DOC, "Prepares the options page for the 10:00 meeting (tasks 3403, 3401).")
act(4, "a4_02", "D4 09:15", "reply", "e_kevin_indirect", f"""
Hi Kevin,

Good question to ask before it goes in. We can't use the de minimis rate here. 2 CFR 200.414(f) allows the 15 percent de minimis only for recipients that don't have a current negotiated indirect cost rate, and OHS has one: {pct(NICR)}% of direct salaries and benefits (our provisional FY27 agreement).

On your draft:
- Indirect at {pct(NICR)}% x {m(KV['personnel'], False)} personnel = {m(KV_NICR)}
- Total {m(KV_DIRECT, False)} direct + {m(KV_NICR)} = {m(KV_TOTAL_NICR)}
- That leaves {m(KV_ROOM)} under the $500,000 maximum, which you could put back into direct costs if the NOFO's own admin limits allow.

You'd treated the subaward right for MTDC (only the first $50,000 counts), but with our negotiated rate the base is salaries and benefits, so it doesn't matter here. Please have Hoang look at the final budget, since he owns the rate agreement.

Lauren
""", "Technical advice on grant budget preparation (task 3398); exact numbers.")
act(4, "a4_03", "D4 09:20", "send", "e_jordan_fncheck", f"""
Jordan - DRAFT fiscal note for 27-0142 attached for Alicia, marked DRAFT on every page. FY28 {m(FY28_ROUND, False)} GF-S ({r2(FY28['fte']).quantize(D('0.1'))} FTE), FY29 {m(FY29['total'].quantize(D('1')), False)} (3.5 FTE), 2027-29 {m(BI_2729.quantize(D('1')), False)}. Landlord recoveries indeterminate. I'll release the final in FNS by 11:30.

Lauren
""", "Shares the draft only through OFM, marked DRAFT, as the fiscal note instructions allow.")
act(4, "a4_04", "D4 10:00", "noop", None, "HSRA spending options meeting with Teresa and Sharon (10:00-11:00).", "Background.")
act(4, "a4_05", "D4 11:05", "read", "e_denise_recon", "", "Final reconciliation: the $18,240 miscode moves 020 GF-S down. The Q1 numbers change again.")
act(4, "a4_06", "D4 11:30", "send", "e_fns_request", "Released fiscal note 27-0142 (H-0287.1/27) to OFM in FNS.\n\n" + fn_table() + "\n" + FN_ASSUMPTIONS +
    "\n- The Attorney General cost is FY28 only because Sec. 7 rules must be adopted before applications open on January 1, 2028; there is no further rulemaking assumed.",
    "Releases the note through FNS on time (task 3405).")
act(4, "a4_07", "D4 13:05", "read", "e_alicia_ask", "", "Recognizes item 2 asks for the confidential Tier 2 list; will answer Friday after checking with Teresa.")
act(4, "a4_08", "D4 14:15", "create_doc", "e_teresa_q1", Q1_REPORT, "Drafts the Q1 report with Accounting's final numbers (tasks 3394, 3395).")
act(4, "a4_09", "D4 15:20", "read", "e_jordan_fnq", "", "Narrative edits only; will do them first thing Friday.")
act(4, "a4_10", "D4 15:40", "reply", "chat_marcus5", "I'll own the crosswalk with you as backup. I'll tell Kim. Enjoy the school thing!", "Takes the crosswalk; doesn't start it this week.")
act(4, "a4_11", "D4 16:10", "send", "e_teresa_q1", "Teresa - draft Q1 Budget Status Report is in the Budget Office folder, on Accounting's signed-off numbers (020 GF-S Q1 variance " + m(P020_GFS_VAR) + "). Please mark it up tonight or first thing; it goes to Monica by 3:00 tomorrow.", "Review before release.")
act(4, "a4_12", "D4 16:40", "read", "e_jenna_pc", "", "Notes 13.5 vacant as of 11/1 for OFM question 4 (the 10/31 extract said 15.5).")

# =============================================================== DAY 5 (Fri 11/6) items
email("e_teresa_d5", "D5 08:05", "c_teresa", ["c_lauren"], "RE: Q1 report draft", f"""
Lauren - nice work. Three things:
(a) Lead with the year-end gap, which you mostly do. Keep it.
(b) Add a line on the ESG subgrant start-date changes Kevin told us about. Monica will get asked why ESG is underspent in Q2.
(c) Please draft three or four talking points I can use at ELT on Monday: the gap, the options, what we've told OFM. I don't need them until Monday 8:00, but I'd like them before you leave today if you can.

OFM answers: send me the draft by 10:30. I'll turn it around fast.

T

{SIG['c_teresa']}
""", "t_q1report")

email("e_kim_crosswalk", "D5 08:30", "c_kim", ["c_lauren"], "OHS crosswalk - what we need by 11/20", """
Thanks for taking it, Lauren. For 11/20 we need, for every AFRS appropriation index and program index you use:
- the Workday Fund, Cost Center and Program worktags;
- which appropriations roll up to which agency-level appropriations in the budget bill (by fund and fiscal year);
- every proviso that needs separate tracking, with its amount;
- the indexes you'd use for a Governor's Emergency Fund allocation if you received one.

Template attached in yesterday's email.

Kim
""", "t_workday")

email("e_darnell_d5", "D5 09:00", "c_darnell", ["c_lauren"], "RE: Funds request: laptop replacement FY27", """
Sorry to nag - Dell rep says the contract price holds through 11/20 only.

D
""", "t_laptops")

email("e_megan2", "D5 10:30", "c_megan", ["c_lauren"], "Following up - rental assistance cut", """
Hi Lauren, following up. A source tells me the list OFM got from OHS includes a $3 million cut to rental assistance. Can you confirm or wave me off? On deadline at 2.

Megan Holt
Cascade Public Ledger
""", "t_media")

chat("chat_teresa_ok", "D5 11:10", "c_teresa", ["c_lauren"], "OFM answers look good. send them. on Alicia: fine to send the public R1-R3 and the Q1 numbers, nothing on Tier 2 - point her to Jordan.", "t_teresa_chat")

email("e_elena_media", "D5 11:40", "c_elena", ["c_lauren", "c_teresa"], "RE: Megan Holt inquiry", """
Thanks for routing this. I'm responding to Megan that the agency's budget request is public on OFM's site and that we don't comment on the Governor's budget before it's released. Please send any follow-ups my way.

Elena Vasquez
Communications Director | OHS
""", "t_media")

email("e_rosa_invoice", "D5 13:00", "c_rosa", ["c_lauren"], "September ESG reimbursement request (A-19)", """
Hi Lauren, attached is our September A-19 for $48,312.60 (shelter operations $31,040.10, rapid rehousing $17,272.50). The $12,000 budget amendment is signed and with Hoang.

Rosa Delgado
Lewis-Mason Shelter Network
""", "t_rosa")

email("e_fns_distrib", "D5 14:00", "c_fns", ["c_lauren", "c_ben"], "FNS: Fiscal note 27-0142 distributed", """
OFM has distributed the fiscal note package for H-0287.1/27 (request 27-0142). It is available on the OFM fiscal note website and has been sent to the requester.

This is an automated message from the OFM Fiscal Note System.
""", "t_fn")

email("e_ben_d5", "D5 14:10", "c_ben", ["c_lauren"], "Thanks on the FN", """
Saw it went out - Tyler says the Rep. is happy with how clear the assumptions are. Thanks for holding the line on the timing.

Ben
""", "t_fn")

email("e_ofm_fm16", "D5 14:30", "c_ofm", ["c_lauren"], "Reminder: FM16 close Monday 11/9", """
Statewide Accounting reminder: AFRS fiscal month 16 (October) closes at 5:00 p.m. Monday, November 9. Accrual entries for October activity should be keyed by then.

OFM Statewide Accounting
""", "t_ofm_fm16")

chat("chat_nora_packet", "D5 15:05", "c_nora", ["c_lauren"], "got the Q1 report - in the packet. thank you!", "t_q1report")

email("e_hr_d5", "D5 15:30", "c_hr", ["c_lauren"], "Veterans Day - offices closed Wednesday 11/11", """
Reminder: state offices are closed Wednesday, November 11, for Veterans Day.

OHS Human Resources
""", "t_hr_hol")

email("e_jordan_thanks", "D5 16:05", "c_jordan", ["c_lauren"], "RE: OHS 2027 Supplemental - follow-up questions", """
Thanks Lauren, this is what I needed. Leave M1 as is for now; I'll let you know if we want a revised package after the November forecast.

Jordan
""", "t_ofm_q")

chat("chat_sharon_d5", "D5 16:20", "c_sharon", ["c_lauren"], "thanks for this week. grantee input on A/B by Weds as promised", "t_sharon_chat")

event("cal_next_week", "D5 16:30", "c_teresa", "HSRA decision follow-up with Monica", "After ELT. Lauren to bring the grantee input on options A and B.",
      "2026-11-10 14:00", "2026-11-10 14:45", "Director's conference room", ["c_teresa", "c_lauren", "c_sharon", "c_monica"], thread="t_hsra_options")

# =============================================================== DAY 5 actions
OFM_ANSWERS = f"""
Jordan,

OHS responses to your questions of November 2 on M1 and FTEs. Teresa Lindqvist has reviewed them.

1. Households and average assistance (grantee data, all fund sources)
- July 2026: 1,942 households, $2,548 average
- August 2026: 1,968 households, $2,561 average
- September 2026: 1,989 households, $2,566 average
- Q1 average: {Q1_HH_MO.quantize(D('1')):,} households a month against {int(FY26_HH_MO):,} in FY26 (+{r2(HH_GROWTH)}%), and {m(Q1_AVG)} per household against {m(FY26_AVG)} (+{r2(AVG_GROWTH)}%). The growth is about evenly split between more households and higher assistance per household (rents). Pierce and Spokane account for most of the household growth.
Updated projection (not in M1): after Accounting's September reconciliation, Q1 020 GF-S spending was {m(P020_GFS_ADJ)} against a {m(ROWS[2][4], False)} allotment. At the Q1 pace FY27 GF-S would be {m(P020_PROJ, False)} against {m(ROWS[2][3], False)}, a shortfall of {m(P020_GAP, False)}, which is {m(GAP_BEYOND_DP, False)} more than M1's {m(DP_M1, False)}. We have not changed M1 in ABS; let us know if you want a revised package.

2. Fit with the supplemental instructions
HSRA is not an entitlement, and we can't spend beyond the appropriation. Management options are under consideration by the Director: capping new intake at the FY26 average (about {m(OPT_A_GFS, False)} GF-S over nine months, about {OPT_A_HH.quantize(D('1')):,} fewer households) and capping average assistance at the FY26 level (about {m(OPT_B_GFS, False)} GF-S). If M1 is not funded, OHS would need both from December, with 30 days' notice to grantees, and together they still leave a gap, so grantee contracts would be reduced for the rest of the year (closing intake in some counties by spring, as M1 states). We'll tell you the Director's decision when it's made.

3. Landlord mitigation proviso (Program 040)
Q1 claims were {m(PROVISO_Q1)} against {m(PROVISO_Q1_ALLOT)} allotted. At that pace FY27 claims will be {m(PROVISO_PROJ)}, a projected lapse of {m(PROVISO_LAPSE)} of the {m(PROVISO, False)}. It will not be redirected.

4. FTEs
As of November 1, {FTE_FILLED_NOV1} FTE filled of {FTE_BUDGET} allotted ({FTE_VACANT_NOV1} vacant, including 4.0 held vacant for reduction option R3). Estimated FY27 vacancy savings are about $940,000: GF-S $610,000, Housing Stability Account $290,000, GF-Federal $40,000. This assumes the 9.5 vacancies not held for R3 fill evenly by March.

Lauren Whitaker
Budget Analyst, Office of Housing Stability
360-555-0167
"""

act(5, "a5_01", "D5 08:45", "read", "e_teresa_d5", "", "Teresa's edits; talking points requested (the human never gets to them).")
act(5, "a5_02", "D5 09:30", "send", "e_jordan_fnq", f"""
Re-released 27-0142 in FNS with the narrative edits:
- Phone line: contract with the statewide information and referral provider at {m(HL_CONTRACT, False)} a year from January 2028, against {m(HL_INHOUSE)} a year plus {m(HL_INHOUSE_EQUIP, False)} one-time for 2.0 Customer Service Specialist 2 in house. The contract is the least expensive reasonable option.
- Second Program Specialist 3 from January 1, 2028: about 820 applications a year (650 approved) at 3.5 hours each is 2,870 hours a year, or about 1,435 hours from January to June 2028, which is more than one PS3 can do (780 productive hours in six months). This is consistent with Commerce's local government note, which assumes code enforcement offices will refer displaced households to OHS.
Numbers unchanged: FY28 {m(FY28_ROUND, False)}, FY29 {m(FY29['total'].quantize(D('1')), False)}.
""", "Revises the narrative for OFM (task 3405).")
act(5, "a5_03", "D5 10:00", "send", "e_it_laptops", f"""
Teresa (cc Darnell, Marcus) - recommendation on IT's laptop request ({m(LAP_ALL, False)} for {LAP_N} units):

Recommend approving {m(LAP_NOW, False)} now for the {LAP_EOL} units that are past the five-year lifecycle and out of warranty, from 010 GF-S. 010 was {m(P010_Q1_UNDER)} under its Q1 allotment from vacancies, and the year looks about {m(P010_PROJ_UNDER, False)} under at that pace (somewhat less now that the two Fiscal Analyst 3 hires have started). Defer the other {LAP_N - LAP_EOL} ({m(LAP_DEFER, False)}) to the FY28 refresh, since they don't reach five years until April-June and every GF-S dollar is under scrutiny while HSRA is short. Laptops are below the $5,000 capitalization threshold, so they're Object E and go on the small and attractive assets inventory.

Your decision; Darnell needs to order by 11/20.

Lauren
""", "Summarizes a funds request and recommends partial approval (task 3399); the Budget Director decides.")
act(5, "a5_04", "D5 10:25", "send", "e_teresa_d5", "Teresa - draft OFM answers below for your review.\n" + OFM_ANSWERS, "Review before release.")
act(5, "a5_05", "D5 11:30", "reply", "e_jordan_q", OFM_ANSWERS, "Sends OFM the answers on time with reconciled numbers, the 11/1 FTE count and the updated projection, without touching ABS.")
act(5, "a5_06", "D5 11:50", "forward", "e_megan2", "Elena - Megan's follow-up below, asking us to confirm a specific figure. I have not responded. Teresa cc'd.", "Media to Communications again; does not confirm or deny.")
act(5, "a5_07", "D5 13:10", "reply", "e_alicia_ask", f"""
Hi Alicia,

Happy to help with the briefing.

1. Submitted reduction options (2027-29 request, released in ABS 9/14 and on OFM's Agency Budget Request website):
   R1 Reduce housing navigation contracts 15% (-$840,000 GF-S for the biennium); R2 Eliminate the Housing Stability Conference (-$60,000); R3 Hold 4.0 FTE vacant in Program 010 (-$812,000). Total -$1,712,000 GF-S.
2. Additional options: any further work we've done with OFM this fall is part of the Governor's budget development, so I'm not able to share it. Jordan Kessler at OFM is the right contact.
3. Q1 HSRA (Program 020) GF-S: {m(P020_GFS_ADJ)} spent against a {m(ROWS[2][4], False)} allotment (after Accounting's September reconciliation). Our response to OFM's questions on M1 includes an updated FY27 projection; Jordan can share it with you.

Lauren Whitaker
Budget Analyst, Office of Housing Stability
""", "Gives legislative staff the public record and the actuals; withholds the pre-decisional list (RCW 42.56.280) with Teresa's OK.")
act(5, "a5_08", "D5 13:40", "forward", "e_rosa_invoice", "Kevin, Hoang - Lewis-Mason's September A-19 ($48,312.60). Over to you for program approval and the ESG draw.", "Routine routing.")
act(5, "a5_09", "D5 14:30", "edit_doc", "a4_08", f"""
Final edits to the Q1 report per Teresa:
- Added under 4. Issues: "ESG subgrant timing: three FY2025 ESG subgrants totaling {m(ESG_DELAYED_TOTAL, False)} (Grays Harbor, Okanogan, Walla Walla) start January 1 instead of October 1 after environmental review delays. About {m(ESG_DELAYED_Q2, False)} of planned Q2 federal spending moves to January-June; the full amounts are still expected to be spent by June 30. The Q7 allotment amendment (due January 25) will move the federal allotment to match."
- Kept the year-end gap as the opening line; marked options A and B as under consideration.
""", "Covers the ESG timing change from Monday (task 3396) in the report; the Q7 amendment itself waits for January.")
act(5, "a5_10", "D5 14:55", "send", "e_nora_elt", "Monica (cc Teresa, Robert, Nora) - the FY27 Q1 Budget Status Report for Monday's ELT is attached, on Accounting's signed-off September numbers. The headline: HSRA GF-S is on pace for a " + m(P020_GAP, False) + " shortfall against its appropriation; options are under consideration for your decision.\n\n" + Q1_REPORT, "Delivers the report on time and reconciled (task 3395).")
act(5, "a5_11", "D5 15:35", "reply", "e_kim_crosswalk", "Hi Kim - I'm the OHS owner, Marcus Bell is backup. We'll have the crosswalk to you by 11/18, including the landlord mitigation proviso (Program 040, index 4030, $1,800,000 FY27 GF-S) as a separate Program worktag.", "Acknowledges; the crosswalk itself is not started this week.")
act(5, "a5_12", "D5 16:40", "noop", None, "Clears the inbox and leaves for the weekend. Teresa's ELT talking points are not drafted.", "The human never writes the talking points.")
