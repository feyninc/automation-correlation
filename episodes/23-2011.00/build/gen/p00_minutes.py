MINUTES_MODEL = {
 "basis": {"reading_wpm": 238, "reading_source": "Brysbaert (2019), J. Memory and Language 109:104047, silent reading of non-fiction", "composing_wpm": 40, "composing_source": "estimate: mean typing speed 51.56 wpm (Dhakal et al., CHI 2018, https://userinterfaces.aalto.fi/136Mkeystrokes/resources/chi-18-analysis.pdf) slowed by composing and checking legal text; see research.md", "document_review_per_hour": "31-100 documents (RAND MG-1208, Pace and Zakaras 2012, https://www.rand.org/content/dam/rand/pubs/monographs/2012/RAND_MG1208.pdf)"},
 "per_proposal": {
   "reply_short": {"do_minutes": 4, "review_minutes": 1, "why": "60-100 words composed; reading the proposal and its source e-mail"},
   "email_substantive": {"do_minutes": 10, "review_minutes": 2, "why": "120-200 words plus looking up facts in 1-3 items"},
   "docketing_request": {"do_minutes": 12, "review_minutes": 2, "why": "rule lookup and calendar count, plus a request; review re-counts the dates"},
   "schedule": {"do_minutes": 8, "review_minutes": 1.5, "why": "checking calendars and sending an invite or vendor request"},
   "doc_short": {"do_minutes": 30, "review_minutes": 6, "why": "1-2 page document from a template (notice, cover letter, verification)"},
   "doc_long": {"do_minutes": 60, "review_minutes": 12, "why": "multi-entry document (privilege log of 20 entries; exhibit list)"},
   "cite_check": {"do_minutes": 75, "review_minutes": 10, "why": "every cite, name, date and exhibit reference checked in a short motion"},
   "reconcile_sheet": {"do_minutes": 30, "review_minutes": 5, "why": "16-entry pre-bill against guidelines; review spot-checks the arithmetic"},
   "time_entries": {"do_minutes": 20, "review_minutes": 4, "why": "a week's entries reconstructed from the record"},
   "call_line": {"do_minutes": 0.3, "review_minutes": 0.1, "why": "one spoken turn; value is the content, not the time"}},
 "occupation_overrides_source": "research.md, 'Minutes model'"
}
EXTRA_SOURCES = [
 {"what": "N.D. Ill. press release: fake Notices of Electronic Filing target attorneys (Nov. 7, 2024)", "url": "https://www.ilnd.uscourts.gov/_assets/_news/ECF%20scam.pdf"},
 {"what": "U.S. Courts public alert on scam e-mails about phony court cases (2014)", "url": "https://web.archive.org/web/20161208003413/http://www.uscourts.gov/news/2014/01/13/public-alert-scam-emails-about-phony-court-cases-carry-computer-virus"},
 {"what": "N.D. Ill. General Order 16-0020 on Electronic Case Filing (login use, signature)", "url": "https://www.ilnd.uscourts.gov/_assets/_documents/_forms/_clerksoffice/rules/admin/pdf-orders/General_Order_16-0020.pdf"},
 {"what": "N.D. Ill. Model Confidentiality Order, Form LR 26.2", "url": "https://www.ilnd.uscourts.gov/_assets/_documents/_forms/_online//Model%20Confidentiality%20Order%20-%20LR%2026.2.pdf"},
 {"what": "Ill. S. Ct. Rule 9 (mandatory e-filing in civil cases)", "url": "https://ilcourtsaudio.blob.core.windows.net/antilles-resources/resources/10719c29-d129-41cc-b4c8-0027ca878a42/Rule%209.pdf"},
 {"what": "Ill. S. Ct. Rule 11 (electronic service)", "url": "https://ilcourtsaudio.blob.core.windows.net/antilles-resources/resources/3dd0a46c-817b-4f5a-992d-71eb62a92e0d/Rule%2011.pdf"},
 {"what": "Clerk of the Circuit Court of Cook County: e-filing mandatory since July 1, 2018 via eFileIL", "url": "https://www.cookcountyclerkofcourt.org/eFile"},
 {"what": "NALA 2020 Utilization and Compensation Survey (29 of 40 weekly hours billable; $149 average rate)", "url": "https://nala.org/wp-content/uploads/2023/02/NALA_2020_Utilization_and_Compensation_Survey.pdf"},
 {"what": "NALA 2024 Compensation and Utilization Report, executive summary ($134 average rate; attorneys supported)", "url": "https://nala.org/wp-content/uploads/2025/01/2024-NALA-Compensation-Utilization-Report-ExecSumm-FINAL-1-15-25.pdf"},
 {"what": "FDIC Outside Counsel Deskbook (0.1-hour increments; block billing prohibited; clerical time not billable)", "url": "https://www.fdic.gov/doing-business-fdic/outside-counsel-deskbook.pdf"},
 {"what": "Missouri v. Jenkins, 491 U.S. 274, 288 n.10 (1989) (clerical tasks not billable at paralegal rates)", "url": "https://www.law.cornell.edu/supremecourt/text/491/274"},
 {"what": "USAO-DC Fitzpatrick Matrix (paralegal rate $273 for 2026)", "url": "https://www.justice.gov/usao-dc/media/1449156/dl?inline"},
 {"what": "Clio: lawyer utilization 37%, 2.9 billable hours in an 8-hour day", "url": "https://web.archive.org/web/20260516091805/https://www.clio.com/blog/how-to-calculate-utilization-rate/"},
 {"what": "RAND MG-1208, Where the Money Goes (review rates 31-100 documents an hour)", "url": "https://www.rand.org/content/dam/rand/pubs/monographs/2012/RAND_MG1208.pdf"},
 {"what": "The Sedona Conference, Commentary on Privilege Logs (2024)", "url": "https://www.thesedonaconference.org/sites/default/files/publications/Commentary-on-Privilege-Logs-May-2024.pdf"},
 {"what": "Radicati Group, Email Statistics Report 2015-2019, executive summary (122 business e-mails sent and received per user per day)", "url": "https://web.archive.org/web/20170101112935id_/http://www.radicati.com/wp/wp-content/uploads/2015/02/Email-Statistics-Report-2015-2019-Executive-Summary.pdf"},
 {"what": "Dhakal et al. (CHI 2018), Observations on Typing from 136 Million Keystrokes (51.56 wpm mean)", "url": "https://userinterfaces.aalto.fi/136Mkeystrokes/resources/chi-18-analysis.pdf"},
 {"what": "Brysbaert (2019), How many words do we read per minute? (238 wpm non-fiction)", "url": "https://doi.org/10.1016/j.jml.2019.104047"},
 {"what": "Lawyers Mutual (NC): missed deadlines the top source of malpractice claims", "url": "https://lawyersmutualnc.com/article/missed-deadlines-are-top-cause-of-legal-malpractice/"}]
OUT_DIR = "/home/user/Code/automation-correlation/episodes/23-2011.00"
