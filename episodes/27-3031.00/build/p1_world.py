# Part 1: meta, economics, world, contacts.
SOC = "27-3031.00"

MEDIA = ["c_dana", "c_mike", "c_jessica", "c_nc9_desk", "c_luis", "c_5news_desk", "c_hannah", "c_tom", "c_scns",
         "c_medialist", "c_student"]
EMBARGO_AGREED = ["c_dana", "c_jessica", "c_hannah", "c_tom"]
NOT_AGREED = ["c_mike", "c_nc9_desk", "c_luis", "c_5news_desk", "c_scns", "c_medialist", "c_student"]

meta = {
    "schema_version": "0.1",
    "soc": SOC,
    "title": "Public Relations Specialists",
    "onet_version": "31.0",
    "status": "draft",
    "authors": ["Claude (draft for owner review), 2026-10-26"],
    "sha256": None,
}

economics = {
    "median_hourly_wage": {"value": 35.94, "year": 2025, "annual": 74750,
                           "source": "BLS OEWS May 2025 via O*NET OnLine; data/wages-onetonline-2026-10-26.csv; "
                                     "https://www.onetonline.org/link/summary/27-3031.00"},
    "employment": {"value": 314500, "year": 2025,
                   "source": "data/wages-onetonline-2026-10-26.csv; BLS OOH "
                             "https://www.bls.gov/ooh/media-and-communication/public-relations-specialists.htm"},
    "projection": {"period": "2025-2035", "growth": "Slower than average (1% to 2%); BLS OOH: 2%, 314,500 to 320,200",
                   "openings": 23000,
                   "source": "data/onetonline/summary-27-3031.00.html; "
                             "https://www.bls.gov/ooh/media-and-communication/public-relations-specialists.htm"},
    "observed_exposure": {"value": 0.453, "source": "data/aei/job_exposure.csv (Anthropic Economic Index, labor "
                                                    "market impacts, 2026-03-05), SOC 27-3031"},
    "task_penetration": {
        "1764": 0.9841, "20555": 0.9177, "23951": 0.0, "20554": 0.7411, "1765": 0.0, "1770": 0.0, "1772": 0.6668,
        "1769": 0.9314, "20557": 0.7262, "1768": 0.0, "1775": 0.9393, "19811": 0.0, "1767": 0.0, "1771": 0.0,
        "1773": 0.0, "19809": 0.0, "19810": 0.0, "1774": 0.0,
        "source": "data/aei/task_penetration.csv joined on O*NET 31.0 task text"},
    "loaded_cost_multiplier": {
        "value": 1.523,
        "basis": "Private industry, hospitals: total compensation $66.85/h, wages and salaries $43.88/h (65.6%), "
                 "June 2026",
        "alternatives": {"health_care_and_social_assistance": 1.421, "all_private_industry": 1.429,
                         "professional_scientific_technical_services": 1.464},
        "source": "BLS Employer Costs for Employee Compensation, June 2026 (released 2026-09-09), Table 4: "
                  "https://www.bls.gov/news.release/ecec.t04.htm"},
    "loaded_hourly_wage": {"value": 54.75, "formula": "35.94 x 1.523"},
    "minutes_model": {
        "basis": "Reading 238 words/min (Brysbaert 2019, https://doi.org/10.1016/j.jml.2019.104047); keyboard "
                 "composition about 19 words/min versus about 33 for transcription (Karat et al. 1999, CHI, "
                 "https://doi.org/10.1145/302979.303160; figures from the paper's results, not its abstract). PR-"
                 "specific times are estimates (no published time-and-motion study found), reasoned in research.md.",
        "per_proposal_type": {
            "reply_short": {"do_minutes": 4, "review_minutes": 1,
                            "why": "60-90 words at ~19 wpm plus a minute to reread the thread"},
            "reply_media_factual": {"do_minutes": 12, "review_minutes": 3,
                                    "why": "look up or confirm a fact (house supervisor, CNO data, release), compose "
                                           "100-150 words, check against policy"},
            "pitch_email": {"do_minutes": 15, "review_minutes": 3,
                            "why": "Muck Rack 2025: journalists want pitches under 200 words, tailored to beat"},
            "statement": {"do_minutes": 40, "review_minutes": 8,
                          "why": "150-250 words that must survive Legal and Privacy review; several passes"},
            "press_release_edit": {"do_minutes": 20, "review_minutes": 5,
                                   "why": "change figures across headline, body, funding paragraph; recheck AP style"},
            "press_release_draft": {"do_minutes": 150, "review_minutes": 15,
                                    "why": "500-700 words, quotes, boilerplate, AP style; estimate"},
            "speech_remarks": {"do_minutes": 75, "review_minutes": 8,
                               "why": "3-4 minutes spoken (~450 words) in the speaker's voice"},
            "qa_update": {"do_minutes": 25, "review_minutes": 5,
                          "why": "new question and bridge answer from approved language"},
            "coverage_report": {"do_minutes": 50, "review_minutes": 8,
                                "why": "tally a clip log, compute totals and shares, write a short read-out"},
            "memo": {"do_minutes": 35, "review_minutes": 6, "why": "one-page options memo"},
            "social_guidance": {"do_minutes": 15, "review_minutes": 3, "why": "approved response line plus rules"},
            "schedule": {"do_minutes": 5, "review_minutes": 1, "why": "find a slot, send invite"},
            "call_line": {"do_minutes": 0.3, "review_minutes": 0.1,
                          "why": "one spoken line; the review is hearing it in the moment"},
        },
    },
}

