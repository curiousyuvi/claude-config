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

## The moat requirement

Learned from the ledger's dead table: most deaths were a mature OSS anchor or a small incumbent
already holding the flat-pricing slot, and every one of those products was **only software**, so
`docker run` or a rival's free tier beat it. Before mining a market, name what the buyer cannot
self-host:

| Moat class | Verdict for a solo founder |
|---|---|
| Only software | Dead by default. Assume an OSS anchor exists until proven otherwise |
| Licensed data or a legal credential | Durable, but run the access test first: most are jurisdiction-bound (court e-filing, notary commissions, NMFC licences) |
| Physical estate (SIM farms, hardware) | Durable but capex-bound. Usually out of reach |
| **Digital, geography-neutral operational estate** | The reachable class. A seed-mailbox network qualifies; a notary commission does not |

If the idea has no moat beyond code, it needs a different reason to live (a live displacement event,
a licensing blocker in the incumbent) or it goes straight to the dead table.

### Correction, 2026-08-19: this gate is miscalibrated and it was causing the deaths

After 29 screenings the moat requirement had produced zero survivors. The failure mode is now legible:
requiring a non-software moat forces every candidate into one of two doomed shapes.

- **Reachable moats are already occupied.** Anything a solo founder can build by polling public pages or
  wrapping public data gets claimed within *months*, not years. Four entrants appeared in the
  API-deprecation-history niche inside a year; six Apify actors cover SaaS pricing diffs; DPAFlow and
  Sub-Processors.com had already accrued the subprocessor dataset.
- **Durable moats are gated against you.** Licensed data is quote-only and negotiated (IATA DGR), sold
  by the licensor itself (NMFTA ClassIT+ at $2,967-9,809/yr), or needs sponsors (ezyVet's partner gate
  wants named clinics vouching for you before issuing a credential).

The reachable-and-unoccupied moat set is therefore close to empty, and the filter meant to prevent
deaths became the cause of them.

**The fix: a moat is a venture-scale requirement, not a $10-15K/month requirement.** At this target the
binding constraint is distribution, not defensibility: a cloner still has to win the search term, and
200 customers is too small a prize to attract a funded attacker. The ledger contains its own proof —
subprocessor monitoring is pure software polling public pages, and DPAFlow sells it at EUR 99-999/mo to
buyers who pay.

Use the moat table as a tiebreaker between otherwise-equal candidates, never as a gate. The gate becomes:
**can I win the search term, and will the buyer pay $50+/mo?** Then run the position test.

## The funnel

### 1. Pick 5 targets
Tools with public per-unit pricing, a simple request contract, and a large user base. Prefer ones the
user would personally buy. Founder-market fit is a bonus, not a requirement.

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

1. **Access test.** Can this founder legally and physically operate it: credentials, jurisdiction,
   capex, data licences? A desk-check, costs nothing, and killed five round-4 ideas before any search.
2. **Buyer arithmetic.** Price point times customers needed, and the incumbent's marginal cost. A
   loved incumbent under $20/mo with zero COGS ends the screening.
3. **Free OSS anchor.** Search GitHub by stars *first*. A mature library kills the API business.
4. **Giant incumbent.** If AWS, Google, Azure, Stripe, or the platform owner ships it as a commodity,
   walk away.
5. **Free anchor inside the market.** A free hosted competitor caps your price at zero.
6. **Position test.** Fetch the pricing pages of the two or three smaller rivals. If one already owns
   the flat-priced, developer-first slot, the wedge is gone even when the giant is complacent.
7. **Contract test.** Can you clone the request and response shape in a weekend? If yes, stage 5 is
   free. If yes, so can everyone else, so this cuts both ways: a trivially clonable contract with no
   moat is a warning, not a win.
8. **COGS test.** Compute cost per unit against your price, in both directions: your unit cost too
   high (media, video, TTS), or the incumbent's at zero (BYOK, free tiers), which no price can get under.
9. **SEO test.** Can you rank for "X alternative"? If volume tools are unavailable, count who is
   already buying the term; five funded bidders means unwinnable regardless of volume.

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
