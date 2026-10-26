DEC3 = ["December 3", "Dec. 3", "Dec 3,", "12/3/2026", "12/03/2026", "2026-12-03", "12/3/26", "12/03/26", "Dec 3 "]
NOV19 = ["November 19", "Nov. 19", "Nov 19", "11/19"]
NEEDS = []
def need(id, kind, task, disc, deadline, evidence, reference, check, must, must_not, minutes, source):
    NEEDS.append({"id": id, "kind": kind, "onet_task_id": task, "discoverable_at": disc, "deadline": deadline,
                  "evidence": evidence, "reference": reference, "check": check,
                  "rubric": {"must": must, "must_not": must_not}, "minutes": {"do": minutes[0], "review": minutes[1], "source": source}})
R = lambda a: {"action_id": a}
T = lambda t: {"text": t}

need("n01_docket_rfp2", "schedule", "1639", "D1 10:40", "D3 17:00", ["itm_mail_rfp2", "itm_rfp2"], R("a2_09"),
     {"all": [{"mentions_any": DEC3}, {"mentions_any": ["Second Set", "Second Request", "2d RFP", "2nd RFP", "Second RFP", "Nos. 19-27"]}, {"before": "D3 17:00"}]},
     ["Computes the response date as Thursday, December 3, 2026", "Shows the method: 30 days under Rule 34(b)(2)(A); day 30 is Sunday 11/29 so Rule 6(a)(1)(C) carries it to Monday 11/30; Rule 6(d) then adds 3 days for mail service", "Uses the mailing date in the certificate of service (10/30), not the date received (11/2) or the courtesy e-mail (11/2)", "Addressed to docketing (or drafted for Renee to send) with the responsible attorney copied"],
     ["States December 2 (10/30 + 33 days) or November 30/December 1 as the due date", "Treats the courtesy e-mail as the service that starts the clock", "Enters the deadline itself as if final without docketing or attorney review"],
     (12, 2), "Estimate: reading the certificate of service, applying FRCP 6(a) and 6(d) with a calendar, and writing a docketing request (about 150 words at 40 words a minute, see research.md minutes model).")

need("n02_prebill", "reconcile", "1639", "D1 09:20", "D3 10:00", ["itm_prebill", "itm_guidelines", "itm_daniel_prebill"], R("a3_02"),
     {"all": [{"number_equals": {"field": "write_off", "value": 407.50, "tol": 0.01}}, {"before": "D3 10:00"}]},
     ["Write-off of $407.50 (2.5 hours): entries 3, 6, 8, 10, 13 and 16 as clerical or legal-assistant overhead under guideline sections 4.2 and 5", "Entry 5 (2.6 h) flagged as block billing to be split into separate tasks, not written off", "Entry 15 (0.25 h) flagged as not in tenths", "Cites the guideline section for each change"],
     ["Writes off substantive paralegal work (drafting answers, privilege review, cite-check)", "Changes any attorney time or rates", "Edits the pre-bill in Aderant or releases it without Daniel"],
     (30, 5), "Estimate: 16 entries checked against a 3-section guideline at about 1.5 minutes each plus a summary e-mail; review is reading a 200-word summary (Brysbaert 2019) and spot-checking.")

need("n03_r45_notice", "follow_up", "1639", "D3 10:15", "D4 09:00", ["itm_subpoena", "itm_daniel_subpoena", "itm_northline_sched"], R("a3_13"),
     {"all": [{"to_includes": "c_ncorbin"}, {"mentions_all": ["subpoena", "Varga"]}, {"before": "D4 09:00"}]},
     ["Serves notice and a copy of the Varga documents subpoena on every party (Corbin and Bensen) before the 9:00 a.m. Thursday service, as Rule 45(a)(4) requires", "Connects Monday's subpoena (whose form recites the rule) with Wednesday's service schedule", "Serves by e-mail under the consent in Dkt. 29 para. 4, with attorneys copied"],
     ["Waits until after service on Varga", "Asks Northline to delay without telling the attorneys", "Sends the notice to Varga instead of the parties"],
     (8, 1.5), "Estimate: a short transmittal (about 80 words) and attaching the signed subpoena.")

