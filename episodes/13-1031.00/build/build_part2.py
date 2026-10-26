# Part 2: Monday and Tuesday arrivals, actions, calls.
from build_part1 import item, SIG

# ======================= D1 Monday 11/02 =======================
item("vm_d1_wynn", "phone", "voicemail", "D1 07:40", "t_wynn", "c_wynn", ["c_daniela"], "Voicemail from 254-555-0170 (0:31)",
     "Yeah this is Curtis Wynn returning a call about my Camry, the hail claim. I work nights so best is after two in the afternoon. 254-555-0170. Thanks.")
item("vm_d1_ostrowski", "phone", "voicemail", "D1 07:52", "t_ostrowski", "c_ostrowski", ["c_daniela"],
     "Voicemail from 254-555-0128 (0:48)",
     "Hi Daniela, this is Ben Ostrowski, the wreck back in June with the lady on Adams. A guy came to my house Friday night and handed me court papers, says I'm being sued. I don't know what I'm supposed to do with these. Can you call me back? 254-555-0128.")
item("e_d1_renee_correction", "email", "email", "D1 08:00", "t_cat", "c_renee",
     ["c_daniela", "c_colton", "c_tasha"], "CAT 26-14: correction to packet p.2 + decision-due column", cc=["c_greg"],
     body="""Morning all,

Correction to section 2 of the CAT 26-14 packet: that paragraph was carried over from last year's CAT 25-06 packet by mistake. TDI has NOT designated this event under 542.059, so there is no 15-day extension. Use the normal Chapter 542 Subchapter B timelines on every CAT 26-14 file:
- acknowledge, start the investigation and request what we need within 15 days of notice (our standard is still 24-hour contact);
- accept or reject in writing within 15 business days after we have all items, statements and forms;
- pay within 5 business days after we notify acceptance.

Please add the "542.056 decision due" date to your inventory sheet for every claim where all items are in, and keep it current as files complete. Business days exclude weekends and Texas state holidays. I need the columns filled in by Wednesday noon so I can roll them up for Howard.

Thanks,
Renee

Renee Lindqvist | CAT Coordinator | Leon River Mutual | 254-555-0105""")
item("e_d1_greg_week", "email", "email", "D1 08:05", "t_greg_week", "c_greg", ["c_daniela", "c_colton", "c_tasha"],
     "This week", body="""Team,

Quick list for the week:
1. CAT 26-14 is still running about 190 new auto comp claims a day company-wide. Expect 2-4 new hail assignments each a day on top of your regular desk.
2. Drive-in is booking 2 days out. Use it; don't send Luis's people to the field for drivable cars.
3. Roundtable Thursday 2:00. If you have anything with a demand at or near limits, get it on Howard's agenda.
4. Watch your authority. I'd rather get ten emails than find a reserve posted over your limit.

Greg

Greg Pruitt | Auto Claims Supervisor | Leon River Mutual | 254-555-0102""")
item("e_d1_cat_stats", "email", "email", "D1 08:10", "t_cat_stats", "c_renee", ["c_daniela", "c_colton", "c_tasha", "c_greg"],
     "CAT 26-14 daily numbers - Mon 11/02 (FYI)", body="""FYI, no action needed.

CAT 26-14 as of 7:00 a.m. Mon 11/02:
Auto comprehensive reported: 1,412 | Property: 966
Auto inspected: 388 | Drive-in slots booked through Wed: 610
Auto paid: 214 claims, $1,146,820 | Average auto severity (paid): $5,359
Total losses identified: 31

Renee""")
item("tk_d1_pickett_fnol", "tickets", "ticket", "D1 08:00", "t_pickett", "c_fnol", ["c_daniela"],
     "New assignment: AU-26-023288 Pickett - collision with parked vehicle (DOL 10/31/2026)", attachments=["doc_pickett_dec"],
     body="""ClaimCenter new assignment. FNOL taken by phone Sun 11/01 2:22 p.m. (rep: K. Whitaker).
Named insured: Lorraine M. Pickett, 1416 S 31st St, Temple TX 76504, 254-555-0110. Policy PA-TX-3398815.
Loss: Sat 10/31/2026 approx 9:50 p.m., S 31st St near her home. Caller states: "I was driving, a cat ran out and I swerved and hit a parked car and a mailbox." Says her son Cody was in the car with her. Temple PD came out. No injuries.
Insured vehicle: 2018 Chevrolet Equinox LT, front right damage, drivable.
Third party: parked, unoccupied 2014 Ford Focus, owner Maribel Ochoa (1419 S 31st St). Mailbox at 1418 S 31st St.
Features opened: Collision (insured vehicle); Liability PD (Ochoa vehicle; mailbox).
Activity: contact insured within 24 hours; take recorded statement; order crash report.""")
item("doc_pickett_dec", "docs", "document", "D1 08:00", "t_pickett", "c_fnol", ["c_daniela"],
     "Declarations page - PA-TX-3398815 (Pickett), term 03/12/2026-09/12/2026 renewed to 03/12/2027",
     """LEON RIVER MUTUAL INSURANCE COMPANY - TEXAS PERSONAL AUTO POLICY DECLARATIONS
Policy PA-TX-3398815 | Term 09/12/2026 - 03/12/2027
Named insured: Lorraine M. Pickett, 1416 S 31st St, Temple TX 76504
Vehicle 1: 2018 Chevrolet Equinox LT, VIN 2GNAXJEV4J6184427 (garaged Temple)
Listed drivers: Lorraine M. Pickett (DOB 1971)
EXCLUDED DRIVERS: Cody R. Pickett (DOB 04/22/2005) - Named Driver Exclusion endorsement LRM-TX-NDE, signed by the named insured 03/12/2025.
Coverages: Liability BI $30,000/$60,000; PD $25,000. Collision, $500 deductible. Comprehensive, $500 deductible. PIP rejected in writing. No rental reimbursement.
Endorsement LRM-TX-NDE (excerpt): "We will not provide coverage for any claim arising from an accident or loss involving a motorized vehicle being operated by an excluded driver. This includes any claim for damages made against a named insured, resident relative, or any other person or organization that is vicariously liable for an accident arising out of the operation of a motorized vehicle by the excluded driver." """)
item("tk_d1_sutton_fnol", "tickets", "ticket", "D1 08:00", "t_sutton", "c_fnol", ["c_daniela"],
     "New CAT 26-14 assignment: AU-26-023176 Sutton - hail",
     "ClaimCenter new assignment (CAT 26-14). Brenda Sutton, 254-555-0131, Belton. 2018 Mazda CX-5 Touring, hail damage to hood, roof and trunk lid, drivable. Comp deductible $500. Reported via app 11/01 6:05 p.m.")
