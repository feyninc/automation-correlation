from part1_world import *

DAYS = {d: {"actions": [], "calls": []} for d in range(1, 6)}


def act(day, id, at, verb, target, content, note, visible=True):
    DAYS[day]["actions"].append({"id": id, "at": at, "verb": verb, "target": target, "content": content.strip("\n"),
                                 "visible_to_model": visible, "note": note})


def call(day, id, at, caller, purpose, turns):
    DAYS[day]["calls"].append({"id": id, "at": at, "caller": caller, "purpose": purpose,
                               "turns": [dict(speaker=s, text=t, **({"patience_s": p} if p else {})) for s, t, p in turns]})


# =============================================================== DAY 1 (Mon 11/2) items
email("e_teresa_q1", "D1 08:00", "c_teresa", ["c_lauren"], "Q1 status report + OFM questions this week", f"""
Hi Lauren,

Two things for this week, both due Friday:

1. FY27 Q1 Budget Status Report to Monica by Friday 3:00 so Nora can put it in the 11/9 ELT packet. Same format as the FY26 Q4 report (two pages, program table, issues). The HSRA burn rate is the headline; I want the projection to year end, not just the quarter, and I want it clear whether we're inside the M1 number we gave OFM.

2. Jordan told me at the budget officers' meeting he's sending follow-up questions on M1 and our reduction options today, due Friday noon. Draft the answers and let me see them before they go. Anything going to OFM comes through me.

Reminder that the September reconciliation isn't signed off yet. Denise says she'll have it by Thursday. Don't put numbers in front of Monica that Accounting hasn't tied out.

Thanks,
Teresa

{SIG['c_teresa']}
""", "t_q1report")

email("e_ofm_fyi", "D1 08:00", "c_ofm", ["c_teresa"], "Budget Division update: fall schedule for agency budget officers", """
Agency Budget Officers,

A reminder of the fall schedule. OFM budget advisors are reviewing 2027-29 biennial and 2027 supplemental requests and will contact agencies directly with questions. The November revenue forecast will be adopted later this month; OFM will tell agencies if maintenance level updates are needed after it. The Governor's proposed 2027-29 and 2027 supplemental budgets will be released in December.

No action is required in response to this message.

OFM Budget Division
Office of Financial Management
""", "t_ofm_fyi", cc=["c_lauren", "c_marcus"])

email("e_denise_fm15", "D1 08:05", "c_denise", ["c_lauren", "c_marcus"], "FM15 closed - September ER reports available", f"""
Morning budget folks,

AFRS fiscal month 15 (September) closed Friday night. ER standard reports are refreshed. The 10/12 run you've been working from should match except for anything we key in FM16 with September service dates. I'm going through the grantee invoice log this week and will flag anything that belongs in September for your quarterly.

Target for the September reconciliation sign-off is Thursday noon.

Denise

{SIG['c_denise']}
""", "t_recon")

event("cal_budget_team", "D1 08:00", "c_teresa", "Budget Office weekly", "Standing agenda: OFM asks, Q1 report, fiscal notes, Workday.",
      "D1 09:30", "D1 10:00", "Teams", ["c_teresa", "c_lauren", "c_marcus"])

chat("chat_marcus1", "D1 08:20", "c_marcus", ["c_lauren"], "morning! Teresa says Jordan's sending questions on M1 today. Also are you going to the Workday budget structure workshop Wed?", "t_marcus_chat")

email("e_jordan_q", "D1 09:10", "c_jordan", ["c_lauren"], "OHS 2027 Supplemental - follow-up questions on M1 and FTEs (responses by Fri 11/6 noon)", f"""
Lauren,

Thanks for the M1 package. To get it through review I need the following by noon Friday, November 6. Short answers with numbers are best.

1. Households and average assistance. Please give HSRA households assisted and average assistance per household by month for July-September 2026, against the FY26 monthly average, and say how much of the growth is more households versus higher assistance per household.

2. Fit with the supplemental instructions. The June 30 supplemental memo limits requests to legally mandated caseload, workload or other legally required changes and technical corrections. HSRA is not an entitlement. Please explain why the shortfall can't be managed within the appropriation (for example by managing intake) and what OHS would do if M1 is not funded.

3. Landlord mitigation proviso. What is your projected FY27 lapse on the $1,800,000 proviso in Program 040?

4. FTEs. Filled FTEs against the {FTE_BUDGET} allotted as of November 1, and your estimate of FY27 vacancy savings by fund.

If anything in M1 has changed since you released it, tell me in the response rather than changing the package; I'll let you know if I need a revised DP.

Thanks,
Jordan

{SIG['c_jordan']}
""", "t_ofm_q")

