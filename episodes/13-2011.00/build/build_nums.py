"""Every number the 13-2011.00 episode uses, computed once so the items agree with each other."""
from decimal import Decimal as D, ROUND_HALF_UP


def m(x):
    """Money with thousands separators; negatives in parentheses."""
    x = D(x).quantize(D("0.01"), rounding=ROUND_HALF_UP)
    s = f"{abs(x):,.2f}"
    return f"({s})" if x < 0 else s


def w(x):
    """Whole dollars."""
    x = D(x).quantize(D("1"), rounding=ROUND_HALF_UP)
    s = f"{abs(x):,.0f}"
    return f"({s})" if x < 0 else s


# ---- operating account 1010 / Lattimore ****4471 ----
B0 = D("2412906.33"); DIT0 = D("54118.62"); OS0 = D("131406.27")
G0 = B0 + DIT0 - OS0
OS_CHECKS = [
    ("48266", "10/27", "Midstate Packaging Corp.", D("9812.40")),
    ("48273", "10/27", "Columbus Industrial Gas Co.", D("3402.15")),
    ("48280", "10/28", "Tri-County Waste Services", D("2915.00")),
    ("48284", "10/28", "Dayton Fastener Supply", D("27640.80")),
    ("48288", "10/29", "Gantry Freight Lines", D("41227.30")),
    ("48291", "10/29", "Pemberton Electric LLC", D("6118.00")),
    ("48295", "10/30", "Ashwood Rubber Products", D("54880.00")),
    ("48297", "10/30", "Lindell Tool & Die", D("66885.00")),
]
OS = sum(c[3] for c in OS_CHECKS)
DIT = D("96204.18")
DUP = D("18430.00"); FEE = D("1245.00"); MERCH_BANK = D("4650.00"); MERCH_GL = D("4560.00")

GL_R = [("Lockbox deposits", D("12884215.40")),
        ("ACH/wire receipts - bank file cash application (BAI2 import)", D("5612330.85")),
        ("Manual wire receipts (entered by AR)", D("412775.20")),
        ("Remote deposit capture", D("1203664.09"))]
GL_D = [("AP ACH payment runs", D("9874120.66")),
        ("Checks issued (check runs 10/06-10/30, #48102-#48297)", D("1146382.91")),
        ("Payroll - ADP net pay and tax impounds", D("2688430.12")),
        ("Benefits funding and 401(k) remittances", D("1012884.37")),
        ("Ohio sales tax payment (September UST-1)", D("148227.64")),
        ("Revolver net repayments (ABL sweep)", D("4250000.00")),
        ("Revolver interest (September)", D("138412.50")),
        ("Merchant card fees, JE-10-0107 (J. Wolcott, 10/06)", MERCH_GL)]
GL_RT = sum(v for _, v in GL_R); GL_DT = sum(v for _, v in GL_D)
G1 = G0 + GL_RT - GL_DT

BK_R = [("Lockbox deposits (21)", GL_R[0][1]),
        ("ACH and wire credits (198)", GL_R[1][1] - DUP + GL_R[2][1]),
        ("Remote deposit capture (19)", GL_R[3][1] - DIT + DIT0)]
BK_D = [("ACH debits - AP payment runs (9 files)", GL_D[0][1]),
        ("Checks paid (164)", GL_D[1][1] - OS + OS0),
        ("ADP payroll debits (6)", GL_D[2][1]),
        ("Benefits and 401(k) debits (5)", GL_D[3][1]),
        ("OHIO DEPT TAX ACH debit 10/23", GL_D[4][1]),
        ("Loan transfers to revolver, sweep (22)", GL_D[5][1]),
        ("Loan interest debit 10/01", GL_D[6][1]),
        ("FISERV MERCH FEES 10/05", MERCH_BANK),
        ("ACCOUNT ANALYSIS CHG 10/30 (September service period)", FEE)]
BK_RT = sum(v for _, v in BK_R); BK_DT = sum(v for _, v in BK_D)
B1 = B0 + BK_RT - BK_DT
ADJ_BANK = B1 + DIT - OS
DIFF = G1 - ADJ_BANK
assert DIFF == DUP + FEE + (MERCH_BANK - MERCH_GL) == D("19765.00"), DIFF
assert G1 - FEE - (MERCH_BANK - MERCH_GL) - DUP == ADJ_BANK

