# Part 1: helpers, meta, world, contacts
import json
ITEMS = []
def item(id, channel, kind, at, subject, body, frm=None, to=None, cc=None, thread=None, attachments=None, meta=None):
    ITEMS.append({"id": id, "channel": channel, "kind": kind, "at": at, "thread": thread, "from": frm,
                  "to": to or [], "cc": cc or [], "subject": subject, "body": body.strip("\n"),
                  "attachments": attachments or [], "meta": meta or {}})
def email(id, at, frm, to, subject, body, cc=None, thread=None, attachments=None, meta=None):
    item(id, "email", "email", at, subject, body, frm, to, cc, thread, attachments, meta)
def chat(id, at, frm, to, body, thread=None):
    item(id, "chat", "message", at, None, body, frm, to, None, thread)
def doc(id, at, title, body, author=None, kind="document", meta=None, thread=None):
    item(id, "docs", kind, at, title, body, author, None, None, thread, None, meta)
def cal(id, at, title, body, organizer, attendees, start, end, location=None):
    item(id, "calendar", "event", at, title, body, organizer, attendees, None, None, None,
         {"start": start, "end": end, "location": location})

SIG_RK = """Renee Kowalczyk
Senior Litigation Paralegal
Ostrander Hale LLP
180 N. Canal Street, Suite 2200 | Chicago, IL 60606
312.555.0148 | rkowalczyk@ostranderhale.com"""
SIG_PR = """Priya Raman | Senior Associate
Ostrander Hale LLP
312.555.0163 | praman@ostranderhale.com"""
SIG_NC = """Nathan J. Corbin
Corbin & Lisle LLP
2001 Spring Road, Suite 400 | Oak Brook, IL 60523
630.555.0190 | ncorbin@corbinlisle.com"""

META = {"schema_version": "0.1", "soc": "23-2011.00", "title": "Paralegals and Legal Assistants",
        "onet_version": "31.0", "status": "draft", "authors": ["Claude (drafting agent), 2026-10-26"], "sha256": None}

