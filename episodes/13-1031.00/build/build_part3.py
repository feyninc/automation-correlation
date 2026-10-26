# Part 3: Wednesday to Friday.
from build_part1 import item, SIG

# ======================= D3 Wednesday 11/04 =======================
item("e_d3_crash_report", "email", "email", "D3 08:00", "t_pickett", "c_brianna", ["c_daniela"],
     "CR-3 posted - Pickett AU-26-023288", attachments=["doc_pickett_cr3"],
     body="Pickett crash report came in overnight, it's in OnBase and attached. -Brianna")
item("doc_pickett_cr3", "docs", "document", "D3 08:00", "t_pickett", "c_brianna", ["c_daniela"],
     "Texas Peace Officer's Crash Report (CR-3) - Temple PD - 10/31/2026 - S 31st St", """TEXAS PEACE OFFICER'S CRASH REPORT (CR-3) - TEMPLE POLICE DEPARTMENT
Crash date/time: 10/31/2026 21:47 | Location: 1400 block S 31st St, Temple, Bell County | Reported: 21:52 | Officer arrived: 22:01 (Ofc. J. Brandvold #412)
Unit 1: 2018 Chevrolet Equinox, owner PICKETT, LORRAINE M, 1416 S 31st St. DRIVER: PICKETT, CODY R, DOB 04/22/2005, TX DL class C. Driver injury: not injured. Insurance shown: Leon River Mutual PA-TX-3398815.
Unit 2: 2014 Ford Focus, parked and unoccupied, owner OCHOA, MARIBEL, 1419 S 31st St.
Other property: mailbox, 1418 S 31st St.
Narrative: Unit 1 was northbound in the 1400 block of S 31st St. Driver of Unit 1 stated an animal ran into the roadway and he swerved right, striking the parked Unit 2 and a mailbox. Witness Dale Henderson (1418 S 31st St) stated he heard the crash and saw the male driver get out of the driver's door. Owner of Unit 1 (driver's mother) arrived on foot from 1416 approx. 5 minutes after the crash. No signs of impairment observed. Exchange-of-information form given to driver of Unit 1.
Contributing factor: driver inattention; evasive action (animal).""")
item("e_d3_cat_stats", "email", "email", "D3 08:05", "t_cat_stats", "c_renee", ["c_daniela", "c_colton", "c_tasha", "c_greg"],
     "CAT 26-14 daily numbers - Wed 11/04 (FYI)", body="""FYI, no action needed.

CAT 26-14 as of 7:00 a.m. Wed 11/04:
Auto comprehensive reported: 1,741 | Property: 1,150
Auto inspected: 748 | Auto paid: 487 claims, $2,669,108 | Average auto severity (paid): $5,481
Total losses identified: 63

Reminder: decision-due column by noon today.

Renee""")
item("e_d3_greg_reserve", "email", "email", "D3 08:20", "t_kessler", "c_greg", ["c_daniela"],
     "RE: Reserve increase request - AU-26-018842 BI Aaliyah Brooks", body="""Approved. I posted the $30,000 on the Brooks BI exposure this morning. Get Howard the report by 3:00 and make sure the excess letter goes to Kessler.

Greg""")
item("vm_d3_ochoa", "phone", "voicemail", "D3 08:40", "t_pickett", "c_ochoa", ["c_daniela"], "Voicemail from 254-555-0126 (0:40)",
     "Hi, this is Maribel Ochoa, my Focus got hit Saturday night on 31st Street by the Picketts' car. Their son's car. I need to know when you're going to fix it, I need it for work. My shop says about twenty-six hundred. 254-555-0126.")
item("e_d3_jordan", "email", "email", "D3 09:30", "t_kessler_jordan", "c_jordan", ["c_daniela"], "my claim - Jordan Brooks",
     body="""Hi Ms Reyes,

I finished PT last week, the doctor released me on 10/28. I have all my bills now, total is $6,184 (ER $2,140, xrays $354, chiro/PT $3,690, I scanned them all into the portal). I just want to get this done, I don't have a lawyer and don't want one. What can you offer? Also is my sister's lawyer going to take all the insurance money? Somebody told me there's a limit.

Thanks
Jordan Brooks
254-555-0122""")
item("ch_d3_luis", "chat", "chat_message", "D3 10:20", "t_okafor", "c_luis", ["c_daniela"], "#auto-claims-temple",
     "reinspect done on okafor rav4. calibration is legit (they have the target setup), moldings legit, glass mess legit. photos uploaded. didn't have time to go line by line against the original, all yours")
item("e_d3_renee_reminder", "email", "email", "D3 11:00", "t_cat", "c_renee", ["c_daniela", "c_colton", "c_tasha"],
     "Reminder: decision-due column by noon", body="One hour. Thanks! - Renee")
item("e_d3_delgado_fu", "email", "email", "D3 11:05", "t_kessler", "c_yesenia", ["c_daniela"], cc=["c_delgado"],
     subject="RE: STOWERS DEMAND - Aaliyah Brooks - AU-26-018842", body="""Ms. Reyes,

Thank you for confirming receipt. Mr. Delgado asked me to let you know that Ms. Brooks is scheduled for the radiofrequency ablation on November 19. We will forward those records when available.

Yesenia Ruiz
Paralegal | Delgado & Finch PLLC""")
item("e_d3_ellis_q", "email", "email", "D3 12:15", "t_ellis", "c_ellis", ["c_daniela"], "my Accord",
     body="""Hi Daniela,

Thank you for calling yesterday. I talked to my grandson and we don't want to keep the car, it's too much work. Please go ahead with the regular way. Can you send me the numbers in writing so I know exactly what I'm getting and what goes to the credit union?

Pat Ellis""")
item("e_d3_centex_inv", "email", "email", "D3 13:20", "t_okafor_rental", "c_centex", ["c_daniela"],
     "Direct-bill invoices - RA 4471809 - Okafor", attachments=["doc_centex_inv"], body="""Daniela,

Attached are the direct-bill invoices through 11/02 for RA 4471809. Please remit at your convenience.

Amber Lyle | Centex Rent-A-Car, Temple""")
item("doc_centex_inv", "docs", "document", "D3 13:20", "t_okafor_rental", "c_centex", ["c_daniela"],
     "Centex invoices CX-88213 and CX-88231 - RA 4471809", """CENTEX RENT-A-CAR - DIRECT BILL INVOICE CX-88213 (issued 11/03/2026)
Bill to: Leon River Mutual, claim AU-26-023127 | Renter: Samuel Okafor | RA 4471809
Period: 10/30/2026 - 11/02/2026, 4 days x $30.00 (insurer authorized rate) = $120.00 | Tax/fees billed to renter
Amount due: $120.00

CENTEX RENT-A-CAR - DIRECT BILL INVOICE CX-88231 (issued 11/03/2026)
Bill to: Leon River Mutual, claim AU-26-023127 | Renter: Samuel Okafor | RA 4471809
Period: 10/30/2026 - 11/02/2026, 4 days x $30.00 (insurer authorized rate) = $120.00 | Tax/fees billed to renter
Amount due: $120.00""")
item("ch_d3_colton", "chat", "chat_message", "D3 14:20", "t_teamchat", "c_colton", ["c_daniela"], "#auto-claims-temple",
     "you presenting kessler at roundtable tmrw? howard moved mine to after yours. 2:20ish")
