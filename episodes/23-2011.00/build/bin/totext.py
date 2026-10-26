import re,html,sys
t=open(sys.argv[1],encoding="utf-8",errors="replace").read()
t=re.sub(r'(?is)<(script|style|noscript).*?</\1>','',t)
t=re.sub(r'(?i)<br\s*/?>|</p>|</li>|</h\d>|</div>|</tr>','\n',t)
s=html.unescape(re.sub(r'<[^>]+>',' ',t))
s=re.sub(r'[ \t]+',' ',s); s=re.sub(r'\n\s*\n+','\n',s)
open(sys.argv[2],"w").write(s)
