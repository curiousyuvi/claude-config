# Verdict ledger

Ideas already screened. **Read before proposing anything. Append after every screening, dead or alive,
with the specific killer named.** Each dead entry is a search nobody has to run again.

Last updated 2026-08-19.

## Dead

| Idea | Killer |
|---|---|
| DMARC report parsing API | `parsedmarc` (1,282 stars), mature and free |
| NACHA / ACH file generation API | `moov-io/ach` (558 stars) ships its own HTTP server |
| ICS / RRULE API | Free libraries, no market. Search found only spec docs |
| ZPL label rendering API | Labelary is a free anchor, plus fckzpl (free Labelary-compatible), zplrender, editorzpl, OSS renderers |
| Invoice / receipt / bank-statement OCR API | Veryfi, Mindee, AWS Textract, Google Document AI, Azure, LlamaParse, plus public price-comparison sites |
| Google Merchant product feed API | Google ships the Merchant API itself |
| Accessibility / WCAG audit API | `axe-core` is the free engine everything is built on |
| HS code classification API | Zonos (90%+ accuracy, ~200 countries, "trusted by customs authorities") and Avalara |
| Utility bill parsing API | LandingAI, invofox, conversiontools |
| FDA nutrition label generation API | ReciPal and LabelCalc, both with APIs |
| AI YouTube thumbnail generator | Pikzels (~819K users), Canva shipping Magic Layers free from 2026-03-11, plus a swarm of free image-to-layers tools (Layerize, GenPsd, Image2Layer, Unlayer, imagetolayers) |
| Docs screenshot / visual freshness tool | AppRefresher, EmbedBlock, Promptless Capture, Scrnify, Heroshot. Video layer taken by Videate |
| Canny alternative | Featurebase ($19/mo vs Canny $29/mo), Frill, FeatureOS, plus an r/SaaS founder who already shipped one. Tip was stale by the time it was checked |
| Meeting-bot recording API (Recall.ai) | Two OSS anchors, Vexa (2,693 stars, Apache-2.0) and Attendee (707 stars), plus Recall's own public flat $0.50/hr so there is no legibility gap, a $38M Series B, and a browser-per-meeting-hour COGS. Undercut already underway via Skribby and MeetingBaaS |
| Email / calendar sync API (Nylas, Cronofy) | Unipile already owns the flat-per-account position (EUR 5/account/mo, EUR 49 minimum, no usage fees, 3,000+ clients) and Nylas now publishes per-connected-account pricing, so the opacity gap is closed. Self-hosted anchors: EmailEngine, rustmailer (493 stars). Only complaint found dated 2018 |
| EDI / X12 translation API (Stedi, Orderful) | Translation is a commodity: omniparser (1,085 stars, MIT), stupidedi (292), staedi (150), plus a free X12-JSON converter posted to HN 2026-04-07. The real asset is AS2/VAN connectivity and per-retailer certification, a capability wall against a solo founder. Stedi took $70M and pivoted to healthcare clearinghouse |
| 1099 / W-9 e-filing API | Stripe Connect ships 1099-NEC/MISC/K filing, state filing and recipient delivery natively for the exact platform segment an API would sell to. Avalara (Track1099) holds the direct-payer side at 195,000+ customers on pay-as-you-go pricing and already markets the FIRE-to-IRIS shift. Stage 2 produced zero user complaints, only a rival founder |
| Webhook delivery infrastructure (Svix, Hookdeck) | Svix ships an open-source core with a free tier, and "webhook delivery service" is the most-cloned portfolio project on GitHub (105+ repos of the exact shape). Upstash QStash, Inngest and Cloudflare sell it as a commodity primitive |

## Alive, small incumbents, correct shape

| Idea | Who is there | Note |
|---|---|---|
| Error tracking, Sentry-SDK-compatible | GlitchTip, Bugsink, both self-host-first | **Current top candidate.** Live displacement: Highlight.io shutting down after the LaunchDarkly acquisition, public migration guides already exist. Opening is hosted, flat-priced, zero-ops. Risk: storage-heavy COGS, and two free OSS anchors |
| Media / image transformation API | ImageKit, imgix, Uploadcare, plus OSS imgproxy and Thumbor | Cloudinary is the most-complained-about tool found in the whole sweep, and the complaint is specific ($99 floor, credit opacity). Risk: bandwidth COGS, crowded |
| Scraping / crawl API | WebcrawlerAPI, Jina, Tavily, Exa, ScrapingBee, Apify, Spider | Firecrawl's three gaps are already published: protected sites, AGPL-3.0, unpredictable credits. AGPL is a non-pricing gap and more defensible. Risk: most crowded field found |
| E-signature API | firma.dev ($0.049/envelope), eSign.AI, Documenso | Undercut already underway without us. Trust and legal weight high |
| 3D / CAD thumbnail rendering API | frame3d.dev, 3DCompare CAD.ai | Closest structural clone of ScreenshotOne. Tiny players. Buyers in e-commerce, 3D printing, CAD |
| COI / ACORD 25 parsing API | coiparseapi.com (ACORD 25 and 28, 50 free parses), Apryse | COI tracking is a painful, money-heavy workflow for GCs, property managers, franchisors |
| Walkthrough video rendering API | Videate at app layer only. Shotstack, Creatomate, JSON2Video do not drive browsers | Real gap. Video COGS is the open question and probably the deciding factor |
| EU Digital Product Passport | eudigitalpassportprocessor.com, dppmcp.com | Very early. Hard deadline: 2027-02-18 for EV, industrial and LMT batteries |
| Peppol / e-invoicing API | Peppox, ClearTax, Complyance, competing openly on developer experience | France mandate Sept 2026. Regulatory deadlines force adoption |

## Checked and too crowded to recommend

Browserbase and Browserless alternatives (Steel.dev, Hyperbrowser, BrowserBash, sliplane), Cloudinary
at the app layer (25+ listed alternatives), WorkOS (Scalekit, Datawiza, Keycloak), ElevenLabs (crowded
and compute-heavy).

## Not verified for any entry above

Pricing tables, review-sentiment counts, "X alternative" search volume, and COGS per unit. These are
the numbers that actually decide it. Do them before writing code.

## Method notes from the session that produced this

Two entries were initially and wrongly declared "empty market" because rate-limited searches returned
nothing. Direct site fetches later found several established competitors. Treat a zero-result search
as a broken tool, not as a finding.


## Session 2026-08-19b: five fresh targets, all dead

Sources reachable that session: HN Algolia full-text, the GitHub search API sorted by stars, and direct
fetches of vendor pricing pages. Reddit (403), Google, Bing, DuckDuckGo and every searx instance tried were
blocked, so no Reddit or G2 sentiment and no keyword-volume numbers back any of the five verdicts below.
Treat them as *not found in the sources checked* on the complaint side; the OSS-anchor and pricing kills are
first-hand and solid.

The recurring pattern across all five: the flat, predictable, per-unit pricing position was already taken by
a small incumbent (Unipile, Skribby, Svix free tier) or by the giant itself (Recall.ai publishes $0.50/hr
prorated to the second). Pricing legibility is getting harder to own than the ledger's earlier entries assume.