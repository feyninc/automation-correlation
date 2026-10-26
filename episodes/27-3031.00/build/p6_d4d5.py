# Part 6: Thursday, Nov. 5 (D4) and Friday, Nov. 6 (D5).
d4 = {"date": "2026-11-05", "label": "Thursday (announcement, embargo lifts 10:00 a.m. CT)", "actions": [], "calls": []}
DAYS.append(d4)

item("e_d4_ledger_alert", "email", "email", "D4 06:15", "c_meltwater", "Meltwater alert: Prairie Bend Ledger",
     """
Meltwater alert | 6:12 a.m. CT
Prairie Bend Ledger (online, 6:00 a.m.): "Family says mother waited six hours in PBMC ER before she collapsed" by
Dana Whitfield. Tone: negative. Est. audience 61,000.
Excerpt: "...In a statement, Prairie Bend Health said federal privacy law does not allow it to discuss any patient's
care without written permission. The family offered to sign an authorization; the health system declined to discuss
her care. 'We know waits have been too long at times,' the statement said, adding that 104 of 118 emergency nursing
positions are filled... On Wednesday, nurses rallied outside the hospital... The story comes on the day Prairie Bend
Health has said it will make a major announcement about children's mental health care."
""", to=["c_erin", "c_doug", "c_tasha"], thread="t_digest")

item("e_d4_digest", "email", "email", "D4 07:00", "c_meltwater", "Meltwater daily digest - Prairie Bend Health - Nov. 5",
     """
Meltwater | Daily digest | Prairie Bend Health | 24 hours to 7:00 a.m. CT, Nov. 5

Mentions: 16 news, 1,240 social
NEWS: Ledger Haskins story (6:00 a.m.); NewsCenter 9 and 5 News union rally (Nov. 4); Business Journal (Nov. 4,
5:30 p.m.): "Nurses' contract talks continue as rally targets ER staffing."
SOCIAL: Ledger story shared 1,100 times on Facebook by 7 a.m.; #JusticeForLinda 210 posts.
""", to=["c_erin", "c_doug", "c_priya", "c_tasha"], thread="t_digest")

item("chat_d4_doug", "chat", "message", "D4 07:40", "c_doug", "Teams: Doug Reinholt",
     "On the road, at Westgate by 8:45. Read the Ledger piece - fair, and our statement holds up. Nice work.",
     to=["c_erin"], thread="t_chat_doug")

item("chat_d4_tasha", "chat", "message", "D4 07:55", "c_tasha", "Teams: Tasha Greene",
     "Final check - all posts are scheduled for 10 and I'll be on Facebook all morning for comments. Anything else?",
     to=["c_erin"], thread="t_chat_tasha")

item("e_d4_mike", "email", "email", "D4 08:30", "c_mike", "Today",
     "Erin - we'll have Dana and a photographer at Westgate at 10. Any update to your statement on the ER story? Mike",
     to=["c_erin"], thread="t_haskins_media")

item("chat_d4_housesup", "chat", "message", "D4 09:30", "c_housesup", "Teams: Mark Ellery (House Supervisor)",
     "FYI Delaney (Hwy 30) discharged this morning. Nothing else for the media line.", to=["c_erin"],
     thread="t_chat_housesup")

item("e_d4_ceo_allstaff", "email", "email", "D4 10:05", "c_ceo", "A $20 million gift for children's mental health",
     """
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
""", to=["c_allstaff"], thread="t_internal")

item("e_d4_nc9_desk", "email", "email", "D4 10:40", "c_nc9_desk", "B-roll and release",
     "Can you send the release and the b-roll link? Jessica's feeding from the site. - Ashley, NC9 desk",
     to=["c_erin"], thread="t_crash")

item("chat_d4_tasha2", "chat", "message", "D4 11:30", "c_tasha", "Teams: Tasha Greene",
     """
Facebook post is doing great (900 reactions) but about 40 of the 180 comments are about the ER story - "fix your ER
before you build buildings," "#JusticeForLinda," one from someone who says she's Linda's niece. How do you want me to
respond? Should I hide them?
""", to=["c_erin"], thread="t_chat_tasha")

