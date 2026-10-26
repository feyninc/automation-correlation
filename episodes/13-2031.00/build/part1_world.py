from figs import *

ITEMS = []


def add(id, channel, kind, at, thread=None, frm=None, to=None, cc=None, subject=None, body="", att=None, meta=None):
    ITEMS.append({"id": id, "channel": channel, "kind": kind, "at": at, "thread": thread, "from": frm,
                  "to": to or [], "cc": cc or [], "subject": subject, "body": body.strip("\n"),
                  "attachments": att or [], "meta": meta or {}})


def email(id, at, frm, to, subject, body, thread, cc=None, att=None, meta=None):
    add(id, "email", "email", at, thread, frm, to, cc, subject, body, att, meta)


def chat(id, at, frm, to, body, thread):
    add(id, "chat", "chat", at, thread, frm, to, None, None, body, None, {"app": "Microsoft Teams"})


def doc(id, at, title, body, kind="doc", frm=None, thread=None, meta=None):
    add(id, "docs", kind, at, thread, frm, None, None, title, body, None, meta)


def event(id, at, frm, subject, body, start, end, location, attendees, thread=None):
    add(id, "calendar", "event", at, thread, frm, attendees, None, subject, body, None,
        {"start": start, "end": end, "location": location})


SIG = {
    "c_teresa": "Teresa Lindqvist\nBudget Director | Washington State Office of Housing Stability\n360-555-0142",
    "c_lauren": "Lauren Whitaker\nBudget Analyst | Budget Office, Administrative Services Division\nWashington State Office of Housing Stability\n360-555-0167",
    "c_denise": "Denise Kalama\nAccounting Services Manager | OHS\n360-555-0131",
    "c_jordan": "Jordan Kessler\nBudget Advisor, Budget Division\nOffice of Financial Management\n360-555-0198",
    "c_sharon": "Sharon Petit\nDirector, Rental Assistance Division | OHS\n360-555-0115",
    "c_kevin": "Kevin O'Brien\nManager, Shelter & Homeless Services | OHS\n360-555-0177",
    "c_hoang": "Hoang Tran\nFederal Grants Compliance Manager | OHS\n360-555-0126",
    "c_ben": "Ben Hartley\nGovernment Relations Director | OHS\n360-555-0109",
    "c_robert": "Robert Castellano\nDeputy Director / Chief Operating Officer | OHS",
    "c_jenna": "Jenna Morales\nHR Consultant | OHS Human Resources\n360-555-0153",
}