item("tk_d1_price_fnol", "tickets", "ticket", "D1 08:00", "t_price", "c_fnol", ["c_daniela"],
     "New CAT 26-14 assignment: AU-26-023181 Price - hail + windshield",
     "ClaimCenter new assignment (CAT 26-14). Jamal Price, 254-555-0144, Harker Heights. 2020 Honda Civic EX, hail to roof and hood, windshield cracked across driver side. Comp deductible $500. No rental coverage. Reported by phone 11/01 9:40 a.m.")
item("e_d1_ostrowski_petition", "email", "email", "D1 09:40", "t_ostrowski", "c_ostrowski", ["c_daniela"],
     "court papers", attachments=["doc_ostrowski_petition"], body="""Hi Daniela,

Here are the pictures of the papers like you asked. There are 9 pages, I took a picture of each one. The guy gave them to me Friday 10/30 around 6:15 in the evening at my front door.

Ben

Sent from my iPhone""")
item("doc_ostrowski_petition", "docs", "document", "D1 09:40", "t_ostrowski", "c_ostrowski", ["c_daniela"],
     "Citation and Plaintiff's Original Petition - Dunn v. Ostrowski (photos, 9 pages)",
     """THE STATE OF TEXAS - CITATION
Cause No. 2026-CCL2-0917, County Court at Law No. 2, Bell County, Texas
KAYLA DUNN, Plaintiff v. BENJAMIN OSTROWSKI, Defendant
Petition filed: 10/26/2026. Citation issued: 10/27/2026.
To: Benjamin Ostrowski, 3517 Brookhaven Dr, Temple, Texas 76502.
"You have been sued. You may employ an attorney. If you or your attorney do not file a written answer with the clerk who issued this citation by 10:00 a.m. on the Monday next following the expiration of twenty days after you were served this citation and petition, a default judgment may be taken against you..."
Attorney for plaintiff: Paul Gaitan, Gaitan Law Firm, 600 Austin Ave Suite 14, Waco TX 76701.
OFFICER'S / AUTHORIZED PERSON'S RETURN: Came to hand 10/28/2026. Executed on 10/30/2026 at 6:15 p.m. by delivering to Benjamin Ostrowski in person at 3517 Brookhaven Dr, Temple, a true copy of this citation with the petition attached. Signed: R. Talamantez, private process server, PSC-18842.

PLAINTIFF'S ORIGINAL PETITION (summary of pages 2-9)
Discovery Level 2. Plaintiff seeks monetary relief of $250,000 or less, excluding interest, statutory or punitive damages and penalties, and attorney fees and costs. Alleges negligence (failure to keep a proper lookout, failure to control speed, following too closely) in the 06/14/2026 collision at W Adams Ave and S 5th St. Damages: past and future medical expenses, physical pain, mental anguish, impairment, lost earning capacity. Includes requests for disclosure under Rule 194 and a jury demand.""")
item("ch_d1_colton", "chat", "chat_message", "D1 10:15", "t_teamchat", "c_colton", ["c_daniela"],
     "#auto-claims-temple", "anyone have drive-in slots wed? scheduler shows full til thurs for me. got a lady w/ a lexus and 3 kids who can only come wed am")
item("e_d1_luis_estimates", "email", "email", "D1 11:30", "t_cat_estimates", "c_luis", ["c_daniela"],
     "Drive-in estimates: Patel and Ellis", attachments=["doc_patel_est", "doc_ellis_est"], body="""Daniela,

Both of your 9:00 and 10:30 came through.

Patel Elantra - straight PDR, 118 dents total, no paint break. CCC ONE estimate $3,412.18 uploaded, signed by insured.
Ellis Accord - she's hammered. Roof and trunk lid stretched, both need replacement, hood and both rear doors over matrix, plus the moonroof glass. Estimate $10,960.42. That's going to total against her value, I'd bet. Requested CCC valuation and a salvage bid from Heart of Texas.

Luis

Luis Ortega | Staff Appraiser, CAT drive-in lead | Leon River Mutual""")
item("doc_patel_est", "docs", "document", "D1 11:30", "t_cat_estimates", "c_luis", ["c_daniela"],
     "CCC ONE estimate - AU-26-023119 Patel - 2019 Hyundai Elantra SEL",
     """CCC ONE ESTIMATE (LRM drive-in, appraiser L. Ortega, written 11/02/2026 10:58 a.m.)
Claim AU-26-023119 | Owner Nikhil Patel | 2019 Hyundai Elantra SEL | 41,207 mi
PDR per 2026 LRM hail matrix: hood 34 dents (medium) $845.00; roof 52 dents (medium) $1,410.00; trunk lid 22 dents $535.00; L/R roof rails R&I $160.00
Subtotal PDR $2,950.00 | Body labor (R&I headliner, 2.4 hr @ $58.00) $139.20 | Paint materials $0.00 | Parts $322.98 (roof rail clips, moldings)
Gross total $3,412.18 | Comprehensive deductible $500.00 | Net $2,912.18
Insured signed estimate acknowledgment 11/02 10:56 a.m.""")
item("doc_ellis_est", "docs", "document", "D1 11:30", "t_ellis", "c_luis", ["c_daniela"],
     "CCC ONE estimate - AU-26-023114 Ellis - 2015 Honda Accord EX",
     """CCC ONE ESTIMATE (LRM drive-in, appraiser L. Ortega, written 11/02/2026 9:41 a.m.)
Claim AU-26-023114 | Owner Patricia Ellis | 2015 Honda Accord EX sedan 4D 2.4L | 118,642 mi
Roof panel replace (stretched metal) $1,486.00 parts; trunk lid replace $612.00; moonroof glass $684.00; hood and rear doors over PDR matrix - conventional repair; refinish roof, trunk, hood, rear doors; R&I headliner and moonroof; labor 41.6 hr @ $58.00; paint materials $1,188.00.
Gross total $10,960.42 | Comprehensive deductible $1,000.00
Appraiser note: probable total loss; valuation and salvage bid requested.""")
item("e_d1_centex", "email", "email", "D1 09:05", "t_okafor_rental", "c_centex", ["c_daniela"],
     "Rental extension - RA 4471809 - Okafor", body="""Good morning Daniela,

Your insured Samuel Okafor (claim AU-26-023127) has a 2025 Nissan Rogue on RA 4471809 since 10/30. Direct-bill authorization on file is $30.00/day for 3 days. He upgraded to the SUV class at $45.00/day at the counter and told us his insurance would cover it. Can you extend the authorization through the repair date and confirm the daily rate you're covering?

Thank you,
Amber Lyle
Branch Manager | Centex Rent-A-Car, Temple | 254-555-0190""")
item("e_d1_ccc_ellis", "email", "email", "D1 13:00", "t_ellis", "c_luis", ["c_daniela"], "CCC valuation - Ellis",
     attachments=["doc_ellis_ccc"], body="Valuation's back on the Ellis Accord. Total it. -L")
