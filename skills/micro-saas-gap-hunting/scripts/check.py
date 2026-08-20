"""Dedupe lookup: check.py "phrase" ["phrase"...] [-v] | check.py --file list.txt [-v]
Prints matching index lines only (with -v adds full ledger rows), so context cost stays constant
as the ledger grows. NEW = no match; NEAR = weak match, judge it yourself."""
import sys,os,re
d=os.path.dirname(os.path.abspath(__file__))
verbose='-v' in sys.argv
args=[a for a in sys.argv[1:] if a!='-v']
cands=[l.strip() for l in open(args[1]) if l.strip()] if args and args[0]=='--file' else args
STOP={'the','for','and','with','api','saas','app','data','tool','tools','service','platform','software','their','into','across'}
def words(s): return {w[:6] for w in re.findall(r'[a-z0-9]+',s.lower()) if len(w)>2 and w not in STOP}
idx=[l for l in open(os.path.join(d,'../references/screened-index.md')) if re.match(r'\s*\d',l)]
lines=[(l.rstrip(),words(l.split('|')[1] if '|' in l else l)) for l in idx]
ledger=None
for c in cands:
    cw=words(c)
    scored=sorted(((len(cw&lw)/max(1,min(len(cw),len(lw))),l,lw) for l,lw in lines),reverse=True,key=lambda t:t[0])
    hits=[(s,l,lw) for s,l,lw in scored if s>=0.5][:3]
    near=[(s,l,lw) for s,l,lw in scored if 0.25<=s<0.5][:2]
    print(f'== {c}')
    if not hits and not near: print('   NEW — no index match'); continue
    for s,l,_ in hits: print(f'   HIT  {s:.2f} {l}')
    for s,l,_ in near: print(f'   NEAR {s:.2f} {l}')
    if verbose and hits:
        if ledger is None: ledger=open(os.path.join(d,'../references/verdict-ledger.md')).read().splitlines()
        kw=sorted(hits[0][2] & cw, key=len, reverse=True)[:2]
        for ln in ledger:
            if ln.startswith('|') and all(k in ln.lower() for k in kw): print('   LEDGER:',ln[:500])