item("e_d3_hailpros2", "email", "email", "D3 15:50", "t_albrecht", "c_hailpros", ["c_daniela"],
     "FINAL NOTICE - Albrecht - storage accruing", body="""Daniela,

Storage on the Albrecht F-150 started today at $75/day. Your insured can't pick up the truck until our invoice of $7,860.00 is paid. Issue payment to Lone Star Hail Pros today and we'll waive storage. Otherwise I'm sending my complaint to TDI tonight.

Brent Kowalski | Lone Star Hail Pros LLC""")
item("tk_d3_ochoa_pd", "tickets", "ticket", "D3 16:40", "t_pickett", "c_fnol", ["c_daniela"],
     "Activity: third-party PD estimate received - AU-26-023288 Ochoa Focus",
     "ClaimCenter activity. Claimant Maribel Ochoa uploaded an estimate from Westfield Auto Body for her 2014 Ford Focus: $2,640.18 (right rear door, quarter panel, bumper cover). Review and respond.")
item("vm_d3_sutton", "phone", "voicemail", "D3 07:55", "t_sutton", "c_sutton", ["c_daniela"], "Voicemail from 254-555-0131 (0:12)",
     "Hi, Brenda Sutton, just confirming I'm still on for 8:30 at the drive-in this morning. Thanks.")
item("e_d3_sutton_est", "email", "email", "D3 11:45", "t_cat_estimates", "c_luis", ["c_daniela"], "Drive-in estimate: Sutton CX-5",
     body="Sutton CX-5 done, light, all PDR. CCC ONE $2,244.00, insured signed. -L")
item("vm_d3_price", "phone", "voicemail", "D3 12:40", "t_price", "c_price", ["c_daniela"], "Voicemail from 254-555-0144 (0:18)",
     "It's Jamal Price. I called the glass number you gave me, they're coming Monday the ninth to do the windshield. Thanks.")

