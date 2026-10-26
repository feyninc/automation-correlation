from decimal import Decimal as D
B0=D("2412906.33"); DIT0=D("54118.62"); OS0=D("131406.27")
G0=B0+DIT0-OS0
print("G0",G0)
os_checks=[("48266","10/27","Midstate Packaging Corp.","9812.40"),("48273","10/27","Columbus Industrial Gas Co.","3402.15"),("48280","10/28","Tri-County Waste Services","2915.00"),("48284","10/28","Dayton Fastener Supply","27640.80"),("48288","10/29","Gantry Freight Lines","41227.30"),("48291","10/29","Pemberton Electric LLC","6118.00"),("48295","10/30","Ashwood Rubber Products","54880.00"),("48297","10/30","Lindell Tool & Die","66885.00")]
OS=sum(D(x[3]) for x in os_checks); print("OS",OS)
DIT=D("96204.18")
gl={"Lockbox deposits":D("12884215.40"),"ACH/wire receipts - bank file cash application":D("5612330.85"),"Manual wire receipts":D("412775.20"),"Remote deposit capture":D("1203664.09")}
gld={"AP ACH payment runs":D("9874120.66"),"Checks issued":D("1146382.91"),"Payroll - ADP net pay and tax impounds":D("2688430.12"),"Benefits funding and 401(k) remittances":D("1012884.37"),"Ohio sales tax payment (Sept UST-1)":D("148227.64"),"Revolver net repayments (ABL sweep)":D("4250000.00"),"Revolver interest (Sept)":D("138412.50"),"Merchant card fees JE-10-0107":D("4560.00")}
R=sum(gl.values()); Dd=sum(gld.values())
G1=G0+R-Dd; print("GLend",G1,"R",R,"D",Dd)
bank_r={"Lockbox deposits":gl["Lockbox deposits"],"ACH and wire credits":gl["ACH/wire receipts - bank file cash application"]-D("18430.00")+gl["Manual wire receipts"],"Remote deposit capture":gl["Remote deposit capture"]-DIT+DIT0}
bank_d={"ACH debits - AP payment runs":gld["AP ACH payment runs"],"Checks paid":gld["Checks issued"]-OS+OS0,"ADP payroll debits":gld["Payroll - ADP net pay and tax impounds"],"Benefits and 401(k) debits":gld["Benefits funding and 401(k) remittances"],"Ohio Dept of Taxation ACH debit":gld["Ohio sales tax payment (Sept UST-1)"],"Loan transfers to revolver":gld["Revolver net repayments (ABL sweep)"],"Loan interest debit":gld["Revolver interest (Sept)"],"Merchant services fees":D("4650.00"),"Account analysis fee (Oct)":D("1245.00")}
BR=sum(bank_r.values()); BD=sum(bank_d.values()); B1=B0+BR-BD
print("bank_r",bank_r,BR); print("bank_d",bank_d,BD); print("Bank end",B1)
adj=B1+DIT-OS; print("adj bank",adj,"diff",G1-adj)