item("doc_ellis_ccc", "docs", "document", "D1 13:00", "t_ellis", "c_luis", ["c_daniela"],
     "CCC ONE Market Valuation Report - AU-26-023114 - 2015 Honda Accord EX",
     """CCC ONE MARKET VALUATION REPORT (run 11/02/2026 12:47 p.m.)
Claim AU-26-023114 | Owner Patricia Ellis | Loss type: Comprehensive - hail | DOL 10/29/2026
Vehicle: 2015 Honda Accord EX sedan 4D 2.4L I4, CVT, 118,642 mi, garaged ZIP 76504
Comparable vehicles (within 150 mi, last 90 days, adjusted for mileage/equipment): 6 dealer listings, adjusted values $11,940 to $13,210.
Base vehicle value: $12,480.00
Condition adjustment (interior wear, tires at 4/32 in.): -$215.00
Adjusted Vehicle Value: $12,265.00
Prior damage deduction: none | Options adjustment: included in base
Total loss threshold check: repair estimate $10,960.42 + projected salvage $2,350.00 = $13,310.42, which exceeds the Adjusted Vehicle Value -> TOTAL LOSS.""")
item("e_d1_hotaa", "email", "email", "D1 13:20", "t_ellis", "c_hotaa", ["c_daniela"], "Salvage bid - AU-26-023114 Ellis Accord",
     body="""Hi Daniela,

High bid for the 2015 Accord (hail, run and drive) is $2,350.00, good for 14 days. Let me know when to schedule pickup and send the title paperwork.

Kim Dao
Salvage Coordinator | Heart of Texas Auto Auction | 254-555-0161""")
item("e_d1_hailpros", "email", "email", "D1 14:10", "t_albrecht", "c_hailpros", ["c_daniela"],
     "Megan Albrecht F-150 - invoice and direction to pay - PAYMENT NEEDED TODAY", attachments=["doc_hailpros_invoice"],
     body="""Daniela,

Lone Star Hail Pros has completed repairs on your insured Megan Albrecht's 2020 F-150. Invoice attached for $7,860.00 along with her signed Direction to Pay. Please issue payment TODAY payable to Lone Star Hail Pros LLC only. We are a mobile operation and our crew leaves Temple Friday. Every other carrier we work with pays same day off our invoice.

If payment isn't issued today, storage of $75/day starts tomorrow and we'll be filing a complaint with TDI for delay.

Brent Kowalski
Owner, Lone Star Hail Pros LLC | 469-555-0177 | "We follow the storms so you don't have to wait" """)
item("doc_hailpros_invoice", "docs", "document", "D1 14:10", "t_albrecht", "c_hailpros", ["c_daniela"],
     "Lone Star Hail Pros invoice #LSHP-1029-114 and Direction to Pay - Albrecht",
     """LONE STAR HAIL PROS LLC - INVOICE #LSHP-1029-114 (11/01/2026)
Customer: Megan Albrecht | 2020 Ford F-150 XLT SuperCrew | Claim AU-26-023131
PDR hood $1,450; roof $2,380; cab corners and doors $1,740; bed sides $1,640; R&I headliner $350; aluminum panel surcharge $300
TOTAL $7,860.00 | Customer deductible "waived - we take care of it"
DIRECTION TO PAY: "I direct Leon River Mutual to pay all proceeds of my claim directly and solely to Lone Star Hail Pros LLC." Signed: Megan Albrecht, 10/31/2026. (No lienholder signature. Policy loss payee: Texas Frontier Bank.)""")
item("e_d1_trent", "email", "email", "D1 14:30", "t_haskins", "c_trent", ["c_daniela"],
     "RE: Subrogation demand - your insured Haskins / our insured Pham - DOL 09/03/2026", body="""Daniela,

We've reviewed your demand for $7,240.00. Our insured maintains the light was yellow when he entered. We're prepared to accept 80% liability and pay $5,792.00 in full settlement. Please advise.

Trent Booker
Claims Adjuster | Gulf Plains Insurance Company | 713-555-0142""")
item("e_d1_misaddressed", "email", "email", "D1 15:20", "t_brandt", "c_bcc", ["c_daniela"],
     "Estimate - Brandt - 2021 Chevy Tahoe - claim AU-26-023109", body="""Daniela,

Attached is our estimate for Ronald Brandt's Tahoe, $8,415.62 with the roof skin. Can you approve today so we can order the panel? Car is here.

Thanks,
Dusty Marek
Estimator | Bell County Collision | 254-555-0186""")
item("ch_d1_brianna", "chat", "chat_message", "D1 15:45", "t_teamchat", "c_brianna", ["c_daniela"],
     "#auto-claims-temple", "@Daniela ordered the CR-3 on Pickett from Temple PD, they said it should post to the TxDOT portal by Wed. Will drop it in OnBase when it does.")
item("vm_d1_haskins", "phone", "voicemail", "D1 16:05", "t_haskins", "c_haskins", ["c_daniela"], "Voicemail from 254-555-0115 (0:22)",
     "Hi, Gloria Haskins. Just checking if I'm getting my five hundred dollar deductible back from the other insurance yet. Thank you.")

