# World, contacts and Monday-morning documents for the 43-4051.00 episode.
ME = "c_marisol"

contacts = [
    # self and internal
    dict(id=ME, name="Marisol Ortega", role="Customer Care Representative II, Tier 1 Team 4", relation="self",
         channels=["email", "chat", "phone", "tickets"], notes="marisol.ortega@northbeamfiber.com; Genesys agent 4471; 3 years at Northbeam"),
    dict(id="c_derek", name="Derek Hamm", role="Team Lead, Tier 1 Team 4", relation="manager", channels=["email", "chat"],
         notes="derek.hamm@northbeamfiber.com; approves schedule swaps, handles supervisor calls"),
    dict(id="c_priya", name="Priya Raman", role="Contact Center Operations Manager", relation="skip-level manager",
         channels=["email"], notes="priya.raman@northbeamfiber.com"),
    dict(id="c_lena", name="Lena Kowalczyk", role="Tier 2 Billing Escalations Specialist", relation="internal: Tier 2 Billing",
         channels=["email", "chat", "tickets"], notes="lena.kowalczyk@northbeamfiber.com; Zendesk group T2-Billing; approves payment refunds up to $150 and equipment-fee reversals"),
    dict(id="c_jamal", name="Jamal Whitfield", role="Tier 2 Technical Support", relation="internal: Tier 2 Technical",
         channels=["email", "chat", "tickets"], notes="jamal.whitfield@northbeamfiber.com; Zendesk group T2-Tech"),
    dict(id="c_kevin", name="Kevin Tran", role="NOC Duty Manager", relation="internal: Network Operations Center",
         channels=["chat"], notes="posts incident updates in #noc-status; does not take customer questions"),
    dict(id="c_shauna", name="Shauna Bell", role="Loyalty Specialist", relation="internal: Loyalty (retention)",
         channels=["chat", "phone"], notes="live transfers via Genesys queue LOYALTY"),
    dict(id="c_ray", name="Ray Delgado", role="Account Security Analyst", relation="internal: Fraud & Account Security",
         channels=["email", "tickets"], notes="account.security@northbeamfiber.com; referrals answered within 4 business hours"),
    dict(id="c_tomas", name="Tomas Reyes", role="Quality Analyst", relation="internal: QA", channels=["email"],
         notes="tomas.reyes@northbeamfiber.com; scores 4 calls per rep per month"),
    dict(id="c_analucia", name="Ana Lucia Pereira", role="Workforce Management Analyst", relation="internal: WFM",
         channels=["email"], notes="ana.pereira@northbeamfiber.com; schedules, OT, holiday bids"),
    dict(id="c_brent", name="Brent Olsen", role="Field Operations Scheduler", relation="internal: Field Ops dispatch",
         channels=["email", "tickets"], notes="dispatch@northbeamfiber.com"),
    dict(id="c_kayla", name="Kayla Nguyen", role="Customer Care Representative II", relation="peer, Team 4",
         channels=["chat"], notes=""),
    dict(id="c_omar", name="Omar Haddad", role="Customer Care Representative I", relation="peer, Team 4 (6 weeks in)",
         channels=["chat"], notes="new hire; asks the team a lot"),
    dict(id="c_jess", name="Jess Moreland", role="Knowledge & Training Manager", relation="internal: Knowledge base",
         channels=["email"], notes="jess.moreland@northbeamfiber.com; owns the KB and macros"),
    dict(id="c_brady", name="Brady Coates", role="Residential Sales Manager", relation="internal: Sales (not in the rep's chain)",
         channels=["email"], notes="brady.coates@northbeamfiber.com"),
    dict(id="c_hannah", name="Hannah Stiles", role="Compliance Manager, Legal & Regulatory", relation="internal: Compliance",
         channels=["email"], notes="hannah.stiles@northbeamfiber.com"),
    dict(id="c_wendy", name="Wendy Marsh", role="Billing Operations Supervisor", relation="internal: Billing Ops",
         channels=["email"], notes="wendy.marsh@northbeamfiber.com"),
    dict(id="c_marisol_ortiz", name="Marisol Ortiz", role="Billing Operations Analyst", relation="internal: Billing Ops (different person, similar name)",
         channels=["email"], notes="marisol.ortiz@northbeamfiber.com"),
    dict(id="c_itsec", name="IT Security (phishing reports)", role="Security mailbox", relation="internal",
         channels=["email"], notes="phishing@northbeamfiber.com; the Report Phish button forwards here"),
    dict(id="c_fake_it", name="\"Northbeam IT Service Desk\" (spoofed)", role="external sender", relation="unknown external",
         channels=["email"], notes="it-servicedesk@northbeam-itsupport.com (not a Northbeam domain)"),
    # customers
    dict(id="c_hector", name="Hector Alvarado", role="customer NB-40318827", relation="customer", channels=["tickets", "email"], notes="hector.alvarado71@gmail.com"),
    dict(id="c_curtis", name="Curtis Wainwright", role="former customer NB-40122953", relation="customer", channels=["tickets", "email", "phone"], notes="cwainwright.or@gmail.com"),
    dict(id="c_naomi", name="Naomi Fischer", role="customer NB-40377412", relation="customer", channels=["tickets"], notes="naomi.fischer@pm.me"),
    dict(id="c_ruth", name="Ruth Engel", role="customer NB-40255190", relation="customer", channels=["tickets", "phone"], notes="mobile 503-555-0115"),
    dict(id="c_gary", name="Gary Lindqvist", role="customer NB-40211736", relation="customer", channels=["phone"], notes=""),
    dict(id="c_tanya", name="Tanya Brooks", role="customer NB-40299018", relation="customer", channels=["phone"], notes=""),
    dict(id="c_walter", name="Walter Kim", role="customer NB-40188364", relation="customer", channels=["phone"], notes=""),
    dict(id="c_amara", name="Amara Okafor", role="customer NB-40350961", relation="customer", channels=["tickets"], notes=""),
    dict(id="c_tobias", name="Tobias Reed", role="customer NB-40402335", relation="customer", channels=["tickets"], notes=""),
    dict(id="c_weilin", name="Wei Lin", role="customer NB-40387720", relation="customer", channels=["tickets"], notes="chat"),
    dict(id="c_jordan", name="Jordan Mehta", role="customer NB-40342281", relation="customer", channels=["phone"], notes="Keizer, segment F-09"),
    dict(id="c_edith", name="Edith Caldwell", role="customer NB-40100457", relation="customer", channels=["phone"], notes="Keizer, segment F-11; mobile 503-555-0164; VULNERABLE tag"),
    dict(id="c_rosa", name="Rosa Villanueva", role="customer NB-40333620", relation="customer", channels=["phone", "tickets"], notes="Keizer, segment F-03; runs Villanueva Bookkeeping from home"),
    dict(id="c_lionel", name="Lionel Baptiste", role="customer NB-40290815", relation="customer", channels=["tickets"], notes="Keizer, segment F-14"),
    dict(id="c_maya", name="Maya Sorensen", role="customer NB-40366104", relation="customer", channels=["tickets"], notes="Monmouth (node MNM-01)"),
    dict(id="c_scott", name="Scott Hargrove", role="customer NB-40347715", relation="customer", channels=["tickets"], notes="Keizer, F-06"),
    dict(id="c_megan", name="Megan Fry", role="customer NB-40321184", relation="customer", channels=["tickets"], notes="Keizer, F-02"),
    dict(id="c_dale", name="Dale Whitcomb", role="customer NB-40336052", relation="customer", channels=["tickets"], notes="Keizer, F-08"),
    dict(id="c_denise", name="Denise Pruitt", role="customer NB-40157739 (account holder)", relation="customer", channels=["email", "phone"], notes="email of record dpruitt.salem@gmail.com; mobile of record 503-555-0181; no authorized users"),
    dict(id="c_wade", name="\"Wade Pruitt\" (caller, unverified)", role="caller claiming to be Denise Pruitt's husband", relation="unverified caller", channels=["phone"], notes="not an authorized user on NB-40157739"),
    dict(id="c_imposter", name="\"Denise Pruitt\" <denise.pruitt.home@outlook.com>", role="sender claiming to be the account holder", relation="unverified sender", channels=["email"], notes="address not on the account"),
    dict(id="c_frank", name="Frank Osei", role="customer NB-40271196", relation="customer", channels=["phone"], notes=""),
    dict(id="c_kenji", name="Kenji Watanabe", role="customer NB-40310088", relation="customer", channels=["tickets"], notes="chat"),
    dict(id="c_arturo", name="Arturo Saldana", role="customer NB-40319946", relation="customer", channels=["tickets"], notes="Keizer, F-12"),
    dict(id="c_theresa", name="Theresa Gould", role="customer NB-40344128", relation="customer", channels=["tickets"], notes="Keizer, F-01"),
    dict(id="c_lucia", name="Lucia Herrera", role="customer NB-40281143", relation="customer", channels=["phone"], notes="Keizer, segment F-14"),
    dict(id="c_beverly", name="Beverly Strand", role="customer NB-40199270", relation="customer", channels=["phone"], notes="Keizer, F-05; phone of record 503-555-0127"),
    dict(id="c_jim", name="Jim Harlan", role="customer NB-40411529", relation="customer", channels=["phone"], notes="Mount Shasta, California"),
    dict(id="c_irene", name="Irene Matsuda", role="customer NB-40244867", relation="customer", channels=["tickets", "email"], notes="email of record irene.matsuda@comcast.net"),
    dict(id="c_kimpham", name="Kim Pham", role="customer NB-40352290", relation="customer", channels=["tickets"], notes="Keizer, F-10"),
    dict(id="c_marcus", name="Marcus Odom", role="customer NB-40398877", relation="customer", channels=["phone"], notes=""),
    dict(id="c_paul", name="Paul Nakamura", role="customer NB-40305572", relation="customer", channels=["phone"], notes="Keizer, segment F-14"),
    dict(id="c_diane", name="Diane Kessler", role="authorized user on NB-40228410 (holder Harold Kessler)", relation="customer", channels=["phone"], notes=""),
    dict(id="c_dolores", name="Dolores Ruiz", role="customer NB-40263391", relation="customer", channels=["phone"], notes=""),
    dict(id="c_eleanor", name="Eleanor Pike", role="customer NB-40116673", relation="customer", channels=["tickets"], notes="age 72"),
    dict(id="c_ryan", name="Ryan Castillo", role="customer NB-40409118", relation="customer", channels=["tickets"], notes=""),
]

