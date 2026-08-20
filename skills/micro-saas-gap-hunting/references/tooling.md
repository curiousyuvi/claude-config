# Source availability on this machine — CURRENT STATE ONLY

Overwrite this file in place when availability changes; never append history here (history goes in
the ledger's round notes). Keeping it small and current is what keeps the per-round read cost flat.

Last verified: 2026-08-20.

Working:
- scripts/ seams: bs.py (Brave HTML search, captchas after ~8 queries/session — spend on discovery,
  verify by direct fetch), f.py, jac.py, mp.py, price.py, cql.py, space.py, page.py
- HN Algolia `hn.algolia.com/api/v1/search?query=` (and `/items/<id>` for exact text)
- GitHub search API by stars + licence
- Direct vendor page fetches (curl, desktop UA)
- Any public Confluence Cloud wiki REST API; jira.atlassian.com public tracker with votes
- Zendesk Gather community API and Help Center article-search API (support domain — excluded)

Machine-dependent, probe each session before relying on either answer:
- Harness WebSearch / WebFetch (worked 2026-08-20; load via ToolSearch exact-name query
  "select:WebSearch,WebFetch" — regex-pattern queries return nothing and had caused false
  "unloadable" reports)

Blocked (do not burn time re-probing unless a round needs them):
- Reddit JSON (403), Google/DuckDuckGo/Startpage/searx direct, Bing (200 but JS-gated, no organic
  links), Mojeek (captcha), Ecosia (403), r.jina.ai (403), G2/Capterra review bodies, keyword-volume
  tools, zendesk.com/marketplace (403)