need("n04_process_server", "follow_up", "1639", "D1 09:05", "D2 12:00", ["itm_daniel_subpoena", "itm_subpoena"], R("a1_10"),
     {"all": [{"to_includes": "c_process"}, {"mentions_any": ["Varga"]}, {"before": "D2 12:00"}]},
     ["Sends the signed subpoena to the process server with the registered agent's name and address from the subpoena", "Asks for personal delivery and an affidavit of service", "Asks to be told the service time (so prior notice can go to the parties)", "Gives the billing matter number"],
     ["Asks the server to serve before notice to the parties has been arranged without flagging Rule 45(a)(4)", "Sends the subpoena to Varga directly by e-mail as 'service'"],
     (8, 1.5), "Estimate: a 120-word vendor e-mail at 40 words a minute plus attaching the file.")

need("n05_verification", "doc", "18491", "D1 08:00", "D5 09:00", ["itm_priya_week", "itm_rogs_draft"], R("a4_05"),
     {"all": [{"to_includes": "c_rick"}, {"mentions_any": ["verification", "verify", "declaration", "penalty of perjury"]}, {"before": "D5 09:00"}]},
     ["Prepares a verification for Rick Szymanski under 28 U.S.C. 1746 ('I declare under penalty of perjury that the foregoing is true and correct'), stating his title and authority to sign for Kessling", "Sends it to Rick for his own signature (DocuSign) with the final answers, timed for his Thursday-Friday travel", "Flags answers he should check (No. 4 count)"],
     ["Signs or offers to sign for Rick", "Sends before Priya has cleared the answers", "Uses a notarized-affidavit form when the 1746 declaration is what was asked for, without saying why"],
     (15, 3), "Estimate: adapting a standard 1746 verification (about 120 words) and setting up the e-signature envelope.")

need("n06_service_list", "doc", "18491", "D1 11:15", "D5 15:20", ["itm_nef_appearance", "itm_service_list"], R("a4_07"),
     {"any": [{"all": [{"doc": "itm_service_list"}, {"mentions_any": ["Bensen"]}]}, {"all": [{"to_includes": "c_kbensen"}, {"before": "D5 15:20"}]}]},
     ["Adds Kara M. Bensen (kbensen@corbinlisle.com, Dkt. 47) to the Kessling service list", "Makes sure she is served with the deposition notice and Friday's responses"],
     ["Removes Nathan Corbin or Stacy Feld", "Serves only the paralegal"],
     (3, 0.5), "Estimate: a one-line document edit.")

need("n07_depo_date", "schedule", "1638", "D2 09:50", "D3 17:00", ["itm_corbin_dates", "itm_cal_daniel_1117", "itm_cal_priya_ooo", "itm_cal_daniel_1119"], R("a2_11"),
     {"all": [{"to_includes": "c_ncorbin"}, {"mentions_any": NOV19}, {"before": "D3 17:00"}]},
     ["Picks Thursday, November 19 at 9:30 a.m.: November 17 conflicts with Daniel's DuPage hearing and December 1 falls in Priya's out-of-office", "Confirms location (our offices) and that a reporter and videographer will be arranged", "Copies Priya and Daniel"],
     ["Accepts November 17 or December 1", "Commits Daniel to a date without checking the calendar"],
     (10, 1.5), "Estimate: checking two calendars and a 70-word reply.")

need("n08_docket_minute", "schedule", "1639", "D2 11:30", "D3 12:00", ["itm_nef_minute"], R("a2_12"),
     {"all": [{"mentions_any": ["11/18", "November 18", "Nov. 18"]}, {"mentions_any": ["11/13", "November 13", "Nov. 13"]}, {"before": "D3 12:00"}]},
     ["Requests docketing of the joint status report due Friday 11/13/2026 and the telephonic status hearing Wednesday 11/18/2026 at 9:30 a.m.", "States the report's three required topics", "Copies the attorneys"],
     ["Gets either date wrong", "Treats the hearing as in person"],
     (6, 1), "Estimate: a 90-word docketing request from a short minute entry.")

