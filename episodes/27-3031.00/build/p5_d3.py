# Part 5: Wednesday, Nov. 4 (D3).
d3 = {"date": "2026-11-04", "label": "Wednesday", "actions": [], "calls": []}
DAYS.append(d3)

item("e_d3_digest", "email", "email", "D3 06:00", "c_meltwater", "Meltwater daily digest - Prairie Bend Health - Nov. 4",
     """
Meltwater | Daily digest | Prairie Bend Health | 24 hours to 6:00 a.m. CT, Nov. 4

Mentions: 11 news, 604 social

NEWS
- Mid-Valley Public Radio, Morning Edition (Nov. 4, 6:50 a.m.): "Flu, RSV arriving early" - Dr. Anita Shah, Prairie
  Bend Health. Tone: positive.
- Prairie Bend Ledger (Nov. 4): "Hartley wins second term" - no PBH mention.
- Prairie Bend Business Journal (Nov. 3, 6:10 p.m.): "Council member Dunleavy absent from election night watch
  party" - "a spokesperson for Prairie Bend Health said she had no information to release." Tone: neutral.

SOCIAL
- Facebook: Haskins post 3,100 shares. Prairie Bend Nurses Association page: "Join us at noon Wednesday outside
  PBMC." 520 shares.
""", to=["c_erin", "c_doug", "c_priya", "c_tasha"], thread="t_digest")

item("e_d3_jessica_union", "email", "email", "D3 08:05", "c_jessica", "Fwd: MEDIA ADVISORY - nurses to speak out on ER staffing",
     """
Saw this - will PBH have a statement for noon? I'll be there. - Jessica

---------- Forwarded message ----------
From: Prairie Bend Nurses Association
Date: Wed, Nov 4, 2026, 7:30 AM

MEDIA ADVISORY
Nurses to speak out on dangerous ER staffing at Prairie Bend Medical Center

WHEN: Noon, Wednesday, Nov. 4
WHERE: Public sidewalk outside the PBMC main entrance, 1500 N. Grand Ave.
WHO: PBNA President Carla Jennings, RN, and emergency department nurses
WHY: "The death of Linda Haskins was preventable. Our ER nurses have warned management for a year that staffing is
unsafe," Jennings said. PBNA represents 1,450 registered nurses at PBMC. Their contract expires Dec. 31. Nurses will
call on legislators to pass the Safe Patient Limits Act.
""", to=["c_erin"], thread="t_union")

item("e_d3_steven", "email", "email", "D3 08:10", "c_steven", "PRIVILEGED - Re: Draft statement - Ledger",
     """
PRIVILEGED & CONFIDENTIAL

Erin - edits to the statement:

Para 1: keep "Our hearts go out to this family." Delete "and that is true even when a family has spoken publicly" -
it suggests we know what was said about a patient's care. Para 1 becomes: "Our hearts go out to this family. Federal
privacy law does not allow us to discuss any patient's care without written permission."
Para 2: fine.
Para 3: add Lisa's numbers: "...Since January we have hired 22 emergency nurses, and 104 of our 118 emergency nursing
positions are filled today. We use contract nurses to cover open shifts while we recruit for the rest."
Q3: "We do not discuss personnel matters." Q5: no response at all; don't say "no comment on litigation" either -
just don't address it.

Legal is fine with it as edited. Rhonda to confirm, then Alicia.

Steven
""", to=["c_erin"], cc=["c_rhonda", "c_doug", "c_alicia"], thread="t_haskins_legal")

item("e_d3_rhonda", "email", "email", "D3 08:20", "c_rhonda", "Re: Draft statement - Ledger",
     """
Agree with Steven's edits. Two more: don't use Ms. Haskins's name in anything we send, including your cover note to
Dana, and avoid "her visit," "her wait" or anything that reads as confirming she was here. On social, no replies to
the family or to commenters about her.

Rhonda Tillman | Chief Privacy & Compliance Officer
""", to=["c_erin"], cc=["c_steven"], thread="t_haskins_legal")

item("e_d3_carol", "email", "email", "D3 08:40", "c_carol", "Re: Thursday remarks for Dr. Ellison",
     "Just checking on the remarks - he has a gap at 9:15 and wants to read them then. Thanks! Carol",
     to=["c_erin"], thread="t_remarks")

