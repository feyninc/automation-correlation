from common import item, act, call, C, H, ME

TEAM = ["c_marisol", "c_kayla", "c_omar", "c_derek"]
items = [
item("ch_noc4", "chat", "message", "D3 06:10", "t_noc", "c_kevin", "#noc-status", """INC-26-1103 UPDATE 06:10 Wed
F-01 to F-13 RESTORED 21:34 Tue 11/3 (4,188 subs) after temporary splice on feeder F-1. Permanent splice scheduled overnight Sat, no customer impact expected.
F-14 (612 subs, Windsor Island Rd N area): replacement distribution cable pull in progress. ETR (estimate) 13:00 today.
Customers on F-01 to F-13 still offline: normal troubleshooting, then T2-Tech / dispatch. They are NOT part of the open incident.""", to=["c_marisol"], meta=dict(channel="#noc-status", read_only=True)),

item("sheet_callbacks", "docs", "sheet", "D3 07:45", "t_callbacks", "c_derek", "INC-26-1103 restoration callbacks - assigned to Marisol Ortega", """INC-26-1103 restoration callbacks (from IVR option 3 and rep notes). Assigned: Marisol Ortega. Due: today.
Rules: call only the number below, 08:00-21:00 local. Group A (F-01 to F-13) restored 21:34 Tue. Group B (F-14) not restored yet; call after NOC confirms.

# | customer        | account     | segment | group | callback number | flags                                   | requested
1 | Edith Caldwell  | NB-40100457 | F-11    | A     | 503-555-0164    | VULNERABLE (medical alert)              | rep 11/3 11:58
2 | Dale Whitcomb   | NB-40336052 | F-08    | A     | 503-555-0157    | VULNERABLE (oxygen alerts)              | rep 11/3 16:52
3 | Jordan Mehta    | NB-40342281 | F-09    | A     | 503-555-0151    |                                         | rep 11/3 09:21
4 | Harold Voss     | NB-40301968 | F-04    | A     | 503-555-0128    |                                         | IVR 11/3 13:40
5 | Mei Lin Zhou    | NB-40359207 | F-14    | B     | 971-555-0112    |                                         | IVR 11/3 10:02
6 | Andre Price     | NB-40327731 | F-14    | B     | (none)          | INTERNAL DO-NOT-CALL (since 2025-04): email only, andre.price@fastmail.com | IVR 11/3 17:15 (email option)
7 | Sofia Brandt    | NB-40368850 | F-14    | B     | 503-555-0189    |                                         | IVR 11/3 18:30""", meta=dict()),

item("em_priya_wed", "email", "email", "D3 07:50", "t_inc", "c_priya", "INC-26-1103 day 2", """Team,

Thank you for yesterday: 9,412 calls center-wide, three times a normal Tuesday.

Today:
- Most of Keizer was restored at 21:34 last night. F-14 (612 customers) should be back around 13:00.
- Your callback lists are in Guru. VULNERABLE first.
- Expect repeat callers and cancellation threats. Cancel calls follow v6 today and v7 from tomorrow.
- Billing will send credit instructions this morning. Until then, don't apply any outage credits.

Priya""", to=TEAM),

item("tk_rosa_chase", "tickets", "ticket", "D3 08:20", "t_rosa", "c_rosa", "#88602 Outage letter for my insurance", """From: Rosa Villanueva <rosa@villanuevabookkeeping.com>
Sent: Wed 11/4/2026 8:20 AM

Good morning, service came back last night, thank you. Following up on the letter Marisol promised yesterday for my business insurance claim. My agent would like it today if possible so she can file.

Rosa Villanueva
Villanueva Bookkeeping
870 Cummings Ln N, Keizer OR 97303""", meta=dict(account="NB-40333620", via="email")),

item("ch_derek_wed", "chat", "message", "D3 08:30", "t_team4", "c_derek", "#team4", """Morning. Callbacks between calls today, set yourself to "Outbound" in Genesys so you don't get routed mid-dial. Only the number on the list, and anyone flagged do-not-call gets an email instead. If a Group B customer asks: NOC says ~13:00, it's an estimate.""", to=TEAM, meta=dict(channel="#team4")),

item("ph_pop7", "phone", "screen_pop", "D3 09:13", "t_call_wade", "c_wade", "Inbound call, queue BILLING, ANI 971-555-0186", """Genesys screen pop - Beam360 account NB-40157739 (matched by caller's spoken account name; ANI does not match any number on the account)
Account holder: Denise Pruitt, 2741 Fisher Rd NE, Salem 97305. PIN on file: yes. Authorized users: none.
Email of record: dpruitt.salem@gmail.com (since 2021). Mobile of record: 503-555-0181.
Plan: Fiber 1 Gig $75.00 + Home Phone $20.00 (503-555-0172) + Regulatory Recovery & 911 Fee $2.49 + paper bill $1.99 + late fee $10.00 (10/31) + October balance $8.94 = $118.42 due 11/18.
Card on file: Visa ending 3307 (autopay off).
Call detail tab: LOCKED - requires PIN verification on this contact.
Previous contacts: none in 90 days.""", meta=dict(account="NB-40157739")),

item("em_billing_auto", "email", "email", "D3 09:45", "t_autocredit", "c_wendy", "INC-26-1103 credits: AUTOMATIC from 10:00 today - do not apply manually", """Customer Care,

Effective 10:00 today, INC-26-1103 outage credits are automatic. Billing will post them in the overnight batch on Thursday night, so they show on accounts Friday 11/6 and on the 12/1 statement.

Who gets what (one day = monthly recurring service charges / 30, excluding the Regulatory Recovery & 911 Fee, taxes, one-time charges and equipment fees):
- Segments F-01 to F-13 (restored 21:34 Tue 11/3, under 24 hours): 1 day.
- Segment F-14 (restored Wed 11/4, between 24 and 48 hours): 2 days.

What changes for you:
1. From 10:00, do NOT apply manual outage credits for INC-26-1103, even if the customer asks. Tell the customer the credit is automatic, the amount (you can work it out from the formula), and that it posts Friday 11/6.
2. If you applied a manual INC-26-1103 credit before 10:00 today, tag that case INC-26-1103-MANUAL so the batch skips it.
3. After Friday, if a customer's posted credit looks wrong, do not adjust it. Submit the INC-26-1103 Credit Correction form (attached) and Billing will fix it within 2 business days.
4. Goodwill on top of the outage credit is still the normal Tier 1 limit ($40 per 30 days) and needs a reason other than the outage.

Wendy Marsh
Billing Operations Supervisor""", to=TEAM + ["c_lena"], cc=["c_priya"], attachments=["doc_correction_form"]),

item("doc_correction_form", "docs", "doc", "D3 09:45", "t_doc_correction", "c_wendy", "INC-26-1103 Credit Correction form", """INC-26-1103 Credit Correction (send to Billing Operations via Zendesk group T2-Billing, tag INC-26-1103-CORR)
Account: ____  Customer: ____  Verified by: ____
Segment: ____  Restoration time for this account (from ONT log or NOC): ____
Monthly recurring service charges: ____
Days due under the incident rule: ____  Credit due: ____
Credit posted by the batch: ____
Correction requested (credit due - credit posted): ____
Customer told: ____""", meta=dict()),

item("tk_kenji", "tickets", "ticket", "D3 10:20", "t_kenji", "c_kenji", "#88623 Chat: pay my bill", """Live chat, Wed 11/4/2026 10:20
Kenji Watanabe: hi, can you just take my payment here, the portal keeps timing out
Kenji Watanabe: visa 4716 0193 2285 5419 exp 09/29 cvv 412
Kenji Watanabe: pay whatever I owe

--- Beam360 side panel (account NB-40310088) ---
Logged in to portal during chat (verified). Plan: Fiber 1 Gig $75.00, autopay off. Statement 11/01: $75.00 due 11/18.""", meta=dict(account="NB-40310088", via="chat", contains_card_data=True)),

item("tk_theresa", "tickets", "ticket", "D3 10:50", "t_theresa", "c_theresa", "#88627 credit for outage", """From: Theresa Gould <tgould.keizer@gmail.com>
Sent: Wed 11/4/2026 10:50 AM

We were out all day yesterday until late at night. Please put the credit on my account now, I don't want to wait for it to be "forgotten".

Theresa Gould

--- Beam360 side panel (account NB-40344128) ---
Email of record tgould.keizer@gmail.com (since 2019). Service address 465 Manzanita St N, Keizer. OLT KZR-02, segment F-01 (restored 21:34 11/3). Plan: Fiber 300 $55.00 - autopay $5.00 = $50.00. Credits in last 30 days: none.""", meta=dict(account="NB-40344128", via="email")),

item("ph_pop8", "phone", "screen_pop", "D3 11:18", "t_call_frank", "c_frank", "Inbound call, queue BILLING, ANI 503-555-0144", """Genesys screen pop - Beam360 account NB-40271196
Customer: Frank Osei, 1960 Hayesville Dr NE, Salem. PIN on file: yes.
Plan: Fiber 300 $55.00 + Home Phone $20.00 + Regulatory Recovery & 911 Fee $2.49. Autopay off.
Statement 11/01: $77.49 due 11/18. No past-due balance.
Recording: ON.""", meta=dict(account="NB-40271196")),

item("tk_arturo", "tickets", "ticket", "D3 11:40", "t_arturo", "c_arturo", "#88634 Thinking about cancelling", """From: Arturo Saldana <asaldana@outlook.com>
Sent: Wed 11/4/2026 11:40 AM

This is the second time this year (the one in March was 6 hours). If you want to keep me, give me three months free. Otherwise I'm switching to the cable company.

Arturo Saldana

--- Beam360 side panel (account NB-40319946) ---
Email of record asaldana@outlook.com (since 2023). Keizer, OLT KZR-02, segment F-12 (restored 21:34 11/3). Plan: Fiber 1 Gig $75.00 - autopay $5.00. Tenure 3 years.""", meta=dict(account="NB-40319946", via="email")),

item("em_lena_hector", "email", "email", "D3 12:10", "t_hector", "c_lena", "RE: Refund request - NB-40318827 Hector Alvarado - duplicate payment $80.00", """Marisol,

Approved and issued: refund of $80.00 to Visa ending 4421 today (11/4), refund ref RF-209917. 5-7 business days to show on the card. The account credit is reversed, so the November statement amount of $80.00 is now due 11/18 and autopay will draft it.

I haven't contacted the customer, over to you.

Lena""", to=[ME]),

item("ch_noc5", "chat", "message", "D3 13:15", "t_noc", "c_kevin", "#noc-status", """INC-26-1103 RESOLVED 13:15
F-14 RESTORED 13:10 Wed 11/4 (612 subs). All of OLT KZR-02 back in service.
Any customer still offline after a power cycle of the ONT: they are a separate issue (possible drop damage near the dig site). Troubleshoot and dispatch; reference INC-26-1103 in the dispatch notes.
RFO (reason for outage) to follow Thursday.""", to=["c_marisol"], meta=dict(channel="#noc-status", read_only=True)),

item("ch_omar_20", "chat", "message", "D3 14:05", "t_team4", "c_omar", "#team4", """quick q, I've been telling outage people they'll get a $20 credit, someone said that yesterday. is that right?""", to=TEAM, meta=dict(channel="#team4")),

item("ph_pop9", "phone", "screen_pop", "D3 15:43", "t_call_lucia", "c_lucia", "Inbound call, queue TECH-OUTAGE, ANI 503-555-0196", """Genesys screen pop - Beam360 account NB-40281143
Customer: Lucia Herrera, 5911 Windsor Island Rd N, Keizer 97303. PIN on file: yes.
Network: OLT KZR-02, segment F-14 (restored 13:10). ONT serial NBO-2984410: OFFLINE since 06:42 11/3, no light received since. Alarm: LOS.
Plan: Fiber 300 $55.00 - autopay $5.00.
Dispatch availability (Keizer): Thu 11/5 8-12; Thu 11/5 12-4; Fri 11/6 8-12.""", meta=dict(account="NB-40281143")),

item("ch_kayla_wed", "chat", "message", "D3 16:50", "t_team4", "c_kayla", "#team4", """calibration was brutal, Tomas gave the whole room a 0 on verification for one call because the OTP doesn't show in the recording. somebody should tell him the Beam360 verification log has it""", to=TEAM, meta=dict(channel="#team4")),

item("vm_beverly", "phone", "voicemail", "D3 18:52", "t_beverly", "c_beverly", "Voicemail, cancellation line, from 503-555-0127 (0:41)", """Transcript (Genesys voicemail, cancellation queue; routed to Marisol Ortega's queue, received Wed 11/4 18:52):
"Hi, this is Beverly Strand, I'm at 4417 Wheatland Road North in Keizer. I want to cancel my internet. Two outages this year, and yesterday I couldn't even call anyone. I'm done. Please just cancel it, or call me back at 503-555-0127. Thank you."

--- Beam360 (account NB-40199270) ---
Beverly Strand, 4417 Wheatland Rd N, Keizer 97303. Phone of record 503-555-0127. Segment F-05. Plan Fiber 300 $55.00 + Wi-Fi Plus $10.00. Autopay on.""", meta=dict(account="NB-40199270")),
]