world = dict(
    worker=dict(name="Marisol Ortega", title="Customer Care Representative II (Tier 1, blended phone and digital)",
                employer="Northbeam Fiber, Inc. (fictional)", manager="c_derek", team="Tier 1 Team 4 (12 reps), Salem contact center",
                schedule="Mon-Fri 08:30-17:00 Pacific, 30-minute lunch at 12:00; phone queue all day except two digital blocks (10:00-11:00 and 14:00-15:00) for the email/chat ticket queue",
                targets="AHT 6:30, QA 85+, FCR 72%+, schedule adherence 92%+"),
    organization=dict(
        name="Northbeam Fiber, Inc.",
        what="Regional fiber-to-the-home internet provider with an interconnected-VoIP Home Phone add-on; about 210,000 residential internet and 38,000 Home Phone customers in the Willamette Valley (Salem, Keizer, Albany, Corvallis, Monmouth, Woodburn), southwest Washington and Siskiyou County, California.",
        size="About 1,900 employees; the Salem contact center has about 160 reps in Tier 1 (phone and digital), Tier 2 Billing, Tier 2 Technical, Loyalty and Account Security.",
        norms=["Verify with account PIN or a one-time passcode before discussing any account (CPNI, 47 CFR 64.2010).",
               "No card numbers by voice, chat or email: Secure Pay IVR or the payment link (PCI DSS).",
               "Tier 1 credit authority $40 per account per rolling 30 days; refunds of payments and equipment-fee reversals go to Tier 2 Billing.",
               "Never give an ETR that NOC has not posted; outage credits per formula only.",
               "Every contact gets a case note; repeat contacts tagged with the incident number.",
               "Service levels: phone 80% answered in 30 s; email/web tickets first response within 24 business hours; chat 80% in 60 s.",
               "Time zone Pacific; daylight saving time ended Sunday 1 November 2026, so times this week are PST."]),
    contacts=contacts,
    systems=[
        dict(id="sys_genesys", name="Genesys Cloud CX", what="ACD/softphone: inbound queues, screen pop, transfers (Secure Pay IVR, LOYALTY, T2-Tech), recording with automatic pause during Secure Pay, outbound callbacks"),
        dict(id="sys_beam360", name="Beam360", what="Northbeam's account and billing console: plans, equipment serials, payments, credits (enforces the $40 Tier 1 limit), ONT status, authorized users, PIN/OTP verification log, call detail (Home Phone) behind PIN"),
        dict(id="sys_zendesk", name="Zendesk Support", what="email, web-form and chat ticket queue; groups T2-Billing, T2-Tech, Account Security; Redact tool for card data; macros"),
        dict(id="sys_slack", name="Slack", what="#team4, #noc-status (read-only for reps), DMs"),
        dict(id="sys_guru", name="Guru knowledge base", what="policies and scripts; the documents in this episode are its cards"),
    ],
)

