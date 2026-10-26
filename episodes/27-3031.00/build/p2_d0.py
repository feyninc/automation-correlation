# Part 2: items already there on Monday morning (D0).
ITEMS = []


def item(iid, channel, kind, at, frm, subject, body, to=(), cc=(), thread=None, attachments=(), meta=None):
    ITEMS.append({"id": iid, "channel": channel, "kind": kind, "at": at, "thread": thread or iid, "from": frm,
                  "to": list(to), "cc": list(cc), "subject": subject, "body": body.strip("\n"),
                  "attachments": list(attachments), "meta": meta or {}})


item("doc_release", "docs", "doc", "D0", "c_erin",
     "DRAFT v3 - Halvorsen gift release (EMBARGOED)",
     """
DRAFT v3 (Oct. 29, Erin) - for Doug, Alicia, Greg. Karen's quote is a draft the family has not yet approved. The
Governor's quote is our proposed language; the Governor's office is reviewing it.

EMBARGOED UNTIL 10 A.M. CT, THURSDAY, NOV. 5, 2026

Media contact: Erin Lindqvist, 555-0143, erin.lindqvist@prairiebendhealth.org

Halvorsen family gives $20 million to build region's first psychiatric hospital for children

Gift is the largest in Prairie Bend Health's history; $62 million center to open in fall 2028

PRAIRIE BEND - The Halvorsen Family Foundation has committed $20 million to Prairie Bend Health to build the Halvorsen
Center for Youth Behavioral Health, a 48-bed inpatient psychiatric hospital for children and teens on the health
system's Westgate campus, Prairie Bend Health President and CEO Dr. Raymond Ellison announced Thursday.

The gift is the largest in the health system's 112-year history. The previous largest, $7.5 million, helped build the
Prairie Bend Cancer Center in 2019.

The $62 million, 68,000-square-foot center will have 32 beds for teens ages 12 to 17 and 16 beds for children ages 6
to 11, along with a partial hospitalization program that can serve 24 young people a day. It will be the only
inpatient psychiatric unit for children within 190 miles. Construction is scheduled to begin in spring 2027, and the
center is expected to open in fall 2028 with about 175 new jobs.

Today, children in a mental health crisis often wait in emergency departments for a bed hundreds of miles away. In
the 12 months that ended Sept. 30, 312 children and teens waited in Prairie Bend Medical Center's emergency
department for an inpatient psychiatric bed, an average of 2.6 days each.

"No child in crisis should spend days in an emergency department waiting for help that is three hours away," Ellison
said. "The Halvorsen family's generosity means families in our region will get that care close to home."

"Our son Eli fought hard, and too often the help he needed was far from home," said Karen Halvorsen Doyle, chair of
the Halvorsen Family Foundation. "We want other families to find that help here, close to the people who love them."

The project will be paid for with the $20 million gift, a $12 million grant from the state's Behavioral Health
Capital Fund, $28 million in Prairie Bend Health capital funds and a $2 million community campaign led by the
Prairie Bend Health Foundation.

"Kids do best when they can be treated near their families and their schools," said Dr. Kathleen Moreau, a child
psychiatrist and Prairie Bend Health's vice president of behavioral health services. "This center lets us keep them
here."

"Every child deserves care close to home," said Gov. Patricia Hartley. "This partnership shows what the Behavioral
Health Capital Fund was built to do."

About Prairie Bend Health
Prairie Bend Health is a nonprofit health system serving 22 counties with three hospitals - Prairie Bend Medical
Center, Westfield Community Hospital and Harlan County Hospital - and 41 clinics. Its 8,900 employees care for more
than 400,000 patients a year. Learn more at prairiebendhealth.org.

###
""", meta={"version": 3, "last_edited": "2026-10-29"})