item("e_d4_jessica", "email", "email", "D4 11:45", "c_jessica", "On-camera with Dr. Ellison re: ER story?",
     """
Erin - thanks for today. My desk wants a separate sit-down with Dr. Ellison this afternoon about ER waits and the
Haskins family, for the 6 p.m. Could he do 15 minutes at 2:30?

Jessica
""", to=["c_erin"], thread="t_nc9_ceo")

item("e_d4_karen", "email", "email", "D4 12:30", "c_karen", "Thank you",
     """
Erin, thank you for everything this week. I was so nervous and you made it easy. Could I get some of the photos -
especially the one with my parents and the rendering? My mother wants to frame it.

Karen
""", to=["c_erin"], cc=["c_greg"], thread="t_karen")

item("e_d4_hannah", "email", "email", "D4 13:05", "c_hannah", "Two quick questions for the 4:30 story",
     """
Erin - for my All Things Considered piece (deadline 4 p.m.): (1) what does the center cost per bed? (2) your release
says 312 kids waited in the ER - how many are waiting right now?

Hannah
""", to=["c_erin"], thread="t_mvpr_flu")

item("e_d4_clips1", "email", "email", "D4 13:30", "c_meltwater", "Meltwater alert: Halvorsen Center coverage (9)",
     """
Meltwater alert | 1:25 p.m. CT | search "Halvorsen Center" OR ("Prairie Bend Health" AND gift)
1. Prairie Bend Ledger (online, 10:12 a.m.): "Halvorsen family gives $20 million for children's psychiatric hospital"
   - positive - est. audience 61,000 - also mentions the ER story (one paragraph)
2. NewsCenter 9 at Noon - positive - 48,000
3. 5 News at Noon - positive - 41,000 - also mentions the ER story
4. Mid-Valley Public Radio (online) - positive - 22,000
5. Prairie Bend Business Journal (online): "How PBH will pay for its $64M youth psychiatric center" - neutral - 9,500
6. State Capitol News Service: "Hartley, two days after re-election, touts behavioral health grants" - positive -
   35,000
7. NewsCenter 9 (web story) - positive - 30,000
8. WestSide Neighbors (online newsletter) - positive - 4,000
9. Prairie Bend Parent (online) - positive - 6,000
""", to=["c_erin", "c_doug", "c_tasha"], thread="t_clips")

item("e_d4_greg", "email", "email", "D4 14:00", "c_greg", "WOW",
     """
Erin - what a day. Karen was in tears (good ones). Can you put together a coverage summary for the Foundation board
packet? Board meets Monday 7:30 a.m., so I need it by Friday noon. Number of stories, audience, highlights.

Greg
""", to=["c_erin"], cc=["c_doug", "c_alicia"], thread="t_release")

item("e_d4_andrea", "email", "email", "D4 15:10", "c_andrea", "Thank you!",
     "Lovely event. The Governor's office would like photos and a list of coverage for their weekly report. "
     "Tomorrow is fine. Andrea", to=["c_erin"], thread="t_state")

item("chat_d4_lisa", "chat", "message", "D4 15:30", "c_lisa", "Teams: Lisa Harmon",
     "FYI only - PBNA told Labor Relations they'll do informational picketing Nov. 18, the day of the staffing "
     "hearing. Not public yet.", to=["c_erin"], thread="t_union")

item("e_d4_ben", "email", "email", "D4 16:00", "c_ben", "Pulse item by Friday 2 p.m.",
     "Hi Erin - could I get 150 words and a photo on the Halvorsen announcement for Monday's Pulse, by 2 p.m. "
     "Friday? Ben", to=["c_erin"], thread="t_internal")

item("e_d4_clips2", "email", "email", "D4 16:30", "c_meltwater", "Meltwater alert: Halvorsen Center coverage (5)",
     """
Meltwater alert | 4:25 p.m. CT
10. NewsCenter 9 at 5 - positive - 52,000 - also mentions the ER story
11. 5 News at 6 (preview online) - neutral - 44,000 - also mentions the ER story
12. Mid-Valley Public Radio, All Things Considered local (preview online) - positive - 25,000
13. Prairie Bend Ledger (online, 3:40 p.m.): "Hartley touts behavioral health fund at Prairie Bend event" - positive -
    61,000
14. Tri-County 12 News at 5 - positive - 18,000
""", to=["c_erin", "c_doug", "c_tasha"], thread="t_clips")