D0 = []
def doc(id, kind, subject, body, frm="c_jess", meta=None, at="D0", thread=None):
    D0.append(dict(id=id, channel="docs", kind=kind, at=at, thread=thread or f"t_{id}", **{"from": frm}, to=[ME], cc=[],
                   subject=subject, body=body, attachments=[], meta=meta or {}))

doc("doc_authority", "doc", "Tier 1 Authority Matrix: Credits, Refunds and Adjustments (rev. 2026-09-14)", """Northbeam Fiber - Customer Care
Tier 1 Authority Matrix: Credits, Refunds and Adjustments
Revision 2026-09-14. Owner: Billing Operations (W. Marsh)

1. Discretionary service credits (goodwill, missed appointment, repeat contact)
   - Tier 1 may apply up to $40.00 per account in any rolling 30 days, total across all reps. Beam360 blocks anything above the remaining limit.
   - Reason code and a case note are required for every credit.
2. Outage credits (confirmed NOC incident only)
   - Eligible when a NOC incident interrupted service for 4 or more consecutive hours.
   - Amount: one day per started 24-hour period of interruption. One day = monthly recurring service charges / 30 (excludes the Regulatory Recovery & 911 Fee, taxes, one-time charges and equipment fees). Round to the cent.
   - Tier 1 may apply outage credits tagged with the incident number after service is restored. They do not count toward the $40 limit.
   - For large incidents Billing Operations may replace manual outage credits with an automatic batch. Follow the incident notice when there is one.
3. Late fee ($10.00): Tier 1 may waive one late fee per account per 12 months.
4. Disputed usage charges (international calls, directory assistance): Tier 1 may give a one-time courtesy credit up to $40.00 per account per 12 months. Counts toward the $40 limit in item 1.
5. Refunds of payments to a card or bank account: Tier 1 may NOT issue refunds. Escalate to Tier 2 Billing (Zendesk group T2-Billing). Tier 2 approves up to $150.00; above $150.00 needs the Billing Operations Supervisor.
6. Equipment non-return fees ($150.00 Wi-Fi gateway NB-GX4, $75.00 mesh extender): Tier 1 may not reverse. Escalate to Tier 2 Billing with the return tracking number and the serial on the account.
7. Promotions: Tier 1 may not extend, re-apply or create promotions. Retention offers belong to Loyalty (see Cancellations & Save Offers).
8. Payment arrangements: one per account per 12 months; total balance up to $250.00; at most 2 installments; final installment within 30 days of the contact. When an arrangement is set, the most recent late fee may be waived (this uses the item 3 waiver).
9. Never promise an amount or outcome you cannot apply yourself. Tell the customer what you are requesting, from whom, and when they will hear back.""", frm="c_wendy")