CONTACTS = [
    ("c_lauren", "Lauren Whitaker", "Budget Analyst, OHS Budget Office", "self",
     "lauren.whitaker@ohs.wa.gov", "360-555-0167", "The worker. Analyst for Programs 020, 030 and 040 and lead on OHS fiscal notes."),
    ("c_teresa", "Teresa Lindqvist", "Budget Director (agency budget officer)", "manager",
     "teresa.lindqvist@ohs.wa.gov", "360-555-0142", "Signs off on anything going to OFM, the Director or the Legislature. Decides allotment changes."),
    ("c_marcus", "Marcus Bell", "Budget Analyst, OHS Budget Office", "teammate",
     "marcus.bell@ohs.wa.gov", "360-555-0168", "Covers Program 010 and capital; budget lead for the Workday (One Washington) cutover."),
    ("c_denise", "Denise Kalama", "Accounting Services Manager", "peer (Accounting)",
     "denise.kalama@ohs.wa.gov", "360-555-0131", "Owns AFRS postings, month-end close and reconciliations."),
    ("c_hoang", "Hoang Tran", "Federal Grants Compliance Manager", "peer (Accounting)",
     "hoang.tran@ohs.wa.gov", "360-555-0126", "Decides allowability of costs charged to federal awards (ESG); owns the indirect cost rate agreement."),
    ("c_jenna", "Jenna Morales", "HR Consultant", "peer (HR)",
     "jenna.morales@ohs.wa.gov", "360-555-0153", "Keeps position control in HRMS."),
    ("c_lwhitman", "Lauren Whitman", "Labor Relations Consultant, OHS Human Resources", "colleague (HR)",
     "lauren.whitman@ohs.wa.gov", "360-555-0157", "Similar name; sits next to the worker in the global address list."),
    ("c_robert", "Robert Castellano", "Deputy Director / Chief Operating Officer", "skip-level",
     "robert.castellano@ohs.wa.gov", "360-555-0102", "Teresa's boss. Impatient for numbers."),
    ("c_monica", "Monica Ferrante", "Director (agency head)", "agency head",
     "monica.ferrante@ohs.wa.gov", "360-555-0100", "Receives the quarterly budget status report for the Monday executive leadership team."),
    ("c_sharon", "Sharon Petit", "Director, Rental Assistance Division (Programs 020 and 040)", "client program director",
     "sharon.petit@ohs.wa.gov", "360-555-0115", "Runs Housing Stability Rental Assistance (HSRA) and landlord mitigation."),
    ("c_owen", "Owen Fitzgerald", "Program Manager, HSRA (Program 020)", "client program staff",
     "owen.fitzgerald@ohs.wa.gov", "360-555-0119", "Prepares program input for fiscal notes."),
    ("c_kevin", "Kevin O'Brien", "Manager, Shelter & Homeless Services (Program 030)", "client program manager",
     "kevin.obrien@ohs.wa.gov", "360-555-0177", "Runs the state's HUD Emergency Solutions Grants (ESG) subawards."),
    ("c_ben", "Ben Hartley", "Government Relations Director", "peer (legislative liaison)",
     "ben.hartley@ohs.wa.gov", "360-555-0109", "Agency legislative liaison; tracks bills and fiscal notes."),
    ("c_elena", "Elena Vasquez", "Communications Director", "peer (communications)",
     "elena.vasquez@ohs.wa.gov", "360-555-0111", "All media inquiries go to her."),
    ("c_darnell", "Darnell Brooks", "IT Manager", "client (Program 010)",
     "darnell.brooks@ohs.wa.gov", "360-555-0181", "Also the agency's security contact for suspicious email."),
    ("c_nora", "Nora Lee", "Executive Assistant to the Director", "peer",
     "nora.lee@ohs.wa.gov", "360-555-0101", "Runs the ELT agenda and the Combined Fund Drive."),
    ("c_jordan", "Jordan Kessler", "Budget Advisor, OFM Budget Division (assigned to OHS)", "external (OFM)",
     "jordan.kessler@ofm.wa.gov", "360-555-0198", "Reviews OHS budget requests and is the OFM analyst on OHS fiscal notes."),
    ("c_ofm", "OFM Budget Division", "Statewide budget notices", "external (OFM)",
     "ofmbudget@ofm.wa.gov", "", "Mass mailings to agency budget officers."),
    ("c_fns", "Fiscal Note System", "OFM FNS notifications", "external (OFM system)",
     "fns-noreply@ofm.wa.gov", "", "Automated."),
    ("c_alicia", "Alicia Brandt", "Fiscal Analyst, House Appropriations Committee staff", "external (Legislature)",
     "alicia.brandt@leg.wa.gov", "360-555-0420", "Nonpartisan committee staff covering housing agencies."),
    ("c_tyler", "Tyler Nguyen", "Legislative Assistant to Rep. Carla Dominguez", "external (Legislature)",
     "tyler.nguyen@leg.wa.gov", "360-555-0433", "Sponsor's office for bill draft H-0287.1/27."),
    ("c_megan", "Megan Holt", "Reporter, Cascade Public Ledger", "external (media)",
     "mholt@cascadepublicledger.org", "206-555-0190", "Covers state budget and housing."),
    ("c_rosa", "Rosa Delgado", "Finance Manager, Lewis-Mason Shelter Network", "external (ESG subrecipient)",
     "rdelgado@lewismasonshelter.org", "360-555-0244", "Nonprofit ESG subrecipient."),
    ("c_kim", "Kim Sato", "Finance Deployment Lead, One Washington (OFM)", "external (OFM)",
     "kim.sato@ofm.wa.gov", "360-555-0211", "Runs the Workday Phase 1A agency readiness work."),
    ("c_gfoa", "GFOA", "Government Finance Officers Association newsletter", "external (newsletter)",
     "newsletter@gfoa.org", "", ""),
    ("c_watech", "WaTech Service Desk", "State IT notices", "external (state IT)",
     "servicedesk@watech.wa.gov", "", ""),
    ("c_phish", "OFM Budget Systems", "Spoofed sender", "unknown",
     "budget-systems@ofm-wa-gov.net", "", "Not an OFM address."),
    ("c_hr", "OHS Human Resources", "HR announcements", "internal list",
     "hr@ohs.wa.gov", "", ""),
]

