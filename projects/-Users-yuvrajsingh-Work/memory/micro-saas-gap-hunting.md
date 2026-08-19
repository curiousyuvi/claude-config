---
name: micro-saas-gap-hunting
description: "Yuvraj's micro-SaaS hunt: method doc + verdict ledger live in ~/Desktop/SaaS-Idea-Finding-Research"
metadata: 
  node_type: memory
  type: project
  originSessionId: beae5e59-ca52-435b-9c4b-95c244dfe26e
  modified: 2026-08-19T11:54:16.299Z
---

As of 2026-08-19 Yuvraj is hunting a solo micro-SaaS at roughly $10-15K MRR, with a stated
preference for **API-shaped products**. The agreed method: enter markets already validated by big
players, then fill gaps left by those players *and their most-used alternatives*. Competitors are
treated as proof of demand, not as a reason to drop an idea.

The verdict ledger was cleared at his request on 2026-08-19; prior verdicts (22 dead, 9 alive,
9 pending) are recoverable via `git -C ~/.claude show 3e9cc16:skills/micro-saas-gap-hunting/references/verdict-ledger.md`.
The method itself, including the moat requirement, access test, and buyer-arithmetic test learned from
those screenings, now lives in the skill's SKILL.md, so clearing the ledger did not lose the lessons.

**Why:** the ledger cost a full session of research, and two ideas were wrongly declared "empty
market" because rate-limited searches returned nothing. Absence of evidence is not evidence of
absence: confirm with direct site fetches plus a GitHub-by-stars search before claiming a gap exists.

**How to apply:** when he asks for ideas, check the ledger first, apply the micro-SaaS filter
(competitors are good) rather than the venture-scale filter (needs a novel insight), and label every
"nothing found" as *not found in the sources I checked*. As of 2026-08-19 evening there is NO live
candidate: the inbox-placement / deliverability API (previous top candidate) was killed the same day —
Unspam already sells the placement API, MailerCheck sells ~$2 pay-as-you-go tests, EmailWarmup gives
unlimited free tests, and a free-tier tool with paid REST API + MCP server holds the dev-first slot; the
seed-mailbox estate is widely reproduced, not a moat. Peppol e-invoicing, EU battery DPP, and CAD
thumbnail rendering were also screened and killed that session (killers in the ledger). Two pendings
remain: the Firecrawl AGPL wedge (position test not run) and walkthrough video rendering (COGS test).
Both remaining pendings were then also killed the same day: the Firecrawl AGPL wedge (using the hosted
API or running it internally never triggers AGPL, so the blocked-buyer segment is tiny, and Crawl4AI is a
68K-star Apache-2.0 anchor) and walkthrough video rendering (Shotstack retails flat $0.20/min, Remotion is
free, app layer saturated at $18-27/mo). **The ledger now has zero alive and zero pending entries: the
pipeline is empty and the next request needs a fresh round of stage-1 targets, not more screening of old
ones.** Dominant killer across recent screens: a small incumbent already holding the flat/self-serve slot —
run the position test FIRST in future rounds, and weight licensing blockers and live displacement events
over pricing gaps.

**The filter that now does the work:** 8 of 19 dead entries died to a mature OSS anchor and 4 to a small
incumbent already holding the flat-pricing slot. Every one died because the product was only software, so
`docker run` or a rival free tier beat it. So require a moat that cannot be self-hosted (licensed data, a
registered credential, or an operational estate) before running any other test.
Related: [[yuvraj-profile]].

**Working research sources (checked 2026-08-19):** the harness WebSearch and WebFetch tools work
(server-side, unaffected by the machine-level blocks), so search-snippet complaint mining and vendor-page
fetches are fully available — use those first. Direct curl from this machine is still blocked for Reddit
JSON (403), Google, Bing, DuckDuckGo, Startpage and public searx instances, so raw keyword-volume tools and
direct G2 review scraping remain unavailable and verdicts relying on them must be labelled accordingly. What does work: the HN Algolia
full-text API (`hn.algolia.com/api/v1/search?query=`, plus `/items/<id>` for exact quote text), the GitHub
search API sorted by stars for the OSS-anchor kill test, and plain fetches of vendor pricing pages. Note
that Bash stdout gets compressed by lean-ctx, which mangles verbatim quotes: write research output to a file
and read it with the native Read tool when the exact wording matters.
