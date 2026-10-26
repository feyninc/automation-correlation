from decimal import Decimal as D
pre=[("Property & casualty package","07/01/26-06/30/27","186000.00","15500.00",3),("Umbrella / product liability","07/01/26-06/30/27","64800.00","5400.00",3),("D&O / EPL","04/01/26-03/31/27","38400.00","3200.00",6),("Cyber liability","08/15/26-08/14/27","47000.00","3916.67",2),("NetSuite annual subscription","02/01/26-01/31/27","97200.00","8100.00",8),("FloQast annual subscription","11/01/25-10/31/26","26400.00","2200.00",11),("Avalara AvaTax annual","01/01/26-12/31/26","14400.00","1200.00",9),("Forklift fleet maintenance contract","01/01/26-12/31/26","27000.00","2250.00",9),("Salesforce Sales Cloud annual","10/01/25-09/30/26","30000.00","2500.00",12)]
tot0=D(0)
for n,p,t,m,k in pre:
    b=D(t)-D(m)*k; tot0+=b; print(n,b)
print("prepaid 9/30 amortizing",tot0,"+trade show 12000 =",tot0+12000)
