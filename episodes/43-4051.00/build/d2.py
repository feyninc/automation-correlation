from common import item, act, call, C, H, ME

TEAM = ["c_marisol", "c_kayla", "c_omar", "c_derek"]
items = [
item("ch_noc1", "chat", "message", "D2 07:05", "t_noc", "c_kevin", "#noc-status", """:rotating_light: INC-26-1103 SEV2 - OPEN
Start: 06:42 PST 11/3. Cause: third-party directional boring cut feeder cable F-1 at River Rd N & Chemawa Rd N, Keizer.
Impact: OLT KZR-02 down, about 4,800 subscribers, Keizer north of Lockhaven Dr NE (ZIP 97303). Internet and Home Phone.
ETR: under assessment. Do NOT give customers an ETR yet.
Next update by 10:30. Affected-area sheet attached in Guru.""", to=["c_marisol"], meta=dict(channel="#noc-status", read_only=True)),

item("em_priya_inc", "email", "email", "D2 07:30", "t_inc", "c_priya", "INC-26-1103 Keizer outage - all hands on phones today", """Team,

We have a major outage in north Keizer (INC-26-1103, about 4,800 customers). The IVR outage message is live for Keizer callers, but expect three to four times normal volume today.

- Digital blocks are cancelled today. Everyone on phones; tickets only between calls if the queue allows.
- Use the Outage Contact Playbook. Check every address against the affected-area sheet before you use the outage macro.
- No ETRs until NOC posts one. No credits until restoration.
- Overtime is approved today and tomorrow. Tell Derek if you can stay late or come in early.
- Tag every case INC-26-1103.

Thank you, this will be a long day.
Priya""", to=TEAM),

item("sheet_affected", "docs", "sheet", "D2 07:40", "t_inc_area", "c_kevin", "INC-26-1103 affected area (OLT KZR-02)", """INC-26-1103 - affected area, as of 07:40 11/3 (NOC)
OLT: KZR-02 (all 14 distribution segments F-01 to F-14)
City / ZIP: Keizer 97303 only, north of Lockhaven Dr NE, between River Rd N and the Willamette River, up to Chemawa Rd N and Wheatland Rd N.
Accounts: 4,800 (internet 4,800; Home Phone 1,062)
NOT affected: Keizer south of Lockhaven Dr NE (OLT KZR-01); Salem; Monmouth/Independence (OLT MNM-01); Woodburn; Albany; Corvallis.
Beam360 lookup: account > Service > Network shows OLT and segment.""", meta=dict()),

item("tk_lionel", "tickets", "ticket", "D2 07:52", "t_lionel", "c_lionel", "#88466 No internet or phone since 6:45 this morning", """From: Lionel Baptiste <lbaptiste@baptistedesign.co>
Sent: Tue 11/3/2026 7:52 AM

No internet, no home phone since about 6:45. I work from home (graphic design) and I have client calls all day. I'm tethering off my cell which is eating my data.

When will it be back and what are you going to do about the days I'm paying for and not getting? I pay over a hundred dollars a month for this.

Lionel Baptiste

--- Beam360 side panel (account NB-40290815) ---
Email of record: lbaptiste@baptistedesign.co (since 2022)
Service address: 5820 Windsor Island Rd N, Keizer 97303. Network: OLT KZR-02, segment F-14.
Plan: Fiber 1 Gig $75.00 + Home Phone $20.00 + Wi-Fi Plus $10.00 = $105.00 monthly recurring service charges; Regulatory Recovery & 911 Fee $2.49. Autopay off.
ONT status: OFFLINE since 06:42 11/3.""", meta=dict(account="NB-40290815", via="email")),

item("tk_scott", "tickets", "ticket", "D2 07:58", "t_scott", "c_scott", "#88468 internet down?", """Web form, Tue 11/3/2026 7:58 AM
Scott Hargrove: is there an outage in Keizer? nothing works since early this morning. lights on the white box are blinking red.

--- Beam360 side panel (account NB-40347715) ---
Service address: 7131 Sunset Ave N, Keizer 97303. Network: OLT KZR-02, segment F-06. ONT OFFLINE since 06:42.
Email of record: s.hargrove@yahoo.com (since 2021).""", meta=dict(account="NB-40347715", via="web form")),

item("tk_maya", "tickets", "ticket", "D2 08:40", "t_maya", "c_maya", "#88479 Internet out - is this the Keizer outage?", """From: Maya Sorensen <maya.sorensen@wou.edu>
Sent: Tue 11/3/2026 8:40 AM

Hi, my internet has been down since around 8 this morning. I saw on the neighborhood Facebook group there's a big outage in Keizer, I assume it's that? Any idea when it'll be fixed? I teach online classes at 1 pm.

Thanks,
Maya

--- Beam360 side panel (account NB-40366104) ---
Email of record: maya.sorensen@wou.edu (since 2024)
Service address: 455 Jackson St N, Monmouth OR 97361. Network: OLT MNM-01, segment M-04.
Plan: Fiber 300 $55.00 - autopay $5.00.
ONT status: OFFLINE since 07:58 11/3. Last alarm: "dying gasp" (power loss at ONT) 07:58.
Other ONTs on segment M-04: 37 of 37 online.""", meta=dict(account="NB-40366104", via="email")),

item("ph_pop4", "phone", "screen_pop", "D2 09:08", "t_call_jordan", "c_jordan", "Inbound call, queue TECH-OUTAGE (IVR: Keizer outage message played), ANI 503-555-0151", """Genesys screen pop - Beam360 account NB-40342281
Customer: Jordan Mehta, 4420 Shoreline Dr N, Keizer 97303. PIN on file: yes.
Network: OLT KZR-02, segment F-09. ONT OFFLINE since 06:42 11/3. Incident: INC-26-1103.
Plan: Fiber 1 Gig $75.00 - autopay $5.00 = $70.00/month.
IVR: caller pressed 0 three times; waited 22:40 in queue.""", meta=dict(account="NB-40342281")),

item("ch_kayla_ivr", "chat", "message", "D2 09:50", "t_team4", "c_kayla", "#team4", """IVR is telling people 40 min wait lol. Third caller in a row asking if we're "even working on it". I've been saying crews are on site, is that right? NOC hasn't said that""", to=TEAM, meta=dict(channel="#team4")),

item("ch_noc2", "chat", "message", "D2 10:15", "t_noc", "c_kevin", "#noc-status", """INC-26-1103 UPDATE 10:15
Splice crew on site since 08:50. Feeder F-1 temporary splice in progress.
ETR (estimate): 18:00 today for segments F-01 to F-13 (about 4,188 subs).
Segment F-14 (Windsor Island Rd N area, 612 subs): distribution cable also damaged, needs replacement. ETR not yet available.
Next update by 14:00.""", to=["c_marisol"], meta=dict(channel="#noc-status", read_only=True)),

item("ch_omar_free", "chat", "message", "D2 10:30", "t_team4", "c_omar", "#team4", """customer is SCREAMING at me, says he's owed a free month. can I just give him a free month credit to calm him down?? its like $75""", to=TEAM, meta=dict(channel="#team4")),

item("ch_derek_reply", "chat", "message", "D2 10:34", "t_team4", "c_derek", "#team4", """@Omar no. Free months aren't ours to give and $75 is over Tier 1's $40 anyway. Outage credit per the playbook after restoration, 1 day per started 24h. If he wants a supervisor, transfer to me.""", to=TEAM, meta=dict(channel="#team4")),

item("ph_pop5", "phone", "screen_pop", "D2 11:48", "t_call_edith", "c_edith", "Inbound call, queue GENERAL, ANI 503-555-0164 (mobile)", """Genesys screen pop - Beam360 account NB-40100457
Customer: Edith Caldwell, 3015 Delight St N, Keizer 97303. PIN on file: no. Mobile of record: 503-555-0164.
Network: OLT KZR-02, segment F-11. ONT OFFLINE since 06:42 11/3. Incident: INC-26-1103.
Plan: Fiber 300 $55.00 + Home Phone $20.00 (503-555-0106). Age on file: 81. Notes: "customer's daughter Joan helps with account".""", meta=dict(account="NB-40100457")),

item("em_kb_v7", "email", "email", "D2 12:30", "t_kb", "c_jess", "Published: Cancellations, Downgrades and Save Offers v7 (effective Thu 11/5)", """Hi all,

v7 of the cancellation card is published (attached) and takes effect Thursday 11/5 at the start of shift. The short version:
- Every cancellation or downgrade contact, every state: say "You can cancel at any time, just say 'cancel'" BEFORE any offer.
- If they say cancel again after that, process it. No second offer.
- Voicemail and email cancellation requests, every state: process or call back within ONE business day.
- Never hold a cancellation until equipment is returned.

Questions to me or your lead.
Jess""", to=TEAM, attachments=["doc_cancel_v7"]),

item("doc_cancel_v7", "docs", "doc", "D2 12:30", "t_doc_cancel_v7", "c_jess", "Cancellations, Downgrades and Save Offers (v7, effective 2026-11-05)", """Cancellations, Downgrades and Save Offers - script and rules
Version 7, effective Thursday 2026-11-05. Replaces v6 (2026-06-01). Owner: Knowledge & Training, approved by Compliance (H. Stiles).

What changed from v6 is marked [NEW].
1. Any Tier 1 rep may process a cancellation or downgrade (removing Home Phone, Wi-Fi Plus, or a lower plan).
2. [NEW] Every state: before any offer, and before asking more than one reason question, say: "You can cancel at any time, just say 'cancel' and I'll process it." (Aligns all states with Cal. Bus. & Prof. Code 17602(e).)
3. Ask the reason once. Moving outside the service area: no offer; process.
4. Otherwise you may present ONE save offer from the Offer Library, or transfer to Loyalty only if the customer asks for something else. [NEW] If the customer says "cancel" (or words to that effect) again, process immediately: no second offer, no transfer.
5. Effective date: the date the customer asks for. Unused days are credited on the final bill at the net monthly service charge / 30 per day.
6. Equipment: gateway and mesh extender back within 30 days with the prepaid UPS label, or the non-return fee applies. [NEW] Never make a cancellation wait for the equipment return. The ONT stays.
7. [NEW] Voicemail and email cancellation requests, every state: within ONE business day of receipt, process the cancellation or call the customer back. A voicemail cannot verify the caller, so call back the phone of record to verify and confirm. (Cal. Bus. & Prof. Code 17602(c).)
8. Case note: CANCEL or DOWNGRADE plus reason code; note that the step 2 statement was given.
Legal basis: FTC ROSCA, 15 U.S.C. 8403 (simple mechanisms to stop recurring charges); Cal. Bus. & Prof. Code 17602.""", meta=dict(effective="D4 08:30")),

item("em_phish", "email", "email", "D2 13:05", "t_phish", "c_fake_it", "ACTION REQUIRED: Zendesk moving to backup instance (INC-26-1103)", """From: Northbeam IT Service Desk <it-servicedesk@northbeam-itsupport.com>
Sent: Tue 11/3/2026 1:05 PM

Due to the load from INC-26-1103, Customer Care's Zendesk is being moved to a backup instance at 3:00 PM today. To keep your assigned tickets, re-authenticate with your Northbeam SSO credentials before 3:00 PM:

https://zendesk-northbeam-backup.com/sso/login

Agents who do not re-authenticate will lose their queue assignments and will need to open a ticket with IT to restore them.

Northbeam IT Service Desk""", to=[ME], meta=dict(headers="SPF: fail; sender domain northbeam-itsupport.com registered 2026-10-30")),

item("tk_megan", "tickets", "ticket", "D2 14:20", "t_megan", "c_megan", "#88531 Chat: when will Keizer internet be back", """Live chat, Tue 11/3/2026 14:20
Megan Fry: hi. Keizer outage. Any time estimate yet? I need to know if I should go work from the library.

--- Beam360 side panel (account NB-40321184) ---
Service address: 1290 Shady Ln N, Keizer 97303. OLT KZR-02, segment F-02. ONT OFFLINE since 06:42. Logged in to portal (verified).""", meta=dict(account="NB-40321184", via="chat")),

item("ph_pop6", "phone", "screen_pop", "D2 15:18", "t_call_rosa", "c_rosa", "Inbound call, queue TECH-OUTAGE, ANI 503-555-0133", """Genesys screen pop - Beam360 account NB-40333620
Customer: Rosa Villanueva, 870 Cummings Ln N, Keizer 97303. PIN on file: yes.
Network: OLT KZR-02, segment F-03. ONT OFFLINE since 06:42 11/3. Incident: INC-26-1103.
Plan: Fiber 1 Gig $75.00 - autopay $5.00. Email of record: rosa@villanuevabookkeeping.com (since 2022).""", meta=dict(account="NB-40333620")),

item("em_derek_ot", "email", "email", "D2 15:50", "t_ot", "c_derek", "OT tomorrow 07:00-08:30?", """Team 4,

Priya approved OT for tomorrow. I need four people to start at 7:00 instead of 8:30 (callbacks and the morning spike). Reply if you want it, first come first served.

Derek""", to=TEAM),

item("ch_noc3", "chat", "message", "D2 16:30", "t_noc", "c_kevin", "#noc-status", """INC-26-1103 UPDATE 16:30
Temporary splice on F-1 taking longer than planned (second cable found damaged).
ETR (estimate) for F-01 to F-13 REVISED: 21:30 tonight.
F-14 (612 subs): replacement cable being pulled; ETR Wed 11/4, 12:00-14:00.
Callbacks: customers can request a restoration callback through IVR option 3; callback lists go to Tier 1 tomorrow morning.""", to=["c_marisol"], meta=dict(channel="#noc-status", read_only=True)),

item("tk_dale", "tickets", "ticket", "D2 16:45", "t_dale", "c_dale", "#88560 Is it going to be back by 6?", """From: Dale Whitcomb <dwhitcomb55@gmail.com>
Sent: Tue 11/3/2026 4:45 PM

The guy I talked to at lunch said 6pm. Is that still right? My wife is on oxygen and her concentrator alerts go through the home phone, I need to know whether to take her to her sister's tonight.

Dale

--- Beam360 side panel (account NB-40336052) ---
Email of record dwhitcomb55@gmail.com (since 2020). Service address 1150 Rivercrest Dr N, Keizer 97303. OLT KZR-02, segment F-08. ONT OFFLINE since 06:42. Plan: Fiber 300 + Home Phone.""", meta=dict(account="NB-40336052", via="email")),
]