doc("doc_verify", "doc", "Account Verification Standard (rev. 2026-08-03)", """Account Verification Standard - all channels
Revision 2026-08-03. Owner: Fraud & Account Security with Compliance

Why: Home Phone is an interconnected VoIP service, so the FCC's CPNI rules (47 CFR 64.2001-64.2011) apply to its account and call information. Northbeam applies the same standard to internet-only accounts.

1. Who we help: the account holder and the authorized users listed in Beam360 > Account > Authorized Users. Nobody else, including spouses, family or "the person who pays" if they are not listed.
2. Verify with one of:
   a. the account PIN (4-8 digits, set by the customer);
   b. a one-time passcode (OTP) texted to the mobile number of record or emailed to the email of record. Never send an OTP to a number or address the caller gives you.
   Not acceptable alone: name, service address, date of birth, last 4 of SSN, mother's maiden name, amount of the last bill. These are "readily available biographical or account information" under 47 CFR 64.2010.
3. Before verification you may: give general information (plans, prices, outage status by area), transfer to the Secure Pay IVR to take a payment, and take a message. You may NOT confirm that the person has an account, or give the balance, payments, plan, contact details or call records, or make any change.
4. Call detail (numbers called, times, durations) on a customer-initiated call: only after PIN. Otherwise offer to send it to the postal or email address of record (on file 30+ days).
5. Changes to email, phone of record, PIN or authorized users: only after verification. Beam360 sends the change notice to the old contact automatically. Requests by email or chat from an address not on the account: make no change, reply only with how to verify by phone, and open an Account Security referral.
6. Suspected pretexting or account takeover (someone posing as the customer or family, pushing for call records or contact changes, failing verification): write a factual case note and send an Account Security referral the same day (Zendesk group Account Security or account.security@northbeamfiber.com, Ray Delgado). Obtaining phone records by false pretenses is a federal crime (18 U.S.C. 1039). Law-enforcement requests go to Legal.
7. An email from the email of record is not verification for changes, but you may answer questions about that account, including call detail, by replying to that address.""", frm="c_ray")

