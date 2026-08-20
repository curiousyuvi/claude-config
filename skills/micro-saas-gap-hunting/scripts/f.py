"""f.py URL OUT  -> fetch, strip tags, write text"""
import sys,re,html,subprocess
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'
h=subprocess.run(['curl','-sL','-m','40','-A',UA,sys.argv[1]],capture_output=True,text=True).stdout
h=re.sub(r'(?is)<(script|style|svg|noscript)[^>]*>.*?</\1>',' ',h)
t=re.sub(r'\s*\n\s*','\n',re.sub(r'[ \t]+',' ',html.unescape(re.sub(r'<[^>]+>','\n',h))))
t='\n'.join(l for l in t.split('\n') if l.strip())
open(sys.argv[2],'w').write(t); print(sys.argv[2],len(t))
