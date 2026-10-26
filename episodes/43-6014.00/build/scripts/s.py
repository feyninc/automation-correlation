import sys,re,html,base64,urllib.parse,urllib.request
q=" ".join(sys.argv[1:])
req=urllib.request.Request("https://www.bing.com/search?q="+urllib.parse.quote(q)+"&setlang=en-US&cc=US",headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36","Accept-Language":"en-US"})
t=urllib.request.urlopen(req,timeout=20).read().decode("utf-8","ignore")
for m in re.finditer(r'<li class="b_algo".*?<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)</a>(.*?)</li>',t,re.S):
    u=html.unescape(m.group(1))
    mm=re.search(r'[?&]u=a1([^&]+)',u)
    if mm:
        s=mm.group(1); s+="="*(-len(s)%4)
        try: u=base64.urlsafe_b64decode(s).decode()
        except Exception: pass
    snip=re.sub(r'<[^>]+>','',html.unescape(m.group(3)))
    snip=re.sub(r'\s+',' ',snip)
    print("-",u,"|",re.sub('<[^>]+>','',html.unescape(m.group(2))),"|",snip[:300])
