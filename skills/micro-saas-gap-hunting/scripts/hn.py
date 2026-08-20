# usage: python3 hn.py "query" [n] — HN Algolia search, prints date | points | title/comment
import json, sys, urllib.parse, urllib.request
q = urllib.parse.quote(sys.argv[1])
n = sys.argv[2] if len(sys.argv) > 2 else "10"
url = f"https://hn.algolia.com/api/v1/search?query={q}&hitsPerPage={n}"
d = json.load(urllib.request.urlopen(url))
for h in d["hits"]:
    t = h.get("title") or (h.get("comment_text") or "")
    print(h.get("created_at", "")[:10], "|", h.get("points"), "|", t.replace("\n", " ")[:240])