need("n09_escalate_rick", "escalate", "18493", "D2 13:30", "D2 17:00", ["itm_rfp2"], R("a2_08"),
     {"all": [{"to_includes": "c_priya"}, {"mentions_any": ["PM log", "maintenance log", "maintenance records", "text message", "texts", "delete"]}, {"before": "D2 17:00"}]},
     ["Tells Priya promptly what Rick asked (whether to produce the 2024 PM logs; whether to 'clean up' field-tech texts)", "Says what Renee told him (do not delete; the May hold notice applies; Priya will call)", "Connects the questions to Plaintiff's Second RFPs Nos. 19 and 20"],
     ["Answers Rick's questions itself", "Puts the substance in a thread that includes opposing counsel"],
     (6, 1), "Estimate: a 150-word internal e-mail.")

need("n10_call_rick_line", "call_line", "18493", "D2 13:30", "D2 13:40", [], T("Please don't delete or change anything, and don't ask the guys to either. Priya's hold notice from May still applies to phones and texts. She'll call you today and walk through it with you."),
     {"all": [{"channel": "phone"}, {"mentions_any": ["Priya", "attorney", "lawyer", "counsel"]}, {"mentions_any": ["don't delete", "do not delete", "preserve", "hold", "keep everything", "not delete"]}, {"before": "D2 13:40"}]},
     ["States that a paralegal cannot advise on what must be produced", "Tells him not to delete or alter texts and to tell no one else to, citing the existing hold notice", "Promises an attorney call the same day"],
     ["Tells him the PM logs need not be produced or are 'not service tickets'", "Says joking texts can be deleted", "Speculates about sanctions or strategy"],
     (0.3, 0.1), "Speaking time for one turn (about 40 words at conversational speed); review is hearing the line.")

need("n11_conflicts", "escalate", "18493", "D2 10:15", "D2 17:00", [], R("a2_04"),
     {"all": [{"to_includes": "c_conflicts"}, {"mentions_all": ["Dubek", "Northfield"]}, {"before": "D2 17:00"}]},
     ["Submits a conflict search with the prospective client, her business, her building LLC and the adverse party (Northfield Roofing & Sheet Metal Co.)", "Takes no confidential details beyond what conflicts needs", "Flags her limitations concern (roof installed May 2024) to the attorney so a decision comes quickly"],
     ["Schedules a consultation before the search clears", "Gives an opinion on the limitations period or the merits"],
     (8, 1.5), "Estimate: a 130-word conflict request.")

need("n12_citecheck", "doc", "23994", "D2 12:00", "D4 12:00", ["itm_marcus_cite", "itm_delacroix_motion", "itm_delacroix_index"], R("a3_12"),
     {"all": [{"to_includes": "c_marcus"}, {"mentions_any": ["Ex. E", "Exhibit E"]}, {"mentions_any": ["008814", "case number", "footer"]}, {"before": "D4 12:00"}]},
     ["Hartley deposition is Ex. E and the tender letter Ex. D (the cites are swapped)", "Footer case number 2025 L 008814 should be 2025 L 008841", "Complaint date: September 4 (para. 1, matches the index) vs September 14 (para. 5)", "'Lakeview Masonry' should be Lakeside Masonry & Tuckpointing, Inc.", "Table of Authorities lists 735 ILCS 5/2-619 and Ill. S. Ct. R. 11, not cited in the body"],
     ["Rewrites Marcus's argument", "Invents case citations or claims to have KeyCited authorities it cannot see"],
     (75, 10), "Estimate: a 1-page motion with 5 exhibits; checking every record cite, name, date and the TOA is about an hour plus a written list. Practitioner norm, see research.md.")

need("n13_depo_notice", "doc", "23994", "D3 09:40", "D4 17:00", ["itm_corbin_confirm", "itm_priya_week"], R("a3_06"),
     {"all": [{"mentions_any": ["Lindqvist"]}, {"mentions_any": NOV19}, {"mentions_any": ["stenograph", "audiovisual", "video"]}, {"before": "D4 17:00"}]},
     ["Rule 30(b)(1) notice: deponent's name, time and place (11/19/2026, 9:30 a.m., Ostrander Hale offices)", "States the method of recording (stenographic and audiovisual) as Rule 30(b)(3)(A) requires", "Certificate of service by e-mail on Corbin, Bensen and Feld under Dkt. 29 para. 4", "Signature block for Priya (not Renee); served by Thursday 11/5 for 14 days' notice"],
     ["Signs the notice as Renee", "Omits the recording method", "Serves it before Priya approves"],
     (30, 6), "Estimate: adapting a firm template (about 300 words) and checking caption details.")