doc("doc_pci", "doc", "Card Payments and Card Data (rev. 2026-05-20)", """Card Payments and Card Data - PCI DSS rules for every channel
Revision 2026-05-20. Owner: Compliance (H. Stiles)

1. Phone: never take a card number by voice. Use Transfer > Secure Pay IVR in Genesys. The customer keys the card on the phone keypad (tones are masked); you stay on the line and see only approved/declined and the last four digits. If a customer starts reading digits, stop them politely and transfer.
2. Never write, type or repeat a full card number or security code: not in Beam360 notes, Zendesk, Slack, email or on paper. Refer to a card by brand and last four only.
3. Chat and email: if a customer sends card data, use Zendesk Redact on that message right away, do not quote it in your reply, and send the secure payment link pay.northbeamfiber.com or the IVR, 1-800-555-0140 option 2.
4. Recordings: Genesys pauses recording automatically during the Secure Pay transfer. If card digits were spoken while recording, tag the interaction PCI-SCRUB so QA deletes that segment.
5. Saving a card for autopay: only by the customer, in the portal or the IVR.
Reference: PCI SSC Information Supplement, Protecting Telephone-Based Payment Card Data, v3.0 (November 2018): sensitive authentication data must not be stored after authorization, even if encrypted.""", frm="c_hannah")

