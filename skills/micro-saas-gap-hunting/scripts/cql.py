import json,sys,urllib.parse,subprocess
base=sys.argv[1]; cql=urllib.parse.quote(sys.argv[2]); lim=sys.argv[3] if len(sys.argv)>3 else '25'
u=f'{base}/wiki/rest/api/search?cql={cql}&limit={lim}'
d=json.loads(subprocess.run(['curl','-sL','-m','40',u],capture_output=True,text=True).stdout)
print('SIZE',d.get('totalSize'))
for r in d.get('results',[]):
    c=r.get('content',{})
    print('-',c.get('title'),'|',r.get('url'))
