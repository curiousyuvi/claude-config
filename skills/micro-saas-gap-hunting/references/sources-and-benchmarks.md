# Sources and benchmarks

## Case study 1: ScreenshotOne (Dmytro)

Screenshot API. Interview: "How I Built It: $12K/Month Micro SaaS", Starter Story, Nov 2024,
https://www.youtube.com/watch?v=TCGXT7ySco8

- 280 customers, ~$12K MRR, 40-60% profit margins, ~$4,500/mo total expenses
- ~2M screenshots/mo, of which $3-4K/mo is servers
- First paying customer: $7/mo, after a month of promoting everywhere
- Pricing went $5 (near-zero margin), then $7, then higher
- Churn 11% to ~7%, targeting under 5%
- Took 5 months to build v1 and calls that his main mistake. Now targets 1 month or less
- Stack: TypeScript + Puppeteer for headless browsers, Go for rate limiting and API keys, Cloudflare
  for storage, PostHog for funnels and paid-signup attribution, Crisp chat wired to his phone,
  Google Search Console and Keyword Planner for SEO

Key quotes:
- *"I went to Google and I saw so many competitors, it means there are people paying. That was a good heuristic to evaluate the niche."*
- *"I reduced my list of ideas only to API products, it was kind of my super skill."*
- *"Some people can just pay you even for a non-existing product, but you still don't know will they use it."*
- On unobvious channels: Zapier and Make listings were surprise winners. A stranger's YouTube tutorial
  about his product brought paying customers, and video ranks in Google where the first page is
  unwinnable for text.

## Case study 2: Youform (Abhishek)

Typeform alternative. Interview: "I Copied a $100M SaaS, Undercut Their Prices, and Hit $10K/Month",
Starter Story, Aug 2025, https://www.youtube.com/watch?v=_KaFS4Dxs5k

- $11K MRR, ~35,000 registered users, ~500 paying, ~35,000 unique visitors/mo
- Freemium, 90%+ of features free, converting 1.5-2%
- 4M+ form submissions, under $1,200/mo total expenses
- MVP in **2 weeks**: name/email/star-rating fields plus CSV export. No integrations, no logo, no
  real landing page. His wife designed the current page once they had 200+ users
- Stack: Laravel, AWS, Cloudflare, Stripe, OpenAI for fraud detection, Slite for help docs,
  Simple Analytics, Canny for feedback, Mailgun

Origin: his previous SaaS (Botflow, a no-code chatbot builder, ~200 users) revealed that most users
wanted a conversational form as a Typeform alternative, and Typeform had just raised prices. He then
mined **Typeform's own forum**, Twitter and Reddit for the other missing features, killed Botflow, and
built Youform.

His four steps, verbatim:
1. Look for a popular tool, search Twitter and Reddit for "X alternative"
2. Find the pain points or gaps they are not solving. *"It is fine if the pain point is pricing, but only if pricing is too high"*
3. Reach out to those users with just a basic landing page. *"Messaging is the key here"*
4. Bonus: a one-click migration tool. Youform lets you paste a Typeform URL and generates the
   equivalent Youform in seconds

Key quotes:
- *"You should not invent things. As an indie hacker, as a bootstrapper, you can't create the next Uber. You should approach the market which is already validated."*
- *"Most developers think most ideas have already been built, but there is always a gap."*
- *"Don't build things because you can. First search for what people are looking for, then build it."*
- Avoid: social media and marketplaces.

## Drop-in compatibility precedents

The migration wedge, already executed in the wild. This is why API-shaped products suit this strategy.

- `sarcascoder/openextract`: *"self-hosted, API-compatible drop-in replacement for AWS Textract. Point
  your existing boto3 Textract code at OpenExtract by changing one line (endpoint_url)."*
- `fckzpl.com`: *"Free Labelary-compatible API for rendering ZPL labels. Drop-in replacement."*
- `bugsink.com`: self-hosted Highlight.io alternative with **Sentry SDK compatibility**, so migration
  is changing a DSN string
- The whole category of OpenAI-compatible inference APIs
- Blog posts of the form "Claude API at 1/10th the price: I built a drop-in proxy"

## Evidence: pricing legibility is the most repeated gap

Four unrelated markets, same complaint, in users' own words:

- Cloudinary, r/webdev: *"Looking for alternatives to Cloudinary to host only images. I like them a lot, but the cheapest tier $99 a month for 225 gigs is overkill"*
- Cloudinary, r/node: *"it gives me 25 credits per month but idk how to estimate"*
- Cloudinary, Toolradar: *"the most feature-rich media management platform but its credit-based [pricing]"*
- Firecrawl, dev.to: *"hits a wall on protected sites, AGPL-3.0 licensing, unpredictable credit costs"*
- Cursor: an article titled *"Cursor's Credit-Based Pricing Model Is Confusing and Leaves Devs Frustrated"*

## Evidence: the kill tests have teeth

Real examples of each test firing:

- Free OSS anchor: `parsedmarc` (1,282 stars) killed DMARC report parsing. `moov-io/ach` (558 stars),
  which ships its own HTTP server, killed NACHA file generation. `axe-core` killed accessibility audit
  APIs. Free date libraries killed the RRULE API.
- Giant incumbent: Google's own Merchant API killed product-feed tooling. AWS Textract, Google
  Document AI and Azure killed invoice and receipt OCR.
- Free anchor in market: Labelary is free and killed ZPL rendering, which also has fckzpl offering a
  free Labelary-compatible clone.

## Related reading in the user's own knowledge base

`~/Desktop/SaaS-Idea-Finding-Research/` holds 20 source deep-dives plus a synthesis. Most relevant:
- `docs/15-idea-evaluation-scoring.md`: the weighted scorecard, painkiller vs vitamin, Sean Ellis 40% test
- `docs/11-mining-reviews-complaints.md`: review mining technique
- `docs/12-reddit-forum-community-mining.md`: pain-signal phrases and monitoring tools
- `docs/18-acquisition-marketplaces-competitor-research.md`: clone-and-improve, SEO gap analysis
- `docs/02-y-combinator-idea-advice.md`: the venture-scale filter and the tarpit test
- `01-METHOD-gap-hunting-for-micro-saas.md`: the narrative version of this skill

Scorecard adjustment when using doc 15 with this method: score "competition" on whether the
incumbents' gaps are **documented and attackable**, not on how few competitors exist.