worker = {
    "name": "Erin Lindqvist",
    "title": "Public Relations Specialist, Media Relations",
    "employer": "Prairie Bend Health",
    "manager": "c_doug",
    "team": "Marketing & Communications (14 people): media relations (Doug Reinholt, Erin Lindqvist, Priya "
            "Natarajan), social media, internal communications, design, video, marketing; reports to VP Alicia Brandt",
    "email": "erin.lindqvist@prairiebendhealth.org",
    "phone": "555-0143 (desk), media line 555-0100 (rotates)",
}

organization = {
    "name": "Prairie Bend Health",
    "what": "Nonprofit regional health system founded in 1914: Prairie Bend Medical Center (412 beds, Level II "
            "trauma center, 71,400 emergency visits in 2025), Westfield Community Hospital (96 beds), Harlan County "
            "Hospital (25-bed critical access), 41 clinics, about 8,900 employees, 22 counties. Not publicly traded; "
            "a HIPAA covered entity. Its foundation (Prairie Bend Health Foundation) raises philanthropy.",
    "size": "8,900 employees; Marketing & Communications 14 FTE",
    "norms": [
        "Only designated spokespeople speak on the record; media relations staff speak for the system and arrange "
        "physician experts.",
        "Statements on patient care complaints, claims or litigation are cleared by Legal (Steven Park) and, where "
        "patient information is involved, the Privacy Officer (Rhonda Tillman), then approved by the VP (Alicia "
        "Brandt).",
        "Patient condition is released only when the caller asks for the patient by name, only in the one-word AHA "
        "terms (undetermined, good, fair, serious, critical), and never for patients who opted out of the facility "
        "directory (45 CFR 164.510(a)).",
        "No filming or photography of patients or in patient care areas without the patient's written "
        "authorization.",
        "Personnel actions are never confirmed or discussed externally.",
        "Embargoed material goes only to reporters who agreed to the embargo in writing beforehand.",
        "Media line on-call rotates weekly; the on-call specialist answers within 30 minutes during business hours.",
        "Times in releases and plans are Central time.",
    ],
    "policy_doc": "doc_media_policy",
}

C = []


def contact(cid, name, role, relation, channels=("email",), notes=""):
    C.append({"id": cid, "name": name, "role": role, "relation": relation, "channels": list(channels),
              "notes": notes})


