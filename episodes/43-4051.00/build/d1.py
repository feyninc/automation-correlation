from common import item, act, call, C, H, ME

items = [
item("tk_curtis", "tickets", "ticket", "D1 06:58", "t_curtis", "c_curtis", "#88402 Charged $150 for a router I RETURNED", """From: Curtis Wainwright <cwainwright.or@gmail.com>
Sent: Mon 11/2/2026 6:58 AM

Hi,

I cancelled my service on Oct 2 when I moved in with my girlfriend (she already has Northbeam). I mailed the router back with the UPS label you emailed me. Dropped it at the UPS Store on Pacific Blvd on Oct 9. Tracking number 1Z8V41E70391245563 and it says DELIVERED Oct 14 to Northbeam Returns in Tualatin.

Now I get a "final bill" for $150.00 for "equipment not returned"??? I returned it. I have the receipt. Please remove this charge. I am not paying $150 for something you have sitting in your warehouse.

Curtis Wainwright
(541) 555-0193

--- Beam360 side panel (account NB-40122953) ---
Status: Disconnected 2026-10-02 (reason: moving, joining another account)
Former service address: 2207 Pacific Blvd SE, Albany OR 97321
Email of record: cwainwright.or@gmail.com (on file since 2023)
Equipment on account: Wi-Fi gateway NB-GX4, serial NB-GX4-77120 - status NOT RECEIVED
Return label: UPS 1Z8V41E70391245563, emailed 2026-10-02
Final statement 2026-11-01: equipment non-return fee $150.00; amount due $150.00 by 2026-11-18""",
     meta=dict(account="NB-40122953", via="email", priority="normal")),

item("tk_hector", "tickets", "ticket", "D1 07:12", "t_hector", "c_hector", "#88405 double charged in october", """From: Hector Alvarado <hector.alvarado71@gmail.com>
Sent: Mon 11/2/2026 7:12 AM

hello, I got charged twice in October. I paid on the phone line on the 16th because I got a new card and thought autopay would fail, then autopay took it again on the 18th. Same card both times. I want the second $80 back on my card please, not sitting on the account.

thanks
Hector

--- Beam360 side panel (account NB-40318827) ---
Plan: Fiber 1 Gig $75.00 + Wi-Fi Plus $10.00 - autopay discount $5.00 = $80.00/month
Email of record: hector.alvarado71@gmail.com (on file since 2024)
Payments: 2026-10-16 IVR, Visa ending 4421, $80.00, conf P-7731904
          2026-10-18 Autopay, Visa ending 4421, $80.00, conf A-7740216
Statement 2026-11-01: previous balance -$80.00 (credit); new charges $80.00; amount due $0.00. Autopay will not draft on 11/18 while the amount due is $0.00.
Credits in last 30 days: none""",
     meta=dict(account="NB-40318827", via="email")),

item("tk_naomi", "tickets", "ticket", "D1 07:30", "t_naomi", "c_naomi", "#88407 Moving to Corvallis - transfer my service", """Web form: Moving / transfer service
Submitted: Mon 11/2/2026 7:30 AM
Name: Naomi Fischer
Account: NB-40377412
Current address: 2280 Lancaster Dr NE Apt 14, Salem OR 97305
New address: 1450 NW Kings Blvd Apt 3B, Corvallis OR 97330
Move date: Saturday November 14
Message: I'd like internet working at the new place by the 14th (I work from home Mondays). Please shut off the old one after I've moved out, the 15th is fine. Can I keep the same plan and price? Best number 541-555-0148.

--- Beam360 side panel ---
Plan: Fiber 300 $55.00 - autopay $5.00 = $50.00/month. Gateway NB-GX4 serial NB-GX4-70233.
Email of record: naomi.fischer@pm.me (since 2025). Web form submitted while logged in to the customer portal (counts as verified).
Serviceability, new address: SERVICEABLE - building fiber present, unit has no ONT: install required.
Install slots, Corvallis: Fri 11/13 8-12; Sat 11/14 8-12; Mon 11/16 12-4.""",
     meta=dict(account="NB-40377412", via="web form")),

item("em_qa_eval", "email", "email", "D1 07:45", "t_qa", "c_tomas", "QA evaluation: call of 10/27 14:02 - 78/100", """Hi Marisol,

Your evaluation for the 10/27 call at 14:02 (customer Gutierrez, billing question, 7:48) is posted in Genesys Quality.

Score: 78/100
- Opening and empathy: 15/15
- Verification: 0/20 (critical) - I couldn't hear a PIN or OTP on the recording before you discussed the balance.
- Resolution and accuracy: 33/35
- Notes and tagging: 15/15
- Closing: 15/15

Because verification is a critical item, the call counts as a compliance miss on the October scorecard. If you think the score is wrong, you can dispute it in Genesys Quality or reply to me within 5 business days (by Fri 11/6, 17:00) with the evidence.

Thanks,
Tomas Reyes
Quality Analyst, Customer Care""", meta=dict()),

item("tk_ruth_note", "tickets", "internal_note", "D1 08:00", "t_ruth", "c_brent", "#88213 Field note: WO-552190 completed 10/31", """Field Ops completion note, WO-552190, Sat 10/31/2026 10:47
Technician: R. Abernathy
Found: ONT optics degraded (-27.9 dBm). Replaced ONT (new serial NBO-3318804). Light level now -19.8 dBm. Speed test at ONT port: 941 down / 938 up.
In-home: customer had to leave at 10:30, could not test Wi-Fi in the home office (upstairs, back bedroom, about 45 ft and two walls from the gateway). Left a note recommending a wired test or Wi-Fi Plus if Wi-Fi speeds are still low there.
Ticket returned to: Marisol Ortega (Tier 1) for the follow-up call.""", meta=dict(account="NB-40255190")),

item("em_wfm_bid", "email", "email", "D1 08:00", "t_bid", "c_analucia", "Holiday shift bid is open - closes Fri 11/6 at 5 pm", """Hi all,

The holiday bid for Thanksgiving week and Dec 21-Jan 1 is open in the WFM portal. Bids are awarded by seniority, then by October adherence. You need to pick at least ONE of: Thu 11/26 (Thanksgiving, holiday pay 1.5x), Fri 11/27, Thu 12/24 (to 2 pm), Thu 12/31 (to 2 pm).

Bids close Friday 11/6 at 5:00 pm. If you don't bid, WFM assigns you.

Ana Lucia
Workforce Management""", to=[ME, "c_kayla", "c_omar"]),

item("em_kb_weekly", "email", "email", "D1 08:05", "t_kb", "c_jess", "KB this week: promo roll-offs, cancellations v7 coming", """Morning Customer Care,

Three things this week:
1. The 12-month launch promo (Fiber 300 at $45) rolled off for about 6,400 customers on the 11/1 statements. Use the "Promo ended" macro. Tier 1 can't extend promos; autopay/paperless saves $5.
2. Cancellations, Downgrades and Save Offers v7 publishes Tuesday and takes effect Thursday 11/5. Compliance asked for changes to how we open cancellation calls. Details Tuesday.
3. Reminder: the Grenada and Jamaica "one ring" callback scam is back. If a Home Phone customer disputes Caribbean calls, check the call detail for short missed inbound calls from the same number before the callbacks.

Jess Moreland
Knowledge & Training""", to=[ME]),

item("ch_derek_huddle", "chat", "message", "D1 08:58", "t_team4", "c_derek", "#team4", """Huddle notes 11/2:
- Forecast: 1,900 calls today center-wide, heavy promo roll-off and "why is my bill higher" from the 11/1 statements.
- Digital blocks as scheduled (10-11, 2-3). Queue has 140 tickets older than 12 hrs, let's get them under 24h SLA.
- Shout-out to Kayla for the 5/5 survey from the Woodburn tech-support call.
- Reminder: NO promo extensions, that's Loyalty only and only on cancel calls.""", to=["c_marisol", "c_kayla", "c_omar"], meta=dict(channel="#team4")),

item("ph_pop1", "phone", "screen_pop", "D1 09:17", "t_call_gary", "c_gary", "Inbound call, queue TECH-WIFI, ANI 503-555-0122", """Genesys screen pop - Beam360 account NB-40211736
Customer: Gary Lindqvist, 4815 Sunnyview Rd NE, Salem. PIN on file: yes.
Plan: Fiber 300 $55.00 - autopay $5.00 = $50.00/month. No add-ons.
Equipment: gateway NB-GX4 (online, uptime 41 days). Gateway Wi-Fi clients: 9. Speed test from gateway (last night): 312 down / 309 up.
Last contact: none in 90 days.""", meta=dict(account="NB-40211736")),

item("tk_amara", "tickets", "ticket", "D1 09:50", "t_amara", "c_amara", "#88419 Need a copy of my October bill", """Chat transcript (converted to ticket, customer left chat)
09:41 Amara Okafor: hi i need a copy of my october statement for my apartment's reimbursement thing. the portal only shows the last one?
09:42 Bot: I can help with billing questions. Would you like to speak with an agent?
09:42 Amara Okafor: yes
09:49 Amara Okafor: nvm I have to go, can you just email it

--- Beam360 side panel (account NB-40350961) ---
Customer logged in to the portal during chat (verified). Email of record amara.okafor@outlook.com (since 2024).
Statements available: 2026-11-01, 2026-10-01, 2026-09-01. October statement (10/01): $50.00, paid 10/18 by autopay.""", meta=dict(account="NB-40350961", via="chat")),

item("ch_kayla_wifi", "chat", "message", "D1 10:40", "t_team4", "c_kayla", "#team4", """anyone know if Wi-Fi Plus still has the free shipping or did that end with the promo? customer asking""", to=["c_marisol", "c_omar", "c_derek"], meta=dict(channel="#team4")),

item("em_misaddr", "email", "email", "D1 11:20", "t_misaddr", "c_wendy", "October manual adjustments - audit sample", """Marisol,

Here's the October audit sample of manual adjustments over $25 for your review before Wednesday's controls meeting. Please check each one has a reason code and a case note and flag anything odd.

account     | customer          | adjustment | reason      | rep
NB-40412207 | Patrice Holloway  | -$38.00    | GOODWILL    | 4410
NB-40177359 | Samuel Ortiz-Bell | -$150.00   | EQUIP-FEE   | T2 5102
NB-40298844 | Lorraine Duvall   | -$27.50    | MISSED-APPT | 4433
NB-40366518 | Kwame Asante      | -$40.00    | GOODWILL    | 4471
NB-40130082 | Beatriz Lanning   | -$95.00    | REFUND      | T2 5108

Thanks!
Wendy

Wendy Marsh | Billing Operations Supervisor | Northbeam Fiber""", to=[ME], meta=dict(note="Addressed to marisol.ortega@ by autocomplete; the Billing Ops analyst is Marisol Ortiz.")),

item("tk_tobias", "tickets", "ticket", "D1 12:30", "t_tobias", "c_tobias", "#88431 How much to go to 2 Gig?", """From: Tobias Reed <treed.salem@gmail.com>
Sent: Mon 11/2/2026 12:30 PM

Hey, I'm on the 1 Gig plan. What would 2 Gig cost me per month and is there an install or anything? My kid is streaming and gaming at the same time and it's getting choppy.

Tobias

--- Beam360 side panel (account NB-40402335) ---
Email of record treed.salem@gmail.com (since 2025). Plan: Fiber 1 Gig $75.00 - autopay $5.00 = $70.00/month. Gateway NB-GX4. Address eligible for 2 Gig: yes.""", meta=dict(account="NB-40402335", via="email")),

item("ph_pop2", "phone", "screen_pop", "D1 13:38", "t_call_tanya", "c_tanya", "Inbound call, queue BILLING, ANI 503-555-0109", """Genesys screen pop - Beam360 account NB-40299018
Customer: Tanya Brooks, 960 Brush College Rd NW, Salem. PIN on file: yes.
Plan: Fiber 300 $55.00 (12-month promo $45.00 ended 2026-10-31) + Home Phone $20.00 + Regulatory Recovery & 911 Fee $2.49. Autopay: off. Paperless: on.
Statement 2026-10-01: $67.49 (paid). Statement 2026-11-01: $77.49 due 2026-11-18.
Promo history: launch promo used (one per household).""", meta=dict(account="NB-40299018")),

item("ch_derek_promo", "chat", "message", "D1 14:50", "t_team4", "c_derek", "#team4", """FYI promo roll-off calls are running ~30% over forecast. If a customer threatens to cancel over it, that's a cancel call: follow the cancel script (one offer from the Offer Library, or Loyalty transfer). Don't build your own discounts.""", to=["c_marisol", "c_kayla", "c_omar"], meta=dict(channel="#team4")),

item("tk_lin", "tickets", "ticket", "D1 15:05", "t_weilin", "c_weilin", "#88440 Chat: locked out of portal", """Live chat, Mon 11/2/2026 15:05
Wei Lin: hi I'm locked out of the customer portal, too many password tries. Can you reset it?
Wei Lin: the email on the account is my work one, weilin@cascadeorthodontics.com

--- Beam360 side panel (account NB-40387720) ---
Email of record: weilin@cascadeorthodontics.com (since 2023). Mobile of record: 971-555-0136. Portal: locked 14:58 (5 failed attempts).""", meta=dict(account="NB-40387720", via="chat")),

item("ph_pop3", "phone", "screen_pop", "D1 16:03", "t_call_walter", "c_walter", "Inbound call, queue ACCOUNT-CHANGES, ANI 503-555-0177", """Genesys screen pop - Beam360 account NB-40188364
Customer: Walter Kim, 3341 Orchard Heights Rd NW, Salem. PIN on file: yes.
Plan: Fiber 1 Gig $75.00. Autopay: off. Statement 2026-11-01: $75.00 due 2026-11-18 (November billed in advance).
Equipment: gateway NB-GX4 serial NB-GX4-66019. Tenure: 4 years.""", meta=dict(account="NB-40188364")),
]

