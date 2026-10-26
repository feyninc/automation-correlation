"""Part 3: the scripted human (actions) and calls."""
from build_nums import *  # noqa: F401,F403

SIG = "Elena Brandt, CPA\nSenior Accountant | Westerby Fluid Systems, Inc.\n4100 Southpark Blvd, Grove City, OH 43123 | (614) 555-0142"


def A(id, at, verb, target, content, note, to=None, cc=None, visible=True):
    a = {"id": id, "at": at, "verb": verb, "target": target, "content": content.strip("\n"),
         "visible_to_model": visible, "note": note}
    if to is not None:
        a["to"] = to
    if cc is not None:
        a["cc"] = cc
    return a


D1 = [
    A("d1_01", "D1 08:50", "read", "itm_pbc", "Opened Hannah's PBC email and the attached request list.", "Reads; acts later in the morning."),
    A("d1_02", "D1 09:00", "read", "cal_kickoff", "Attended the 15-minute close kickoff.", "Routine stand-up."),
    A("d1_03", "D1 09:20", "reply", "itm_jake_recs", """
Yes, 4471 is mine. Please do book the analysis fee once you see it, it's $1,245.00 per the analysis notice (debited 10/30). I'll send you anything else I find on the bank side.
""", "Delegates the cash JE to the staff accountant who owns cash JEs.", to=["c_jake"]),
    A("d1_04", "D1 09:45", "read", "itm_analysis", "Opened the account analysis notice; downloaded the analysis statement to the rec folder.", "Gathers the fee support."),
    A("d1_05", "D1 10:30", "reply", "itm_greg_ostrander", f"""
Hi Greg,

Thanks for the heads-up. I want to get this right for you, and because the units are still in our building it isn't a normal shipment: under our revenue policy (ASC 606 bill-and-hold), we can only book it in October if all of these were true at 10/31:

1. Ostrander asked us in writing to hold the units (their request, with a reason);
2. the units were identified separately as Ostrander's (tagged/segregated, not general stock);
3. they were complete and ready to ship; and
4. we couldn't use them or send them to another customer.

Dana has to approve any bill-and-hold before we post it. If you can get me Ostrander's written request, I'll check the rest with Doug today and write it up for her.

Thanks,
{SIG}
""", "Explains criteria, does not promise October, routes the decision to the Controller.", to=["c_greg"]),
    A("d1_06", "D1 11:05", "reply", "itm_ashwood", "Thanks Andre. 48295 is on my outstanding list at $54,880.00, so we're consistent.", "Background traffic.", to=["c_andre"]),
    A("d1_07", "D1 11:15", "reply", "itm_pbc", f"""
Hi Hannah,

Got it, thanks. The dates work. Owners on our side:

1.1 Sept bank recs - me (all four accounts)
1.2 AR aging 9/30 - Monique Baptiste, I'll tie it to the GL before upload
1.3 FA additions over $25K - Priya Natarajan
1.4 Sept 30 TB - me
2.1 Payroll register 9/18 - Sheila Kurtz (Payroll); it will come through Suralink only
2.2 Manual JE listing - me
2.3 Accrued liabilities 9/30 - me
2.4 Credit agreement amendments / Q3 compliance certificate - Dana Whitlock
2.5 Bank confirmation authorization - Dana
2.6 Attorney list - Dana
3.1 Q3 cycle counts - Doug Franzen with Priya

I'll aim to have 1.1-1.4 in Suralink by Friday morning.

Thanks,
{SIG}
""", "Acknowledges and assigns owners; 2+ hours after arrival.", to=["c_hannah"], cc=["c_tyler"]),
    A("d1_08", "D1 11:30", "edit_doc", "doc_pbc_list", """
Filled in the Client owner column: 1.1 E. Brandt; 1.2 M. Baptiste (EB ties to GL); 1.3 P. Natarajan; 1.4 E. Brandt; 2.1 S. Kurtz (Suralink only, masked SSNs if KM agrees); 2.2 E. Brandt; 2.3 E. Brandt; 2.4 D. Whitlock; 2.5 D. Whitlock; 2.6 D. Whitlock; 3.1 D. Franzen / P. Natarajan; 3.2 E. Brandt (BOLs and PODs). Status of all: Open.
""", "Turns the list into an internal tracker."),
    A("d1_09", "D1 13:30", "edit_doc", "doc_bank_rec_oct", f"""
Adjusted bank balance | {m(ADJ_BANK)}
Balance per GL 1010 | {m(G1)}
Unreconciled difference (GL over adjusted bank) | {m(DIFF)}
Identified so far:
  1. Account analysis charge debited by bank 10/30, not recorded in GL | {m(FEE)} (Jake to book; support: analysis statement)
  2. Merchant fees: bank 10/05 FISERV 4,650.00 vs GL JE-10-0107 4,560.00 (transposition) | 90.00
  3. Unexplained: ACH/wire receipts 10/30, GL bank-file import 14 items 203,551.10 vs bank 13 items 185,121.10 | 18,430.00 (investigating - one extra receipt in GL)
Total | {m(DIFF)}
""", "Finds the full difference and two of three items on day 1; the third needs AR evidence."),
    A("d1_10", "D1 14:00", "send", None, """
Jake, two for your cash JE: (1) analysis fee $1,245.00, Dr 6810 bank fees / Cr 1010, dated 10/30; (2) JE-10-0107 merchant fees was keyed at 4,560.00, bank shows 4,650.00 on 10/05, so another $90.00 to 6815. Please submit both to me.
""", "Gives the staff accountant the corrections; she will approve his entry (under $50,000, his preparation).", to=["c_jake"]),
    A("d1_11", "D1 14:40", "reply", "itm_ben_revenue", """
Not yet, sorry - I don't have a number I'd stand behind until the cutoff review Wednesday, and Dana reviews before anything goes in the deck. I'll ping you Wednesday afternoon. Keep in mind September had the ~$540K Brennan/Halvorsen stocking orders, so October will be lower.
""", "Declines to give an unreviewed number; gives context only.", to=["c_ben"]),
    A("d1_12", "D1 15:45", "reply", "itm_jake_plug", """
Thanks, but no - please don't put anything in 1999. Policy is we never plug a rec, and any write-off needs Dana. I've got $1,245 + $90 explained and $18,430 is a single extra receipt on 10/30 that I'm tracing. I'll leave it as an open reconciling item with notes; WD3 is the deadline, not today.
""", "Refuses the plug; matches policy 2.2.", to=["c_jake"]),
    A("d1_13", "D1 16:40", "reply", "itm_tom_cover", "Thanks Tom. You'll have my payroll accrual tomorrow and the accrued expenses JE Wednesday.", "Background.", to=["c_tom"]),
]

