# Part 3: Monday 2026-11-02 arrivals
PREBILL_ROWS = [
 ("10/01/26","RK",0.3,195,"Draft letter to N. Corbin enclosing supplemental Rule 26(a)(1) disclosures."),
 ("10/02/26","RK",1.2,195,"Review Plaintiff's First Set of Interrogatories and First Requests for Production; prepare chart of requests and likely custodians for P. Raman."),
 ("10/06/26","RK",0.4,195,"Calendar discovery response deadlines; update case calendar."),
 ("10/08/26","RK",0.2,195,"Telephone conference with R. Szymanski re location of 2024 field service records."),
 ("10/09/26","RK",2.6,195,"Review client service tickets for responsiveness; draft summary of 2025 service history; conference with P. Raman re same."),
 ("10/13/26","RK",0.8,195,"Scan and upload client hard-copy warranty files to Relativity."),
 ("10/14/26","RK",1.5,195,"Draft answers to Interrogatory Nos. 1-9 for attorney review."),
 ("10/15/26","GE",0.5,95,"Schedule conference call with client; circulate dial-in."),
 ("10/16/26","RK",1.1,195,"Prepare chronology of KX-40 shipments and warranty claims from client sales data."),
 ("10/20/26","RK",0.3,195,"Bates-stamp and QC supplemental Volume 1 pages."),
 ("10/21/26","RK",0.7,195,"Cite-check P. Raman letter brief to Magistrate Judge Talbot re ESI search terms."),
 ("10/22/26","RK",0.5,195,"Conference with T. Nguyen re search term hit report; revise hit report summary for P. Raman."),
 ("10/26/26","RK",0.2,195,"File correspondence and e-mails to iManage workspace."),
 ("10/27/26","RK",1.8,195,"First-level privilege review of R. Szymanski e-mail (Relativity batch 14); code for privilege."),
 ("10/29/26","RK",0.25,195,"Telephone call with S. Feld (Plaintiff's paralegal) re production format for native spreadsheets."),
 ("10/30/26","GE",0.3,95,"Copy and assemble binder of client warranty files for D. Achterberg."),
]
rows=[]; tot_h=0; tot_amt=0
for i,(d,t,h,r,n) in enumerate(PREBILL_ROWS,1):
    amt=round(h*r,2); tot_h+=h; tot_amt+=amt
    rows.append(f"{i:>2} | {d} | {t} | {h:.2f} | ${r} | ${amt:,.2f} | {n}")
PREBILL_TOTAL_H=round(tot_h,2); PREBILL_TOTAL_AMT=round(tot_amt,2)
WRITE_OFF_ROWS=[3,6,8,10,13,16]
WRITE_OFF=round(sum(round(PREBILL_ROWS[i-1][2]*PREBILL_ROWS[i-1][3],2) for i in WRITE_OFF_ROWS),2)
assert WRITE_OFF==407.50, WRITE_OFF
AFTER_H=round(PREBILL_TOTAL_H-2.5,2); AFTER_AMT=round(PREBILL_TOTAL_AMT-WRITE_OFF,2)
AFTER2_H=round(AFTER_H-0.05,2); AFTER2_AMT=round(AFTER_AMT-0.05*195,2)
doc("itm_prebill", "D1 08:00", "Pre-bill 10442-003 Kessling / Prairie Hollow - October 2026 - paralegal and legal assistant entries", 
"Ostrander Hale LLP - PRE-BILL (draft, not an invoice) - Client 10442 Kessling Pump & Controls, Inc. - Matter 003 Prairie Hollow litigation - Period 10/01/2026-10/31/2026\n"
"Section shown: timekeepers RK (R. Kowalczyk, paralegal) and GE (G. Esposito, legal assistant). Attorney time is on pages 1-3 (D. Achterberg 21.4 h; P. Raman 46.9 h).\n\n"
"#  | Date     | Tkpr | Hours | Rate | Amount | Narrative\n" + "\n".join(rows) +
f"\n\nSubtotal RK/GE: {PREBILL_TOTAL_H:.2f} hours, ${PREBILL_TOTAL_AMT:,.2f}\nBilling attorney: D. Achterberg. Edits due to Billing by Wednesday 11/4, 10:00 a.m.", "c_kevin", kind="sheet")

