import json,re,sys
e=json.load(open(sys.argv[1]))
items={i['id']:i for i in e['items']}
def mins(t):
    m=re.match(r"D(\d)(?: (\d\d):(\d\d))?$",t); d,h,mi=m.groups(); return int(d)*1440+(int(h)*60+int(mi) if h else 0)
CH={'reply':None}
def prop_of(a):
    tgt=a.get('target'); it=items.get(tgt)
    ch = 'chat' if (it and it['channel']=='chat') else ('docs' if a['verb'] in ('edit_doc','create_doc') else 'email')
    return {'channel':ch,'verb':a['verb'],'thread':it['thread'] if it else None,'target':tgt,
            'to':a.get('to',[])+a.get('cc',[]),'text':a['content']+' '+a.get('subject',''),'t':mins(a['at']),
            'doc':tgt if (it and it['channel']=='docs' and a['verb'] in ('edit_doc','create_doc')) else None}
def ev(p,x):
    (k,v),=p.items()
    if k=='all': return all(ev(q,x) for q in v)
    if k=='any': return any(ev(q,x) for q in v)
    if k=='not': return not ev(v,x)
    if k=='channel': return x['channel']==v
    if k=='verb_in': return x['verb'] in v
    if k=='thread': return x['thread']==v
    if k=='target': return x['target']==v
    if k=='to_includes': return v in x['to']
    if k=='before': return x['t']<mins(v)
    if k=='after': return x['t']>=mins(v)
    if k=='mentions_all': return all(s.lower() in x['text'].lower() for s in v)
    if k=='mentions_any': return any(s.lower() in x['text'].lower() for s in v)
    if k=='doc': return x['doc']==v
    raise Exception(k)
acts={a['id']:a for d in e['days'] for a in d['actions']}
for n in e['needs']:
    r=n['reference'].get('action_id')
    if r: print(n['id'], 'ref', r, 'PASS' if ev(n['check'],prop_of(acts[r])) else 'FAIL')
    else: print(n['id'], 'text-only')
for t in e['traps']:
    hits=[a for a in acts if ev(t['check'],prop_of(acts[a]))]
    print(t['id'],'fires on human actions:',hits)