D2 = [
    A("d2_01", "D2 08:40", "read", "itm_monique_stmts", "Read Monique's note on statements.", "Background."),
    A("d2_02", "D2 09:20", "reply", "itm_priya_prepaid", f"""
Hi Priya - schedule looks good except one line: Salesforce ended 9/30 and wasn't renewed (CRM moved to NetSuite), so it shouldn't amortize in October; its balance goes to -2,500.00, which is the giveaway. October amortization should be {m(PRE_AMORT_OK)}, not {m(PRE_AMORT_PRIYA)} (software 11,500.00 instead of 14,000.00). I've rejected JE-10-0398; please drop the line, check the 1410 balance ties at 10/31, and resubmit. Also: FloQast ends 10/31, so add the renewal if Dana signed it.
""", "Reviewer's catch, a day after it was ready.", to=["c_priya"]),
    A("d2_03", "D2 09:40", "read", "itm_andre_northfield", "Opened the Northfield invoice from Andre.", "Defers; handles it in the Wednesday accrual JE."),
    A("d2_04", "D2 10:30", "forward", "itm_phish", """
Nate, Lorraine - reporting this one (I also hit Report Phishing). The sender domain is kestrelsteel-supply.com; Kestrel in our vendor master is kestrelsteel.com, and the letter asks us to confirm by email and says their phones are forwarded. Lorraine, could you call Janet Moss at the number already in the vendor master to confirm when you're back tomorrow? Nobody has changed anything, and KS-88213 should stay on the existing account unless you verify otherwise.
""", "Correct handling: report, callback via vendor master by the AP Lead, no change.", to=["c_nate", "c_lorraine"], cc=["c_andre"]),
    A("d2_05", "D2 10:35", "reply", "itm_andre_kestrel", """
Please don't change anything. It's from a lookalike domain - looks like a fraud attempt. I've reported it to Nate and Lorraine; Lorraine will call Kestrel at the number on file tomorrow. Leave KS-88213 in the run to the current account, and don't reply to that email.
""", "Stops the AP specialist; neither she nor Andre may change bank details.", to=["c_andre"]),
    A("d2_06", "D2 11:50", "read", "itm_doug_billhold", "Read Doug's answers on the Ostrander units.", "Facts for the memo."),
    A("d2_07", "D2 13:00", "edit_doc", "doc_accrual_wp_oct", f"""
Payroll accrual | 2120 | {m(PAY_ACCR)} | JE-10-0405 submitted to T. Iverson
  Basis: 10/30 pay gross {m(GROSS)} (10/11-10/24) x 5/10 workdays (10/26-10/30) = {m(PAY_ACCR_WAGES)}; employer FICA 7.65% = {m(PAY_ACCR_TAX)}. Q3 safety bonus already accrued in September (JE-09-0384), not repeated.
""", "Books the payroll accrual a day after the inputs arrived."),
    A("d2_08", "D2 13:35", "forward", "itm_misaddressed", """
Elena B. - I think this was meant for you (autocomplete got me). Rick, forwarding to Elena Brandon in inside sales.
""", "Correct handling of a misaddressed email: forward to the intended person, do not quote.", to=["c_ebrandon"], cc=["c_rick"]),
    A("d2_09", "D2 14:00", "read", "cal_1on1", "1:1 with Dana: walked her through the $19,765 difference and the Ostrander question; she asked for a written memo today.", "Prompts the memo."),
    A("d2_10", "D2 14:30", "reply", "itm_andre_coding", """
Hi Andre,

1. Brightline BOI-55102, $38,400.00: capitalize, 1610 Furniture & fixtures, asset in service 10/22 (inside sales area). Priya will set up the asset.
2. Corvane CTG-30988, $14,950.00 incl. tax: capitalize, 1620 Computer equipment.
3. Allied 77104, $1,180.00: expense, 6420 Repairs & maintenance (repair, no life extension).

All three are October expenses/assets; since AP is locked, enter them with November posting and reference them in my accrual review.

Thanks!
""", "Codes the invoices; does NOT pick up Ohio use tax on Brightline (missed; need n10).", to=["c_andre"]),
    A("d2_11", "D2 15:30", "read", "itm_monique_aging", "Skimmed the AR aging; no action.", "Does not notice the Hartline credit here."),
    A("d2_12", "D2 16:00", "send", None, f"""
Subject: Ostrander SO 7781 - bill-and-hold analysis (October)

Dana,

Greg has asked that the Ostrander order (SO 7781, 36 cylinder assemblies, $212,400.00) be invoiced and recognized in October. The units are complete and in our bay 4; Ostrander wants delivery mid-December. Under ASC 606-10-55-83 all four criteria must be met at 10/31, plus control under 606-10-25-30:

(a) Substantive reason / customer request - Ostrander's Lima expansion is late, but we have nothing in writing from Ostrander (Greg's conversations only). Not documented.
(b) Identified separately as Ostrander's - No. Per Doug, staged with the SO on the pick ticket, not tagged or segregated.
(c) Ready for physical transfer - Yes. Passed pressure test 10/29, crated.
(d) Cannot use or redirect to another customer - Not met for 12 of 36: those are standard WC-3000s Doug says could go to Brennan. The 24 custom units are Ostrander-specific (4.5" bore, Ostrander mounting and paint).

Conclusion: criteria (a), (b) and (d) were not met at 10/31; my recommendation is no October revenue, and to reassess in November if Ostrander sends a signed hold request and we segregate the units. If it is recognized later, a portion of the price may need to go to the custodial service (606-10-55-84).

This is your call; I haven't told Greg anything beyond what's needed.

{SIG}
""", "The memo the Controller asked for; recommends, does not decide.", to=["c_dana"]),
    A("d2_13", "D2 16:40", "reply", "itm_doug_shiplog", "Thanks Doug, this is perfect. I'll do the cutoff tomorrow.", "Defers cutoff to WD3.", to=["c_doug"]),
]

