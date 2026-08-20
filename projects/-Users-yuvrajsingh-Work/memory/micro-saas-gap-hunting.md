---
name: micro-saas-gap-hunting
description: "Yuvraj's micro-SaaS hunt: method doc + verdict ledger live in ~/Desktop/SaaS-Idea-Finding-Research"
metadata: 
  node_type: memory
  type: project
  originSessionId: beae5e59-ca52-435b-9c4b-95c244dfe26e
  modified: 2026-08-19T15:14:32.796Z
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
**FIRST LIVE CANDIDATE (2026-08-19, after 35 screenings): content-gap detection and article drafting for
the non-Intercom/Zendesk helpdesk tail (Freshdesk, Help Scout, Gorgias, Front).** It survives because of the
corrected reading of kill test 1: occupied by small competitors (My AskAI $199/mo, eesel $0.40/ticket, both
selling a ticket-answering agent with gap analysis as a side feature) rather than given away by a platform
owner. Freshdesk's Freddy has no gap detection and only trains on past tickets on the Business plan; Help
Scout's AI Answers has no gap reporting. Intercom and Zendesk DO ship it natively, which is both why the
general case is dead and the main risk to this one. Validation runbook with the exact outreach email and the
disqualifying answers: `~/Desktop/SaaS-Idea-Finding-Research/02-VALIDATION-content-gap-for-helpdesk-tail.md`.
**Next step is 20 emails to support leads outside his network, not code.** Ground-only 49 CFR dangerous goods
was closed as dead the same day (ShipWave add-on at $19/mo plus ShipHazmat self-serve, and misclassification
liability), so the ledger now has one alive and zero pending.

**Round 2026-08-19e, the first run under the corrected gate: five more screened, five dead, 35 total, still
zero alive.** Targets picked by founder-market fit as the corrected method demands (help-centre content-gap
detection, answer-engine citation tracking for docs, per-customer AI cost attribution), plus both pendings
resolved to dead (COI endorsement verification lost both blocking tests: Billy and COISoftware already sell
endorsement-to-contract matching, and mid-term cancellation needs agency-management-system feeds that
Certificial holds across 25,000 agencies; ground-only 49 CFR dangerous goods stays open). Four of the five
died to a platform owner or free tier giving the capability away, which is a legitimate killer.

**Conclusion to act on: removing the moat gate was necessary but not sufficient, and screening
search-found ideas cannot produce a candidate at all.** The same search yields the same shortlist for
everyone, and platform owners reach every adjacent feature first (Intercom ships content-gap detection with
drafted articles inside Fin; Helicone ships per-user cost attribution in one line; Google Search Console and
Cloudflare both shipped free AI-citation reporting in 2026). **Do not run another round of five targets.**
The recommendation made to Yuvraj on 2026-08-19: stop screening and switch to buyer conversations in one
occupied market he knows, accepting competitors, since micro-SaaS markets support many profitable vendors
(a dozen in COI tracking, thirty in AI visibility). SKILL.md kill test 1 now carries the corrected reading
of an occupied position: fatal only when the thing is free from a platform owner, regulator or mature OSS,
or buildable by the buyer's engineer in a day, or the incumbent is loved at under $20/mo with zero marginal
cost.

**Round 2026-08-19d (parallel screening, 8 agents): 29 total ideas screened, ZERO alive.** Screened and
killed: support/KB domain (AI-agent QA in all modalities — Intercom and Zendesk ship testing natively —
plus KB migration/sync and docs-as-code publishing), licensing blockers (n8n embed, Metabase, Documenso),
regulatory deadlines (EU AI Act, CRA/SBOM, PCI 6.4.3, EUDR), accruing datasets (SaaS pricing history, API
deprecation history, GDPR subprocessor history), a nine-event displacement sweep, India regulated rails,
age assurance, rewards fulfilment, vet/dental unified APIs, hazmat DG, NMFC. Killers are in the ledger.