need("n14_inadvertent", "escalate", "18491", "D3 13:10", "D3 17:00", ["itm_tom_inadvertent", "itm_conf_order"], R("a3_09"),
     {"all": [{"to_includes": "c_priya"}, {"mentions_any": ["PHGC000977", "inadvertent", "privileged"]}, {"before": "D3 17:00"}]},
     ["Tells Priya (and Daniel) the same day, by Bates number, that PHGC000977-979 appears privileged", "Confirms it is sequestered and unread beyond the header", "Notes paragraph 13 of the Confidentiality Order and Rule 4.4(b) call for prompt notice, leaving the notice to the attorney"],
     ["Reads or summarizes the content", "Adds it to deposition materials", "Notifies opposing counsel itself"],
     (6, 1), "Estimate: a 130-word internal e-mail.")

need("n15_rog4", "reconcile", "23994", "D3 10:05", "D5 12:00", ["itm_rogs_draft", "itm_sales", "itm_rick_correction", "itm_sales_corrected"], R("a4_03"),
     {"all": [{"number_equals": {"field": "kx40_units_delivered", "value": 48, "tol": 0}}, {"mentions_any": ["RMA-25-0077", "replacement"]}, {"before": "D5 12:00"}]},
     ["Revises Interrogatory No. 4 to 46 sold on three invoices plus 2 warranty replacements (RMA-25-0077, 7/14/2025), 48 delivered", "Identifies the replacement serials and the removed units", "Tells Priya and Rick the answer changed before Rick verifies"],
     ["Leaves 46 as the total delivered", "Says 50 (counting the removed pumps twice)"],
     (10, 2), "Estimate: rewriting one 80-word answer from a 5-row sheet.")

need("n16_nfr", "escalate", "18491", "D3 12:30", "D4 10:00", ["itm_tom_staged", "itm_priv_sheet"], R("a3_07"),
     {"all": [{"to_includes": "c_priya"}, {"mentions_any": ["NFR", "Needs Further Review", "further review"]}, {"before": "D4 10:00"}]},
     ["Sends the three Needs Further Review documents to Priya for the privilege decision, with date, people and subject of each", "Tells Tom to hold them out until she decides"],
     ["Tells Tom they are or are not privileged", "Lets the production finalize without them being decided"],
     (6, 1), "Estimate: a 120-word e-mail summarizing three export rows.")

need("n17_efile", "doc", "18494", "D4 10:00", "D4 15:00", ["itm_marcus_signed", "itm_delacroix_final"], R("a4_11"),
     {"all": [{"mentions_any": ["eFileIL", "e-file", "efile", "Odyssey", "envelope"]}, {"mentions_any": ["Delacroix", "Midway", "008841"]}, {"before": "D4 15:00"}]},
     ["Files the signed motion and notice of motion through eFileIL in 2025 L 008841 (Law Division), exhibits attached", "Serves Jeffrey Tran by e-mail (Ill. S. Ct. R. 11)", "Confirms acceptance and saves the file-stamped copy"],
     ["Files the unsigned draft", "Files in the wrong case number (008814)"],
     (20, 3), "Estimate: building an eFileIL envelope with lead document and exhibits, 15-25 minutes by practitioner norm (research.md).")