email("e_sharon_dp", "D1 10:15", "c_sharon", ["c_lauren"], "New DP for eviction filings?", f"""
Lauren,

Court filings for unlawful detainer are up again in Pierce and Spokane. I'd like to add a new policy package to the supplemental for a $2M eviction defense "surge" pilot with our grantees, separate from M1. Can we still get that in? Ben says the sponsor of the relocation bill would support it.

Sharon

{SIG['c_sharon']}
""", "t_sharon_dp")

email("e_kevin_delay", "D1 10:40", "c_kevin", ["c_lauren"], "ESG subgrant start dates moving to 1/1", f"""
Hi Lauren,

FYI three of the new FY2025 ESG subgrants won't start until January 1 instead of October 1. The counties needed more time on their environmental reviews. Contracts are being amended now.

""" + "\n".join(f"- {n}: {m(a, False)}" for n, a in ESG_DELAYED) + f"""
Total {m(ESG_DELAYED_TOTAL, False)}. The contract end dates stay at 6/30/2027 so the full amounts still go out this fiscal year, just compressed into six months instead of nine.

Kevin

{SIG['c_kevin']}
""", "t_esg_delay")

email("e_hr_openenroll", "D1 11:00", "c_hr", ["c_lauren"], "PEBB open enrollment is open through November 30", """
All staff,

PEBB annual open enrollment runs through November 30. Changes take effect January 1. If you don't need to change anything, you don't need to do anything. Benefits 24/7 has the details. Questions: hr@ohs.wa.gov.

OHS Human Resources
""", "t_hr_oe")

chat("chat_owen1", "D1 11:30", "c_owen", ["c_lauren"], "heads up - Ben says there's a bill draft on tenant relocation assistance going around (Rep. Dominguez). we might get a fiscal note request this week. want me to start numbers?", "t_owen_chat")

email("e_workday_wkshp", "D1 12:00", "c_kim", ["c_lauren", "c_marcus"], "Workday Phase 1A: budget structure workshop Wed 11/4 1:00", f"""
Hello OHS team,

You're invited to the Phase 1A budget structure workshop for agencies in wave 2. We'll walk through how AFRS program index and appropriation index codes map to Workday worktags (Fund, Cost Center, Program, Grant), and what the agency crosswalk template needs. The crosswalk itself is due November 20.

Please bring your current program index list.

Kim Sato
Finance Deployment Lead, One Washington
Office of Financial Management
""", "t_workday")

event("cal_workday", "D1 12:00", "c_kim", "Workday Phase 1A budget structure workshop (wave 2 agencies)", "Bring your program index list.",
      "D3 13:00", "D3 14:30", "Teams", ["c_lauren", "c_marcus"], thread="t_workday")

email("e_gfoa", "D1 13:00", "c_gfoa", ["c_lauren"], "GFOA Weekly: budget monitoring in a tight year", """
This week from GFOA:
- Best practice spotlight: budget monitoring. Go beyond identifying deviations from budget to explaining why they happened, and compare against prior-year actuals and forecasts, not just the current budget.
- Webinar: Building scalable reduction options (Nov 12).
- New research: state and local hiring trends after the 2025 freezes.

Government Finance Officers Association
""", "t_gfoa")

email("e_rosa_q", "D1 13:30", "c_rosa", ["c_lauren"], "Budget revision question - Lewis-Mason ESG subgrant", """
Hello Lauren,

Our ESG subgrant (rapid rehousing and shelter) has $12,000 left in the shelter operations line that we won't need because our new building came in under on utilities. Can we move it to rapid rehousing rental assistance? Do we need a formal amendment or can we just report it on the next A-19?

Thank you,
Rosa Delgado
Finance Manager
Lewis-Mason Shelter Network
""", "t_rosa")

chat("chat_teresa1", "D1 14:10", "c_teresa", ["c_lauren"], "also pull the Q1 proviso numbers for 040 - Jordan asked informally last month, and he's going to ask again", "t_teresa_chat")

email("e_denise_coding", "D1 14:45", "c_denise", ["c_lauren"], "Coding question - interpreter invoice $3,180", f"""
Lauren,

We have a $3,180.00 invoice from Puget Language Access for Spanish and Russian interpretation at HSRA applicant review hearings in October. It came in coded to Program 010. Should it be 020? Need to know before I key it.

Denise

{SIG['c_denise']}
""", "t_coding")

email("e_nora_cfd", "D1 15:20", "c_nora", ["c_lauren"], "Combined Fund Drive bake sale Thursday", """
Hi all,

The Combined Fund Drive bake sale is Thursday 11:30-1:00 in the 2nd floor break room. Cash, Venmo or payroll deduction pledges welcome.

Nora
""", "t_cfd")

chat("chat_marcus2", "D1 16:05", "c_marcus", ["c_lauren"], "for the Workday crosswalk can you send me the program index codes you use for 020/030/040? I only have 010 and capital", "t_marcus_chat")