calls = [
call("call_d1_gary", "D1 09:18", "c_gary", "Weak Wi-Fi upstairs; candidate for Wi-Fi Plus", [
    (C, "Hi, yeah, my internet's fine downstairs but upstairs in the office it's terrible. Video calls keep freezing.", 6),
    (H, "I'm sorry about that, Gary, frozen video calls are no fun. Before I look at your account, can I get your account PIN?", None),
    (C, "Sure, it's 6 0 4 1 7 2.", 5),
    (H, "Thank you, you're verified. I can see your gateway is online and last night's test at the gateway was 312 down, 309 up, so the fiber line is doing its job. Where is the gateway compared with the office?", None),
    (C, "It's in the living room by the TV. Office is upstairs at the other end of the house.", 6),
    (H, "That's very likely the Wi-Fi range, not the service. Two options: run an ethernet cable to the office, or add Wi-Fi Plus, which is a mesh extender we ship and manage for $10 a month. It would take your bill from $50 to $60 a month with your autopay discount.", None),
    (C, "Ten bucks a month. Do I have to have someone come out?", 5),
    (H, "No, it's self-install. It ships in 2 to 3 business days, you plug it in about halfway between the living room and the office, and the app walks you through it. You can cancel the add-on any time.", None),
    (C, "Okay, let's do it.", 5),
    (H, "Done. Wi-Fi Plus is added, the extender ships to 4815 Sunnyview Road, and you'll get a tracking email. Your next bill will be $60. Anything else I can help with today?", None),
    (C, "No, that's it, thanks.", 6),
    (H, "Thanks for calling Northbeam, Gary. Have a good day.", None)]),

call("call_d1_tanya", "D1 13:40", "c_tanya", "Bill went up $10: promo ended", [
    (C, "Hi, my bill went up ten dollars and nobody told me. What's going on?", 5),
    (H, "I can look at that for you, Tanya. Can I have your account PIN first?", None),
    (C, "It's 2 8 8 1.", 5),
    (H, "Thanks, you're verified. Your 12-month launch price of $45 for Fiber 300 ended on October 31, so the plan is now the regular $55. With Home Phone at $20 and the $2.49 Regulatory Recovery and 911 fee, November is $77.49 instead of $67.49.", None),
    (C, "Can't you just extend it? I've been a customer for a year.", 4),
    (H, "I can't extend the promotion, it was a one-time launch price. What I can do is make sure you're getting every discount: you're on paperless but not autopay, and turning on autopay takes $5 off, so your monthly bill would be $72.49.", None),
    (C, "How do I do the autopay?", 6),
    (H, "You can set it up in the customer portal under Billing, or I can transfer you to our secure payment line where you key in the card yourself. Once it's on, the $5 discount starts with the next statement.", None),
    (C, "I'll do it online tonight. Fine.", 5),
    (H, "Sounds good. I've noted the account. Is there anything else I can help with?", None),
    (C, "No.", 4),
    (H, "Thanks for calling, Tanya. Take care.", None)]),

call("call_d1_walter", "D1 16:05", "c_walter", "Cancel: moving to Tucson", [
    (C, "Hi, I need to cancel my internet. We're moving to Tucson.", 6),
    (H, "Congratulations on the move, Walter. I can take care of that. Can I have your account PIN?", None),
    (C, "4 4 0 9 2 1.", 5),
    (H, "Thanks, you're verified. What date would you like the service to end?", None),
    (C, "The movers come the 20th, so the 20th.", 6),
    (H, "Got it, disconnect on Friday November 20. November was billed in advance at $75, so the 10 unused days, the 21st through the 30th, come back as a $25.00 credit on your final bill.", None),
    (C, "Okay. What about the router?", 6),
    (H, "We'll email a prepaid UPS label when the service disconnects. Please send the gateway back within 30 days, so by December 20, or there's a $150 non-return fee. The small white box on the wall, the ONT, stays at the house.", None),
    (C, "Got it. Anything else I need to do?", 6),
    (H, "That's it. You'll get a confirmation email shortly. Thanks for four years with Northbeam, and good luck in Tucson.", None)]),
]