contact("c_erin", "Erin Lindqvist", "Public Relations Specialist, Media Relations", "self", ("email", "chat", "phone"))
contact("c_doug", "Doug Reinholt", "Director, Media Relations & Public Affairs", "manager", ("email", "chat", "phone"),
        "At the state hospital association board meeting in the capital Wednesday; back Thursday 8:45 a.m.")
contact("c_alicia", "Alicia Brandt", "Vice President, Marketing & Communications", "manager's manager",
        ("email", "chat", "phone"), "Approves statements and any change to the Thursday plan; reports to the CEO.")
contact("c_ceo", "Dr. Raymond Ellison", "President and CEO", "executive", ("email",),
        "Spokesperson for the Thursday announcement.")
contact("c_carol", "Carol Mendez", "Executive Assistant to the CEO", "colleague", ("email", "chat", "phone"))
contact("c_steven", "Steven Park", "Associate General Counsel", "colleague (Legal)", ("email", "chat", "phone"),
        "Handles the Haskins claim; issued the legal hold.")
contact("c_rhonda", "Rhonda Tillman", "Chief Privacy & Compliance Officer", "colleague (Privacy)", ("email", "chat"))
contact("c_janelle", "Janelle Ortiz", "Director, Patient Experience", "colleague", ("email", "chat"),
        "Patient Relations line 555-0190.")
contact("c_lisa", "Lisa Harmon, DNP, RN", "Chief Nursing Officer", "executive", ("email", "chat"))
contact("c_kathleen", "Dr. Kathleen Moreau", "Vice President, Behavioral Health Services (child psychiatrist)",
        "colleague / spokesperson", ("email", "chat", "phone"))
contact("c_sameer", "Dr. Sameer Qureshi", "Medical Director, PBMC Emergency Department", "physician leader", ("email", "chat"))
contact("c_anita", "Dr. Anita Shah", "Infectious disease physician", "physician expert", ("email", "chat"))
contact("c_housesup", "Mark Ellery, RN", "House Supervisor, Nursing Administration (days)", "colleague",
        ("chat", "phone"), "Gives media relations the directory status and one-word condition of patients.")
contact("c_priya", "Priya Natarajan", "Public Relations Specialist", "teammate", ("email", "chat"),
        "On call last weekend; on PTO Monday and Tuesday.")
contact("c_tasha", "Tasha Greene", "Social Media Manager", "teammate", ("email", "chat"),
        "Schedules posts in Sprout Social.")
contact("c_ben", "Ben Adeyemi", "Internal Communications Specialist", "teammate", ("email", "chat"),
        "Edits PBH Pulse, the weekly employee newsletter (Mondays).")
contact("c_marisol", "Marisol Reyes", "Graphic Designer", "teammate", ("email", "chat"))
contact("c_kyle", "Kyle Brandvold", "Video Producer", "teammate", ("email", "chat"))
contact("c_jordan", "Jordan Fitch", "Marketing Coordinator", "teammate", ("email", "chat"),
        "Runs the North Prairie urgent care opening (Nov. 16).")
contact("c_greg", "Greg Whitcomb", "Vice President and Chief Development Officer, Prairie Bend Health Foundation",
        "internal client", ("email", "phone"))
contact("c_denise", "Denise Kowalski", "Events Manager, Prairie Bend Health Foundation", "internal client",
        ("email", "chat"))
contact("c_karen", "Karen Halvorsen Doyle", "Board chair, Halvorsen Family Foundation", "donor", ("email", "phone"),
        "Her son Eli died in 2021 at 16; the family has spoken publicly about his illness.")
contact("c_andrea", "Andrea Lutz", "Communications Director, state Department of Health and Human Services",
        "government partner", ("email", "phone"))
contact("c_dana", "Dana Whitfield", "Health reporter, Prairie Bend Ledger", "media", ("email", "phone"),
        "Honors embargoes. Also reporting the Haskins story.")