item("e_d3_luis", "email", "email", "D3 09:25", "c_luis", "Re: our call",
     """
Erin - following up. If you change your mind just send the release, I'll hold it till 10 tomorrow, you have my
word. And can you at least confirm it's $20 million from the Halvorsen family? That's what I'm hearing.

Luis Ortega | 5 News
""", to=["c_erin"], thread="t_luis")

item("chat_d3_alicia", "chat", "message", "D3 10:00", "c_alicia", "Teams: Alicia Brandt",
     """
Steven's edits look right; I'll approve the statement after my 1:00 with Ray. Ray asked whether we should push
Thursday given the Ledger story lands that morning. I need options from you by 1 p.m. - pros and cons, your
recommendation to me is fine, but nothing to Greg or the family yet. Ray and I will decide.
""", to=["c_erin"], thread="t_chat_alicia")

item("e_d3_steven_auth", "email", "email", "D3 10:15", "c_steven", "PRIVILEGED - Re: Fwd: family authorization",
     """
PRIVILEGED & CONFIDENTIAL

Thanks for flagging. Even with an authorization we won't discuss her care while the claim is pending. Ray agrees.
You can tell Dana we've considered the offer and the statement is our response. Don't characterize why.

Steven
""", to=["c_erin"], thread="t_haskins_legal")

item("doc_d3_social_plan", "docs", "doc", "D3 10:30", "c_tasha", "Thursday social plan - Halvorsen announcement",
     """
THURSDAY SOCIAL PLAN (Tasha, Nov. 4) - scheduled in Sprout Social
Note: Sprout shows times in the account time zone (America/New_York - set by the agency in 2024).

Facebook | Thu Nov 5, 10:00 AM EST | "Big news for kids in our region: thanks to a $20 million gift from the Halvorsen
family, Prairie Bend Health will build the Halvorsen Center for Youth Behavioral Health - 48 beds for children and
teens, close to home. prairiebendhealth.org/news/halvorsen-center" | image: rendering
Instagram | Thu Nov 5, 10:00 AM EST | same copy, shortened; carousel: rendering, Westgate site, Dr. Moreau
LinkedIn | Thu Nov 5, 10:05 AM EST | longer copy for professional audience, tags the Foundation
X | Thu Nov 5, 10:00 AM EST | "A $20 million gift will bring the region's first psychiatric hospital for children
to Prairie Bend. prairiebendhealth.org/news/halvorsen-center"
Facebook Live | manual from Westgate at program start
Moderation: Tasha on Facebook/Instagram 10 a.m.-1 p.m.; Kyle backup.
""", thread="t_chat_tasha")

item("e_d3_andrea", "email", "email", "D3 11:00", "c_andrea", "Governor's quote + our release (embargoed)",
     """
Erin - the Governor's final quote:

"Every child in crisis deserves care close to home, not a hospital hallway hours away," said Gov. Patricia Hartley.
"The Behavioral Health Capital Fund was created for exactly this kind of partnership, and I'm proud the state is part
of it."

Our release is attached, embargoed until 10 a.m. CT Thursday. See you there.

Andrea
""", to=["c_erin"], thread="t_state", attachments=["doc_d3_state_release"])

item("doc_d3_state_release", "docs", "doc", "D3 11:00", "c_andrea", "DHHS release (EMBARGOED) - Behavioral Health Capital Fund grant",
     """
EMBARGOED UNTIL 10 A.M. CT, THURSDAY, NOV. 5, 2026

Gov. Hartley announces $12 million grant for children's psychiatric hospital in Prairie Bend

The Department of Health and Human Services will award a $12 million Behavioral Health Capital Fund grant to Prairie
Bend Health for the Halvorsen Center for Youth Behavioral Health, a 48-bed inpatient psychiatric hospital for
children and teens. The fund, created by the Legislature in 2025, has awarded $41 million to nine projects.

(Governor's quote as sent.)

Contact: Andrea Lutz, Department of Health and Human Services
""", thread="t_state")

item("e_d3_karen", "email", "email", "D3 11:30", "c_karen", "Interviews this afternoon",
     """
Erin, I'm doing NewsCenter 9 at 3:00 and the Ledger at 3:30. Dana is the one writing about the woman who died in
the ER, isn't she? What do I say if she asks me about that? Should I say the hospital is wonderful? I don't want to
make it worse for anyone.

Karen
""", to=["c_erin"], cc=["c_greg"], thread="t_karen")