email("itm_priya_week", "D1 08:00", "c_priya", ["c_renee"], "Kessling - this week (responses due Fri 11/6)", f"""
Renee,

Big week on Kessling. Responses to Prairie Hollow's first rogs and RFPs are due Friday 11/6 (served 10/7 by email, so no extra 3 days). What I need:

1. Rog answers and RFP responses: fold in whatever Rick sent and get me clean drafts by Wednesday 5 pm. I'll turn comments Wednesday night.
2. Vol. 2 production: Tom is staging it. Nothing goes out until I've signed off on the privilege QC.
3. Privilege log: under para. 9 of the ESI stip it has to go out WITH the production, so it's due Friday too. Remember the post-complaint carve-out.
4. Verification: Rick has to sign the rog verification himself (1746 declaration). He travels a lot, so get it to him in time.
5. Lindqvist: Daniel wants to depose Dale Lindqvist (PHGC's ops manager) in mid-November. Get dates from Nathan and get the notice out this week; I want the full 14 days' notice so there's no Rule 32(a)(5) argument.

Thanks!
{SIG_PR}
""", thread="t_week")

email("itm_kevin_prebill", "D1 08:00", "c_kevin", ["c_daniel"], "October pre-bills ready for review - 10442-003 Kessling", f"""
Daniel,

Your October pre-bills are posted in Aderant. Kessling (10442-003) is attached as a sheet: paralegal/LA section {PREBILL_TOTAL_H:.2f} hours, ${PREBILL_TOTAL_AMT:,.2f}. Kessling's guidelines are strict on clerical time and block billing, so please have entries reviewed before you release. Edits due Wednesday 11/4 by 10:00 a.m. so the invoice can go out on the 5th.

Thanks,
Kevin Doyle
Billing Coordinator | Ostrander Hale LLP | x0121
""", thread="t_prebill", attachments=["itm_prebill"])

email("itm_docket_report", "D1 08:00", "c_docket", ["c_renee"], "Weekly deadline report - R. Kowalczyk matters - 11/02/2026 to 11/16/2026", """
CompuLaw Vision - Deadline Report for paralegal R. Kowalczyk - generated 11/02/2026 06:00

11/04/2026 Wed  11870-002 Midway/Delacroix   INTERNAL: target to file Motion for Leave to File Third-Party Complaint (M. Bell)
11/06/2026 Fri  10442-003 Kessling/PHGC      Defendant's responses to Plaintiff's First Set of Interrogatories due (served 10/07/2026 by e-mail; FRCP 33(b)(2), 6(a)) - Resp. atty P. Raman
11/06/2026 Fri  10442-003 Kessling/PHGC      Defendant's responses to Plaintiff's First Requests for Production due (served 10/07/2026 by e-mail; FRCP 34(b)(2)(A)) - Resp. atty P. Raman
11/06/2026 Fri  10442-003 Kessling/PHGC      Privilege log due with production (ESI Stip. para. 9(a), Dkt. 29)
11/10/2026 Tue  11870-002 Midway/Delacroix   Plaintiff's answers to Midway's Second Interrogatories due (served 10/13/2026 by e-mail; 28 days, Ill. S. Ct. R. 213(d))
11/16/2026 Mon  10442-003 Kessling/PHGC      Reminder: fact discovery closes 01/29/2027 (Dkt. 44)

Questions: docketing@ostranderhale.com | x0109
""", thread="t_docket")

email("itm_rick_sunday", "D1 08:00", "c_rick", ["c_renee"], "RE: open rog questions (6, 7, 11, 14)", f"""
Renee - sorry this is late, finally got through it Sunday night.

6 - Teardowns: Hui's engineering group tore down the two pumps we pulled on RMA-25-0077 (serials KX40-24-0528 and -0530) on 7/29/25. Both reports say seal faces heat checked and carbon face cracked, consistent with dry running. Reports are TR-25-031 and TR-25-032, Hui has the PDFs and the photos.

7 - Other customers with Type 21 seal failures in IL/IN/IA/WI since 1/2023: Hollins Farms (Iowa, 2 pumps, 2024), Wabash Valley Ag Services (Indiana, 1 pump, 2025), Tri-County Sod (Illinois, 1 pump, 2023). Brett can confirm dates.

11 - Misuse: besides the teardowns, on FS-25-0590 the pump's own controller log showed 41 hours running against a closed valve. And Paul found the flush line closed on FS-25-0412. Prairie Hollow's own guys run the pumps, we don't.

14 - People who talked to Prairie Hollow about the failures: me (calls with Walt Herrmann their GM, Aug 2025 and Sept 2025), Brett Nowak (site visit 6/2025 with Dale Lindqvist), Dennis Okon (emails with Dale Lindqvist June-Aug 2025), and Paul and Andre on site.

Let me know what else.

Rick Szymanski
VP Operations | Kessling Pump & Controls, Inc.
4410 Kishwaukee St. | Rockford, IL 61109
o 815.555.0120 | c 815.555.0127
""", thread="t_rick_rogs")