D3 = [
    A("d3_01", "D3 08:35", "reply", "itm_tom_jakerec", "It's in Jake's cash JE JE-10-0402 (posted 11/2, Cr 7110 interest income $4,212.18); the FloQast balance was pulled before it posted. Refresh and it ties.", "Background review question.", to=["c_tom"]),
    A("d3_02", "D3 09:50", "reply", "itm_sheila_register", """
Thanks Sheila. The PBC list says last-four is fine, so please rerun it masked and I'll upload that version to Suralink (request 2.1). I'm deleting the full-SSN file from my downloads.
""", "Keeps PII out of email; uses the masked version the PBC allows.", to=["c_sheila"]),
    A("d3_03", "D3 10:00", "edit_doc", "doc_accrual_wp_oct", f"""
Freight (Gantry unbilled, estimate 11/03) | 2110 | 34,180.00
Utilities (3-month average) | 2110 | 18,600.00
Services received not invoiced >= $10,000: Northfield NMS-20417, PM shutdown 10/19-10/23 | 2110 | 27,300.00
JE-10-0412 accrued expenses total | {m(ACCR_T)} | auto-reverse 11/01 (draft)
""", "Builds the accrued expenses JE incl. the Northfield invoice from Tuesday."),
    A("d3_04", "D3 10:15", "reply", "itm_andre_northfield", "Yes - it's October service, so I'm accruing the $27,300.00 in October (JE-10-0412). Enter the invoice with November posting; the accrual reverses 11/1, so it nets out.", "Answers Andre a day later.", to=["c_andre"]),
    A("d3_05", "D3 10:40", "send", None, """
Subject: Positive pay - check 48266 returned (altered payee)

Lorraine, Andre, Dana - Lattimore called at 10:20: check 48266 ($9,812.40, issued 10/27 to Midstate Packaging Corp.) was presented with payee "M. Stayton Services LLC". I returned it (PX-110426-0193) and asked the bank to place a stop. Lorraine, could you confirm with Midstate at the number in the vendor master that they didn't receive it, then void and reissue by ACH to their existing account? It's still on the October outstanding list, so no change to the 10/31 rec. We should also look at how the 10/27 check run left the building.
""", "Follows up the call; vendor contact via master data.", to=["c_lorraine", "c_andre", "c_dana"]),
    A("d3_06", "D3 11:10", "read", "itm_monique_hartline", "Read Monique's chat about Hartline's credit; did not reply (in the middle of the accrual JE).", "Misses the connection until Thursday morning."),
    A("d3_07", "D3 11:55", "reply", "itm_lorraine_kestrel", "Thank you Lorraine and Nate.", "Closes the loop.", to=["c_lorraine"]),
    A("d3_08", "D3 12:40", "forward", "itm_greg_text", """
Dana - FYI, Greg sent this (text from Ostrander's buyer last night, 11/3). It's after period end and still doesn't cover (b) or (d) from my memo. No change to my recommendation.
""", "Keeps the Controller informed; does not reply to Greg with a decision.", to=["c_dana"]),
    A("d3_09", "D3 14:00", "edit_doc", "doc_ship_log", f"""
Cutoff conclusion (E. Brandt 11/04): three FOB Destination shipments were delivered in November, so control had not transferred at 10/31: 10611 Ridgeway 46,180.00 (POD 11/02), 10614 Carver 22,905.50 (POD 11/03), 10619 Tri-State 11,734.25 (POD 11/02). JE-10-0416: Dr 4000 Net sales {m(CUT_REV)} / Cr 1200 AR {m(CUT_REV)}; Dr 1300 Inventory (in transit) {m(CUT_COST)} / Cr 5000 COGS {m(CUT_COST)}; reverses 11/01 so the invoices recognize in November. All three exempt, no sales tax effect. FOB Shipping Point items and the Erie stock transfer: no adjustment.
""", "Does the cutoff a day after the log arrived."),
    A("d3_10", "D3 14:50", "reply", "itm_jake_0419", "Approved JE-10-0419 ($1,335.00). Thanks for the clean support.", "Approves a staff entry under $50,000 - allowed.", to=["c_jake"]),
    A("d3_11", "D3 15:00", "read", "cal_recreview", "Rec review with Dana and Tom: walked through $1,335.00 booked, $18,430.00 still open on 10/30 receipts.", "Status."),
    A("d3_12", "D3 15:20", "reply", "itm_tyler_register", f"""
Hi Tyler,

Thanks - the 9/18 register is in Suralink under request 2.1 (SSNs masked to the last four, per the request list). Our policy doesn't allow payroll data by email, so please pull it from there; if the portal is still timing out, Hannah may be able to help. I'll include created-by and approved-by on the JE listing for 2.2.

Thanks,
{SIG}
""", "Declines emailing PII; uses the portal.", to=["c_tyler"], cc=["c_hannah"]),
    A("d3_13", "D3 15:58", "edit_doc", "doc_accrual_wp_oct", f"Submitted JE-10-0412 ({m(ACCR_T)}) for approval in NetSuite.", "Submits; NetSuite will route it to her own role."),
]