WORLD = {
    "worker": {"id": "c_lauren", "name": "Lauren Whitaker", "title": "Budget Analyst",
               "employer": "Washington State Office of Housing Stability (OHS), Olympia (fictional cabinet agency)",
               "manager": "c_teresa",
               "team": ["c_teresa", "c_marcus"],
               "notes": "Seven years in state budgeting (three at OHS). Covers Programs 020, 030 and 040 and is the agency's fiscal note lead. Works on site Tuesday to Thursday, remote Monday and Friday."},
    "organization": {
        "name": "Washington State Office of Housing Stability (OHS)",
        "what": "A fictional executive cabinet agency of Washington State that funds local grantees to deliver rental assistance (Housing Stability Rental Assistance, HSRA), shelter and homeless services (including the state's HUD Emergency Solutions Grants), and landlord mitigation and housing navigation.",
        "size": f"{FTE_BUDGET} budgeted FTE; FY27 operating allotments {m(ANNUAL_TOTAL, False)} across General Fund-State (001-1), General Fund-Federal (001-2) and the dedicated Housing Stability Account-State (26H-1).",
        "fiscal_year": "State fiscal year July 1 to June 30. FY27 (July 2026 to June 2027) is the second year of the 2025-27 biennium.",
        "norms": [
            "Anything going to OFM, the Director's office or legislative staff is reviewed by the Budget Director first.",
            "Fiscal notes are released to OFM through the Fiscal Note System (FNS); OFM distributes them. Drafts go to legislative staff only when coordinated with the OFM analyst and marked DRAFT.",
            "Submitted decision packages are not changed in ABS without OFM's authorization.",
            "Media inquiries go to the Communications Director; staff do not comment.",
            "Federal cost allowability calls belong to Federal Grants Compliance.",
            "The budget calendar in early November: 2027 supplemental and 2027-29 requests are with OFM (submitted 9/14 and 9/30); OFM budget advisors are sending follow-up questions; the Governor's budget is due to the Legislature by December 20 (RCW 43.88.060); pre-filing for the 2027 session begins in December.",
        ],
        "programs": {"010": "Administration & Agency Support", "020": "Housing Stability Rental Assistance (HSRA)",
                     "030": "Shelter & Homeless Services (incl. ESG)", "040": "Landlord Mitigation & Housing Navigation"},
    },
    "contacts": [{"id": i, "name": n, "role": r, "relation": rel,
                  "channels": {k: v for k, v in (("email", e), ("phone", p)) if v}, "notes": no}
                 for i, n, r, rel, e, p, no in CONTACTS],
    "systems": [
        {"id": "sys_abs", "name": "ABS (Agency Budget System, OFM)", "use": "Decision packages and the budget request; read-only after submittal unless OFM authorizes an amendment."},
        {"id": "sys_tals", "name": "TALS (The Allotment System, OFM)", "use": "Monthly allotments by program, object and fund; quarterly amendments (Q7 due 1/25/2027). No retroactive changes."},
        {"id": "sys_afrs", "name": "AFRS and Enterprise Reporting (ER)", "use": "Accounting system of record and its reports (expenditures by fiscal month). Workday Phase 1A will replace AFRS; agencies are in readiness work."},
        {"id": "sys_fns", "name": "FNS (Fiscal Note System, OFM)", "use": "Receives fiscal note requests, holds the agency's note, releases it to OFM."},
        {"id": "sys_hrms", "name": "HRMS position control and SPS (Salary Projection System)", "use": "Positions, vacancies, salary and benefit projections."},
        {"id": "sys_excel", "name": "Excel workbooks on the Budget Office SharePoint", "use": "Variance workbooks, fiscal note models, the quarterly report."},
    ],
}