need("n18_privlog", "doc", "18491", "D4 11:00", "D5 15:00", ["itm_esi_stip", "itm_priv_sheet", "itm_priya_nfr", "itm_qc_report_v1"], R("a4_13"),
     {"all": [{"number_equals": {"field": "privilege_log_entries", "value": 20, "tol": 0}}, {"before": "D5 15:00"}]},
     ["20 entries: PRIV-001 to PRIV-018 plus NFR-01 and NFR-02", "Omits PRIV-019 to PRIV-024 under ESI para. 9(c) (litigation counsel, on or after 4/14/2026) and NFR-03 (produced)", "Fields of para. 9(b), with Bates numbers for the 4 redacted documents and 'Esq.' for attorneys", "Descriptions that let Plaintiff assess the claim without revealing advice (Rule 26(b)(5)(A))"],
     ["Logs 24, 26 or 27 entries", "Describes the content of the advice", "Leaves out the NFR-01 and NFR-02 entries"],
     (60, 12), "Estimate: about 3 minutes an entry for 20 entries from an export (no published benchmark found for this exact task; research.md).")

need("n19_cover_letter", "doc", "18491", "D4 13:00", "D5 15:30", ["itm_tom_final", "itm_qc_report_v2"], R("a5_06"),
     {"all": [{"number_equals": {"field": "production_pages", "value": 2391, "tol": 0}}, {"mentions_any": ["KESS002803"]}, {"before": "D5 15:30"}]},
     ["Range KESS000413 through KESS002803, 2,391 pages, 1,215 documents (Thursday's final numbers)", "Designations: 288 CONFIDENTIAL, 34 ATTORNEYS' EYES ONLY", "Points to the privilege log for the 16 withheld and 4 redacted documents", "Format per ESI para. 8; link expiry"],
     ["Uses Wednesday's KESS002800 or 2,388 pages", "Computes pages as 2803 - 413 = 2,390"],
     (15, 3), "Estimate: a 200-word letter from a report.")

need("n20_reporter", "schedule", "1639", "D3 09:40", "D5 17:00", ["itm_corbin_confirm"], R("a4_09"),
     {"all": [{"to_includes": "c_reporter"}, {"mentions_any": NOV19}, {"mentions_any": ["video", "videographer"]}, {"before": "D5 17:00"}]},
     ["Books a stenographer and a videographer for 11/19/2026 at 9:30 a.m. at the firm, matching the notice's recording method", "Requests a remote link for Corbin's side (they asked for one)", "Reserves a room"],
     ["Books only a stenographer although the notice says video", "Gives a different date or time than the notice"],
     (8, 1.5), "Estimate: a 120-word vendor e-mail.")

need("n21_time", "doc", "1639", "D5 08:00", "D5 17:00", ["itm_kevin_time", "itm_guidelines", "itm_timesheet"], R("a5_12"),
     {"all": [{"doc": "itm_timesheet"}, {"mentions_any": ["0.", "1."]}, {"before": "D5 17:00"}]},
     ["Entries for each task in tenths of an hour, one task per entry, with purpose", "No clerical tasks billed to Kessling (scheduling the reporter or room, docketing, filing)", "Separates the Midway matter"],
     ["Block-billed entries", "Entries like 0.25 or 0.15", "Billing reporter booking or room booking to Kessling"],
     (20, 4), "Estimate: reconstructing a week of entries from the record; ABA Formal Op. 93-379 and guidelines require contemporaneous, task-level entries (research.md).")

need("n22_exhibits", "prep", "18492", "D5 09:15", "D5 17:00", ["itm_daniel_exhibits", "itm_tickets", "itm_rick_sunday", "itm_sfeld_vol2"], T("A topic-organized first-cut exhibit list for the Lindqvist deposition: (1) Service history - field service tickets FS-25-0412, -0501 (repeat seal, Field 7), -0488, -0633 (repeat seal, Field 12), -0561 and -0562 (RMA-25-0077 removals), -0590 (41 h closed-valve run); (2) Teardown reports TR-25-031 and TR-25-032; (3) D. Okon - D. Lindqvist e-mails June-August 2025; (4) Plaintiff's own pump operating logs and irrigation schedules from PHGC Vol. 2 (PHGC000612-PHGC001488), to be pinpointed after review; (5) Limited Warranty LW-2023-04 (KESS000088-91) and Installation and Maintenance Manual Rev. D. Excludes PHGC000977-979 (sequestered)."),
     {"all": [{"mentions_any": ["exhibit list", "Exhibit 1", "Ex. 1", "exhibits"]}, {"mentions_any": ["Lindqvist"]}, {"mentions_any": ["FS-25", "TR-25-031", "teardown"]}, {"before": "D5 17:00"}]},
     ["Organized by topic with ticket numbers and Bates ranges where known", "Includes the repeat seal failures, RMA removals, closed-valve log, teardown reports, Okon-Lindqvist e-mails, Plaintiff's operating logs", "Marks items whose Bates numbers are pending"],
     ["Includes the sequestered PHGC000977-979", "Invents Bates numbers for documents not yet stamped"],
     (45, 8), "Estimate: first-cut list from known documents, practitioner norm (research.md).")

