import json,re,sys
sys.path.insert(0,'/nonexistent')
e=json.load(open(sys.argv[1]))
items={i['id']:i for i in e['items']}
acts={a['id']:a for d in e['days'] for a in d['actions']}
contacts=e['world']['contacts']
def tmin(t):
    m=re.match(r'D(\d)(?: (\d\d):(\d\d))?',t); d,h,mi=m.groups(); return int(d)*1440+(int(h)*60+int(mi) if h else 0)
def recips(a):
    txt=a['content']; hdr="\n".join(l for l in txt.splitlines()[:4] if re.match(r'(To|Cc|DocuSign envelope to)',l))
    out=set()
    for c in contacts:
        last=c['name'].split()[-1].strip('"<>')
        if last and last in hdr: out.add(c['id'])
    if 'Docketing' in hdr: out.add('c_docket')
    if 'conflicts@' in hdr or 'Alana' in hdr: out.add('c_conflicts')
    if 'Lakefront' in hdr: out.add('c_reporter')
    if 'Northline' in hdr or 'Ray Duda' in hdr: out.add('c_process')
    if a['verb']=='reply' and a['target'] in items: out.add(items[a['target']]['from'])
    return out
def ev(p,a):
    (k,v),=p.items()
    txt=a['content'].lower()
    if k=='all': return all(ev(q,a) for q in v)
    if k=='any': return any(ev(q,a) for q in v)
    if k=='not': return not ev(v,a)
    if k=='mentions_any': return any(s.lower() in txt for s in v)
    if k=='mentions_all': return all(s.lower() in txt for s in v)
    if k=='before': return tmin(a['at'])<tmin(v)
    if k=='after': return tmin(a['at'])>tmin(v)
    if k=='to_includes': return v in recips(a)
    if k=='doc': return a.get('target')==v
    if k=='target': return a.get('target')==v
    if k=='number_equals':
        val=v['value']; s=f"{val:,.2f}" if isinstance(val,float) else f"{val:,}"
        return s in a['content'] or str(val) in a['content']
    if k=='channel': return True
    if k=='verb_in': return a['verb'] in v
    if k=='thread': return items.get(a.get('target'),{}).get('thread')==v
    return None
for n in e['needs']:
    r=n['reference'].get('action_id')
    if r: print(n['id'], r, ev(n['check'],acts[r]))
print('--- traps vs all actions (should be False)')
for t in e['traps']:
    hits=[a['id'] for a in acts.values() if ev(t['check'],a)]
    print(t['id'], hits)
