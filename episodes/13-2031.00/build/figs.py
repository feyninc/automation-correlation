"""Every figure in the 13-2031.00 episode, computed once so items agree with each other."""
from decimal import Decimal as D, ROUND_HALF_UP


def r2(x):
    return D(x).quantize(D("0.01"), rounding=ROUND_HALF_UP)


def m(x, cents=True):
    x = r2(x)
    s = f"{abs(x):,.2f}" if cents else f"{abs(x.quantize(D('1'), rounding=ROUND_HALF_UP)):,.0f}"
    return ("-$" if x < 0 else "$") + s


# ---------------- FY27 allotments and Q1 actuals (AFRS FM01-FM03, run 10/12/2026) ----------------
# program, fund, annual FY27 allotment, Q1 allotment, Q1 actual as first run
ROWS = [
    ("010", "Administration & Agency Support", "001-1 GF-S", D("4860000"), D("1215000"), D("1108742.36")),
    ("010", "Administration & Agency Support", "26H-1 HSA-S", D("1140000"), D("285000"), D("279415.90")),
    ("020", "Housing Stability Rental Assistance", "001-1 GF-S", D("38400000"), D("9800000"), D("10373542.05")),
    ("020", "Housing Stability Rental Assistance", "26H-1 HSA-S", D("22600000"), D("5650000"), D("5702118.40")),
    ("030", "Shelter & Homeless Services", "001-1 GF-S", D("9500000"), D("2375000"), D("2301876.12")),
    ("030", "Shelter & Homeless Services", "001-2 GF-F (ESG)", D("5480000"), D("1260000"), D("1018233.47")),
    ("030", "Shelter & Homeless Services", "26H-1 HSA-S", D("14800000"), D("3700000"), D("3688402.75")),
    ("040", "Landlord Mitigation & Housing Navigation", "001-1 GF-S", D("3200000"), D("800000"), D("512960.30")),
    ("040", "Landlord Mitigation & Housing Navigation", "26H-1 HSA-S", D("2400000"), D("600000"), D("571880.64")),
]
ANNUAL_TOTAL = sum(r[3] for r in ROWS)
Q1_ALLOT_TOTAL = sum(r[4] for r in ROWS)
Q1_ACT_TOTAL = sum(r[5] for r in ROWS)

P020_MONTHS = [("July", D("3400000"), D("3612410.22")), ("August", D("3200000"), D("3498227.65")),
               ("September", D("3200000"), D("3262904.18"))]
assert sum(x[2] for x in P020_MONTHS) == ROWS[2][5]
assert sum(x[1] for x in P020_MONTHS) == ROWS[2][4]

# Reconciling items from Accounting
ACCRUAL = D("612480.00")      # Sept grantee invoices keyed in FM04 (D2 email)
ACCRUAL_PARTS = [("Capitol Region Housing Partners", D("287915.00")), ("Spokane Valley Tenant Services", D("201330.00")),
                 ("Yakima Basin Community Action", D("123235.00"))]
assert sum(x[1] for x in ACCRUAL_PARTS) == ACCRUAL
MISCODE = D("18240.00")       # P030 shelter payment coded to P020 GF-S (D4 email)

P020_GFS_ADJ = ROWS[2][5] + ACCRUAL - MISCODE
P020_GFS_VAR = ROWS[2][4] - P020_GFS_ADJ                    # -1,167,782.05
P030_GFS_ADJ = ROWS[4][5] + MISCODE
P030_GFS_VAR = ROWS[4][4] - P030_GFS_ADJ
P020_GFS_VAR_PRE = ROWS[2][4] - ROWS[2][5]
P020_GFS_VAR_ACCRUAL_ONLY = ROWS[2][4] - (ROWS[2][5] + ACCRUAL)

P020_MONTHLY_ADJ = r2(P020_GFS_ADJ / 3)
P020_PROJ = P020_GFS_ADJ * 4                                # straight line: 9 more months at the Q1 average
P020_GAP = P020_PROJ - ROWS[2][3]
DP_M1 = D("3900000")
GAP_BEYOND_DP = P020_GAP - DP_M1
REMAIN_ALLOT_P020 = ROWS[2][3] - ROWS[2][4]                 # Oct-Jun allotment
Q1_ACT_TOTAL_ADJ = Q1_ACT_TOTAL + ACCRUAL                   # miscode nets to zero agency-wide

# Q6 allotment (submitted 10/23) monthly P020 GF-S Oct-Jun: unchanged total 28.6M
P020_ALLOT_OCT_JUN = [D("3200000"), D("3200000"), D("3150000"), D("3150000"), D("3150000"), D("3150000"),
                      D("3200000"), D("3200000"), D("3200000")]
assert sum(P020_ALLOT_OCT_JUN) == REMAIN_ALLOT_P020

