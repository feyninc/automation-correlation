import csv,sys
root=sys.argv[1]
soc="23-2011.00"
D=root+"/data/onet/db_31_0_text/"
tasks={}
for r in csv.DictReader(open(D+"Task Statements.txt",encoding="utf-8"),delimiter="\t"):
    if r["O*NET-SOC Code"]==soc: tasks[r["Task ID"]]=r
print(list(next(iter(tasks.values())).keys()))
rat={}
for r in csv.DictReader(open(D+"Task Ratings.txt",encoding="utf-8"),delimiter="\t"):
    if r["O*NET-SOC Code"]==soc: rat.setdefault(r["Task ID"],[]).append(r)
pen={}
for r in csv.DictReader(open(root+"/data/aei/task_penetration.csv",encoding="utf-8")):
    pen[r["task"].strip()]=r["penetration"]
for tid,t in tasks.items():
    rs=rat.get(tid,[])
    im=[x["Data Value"] for x in rs if x["Scale ID"]=="IM"]
    rt=[x["Data Value"] for x in rs if x["Scale ID"]=="RT"]
    fq={x["Category"]:x["Data Value"] for x in rs if x["Scale ID"]=="FT"}
    # mean freq category weighted
    mf=sum(int(k)*float(v) for k,v in fq.items())/100 if fq else None
    # share daily or more: cats 5,6,7
    daily=sum(float(v) for k,v in fq.items() if k in("5","6","7"))
    print(tid,t["Task Type"],"IM",im,"RT",rt,"FTmean",round(mf,2) if mf else None,"daily+%",round(daily,1),"pen",pen.get(t["Task"].strip()),"|",t["Task"])