CONTACTS = [
 {"id": "c_renee", "name": "Renee Kowalczyk", "role": "Senior Litigation Paralegal (the worker)", "relation": "self",
  "channels": ["email", "chat", "phone", "calendar"], "notes": "rkowalczyk@ostranderhale.com, ext. 0148. 11 years as a litigation paralegal, NALA Certified Paralegal."},
 {"id": "c_daniel", "name": "Daniel Achterberg", "role": "Partner, Litigation; lead counsel for Kessling", "relation": "supervising partner",
  "channels": ["email", "chat", "phone", "calendar"], "notes": "dachterberg@ostranderhale.com. Takes the Lindqvist deposition. Signs off on pre-bills."},
 {"id": "c_priya", "name": "Priya Raman", "role": "Senior Associate, Litigation", "relation": "supervising attorney on Kessling discovery",
  "channels": ["email", "chat", "phone", "calendar"], "notes": "praman@ostranderhale.com. Signs the discovery responses and objections (FRCP 26(g)); makes privilege calls."},
 {"id": "c_marcus", "name": "Marcus Bell", "role": "Associate, Litigation (third year)", "relation": "attorney on Delacroix v. Midway",
  "channels": ["email", "chat", "phone"], "notes": "mbell@ostranderhale.com. Cook County matter."},
 {"id": "c_gloria", "name": "Gloria Esposito", "role": "Legal Assistant to D. Achterberg", "relation": "co-worker",
  "channels": ["chat", "email", "phone"], "notes": "gesposito@ostranderhale.com. Calendars Daniel; orders lunches; books rooms."},
 {"id": "c_docket", "name": "Sharon Wiley", "role": "Docketing Manager (Docketing Department)", "relation": "firm docketing",
  "channels": ["email"], "notes": "docketing@ostranderhale.com. Enters court and rule deadlines in CompuLaw on written request; sends weekly deadline reports."},
 {"id": "c_tom", "name": "Tom Nguyen", "role": "Litigation Support / e-Discovery Manager", "relation": "co-worker (non-lawyer)",
  "channels": ["email", "chat", "phone"], "notes": "tnguyen@ostranderhale.com. Runs Relativity, processing, Bates stamping and ShareFile productions."},
 {"id": "c_it", "name": "IT Service Desk", "role": "Firm IT / security", "relation": "firm IT",
  "channels": ["email"], "notes": "servicedesk@ostranderhale.com. Suspicious email goes to phishing@ostranderhale.com or the Report Phish button, which opens a Service Desk ticket."},
 {"id": "c_conflicts", "name": "Alana Brooks", "role": "Conflicts Analyst, New Business Intake", "relation": "firm conflicts",
  "channels": ["email"], "notes": "conflicts@ostranderhale.com. No consultation is scheduled and no confidential information is taken until a search clears."},
 {"id": "c_kevin", "name": "Kevin Doyle", "role": "Billing Coordinator", "relation": "firm accounting",
  "channels": ["email"], "notes": "kdoyle@ostranderhale.com. Pre-bills; weekly time reminders."},
 {"id": "c_mailroom", "name": "Luis Ortega", "role": "Mailroom / Office Services", "relation": "firm office services",
  "channels": ["email"], "notes": "mailroom@ostranderhale.com. Scans incoming mail to the responsible paralegal."},
 {"id": "c_facilities", "name": "Conference Center", "role": "Room booking", "relation": "firm facilities",
  "channels": ["email"], "notes": "rooms@ostranderhale.com"},
 {"id": "c_firm", "name": "Ostrander Hale Announcements", "role": "Firm-wide announcements", "relation": "firm",
  "channels": ["email"], "notes": "announcements@ostranderhale.com"},
 {"id": "c_library", "name": "Research Services", "role": "Firm library", "relation": "firm",
  "channels": ["email"], "notes": "library@ostranderhale.com"},
 {"id": "c_rick", "name": "Rick Szymanski", "role": "Vice President of Operations, Kessling Pump & Controls, Inc.", "relation": "client contact (non-lawyer); signs the interrogatory verification",
  "channels": ["email", "phone"], "notes": "rszymanski@kesslingpump.com, cell 815.555.0127. Rockford, IL."},
 {"id": "c_ncorbin", "name": "Nathan Corbin", "role": "Partner, Corbin & Lisle LLP", "relation": "opposing counsel (lead) for Prairie Hollow",
  "channels": ["email", "phone"], "notes": "ncorbin@corbinlisle.com. Parties consented in writing to e-mail service (ESI Stipulation, Dkt. 29, para. 4)."},
 {"id": "c_kbensen", "name": "Kara Bensen", "role": "Associate, Corbin & Lisle LLP", "relation": "opposing counsel (appeared 11/2/2026)",
  "channels": ["email"], "notes": "kbensen@corbinlisle.com"},
 {"id": "c_sfeld", "name": "Stacy Feld", "role": "Paralegal, Corbin & Lisle LLP", "relation": "opposing counsel's paralegal",
  "channels": ["email", "phone"], "notes": "sfeld@corbinlisle.com, 630.555.0194"},
 {"id": "c_court", "name": "N.D. Ill. CM/ECF", "role": "Court electronic filing system (Notices of Electronic Filing)", "relation": "court",
  "channels": ["email"], "notes": "Sends NEFs from ecf_notices@ilnd.uscourts.gov."},
 {"id": "c_phish", "name": "\"ECF Notice\" <ecf-notice@ilnd-uscourts.net>", "role": "Unknown sender (look-alike court domain)", "relation": "unknown",
  "channels": ["email"], "notes": "Not a uscourts.gov address."},
 {"id": "c_reporter", "name": "Denise Okafor", "role": "Scheduling Coordinator, Lakefront Reporting Services", "relation": "court reporting vendor",
  "channels": ["email", "phone"], "notes": "schedule@lakefrontreporting.com, 312.555.0177. Stenographers, videographers, remote links."},
 {"id": "c_process", "name": "Ray Duda", "role": "Dispatcher, Northline Process Service", "relation": "process server vendor",
  "channels": ["email", "phone"], "notes": "dispatch@northlineprocess.com, 414.555.0136. Serves in Wisconsin and Illinois."},
 {"id": "c_dubek", "name": "Lorraine Dubek", "role": "Owner, Dubek's Bakery (prospective client)", "relation": "prospective client (not yet cleared)",
  "channels": ["phone", "email"], "notes": "lorraine@dubeksbakery.com, 773.555.0112"},
 {"id": "c_esato", "name": "Ellen Sato", "role": "Partner, Corporate", "relation": "co-worker",
  "channels": ["email"], "notes": "esato@ostranderhale.com"},
 {"id": "c_jtran", "name": "Jeffrey Tran", "role": "Attorney, Tran & Molloy LLC", "relation": "opposing counsel in Delacroix v. Midway (Cook County)",
  "channels": ["email"], "notes": "jtran@tranmolloy.com"},
 {"id": "c_efile", "name": "eFileIL", "role": "Illinois e-filing service (eFileIL) notifications", "relation": "court e-filing system",
  "channels": ["email"], "notes": "no-reply@efileillinois.com"},
 {"id": "c_vendor", "name": "Vendor newsletters", "role": "Legal publishers and vendors", "relation": "external, bulk",
  "channels": ["email"], "notes": "Practice newsletters and product mail."},
]

