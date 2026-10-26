act(2, "a2_01", "D2 09:00", "reply", "itm_sfeld_vol2", f"""
To: Stacy Feld
Subject: RE: Prairie Hollow v. Kessling - Plaintiff's Production Volume 2 (PHGC000612-PHGC001488)

Thanks, Stacy - received. We'll let you know if anything doesn't load.

{SIG_RK}
""", "Courtesy acknowledgment.")
act(2, "a2_02", "D2 09:15", "forward", "itm_sfeld_vol2", """
To: Tom Nguyen
Subject: FW: Plaintiff's Production Volume 2 (PHGC000612-PHGC001488)

Tom - please download and load PHGC Vol. 2 to the Kessling workspace (password is in Stacy's separate e-mail, which I'm forwarding next). Usual QC: page count should be 877.
""", "Routine processing request.")
act(2, "a2_03", "D2 10:00", "read", "itm_corbin_dates", "Read Nathan's e-mail offering Nov 17, Nov 19 or Dec 1 for Lindqvist.", "Does not reply until 15:00, after checking calendars.")
act(2, "a2_04", "D2 11:02", "send", None, f"""
To: Alana Brooks (conflicts@ostranderhale.com)
Subject: New conflict search - prospective client Lorraine Dubek / Dubek's Bakery

Alana,

Please run a conflict search before any consultation is scheduled:
- Prospective client: Lorraine Dubek, individually and as owner of Dubek's Bakery (sole proprietorship), 2650 W. Belmont Ave., Chicago, IL 60618.
- Adverse party: Northfield Roofing & Sheet Metal Co. (roofing contractor; installed the bakery roof in May 2024).
- Other: building owner is Ms. Dubek's LLC, 2650 Belmont LLC.
- Nature: possible construction defect / warranty dispute over a commercial roof. Requesting attorney: Daniel Achterberg.

She called the main line this morning; I took only names and the general nature of the dispute and told her an attorney would contact her after the conflict check. She mentioned a possible time-limit concern (roof installed May 2024), so Daniel should hear about this promptly once the search is back.

{SIG_RK}
""", "Reference for N11: conflicts first, no advice, flags the limitations concern for the attorney.")
act(2, "a2_05", "D2 11:40", "read", "itm_nef_minute", "Opened the NEF for Dkt. 48 (status hearing 11/18, joint status report due 11/13). Saved to iManage.", "Docketing request comes at 15:20 (late).")
act(2, "a2_06", "D2 12:15", "read", "itm_marcus_cite", "Opened Marcus's motion and exhibit index; saved to the Midway workspace.", "Cite-check done Wednesday afternoon.")
act(2, "a2_07", "D2 12:45", "reply", "itm_gloria_d2", "Yes please, turkey for me - thanks! Feel better tomorrow.", "Chat.")
act(2, "a2_08", "D2 13:45", "send", None, f"""
To: Priya Raman
Cc: Daniel Achterberg
Subject: Kessling - Rick called with questions you need to answer (today please)

Priya,

Rick called at 1:30. Two questions I told him I can't answer and that you would call him today:
1. Whether Kessling has to produce the 2024 field-tech PM logs for Prairie Hollow's sites (he called them "embarrassing" and said some visits were never logged).
2. Whether he can "clean up" old text messages among the field techs (Paul Varela, Andre Whitlock, Dennis Okon) on their company phones.

I told him not to delete or change anything, that the hold notice you sent in May still applies, and that you'd call. He's at his desk until 5 (815.555.0120). Note Plaintiff's Second RFPs (served 10/30) ask for exactly these: No. 19 (PM records) and No. 20 (field-tech text messages).

{SIG_RK}
""", "Reference for N09: escalation with the preservation point and the link to RFP 19-20.")
act(2, "a2_09", "D2 14:10", "send", None, f"""
To: Docketing (Sharon Wiley)
Cc: Priya Raman
Subject: Docketing request - 10442-003 Kessling - response to Plaintiff's Second RFPs

Sharon,

Please enter:
Matter: 10442-003 Prairie Hollow v. Kessling, No. 1:26-cv-03182 (N.D. Ill.)
Event: Plaintiff's Second Set of Requests for Production (Nos. 19-27), served by U.S. Mail on Friday 10/30/2026 (certificate of service; received 11/2). Corbin's 11/2 e-mail was a courtesy copy only.
Deadline: Defendant's responses due THURSDAY, DECEMBER 3, 2026.
Computation: FRCP 34(b)(2)(A) 30 days; FRCP 6(a)(1): day 30 = Sunday 11/29/2026, so the period runs to Monday 11/30/2026; FRCP 6(d) adds 3 days for mail service after the period would otherwise expire = Thursday 12/3/2026. (Note: 10/30 + 33 calendar days would give 12/2, which is not the rule's method.)
Reminders: 11/19 and 11/30. Responsible attorney: P. Raman.

{SIG_RK}
""", "Reference for N01 (late: discoverable Monday 10:40).")
act(2, "a2_10", "D2 14:40", "forward", "itm_conflicts_result", """
To: Daniel Achterberg
Cc: Ellen Sato
Subject: FW: Conflict search results - prospective client Lorraine Dubek / Dubek's Bakery (Search #26-4471)

Daniel, Ellen - conflicts flagged Northfield Roofing as a current client (20871-001). I have not scheduled anything with Ms. Dubek and won't contact her further. She mentioned the roof went on in May 2024, so if we decline she may need to hear that promptly. How would you like to handle the call back?
""", "Routes the decision to the attorneys (who decline themselves).")
act(2, "a2_11", "D2 15:00", "reply", "itm_corbin_dates", f"""
To: Nathan Corbin
Cc: Priya Raman; Daniel Achterberg; Stacy Feld; Kara Bensen
Subject: RE: Prairie Hollow v. Kessling - Lindqvist deposition dates

Nathan,

Thank you. Thursday, November 19 at 9:30 a.m. works for us, at our offices (180 N. Canal Street, Suite 2200). We will serve a notice this week and arrange a court reporter and videographer. Please confirm.

{SIG_RK}
""", "Reference for N07: Nov 17 conflicts with Daniel's DuPage hearing; Dec 1 falls in Priya's out-of-office.")
act(2, "a2_12", "D2 15:20", "send", None, f"""
To: Docketing (Sharon Wiley)
Cc: Priya Raman; Daniel Achterberg
Subject: Docketing request - 10442-003 Kessling - Dkt. 48

Sharon, please enter from Dkt. 48 (Magistrate Judge Talbot, entered 11/3/2026):
1. Joint written status report due FRIDAY 11/13/2026 (status of written discovery; depositions taken and scheduled; disputes and LR 37.2 efforts). Reminder 11/10.
2. Telephonic status hearing WEDNESDAY 11/18/2026 at 9:30 a.m. (call-in on the Court's web page). Attorneys: D. Achterberg, P. Raman.

{SIG_RK}
""", "Reference for N08 (late).")
act(2, "a2_13", "D2 16:10", "schedule", "itm_priya_mc_fwd", """
Calendar invite sent (Teams with dial-in) - Organizer: Renee Kowalczyk on behalf of Priya Raman
Title: Prairie Hollow v. Kessling - LR 37.2 meet and confer (search terms, custodians)
When: Monday, November 9, 2026, 2:30-3:00 p.m. Central
Attendees: Priya Raman; Nathan Corbin; Stacy Feld (optional)
Body: Telephone conference under Local Rule 37.2 regarding Plaintiff's 11/3/2026 letter on custodians and search terms. Teams link and dial-in 312.555.0100, code 771205.
""", "Reference for N10 (late). Invite body mentions only the letter, nothing internal.")
act(2, "a2_14", "D2 17:00", "edit_doc", "itm_timesheet", """
Tue 11/3 (10442-003): 0.3 Review Plaintiff's deposition date proposals; check attorney calendars; correspond with N. Corbin re Lindqvist deposition date. | 0.3 Prepare summary of client questions for P. Raman. | 0.2 Review Dkt. 48 minute order.
(11870-002): 0.2 Review draft motion for leave and exhibit index for cite-check.
""", "Daily time; the docketing requests are left off (calendaring is non-billable under Kessling's guidelines, section 5).")

