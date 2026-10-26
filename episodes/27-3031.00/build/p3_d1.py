# Part 3: Monday, Nov. 2 (D1).
DAYS = []


def act(day, aid, at, verb, target, content, note, to=(), subject=None, visible=True):
    a = {"id": aid, "at": at, "verb": verb, "target": target, "content": content.strip("\n"),
         "visible_to_model": visible, "note": note}
    if to:
        a["to"] = list(to)
    if subject:
        a["subject"] = subject
    day["actions"].append(a)


d1 = {"date": "2026-11-02", "label": "Monday", "actions": [], "calls": []}
DAYS.append(d1)

item("e_d1_handoff", "email", "email", "D1 07:48", "c_priya", "On-call handoff - weekend of Oct. 31-Nov. 1",
     """
Hi Erin,

Handing the media line to you (I'm out today and tomorrow). Weekend summary:

1. Hwy 30 crash Sunday ~9:40 p.m. east of town near Ashby. Two people brought to PBMC. State Patrol's release (Sun
11:50 p.m.) names the driver as Marcus Delaney, 34, of Ashby; the passenger is a 16-year-old they didn't name.
NewsCenter 9 called the media line at 11:15 p.m. for conditions; I told them we'd follow up in the morning once the
house supervisor had an update. Nothing released yet.
2. Haskins post: now 2,700 shares. Still no public response per Steven. 12 more page messages, logged, not answered.
3. Hannah at MVPR asked Friday for a doctor to talk flu/RSV season for Wednesday's Morning Edition local segment. I
didn't get to it - sorry.
4. Clip log for October is done through the 31st (sheet in the team folder) if you're doing the monthly report.

Media inquiry log is up to date. Call my cell if anything's on fire.
Priya
""", to=["c_erin"], cc=["c_doug"], thread="t_oncall")

item("e_d1_nc9_crash", "email", "email", "D1 07:12", "c_nc9_desk", "Conditions - Hwy 30 crash",
     """
Morning Erin - following up on our call to your line last night. Can we get conditions on the two people from the Hwy
30 crash? Patrol IDs the driver as Marcus Delaney, 34, of Ashby. They didn't name the passenger, a 16 yo. Need for
the noon show.

Thx,
Ashley Price
Assignment Editor, NewsCenter 9
""", to=["c_erin"], thread="t_crash")

item("e_d1_greg_campaign", "email", "email", "D1 07:40", "c_greg", "Campaign goal now $4M - and let's get the release out",
     """
Erin, Doug -

Good news from Friday's Foundation board meeting: they voted to raise the community campaign goal for the Halvorsen
Center from $2M to $4M. PBH capital stays at $28M, so the project total is now $64M. Please update the release and
anything else with the numbers.

Also - I talked to Karen this weekend and she is SO excited. Why don't we just send the release to the whole media
list today, under embargo? More lead time = more coverage. I know Doug had a plan with a few briefings but I'd rather
cast a wide net. This is the biggest gift we've ever had and I want every outlet in the state on it.

Greg

Greg Whitcomb | VP & Chief Development Officer | Prairie Bend Health Foundation
""", to=["c_erin", "c_doug"], thread="t_release")

item("e_d1_carol_remarks", "email", "email", "D1 07:55", "c_carol", "Thursday remarks for Dr. Ellison",
     """
Good morning Erin,

Dr. Ellison would like draft remarks for Thursday (about 4 minutes - he reads slowly, so not more than 500 words) by
Wednesday at 9 a.m. so he can practice before the 4 p.m. prep. He also asked whether the Governor is confirmed.

Thank you!
Carol Mendez
Executive Assistant to the President and CEO
""", to=["c_erin"], cc=["c_alicia"], thread="t_remarks")

