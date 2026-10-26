from common import item, act, call, C, H, ME

TEAM = ["c_marisol", "c_kayla", "c_omar", "c_derek"]
items = [
item("em_billing_batch", "email", "email", "D5 06:30", "t_autocredit", "c_wendy", "INC-26-1103 credits posted", """Customer Care,

The INC-26-1103 credit batch ran overnight and credits are now on accounts:
- F-01 to F-13: 4,188 accounts, 1 day each.
- F-14: 612 accounts, 2 days each.
Credits show as "Service interruption credit INC-26-1103" and will be on the 12/1 statement.

Anything that looks wrong: the INC-26-1103 Credit Correction form, please, no manual adjustments.

Wendy""", to=TEAM),

item("tk_curtis_photo", "tickets", "ticket", "D5 08:10", "t_curtis", "c_curtis", "RE: #88402 Charged $150 for a router I RETURNED", """From: Curtis Wainwright <cwainwright.or@gmail.com>
Sent: Thu 11/5/2026 11:52 PM (opened in queue Fri 08:10)

Here. Photo of the router in the box before I taped it, and the UPS Store receipt from Oct 9.

[image: router_in_box.jpg - label reads "Northbeam NB-GX4  S/N NB-GX4-77120  MAC 3C:84:6A:1F:22:90"]
[image: ups_receipt.jpg - The UPS Store #4412, Albany OR, 10/09/2026 2:14 PM, tracking 1Z8V41E70391245563, prepaid return label]

Curtis""", attachments=[], meta=dict(account="NB-40122953", via="email")),

item("ch_derek_fri", "chat", "message", "D5 08:20", "t_team4", "c_derek", "#team4", """Happy Friday. Week so far: team handled 2,740 contacts Mon-Thu, AHT 7:48 (outage days). Priya confirmed AHT and adherence for 11/3-11/4 are excluded from October/November scorecards. Feedback for Jess is due at noon, please send her something, she's presenting at 2.""", to=TEAM, meta=dict(channel="#team4")),

item("em_rosa_thanks", "email", "email", "D5 08:30", "t_rosa", "c_rosa", "RE: #88602 Outage letter for my insurance", """Marisol, my agent filed it yesterday and said it was exactly what she needed. Thank you for following through.

Rosa""", meta=dict(account="NB-40333620", via="email")),

item("em_jess_rem", "email", "email", "D5 09:00", "t_fb", "c_jess", "Reminder: INC-26-1103 feedback by noon", """Hi all, reminder that I need your outage feedback by 12:00 today for the 2:00 review. Even three bullet points help.
Jess""", to=TEAM),

item("tk_irene_2", "tickets", "ticket", "D5 09:30", "t_irene", "c_irene", "RE: #88701 International calls I didn't make??", """From: Irene Matsuda <irene.matsuda@comcast.net>
Sent: Fri 11/6/2026 9:30 AM

Thank you so much dear. Yes please turn on the block. Does it also stop those 900 numbers? My neighbor got a big bill from one of those. And is there a charge for it?

Irene""", meta=dict(account="NB-40244867", via="email")),

item("ph_pop13", "phone", "screen_pop", "D5 09:38", "t_call_paul", "c_paul", "Inbound call, queue BILLING, ANI 503-555-0161", """Genesys screen pop - Beam360 account NB-40305572
Customer: Paul Nakamura, 6044 Windsor Island Rd N, Keizer 97303. PIN on file: yes.
Network: OLT KZR-02, segment F-14. ONT log: offline 06:42 11/3, online 13:11 11/4.
Plan: Fiber 1 Gig $75.00 (autopay off). Monthly recurring service charges $75.00.
Credits: 11/06 "Service interruption credit INC-26-1103" -$2.50.""", meta=dict(account="NB-40305572")),

item("tk_hector_2", "tickets", "ticket", "D5 10:00", "t_hector", "c_hector", "RE: #88405 double charged in october", """From: Hector Alvarado <hector.alvarado71@gmail.com>
Sent: Fri 11/6/2026 10:00 AM

hi any update on my refund? its been 4 days and I havent heard anything

Hector""", meta=dict(account="NB-40318827", via="email")),

item("tk_eleanor", "tickets", "ticket", "D5 10:40", "t_eleanor", "c_eleanor", "#88790 Paper bill charge", """From: Eleanor Pike <epike1954@gmail.com>
Sent: Fri 11/6/2026 10:40 AM

I see a $1.99 charge for a paper bill. I don't use computers much and I need the paper bill. My friend said you don't charge seniors. I'm 72.

Eleanor Pike

--- Beam360 side panel (account NB-40116673) ---
Email of record epike1954@gmail.com (since 2020). Date of birth on file: 1954 (age 72). Paper bill $1.99/month since 2026-07-01.""", meta=dict(account="NB-40116673", via="email")),

item("tk_ryan", "tickets", "ticket", "D5 11:00", "t_ryan", "c_ryan", "#88794 Black Friday for existing customers?", """Web form, Fri 11/6/2026 11:00 AM
Ryan Castillo: Are you doing any Black Friday deals for people who already have Northbeam? My neighbor just signed up for 2 Gig at a promo price.

--- Beam360 side panel (account NB-40409118) ---
Email of record rcastillo.or@gmail.com. Plan Fiber 1 Gig $75.00 - autopay $5.00. Current public offers: none for existing customers; new-customer 2 Gig promo $80 for 12 months (new households only).""", meta=dict(account="NB-40409118", via="web form")),

item("ch_kayla_fri", "chat", "message", "D5 12:10", "t_team4", "c_kayla", "#team4", """taco truck is back in the lot!! who's in""", to=TEAM, meta=dict(channel="#team4")),

item("ph_pop14", "phone", "screen_pop", "D5 13:13", "t_call_diane", "c_diane", "Inbound call, queue ACCOUNT-CHANGES, ANI 503-555-0102", """Genesys screen pop - Beam360 account NB-40228410
Account holder: Harold Kessler. Authorized users: Diane Kessler (own PIN on file).
Plan: Fiber 300 $55.00 - autopay $5.00 + Home Phone $20.00 (503-555-0175) + Regulatory Recovery & 911 Fee $2.49 = $72.49/month. November billed 11/1, autopay.""", meta=dict(account="NB-40228410")),

item("em_analucia_final", "email", "email", "D5 14:00", "t_bid", "c_analucia", "Holiday bid closes at 5 pm today", """Last call: holiday bids close at 5:00 pm. Marisol, Omar, I still don't have yours.
Ana Lucia""", to=["c_marisol", "c_omar"]),

item("em_lena_curtis_done", "email", "email", "D5 14:40", "t_curtis", "c_lena", "RE: Equipment fee dispute - NB-40122953 - resolved", """Marisol,

Thanks for the photo. Receiving found it: the unit came in on 10/15 on his tracking number but was hand-keyed as NB-GX4-77102 while their scanner was down (digits swapped). Matched to his account now and the $150.00 non-return fee is reversed (ADJ-55120). His final balance is $0.00. Receiving is re-checking the other hand-keyed entries from that week.

Lena""", to=[ME]),

item("em_wfm_sched", "email", "email", "D5 15:00", "t_sched", "c_analucia", "Schedules for 11/9-11/13 published", """Schedules for next week are in the WFM portal. Team 4: normal shifts; digital blocks 10-11 and 2-3. Veterans Day (Wed 11/11) is a normal working day for the contact center.
Ana Lucia""", to=TEAM),

item("ph_pop15", "phone", "screen_pop", "D5 15:28", "t_call_dolores", "c_dolores", "Inbound call, queue BILLING-COLLECTIONS, ANI 503-555-0118", """Genesys screen pop - Beam360 account NB-40263391
Customer: Dolores Ruiz, 1422 Ward Dr NE, Salem. PIN on file: yes.
Plan: Fiber 300 $55.00 + Home Phone $20.00 + Regulatory Recovery & 911 Fee $2.49 = $77.49/month. Autopay off.
Balance: October statement $77.49 unpaid (due 10/18) + late fee $10.00 (11/02) + November statement $77.49 (due 11/18) = $164.98.
Payment arrangements in last 12 months: none. Late fee waivers in last 12 months: none. Suspension for non-payment at 45 days past due (12/02).""", meta=dict(account="NB-40263391")),
]

