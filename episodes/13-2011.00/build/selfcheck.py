import json,re,sys
e=json.load(open(sys.argv[1]))
items={i['id']:i for i in e['items']}
def mins(t):
    m=re.match(r"D(\d)(?: (\d\d):(\d\d))?$",t); d,h,mi=m.groups(); return int(d)*1440+(int(h)*60+int(mi) if h else 0)
def prop_from_action(a):
    it=items.get(a.get('target'))
    return {"verb":a['verb'],"target":a.get('target'),"to":(a.get('to') or [])+(a.get('cc') or []),"text":a['content'],
            "thread":it['thread'] if it else None,"channel":(it['channel'] if it else ('chat' if a['verb']=='send' and 'Subject:' not in a['content'] else 'email')),"at":a['at']}
def ev(p,x):
    (k,v),=x.items()
    if k=='all': return all(ev(p,q) for q in v)
    if k=='any': return any(ev(p,q) for q in v)
    if k=='not': return not ev(p,v)
    if k=='channel': return p['channel']==v
    if k=='verb_in': return p['verb'] in v
    if k=='thread': return p['thread']==v
    if k=='target': return p['target']==v
    if k=='doc': return p['target']==v
    if k=='to_includes': return v in p['to']
    if k=='before': return mins(p['at'])<=mins(v)
    if k=='after': return mins(p['at'])>=mins(v)
    if k=='mentions_all': return all(s.lower() in p['text'].lower() for s in v)
    if k=='mentions_any': return any(s.lower() in p['text'].lower() for s in v)
    if k=='number_equals': return False
acts={a['id']:a for d in e['days'] for a in d['actions']}
for n in e['needs']:
    r=n['reference'].get('action_id')
    if r:
        print(n['id'], 'REF PASSES' if ev(prop_from_action(acts[r]),n['check']) else 'REF FAILS')
for t in e['traps']:
    hits=[a for a in acts if ev(prop_from_action(acts[a]),t['check'])]
    print(t['id'],'fires on human actions:',hits)