contact("c_mike", "Mike Torres", "City editor, Prairie Bend Ledger", "media", ("email", "phone"))
contact("c_jessica", "Jessica Ruiz", "Reporter, NewsCenter 9", "media", ("email", "phone"))
contact("c_nc9_desk", "NewsCenter 9 assignment desk (Ashley Price, assignment editor)", "TV assignment desk", "media",
        ("email", "phone"))
contact("c_luis", "Luis Ortega", "Reporter, 5 News", "media", ("email", "phone"),
        "Broke the March 12, 2026 cancer center embargo; no embargoed material through March 2027 (Doug).")
contact("c_5news_desk", "5 News assignment desk", "TV assignment desk", "media", ("email", "phone"))
contact("c_hannah", "Hannah Brooks", "Reporter and Morning Edition host, Mid-Valley Public Radio", "media",
        ("email", "phone"))
contact("c_tom", "Tom Albrecht", "Reporter, Prairie Bend Business Journal", "media", ("email", "phone"))
contact("c_scns", "Colleen Burke", "Reporter, State Capitol News Service", "media", ("email",))
contact("c_medialist", "PBH media list (all outlets, Cision distribution list)", "distribution list", "media",
        ("email",))
contact("c_student", "Maya Lindgren", "Student, Prairie State University journalism program", "public", ("email",))
contact("c_monica", "Monica Feld", "Executive director, Prairie Bend Youth Mental Health Coalition",
        "community partner", ("email", "phone"))
contact("c_pbna", "Carla Jennings, RN", "President, Prairie Bend Nurses Association (union for 1,450 PBMC RNs)",
        "labor union", ("email",))
contact("c_meltwater", "Meltwater Alerts (alerts@meltwater.com)", "media monitoring service", "vendor", ("email",))
contact("c_phish", "Meltwater Support (support@meltwater-secure-login.com)", "spoofed sender", "unknown", ("email",),
        "Not Meltwater: look-alike domain.")
contact("c_itsec", "PBH IT Security (phishing@prairiebendhealth.org)", "IT security mailbox", "internal", ("email",))
contact("c_vendor", "Healthcare Excellence Honors (awards@hc-excellence-honors.com)", "pay-to-play awards vendor",
        "vendor", ("email",))
contact("c_hr", "PBH Human Resources", "all-staff sender", "internal", ("email",))
contact("c_hospassoc", "State Hospital Association communications", "trade association newsletter", "external",
        ("email",))
contact("c_prsa", "Mid-Valley PRSA Chapter", "professional association chapter", "external", ("email",))
contact("c_allstaff", "All PBH staff (distribution list)", "distribution list", "internal", ("email",))

systems = [
    {"id": "sys_cision", "name": "Cision (media database and distribution lists)",
     "use": "media list, distribution of advisories and releases to the PBH media list"},
    {"id": "sys_prnewswire", "name": "PR Newswire state circuit",
     "use": "paid wire distribution of the release at 10:00 a.m. CT Thursday"},
    {"id": "sys_meltwater", "name": "Meltwater media monitoring",
     "use": "daily digest and real-time alerts; clip log for monthly reports"},
    {"id": "sys_sprout", "name": "Sprout Social", "use": "scheduling and moderating Facebook, Instagram, LinkedIn, X"},
    {"id": "sys_wordpress", "name": "WordPress newsroom (prairiebendhealth.org/news)", "use": "newsroom posts"},
    {"id": "sys_medialog", "name": "Media inquiry log (SharePoint list)",
     "use": "every inquiry logged: outlet, reporter, topic, deadline, response, approver"},
    {"id": "sys_ap", "name": "AP Stylebook Online", "use": "style for releases and statements"},
]

world = {"worker": worker, "organization": organization, "contacts": C, "systems": systems}
channels = ["email", "chat", "docs", "calendar", "phone"]