email("e_watech", "D1 16:30", "c_watech", ["c_lauren"], "Planned maintenance: Enterprise Reporting unavailable Sat 11/7 6am-2pm", """
Enterprise Reporting (ER) will be unavailable Saturday, November 7, 6:00 a.m. to 2:00 p.m. for database maintenance. AFRS is not affected.

WaTech Service Desk
""", "t_watech")

# =============================================================== DAY 1 actions
act(1, "a1_01", "D1 09:02", "read", "e_teresa_q1", "", "Sets up the week: Q1 report Friday 3:00, OFM answers Friday noon, nothing to Monica before Accounting ties out September.")
act(1, "a1_02", "D1 09:10", "reply", "chat_marcus1", "Morning! Yes, saw Teresa's note. And yes I'll be at the Workday thing Wed.", "Light chat.")
act(1, "a1_03", "D1 10:05", "read", "e_jordan_q", "", "Reads OFM's four questions after the 9:30 team meeting.")
act(1, "a1_04", "D1 10:20", "reply", "e_jordan_q", f"""
Hi Jordan,

Got it, thanks. You'll have responses to all four by noon Friday. We are seeing higher Q1 HSRA spending than the July-August data in M1 assumed, so expect an updated projection in the response to question 1 and 2.

Lauren

{SIG['c_lauren']}
""", "Acknowledges; flags that the projection has moved without changing M1 (which OFM said not to do).")
act(1, "a1_05", "D1 10:50", "read", "e_sharon_dp", "", "Knows the supplemental instructions do not allow new policy items; decides to answer tomorrow after checking the memo wording.")
act(1, "a1_06", "D1 11:15", "read", "e_kevin_delay", "", "Notes the ESG timing change; will deal with the allotment later (Q7 is due 1/25). Never gets to it this week.")
act(1, "a1_07", "D1 11:40", "reply", "chat_owen1", "Thanks Owen. Don't start yet - requests come through FNS from OFM with the actual draft and a due date. If we get it I'll send you the sections that hit 020 and ask for workload numbers (applications, processing time, average payment). Please use the FY27 cost model in the Fiscal Notes folder, not the 2025 one.", "Sets up the fiscal note process and points Owen at the current cost model (he ignores it).")
act(1, "a1_08", "D1 13:45", "forward", "e_rosa_q", f"""
Kevin, Hoang - Lewis-Mason wants to move $12,000 from shelter operations to rapid rehousing assistance in their ESG subgrant. Both are ESG components, but it changes their approved budget and may affect our 60% cap on shelter and outreach. Can you two decide whether this needs a contract amendment and answer Rosa directly? I've told her you'll follow up.

Lauren
""", "Routes a subrecipient budget revision to the grant manager and compliance; not the budget analyst's call.")
act(1, "a1_08b", "D1 13:50", "reply", "e_rosa_q", """
Hi Rosa,

Thanks for asking before moving it. Because it changes your approved subgrant budget, Kevin O'Brien (program) and Hoang Tran (grants compliance) will confirm whether it needs an amendment. Please hold off reporting it on the A-19 until you hear from them.

Lauren Whitaker
Budget Analyst, Office of Housing Stability
""", "Holds the subrecipient until the right people answer.")
act(1, "a1_09", "D1 14:20", "reply", "chat_teresa1", "Will do - I'll have the 040 proviso actuals and a projected lapse in the Q1 report and in the answer to Jordan's question 3.", "")
act(1, "a1_10", "D1 15:05", "reply", "e_denise_coding", f"""
Denise - yes, 020. Interpretation at applicant review hearings is an HSRA program cost. Please use the 020 program index (2010, HSRA operations), object E, sub-object EZ. Thanks for catching it.

Lauren
""", "Routine coding call within the analyst's authority.")
act(1, "a1_11", "D1 15:45", "edit_doc", "d_q1_actuals", "Added a 'projected year end at Q1 pace' column to Sheet 1 and highlighted 020 GF-S (Q1 variance -$573,542.05 as posted). Left a note: 'waiting on Denise for FM16 items with September service dates.'", "Starts the variance workbook; the posted numbers are not final.")
act(1, "a1_12", "D1 16:20", "reply", "chat_marcus2", "020 = 2010 (HSRA ops), 2020 (HSRA grants); 030 = 3010 (shelter ops), 3020 (shelter grants GF-S/HSA), 3050 (ESG federal); 040 = 4010 (navigation), 4030 (landlord mitigation proviso). Appropriation index is by fund: 011/012 GF-S FY26/FY27, 0F1 GF-F, 26H HSA.", "Gives the codes Marcus needs for the crosswalk.")
act(1, "a1_13", "D1 16:40", "schedule", "cal_workday", "Accepted: Workday Phase 1A budget structure workshop, Wed 11/4 1:00-2:30.", "")
