---
name: micro-saas-gap-hunting
description: "Use when finding, screening, or validating a micro-SaaS or indie product idea, especially API-shaped ones. Enter markets big players already validated, then attack documented gaps in those players and their most-used alternatives. Examples: \"find me a SaaS idea\", \"is this idea any good\", \"who else is doing this\", \"X alternative opportunity\", \"should I build this\", \"validate this idea\", \"competitor gap analysis\", \"micro SaaS ideas\"."
---

# Gap hunting for micro-SaaS

Target outcome: a solo-built product at roughly $10-15K MRR, i.e. 100-300 business customers at
$50+/mo. Do not invent. Enter a market big players have already validated, then fill the gaps left by
those players and their most-used alternatives. Competitors are the prerequisite, not the disqualifier:
they prove people switch and pay.

**What desk research can and cannot conclude.** It can kill an idea on hard evidence, and it can
promote an idea to WORTH A CHEAP TEST. It can never conclude an idea is validated. The terminal output
of this skill is always a designed cheap live test (outreach emails, a landing page with traffic, five
Mom Test conversations), never a build decision. Rob Walling's framing governs the whole method: each
check below is "another data point to gather when evaluating the idea", not an absolute deal breaker.
Only three checks are hard gates; everything else scores.

## Before anything else

1. **Read `references/verdict-ledger.md`.** Every idea ever screened, with the specific killer named.
   Never re-run a dead search. A variant of a dead idea inherits the verdict unless the twist defeats
   the named killer — check the dead table for the general shape, not the exact phrasing.
2. **Load the founder constraints** from project memory: solo, jurisdiction, capital, sales motion,
   time to first ship, no SOC 2 / ISO 27001. An idea the founder cannot legally or physically operate
   is dead at zero research cost.
3. **Tooling check.** Load WebSearch and WebFetch schemas via ToolSearch before concluding anything —
   agents have twice wrongly decided they were unavailable and produced rounds with no search evidence.
   Machine-specific source availability (what is blocked, what works) is recorded at the bottom of the
   ledger; verify against it and name unchecked sources in every verdict.
4. **Confirm the goal.** Micro-SaaS filter: competitors mean people pay, so enter. Venture filter:
   name the novel insight or drop it. Applying the venture filter to a $10-15K/mo goal kills good
   ideas. It rarely arrives labelled — it sneaks in as a defensibility rule ("what stops a cloner",
   "name the moat"). When a rule asks what a competitor might do to you rather than whether a buyer
   will pay you, it is the venture filter in disguise. Defensibility is a tiebreaker between two
   candidates, never a gate; at this scale distribution is the defence.

## Stage 1: pick targets

**Founder-market fit and proprietary access are the primary selectors.** Public complaint mining is
the most arbitraged sourcing channel in existence: every competitor runs the same searches with the
same tools, and the window between "niche identifiable by search" and "four self-serve competitors
exist" is now months. The edge is knowing a market from the inside — the day job, communities the
founder is embedded in, workflows only visible from within — where complaint severity can be judged
directly instead of inferred from a listicle. Weight targets the search engine describes poorly.

**Buyer arithmetic is part of target selection.** Price point times customers needed is a two-minute
check that outranks any feature comparison. Want business buyers and incumbent price points of
$50+/mo. An incumbent loved at under $20/mo in a churny consumer market means ~1,000 subscribers to
goal; skip.

Pick 3-5 targets per round, no more. Complaint-first mining (search pain phrases, derive targets)
does not work: generic phrases return noise, exact phrases return too few hits to steer by. Pick
targets, then mine them.

## Stage 2: mine the gap and grade the evidence

Search each target for:

```
"<tool> alternative"        "<tool> too expensive"     "<tool> limitations"
"<tool> pricing"            "<tool> credits"           "migrating off <tool>"
"cheaper than <tool>"
```

Sources by signal quality: (1) the incumbent's own forum, changelog, and GitHub issues — richest and
least-worked seam; (2) Reddit and X via search snippets; (3) G2/Capterra 1-3 star reviews; (4)
comparison listicles — low trust, but they enumerate the competitive set fast; (5) displacement
events (acquisition, shutdown, licence change, price rise) — highest value when present and fastest
to go stale; date-check against a fresh fetch of the incumbent's site before treating as live.

