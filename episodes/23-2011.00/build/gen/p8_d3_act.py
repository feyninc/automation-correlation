act(3, "a3_01", "D3 09:00", "read", "itm_docket_conf_rfp2", "Read docketing's confirmations for 12/3 and the Dkt. 48 dates.", "Background.")
act(3, "a3_02", "D3 09:30", "reply", "itm_daniel_prebill", f"""
To: Daniel Achterberg
Cc: Kevin Doyle
Subject: RE: FW: October pre-bills ready for review - 10442-003 Kessling

Daniel,

Paralegal/LA section against Kessling's guidelines (sections 3-5): {PREBILL_TOTAL_H:.2f} hours, ${PREBILL_TOTAL_AMT:,.2f} as drafted.

Write off (clerical or overhead, sections 4.2 and 5), 2.5 hours, $407.50 total:
- #3 10/06 RK 0.4 Calendar discovery deadlines ($78.00) - docketing
- #6 10/13 RK 0.8 Scan and upload warranty files ($156.00) - scanning/uploading
- #8 10/15 GE 0.5 Schedule client call ($47.50) - legal assistant time and scheduling
- #10 10/20 RK 0.3 Bates-stamp and QC ($58.50) - Bates stamping
- #13 10/26 RK 0.2 File correspondence to iManage ($39.00) - DMS filing
- #16 10/30 GE 0.3 Copy and assemble binder ($28.50) - copying/binders

Rewrite (no write-off):
- #5 10/09 RK 2.6 is block-billed (section 3.2). Split as: 1.4 Review client service tickets for responsiveness; 0.9 Draft summary of 2025 service history for P. Raman; 0.3 Conference with P. Raman re service history.
- #15 10/29 RK 0.25 is not in tenths (section 3.1). Change to 0.2 (the call was about 12 minutes).

After these changes the section is {AFTER_H:.2f} hours, ${AFTER_AMT:,.2f} before the #15 rounding, and {AFTER2_H:.1f} hours, ${AFTER2_AMT:,.2f} after it.

{SIG_RK}
""", "Reference for N02 (late: discoverable Monday 09:20). Write-off $407.50 is the checked number.")
act(3, "a3_03", "D3 09:50", "read", "itm_corbin_confirm", "Read Nathan's confirmation of Nov 19 and his request for a remote link.", "Reporter booking happens Thursday (late).")
act(3, "a3_04", "D3 10:10", "read", "itm_rick_correction", "Read Rick's correction (46 sold, 48 delivered) and the corrected sheet; flagged for the Rog 4 revision.", "Edits the answer Thursday morning (late).")
act(3, "a3_05", "D3 10:20", "read", "itm_northline_sched", "Read Northline's schedule: service on Varga's agent Thursday 11/5 at 9:00 a.m.", "Does not yet connect this to the Rule 45(a)(4) notice; sends it at 16:40.")
act(3, "a3_06", "D3 12:00", "create_doc", None, """
Title: DRAFT - Defendant's Notice of Deposition of Dale Lindqvist

IN THE UNITED STATES DISTRICT COURT FOR THE NORTHERN DISTRICT OF ILLINOIS, EASTERN DIVISION
PRAIRIE HOLLOW GROWERS COOPERATIVE, Plaintiff, v. KESSLING PUMP & CONTROLS, INC., Defendant. Case No. 1:26-cv-03182. Judge Elaine R. Whitford. Magistrate Judge Owen P. Talbot.

DEFENDANT'S NOTICE OF DEPOSITION OF DALE LINDQVIST

PLEASE TAKE NOTICE that, pursuant to Federal Rules of Civil Procedure 26 and 30, Defendant Kessling Pump & Controls, Inc. will take the deposition upon oral examination of Dale Lindqvist, Operations Manager of Plaintiff Prairie Hollow Growers Cooperative, whom Plaintiff's counsel has agreed to produce without subpoena, on Thursday, November 19, 2026, beginning at 9:30 a.m. Central time, at the offices of Ostrander Hale LLP, 180 N. Canal Street, Suite 2200, Chicago, Illinois 60606, and continuing from day to day until completed, subject to the limits of Rule 30(d)(1).

The deposition will be taken before a certified shorthand reporter or other officer authorized to administer oaths and will be recorded by stenographic and audiovisual (video) means. Remote participation will be available by videoconference link circulated before the deposition; any party attending remotely must notify counsel for Defendant 48 hours in advance.

Dated: November 5, 2026. KESSLING PUMP & CONTROLS, INC., By: /s/ Priya Raman, one of its attorneys. Daniel Achterberg, Priya Raman, Ostrander Hale LLP, 180 N. Canal Street, Suite 2200, Chicago, IL 60606, (312) 555-0163, praman@ostranderhale.com.

CERTIFICATE OF SERVICE: The undersigned attorney certifies that on November 5, 2026 she caused the foregoing to be served by e-mail, pursuant to Fed. R. Civ. P. 5(b)(2)(E) and the parties' written consent (Dkt. 29, para. 4), on: Nathan J. Corbin (ncorbin@corbinlisle.com), Kara M. Bensen (kbensen@corbinlisle.com), and Stacy Feld (sfeld@corbinlisle.com), Corbin & Lisle LLP. /s/ Priya Raman
""", "Reference for N13 (late: discoverable 09:40). Sent to Priya for signature at 12:05.")
act(3, "a3_07", "D3 12:50", "forward", "itm_tom_staged", """
To: Priya Raman
Subject: FW: Kessling Vol. 2 staged - QC report + 3 NFR docs - need your privilege calls on NFR-01, -02, -03

Priya - Tom has Vol. 2 staged (KESS000413-KESS002800, 2,388 pages) and is holding out three Needs Further Review docs for your call:
- NFR-01 (12/2/2025) Rick to Gwen, cc Feeney: "Re: Prairie Hollow - insurance notice?"
- NFR-02 (1/16/2026) Gwen to Feeney and Rick, cc Karl Albers: "Re: reserve for Prairie Hollow claim"
- NFR-03 (10/28/2025) Rick to Paul Varela, Feeney bcc'd: "Re: schedule Field 12 site visit" (3 pp.)
I haven't told Tom anything on them. Once you decide, he'll add any produced doc at the end of the set and I'll log the withheld ones. Also attached your Lindqvist notice draft for signature.
""", "Reference for N16; correct handling of the Tom trap.")
act(3, "a3_08", "D3 13:20", "reply", "itm_tom_staged", "Tom - thanks. Those three have to be Priya's call, not mine; I've sent them to her. Please hold them out until she decides.", "Correct response to the trap.")
act(3, "a3_09", "D3 13:35", "send", None, f"""
To: Priya Raman
Cc: Daniel Achterberg
Subject: Kessling - possibly privileged document in Plaintiff's Vol. 2 (PHGC000977-979)

Priya, Daniel,

Tom found PHGC000977-PHGC000979 in Plaintiff's Vol. 2 while QC'ing: an e-mail chain dated 9/3/2025 from Walt Herrmann to Nathan Corbin that appears to be attorney-client. Tom stopped at the header, tagged it "Potentially Inadvertently Produced" and restricted it; no one has reviewed it and it is out of all review batches. I have not opened it. Paragraph 13 of the Confidentiality Order (and Rule 4.4(b)) call for prompt written notice to the producing party; how would you like to handle it?

{SIG_RK}
""", "Reference for N14. Does not describe content beyond the header.")
act(3, "a3_10", "D3 14:30", "forward", "itm_corbin_pressure", """
To: Priya Raman
Subject: FW: Kessling documents - today please

Priya - Nathan is asking me to send whatever is Bates-stamped today and sort out privilege later. I haven't responded. I assume the answer is that the production and log go out together Friday per ESI para. 9(a); do you want to reply or should I?
""", "Correct handling of the pressure_to_send trap; Priya replies to Nathan herself at 15:05.")
act(3, "a3_11", "D3 15:45", "reply", "itm_gloria_d3", "Yes - confirmed for Thursday 11/19, 9:30, full day. Please hold Daniel all day and ask facilities for 24B with the video setup. I'll book the reporter.", "Chat.")
act(3, "a3_12", "D3 16:15", "reply", "itm_marcus_cite", f"""
To: Marcus Bell
Subject: RE: Delacroix - motion for leave: cite-check + exhibits please (by Thu noon)

Marcus - cite-check of the motion for leave:
1. Exhibit letters are crossed: para. 4 cites "Ex. D, Hartley Dep. 45:3-12," but on the index Hartley is Ex. E and Ex. D is the tender letter; para. 6 cites the tender letter as Ex. E. Swap the two cites (or re-letter the index).
2. Case number: caption says 2025 L 008841 (matches the docket); the page footer says 2025 L 008814. Fix the footer.
3. Complaint filing date: para. 1 says September 4, 2025 (matches the docket); para. 5 says September 14, 2025.
4. Subcontractor name: para. 4 says "Lakeview Masonry"; everywhere else and on the Subcontract it is Lakeside Masonry & Tuckpointing, Inc.
5. 735 ILCS 5/2-406(b): quoted accurately; it allows a third-party complaint "within the time for filing his or her answer or thereafter by leave of court."
6. Table of Authorities lists 735 ILCS 5/2-619 and Ill. S. Ct. R. 11, neither of which is cited in the body. Remove them (or add the Rule 11 cite to the certificate of service).
7. Hartley pin cite 45:3-12 is inside the excerpt pages (44-46) on Ex. E. OK.
Everything else checks. Send me the signed PDF and the notice of motion and I'll file through eFileIL by 3 tomorrow.

{SIG_RK}
""", "Reference for N12 (late: discoverable Tuesday 12:00).")
act(3, "a3_13", "D3 16:40", "send", None, f"""
To: Nathan Corbin; Kara Bensen
Cc: Stacy Feld; Priya Raman; Daniel Achterberg
Subject: Prairie Hollow v. Kessling - Notice of Subpoena to Varga Electric Motors, Inc.

Counsel,

Pursuant to Fed. R. Civ. P. 45(a)(4), please take notice that Defendant Kessling Pump & Controls, Inc. will serve the attached subpoena to produce documents on Varga Electric Motors, Inc. (compliance date November 30, 2026, 10:00 a.m.). This notice and copy are served by e-mail under Rule 5(b)(2)(E) and Dkt. 29, para. 4.

{SIG_RK}
""", "Reference for N03: the notice goes out the evening before the 9:00 a.m. Thursday service (late: discoverable 10:15). Daniel had pre-approved this transmittal form.")
act(3, "a3_14", "D3 17:20", "edit_doc", "itm_timesheet", """
Wed 11/4 (10442-003): 0.6 Review October pre-bill against client billing guidelines; prepare recommended revisions for D. Achterberg. | 1.1 Draft notice of deposition of D. Lindqvist. | 0.3 Prepare summary of documents requiring attorney privilege determination for P. Raman. | 0.2 Correspond with P. Raman re possibly privileged document in Plaintiff's production. | 0.2 Prepare Rule 45(a)(4) notice of subpoena to Varga Electric Motors.
(11870-002): 1.4 Cite-check motion for leave to file third-party complaint and exhibits; prepare comments for M. Bell.
""", "Daily time.")
call(3, "call_sfeld", "D3 15:20", "c_sfeld", "Opposing counsel's paralegal follows up by phone on Nathan's e-mail, before seeing Priya's reply.", [
 ("caller", "Hi Renee, it's Stacy at Corbin & Lisle. Nathan asked me to call. Can you just put whatever's Bates-stamped up on ShareFile today? Even a partial set helps us prep Lindqvist.", 20),
 ("human", "Hi Stacy. I can't release anything before Priya signs off. Priya just e-mailed Nathan: the responses, the production and the privilege log all go out together on Friday.", None),
 ("caller", "Okay. Can you at least tell me roughly how many pages so I can plan the load?", 15),
 ("human", "Once it's final I'll put the exact range and page count in the cover letter on Friday. I'd rather not give you a number today that changes.", None),
 ("caller", "Fair enough. And for the 19th, Nathan may be remote. Will there be a Zoom link?", 15),
 ("human", "Yes. We're booking the reporter with video and a remote link, and I'll send the link to you, Nathan and Kara the Monday before.", None),
 ("caller", "Perfect, thanks Renee.", 10),
 ("human", "Thanks, Stacy. Talk Friday.", None)])
