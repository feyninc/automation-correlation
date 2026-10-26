from part3_d2 import *


def fn_table():
    cols = [("FY28", FY28), ("FY29", FY29), ("FY30", FYOUT), ("FY31", FYOUT), ("FY32", FYOUT), ("FY33", FYOUT)]
    out = ["Object | " + " | ".join(c for c, _ in cols)]
    out.append("FTE | " + " | ".join(f"{r2(v['fte']).quantize(D('0.1'))}" for _, v in cols))
    for key, label in [("A", "A Salaries and wages"), ("B", "B Employee benefits"), ("C", "C Professional service contracts (toll-free line)"),
                       ("E", "E Goods and services"), ("G", "G Travel"), ("N", "N Grants, benefits and client services"),
                       ("T", "T Intra-agency reimbursements (indirect)")]:
        out.append(f"{label} | " + " | ".join(m(v[key], False) for _, v in cols))
    out.append("Total GF-S (001-1) | " + " | ".join(m(v["total"], False) for _, v in cols))
    out.append(f"Biennial totals: 2027-29 {m(BI_2729, False)}; 2029-31 {m(BI_2931, False)}; 2031-33 {m(BI_3133, False)}")
    return "\n".join(out)


FN_ASSUMPTIONS = f"""
Assumptions
- Effective 90 days after the 2027 session adjourns (late July 2027). Applications accepted from January 1, 2028 (Sec. 3(4)).
- Displaced households: {HH_YEAR} a year statewide (local code enforcement survey compiled by the program). FY28 covers six months of applications: 325 households.
- Average payment {m(AVG_PAY, False)} (documented relocation costs in OHS's 2025 pilot), below the $2,000 cap in Sec. 3(2).
- Staffing, prorated from hire dates: 1.0 Management Analyst 5 from August 1, 2027 (program design, rules, contract); 1.0 Program Specialist 3 from November 1, 2027 (procedures, then applications) and a second from January 1, 2028 (about 820 applications a year, 79 percent approved, at 3.5 hours each is 2,870 hours, or 1.8 FTE at 1,560 productive hours; the first six months need about 1,435 hours); 0.5 Fiscal Analyst 2 from January 1, 2028 (payments and landlord recoveries). FY28 {r2(FY28['fte']).quantize(D('0.1'))} FTE, 3.5 FTE ongoing.
- Salaries at FY28 step L from SPS; benefits {pct(BEN_PCT)}% plus {m(INS, False)} per FTE for insurance; goods and services {m(GS_FTE, False)} per FTE; travel {m(TRAVEL_FTE, False)} per FTE; one-time equipment {m(EQUIP, False)} per new hire; agency indirect {pct(INDIRECT)}% of salaries and benefits (OHS FY27 cost model).
- Attorney General rulemaking support {m(AAG, False)} in FY28 (Sec. 7).
- Toll-free line (Sec. 4) contracted with the statewide information and referral provider at {m(HOTLINE_MO, False)} a month from January 2028: {m(HL_CONTRACT, False)} a year, against {m(HL_INHOUSE)} a year (plus {m(HL_INHOUSE_EQUIP, False)} one-time) to staff it in house with 2.0 Customer Service Specialist 2. The contract is the least expensive reasonable option.
- Cash receipts: landlord recoveries under Sec. 5 are indeterminate. OHS has no data on how often landlords of condemned buildings can be found or will pay; recoveries would go to the new nonappropriated tenant relocation assistance account and would not reduce the GF-S need in the first years.
- Local government impacts are for the Department of Commerce's Local Government Fiscal Note Program.
"""

# =============================================================== DAY 3 (Wed 11/4) items
email("e_robert_push", "D3 08:05", "c_robert", ["c_lauren"], "Q1 report - need it today", f"""
Lauren,

Teresa's at OFM this morning so I'm coming to you directly. Monica is meeting the Governor's policy advisor Thursday afternoon and wants the HSRA number in hand. Please send the Q1 report to Monica and me by noon today. The numbers are what they are; don't wait on Accounting's paperwork.

Robert

{SIG['c_robert']}
""", "t_q1report")

email("e_rosa_thanks", "D3 09:00", "c_rosa", ["c_lauren"], "RE: Budget revision question - Lewis-Mason ESG subgrant", """
Thank you Lauren - Hoang sent the amendment form and we'll return it this week.

Rosa
""", "t_rosa")

