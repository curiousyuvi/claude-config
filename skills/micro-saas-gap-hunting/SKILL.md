---
name: micro-saas-gap-hunting
description: Use when finding, screening, scoring, or validating micro-SaaS or indie product ideas, when comparing an idea against competitors, or when the user asks for SaaS ideas, "is this idea any good", "who else is doing this", "should I build this", "X alternative opportunity", or a competitor gap analysis.
---

# Gap hunting for micro-SaaS

Target outcome: a solo-built product at roughly $10-15K MRR, i.e. 100-300 business customers at
$50+/mo. Do not invent. Enter a market big players have already validated, then fill the gaps left by
those players and their most-used alternatives. Competitors are the prerequisite, not the disqualifier:
they prove people switch and pay.

**What desk research can and cannot conclude.** It can kill an idea on hard evidence, and it can score
an idea high enough to design a cheap live test. It can never conclude an idea is validated. The
terminal output is always a designed cheap test (outreach emails, a landing page with traffic, five Mom
Test conversations), never a build decision. Rob Walling's framing governs: each check is a data point,
not a deal breaker — except the three hard gates, which cap the score near zero.

## Before anything else

1. **Dedupe by lookup, never by reading.** Run `python3 scripts/check.py "idea" ["idea"...]` (or
   `--file list.txt` for a batch; `-v` adds the ledger evidence rows for hits). It prints only
   matches, so the cost per round is constant no matter how large the ledger grows. Never read
   screened-index.md or verdict-ledger.md in full during a round — the only whole-file reads are the
   occasional anti-portfolio review and filter audits. A variant inherits a hit's score unless the
   twist defeats the named killer.
2. **Founder constraints** from project memory: solo, jurisdiction, capital, sales motion, time to
   first ship, no SOC 2 / ISO 27001.
   **Excluded domain, contractual, non-negotiable: customer support.** Helpdesks and ticketing, help
   centres and support KBs, support AI agents, conversation QA, support analytics, anything sold as an
   app or add-on to Zendesk / Intercom / Freshdesk / Help Scout / Gorgias / Front. The line is the
   **buyer**, and it is customer support only: developer/API documentation tooling sold to DevRel,
   docs and product teams is IN SCOPE (confirmed 2026-08-20). Permitted axes: developer/API docs,
   edge/CDN and multi-tenant web infrastructure, document and video generation, LLM application
   engineering, India-side operations.
3. **Tooling check.** Read `references/tooling.md` (small, current-state-only — overwrite it in
   place when availability changes). Try WebSearch/WebFetch via ToolSearch; the fallback seams live
   in `scripts/`. Name unchecked sources in every verdict.
4. **Micro-SaaS filter, not venture filter.** Competitors mean people pay. Any rule asking what a
   competitor might do to you rather than whether a buyer will pay you is the venture filter in
   disguise. Defensibility is a tiebreaker, never a gate.

## The score: every candidate gets 1-100

One number per candidate, recorded in the ledger with the evidence that produced it. The composite:

| Dimension | Weight | 100% of weight | 0% of weight |
|---|---|---|---|
| Demand evidence | 25 | Tier 1-2 on the Mom Test hierarchy, dated, current | Only tier 5-6, or pricing-page inference |
| Position | 20 | Expensive/sales-led vendors leaving a self-serve slot | Loved cheap self-serve incumbent in the exact slot |
| Founder fit | 15 | Buyer/domain known from the inside | Learned from a listicle this week |
| Distribution | 15 | Winnable channel: marketplace category, unfarmed long tail, owned audience | Head terms owned by content machines AND no marketplace/audience |
| Buyer arithmetic | 15 | 100-300 buyers at $50+ plausible | Needs 1,000+ churny consumers |
| Contract test | 10 | Weeks of integration/domain work | Buyer's engineer builds it in a day |

Score each dimension 0-100% of its weight, sum. Then apply caps, in order:

- **Gate cap = 5.** Any hard gate fired with specific evidence: (1) given away, shipped and adequate,
  by a platform owner / regulator / mature permissive-licence OSS (check current + previous year
  releases by name; check GitHub stars AND licence); (2) COGS structurally above price in either
  direction (your unit cost exceeds market price, or incumbent's marginal cost is zero); (3) access —
  founder cannot legally or physically operate it (licences, credentials, capex, float, compliance
  evidence sold unaudited, or the excluded support domain).
- **Unverified cap = 69.** No candidate scores 70+ until the verification pass (below) has run and
  failed to kill it. First-pass survivors flipped to dead 4 of 4 times before this was structural.
- **Evidence-staleness discount.** Any load-bearing complaint or displacement event not re-based
  against the incumbent's current docs drops that dimension by half.

Bands: **0-15 dead** (gate fired — never revisit without defeating the named killer), **16-39 weak**
(scored and shelved; do not iterate), **40-69 promising-unverified** (queue for verification),
**70+ verified — design the cheap test now; one 70+ candidate ends the round.**

Old-ledger mapping: KILL ≤ 15, WEAK = 16-39, WORTH A CHEAP TEST = 70+.

## Round checklist

Copy into the response and check off as the round progresses:

```
Round progress:
- [ ] Batch deduped via scripts/check.py (no whole-file index/ledger reads)
- [ ] Founder constraints + support exclusion applied
- [ ] tooling.md read; WebSearch/WebFetch probed; check.py sanity-checked ("outbound
      webhook delivery" must HIT)
- [ ] Tier 0: whole batch triaged, <30 dropped and index-lined
- [ ] Tier 1: survivors probed in parallel, <40 dropped
- [ ] Tier 2: full screen on top scorers, evidence verbatim+dated
- [ ] Tier 3: verification (refutation framing) on any candidate near 70
- [ ] Index + ledger appended (cat >>) for every candidate; unchecked sources named;
      tooling.md overwritten if availability changed
- [ ] If 70+: cheap test designed (cost + threshold) and the round ENDED
```

## Throughput: the tiered pipeline

Built to score hundreds of candidates. Spend is proportional to score: cheap checks first, expensive
checks only on what survives them. Never run a tier's checks on a candidate a lower tier already
capped.

**Tier 0 — triage, no network, ~1 minute each.** Ledger dedupe, exclusion check, buyer arithmetic
(price × customers), COGS sanity, known trap patterns (document parsing is a commodity; marketplaces
you'd bootstrap; media/video per-minute COGS; one-time migration demand). Assign a provisional score
from priors. **Drop < 30 provisional; they go to the ledger as one line each.** A whole batch of 50
ideas is a single table pass.

**Tier 1 — position probe, 2-5 fetches, ~5-10 minutes each.** One marketplace/API query for install
counts and live pricing, one web search, one incumbent pricing-page fetch. This is where most deaths
happen (position taken, free anchor, giant). Update the score; drop < 40. Run candidates in parallel
batches — the probes are independent. Budget searches: Brave captchas after ~8 queries/session, so
spend searches on discovery and direct fetches on verification.

**Tier 2 — full screen, ~30-45 minutes each, top scorers only.** Complaint mining with verbatim
quotes, source and date; Mom Test grading; OSS anchor by stars and licence; platform-owner releases
current + previous year; full scorecard. Output: a 40-69 score or a kill.

**Tier 3 — verification, mandatory before any 70+.** Refutation framing: try to kill it and fail.
(1) Sales-gated competitors' real capability from their product docs, changelogs, marketplace
listings — not pricing pages. (2) Platform-owner releases, current year, by name. (3) Re-base every
dated complaint against the incumbent's current docs or drop it. Passing verification lifts the
69 cap.

**Seams (`scripts/`, python3+curl, ~20 lines each — fix in place when a site changes):**
```
python3 scripts/check.py "idea"... [-v]        # ledger dedupe lookup (constant cost)
python3 scripts/bs.py "query" [n]              # Brave search (captchas ~8/session)
python3 scripts/f.py URL out.txt               # any URL -> stripped text
python3 scripts/jac.py 'JQL' [n]               # jira.atlassian.com requests + votes
python3 scripts/mp.py "query" [n]              # Atlassian Marketplace apps + installs
python3 scripts/price.py addonKey              # Marketplace live cloud pricing
python3 scripts/cql.py BASE 'CQL' [n]          # public Confluence wiki search
python3 scripts/space.py BASE KEY              # wiki space page list
python3 scripts/page.py BASE KEY "Title" out   # wiki page body (defeats JS sites)
```
Also working: HN Algolia (`hn.algolia.com/api/v1/search?query=`), GitHub search API by stars+licence,
direct vendor fetches. Write research output to files and read with native Read when exact wording
matters (shell output can be compressed).

## Stage 1: pick targets

**Founder-market fit and proprietary access are the primary selectors.** Public complaint mining is
the most arbitraged sourcing channel in existence; the edge is knowing a market from the inside.
Weight targets the search engine describes poorly. Buyer arithmetic is part of selection: $50+/mo
business buyers, or skip. **Proven-shape transplant is a legitimate second selector**: take the shape
of a candidate that survived gates (e.g. compliance fan-out across a fragmented suite, marketplace
distribution, flat price) and run it on another platform — but score founder fit honestly there.
Complaint-first mining (search pain phrases, derive targets) does not work.

With the tiered pipeline, a round can open with 20-100 raw candidates instead of 3-5, because tier 0
costs a minute each. Generate wide at tier 0, narrow hard at tier 1.

## Stage 2: evidence and grading

Search per target: `"<tool> alternative"`, `"<tool> too expensive"`, `"<tool> limitations"`,
`"<tool> pricing"`, `"migrating off <tool>"`, `"cheaper than <tool>"`.

Sources by signal: (1) incumbent's own forum/changelog/GitHub issues and public trackers with vote
counts; (2) Reddit/X via snippets; (3) G2/Capterra 1-3 star; (4) listicles (low trust, fast set
enumeration); (5) displacement events — date-check before use. Record complaints **verbatim with
source and date**.

**Mom Test hierarchy** (strongest first): 1 money already spent; 2 commitment/migration language;
3 specific past-tense pain from a named non-vendor, dated; 4 feature requests and upvotes; 5
complaint volume/compliments; 6 vendor-authored content — **inverted signal**. Two costly lessons:
pricing-page inference ("nobody sells this self-serve, so small teams are shut out") is not demand
evidence; complaints go stale — verify against current docs.

## Ledger discipline

Record every scored candidate in BOTH files, by shell append (`cat >>`) — appending never requires
reading either file, which is what keeps run cost flat as they grow:

- `references/screened-index.md`: one line, `score | idea | killer keyword` — this is what check.py
  matches against, so make the idea phrasing literal and keyword-rich.
- `references/verdict-ledger.md`: tier-0 drops get one table line; 40+ candidates get the full
  evidence paragraph.

Never delete a dead entry; re-scoring under a corrected rule re-opens only entries whose sole killer
was the changed rule. If tooling availability changed, overwrite `references/tooling.md`.

**Base-rate check.** A rigorous screen should still put ~10-30% of a batch above 40. A 10+ batch with
nothing above 40 flags the filter, not the ideas — audit which rule did the killing. **Anti-portfolio:**
every 6-12 months, revisit kills for false negatives; before any kill, one paragraph on "why WILL this
work".

## Validation (the cheap test) and after

70+ ends the round: name the test, its cost, its threshold (e.g. "20 outreach emails to non-network
buyers; 3 replies saying 'we built this ourselves' or 'what would it cost' passes"). The real bar: 10
paying customers outside the founder's network who actually use it. Ship in two weeks: one endpoint or
one screen; drop-in compatible for APIs, one-click importer for apps. Distribution: the winnable
channel from the scorecard first. Price higher than instinct. Churn is often a marketing bug.

## Traps

1. Absence of evidence is not evidence of absence — label every "nothing found" as *not found in the
   sources I checked*; confirm with direct fetches plus GitHub-by-stars.
2. Do not invent a differentiator to rescue an idea.
3. A variant revives a dead idea only if the twist defeats the named killer.
4. Document parsing/extraction is a commodity.
5. Avoid social networks and marketplaces you'd have to bootstrap (selling INTO one is fine).
6. Never delete dead ledger entries to make room for optimism.
7. Skill drift: correct rules in place, move history to the ledger, keep this file under 250 lines.
8. **Guessed buyer access is still search-derived sourcing.** Round 2026-08-20c proved it: four
   plausible-buyer targets, zero dated non-vendor complaints. Buyer-access targets must come from the
   founder naming real reachable operators.

## References
- `references/verdict-ledger.md`: every idea screened (read first, append after), source availability,
  method history.
- `references/sources-and-benchmarks.md`: founder case studies, drop-in-compatibility precedents.
- `scripts/`: the working research seams (see Throughput).
