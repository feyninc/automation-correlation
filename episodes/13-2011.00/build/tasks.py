import csv,sys
root=sys.argv[1]; O=root+"/data/onet/db_31_0_text/"
soc="13-2011.00"
tasks={r["Task ID"]:r["Task"] for r in csv.DictReader(open(O+"Task Statements.txt"),delimiter="\t") if r["O*NET-SOC Code"]==soc}
im={};ft={}
for r in csv.DictReader(open(O+"Task Ratings.txt"),delimiter="\t"):
    if r["O*NET-SOC Code"]!=soc: continue
    if r["Scale ID"]=="IM": im[r["Task ID"]]=float(r["Data Value"])
    if r["Scale ID"]=="FT": ft.setdefault(r["Task ID"],{})[int(r["Category"])]=float(r["Data Value"])
pen={}
for r in csv.DictReader(open(root+"/data/aei/task_penetration.csv")):
    pen[r["task"].strip()]=float(r["penetration"])
# FT categories: 1 yearly or less,2 more than yearly,3 more than monthly,4 more than weekly,5 daily,6 several times daily,7 hourly+
rows=[]
for t,txt in tasks.items():
    f=ft.get(t,{})
    mean=sum(k*v for k,v in f.items())/100 if f else 0
    daily=sum(v for k,v in f.items() if k>=5)
    rows.append((t,im.get(t),round(mean,2),round(daily,1),pen.get(txt.strip(),"NA"),txt[:90]))
rows.sort(key=lambda r:-r[2])
print("id\tIM\tFTmean\t%daily+\tpen\ttask")
for r in rows: print("\t".join(map(str,r)))