Record complaints **verbatim with source and date** — the exact phrasing becomes landing-page copy.

**Grade every piece of demand evidence on the Mom Test hierarchy.** From strongest to worthless:

1. Money already spent on this problem (a paid tool, a consultant, an internal build)
2. Commitment or migration language ("we switched", "we built it ourselves, wish we hadn't", a named budget)
3. Specific past-tense pain from a named non-vendor, dated ("we had to delete the whole ticket")
4. Feature requests and upvotes
5. Complaint volume, compliments, survey yeses
6. Vendor-authored content (blogs, templates, lead magnets) — **inverted signal**: wide circulation
   of vendor "pain" content is evidence of content marketing, not unmet demand

Two rules learned at cost: **inferring an unserved buyer from vendor pricing pages ("nobody sells
this self-serve, so small teams must be shut out") is not demand evidence** — three candidates died
carrying only that inference. And **complaints go stale like displacement events do**: verify every
load-bearing complaint against the incumbent's current docs before relying on it; a 2020 limitation
the vendor has since fixed is a kill for that evidence, though the gap may survive on current
documentation (which is stronger evidence than old forum threads anyway).

## Stage 3: the three hard gates

Only these produce an immediate KILL. Each needs specific evidence, not vibes.

1. **Given away, adequately, by a platform owner / regulator / mature permissive-licence OSS.**
   "Shipped and adequate" — a roadmap item or a half-feature scores as risk in stage 4 instead.
   Check the platform owner's releases from the CURRENT and PREVIOUS year by name: this killed 6 of
   the last 8 dead candidates (Intercom Fin Operator, Intercom Monitors at $99 flat, Zendesk macro
   suggestions, Zendesk resolution tiers). For OSS, search GitHub by stars AND check the licence — a
   permissive peer beside a restrictive leader closes a licensing wedge.
2. **COGS structurally above price**, in either direction: your unit cost exceeds what the market
   pays (media, video, OCR at volume), or the incumbent's marginal cost is zero (BYOK, free tier,
   monetised elsewhere — e.g. free gift cards funded by brand rebates) so no price can undercut it.
3. **Access: the founder cannot legally or physically operate it.** Licences, credentials,
   accreditation regimes, discretionary partner gates wanting local sponsors, capex, float, or a
   product whose deliverable is compliance evidence sold by an unaudited vendor.

## Stage 4: the scorecard

Everything else is a score, not a gate. Rate each 0-2 and record the evidence:

| Dimension | 2 | 0 |
|---|---|---|
| Demand evidence | Tier 1-2 on the hierarchy, dated, current | Only tier 5-6, or inference from pricing pages |
| Position | Occupied by expensive/sales-led vendors leaving a self-serve or down-market slot | A loved, cheap, self-serve incumbent already in the exact slot |
| Founder fit | Buyer/domain known from the inside | Learned from a listicle this week |
| Contract test | Weeks of integration/domain work | Buyer's engineer builds it in a day (then it is a snippet, not a product) |
| Distribution | A winnable channel exists: marketplace category, unfarmed long-tail terms, an owned audience | Head terms owned by funded content machines AND no marketplace/audience alternative |
| Buyer arithmetic | 100-300 buyers at $50+ plausible | Needs 1,000+ churny consumers |

Notes that correct past mistakes:
- **An occupied position is normal and usually good.** Real micro-SaaS markets support many
  profitable vendors (a dozen in COI tracking; GrowthDot and Sparkly both selling GDPR deletion at
  $50-249/mo in one marketplace). A sales-gated incumbent with no public pricing is evidence of a
  self-serve gap as much as a threat — score it, don't flinch.
- **SEO failure is not fatal on its own.** Marketplace categories, integrations directories, and an
  owned audience are distribution channels too; Sparkly built 100+ installs with no content
  operation. Score distribution as a whole.
- Moat class breaks ties between two candidates that both score well. Nothing more.

## Stage 5: verify before calling anything alive

First-pass survivors flipped to dead 4 out of 4 times until verification became structural. A
screening without this stage produces "not yet killed", never "worth testing". Hunt specifically for:

1. **Sales-gated competitors' real capability.** Their pricing page hides it; read their product
   docs, changelogs, marketplace listings, demo videos, and customer quotes. (Pageloop's homepage
   detail killed a candidate the pricing-page pass had cleared.)