# ---------------- Households (grantee data, all fund sources) ----------------
FY26_HH = 21720
FY26_AVG = D("2360")
FY26_PAID = FY26_HH * FY26_AVG
FY26_HH_MO = D(FY26_HH) / 12                                 # 1,810
Q1_HH = [("July", 1942, D("2548")), ("August", 1968, D("2561")), ("September", 1989, D("2566"))]
Q1_HH_TOTAL = sum(x[1] for x in Q1_HH)
Q1_PAID = sum(x[1] * x[2] for x in Q1_HH)
Q1_AVG = r2(Q1_PAID / Q1_HH_TOTAL)                           # 2,558.41
Q1_HH_MO = D(Q1_HH_TOTAL) / 3
HH_GROWTH = (Q1_HH_MO / FY26_HH_MO - 1) * 100
AVG_GROWTH = (Q1_AVG / FY26_AVG - 1) * 100
GFS_SHARE = ROWS[2][3] / (ROWS[2][3] + ROWS[3][3])          # 38.4 / 61.0
# Options (9 remaining months)
OPT_A_ALL = r2((Q1_HH_MO - FY26_HH_MO) * Q1_AVG * 9)
OPT_A_GFS = r2(OPT_A_ALL * GFS_SHARE)
OPT_B_ALL = r2((Q1_AVG - FY26_AVG) * Q1_HH_MO * 9)
OPT_B_GFS = r2(OPT_B_ALL * GFS_SHARE)

# ---------------- Program 040 proviso ----------------
PROVISO = D("1800000")
PROVISO_Q1_ALLOT = D("450000")
PROVISO_Q1 = D("214350.00")
PROVISO_PROJ = r2(PROVISO_Q1 / 3 * 12)                       # 857,400
PROVISO_LAPSE = PROVISO - PROVISO_PROJ                       # 942,600
P040_NONPROVISO_Q1 = ROWS[7][5] - PROVISO_Q1
P040_NONPROVISO_ALLOT_Q1 = ROWS[7][4] - PROVISO_Q1_ALLOT
P040_NONPROVISO_ANNUAL = ROWS[7][3] - PROVISO

# ---------------- Positions ----------------
FTE_BUDGET = D("186.5")
FTE_FILLED_1031 = D("171.0")
FTE_VACANT_1031 = FTE_BUDGET - FTE_FILLED_1031               # 15.5
FTE_FILLED_NOV1 = FTE_FILLED_1031 + 2                         # two P010 Fiscal Analyst 3 start Nov 1
FTE_VACANT_NOV1 = FTE_BUDGET - FTE_FILLED_NOV1                # 13.5
POS = [  # program, budgeted, filled 10/31
    ("010", D("38.0"), D("33.0")), ("020", D("61.5"), D("57.0")), ("030", D("52.0"), D("48.0")), ("040", D("35.0"), D("33.0"))]
assert sum(p[1] for p in POS) == FTE_BUDGET and sum(p[2] for p in POS) == FTE_FILLED_1031

# ---------------- Fiscal note H-0287.1/27 ----------------
SAL = {"MA5": D("98736"), "PS3": D("72180"), "FA2": D("68604"), "CSS2": D("52836")}
OLD_SAL = {"MA5": D("88212"), "PS3": D("64488"), "FA2": D("61308"), "CSS2": D("47280")}
BEN_PCT = D("0.224")
INS = D("16140")
OLD_BEN_PCT = D("0.312")
GS_FTE = D("6300")
OLD_GS_FTE = D("5400")
TRAVEL_FTE = D("1200")
EQUIP = D("4800")
INDIRECT = D("0.126")
AAG = D("18000")
HOTLINE_MO = D("8000")
AVG_PAY = D("1850")
HH_YEAR = 650


def fn_year(staff, months_hotline, households, new_hires, aag):
    """staff: list of (class, fte, months)."""
    fte = sum(D(f) * D(mo) / 12 for _, f, mo in staff)
    a = r2(sum(SAL[c] * D(f) * D(mo) / 12 for c, f, mo in staff))
    b = r2(a * BEN_PCT) + r2(INS * fte)
    c = HOTLINE_MO * months_hotline
    e = r2(GS_FTE * fte) + EQUIP * new_hires + aag
    g = r2(TRAVEL_FTE * fte)
    n = AVG_PAY * households
    t = r2((a + b) * INDIRECT)
    total = a + b + c + e + g + n + t
    return dict(fte=fte, A=a, B=b, C=c, E=e, G=g, N=n, T=t, total=total, ben_pct=r2(a * BEN_PCT), ins=r2(INS * fte),
                gs=r2(GS_FTE * fte), equip=EQUIP * new_hires, aag=aag)


FY28 = fn_year([("MA5", 1, 11), ("PS3", 1, 8), ("PS3", 1, 6), ("FA2", D("0.5"), 6)], 6, 325, 4, AAG)
FY29 = fn_year([("MA5", 1, 12), ("PS3", 2, 12), ("FA2", D("0.5"), 12)], 12, HH_YEAR, 0, D(0))
FYOUT = fn_year([("MA5", 1, 12), ("PS3", 2, 12), ("FA2", D("0.5"), 12)], 12, HH_YEAR, 0, D(0))
BI_2729 = FY28["total"] + FY29["total"]
BI_2931 = FYOUT["total"] * 2
BI_3133 = FYOUT["total"] * 2
FY28_ROUND = FY28["total"].quantize(D("1"), rounding=ROUND_HALF_UP)