actions = [
act("a101", "D1 09:02", "read", "tk_hector", "Opened #88405 (Hector Alvarado, duplicate October payment).", "Triage while waiting for the first call."),
act("a102", "D1 09:06", "read", "em_qa_eval", "Read Tomas's QA evaluation (78/100, verification marked 0).", "She remembers verifying that call by OTP; decides to look at it later."),
act("a103", "D1 09:30", "update_ticket", "ph_pop1", """Case note NB-40211736: Caller Gary Lindqvist, verified PIN. Weak Wi-Fi in upstairs office; gateway online, 312/309 at gateway, so range not service. Offered ethernet or Wi-Fi Plus; customer accepted Wi-Fi Plus ($10/mo, self-install). Order WP-118340 placed, ships 2-3 business days. New monthly $60.00 with autopay. Reason: TECH-WIFI / SALE-ADDON.""", "After-call work for call_d1_gary."),
act("a104", "D1 10:05", "reply", "tk_hector", """Hi Hector,

Thanks for letting us know, and sorry for the hassle. You're right: we received two payments of $80.00 from your Visa ending 4421, on October 16 (phone payment) and October 18 (autopay).

Right now the extra $80.00 is sitting on your account as a credit, and it has already paid your November bill, which is why your November statement shows $0.00 due. Since you'd like the money back on your card instead, I've sent a refund request for $80.00 to our Billing team, who handle refunds. They respond within 2 business days, and once they approve it the refund usually shows on your card in 5 to 7 business days.

One heads-up: once the $80.00 goes back to your card, your November bill of $80.00 will be due again on November 18 and autopay will take it that day.

I'll update you as soon as Billing confirms.

Marisol
Northbeam Fiber Customer Care""", "Done in the 10:00 digital block; Tier 1 cannot refund, so she sets expectations."),
act("a105", "D1 10:12", "send", "tk_hector", """To: Lena Kowalczyk (T2-Billing)
Subject: Refund request - NB-40318827 Hector Alvarado - duplicate payment $80.00

Lena, customer asks for a refund to card of a duplicate October payment.
- Account NB-40318827, Hector Alvarado, email of record hector.alvarado71@gmail.com
- 10/16 IVR payment $80.00, Visa ending 4421, conf P-7731904
- 10/18 autopay $80.00, Visa ending 4421, conf A-7740216
- Account shows -$80.00 credit; 11/1 statement $0.00 due. Customer wants $80.00 refunded to the Visa rather than left as credit. I told him Nov ($80.00) will then autopay on 11/18.
Zendesk #88405. Thanks!
Marisol (4471)""", "Escalation to Tier 2 per authority matrix item 5.", to=["c_lena"]),
act("a106", "D1 10:25", "reply", "tk_amara", """Hi Amara,

Here's your October 1 statement ($50.00, paid October 18 by autopay) as a PDF, attached. You can also download the last three statements any time in the portal under Billing > Statements; older ones I can send on request.

Have a great day,
Marisol
Northbeam Fiber Customer Care""", "Simple ticket.", attachments=["statement NB-40350961 2026-10-01.pdf"]),
act("a107", "D1 10:46", "send", "ch_kayla_wifi", """@Kayla Wi-Fi Plus never had a shipping charge, it's $10/mo and ships free 2-3 days. The promo that ended was the Fiber 300 $45 launch price.""", "Peer question.", to=["c_kayla"]),
act("a108", "D1 11:26", "reply", "em_misaddr", """Hi Wendy, I think this was meant for Marisol Ortiz in Billing Ops (I'm Marisol Ortega in Customer Care, autocomplete strikes again). I haven't opened the details or forwarded it, and I've deleted it from my inbox. You may want to resend it to her.

Marisol""", "Correct handling of a misaddressed email with customer data."),
act("a109", "D1 12:48", "reply", "tk_tobias", """Hi Tobias,

Good news, your address can get Fiber 2 Gig. It's $95.00 a month, or $90.00 with your autopay discount, so $20 a month more than you pay now. There's no install fee. 2 Gig needs our newer Wi-Fi 7 gateway (NB-GX7); we swap it for free, either shipped to you for self-install or with a technician visit if you prefer.

If you'd like to go ahead, just reply "yes" and tell me shipped or technician, and I'll set it up. The change is prorated on your next bill.

Marisol
Northbeam Fiber Customer Care""", "Simple ticket; mild upsell question from customer."),
act("a110", "D1 13:53", "update_ticket", "ph_pop2", """Case note NB-40299018: Caller Tanya Brooks, verified PIN. Asked why bill rose $10. Explained launch promo ($45) ended 10/31, Fiber 300 now $55; Nov statement $77.49. Customer asked for extension; declined per policy (Tier 1 cannot extend promos). Advised autopay saves $5 -> $72.49; customer will enroll in portal. Reason: BILL-PROMO-END.""", "After-call work."),
act("a111", "D1 14:10", "send", "tk_curtis", """To: Lena Kowalczyk (T2-Billing)
Subject: Equipment fee dispute - NB-40122953 Curtis Wainwright - $150.00 NB-GX4

Lena, former customer disputes the $150.00 non-return fee on his 11/1 final statement.
- Account NB-40122953, disconnected 10/02. Gateway on account NB-GX4-77120, shows NOT RECEIVED.
- Return label UPS 1Z8V41E70391245563 (ours, emailed 10/02); UPS shows delivered to Returns Center Tualatin 10/14. Customer has the UPS Store receipt (dropped off 10/09).
- Asks for the fee to be removed. Final statement due 11/18.
Zendesk #88402. Thanks,
Marisol (4471)""", "Escalation per authority matrix item 6. She does not notice the returns sheet's transposed serial.", to=["c_lena"]),
act("a112", "D1 14:16", "reply", "tk_curtis", """Hi Curtis,

Thank you for the tracking number, and I'm sorry for the surprise bill. I can see our UPS label on your account and the delivery to our Returns Center in Tualatin.

I'm not able to remove equipment fees myself, so I've sent your case to our Billing Escalations team with the tracking details. They review these within 2 business days and will make sure the return is matched to your account. Please don't pay the $150.00 while it's being reviewed; it isn't due until November 18 and we'll update you before then.

If you still have the UPS Store receipt, keep it handy in case they ask for it.

Marisol
Northbeam Fiber Customer Care""", "Sets expectation, no promise of reversal."),
act("a113", "D1 15:12", "reply", "tk_lin", """Hi Wei, I can help with that. For security I've just sent a one-time passcode by text to the mobile number we have on your account (ending 0136). Could you type the 6-digit code here?
[15:14 customer entered code; verified]
Thanks, you're verified. I've unlocked your portal and sent a password reset link to weilin@cascadeorthodontics.com. The link works for 30 minutes. Anything else I can do for you today?""", "Chat; OTP to the mobile of record, not to anything the customer typed."),
act("a114", "D1 15:40", "create_doc", "tk_naomi", """Service Transfer (Move) Order
Account: NB-40377412  Customer: Naomi Fischer  Verified by: logged-in portal web form
Current service address: 2280 Lancaster Dr NE Apt 14, Salem OR 97305
New service address: 1450 NW Kings Blvd Apt 3B, Corvallis OR 97330  Serviceability result: SERVICEABLE, building fiber present, install required (no ONT in unit)
Plan at new address: Fiber 300  Monthly price: $55.00 - $5.00 autopay = $50.00 (unchanged)
Install at new address: Sat 11/14/2026, 8-12
Disconnect at current address: Sun 11/15/2026
Equipment: customer brings gateway NB-GX4-70233; ONT stays at old address
Contact phone for technician: 541-555-0148
Notes: customer works from home Mondays; earlier slot Fri 11/13 8-12 also available if she wants a buffer.""", "Move order; done in the afternoon, more than 2 hours after the request arrived."),
act("a115", "D1 15:46", "reply", "tk_naomi", """Hi Naomi,

You're all set. Here's your move:
- New address: 1450 NW Kings Blvd Apt 3B, Corvallis. A technician will install the fiber box in your unit on Saturday, November 14, between 8 and 12. Please bring your Wi-Fi gateway with you.
- Old address: service stays on until Sunday, November 15, then disconnects.
- Plan and price stay the same: Fiber 300, $50.00 a month with autopay. No move or install fee.

If you'd like a buffer before your Monday work day, Friday the 13th 8-12 is also open; just reply and I'll switch it.

Marisol
Northbeam Fiber Customer Care""", "Confirms the move order."),
act("a116", "D1 16:18", "update_ticket", "ph_pop3", """Case note NB-40188364: Caller Walter Kim, verified PIN. CANCEL, reason MOVE-OUT-OF-AREA (Tucson); no save offer per script. Disconnect order DO-77412 effective Fri 11/20/2026. Final bill: credit 10 unused days x $75.00/30 = $25.00. Return label for NB-GX4-66019 emails at disconnect; return by 12/20 or $150 non-return fee. Confirmation email sent.""", "After-call work."),
]