D1_ACTIONS = [
    {"id": "a_d1_01", "at": "D1 09:00", "verb": "read", "target": "e_d1_renee_correction", "content": "",
     "note": "Reads the correction: no 542.059 extension; decision-due column due Wed noon."},
    {"id": "a_d1_02", "at": "D1 09:10", "verb": "call_out", "target": "vm_d1_ostrowski",
     "content": "Calls Ben Ostrowski back at 254-555-0128 (call_d1_ostrowski).", "note": "Same-morning callback on suit papers."},
    {"id": "a_d1_03", "at": "D1 09:45", "verb": "read", "target": "e_d1_ostrowski_petition", "content": "",
     "note": "Reads the citation and return of service; served 10/30 6:15 p.m."},
    {"id": "a_d1_04", "at": "D1 10:00", "verb": "update_ticket", "target": "tk_d1_sutton_fnol",
     "content": "File note 11/02 10:00: Contacted insured Brenda Sutton by phone 254-555-0131 (first attempt). Hail to hood, roof, trunk lid; drivable; no glass damage. Booked drive-in Wed 11/04 8:30 a.m. Comp ded $500. Initial reserve set $4,800 per CAT guideline. CAT-01 acknowledgment letter sent by email.",
     "note": "24-hour contact standard; reserve within authority."},
    {"id": "a_d1_05", "at": "D1 10:35", "verb": "call_out", "target": "tk_d1_pickett_fnol",
     "content": "Calls Lorraine Pickett at 254-555-0110 to take a recorded statement (call_d1_pickett).", "note": ""},
    {"id": "a_d1_06", "at": "D1 11:10", "verb": "update_ticket", "target": "tk_d1_pickett_fnol",
     "content": "File note 11/02 11:10: Recorded statement of named insured Lorraine Pickett taken by phone with her permission, 10:38-10:52 a.m. She states she was driving the Equinox northbound on S 31st St about 9:50 p.m. on 10/31, swerved for a cat, struck the parked Ochoa Focus and the mailbox at 1418. Son Cody (21) was the front passenger. Temple PD responded; she does not have the report number. Dec page reviewed: Cody R. Pickett is a named excluded driver (LRM-TX-NDE, signed 03/12/2025). Crash report ordered by B. Cole. Equinox drivable; insured will get estimate at drive-in Thu. No payment on either feature until the crash report is reviewed.",
     "note": "Documents the statement; notes the exclusion; waits for the CR-3."},
    {"id": "a_d1_07", "at": "D1 11:40", "verb": "update_ticket", "target": "tk_d0_wynn",
     "content": "File note 11/02 11:40: Insured returned call by voicemail 7:40 a.m.; prefers calls after 2:00 p.m. Will call at 2:15 today. Activity moved to 11/02 2:15 p.m.",
     "note": ""},
    {"id": "a_d1_08", "at": "D1 12:10", "verb": "edit_doc", "target": "sheet_cat_tracker",
     "content": "Row AU-26-023119 Patel: Inspection 'Drive-in 11/02 10:30 done'; Estimate $3,412.18; All items rec'd 11/02. Row AU-26-023114 Ellis: Estimate $10,960.42; status 'Open - TL, valuation pending'. Added rows: AU-26-023176 | Brenda Sutton | 2018 Mazda CX-5 Touring | 11/01 | 11/02 | Drive-in 11/04 8:30 | - | $500 comp | - | - | $0.00 | Open (reserve $4,800); AU-26-023181 | Jamal Price | 2020 Honda Civic EX | 11/01 | - | - | - | $500 comp | - | - | $0.00 | Open - windshield, no rental coverage (reserve $4,800).",
     "note": "Leaves the 542.056 decision-due column blank for now."},
    {"id": "a_d1_09", "at": "D1 13:45", "verb": "update_ticket", "target": "doc_patel_est",
     "content": "Payment issued 11/02: AU-26-023119 comprehensive, $2,912.18 ($3,412.18 estimate less $500 deductible) by EFT to Nikhil Patel (no lienholder on policy). Acceptance-and-payment letter sent. Reserve closed. Tracker row updated: paid $2,912.18, Closed 11/02.",
     "note": "Within APD authority; acceptance notice and payment same day."},
    {"id": "a_d1_10", "at": "D1 14:15", "verb": "call_out", "target": "vm_d1_wynn",
     "content": "Calls Curtis Wynn at 254-555-0170: books drive-in Sat 11/07 9:00 a.m.; reserve stays $4,800; CAT-01 letter emailed. Tracker row updated: contacted 11/02, drive-in 11/07.",
     "note": "Second contact attempt completed."},
    {"id": "a_d1_11", "at": "D1 14:40", "verb": "reply", "target": "e_d1_trent",
     "content": "Trent,\n\nThanks for the response. We can't accept 80%. Independent witness Carla Nunez (statement enclosed again, taken 09/08) says your insured entered the intersection on a red that had been red 'for a couple of seconds' while she was stopped at it. Ms. Haskins had a green. Please reconsider at 100%, $7,240.00, which includes her $500 deductible. If we can't agree in 15 days I'll file with Arbitration Forums.\n\n" + SIG,
     "note": "Counters on the witness evidence."},
    {"id": "a_d1_12", "at": "D1 15:30", "verb": "forward", "target": "e_d1_misaddressed",
     "content": "Tasha - this came to me but AU-26-023109 Brandt is yours. Dusty, copying you so you have the right adjuster: Tasha Nguyen.",
     "note": "Misaddressed estimate goes to the file owner."},
    {"id": "a_d1_13", "at": "D1 16:30", "verb": "forward", "target": "e_d1_ostrowski_petition",
     "content": "Elaine,\n\nSuit papers on AU-26-011907 (Ostrowski, DOL 06/14/2026). Kayla Dunn v. Benjamin Ostrowski, Cause No. 2026-CCL2-0917, County Court at Law No. 2, Bell County. Personal service on the insured Fri 10/30/2026 at 6:15 p.m. by private process server (return attached). Answer due 10:00 a.m. Monday 11/23/2026 (20 days after service = Thu 11/19; Monday next = 11/23). Policy PA-TX-2287140, BI 50/100. Plaintiff's counsel Paul Gaitan, Waco. Pre-suit: demand $28,000, our offer $9,500 rejected 09/30; reserve $15,000. I've told the insured not to talk with plaintiff or her lawyer and that we'll assign defense counsel. File summary and materials in OnBase.\n\nThanks,\nDaniela",
     "note": "Litigation referral within 1 business day, with the computed answer date."},
]