calls = [
call("call_d2_jordan", "D2 09:10", "c_jordan", "Angry work-from-home caller in the Keizer outage", [
    (C, "Finally. I've been on hold for twenty minutes. My internet's been dead since before seven and I have a deadline today. When is it coming back?", 4),
    (H, "I'm really sorry, Jordan, both for the outage and the wait. Let me pull up your account. Can I have your PIN?", None),
    (C, "1 9 3 3 0 5. So when?", 4),
    (H, "Thank you, you're verified. Your address is in the area of a fiber cut in north Keizer this morning; a contractor hit our main cable at 6:42. Repair crews are working on it, but our network team hasn't posted a time estimate yet, and I don't want to give you a guess.", None),
    (C, "That's ridiculous. I'm paying for this. I want a free month.", 3),
    (H, "I understand. I can't give a free month, but you will get an outage credit: for an outage of four hours or more, one day of your service for each 24 hours you're down, applied after it's restored. And I can set you up for a callback the moment it's back.", None),
    (C, "One day? That's like two bucks. Whatever. Yes, call me when it's back.", 4),
    (H, "Done, you're on the restoration callback list at this number, 503-555-0151. In the meantime, the Keizer library and the Salem library have free Wi-Fi if you need to get your deadline in. Is there anything else I can do right now?", None),
    (C, "No. Just fix it.", 4),
    (H, "We're on it. Thank you for your patience, Jordan.", None)]),

call("call_d2_edith", "D2 11:50", "c_edith", "81-year-old customer: Home Phone and medical alert down", [
    (C, "Hello? My telephone isn't working, the house phone. My medical alert button goes through it, my daughter set it up. I'm calling from the little cell phone.", 8),
    (H, "Hello Mrs. Caldwell, I'm glad you called. I'll help you. To look at your account I need to send a code to your cell phone; is that the phone you're calling from, ending 0164?", None),
    (C, "Yes, this one. Oh, it buzzed. It says 4 1 7 7 2 0.", 8),
    (H, "That's it, thank you, you're verified. There's a big outage in your part of Keizer since this morning, so your house phone and internet are both down. While it's out, the house phone can't call 911, and your medical alert button may not work either.", None),
    (C, "Oh dear. What should I do?", 8),
    (H, "Please keep the cell phone you're on now charged and near you, and use it to call 911 if you need help. It would also be a good idea to call your medical alert company; many can switch your button to a cellular backup. Would you like me to note your daughter Joan so we can reach her too?", None),
    (C, "Joan's number is in my cell, I'll call her. When will it be fixed?", 8),
    (H, "The crews are repairing it now and the estimate for your area is around 6 this evening, but it could change. I'm putting you at the top of our callback list so we call your cell when it's back, and I've marked your account so we know about your medical alert.", None),
    (C, "Thank you, dear. You've been very kind.", 8),
    (H, "You're welcome, Mrs. Caldwell. Keep that cell phone close, and we'll call you as soon as it's fixed.", None)]),

call("call_d2_rosa", "D2 15:20", "c_rosa", "Home business needs written outage confirmation for insurance", [
    (C, "Hi, I run a bookkeeping business out of my house and I've lost a full day of client work. My business insurance has interruption coverage but they need something in writing from you. Can you give me that?", 6),
    (H, "Absolutely, Rosa, we can do that. Can I verify you with your PIN first?", None),
    (C, "Sure, 5 5 8 0 1 4.", 5),
    (H, "Thank you. I can see your address is in today's outage, incident INC-26-1103, which started at 6:42 this morning. We have a standard outage confirmation letter with the incident number and the start and restoration times for your segment.", None),
    (C, "Great. Can you send it now?", 5),
    (H, "I can't send it until your service is restored, because the letter needs the restoration time; right now the estimate for your area is this evening. I'll email it to rosa@villanuevabookkeeping.com tomorrow once it's confirmed. Does that work for your insurer?", None),
    (C, "Yes, they said within the week is fine. Will I get a credit too?", 6),
    (H, "Yes. You'll get the outage credit, one day of service for each 24 hours of outage, after it's restored. I'll note the letter on your account so anyone here can see it's promised.", None),
    (C, "Okay, thank you.", 6),
    (H, "Thanks for your patience, Rosa. You'll have the letter tomorrow.", None)]),
]