doc("doc_cancel_v6", "doc", "Cancellations, Downgrades and Save Offers (rev. 2026-06-01)", """Cancellations, Downgrades and Save Offers - script and rules
Revision 2026-06-01 (v6). Owner: Knowledge & Training

1. Any Tier 1 rep may process a cancellation or downgrade.
2. Ask the reason once. Moving outside the service area: no offer; process.
3. Otherwise you may present ONE save offer from the Offer Library (6 months $10 off; or Wi-Fi Plus free for 3 months), or transfer to Loyalty if the customer asks for something else. If the customer declines, process.
4. California accounts (Siskiyou County): before any offer, tell the customer they can cancel at any time (Cal. Bus. & Prof. Code 17602(e)).
5. Effective date: the date the customer asks for (today or later). Unused days are credited on the final bill at the net monthly service charge / 30 per day.
6. Equipment: the Wi-Fi gateway (and any mesh extender) must be returned within 30 days of disconnect with the prepaid UPS label emailed at disconnect, or the non-return fee applies. The ONT stays at the home.
7. Voicemail and email cancellation requests: California - process or call back within one business day; other states - within two business days.
8. Case note: CANCEL plus reason code.""")

doc("doc_outage_playbook", "doc", "Outage Contact Playbook (rev. 2026-03-09)", """Outage Contact Playbook
Revision 2026-03-09. Owner: Contact Center Operations (P. Raman)

1. Check the customer's service address and segment against the incident's affected-area sheet and #noc-status. Only customers inside the affected area get the outage macro. Outside it, troubleshoot normally (ONT lights, gateway status in Beam360) and escalate to Tier 2 Technical if the ONT is offline.
2. ETR: give it exactly as NOC last posted it, as an estimate, with the time it was posted. If NOC has not posted one, say crews are working and there is no estimate yet. Never give a time NOC has not posted.
3. Credits: customers out 4+ hours get an outage credit of one day of service per started 24 hours of interruption, after restoration (Authority Matrix item 2). Do not quote other amounts or free months.
4. Callbacks: customers can ask for a callback at restoration through IVR option 3. Lists are assigned the next morning. Call only the number the customer gave, between 8:00 and 21:00 their local time, and respect internal do-not-call flags (email instead).
5. Home Phone during an outage: Home Phone, including 911 from it, does not work while the internet service is down. Tell customers to use a mobile phone for 911. Customers with medical alert devices or other safety needs: tag VULNERABLE and put them first on callback lists.
6. Customers who need documentation (insurance, employer): after restoration, send the Outage Confirmation Letter (template) with the incident number and the interruption times for their segment.
7. Tag every related case INC-<number> for reporting.""", frm="c_priya")

doc("doc_rates", "doc", "Residential Rate Card (effective 2026-07-01)", """Northbeam Fiber - Residential Rate Card, effective 2026-07-01 (all states)

Internet (price per month; symmetrical speeds; Wi-Fi gateway NB-GX4 included)
- Fiber 300: $55.00
- Fiber 1 Gig: $75.00
- Fiber 2 Gig: $95.00 (needs the NB-GX7 Wi-Fi 7 gateway; swap is free)
- Autopay & paperless discount: -$5.00 per month (internet plans only)

Add-ons
- Wi-Fi Plus (one mesh extender + app management): $10.00 per month; ships in 2-3 business days, self-install
- Home Phone (interconnected VoIP; unlimited US/Canada; voicemail; international per-minute): $20.00 per month
- Regulatory Recovery & 911 Fee (Home Phone lines only): $2.49 per month
- International & premium-number block (Home Phone): free, on request
- International rates per minute (selected): Mexico $0.05; Philippines $0.19; Jamaica $0.52; Grenada $0.58; Dominican Republic $0.21

Fees
- Late fee: $10.00 when a balance is unpaid 15 days after the due date
- Equipment non-return: NB-GX4 gateway $150.00; mesh extender $75.00
- Paper bill: $1.99 per month (waived on request for customers 65 and older)
- Installation and moves within the service area: $0

Billing: statements on the 1st, due the 18th; services billed a month in advance.""", frm="c_wendy")