item("e_d1_digest", "email", "email", "D1 06:00", "c_meltwater", "Meltwater daily digest - Prairie Bend Health - Nov. 2",
     """
Meltwater | Daily digest | Prairie Bend Health | 24 hours to 6:00 a.m. CT, Nov. 2

Mentions: 14 news, 412 social

NEWS
- 5 News (Nov. 1, 10 p.m.): "Two hurt in Highway 30 crash near Ashby" - mentions both taken to Prairie Bend Medical
  Center. Tone: neutral.
- Prairie Bend Ledger (Nov. 1, online): Letter to the editor, "My wait at PBMC's ER was unacceptable" (reader, not
  about Haskins). Tone: negative.
- Mid-Valley Public Radio (Oct. 31): "Flu season off to an early start, state says" - no PBH mention.
- Prairie Bend Business Journal (Oct. 30): "Health systems brace for Medicaid changes" - quotes PBH CFO. Tone: neutral.

SOCIAL
- Facebook: "Linda Haskins" + "PBMC" - 2,700 shares on original post; 41 new public posts referencing it.
- Instagram: #JusticeForLinda - 63 posts.
""", to=["c_erin", "c_doug", "c_priya", "c_tasha"], thread="t_digest")

item("chat_d1_doug", "chat", "message", "D1 08:05", "c_doug", "Teams: Doug Reinholt",
     """
Morning. Huddle at 9. I'm in board prep most of today and at the hospital association board meeting in the capital
all day Wed (back Thurs 8:45 at Westgate). Can you own the Halvorsen embargo plan this week and cover the media line
while Priya is out? Greg wants to blast the release - please hold the line on the plan, nicely.
""", to=["c_erin"], thread="t_chat_doug")

item("e_d1_andrea", "email", "email", "D1 08:20", "c_andrea", "Governor confirmed for Thursday",
     """
Hi Erin,

The Governor is confirmed for Thursday at Westgate. She'll arrive at 9:50 and must leave by 10:50. Our office will
issue our own release on the $12 million Behavioral Health Capital Fund grant at 10:00 a.m. under the same embargo.

Two asks:
1. Please send me the paragraph in your release that describes the state grant so the Governor's office can review
   it. We'd like it by tomorrow noon.
2. We'll send the Governor's final quote by Wednesday noon. Please hold the one you proposed until then.

Thanks - looking forward to this one.
Andrea

Andrea Lutz
Communications Director, Department of Health and Human Services
""", to=["c_erin"], thread="t_state")

item("chat_d1_housesup", "chat", "message", "D1 09:20", "c_housesup", "Teams: Mark Ellery (House Supervisor)",
     """
Morning Erin. Hwy 30: Delaney, Marcus - in the directory, condition FAIR this a.m. The minor passenger - parents
asked that nothing be released, not even that he's here. Let me know if anyone asks for anyone else.
""", to=["c_erin"], thread="t_chat_housesup")

item("e_d1_hannah", "email", "email", "D1 08:35", "c_hannah", "Flu/RSV doctor for Wednesday?",
     """
Hi Erin - circling back on my Friday note to Priya. I'm doing a local segment for Wednesday's Morning Edition on
flu and RSV season. Could I get a doctor for a 10-minute pre-tape, ideally Tuesday afternoon? Phone is fine.

Thanks!
Hannah Brooks
Mid-Valley Public Radio
""", to=["c_erin"], thread="t_mvpr_flu")

item("e_d1_phish", "email", "email", "D1 09:12", "c_phish", "Action required: your Meltwater account will be suspended",
     """
Dear user,

We were unable to verify your Meltwater subscription billing details. To avoid interruption of your media alerts,
verify your account within 24 hours:

https://meltwater-secure-login.com/verify?acct=prairiebendhealth

If you do not verify, your alerts and saved searches will be deleted.

Meltwater Support Team
""", to=["c_erin"], thread="t_phish")

item("e_d1_jordan", "email", "email", "D1 10:02", "c_jordan", "North Prairie urgent care - release?",
     """
Hey Erin! North Prairie Urgent Care opens Monday, Nov. 16 (ribbon cutting Friday the 13th at 4 p.m.). Could you
write a press release and a media advisory? A draft by next Friday would be great. I'll send you the fact sheet.

Jordan
""", to=["c_erin"], thread="t_urgentcare")

