"""brave search via curl; usage: bs.py "query" [n]"""
import sys,re,html,urllib.parse,subprocess
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'
def txt(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s))).strip()
q=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 12
u='https://search.brave.com/search?q='+urllib.parse.quote(q)
h=subprocess.run(['curl','-sL','-m','30','-A',UA,u],capture_output=True,text=True).stdout
blocks=re.split(r'<div class="result-wrapper',h)[1:]
print('QUERY:',q,'|',len(blocks),'results')
for b in blocks[:n]:
    m=re.search(r'href="(https?://[^"]+)"',b)
    t=re.search(r'class="title[^"]*"[^>]*>(.*?)</',b) or re.search(r'<div class="[^"]*title[^"]*"[^>]*>(.*?)</div>',b)
    s=re.search(r'class="snippet-description[^"]*"[^>]*>(.*?)</div>',b,re.S) or re.search(r'class="snippet [^"]*"[^>]*>(.*?)</div>',b,re.S)
    print('-',(txt(t.group(1))[:120] if t else '?'),'|',m.group(1)[:110] if m else '?')
    if s: print('   ',txt(s.group(1))[:400])
