"""jac.py 'JQL' [n]  -> Atlassian public issue tracker search"""
import sys,json,urllib.parse,subprocess
jql=urllib.parse.quote(sys.argv[1]); n=sys.argv[2] if len(sys.argv)>2 else '20'
u=f'https://jira.atlassian.com/rest/api/2/search?jql={jql}&maxResults={n}&fields=key,summary,votes,status,created,project'
d=json.loads(subprocess.run(['curl','-sL','-m','40',u],capture_output=True,text=True).stdout)
print('TOTAL',d.get('total'))
for i in d.get('issues',[]):
    f=i['fields']
    print(f"{f['votes']['votes']:>5} votes | {i['key']:<14} | {f['status']['name']:<12} | {f['created'][:10]} | {f['summary'][:110]}")