item("doc_advisory", "docs", "doc", "D0", "c_doug",
     "DRAFT media advisory - Thursday announcement",
     """
DRAFT (Oct. 28, Doug) - send to full media list Wednesday, Nov. 4, 9 a.m. CT. Advisory only: no gift amount, no
family name.

MEDIA ADVISORY

Prairie Bend Health to make major announcement on mental health care for children and teens

WHAT: Prairie Bend Health will announce a major investment in mental health care for children and teens in the
region.

WHO: Dr. Raymond Ellison, president and CEO, Prairie Bend Health; Dr. Kathleen Moreau, vice president, behavioral
health services; community and state leaders; Gov. Patricia Hartley (invited).

WHEN: 10:30 a.m. Thursday, Nov. 5. Media check-in begins at 9:45 a.m.

WHERE: Westgate Community Room, Prairie Bend Health Westgate Campus, 2200 Westgate Road, Prairie Bend. Media parking
in Lot B by the north entrance.

VISUALS: Speakers at podium, site renderings, the future building site.

INTERVIEWS: Speakers will be available after the program.

CONTACT: Erin Lindqvist, 555-0143, erin.lindqvist@prairiebendhealth.org
""", meta={"version": 1, "last_edited": "2026-10-28"})

item("doc_run_of_show", "docs", "doc", "D0", "c_denise",
     "Run of show v2 - Halvorsen announcement, Thu Nov 5",
     """
RUN OF SHOW v2 (updated Oct. 30, Denise) - CHANGE FROM v1: program moved from 10:30 to 10:00 a.m. because the
Governor must leave Westgate by 10:50 a.m.

Location: Westgate Community Room, 2200 Westgate Road (seats 120). Media riser at back, mult box (12 outputs) by
the riser. Lot B reserved for media vans.

8:30 a.m.   Comms and Foundation staff on site; AV check (Kyle)
9:00 a.m.   Halvorsen family arrives; green room (Conference Room 2)
9:15 a.m.   Media check-in opens (Erin, Priya if back)
9:30 a.m.   Optional b-roll walk of the building site with Dr. Moreau (exterior only)
9:45 a.m.   Guests seated
10:00 a.m.  Program begins (EMBARGO LIFTS)
            - Welcome: Alicia Brandt (1 min)
            - Dr. Raymond Ellison (4 min) - announces gift
            - Karen Halvorsen Doyle (4 min)
            - Gov. Patricia Hartley (4 min) - Behavioral Health Capital Fund grant
            - Dr. Kathleen Moreau (3 min) - what the center will do
            - Unveiling of rendering (Greg, family) (2 min)
10:20 a.m.  Photos with family, Governor, board
10:35 a.m.  Media availability (Ellison, Halvorsen Doyle, Moreau; Governor until 10:50)
11:00 a.m.  End

Release goes out at 10:00 a.m. on PR Newswire and to the media list (Erin). Social posts at 10:00 a.m. (Tasha).
CEO all-staff email 10:05 a.m. (Ben). Foundation donor email 10:15 a.m. (Greg).
""", meta={"version": 2, "last_edited": "2026-10-30"})

item("doc_embargo_plan", "docs", "doc", "D0", "c_doug",
     "Embargo and media plan - Halvorsen announcement",
     """
EMBARGO AND MEDIA PLAN (Doug, Oct. 29)

Embargo: 10:00 a.m. Central, Thursday, Nov. 5. All times in this plan are Central.

1. Embargoed briefings (Tue. Nov. 3 to Wed. Nov. 4)
   Offer to: Dana Whitfield (Ledger), Jessica Ruiz (NewsCenter 9), Hannah Brooks (Mid-Valley Public Radio), Tom
   Albrecht (Business Journal).
   Rule: the reporter must agree in writing (a reply email is fine) to hold everything until 10:00 a.m. CT Thursday
   BEFORE we send the release or schedule interviews. The pitch itself says only that we have a significant
   announcement about children's mental health care, not the donor or the amount.
   Interviews available Wed. 1-4 p.m.: Dr. Moreau; Karen Halvorsen Doyle (if she agrees); Dr. Ellison 2:00-2:30 only.
   Do NOT offer embargoed material to 5 News (embargo break, March 12 cancer center story; no embargoes through
   March 2027). They get the advisory and the release at 10:00 like everyone else.
2. Advisory to the full media list: Wed. Nov. 4, 9:00 a.m. (no donor name or amount).
3. Release: 10:00 a.m. Thursday via PR Newswire state circuit and email to the full media list; newsroom post at
   10:00 a.m.; social posts at 10:00 a.m.; CEO all-staff email 10:05 a.m.; Foundation donor email 10:15 a.m.
4. The state's release (DHHS) goes at 10:00 a.m. under the same embargo; Andrea Lutz coordinates.
5. Donor family and Foundation: no public posts before 10:00 a.m. Thursday.
6. Election Day is Tuesday, so do not pitch anything else Tuesday or Wednesday morning.
""", meta={"last_edited": "2026-10-29"})