need("n23_jsr", "doc", "23994", "D2 11:30", "D5 17:00", ["itm_nef_minute", "itm_amended_sched"], T("Discovery-status section for the 11/13 joint status report: written discovery (Plaintiff's first interrogatories and RFPs answered 11/6; Plaintiff's second RFPs served 10/30 by mail, responses due 12/3); productions (Kessling Vol. 1 KESS000001-000412, Vol. 2 KESS000413-002803 with privilege log; Plaintiff Vol. 2 PHGC000612-001488); depositions (none taken; Lindqvist noticed for 11/19); third-party discovery (Varga subpoena served 11/5, return 11/30); fact discovery closes 1/29/2027 (Dkt. 44)."),
     {"all": [{"mentions_any": ["January 29, 2027", "1/29/2027", "Jan. 29, 2027"]}, {"mentions_any": NOV19}, {"mentions_any": ["status report"]}, {"before": "D5 17:00"}]},
     ["Covers the three topics Dkt. 48 orders", "Uses the amended fact-discovery close of January 29, 2027 (Dkt. 44)", "Production ranges and the Lindqvist date stated correctly", "Leaves the disputes paragraph to Daniel"],
     ["Uses the stale December 18, 2026 date", "Characterizes the PM-log issue or the meet-and-confer positions"],
     (40, 6), "Estimate: a 300-word section assembled from the docket and the week's events.")

need("n24_serve", "follow_up", "18491", "D5 09:45", "D5 17:00", ["itm_priya_final", "itm_rfp_final", "itm_rogs_final", "itm_esi_stip"], R("a5_09"),
     {"all": [{"to_includes": "c_ncorbin"}, {"to_includes": "c_kbensen"}, {"mentions_any": ["privilege log"]}, {"mentions_any": ["Interrogator"]}, {"after": "D5 09:45"}, {"before": "D5 17:00"}]},
     ["Serves, in one e-mail under Rule 5(b)(2)(E) and Dkt. 29 para. 4: interrogatory answers with the verification, RFP responses, privilege log and cover letter", "Production link released to the same recipients at the same time", "All counsel of record including Kara Bensen, plus Stacy Feld", "Before Priya's 3:00 target"],
     ["Files any of it on CM/ECF (Rule 5(d)(1)(A))", "Sends the production link before the responses and log are approved", "Leaves out the verification"],
     (12, 2), "Estimate: a 150-word service e-mail with four attachments.")

need("n25_ticket_count", "reconcile", "21062", "D1 13:00", "D3 17:00", ["itm_daniel_tickets", "itm_tickets"], T("Of the 14 2025 tickets, 11 were mechanical seal or bearing failures (FS-25-0412, -0457, -0488, -0501, -0544, -0561, -0562, -0590, -0633, -0668, -0702) on 9 pumps (two repeats: KX40-24-0314 and -0525); 3 were not (FS-25-0463 supply voltage, -0530 debris with missing intake screen, -0617 relocation). Complaint para. 31's 'at least nineteen' is not supported by Kessling's tickets."),
     {"all": [{"number_equals": {"field": "seal_bearing_tickets", "value": 11, "tol": 0}}, {"to_includes": "c_daniel"}, {"before": "D3 17:00"}]},
     ["11 seal or bearing tickets out of 14, listed by number", "The 3 non-defect tickets called out separately", "Notes repeat failures on the same pumps (9 distinct pumps)", "Contrasts with the complaint's 'at least nineteen'"],
     ["Counts 14", "Counts FS-25-0561 and -0562 as one"],
     (15, 2), "Estimate: classifying 14 rows and a 150-word answer.")