# ---- prepaid 1410 ----
PREPAID = [  # name, term, total, monthly, months amortized before October, should amortize in October?
    ("Property & casualty package (Brookfield Mutual)", "07/01/26-06/30/27", D("186000.00"), D("15500.00"), 3, True),
    ("Umbrella / product liability", "07/01/26-06/30/27", D("64800.00"), D("5400.00"), 3, True),
    ("D&O / EPL", "04/01/26-03/31/27", D("38400.00"), D("3200.00"), 6, True),
    ("Cyber liability", "08/15/26-08/14/27", D("47000.00"), D("3916.67"), 2, True),
    ("NetSuite annual subscription", "02/01/26-01/31/27", D("97200.00"), D("8100.00"), 8, True),
    ("FloQast annual subscription", "11/01/25-10/31/26", D("26400.00"), D("2200.00"), 11, True),
    ("Avalara AvaTax annual", "01/01/26-12/31/26", D("14400.00"), D("1200.00"), 9, True),
    ("Forklift fleet maintenance contract", "01/01/26-12/31/26", D("27000.00"), D("2250.00"), 9, True),
    ("Salesforce Sales Cloud annual (not renewed; CRM moved to NetSuite 10/01)", "10/01/25-09/30/26", D("30000.00"), D("2500.00"), 12, False),
]
TRADE_SHOW = D("12000.00")
PRE_BEGIN = sum(t - mo * k for _, _, t, mo, k, _ in PREPAID) + TRADE_SHOW
PRE_AMORT_PRIYA = sum(mo for *_, mo, k, ok in [(p[0], p[1], p[2], p[3], p[4], p[5]) for p in PREPAID])
PRE_AMORT_OK = sum(p[3] for p in PREPAID if p[5])
assert PRE_AMORT_OK == D("41766.67") and PRE_AMORT_PRIYA == D("44266.67")

# ---- payroll accrual ----
GROSS_HOURLY = D("812460.00"); GROSS_SAL = D("714380.00"); GROSS = GROSS_HOURLY + GROSS_SAL
ER_TAX_RATE = D("0.0765")
PAY_ACCR_WAGES = GROSS * 5 / 10
PAY_ACCR_TAX = (PAY_ACCR_WAGES * ER_TAX_RATE).quantize(D("0.01"), rounding=ROUND_HALF_UP)
PAY_ACCR = PAY_ACCR_WAGES + PAY_ACCR_TAX
assert PAY_ACCR == D("821821.63")

# ---- accrued expenses JE-10-0412 (Elena prepares) ----
ACCR = [("Northfield Mechanical Services - preventive maintenance shutdown 10/19-10/23 (inv NMS-20417 rec'd 11/03)", "6420 Repairs & maintenance", D("27300.00")),
        ("Gantry Freight Lines - October shipments not yet billed (Gantry estimate 11/03)", "6300 Freight-out", D("34180.00")),
        ("Electric and gas, October (3-month average; bills arrive mid-November)", "6500 Utilities", D("18600.00"))]
ACCR_T = sum(a[2] for a in ACCR)
assert ACCR_T == D("80080.00")

# ---- use tax ----
BRIGHTLINE = D("38400.00"); USE_RATE = D("0.08"); USE_TAX = BRIGHTLINE * USE_RATE
assert USE_TAX == D("3072.00")

# ---- revenue cutoff ----
SHIP = [  # ship date, BOL, customer, invoice, terms, carrier, POD, amount, cost, tax
    ("10/29", "B-77412", "Brennan Tractor Co.", "10598", "FOB Shipping Point", "Gantry LTL", "10/30", D("38420.00"), D("27105.00"), "exempt (resale cert.)"),
    ("10/29", "B-77415", "Hartline Mechanical Contractors", "10601", "FOB Shipping Point", "customer pickup", "10/29", D("6882.40"), D("4710.00"), "OH taxable, 8.0%"),
    ("10/29", "B-77419", "Lakeview Irrigation", "10603", "FOB Destination", "Gantry LTL", "10/30", D("17560.00"), D("12380.00"), "exempt (agricultural)"),
    ("10/30", "B-77426", "Ridgeway Agricultural Supply", "10611", "FOB Destination", "Gantry LTL", "11/02", D("46180.00"), D("33250.00"), "exempt (resale cert.)"),
    ("10/30", "B-77428", "Carver Marine Hydraulics", "10614", "FOB Destination", "Gantry LTL", "11/03", D("22905.50"), D("16720.00"), "exempt (resale cert.)"),
    ("10/30", "B-77431", "Dunmore Equipment", "10616", "FOB Shipping Point", "Dunmore truck", "11/02", D("29744.00"), D("21260.00"), "exempt (resale cert.)"),
    ("10/30", "B-77433", "Tri-State Mill Services", "10619", "FOB Destination", "Gantry LTL", "11/02", D("11734.25"), D("8450.00"), "exempt (resale cert.)"),
    ("10/30", "B-77436", "Brennan Tractor Co. (expedite)", "10620", "FOB Shipping Point", "Ace Hotshot", "10/30", D("9215.00"), D("6480.00"), "exempt (resale cert.)"),
]
CUT_REV = sum(s[7] for s in SHIP if s[4] == "FOB Destination" and s[6].startswith("11/"))
CUT_COST = sum(s[8] for s in SHIP if s[4] == "FOB Destination" and s[6].startswith("11/"))
assert CUT_REV == D("80819.75") and CUT_COST == D("58420.00")

