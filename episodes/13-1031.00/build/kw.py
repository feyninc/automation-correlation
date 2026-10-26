import re,html,sys
t=open(sys.argv[1],encoding='utf-8',errors='replace').read()
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S);t=re.sub(r'<[^>]+>',' ',t);t=re.sub(r'\s+',' ',html.unescape(t))
n=int(sys.argv[2]); 
for k in sys.argv[3:]:
  for m in list(re.finditer(k,t,flags=re.I))[:n]:
    print('['+k+']',t[max(0,m.start()-200):m.start()+500]);print()