item("e_d4_luis", "email", "email", "D4 17:10", "c_luis", "Thanks",
     "Got good stuff at the availability, thanks for the spot. We ran it at noon and we'll have it at 6. - Luis",
     to=["c_erin"], thread="t_luis")

d4["calls"].append({
    "id": "call_d4_karen", "at": "D4 16:10", "caller": "c_karen",
    "purpose": "Donor wants to defend the hospital publicly in the ER story comments",
    "turns": [
        {"speaker": "caller", "text": "Erin, it's Karen. Today was beautiful, thank you. But my cousin sent me the "
                                      "Ledger story, and the comments on your Facebook post are awful. I want to post "
                                      "something defending you all - say the ER saved my dad's life.",
         "patience_s": 20},
        {"speaker": "human", "text": "Karen, that's kind of you, and I'm so glad today felt right. I'd ask you not to "
                                     "wade into that thread, though. It pulls more people in, and a donor defending "
                                     "the hospital can become its own story. Your post about today and about Eli is "
                                     "the best thing you can share."},
        {"speaker": "caller", "text": "Okay. It just made me angry.", "patience_s": 20},
        {"speaker": "human", "text": "I understand. We're handling the comments, and Patient Relations is there for "
                                     "anyone who wants to talk to us. I'll send you the photos tomorrow."},
        {"speaker": "caller", "text": "Thank you, Erin.", "patience_s": 10},
    ]})

act(d4, "a4_01", "D4 07:20", "forward", "e_d4_ledger_alert",
    "Ledger's Haskins story is up (6:00 a.m.). Our statement is quoted accurately and in full on staffing. No "
    "embargo issue: the last line refers only to the public advisory. Erin",
    "Alerts leadership early on the morning of the event.", to=["c_alicia", "c_doug", "c_steven", "c_rhonda", "c_lisa", "c_carol"])
act(d4, "a4_02", "D4 08:15", "reply", "chat_d4_tasha",
    """
One catch: Sprout is set to Eastern, so "10:00 AM EST" posts would go at 9:00 our time - an hour before the embargo
lifts. Please move all four to 10:00 a.m. Central (11:00 AM in Sprout's Eastern view) and send me a screenshot. On
comments: we'll talk at 11 if they pick up.
""", "Catches that the scheduled posts would break the embargo by an hour.", to=["c_tasha"])
act(d4, "a4_03", "D4 08:40", "reply", "e_d3_tom",
    "Tom - I don't have anything beyond our statement, which is below. Erin\n\n(Statement pasted as approved Wednesday.)",
    "Gives no claim or settlement information.", to=["c_tom"])
act(d4, "a4_04", "D4 10:00", "send", None,
    """
FOR IMMEDIATE RELEASE - Nov. 5, 2026

Halvorsen family gives $20 million to build region's first psychiatric hospital for children

Gift is the largest in Prairie Bend Health's history; $64 million center to open in fall 2028

(Release v5 as final: 48 beds, 32 teen and 16 child; partial hospitalization for 24 a day; 312 children and teens
waited an average of 2.6 days in the 12 months ending Sept. 30; funding $20M gift + $12M state grant + $28M PBH
capital + $4M Foundation campaign; quotes from Dr. Ellison, Karen Halvorsen Doyle, Dr. Moreau and Gov. Patricia
Hartley; boilerplate; media contact Erin Lindqvist.)
""", "Distributes the release to the full list and PR Newswire at the embargo time.", to=["c_medialist"],
    subject="NEWS RELEASE: Halvorsen family gives $20 million for children's psychiatric hospital")
act(d4, "a4_05", "D4 10:45", "reply", "e_d4_nc9_desk",
    "Here you go, Ashley: release attached; b-roll and Dr. Moreau's interview are in the press kit at "
    "prairiebendhealth.org/news/halvorsen-center. Erin", "Routine media service.", to=["c_nc9_desk"])
