act(5, "a5_01", "D5 08:30", "read", "itm_docusign_done", "Opened the DocuSign completion; saved the signed verification to iManage.", "Verification complete.")
act(5, "a5_02", "D5 08:50", "read", "itm_northline_aff", "Saved the Varga affidavit of service to iManage.", "Filing housekeeping.")
act(5, "a5_03", "D5 09:20", "read", "itm_daniel_exhibits", "Read Daniel's request for a Lindqvist exhibit list by Tuesday.", "The human does not start it this week (N22 never done in-week).")
act(5, "a5_04", "D5 10:00", "read", "itm_priya_final", "Opened Priya's signed responses and approval.", "")
act(5, "a5_05", "D5 10:30", "edit_doc", "itm_rfp_final", "Conformed the introductory paragraph: 'Kessling's Volume 2 production, Bates numbered KESS000413 through KESS002803, is served herewith.' No other change to the signed text.", "Conforming change only, Bates from Tom's final report.")
act(5, "a5_06", "D5 11:30", "create_doc", None, """
Title: Cover letter - Kessling Volume 2 production (11/6/2026)

OSTRANDER HALE LLP | 180 N. Canal Street, Suite 2200 | Chicago, Illinois 60606
November 6, 2026
VIA E-MAIL AND SHAREFILE
Nathan J. Corbin, Kara M. Bensen, Corbin & Lisle LLP, 2001 Spring Road, Suite 400, Oak Brook, IL 60523

Re: Prairie Hollow Growers Cooperative v. Kessling Pump & Controls, Inc., No. 1:26-cv-03182 (N.D. Ill.)

Dear Counsel:

Enclosed with Defendant's discovery responses served today is Kessling's Volume 2 production (KESS PROD 002), produced by secure ShareFile link:
- Bates range: KESS000413 through KESS002803 (1,215 documents; 2,391 pages), in the format required by paragraph 8 of the ESI Stipulation (Dkt. 29), with 61 native files slip-sheeted.
- Confidentiality designations under the Stipulated Confidentiality Order (Dkt. 31): 288 documents designated CONFIDENTIAL INFORMATION - SUBJECT TO PROTECTIVE ORDER and 34 documents designated ATTORNEYS' EYES ONLY, as marked on each page.
- Four documents are produced with privilege redactions and sixteen are withheld; each is identified on Kessling's privilege log, served herewith under paragraph 9 of the ESI Stipulation. Communications with litigation counsel of record dated on or after April 14, 2026 are not logged (paragraph 9(c)).

The ShareFile link expires on December 6, 2026. Please let me know if you have any difficulty accessing the production.

Very truly yours,
Renee Kowalczyk, Senior Litigation Paralegal
cc: Priya Raman; Daniel Achterberg; Stacy Feld
""", "Reference for N19 (late: discoverable Thursday 13:00). 2,391 pages and KESS002803 are the checked values.")
act(5, "a5_07", "D5 12:00", "reply", "itm_sfeld_eta", "Hi Stacy - this afternoon, before 3:00. You'll get the responses, the privilege log, the cover letter and the ShareFile link in one e-mail. - Renee", "Logistics reply; does not send anything early.")
act(5, "a5_08", "D5 13:30", "edit_doc", None, "Final QC of the privilege log against Tom's final QC report: 20 entries; redaction Bates numbers match (KESS001022-1023, KESS001310, KESS001577, KESS002411-2414); NFR-03 not on the log (produced at KESS002801-2803); attorneys marked Esq.; no entry dated on or after 4/14/2026.", "QC of her own log (no target: the log is the document she created Thursday).")
act(5, "a5_09", "D5 15:20", "send", None, f"""
To: Nathan Corbin; Kara Bensen
Cc: Stacy Feld; Priya Raman; Daniel Achterberg
Subject: Prairie Hollow v. Kessling - Defendant's discovery responses, Volume 2 production and privilege log

Counsel,

Served today by e-mail under Fed. R. Civ. P. 5(b)(2)(E) and Dkt. 29, para. 4, please find attached:
1. Defendant Kessling Pump & Controls, Inc.'s Answers and Objections to Plaintiff's First Set of Interrogatories, with the Verification of Richard Szymanski;
2. Defendant's Responses and Objections to Plaintiff's First Requests for Production;
3. Defendant's Privilege Log for the Volume 2 production (20 entries); and
4. A cover letter describing the Volume 2 production, KESS000413 through KESS002803 (2,391 pages).
The production is available through the ShareFile link Tom Nguyen is releasing to the three of you now; the link requires recipient verification and expires December 6, 2026.

{SIG_RK}
""", "Reference for N24 (served by 3:00 as Priya asked; late: discoverable 09:45). Not filed on ECF.")
act(5, "a5_10", "D5 15:25", "reply", "itm_tom_link", "Tom - service e-mail is out. Please release the KESS PROD 002 link now to Nathan Corbin, Kara Bensen and Stacy Feld only. Thanks!", "Release only after service.")
act(5, "a5_11", "D5 16:00", "send", None, """
To: Docketing (Sharon Wiley)
Cc: Priya Raman
Subject: 10442-003 Kessling - 11/6 deadlines complied with

Sharon - please mark complied: (1) responses to Plaintiff's First Interrogatories, (2) responses to Plaintiff's First RFPs, (3) privilege log with production - all served by e-mail on 11/6/2026 at 3:20 p.m. Please also add: deposition of Dale Lindqvist, Thursday 11/19/2026 9:30 a.m. (noticed 11/5), and Varga subpoena compliance date Monday 11/30/2026 10:00 a.m. Thanks. - Renee
""", "Closing the loop with docketing.")
act(5, "a5_12", "D5 16:30", "edit_doc", "itm_timesheet", """
Fri 11/6 (10442-003): 0.6 Prepare production cover letter for Volume 2 production. | 0.4 Quality-check privilege log against final production report. | 0.4 Serve discovery responses, privilege log and production on Plaintiff's counsel. | 0.2 Conform Bates range in responses to requests for production.
Week released: Mon 2.8, Tue 0.8 (10442) + 0.2 (11870), Wed 2.4 (10442) + 1.4 (11870), Thu 3.3 (10442) + 0.3 (11870), Fri 1.6 (10442). Total 12.8 hours released.
""", "Reference for N21 (late: discoverable 08:00).")
act(5, "a5_13", "D5 16:50", "reply", "itm_daniel_exhibits", "Will do - you'll have a first cut by Tuesday afternoon, organized by topic with Bates numbers. Have a good weekend.", "Commits to the exhibit list for next week; never done in-week.")