D3_ACTIONS = [
    {"id": "a_d3_01", "at": "D3 09:00", "verb": "read", "target": "doc_pickett_cr3", "content": "",
     "note": "The crash report names Cody as the driver, contradicting Monday's recorded statement."},
    {"id": "a_d3_02", "at": "D3 09:20", "verb": "call_out", "target": "vm_d2_price",
     "content": "Calls Jamal Price: gives him the LRM glass line and confirms the windshield is covered under comprehensive, $500 deductible applies to the whole claim once; books drive-in for the hail Fri 11/06 3:00 p.m. File note entered.",
     "note": ""},
    {"id": "a_d3_03", "at": "D3 10:00", "verb": "noop", "target": "cal_d0_1on1",
     "content": "1:1 with Greg: raises the Pickett crash report and the Villarreal SIU referral; Greg asks for the Pickett facts in writing today.",
     "note": "Meeting; outcome stated in the next action."},
    {"id": "a_d3_04", "at": "D3 10:40", "verb": "send", "target": "doc_pickett_cr3",
     "content": "To Greg Pruitt. Subject: Coverage question - AU-26-023288 Pickett - excluded driver. Greg, as discussed: the Temple PD CR-3 lists Cody R. Pickett (DOB 04/22/2005) as the driver of the insured Equinox on 10/31, and witness Dale Henderson saw the male driver get out of the driver's door; the mother arrived on foot about 5 minutes later. Cody is a named excluded driver (LRM-TX-NDE, signed 03/12/2025). In her recorded statement on 11/02 Lorraine said she was driving and Cody was the passenger. Features: collision on the Equinox and liability PD for Ochoa's Focus ($2,640.18 estimate received today) and the Henderson mailbox. I'm holding all payments. Recommend coverage counsel review, a reservation of rights to the insured, and an SIU referral for the conflicting statement. I have not discussed coverage with the insured or Ms. Ochoa. Daniela",
     "note": "Escalates the coverage defense with facts; does not decide it."},
    {"id": "a_d3_05", "at": "D3 11:00", "verb": "edit_doc", "target": "sheet_cat_tracker",
     "content": "542.056 decision due column: Okafor AU-26-023127 (all items 10/30) -> 11/23/2026; Hollis AU-26-023140 (10/31) -> 11/23/2026 (accepted and paid 10/31); Patel AU-26-023119 (11/02) -> 11/24/2026 (accepted and paid 11/02); Ferreira AU-26-023152 (11/03) -> 11/25/2026. Counted 15 business days excluding Sat/Sun and Veterans Day 11/11 (Gov't Code 662.003). Ellis, Albrecht, Wynn, Sutton, Price, Villarreal: items outstanding, no date yet.",
     "note": "Exact dates with the Veterans Day holiday excluded."},
    {"id": "a_d3_06", "at": "D3 11:30", "verb": "reply", "target": "e_d2_bcc_supplement",
     "content": "Dusty,\n\nSupplement 1 on the Okafor RAV4 is approved at $1,161.40. Line S3 (R&I rear wiper motor 0.4 hr, $23.20) duplicates line 14 on the original estimate we already paid, so it's removed. Luis confirmed the calibration, molding kit and glass clean-up at reinspection this morning. Payment goes out today. Please keep me posted on the 11/10 completion date since the rental runs off it.\n\n" + SIG,
     "note": "Catches the duplicated labor line."},
    {"id": "a_d3_07", "at": "D3 12:30", "verb": "update_ticket", "target": "e_d3_sutton_est",
     "content": "Payments 11/04: (1) AU-26-023127 Okafor supplement 1, $1,161.40 to Samuel Okafor and Bell County Collision (Okafor paid to date $4,947.75). (2) AU-26-023152 Ferreira, $5,940.75 ($6,940.75 less $1,000 deductible) to Ana Ferreira, acceptance letter sent; closed. Sutton estimate $2,244.00 received; payment to follow after insured confirms no lienholder. Tracker updated: Okafor paid $4,947.75; Ferreira paid $5,940.75, Closed 11/04; Sutton estimate $2,244.00, all items 11/04.",
     "note": "Within authority."},
    {"id": "a_d3_08", "at": "D3 14:00", "verb": "create_doc", "target": "doc_brooks_meds",
     "content": "LARGE LOSS REPORT - AU-26-018842 Kessler / Aaliyah Brooks - Roundtable 11/05/2026 - D. Reyes\n1. Demand: Stowers demand for the $30,000 per-person BI limit, received 11/03, expires 5:00 p.m. CT Thu 12/03/2026; payment within 10 business days of acceptance; release of Wade Kessler only, no indemnity; sworn statement of other insurance from the insured.\n2. Coverage: PA-TX-4417203, BI 30/60, PD 25 (PD paid $24,948.14, closed). Coverage confirmed; no defenses.\n3. Liability: insured rear-ended the Brooks Civic on I-35 in rain, pushing it into the Salinas Camry; cited for failure to control speed; liability accepted 100% on 09/16.\n4. Injuries: ER by ambulance; MRI 10/02 C5-6 herniation with foraminal narrowing and L4-5 protrusion; 24 PT visits; lumbar ESIs 10/09 and 10/23; RF ablation recommended (scheduled 11/19), estimate $9,500.\n5. Specials (billed): EMS $1,450.00; Temple Regional ER $6,812.00; Belton Imaging MRI $4,980.00; Lakeside PT $7,440.00 (LOP); Central Texas Spine & Pain $14,600.00 (LOP); Dr. Leal $1,250.00; pharmacy $386.42. Total billed medical $36,918.42. Wage loss $3,264.00 (160 hr x $20.40). Total specials $40,182.42 plus $9,500 future. Paid-vs-billed (CPRC 41.0105) unknown for the two LOP providers.\n6. Other claimants (per-accident limit $60,000): Jordan Brooks, unrepresented, specials $6,184.00, released 10/28, evaluating at $7,000-$8,500; Hector Salinas, unrepresented, chiropractic about $3,100, evaluating at $4,000-$5,000. A $30,000 payment to Aaliyah leaves $30,000 for both, above their combined value.\n7. Evaluation: verdict range in Bell County with herniation, injections and recommended ablation is above $30,000; excess exposure to the insured is real.\n8. Recommendation: accept the demand and tender the $30,000 per-person limit before 12/03, release reviewed by staff counsel; excess letter sent to insured; obtain the insured's sworn statement of other insurance.",
     "note": "Report for the Roundtable; medical total computed exactly."},
    {"id": "a_d3_09", "at": "D3 14:45", "verb": "send", "target": "e_d2_howard",
     "content": "To Howard Kim, cc Greg Pruitt. Subject: Large loss report - Kessler / Brooks - Roundtable 11/05. Howard, report attached for tomorrow. Short version: limits demand $30,000 open to 12/03 5:00 p.m.; liability 100%; billed medical $36,918.42 plus RF ablation; my recommendation is to accept and tender the per-person limit. Daniela",
     "note": "Meets the 3:00 deadline."},
    {"id": "a_d3_10", "at": "D3 15:10", "verb": "reply", "target": "e_d3_ellis_q",
     "content": "Ms. Ellis,\n\nThank you for letting me know. Here is the settlement for your 2015 Honda Accord (claim AU-26-023114), with the CCC ONE valuation report attached:\n\nAdjusted vehicle value: $12,265.00\nTexas motor vehicle sales tax (6.25%): $766.56\nLess comprehensive deductible: -$1,000.00\nTotal settlement: $12,031.56\nPaid to Central Texas Teachers Credit Union (payoff good through 11/12): $8,912.40\nPaid to you: $3,119.16\n\nTitle and registration fees are reimbursed separately if you buy a replacement vehicle within 30 days; just send me the receipt. To finish, please e-sign the power of attorney and odometer statement I'm sending through DocuSign. Heart of Texas Auto Auction will pick the car up from your home; I'll have them call you. If you believe the value is low, send me listings for similar cars, and you also have the appraisal option in your policy. You may contact the Texas Department of Insurance at 800-252-3439 with any concern.\n\n" + SIG,
     "note": "Itemized total-loss letter."},
    {"id": "a_d3_11", "at": "D3 16:20", "verb": "reply", "target": "e_d3_hailpros2",
     "content": "Brent,\n\nAs I said Tuesday, we will inspect the truck at our drive-in Thursday 1:00 p.m. (Megan has the appointment) or, if it can't be moved, at your tent. Payment will be based on our estimate and any supplement your photos support, issued to Megan Albrecht and Texas Frontier Bank under the policy's loss-payable clause, with your company added as a payee per her direction to pay. LRM does not pay storage to repair vendors. You're welcome to contact TDI; this correspondence is in the file.\n\n" + SIG,
     "note": "Firm, no commitment to his invoice."},
    {"id": "a_d3_12", "at": "D3 16:45", "verb": "update_ticket", "target": "tk_d3_ochoa_pd",
     "content": "File note 11/04 16:45: Ochoa estimate $2,640.18 received. Liability PD feature on hold pending coverage review (see email to G. Pruitt 10:40). Called claimant 254-555-0126: told her we received her estimate and are still completing our investigation, will update her by early next week; suggested she use her own collision coverage if she has it. No coverage statement made.",
     "note": ""},
]

D3_CALLS = [
    {"id": "call_d3_delgado", "at": "D3 15:30", "caller": "c_delgado", "purpose": "Inbound: claimant attorney presses for an immediate written answer on the limits demand",
     "turns": [
         {"speaker": "caller", "text": "Ms. Reyes, Marcus Delgado. I'll be direct. You've got a herniated disc, two injections and an ablation coming on a thirty-thousand-dollar policy. My client wants this done. I need your acceptance in writing today, tomorrow at the latest, or I'm telling her to file Monday.", "patience_s": 12},
         {"speaker": "human", "text": "I understand. Your letter gives us until 5:00 p.m. on Thursday, December 3, and we'll respond in writing before then. It's being reviewed by management this week."},
         {"speaker": "caller", "text": "So are you rejecting it? Because if you're sitting on a limits demand with these records, your insured's going to have a problem, and so are you.", "patience_s": 10},
         {"speaker": "human", "text": "No, we are not rejecting it. It's under review, and you'll have our written response before the deadline. If you have the ablation records or anything else, send them and they'll be considered."},
         {"speaker": "caller", "text": "Fine. I'll hold until December 3. Not a minute longer.", "patience_s": 6},
         {"speaker": "human", "text": "Understood. Thank you, Mr. Delgado."}]},
    {"id": "call_d3_hector", "at": "D3 16:05", "caller": "c_hector", "purpose": "Inbound: third-party BI claimant asks about another claimant's injuries and the limits",
     "turns": [
         {"speaker": "caller", "text": "Hi, Hector Salinas, from the wreck on 35 in September. My chiropractor's done. But I heard the girl in the Honda has a lawyer and is getting surgery. Is she getting all the insurance money? How much is she getting? Is there going to be anything left for me?", "patience_s": 12},
         {"speaker": "human", "text": "Hi Mr. Salinas. I can't discuss anyone else's claim or medical care, the same way I wouldn't discuss yours with them. Your claim is separate, and I'm handling it. Let's talk about where you are."},
         {"speaker": "caller", "text": "Okay but just tell me what the policy limit is so I know.", "patience_s": 10},
         {"speaker": "human", "text": "I'm not able to share the policy details without our insured's permission. What I can do is evaluate your claim as soon as I have your final bills and records. Has the chiropractor sent you an itemized final bill?"},
         {"speaker": "caller", "text": "I have it, it's like thirty-one hundred. I can take a picture.", "patience_s": 8},
         {"speaker": "human", "text": "Please upload it to the portal or email it to me, along with any time you missed from work. Once I have it I'll call you with an offer, usually within a few days."}]},
]

