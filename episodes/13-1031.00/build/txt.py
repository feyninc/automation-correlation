import re,html,sys
t=open(sys.argv[1],encoding='utf-8',errors='replace').read()
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
t=re.sub(r'<[^>]+>',' ',t); t=html.unescape(t); t=re.sub(r'\s+',' ',t)
a=sys.argv[2] if len(sys.argv)>2 else None
if a and a in t:
    i=t.index(a); print(t[i:i+int(sys.argv[3]) if len(sys.argv)>3 else i+3000])
else: print(t[:3000])
