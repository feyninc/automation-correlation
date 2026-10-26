import re,html,base64,urllib.parse,sys,subprocess
q=urllib.parse.quote_plus(sys.argv[1])
t=subprocess.run(["curl","-s","-m","20","-A","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36","-H","Accept-Language: en-US,en;q=0.9",f"https://www.bing.com/search?q={q}&mkt=en-US&cc=US"],capture_output=True,text=True).stdout
for m in re.finditer(r'<li class="b_algo"(.*?)</li>',t,re.S):
    b=m.group(1)
    a=re.search(r'<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)</a>',b,re.S)
    if not a: continue
    u=html.unescape(a.group(1))
    qq=urllib.parse.parse_qs(urllib.parse.urlparse(u).query).get('u',[''])[0]
    if qq.startswith('a1'):
        s=qq[2:]; s+='='*(-len(s)%4)
        try: u=base64.urlsafe_b64decode(s).decode()
        except Exception: pass
    print('-',re.sub('<[^>]+>','',html.unescape(a.group(2)))[:90],'|',u)
