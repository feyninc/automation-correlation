from part2_d1d2 import *

PRELIM_ADJ = ROWS[2][5] + ACCRUAL
PRELIM_PROJ = PRELIM_ADJ * 4
PRELIM_GAP = PRELIM_PROJ - ROWS[2][3]

# =============================================================== DAY 2 (Tue 11/3) items
email("e_fns_request", "D2 08:00", "c_fns", ["c_lauren", "c_ben"], "FNS: Fiscal note request 27-0142, H-0287.1/27 - due 11/05/2026 12:00 PM", """
A fiscal note has been requested. Your agency has been assigned.

Request #: 27-0142
Bill/draft: H-0287.1/27 (tenant relocation assistance)
Requested by: Alicia Brandt, House Appropriations Committee staff, at the request of Rep. Carla Dominguez
Lead agency: Office of Housing Stability (OHS)
Also assigned: Department of Commerce, Local Government Fiscal Note Program
OFM analyst: Jordan Kessler
Due to OFM: 11/05/2026 12:00 PM
Hearing: none scheduled (interim); the sponsor intends to pre-file in December.
Special instructions: Include assumptions for the number of displaced households and for the toll-free line. Lead agency please record shared assumptions on the Request tab.

The draft language is attached and available in FNS.

This is an automated message from the OFM Fiscal Note System.
""", "t_fn", att=["d_bill_h0287"])

doc("d_bill_h0287", "D2 08:00", "H-0287.1/27 bill draft - tenant relocation assistance.pdf", """
BILL REQUEST - CODE REVISER'S OFFICE
BILL REQ. #: H-0287.1/27
BRIEF DESCRIPTION: Providing relocation assistance to tenants displaced when a dwelling is condemned or declared unlawful to occupy.

AN ACT Relating to relocation assistance for tenants displaced when a dwelling is condemned or declared unlawful to occupy; adding a new chapter to Title 43 RCW; and creating a new account.

BE IT ENACTED BY THE LEGISLATURE OF THE STATE OF WASHINGTON:

NEW SECTION. Sec. 1. The legislature finds that tenants who must leave their homes on short notice because a local government has condemned the building or declared it unlawful to occupy often receive no relocation help, and that a statewide safety net is needed while landlords are held responsible.

NEW SECTION. Sec. 2. The definitions in this section apply throughout this chapter. (1) "Office" means the office of housing stability. (2) "Displaced household" means a tenant household required to vacate a dwelling unit because a local government has condemned the unit or declared it unlawful to occupy. (3) "Director" means the director of the office.

NEW SECTION. Sec. 3. (1) Subject to the availability of amounts appropriated for this specific purpose, the office shall establish and administer the tenant relocation assistance program. (2) The office shall pay each eligible displaced household relocation assistance of up to two thousand dollars, based on documented moving, deposit and temporary lodging costs. (3) A household must apply within ninety days of the date it was required to vacate. (4) Beginning January 1, 2028, the office shall accept applications.

NEW SECTION. Sec. 4. The office may contract with a statewide information and referral provider to operate a toll-free line that tells displaced households how to apply.

NEW SECTION. Sec. 5. The office may seek reimbursement from the landlord of a dwelling for assistance paid to its tenants under section 3 of this act. Amounts recovered must be deposited in the tenant relocation assistance account.

NEW SECTION. Sec. 6. The tenant relocation assistance account is created in the custody of the state treasurer. Only the director or the director's designee may authorize expenditures from the account. The account is subject to allotment procedures under chapter 43.88 RCW, but an appropriation is not required for expenditures. Expenditures may be used only for assistance under section 3 of this act.

NEW SECTION. Sec. 7. The office shall adopt rules to implement this chapter.

NEW SECTION. Sec. 8. By December 1, 2028, and annually thereafter, the office shall report to the appropriate committees of the legislature the number of households assisted, the amounts paid and the amounts recovered.

NEW SECTION. Sec. 9. Sections 1 through 8 of this act constitute a new chapter in Title 43 RCW.

--- END ---
""", thread="t_fn", meta={"format": "pdf"})

email("e_ben_fn", "D2 08:30", "c_ben", ["c_lauren"], "Relocation bill FN", f"""
Lauren,

You'll have seen the FNS request on H-0287.1. Rep. Dominguez's office is keen - she wants to pre-file and talk about it at the housing caucus. Her LA Tyler Nguyen may reach out to you directly; he's friendly. We're neutral on the bill for now, so the note just needs to be straight.

Ben

{SIG['c_ben']}
""", "t_fn")

