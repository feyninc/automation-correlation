import csv,sys
root=sys.argv[1]; soc="23-2011.00"; D=root+"/data/onet/db_31_0_text/"
def rows(f): return [r for r in csv.DictReader(open(D+f,encoding="utf-8"),delimiter="\t") if r["O*NET-SOC Code"]==soc]
cat={}
for r in csv.DictReader(open(D+"Work Context Categories.txt",encoding="utf-8"),delimiter="\t"):
    cat[(r["Element ID"],r["Scale ID"],r["Category"])]=r["Category Description"]
print("== Work Context (CX/CT means)")
for r in rows("Work Context.txt"):
    if r["Scale ID"] in("CX","CT"):
        print(r["Element Name"],r["Scale ID"],r["Data Value"])
print("== Work Activities IM>=3.8")
for r in rows("Work Activities.txt"):
    if r["Scale ID"]=="IM" and float(r["Data Value"])>=3.8: print(r["Element Name"],r["Data Value"])
print("== Software")
for r in rows("Software Skills.txt"):
    print(r.get("Example") , "|", r.get("Commodity Title"), "|", r.get("Hot Technology"))
print("== Job zone"); print(rows("Job Zones.txt"))