email("itm_news_d1a", "D1 08:00", "c_vendor", ["c_renee"], "Litigation Daily Briefing - Monday, November 2", """
Today's briefing: Seventh Circuit hears argument on arbitration waiver; Sedona Conference opens comment period on a draft commentary on AI-assisted review; five tips for managing deposition exhibits remotely.
Manage your subscription preferences in your account.
""")
email("itm_it_d1", "D1 08:00", "c_it", ["c_firm"], "Reminder: iManage Work upgrade Saturday 11/7, 6 pm - midnight", """
All,

iManage Work will be unavailable Saturday 11/7 from 6:00 p.m. to midnight for the version upgrade. Save and check in open documents before you leave Friday. Outlook filing will queue and catch up Sunday.

Reminder: if an e-mail looks suspicious, use the Report Phish button in Outlook. Do not forward it to colleagues and do not enter your credentials anywhere.

IT Service Desk | x4357 | servicedesk@ostranderhale.com
""")
email("itm_marcus_headsup", "D1 08:10", "c_marcus", ["c_renee"], "Delacroix - motion for leave coming your way", """
Hi Renee - heads up that the Motion for Leave to File Third-Party Complaint (against Lakeside Masonry) will come to you Tuesday midday for a cite-check and exhibits. I'd like to file Thursday rather than Wednesday so I can get Daniel's eyes on it. Thanks!
Marcus
""", thread="t_delacroix")

email("itm_daniel_subpoena", "D1 09:05", "c_daniel", ["c_renee"], "Kessling - Varga subpoena (signed)", """
Renee,

Attached is the documents subpoena to Varga Electric Motors (the KX-40 motor supplier), signed. Please get it served this week. Their registered agent is in Milwaukee. Compliance date is 11/30.

Daniel

Daniel Achterberg | Partner | Ostrander Hale LLP | 312.555.0150
""", cc=["c_priya"], thread="t_varga", attachments=["itm_subpoena"])
doc("itm_subpoena", "D1 09:05", "Subpoena to Produce Documents - Varga Electric Motors, Inc. (AO 88B), signed 11/2/2026", """
UNITED STATES DISTRICT COURT for the Northern District of Illinois
Prairie Hollow Growers Cooperative, Plaintiff, v. Kessling Pump & Controls, Inc., Defendant. Civil Action No. 1:26-cv-03182

SUBPOENA TO PRODUCE DOCUMENTS, INFORMATION, OR OBJECTS OR TO PERMIT INSPECTION OF PREMISES IN A CIVIL ACTION

To: Varga Electric Motors, Inc., c/o its registered agent, Badger State Registered Agents, Inc., 777 E. Wisconsin Avenue, Suite 1400, Milwaukee, WI 53202

Production: YOU ARE COMMANDED to produce at the time, date and place set forth below the documents described in Schedule A, and to permit inspection, copying, testing or sampling of the material.
Place: Ostrander Hale LLP, 180 N. Canal Street, Suite 2200, Chicago, IL 60606 (or by electronic delivery to rkowalczyk@ostranderhale.com). Date and time: November 30, 2026, 10:00 a.m.

The provisions of Fed. R. Civ. P. 45(c), (d)(1)-(3) and (e)-(g) are attached.

Date: 11/02/2026. /s/ Daniel Achterberg, Attorney's signature. Attorney for Defendant Kessling Pump & Controls, Inc., Ostrander Hale LLP, 180 N. Canal Street, Suite 2200, Chicago, IL 60606, dachterberg@ostranderhale.com, 312.555.0150.

Notice to the person who issues or requests this subpoena: If this subpoena commands the production of documents, electronically stored information, or tangible things or the inspection of premises before trial, a notice and a copy of the subpoena must be served on each party in this case before it is served on the person to whom it is directed. Fed. R. Civ. P. 45(a)(4).

SCHEDULE A (period January 1, 2023 to present)
1. Specifications and data sheets for the motors Varga supplied to Kessling for the KX-40 pump line.
2. Documents sufficient to show the motor serial numbers Varga shipped to Kessling for the pumps bearing Kessling serials KX40-24-0311 to -0330, KX40-24-0517 to -0534 and KX40-25-0102 to -0109.
3. Warranty claims, returns or failure reports Varga received concerning motors supplied for the KX-40 line.
4. Communications with Prairie Hollow Growers Cooperative or its counsel.
""", "c_daniel")