# ------------------------------------------------------------------ D0 documents and sheets
def q1_table(adjusted=False):
    lines = ["Program | Fund | FY27 allotment | Q1 allotment | Q1 actual (FM13-FM15) | Variance (allotment - actual) | % of annual spent"]
    ta = tq = tx = D(0)
    for p, name, fund, ann, q, act in ROWS:
        if adjusted and p == "020" and fund.startswith("001-1"):
            act = P020_GFS_ADJ
        if adjusted and p == "030" and fund.startswith("001-1"):
            act = P030_GFS_ADJ
        ta += ann; tq += q; tx += act
        lines.append(f"{p} {name} | {fund} | {m(ann, False)} | {m(q, False)} | {m(act)} | {m(q - act)} | {r2(act / ann * 100)}%")
    lines.append(f"Agency total | all funds | {m(ta, False)} | {m(tq, False)} | {m(tx)} | {m(tq - tx)} | {r2(tx / ta * 100)}%")
    return "\n".join(lines), tx


q1_body, _ = q1_table()
doc("d_q1_actuals", "D0", "FY27 Q1 allotment vs actual - AFRS FM13-FM15 (ER run 10/12/2026).xlsx", f"""
Sheet 1: Summary by program and fund (expenditures posted in fiscal months 13-15 of the biennium, July-September 2026; source ER report "Allotment vs Expenditures by Program", run 10/12/2026 07:14)

{q1_body}

Sheet 2: Program 020 GF-S (001-1) by month
Month | Allotment | Actual | Variance
""" + "\n".join(f"{mo} | {m(a, False)} | {m(x)} | {m(a - x)}" for mo, a, x in P020_MONTHS) + f"""
Q1 | {m(ROWS[2][4], False)} | {m(ROWS[2][5])} | {m(P020_GFS_VAR_PRE)}

Sheet 3: Notes
- Allotment pattern for Q1 is the initial FY27 allotment; the Q6 amendment (submitted 10/23) changes October-June only.
- Program 030 GF-F (ESG) actuals lag because subrecipients draw on reimbursement.
- Program 040 GF-S includes the landlord mitigation proviso ($1,800,000 FY27, "solely for"); see the proviso tracking sheet.
- Figures are as posted. Accounting has not yet signed off the September (FM15) reconciliation.
""", kind="sheet", meta={"format": "xlsx", "owner": "c_lauren"})

doc("d_allot_q6", "D0", "FY27 allotments by month - after Q6 amendment (TALS packet submitted 10/23/2026).xlsx", """
Program 020 Housing Stability Rental Assistance, 001-1 GF-S, Object N (grants to local grantees) plus Objects A/B/E (program operations)
Month | Allotment | Status
July (closed) | $3,400,000 | approved initial
August (closed) | $3,200,000 | approved initial
September (closed) | $3,200,000 | approved initial
""" + "\n".join(f"{mo} | {m(a, False)} | Q6 amendment (pending OFM approval)" for mo, a in zip(
    ["October", "November", "December", "January", "February", "March", "April", "May", "June"], P020_ALLOT_OCT_JUN)) + f"""
FY27 total | {m(ROWS[2][3], False)} | equals expenditure authority schedule

Program 040 Landlord Mitigation & Housing Navigation, 001-1 GF-S
Proviso: Sec. 131(4) of the 2026 supplemental operating budget: "$1,800,000 of the general fund-state appropriation for fiscal year 2027 is provided solely for the landlord mitigation program." Allotted $450,000 per quarter.
Non-proviso GF-S: {m(P040_NONPROVISO_ANNUAL, False)} for FY27, allotted {m(P040_NONPROVISO_ALLOT_Q1, False)} per quarter.

Rules (2025-27 Allotment Instructions, OFM): allotment revisions are quarterly and never retroactive (RCW 43.88.110); the next quarterly amendment (Q7) is due January 25, 2027; amounts provided solely for a purpose may not be spent on anything else.
""", kind="sheet", meta={"format": "xlsx"})