email("e_sharon_intake", "D3 08:50", "c_sharon", ["c_lauren"], "County intake numbers you asked for", f"""
Lauren, here's what Owen pulled from the grantee data system. Spokane and Pierce are the big growth.

Sharon

{SIG['c_sharon']}
""", "t_hsra_options", att=["d_intake"])

doc("d_intake", "D3 08:50", "HSRA intake by county - September and October 2026.xlsx", """
New HSRA applications approved, by county group (grantee data system, pulled 11/3)
County group | FY26 monthly average | September 2026 | October 2026 (preliminary)
King | 610 | 641 | 652
Pierce | 290 | 341 | 352
Spokane | 205 | 262 | 270
Snohomish | 180 | 188 | 191
Clark | 140 | 146 | 150
All other counties (34) | 385 | 411 | 418
Statewide | 1,810 | 1,989 | 2,033

October is preliminary; grantees report through the 10th of the following month. Waitlists: Pierce 410 households, Spokane 260.
""", kind="sheet", thread="t_hsra_options", meta={"format": "xlsx"})

email("e_sharon_transfer", "D3 09:40", "c_sharon", ["c_lauren"], "Use the landlord mitigation money for HSRA", f"""
Lauren,

040 isn't going to spend the landlord mitigation money. Q1 claims were only {m(PROVISO_Q1, False)}. Let's move about $940K of it over to HSRA in the next allotment amendment so I don't have to close intake in Pierce and Spokane. It's all GF-S in our agency anyway. Can you just do that in TALS?

Sharon

{SIG['c_sharon']}
""", "t_transfer")

email("e_tyler_ask", "D3 10:15", "c_tyler", ["c_lauren"], "Relocation bill fiscal note - quick number?", """
Hi Lauren,

Ben Hartley gave me your name. Rep. Dominguez is doing a housing caucus press availability tomorrow morning and wants to be able to say what the relocation bill costs. Could you send me the number today, even a ballpark? We won't quote you or the agency.

Thanks a ton!
Tyler Nguyen
Legislative Assistant to Rep. Carla Dominguez
""", "t_tyler")

chat("chat_ben3", "D3 10:25", "c_ben", ["c_lauren"], "Tyler's pinging me too. can we just give him a ballpark? it'll be public Thursday anyway and the Rep is a friend of the agency", "t_ben_chat")

email("e_sharon_abs", "D3 10:30", "c_sharon", ["c_lauren"], "RE: Use the landlord mitigation money for HSRA", f"""
Also - can you update M1 in ABS to $5.5M today so OFM is looking at the right number before they make decisions? Robert agrees.

S
""", "t_transfer")

email("e_it_laptops", "D3 11:00", "c_darnell", ["c_lauren", "c_marcus"], "Funds request: laptop replacement FY27", f"""
Lauren, Marcus,

Requesting {m(LAP_ALL, False)} in FY27 to replace {LAP_N} laptops (Dell Latitude under the state master contract at {m(LAP_UNIT, False)} each). {LAP_EOL} of ours are past the five-year lifecycle and out of warranty; the other {LAP_N - LAP_EOL} reach five years in April-June 2027. Can 010 cover it? I need to place the order by 11/20 to hold the contract price.

Darnell Brooks
IT Manager | OHS
""", "t_laptops")

event("cal_ra_options", "D3 11:15", "c_teresa", "HSRA spending options (Sharon, Teresa, Lauren)",
      "Lauren - please bring a one-page set of options with what each saves this fiscal year, GF-S and all funds.",
      "D4 10:00", "D4 11:00", "OHS 3rd floor conference room B", ["c_teresa", "c_sharon", "c_lauren"], thread="t_hsra_options")

email("e_kevin_indirect", "D3 11:30", "c_kevin", ["c_lauren"], "Indirect on the HUD youth planning grant application", f"""
Lauren,

We're applying for a HUD youth homelessness planning grant, $500,000 maximum over two years, application due 11/16. Draft budget:

Personnel (salaries and benefits) {m(KV['personnel'], False)}
Travel {m(KV['travel'], False)}
Supplies {m(KV['supplies'], False)}
Subaward to Spokane County {m(KV['subaward'], False)}
Other (printing, meeting space) {m(KV['other'], False)}
Total direct {m(KV_DIRECT, False)}
Indirect at the 15% de minimis on MTDC ({m(KV_MTDC, False)}): {m(KV_DEMIN)}
Total {m(KV_TOTAL_DEMIN)}

OK to use the de minimis? It seemed simplest.

Kevin

{SIG['c_kevin']}
""", "t_indirect")