doc("doc_escalation", "doc", "Escalation Paths and Response Times (rev. 2026-04-15)", """Escalation Paths and Response Times
Revision 2026-04-15

- Tier 2 Billing (Zendesk T2-Billing; Lena Kowalczyk and team): payment refunds, equipment-fee disputes, credits above Tier 1 authority. Response 2 business days. Include: account number, amounts, dates, payment confirmation numbers, tracking numbers, what the customer wants.
- Tier 2 Technical (Zendesk T2-Tech; Jamal Whitfield and team): ONT offline outside a known incident, repeated drops, speed below plan after basic steps. Same business day.
- Field dispatch (Dispatch Request form to dispatch@northbeamfiber.com): customer premises issues that need a technician (red LOS light on the ONT, damaged drop). Include ONT serial, light status, access notes, best phone, first available slot offered.
- Loyalty (Genesys queue LOYALTY): live transfer when a customer wants a retention offer that is not in the Offer Library.
- Account Security (Ray Delgado): suspected pretexting, account takeover, fraud. Within 4 business hours.
- Supervisor (team lead): customer asks for a supervisor, or anything not covered here.
- Contact-center SLAs: phone 80% answered in 30 seconds; email/web tickets first response within 24 business hours; chat 80% answered in 60 seconds.""", frm="c_priya")

doc("doc_letter_template", "doc", "Outage Confirmation Letter - template", """Northbeam Fiber, Inc. | Customer Care | PO Box 7710, Salem OR 97303 | 1-800-555-0140

Date: <date>
To: <customer name>, <service address>
Account: <account number>

Re: Confirmation of service interruption, incident <incident number>

This letter confirms that Northbeam Fiber internet service (and Home Phone service, if subscribed) at the address above was interrupted by a network incident, <incident number>, from approximately <start time and date> until <restoration time and date> (<duration>). The cause was <one-line cause from the NOC reason-for-outage notice>.

An outage credit under Northbeam's service interruption policy will appear on the customer's account as described in the incident notice.

If you need anything further, contact Northbeam Customer Care at 1-800-555-0140.

<rep name>, Customer Care, Northbeam Fiber""", frm="c_jess")

doc("doc_move_form", "doc", "Service Transfer (Move) Order - form", """Service Transfer (Move) Order
Account: ____  Customer: ____  Verified by: PIN / OTP / email of record
Current service address: ____
New service address: ____  Serviceability result: ____
Plan at new address: ____  Monthly price: ____
Install at new address: date ____ window ____  (install needed if no ONT present)
Disconnect at current address: date ____
Equipment: customer brings gateway (serial ____); ONT stays at old address
Contact phone for technician: ____
Notes: ____""", frm="c_jess")

doc("doc_dispatch_form", "doc", "Field Dispatch Request - form", """Field Dispatch Request (send to dispatch@northbeamfiber.com)
Account: ____  Customer: ____  Best phone: ____
Service address and segment: ____
ONT serial: ____  ONT lights (PON / LOS / power): ____  Offline since: ____
Steps taken: ____
Related incident (if any): ____
Access notes (gate, pets, where the ONT is): ____
Slot offered and accepted: ____
Priority flags (VULNERABLE, repeat): ____""", frm="c_brent")

doc("sheet_returns", "sheet", "Returns Center - unmatched receipts, October 2026 (Tualatin)", """Returns Center (Tualatin, OR) - equipment received with no account match, October 2026
Shared read-only with Customer Care for lookups. Questions: returns@northbeamfiber.com (Luis Ferreira)

received   | carrier tracking         | model   | serial scanned | account match | note
2026-10-05 | 1Z8V41E70390988127       | NB-GX4  | NB-GX4-60318   | NO MATCH      | label torn
2026-10-08 | 9405511206213648820197   | MESH-2  | NBM2-11873     | NO MATCH      | USPS, no RMA
2026-10-12 | 1Z8V41E70391140072       | NB-GX4  | NB-GX4-71946   | NO MATCH      |
2026-10-15 | 1Z8V41E70391245563       | NB-GX4  | NB-GX4-77102   | NO MATCH      | hand-keyed, scanner down
2026-10-19 | 1Z8V41E70391302218       | NB-GX7  | NB-GX7-02215   | NO MATCH      |
2026-10-22 | 1Z8V41E70391377940       | MESH-2  | NBM2-13060     | NO MATCH      | hand-keyed, scanner down
2026-10-27 | 1Z8V41E70391468805       | NB-GX4  | NB-GX4-80451   | NO MATCH      |
2026-10-29 | 1Z8V41E70391511396       | NB-GX4  | NB-GX4-81277   | NO MATCH      |""", frm="c_wendy")