item("chat_d3_alicia2", "chat", "message", "D3 11:40", "c_alicia", "Teams: Alicia Brandt",
     """
Union statement approved, with one change: drop "in good faith" - Labor Relations would rather we not characterize
bargaining at all. Send it to anyone who asks.
""", to=["c_erin"], thread="t_chat_alicia")

item("chat_d3_doug", "chat", "message", "D3 12:30", "c_doug", "Teams: Doug Reinholt",
     "From the capital: saw the union statement, good. Where are we on the Haskins statement? Call me if you need me "
     "- I'm in session until 3.", to=["c_erin"], thread="t_chat_doug")

item("e_d3_union_clip", "email", "email", "D3 13:20", "c_meltwater", "Meltwater alert: Prairie Bend Health",
     """
Meltwater alert | 1:15 p.m. CT
- NewsCenter 9 at Noon (live): "Nurses rally outside PBMC over ER staffing" - includes PBH statement ("We respect
  our nurses' right to speak out..."). Tone: negative. Est. audience 48,000.
- 5 News (online, 12:40 p.m.): "Nurses: ER staffing unsafe" - "PBH said in a statement..." Tone: negative.
""", to=["c_erin", "c_doug", "c_tasha"], thread="t_digest")

item("e_d3_alicia_approve", "email", "email", "D3 13:40", "c_alicia", "APPROVED - Ledger statement; Thursday proceeds",
     """
Erin,

The statement below is approved (Steven, Rhonda and me). Please send it to Dana.

"Our hearts go out to this family. Federal privacy law does not allow us to discuss any patient's care without
written permission.

When any family raises a concern about care at Prairie Bend Medical Center, we take it seriously and review it
through our patient safety process, which includes physicians and nurses who were not involved in the care.

Our emergency department cared for 71,400 patients last year, and this year has been busier. We know waits have been
too long at times, and we are working to shorten them. Since January we have hired 22 emergency nurses, and 104 of
our 118 emergency nursing positions are filled today. We use contract nurses to cover open shifts while we recruit
for the rest."

On personnel: "We do not discuss personnel matters." Nothing on the claim.

Ray and I talked about your options memo: we proceed Thursday as planned. Ray will take the ER question at the media
availability using the Q&A language. I'll tell Greg.

Alicia
""", to=["c_erin"], cc=["c_doug", "c_steven", "c_rhonda"], thread="t_haskins_legal")

item("e_d3_dana2", "email", "email", "D3 14:55", "c_dana", "Re: Statement",
     """
Thanks, Erin. Can you at least confirm she was a patient? The family is signing the authorization this afternoon.
If not, I'll note that PBH declined to confirm she was treated there despite the family's offer.

Dana
""", to=["c_erin"], thread="t_haskins_media")

item("e_d3_ben", "email", "email", "D3 15:00", "c_ben", "Re: CEO all-staff email Thursday 10:05",
     "Still good for a draft today? Carol needs it by 5 so Dr. E can OK it tonight. Ben", to=["c_erin"],
     thread="t_internal")

item("chat_d3_kyle", "chat", "message", "D3 15:45", "c_kyle", "Teams: Kyle Brandvold",
     "B-roll done at Westgate with NewsCenter 9 and the Ledger photog. Dr. Moreau interview is cut (90 sec). Uploading "
     "to the press kit folder for 10 a.m. tomorrow.", to=["c_erin"], thread="t_chat_kyle")

item("e_d3_tom", "email", "email", "D3 17:05", "c_tom", "Haskins - claim?",
     """
Erin - sources tell me the Haskins family has hired Mark Feldner and sent PBH a notice of claim. Can you confirm? Is
PBH looking to settle? Writing for Friday's print edition.

Tom
""", to=["c_erin"], thread="t_haskins_bj")