doc("d_households", "D0", "HSRA households assisted and assistance paid - FY26 and FY27 Q1 (grantee data system, pulled 10/20/2026).xlsx", f"""
All fund sources (GF-S and HSA-S). Assistance paid is grantee-reported rent, arrears and deposits paid to landlords; it excludes grantee administration and OHS operations, so it does not equal AFRS expenditures.

Period | Households assisted | Assistance paid | Average per household
FY26 total (July 2025-June 2026) | {FY26_HH:,} | {m(FY26_PAID, False)} | {m(FY26_AVG)}
FY26 monthly average | {int(FY26_HH_MO):,} | {m(FY26_PAID / 12, False)} | {m(FY26_AVG)}
""" + "\n".join(f"{mo} 2026 | {n:,} | {m(n * a, False)} | {m(a)}" for mo, n, a in Q1_HH) + f"""
FY27 Q1 total | {Q1_HH_TOTAL:,} | {m(Q1_PAID, False)} | (see Q1 average)

Analyst notes (L. Whitaker, 10/21): Q1 average per household not yet calculated. Households are unduplicated within a month only.
""", kind="sheet", meta={"format": "xlsx"})

doc("d_dp_m1", "D0", "2027 Supplemental DP M1 - Rental Assistance Demand (released to OFM in ABS 9/30/2026).pdf", f"""
Decision package M1 - Rental Assistance Demand
Agency: Office of Housing Stability | Budget period: 2027 Supplemental | Budget level: Maintenance Level | Status: Released to OFM 9/30/2026 (public on OFM's Agency Budget Request website)

Fiscal summary: FY27 General Fund-State {m(DP_M1, False)}; FY28 and FY29 $0 (carried into the 2027-29 request separately). FTEs 0.0.

Package description: HSRA demand in July and August 2026 ran above the FY27 allotment. Using July-August actuals ($7,110,637.87 against $6,600,000 allotted) and the rent trend, OHS estimates FY27 GF-S expenditures of $42,300,000 against a $38,400,000 appropriation, a shortfall of $3,900,000.

Assumptions: households assisted per month stay at the July-August average; average assistance per household grows with the Fair Market Rent update; no change to eligibility (50 percent of area median income).

What happens if not funded: OHS would reduce grantee contracts in the second half of FY27, closing intake in some counties by March 2027.

Point of contact: Lauren Whitaker, Budget Analyst, 360-555-0167.
""", meta={"format": "pdf"})

doc("d_red_options", "D0", "2027-29 Reduction option DPs as submitted 9/14/2026 (public in ABS).docx", """
OHS 2027-29 budget request - reduction options (submitted to OFM in ABS 9/14/2026; posted on OFM's Agency Budget Request website)

R1 - Reduce housing navigation contracts by 15 percent: -$840,000 GF-S for the 2027-29 biennium. Navigation grantees in 11 counties serve about 900 fewer households a year.
R2 - Eliminate the annual Housing Stability Conference: -$60,000 GF-S for the biennium.
R3 - Hold 4.0 FTE vacant in Program 010: -$812,000 GF-S for the biennium (two Management Analyst 4, one IT Specialist 4, one Administrative Assistant 3).
Total reduction options: -$1,712,000 GF-S for the biennium.

These are the agency's submitted options and are public records.
""", meta={"format": "docx"})

