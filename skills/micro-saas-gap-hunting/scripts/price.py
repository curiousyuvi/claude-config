"""price.py addonKey -> cloud live pricing"""
import sys,json,subprocess
k=sys.argv[1]
u=f'https://marketplace.atlassian.com/rest/2/addons/{k}/pricing/cloud/live'
d=json.loads(subprocess.run(['curl','-sL','-m','30',u],capture_output=True,text=True).stdout)
print(k,'| model:',d.get('pricingModel'),'| type:',d.get('pricingType'))
for it in d.get('items',[])[:8]:
    print('  ',it.get('unitCount'),'users ->',it.get('amount'),d.get('currency','USD'),'|',it.get('monthsValid'),'mo')