d3["calls"].append({
    "id": "call_d3_luis", "at": "D3 09:10", "caller": "c_luis",
    "purpose": "5 News reporter excluded from embargoes presses for the embargoed release",
    "turns": [
        {"speaker": "caller", "text": "Erin, Luis at 5 News. I'm hearing you've got a big gift announcement tomorrow and "
                                      "the Ledger already has the release. Can you send it to me? I'll hold it till "
                                      "ten, I promise.", "patience_s": 20},
        {"speaker": "human", "text": "Hi Luis. The advisory went to everyone at nine, and you're welcome at Westgate - "
                                     "check-in starts at 9:15 and the program is at ten. The release goes to the whole "
                                     "list at ten."},
        {"speaker": "caller", "text": "Come on. This is about March, isn't it? I said I was sorry. My news director is "
                                      "all over me.", "patience_s": 20},
        {"speaker": "human", "text": "I appreciate that, and I know it puts you in a tough spot. After an embargo break "
                                     "it's twelve months without embargoed material, for any outlet. What I can do is "
                                     "make sure you get time with Dr. Ellison and the family at the media availability "
                                     "at 10:35."},
        {"speaker": "caller", "text": "Fine. Save me a spot by the mult box.", "patience_s": 10},
        {"speaker": "human", "text": "Will do. See you tomorrow."},
    ]})
d3["calls"].append({
    "id": "call_d3_dana", "at": "D3 15:20", "caller": "c_dana",
    "purpose": "Reporter on deadline presses for off-the-record confirmation",
    "turns": [
        {"speaker": "caller", "text": "Erin, it's Dana. I'm filing in an hour. Off the record - was she seen by a doctor "
                                      "before she collapsed?", "patience_s": 15},
        {"speaker": "human", "text": "Dana, I can't - on or off the record. The statement is everything we can say. I "
                                     "know that's frustrating."},
        {"speaker": "caller", "text": "The family is signing the authorization today. Why won't you talk then?",
         "patience_s": 20},
        {"speaker": "human", "text": "We've considered the offer, and the statement is our response. You can say the "
                                     "family offered an authorization and that we declined to discuss her care."},
        {"speaker": "caller", "text": "Okay. Will Dr. Ellison take questions about it tomorrow?", "patience_s": 20},
        {"speaker": "human", "text": "He'll be at the media availability after the program, at 10:35, and he'll take "
                                     "questions."},
        {"speaker": "caller", "text": "Got it. Thanks.", "patience_s": 10},
    ]})

act(d3, "a3_01", "D3 08:45", "send", None,
    """
Carol - Dr. Ellison's remarks for Thursday (about 340 words, a little over 3 minutes at his pace):

Good morning, and thank you for being here.

Last year, 312 children and teenagers from our region spent days in our emergency department - on average, more than
two and a half days - waiting for a psychiatric bed. Most of them eventually traveled 190 miles or more for care,
away from their parents, their schools and their friends, at the moment they most needed all three.

Our nurses and doctors do everything they can for those kids. But an emergency department is not where a child in
crisis should spend the weekend.

Today that starts to change.

I am proud to announce that the Halvorsen Family Foundation has committed $20 million to Prairie Bend Health - the
largest gift in our 112-year history - to build the Halvorsen Center for Youth Behavioral Health right here on our
Westgate campus.

The center will have 48 beds: 32 for teens and 16 for younger children. It will also have a day program that can
serve 24 young people at a time, so many kids can get intensive care and still sleep in their own beds. It will be
the only inpatient psychiatric unit for children within 190 miles. We expect to break ground in spring 2027 and open
in fall 2028, with about 175 new jobs.

This is a $64 million project, and it takes partners. Thank you to the Halvorsen family. Thank you to Gov. Hartley
and the Legislature for the Behavioral Health Capital Fund grant of $12 million. Prairie Bend Health is investing $28
million, and our Foundation will raise $4 million from this community - a campaign that starts today.

Karen, you and your family have turned the hardest thing a parent can face into hope for families you will never
meet. Thank you for trusting us with Eli's name.

To the parents in this room who have sat in a waiting room at 2 a.m. with a child who is not safe: we hear you, and
help is coming closer to home.

It is my privilege to introduce Karen Halvorsen Doyle.
""", "Speechwriting for the CEO, ahead of his 9:15 read; uses the current $64M figures.", to=["c_carol"],
    subject="Dr. Ellison's remarks - Thursday")
