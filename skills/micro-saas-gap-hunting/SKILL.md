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

1. **Read `references/verdict-ledger.md`.** It records ideas already screened and killed, with the
   specific killer named. Never re-run a dead search or re-propose a dead idea.
2. **Confirm the goal.** These two filters conflict and both are correct in context:
   - Venture-scale filter (YC): name the novel insight incumbents lack, or drop it.
   - Micro-SaaS filter (this skill): competitors mean people are paying, so enter.
   Applying the venture filter to a $10K/month goal kills good ideas. Ask which one applies if unclear.

## The funnel

### 1. Pick 5 targets
Tools with public per-unit pricing, a simple request contract, and a large user base. Prefer ones the
user would personally buy. Founder-market fit is a bonus here, not a requirement: market validation
substitutes for personal insight under this strategy.

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
   migrating right now. Highest-value signal when present.

Record complaints **verbatim**. The exact phrasing becomes landing-page copy. Messaging is the
primary lever, not features.

### 3. Classify the gap
Ranked by durability:

| Gap type | Durability |
|---|---|
| Licensing blocker (AGPL etc.) | High. Hard enterprise no |
| Capability wall | High |
| Displacement event | High but time-boxed |
| Complexity / bad DX | Medium-high |
| Upmarket drift | Medium |
| Pricing opacity (credits) | Medium, and very common |
| Raw price alone | Low. A race to the bottom |

The most repeated gap across unrelated markets is **pricing legibility, not a missing feature**. See
`references/sources-and-benchmarks.md` for the evidence. "Flat, predictable, per-unit pricing, no
credits" is a positioning you can own without inventing anything. Pair it with at least one
non-pricing gap so you are not competing on price alone.

### 4. Run the kill tests, in this order
Cheapest first. Each has killed a real candidate.

1. **Free OSS anchor.** Search GitHub by stars *first*. A mature library kills the API business.
2. **Giant incumbent.** If AWS, Google, Azure, or the platform owner ships it as a commodity, walk away.
3. **Free anchor inside the market.** A free hosted competitor caps your price at zero.
4. **Contract test.** Can you clone the request and response shape in a weekend? If yes, stage 5 is free.
5. **COGS test.** Compute cost per unit against your price. Where media, video, and TTS ideas die.
6. **SEO test.** Can you rank for "X alternative"? This is the hidden prerequisite, see traps.

A high score on any scorecard does not survive a failed kill test.

### 5. Build the migration path, not the product
For an API this means **be drop-in compatible with the incumbent's contract**, so migration is one
line of the customer's code. For an app, build the one-click importer. Verified precedents are in
`references/sources-and-benchmarks.md`.

### 6. Validate before building
Landing page plus direct outreach to the people found complaining in stage 2. No product yet.

The bar for real validation is stricter than usual: **10 paying customers from outside the user's
network who actually use it.** Payment alone is not validation; people will pay for a non-existent
product out of politeness. For an API, watch for the second call, not the first.

### 7. Ship in two weeks
One endpoint or one screen. No auth, no dashboard, no billing, no integrations, no logo.

## After launch
- **Distribution order:** SEO on "X alternative", then Zapier and Make listings, then YouTube
  tutorials (video ranks where the first page is unwinnable), then Product Hunt for backlinks, then
  answering the threads from stage 2.
- **Pricing:** start higher than instinct. Raising prices improves customer quality.
- **Churn:** cancellation dropdowns produce nothing. Research the account, guess the reason, email one
  yes/no question. Near-100% response rates, and it took one founder from 11% to 7% churn.
- **Churn is often a marketing bug.** Wrong-expectation arrivals churn. Fix copy before building.

## Traps

1. **Absence of evidence is not evidence of absence.** The most common failure. Rate-limited or badly
   worded searches return nothing and you conclude the market is empty. Always confirm with direct
   fetches of named candidate sites plus a GitHub-by-stars search. Label every "nothing found" as
   *not found in the sources I checked*, and say which sources went unchecked.
2. **Do not invent a differentiator to rescue an idea.** If stage 2 produced no verbatim complaints,
   there is no gap. Go back to stage 1.
3. **SEO is the hidden prerequisite.** The reference benchmark converts 1.5-2% of freemium users, so
   $11K MRR rides on ~35,000 visitors a month. Undercutting is not a moat; owning the search term is.
   If that term is unwinnable, find the channel before starting.
4. **Document parsing and extraction are commodities.** Anything shaped like "API that extracts
   structured data from documents" competes with AWS Textract, Google Document AI, and Azure on price.
   Rendering and infrastructure ideas hold up far better.
5. **Avoid social networks and marketplaces.** Cold-start problems are not solo-founder problems.

## Output discipline

When screening an idea, always report:
- the verbatim complaints found, with source
- which kill tests it passed and failed
- **what was not checked** (pricing tables, review counts, search volume, COGS are the usual gaps)

Then append the verdict to `references/verdict-ledger.md`, dead or alive, with the killer named.

## References
- `references/verdict-ledger.md`: ideas already screened. Read first, append after.
- `references/sources-and-benchmarks.md`: the two founder case studies with real numbers, the
  drop-in-compatibility precedents, and the evidence behind the gap taxonomy.