email("e_workday_materials", "D3 12:30", "c_kim", ["c_lauren", "c_marcus"], "Slides and crosswalk template for today's workshop", """
Attached are today's slides and the agency crosswalk template. Key decisions for agencies: one Cost Center per AFRS organization index; Program worktag replaces the program index; appropriations become Fund plus a budget "Appropriation" worktag; budget provisos that require separate tracking get their own Program worktag. Crosswalks are due November 20.

Kim
""", "t_workday")

email("e_kevin_luncheon", "D3 13:05", "c_kevin", ["c_lauren"], "Coding for the 11/19 provider training and appreciation day", f"""
Lauren,

We're holding a Provider Training & Appreciation Day on November 19 for our ESG subrecipients: morning training on the new HMIS data standards and the HUD ESG changes, then lunch, afternoon networking, a wine and cheese reception at 4, and $25 gift cards as a thank-you. Quote attached, {m(LUNCH_TOTAL)} total.

We have ESG admin left, so can I code it all to ESG admin (index 3050, object E)? I need to sign the venue contract Friday.

Kevin

{SIG['c_kevin']}
""", "t_luncheon", att=["d_luncheon_quote"])

doc("d_luncheon_quote", "D3 13:05", "Quote - Provider Training & Appreciation Day 11-19-2026.xlsx", "\n".join(
    [f"{n} | {m(a)}" for n, a in LUNCH] + [f"Total | {m(LUNCH_TOTAL)}"]), kind="sheet", thread="t_luncheon", meta={"format": "xlsx"})

chat("chat_marcus4", "D3 15:30", "c_marcus", ["c_lauren"], "so provisos get their own Program worktag - that means 4030 landlord mitigation needs one. I'll put it in the crosswalk draft, you check the 020/030 rows when you can?", "t_marcus_chat")

email("e_jordan_fncheck", "D3 15:45", "c_jordan", ["c_lauren"], "RE: H-0287.1 - OFM analyst", """
How's 27-0142 coming? Alicia asked whether she could see a draft before Thursday. If you want to share one, send it to me marked DRAFT and I'll pass it along.

Jordan
""", "t_fn")

email("e_nora_elt", "D3 16:00", "c_nora", ["c_lauren", "c_teresa"], "11/9 ELT packet", """
Hi Lauren and Teresa - I'm assembling Monday's ELT packet Friday at 3:00. The Q1 budget status report is item 2. Thanks!

Nora
""", "t_q1report")

chat("chat_teresa3", "D3 16:45", "c_teresa", ["c_lauren"], "back from OFM. saw your note on HSRA and Sharon's asks - agree on all of it. we'll sort the options at 10 tomorrow. FN draft looks good, two small comments in the file.", "t_teresa_chat")

# =============================================================== DAY 3 calls
call(3, "call_tyler", "D3 14:40", "c_tyler", "The sponsor's legislative assistant presses for the fiscal note number before it goes to OFM.", [
    ("caller", "Hi Lauren, it's Tyler from Rep. Dominguez's office. Sorry to chase. Just trying to get a ballpark on the relocation note for tomorrow. Are we talking under a million?", 15),
    ("human", "Hi Tyler. I'm sorry, I can't give you a number before OFM has reviewed it. Fiscal notes go to OFM through the Fiscal Note System. Ours is due tomorrow at noon, and OFM distributes it to you and posts it.", None),
    ("caller", "Not even off the record? She just doesn't want to be caught flat-footed at the press availability.", 15),
    ("human", "I understand. If House staff need to see something before it's final, Jordan Kessler at OFM can share a draft marked DRAFT, so the best route is through him or Alicia Brandt on the committee. What I can do is walk you through what the bill asks the agency to do, if that helps with talking points.", None),
    ("caller", "Okay, I'll ping Alicia. Thanks Lauren.", 10),
    ("human", "Thanks Tyler. For anything on the agency's position on the bill, Ben Hartley is your contact.", None),
])

