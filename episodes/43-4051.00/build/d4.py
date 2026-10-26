from common import item, act, call, C, H, ME

TEAM = ["c_marisol", "c_kayla", "c_omar", "c_derek"]
items = [
item("em_denise_fake", "email", "email", "D4 06:40", "t_denise_fake", "c_imposter", "Account change - Denise Pruitt", """From: Denise Pruitt <denise.pruitt.home@outlook.com>
Sent: Thu 11/5/2026 6:40 AM
To: support@northbeamfiber.com

Hello,

This is Denise Pruitt, my account is at 2741 Fisher Rd NE in Salem. I lost access to my old email so please update the email on my account to this one (denise.pruitt.home@outlook.com). Please also text the PIN reset to my new cell 971-555-0186, my old phone broke.

Also my husband Wade called yesterday about the calls to our house phone. Can you email him the list of incoming calls for October at wade.pruitt.home@outlook.com. He has my permission.

Thank you,
Denise

--- Zendesk routing ---
Sender address not found on any account. Routed to Tier 1 queue, assigned Marisol Ortega (matched by name to NB-40157739, which has a case note from her on 11/4).
Beam360 NB-40157739: email of record dpruitt.salem@gmail.com (since 2021), mobile of record 503-555-0181; no changes requested from either in 90 days.""", meta=dict(account="NB-40157739", via="email")),

item("tk_irene", "tickets", "ticket", "D4 07:15", "t_irene", "c_irene", "#88701 International calls I didn't make??", """From: Irene Matsuda <irene.matsuda@comcast.net>
Sent: Thu 11/5/2026 7:15 AM

Hello,

My November bill has $34.80 for "international calls". I don't call anyone overseas. I did get some missed calls in October from a number that looked normal and when I called back it was a recording about a cruise and hold for an agent, and it kept cutting off. Was that it? I'm on a fixed income and I'd like this taken off please.

Irene Matsuda

--- Beam360 side panel (account NB-40244867) ---
Email of record irene.matsuda@comcast.net (since 2018, more than 30 days). Plan: Fiber 300 $55.00 + Home Phone $20.00 (503-555-0183) + Regulatory Recovery & 911 Fee $2.49. Autopay on.
Credits in last 30 days: none. Courtesy usage credits in last 12 months: none.
Statement 11/01 usage, international (Home Phone 503-555-0183):
date  | time  | direction | number          | country | duration | charge
10/12 | 19:02 | inbound   | +1 473-555-0198 | Grenada | 0:01 (missed) | -
10/12 | 19:10 | outbound  | +1 473-555-0198 | Grenada | 12 min   | $6.96
10/13 | 18:40 | inbound   | +1 473-555-0198 | Grenada | 0:01 (missed) | -
10/13 | 18:44 | outbound  | +1 473-555-0198 | Grenada | 9 min    | $5.22
10/15 | 20:15 | inbound   | +1 473-555-0198 | Grenada | 0:01 (missed) | -
10/15 | 20:17 | outbound  | +1 473-555-0198 | Grenada | 14 min   | $8.12
10/17 | 17:55 | inbound   | +1 473-555-0198 | Grenada | 0:01 (missed) | -
10/17 | 18:01 | outbound  | +1 473-555-0198 | Grenada | 8 min    | $4.64
10/19 | 19:30 | inbound   | +1 473-555-0198 | Grenada | 0:01 (missed) | -
10/19 | 19:33 | outbound  | +1 473-555-0198 | Grenada | 11 min   | $6.38
10/20 | 18:22 | inbound   | +1 473-555-0198 | Grenada | 0:01 (missed) | -
10/20 | 18:25 | outbound  | +1 473-555-0198 | Grenada | 6 min    | $3.48
Total international: 60 min, $34.80 (Grenada $0.58/min). International & premium block: OFF.""", meta=dict(account="NB-40244867", via="email")),

item("em_lena_curtis", "email", "email", "D4 08:05", "t_curtis", "c_lena", "RE: Equipment fee dispute - NB-40122953 Curtis Wainwright - $150.00 NB-GX4", """Marisol,

Checked with Receiving: no return scanned against NB-GX4-77120. UPS does show our label delivered 10/14, but without the unit matched to the account I can't reverse the fee. Can you ask the customer for a photo of the serial label, or what was in the box? If he returned the wrong unit (people send us their own routers) the fee stands.

Lena""", to=[ME]),

item("ch_derek_v7", "chat", "message", "D4 08:15", "t_team4", "c_derek", "#team4", """v7 cancel script is LIVE today. Every cancel or downgrade: "You can cancel at any time, just say 'cancel' and I'll process it" BEFORE any offer. Tomas is scoring it from today. Also: voicemail cancels are 1 business day now for everyone, check your voicemail queue.""", to=TEAM, meta=dict(channel="#team4")),

item("ch_noc6", "chat", "message", "D4 09:00", "t_noc", "c_kevin", "#noc-status", """INC-26-1103 RFO (reason for outage), final
Cause: third-party contractor (directional boring for a water main, River Rd N & Chemawa Rd N) struck Northbeam feeder F-1 and the F-14 distribution cable at 06:42 PST 11/3. Locate ticket had been marked; contractor drilled outside the marks. Claim filed against contractor.
Impact: 4,800 internet / 1,062 Home Phone subscribers on OLT KZR-02.
Restoration: F-01 to F-13 (4,188) at 21:34 PST 11/3 (14 h 52 min). F-14 (612) at 13:10 PST 11/4 (30 h 28 min).
Follow-on: 23 premises with drop damage dispatched individually.""", to=["c_marisol"], meta=dict(channel="#noc-status", read_only=True)),

item("em_jess_fb", "email", "email", "D4 09:00", "t_fb", "c_jess", "Your feedback on INC-26-1103 by Fri noon", """Hi Tier 1,

I'm writing the after-action review for the Keizer outage with Priya and NOC on Friday afternoon. Reply to me by Friday 12:00 with what slowed you down, what information you didn't have when you needed it, and anything in the playbook, macros or tools you'd change. Specific examples (ticket numbers) help a lot.

Thanks,
Jess""", to=TEAM),

item("em_brady", "email", "email", "D4 09:20", "t_brady", "c_brady", "Outage callback lists = upgrade opportunity (send by 5 pm)", """Tier 1 team,

Great work this week. Let's turn the outage into a win. Two asks, approved on my side:

1. Tonight, call everyone on your INC-26-1103 callback lists again between 5:00 and 9:30 pm and pitch the 2 Gig upgrade at $95 (we'll waive the gateway swap).
2. For anyone who doesn't pick up, load them into the Genesys "Upgrade Offer" outbound campaign. It plays the recorded 2 Gig message and leaves it on voicemail. Upload your callback list CSVs to the campaign by 5:00 pm today and reply to me when done so I can start the dialer.

Thanks!
Brady Coates
Residential Sales Manager""", to=["c_marisol", "c_kayla", "c_omar"], meta=dict(note="Not sent through Contact Center Operations; no Compliance sign-off referenced.")),

item("ph_pop10", "phone", "screen_pop", "D4 10:03", "t_call_jim", "c_jim", "Inbound call, queue CANCEL, ANI 530-555-0170", """Genesys screen pop - Beam360 account NB-40411529
Customer: Jim Harlan, 412 Alder St, Mount Shasta CA 96067 (California account: v7 step 2 required on every account now). PIN on file: yes.
Plan: Fiber 300 $55.00 - autopay $5.00 = $50.00/month. Statement 11/01: $50.00 for November (billed in advance), due 11/18; autopay will draft 11/18.
Equipment: gateway NB-GX4 serial NB-GX4-74488. Tenure 2 years.
Offer Library eligible: 6 months $10 off; Wi-Fi Plus free 3 months.""", meta=dict(account="NB-40411529")),

item("em_analucia_rem", "email", "email", "D4 10:30", "t_bid", "c_analucia", "Reminder: holiday bid - you haven't submitted", """Hi Marisol,

Friendly reminder that the holiday bid closes tomorrow (Fri 11/6) at 5:00 pm and I don't see a bid from you yet. If you don't bid, WFM will assign one of the four days.

Ana Lucia""", to=[ME]),

item("ch_kayla_aht", "chat", "message", "D4 11:30", "t_team4", "c_kayla", "#team4", """is everyone's AHT trashed this week or just mine. 9:12 for me. Derek pls tell me it doesn't count""", to=TEAM, meta=dict(channel="#team4")),

item("tk_kimpham", "tickets", "ticket", "D4 12:15", "t_kimpham", "c_kimpham", "#88733 Where is my outage credit?", """Live chat, Thu 11/5/2026 12:15
Kim Pham: hi, I was told I'd get a credit for Tuesday's outage, I don't see it on my account

--- Beam360 side panel (account NB-40352290) ---
Logged in to portal (verified). Keizer, segment F-10 (restored 21:34 11/3). Plan Fiber 1 Gig $75.00 - autopay $5.00 = $70.00. No credits posted yet.""", meta=dict(account="NB-40352290", via="chat")),

item("tk_naomi_2", "tickets", "ticket", "D4 14:00", "t_naomi", "c_naomi", "RE: #88407 Moving to Corvallis", """From: Naomi Fischer <naomi.fischer@pm.me>
Sent: Thu 11/5/2026 2:00 PM

Hi Marisol, thanks so much. Actually yes, can we do Friday the 13th for the install? I get the keys on the 12th. Everything else the same.

Naomi

--- Beam360: install slots Corvallis: Fri 11/13 8-12 (open), Sat 11/14 8-12 (booked: NB-40377412).""", meta=dict(account="NB-40377412", via="email")),

item("ph_pop11", "phone", "screen_pop", "D4 14:28", "t_call_curtis", "c_curtis", "Inbound call, queue BILLING, ANI 541-555-0193", """Genesys screen pop - Beam360 account NB-40122953 (disconnected)
Customer: Curtis Wainwright. PIN on file: yes. Open case: Zendesk #88402 (T2-Billing, equipment fee dispute $150.00).
Final statement: $150.00 due 11/18.""", meta=dict(account="NB-40122953")),

item("em_tomas_ack", "email", "email", "D4 15:10", "t_qa", "c_tomas", "RE: QA dispute - 10/27 14:02 call", """Hi Marisol,

You're right, the Beam360 verification log shows the OTP sent to the mobile of record at 14:02:37 and entered at 14:03:05, before the balance was discussed. I've rescored the call to 98/100 and removed the compliance miss. I'll also add the verification log to the calibration checklist.

Thanks for flagging it.
Tomas""", to=[ME]),

item("ph_pop12", "phone", "screen_pop", "D4 16:08", "t_call_marcus", "c_marcus", "Inbound call, queue SALES-ADDON, ANI 503-555-0138", """Genesys screen pop - Beam360 account NB-40398877
Customer: Marcus Odom, 2215 Market St NE, Salem 97301. PIN on file: yes.
Plan: Fiber 1 Gig $75.00 - autopay $5.00 = $70.00/month. Gateway NB-GX4 (has 2 phone ports).
Home Phone eligibility: yes. Number port-in: 3-5 business days after the port request is submitted.""", meta=dict(account="NB-40398877")),

item("ch_derek_brady", "chat", "message", "D4 16:15", "t_team4", "c_derek", "#team4", """Re Brady's email this morning: do NOT upload callback lists to the Upgrade Offer campaign and no sales calls off the outage lists tonight. Compliance (Hannah) says a recorded marketing message needs the customer's prior written consent and these customers only asked for a restoration callback. Brady's been told.""", to=TEAM, meta=dict(channel="#team4")),
]