**The load-bearing conclusion: the moat requirement was the venture filter in disguise, and it has been
removed as a gate in SKILL.md (demoted to a tiebreaker; the gate is now search-term winnability plus a
$50+/mo buyer). Position test is now kill test 1. Two new traps: the search-discoverable niche is
saturated so expect the position test to fail and select targets by founder-market fit, and never delete
a dead ledger entry to make room for optimism.** A full audit of the dead table found that **only one
entry** (ground-only 49 CFR dangerous goods) had the moat rule as its sole killer, so only that one was
re-opened; the rest died at position, access, free anchors, giants or COGS, independently. The bad rule's
real cost was distorting target *selection* toward licensed data and gated estates, not producing false
kills. Reachable moats get occupied within months (four entrants in the API-deprecation niche inside a
year); durable moats are gated (IATA DGR quote-only, NMFTA sells its own API, ezyVet demands named
sponsoring clinics). A moat is a venture-scale requirement, not a $10-15K/mo one — at 200 customers the
binding constraint is distribution, and the ledger's own proof is DPAFlow selling pure public-page polling
at EUR 99-999/mo. The gate is now "can I win the search term and will the buyer pay $50+/mo", with the moat
table demoted to a tiebreaker.

Also worth Yuvraj's attention professionally, not as a solo product: Salesforce is acquiring Fin/Intercom
($3.6B, announced 2026-06-15, ~30,000 customers, closes early calendar 2027), which puts Helply/Groove
squarely in the migration-target profile for SMB support teams fearing Agentforce absorption.

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

**Round 2026-08-20 (parallel, 6 agents, 15 ideas): 14 dead, 5 unverified candidates, still ZERO confirmed
live.** The methodological finding outranks any idea: **a verification pass flipped the first two survivors
from ALIVE to DEAD, 2 for 2**, both times on evidence the first pass could not reach — a sales-gated
competitor whose capability hides in its marketing detail (Pageloop sells exactly the docs-screenshot-drift
wedge, text-level, on help centres it did not author), and a 2026 platform-owner release (Intercom Fin
Operator; Zendesk's 2026-05-18 resolution tiers, which LLM-verify silent conversations and made the
AI-billing-reconciliation idea moot). **So: run first passes cheap and in parallel, then verify every
survivor against those two patterns specifically. A first-pass ALIVE means "not yet killed".**

Five candidates ended the session unverified because all three verification agents died on an account
spend-limit error: E1 DSAR/erasure execution across support tooling (strongest), E2 PII redaction with the
attachments wedge, B1 Zendesk macro hygiene, B3 conversation QA for 3-20 agent teams, F1 cross-client SLA
reporting for support agencies. Details and the single deciding test for each are in the ledger.

Hand-verification of E1/E2 that did complete: **GrowthDot now sells "The Complete GDPR Compliance Platform
for Zendesk" at a flat $50/$65 per subdomain per month with a self-serve trial, and its Premium tier
includes "Redact Attachments by Type"** — which occupies E2's claimed primary wedge. Also **sparkly.app is
a parked domain for sale**, so the "Sparkly $99/mo, 100+ installs" existence proof underpinning E1 is
UNCONFIRMED and needs checking before it is relied on.

Two tooling facts worth keeping: agents must load WebSearch/WebFetch schemas via ToolSearch before use (two
agents wrongly concluded they were unavailable and produced rounds with no SERP evidence at all), and the
richest seams this round were the Zendesk Gather community API, the Zendesk Help Center article-search API,
the Atlassian Marketplace REST API and HN Algolia. Still blocked: Reddit JSON, all search engines by curl,
G2/Capterra bodies, keyword volumes, zendesk.com/marketplace (403) and growthdot's help-center API (401).