email("e_jordan_fn", "D2 08:40", "c_jordan", ["c_lauren"], "H-0287.1 - OFM analyst", f"""
Lauren,

I'm the OFM analyst on 27-0142. A few things so we don't go back and forth:
- Effective date would be 90 days after the 2027 session adjourns, so late July 2027; Sec. 3(4) holds applications until 1/1/2028. Please prorate staff from realistic hire dates.
- Sec. 4 lets you contract the phone line; price the least expensive reasonable option.
- The landlord recovery revenue in Sec. 5 is probably indeterminate; say why.
- If House staff want to see numbers before Thursday, send a DRAFT to me and I'll coordinate. Nothing goes to the sponsor's office from the agency.

Thanks,
Jordan

{SIG['c_jordan']}
""", "t_fn")

chat("chat_teresa2", "D2 09:15", "c_teresa", ["c_lauren"], "FN request on the relocation draft - you're lead, Jordan's the OFM analyst. Get me the number by Wed afternoon so I can look before it goes Thursday.", "t_teresa_chat")

email("e_hoang_rosa", "D2 09:40", "c_hoang", ["c_lauren", "c_kevin"], "RE: Budget revision question - Lewis-Mason ESG subgrant", f"""
Lauren, Kevin -

Shelter to rapid rehousing is a move between ESG components, so it needs a written subgrant amendment, not just an A-19 line. It's small and it doesn't push us over the 60 percent shelter/outreach cap. Kevin, if you're fine with it I'll send Rosa the amendment form today.

Hoang

{SIG['c_hoang']}
""", "t_rosa")

email("e_denise_accrual", "D2 10:20", "c_denise", ["c_lauren"], "September HSRA invoices keyed in FM16", f"""
Lauren,

Going through the grantee invoice log I found three HSRA invoices with September service dates that were keyed in FM16 (October) because they came in after the FM15 cutoff:

""" + "\n".join(f"- {n}: {m(a)}" for n, a in ACCRUAL_PARTS) + f"""
Total {m(ACCRUAL)}, all 020 GF-S (001-1), object N.

FM15 is closed so I can't post them there. I'm booking an accrual JV in FM16 that references September; for your Q1 report please treat them as September expenditures. I'm still working through the rest of the log and the payroll tie-out; sign-off target is still Thursday noon.

Denise

{SIG['c_denise']}
""", "t_recon")

email("e_megan", "D2 11:45", "c_megan", ["c_lauren"], "Question on OHS budget - rental assistance cuts?", """
Hi Lauren,

I'm working on a story about the Governor's upcoming budget. I'm hearing OFM asked cabinet agencies for a second round of cuts last month, beyond what was submitted in September. Is OHS proposing to cut rental assistance? Can you tell me what's on your list and the dollar amounts? My deadline is Thursday.

Thanks so much,
Megan Holt
Cascade Public Ledger
206-555-0190
""", "t_media")

email("e_phish", "D2 12:10", "c_phish", ["c_lauren"], "ACTION REQUIRED: ABS/TALS access recertification (24 hours)", """
Dear Budget System User,

Your Agency Budget System (ABS) and TALS access is due for annual recertification. To avoid losing access during the budget review period, re-verify within 24 hours:

https://ofm-wa-gov.net/abs-recertify

Sign in with your SecureAccess Washington (SAW) username and password and confirm your MFA code.

OFM Budget Systems Support
""", "t_phish")

email("e_jenna_misaddr", "D2 13:15", "c_jenna", ["c_lauren"], "Kowalski timesheet review - summary for Thursday", """
Lauren,

Here's the summary for Thursday's pre-disciplinary meeting. Paul Kowalski (Program Specialist 3, Program 030) reported 46 hours of telework in September on days the VPN logs show no connection, and two days coded as sick leave while he was posting from a conference in Portland. His manager has not been told the details. Please keep this between us and the Labor Relations file until the meeting.

Jenna

Jenna Morales
HR Consultant | OHS Human Resources
""", "t_misaddr")

email("e_owen_input", "D2 14:00", "c_owen", ["c_lauren"], "H-0287.1 numbers from the program", f"""
Lauren,

Here's what we came up with for the relocation bill: {m(OW_TOTAL)} a year starting FY28. Breakdown attached. I used the rates from the Fiscal Notes folder. Sharon wants to see the number Wednesday so she can brief Robert.

Owen

Owen Fitzgerald
Program Manager, Housing Stability Rental Assistance | OHS
""", "t_fn", att=["d_owen_input"])