item("sheet_media_list", "docs", "sheet", "D0", "c_erin",
     "Media list - Halvorsen announcement (Cision export, edited)",
     """
Outlet | Contact | Beat | Phone | Embargo OK | Notes
Prairie Bend Ledger | Dana Whitfield | Health | 555-0161 | Yes | Embargoed briefing; prefers email; also on the Haskins ED story
Prairie Bend Ledger | Mike Torres | City editor | 555-0162 | n/a | Copy on release only
NewsCenter 9 | Jessica Ruiz | General/health | 555-0171 | Yes | Embargoed briefing; will want b-roll and a family interview
NewsCenter 9 | Assignment desk (Ashley Price) | Desk | 555-0170 | n/a | Advisory and release
5 News | Luis Ortega | General | 555-0181 | NO | Broke 3/12/26 embargo (cancer center). No embargoed material through 3/2027 (Doug)
5 News | Assignment desk | Desk | 555-0180 | n/a | Advisory and release
Mid-Valley Public Radio | Hannah Brooks | Health/Morning Edition | 555-0151 | Yes | Embargoed briefing; tape interviews by phone
Prairie Bend Business Journal | Tom Albrecht | Business/health care | 555-0191 | Yes | Embargoed briefing; will ask about financing
State Capitol News Service | Colleen Burke | Statehouse | 555-0121 | n/a | Advisory and release; will cover the Governor
Tri-County 12 News | Desk | Regional TV | 555-0131 | n/a | Advisory and release
The State Courier | Health desk | Statewide newspaper | 555-0111 | n/a | Release only
Prairie Bend Parent | Editor | Family magazine (monthly) | 555-0141 | n/a | Release only
""", meta={"rows": 12})

item("doc_qa", "docs", "doc", "D0", "c_erin",
     "Anticipated Q&A v1 - Halvorsen announcement (internal)",
     """
ANTICIPATED Q&A v1 (Oct. 28, Erin) - INTERNAL, NOT FOR DISTRIBUTION. For Dr. Ellison, Dr. Moreau, Alicia, Greg.

1. Why does the region need this?
In the 12 months that ended Sept. 30, 312 children and teens waited in our emergency department for an inpatient
psychiatric bed, an average of 2.6 days each. The nearest inpatient unit for children is 190 miles away.

2. What will it cost and who is paying?
$62 million: the $20 million Halvorsen gift, a $12 million state Behavioral Health Capital Fund grant, $28 million in
Prairie Bend Health capital funds and a $2 million Foundation community campaign.

3. When will it open?
Construction begins in spring 2027; we expect to open in fall 2028.

4. Can you staff it, given the shortage of nurses and behavioral health workers?
The center will add about 175 jobs. We have a strong record of recruiting: our emergency department nursing vacancy
rate is under 8% (June 2026), and we will start a child and adolescent psychiatric nursing residency in 2027.

5. Why the Westgate campus?
We own the land, it is on the bus line, and it is 10 minutes from Prairie Bend Medical Center for medical backup.

6. Will it take Medicaid?
Yes. About 55% of the children who waited in our emergency department last year were covered by Medicaid.

7. What happens to children in crisis until 2028?
We will keep caring for them in our emergency department with our behavioral health team, and we have added a
child psychiatrist to the consult service.

8. Is the Governor's appearance political, two days after the election?
The Behavioral Health Capital Fund grant was awarded in August through a competitive process. We invited the
Governor because the state is a funding partner.

9. Why is the family giving?
Ask Karen to speak for the family. Their son Eli died in 2021 at 16; the family has spoken publicly about his
illness. We do not add details beyond what Karen chooses to share.

10. Will there be adult beds?
No. The center is for children and teens only.
""", meta={"version": 1, "last_edited": "2026-10-28"})

