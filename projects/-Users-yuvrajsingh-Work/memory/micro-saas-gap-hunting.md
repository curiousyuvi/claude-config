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
(18 dead with the specific killer named, 9 alive) are written up in
`~/Desktop/SaaS-Idea-Finding-Research/01-METHOD-gap-hunting-for-micro-saas.md`, indexed from that
folder's README. Read the ledger before proposing any idea, to avoid re-running dead searches.

**Why:** the ledger cost a full session of research, and two ideas were wrongly declared "empty
market" because rate-limited searches returned nothing. Absence of evidence is not evidence of
absence: confirm with direct site fetches plus a GitHub-by-stars search before claiming a gap exists.

**How to apply:** when he asks for ideas, check the ledger first, apply the micro-SaaS filter
(competitors are good) rather than the venture-scale filter (needs a novel insight), and label every
"nothing found" as *not found in the sources I checked*. Current top candidate is a
Sentry-SDK-compatible hosted error tracker, unblocked pending a COGS model and search-volume check.
Related: [[yuvraj-profile]].

**Working research sources (checked 2026-08-19):** Reddit JSON (403), Google, Bing, DuckDuckGo, Startpage
and public searx instances are all blocked from this machine, so keyword-volume and review-sentiment tests
cannot be run and every complaint verdict has to be labelled accordingly. What does work: the HN Algolia
full-text API (`hn.algolia.com/api/v1/search?query=`, plus `/items/<id>` for exact quote text), the GitHub
search API sorted by stars for the OSS-anchor kill test, and plain fetches of vendor pricing pages. Note
that Bash stdout gets compressed by lean-ctx, which mangles verbatim quotes: write research output to a file
and read it with the native Read tool when the exact wording matters.