2. **Platform-owner releases, current year, by name.** Release notes and community announcements,
   not just the marketing site.
3. **Refutation framing.** The verifier's job is to refute the candidate and fail. A candidate
   confirmed by a refutation attempt that found both killers absent (Sparkly delete-only, GrowthDot
   Support-only, Zendesk's own docs stating the fragmentation) is the strongest desk result this
   method can produce.
4. **Re-base the evidence.** Replace every dated complaint with the incumbent's current
   documentation of the same limitation, or drop it.

## Verdicts and the funnel discipline

Three verdicts, appended to the ledger every time with evidence and unchecked sources named:

- **KILL** — a hard gate fired, with the killer named and cited. A high scorecard never survives a
  fired gate.
- **WEAK** — no gate fired but the scorecard is poor. Record and rank; do not iterate on it.
- **WORTH A CHEAP TEST** — verified survivor. Name the designed test, its cost, and its threshold
  (e.g. "20 outreach emails to non-network buyers; 3 replies saying 'we built this ourselves' or
  'what would it cost' passes").

**One WORTH A CHEAP TEST candidate ends the screening round.** Run the test before screening anything
else. Endless screening is the failure mode this skill has actually exhibited, not a hypothetical.

**Base-rate check.** A rigorous screen should still pass roughly 10-30% of a batch to WORTH A CHEAP
TEST. A batch of 10+ ideas with zero survivors flags the filter, not the ideas — stop and audit which
rule did the killing before running another batch. (The ledger's own history: 49 straight kills, then
an audit found the verdicts individually sound but the sourcing and gate structure at fault.)

**Anti-portfolio.** Every 6-12 months, revisit the dead table: which kills turned out false (someone
built it and it worked)? Log which rule produced the false negative. Before killing any idea, spend
one paragraph on "why WILL this work" — domain experts find it easy to list reasons something fails.

## Validation (the cheap test) and after

The bar: **10 paying customers from outside the founder's network who actually use it** (for an API,
the second call, not the first). Payment alone is not validation. When the buyer is a platform's
customers, one emailed question to 30 companies ("do you run X today, and did you build it
yourselves?") beats a waitlist: three "built it ourselves, wish we hadn't" outweigh any signup count.

Ship in two weeks: one endpoint or one screen. For an API, be drop-in compatible with the incumbent's
contract; for an app, build the one-click importer. Distribution order after launch: the winnable
channel found in stage 4 first (marketplace listing, "X alternative" SEO, Zapier/Make, YouTube,
answering the stage-2 threads). Start pricing higher than instinct. Churn is often a marketing bug:
wrong-expectation arrivals churn, so fix copy before building.

## Traps

1. **Absence of evidence is not evidence of absence.** Rate-limited or badly worded searches return
   nothing and the market looks empty. Confirm with direct fetches of named candidate sites plus a
   GitHub-by-stars search, and label every "nothing found" as *not found in the sources I checked*.
2. **Do not invent a differentiator to rescue an idea.** No graded demand evidence means no gap.
3. **The variant is not a new idea.** "But with X export" or "but for Y niche" revives a dead idea
   only if X or Y defeats the named killer. Usually X is the free part.
4. **Document parsing/extraction is a commodity** (AWS, Google, Azure price floor).
5. **Avoid social networks and marketplaces you'd have to bootstrap** — cold starts are not
   solo-founder problems. (Selling INTO an existing marketplace is fine and often the channel.)
6. **Do not delete dead ledger entries to make room for optimism.** Re-screening under a corrected
   rule is legitimate; erasing a kill that rested on independent evidence guarantees the search gets
   re-run. When a rule changes, audit which entries died ONLY to the changed rule and re-open just
   those.
7. **Skill drift.** When this file needs correcting, rewrite the rule in place and move the history
   to the ledger. Layered rules-about-rules push every future reading toward the most conservative
   interpretation, which biases toward KILL. Keep this file under 250 lines.

## References
- `references/verdict-ledger.md`: every idea screened (read first, append after), plus
  machine-specific source availability and the method's change history.
- `references/sources-and-benchmarks.md`: founder case studies with real numbers,
  drop-in-compatibility precedents, and the evidence behind the gap taxonomy.