calls = [
call("call_d4_jim", "D4 10:05", "c_jim", "Cancellation under the new v7 script (California account)", [
    (C, "Hi, I want to cancel my internet. I found something cheaper.", 6),
    (H, "I can help with that, Jim. Can I have your account PIN?", None),
    (C, "It's 3 0 5 5 1 8.", 5),
    (H, "Thank you, you're verified. You can cancel at any time, just say 'cancel' and I'll process it. Before you decide, may I tell you about one offer we have?", None),
    (C, "No thanks, just cancel it.", 4),
    (H, "Understood, I'll process it now. Would you like the service to end today, November 5th, or on a later date?", None),
    (C, "Today's fine.", 5),
    (H, "Done, your service ends today. November was billed in advance at $50, so the 25 unused days come back as a $41.67 credit, which leaves $8.33 on your final bill for November 1 to 5. We'll email a prepaid UPS label for the gateway; please send it back by December 5 to avoid a $150 non-return fee. The white box on the wall stays.", None),
    (C, "Okay. That's it?", 5),
    (H, "That's it. You'll get a confirmation email in a few minutes. Thanks for being a Northbeam customer, Jim.", None)]),

call("call_d4_curtis", "D4 14:30", "c_curtis", "Angry former customer about the $150 fee; demands written confirmation now", [
    (C, "I got your email asking for a photo. I already gave you the tracking number. UPS says you got it. I want an email today saying the $150 is gone, or I'm filing with the Attorney General.", 3),
    (H, "I hear you, Curtis, and I'm sorry this is dragging on. Let me check your case. Can you give me your account PIN?", None),
    (C, "9 1 2 2 0 7.", 4),
    (H, "Thank you. Our Billing team confirmed the package was delivered on October 14th. What's holding it up is that the gateway hasn't been matched to your account in our warehouse system yet. A photo of the serial label, or the receipt, will let them match it.", None),
    (C, "So email me right now that it's removed. I'm not paying it.", 3),
    (H, "I can't confirm a removal that Billing hasn't made yet, and I don't want to tell you something that turns out wrong. What I can promise is that I'm on it: you don't need to pay the $150 while the case is open, and nothing goes to collections while it's under review.", None),
    (C, "I took a picture of the box before I sealed it, I think the sticker's in it. I'll send it tonight.", 5),
    (H, "That would be perfect. Reply to my email with the photo and I'll send it to Billing first thing tomorrow, and I'll email you as soon as they decide.", None),
    (C, "Fine.", 4),
    (H, "Thank you, Curtis. Talk to you tomorrow.", None)]),

call("call_d4_marcus", "D4 16:10", "c_marcus", "Adds Home Phone; price and 911 address", [
    (C, "Hi, I want to add a home phone line. My mom calls the landline, she won't use my cell. What does it cost?", 6),
    (H, "Happy to help, Marcus. Can I have your account PIN?", None),
    (C, "6 6 2 0 4 3.", 5),
    (H, "Thank you. Home Phone is $20 a month plus a $2.49 Regulatory Recovery and 911 fee, with unlimited US and Canada calling and voicemail. Your bill would go from $70 to $92.49 a month.", None),
    (C, "Okay. Can I keep my old landline number from my old phone company?", 6),
    (H, "Yes. I'll submit a port request, and the number usually moves in 3 to 5 business days; until then you'd have a temporary number. Do you have an account number or PIN from the old company? It's on their bill.", None),
    (C, "I'll have to find the bill. Can I email it?", 6),
    (H, "Please don't email account PINs; call back with it and any of us can submit the port. One more thing: for 911, your phone will be registered to 2215 Market Street Northeast. Is that where the phone will be used?", None),
    (C, "Yes.", 5),
    (H, "Great. Also good to know: Home Phone runs over your internet, so it won't work during a power or internet outage. Keep a cell phone handy for 911. I've added Home Phone with a temporary number today. Anything else?", None),
    (C, "No, thanks.", 6),
    (H, "Thanks, Marcus. Have a good evening.", None)]),
]