actions = [
act("a201", "D2 09:00", "read", "ch_noc1", "Read the INC-26-1103 opening notice in #noc-status.", "Start of shift on the outage day."),
act("a202", "D2 09:04", "read", "sheet_affected", "Opened the affected-area sheet for OLT KZR-02.", "Playbook step 1."),
act("a203", "D2 09:23", "update_ticket", "ph_pop4", """Case note NB-40342281: INC-26-1103. Caller Jordan Mehta, verified PIN, F-09, ONT offline since 06:42. Upset (22 min hold). No ETR given (none posted at the time). Asked for free month; declined, explained outage credit policy (1 day per started 24h, after restoration). Added to restoration callback list at 503-555-0151. Offered library Wi-Fi.""", "After-call work."),
act("a204", "D2 09:40", "reply", "tk_lionel", """Hi Lionel,

I'm sorry. Your area of north Keizer has been out since 6:42 this morning because a contractor cut one of our main fiber cables (incident INC-26-1103). It affects internet and Home Phone. Repair crews are working on it now; our network team hasn't posted a time estimate yet, and I'll update you when they do.

About the days you're paying for: when an outage lasts 4 hours or more, you get an outage credit of one day of your monthly service for every 24 hours (or part of it) that you're down. It's applied after service is restored, and I'll confirm the amount for you then.

Marisol
Northbeam Fiber Customer Care""", "Outage macro, personalized. She can't give the amount until restoration."),
act("a205", "D2 09:48", "reply", "tk_scott", """Hi Scott, yes: there's a confirmed outage in north Keizer since 6:42 this morning (incident INC-26-1103) after a contractor cut a main fiber cable, and your address is in the affected area. The blinking red light is expected until it's repaired; there's nothing you need to do at your end. Crews are on site. We'll post updates, and you can request a callback at restoration by calling 1-800-555-0140 and choosing option 3. You'll get an outage credit after restoration.

Marisol, Northbeam Fiber""", "Outage macro, address checked."),
act("a206", "D2 10:02", "reply", "tk_maya", """Hi Maya,

Thanks for reaching out, and sorry for the trouble. There is a confirmed outage in our network in the Keizer area since early this morning (incident INC-26-1103) after a contractor cut a fiber cable. Repair crews are working on it now; we don't have a time estimate yet. You'll receive an outage credit after service is restored.

Marisol
Northbeam Fiber Customer Care""", "MISTAKE under volume: Maya is in Monmouth (OLT MNM-01), not in the affected area, and her ONT shows a power-loss alarm at 07:58. She should have been troubleshot (ONT power) or escalated to Tier 2 Technical.", ),
act("a207", "D2 10:36", "read", "ch_derek_reply", "Read Derek's answer to Omar about free-month credits.", "Context."),
act("a208", "D2 12:04", "update_ticket", "ph_pop5", """Case note NB-40100457: INC-26-1103. Caller Edith Caldwell (81), verified by OTP to mobile of record 0164. Home Phone and internet down (F-11). Advised Home Phone and 911 from it do not work during outage; use her cell for 911; suggested she call her medical alert company about cellular backup. Tagged VULNERABLE. Added to restoration callback list, first priority, mobile 503-555-0164. Gave ETR "around 6 pm" as NOC's 10:15 estimate.""", "After-call work; playbook step 5."),
act("a209", "D2 12:40", "read", "em_kb_v7", "Read Jess's email and the v7 cancellation card (effective Thursday).", "Policy change announced."),
act("a210", "D2 13:12", "forward", "em_phish", """Reported with the Report Phish button: "Zendesk backup instance" email from it-servicedesk@northbeam-itsupport.com, link to zendesk-northbeam-backup.com. Not clicked, no credentials entered.""", "Correct handling of phishing.", to=["c_itsec"]),
act("a211", "D2 14:26", "reply", "tk_megan", """Hi Megan, our network team's latest estimate (posted 10:15 this morning) is about 6:00 pm today for your part of Keizer. It's an estimate and could change, so if you need a sure thing this afternoon the library is the safer bet. You'll get an outage credit after restoration, and you can ask for a callback when it's back through 1-800-555-0140, option 3.

Marisol, Northbeam Fiber""", "ETR given as NOC's posted estimate with its time stamp."),
act("a212", "D2 15:33", "update_ticket", "ph_pop6", """Case note NB-40333620: INC-26-1103. Caller Rosa Villanueva, verified PIN, F-03. Home business (bookkeeping); needs written outage confirmation for business interruption insurance. Promised Outage Confirmation Letter by email to rosa@villanuevabookkeeping.com on Wed 11/4 after restoration time is confirmed. Explained outage credit policy.""", "After-call work; the letter is promised for tomorrow."),
act("a213", "D2 15:56", "reply", "em_derek_ot", """Hi Derek, put me down for 7:00 tomorrow. Thanks!
Marisol""", "Her own choice to take OT."),
act("a214", "D2 16:50", "reply", "tk_dale", """Hi Dale,

I'm sorry, the estimate has changed. Our network team updated it at 4:30 pm: service for your part of Keizer is now expected around 9:30 tonight, and that is still an estimate. Until it's back, your home phone can't make calls or send alerts, including 911.

Given your wife's oxygen concentrator alerts go through the home phone, please don't count on it tonight. If you can, staying at her sister's, or calling the concentrator's supplier about a cellular alert option, would be the safer choice. Keep a charged cell phone with you for 911.

I've tagged your account so we call you as soon as service is restored. You'll also receive an outage credit afterwards.

Marisol
Northbeam Fiber Customer Care""", "Gives the revised 16:30 ETR, not the stale 18:00; safety first; tags VULNERABLE."),
]
