import json,sys,re,html,urllib.parse,subprocess
base,space,title,out=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
u=f'{base}/wiki/rest/api/content?spaceKey={space}&title={urllib.parse.quote(title)}&expand=body.storage'
d=json.loads(subprocess.run(['curl','-sL','-m','40',u],capture_output=True,text=True).stdout)
r=d.get('results',[])
if not r: print('not found'); sys.exit()
b=r[0]['body']['storage']['value']
t=re.sub(r'\n{2,}','\n',html.unescape(re.sub(r'<[^>]+>','\n',b)))
open(out,'w').write(t); print(out,len(t))