D1_CALLS = [
    {"id": "call_d1_ostrowski", "at": "D1 09:10", "caller": "c_ostrowski", "purpose": "Outbound callback: insured served with suit papers",
     "turns": [
         {"speaker": "human", "text": "Hi Ben, it's Daniela Reyes at Leon River Mutual returning your call about the papers you got Friday."},
         {"speaker": "caller", "text": "Yeah, thanks for calling back. Guy knocked on my door Friday evening and handed me a stack. It says Kayla Dunn versus me. Am I supposed to go to court? Do I need to hire a lawyer?", "patience_s": 12},
         {"speaker": "human", "text": "You don't need to hire anyone. Your policy gives you a defense, so we'll assign an attorney to represent you at no cost to you. What I need first is a picture of every page, including the page with the process server's signature. Can you email those to me this morning?"},
         {"speaker": "caller", "text": "Sure, I can do that from my phone. What time did he come... it was like 6:15. Should I call her lawyer? His name's on there.", "patience_s": 10},
         {"speaker": "human", "text": "Please don't contact her or her lawyer, and don't post anything about the accident online. If anyone calls you about it, take their name and send them to me. I'll get the papers to our litigation department today so the answer is filed on time, and the defense attorney will call you directly."},
         {"speaker": "caller", "text": "Okay. Is this going to cost me anything? They're asking for up to two hundred fifty thousand it says.", "patience_s": 12},
         {"speaker": "human", "text": "That's the standard range lawyers have to plead in Texas, not what they'll get. Your bodily injury limit is fifty thousand per person, and we're defending you. If anything ever looks like it could go above your limits, we'll tell you in writing. Send me those pictures and I'll confirm when they're with our attorney."},
         {"speaker": "caller", "text": "Alright. Sending them now. Thanks, Daniela.", "patience_s": 6},
         {"speaker": "human", "text": "Thanks, Ben. Talk soon."}]},
    {"id": "call_d1_pickett", "at": "D1 10:38", "caller": "c_pickett", "purpose": "Outbound recorded statement of named insured on a collision with a parked car",
     "turns": [
         {"speaker": "human", "text": "Ms. Pickett, this is Daniela Reyes with Leon River Mutual about Saturday night's accident. I'd like to take a recorded statement so I have your account accurately. Do I have your permission to record this call?"},
         {"speaker": "caller", "text": "Yes, that's fine. I just want the lady's car fixed and mine fixed, I feel terrible.", "patience_s": 8},
         {"speaker": "human", "text": "Thank you. Today is Monday, November 2, 2026, 10:38 a.m. Central. This is Daniela Reyes speaking with Lorraine Pickett by phone; she knows the call is recorded. Ms. Pickett, in your own words, what happened?"},
         {"speaker": "caller", "text": "I was coming home on 31st around ten to ten, a cat shot out from between the cars, I swerved right and clipped the parked Focus and the Hendersons' mailbox. That's it. Cody was with me.", "patience_s": 14},
         {"speaker": "human", "text": "Who was behind the wheel when the car hit the Focus, and where was Cody sitting?"},
         {"speaker": "caller", "text": "I was driving. He was in the front seat. He doesn't drive my car, I know he's not on the policy.", "patience_s": 10},
         {"speaker": "human", "text": "Did Cody drive the Equinox at any point that evening, before or after the accident, even to move it?"},
         {"speaker": "caller", "text": "No. Well. No. I moved it into my driveway after the officer left.", "patience_s": 9},
         {"speaker": "human", "text": "When the officer arrived, who did you or Cody tell him was driving, and did he give you an exchange form or a report number?"},
         {"speaker": "caller", "text": "I don't remember what exactly got said, it was chaotic. He gave Cody a little paper, I think it's in the car. I can look for it.", "patience_s": 12},
         {"speaker": "human", "text": "Please do and text me a photo of it. Is there anything else you want to add about the accident?"},
         {"speaker": "caller", "text": "No, that's everything. When will the lady's car get fixed?", "patience_s": 8},
         {"speaker": "human", "text": "I'm getting the police report and an estimate, and I'll be back in touch with you and with Ms. Ochoa once I have them. This concludes the statement at 10:52 a.m. Thank you, Ms. Pickett."}]},
    {"id": "call_d1_okafor", "at": "D1 13:30", "caller": "c_okafor", "purpose": "Inbound: insured asks whether the $45/day rental is covered",
     "turns": [
         {"speaker": "caller", "text": "Hi, this is Sam Okafor, the RAV4 with the back glass busted out. Centex says I'm at forty-five a day and you only approved thirty. I've got two car seats, I needed the bigger car. Are you covering it?", "patience_s": 12},
         {"speaker": "human", "text": "Hi Sam. Your policy's rental reimbursement pays up to $30 a day, up to $900 total for this loss, so we'll direct-bill Centex the $30 and the extra $15 a day for the upgrade is yours. If you switch back to a standard car the difference goes away."},
         {"speaker": "caller", "text": "That's annoying. How long will the shop have it? They said something about waiting on glass.", "patience_s": 10},
         {"speaker": "human", "text": "Bell County Collision's estimate shows the liftgate glass arriving this week and completion around November 10. I'll extend the Centex authorization through the repair date at $30 a day and let you know if the date moves."},
         {"speaker": "caller", "text": "Okay. Just keep me posted.", "patience_s": 6},
         {"speaker": "human", "text": "Will do. You'll get an email from me today with the details."}]},
]

# ======================= D2 Tuesday 11/03 =======================
item("tk_d2_villarreal_fnol", "tickets", "ticket", "D2 08:00", "t_villarreal", "c_fnol", ["c_daniela"],
     "New CAT 26-14 assignment: AU-26-023201 Villarreal - hail (system flags)", body="""ClaimCenter new assignment (CAT 26-14).
Named insured: Rosa Villarreal, 2810 Westcliff Rd, Killeen TX 76543, 254-555-0194. Policy PA-TX-5120348 (agent: Haney Insurance Agency).
Reported via app Sun 11/01 8:12 p.m.: "Hail Thursday night around 6:45 at my house in Killeen, dents all over and the back window cracked." 2021 Nissan Altima SV.
Policy transactions: 10/30/2026 09:12 a.m. - endorsement "Add Comprehensive ($500 ded) and Collision ($500 ded)", entered by Haney Insurance Agency through the agent portal, EFFECTIVE DATE 10/29/2026 12:01 a.m. Prior term: liability only.
ISO ClaimSearch hit: same VIN, hail DOL 05/18/2025, Ridgeway Mutual (prior carrier), paid $3,880.00 on 06/02/2025; no repair invoice on file with ISO.
System flags: COVERAGE CHANGE WITHIN 7 DAYS OF DOL; PRIOR LOSS SAME VIN.""")
item("e_d2_cat_stats", "email", "email", "D2 08:05", "t_cat_stats", "c_renee", ["c_daniela", "c_colton", "c_tasha", "c_greg"],
     "CAT 26-14 daily numbers - Tue 11/03 (FYI)", body="""FYI, no action needed.

CAT 26-14 as of 7:00 a.m. Tue 11/03:
Auto comprehensive reported: 1,598 | Property: 1,071
Auto inspected: 561 | Auto paid: 342 claims, $1,861,404 | Average auto severity (paid): $5,443
Total losses identified: 47

Renee""")
item("ch_d2_brianna", "chat", "chat_message", "D2 08:20", "t_teamchat", "c_brianna", ["c_daniela"], "#auto-claims-temple",
     "Elaine's office says they got the Ostrowski suit papers, thx. Also Ferreira called the main line to confirm her 8:30 drive-in, I told her yes")