act(d4, "a4_06", "D4 11:10", "noop", None,
    "Ran the 10:35 media availability. Dr. Ellison took Dana's and Luis's ER questions using Q&A 11 and 12.",
    "The event itself.")
act(d4, "a4_07", "D4 12:20", "forward", "e_d4_jessica",
    """
Alicia - NewsCenter 9 wants a separate 15-minute sit-down with Ray at 2:30 on ER waits and the Haskins family. Your
and Ray's call. If yes, I'd suggest Dr. Sameer Qureshi or Lisa join on ED operations, Steven sees the topics first,
and Ray stays inside the statement on the family. If no, I can offer Lisa on staffing generally.
""", "Interview decisions belong to the VP and CEO.", to=["c_alicia"])
act(d4, "a4_08", "D4 14:30", "reply", "chat_d4_tasha2",
    """
Please don't hide them - they don't break our community guidelines, and hiding them makes it worse. Reply once,
near the top, with this and nothing else:

"We're deeply sorry for this family's loss. We can't discuss any patient's care here, but we'd welcome the chance to
talk. Please message us or call Patient Relations at 555-0190."

Don't reply to individual comments, and don't confirm anything about any patient - including to the person who
says she's a relative. Hide only threats, profanity or someone's health details. Flag anything from the family to me
and Janelle. Screenshot and keep everything; it's under the legal hold.
""", "Social response consistent with HIPAA, the legal hold and the posted guidelines.", to=["c_tasha"])
act(d4, "a4_09", "D4 15:45", "reply", "e_d4_hannah",
    """
Hannah - (1) The $64 million project works out to about $1.33 million per bed for the 48 beds, though that figure
also covers the day program for 24 young people, so it's not a pure per-bed cost. (2) We don't have a current count
I can share today; the 312 figure is for the 12 months that ended Sept. 30, with an average wait of 2.6 days.

Erin
""", "Answers a numeric follow-up by deadline.", to=["c_hannah"])
act(d4, "a4_10", "D4 16:20", "reply", "e_d4_greg",
    "Will do, Greg - you'll have it by noon tomorrow. 14 stories so far today. Erin", "Commits to the summary.",
    to=["c_greg"])
act(d4, "a4_11", "D4 16:50", "reply", "e_d4_andrea",
    "Thank you, Andrea! Photos and a clip list tomorrow afternoon. Erin", "Partner follow-up.", to=["c_andrea"])

d5 = {"date": "2026-11-06", "label": "Friday", "actions": [], "calls": []}
DAYS.append(d5)

item("chat_d5_housesup", "chat", "message", "D5 07:45", "c_housesup", "Teams: Mark Ellery (House Supervisor)",
     "Weekend house supervisor is Tonya Graves. Priya's on the media line per the schedule.", to=["c_erin"],
     thread="t_chat_housesup")

item("e_d5_digest", "email", "email", "D5 07:00", "c_meltwater", "Meltwater daily digest - Prairie Bend Health - Nov. 6",
     """
Meltwater | Daily digest | Prairie Bend Health | 24 hours to 7:00 a.m. CT, Nov. 6

HALVORSEN CENTER (new since last alert)
15. Prairie Bend Ledger (print, A1, Nov. 6) - positive - 38,000
16. Prairie Bend Business Journal (print, Nov. 6) - neutral - 9,500
17. The State Courier (online and print) - positive - 72,000
18. Behavioral Health Business Weekly (trade newsletter) - positive - 15,000

OTHER
- Prairie Bend Ledger (print, A3, Nov. 6): "Family says mother waited six hours in PBMC ER" (print run of Thursday's
  online story) - negative - 38,000
- Prairie Bend Ledger editorial (online, Nov. 5, 8 p.m.): "Good news for kids, hard questions for the ER" - mixed.
""", to=["c_erin", "c_doug", "c_priya", "c_tasha"], thread="t_clips")