# ======================= D4 Thursday 11/05 =======================
item("vm_d4_ellis", "phone", "voicemail", "D4 07:45", "t_ellis", "c_ellis", ["c_daniela"], "Voicemail from 254-555-0139 (0:26)",
     "Daniela, Pat Ellis. I signed the papers on the computer this morning, the DocuSign. The numbers are fine. Thank you for explaining it. Bye-bye.")
item("e_d4_cat_stats", "email", "email", "D4 08:05", "t_cat_stats", "c_renee", ["c_daniela", "c_colton", "c_tasha", "c_greg"],
     "CAT 26-14 daily numbers - Thu 11/05 (FYI)", body="""FYI, no action needed.

CAT 26-14 as of 7:00 a.m. Thu 11/05:
Auto comprehensive reported: 1,866 | Property: 1,212
Auto inspected: 927 | Auto paid: 640 claims, $3,540,640 | Average auto severity (paid): $5,532
Total losses identified: 78

Renee""")
item("e_d4_renee_request", "email", "email", "D4 09:00", "t_cat_report", "c_renee", ["c_daniela", "c_colton", "c_tasha"],
     "Need your CAT inventory numbers by Fri noon", body="""Hi all,

For Howard's Friday CAT report, please send me by noon Friday, from your inventory sheet as of Thursday close:
1. CAT 26-14 files assigned to you (total), open, and closed;
2. Total indemnity paid to date on your CAT files (vehicle damage net of deductible; exclude rental and expense);
3. Any total losses and any files referred to SIU (count only).

Thanks,
Renee""")
item("e_d4_ray", "email", "email", "D4 08:30", "t_villarreal", "c_ray", ["c_daniela"], "RE: SIU referral - AU-26-023201 Villarreal",
     body="""Daniela,

Thanks, good referral. SIU accepts. I'll handle the recorded statement and the vehicle inspection (I want to see it before anything is touched; I've asked Luis to do it with me next week). Pulled the Ridgeway Mutual file; their 2025 payment was for roof, hood and trunk.

From your side: keep your normal contact going, and send her our standard letter that we've received her claim and the investigation is continuing and we'll be in touch to schedule an inspection. Please get it out by Friday. Do not mention SIU or the endorsement to her or the agent. If the agent calls, the claim is under investigation, period.

Ray Dominguez | SIU Investigator | Leon River Mutual | 254-555-0109""")
item("tk_d4_albrecht", "tickets", "ticket", "D4 08:00", "t_albrecht", "c_fnol", ["c_daniela"],
     "Activity: drive-in inspection today 1:00 p.m. - AU-26-023131 Albrecht",
     "ClaimCenter activity. Insured Megan Albrecht confirmed she will bring the F-150 from Lone Star Hail Pros to the drive-in at 1:00 p.m. today. Appraiser: L. Ortega.")
item("e_d4_kessler", "email", "email", "D4 08:50", "t_kessler", "c_kessler", ["c_daniela"], "Anything new?",
     body="""Hi Daniela,

Just checking in on the claims from the September wreck. I haven't heard anything in a few weeks. Is everything ok? Do I need to do anything?

Wade""")
item("ch_d4_brianna", "chat", "chat_message", "D4 09:40", "t_teamchat", "c_brianna", ["c_daniela"], "#auto-claims-temple",
     "Lorraine Pickett called the main line twice this morning asking if her car is covered. I told her you'd call her back, she sounded upset")
item("e_d4_luis_alb", "email", "email", "D4 13:45", "t_albrecht", "c_luis", ["c_daniela"], "Albrecht F-150 estimate",
     attachments=["doc_albrecht_est"], body="""Daniela - looked at the F-150 at 1:00. Repairs are already done (nice work actually, he's good). Wrote it off his before photos plus what I could see: our matrix comes to $6,212.50. The difference to his invoice is mostly the aluminum surcharge and his roof count (he says 210 dents, his own photos show about 160). I told Megan you'd call. -L""")
item("doc_albrecht_est", "docs", "document", "D4 13:45", "t_albrecht", "c_luis", ["c_daniela"],
     "CCC ONE estimate - AU-26-023131 Albrecht - 2020 Ford F-150 XLT", """CCC ONE ESTIMATE (LRM drive-in, appraiser L. Ortega, 11/05/2026 1:38 p.m.; repairs completed before inspection; written from vendor before-photos and post-repair inspection)
PDR per 2026 LRM hail matrix (aluminum panels, matrix aluminum factor applied): hood $1,320.00; roof (approx. 160 dents per photos) $1,985.00; cab corners and doors $1,610.00; bed sides $1,447.50; R&I headliner $350.00; aluminum surcharge included in matrix $0.00; sublet $0.00; parts $0.00; adjustments -$500.00 (roof rail R&I not required on this cab)
Gross total $6,212.50 | Comp deductible $500.00 | Net $5,712.50 | Lienholder: Texas Frontier Bank""")
item("e_d4_howard_approval", "email", "email", "D4 15:10", "t_roundtable", "c_howard", ["c_daniela", "c_greg", "c_elaine"],
     "Roundtable decision - Kessler / Brooks", body="""Roundtable decision 11/05:

AU-26-018842 Kessler / Aaliyah Brooks: APPROVED to accept the 11/03 demand and tender the $30,000 per-person BI limit. Elaine to review the release language today. Daniela to send the acceptance letter to Delgado once Elaine clears the release, and to get Mr. Kessler's sworn statement of other insurance. Payment within the demand's 10 business days.

Good report, Daniela.

Howard""")
item("e_d4_elaine_release", "email", "email", "D4 15:35", "t_roundtable", "c_elaine", ["c_daniela"], cc=["c_greg"],
     subject="RE: Roundtable decision - Kessler / Brooks - release", attachments=["doc_brooks_release"], body="""Daniela,

Release attached. It meets his terms (insured only, no indemnity, no confidentiality, UIM carve-out). OK to send with your acceptance letter. Keep the acceptance unconditional except for the release and the payee he specified.

Elaine Whitcomb | Staff Counsel | Leon River Mutual""")
item("doc_brooks_release", "docs", "document", "D4 15:35", "t_roundtable", "c_elaine", ["c_daniela"],
     "Release of all claims - Aaliyah Brooks v. Wade Kessler (approved form)", """RELEASE OF ALL CLAIMS
For $30,000.00, Aaliyah Brooks releases Wade Kessler from all claims for bodily injury arising from the 09/12/2026 collision on I-35 in Temple, Texas. This release does not release any claim against any underinsured motorist carrier. No indemnity, no confidentiality. Payable to "Aaliyah Brooks and Delgado & Finch PLLC." Approved by E. Whitcomb 11/05/2026.""")
item("e_d4_greg_ror", "email", "email", "D4 16:30", "t_pickett", "c_greg", ["c_daniela"], "RE: Coverage question - AU-26-023288 Pickett",
     body="""Daniela,

Talked with Elaine this afternoon. The exclusion looks like it applies if Cody was driving, and the CR-3 plus the neighbor make that likely. We'll reserve rights rather than deny today, because we still have conflicting accounts and we want Cody's statement. Draft the ROR letter to Lorraine for my signature (cite the NDE endorsement language, the facts so far, what we still need, that we're continuing to investigate under a full reservation, and that she can call me) and get it to me by end of day Friday. Also send the SIU referral on the statement conflict.

Don't tell Lorraine or Ms. Ochoa anything about coverage until the letter is signed. If Lorraine calls, it's still under review.

Greg""")
item("vm_d4_ochoa", "phone", "voicemail", "D4 12:10", "t_pickett", "c_ochoa", ["c_daniela"], "Voicemail from 254-555-0126 (0:19)",
     "Hi, Maribel Ochoa again. Just wanted to say thanks for calling yesterday. I'll wait to hear from you. Thanks.")