act(d3, "a3_02", "D3 09:00", "send", None,
    """
MEDIA ADVISORY

Prairie Bend Health to make major announcement on mental health care for children and teens

WHAT: Prairie Bend Health will announce a major investment in mental health care for children and teens in the
region.
WHO: Dr. Raymond Ellison, president and CEO, Prairie Bend Health; Gov. Patricia Hartley; Dr. Kathleen Moreau, vice
president, behavioral health services; community leaders.
WHEN: 10 a.m. Thursday, Nov. 5. Media check-in begins at 9:15 a.m.; optional b-roll walk of the building site at 9:30
a.m.
WHERE: Westgate Community Room, Prairie Bend Health Westgate Campus, 2200 Westgate Road, Prairie Bend. Media parking
in Lot B by the north entrance.
INTERVIEWS: Media availability at 10:35 a.m.; the Governor is available until 10:50 a.m.
CONTACT: Erin Lindqvist, 555-0143, erin.lindqvist@prairiebendhealth.org
""", "Advisory v2 to the full list at 9:00 as planned; no donor name or amount.",
    to=["c_medialist"], subject="MEDIA ADVISORY: Prairie Bend Health announcement Thursday, 10 a.m.")
act(d3, "a3_03", "D3 09:30", "edit_doc", "doc_qa",
    """
Q&A v2, Q4 (staffing): replaced "our emergency department nursing vacancy rate is under 8% (June 2026)" with "As of
this week, 104 of our 118 emergency nursing positions are filled (14 open), and we have hired 22 emergency nurses
since January." Q2 now "$64 million ... and a $4 million Foundation community campaign."
""", "Replaces the stale June vacancy figure with the CNO's Nov. 2 numbers (14 open = 11.9%).")
act(d3, "a3_04", "D3 09:40", "reply", "e_d3_luis",
    """
Luis - as I said on the phone, I can't share details before 10 a.m. tomorrow, including the amount. The advisory is
attached, and I'll save you a spot by the mult box for the 10:35 availability.

Erin
""", "Holds the embargo with an excluded outlet; confirms nothing.", to=["c_luis"])
act(d3, "a3_05", "D3 10:30", "edit_doc", "doc_qa",
    """
Q&A v2, new Q11-Q13:

11. A family says their mother died after waiting six hours in your emergency department. Why build a new building
when your ER can't keep up?
Our hearts go out to that family. Federal privacy law does not allow us to discuss any patient's care. When any
family raises a concern, we review it through our patient safety process. Our emergency department cared for 71,400
patients last year; we know waits have been too long at times, and we are working on it - we have hired 22
emergency nurses since January. This center helps the emergency department too: children waiting days for a
psychiatric bed will have a place to go.

12. Was the nurse disciplined?
We do not discuss personnel matters.

13. Is the family suing? Will you settle?
Bridge: "I can't discuss any patient's care. What I can tell you is what we are doing about emergency department
waits..." (Do not mention any claim, letter or attorney.)
""", "Connects Tuesday's Ledger inquiry to Thursday's Q&A; uses only approved language.")
act(d3, "a3_06", "D3 11:05", "send", None,
    """
Alicia - draft statement for the PBNA news conference at noon (Jessica Ruiz asked):

"We respect our nurses' right to speak out, and we share their commitment to safe care for every patient. We are
bargaining in good faith with the Prairie Bend Nurses Association and believe the bargaining table is the right place
to work through our differences. Federal privacy law does not allow us to discuss any patient's care. Since January
we have hired 22 emergency nurses, and 104 of our 118 emergency nursing positions are filled today. We use contract
nurses to cover open shifts while we recruit for the rest."

Erin
""", "Drafts the union response for approval; reuses approved staffing language.", to=["c_alicia"],
    subject="Draft: statement on PBNA news conference")
act(d3, "a3_07", "D3 11:50", "reply", "e_d3_jessica_union",
    """
Jessica - here's our statement:

"We respect our nurses' right to speak out, and we share their commitment to safe care for every patient. We are
bargaining with the Prairie Bend Nurses Association and believe the bargaining table is the right place to work
through our differences. Federal privacy law does not allow us to discuss any patient's care. Since January we have
hired 22 emergency nurses, and 104 of our 118 emergency nursing positions are filled today. We use contract nurses to
cover open shifts while we recruit for the rest."

Erin Lindqvist, Prairie Bend Health
""", "Sends the approved statement with Labor Relations' edit.", to=["c_jessica"])
act(d3, "a3_08", "D3 12:15", "send", None,
    """
Alicia - options for Thursday, given the Ledger's Haskins story is likely online early Thursday:

A. Proceed as planned (my recommendation). The embargo is set with four outlets, the Governor's schedule is fixed,
and the family is ready. Ray takes the ER question at the 10:35 availability with Q&A 11-13. Risk: some stories pair
the two; we can live with that, and the center is part of the ER answer.
B. Proceed, but have Ray address ER waits in his remarks. Risk: it puts the Haskins story in the lead of our own
announcement and strains what Legal will allow.
C. Postpone. Four outlets already hold the embargoed release and the Governor would have to move; the embargo would be
hard to keep for another week, and postponing the morning the story runs would look like hiding. It would also hurt
the family.

Nothing has gone to Greg or the family. Erin
""", "Gives the decision-makers options; does not decide or tell the Foundation.", to=["c_alicia"],
    subject="Thursday options")