doc("d_owen_input", "D2 14:00", "H-0287.1 program estimate (Owen).xlsx", f"""
H-0287.1/27 tenant relocation assistance - Program 020 estimate (O. Fitzgerald, 11/3)
Assumes program starts July 1, 2027; same cost each year.

Item | FTE | FY28 cost
Management Analyst 5 (program manager) | 1.0 | {m(OLD_SAL['MA5'], False)}
Program Specialist 3 (applications) | 2.0 | {m(OLD_SAL['PS3'] * 2, False)}
Customer Service Specialist 2 (in-house toll-free line) | 2.0 | {m(OLD_SAL['CSS2'] * 2, False)}
Salaries subtotal | 5.0 | {m(OW_A, False)}
Benefits at {pct(OLD_BEN_PCT)}% | | {m(OW_B)}
Goods and services, 5 FTE x {m(OLD_GS_FTE, False)} | | $27,000
Equipment, 5 x $4,800 | | $24,000
Relocation payments, 650 households x $2,000 | | {m(OW_N, False)}
Total FY28 (and each year after) | 5.0 | {m(OW_TOTAL)}

Source for 650 households: local code enforcement offices told us about 650 displaced households a year statewide. Average documented relocation cost in our 2025 pilot was $1,850.
""", kind="sheet", thread="t_fn", meta={"format": "xlsx"})

email("e_marcus_wd", "D2 15:00", "c_marcus", ["c_lauren"], "Crosswalk template - first pass", """
Lauren,

Thanks for the codes. I put a first pass of the Workday crosswalk in the Workday folder: AFRS program index -> Workday Cost Center + Program worktag, appropriation index -> Fund. I left your programs' rows blank where I wasn't sure which ones are proviso-tracked. The workshop tomorrow should tell us whether provisos get their own Program worktag.

Marcus
""", "t_workday")

email("e_ofm_training", "D2 15:30", "c_ofm", ["c_lauren"], "Registration open: Fiscal Note System refresher (Nov 17 and Dec 2)", """
OFM is offering two 90-minute FNS refreshers for agency fiscal note preparers before the 2027 session: November 17 and December 2, 10:00-11:30, on Teams. Register through the OFM training page.

OFM Budget Division
""", "t_ofm_training")

chat("chat_owen2", "D2 16:10", "c_owen", ["c_lauren"], "did you get my sheet? Sharon wants the number tomorrow", "t_owen_chat")

email("e_kevin_thanks", "D2 16:35", "c_kevin", ["c_lauren", "c_hoang"], "RE: Budget revision question - Lewis-Mason ESG subgrant", """
Fine by me. Hoang, go ahead and send Rosa the amendment form. Thanks both.

K
""", "t_rosa")

# =============================================================== DAY 2 calls
call(2, "call_sharon", "D2 11:00", "c_sharon", "Sharon has heard from Denise about the September invoices and wants to know how bad HSRA spending is.", [
    ("caller", "Lauren, hi, it's Sharon. Denise says there are more September invoices. How bad is it?", 20),
    ("human", f"Hi Sharon. As posted, Q1 GF-S was {m(-P020_GFS_VAR_PRE, False)} over allotment. With Denise's {m(ACCRUAL, False)} it's about {m(-(ROWS[2][4] - PRELIM_ADJ), False)} over for the quarter, and she hasn't finished the tie-out. If we keep spending at that pace we'd end the year around $43.9 million against $38.4 million, so roughly $5.5 million short. That's more than the $3.9 million in M1.", None),
    ("caller", "Can't we just keep paying through March and get it fixed in the supplemental? The Legislature always backfills HSRA.", 25),
    ("human", "We can't plan on that. We can't spend past the appropriation (that's RCW 43.88.130), and OFM's instructions say the supplemental is only for mandated caseload and technical corrections. I'd like to bring Teresa real options, like capping intake at the FY26 level or capping assistance per household, with what each one saves. Could you get me intake by county for September and October by Wednesday?", None),
    ("caller", "Fine, I'll have Owen pull it. Is Owen also doing the relocation bill numbers?", 15),
    ("human", "He's sending program input. I'll check it against the FY27 cost model and own the note. It's due to OFM Thursday at noon.", None),
])

