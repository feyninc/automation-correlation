# Part 11: Friday 2026-11-06
email("itm_kevin_time", "D5 08:00", "c_kevin", ["c_firm"], "Reminder: release this week's time by 5:00 p.m. today", """
All timekeepers: please release all time for the week of November 2 in iTimekeep by 5:00 p.m. today. Reminder for Kessling (10442) and other guideline clients: one task per entry, tenths of an hour, no clerical tasks.
Kevin Doyle, Billing
""", thread="t_time")
email("itm_docusign_done", "D5 08:00", "c_vendor", ["c_renee"], "Completed: Please DocuSign: Kessling - Verification of Answers to Plaintiff's First Set of Interrogatories", """
DocuSign: All parties have completed. Richard Szymanski signed on 11/5/2026 at 9:47 PM CT (Kearney, NE). Certificate of completion attached. Envelope ID 7C1F-22A9-41D0.
""", thread="t_docusign")
email("itm_northline_aff", "D5 08:00", "c_process", ["c_renee"], "Affidavit of service - Varga Electric Motors (Job #NP-26-11088)", """
Renee - signed and notarized affidavit of service attached: served 11/5/2026 at 9:04 a.m., Badger State Registered Agents, Inc., 777 E. Wisconsin Ave., Suite 1400, Milwaukee, by delivery to Janice Moore, authorized intake clerk. Invoice to follow ($145.00 rush-route rate). - Ray
""", thread="t_varga_ps")
email("itm_news_d5", "D5 08:00", "c_vendor", ["c_renee"], "Litigation Daily Briefing - Friday, November 6", """
Today: weekend reading on the Sedona privilege log commentary; how to build a deposition exhibit list from a document database; a Chicago court reporter shortage.
""")
email("itm_facilities_ok", "D5 08:30", "c_facilities", ["c_renee"], "Confirmed: 24B, Thu 11/19, 8:30-6:00 (and 24C breakout)", """
Confirmed: Conference Room 24B with video conferencing, Thursday 11/19/2026 8:30 a.m. - 6:00 p.m.; breakout room 24C held for the same hours.
""", thread="t_room")
email("itm_daniel_exhibits", "D5 09:15", "c_daniel", ["c_renee"], "Lindqvist - exhibit list first cut by Tuesday", """
Renee - great work this week. For Lindqvist on the 19th, can you put together a first cut of an exhibit list by Tuesday 11/10? I want: the service tickets on his fields (especially the repeat seal failures), the two teardown reports, the controller log showing the closed-valve run, his June 2025 e-mails with Dennis Okon, and whatever in Plaintiff's Vol. 2 shows their own operating logs and PM practices. Organize by topic, with Bates numbers.
D.
""", thread="t_exhibits")
email("itm_priya_final", "D5 09:45", "c_priya", ["c_renee"], "Kessling - signed responses; OK to serve", """
Renee - attached are the signed RFP responses and the signed objections to the interrogatories (final, my /s/). Answers + Rick's verification are good. Production and privilege log approved. Please serve everything on Nathan, Kara and Stacy by 3:00 today, with a cover letter listing the production range, and release the ShareFile link to them at the same time. Then let docketing know.
P
""", thread="t_week", attachments=["itm_rfp_final", "itm_rogs_final"])
doc("itm_rfp_final", "D5 09:45", "FINAL - Kessling's Responses and Objections to Plaintiff's First Requests for Production (signed 11/6/2026)", """
Final per v4 and P. Raman's comments; RFP 11 revised to: "Kessling will produce the field service tickets and any preventative-maintenance records located for Plaintiff's sites for 2024-2025. Kessling's search for additional 2024 preventative-maintenance records is continuing, and Kessling will supplement under Rule 26(e)." Introductory paragraph: production served herewith as Volume 2, Bates numbers beginning KESS000413 (closing number to be conformed to the final production report before service). Signed: /s/ Priya Raman, Ostrander Hale LLP, attorney for Defendant, November 6, 2026 (Fed. R. Civ. P. 26(g)).
""", "c_priya")
doc("itm_rogs_final", "D5 09:45", "FINAL - Kessling's Answers and Objections to Plaintiff's First Set of Interrogatories (objections signed 11/6/2026; verified 11/5/2026)", """
Final answers as revised 11/5/2026 (No. 4: 46 sold on three invoices, 48 delivered including the two RMA-25-0077 replacements). Objections signed /s/ Priya Raman, November 6, 2026. Verification executed by Richard Szymanski via DocuSign on November 5, 2026 under 28 U.S.C. 1746.
""", "c_priya")
email("itm_priya_jsr", "D5 10:20", "c_priya", ["c_renee"], "JSR due 11/13", """
Renee - Nathan's office will circulate a first draft of the joint status report Monday. Can you draft our discovery-status section by Tuesday? Written discovery served and answered, the productions by volume and Bates range, the Lindqvist deposition, what's outstanding (their 2d RFPs, Varga subpoena), and the fact discovery close. Keep the disputes paragraph short; Daniel will write that after the 11/9 call.
P
""", thread="t_jsr")
email("itm_sfeld_eta", "D5 11:00", "c_sfeld", ["c_renee"], "ETA on Kessling responses?", """
Hi Renee - Nathan asked me to check on timing for today's responses and production. Thanks!
Stacy
""", thread="t_sfeld_eta")
email("itm_marcus_d5", "D5 12:10", "c_marcus", ["c_renee"], "Thanks!", """
Saw the accepted envelope and Jeff's reply - thanks for turning that around. I owe you a coffee.
M.
""", thread="t_delacroix")
email("itm_tom_link", "D5 14:00", "c_tom", ["c_renee"], "RE: KESS PROD 002 - link ready", """
Renee - ShareFile link for KESS PROD 002 (1,215 docs, 2,391 pages, KESS000413-KESS002803) is set to expire in 30 days and requires recipient verification. I'll release it to whoever you say when you send the service e-mail.
Tom
""", thread="t_vol2")
email("itm_corbin_receipt", "D5 15:50", "c_ncorbin", ["c_renee"], "RE: Prairie Hollow v. Kessling - Defendant's discovery responses, Volume 2 production and privilege log", f"""
Renee - received, and the ShareFile link works. Thank you.
{SIG_NC}
""", cc=["c_priya", "c_sfeld", "c_kbensen"], thread="t_service_1106")
email("itm_reporter_d5", "D5 16:00", "c_reporter", ["c_renee"], "Confirmation LRS-114582 (PDF)", """
Attached is our written confirmation for the Lindqvist deposition, 11/19/2026, 9:30 a.m., stenographer + videographer + Zoom. Cancellation within 48 hours incurs a 2-hour minimum.
Denise
""", thread="t_reporter")
chat("itm_gloria_d5", "D5 16:20", "c_gloria", ["c_renee"], "Daniel's gone for the day - says have a great weekend and thanks for this week!", thread="t_gloria")
email("itm_firm_d5", "D5 12:00", "c_firm", ["c_firm"], "Friday social - 5:00 p.m., 27th floor", """
Join colleagues on 27 at 5:00 for the November Friday social. Mocktails and snacks.
""")
email("itm_library_d5", "D5 13:00", "c_library", ["c_renee"], "New: N.D. Ill. judges' standing orders binder updated", """
Research Services has updated the N.D. Ill. standing orders binder on the intranet (Judges Whitford and Talbot pages revised 10/30/2026).
""")
email("itm_it_d5", "D5 10:00", "c_it", ["c_renee"], "Ticket SD-88214 closed: reported phishing", """
Thanks for reporting the fake NEF. The domain ilnd-uscourts.net has been blocked firm-wide and matching messages removed from 41 mailboxes. No credentials were entered from your account.
""", thread="t_phish_ticket")