item("e_d4_hotaa", "email", "email", "D4 11:20", "t_ellis", "c_hotaa", ["c_daniela"], "Pickup scheduled - Ellis Accord",
     body="Ellis Accord pickup scheduled Mon 11/09 between 9 and 12 at her address. Title and POA received from your DocuSign. Thanks! - Kim")
item("e_d4_jordan_bills", "email", "email", "D4 10:55", "t_kessler_jordan", "c_jordan", ["c_daniela"], "RE: my claim - Jordan Brooks",
     body="Also forgot to say I missed 3 days of work at the warehouse, $17/hr 8 hr days. My manager can write a letter. - Jordan")

D4_ACTIONS = [
    {"id": "a_d4_01", "at": "D4 09:00", "verb": "read", "target": "e_d4_ray", "content": "", "note": ""},
    {"id": "a_d4_02", "at": "D4 09:30", "verb": "update_ticket", "target": "vm_d4_ellis",
     "content": "Payment issued 11/05: AU-26-023114 Ellis total loss $12,031.56 (adjusted value $12,265.00 + tax $766.56 - $1,000 deductible). $8,912.40 to Central Texas Teachers Credit Union by check to the payoff address on the 11/02 payoff letter (payoff verified by phone with Lori Banda at 254-555-0100, the number on file, 9:20 a.m.; she confirmed no change to remittance instructions). $3,119.16 to Patricia Ellis by EFT. POA and odometer statement received via DocuSign. Salvage assigned to Heart of Texas Auto Auction (bid $2,350.00). Tracker updated: paid $12,031.56, Open pending title.",
     "note": "Verifies payoff by phone on file; ignores the look-alike email."},
    {"id": "a_d4_03", "at": "D4 11:00", "verb": "send", "target": "e_d4_kessler",
     "content": "To Wade Kessler (email and certified mail). Subject: Important - settlement demand above or at your policy limits - Claim AU-26-018842.\n\nDear Mr. Kessler,\n\nOn November 3, 2026, we received a settlement demand from Marcus Delgado, attorney for Aaliyah Brooks, the driver of the Honda Civic in the September 12, 2026 accident. A copy is enclosed. Ms. Brooks offers to release you from her claim for $30,000, which is your policy's bodily injury limit of $30,000 for each person. The offer is open until 5:00 p.m. on December 3, 2026.\n\nMs. Brooks's claimed damages may exceed your $30,000 per-person limit. If her claim were not resolved within your limits and a judgment exceeded them, you could be personally responsible for the amount above the limits. We are evaluating the demand and will respond before the deadline, and we will keep you informed.\n\nYou have the right to hire your own attorney, at your own expense, to advise you about this. Please also tell us right away about any other insurance that might cover you for this accident, such as an umbrella or excess policy, another auto policy in your household, or coverage through an employer if you were driving for work. The attorney has asked for a sworn statement listing all such insurance; I will send you a short form to sign.\n\nPlease call me with any questions.\n\n" + SIG,
     "note": "Excess-exposure letter within 2 business days of the demand."},
    {"id": "a_d4_04", "at": "D4 11:30", "verb": "call_out", "target": "e_d3_jordan",
     "content": "Calls Jordan Brooks at 254-555-0122 to discuss settlement (call_d4_jordan).", "note": ""},
    {"id": "a_d4_05", "at": "D4 12:05", "verb": "send", "target": "e_d3_jordan",
     "content": "To Jordan Brooks. Subject: Settlement of your claim - AU-26-018842.\n\nHi Jordan,\n\nThanks for talking with me today. As agreed, Leon River Mutual will pay $7,800.00 to settle your bodily injury claim from the September 12, 2026 accident (your medical bills of $6,184.00, three days of missed work, and your pain and inconvenience). The release is attached; please read it, sign it in front of a notary or through the DocuSign link, and return it. Payment will be issued within 5 business days after I receive the signed release. If any health insurer or provider has a lien for your treatment, let me know so it can be included on the check.\n\n" + SIG,
     "note": "Settlement within authority; no information about his sister."},
    {"id": "a_d4_06", "at": "D4 12:15", "verb": "update_ticket", "target": "tk_d0_kessler_review",
     "content": "Reserve change 11/05: BI exposure Jordan Brooks from $6,500 to $7,800 (agreed settlement, within Rep II authority). Release sent 12:05.", "note": ""},
    {"id": "a_d4_07", "at": "D4 13:55", "verb": "edit_doc", "target": "sheet_cat_tracker",
     "content": "Row Albrecht AU-26-023131: Inspection 'Drive-in 11/05 (post-repair)'; Estimate $6,212.50; all items 11/05. Row Ellis: paid $12,031.56; status Open - TL, awaiting title. Row Sutton: paid $1,744.00 ($2,244.00 less $500), Closed 11/05 (no lienholder confirmed 11:40 by phone).",
     "note": ""},
    {"id": "a_d4_08", "at": "D4 14:00", "verb": "noop", "target": "cal_d0_roundtable",
     "content": "Presents Kessler / Brooks at the Large Loss Roundtable (20 minutes).", "note": ""},
    {"id": "a_d4_09", "at": "D4 15:15", "verb": "read", "target": "e_d4_howard_approval", "content": "", "note": "Approval in hand."},
    {"id": "a_d4_10", "at": "D4 16:00", "verb": "send", "target": "e_d4_elaine_release",
     "content": "To Marcus Delgado, cc Yesenia Ruiz. Subject: Acceptance of 11/03/2026 demand - Aaliyah Brooks - AU-26-018842.\n\nMr. Delgado,\n\nOn behalf of our insured Wade Kessler, Leon River Mutual accepts your client's November 3, 2026 offer to release Mr. Kessler from all claims arising from the September 12, 2026 collision in exchange for the $30,000.00 per-person bodily injury limit. The enclosed release follows your terms: it releases Mr. Kessler only, contains no indemnity or confidentiality provisions, and does not release any underinsured motorist claim. Payment of $30,000.00 payable to \"Aaliyah Brooks and Delgado & Finch PLLC\" will be delivered within 10 business days of today. Mr. Kessler's sworn statement of other insurance will follow under separate cover. Please return the signed release and your firm's W-9.\n\n" + SIG,
     "note": "Sent only after the Claims Manager's approval and counsel's release review."},
    {"id": "a_d4_11", "at": "D4 16:40", "verb": "reply", "target": "e_d4_greg_ror",
     "content": "Will do - ROR draft to you tomorrow by end of day, and the SIU referral goes to Ray tomorrow morning. Lorraine has called the main line twice; I'll call her back and keep it to 'still under review.'",
     "note": "Acknowledges; the draft itself slips to Monday (not in this week)."},
    {"id": "a_d4_12", "at": "D4 16:55", "verb": "call_out", "target": "ch_d4_brianna",
     "content": "Calls Lorraine Pickett back: tells her the claim is still under review, that she will get a letter, and that Greg Pruitt or Daniela will follow up; no coverage position stated. File note entered.",
     "note": "Keeps to the script Greg set."},
]