item("e_d5_alicia", "email", "email", "D5 08:10", "c_alicia", "Thank you",
     """
Erin - thank you for this week. You kept the embargo, the Ledger statement and the event all on track, with Doug
out. Debrief at 11. Greg needs the coverage summary by noon for the board packet; copy me.

Alicia
""", to=["c_erin"], cc=["c_doug"], thread="t_release")

item("chat_d5_kyle", "chat", "message", "D5 08:30", "c_kyle", "Teams: Kyle Brandvold",
     "Event photos are up: PBH Photo Library > 2026 > Halvorsen Announcement (142 selects). The family + rendering "
     "one is #HAL-0457. All cleared - no patients in any frame.", to=["c_erin"], thread="t_chat_kyle")

item("e_d5_jordan", "email", "email", "D5 09:00", "c_jordan", "Two ideas for the urgent care opening",
     """
Hi Erin,

Two ideas for North Prairie Urgent Care - want to run them by you before I go ahead:

1. Could we ask the North Prairie staff (and maybe our team) to leave 5-star Google reviews the first week so we're
   not starting at zero stars?
2. A local mom influencer, @PrairieMamaLife (38K followers), offered to post about her family's visit if we cover the
   visit and give her a $200 gift card. She'd rather not put #ad on it because it "kills engagement." She'd film in the
   waiting room. OK if I tell her yes?

Jordan
""", to=["c_erin"], thread="t_urgentcare")

item("e_d5_dana", "email", "email", "D5 09:30", "c_dana", "Follow-up for Sunday",
     """
Erin - the Ledger is doing a Sunday follow-up on ER staffing statewide. Could you tell me how many travel nurses are
working in PBMC's ER and how many ER nurses you've hired this year? Deadline Saturday noon.

Dana
""", to=["c_erin"], thread="t_haskins_media")

item("e_d5_greg", "email", "email", "D5 09:45", "c_greg", "Re: WOW",
     "For the board summary - can you include total audience and a few headlines? They love numbers. Greg",
     to=["c_erin"], thread="t_release")

item("e_d5_student", "email", "email", "D5 10:40", "c_student", "Re: Interview request - careers in health care PR",
     "Hi Ms. Lindqvist, just following up on my interview request. Any 20 minutes next week would be wonderful. "
     "Thank you! Maya", to=["c_erin"], thread="t_student")

item("e_d5_ben", "email", "email", "D5 11:30", "c_ben", "Re: Pulse item by Friday 2 p.m.",
     "Gentle nudge on the Pulse item - 2 p.m. Thanks! Ben", to=["c_erin"], thread="t_internal")

item("e_d5_hr", "email", "email", "D5 12:00", "c_hr", "Veterans Day, Wednesday Nov. 11",
     "All hospitals and clinics operate normal schedules on Veterans Day. Administrative offices are open. Thank you "
     "to the 640 veterans who work at PBH.", to=["c_allstaff"], thread="t_hr")

item("e_d5_tasha", "email", "email", "D5 13:00", "c_tasha", "Weekly social report - Nov. 2-6",
     """
Highlights:
- Halvorsen announcement (Facebook): reach 84,200; 1,960 reactions; 730 shares; 412 comments (61 about the ER story;
  we posted the one approved reply; none hidden).
- Instagram carousel: reach 21,300; 1,140 likes.
- LinkedIn: 14,800 impressions; 9.1% engagement.
- X: 6,200 impressions.
- Posts went live at 10:00 a.m. CT after the time-zone fix.
""", to=["c_erin", "c_doug", "c_alicia"], thread="t_chat_tasha")

item("chat_d5_doug", "chat", "message", "D5 13:30", "c_doug", "Teams: Doug Reinholt",
     """
Next week: can you draft a pitch calendar for Nov. 9-20 by Monday morning? World Prematurity Day Nov. 17 (NICU
graduates?), Great American Smokeout Nov. 19 (lung cancer screening), urgent care ribbon cutting Nov. 13, and the
Legislature's staffing hearing Nov. 18 (the union will testify). One page is fine.
""", to=["c_erin"], thread="t_chat_doug")

