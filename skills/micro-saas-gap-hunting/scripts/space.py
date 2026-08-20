import json,sys,subprocess
base,space=sys.argv[1],sys.argv[2]
u=f'{base}/wiki/rest/api/content?spaceKey={space}&limit=100&expand=title'
d=json.loads(subprocess.run(['curl','-sL','-m','40',u],capture_output=True,text=True).stdout)
print('n=',len(d.get('results',[])))
for r in d.get('results',[]): print('-',r.get('title'))