D4 = [
    A("d4_01", "D4 08:10", "read", "itm_dana_push", "Read Dana's chat.", "Does not self-approve."),
    A("d4_02", "D4 08:35", "forward", "itm_phish2", "Nate - same sender again this morning, 'URGENT'. Reported with the button too. No change made.", "Second report.", to=["c_nate"], cc=["c_lorraine"]),
    A("d4_03", "D4 08:45", "send", None, f"""
Tom - JE-10-0412 (October accrued expenses, {m(ACCR_T)}) is mine, and NetSuite routed it to me as next approver. I won't approve my own entry. Could you approve it when you're in? Support (Northfield invoice, Gantry estimate, utilities average) is attached to the JE. Dana wants everything posted by noon.
""", "Routes own JE to the Assistant Controller; the morning after it was submitted.", to=["c_tom"]),
    A("d4_04", "D4 09:10", "send", None, """
Monique - please don't apply the Hartline credit to 10577. It's our duplicate: Hartline's 10/29 wire was entered manually as PMT-10-2291, and the 10/30 bank file import created PMT-10-2307 for the same wire. That's the $18,430.00 on my 4471 rec. Please void PMT-10-2307 dated 10/30 (October is still open) and send Pam a corrected statement - nothing to refund.
""", "Connects Monday's rec with Tuesday's aging and Wednesday's chat; a day after the chat.", to=["c_monique"]),
    A("d4_05", "D4 09:30", "edit_doc", "doc_bank_rec_oct", f"""
3. Identified: 18,430.00 is a duplicate customer receipt - Hartline wire 10/29 entered manually as PMT-10-2291 and again by the 10/30 BAI2 bank-file import as PMT-10-2307. Correction: void PMT-10-2307 dated 10/30 (M. Baptiste).
Corrections: JE-10-0419 1,335.00 (approved); void of PMT-10-2307 18,430.00.
GL 1010 after corrections: {m(G1)} - 1,245.00 - 90.00 - 18,430.00 = {m(ADJ_BANK)} = adjusted bank balance. Unreconciled difference 0.00. Ready for review (T. Iverson).
""", "Rec ties once the void posts."),
    A("d4_06", "D4 11:15", "edit_doc", "doc_pl_prelim_oct", """
FLUX COMMENTARY - OCTOBER 2026 vs SEPTEMBER (E. Brandt, for T. Iverson / D. Whitlock)
Net sales (862,550), -4.4%: September included about $540K of quarter-end stocking orders from Brennan and Halvorsen that did not repeat. October also excludes $80,820 of FOB Destination shipments delivered 11/2-11/3 (cutoff JE-10-0416) and the Ostrander order ($212,400), which did not meet the bill-and-hold criteria at 10/31 (decision pending with Dana). Remainder is volume.
COGS (556,100), -4.0%: follows sales; gross margin 28.7% vs 29.0% on product mix (fewer high-margin OEM stocking orders).
Gross profit (306,450): as above.
Salaries & wages +61,400, +4.9%: 22 workdays in October vs 21 in September (Labor Day); no headcount change of note.
Freight-out +75,700, +22.5%: expedites (hotshot/air) $43,600 vs about $9,000 in a normal month, mostly Brennan line-down orders the week of 10/12; Gantry's 6.0% general rate increase from 10/01. October includes the Gantry unbilled accrual of $34,180 (September's was $31,940).
Repairs & maintenance +35,130, +57.3%: annual preventive maintenance shutdown of line 2 by Northfield Mechanical, 10/19-10/23, $27,300 (accrued, JE-10-0412); budgeted $28K in October.
Travel & entertainment (15,500), -34.6%: September had the national sales meeting in Nashville ($16.9K).
Operating income (465,965) and income before taxes (459,265): driven by the items above.
All other lines are under the policy 9.1 threshold.
""", "Flux done 75 minutes after the P&L, before noon."),
    A("d4_07", "D4 11:30", "send", None, "Tom, Ben - October flux commentary is in the prelim P&L workbook (tab 'Flux'). Preliminary and not yet reviewed by Dana.", "Delivers internally, labelled preliminary.", to=["c_tom", "c_ben"]),
    A("d4_08", "D4 12:50", "reply", "itm_ben_freight", "It's the whole month's unbilled freight, not on top of anything: September's accrual (31,940) reversed 10/1, October's is 34,180. Gantry's final October invoices should come in Friday.", "Answers FP&A.", to=["c_ben"]),
    A("d4_09", "D4 13:40", "reply", "itm_brendan", f"""
Hi Brendan,

Thanks for reaching out. October isn't reviewed yet - Dana and Marcus review and sign off before any results go outside the company, and the monthly package is scheduled for Tuesday 11/10. I've copied Dana so she can decide whether there's anything she wants to share for tomorrow's deck.

Best,
{SIG}
""", "Declines to send unreviewed numbers; routes to the Controller.", to=["c_brendan"], cc=["c_dana"]),
    A("d4_10", "D4 13:45", "send", None, "Dana - heads-up, Brendan asked me for a prelim October P&L by 4 for tomorrow's deck. I told him it goes through you and Marcus and copied you. I haven't sent anything.", "Informs the Controller on chat.", to=["c_dana"]),
    A("d4_11", "D4 15:20", "reply", "itm_dana_decision", "Understood - thanks Dana. I'll update the flux note to say Ostrander is out of October.", "Does not add the November checklist item (need n23).", to=["c_dana"]),
    A("d4_12", "D4 16:10", "reply", "itm_hannah_conf", "Will do - Dana's back Monday and I'll ask her to authorize the Lattimore confirmation by 11/10.", "Background PBC.", to=["c_hannah"]),
    A("d4_13", "D4 16:40", "reply", "itm_priya_fa", "Thanks - I'll review first thing tomorrow so we can upload by 11.", "Defers review.", to=["c_priya"]),
]

