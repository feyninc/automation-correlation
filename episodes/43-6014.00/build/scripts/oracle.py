import json,sys
e=json.load(open(sys.argv[1]))
acts={a['id']:a for d in e['days'] for a in d['actions']}
def ev(p,txt):
    (k,v),=p.items()
    if k=='all': return all(ev(q,txt) for q in v)
    if k=='any': return any(ev(q,txt) for q in v)
    if k=='not': return True
    if k=='mentions_any': return any(x.lower() in txt for x in v)
    if k=='mentions_all': return all(x.lower() in txt for x in v)
    if k=='number_equals':
        import re
        val=v['value']; nums=[float(x.replace(',','')) for x in re.findall(r'\$?(\d[\d,]*\.?\d*)',txt)]
        return any(abs(n-val)<=v['tol']+1e-9 for n in nums)
    return True
for n in e['needs']:
    r=n['reference'].get('action_id')
    if not r: continue
    a=acts[r]; txt=(a['content']).lower()
    ok=ev(n['check'],txt)
    late=a['at']<=n['deadline']
    print(n['id'],r,a['at'],'text-ok' if ok else 'TEXT-FAIL','in-time' if late else 'after-deadline')
# traps vs human actions: mention-only parts
for t in e['traps']:
    hits=[a['id'] for a in acts.values() if ev(t['check'],a['content'].lower())]
    print(t['id'],'mention-pattern hits in human actions (ignoring recipients/time):',hits)
