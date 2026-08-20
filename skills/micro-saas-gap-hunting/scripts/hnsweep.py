# usage: python3 hnsweep.py out.txt min_year "phrase" ["phrase"...] — batch HN phrase sweep
import calendar, json, sys, time, urllib.parse, urllib.request

out, year, phrases = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
ts = calendar.timegm((year, 1, 1, 0, 0, 0))
with open(out, "w") as f:
    for p in phrases:
        url = (f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(p)}"
               f"&hitsPerPage=25&numericFilters=created_at_i>{ts}")
        try:
            hits = json.load(urllib.request.urlopen(url))["hits"]
        except Exception as e:
            f.write(f"\n### {p} -- FAILED {e}\n")
            continue
        f.write(f"\n### {p} ({len(hits)} hits)\n")
        for h in hits:
            body = (h.get("comment_text") or h.get("title") or "").replace("\n", " ")
            f.write(f"{h.get('created_at','')[:10]} | {h.get('objectID')} | {body[:400]}\n")
        time.sleep(1)
print("wrote", out)
