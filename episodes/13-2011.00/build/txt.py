import re,sys,html
t=open(sys.argv[1],errors='ignore').read()
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S); t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
pat=sys.argv[2] if len(sys.argv)>2 else None
if pat:
    for m in re.finditer(r'.{0,250}(?:'+pat+r').{0,250}',t,flags=re.I): print('>>',m.group(0))
else: print(t[:6000])