# Hotline in-house alternative (2.0 Customer Service Specialist 2), ongoing year
HL_A = SAL["CSS2"] * 2
HL_B = r2(HL_A * BEN_PCT) + INS * 2
HL_E = GS_FTE * 2
HL_G = TRAVEL_FTE * 0
HL_T = r2((HL_A + HL_B) * INDIRECT)
HL_INHOUSE = HL_A + HL_B + HL_E + HL_T
HL_INHOUSE_EQUIP = EQUIP * 2
HL_CONTRACT = HOTLINE_MO * 12

# Owen's (program) input: old model, 3.0 FTE + 2.0 CSS2 in-house all of FY28 from July 1, 650 x $2,000, no indirect
OW_A = OLD_SAL["MA5"] + OLD_SAL["PS3"] * 2 + OLD_SAL["CSS2"] * 2
OW_B = r2(OW_A * OLD_BEN_PCT)
OW_E = OLD_GS_FTE * 5 + EQUIP * 5
OW_N = D("2000") * HH_YEAR
OW_TOTAL = OW_A + OW_B + OW_E + OW_N

# ---------------- ESG ----------------
ESG_AWARD = D("6212000")
ESG_ADMIN_CAP = r2(ESG_AWARD * D("0.075"))                   # 465,900
ESG_ADMIN_RETAINED = r2(ESG_AWARD * D("0.06"))              # 372,720
ESG_ADMIN_SHARED = ESG_ADMIN_CAP - ESG_ADMIN_RETAINED        # 93,180
ESG_ADMIN_SPENT = D("341055.18")
ESG_ADMIN_LEFT = ESG_ADMIN_RETAINED - ESG_ADMIN_SPENT
LUNCH = [("Venue rental, Tumwater Community Center (full day)", D("2400.00")),
         ("Catered lunch, 140 attendees x $28.50", D("3990.00")),
         ("Evening wine and cheese reception", D("1260.00")),
         ("Provider appreciation gift cards, 80 x $25", D("2000.00")),
         ("AV equipment rental", D("196.50"))]
LUNCH_TOTAL = sum(x[1] for x in LUNCH)
LUNCH_MAYBE = LUNCH[0][1] + LUNCH[1][1] + LUNCH[4][1]
LUNCH_NO = LUNCH[2][1] + LUNCH[3][1]
ESG_DELAYED = [("Grays Harbor Shelter Collaborative", D("410000")), ("Okanogan County Housing Authority", D("385000")),
               ("Walla Walla Valley Family Shelter", D("345000"))]
ESG_DELAYED_TOTAL = sum(x[1] for x in ESG_DELAYED)
ESG_DELAYED_Q2 = r2(ESG_DELAYED_TOTAL / 9 * 3)                # 3 of 9 contract months shift out of Q2

# ---------------- Indirect question (Kevin) ----------------
KV = dict(personnel=D("212400"), travel=D("8600"), supplies=D("4000"), subaward=D("220000"), other=D("9000"))
KV_DIRECT = sum(KV.values())
KV_MTDC = KV["personnel"] + KV["travel"] + KV["supplies"] + D("50000") + KV["other"]
KV_DEMIN = r2(KV_MTDC * D("0.15"))
KV_TOTAL_DEMIN = KV_DIRECT + KV_DEMIN
NICR = D("0.162")
KV_NICR = r2(KV["personnel"] * NICR)
KV_TOTAL_NICR = KV_DIRECT + KV_NICR
KV_CAP = D("500000")
KV_ROOM = KV_CAP - KV_TOTAL_NICR

# ---------------- Laptops ----------------
LAP_N, LAP_EOL, LAP_UNIT = 60, 32, D("1410")
LAP_ALL = LAP_UNIT * LAP_N
LAP_NOW = LAP_UNIT * LAP_EOL
LAP_DEFER = LAP_ALL - LAP_NOW
P010_Q1_UNDER = ROWS[0][4] - ROWS[0][5]

if __name__ == "__main__":
    for k, v in sorted(globals().items()):
        if k.isupper() and not callable(v):
            print(k, v)

# combined option A+B and GF-S totals (added)
OPT_AB_ALL = r2((Q1_PAID / 3 - FY26_HH_MO * FY26_AVG) * 9)
OPT_AB_GFS = r2(OPT_AB_ALL * GFS_SHARE)
OPT_A_HH = r2((Q1_HH_MO - FY26_HH_MO) * 9)
GFS_Q1_ALLOT = ROWS[0][4] + ROWS[2][4] + ROWS[4][4] + ROWS[7][4]
GFS_Q1_ADJ = ROWS[0][5] + P020_GFS_ADJ + P030_GFS_ADJ + ROWS[7][5]
GFS_Q1_VAR = GFS_Q1_ALLOT - GFS_Q1_ADJ
PROVISO_MONTHS = [("July", D("68920.00")), ("August", D("71180.00")), ("September", D("74250.00"))]
assert sum(x[1] for x in PROVISO_MONTHS) == PROVISO_Q1
P010_PROJ_UNDER = P010_Q1_UNDER * 4


def pct(x):
    return f"{(x * 100).normalize():f}"