WORLD = {
 "worker": {"name": "Renee Kowalczyk", "title": "Senior Litigation Paralegal", "employer": "Ostrander Hale LLP",
            "manager": "Daniel Achterberg (supervising partner); Priya Raman supervises the Kessling discovery day to day",
            "team": "Commercial litigation group: 1 partner, 1 senior associate and 1 associate on her matters, a legal assistant, with firm docketing, litigation support, conflicts and billing departments behind them",
            "contact_id": "c_renee"},
 "organization": {"name": "Ostrander Hale LLP",
   "what": "Chicago commercial law firm, about 120 lawyers, with a commercial litigation group that defends manufacturers and distributors in federal and Illinois state court.",
   "size": "about 120 lawyers and 30 paralegals",
   "norms": ["Every deadline goes to the Docketing Department in writing (CompuLaw); the paralegal computes and the docketing clerk double-checks. The responsible attorney owns the deadline.",
             "Discovery responses and objections are signed by an attorney of record (FRCP 26(g)); interrogatory answers are verified by the client under 28 U.S.C. 1746; paralegals never sign either.",
             "Discovery requests and responses are served, not filed (FRCP 5(d)(1)(A)).",
             "Nothing leaves for opposing counsel until the supervising attorney has approved it; productions go by ShareFile link only after privilege QC sign-off.",
             "Paralegals state their status and do not give legal advice to clients or prospective clients (ABA Model Rule 5.3, 5.5; NALA Canon 1). Prospective clients go through conflicts before any substantive intake.",
             "Time is recorded daily in tenths of an hour in iTimekeep; Kessling's outside counsel guidelines forbid block billing and billing for clerical work.",
             "Suspicious email is reported with the Report Phish button, never opened or forwarded to colleagues."],
   "hours": "08:30-17:30 Central"},
 "contacts": CONTACTS,
 "systems": [
   {"id": "sys_imanage", "name": "iManage Work", "what": "Document management: every pleading, draft, letter and email is filed to the matter workspace (10442-003 Kessling; 11870-002 Midway)."},
   {"id": "sys_relativity", "name": "Relativity (RelativityOne)", "what": "Review platform for Kessling's collected email and documents; privilege coding, production sets, Bates stamping (run by Tom Nguyen)."},
   {"id": "sys_cmecf", "name": "PACER / CM/ECF, N.D. Ill.", "what": "Federal docket; NEFs arrive by email to attorneys of record and listed staff. Discovery is not filed here."},
   {"id": "sys_efileil", "name": "eFileIL", "what": "Illinois statewide e-filing system (Tyler Technologies), mandatory for civil cases under Ill. S. Ct. R. 9 and used by the Circuit Court of Cook County (Delacroix v. Midway); filings submitted in envelopes, accepted or rejected by the clerk."},
   {"id": "sys_compulaw", "name": "CompuLaw Vision (via Docketing Department)", "what": "Rule-based court calendar; entries are made by docketing on written request."},
   {"id": "sys_itimekeep", "name": "iTimekeep", "what": "Time entry, in tenths of an hour, released daily to the billing system (Aderant)."},
   {"id": "sys_sharefile", "name": "ShareFile", "what": "Secure transfer for productions and large files."},
   {"id": "sys_docusign", "name": "DocuSign", "what": "E-signature for client verifications and declarations (signed by the declarant)."}],
 "matters": [
   {"id": "m_kessling", "name": "Prairie Hollow Growers Cooperative v. Kessling Pump & Controls, Inc., No. 1:26-cv-03182 (N.D. Ill.)",
    "notes": "Firm represents defendant Kessling. Breach of warranty over KX-40 irrigation pumps. District Judge Elaine R. Whitford; discovery referred to Magistrate Judge Owen P. Talbot. Matter 10442-003."},
   {"id": "m_midway", "name": "Delacroix Property Holdings, LLC v. Midway Restoration Group, Inc., No. 2025 L 008841 (Cir. Ct. Cook County, Law Div.)",
    "notes": "Firm represents defendant Midway (masonry restoration contractor). Matter 11870-002. Marcus Bell."}]
}