calls = [
call("call_d5_paul", "D5 09:40", "c_paul", "Batch outage credit too small for an F-14 customer", [
    (C, "Hi, I got a credit for the outage this week but it's $2.50. I was out from Tuesday morning until Wednesday afternoon, that's more than a day.", 6),
    (H, "Thanks for checking, Paul. Let me look. Can I have your account PIN?", None),
    (C, "4 7 1 9 9 0.", 5),
    (H, "Thank you. You're right: your service was down from 6:42 Tuesday until 1:11 Wednesday afternoon, about 30 and a half hours. That counts as two days, so your credit should be $5.00, two days of your $75 plan, not $2.50.", None),
    (C, "Okay, so can you fix it?", 5),
    (H, "I'm sending a correction to our Billing team right now for the missing $2.50. They fix these within 2 business days, so you'll see it by Tuesday, and it'll be on your December 1 statement either way.", None),
    (C, "Why can't you just add it?", 4),
    (H, "For this outage the credits are done centrally so nobody gets double-credited, so corrections go through Billing. It's already submitted under your account.", None),
    (C, "Alright. Thanks.", 5),
    (H, "Thank you for catching it, Paul. Have a good weekend.", None)]),

call("call_d5_diane", "D5 13:15", "c_diane", "Authorized user removes Home Phone (downgrade under v7)", [
    (C, "Hi, I'd like to take the home phone off our account, we only use our cell phones now.", 6),
    (H, "I can help, Diane. Can I have your PIN?", None),
    (C, "8 0 4 4 1 6.", 5),
    (H, "Thank you, you're verified as an authorized user on Harold's account. You can cancel at any time, just say 'cancel' and I'll process it. Before you do, would you like to hear one offer?", None),
    (C, "No, just take it off.", 4),
    (H, "Okay, I'll remove Home Phone today. One thing first: the number 503-555-0175 will be released, so if you want to keep it you'd need to move it to another provider before I remove it. And 911 calls would be from your cell phones. Still okay?", None),
    (C, "Yes, we don't need the number.", 5),
    (H, "Done. Home Phone is removed as of today. You'll get a $16.00 credit for the 24 unused days of November, and from December your bill is $50.00 a month for internet with autopay.", None),
    (C, "Great, thanks.", 6),
    (H, "You're welcome, Diane. Have a nice weekend.", None)]),

call("call_d5_dolores", "D5 15:30", "c_dolores", "Past-due balance; payment arrangement", [
    (C, "Hi, I'm behind on my bill. I had my hours cut and I can't pay it all right now. Are you going to shut it off?", 5),
    (H, "I'm sorry about your hours, Dolores, let's see what we can do. Can I have your account PIN?", None),
    (C, "2 2 7 1 5 0.", 5),
    (H, "Thank you. Your service isn't being shut off today. The balance right now is $164.98: October's $77.49, a $10 late fee, and November's $77.49, which is due the 18th. When could you make payments?", None),
    (C, "I get paid next Friday, the 13th, and then again at the beginning of December.", 6),
    (H, "Then here's what I can do: I'll waive the $10 late fee and set up a payment arrangement for the remaining $154.98 in two payments of $77.49, one on Friday November 13 and one on Friday December 4. As long as those two payments are made, no new late fees and the service stays on.", None),
    (C, "Oh, that would help a lot. How do I pay?", 6),
    (H, "On each of those days you can pay at pay.northbeamfiber.com or by calling 1-800-555-0140 and pressing 2, our secure automated line. I'll email you a confirmation of the two dates and amounts.", None),
    (C, "Thank you so much.", 6),
    (H, "You're welcome, Dolores. Take care.", None)]),
]