doc("sheet_scorecard", "sheet", "Team 4 scorecard - October 2026", """Team 4 scorecard, October 2026 (Genesys + QA + post-contact survey)
rep              | contacts | AHT  | FCR | QA avg | CSAT (1-5) | adherence
Marisol Ortega   | 1,188    | 6:41 | 74% | 88.5   | 4.4        | 93%
Kayla Nguyen     | 1,241    | 6:12 | 71% | 90.0   | 4.3        | 95%
Omar Haddad      |   702    | 8:55 | 58% | 79.0   | 4.0        | 90%
Team (12 reps)   | 13,406   | 6:48 | 70% | 86.1   | 4.3        | 93%
Targets          |          | 6:30 | 72% | 85     | 4.2        | 92%
Note: Marisol's October QA includes the 10/27 evaluation (see email of 11/2).""", frm="c_derek")

D0.append(dict(id="tk_ruth", channel="tickets", kind="ticket", at="D0", thread="t_ruth", **{"from": "c_ruth"}, to=[ME], cc=[],
    subject="#88213 Slow speeds on 1 Gig plan (status: Pending)", body="""Ticket #88213, opened 2026-10-29 by Marisol Ortega (phone). Status: Pending. Group: Tier 1. Next action owner: Marisol Ortega.

Customer: Ruth Engel, NB-40255190, 1622 Mildred Ln SE, Salem. Plan Fiber 1 Gig ($75.00, autopay). Verified by PIN 10/29.
Issue: customer reports 70-90 Mbps on speed tests from her home office laptop over Wi-Fi; wired test not possible (no ethernet port on laptop). Beam360 showed ONT light level -27.9 dBm (marginal).
Actions 10/29: power-cycled ONT and gateway; no change. Booked technician Sat 10/31 8-12 (WO-552190).
Next step: rep to call customer Mon 11/2 after the visit to confirm the problem is fixed, then close or escalate to T2-Tech.
Best phone: mobile 503-555-0115 (customer asked for calls after 9 am).""", attachments=[], meta=dict(account="NB-40255190", via="phone")))

D0.append(dict(id="cal_week", channel="calendar", kind="event", at="D0", thread="t_cal", **{"from": "c_derek"}, to=[ME], cc=[],
    subject="Recurring: Team 4 daily huddle (08:40-08:55, Mon-Fri)", body="Daily 15-minute stand-up at pod 4: queue forecast, KB changes, shout-outs. Derek posts notes in #team4 after.", attachments=[], meta=dict(start="D1 08:40", end="D1 08:55", recurrence="weekdays")))
D0.append(dict(id="cal_1on1", channel="calendar", kind="event", at="D0", thread="t_cal_1on1", **{"from": "c_derek"}, to=[ME], cc=[],
    subject="1:1 Marisol / Derek (Thu 11/5 13:00-13:30)", body="Monthly 1:1. Agenda: October scorecard, QA, development plan (Tier 2 Billing shadowing), anything you want to raise.", attachments=[], meta=dict(start="D4 13:00", end="D4 13:30")))
D0.append(dict(id="cal_qa_calib", channel="calendar", kind="event", at="D0", thread="t_cal_qa", **{"from": "c_tomas"}, to=[ME], cc=["c_derek"],
    subject="QA calibration, Team 4 (Wed 11/4 16:00-16:45)", body="Monthly calibration: we score two recorded calls together against the QA form and compare. Your phone status is set to Meeting automatically.", attachments=[], meta=dict(start="D3 16:00", end="D3 16:45")))