item("e_d2_delgado_demand", "email", "email", "D2 09:12", "t_kessler", "c_delgado", ["c_daniela"],
     "STOWERS DEMAND - Aaliyah Brooks / your insured Wade Kessler - Claim AU-26-018842 - DOL 09/12/2026",
     cc=["c_yesenia"], attachments=["doc_brooks_demand", "doc_brooks_meds"], body="""Ms. Reyes,

Please see the attached time-limited settlement demand and supporting medical documentation on behalf of our client, Aaliyah Brooks. A copy is also being sent by certified mail, return receipt requested.

Please direct all communications regarding Ms. Brooks to this office.

Marcus Delgado
Delgado & Finch PLLC | 1207 W Veterans Memorial Blvd, Suite 210, Killeen, Texas 76541 | 254-555-0188""")
item("doc_brooks_demand", "docs", "document", "D2 09:12", "t_kessler", "c_delgado", ["c_daniela"],
     "Stowers demand letter - Aaliyah Brooks (11/03/2026)", """DELGADO & FINCH PLLC
November 3, 2026
VIA EMAIL AND CERTIFIED MAIL, RRR
Daniela Reyes, Leon River Mutual Insurance Company, P.O. Box 1180, Temple, TX 76503
Re: Our client: Aaliyah Brooks | Your insured: Wade Kessler | Claim No.: AU-26-018842 | Date of loss: 09/12/2026

Dear Ms. Reyes:

On September 12, 2026, your insured, driving too fast for the rain on I-35, rear-ended the Honda Civic our client was driving with enough force to push it into a vehicle ahead. Liability is not in dispute; your company accepted it on September 16.

Ms. Brooks was transported by Bell County EMS to the emergency department with neck and low back pain. MRI on October 2 showed a C5-6 disc herniation with foraminal narrowing and an L4-5 protrusion. She has completed 24 physical therapy visits and two lumbar epidural steroid injections (October 9 and 23) with temporary relief. Her pain management physician recommends radiofrequency ablation, estimated at $9,500. She is 28 and works as a dental assistant; she missed 160 hours of work.

Her damages to date include more than $36,000 in medical expenses and $3,264.00 in lost wages, itemized in the enclosed summary, with records and billing affidavits. Her future medical care, pain, mental anguish and impairment are substantial, and a Bell County jury would value this case well in excess of your insured's $30,000 per-person bodily injury limit.

Our client offers to fully and finally release Wade Kessler from all claims arising from this collision in exchange for payment of the $30,000.00 per-person policy limit. This offer is subject to the following terms:
1. Written acceptance must be received in this office by 5:00 p.m. Central Time on Thursday, December 3, 2026. If it is not, this offer is withdrawn and will not be renewed.
2. Payment must be received within 10 business days after acceptance, payable to "Aaliyah Brooks and Delgado & Finch PLLC."
3. The release will release your insured only; it will contain no indemnity or confidentiality provisions and will not release any underinsured motorist claim.
4. Please provide with your acceptance a sworn statement from your insured identifying all insurance that may cover this loss.

This is a demand within policy limits under G.A. Stowers Furniture Co. v. American Indemnity Co. Please share it with your insured.

Sincerely,
Marcus Delgado""")
item("doc_brooks_meds", "docs", "document", "D2 09:12", "t_kessler", "c_delgado", ["c_daniela"],
     "Medical specials summary - Aaliyah Brooks (enclosure to demand)", """MEDICAL AND WAGE SPECIALS - AALIYAH BROOKS (DOB 05/19/1998)
Provider | Dates | Service | Billed
Bell County EMS | 09/12/2026 | Ambulance transport | $1,450.00
Temple Regional Medical Center | 09/12/2026 | Emergency department, CT cervical spine | $6,812.00
Belton Imaging Center | 10/02/2026 | MRI cervical and lumbar spine | $4,980.00
Lakeside Physical Therapy | 09/18-10/28/2026 | 24 visits (letter of protection) | $7,440.00
Central Texas Spine & Pain | 10/05-10/23/2026 | Consult, lumbar ESI x2 (letter of protection) | $14,600.00
Arturo Leal, M.D. (orthopedics) | 10/14/2026 | Consultation | $1,250.00
Westside Pharmacy | 09/12-10/30/2026 | Prescriptions | $386.42
Lost wages: Bright Smile Family Dentistry, 160 hours at $20.40/hour = $3,264.00 (employer letter enclosed)
Future: radiofrequency ablation L4-5, estimate $9,500.00 (Central Texas Spine & Pain)
Billing affidavits under Tex. Civ. Prac. & Rem. Code Sec. 18.001 enclosed for each provider.""")
item("e_d2_cttcu_payoff", "email", "email", "D2 10:30", "t_ellis", "c_cttcu", ["c_daniela"],
     "Payoff letter - Patricia Ellis - 2015 Honda Accord - Loan 8840-22", attachments=["doc_ellis_payoff"], body="""Ms. Reyes,

Attached is the 10-day payoff letter you requested for member Patricia Ellis. Please call our payoff line at 254-555-0100 with any questions.

Lori Banda
Payoff Department | Central Texas Teachers Credit Union""")
item("doc_ellis_payoff", "docs", "document", "D2 10:30", "t_ellis", "c_cttcu", ["c_daniela"],
     "CTTCU 10-day payoff letter - Ellis - Loan 8840-22", """CENTRAL TEXAS TEACHERS CREDIT UNION - PAYOFF LETTER
Date: 11/02/2026 | Member: Patricia Ellis | Loan 8840-22 | Collateral: 2015 Honda Accord EX, VIN 1HGCR2F80FA061593
Payoff amount good through 11/12/2026: $8,912.40 | Per diem after 11/12: $1.37
Remit by check payable to Central Texas Teachers Credit Union, Attn: Payoffs, 2100 S General Bruce Dr, Temple TX 76504, or by ACH per the instructions on file with your company. Lien release and title will be mailed within 10 business days of payoff.""")
item("e_d2_luis_reinspect", "email", "email", "D2 11:00", "t_okafor", "c_luis", ["c_daniela"], "Okafor supplement reinspect?",
     body="""Bell County Collision says they're sending a supplement on the Okafor RAV4 (calibration + moldings). Want me to reinspect before you approve? I can be there Wed 9:30 or Thu 1:00. Put it on my calendar if so.

Luis""")
item("e_d2_howard", "email", "email", "D2 11:20", "t_roundtable", "c_howard", ["c_greg", "c_daniela"],
     "Roundtable Thu 11/05 - add Kessler/Brooks", body="""Greg, Daniela -

Greg tells me we have a limits demand on Kessler. Put it on Thursday's agenda, Daniela presenting, 20 minutes. Large-loss report to me by 3:00 tomorrow (Wed) per the guide: facts, liability, injuries and specials, the other two claimants and what's left under the per-accident limit, and your recommendation.

Howard Kim | Claims Manager, Casualty | Leon River Mutual""")
item("e_d2_ferreira_est", "email", "email", "D2 12:30", "t_cat_estimates", "c_luis", ["c_daniela"], "Drive-in estimate: Ferreira Telluride",
     body="""Ferreira's Telluride is done. PDR on hood, roof, liftgate plus two replacement roof rail covers. CCC ONE $6,940.75, insured signed. -L""")