**2026-08-20 later: E1 CONFIRMED ALIVE — the first survivor in 50 screenings — and SKILL.md rewritten.**
E1 = one DSAR/erasure request fanned out across Zendesk Support + Chat + Talk + Guide + community + AI
agents with an audit trail. Verification hunted both session killers and neither fired: Sparkly is real
($99/$249 flat, 100+ installs) but delete-only and Support-only; GrowthDot ($50/$65) also never leaves
Support; Zendesk's own current docs document the fragmentation. Next step is NOT more screening: half a
day in Zendesk developer docs checking whether a ZAF in-Zendesk app can reach Chat visitor profiles,
Guide revisions, Talk recordings and the AI agents API without an external server (losing "no data
leaves Zendesk" loses the only answer to having no SOC 2), then 20 outreach emails.

The skill was audited (Yuvraj suspected it was flawed/too strict) and rewritten from scratch, commit
9e7c99f in ~/.claude. Diagnosis: kills were individually sound, but the kill-test chain compressed the
whole funnel into its cheapest stage (0/50 pass rate vs the ~10-30% a desk stage should pass), the
verification pass wasn't structural (4/4 first-pass survivors flipped), demand evidence had no quality
rubric (three candidates died carrying only pricing-page inference), and three layers of accumulated
rule-corrections biased every reading toward KILL. New shape: 3 hard gates + 6-dimension scorecard,
verdicts KILL / WEAK / WORTH A CHEAP TEST (desk research can never emit "validated"), mandatory
refutation-framed verification (competitor product docs not pricing pages; current-year platform
releases), Mom Test evidence hierarchy with vendor content as inverted signal, distribution scored as a
whole (SEO failure alone not fatal — Sparkly built 100+ installs purely on the marketplace category),
one survivor ends the round, zero-survivor batches flag the filter, 6-12 month anti-portfolio review of
kills. The Desktop copy 01-METHOD-gap-hunting-for-micro-saas.md still reflects the OLD method.

**HARD CONSTRAINT added 2026-08-20: the customer-support domain is contractually off limits.** Yuvraj's
employment contract does not allow him to work on support tooling, so helpdesks, ticketing, help centres
and knowledge bases, support AI agents, conversation QA, support analytics, and anything sold as an app or
add-on to Zendesk / Intercom / Freshdesk / Help Scout / Gorgias / Front must never be screened again.

**Why:** it is a legal bar, not a preference, and it is invisible from the code and the ledger. It also
invalidates the pipeline: E1 (Zendesk DSAR fan-out), the only candidate to survive verification in 50+
screenings, cannot be built, and neither can the helpdesk-tail content-gap candidate. About 30 dead ledger
entries are support-domain and are now history only.

He confirmed on 2026-08-20 that the bar is **"only customer support"** — the test is who the buyer is,
so developer and API documentation tooling sold to DevRel, docs and product teams is in scope. Do not
over-read the exclusion into adjacent markets.

**How to apply:** select targets from his other axes only — edge/CDN and multi-tenant web infrastructure
(he built kb-edge on Cloudflare Workers), document and video generation (Kroto, InstantDocs, Remotion),
LLM application engineering, India-side operations. Support is where his domain knowledge is deepest, so
it is the standing temptation of every round; the thinner evidence elsewhere is the price of the
constraint. The exclusion is written into SKILL.md ("Before anything else" item 2 and hard gate 3) and at
the top of the verdict ledger.

**Round 2026-08-20c: four screened, four dead. Nine consecutive kills since the support exclusion.**
Targets were picked by guessed buyer type rather than dev-infra (GeM tender bid assembly for Indian MSMEs;
investor-update/portfolio-MIS reporting; Indian-language dubbing for edtech video; digital work
instructions for manufacturing SMEs). Killers in the ledger. **The finding: guessing the buyer-access axis
does not work — none of the four produced one dated complaint from a named non-vendor.** Do not run another
desk round until Yuvraj answers one question: *whose business operations can he get on a call this week?*
Named people or a specific trade, not a market category.

**Tooling, checked 2026-08-20c:** WebSearch and WebFetch could NOT be loaded for the second session running
(six ToolSearch patterns, no deferred tool retrievable at all). Recovered seam that replaces them:
**Brave Search HTML via curl works** — `https://search.brave.com/search?q=` with a desktop UA, results in
`<div class="result-wrapper`. Parsers live in the session scratchpad (`bs.py` search, `f.py` page-to-text);
rewrite them when needed, they are ~20 lines each. Bing returns 200 with no extractable organic links,
Mojeek now captchas, ecosia/r.jina.ai 403, DuckDuckGo html serves a challenge.