D4_CALLS = [
    {"id": "call_d4_haney", "at": "D4 10:30", "caller": "c_haney", "purpose": "Inbound: agent asks why the Villarreal claim is held up",
     "turns": [
         {"speaker": "caller", "text": "Daniela, Doug Haney. Rosa Villarreal says nobody's scheduled her inspection. Is something wrong with the claim? I put the comp on for her myself, everything's in order.", "patience_s": 10},
         {"speaker": "human", "text": "Hi Doug. The claim is open and under investigation, like every claim from this storm. She'll get a letter from us this week, and we'll contact her to schedule the inspection."},
         {"speaker": "caller", "text": "Under investigation for what? It's a hail claim. Is this about when the endorsement went in? She called me Friday morning and I took care of it.", "patience_s": 10},
         {"speaker": "human", "text": "I can't go into the details of the investigation, Doug. We're handling it in the normal course, and we'll be in touch with Rosa directly."},
         {"speaker": "caller", "text": "Well, she's a good customer. I'd appreciate you moving it along.", "patience_s": 6},
         {"speaker": "human", "text": "Understood. Thanks for calling."}]},
    {"id": "call_d4_jordan", "at": "D4 11:30", "caller": "c_jordan", "purpose": "Outbound: negotiate settlement with an unrepresented BI claimant",
     "turns": [
         {"speaker": "human", "text": "Hi Jordan, Daniela Reyes from Leon River Mutual. I got your email and your bills. Do you have a few minutes to talk about settling your claim?"},
         {"speaker": "caller", "text": "Yeah. I was thinking nine thousand. My neck still gets stiff at work. And did you see my question about my sister?", "patience_s": 12},
         {"speaker": "human", "text": "About your sister, I can't discuss her claim with you; she has her own attorney, and her claim is handled separately. Yours doesn't depend on hers. On yours: your bills are $6,184, and you missed three days at $17 an hour, which is $408. Considering a two-month recovery and a full release on October 28, I can offer $7,200."},
         {"speaker": "caller", "text": "Seventy-two hundred. Can you do better? Eight and a half and we're done today.", "patience_s": 10},
         {"speaker": "human", "text": "I can go to $7,800, and that's the best I can do on this claim. It covers your bills, your lost wages and your pain and inconvenience."},
         {"speaker": "caller", "text": "Okay. Seventy-eight hundred. What do I need to do?", "patience_s": 8},
         {"speaker": "human", "text": "I'll email you a release in the next half hour. Sign it and send it back, and the check goes out within five business days after I get it. If any health insurance paid your bills, tell me so it's included."}]},
    {"id": "call_d4_mabry", "at": "D4 13:05", "caller": "c_mabry", "purpose": "Inbound: claimant on a disputed parking-lot loss demands that the adjuster admit fault",
     "turns": [
         {"speaker": "caller", "text": "This is Terrence Mabry, the Highlander that hit me at Lakeview Plaza. Your lady backed into me, plain and simple. I need you to tell me right now you're accepting liability so my shop can start.", "patience_s": 10},
         {"speaker": "human", "text": "Mr. Mabry, thanks for calling. Our insured gives a different account, so I haven't made a liability decision yet. I'd like to take your recorded statement. Do I have your permission to record?"},
         {"speaker": "caller", "text": "Record whatever you want. I've got a dashcam from my buddy's car parked across the lane. Once you see it you'll know. Just say you'll pay.", "patience_s": 10},
         {"speaker": "human", "text": "The video would help a lot. Please email it to me today, and the names of anyone who saw it. I'll review it with your statement and our insured's, and I'll call you with our decision. Until then I can't say who's at fault. If you have collision coverage, your own insurer can repair your car now and recover from us if we're responsible."},
         {"speaker": "caller", "text": "Fine. I'll send the video.", "patience_s": 6},
         {"speaker": "human", "text": "Thank you. I'll look for it this afternoon."}]},
]

# ======================= D5 Friday 11/06 =======================
item("e_d5_cat_stats", "email", "email", "D5 08:05", "t_cat_stats", "c_renee", ["c_daniela", "c_colton", "c_tasha", "c_greg"],
     "CAT 26-14 daily numbers - Fri 11/06 (FYI)", body="""FYI, no action needed.

CAT 26-14 as of 7:00 a.m. Fri 11/06:
Auto comprehensive reported: 1,957 | Property: 1,266
Auto inspected: 1,104 | Auto paid: 803 claims, $4,486,573 | Average auto severity (paid): $5,587
Total losses identified: 91
Drive-in open Saturday 8-12 for overflow.

Renee""")
item("vm_d5_villarreal", "phone", "voicemail", "D5 07:50", "t_villarreal", "c_villarreal", ["c_daniela"], "Voicemail from 254-555-0194 (0:41)",
     "This is Rosa Villarreal. Doug says there's some kind of problem with my claim. Nobody has even looked at my car. Are you denying it? I pay my insurance every month. Call me back today please, 254-555-0194.")
