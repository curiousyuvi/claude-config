---
name: micro-saas-gap-hunting
description: "Yuvraj's micro-SaaS hunt: method doc + verdict ledger live in ~/Desktop/SaaS-Idea-Finding-Research"
metadata:
  type: project
---

As of 2026-08-19 Yuvraj is hunting a solo micro-SaaS at roughly $10-15K MRR, with a stated
preference for **API-shaped products**. The agreed method: enter markets already validated by big
players, then fill gaps left by those players *and their most-used alternatives*. Competitors are
treated as proof of demand, not as a reason to drop an idea.

The full procedure, the six kill tests, and a **verdict ledger of ~26 ideas already screened**
(19 dead with the specific killer named, 8 alive) are written up in
`~/Desktop/SaaS-Idea-Finding-Research/01-METHOD-gap-hunting-for-micro-saas.md`, indexed from that
folder's README. Read the ledger before proposing any idea, to avoid re-running dead searches.

**Why:** the ledger cost a full session of research, and two ideas were wrongly declared "empty
market" because rate-limited searches returned nothing. Absence of evidence is not evidence of
absence: confirm with direct site fetches plus a GitHub-by-stars search before claiming a gap exists.

**How to apply:** when he asks for ideas, check the ledger first, apply the micro-SaaS filter
(competitors are good) rather than the venture-scale filter (needs a novel insight), and label every
"nothing found" as *not found in the sources I checked*. The Sentry-SDK-compatible hosted error tracker was the top candidate until 2026-08-19, when it was killed:
GlitchTip and Bugsink both already sell hosted flat-priced plans, and the Highlight.io displacement had closed
months earlier. Its COGS test passed, so storage was never the blocker; the blocker was that the position was
already taken. Current top candidate is an inbox-placement / deliverability testing API: it is the only idea
screened so far with zero OSS anchors AND a moat that cannot be self-hosted (a seed-mailbox network at
Gmail/Outlook/Yahoo), and GlockApps sells it as credits at $59-$129/mo. Open questions before building: seed
mailbox COGS and ToS exposure, and whether he wants a cold-outbound-adjacent customer base.

**The filter that now does the work:** 8 of 19 dead entries died to a mature OSS anchor and 4 to a small
incumbent already holding the flat-pricing slot. Every one died because the product was only software, so
`docker run` or a rival free tier beat it. So require a moat that cannot be self-hosted (licensed data, a
registered credential, or an operational estate) before running any other test.
Related: [[yuvraj-profile]].

**Working research sources (checked 2026-08-19):** Reddit JSON (403), Google, Bing, DuckDuckGo, Startpage
and public searx instances are all blocked from this machine, so keyword-volume and review-sentiment tests
cannot be run and every complaint verdict has to be labelled accordingly. What does work: the HN Algolia
full-text API (`hn.algolia.com/api/v1/search?query=`, plus `/items/<id>` for exact quote text), the GitHub
search API sorted by stars for the OSS-anchor kill test, and plain fetches of vendor pricing pages. Note
that Bash stdout gets compressed by lean-ctx, which mangles verbatim quotes: write research output to a file
and read it with the native Read tool when the exact wording matters.