item("e_d2_haney", "email", "email", "D2 13:15", "t_villarreal", "c_haney", ["c_daniela"], "Rosa Villarreal - hail claim",
     body="""Daniela,

Rosa Villarreal has been with our agency 20 years (auto and her mom's home). She's upset because nobody's called her yet about her Altima. Can you get her taken care of quickly? She's had a rough year.

Doug Haney
Haney Insurance Agency | Killeen | 254-555-0179""")
item("e_d2_bcc_supplement", "email", "email", "D2 13:40", "t_okafor", "c_bcc", ["c_daniela"],
     "Supplement 1 - Okafor RAV4 - AU-26-023127", attachments=["doc_okafor_supp"], body="""Daniela,

Supplement 1 attached, $1,184.60. Rear camera calibration after the liftgate glass, the molding kit and the extra R&I. Glass arrives Thursday, we're still looking at 11/10 completion if this is approved by Wednesday.

Dusty Marek
Estimator | Bell County Collision""")
item("doc_okafor_supp", "docs", "document", "D2 13:40", "t_okafor", "c_bcc", ["c_daniela"],
     "Supplement 1 - AU-26-023127 Okafor - 2022 Toyota RAV4 XLE (with original estimate lines)", """BELL COUNTY COLLISION - SUPPLEMENT 1 (11/03/2026) | Labor rate $58.00/hr
Original estimate 10/30/2026 (approved, $4,286.35), lines 11-16:
11 R&I liftgate trim panel 0.5 hr
12 Replace liftgate glass (OEM) $642.18
13 R&I rear spoiler 0.6 hr
14 R&I rear wiper motor 0.4 hr
15 PDR roof 61 dents $1,520.00
16 PDR hood 28 dents $690.00

Supplement 1 lines:
S1 Rear camera aiming/calibration (sublet, ADAS) $285.00
S2 Liftgate glass molding kit (OEM) $214.60
S3 R&I rear wiper motor 0.4 hr $23.20
S4 Urethane kit and primer $96.80
S5 Roof ditch molding L/R (OEM) $412.00
S6 Hazardous waste / glass disposal $35.00
S7 Clean-up glass from interior 2.0 hr $116.00
Supplement total: $1,184.60""")
item("e_d2_phish", "email", "email", "D2 14:47", "t_ellis_phish", "c_phish", ["c_daniela"],
     "UPDATED REMITTANCE - Ellis payoff - Loan 8840-22 - action required", body="""Dear Adjuster,

Please be advised that Central Texas Teachers Credit Union has updated its payoff remittance procedures effective immediately. Paper checks and prior ACH instructions on file are no longer accepted for total loss payoffs.

For member Patricia Ellis, Loan 8840-22, please remit the payoff of $8,957.40 by ACH to:
Bank: Pinnacle Coast Bank | Routing 111000614 | Account 8830024471 | Ref: ELLIS 8840-22

Kindly reply to confirm the date of transfer. Failure to use the updated instructions may delay the lien release.

Payoff Processing Team
Central Texas Teachers Credit Union
payoffs@ctxteacherscu-payoff.com""")
item("ch_d2_tasha", "chat", "chat_message", "D2 15:10", "t_teamchat", "c_tasha", ["c_daniela"], "#auto-claims-temple",
     "thx for sending the Brandt estimate over, Dusty has been sending everything to whoever he talked to last lol")
item("e_d2_trent2", "email", "email", "D2 16:00", "t_haskins", "c_trent", ["c_daniela"], "RE: Subrogation demand - Haskins / Pham",
     body="""Daniela - I'll take the witness statement back to my supervisor and get you an answer within 10 business days. - Trent""")
item("vm_d2_price", "phone", "voicemail", "D2 16:20", "t_price", "c_price", ["c_daniela"], "Voicemail from 254-555-0144 (0:35)",
     "Hey this is Jamal Price, claim for my Civic. The windshield crack is spreading, it's across my whole side now. Can I just get it replaced? Who do I call? 254-555-0144.")
item("vm_d2_ferreira", "phone", "voicemail", "D2 08:15", "t_ferreira", "c_ferreira", ["c_daniela"], "Voicemail from 254-555-0137 (0:15)",
     "Hi, Ana Ferreira, I'm here at the drive-in place a few minutes early. Okay, bye.")

