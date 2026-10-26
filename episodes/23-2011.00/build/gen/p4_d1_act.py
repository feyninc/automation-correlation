DAYS = [{"date": "2026-11-02", "actions": [], "calls": []}, {"date": "2026-11-03", "actions": [], "calls": []},
        {"date": "2026-11-04", "actions": [], "calls": []}, {"date": "2026-11-05", "actions": [], "calls": []},
        {"date": "2026-11-06", "actions": [], "calls": []}]
def act(day, id, at, verb, target, content, note, visible=True):
    DAYS[day-1]["actions"].append({"id": id, "at": at, "verb": verb, "target": target, "content": content.strip("\n"),
                                   "visible_to_model": visible, "note": note})
def call(day, id, at, caller, purpose, turns):
    DAYS[day-1]["calls"].append({"id": id, "at": at, "caller": caller, "purpose": purpose,
        "turns": [{"speaker": s, "text": t, **({"patience_s": p} if p else {})} for s, t, p in turns]})

act(1, "a1_01", "D1 09:00", "read", "itm_priya_week", "Opened Priya's 'Kessling - this week' list.", "Sets the week's agenda.")
act(1, "a1_02", "D1 09:10", "read", "itm_daniel_subpoena", "Opened Daniel's e-mail and the signed Varga subpoena.", "Notes the subpoena must be served this week; does not yet think about the Rule 45(a)(4) prior notice.")
act(1, "a1_03", "D1 09:25", "reply", "itm_priya_week", f"""
To: Priya Raman
Subject: RE: Kessling - this week (responses due Fri 11/6)

Got it. Plan:
- Clean drafts of the rog answers and RFP responses to you by Wednesday 5 pm. Rick sent answers on 6, 7, 11 and 14 last night; folding them in today.
- Tom stages Vol. 2 Wednesday; nothing goes to Corbin until you sign off on priv QC.
- Priv log from Tom's export (Tuesday), with the para. 9(c) post-4/14 carve-out.
- I'll get Nathan's dates for Lindqvist and draft the notice as soon as we have a date.

{SIG_RK}
""", "Ordinary acknowledgment; reference for a plan-of-week reply.")
act(1, "a1_04", "D1 09:40", "read", "itm_docket_report", "Reviewed the weekly deadline report; confirmed 11/6 entries for the first rogs and RFPs.", "Background docket check.")
act(1, "a1_05", "D1 10:20", "edit_doc", "itm_rogs_draft", """
DRAFT v5 changes:
- No. 6 ANSWER: Kessling's engineering group performed teardown inspections on July 29, 2025 of the two pumps removed from Plaintiff's Field 12 site under RMA-25-0077 (serials KX40-24-0528 and KX40-24-0530). The results are recorded in Teardown Reports TR-25-031 and TR-25-032, which Kessling will produce, and which Kessling refers to under Rule 33(d).
- No. 7 ANSWER (subject to the objection): Hollins Farms (Iowa; two pumps; 2024); Wabash Valley Ag Services (Indiana; one pump; 2025); Tri-County Sod (Illinois; one pump; 2023).
- No. 11 ANSWER: The teardown reports for KX40-24-0528 and -0530 record heat-checked seal faces and a cracked carbon face consistent with dry running; the controller log reviewed on ticket FS-25-0590 recorded 41 hours of operation against a closed discharge valve; on ticket FS-25-0412 the seal-flush line was found closed. Plaintiff's personnel operated the pumps. Discovery continues.
- No. 14 ANSWER: Rick Szymanski (telephone calls with Walt Herrmann, Plaintiff's general manager, in August and September 2025, concerning warranty claims); Brett Nowak (site visit with Dale Lindqvist, June 2025); Dennis Okon (e-mails with Dale Lindqvist, June-August 2025, concerning service visits); Paul Varela and Andre Whitlock (on-site communications during service visits listed on the field service tickets).
""", "The human does much of the drafting; reference for document edits.")
act(1, "a1_06", "D1 10:50", "read", "itm_mail_rfp2", "Opened the scanned Second RFPs; saved to iManage 10442-003 as 'Pl 2d RFP (Nos 19-27) served by mail 10-30-26'. Did not send a docketing request yet.", "The docketing need (N01) stays open until Tuesday afternoon.")
act(1, "a1_07", "D1 11:30", "read", "itm_nef_appearance", "Opened the NEF for Dkt. 47; downloaded the free copy of the appearance to iManage.", "Does not update the service list now; Kara is added when the deposition notice is served Thursday.")
act(1, "a1_08", "D1 12:00", "reply", "itm_gloria_d1", "No date yet - I'm asking Nathan Corbin this week. I'll tell you as soon as it's confirmed so you can put the hold on Daniel's calendar.", "Chat reply.")
act(1, "a1_09", "D1 13:40", "edit_doc", "itm_rfp_draft", """
DRAFT v4 changes:
- RFP 5: add "including Teardown Reports TR-25-031 and TR-25-032 and associated photographs."
- RFP 11: add "Kessling has located no separate 2024 preventative-maintenance visit records for Plaintiff's sites beyond the field service tickets; its search continues and it will supplement under Rule 26(e)." (flagged for Priya: confirm with Rick before service)
- RFP 18: add "Kessling's communications with its insurer, Great Lakes Mutual Casualty Co., made through litigation counsel on or after April 14, 2026, are withheld and are not logged under ESI Stipulation para. 9(c)." (flagged for Priya: Rick says there were no direct client-insurer e-mails about the claim)
""", "Human drafting; note RFP 11 wording ties to the sensitive PM-log issue.")
act(1, "a1_10", "D1 14:30", "forward", "itm_daniel_subpoena", f"""
To: Ray Duda (Northline Process Service)
Subject: Service request - Varga Electric Motors (Kessling)

Ray,

Please serve the attached subpoena to produce documents (N.D. Ill. No. 1:26-cv-03182) on Varga Electric Motors, Inc., through its registered agent, Badger State Registered Agents, Inc., 777 E. Wisconsin Avenue, Suite 1400, Milwaukee, WI 53202, this week. Personal delivery to the agent, please, with an affidavit of service stating date, time and the name of the person served. Please confirm the service time before you go out. Bill to Ostrander Hale, matter 10442-003.

Thanks,
{SIG_RK}
""", "Reference for N04: forwards the signed subpoena to the process server; Northline acknowledges at 15:40.")
act(1, "a1_11", "D1 15:10", "reply", "itm_priya_chat_d1", "Sent - Rick's 11/1 email and the 10/20 KX-40 invoice summary (46 units on three invoices) are in your inbox.", "Chat reply plus forward.")
act(1, "a1_12", "D1 16:20", "reply", "itm_rick_travel", f"""
To: Rick Szymanski
Subject: RE: travel this week

Thanks, Rick - that's helpful. Your answers on 6, 7, 11 and 14 are in the draft. Priya will review Wednesday; I'll send you the final answers and the verification page Thursday morning by DocuSign so you can sign from the show.

{SIG_RK}
""", "Commits to Thursday verification; reference context for N05.")
act(1, "a1_13", "D1 17:00", "edit_doc", "itm_timesheet", """
Mon 11/2 (10442-003): 0.2 Review P. Raman instructions re discovery responses due 11/6. | 1.4 Revise answers to Interrogatory Nos. 6, 7, 11 and 14 based on client information. | 0.9 Revise responses to Requests for Production Nos. 5, 11 and 18. | 0.3 Correspond with process server re service of subpoena on Varga Electric Motors.
""", "Daily time; clerical items (calendaring, filing NEF) left off per guidelines.")
