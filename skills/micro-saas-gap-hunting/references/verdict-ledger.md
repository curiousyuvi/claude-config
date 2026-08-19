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