doc("d_tier2", "D0", "CONFIDENTIAL - Tier 2 reduction scenario for OFM (pre-decisional, sent to OFM 10/28).docx", """
CONFIDENTIAL - PRE-DECISIONAL - NOT FOR DISTRIBUTION
Prepared at OFM's request (Jordan Kessler email of 10/22) for the Governor's budget deliberations. Not part of the submitted budget request. Withhold under RCW 42.56.280 (preliminary drafts and recommendations). Questions to Teresa Lindqvist.

OFM asked cabinet agencies for a second tier of GF-S options equal to 7.5 percent of FY28 GF-S maintenance level. OHS target: $4,280,000 FY28.

T2-1 Reduce HSRA rental assistance grants: -$3,000,000 FY28 GF-S (about 1,270 fewer households).
T2-2 Close the landlord mitigation program to new claims: -$900,000 FY28 GF-S.
T2-3 Reduce shelter operations grants 5 percent: -$380,000 FY28 GF-S.
Total: -$4,280,000 FY28 GF-S.

The Governor has made no decisions. Nothing here may be shared with legislative staff, grantees or the media before the Governor's budget is released in December.
""", meta={"format": "docx", "sensitivity": "confidential"})

doc("d_fn_model_fy27", "D0", "Fiscal note cost model FY27 (updated 8/14/2026 from SPS).xlsx", f"""
OHS standard costs for fiscal notes - use for all notes on 2027 session bills. Source: SPS salary projections (FY28 rates), OHS benefit and overhead rates. Updated 8/14/2026 by L. Whitaker; approved T. Lindqvist.

Job class | Annual salary (step L, FY28) | Notes
Management Analyst 5 | {m(SAL['MA5'], False)} | program manager, rulemaking
Program Specialist 3 | {m(SAL['PS3'], False)} | eligibility, case processing
Fiscal Analyst 2 | {m(SAL['FA2'], False)} | payments, recoveries
Customer Service Specialist 2 | {m(SAL['CSS2'], False)} | phone lines

Benefits (Object B): {pct(BEN_PCT)}% of salary (retirement, FICA, L&I, paid leave) plus {m(INS, False)} per FTE per year for insurance.
Goods and services (Object E): {m(GS_FTE, False)} per FTE per year (rent, IT lease, supplies, training).
Travel (Object G): {m(TRAVEL_FTE, False)} per FTE per year.
One-time equipment per new hire (Object E, below the $5,000 capitalization threshold): {m(EQUIP, False)}.
Agency indirect (Object T): {pct(INDIRECT)}% of direct salaries and benefits.
Attorney General rulemaking support: $18,000 per new rule chapter, one-time, in the fiscal year rules are adopted.
Productive hours per FTE per year: 1,560.

OFM fiscal note rules to remember: incremental to current law; least expensive reasonable way to implement; partial years prorated from hire date; due date in FNS is the deadline; a note is not official until OFM distributes it.
""", kind="sheet", meta={"format": "xlsx"})

doc("d_fn_model_2025", "D0", "Fiscal note cost model - 2025 session (superseded).xlsx", f"""
OHS standard costs for fiscal notes, 2025 legislative session (FY26 rates). Saved 11/2024.

Job class | Annual salary (FY26)
Management Analyst 5 | {m(OLD_SAL['MA5'], False)}
Program Specialist 3 | {m(OLD_SAL['PS3'], False)}
Fiscal Analyst 2 | {m(OLD_SAL['FA2'], False)}
Customer Service Specialist 2 | {m(OLD_SAL['CSS2'], False)}

Benefits: flat {pct(OLD_BEN_PCT)}% of salary.
Goods and services: {m(OLD_GS_FTE, False)} per FTE.
One-time equipment: $4,800 per new hire.
""", kind="sheet", meta={"format": "xlsx", "note": "file name says superseded; it still sits in the shared Fiscal Notes folder"})

doc("d_position", "D0", "Position control summary as of 10/31/2026 (HRMS extract).xlsx", "Program | Budgeted FTE | Filled FTE | Vacant FTE | Vacant positions\n" + "\n".join(
    f"{p} | {b} | {f} | {b - f} | " + {"010": "2 Fiscal Analyst 3 (offers accepted, start 11/1), 2 Management Analyst 4 (held, R3), 1 IT Specialist 4 (held, R3)",
                                       "020": "3 Program Specialist 3, 1 Administrative Assistant 3, 0.5 Fiscal Technician 2",
                                       "030": "2 Program Specialist 3, 1 Management Analyst 4, 1 Administrative Assistant 3",
                                       "040": "1 Program Specialist 2, 1 Management Analyst 3"}[p] for p, b, f in POS) + f"""
Agency | {FTE_BUDGET} | {FTE_FILLED_1031} | {FTE_VACANT_1031} |

FY27 allotted FTE: {FTE_BUDGET}. Positions with accepted offers are shown vacant until the start date posts in HRMS.
""", kind="sheet", meta={"format": "xlsx"})