item("sheet_oct_clips", "docs", "sheet", "D0", "c_priya",
     "October 2026 coverage log - summary by outlet (from Meltwater export, coded)",
     """
October 2026 earned media, Prairie Bend Health (Oct. 1-31). Coded by Priya and Erin. Tone: positive / neutral /
negative toward PBH. Audience = Meltwater estimated audience per story (unique visitors or viewers).

Outlet | Type | Stories | Positive | Neutral | Negative | Est. audience per story
Prairie Bend Ledger | print/online | 12 | 6 | 4 | 2 | 61,000
NewsCenter 9 | TV/online | 9 | 5 | 3 | 1 | 48,000
5 News | TV/online | 7 | 3 | 3 | 1 | 41,000
Mid-Valley Public Radio | radio/online | 5 | 3 | 2 | 0 | 22,000
Prairie Bend Business Journal | print/online | 4 | 2 | 2 | 0 | 9,500
Statewide/regional outlets | mixed | 6 | 2 | 3 | 1 | 35,000
Trade/national | online | 3 | 2 | 1 | 0 | 120,000
Community/neighborhood | online | 8 | 6 | 2 | 0 | 4,000

Pitched (our outreach led to the story): 21 stories.
September 2026 for comparison: 47 stories, 24 positive.
Note: the Haskins Facebook post (Oct. 29) is in the social listening log, not here; no news story in October.
""", meta={"month": "2026-10"})

item("doc_media_policy", "docs", "doc", "D0", "c_alicia",
     "PBH Media Relations Policy (excerpt, rev. 2025)",
     """
PRAIRIE BEND HEALTH - MEDIA RELATIONS POLICY (excerpt, rev. March 2025)

1. Spokespeople. Only the CEO, executives designated by Marketing & Communications, and physicians or staff arranged
by Media Relations speak to news media on the record. Media Relations staff may give approved statements and
factual information already public.

2. Patient information (HIPAA, 45 CFR 164.510(a)). Media Relations may release a patient's one-word condition only
when the caller asks for the patient by full name, the patient is listed in the facility directory, and the patient
has not asked to be excluded. Use only the AHA terms: undetermined, good, fair, serious, critical. For a patient who
has opted out ("no information" status), say: "I don't have any information I can release on anyone by that name."
Do not confirm that the person is a patient. Never release information about a patient who is not named by the
caller. Minors: condition only with a parent's permission.

3. Filming and photography. No filming, photography or recording of patients, or in any patient care area, without
each patient's written HIPAA authorization obtained before filming. Blurring afterward is not enough.

4. Complaints, claims and litigation. Any inquiry about a care complaint, a claim, or a lawsuit goes to Legal and the
Privacy Officer before any response other than an acknowledgment. Statements are approved by the VP of Marketing &
Communications. Even when a patient or family speaks publicly, we do not confirm or discuss the patient's care
without a valid authorization AND Legal's approval.

5. Personnel. We do not confirm or discuss personnel actions (discipline, leave, termination) about any employee.

6. Embargoes. Embargoed materials go only to reporters who have agreed to the embargo in writing beforehand. Any
reporter who breaks an embargo is excluded from embargoed material for 12 months.

7. Labor relations. Statements about the union or bargaining are approved by the VP and Labor Relations. Do not
comment on the substance of negotiations or on individual employees' union activity.

8. Social media. Do not delete or hide critical comments unless they break the posted community guidelines (threats,
profanity, spam, someone's health information). Never confirm that a commenter is or was a patient.
""")