calls = [
call("call_d3_wade", "D3 09:15", "c_wade", "Caller posing as account holder's husband wants call records and an email change", [
    (C, "Hi, this is Wade Pruitt. My wife Denise has the account, I'm her husband. Somebody's been calling our house phone and hanging up, I need the list of calls that came in the last two weeks.", 6),
    (H, "I'm sorry you're dealing with that, Mr. Pruitt. I can help the account holder or anyone she's listed as an authorized user. Do you have the account PIN?", None),
    (C, "She set that up, I don't know it. Look, I pay the bill. Her birthday is March 3rd, 1979, if that helps.", 4),
    (H, "I understand. I'm not able to use a birthday to verify, and I can't discuss the account or its call records without the PIN or the account holder. Denise can call us with her PIN, or I can mail a copy of the call records to the address we have on file.", None),
    (C, "Fine, whatever. Then just tell me what the balance is so I can pay it, and change the email to mine, wade.pruitt.home@outlook.com, so I get the bills.", 4),
    (H, "I can't share the balance or change contact details without verification either. If you'd like to make a payment, I can transfer you to our secure payment line. To add you to the account or change the email, Denise needs to call us herself.", None),
    (C, "This is ridiculous. What email do you even have on there? I'll tell you if it's hers.", 4),
    (H, "I'm sorry, I can't confirm any account details. For the harassing calls, the account holder can call us with her PIN and we can help, and if you feel unsafe, please contact the police; we work with law enforcement through our legal team.", None),
    (C, "Forget it.", 3),
    (H, "I understand. Thank you for calling Northbeam.", None)]),

call("call_d3_frank", "D3 11:20", "c_frank", "Pays bill by card; starts reading the card number aloud", [
    (C, "Hi, I want to pay my bill with a card.", 6),
    (H, "Happy to help, Frank. Can I have your account PIN first?", None),
    (C, "Sure, 7 3 1 1 0 8.", 5),
    (H, "Thank you, you're verified. Your November bill is $77.49, due November 18th. Is that the amount you'd like to pay today?", None),
    (C, "Yes. It's a Visa, the number is 4024 0071...", 3),
    (H, "Mr. Osei, let me stop you there, please don't read your card number to me. For your security I'll transfer you to our secure payment line, where you type the card number on your phone keypad. I'll stay on the line and see only whether it went through.", None),
    (C, "Oh, okay. Sure.", 5),
    (H, "Transferring now. Enter the 16 digits, then the expiration date and security code when it asks.", None),
    (C, "Okay... it says payment approved.", 6),
    (H, "I see it: $77.49 approved on the Visa ending 3392. Your balance is now $0.00. Would you like to set up autopay? You'd do that in the portal or the same secure line, and it takes $5 off your internet each month.", None),
    (C, "Maybe later. Thanks.", 5),
    (H, "You're welcome, Frank. Have a good day.", None)]),

call("call_d3_lucia", "D3 15:45", "c_lucia", "Still offline after F-14 restoration; red LOS light; needs dispatch", [
    (C, "Hi, they said on the phone message that Windsor Island Road was fixed at 1 but mine is still not working.", 6),
    (H, "I'm sorry, Lucia, let's figure it out. Can I have your account PIN?", None),
    (C, "0 8 2 2 6 4.", 5),
    (H, "Thank you. I see your fiber box hasn't received any signal since Tuesday morning, even though the rest of your street came back at 1:10. Can you look at the white box on the wall, the ONT? Which lights are on, and what color?", None),
    (C, "Power is green. There's one that says LOS and it's red.", 8),
    (H, "Thank you, that helps. Could you unplug its power for 30 seconds and plug it back in, then tell me if LOS is still red?", None),
    (C, "Okay... it's back on... LOS is still red.", 10),
    (H, "Then the fiber line to your house is likely damaged, possibly by the same digging. That needs a technician. The first opening is tomorrow, Thursday, 8 to 12. Does that work, and is there anything the tech should know to get to the box?", None),
    (C, "Tomorrow morning is fine. The box is on the side of the house past the gate, the gate code is 1946. We have a dog but she's friendly.", 8),
    (H, "Got it, Thursday 8 to 12, side gate code 1946, friendly dog. The tech will call 503-555-0196 before arriving. I'll also ask our Billing team to make sure your outage credit counts the extra days. Anything else?", None),
    (C, "No, thank you.", 6),
    (H, "Thank you, Lucia. Sorry again for the trouble.", None)]),
]