call(2, "call_dubek", "D2 10:15", "c_dubek", "Prospective client calls the main line, transferred to Renee because the receptionist heard 'construction lawsuit'.", [
 ("caller", "Hi, this is Lorraine Dubek, I own Dubek's Bakery on Belmont. My roof has been leaking since spring and the roofer, Northfield Roofing, says it's not their problem. A friend said your firm does construction cases. Do I have a case?", 20),
 ("human", "Thanks for calling, Ms. Dubek. I'm Renee Kowalczyk, a paralegal here, not an attorney, so I can't tell you whether you have a case. What I can do is get the information our attorneys need to check for conflicts first. Can I get the full names of you, your business and the roofing company?", None),
 ("caller", "Sure. Lorraine Dubek, Dubek's Bakery, it's just me, and the building's in my LLC, 2650 Belmont LLC. The roofer is Northfield Roofing and Sheet Metal. They put the roof on in May 2024. I heard there's a two-year deadline on these things. Am I already too late?", 20),
 ("human", "I'm not able to advise you on deadlines, and I don't want to guess about something that important. I'll make a note that you're concerned about timing so the attorney sees it right away. Before we go further, please don't send me any documents or details yet; once our conflict check clears, an attorney will call you. What's the best number?", None),
 ("caller", "773-555-0112. Can't you at least tell me if two years is right? I just need to know if I should panic.", 15),
 ("human", "I understand. I really can't answer that one, but I'll get this to an attorney today so you hear back quickly. If you haven't heard from us by tomorrow afternoon, please call me back at 312-555-0148.", None),
 ("caller", "Okay. Thank you, Renee.", 10),
 ("human", "You're welcome. Talk soon.", None)])
call(2, "call_rick", "D2 13:30", "c_rick", "Client calls Renee directly while Priya is in a meeting.", [
 ("caller", "Renee, it's Rick. Quick question before Friday. Those 2024 PM logs from the field guys - honestly they're embarrassing, half the visits never got written up. Do we have to hand those over? They're not really 'service tickets.'", 20),
 ("human", "Rick, that's a question for Priya, and I can't give you legal advice on what has to be produced. I'll get her to call you this afternoon.", None),
 ("caller", "Okay. And the other thing - the guys have years of texts on their company phones, a lot of it is just joking around. Can I tell them to clean that up? It's a mess.", 15),
 ("human", "Please don't delete or change anything, and don't ask the guys to either. Priya's hold notice from May still applies to phones and texts. She'll call you today and walk through it with you.", None),
 ("caller", "Got it. Nobody touches anything. Have her call me, I'm here till five.", 10),
 ("human", "Will do. I'm sending her a note right now.", None)])