item("e_d5_delgado_ack", "email", "email", "D5 08:40", "t_kessler", "c_delgado", ["c_daniela"], cc=["c_yesenia"],
     subject="RE: Acceptance of 11/03/2026 demand - Aaliyah Brooks", attachments=["doc_delgado_w9"], body="""Ms. Reyes,

Received, thank you. Ms. Brooks will sign the release Monday. Our W-9 is attached. Please send the check to our office.

Marcus Delgado""")
item("doc_delgado_w9", "docs", "document", "D5 08:40", "t_kessler", "c_delgado", ["c_daniela"], "Form W-9 - Delgado & Finch PLLC",
     "Form W-9 (Rev. March 2024). Name: Delgado & Finch PLLC. Federal tax classification: LLC taxed as partnership. Address: 1207 W Veterans Memorial Blvd, Suite 210, Killeen TX 76541. TIN on file (masked in OnBase). Signed M. Delgado 11/06/2026.")
item("e_d5_jordan_signed", "email", "email", "D5 09:05", "t_kessler_jordan", "c_jordan", ["c_daniela"], "RE: Settlement of your claim",
     body="Signed it on the docusign last night. No health insurance paid anything, I paid the ER myself on a payment plan. Thanks for being straight with me. - Jordan")
item("e_d5_elaine_defense", "email", "email", "D5 09:30", "t_ostrowski", "c_elaine", ["c_daniela", "c_hartley"],
     "Dunn v. Ostrowski - defense counsel assigned - AU-26-011907", body="""Daniela,

I've assigned Dunn v. Ostrowski (Cause No. 2026-CCL2-0917, County Court at Law No. 2, Bell County) to Rebecca Voss at Hartley & Voss LLP, copied here. Answer date 11/23. Please send Rebecca the claim materials today: the insured's recorded statement, crash report, photos, the plaintiff's pre-suit medical records and bills, our estimate and payment on the Rogue, the dec page, and the pre-suit demand and offer correspondence. Rebecca will contact Mr. Ostrowski directly.

Elaine Whitcomb | Staff Counsel | Leon River Mutual""")
item("e_d5_hartley", "email", "email", "D5 10:15", "t_ostrowski", "c_hartley", ["c_daniela"], cc=["c_elaine"],
     subject="RE: Dunn v. Ostrowski - defense counsel assigned", body="""Daniela,

Nice to meet you. Looking forward to the file. If you can include a short summary of the pre-suit negotiations and anything you know about the plaintiff's prior claims (ISO), that would help with the answer and initial disclosures.

Rebecca Voss | Hartley & Voss LLP | Waco | 254-555-0153""")
item("ch_d5_renee", "chat", "chat_message", "D5 10:30", "t_cat_report", "c_renee", ["c_daniela"], "#auto-claims-temple",
     "@Daniela @Colton @Tasha reminder numbers by noon pls, Howard's report goes at 1")
item("e_d5_albrecht", "email", "email", "D5 11:15", "t_albrecht", "c_albrecht", ["c_daniela"], "Brent says you won't pay",
     body="""Daniela,

Brent at Lone Star says LRM is refusing to pay and he won't release my truck until he gets $7,860. I signed his paper because he said that's how it works. I just want my truck back. What do I do?

Megan Albrecht""")
item("tk_d5_kessler_review", "tickets", "ticket", "D5 08:00", "t_kessler", "c_fnol", ["c_daniela"],
     "Activity due today: 30-day file review - AU-26-018842 Kessler",
     "ClaimCenter activity reminder. 30-day review due 11/06.")
item("e_d5_mabry_video", "email", "email", "D5 12:30", "t_coyle", "c_mabry", ["c_daniela"], "dashcam video",
     body="Here is the video like I said. You can see her backing. - Terrence Mabry\n[Attachment: dashcam_1024.mp4, 38 sec; timestamp 10/24/2026 17:41]")
item("e_d5_greg_sat", "email", "email", "D5 13:30", "t_greg_week", "c_greg", ["c_daniela", "c_colton", "c_tasha"], "Saturday drive-in coverage",
     body="Colton has the Saturday drive-in desk 8-12. Thanks all for a heavy week. - Greg")
item("e_d5_trent3", "email", "email", "D5 14:20", "t_haskins", "c_trent", ["c_daniela"], "RE: Subrogation demand - Haskins / Pham",
     body="Daniela - my supervisor approved 100% after the witness statement. $7,240.00 check will issue next week. - Trent")
item("tk_d5_salinas_bills", "tickets", "ticket", "D5 10:40", "t_kessler", "c_fnol", ["c_daniela"],
     "Activity: documents uploaded by claimant - AU-26-018842 BI Hector Salinas",
     "ClaimCenter portal upload by claimant Hector Salinas: final itemized bill, Killeen Family Chiropractic, 09/15-10/20/2026, 14 visits, $3,105.00; no lost wages claimed. Review and evaluate.")
item("ch_d5_tasha", "chat", "chat_message", "D5 13:10", "t_teamchat", "c_tasha", ["c_daniela"], "#auto-claims-temple",
     "anyone else getting calls from that lone star hail pros guy? he told my insured LRM \"never pays mobile PDR\". I just keep telling them two-party check per the policy")
item("vm_d5_okafor", "phone", "voicemail", "D5 15:05", "t_okafor", "c_okafor", ["c_daniela"], "Voicemail from 254-555-0151 (0:20)",
     "Sam Okafor. Shop says Tuesday the tenth still. Just letting you know. Thanks.")