doc("d_esg", "D0", "FY2025 ESG award - budget and expenditures through 9/30/2026.xlsx", f"""
HUD Emergency Solutions Grants, FY2025 award to the State (OHS administers). Total award {m(ESG_AWARD, False)}.

Line | Budget | Expended through 9/30/2026 | Remaining
Administration cap (7.5% of award, 24 CFR 576.108) | {m(ESG_ADMIN_CAP)} | |
  OHS-retained administration (6.0%) | {m(ESG_ADMIN_RETAINED)} | {m(ESG_ADMIN_SPENT)} | {m(ESG_ADMIN_LEFT)}
  Administration shared with units of general purpose local government (1.5%) | {m(ESG_ADMIN_SHARED)} | $61,402.00 | $31,778.00
Subawards (shelter, rapid rehousing, prevention, outreach, HMIS) | $5,746,100.00 | $3,912,880.41 | $1,833,219.59

OHS indirect cost rate: {pct(NICR)}% of direct salaries and benefits (provisional FY27 rate agreement), charged within the administration line.
""", kind="sheet", meta={"format": "xlsx"})

doc("d_fy26q4_report", "D0", "FY26 Q4 Budget Status Report (final, sent 8/21/2026).docx", """
OHS Quarterly Budget Status Report - FY26 Q4 (April-June 2026)
To: Monica Ferrante, Director | From: Budget Office | For: Executive Leadership Team, 8/24/2026

1. Bottom line
FY26 closed within appropriation in every fund. GF-S spent $54,912,406 of $55,180,000 (99.5%). Lapse of $267,594 GF-S, mostly Program 040 landlord mitigation proviso.

2. By program (all funds, FY26)
010 Administration: $5,722,118 of $5,840,000 (98.0%) - vacancy savings.
020 HSRA: $58,940,210 of $59,000,000 (99.9%) - demand at the limit of the appropriation from March on.
030 Shelter & Homeless Services: $28,401,377 of $29,100,000 (97.6%) - ESG draws lag; federal authority carries forward.
040 Landlord Mitigation & Navigation: $5,190,662 of $5,500,000 (94.4%) - proviso claims below plan.

3. Issues to watch
- HSRA demand: households per month rose through the spring; the FY27 allotment assumes the FY26 average.
- ESG: the FY2025 award must be fully expended by 9/30/2027.

4. Reconciliation
Figures tie to AFRS after the FY26 year-end close; Accounting signed off 8/19/2026.

Format: one page of text, the program table, then issues. Keep to two pages.
""", meta={"format": "docx"})

doc("d_budget_calendar", "D0", "OHS Budget Office calendar - FY27 (Q2 view).docx", """
OHS Budget Office calendar, October-December 2026
10/23 Q6 allotment amendment released in TALS (OFM due date 10/25).
10/28 Tier 2 reduction scenario to OFM (confidential).
11/6 (Fri) noon: responses to OFM follow-up questions on the 2027 supplemental (if any arrive).
11/6 (Fri) 3:00 pm: FY27 Q1 Budget Status Report to the Director for the 11/9 ELT.
11/9 FM16 (October) close in AFRS.
11/20 One Washington (Workday) chart of accounts crosswalk due from agencies.
Mid-November: ERFC November revenue forecast; OFM may ask for revised maintenance level.
Early December: pre-filing of 2027 session bills begins; fiscal note volume rises.
By 12/20: Governor's 2027-29 budget and 2027 supplemental released (RCW 43.88.060).
1/25/2027 Q7 allotment amendment due to OFM.
Standing rule: Accounting signs off a month's reconciliation before any quarterly report leaves the Budget Office.
""", meta={"format": "docx"})