email("itm_daniel_prebill", "D1 09:20", "c_daniel", ["c_renee"], "FW: October pre-bills ready for review - 10442-003 Kessling", """
Renee - can you go through your and Gloria's entries against the Kessling guidelines (sections 3-5)? Tell me what has to come off or be rewritten and the dollar amount of any write-off. I want to release this Wednesday morning before Kevin's 10:00 cutoff.
D.

-----Original Message-----
From: Kevin Doyle
Sent: Monday, November 2, 2026 7:52 AM
To: Daniel Achterberg
Subject: October pre-bills ready for review - 10442-003 Kessling
(see attached sheet)
""", thread="t_prebill", attachments=["itm_prebill"])

email("itm_mail_rfp2", "D1 10:40", "c_mailroom", ["c_renee"], "Scanned mail - 10442-003 - Corbin & Lisle envelope", """
Renee,

Received in today's U.S. Mail, scanned and attached. Envelope from Corbin & Lisle LLP, Oak Brook, postmarked October 30, 2026. Original is in your mail slot.

Contents: Plaintiff's Second Set of Requests for Production of Documents to Defendant (Nos. 19-27), with Certificate of Service.

Luis Ortega | Office Services
""", thread="t_rfp2", attachments=["itm_rfp2"])
doc("itm_rfp2", "D1 10:40", "Plaintiff's Second Set of Requests for Production to Defendant (Nos. 19-27) - scanned", """
IN THE UNITED STATES DISTRICT COURT FOR THE NORTHERN DISTRICT OF ILLINOIS, EASTERN DIVISION
Prairie Hollow Growers Cooperative v. Kessling Pump & Controls, Inc., No. 1:26-cv-03182

PLAINTIFF'S SECOND SET OF REQUESTS FOR PRODUCTION OF DOCUMENTS TO DEFENDANT
Pursuant to Fed. R. Civ. P. 26 and 34, Plaintiff requests that Defendant produce the following documents within thirty (30) days of service, at the offices of Corbin & Lisle LLP. Definitions and instructions in Plaintiff's First Requests are incorporated.

19. All preventative maintenance ("PM") schedules, PM visit records and PM checklists for Plaintiff's KX-40 pumps for 2024 and 2025.
20. All text messages, Teams or other instant messages among Kessling field service personnel concerning Plaintiff or Plaintiff's pumps.
21. All documents concerning RMA-25-0077, including teardown reports, photographs and test data.
22. Kessling's communications with Varga Electric Motors, Inc. concerning the KX-40 motors.
23. Training materials provided to Kessling field technicians on the Type 21 seal.
24. Documents concerning the January 2025 revision (Rev. D) of the KX-40 Installation and Maintenance Manual.
25. Kessling's communications with any distributor concerning seal or bearing failures in KX-40 pumps.
26. Documents sufficient to show the controller data-logging capability of the KX-40 pump controllers.
27. All controller data logs downloaded from Plaintiff's pumps.

Dated: October 30, 2026. Respectfully submitted, PRAIRIE HOLLOW GROWERS COOPERATIVE, By: /s/ Nathan J. Corbin, Corbin & Lisle LLP, 2001 Spring Road, Suite 400, Oak Brook, IL 60523, ncorbin@corbinlisle.com

CERTIFICATE OF SERVICE
I certify that on October 30, 2026, I caused a copy of the foregoing to be served on counsel of record for Defendant by depositing it in the U.S. Mail at Oak Brook, Illinois, first-class postage prepaid, addressed to: Daniel Achterberg and Priya Raman, Ostrander Hale LLP, 180 N. Canal Street, Suite 2200, Chicago, IL 60606.
/s/ Stacy Feld
""", "c_ncorbin")

email("itm_nef_appearance", "D1 11:15", "c_court", ["c_daniel", "c_priya", "c_renee", "c_ncorbin"], "Activity in Case 1:26-cv-03182 Prairie Hollow Growers Cooperative v. Kessling Pump & Controls, Inc. Attorney Appearance", """
This is an automatic e-mail message generated by the CM/ECF system. Please DO NOT RESPOND to this e-mail because the mail box is unattended.
***NOTE TO PUBLIC ACCESS USERS*** Judicial Conference of the United States policy permits attorneys of record and parties in a case (including pro se litigants) to receive one free electronic copy of all documents filed electronically, if receipt is required by law or directed by the filer. PACER access fees apply to all other users. To avoid later charges, download a copy of each document during this first viewing.

United States District Court, Northern District of Illinois - CM/ECF NextGen
Notice of Electronic Filing
The following transaction was entered by Bensen, Kara on 11/2/2026 at 10:58 AM CST and filed on 11/2/2026
Case Name: Prairie Hollow Growers Cooperative v. Kessling Pump & Controls, Inc.
Case Number: 1:26-cv-03182
Document Number: 47
Docket Text: ATTORNEY Appearance for Plaintiff Prairie Hollow Growers Cooperative by Kara M. Bensen (Bensen, Kara) (Entered: 11/02/2026)

1:26-cv-03182 Notice has been electronically mailed to:
Nathan J. Corbin ncorbin@corbinlisle.com, sfeld@corbinlisle.com
Kara M. Bensen kbensen@corbinlisle.com
Daniel Achterberg dachterberg@ostranderhale.com, rkowalczyk@ostranderhale.com
Priya Raman praman@ostranderhale.com
""", thread="t_nef47")