act(d3, "a3_09", "D3 12:30", "edit_doc", "doc_release",
    """
Release v5: added the Governor's final quote (Andrea, 11:00) and Karen's approved quote: "Our son Eli fought hard for
years, and too often the help he needed was three hours away," ... Grant sentence now "a $12 million grant from the
state's Behavioral Health Capital Fund, created by the Legislature in 2025."
""", "Final release.")
act(d3, "a3_10", "D3 12:40", "send", None,
    "(To Dana, Hannah, Jessica and Tom, separately.) Final embargoed release attached with the Governor's quote. Still "
    "EMBARGOED UNTIL 10:00 A.M. CT THURSDAY. Erin", "Final version only to agreed reporters.",
    to=["c_dana", "c_hannah", "c_jessica", "c_tom"], subject="EMBARGOED - final release with Governor's quote")
act(d3, "a3_11", "D3 14:00", "reply", "e_d3_karen",
    """
Karen, you'll be great. A few things that help:

- Your story is the reason this is happening. Talk about Eli, the drive to get him care, and what this means for
  families. Share only what you want to; nothing is ever really off the record.
- If Dana or anyone asks about the woman who died in the ER, it's fine to say: "I don't know anything about that, and
  my heart goes out to her family. That's a question for the hospital." Then come back to why you're here. You don't
  need to defend the hospital - that's our job.
- It's OK to pause, and OK to say "I'd rather not talk about that."
- Remember both reporters agreed to hold the story until 10 tomorrow.

I'll be on the line for the 4:30 prep call, and I'm at Westgate if you'd like me in the room for the interviews.

Erin
""", "Coaches a donor spokesperson before her interviews; keeps her out of the ED story.", to=["c_karen"])
act(d3, "a3_12", "D3 14:45", "reply", "e_d2_dana_ed",
    """
Dana - here is Prairie Bend Health's statement:

"Our hearts go out to this family. Federal privacy law does not allow us to discuss any patient's care without
written permission.

When any family raises a concern about care at Prairie Bend Medical Center, we take it seriously and review it
through our patient safety process, which includes physicians and nurses who were not involved in the care.

Our emergency department cared for 71,400 patients last year, and this year has been busier. We know waits have been
too long at times, and we are working to shorten them. Since January we have hired 22 emergency nurses, and 104 of
our 118 emergency nursing positions are filled today. We use contract nurses to cover open shifts while we recruit
for the rest."

On your question about staff: we do not discuss personnel matters. For emergency department measures, PBMC's
publicly reported data is on CMS Care Compare.

Erin
""", "Sends the approved statement before the 3 p.m. deadline; no name, no confirmation, nothing on the claim.",
    to=["c_dana"])
act(d3, "a3_13", "D3 15:30", "reply", "e_d3_ben",
    """
Ben (cc Carol) - draft all-staff email from Dr. Ellison, Thursday 10:05 a.m.:

Subject: A $20 million gift for children's mental health

Colleagues,

This morning I announced that the Halvorsen Family Foundation has given $20 million - the largest gift in our
history - to build the Halvorsen Center for Youth Behavioral Health on our Westgate campus: 48 beds for children and
teens and a day program for 24 more, opening in fall 2028.

Many of you have cared for children who waited days in our emergency department for a psychiatric bed hours away.
Last year there were 312 of them. Thank you for that care. This center is how we stop asking kids and families to
wait.

The project is $64 million, with a $12 million state grant, $28 million from Prairie Bend Health and a $4 million
community campaign through our Foundation. You'll hear more about how to be part of it.

If a reporter contacts you, please refer them to Media Relations at 555-0100.

Raymond Ellison, MD
""", "Internal announcement timed with the embargo; reminds staff to route media calls.", to=["c_ben", "c_carol"])