D5_ACTIONS = [
    {"id": "a_d5_01", "at": "D5 09:00", "verb": "read", "target": "e_d5_delgado_ack", "content": "", "note": ""},
    {"id": "a_d5_02", "at": "D5 09:15", "verb": "update_ticket", "target": "e_d5_jordan_signed",
     "content": "Payment issued 11/06: BI Jordan Brooks $7,800.00 to Jordan Brooks on receipt of signed release (no liens per claimant). BI exposure closed. Aaliyah Brooks: $30,000.00 check request to 'Aaliyah Brooks and Delgado & Finch PLLC' set for Mon 11/09 on receipt of signed release; W-9 received. Per-accident BI paid or committed: $37,800 of $60,000.",
     "note": ""},
    {"id": "a_d5_03", "at": "D5 10:00", "verb": "send", "target": "e_d4_ray",
     "content": "To Rosa Villarreal (email and mail). Subject: Your claim AU-26-023201.\n\nDear Ms. Villarreal,\n\nThis letter confirms that Leon River Mutual received your claim for hail damage to your 2021 Nissan Altima, reported November 1, 2026. Our investigation is continuing. We will contact you to schedule an inspection of the vehicle and to take your statement about the loss. Please do not have the vehicle repaired before it is inspected, and keep any photos you have of the damage. If we need any documents from you, we will tell you in writing.\n\nIf you have questions, please call me at 254-555-0147.\n\n" + SIG,
     "note": "The letter Ray asked for, with no mention of SIU or the endorsement."},
    {"id": "a_d5_04", "at": "D5 10:20", "verb": "call_out", "target": "vm_d5_villarreal",
     "content": "Calls Rosa Villarreal back (call_d5_villarreal).", "note": ""},
    {"id": "a_d5_05", "at": "D5 11:40", "verb": "send", "target": "e_d4_renee_request",
     "content": "To Renee Lindqvist. Subject: Reyes CAT 26-14 numbers as of Thu 11/05 close. Files assigned: 10 (Ellis, Patel, Okafor, Albrecht, Hollis, Ferreira, Wynn, Sutton, Price, Villarreal). Open 6, closed 4 (Hollis, Patel, Ferreira, Sutton). Indemnity paid to date, net of deductible, excluding rental: $29,994.64 (Hollis $2,418.40; Patel $2,912.18; Okafor $4,947.75; Ferreira $5,940.75; Ellis $12,031.56; Sutton $1,744.00). Total losses: 1. SIU referrals: 1.",
     "note": "Numbers from the tracker as of Thursday close."},
    {"id": "a_d5_06", "at": "D5 12:00", "verb": "send", "target": "e_d5_hartley",
     "content": "To Rebecca Voss, cc Elaine Whitcomb. Subject: Dunn v. Ostrowski - claim materials - AU-26-011907.\n\nRebecca,\n\nAttached from the claim file: (1) Ben Ostrowski's recorded statement of 06/16/2026 (14 min) and transcript; (2) Temple PD crash report; (3) 22 photos of both vehicles; (4) Kayla Dunn's pre-suit medical records and bills received 09/10 (chiropractic 06/16-09/02, billed $8,940.00); (5) CCC ONE estimate and the $3,108.77 payment for the Rogue on 06/30; (6) declarations page PA-TX-2287140 (BI 50/100, PD 50); (7) Gaitan's $28,000 demand of 09/12 and our $9,500 offer of 09/28, rejected 09/30. Negotiation summary: liability accepted; the gap is the value of a soft-tissue chiropractic case. ISO ClaimSearch on Ms. Dunn: one prior auto claim, 2021, rear-end, BI with chiropractic treatment; report attached. Mr. Ostrowski was served personally 10/30 at 6:15 p.m.; his number is 254-555-0128 and he knows you'll call.\n\n" + SIG,
     "note": "Evidence package for defense counsel."},
    {"id": "a_d5_07", "at": "D5 13:00", "verb": "update_ticket", "target": "tk_d5_kessler_review",
     "content": "30-day review 11/06: A. Brooks - demand accepted 11/05 per Roundtable, $30,000 payment pending signed release; excess letter sent 11/05; sworn statement of other insurance form sent to insured. J. Brooks - settled $7,800, paid 11/06, closed. Salinas - final chiropractic bill $3,105.00 uploaded today (14 visits, no wage claim); evaluate and call with an offer Monday. Remaining per-accident BI limit after both: $22,200. Next review 12/06.",
     "note": ""},
    {"id": "a_d5_08", "at": "D5 14:00", "verb": "reply", "target": "e_d5_albrecht",
     "content": "Hi Megan,\n\nWe aren't refusing to pay. Our appraiser inspected your truck yesterday and wrote an estimate of $6,212.50. After your $500 deductible, the payment is $5,712.50. Under your policy the check must include your lienholder, Texas Frontier Bank, and because you signed Lone Star's direction to pay, I'll add Lone Star Hail Pros as a payee too. I'm issuing that today. The $1,647.50 difference from Brent's invoice is mostly his roof dent count and an aluminum surcharge our estimate already accounts for; if he sends photos that support more, we'll review a supplement. We do not pay storage to repair shops. Also, please know that your deductible is your responsibility under the policy, and a shop can't waive it on the insurance claim. Call me if Brent won't release the truck once the check is issued.\n\n" + SIG,
     "note": ""},
    {"id": "a_d5_09", "at": "D5 14:30", "verb": "update_ticket", "target": "doc_albrecht_est",
     "content": "Payment issued 11/06: AU-26-023131 Albrecht $5,712.50 ($6,212.50 less $500 deductible), check payable to Megan Albrecht, Texas Frontier Bank and Lone Star Hail Pros LLC (direction to pay on file). Tracker updated.",
     "note": ""},
    {"id": "a_d5_10", "at": "D5 15:00", "verb": "update_ticket", "target": "e_d5_trent3",
     "content": "File note 11/06: Gulf Plains accepted 100%; $7,240.00 recovery expected next week; on receipt, refund insured's $500 deductible in full. Called Gloria Haskins to tell her. Arbitration diary cancelled.",
     "note": ""},
    {"id": "a_d5_11", "at": "D5 15:30", "verb": "update_ticket", "target": "e_d5_mabry_video",
     "content": "File note 11/06: Claimant's dashcam video received (38 s, 10/24 17:41). Shows the Highlander reversing out of a space as the claimant's vehicle backs out opposite; both moving. Liability remains disputed; will discuss comparative split with G. Pruitt Monday before responding. No determination communicated.",
     "note": ""},
    {"id": "a_d5_12", "at": "D5 16:30", "verb": "edit_doc", "target": "sheet_cat_tracker",
     "content": "Row Albrecht: paid $5,712.50, Closed 11/06. Row Price: drive-in 11/06 3:00 p.m. done, hail estimate pending upload; windshield replacement booked Mon 11/09 with the LRM glass vendor. Row Villarreal: Open - investigation continuing, letter sent 11/06.",
     "note": "End-of-week tracker update."},
]

D5_CALLS = [
    {"id": "call_d5_villarreal", "at": "D5 10:20", "caller": "c_villarreal", "purpose": "Outbound callback: insured asks whether her claim is being denied",
     "turns": [
         {"speaker": "human", "text": "Ms. Villarreal, this is Daniela Reyes at Leon River Mutual returning your call."},
         {"speaker": "caller", "text": "Finally. Doug says there's a problem. Are you denying my claim? Nobody's even looked at my car and my neighbor already got paid.", "patience_s": 10},
         {"speaker": "human", "text": "No decision has been made on your claim. It's open, and the investigation is continuing. You'll get a letter from me today confirming that, and someone from our office will call you next week to schedule the inspection and talk with you about the loss."},
         {"speaker": "caller", "text": "What does that mean, investigation? Is it because of the coverage Doug added? I had it before, I just didn't have the full one.", "patience_s": 10},
         {"speaker": "human", "text": "I can't go into the details of the investigation over the phone, but you'll have the chance to explain everything when we take your statement. Please don't have the car repaired before it's inspected, and keep any photos you took."},
         {"speaker": "caller", "text": "Fine. Next week. Somebody better call me.", "patience_s": 6},
         {"speaker": "human", "text": "They will. And you can call me directly at 254-555-0147 in the meantime."}]},
]