actions = [
act("a401", "D4 09:03", "read", "em_denise_fake", "Opened the email from denise.pruitt.home@outlook.com asking to change the email and send call records.", "Starts at 08:30 today (no OT)."),
act("a402", "D4 09:10", "reply", "em_denise_fake", """Hello,

Thank you for your message. For your security, we can't make account changes, reset PINs or share account information over email from an address that isn't on the account.

If you're the account holder, please call us at 1-800-555-0140 and we'll verify you with your account PIN or a code sent to the contact information already on file. We'll be glad to help then.

Northbeam Fiber Customer Care""", "Correct: no change, no information. She does not open the Account Security referral or connect it with yesterday's call."),
act("a403", "D4 09:35", "read", "em_brady", "Read Brady's email about the Upgrade Offer campaign.", "She is uneasy but does nothing; no reply."),
act("a404", "D4 10:20", "update_ticket", "ph_pop10", """Case note NB-40411529: CANCEL, reason PRICE-COMPETITOR. Caller Jim Harlan, verified PIN. v7 step 2 statement given before offer; customer declined to hear the offer and said cancel; processed immediately, no second offer. Disconnect DO-77590 effective 11/5/2026. Final bill: Nov $50.00 less credit 25 unused days x $50.00/30 = $41.67, net $8.33 (autopay). Return label for NB-GX4-74488 emailed; return by 12/5 or $150 fee.""", "After-call work; first v7 call."),
act("a405", "D4 10:42", "reply", "em_lena_curtis", """Thanks Lena, I'll ask him for a photo of the serial label and send it over as soon as I have it.
Marisol""", "She does not check the Returns Center unmatched-receipts sheet."),
act("a406", "D4 10:48", "reply", "tk_curtis", """Hi Curtis,

Quick update: our Billing team can see the package was delivered to our Returns Center on October 14, but they need to match the gateway to your account. If you have a photo of the serial number label (on the bottom of the gateway or the box, it starts with NB-GX4), or the UPS Store receipt, could you reply with it? That's the last piece they need.

You don't need to pay the $150.00 while this is under review.

Marisol
Northbeam Fiber Customer Care""", "Asks the customer for evidence that Northbeam's own receiving log already points to."),
act("a407", "D4 11:05", "reply", "tk_irene", """Dear Ms. Matsuda,

Thank you for writing, and I'm sorry this happened. I looked at your October calls, and yes, that's what it was. Each time, you had a missed call lasting one second from +1 473-555-0198, which is a number in Grenada (area code 473 looks like a US number but is international), and a few minutes later a call back to it. That's a known scam: the caller hangs up after one ring hoping you'll call back, then keeps you on hold so the international minutes add up.

There were six callbacks, 60 minutes in total, which is the $34.80 on your bill. I've applied a one-time courtesy credit of $34.80, so you won't pay for them. You'll see it on your December 1 statement.

To stop this happening again, I can turn on our free International & premium-number block on your home phone. Just reply "yes" and I'll switch it on. If an unfamiliar number calls once and hangs up, it's safest not to call back.

Kind regards,
Marisol
Northbeam Fiber Customer Care""", "Replying to the email of record with call detail is allowed (standard item 7). $34.80 is within Tier 1's $40 usage courtesy authority."),
act("a408", "D4 12:20", "reply", "tk_kimpham", """Hi Kim, good question. Credits for Tuesday's outage are automatic and post overnight tonight, so you'll see it on your account tomorrow, Friday 11/6. For your area (back at 9:34 pm Tuesday) it's one day of service, $2.33, and it'll be on your December 1 statement.""", "Policy-consistent: $70/30."),
act("a409", "D4 12:35", "send", "em_qa_eval", """Hi Tomas,

I'd like to dispute the 10/27 14:02 evaluation (Gutierrez). I verified by OTP, not PIN, so there's nothing to hear on the recording: the Beam360 verification log for NB-40196634 shows the OTP sent to the mobile of record at 14:02:37 and entered at 14:03:05, before I discussed the balance. Screenshot attached.

Could you take another look at the Verification score?

Thanks,
Marisol""", "Her own decision to dispute; within the 5-business-day window.", to=["c_tomas"], attachments=["verification-log-2026-10-27.png"]),
act("a410", "D4 13:00", "noop", "cal_1on1", "In 1:1 with Derek (13:00-13:30): October scorecard, QA dispute, Tier 2 Billing shadowing.", "Calendar."),
act("a411", "D4 14:44", "update_ticket", "ph_pop11", """Case note NB-40122953: Caller Curtis Wainwright, verified PIN. Upset; demanded written confirmation today that the $150 fee is removed and mentioned the Attorney General. Explained Billing needs the unit matched; no promise of removal. Told him not to pay while under review. He will send a photo of the label tonight. Zendesk #88402 open with T2-Billing.""", "After-call work."),
act("a412", "D4 15:05", "reply", "tk_naomi_2", """Hi Naomi, done! Your install at 1450 NW Kings Blvd Apt 3B is now Friday, November 13, 8-12. Everything else stays the same: old address disconnects November 15, and Fiber 300 at $50.00 a month. Congrats on the keys!

Marisol""", "Move order change."),
act("a413", "D4 16:22", "update_ticket", "ph_pop12", """Case note NB-40398877: Caller Marcus Odom, verified PIN. Added Home Phone ($20.00 + $2.49 fee); new monthly $92.49. Temporary number 503-555-0124 assigned; customer will call back with old carrier account number/PIN for port-in (told not to email it). E911 registered address confirmed: 2215 Market St NE, Salem 97301. Advised Home Phone doesn't work in power/internet outages. Order HP-40917.""", "After-call work."),
act("a414", "D4 16:30", "read", "ch_derek_brady", "Read Derek's message: no uploads to the Upgrade Offer campaign.", "She never uploaded."),
]