chat("itm_gloria_d1", "D1 11:50", "c_gloria", ["c_renee"], "Hi! Daniel wants a hold on his calendar for the Lindqvist depo once there's a date. Any idea yet? Also he says thank you for the pre-bill look, he hates those :)", thread="t_gloria")

email("itm_tom_status", "D1 12:30", "c_tom", ["c_renee"], "Kessling Vol. 2 - status", """
Renee,

Status on Vol. 2:
- First-level review complete: 1,237 docs responsive.
- Privilege QC about 80% done. 24 of those are coded Privileged (withhold or redact) and 3 are still "Needs Further Review - Priv" (I'll send you those).
- I'll run Bates/legends Wednesday and send you the QC report. Prefix KESS, starting at KESS000413 (Vol. 1 ended at KESS000412).
- Privilege export (for the log) to you Tuesday afternoon.

Tom
Tom Nguyen | Litigation Support Manager | Ostrander Hale LLP | x0188
""", thread="t_vol2")

email("itm_daniel_tickets", "D1 13:00", "c_daniel", ["c_renee"], "Kessling - service ticket count", """
Renee, quick one for my Lindqvist outline: of the 2025 field service tickets for Prairie Hollow, how many were actually mechanical seal or bearing failures? Complaint para. 31 says "at least nineteen seal and bearing failures." I'd like the number and the ticket list, and anything that wasn't a seal or bearing problem called out separately. No rush - by Wednesday is fine.
D.
""", thread="t_tickets")

email("itm_corbin_courtesy", "D1 15:30", "c_ncorbin", ["c_priya"], "Prairie Hollow v. Kessling - courtesy copy of Plaintiff's Second Requests for Production", f"""
Priya,

As a courtesy, attached is a PDF of Plaintiff's Second Set of Requests for Production (Nos. 19-27). Service was made by U.S. Mail on Friday, October 30.

Regards,
{SIG_NC}
""", cc=["c_renee", "c_sfeld"], thread="t_rfp2_courtesy", attachments=["itm_rfp2"])

chat("itm_priya_chat_d1", "D1 15:00", "c_priya", ["c_renee"], "Can you send me Rick's email from last night with the rog answers? And the KX-40 invoice summary - I want to look at No. 4 before Wednesday.", thread="t_priya_chat")

email("itm_northline_ack", "D1 15:40", "c_process", ["c_renee"], "RE: Service request - Varga Electric Motors (Kessling)", """
Renee,

Got it, thanks. Job #NP-26-11088. Registered agent office hours are 9-4. We'll let you know the service time as soon as it's on the route sheet - probably Wednesday or Thursday.

Ray Duda
Dispatch | Northline Process Service | 414.555.0136
""", thread="t_varga_ps")

email("itm_rick_travel", "D1 16:10", "c_rick", ["c_renee"], "travel this week", """
Renee - FYI I'm at the Midwest Irrigation Expo in Kearney, NE Thursday and Friday. I'll have my phone and laptop but I'm on the show floor most of the day. Wednesday is best if you need me for anything in person-ish.
Rick
""", thread="t_rick_travel")

email("itm_library_d1", "D1 16:45", "c_library", ["c_firm"], "Thursday: Westlaw Precision refresher at noon", """
Join Research Services Thursday at 12:00 in Training Room 27A for a 45-minute Westlaw Precision refresher (KeyCite flags, Litigation Analytics for N.D. Ill. judges). Lunch provided; RSVP not required.
""")
email("itm_news_d1b", "D1 14:00", "c_vendor", ["c_renee"], "Webinar: Privilege logs after the 2026 Sedona commentary", """
Join our 60-minute webinar on categorical privilege logs, metadata logs and what courts are accepting in 2026. One hour of CLE credit available in Illinois. Register online.
""")
email("itm_firm_d1", "D1 12:00", "c_firm", ["c_firm"], "Food drive - last week for donations", """
The Greater Chicago Food Depository drive closes Friday. Bins are by the 22nd and 27th floor elevators. Thank you to everyone who has donated so far.
""")