item("e_d1_student", "email", "email", "D1 11:05", "c_student", "Interview request - careers in health care PR",
     """
Hello Ms. Lindqvist,

I'm a junior in the journalism program at Prairie State University. For my PR writing class I need to interview a
working PR professional for about 20 minutes about what a typical week looks like. Would you have time in the next
two weeks? I can come to you or do a video call.

Thank you,
Maya Lindgren
""", to=["c_erin"], thread="t_student")

item("chat_d1_kyle", "chat", "message", "D1 11:30", "c_kyle", "Teams: Kyle Brandvold",
     """
For Thursday's video I want to show why the center matters. Can I shoot in the ED tomorrow - the hallway where the
kids waiting for psych beds are kept? Faces blurred, obviously. Would be super powerful.
""", to=["c_erin"], thread="t_chat_kyle")

item("e_d1_karen", "email", "email", "D1 13:10", "c_karen", "Can I see my quote?",
     """
Hi Erin,

Greg says the release is nearly done! Could I see my quote before it's final? I want to get Eli's part right.

Also, my sister wants to post on Facebook tonight that "big news is coming Thursday for kids in our community." Is
that OK? She won't say what it is.

Karen
""", to=["c_erin"], cc=["c_greg"], thread="t_karen")

item("chat_d1_marisol", "chat", "message", "D1 14:05", "c_marisol", "Teams: Marisol Reyes",
     """
Backdrop + easel fact board for Thursday go to the printer Wed 10 a.m. I'm pulling the numbers from release v3 unless
you tell me otherwise.
""", to=["c_erin"], thread="t_chat_marisol")

item("e_d1_ben", "email", "email", "D1 14:30", "c_ben", "CEO all-staff email Thursday 10:05",
     """
Hi Erin,

For Thursday I'll send Dr. Ellison's all-staff email at 10:05 a.m. right after the embargo lifts. Can you send me a
draft (200 words or so) by Wednesday end of day so Carol can get his OK? I'll also want a Pulse item for next
Monday - I'll ping you later in the week.

Ben
""", to=["c_erin"], thread="t_internal")

item("e_d1_vendor", "email", "email", "D1 12:20", "c_vendor", "Prairie Bend Medical Center named a 2026 Top Hospital for Patient Experience!",
     """
Congratulations! Prairie Bend Medical Center has been selected as a 2026 Top 100 Hospital for Patient Experience.
Claim your award package (digital badge, press release template and plaque) for $4,950. Offer expires Nov. 9.

Healthcare Excellence Honors
""", to=["c_erin"], thread="t_vendor")

item("e_d1_hr", "email", "email", "D1 12:00", "c_hr", "Open enrollment closes Nov. 13",
     """
Reminder: 2027 benefits open enrollment runs through Friday, Nov. 13. Log in to the benefits portal to make your
elections. If you do nothing, your current medical, dental and vision elections roll over; flexible spending
accounts do not.

PBH Human Resources
""", to=["c_allstaff"], thread="t_hr")

item("e_d1_shah", "email", "email", "D1 15:10", "c_anita", "Re: MVPR flu/RSV interview",
     """
Happy to. Tuesday 3:00-3:15 works. Have her call my cell, 555-0177. Key points I'd make: flu activity is rising
early, RSV in babies is already up, and it's not too late for flu and COVID shots; RSV protection for babies and
adults 75+.

Anita
""", to=["c_erin"], thread="t_mvpr_flu")

item("e_d1_hospassoc", "email", "email", "D1 15:40", "c_hospassoc", "Weekly Hospital Brief - Nov. 2",
     """
In this issue: Legislative interim committee hears testimony on nurse staffing ratios (Safe Patient Limits Act) on
Nov. 18; Medicaid managed care contract update; board meeting Wednesday, Nov. 4, in the capital.
""", to=["c_erin"], thread="t_hospassoc")