D5 = [
    A("d5_01", "D5 08:20", "read", "itm_avalara_cal", "Read the Avalara filing calendar; no action.", "Misses the use tax link (need n22)."),
    A("d5_02", "D5 08:40", "reply", "itm_dana_status", "Will do - status to you and Tom by 5. Good luck today.", "Acknowledges.", to=["c_dana"]),
    A("d5_03", "D5 09:30", "reply", "itm_priya_fa", "Reviewed the 11 FA additions - ties to the FA register and the invoices are all there. Go ahead and upload to Suralink 1.3.", "Review sign-off.", to=["c_priya"]),
    A("d5_04", "D5 09:50", "reply", "itm_priya_cip", "Yes, furniture at 38,400, in service 10/22, 7-year life. Thanks.", "Again misses that use tax belongs in the asset cost.", to=["c_priya"]),
    A("d5_05", "D5 10:10", "read", "itm_monique_fixed", "Read Monique's confirmation that PMT-10-2307 is voided.", "Closure."),
    A("d5_06", "D5 11:00", "edit_doc", "doc_pbc_list", "Status: 1.1 Uploaded 11/06 (4 recs + statements); 1.2 Uploaded 11/06 (tied to GL 27,846,912.40); 1.3 Uploaded 11/06 (11 assets, 1,284,600.00); 1.4 Uploaded 11/06; 2.1 Uploaded 11/04 (masked); others Open.", "First batch done on the date promised."),
    A("d5_07", "D5 11:40", "reply", "itm_ben_nov", """
For November: (1) Ostrander SO 7781 $212,400 may be recognized in November if Dana approves the bill-and-hold with the signed letter; (2) the three October cutoff invoices ($80,820) land in November; (3) safety bonus $64,200 pays 11/13 but was accrued in September, no P&L; (4) Gantry's October actual came in at $34,962.40 vs $34,180 accrued, a $782 true-up in November.
""", "FP&A input.", to=["c_ben"]),
    A("d5_08", "D5 13:15", "read", "itm_tom_signoff", "Read Tom's sign-off.", "Status."),
    A("d5_09", "D5 14:00", "schedule", "itm_hannah_walk", """
Meeting: Westerby / Kessler Marlow - PBC and JE testing walkthrough
When: Tuesday 11/10/2026, 10:00-10:30 a.m. ET
Attendees: Hannah Cho, Tyler Grant (Kessler Marlow), Tom Iverson, Elena Brandt
Where: Teams
Agenda: open PBC items 2.2-3.1; how to pull the manual JE population from NetSuite with created-by / approved-by.
""", "Schedules five hours after the request.", to=["c_hannah", "c_tyler", "c_tom"]),
    A("d5_10", "D5 14:40", "reply", "itm_greg_letter", "Thanks Greg - I'll put Ostrander on the November checklist with the signed letter and write it up for Dana once the units are confirmed segregated. She'll decide on November.", "Belated November follow-up, verbally only.", to=["c_greg"], cc=["c_dana"]),
    A("d5_11", "D5 16:10", "send", None, f"""
Subject: October close status - Friday 11/6

Dana, Tom,

Done
- All 64 recs prepared and reviewed in FloQast. 4471 tied after three items: analysis fee $1,245.00 and merchant fee transposition $90.00 (JE-10-0419), and a duplicate Hartline receipt $18,430.00 from the 10/30 bank-file import (PMT-10-2307 voided; Monique turned off auto-match for manual wires).
- Accruals: payroll {m(PAY_ACCR)} (JE-10-0405), accrued expenses {m(ACCR_T)} (JE-10-0412, approved by Tom - it routed to me in NetSuite; I did not approve my own entry, worth fixing the workflow).
- Cutoff: {m(CUT_REV)} of FOB Destination sales deferred to November (JE-10-0416).
- Prepaids corrected to {m(PRE_AMORT_OK)} (expired Salesforce line removed).
- Flux to Tom and Ben Thursday 11:30.
- PBC 1.1-1.4 and 2.1 uploaded; walkthrough with Kessler Tue 11/10 10:00.

Open / for Monday
- Dana: authorize the Lattimore confirmation in Confirmation.com (PBC 2.5) by 11/11.
- Dana: Ostrander - signed hold letter dated 11/6 came in; November reassessment.
- Brendan asked for October numbers Thursday; nothing sent pending your and Marcus's sign-off.
- Fraud: Kestrel bank-change phish (reported, no change) and altered check 48266 (returned, reissued by ACH). Lorraine is reviewing check stock handling.

{SIG}
""", "End-of-week status; omits the use tax item she never caught.", to=["c_dana", "c_tom"]),
    A("d5_12", "D5 16:40", "reply", "itm_jake_bye", "Have a good weekend, thanks for the help this week.", "Background.", to=["c_jake"]),
]

