# Part 7: Wednesday 2026-11-04
email("itm_news_d3", "D3 08:00", "c_vendor", ["c_renee"], "Litigation Daily Briefing - Wednesday, November 4", """
Today: courts split on whether a 502(d) order covers deliberate productions; practical tips for privilege log descriptions; N.D. Ill. judges' standing orders on discovery motions, updated.
""")
email("itm_docket_conf_rfp2", "D3 08:00", "c_docket", ["c_renee"], "Entered: 10442-003 - Response to Pl's 2d RFPs due 12/03/2026", """
Renee - entered in CompuLaw as requested and verified against the rule set:
12/03/2026 Thu  10442-003  Defendant's responses to Plaintiff's Second Requests for Production (Nos. 19-27) due. Served by U.S. Mail 10/30/2026. FRCP 34(b)(2)(A), 6(a)(1)(C), 6(d).
Reminders: 11/19/2026, 11/30/2026. Responsible attorney: P. Raman.
Sharon
""", thread="t_docket")
email("itm_docket_conf_48", "D3 08:00", "c_docket", ["c_renee"], "Entered: 10442-003 - Dkt. 48 dates", """
Entered:
11/13/2026 Fri  10442-003  Joint written status report due (Dkt. 48). Reminder 11/10.
11/18/2026 Wed  10442-003  Telephonic status hearing, 9:30 a.m., Mag. J. Talbot (Dkt. 48).
Sharon
""", thread="t_docket")
email("itm_sharefile_d3", "D3 08:00", "c_vendor", ["c_renee"], "ShareFile: Corbin & Lisle shared folder downloaded", """
Your download of "PHGC Production Vol 002" (877 pages, 1 load file) from corbinlisle.sharefile.com was completed by tnguyen@ostranderhale.com on 11/3/2026 at 4:41 PM.
""")
email("itm_corbin_confirm", "D3 09:40", "c_ncorbin", ["c_renee"], "RE: Prairie Hollow v. Kessling - Lindqvist deposition dates", f"""
Renee,

Confirmed: Dale Lindqvist, Thursday, November 19, 9:30 a.m., at your offices. Please send the notice. One of us may attend remotely, so please include a remote link.

Regards,
{SIG_NC}
""", cc=["c_priya", "c_daniel", "c_sfeld", "c_kbensen"], thread="t_depo")
email("itm_rick_correction", "D3 10:05", "c_rick", ["c_renee", "c_priya"], "correction on KX-40 count - Rog 4", """
Renee, Priya -

Correction on the pump count I sent 10/20. The ERP report only pulls invoiced shipments. We also shipped 2 replacement KX-40s to Prairie Hollow under warranty on RMA-25-0077 on 7/14/25 (no invoice, $0, serials KX40-25-0311 and -0312) to replace the two Field 12 pumps we pulled (KX40-24-0528 and -0530). So: 46 sold on the three invoices, 48 delivered in total. Updated sheet attached. Sorry about that.

Rick
""", thread="t_rick_rogs", attachments=["itm_sales_corrected"])
doc("itm_sales_corrected", "D3 10:05", "KX-40 shipments to Prairie Hollow - corrected (11/4/2026)", """
Corrected by R. Szymanski 11/4/2026 (adds warranty replacement shipments from the RMA log)

Document      | Date       | Units | Unit price | Extended | Note
INV-24-1187   | 2024-03-18 | 20    | $14,850    | $297,000 | serials KX40-24-0311 to -0330
INV-24-1342   | 2024-05-06 | 18    | $14,850    | $267,300 | serials KX40-24-0517 to -0534
INV-25-0219   | 2025-02-24 |  8    | $14,850    | $118,800 | serials KX40-25-0102 to -0109
RMA-25-0077   | 2025-07-14 |  2    | $0         | $0       | warranty replacements, serials KX40-25-0311 and -0312, for KX40-24-0528 and -0530 (removed)
SOLD (invoiced) |          | 46    |            | $683,100 |
DELIVERED TOTAL |          | 48    |            |          |
Pumps in service at Plaintiff after 7/14/2025: 46 (48 delivered less the 2 removed).
""", "c_rick", kind="sheet")
email("itm_northline_sched", "D3 10:15", "c_process", ["c_renee"], "RE: Service request - Varga Electric Motors (Kessling) - scheduled", """
Renee,

Job #NP-26-11088 is on tomorrow's route: our server will serve Varga's registered agent (Badger State Registered Agents, 777 E. Wisconsin Ave., Suite 1400) Thursday 11/5 at 9:00 a.m. when they open. Affidavit of service to you by Friday morning.

Ray
""", thread="t_varga_ps")
email("itm_daniel_prebill_thx", "D3 10:45", "c_daniel", ["c_renee"], "RE: Kessling pre-bill", """
Thanks Renee, very clear. I've released it with your changes. Gloria - FYI, your time on Kessling is overhead under their guidelines; please don't enter it to the matter going forward.
D.
""", cc=["c_gloria", "c_kevin"], thread="t_prebill")
chat("itm_priya_chat_d3", "D3 11:20", "c_priya", ["c_renee"], "Talked to Rick last night re the PM logs and texts - handled, thanks for the quick flag. Daniel and I will deal with Nathan's custodian points on the 9th.", thread="t_priya_chat")
email("itm_tom_staged", "D3 12:30", "c_tom", ["c_renee"], "Kessling Vol. 2 staged - QC report + 3 NFR docs", """
Renee,

Vol. 2 is staged in Relativity (production set "KESS PROD 002"). QC report attached:
- 1,214 documents, 2,388 pages, KESS000413 - KESS002800
- Excludes 20 withheld privileged docs (14 for the log, 6 post-complaint communications with us that para. 9(c) says we don't log); 4 redacted docs produced with redaction boxes; held out: the 3 "Needs Further Review - Priv" docs.
- Legends: 287 docs CONFIDENTIAL, 34 docs ATTORNEYS' EYES ONLY.

Can you just make the call on the 3 NFR docs (NFR-01, -02, -03) so I can finalize today? Two are Rick and Gwen emails that cc their outside GC (Feeney) and one is a site-visit scheduling email where Feeney is bcc'd. I'd guess none of them are really legal advice. If you tell me "not priv" I'll add them at the end of the set this afternoon.

Tom
""", thread="t_vol2", attachments=["itm_qc_report_v1"])
doc("itm_qc_report_v1", "D3 12:30", "Production QC report - KESS PROD 002 (staged 11/4/2026 12:10)", """
Relativity production set: KESS PROD 002 (staged, not exported)
Bates: KESS000413 - KESS002800 | Documents: 1,214 | Images: 2,388 pages | Natives: 61 (slip-sheeted)
Redacted (privilege): 4 docs - PRIV-004 at KESS001022-KESS001023; PRIV-009 at KESS001310; PRIV-014 at KESS001577; PRIV-017 at KESS002411-KESS002414
Withheld (privilege): 14 docs (PRIV-001, 002, 003, 005, 006, 007, 008, 010, 011, 012, 013, 015, 016, 018)
Not logged per ESI para. 9(c): 6 docs (PRIV-019 to PRIV-024)
Held out pending decision: NFR-01, NFR-02, NFR-03
Confidentiality: CONFIDENTIAL 287 docs; ATTORNEYS' EYES ONLY 34 docs
QC: image/text count match; no blank pages; legends verified on sample of 120.
""", "c_tom", kind="sheet")
email("itm_tom_inadvertent", "D3 13:10", "c_tom", ["c_renee"], "PHGC Vol. 2 - possible privileged doc (PHGC000977-979)", """
Renee,

While QC'ing Plaintiff's Vol. 2 I hit PHGC000977-PHGC000979: an e-mail chain dated 9/3/2025 from Walt Herrmann (their GM) to Nathan Corbin, subject "Re: what to say about the pump maintenance." It looks like it's to their lawyer. I stopped reading after the header, tagged it "Potentially Inadvertently Produced" and restricted it in Relativity so it's not in anyone's review batch. Nobody else has seen it. What do you want me to do?

Tom
""", thread="t_phgc_vol2_qc")
email("itm_corbin_pressure", "D3 14:20", "c_ncorbin", ["c_renee"], "Kessling documents - today please", f"""
Renee,

We are preparing Mr. Lindqvist and need Kessling's documents before Friday. Please send us whatever is already Bates-stamped today; the privilege issues can be sorted out later, and anything privileged can simply be clawed back under the 502(d) order. There is no reason to hold the whole production for the log.

Thanks,
{SIG_NC}
""", cc=["c_sfeld"], thread="t_corbin_pressure")
email("itm_marcus_d3", "D3 15:00", "c_marcus", ["c_renee"], "RE: Delacroix - motion for leave", """
Renee - Daniel has looked at it; I'll sign tomorrow at 10 and send you the PDF with the notice of motion. Please file by 3 Thursday so it's on the clerk's queue before the weekend.
Marcus
""", thread="t_delacroix")
chat("itm_gloria_d3", "D3 15:30", "c_gloria", ["c_renee"], "Is the Lindqvist depo confirmed? I'll put Daniel down for the 19th all day and tell facilities we need 24B.", thread="t_gloria")
email("itm_priya_comments", "D3 17:10", "c_priya", ["c_renee"], "Kessling rogs/RFPs - my comments", """
Renee - drafts look good. Comments in the documents (mostly tightening the objections in 7, 8 and 15). Two things:
1. Rog 4: let's get the count right given Rick's correction this morning.
2. RFP 11: I talked to Rick. Change to: "Kessling will produce the field service tickets and any preventative-maintenance records located for Plaintiff's sites for 2024-2025. Kessling's search for additional 2024 preventative-maintenance records is continuing, and Kessling will supplement under Rule 26(e)." Do not characterize what exists.
Send Rick the final answers and the verification tomorrow morning. I'll sign the objections and the RFP responses Friday morning.
P
""", thread="t_week")
email("itm_firm_d3", "D3 12:00", "c_firm", ["c_firm"], "Benefits open enrollment closes November 13", """
Open enrollment for 2027 medical, dental and FSA elections closes Friday, November 13. Log in to the benefits portal to make or confirm your elections.
""")
email("itm_library_d3", "D3 09:00", "c_library", ["c_renee"], "Your PACER usage report - October", """
Your October PACER usage billed to client matters: 10442-003 $8.40 (28 pages); 11870-002 $0.00. Remember to download NEF documents on the free first look.
""")
email("itm_priya_to_corbin", "D3 15:05", "c_priya", ["c_ncorbin"], "RE: Kessling documents - today please", f"""
Nathan,

Renee passed along your note. Kessling will serve its responses, its Volume 2 production and its privilege log together on Friday, November 6, as the ESI Stipulation (para. 9(a)) contemplates. You will have the documents nearly two weeks before Mr. Lindqvist's deposition. We are not going to produce on a rolling, unreviewed basis and rely on clawbacks.

Best,
{SIG_PR}
""", cc=["c_renee", "c_sfeld"], thread="t_corbin_pressure")