item("doc_fb_log", "docs", "doc", "D0", "c_priya",
     "Social listening log - Haskins Facebook post",
     """
SOCIAL LISTENING LOG - Haskins post (Priya; started Oct. 29)

Post: public Facebook post by Derek Haskins, Oct. 29, 7:12 p.m.:
"My mom Linda Haskins went to the Prairie Bend Medical Center ER on Oct. 24 around 2 p.m. with chest pain. She sat
in the waiting room almost six hours. She collapsed in that waiting room and died the next day. She was 67. Nobody
should die waiting. Please share so this never happens to another family. #JusticeForLinda"

Shares / comments:
Oct. 29, 11 p.m. - 410 shares, 120 comments
Oct. 30, 5 p.m. - 2,300 shares, 640 comments
Comment themes: ER waits (most), nurse staffing, "the hospital only cares about money", several former patients
describing their own waits, two people claiming to be PBH employees.

Messages to our Facebook page about the post: 37 (logged; not answered).

Status: no public response, per Legal (Steven Park, Oct. 30). Patient Relations (Janelle Ortiz) is handling the
family's grievance. Do not reply to comments or messages about this post.
""")

item("e_legal_hold", "email", "email", "D0", "c_steven",
     "PRIVILEGED & CONFIDENTIAL - Legal hold notice: Linda Haskins (ED, Oct. 24-25)",
     """
PRIVILEGED & CONFIDENTIAL - ATTORNEY-CLIENT COMMUNICATION

All,

Prairie Bend Health has received a letter from an attorney representing the family of Linda Haskins concerning her
care in the PBMC emergency department on Oct. 24-25, 2026. You are receiving this notice because you may have
documents or messages related to her visit or to public comments about it.

Effective immediately, preserve everything related to Ms. Haskins, her visit, or the public posts about it: email,
Teams messages, texts, voicemail, notes, Facebook page messages and comments, media inquiry log entries and
drafts. Do not delete, edit or move these items. This hold overrides any routine deletion.

Do not discuss this matter with anyone outside Prairie Bend Health, and inside only with people who need to know.
Any media inquiry about it goes to Media Relations, who will coordinate with me before any response.

No reply is needed. This notice stays in effect until Legal releases it in writing.

Steven Park
Associate General Counsel, Prairie Bend Health
""", to=["c_doug", "c_erin", "c_priya", "c_tasha", "c_janelle"], cc=["c_alicia", "c_rhonda"],
     thread="t_haskins_legal", meta={"sent": "2026-10-30 16:42"})

item("cal_huddle", "calendar", "event", "D0", "c_doug", "Comms team huddle",
     "Mon., Nov. 2, 9:00-9:30 a.m., Marketing & Communications conference room / Teams. Weekly priorities.",
     to=["c_erin", "c_tasha", "c_ben", "c_marisol", "c_kyle", "c_jordan"], meta={"start": "D1 09:00", "end": "D1 09:30"})
item("cal_exec", "calendar", "event", "D0", "c_alicia", "Exec team meeting (Alicia: October media report)",
     "Tue., Nov. 3, 10:00-11:00 a.m., Board Room. Alicia presents the October media report; she needs it by 9:00 a.m. "
     "Tuesday.", to=["c_erin", "c_doug"], meta={"start": "D2 10:00", "end": "D2 11:00", "erin_attends": False})
item("cal_ceo_prep", "calendar", "event", "D0", "c_carol", "CEO prep and rehearsal - Thursday announcement",
     "Wed., Nov. 4, 4:00-5:00 p.m., CEO conference room. Dr. Ellison, Dr. Moreau, Alicia, Erin; Karen Halvorsen "
     "Doyle by phone 4:30-4:45. Remarks run-through and Q&A practice.",
     to=["c_erin", "c_alicia", "c_kathleen", "c_ceo"], meta={"start": "D3 16:00", "end": "D3 17:00"})
item("cal_event", "calendar", "event", "D0", "c_denise", "Halvorsen announcement (program 10:00 a.m.)",
     "Thu., Nov. 5, 8:30-11:00 a.m., Westgate Community Room, 2200 Westgate Road. See run of show v2.",
     to=["c_erin", "c_doug", "c_alicia", "c_tasha", "c_kyle", "c_greg"], meta={"start": "D4 08:30", "end": "D4 11:00"})
item("cal_debrief", "calendar", "event", "D0", "c_alicia", "Announcement debrief",
     "Fri., Nov. 6, 11:00-11:30 a.m., Teams. What worked, coverage, follow-ups.",
     to=["c_erin", "c_doug", "c_greg", "c_tasha"], meta={"start": "D5 11:00", "end": "D5 11:30"})