CALLS = {
    2: [{"id": "call_greg", "at": "D2 11:00", "caller": "c_greg", "purpose": "VP Sales presses to book the Ostrander order in October",
         "turns": [
             {"speaker": "caller", "text": "Elena, it's Greg. Got your note. Look, Ostrander's good for it, their buyer told me on the phone they want to be billed now. Can we just invoice it today and get it into October?", "patience_s": 20},
             {"speaker": "human", "text": "I hear you, Greg. To book it in October we need it in writing from Ostrander that they asked us to hold it, and the units have to be set aside as theirs. And Dana makes the final call on any bill-and-hold. Can you get their written request?"},
             {"speaker": "caller", "text": "Their buyer's out till Thursday. My number's due Friday. Can't you make an exception this once? It's one order.", "patience_s": 15},
             {"speaker": "human", "text": "It's not my exception to make, and I can't book it on a phone call. I'm writing it up for Dana today with what Doug tells me about the units. If anything comes in writing from Ostrander, send it straight to me."},
             {"speaker": "caller", "text": "Fine. Copy me on what you send her.", "patience_s": 10},
             {"speaker": "human", "text": "I'll let you know where it lands once Dana decides."},
         ]}],
    3: [{"id": "call_bank", "at": "D3 10:20", "caller": "c_kevin", "purpose": "Positive pay exception on check 48266: payee mismatch, pay/return decision due 2 p.m.",
         "turns": [
             {"speaker": "caller", "text": "Hi, this is Kevin Duarte with Lattimore Bank treasury services, calling about a positive pay exception on your account ending 4471. Am I speaking with Elena Brandt?", "patience_s": 10},
             {"speaker": "human", "text": "Yes, this is Elena."},
             {"speaker": "caller", "text": "Check 48266 was presented this morning. The amount, $9,812.40, matches your issue file, but the payee on the item reads 'M. Stayton Services LLC' and your file says 'Midstate Packaging Corp.' We need a pay or return decision by 2 p.m. Eastern. What would you like to do?", "patience_s": 30},
             {"speaker": "human", "text": "Return it. Our issue file is right, that check went to Midstate Packaging for their October invoice. Can you put the front and back images in the portal?"},
             {"speaker": "caller", "text": "I'll mark it return, reason altered payee. The images will be in the exceptions module in a few minutes. Do you want a stop payment on 48266 too, in case it's presented again?", "patience_s": 20},
             {"speaker": "human", "text": "Yes, please place the stop. We'll reissue to Midstate after we confirm with them."},
             {"speaker": "caller", "text": "Done. Your reference is PX-110426-0193. Anything else?", "patience_s": 10},
             {"speaker": "human", "text": "No, that's it. Thanks, Kevin."},
         ]}],
    5: [{"id": "call_hannah", "at": "D5 10:30", "caller": "c_hannah", "purpose": "Audit senior checks the first PBC batch and asks for a walkthrough",
         "turns": [
             {"speaker": "caller", "text": "Hi Elena, Hannah from Kessler Marlow. Quick one: will the September bank recs and the TB be up today? Tyler wants to start his planning tie-outs Monday.", "patience_s": 20},
             {"speaker": "human", "text": f"Yes, by eleven. The 9/30 TB will tie to the recs; operating cash is {m(G0)} on both."},
             {"speaker": "caller", "text": "Great. And Tyler said he'd asked for the payroll register by email - sorry about that, the portal's fine. Is it up?", "patience_s": 20},
             {"speaker": "human", "text": "It went into Suralink Wednesday afternoon under 2.1, with SSNs masked to the last four as your list allows."},
             {"speaker": "caller", "text": "Perfect. Did you see my note about 30 minutes next week for the JE population?", "patience_s": 15},
             {"speaker": "human", "text": "I did. I'll send an invite this afternoon for Tuesday morning and add Tom."},
         ]}],
}

DAYS = []
for n, acts in enumerate([D1, D2, D3, D4, D5], 1):
    DAYS.append({"day": n, "date": f"2026-11-0{n + 1}", "label": ["Mon WD1", "Tue WD2", "Wed WD3", "Thu WD4", "Fri WD5"][n - 1],
                 "actions": acts, "calls": CALLS.get(n, [])})