# =============================================================== DAY 3 actions
act(3, "a3_01", "D3 08:20", "reply", "e_robert_push", f"""
Hi Robert,

I can give you a preliminary internal number now, for Monica's prep only: Q1 HSRA GF-S is about {m(-(ROWS[2][4] - PRELIM_ADJ), False)} over allotment once Accounting's September invoices are counted. At that pace we'd be roughly $5.5 million short for the year, against the $3.9 million in M1.

The report itself shouldn't go until Accounting signs off September. That's tomorrow at noon, and Denise is still finding items (the September invoices alone moved Q1 by {m(ACCRUAL, False)}). I'll have the report to Teresa Thursday afternoon and to Monica Friday as scheduled. If Monica needs it before her Thursday meeting, I can get Teresa a reviewed version by Thursday 3:00 once the reconciliation is done.

Lauren

{SIG['c_lauren']}
""", "Holds the line on reconciliation but gives the COO what he actually needs, marked preliminary and internal. Copies Teresa.")
act(3, "a3_02", "D3 09:30", "reply", "e_owen_input", f"""
Hi Owen,

Thanks for turning this around fast. I've reviewed it against the bill and the FY27 cost model, and it needs several changes before it's usable:

1. Rates: the sheet uses the 2025-session model (superseded). FY27 model: MA5 {m(SAL['MA5'], False)}, PS3 {m(SAL['PS3'], False)}; benefits are {pct(BEN_PCT)}% plus {m(INS, False)} per FTE for insurance, not a flat {pct(OLD_BEN_PCT)}%.
2. Timing: the bill takes effect late July 2027 and Sec. 3(4) holds applications until 1/1/2028. Staff should be prorated from hire dates, and FY28 payments cover six months (325 households), not 650.
3. Payments: use the $1,850 average from your pilot, not the $2,000 cap.
4. Phone line: Sec. 4 lets us contract it. A contract at about $96,000 a year is roughly half the cost of 2.0 in-house CSS2s, and OFM wants the least expensive reasonable option.
5. Missing: 0.5 Fiscal Analyst 2 for payments and Sec. 5 recoveries, Attorney General rulemaking support (Sec. 7), and agency indirect (Object T).
6. Recoveries under Sec. 5 should be marked indeterminate.

I'll build the note from your workload numbers (650 households, the pilot average and your processing time), which are the parts that matter most. FY28 will be well under your figure; the full years after that end up close to it.

Lauren
""", "Examines the program's estimate for accuracy and conformance (task 3402).")
act(3, "a3_03", "D3 10:05", "edit_doc", "a2_12", "H-0287.1 fiscal note working file - Staffing and Summary tabs completed:\n\n" + fn_table() + "\n" + FN_ASSUMPTIONS,
    "Builds the cost estimate from accounting records and the cost model (task 3405); the contract option comes from the hotline comparison.")