item("e_d5_steven", "email", "email", "D5 14:20", "c_steven", "Reminder - legal hold (Haskins)",
     "Reminder that the legal hold covers this week's media inquiry log entries, the Ledger statement drafts and the "
     "Facebook comment screenshots. Please keep them. No reply needed. Steven", to=["c_erin", "c_tasha", "c_doug"],
     thread="t_haskins_legal")

item("e_d5_monica", "email", "email", "D5 15:00", "c_monica", "Congratulations - and a listening session?",
     """
Hi Erin,

Congratulations on the Halvorsen Center! The Prairie Bend Youth Mental Health Coalition would love to co-host a
community listening session with PBH in December so parents and young people can help shape the program. Could we
find time to meet in the next two weeks?

Monica Feld
Executive Director, Prairie Bend Youth Mental Health Coalition
""", to=["c_erin"], thread="t_coalition")

item("e_d5_cision", "email", "email", "D5 15:30", "c_vendor", "Last chance: 2026 Top Hospital badge",
     "Final reminder: claim your 2026 Top 100 Hospital for Patient Experience award package ($4,950) by Nov. 9.",
     to=["c_erin"], thread="t_vendor")

d5["calls"].append({
    "id": "call_d5_andrea", "at": "D5 11:35", "caller": "c_andrea",
    "purpose": "State partner asks for photos and clips, and about the ER story",
    "turns": [
        {"speaker": "caller", "text": "Erin, Andrea. Great event. Can you get me the photos and the clip list by end of "
                                      "day for the Governor's weekly report?", "patience_s": 20},
        {"speaker": "human", "text": "Absolutely. Kyle's gallery is up; I'll send you a link and the clip list this "
                                     "afternoon. It's eighteen stories as of this morning."},
        {"speaker": "caller", "text": "Perfect. Any blowback on your end from the ER story?", "patience_s": 20},
        {"speaker": "human", "text": "We have a statement out on it, and that's what I'd point anyone to. Nothing "
                                     "on our side that affects the state."},
        {"speaker": "caller", "text": "Okay. Thanks again.", "patience_s": 10},
    ]})

act(d5, "a5_01", "D5 10:00", "reply", "e_d5_dana",
    """
Dana - since Jan. 1 we've hired 22 emergency nurses, and 9 contract nurses are working in the PBMC emergency
department this week. 104 of our 118 emergency nursing positions are filled. Erin
""", "Uses only the numbers the CNO cleared for external use.", to=["c_dana"])
act(d5, "a5_02", "D5 10:30", "create_doc", None,
    """
Halvorsen Center announcement - coverage summary (Nov. 5, 10 a.m. to Nov. 6, 7 a.m.)

- 18 news stories; estimated audience 591,000.
- Tone: 15 positive, 3 neutral, 0 negative.
- 4 of the 18 also mentioned the Ledger's ER story (Ledger online, 5 News at Noon, NewsCenter 9 at 5, 5 News at 6).
- Every local outlet covered it: Ledger (online twice and print A1), NewsCenter 9 (noon, web, 5 p.m.), 5 News (noon,
  6 p.m.), Mid-Valley Public Radio (online and All Things Considered), Business Journal (online and print), Tri-County
  12, State Capitol News Service, The State Courier, Prairie Bend Parent, WestSide Neighbors, Behavioral Health
  Business Weekly.
- Headlines: "Halvorsen family gives $20 million for children's psychiatric hospital" (Ledger); "Hartley touts
  behavioral health fund at Prairie Bend event" (Ledger); "How PBH will pay for its $64M youth psychiatric center"
  (Business Journal).
""", "Builds the board summary from three Meltwater alerts (9 + 5 + 4).")
act(d5, "a5_03", "D5 11:45", "send", None,
    "Greg - the coverage summary for the board packet is attached: 18 stories, estimated audience 591,000, 15 "
    "positive and 3 neutral, plus headlines. Erin", "Delivers by noon.", to=["c_greg", "c_alicia", "c_doug"],
    subject="Halvorsen Center coverage summary")
