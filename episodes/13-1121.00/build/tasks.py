import csv,sys
root=sys.argv[1]
soc="13-1121.00"
pen={}
with open(root+"/aei/task_penetration.csv") as f:
    for r in csv.DictReader(f): pen[r["task"].strip().lower()]=r["penetration"]
rat={}
with open(root+"/onet/db_31_0_text/Task Ratings.txt") as f:
    for r in csv.DictReader(f,delimiter="\t"):
        if r["O*NET-SOC Code"]!=soc: continue
        rat.setdefault(r["Task ID"],{})
        if r["Scale ID"]=="IM": rat[r["Task ID"]]["IM"]=r["Data Value"]
        if r["Scale ID"]=="RT": rat[r["Task ID"]]["RT"]=r["Data Value"]
        if r["Scale ID"]=="FT":
            rat[r["Task ID"]].setdefault("FT",{})[r["Category"]]=float(r["Data Value"])
with open(root+"/onet/db_31_0_text/Task Statements.txt") as f:
    for r in csv.DictReader(f,delimiter="\t"):
        if r["O*NET-SOC Code"]!=soc: continue
        t=r["Task ID"]; x=rat.get(t,{})
        ft=x.get("FT",{})
        # categories 1..7: yearly or less, more than yearly, more than monthly, more than weekly, daily, several times daily, hourly+
        mean=sum(int(k)*v for k,v in ft.items())/max(1,sum(ft.values())) if ft else 0
        daily=sum(v for k,v in ft.items() if int(k)>=5)
        print(f'{t}\t{r["Task Type"]}\tIM={x.get("IM")}\tRT={x.get("RT")}\tFTmean={mean:.2f}\tdaily+={daily:.0f}%\tpen={pen.get(r["Task"].strip().lower())}\t{r["Task"]}')