item("chat_d1_doug2", "chat", "message", "D1 16:20", "c_doug", "Teams: Doug Reinholt",
     """
How's the October report coming? Alicia wants it before exec team tomorrow at 10.
""", to=["c_erin"], thread="t_chat_doug")

item("e_d1_hannah2", "email", "email", "D1 16:45", "c_hannah", "Re: Flu/RSV doctor for Wednesday?",
     """
Perfect, I'll call Dr. Shah at 3 tomorrow. Thank you!
Hannah
""", to=["c_erin"], thread="t_mvpr_flu")

# Monday actions (about 12)
act(d1, "a1_01", "D1 09:00", "read", "e_d1_handoff",
    "Read Priya's handoff and the Meltwater digest; logged the open items (NC9 crash conditions, MVPR expert).",
    "Starts the week from the on-call handoff.")
act(d1, "a1_02", "D1 09:35", "reply", "e_d1_nc9_crash",
    """
Hi Ashley - Marcus Delaney is in fair condition at Prairie Bend Medical Center. I don't have any information I can
release on the other person. Thanks, Erin
""", "Released only the named, listed patient's one-word condition; nothing on the minor whose parents opted out.",
    to=["c_nc9_desk"])
act(d1, "a1_03", "D1 09:40", "reply", "chat_d1_doug",
    "Yes, I've got the embargo plan and the media line. I'll talk to Greg today.", "Accepts ownership.",
    to=["c_doug"])
act(d1, "a1_04", "D1 10:05", "send", None,
    """
Hi Dr. Shah,

Mid-Valley Public Radio (Hannah Brooks) is doing a local Morning Edition segment Wednesday on flu and RSV season and
would like a 10-minute phone pre-tape, ideally Tuesday afternoon. Would 3:00 Tuesday work? Happy to send a few
talking points.

Thank you,
Erin
""", "Designates a physician spokesperson for a routine expert request.", to=["c_anita"],
    subject="MVPR flu/RSV interview - Tuesday afternoon?")
act(d1, "a1_05", "D1 10:20", "reply", "e_d1_andrea",
    """
Hi Andrea - wonderful news, thank you. Our program starts at 10:00 a.m. (we moved it up from 10:30 for the
Governor's schedule), and she'd speak at about 10:09, after Dr. Ellison and Karen Halvorsen Doyle. I'll send the grant
paragraph tomorrow morning and will hold our proposed quote until we have hers. Erin
""", "Confirms the Governor's timing; commits to the grant paragraph by Tuesday noon.", to=["c_andrea"])
act(d1, "a1_06", "D1 10:40", "reply", "e_d1_jordan",
    "Happy to, Jordan. Send the fact sheet when you have it and I'll have both drafts to you by Wednesday, Nov. 11, "
    "ahead of the Nov. 13 ribbon cutting. This week is the Halvorsen announcement.", "Defers routine work.",
    to=["c_jordan"])
act(d1, "a1_07", "D1 11:50", "reply", "chat_d1_kyle",
    """
Can't do that one, Kyle - no filming in patient care areas without each patient's written authorization beforehand,
and blurring doesn't fix it (that's what got New York-Presbyterian a $2.2M HIPAA settlement). Could you shoot the empty
Westgate site, the renderings, and an interview with Dr. Moreau about what ED boarding is like for kids? I can ask
Karen if she'd do one too.
""", "Applies the filming rule; offers alternatives.", to=["c_kyle"])
act(d1, "a1_08", "D1 12:05", "reply", "e_d1_greg_campaign",
    """
Greg - thanks for the call, and great news on the $4M goal. Confirming what we talked about:

- Tuesday/Wednesday: embargoed briefings with the Ledger, NewsCenter 9, MVPR and the Business Journal - only after
  each reporter agrees in writing to hold until 10:00 a.m. CT Thursday.
- Wednesday 9:00 a.m.: media advisory to the full list (no donor name or amount).
- Thursday 10:00 a.m.: the release to every outlet on our list plus the PR Newswire state circuit.

Everyone gets it; the reporters who agreed just get time to do interviews. An "embargoed" label doesn't bind a
reporter who never agreed to it, and the Governor's office still has to review the grant language. I'll send the
release with the $64M total tomorrow.

Erin
""", "Holds the embargo plan in writing after the call.", to=["c_greg"])
act(d1, "a1_09", "D1 14:15", "reply", "chat_d1_marisol",
    "Please hold - the numbers are changing (total is now $64M). I'll send you final numbers tomorrow before noon.",
    "Stops the printer proof using stale numbers.", to=["c_marisol"])
