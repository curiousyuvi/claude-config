"""Atlassian Marketplace search: mp.py "query" [n]"""
import sys,json,urllib.parse,subprocess
q=urllib.parse.quote(sys.argv[1]); n=sys.argv[2] if len(sys.argv)>2 else '15'
u=f'https://marketplace.atlassian.com/rest/2/addons?text={q}&limit={n}&hosting=cloud'
r=subprocess.run(['curl','-sL','-m','30',u],capture_output=True,text=True).stdout
d=json.loads(r)
for a in d.get('_embedded',{}).get('addons',[]):
    e=a.get('_embedded',{})
    dist=e.get('distribution',{}) or {}
    print('*',a.get('name'),'|',a.get('key'))
    print('   vendor:',(e.get('vendor',{}) or {}).get('name'),'| installs:',dist.get('totalInstalls'),'| rating:',(dist.get('reviews') or {}).get('averageStars'))
    print('   ',(a.get('summary') or '')[:220])