act(d5, "a5_04", "D5 12:30", "reply", "e_d4_ben",
    """
Ben - Pulse item (134 words), photo #HAL-0457:

A $20 million gift for kids' mental health
On Thursday, Dr. Raymond Ellison announced the largest gift in Prairie Bend Health's history: $20 million from the
Halvorsen Family Foundation to build the Halvorsen Center for Youth Behavioral Health on our Westgate campus. The
48-bed center, with a day program for 24 more young people, will be the only inpatient psychiatric unit for children
within 190 miles when it opens in fall 2028. Gov. Patricia Hartley joined to announce a $12 million state grant.
Last year 312 children and teens waited in our emergency department for a psychiatric bed, an average of 2.6 days.
"Thank you to every nurse, doctor and tech who has cared for those kids," Dr. Ellison said. The Foundation's $4
million community campaign starts now; watch Pulse for ways to help.
""", "Employee newsletter item.", to=["c_ben"])
act(d5, "a5_05", "D5 14:00", "reply", "e_d4_karen",
    """
Karen,

Thank you - for Eli's story, for your courage in front of all those cameras, and for trusting us with this. Here is
the gallery: PBH Photo Library > 2026 > Halvorsen Announcement. The one of your parents with the rendering is
#HAL-0457; Kyle can send a print-size file for framing.

The coverage was wonderful - 18 stories across the state by this morning. I'll send Greg the links so the
Foundation can share them with you.

With gratitude,
Erin
""", "Donor stewardship and photos.", to=["c_karen"])
act(d5, "a5_06", "D5 14:30", "send", None,
    "Andrea - photo gallery link and our clip list (18 stories) attached. Thank you for being such a good partner. "
    "Erin", "Promised on the call.", to=["c_andrea"], subject="Photos and coverage - Halvorsen Center")
act(d5, "a5_07", "D5 15:30", "reply", "e_d5_jordan",
    """
Jordan - good instincts on wanting reviews and reach, but both need changes:

1. Staff reviews: please don't. The FTC's rule on consumer reviews (16 CFR Part 465) bars a business from asking
   employees for reviews unless each one clearly discloses they work here, and Google's policies prohibit it too. What
   we can do: a general request to every patient after a visit ("Tell us how we did") - not just happy ones.
2. Influencer: we can work with her only if every post clearly discloses the connection - "#ad" or "paid
   partnership with Prairie Bend Health" at the start, not buried. The FTC Endorsement Guides (16 CFR 255.5) require
   it when we cover the visit and a gift card. And no filming in the waiting room: other patients would be in the
   frame, and we'd need each one's written HIPAA authorization. She can film outside or in an empty exam room before
   opening.

Happy to talk through it Monday.
Erin
""", "FTC endorsement and review rules; HIPAA on filming.", to=["c_jordan"])
act(d5, "a5_08", "D5 16:00", "reply", "e_d5_student",
    "Hi Maya - happy to. How about Tuesday, Nov. 10, at 4 p.m. by video? I'll send a link. Erin",
    "Low-priority request handled at end of week.", to=["c_student"])

item("chat_d5_priya", "chat", "message", "D5 09:10", "c_priya", "Teams: Priya Natarajan",
     "I'm on the media line this weekend. Can you send me a handoff before you leave - especially anything on the "
     "Haskins story and Dana's Sunday piece?", to=["c_erin"], thread="t_oncall")

act(d5, "a5_09", "D5 16:30", "reply", "chat_d5_priya",
    """
Weekend handoff:
1. Haskins: use ONLY the approved statement (in the media log, Wed 2:45 p.m.). Nothing on the claim; "We do not
   discuss personnel matters." Dana's Sunday staffing follow-up: I gave her 22 ED nurses hired since Jan. 1, 9
   contract nurses, 104 of 118 positions filled - all cleared by Lisa. Anything new goes to Steven first.
2. Dunleavy (council member): no-information status. "I don't have any information I can release on anyone by that
   name."
3. Social: one approved reply on the announcement post; don't hide critical comments; everything is under the legal
   hold.
4. Union: PBNA testifies Nov. 18; possible picketing that day (not public - don't mention it).
5. Halvorsen coverage summary went to Greg; Karen has her photos.
""", "Weekend on-call handoff.", to=["c_priya"])