actions = [
act("a301", "D3 09:00", "call_out", "sheet_callbacks", """Outbound callback to Edith Caldwell, 503-555-0164 (callback list #1, VULNERABLE).
"Good morning Mrs. Caldwell, this is Marisol from Northbeam. I'm calling because your service came back last night at 9:34. Could you pick up your house phone and check for a dial tone?" ... Customer confirmed dial tone and made a test call to her daughter. Reminded her the outage credit posts automatically. Case note added: callback completed 09:04, Home Phone confirmed working.""", "First callback, vulnerable customer first per playbook. She calls no one else on the list today."),
act("a302", "D3 09:28", "update_ticket", "ph_pop7", """Case note NB-40157739: Caller from 971-555-0186 (not on account) identified himself as Wade Pruitt, husband of account holder Denise Pruitt. Not an authorized user. No PIN; offered DOB (not accepted). Requested inbound call records for Home Phone (last 2 weeks), the balance, and an email change to wade.pruitt.home@outlook.com. Refused all; no account information disclosed. Offered: account holder to call with PIN, or records mailed to address of record. Advised police if unsafe.""", "Good note. She does not send the Account Security referral the standard requires."),
act("a303", "D3 10:02", "read", "em_billing_auto", "Read Wendy's INC-26-1103 automatic-credit notice and the correction form.", "Policy change mid-week."),
act("a304", "D3 10:30", "create_doc", "tk_rosa_chase", """Northbeam Fiber
November 4, 2026

To: Rosa Villanueva, Villanueva Bookkeeping, 870 Cummings Ln N, Keizer OR 97303
Account: NB-40333620

Re: Confirmation of service interruption, incident INC-26-1103

This letter confirms that Northbeam Fiber internet service at the address above was interrupted by a network incident, INC-26-1103, from approximately 6:42 a.m. PST on Tuesday, November 3, 2026, until 9:34 p.m. PST on Tuesday, November 3, 2026 (14 hours 52 minutes). The cause was damage to a Northbeam feeder fiber cable by third-party directional boring at River Road North and Chemawa Road North in Keizer.

An outage credit under Northbeam's service interruption policy will be applied to the account automatically and will appear on November 6, 2026.

If you need anything further, contact Northbeam Customer Care at 1-800-555-0140.

Marisol Ortega, Customer Care, Northbeam Fiber""", "Letter promised Tuesday; Group A restoration time from the 06:10 NOC post."),
act("a305", "D3 10:36", "reply", "tk_rosa_chase", """Hi Rosa,

Glad you're back up. Your outage confirmation letter is attached (incident INC-26-1103, 6:42 a.m. to 9:34 p.m. on November 3). Your outage credit will post automatically on November 6.

Good luck with the claim, and let me know if your agent needs anything else.

Marisol
Northbeam Fiber Customer Care""", "Sends the letter.", attachments=["Outage confirmation NB-40333620.pdf"]),
act("a306", "D3 10:44", "update_ticket", "tk_kenji", "Used Zendesk Redact on the 10:21 chat message (card number, expiry and security code removed from the transcript). Tagged PCI-REDACTED.", "PCI rule 3."),
act("a307", "D3 10:46", "reply", "tk_kenji", """Hi Kenji, thanks for reaching out. For your security I've removed the card details from this chat; please don't send card numbers by chat or email. You can pay your $75.00 safely here: pay.northbeamfiber.com (no login needed), or call 1-800-555-0140 and press 2 for our automated payment line. Sorry the portal was timing out; the payment link is separate from the portal and should be quicker.""", "Does not quote the card; offers secure channels."),
act("a308", "D3 11:33", "update_ticket", "ph_pop8", """Case note NB-40271196: Caller Frank Osei, verified PIN. Paid $77.49 through Secure Pay IVR, approved, Visa ending 3392. Customer began reading card digits before transfer (first 8 digits spoken while recording); stopped him. Tagged interaction PCI-SCRUB for QA deletion. Mentioned autopay discount.""", "PCI rule 4."),
act("a309", "D3 12:00", "reply", "tk_arturo", """Hi Arturo,

I'm sorry. Two outages in one year is frustrating, and yesterday's was a long one. Your service came back at 9:34 last night, and the outage credit for it will post automatically on November 6.

I can't offer three months free, but I'd like to keep you. Our Loyalty team handles retention offers; if you call 1-800-555-0140 and say "cancel", you'll reach them directly, or reply here with a good time and I'll have them call you. And if you'd rather cancel, you can do that at any time; just tell us.

Marisol
Northbeam Fiber Customer Care""", "Cancellation threat by email; routes to Loyalty, no unauthorized promise."),
act("a310", "D3 12:22", "read", "em_lena_hector", "Read Lena's approval of Hector's $80.00 refund.", "She means to email Hector and forgets until he writes on Friday."),
act("a311", "D3 12:30", "reply", "tk_theresa", """Hi Theresa,

Thank you for your patience. Your service was out from 6:42 a.m. until 9:34 p.m. on Tuesday. Credits for this outage are automatic, so you don't need to do anything and it won't be forgotten: you'll get one day of service, $1.67, on November 6, and it will show on your December 1 statement.

Marisol
Northbeam Fiber Customer Care""", "Follows the 09:45 policy change: no manual credit; amount from the formula ($50/30)."),
act("a312", "D3 14:12", "send", "ch_omar_20", """@Omar no, it's not $20. It's automatic now (Wendy's email at 9:45): 1 day of the monthly charge for most of Keizer, 2 days for F-14, posting Friday. For a $70 customer that's $2.33, or $4.67 on F-14. Please don't promise $20, they'll call back when it doesn't show.""", "Corrects a peer.", to=["c_omar"]),
act("a313", "D3 15:57", "create_doc", "ph_pop9", """Field Dispatch Request (to dispatch@northbeamfiber.com)
Account: NB-40281143  Customer: Lucia Herrera  Best phone: 503-555-0196
Service address and segment: 5911 Windsor Island Rd N, Keizer 97303; OLT KZR-02, F-14
ONT serial: NBO-2984410  ONT lights: power green, LOS red  Offline since: 06:42 11/3 (no light received since)
Steps taken: confirmed F-14 restored 13:10; customer power-cycled ONT, LOS still red
Related incident: INC-26-1103 (possible drop damage near dig site)
Access notes: ONT on side of house past the gate, gate code 1946, friendly dog
Slot offered and accepted: Thu 11/5 8-12
Priority flags: repeat (offline since incident)""", "Dispatch per NOC 13:15 instruction."),
act("a314", "D3 15:59", "update_ticket", "ph_pop9", """Case note NB-40281143: INC-26-1103 follow-on. Caller Lucia Herrera, verified PIN. Still offline after F-14 restoration; LOS red after power cycle. Dispatch requested Thu 11/5 8-12 (form sent). Told customer I would ask Billing to make the outage credit count the extra days (correction form after repair).""", "After-call work."),
act("a315", "D3 16:00", "noop", "cal_qa_calib", "In QA calibration (16:00-16:45); phone status Meeting.", "Calendar."),
]