# =============================================================== DAY 2 actions
act(2, "a2_01", "D2 08:45", "read", "e_fns_request", "", "Fiscal note request arrives; due Thursday noon (OFM's usual 72 hours).")
act(2, "a2_02", "D2 09:05", "read", "d_bill_h0287", "", "Reads the whole draft first, as the OFM instructions say.")
act(2, "a2_03", "D2 09:20", "reply", "chat_teresa2", "On it. You'll have a draft by Wednesday 3:00. Jordan has already said to prorate from realistic hire dates and to cost the phone line as a contract if that's cheaper.", "")
act(2, "a2_04", "D2 09:35", "reply", "e_sharon_dp", f"""
Hi Sharon,

I checked the instructions. Unfortunately we can't add it to the supplemental:

- OFM's June 30 supplemental memo limits 2027 supplemental requests to legally mandated caseload, workload or other legally required changes, plus technical corrections to the enacted budget. A new $2M pilot is a policy-level expansion, and the June 5 memo tells agencies not to propose new programs this cycle.
- The 2027-29 instructions also say an agency may not amend its request after submittal without OFM's prior authorization. Our supplemental went in 9/30.

What we can do: the eviction filing data helps M1, since it shows demand is still rising. I'll use it in our answers to Jordan's questions this week. If the Rep. wants a pilot, that's a legislative decision she can pursue in the session; it would then come to us as a fiscal note.

Happy to talk it through.

Lauren

{SIG['c_lauren']}
""", "Interprets OFM's directives for a program director (task 3404). Done the day after it arrived.")
act(2, "a2_05", "D2 09:55", "reply", "e_ben_fn", f"""
Thanks Ben. I'm lead and Jordan Kessler is the OFM analyst. If Tyler reaches out I'll point him to OFM: the note goes to OFM through FNS Thursday and OFM distributes it. Any early look for House staff goes as a DRAFT through Jordan. Please send anything you hear about the sponsor's intent my way, since it may change the assumptions.

Lauren
""", "Sets the distribution rule before the pressure arrives.")
act(2, "a2_06", "D2 10:10", "forward", "e_fns_request", """
Owen - here's the request and the draft (H-0287.1). Sections 3, 4 and 5 hit your program. What I need from you by 2:00 today: (1) the estimated number of displaced households a year and where it comes from; (2) processing time per application; (3) the average documented relocation cost from the 2025 pilot. I'll build the cost estimate. Please use the FY27 cost model (updated 8/14), not the 2025 file.

Lauren
""", "Asks the program for workload drivers, not a finished estimate.")
act(2, "a2_07", "D2 10:35", "reply", "e_denise_accrual", f"""
Thanks Denise, that's exactly what I needed. I'll show the {m(ACCRUAL)} as September expenditures in the Q1 report, as a reconciling item against the posted ER numbers, and I'll wait for your Thursday sign-off before anything goes to Monica.

Lauren
""", "Waits for the reconciliation, per Teresa and the Budget Office rule.")
act(2, "a2_08", "D2 12:00", "forward", "e_megan", """
Elena - media inquiry below from Megan Holt (Cascade Public Ledger) about possible reductions, deadline Thursday. I haven't responded and won't. Flagging that she is asking about a second round of OFM cuts, which is pre-decisional. Teresa is cc'd.

Lauren
""", "Media goes to Communications; no budget numbers. (cc Teresa in content.)")
act(2, "a2_09", "D2 12:20", "forward", "e_phish", """
Darnell - this looks like phishing. The sender domain is ofm-wa-gov.net, not ofm.wa.gov, and it asks for SAW credentials. I didn't click. Forwarding as an attachment for the security team.

Lauren
""", "Reports the phish to the agency security contact.")
act(2, "a2_10", "D2 13:25", "reply", "e_jenna_misaddr", """
Hi Jenna, I think this was meant for Lauren Whitman in Labor Relations. I haven't read past the first line or shared it, and I've deleted it from my mailbox.

Lauren
""", "Misaddressed HR personnel matter: notify sender, don't forward.")
act(2, "a2_11", "D2 14:30", "read", "e_owen_input", "", "Sees $1.76M and the 31.2% benefits rate; knows the program used the superseded model.")
act(2, "a2_12", "D2 15:15", "create_doc", "e_fns_request", """
Created 'H-0287.1 fiscal note working file.xlsx' in the Fiscal Notes folder with three tabs:
Assumptions - effective late July 2027; applications from 1/1/2028; 650 displaced households a year (local code enforcement survey, per program); average payment $1,850 (2025 pilot), cap $2,000; recovery revenue indeterminate.
Staffing - to be built from the FY27 cost model.
Hotline - contract vs in-house comparison (to do).
""", "Starts the note; the numbers come Wednesday.")
act(2, "a2_13", "D2 16:20", "reply", "chat_owen2", "Got it, thanks. At first look it uses the 2025 rates and starts everything July 1, so FY28 will come down a lot. Please don't send it to Sharon as the number. I'll have a reviewed estimate tomorrow morning.", "Stops a wrong number from travelling up the chain.")