# ---- P&L (whole dollars): Sep actual, Oct prelim, Oct budget ----
PL = [("Net sales", 19604850, 18742300, 19100000),
      ("Cost of goods sold", 13920600, 13364500, 13561000)]
OPEX = [("Salaries & wages (SG&A)", 1262000, 1323400, 1301000),
        ("Payroll taxes & benefits", 341200, 352900, 349000),
        ("Sales commissions", 401200, 383500, 392000),
        ("Freight-out", 336900, 412600, 340000),
        ("Rent & occupancy", 214600, 214600, 214600),
        ("Repairs & maintenance", 61320, 96450, 88000),
        ("Utilities", 48900, 51200, 50000),
        ("Professional fees", 31400, 36100, 35000),
        ("Software & subscriptions", 39800, 40100, 41000),
        ("Insurance", 28017, 28017, 28100),
        ("Bank & merchant fees", 5610, 5895, 5500),
        ("Depreciation", 182300, 184900, 185000),
        ("Travel & entertainment", 44800, 29300, 30000),
        ("Vehicle & fleet", 57800, 59100, 58000),
        ("Other operating", 72100, 69400, 70000)]
INTEREST = ("Interest expense", 138400, 131700, 135000)


def pl_sheet():
    rows = []
    def row(n, s, o, b):
        d = o - s; pct = (d / s * 100) if s else 0
        rows.append(f"{n} | {w(s)} | {w(o)} | {w(b)} | {w(d)} | {pct:+.1f}%")
    sales, cogs = PL
    row(*sales); row(*cogs)
    gp = [sales[i] - cogs[i] for i in (1, 2, 3)]
    row("Gross profit", *gp)
    for r in OPEX:
        row(*r)
    ox = [sum(r[i] for r in OPEX) for i in (1, 2, 3)]
    row("Total operating expenses", *ox)
    oi = [gp[i] - ox[i] for i in range(3)]
    row("Operating income", *oi)
    row(*INTEREST)
    pti = [oi[i] - INTEREST[i + 1] for i in range(3)]
    row("Income before taxes", *pti)
    return rows, gp, ox, oi, pti


PL_ROWS, GP, OX, OI, PTI = pl_sheet()

# ---- trial balance 9/30 (Dr positive) ----
SEP_OPEX = OX[0]
TB = [("1010", "Cash - operating (Lattimore ****4471)", G0),
      ("1015", "Cash - payroll (Lattimore ****4489)", D("25000.00")),
      ("1030", "Cash - money market (Lattimore ****7702)", D("1250000.00")),
      ("1200", "Accounts receivable - trade", D("27846912.40")),
      ("1250", "Allowance for doubtful accounts", D("-412000.00")),
      ("1300", "Inventory", D("31904227.85")),
      ("1350", "Inventory reserve", D("-1186400.00")),
      ("1410", "Prepaid expenses", PRE_BEGIN),
      ("1500", "Property, plant & equipment, at cost", D("38620450.00")),
      ("1590", "Accumulated depreciation", D("-19442880.00")),
      ("1700", "Other assets", D("1104300.00")),
      ("2010", "Accounts payable - trade", D("-14226518.33")),
      ("2110", "Accrued liabilities", D("-2904615.40")),
      ("2120", "Accrued payroll", D("-812604.18")),
      ("2310", "Sales tax payable (OH 148,227.64; IN 2,188.40; PA 1,224.18)", D("-151640.22")),
      ("2320", "Use tax payable", D("0.00")),
      ("2350", "Income taxes payable", D("-1312000.00")),
      ("2400", "ABL revolver - Lattimore Bank", D("-14250000.00")),
      ("2500", "Term loan - Lattimore Bank", D("-6000000.00")),
      ("3000", "Common stock and APIC", D("-18500000.00")),
      ("4000", "Net sales (YTD)", D("-171906330.00")),
      ("5000", "Cost of goods sold (YTD)", D("122083420.00")),
      ("6000", "Operating expenses (YTD)", D("28116904.00")),
      ("7000", "Interest expense (YTD)", D("1262300.00")),
      ("8000", "Income tax expense (YTD)", D("5111000.00"))]
RE = -sum(v for _, _, v in TB)
TB.insert(20, ("3100", "Retained earnings", RE))
assert sum(v for _, _, v in TB) == 0

if __name__ == "__main__":
    print("G0", G0, "G1", G1, "B1", B1, "ADJ", ADJ_BANK, "DIFF", DIFF, "OS", OS)
    print("prepaid begin", PRE_BEGIN, "RE", RE)
    for r in PL_ROWS: print(r)