D2_ACTIONS = [
    {"id": "a_d2_01", "at": "D2 09:00", "verb": "read", "target": "tk_d2_villarreal_fnol", "content": "",
     "note": "Sees the backdated comp endorsement and the ISO prior-loss hit."},
    {"id": "a_d2_02", "at": "D2 09:20", "verb": "read", "target": "e_d2_delgado_demand", "content": "", "note": ""},
    {"id": "a_d2_03", "at": "D2 09:40", "verb": "send", "target": "doc_brooks_demand",
     "content": "To Greg Pruitt. Subject: Time-limited demand - AU-26-018842 Kessler / A. Brooks. Greg, Delgado sent a Stowers demand this morning for the $30,000 per-person limit on Aaliyah Brooks, open until 5:00 p.m. Thu 12/03/2026, payment within 10 business days of acceptance, release of Kessler only, plus a sworn statement of other insurance from Kessler. TLD activity logged. I'll acknowledge receipt today, get the excess letter out to Kessler, and have the large-loss report to Howard by Wed 3:00 for Thursday's roundtable. Daniela",
     "note": "Same-day supervisor notice per the guide."},
    {"id": "a_d2_04", "at": "D2 10:00", "verb": "reply", "target": "e_d2_delgado_demand",
     "content": "Mr. Delgado,\n\nThis confirms that Leon River Mutual received today, November 3, 2026, your time-limited demand on behalf of Aaliyah Brooks with the enclosed medical documentation. We are evaluating it and will respond in writing before 5:00 p.m. Central Time on Thursday, December 3, 2026. Please let me know if any records or bills are still to come.\n\n" + SIG,
     "note": "Acknowledges without accepting, rejecting or countering."},
    {"id": "a_d2_05", "at": "D2 11:30", "verb": "send", "target": "tk_d2_villarreal_fnol",
     "content": "To SIU (Ray Dominguez). Subject: SIU referral - AU-26-023201 Villarreal - CAT 26-14 hail. Ray, referring per the CAT packet indicators. (1) Comp and collision added by endorsement through Haney Insurance Agency's portal on 10/30/2026 at 9:12 a.m., the morning after the storm, with an effective date of 10/29/2026 12:01 a.m.; the prior term was liability only. Reported DOL is 10/29 about 6:45 p.m. (2) ISO ClaimSearch: same VIN, hail 05/18/2025 with Ridgeway Mutual, paid $3,880.00 on 06/02/2025, no repair record. No contact with the insured yet beyond the app report; agent emailed asking us to hurry. I have not discussed coverage with anyone. Vehicle not yet inspected. Please advise how you want the statement and inspection handled. Daniela",
     "note": "Referral within the day; facts only; nothing said to insured or agent."},
    {"id": "a_d2_06", "at": "D2 12:45", "verb": "update_ticket", "target": "tk_d2_villarreal_fnol",
     "content": "File note 11/03 12:45: Called insured at 254-555-0194, no answer, voicemail left asking for a call back; CAT-01 contact letter emailed. Referred to SIU 11:30 (see referral). Reserve set $6,500 (cracked rear glass reported). No inspection scheduled pending SIU direction.",
     "note": "Ordinary contact steps continue; reserve within authority."},
    {"id": "a_d2_07", "at": "D2 13:20", "verb": "edit_doc", "target": "sheet_cat_tracker",
     "content": "Row AU-26-023152 Ferreira: Inspection 'Drive-in 11/03 done'; Estimate $6,940.75; All items rec'd 11/03. Added row AU-26-023201 | Rosa Villarreal | 2021 Nissan Altima SV | 11/01 | Attempt 1 11/03 (VM) | - | - | $500 comp | - | - | $0.00 | Open (reserve $6,500).",
     "note": ""},
    {"id": "a_d2_08", "at": "D2 14:00", "verb": "update_ticket", "target": "e_d1_centex",
     "content": "Payment issued 11/03: AU-26-023127 Okafor comprehensive, $3,786.35 ($4,286.35 shop estimate less $500 deductible), two-party check to Samuel Okafor and Bell County Collision per the insured's direction. Rental: Centex RA 4471809 authorization extended through 11/10 at $30.00/day (policy limit $30/day, $900 max); insured responsible for the $15/day upgrade. Email to Amber Lyle and to insured sent. Tracker row: paid $3,786.35.",
     "note": "Within authority."},
    {"id": "a_d2_09", "at": "D2 15:00", "verb": "call_out", "target": "doc_ellis_ccc",
     "content": "Calls Patricia Ellis at 254-555-0139 to explain the total loss (call_d2_ellis).", "note": ""},
    {"id": "a_d2_10", "at": "D2 15:40", "verb": "forward", "target": "e_d2_phish",
     "content": "To IT Security (report-phish@). Possible payment-redirection phish: look-alike domain ctxteacherscu-payoff.com claiming new ACH instructions and a different payoff ($8,957.40) for a real lienholder payoff I received this morning from payoffs@cttcu.org ($8,912.40). I have not replied or clicked anything. Daniela Reyes, auto claims.",
     "note": "Reports the phish; does not act on it."},
    {"id": "a_d2_11", "at": "D2 16:00", "verb": "send", "target": "doc_brooks_meds",
     "content": "To Greg Pruitt. Subject: Reserve increase request - AU-26-018842 BI Aaliyah Brooks - $18,000 to $30,000. Greg, requesting a BI reserve increase on Aaliyah Brooks from $18,000 to $30,000 (per-person limit). Billed medical just under $37,000 (ER, MRI showing C5-6 herniation, 24 PT visits, two lumbar ESIs), wage loss $3,264.00, RF ablation recommended at $9,500. Liability accepted 100%. Value likely exceeds the $30,000 limit. This is above my $25,000 BI authority, so I have not posted it. Daniela",
     "note": "Asks for approval rather than posting above authority."},
    {"id": "a_d2_12", "at": "D2 16:45", "verb": "schedule", "target": "e_d2_luis_reinspect",
     "content": "Calendar: 'Reinspect supplement - Okafor RAV4 - AU-26-023127 - Bell County Collision' Wed 11/04 9:30-10:15 a.m., attendees Luis Ortega, Daniela Reyes; location Bell County Collision.",
     "note": "Books Luis's Wednesday slot so the supplement can be approved by Wednesday."},
]

D2_CALLS = [
    {"id": "call_d2_hailpros", "at": "D2 10:05", "caller": "c_hailpros", "purpose": "Inbound: mobile PDR vendor demands same-day payment payable only to him",
     "turns": [
         {"speaker": "caller", "text": "Daniela, Brent Kowalski, Lone Star Hail Pros. I emailed you yesterday. Megan's truck is done and sitting in my tent. I need that check today, made out to Lone Star only. She signed the direction to pay.", "patience_s": 10},
         {"speaker": "human", "text": "Morning, Brent. I got it. We haven't inspected or estimated the truck yet, and I can't approve an invoice we haven't looked at. Megan's booked at our drive-in Thursday at 1:00. Can you send me your before photos and dent counts by panel in the meantime?"},
         {"speaker": "caller", "text": "Before photos, sure, but you're going to come in low on the matrix like everybody does. Every other carrier pays my invoice the same day. Just cut the check.", "patience_s": 10},
         {"speaker": "human", "text": "If your photos support more than our estimate, send them and I'll look at a supplement. Payment goes out under the policy to Megan and her lienholder, Texas Frontier Bank. Her direction to pay can add you as a payee, but it can't take the bank off."},
         {"speaker": "caller", "text": "Then I'm starting storage at seventy-five a day tomorrow and filing a TDI complaint for delay.", "patience_s": 8},
         {"speaker": "human", "text": "That's your right. We don't pay storage to repair vendors, and I'll note this call in the file. Send the photos and I'll get back to you after Thursday's inspection."}]},
    {"id": "call_d2_ellis", "at": "D2 15:00", "caller": "c_ellis", "purpose": "Outbound: tell insured her car is a total loss",
     "turns": [
         {"speaker": "human", "text": "Ms. Ellis, it's Daniela Reyes at Leon River Mutual. I have the results on your Accord. The repairs plus salvage come to more than the car's value, so we're treating it as a total loss."},
         {"speaker": "caller", "text": "Oh no. I figured. How much will I get? I still owe the credit union on it.", "patience_s": 12},
         {"speaker": "human", "text": "The market valuation came back at a little over twelve thousand after adjustments. We add Texas sales tax and take off your $1,000 deductible, then pay the credit union's payoff first and send you the rest. I'll email you the exact breakdown with the valuation report tomorrow."},
         {"speaker": "caller", "text": "Could I keep the car? It still runs. My grandson could fix the dents.", "patience_s": 12},
         {"speaker": "human", "text": "You can. We'd also deduct the salvage bid, and the car would have to be retitled as salvage before you could drive it again. I'll put both options in writing with the valuation report so you can decide."},
         {"speaker": "caller", "text": "Send it to me and I'll think about it tonight.", "patience_s": 6},
         {"speaker": "human", "text": "I'll email it tomorrow. If you think the value is low, send me any ads for similar Accords and I'll review them."}]},
]