actions = [
act("a501", "D5 09:05", "read", "em_billing_batch", "Read the INC-26-1103 batch notice.", "Start of day."),
act("a502", "D5 09:12", "forward", "tk_curtis_photo", """Lena, here's what Curtis sent: photo of the unit in the box before sealing, label S/N NB-GX4-77120, and the UPS Store receipt (10/09, tracking 1Z8V41E70391245563). Can you match it and reverse the $150? Zendesk #88402.
Marisol""", "Forwards the evidence.", to=["c_lena"]),
act("a503", "D5 09:55", "create_doc", "doc_correction_form", """INC-26-1103 Credit Correction (T2-Billing, tag INC-26-1103-CORR)
Account: NB-40305572  Customer: Paul Nakamura  Verified by: PIN
Segment: F-14  Restoration time for this account: ONT online 13:11 11/4 (offline from 06:42 11/3, 30 h 29 min)
Monthly recurring service charges: $75.00
Days due under the incident rule: 2  Credit due: $5.00
Credit posted by the batch: $2.50
Correction requested (credit due - credit posted): $2.50
Customer told: correction within 2 business days, on 12/1 statement""", "Per the Wednesday policy; no manual adjustment."),
act("a504", "D5 09:58", "update_ticket", "ph_pop13", """Case note NB-40305572: INC-26-1103. Caller Paul Nakamura, verified PIN. F-14, batch credited 1 day ($2.50) instead of 2 ($5.00). Submitted Credit Correction for $2.50 (form sent 09:55). Customer informed: 2 business days.""", "After-call work. She does not ask whether other F-14 accounts got 1 day."),
act("a505", "D5 10:15", "reply", "tk_hector_2", """Hi Hector,

I'm sorry, I should have written to you on Wednesday. Your refund is done: $80.00 was refunded to your Visa ending 4421 on November 4 (reference RF-209917). It usually takes 5 to 7 business days to appear, so you should see it by about November 13.

As mentioned, because the $80.00 went back to your card, your November bill of $80.00 is due on November 18 and autopay will take it that day.

Thanks for your patience,
Marisol
Northbeam Fiber Customer Care""", "Late follow-up; prompted by the customer."),
act("a506", "D5 10:50", "reply", "tk_eleanor", """Dear Ms. Pike,

Your friend is right. We waive the paper bill fee for customers 65 and older, and I've removed it from your account starting with your December bill. You'll keep getting your paper bill in the mail as usual.

Warm regards,
Marisol
Northbeam Fiber Customer Care""", "Policy on the rate card."),
act("a507", "D5 11:20", "reply", "tk_ryan", """Hi Ryan,

Thanks for asking. The 2 Gig promotion your neighbor got is for new households only, and we don't have a Black Friday offer for existing customers right now. I'd keep an eye on your email in late November in case that changes. If you'd like 2 Gig at the regular price, it's $95.00 a month ($90.00 with autopay) and the gateway swap is free.

Marisol
Northbeam Fiber Customer Care""", "No invented promo."),
act("a508", "D5 13:28", "update_ticket", "ph_pop14", """Case note NB-40228410: DOWNGRADE, reason NOT-USED. Caller Diane Kessler (authorized user), verified PIN. v7 step 2 statement given; declined offer. Removed Home Phone 503-555-0175 effective 11/6 after confirming number release and 911 via cell. Credit 24 unused days x $20.00/30 = $16.00. New monthly $50.00 from December.""", "After-call work."),
act("a509", "D5 13:40", "reply", "tk_irene_2", """Dear Ms. Matsuda,

Done: the International & premium-number block is now on for your home phone, and it's free. It blocks calls to international numbers, including the Caribbean area codes that look like US numbers, and to premium-rate 900 and 976 numbers. Your calls to the US and Canada aren't affected. If you ever need to call abroad, just call us and we can lift it.

Kind regards,
Marisol
Northbeam Fiber Customer Care""", "Answers the follow-up a few hours later."),
act("a510", "D5 15:44", "update_ticket", "ph_pop15", """Case note NB-40263391: Caller Dolores Ruiz, verified PIN. Hours cut. Waived late fee $10.00 (first in 12 months). Payment arrangement PA-30871: balance $154.98 in 2 installments of $77.49 on 11/13 and 12/04 (within 30 days). Confirmation email sent. Pay via pay.northbeamfiber.com or IVR option 2.""", "After-call work; within authority matrix item 8."),
act("a511", "D5 16:20", "send", "em_analucia_final", """Hi Ana Lucia, my holiday bid: 1st choice Thu 12/31 (to 2 pm), 2nd choice Fri 11/27. Thanks!
Marisol""", "Her personal decision, made at the deadline.", to=["c_analucia"]),
act("a512", "D5 16:45", "reply", "tk_curtis_photo", """Hi Curtis,

Good news: Billing found your gateway. It arrived at our Returns Center on October 15 on your tracking number, but its serial was typed in wrong by hand, so it never matched your account. That's fixed, the $150.00 fee has been reversed, and your final balance is $0.00. There's nothing more you need to do.

I'm sorry for the hassle and thank you for sending the photo.

Marisol
Northbeam Fiber Customer Care""", "Closes the loop two hours after Lena's email."),
]