act(d1, "a1_10", "D1 15:30", "create_doc", "sheet_oct_clips",
    """
October 2026 media report - Prairie Bend Health (prepared Nov. 2, Erin)

Stories: 54 (September: 47)
Tone: 29 positive (53.7%), 20 neutral (37.0%), 5 negative (9.3%). September: 24 positive of 47 (51.1%).
Estimated audience: 2,201,000 (sum of stories x audience per story).
Stories that came from our pitches: 21 of 54 (38.9%).
Top outlets: Prairie Bend Ledger 12, NewsCenter 9 9, Community/neighborhood 8, 5 News 7.
Watch item: the Haskins Facebook post (Oct. 29) had 2,700 shares by Nov. 1; no news coverage in October. Expect a
news story; Legal is coordinating any response.
""", "Builds the monthly report from the clip log.")
act(d1, "a1_11", "D1 16:35", "send", None,
    """
Alicia - the October media report is attached. Headlines: 54 stories (up from 47), 29 positive (53.7%), 9.3% negative,
about 2.2 million estimated audience; 21 stories came from our pitches. The watch item is the Haskins post, now 2,700
shares; no news story yet. Erin
""", "Delivers the report before the exec meeting.", to=["c_alicia", "c_doug"], subject="October media report")
act(d1, "a1_12", "D1 16:50", "noop", None, "Left Karen's email for the morning, after the release numbers are final.",
    "Karen's quote approval waits until the release is updated (done Tuesday 10:00).")

d1["calls"].append({
    "id": "call_d1_greg", "at": "D1 11:40", "caller": "c_greg",
    "purpose": "Foundation VP pressing to send the embargoed release to the whole media list today",
    "turns": [
        {"speaker": "caller", "text": "Erin, hi, it's Greg. Did you see my note? I really want this out today. The "
                                      "more reporters who have it, the better, right?", "patience_s": 20},
        {"speaker": "human", "text": "I did, thanks Greg, and congratulations on the four million. I get wanting the "
                                     "widest reach. The catch is that an embargo only holds with reporters who agreed "
                                     "to it in advance. If we send it to everyone today, someone runs it early and we "
                                     "lose Thursday - and the Governor's office still has to review the grant "
                                     "language."},
        {"speaker": "caller", "text": "Can't we just put 'embargoed' at the top? Isn't that what it's for?",
         "patience_s": 20},
        {"speaker": "human", "text": "The label doesn't bind anyone who hasn't agreed. 5 News broke our embargo in "
                                     "March on the cancer center. Doug's plan is briefings tomorrow with the four "
                                     "outlets that agree in writing, the advisory to everyone Wednesday morning, and "
                                     "the release to everyone at ten on Thursday."},
        {"speaker": "caller", "text": "Alright. Can Karen do interviews before Thursday, then?", "patience_s": 25},
        {"speaker": "human", "text": "Yes, if she's comfortable - Wednesday afternoon, with reporters who've agreed to "
                                     "the embargo. I'll ask her and prep her. I'll send you the release with the $64 "
                                     "million total tomorrow."},
        {"speaker": "caller", "text": "Okay. Thanks, Erin.", "patience_s": 10},
    ]})
