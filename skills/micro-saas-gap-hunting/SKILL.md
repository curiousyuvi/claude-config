---
name: micro-saas-gap-hunting
description: "Use when finding, screening, or validating a micro-SaaS or indie product idea, especially API-shaped ones. Enter markets big players already validated, then attack documented gaps in those players and their most-used alternatives. Examples: \"find me a SaaS idea\", \"is this idea any good\", \"who else is doing this\", \"X alternative opportunity\", \"should I build this\", \"validate this idea\", \"competitor gap analysis\", \"micro SaaS ideas\"."
---

# Gap hunting for micro-SaaS

Target outcome: a solo-built product at roughly $10-15K MRR. Do not invent. Enter a market big
players have already validated, then fill the gaps left by those players **and their most-used
alternatives**. The alternatives matter as much as the giants: they prove people switch and pay, and
they are far more attackable.

**Competitors are the prerequisite, not the disqualifier.**

## Before anything else

1. **Read `references/verdict-ledger.md`.** It records every idea screened, with the specific killer
   named. Never re-run a dead search or re-propose a dead idea. A *variant* of a dead idea inherits
   the verdict unless the twist defeats the named killer; check the dead table for the general shape,
   not just the exact phrasing. (The killer for "AI thumbnail generator" also killed "thumbnail
   generator with editable PSD export": the twist was the free part.)
2. **Load the founder constraint set** and hold every idea against it: solo or team, jurisdiction,
   capital, sales motion the founder will actually do, time to first ship. An idea the founder cannot
   legally or physically operate is dead at zero research cost. Constraints live in project memory,
   not in this file.
3. **Confirm the goal.** These two filters conflict and both are correct in context:
   - Venture-scale filter (YC): name the novel insight incumbents lack, or drop it.
   - Micro-SaaS filter (this skill): competitors mean people are paying, so enter.
   Applying the venture filter to a $10K/month goal kills good ideas. Ask which one applies if unclear.

   The venture filter does not arrive labelled. It sneaks in as a reasonable-sounding rule about
   defensibility: "name what the buyer cannot self-host", "what stops someone cloning this". That is how
   a moat gate got into this file and produced 29 straight kills. When a new rule asks what a competitor
   might do to you rather than whether a buyer will pay you, it is the venture filter wearing a disguise.

## Defensibility is a tiebreaker, not a gate

**The gate is: can I win the search term, and will the buyer pay $50+/mo?** Nothing else. Run the
position test immediately after.

This replaces an earlier rule that required every idea to name something the buyer could not
self-host. That rule was wrong and it is worth knowing why, because it looked sensible and it wasted a
full round of research. It was the venture-scale filter smuggled back in: "what stops a competitor
copying you" is a defensibility question, which matters when the prize is a category and does not
matter when the prize is 200 customers paying $50 a month. Nobody funded is coming for that, and a
cloner still has to win the search term you already own.

Held as a gate it also had an almost empty solution set, in two directions:

- **Reachable moats are already occupied.** Anything a solo founder can build by polling public pages
  or wrapping public data gets claimed in *months*. Four entrants appeared in the API-deprecation-history
  niche inside a year; six Apify actors cover SaaS pricing diffs; Sub-Processors.com had already accrued
  3,901 companies of subprocessor history in public.
- **Durable moats are gated against the founder.** Licensed data is quote-only and negotiated (IATA DGR),
  or sold by the licensor itself (NMFTA ClassIT+ at $2,967-9,809/yr), or needs sponsors (ezyVet's partner
  gate wants named clinics vouching for you before it issues a credential).

The ledger carries its own counterexample: subprocessor monitoring is pure software polling public web
pages, with no moat of any kind, and DPAFlow sells it at EUR 99-999/mo to buyers who pay.

The damage this rule did was in **target selection**, not screening. It steered every round toward
licensed data, regulated rails and gated integration estates, which is exactly where a solo founder
without local presence gets refused at the door, and steered away from ordinary software niches that
work fine at this revenue level. Almost none of the ledger's dead entries actually died of it; they
died at the position test, which is a real kill either way.

So keep the classes below only to break a tie between two candidates that both pass the gate:

| Moat class | Note |
|---|---|
| Only software | Fine at this scale. Distribution is the defence |
| Licensed data or a legal credential | Nice if you already have it; run the access test before valuing it, most are jurisdiction-bound or sold by the licensor |
| Physical estate (SIM farms, hardware) | Capex-bound, usually out of reach |
| Digital, geography-neutral operational estate | Genuinely useful when unoccupied, but verify it is unoccupied, this is where the last round kept guessing wrong |

## The funnel

### 1. Pick 5 targets
Tools with public per-unit pricing, a simple request contract, and a large user base. Prefer ones the
user would personally buy.

**Founder-market fit is now the primary selector, not a bonus.** See trap 9: anything a search engine
describes well is already crowded, so the edge is knowing a market from the inside, where you can judge
whether a complaint is severe without inferring it from a listicle. Prefer targets whose buyers the
founder has actually worked with, and treat a round of targets nobody in the room knows first-hand as
the low-probability path it now is.

**Buyer arithmetic is part of target selection.** Price point times customers needed is a two-minute
check that outranks any feature comparison. If the incumbent charges hobbyists under $20/mo, the goal
needs ~1,000 subscribers in a churny consumer market; if the incumbent is BYOK or otherwise carries
zero marginal cost, it cannot be undercut at all. Want business buyers and incumbent price points of
$50+/mo, where the goal is 100-300 customers.

Complaint-first mining (search pain phrases, derive targets) sounds better and does not work: generic
phrases like "priced us out" return politics, and exact phrases return too few hits to steer by.
Pick targets, then mine them.

### 2. Mine the gap
The highest-leverage stage. Search each target for:

```
"<tool> alternative"        "<tool> too expensive"     "<tool> limitations"
"<tool> pricing"            "<tool> credits"           "migrating off <tool>"
"cheaper than <tool>"
```

Sources ranked by signal quality:
1. The incumbent's own forum, changelog, and GitHub issues. Richest and least-worked seam.
2. Reddit and X. Search snippets surface Reddit threads even when its API is blocked.
3. G2 and Capterra 1-3 star reviews.
4. Comparison listicles. Low trust, but they enumerate the competitive set fast.
5. Displacement events: an acquisition, shutdown, licence change, or price rise creates a cohort
   migrating right now. Highest-value signal when present, **and the fastest to go stale**: windows
   close within months. Date-check every displacement tip against a fresh fetch of the incumbent's
   site before treating it as live. (Highlight.io was recorded as a live displacement eight months
   after the migration ended; the Canny tip was stale on arrival.)

Source availability is machine-specific and recorded in project memory. Verify which sources actually
return results before concluding anything, and name the unchecked ones in the verdict. Record
complaints **verbatim**; the exact phrasing becomes landing-page copy.

### 3. Classify the gap
Ranked by durability:

| Gap type | Durability |
|---|---|
| Licensing blocker (AGPL etc.) | High. Hard enterprise no |
| Capability wall | High, but check it does not also wall *you* out (EDI's AS2 certification killed the founder, not the incumbent) |
| Displacement event | High but time-boxed. Date-check it |
| Complexity / bad DX | Medium-high |
| Upmarket drift | Medium |
| Pricing opacity (credits) | Medium. Common, but the flat-pricing slot is often already taken by a small incumbent (see position test below) |
| Raw price alone | Low. A race to the bottom |

Pricing legibility used to be the ownable default. Ledger evidence now shows it usually taken by the
time you arrive (Unipile, GlitchTip, Skribby, or the giant itself publishing clean per-unit rates).
Treat "flat, predictable pricing" as a pairing, never the sole wedge.

### 4. Run the kill tests, in this order
Cheapest first. Each has killed a real candidate.

1. **Position test. Run this first.** Fetch the pricing pages of the two or three smaller rivals. It is
   cheap (two or three fetches) and it accounts for the large majority of the ledger's dead entries, so
   running it sixth wasted whole screenings.

   **But read the result correctly, because using it as an absolute gate is the next version of the same
   mistake.** "The slot is occupied" is a venture-scale objection: real micro-SaaS markets support many
   profitable vendors at once (COI tracking has a dozen, AI visibility has thirty, and they all bill).
   After 35 screenings, treating any occupied position as fatal produced zero survivors, which says more
   about the test than about the markets. What is actually fatal is narrower:
   - the capability is given away free by a platform owner, the regulator, or a mature OSS project, so
     price cannot go anywhere (Intercom shipping content-gap detection, Helicone shipping per-user cost
     attribution, Tremendous sending gift cards free on rebates);
   - the buyer's own engineer can build it in a day (see the contract test);
   - or the incumbent's marginal cost is zero and it is loved at under $20/mo.

   A well-funded rival at $399/mo with bad onboarding is a *competitor*, not a killer. In that case the
   question moves to whether you can win a segment and its search term, which is stage 2 and stage 6
   work, not a desk-check.
2. **Access test.** Can this founder legally and physically operate it: credentials, jurisdiction,
   capex, data licences? A desk-check, costs nothing, and killed five round-4 ideas before any search.
   Watch for the two patterns that recur: an accreditation regime (ISO 27001, notified bodies,
   OpenPeppol fees) and discretionary partner gates that want a local sponsor or referral.
3. **Buyer arithmetic.** Price point times customers needed, and the incumbent's marginal cost. A
   loved incumbent under $20/mo with zero COGS ends the screening.
4. **Free anchor inside the market.** A free hosted competitor caps your price at zero. Include the
   case where the incumbent gives the product away and monetises elsewhere (Tremendous sends gift cards
   free on brand rebates), which no price can undercut.
5. **Free OSS anchor.** Search GitHub by stars. A mature library kills the API business. Check the
   *licence* as well as the stars: a permissive peer (Apache or MIT) beside a restrictive leader closes
   any licensing-blocker wedge, which is what killed the n8n embed idea.
6. **Giant incumbent.** If AWS, Google, Azure, Stripe, the platform owner, or the regulator ships it as
   a commodity, walk away. Platform owners treat adjacent tooling as free retention (Intercom and Zendesk
   both ship AI-agent testing and help-centre importers free), and regulators ship free portals.
7. **Contract test.** Can you clone the request and response shape in a weekend? If yes, stage 5 is
   free. If yes, so can everyone else, so this cuts both ways: if the buyer's own engineer can build it
   in a day, there is no product, only a snippet.
8. **COGS test.** Compute cost per unit against your price, in both directions: your unit cost too
   high (media, video, TTS), or the incumbent's at zero (BYOK, free tiers), which no price can get under.
9. **SEO test.** Can you rank for "X alternative"? If volume tools are unavailable, count who is
   already buying the term; five funded bidders means unwinnable regardless of volume. Since owning the
   term is now the whole defence, a failure here is fatal rather than a warning.

A high score on any scorecard does not survive a failed kill test. When a test cannot be run with
available sources, the idea is **pending, not alive**: park it with the blocker named.

### 5. Build the migration path, not the product
For an API this means **be drop-in compatible with the incumbent's contract**, so migration is one
line of the customer's code. For an app, build the one-click importer. Verified precedents are in
`references/sources-and-benchmarks.md`.

### 6. Validate before building
Landing page plus direct outreach to the people found complaining in stage 2. No product yet.

The bar: **10 paying customers from outside the user's network who actually use it.** Payment alone
is not validation. For an API, watch for the second call, not the first.

An alternative stage-6 shape that beats the landing page when the buyer is a platform: one emailed
question to 30 companies who need the capability as a feature ("do you run X today, and did you
build it yourselves?"). Three "built it ourselves, wish we hadn't" answers outweigh any waitlist.

### 7. Ship in two weeks
One endpoint or one screen. No auth, no dashboard, no billing, no integrations, no logo.

## After launch
- **Distribution order:** SEO on "X alternative", then Zapier and Make listings, then YouTube
  tutorials, then Product Hunt for backlinks, then answering the threads from stage 2.
- **Pricing:** start higher than instinct. Raising prices improves customer quality.
- **Churn:** cancellation dropdowns produce nothing. Research the account, guess the reason, email one
  yes/no question.
- **Churn is often a marketing bug.** Wrong-expectation arrivals churn. Fix copy before building.

## Traps

1. **Absence of evidence is not evidence of absence.** Rate-limited or badly worded searches return
   nothing and you conclude the market is empty. Always confirm with direct fetches of named candidate
   sites plus a GitHub-by-stars search. Label every "nothing found" as *not found in the sources I
   checked*, and say which sources went unchecked.
2. **Do not invent a differentiator to rescue an idea.** If stage 2 produced no verbatim complaints,
   there is no gap. Go back to stage 1.
3. **SEO is the hidden prerequisite.** ~$11K MRR rides on ~35,000 visitors a month at reference
   conversion rates. Owning the search term is the moat, not undercutting.
4. **Document parsing and extraction are commodities.** Anything shaped like "API that extracts
   structured data from documents" competes with AWS, Google, and Azure on price.
5. **Avoid social networks and marketplaces.** Cold-start problems are not solo-founder problems.
6. **Stale displacement.** A displacement event found in a note or an old thread has usually already
   closed. Verify against the incumbent's live site, today.
7. **The variant is not a new idea.** Adding "but with X export" or "but for Y niche" to a dead idea
   only revives it if X or Y defeats the named killer. Usually X is the free part.
8. **Endless screening is a failure mode.** The ledger caps open work: one live candidate at a time,
   kill-tested to completion before the next round of targets. Nine alive entries nobody has
   finished testing is a to-do list, not a pipeline.
9. **The search-discoverable niche is saturated, so this method's core premise is decaying.** Mining an
   incumbent's complaints to find an unclaimed position assumes you are the only one mining. You are
   not: every competitor runs the same play with the same tools, and the window between "a niche is
   identifiable by search" and "four self-serve competitors exist" has compressed from years to months
   (four entrants in API-deprecation history inside a year). Two consequences. First, expect the
   position test to fail and treat that as normal rather than as evidence you picked badly. Second,
   weight targets the search engine describes *poorly*: buyers who do not post online, workflows only
   visible from inside a job, and niches whose vocabulary you know from experience rather than from a
   listicle. Founder-market fit stops being a bonus here and becomes the main way to find anything
   before the crowd does.
10. **Do not delete a dead ledger entry to make room for optimism.** Re-screening under a corrected rule
   is legitimate; erasing a kill that rested on independent evidence is not, because the next round then
   repeats the search. When a rule changes, audit each entry for whether the *changed* rule was its only
   killer, re-open just those, and say plainly how few qualified.

## Output discipline

When screening an idea, always report:
- the verbatim complaints found, with source
- which kill tests it passed and failed, including the access and arithmetic tests
- **what was not checked**, and which sources were unavailable

Then append the verdict to `references/verdict-ledger.md`: dead with the killer named, alive with the
open risks named, or pending with the blocking test named.

## References
- `references/verdict-ledger.md`: ideas already screened (dead, alive, pending). Read first, append after.
- `references/sources-and-benchmarks.md`: founder case studies with real numbers, drop-in-compatibility
  precedents, and the evidence behind the gap taxonomy.