act(3, "a3_04", "D3 10:40", "reply", "e_tyler_ask", """
Hi Tyler,

Thanks for reaching out. Fiscal notes go from the agency to OFM through the Fiscal Note System. Ours on H-0287.1 is due to OFM tomorrow at noon, and OFM reviews it and distributes it to the requester and posts it publicly. I'm not able to share numbers before that. If House staff need a look before then, Jordan Kessler at OFM (jordan.kessler@ofm.wa.gov) coordinates drafts with Alicia Brandt on the committee.

Best,
Lauren Whitaker
Budget Analyst, Office of Housing Stability
""", "Declines to release the fiscal note directly (OFM fiscal note instructions).")
act(3, "a3_05", "D3 10:45", "reply", "chat_ben3", "I can't. OFM's rule is that agencies don't distribute fiscal notes; drafts go through the OFM analyst, marked DRAFT. Jordan already offered to share a draft with Alicia. I've told Tyler that politely and pointed him to Jordan/Alicia.", "")
act(3, "a3_06", "D3 11:20", "read", "e_it_laptops", "", "Funds request to evaluate against Program 010's projected underspend; recommends Friday.")
act(3, "a3_07", "D3 11:30", "schedule", "cal_ra_options", "Accepted: HSRA spending options, Thu 11/5 10:00-11:00, conf room B.", "")
act(3, "a3_08", "D3 12:00", "read", "e_kevin_indirect", "", "Sees the de minimis problem; answers Thursday morning.")
act(3, "a3_09", "D3 13:00", "noop", None, "Attends the Workday Phase 1A budget structure workshop (1:00-2:30).", "Background.")
act(3, "a3_10", "D3 15:05", "send", "chat_teresa2", f"Teresa - DRAFT fiscal note on H-0287.1 is in the Fiscal Notes folder ('H-0287.1 fiscal note working file'). FY28 {m(FY28_ROUND, False)} GF-S, {r2(FY28['fte']).quantize(D('0.1'))} FTE; FY29 {m(FY29['total'], False)}, 3.5 FTE; 2027-29 {m(BI_2729, False)}. Phone line costed as a contract (cheaper than in-house by about $98K a year). Recoveries indeterminate. Owen's $1.76M used the 2025 rates and a July start. I plan to send Jordan a DRAFT tomorrow 9:00 and release in FNS by 11:30 if you're OK.", "Gets the Budget Director's review before release.")
act(3, "a3_11", "D3 15:20", "reply", "e_kevin_luncheon", f"""
Hi Kevin,

Thanks for checking before signing. Short version: not all of this can go on ESG, and the final call is Hoang's.

- The wine and cheese reception ({m(LUNCH[2][1])}) is unallowable on a federal award (2 CFR 200.423, alcoholic beverages).
- The gift cards ({m(LUNCH[3][1])}) are entertainment or gifts; 2 CFR 200.438 makes those unallowable unless they have a specific programmatic purpose and are in the award, and ours aren't.
- The training part (venue, lunch and AV, {m(LUNCH_MAYBE)}) may be allowable as a conference cost under 2 CFR 200.432, but only if the day's main purpose is the technical training and the costs are reasonable. It would also come out of our retained ESG admin, which has {m(ESG_ADMIN_LEFT)} left for the rest of the award (24 CFR 576.108 caps admin at 7.5%).

I've copied Hoang. Please don't sign the venue contract until he confirms the coding, and let's not assume the unallowable part can just move to state funds either; Denise can tell you what state rules allow.

Lauren
""", "Advises on allowability but leaves the decision with Grants Compliance (2 CFR 200 cost principles).")
act(3, "a3_12", "D3 15:55", "send", "e_teresa_q1", f"""
Teresa,

Three things before tomorrow's 10:00:

1. HSRA (020 GF-S) is on track to overspend its appropriation. Q1 is about {m(-(ROWS[2][4] - PRELIM_ADJ), False)} over allotment with Denise's {m(ACCRUAL, False)} of September invoices (final tie-out Thursday noon). At the Q1 pace we'd spend about {m(PRELIM_PROJ, False)} against {m(ROWS[2][3], False)}, a gap of about {m(PRELIM_GAP, False)}, or {m(PRELIM_GAP - DP_M1, False)} more than M1. We can't spend past the appropriation (RCW 43.88.130), so we need a management decision this month, not in session. I'll bring options with savings tomorrow.
2. Sharon asked me to move about $940K of the 040 landlord mitigation proviso to HSRA in TALS. It's "solely for" money (Sec. 131(4)), so it can't be used for HSRA. Only the non-proviso 040 GF-S could be reallotted between programs, and that's your call with OFM in the Q7 amendment. I haven't done anything.
3. She also asked me to change M1 in ABS to $5.5M. We can't amend after submittal without OFM's authorization, and Jordan asked us to report changes in Friday's answers instead, so that's where I'll put the updated projection unless you want to ask him for a revised DP.

Robert asked for the Q1 report today. I gave him the preliminary number for Monica's prep and said the report follows Accounting's sign-off.

Lauren
""", "Escalates the projected overspend and the two improper requests to the decision-maker.")
act(3, "a3_13", "D3 16:30", "reply", "e_sharon_transfer", f"""
Hi Sharon,

I understand the pressure on Pierce and Spokane. On both asks:

- Landlord mitigation: the $1,800,000 is provided "solely for" the landlord mitigation program (Sec. 131(4) of the 2026 supplemental). If it isn't spent on that, it lapses; we can't redirect it to HSRA through allotments or anything else. We're projecting about {m(PROVISO_LAPSE, False)} unspent, and that will be visible to OFM and the Legislature.
- The rest of 040's GF-S ({m(P040_NONPROVISO_ANNUAL, False)} this year) isn't restricted that way. Moving some of it between programs would be a quarterly allotment amendment (Q7, due January 25, not retroactive), and that's Teresa's decision with OFM, not something I can do in TALS on my own. I've flagged it to her for tomorrow.
- M1: we can't change a released decision package in ABS without OFM's authorization. Jordan asked us to tell him about changes in our Friday answers, and I'll give him the updated projection there.

See you at 10.

Lauren
""", "Explains appropriation limits and who decides (task 3397); does not move money or amend the DP.")
act(3, "a3_14", "D3 16:50", "reply", "e_jordan_fncheck", f"""
Hi Jordan - Teresa is reviewing now. I'll send you a DRAFT for Alicia by 9:00 tomorrow and release the note in FNS by 11:30. Lead-agency assumptions are going on the Request tab this afternoon.

Lauren
""", "Coordinates the draft through OFM.")
