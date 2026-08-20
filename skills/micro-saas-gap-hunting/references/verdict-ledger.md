# Verdict ledger

Contents: contractual exclusion note · Dead table (round 1) · Alive table · Pending · per-round
sections in date order (2026-08-19c/d/e, 2026-08-20 a-e) · method-change notes · source availability
per round. For dedupe use references/screened-index.md; this file holds the full evidence.

Ideas already screened. **Read before proposing anything. Append after every screening, dead or alive,
with the specific killer named.** Each dead entry is a search nobody has to run again.

Cleared 2026-08-19 at Yuvraj's request. The prior ledger (22 dead, 9 alive, 9 pending, plus method
notes) is recoverable with:
`git -C ~/.claude show 3e9cc16:skills/micro-saas-gap-hunting/references/verdict-ledger.md`

## CONTRACTUAL EXCLUSION 2026-08-20: the entire support/helpdesk domain is off limits

Yuvraj's employment contract bars him from building customer-support tooling. Nothing in that market
may be screened again: helpdesks, ticketing, help centres and support knowledge bases, support AI agents,
conversation QA, support analytics, and any app or add-on sold to Zendesk / Intercom / Freshdesk /
Help Scout / Gorgias / Front.

**Scope, confirmed by him 2026-08-20: "only customer support".** The test is who the buyer is. Developer
and API documentation tooling sold to DevRel, docs and product teams is NOT excluded and may be screened.
The first round under this constraint over-read it and dropped the docs axis for nothing.

Consequences, which are severe and must not be quietly forgotten:

- **E1 (Zendesk DSAR / right-to-erasure fan-out) is unavailable.** It remains the only candidate that
  ever passed verification in 50+ screenings and its research still stands as the method's best
  worked example, but it cannot be built. Do not revive it, and do not treat its ZAF feasibility
  check or the 20 outreach emails as pending work.
- The "content-gap detection for the non-Intercom/Zendesk helpdesk tail" entry in the alive table is
  likewise unavailable.
- Roughly 30 of the dead entries below are support-domain screenings. They stay in the ledger as
  history, but the anti-portfolio review should skip them: a false negative there is unactionable.
- Target selection must move to the founder's other axes: edge/CDN and multi-tenant web
  infrastructure, document and video generation, LLM application engineering, India-side operations.
  These have thinner evidence than support, and that is the cost of the constraint, not a reason to
  drift back.

## Dead

| Idea | Killer |
|---|---|
| Ground-only dangerous goods shipping papers (49 CFR) | Position test run 2026-08-19 and it fails at the bottom of the market, which is where the buyer arithmetic needed it to be open. ShipWave sells a dangerous-goods add-on from **$19/mo** on top of a free shipping core, generating the Shipper's Declaration; ShipHazmat (Bureau of Dangerous Goods) is web-based self-serve with a free trial, published plans and FedEx approval, producing bills of lading compliant with 49 CFR 172.200-172.204 and declarations meeting IATA Section 8. DGOffice ~$500/user/yr and Labelmaster from $500/mo sit above. A $19/mo floor means ~600 customers to reach the goal. Two independent kills stand alongside: misclassification liability (penalties run $1,200-$7,500 per shipping-paper defect) which a solo founder in India cannot underwrite, and carrier acceptance depending on vendor-recognition lists |
| Help-centre content-gap detection from support tickets (general case, Intercom/Zendesk shops) | Platform owner ships it natively inside the product the buyer already pays for. Intercom's Fin content gap recommendations scan unresolved conversations, compare them to human replies, and surface missing, unclear, duplicated or contradictory help content, ranked by impact, generated weekly, at Fin AI Agent > Analyze > Optimize, with a review drawer showing the conversations behind each suggestion and one-click article edits or snippets. It even operates on content synced from Zendesk and on Salesforce knowledge articles, so it covers the competitor's KB too. Recommendations sit behind the Pro add-on but snippet-creation suggestions are available to all customers; Zendesk ships knowledge-gap stats plus A/B answer testing. The one documented limitation is that it is reactive rather than predicting staleness, which is a docs-QA product Intercom can ship natively and not a wedge for an outsider. Zendesk removed Content Cues on 2025-05-01 but replaced it with Knowledge Builder (analyses the last 90 days of tickets and auto-drafts articles) plus a Knowledge Base Gaps Discovery add-on, so that gap closed itself. The leftover Freshdesk/HelpScout/Gorgias tail is already camped on by eesel AI, self-serve at $0.40/ticket with no platform fee and a no-card trial, plus Forethought upmarket. The single demand signal found was a Zendesk community complaint about Content Cues being removed, and Zendesk answered it in the same thread by pointing at Knowledge Builder; GitLab's support team hand-rolled the job internally rather than buying. SEO is owned by Zendesk, Intercom, eesel and Forethought content marketing. Screened 2026-08-19 under the corrected gate |
| Answer-engine citation tracking for product documentation / help centres | No docs-specific entrant exists, but the generics cover the mechanics and the free layer covers what a docs team would actually check. Profound ships page-level "Watched Pages" citation tracking ($399-499/mo), Gauge does domain and page-level citation rates across 6+ engines, Otterly does URL-level link citation analysis from $29/mo; Peec from ~EUR 89/mo on $29M raised and $4M ARR in ten months; Scrunch $250, Athena $295, Rankscale $20-49. Free anchors killed the cheap end: Google Search Console shipped Generative AI performance reports (AI Overviews, AI Mode, per-page) on 2026-06-03 and Cloudflare AI Crawl Control gives per-bot per-path analytics free on all plans, with server logs showing OAI-SearchBot for nothing. The docs platforms are the natural owners and are already moving: Mintlify ships AI agent traffic analytics (213M agent requests in July, 66% of docs traffic) and launched Mintlify Index in Aug 2026, with GitBook and kapa.ai adjacent. Buyer arithmetic fails on budget location: citation-tracking spend sits in marketing, while docs teams buy deflection bots (kapa, Inkeep, Fin), not monitoring. SEO fails both ways, head terms owned by funded content machines and the docs long tail has no measurable volume. COGS actually passed (~$20-90/mo per customer against $100-400 pricing) but is moot |
| COI endorsement + mid-term cancellation verification | **Was the top pending candidate; both blocking tests came back negative on 2026-08-19.** Endorsement matching against contract requirements is already sold: Billy does AI extraction of insurance requirements from contracts plus automatic contract-to-COI-to-endorsement comparison, explicitly detecting Additional Insured, CG 20 10, CG 20 37, PNC and waivers of subrogation, and exposes an API; COISoftware markets reading "the CG 20 10 itself" to catch endorsements that do not name the certificate holder, covering ACORD 24/25/27/28, CG 20 10/20 37, CG 24 04, WC 00 03 13, declarations, bonds, W-9s and loss runs, also with an API. The cancellation half confirms the feared answer: document-based monitoring structurally cannot detect a mid-term cancellation (a PDF never changes, and ACORD 25 says insurers have no obligation to notify holders), so it requires agency-management-system feeds, and Certificial holds that estate with connections to 25,000+ agencies writing 90%+ of US and Canadian commercial business, updating within seconds. That estate is unreachable for a solo founder in India. CB Insights scored Certificial 9.4/10 as the only real-time player of six assessed |
| Per-customer AI cost and gross-margin attribution for AI-native SaaS | Position taken and given away free. Helicone ships per-request cost attribution, per-user spending, per-model breakdown and budget alerts as first-class out-of-the-box features via one line of headers, free to 10,000 requests/mo then from $20/mo; Langfuse self-hosts free and unmetered (MIT/Apache) with 50,000 events/mo free cloud and Core at $29/mo, and supports per-tenant attribution through span attributes. Also in-market: Portkey, Traceloop, OpenMeter, Vantage, CloudZero for the FinOps rollup to business dimensions, native LLM cost views in Datadog, and Attribute (attrb.io) already selling the runtime eBPF version for untagged gateways. The literature treats gateway-tier tagging as the solved standard approach on OpenTelemetry GenAI conventions, so the buyer's engineer adds a `user_id` tag rather than buying a product. Screened 2026-08-19 under the corrected gate; the pain is real and well documented but the seat is taken at $0 |
| Inbox placement / deliverability testing API (was the top candidate) | Position and free-anchor tests failed 2026-08-19. Unspam already sells a per-provider inbox placement API (async, Bearer token). MailerCheck sells placement tests pay-as-you-go at 200 credits = ~$2/test, no subscription. "Inbox Placement Test" (check.live-direct-marketing.online, on Capterra) holds the dev-first slot: free tier 3 tests/day no signup, paid REST API, even an MCP server. Free anchors inside the market: EmailWarmup.com (unlimited free tests, 15+ providers), MailReach (3 free/day), Unspam (10 free/mo), MailGenius. Inbox Radar took the flat-unlimited slot at $23/mo. The seed-mailbox estate turned out to be widely reproduced, not a moat — the old ledger's "zero entrants" read was stale (SpamCipher and Hello Inbox were already the warning) |
| Peppol / e-invoicing API | Position taken several times over: e-invoice.be (€0.18/invoice pay-per-use, "no sales call"), getpeppr (built exactly for embedded multi-tenant SaaS: one key, N legal entities), peppol.sh, Storecove (API-first from €495/mo). Owning the estate also fails the access test: certified AP needs mandatory ISO 27001, ~€1,025 sign-up + €1,800/yr candidate then €4,150/yr certified OpenPeppol fees, 3-stage accreditation, 24/7 AS4 uptime. France Sept 2026 wedge needs separate PA (ex-PDP) certification and 101 PAs are already approved |
| EU Digital Product Passport (battery, deadline 2027-02-18) | Position test failed: DPP-Tool owns the self-serve SME slot at €9/mo, no implementation fee, no sales call. PicoNext and Tappr at ~€520/mo mid-market, Substantio/ProductPass/DPP Automate/Circularise/Siemens above. OSS-anchor test passed (biggest active repo open-dpp, 28 stars AGPL; reference impl archived) but the €9 floor caps pricing and the deadline demand is already being served |
| 3D / CAD thumbnail rendering API | Giant + OSS + position all failed: Autodesk Model Derivative renders 70+ formats incl. STEP/STL thumbnails at ~$0.30/simple job with a free monthly tier arriving under the new APS model; `fpurchess/preview-service` is an MIT docker-run HTTP thumbnail service (stl/obj/ply), stl-thumb + FreeCAD/OpenCascade cover the conversion path free; 3DCompare CAD.ai already holds the niche hosted slot |
| COI / ACORD 25 parsing API (re-screened under the corrected gate) | Textbook instance of trap 4, document extraction is a commodity. Position is taken many times over by insurance-native extractors: Sensible ships prebuilt ACORD 25 and loss-run extractors and a 400+ form comparison rates it best on developer experience and transparent pricing; ScanDocFlow sells a dedicated ACORD 25 OCR API (99% claimed, <15s/form); Base64.ai covers ACORD 23/24/25/27/28/101/125/126 by API; Docsumo has pre-trained ACORD 24/25/125 models; Reducto, Talonic (free browser tool plus API), Klippa and Parsio all parse COIs, with Textract underneath as the giant. Note the survivors' own pricing floor: Parsli free then $25/mo with API on every tier, Parseur ~$39/mo. Re-screened 2026-08-19 after the moat-gate correction and it dies on position alone, so the correction did not rescue it |
| Unified API over veterinary PIMS (and the dental variant) | The integration-estate moat is real and it belongs to the incumbents. Position: DataHub Vet sells itself verbatim as a "Veterinary API & PIMS Integration Platform" covering AVImark, Cornerstone and Shepherd; Sikka's "ONE API for Dental and Veterinary Developers" spans 100+ endpoints across both verticals, so one player guts both. NexHealth is funded in the dental lane, Bitwerx and Vetdata do vet connectivity. Access is the decisive kill: ezyVet, the friendliest system, gates its API behind a discretionary application that requires **named sponsoring clinics and a referral** ("you will still need to engage the clinic(s) to obtain approval to access their data", "indicate who referred you to the ezyVet API"), while Cornerstone and AVImark are on-prem with no public API, reachable only through IDEXX/Covetrus enterprise partner programmes. A solo founder in India with no clinic relationships cannot get in, and a v1 covering only ezyVet is worthless because that is the one API buyers can already get direct. Open Dental being open source with a public API removes the moat on the one dental system he could reach |
| Hazmat / dangerous goods, **air (IATA DGR) half only** | Access test failed: air DG, which is where shippers actually fear rejection, needs a negotiated IATA DGR redistribution licence, quote-only through authorised sales agents, plus per-carrier software recognition (FedEx maintains a "Recognized DG Software Vendor" list). UN Model Regs and ADR are free to read but copyright-reserved, redistribution via the Copyright Clearance Center. Incumbent sales motion is quote-only enterprise trust selling (Labelmaster DGIS, DGOffice, IATA DG AutoCheck) to compliance managers rather than developers with a card. **Scope note 2026-08-19: this verdict covers the air/IATA half only.** The ground-only variant was originally killed alongside it partly on "then the moat is only software", which is no longer a valid killer, so it has been moved to pending below |
| NMFC freight classification API | The licensor now sells the product itself, self-serve with published prices: NMFTA's ClassIT+ API is tiered by revenue at $2,967-$9,809/yr ($3,412 for the non-member small-shipper tier), and NMFC data cannot be resold, so any entrant is a middleman on top of the licensor. SMC3 FastClass and BatchMark cover the rest. Demand side is gone too: NMFTA shipped a free NMFC Item Lookup Tool, Tai and ViewPoint TMS build classification in, and C.H. Robinson built its own internal agent — nobody buys a standalone third-party classification API. The 2025 density-restructure displacement is over |
| Age assurance / age estimation API | Platform owners now ship it free where the demand is: Apple's Declared Age Range API (iOS 26, no fee beyond developer membership) and Google Play Age Signals both return privacy-preserving age bands, going live for Texas 2026-01-01 with Utah 2026-05-06, Louisiana 2026-07-01 and a worldwide Play rollout through 2026, which is exactly the App Store Accountability Act demand. Position test also failed: Didit sells age estimation at a published $0.10/check with instant self-serve onboarding across 220+ countries and ID/KYC fallback on the same API; Patronscan $49/mo + $0.25/scan. The real moat is regulator recognition (Ofcom-recognised "highly effective" methods) and that accrues to the incumbents, not to a new entrant. Cloudflare ships nothing here, so that threat was unfounded |
| Reward / gift-card / incentive fulfilment API | Killed by a zero price, not by licensing: Tremendous makes gift cards, prepaid cards and donations **free to send**, monetising instead on rebates from the reward brands recipients choose (Amazon, Visa), charging only 4-6% on cash rails. You cannot undercut free, and matching the model requires brand rebate deals — a supplier estate a new entrant has no volume to negotiate. Access test fails too: the model is prefunded (fund the balance before sending, free only from US/EU/UK bank accounts), so it needs float Yuvraj does not have and cross-border payout rails he cannot legally operate solo. Runa already holds the developer-first payout-infrastructure position. Not independently verified: the specific money-transmitter and e-money licence positions of either vendor |
| Displacement sweep 2026-08-19: nine live events, all nine dead | A full HN-Algolia-plus-web sweep of 2026-05 onward, every event date-checked against a vendor page the same day. **Airtable acquired by Bending Spoons** (2026-08-04, $1.285B EV vs $11B 2021 peak, ~$480M ARR, closes late 2026): dead on position, NocoDB is a 64,590-star OSS anchor with an Airtable importer, Baserow 5,636, and Softr/Baserow/Noloco/Zite all shipped migration content within days, before any price change even exists to flee. **OpenAI Assistants API shutdown** (2026-08-26, seven days out; a compatibility-proxy search returns zero GitHub repos, so the position is genuinely open) dead on buyer arithmetic: one-time migration demand, OpenAI's own guide plus any coding agent does the port free, and laggards will not route their OpenAI keys through a stranger. **Fiddler Classic relicensed noncommercial** (2026-08-03, 45-day window to 2026-09-17): dead because Progress engineered the displacement to capture it itself via Fiddler Everywhere with a one-click importer, plus mitmproxy as the free anchor. **Fin/Intercom acquired by Salesforce** ($3.6B, 2026-06-15, ~30,000 customers): dead for a solo founder, every helpdesk published a capture page within weeks and Chatwoot is the OSS anchor. **Stripe Radar opt-out repricing** (July 2026, CA$0.07/screened txn after a forced trial ending 2027-01-22): dead, Stripe ships the free exit (downgrade to Radar Lite) and nobody solo out-models fraud ML trained on $1.9T. **Flowise shutdown** (announced 2026-07-29, EOL 2026-08-31): dead, code stays Apache-2.0 and "fork it" is the vendor's own advice, with Langflow and Dify as anchors. **Strava free API sunset** (2026-06-01, flat $11.99/mo, 241,000 developers): dead, the fee is priced to be payable so few migrate, and orphaned endpoints have no alternative source to sell. **Garnix Nix CI** (data deleted 2026-07-15): stale, and hosted CI fails the no-capex test. **Hetzner dedicated repriced 3-4x** (2026-06-15): real cohort, but serving it means owning servers. Confirmed stale or no-cohort, do not re-propose: Delighted/Qualtrics, Oracle free tier, omg.lol, Directus MSCL relicense, Mongock, Trinket.io, OpenRouter-to-Stripe, Resend new.email, Productiv. **Pattern: every live event dies to one of three things — the path was claimed within days by OSS anchors or funded vendors, the vendor engineered its own capture or free exit, or the demand is one-time** |
| EU AI Act compliance tooling (Annex IV docs, AI inventory, conformity files) | Position test failed at the exact wedge price: SetAIComply sells Starter at EUR 39/mo with a 14-day no-card trial including Annex IV templates and a risk classifier; Aurora Trust from EUR 49/mo self-serve, "no consultants"; Legalithm gives an AI-Act suite away free through ~April 2028. Worse, the urgency evaporated: the Digital Omnibus entered force 2026-07-27 and pushed Annex III high-risk obligations from 2026-08-02 out to 2027-12-02 (Annex I to 2028-08-02), leaving only Article 50 transparency biting now |
| EU Cyber Resilience Act / SBOM tooling | Free end to end. sbomify already sells self-serve (free Community tier, Business $159/mo, 14-day trial, literal "CRA Compliance Wizard") and is itself open source and self-hostable. OSS anchors: trivy 37,497 stars, syft 9,435, dependency-track 4,124, microsoft/sbom-tool 2,064, ort 2,068. GitHub and GitLab ship SBOM export free in CI, and the Article 16 reporting side routes through ENISA's own free single reporting platform, so there is no paid gap between free generation and free submission |
| PCI DSS 4.0 client-side script monitoring (6.4.3 / 11.6.1) | The buyer pool was regulated out of existence: on 2025-01-30 the PCI SSC removed both requirements from SAQ A entirely, so they now bind only SAQ A-EP, SAQ D and ROC merchants, not the small-merchant tail the idea targeted. Position also failed: c/side sells it self-serve with a free tier to 2,500 pageviews and Business from $99/mo with automated evidence generation. And Cloudflare ships client-side security script monitoring on ALL plans including Free, with a QSA whitepaper mapping it to these exact requirements |
| EU Deforestation Regulation (EUDR) due diligence | Position test failed: EUDRReady sells free/EUR 29/EUR 79 self-serve with 2-minute signup and AI extraction of DDS reference numbers; IntegrityNext sells a fixed-price self-service starter. Deadline and scope both moved against it: Regulation (EU) 2025/2650 (OJEU 2025-12-23) pushed application to 2026-12-30 for large/medium and 2027-06-30 for micro/small, AND removed the DDS obligation for most downstream actors and non-SME traders, so the long-tail buyer is exempt rather than late. TRACES remains free for manual submission |
| SaaS pricing / plan-change history API | Position taken by SaaS Price Pulse (276 pricing pages polled daily, free tier for 3 tools, Pro $19/mo, public API) — and its Pro tier is still "early access", meaning even the incumbent cannot find buyers above free. At least 6 Apify actors do poll-diff-webhook as a commodity. Buyer arithmetic also fails against a $19/mo incumbent with zero marginal cost. (Audit 2026-08-19: the original entry led with "Wayback backfills the history so there is no moat", which is no longer a valid killer; the position and arithmetic kills are independent and stand) |
| Third-party API deprecation / breaking-change history | Position test failed four times over in a niche barely a year old: APIDrift is live and self-serve (OAuth, no card), tracking 26+ APIs daily from 4 source types with AI severity classification and migration guides, free for 3 APIs, Pro $10-12/mo for 20, Team $30-35/mo unlimited. Breakage Radar, APIScout and ShiftGraph are all circling the same buyer. OSS anchors too: optic 1,535 stars, oasdiff 1,322, both free OpenAPI breaking-change detectors with CI actions |
| SaaS subprocessor-list change history (GDPR Art. 28) | The best-shaped idea of the data-moat round and still dead. DPAFlow already sells the exact product self-serve (7-day no-card trial, Starter EUR 99/mo, Professional EUR 299, Business EUR 999) including the supposed moat itself: dated evidence with URL, timestamp, content hash and stored snapshot plus itemised before/after diffs. Sub-Processors.com has already accrued the dataset in public: 3,901 companies and 55,162 subprocessors with per-company change timelines. Registora, ComplyDog and PageCrawl are also in-market. **Consolation signal worth keeping: buyers here demonstrably pay EUR 99-999/mo for diffed public-page history, so the class arithmetic is sound, the seats are just taken** |
| AI support-agent QA / regression testing, TEXT chat and email (the non-voice variant) | Inherits the voice-testing killer and adds a worse one: the platform owners ship it free inside the product the buyer already pays for. Intercom ships Fin batch tests, simulations, staged rollouts and pre-deployment scorecard Monitors natively; Zendesk ships "Test AI agent" in Admin Center plus a dialogue test widget and publishes its own multi-turn test-generation research. Position also taken: Coval sells self-serve text-or-voice simulation from $100/mo with a 7-day trial; Solidroad does AI-support QA with Zendesk/Intercom/Gorgias connectors on a $25M Series A. Free OSS anchors: openai/evals 19,200 stars, deepeval 17,697, evidently 7,819. Free hosted anchors: Braintrust Starter $0 with LLM-as-judge and unlimited experiments, Langfuse Hobby free and self-hostable. **Extend the dead voice entry to AI-agent testing in all modalities** |
| Help-center / KB migration and two-way sync API | Platform owner ships both halves free: Intercom's Zendesk help-center importer is free and no-code, and free hourly "sync public articles with Zendesk" plus Confluence/Guru/Notion sync; Featurebase ships free one-click importers for Intercom, Zendesk and Crisp. Every AI-support entrant subsidises migration to win the account, so the free anchor keeps regenerating. The paid remainder fails buyer arithmetic structurally: Help Desk Migration (Relokia) sells one-time per-record work ($100/1,000 records, $514 at 10,000), and a migration customer churns by definition, so there is no recurring $50+/mo base. Unito already sells two-way Zendesk sync |
| Docs-as-code publishing / git-backed sync for Zendesk-class help centres | The whole product is "render Markdown to HTML and PUT to the Help Center API keyed by an article ID in front matter" — a GitHub Action the buyer's engineer writes in a day, and Zendesk's own docs team publicly documents running exactly that pipeline in-house. The OSS that exists is stale and tiny (zendoc, zenpush, zendesk-helpcenter-cms all low-star), and GitHub tops out at 3 stars for the search, which is absence of pull rather than an opening. Buyers who want docs-as-code already left for GitBook/Mintlify, whose cheap tiers include GitHub sync natively; the Zendesk Guide holdouts are support teams who do not want git |
| Safe-to-embed workflow automation (the n8n Sustainable Use Licence blocked segment) | The best licensing-blocker story found and it still dies. The licence genuinely blocks embedding ("You may distribute the software or provide it to others only if you do so free of charge for non-commercial purposes"), n8n charges ~$50K/yr for the OEM exemption, Activepieces Embed is "from $36k/year" talk-to-sales, and no self-serve mid-market embed tier exists — so the position test actually PASSED. Killed by the free OSS anchor instead: the Activepieces core is MIT Expat (23,888 stars, only `packages/ee/` separately licensed), so a SaaS vendor can legally embed it for $0; what the $36K gates is the SDK and support, not the legal right. Apache-2.0 peers too: sim 29,433 stars, kestra 27,853. Also far beyond a 2-week solo build |
| AGPL-free embedded analytics (the Metabase blocked segment) | Position test failed twice. The leader is not structurally blocked from serving the segment — Metabase sells the commercial exemption itself, published and self-serve, Pro at $575/mo + $12/user/mo with white-label embedding — so the AGPL is a deliberate upsell funnel, which makes any wedge a mere pricing gap. And apache/superset is Apache-2.0 at 74,310 stars, legally embeddable for free, with MIT evidence-dev at 6,862 |
| Embeddable e-signing without AGPL (the Documenso blocked segment) | Position test failed at step 1: Docuseal already sells the flat-priced self-serve developer version, Pro $20/user/mo including "API and Embedding" plus embedded signing at $0.20/completion, no sales call, with a dedicated document-signing-for-SaaS page and React embed components. SignWell and BoldSign also sell cheap self-serve e-sign APIs |
| India regulated rails (GST e-invoice / e-way bill / KYC-KYB verification APIs) | Screened 2026-08-19 as the "jurisdiction as advantage" inversion: being Indian is a credential foreigners cannot get, which should invert the round-4 killer. Both halves fail. Owning the moat is out: a GSP licence requires an Indian *company* in IT/BFSI with >= Rs 2 crore paid-up capital and Rs 5 crore average 3-year turnover, India-based servers, a scored sandbox demo (60% pass mark), and there is no open application batch in 2026 (62 GSPs empanelled). Reselling someone else's GSP leaves no moat. The layer above it fails the position test: Deepvue sells 150+ verification APIs self-serve pay-per-call with a free trial, volume tiers and "no commitments", and Sandbox.co.in publishes a transparent tax-API price page with a free start (Amazon and Tata as references); Surepass has 300+ APIs. The transparent developer-first slot is taken, and Indian ARPU makes the buyer arithmetic worse than USD markets |
| Walkthrough video rendering API | COGS test failed on both sides. Your unit cost is a browser session PLUS a video encode per minute, while the generic renderers already retail below that: Shotstack flat $0.20/min subscribed ($0.40 pay-as-you-go), resolution- and fps-independent, independently benchmarked at ~$0.10-0.84/min across vendors at 1080p. Remotion (which Yuvraj already uses in InstantDocs) is the free programmatic-video anchor and self-hosts on Lambda. App layer is saturated and cheap: Guidde $18/creator, Supademo $27, Arcade with the most generous free plan, plus Trupeer, Screen Studio, Capptivo, HowdyGo. Screened 2026-08-19. (Audit 2026-08-19: a trailing "only software, no moat" clause was struck as invalid reasoning; the COGS kill stands on its own) |
| Scraping / crawl API, Firecrawl AGPL wedge | The AGPL gap barely exists: using Firecrawl's hosted API or running it internally never triggers AGPL, only distributing modifications does, so the blocked-buyer segment is tiny. Free permissive anchor: Crawl4AI, Apache-2.0, ~68K stars, docker self-host with FastAPI server — "the cleanest architectural replacement, commercial-friendly license". Position also taken: `us/crw` already ships a drop-in Firecrawl-compatible REST API, vakra-dev/reader (Apache-2.0) self-tags "firecrawl-alternative", Spider.cloud owns the speed/transparent-billing slot. Screened 2026-08-19 |

## Alive, small incumbents, correct shape

| Idea | Who is there | Note |
|---|---|---|
| **Content-gap detection and article drafting for the non-Intercom/Zendesk helpdesk tail** (Freshdesk, Help Scout, Gorgias, Front) | My AskAI from $199/mo flat with a 30-day no-sales-call trial, claiming knowledge-gap detection (its own marketing). eesel AI at $0.40/ticket handled, integrating Zendesk, Freshdesk, Gorgias, Front, Help Scout, HubSpot and Jira SM — but gap reporting is absent from its pricing page; it sells a ticket-handling agent. Forethought upmarket, no public pricing | **The first candidate to survive in 35 screenings, and it survives specifically because of the corrected reading of kill test 1: the position is occupied by small competitors rather than given away by a platform owner.** Unlike Intercom (Fin content-gap recommendations with drafted articles) and Zendesk (Knowledge Builder, after retiring Content Cues), Freshdesk and Help Scout do NOT ship this well: Freddy trains on past tickets only on the Business plan and "doesn't offer automated self-learning or knowledge gap detection", and Help Scout's AI Answers has no gap reporting and the KB has zero article version control. Both existing third parties sell the whole AI agent with gap detection as a side feature, so nobody sells the gap-analysis job standalone. **Open risks, all real: (1) trajectory — Intercom and Zendesk both shipped this natively, so Freshdesk and Help Scout plausibly follow, which would end it; (2) it may be a feature rather than a product, since buyers may prefer buying one agent that also deflects tickets; (3) cheap buyer base (Help Scout Standard is $25/user/mo), so test whether they will pay $50-200/mo for analysis that does not itself answer tickets; (4) SEO head terms are owned by Zendesk, Intercom, eesel and Forethought content marketing.** Next step is stage 6, not code: talk to support leads at Freshdesk/Help Scout shops. Founder-market fit is strong (he built the KB layer of an AI-native support platform) |

## Pending, blocked on a named test

| Idea | What is there | Blocking test |
|---|---|---|
| ~~COI endorsement + mid-term cancellation verification~~ RESOLVED TO DEAD, see the dead table. Kept here only to record what the pending entry said before its blocking tests were run | The sliver found while killing COI parsing. Two specific failures are stated openly in the buyer-facing literature: cheap tiers "lack automated verification with insurance carriers... advanced compliance monitoring that catches policy cancellations", so "if a vendor submits a valid certificate in January and their policy is cancelled in March, a document-based tool will continue showing it as compliant until the expiration date"; and what separates platforms is whether AI review "goes beyond surface extraction" to verify endorsements (CG 20 10, CG 20 37, Additional Insured, Primary & Noncontributory, Waivers of Subrogation) **against the actual contract requirements**. Buyers demonstrably pay: bcs $11.40/vendor/yr self-serve, CertFocus $6-8, full-service $13-30/vendor/yr with a $10,000 floor at bcs, myCOI $200-400/mo, and subs are charged $500-5,000/yr on legacy networks | **Blocking test not run: whether the cancellation half requires carrier data connections.** Certificial already sells a bi-directional "real-time, source-verified" insurance API, which is the carrier-connected version and would be the killer if carrier data is required. The endorsement-versus-contract half needs no carrier feed and may stand alone. Also unrun: whether bcs/CertFocus AI review already covers endorsement matching, since both include AI certificate review at every tier |
| ~~Ground-only dangerous goods (49 CFR, ADR)~~ RESOLVED TO DEAD, see below. Kept to show the test that closed it | Re-opened by the 2026-08-19 audit: originally killed alongside the air/IATA half partly because "a 49-CFR-only API is then pure software plus a PDF parse", which is no longer a valid killer. The data really is free and machine-readable: 49 CFR 172.101 via the eCFR versioner API and GovInfo bulk data, plus a parseable ADR Table A derivative (the `l10n-eu-product-adr` Odoo module built from a cepa.be spreadsheet). No mature OSS anchor was found. The only self-serve rival found was Moaah at $36/mo, and that is an HS/regulations lookup rather than a DG shipping-paper engine | **Position test never run for a cheap self-serve ground-DG product** (the screening stopped at the IATA licence). Also unresolved and possibly fatal on their own: product liability for getting a hazmat classification wrong, which a solo founder in India cannot underwrite, and whether the buyer is ever a developer with a card rather than a compliance manager buying through procurement |

Everything else has been resolved to a verdict.

## Round 2026-08-19e: first round run under the corrected gate. Five screened, five dead

Targets were selected by founder-market fit (support, KB, AI-docs) as the corrected method requires, the
moat gate was not applied, and the position test ran first. Results: help-centre content-gap detection,
answer-engine citation tracking for docs, per-customer AI cost attribution, plus the two resolved pendings
(COI endorsement verification, which lost both blocking tests, and it is now dead). Zero survivors, again.

**What this round proves, and it is the useful part: removing the moat gate was necessary but not
sufficient.** Four of the five died to a platform owner or a free tier giving the capability away, which
the corrected gate still treats as fatal and correctly so. Intercom ships content-gap detection with
AI-drafted articles inside Fin; Helicone ships per-user cost attribution in one line of headers; Google
Search Console and Cloudflare both shipped free AI-citation and AI-crawler reporting in 2026; Certificial
holds 25,000 agency feeds. None of that is a pricing gap you can undercut.

The pattern across 35 screenings is now unambiguous and it is a statement about the method, not the
markets: **screening ideas found by search cannot produce a candidate, because the same search produces
the same shortlist for everyone, and the platform owners reach every adjacent feature first.** The next
round should not be another five targets. See SKILL.md kill test 1 for the corrected reading of an
occupied position, and traps 9 and 10.

## Audit 2026-08-19: what the corrected moat rule did and did not change

The moat gate was demoted to a tiebreaker in SKILL.md, so every dead entry above was re-read to check
whether that rule was its *only* killer. **Exactly one qualified**, the ground-only DG variant, now
pending above. Nothing else was removed, and that is the finding rather than an omission: the dead
entries died at the position test, the access test, a free anchor, a giant, or COGS, and every one of
those kills is independent of the moat rule. Deleting them would only guarantee someone re-runs the
search later, which is the whole thing this file exists to prevent.

Two entries carried moat reasoning as decoration rather than as the killer, and that reasoning was
struck in place while the entry stayed dead: walkthrough video rendering (COGS kill stands) and SaaS
pricing history (position and arithmetic kills stand).

The bad rule's real cost was in target *selection*, not screening. It aimed four rounds at licensed
data, regulated rails and gated integration estates, which is precisely where a solo founder without
local presence is refused at the door. That cost shows up as the shots never taken, and no ledger edit
can recover it. The next round should be selected under the corrected gate instead.

## Session 2026-08-19c notes

Sources this session: harness WebSearch and WebFetch both work (server-side, unaffected by the
machine-level blocks recorded earlier), plus GitHub API by stars. Not checked: G2/Capterra 1-3 star
review bodies, Reddit threads directly, keyword volumes. All four kills above rest on position/free-anchor/
giant evidence from vendor pages and search snippets, which is first-hand enough; complaint mining was not
the deciding factor for any of them.

Recurring killer, now 6 of the last 7 screens: the flat-priced or self-serve slot was already taken by a
small incumbent (GlitchTip, Bugsink, Unipile, Skribby, DPP-Tool, e-invoice.be, Inbox Radar, Unspam). The
gap between "big players leave a pricing/DX gap" and "someone small already filled it" is closing in
roughly every market reachable by search. Next round should weight displacement events and licensing
blockers over pricing gaps, and screen the position test FIRST since it is what kills.

Superseded in part by the 2026-08-19d round: displacement events and licensing blockers were both
weighted heavily and both produced zero survivors (nine live displacements, three licence blockers, all
dead). The position-test-first advice held up and is now rule 1 of the kill tests. The revised advice is
in SKILL.md traps 9 and 10: expect the position test to fail, and select targets by founder-market fit
because the search-discoverable niche is saturated.

## Round 2026-08-20: parallel screening, 15 ideas across 6 agents

Targets picked by founder-market fit (support ops, KB/docs infrastructure, AI-agent operations, plus two
deliberately search-poor buyer clusters), not by search. Position test run first in every case. Verdicts
below; the three survivors are in the alive table and carry their verification status.

**The methodological finding of this round: a verification pass flipped the first two survivors from ALIVE
to DEAD, 2 for 2.** Both flips came from evidence the first pass could not reach: a sales-gated competitor
whose actual capability is visible only in its marketing detail (Pageloop), and a 2026 platform-owner
release (Intercom Fin Operator). **A first-pass ALIVE now means "not yet killed", not "live". Verify every
survivor against those two patterns specifically before acting on it.** A second cause of bad first passes:
two agents concluded WebSearch/WebFetch were unavailable and fell back to curl, producing screenings with no
SERP evidence at all. The tools work; their schemas must be loaded first.

### Dead

| Idea | Killer |
|---|---|
| Documentation / help-centre screenshot and UI staleness detection | Survived the first pass, killed on verification. **Pageloop sells the exact wedge**: text-level detection driven off release notes and PRDs ("Keyword searches can only catch some articles"), operating on a help centre it did not author ("works on top of your existing help center", "No switching needed"), across Zendesk, Intercom, Freshdesk, Help Scout, Mintlify, GitBook and ReadMe, and it also flags screenshots when UI changes. Sales-gated by KB size, which is why the first pass missed it. LaunchBrightly was correctly read (pixel-only, recipe-bound, Free/$229/$499 self-serve) but was the wrong competitor to check. Second independent killer: Intercom shipped **Fin Operator**, whose change-impact scan runs "when a product change, policy update, or pricing change comes through" and "searches the knowledge base, surfaces the relevant content, and proposes the updates" (Pro add-on) — and Intercom's Senior Knowledge Manager pointed complaining customers at it inside the very thread that was this idea's buyer evidence. Also in-market: HappySupport self-serve EUR 129/399/899, Swifteq EUR 89/mo. **Worth remembering: the buyer evidence was excellent and the demand is real** (HN item 47908051 at 489 points, "The users WILL DEFINITELY notice if the screenshots don't match what they have in front of their eyes"; GitLab issue 540572; four distinct non-engineer docs teams complaining on one Intercom thread). The pain is real, the slot is taken |
| AI resolution-billing reconciliation and audit (per-resolution billing for Fin/Zendesk/Agentforce) | Survived the first pass, killed on verification: **the platforms engineered the variance away**. Zendesk's resolution tiers (2026-05-18) mean silence no longer auto-bills — after "a 72-hour window with no customer follow-up", "a verification process is performed by a large language model (LLM) that evaluates the text of the conversation", and a failure becomes a Contained resolution which "does not count against your resolution allowance"; Zendesk also ships a free per-conversation resolution icon and an Automated resolution panel explaining why it counted. Intercom's terms now state "You will never be charged for an outcome that didn't happen", with reopens deducted across billing periods and the 2026-03-12 change from resolutions to outcomes. Salesforce offers turn-by-turn transcripts on dispute. The recurring slot IS open (TareCount is confirmed one-off consulting: "Full audit + negotiation evidence pack — $2,500 flat", one billing month, no renewals) but it is open because the problem is closing. Complaint volume is thin: 7-8 identifiable customers total, skewed to 2024-2025 Zendesk complaints about the defect since fixed. Buyer pool was NOT the killer — Fin at ~8,000 businesses and $100M+ ARR implies order of 2,000-4,000 companies above the $1,000/mo threshold. **Correction to an earlier claim in this round: Supportman does NOT sell a "Fin Audit"; its $25/$50/$100 tiers buy Slack CSAT alerts, IQS scoring and approvals** |
| Multilingual help-centre translation drift | Contract test. Zendesk's Help Center API ships `outdated=true` on the article-translations endpoint plus per-locale `updated_at`, so detection is an afternoon's work on a documented first-party field. Re-translation is simultaneously free from the platform (Zendesk AI translations on by default) and commoditised (Swifteq EUR 79/mo, TranslateDesk "$79 for 100 translations", Crowdin's Zendesk Guide connector with daily scheduled sync). No non-vendor human complaint found in the sources checked — every pain statement located was written by someone selling the fix |
| Help-centre health auditing (link rot, orphans, duplicates) | Three stacked anchors. Free in-market: Swifteq's Help Center Export is free and already emits broken links and images per article. Mature OSS: lychee 3,845 stars Apache-2.0, broken-link-checker 2,077 MIT, linkinator 1,250 MIT, plus Screaming Frog's free 500-URL tier for 404s and near-duplicates. Platform owners bundle it: Document360 "Links status", KnowledgeOwl "Broken link checker". The residual Zendesk-only slice is Swifteq at EUR 69/mo, and the author of the flagship complaint replied in 2024 that it "does the job very nicely". Demand signal is 27 likes in 5.5 years. Narrow sub-slice NOT conclusively dead: in-app deep links into SPAs that return 200 with an error screen defeat every link checker listed — real, but too narrow to be a product |
| Support-to-engineering escalation loop closure | Platform owners ship it free. Zendesk Support for Jira is free with 13,052 installs, no paid tiers, on every Support/Suite plan, and its post function "can change the ticket status, add an internal or public comment" on all linked tickets when the issue hits Done. Linear: "Automate updates to Zendesk tickets when their related Linear issues are closed… will also re-open the ticket." Duplicate-escalation counting is native. Savio ($39-249 self-serve, nav item literally "Close the Loop") and Canny (free tier plus $79) own the term. Zendesk community demand is feeble: 8 votes on the top related post |
| Knowledge and AI-agent config change management (versioning, approval, rollback) | Platform owner shipped exact parity free on 2026-04-24: Intercom's "See who changed what and when, add notes to explain why, and restore a previous version if something goes wrong", plus Procedure Draft/Live staging with version history and restore. Independently fatal on access: no third party can gate a publish inside Intercom or Zendesk. The one live gap (Zendesk QA AI config versioning) is a 9-upvote idea Zendesk has already marked Under review |
| Production answer-quality monitoring on live AI-agent traffic | It is the dead AI-agent-QA entry relabelled. Intercom Monitors "continuously evaluate every conversation that matches your criteria", with Custom Scorecards "Evaluated using AI" and a named use case of tracking conversations tied to a launch or product change, free with Fin, docs updated 2026-06-11. Zendesk sells QA for AI agents as a product line. Supportman already sells "AI Evaluation on every closed conversation" at $50/mo. Moving evaluation from pre-release to production changes the trigger, not the product, the buyer, or the vendor set |
| Code-sample / quickstart verification for API documentation | Free anchors end to end, and the paying segment left the problem behind. The language platforms ship it: Python `doctest` is stdlib, `cargo test` runs Rust doc examples by default, Go runs Example functions under `go test`, JDK 18 ships Javadoc `@snippet`. OSS: doc-detective 129 stars AGPL-3.0, Docploy free GitHub Action. The segment rich enough to pay moved to spec-generated SDKs where snippets cannot drift (Speakeasy's Code Samples API feeds Mintlify directly; Stainless and Fern do the same via `x-codeSamples`); Twilio, MongoDB and Stripe built it in-house years ago. No commercial vendor sells it at any price, and the reason is that every complaint found comes from a docs *consumer*, never a docs *owner* with a budget. Does not collapse into the dead API-deprecation entry — different mechanism, its own killers |
| Demo / sandbox data seeding for B2B SaaS trials and demos | **Snaplet already was this idea and died**: YC-backed 2021-2024, `@snaplet/seed` generated realistic data from your schema with real Postgres/Supabase traction, hosted cutoff 2024-08-31, tools open-sourced, team joined Supabase — which now maintains and gives it away (`supabase-community/seed`). The market is a barbell with nothing in the middle: Seedfast $0/$16/$69 self-serve at one end; Demostack ~$55K/yr, Saleo $120K+/yr, TestBox $44,750/yr sales-only at the other. The paying end needs SOC 2, a US GTM motion and implementation services, the worst access profile for a solo founder in India, and the "coherent narrative" that makes demo data valuable is customer-schema-specific implementation work, which is why those vendors staff CSMs against it |
| Support-facing customer context / account timeline sidebar for the helpdesk tail | All four target platforms ship the capability free on every paid plan: Help Scout Dynamic Apps (paste a callback URL and secret, official free `helpscout/app-template` starter), Gorgias's drag-and-drop no-code sidebar editor from $10/mo, Freshdesk Custom Apps "free to build, publish, and run", and Front's Plugin SDK, which now publishes an AI prompt file that scaffolds a working plugin "in ten minutes or less". Separately, every SaaS a support team already pays for hosts its own free Help Scout callback (Userlist, Freemius, 100+ native integrations). A developer documented building the Stripe-to-Help-Scout sidebar himself: "The integration process is surprisingly simple, yet very flexible since you can render whatever data and HTML that you wish." No independent buyer complaint found in the sources checked |
| Billable support-time reconciliation for outsourced agencies | Two independent killers. PSA side: HaloPSA tracks prepaid block drawdown in real time, alerts on low balance and auto-generates the top-up invoice at a percentage threshold; Autotask has a Block Hour Contract type; ConnectWise has amount-based agreements. That is the entire feature list, already paid for. Helpdesk side: Zendesk's Time Tracking app is first-party and included on Suite Growth and above; Clockify and Jibble are free forever; Harvest is $9/seat and closes ticket-to-invoice; TimeCamp does per-client rates, budgets and invoices from a Marketplace app. The residual per-ticket-count wedge ("client is at 380 of 400 tickets on the 22nd") is a saved view plus a threshold, a one-day build |
| Multi-client / multi-brand knowledge-base management for agencies | Three killers. Platform owners give it away: Zendesk Suite Enterprise includes 300 brands and 300 help centres with per-brand branding and domains; Freshdesk Multiple Products gives unlimited branded portals on Enterprise "without paying for extra licenses". Already shipping: Docsie Enterprise Portals from $350/mo sells "unlimited tenants/portals", "white-label ready — custom branding, domains and styling for each portal", centrally managed, reusable content blocks and analytics for "version drift" — both claimed differentiators; HelpSite is $45-90/mo flat for 5-25 branded sites and markets to agencies explicitly. And the one genuinely uncovered feature, cross-platform propagation of a shared procedure, is read-canonical-diff-against-N-APIs-and-push, which is the dead KB migration/sync entry with new marketing |

### Sources and gaps for this round

Working: WebSearch and WebFetch (when their schemas are loaded), HN Algolia full-text API, GitHub search
API by stars, direct vendor pricing-page fetches, and the Zendesk Gather community API, Zendesk Help Center
article-search API and Atlassian Marketplace REST API, all of which proved to be rich seams.

Blocked or unchecked, and every verdict above should be read with these in mind: Reddit JSON, direct
Google/Bing/DuckDuckGo queries, G2 and Capterra review bodies, all keyword-volume tools, and the entire
Zendesk Marketplace (`www.zendesk.com/apps/*`, Cloudflare). **No keyword-volume evidence exists anywhere in
this round**, so every SEO judgement is a count of who is visibly farming the term, not a volume estimate.

### Round 2026-08-20, cluster E (privacy and data governance in support tooling), additional dead entry

| Idea | Killer |
|---|---|
| AI-agent conversation data governance (what the agent sent to which model provider, auditable record for security questionnaires) | The AI support vendor is the platform owner and gives the whole answer packet away free. trust.intercom.com supplies SOC 2 Type II, ISO 27001/27701/27018/42001, HIPAA, HDS, AIUC-1 with quarterly adversarial testing, CSA CAIQ, pen-test summaries, the DPA, an EU AI Act overview and the subprocessor list naming OpenAI, Anthropic and Google, and states LLM providers do not train on customer data plus "detailed logging of all LLM interactions". The SMB forwards the link; the questionnaire is answered in minutes by the vendor whose name is on it. Self-built agents are covered free by OSS: langfuse 33,426 stars (self-hostable tracing, prompt management, evals) and BerriAI/litellm 56,795 (gateway with cost tracking, guardrails, logging across 100+ providers), plus Presidio 10,549 MIT for prompt-side PII — which also trips the contract test, since the buyer's engineer puts LiteLLM in front of the agent in an afternoon and has the log. Compounding and specific to this founder: the deliverable IS compliance evidence, so an unaudited solo vendor with no SOC 2 cannot sell it — this is the one idea in the cluster where structural unsellability genuinely bites. **Zero verbatim buyer complaints found in any source checked; every page ranking on the topic is vendor content, so the demand signal is vendor-manufactured** |

## Round 2026-08-20: five candidates left UNVERIFIED — read this before acting on any of them

Three verification agents (E1+E2, B1+B3, F1) were launched and **all three died on an account spend-limit
error, not on findings**. The five candidates below therefore carry only a first-pass verdict. Given that
verification flipped the first two survivors of this round from ALIVE to DEAD (2 for 2), **a first-pass
ALIVE here means "not yet killed", and none of these should be treated as live until verified.**

Partial verification WAS completed by hand on E1/E2 via direct vendor fetches (WebSearch/WebFetch were not
in the session tool registry by this point; curl to vendor pages works, Zendesk help-center APIs return 401,
zendesk.com/marketplace 403s). What it found, and it matters:

**GrowthDot has grown well beyond how the screening described it.** Fetched 2026-08-20 from
growthdot.com/gdpr-compliance-for-zendesk: it now markets "The Complete GDPR Compliance Platform for
Zendesk — Retrieve personal data, anonymize sensitive information, redact attachments, delete records,
automate recurring compliance tasks, and maintain a complete audit trail—all without leaving Zendesk."
Pricing is flat per tenant, not per agent: **Standard $50 and Premium $65 per Subdomain per month**
($41.70/$54.20 annual), self-serve trial, "No credit card required · Free forever on Sandbox accounts".
Premium's comparison table includes **"Redact Attachments by Type"**, "Export tickets with attachments",
Automations, scheduling, bulk anonymization, organization-level deletion, agent permission control and
reports. **This directly occupies E2's claimed primary wedge (attachments) at $65 flat**, and covers much
of E1's audit-trail and automation story too. Unresolved: whether "by Type" means content-aware redaction
or delete-by-filetype, and whether GrowthDot or Sparkly reach Chat, Talk, Guide, side conversations and AI
agent logs — no mention of any of those was found on the page, which is the one thread E1 still hangs on.
Note also that **sparkly.app is a parked domain for sale**, so the Sparkly vendor identity, install count
and $99/$249 pricing in the E1 screening are UNCONFIRMED and were never verified against a live vendor site.

| Candidate | First-pass verdict | The single test that decides it |
|---|---|---|
| E1 DSAR / right-to-erasure execution across support tooling | ALIVE, narrowed to Zendesk-only and in-platform | Does GrowthDot ($50/$65 flat) or Sparkly already fan out across Support + Guide + Chat + Talk + side conversations + AI agent logs with an audit trail? If yes, dead. Also: verify Sparkly exists as described |
| E2 PII redaction / retention in support conversations | ALIVE, wedge = attachments, retroactive backfill, audit dashboard | **Already dented by hand-verification**: GrowthDot Premium sells "Redact Attachments by Type" at $65/subdomain/mo flat. Remaining wedge is content-aware OCR redaction and retroactive backfill over closed tickets. Also unchecked: Strac's real price (sales-gated), Help Scout's native Comprehend masking GA status |
| B1 Zendesk macro / canned-response hygiene | ALIVE | Pythia Advanced Macros' actual scope and price (never read, Cloudflare-blocked); whether Zendesk shipped macro analytics or AI macro consolidation in 2025-26; whether the 30-day usage-history cap still holds |
| B3 Conversation QA for small support teams (3-20 agents) | ALIVE, strongest of its cluster | Whether ANY self-serve sub-$50/agent QA vendor exists (the whole thesis is that none does), and whether Intercom/Front/Help Scout/Freshdesk ship native QA. Demand side has NO verbatim complaint and no SEO data at all |
| F1 Cross-client SLA reporting for outsourced support agencies | ALIVE, weakest | Buyer pool is unmeasured and ZERO verbatim agency-owner complaints were found. Needs 20 outbound conversations, not more desk research |

**Method note for the next session.** This round's real lesson is not about any one idea: it is that the
first-pass/verification split is worth institutionalising. Cheap parallel first passes generate candidates;
a second pass hunting specifically for (a) sales-gated competitors whose capability hides in their docs and
(b) 2026 platform-owner releases is what produces a trustworthy verdict, and it overturned two of two.
A secondary lesson: two agents wrongly concluded WebSearch/WebFetch were unavailable and fell back to curl,
producing screenings with no SERP evidence — always confirm the tools are loaded before trusting a round.

### Round 2026-08-20: B1 and B3 verified, both DEAD. Verification now 4 for 4 in overturning first passes

| Idea | Killer |
|---|---|
| Zendesk macro / canned-response hygiene auditing | Three independent killers. **Pythia "Macros Reporting and Management"** (Marketplace app 270376, 100+ installs) sells the wedge verbatim — "Manage, audit, and improve your Zendesk macros", "Unused and underused macro identification", "Quick Audit links to active macros unused in the previous 30 days", last-used dates, bulk activate/deactivate/delete/label, "Persistent history and versioning", "Actor and source attribution" — **flat and self-serve at $19/mo Essential and $29/mo Pro, 14-day trial no credit card, SOC 2 Type 2**, i.e. below the price this idea needed to charge (volume slider scales it up, so $19/$29 is the entry tier). It also already solved the claimed technical wedge, the 30-day usage cap, by accumulating prospectively: "History is prospective. Tracking starts after installation, connection, and the first library synchronization." **Second killer: Zendesk shipped native macro content suggestions on 2026-04-30** — Copilot Recommendations that "analyze how your agents resolve tickets and propose concrete edits to existing macros or suggest new ones based on actual ticket data", replacing the legacy Suggestions tab (Copilot add-on). **Third: the niche is crowded and Zendesk promotes the rivals** — Macro Hero at $49.99/mo flat self-serve ("Bulk search, edit, toggle, and rank hundreds of macros", usage ranking, find-and-replace), Configly (free app, Solo from GBP 99/mo, flags "macros nobody uses"), ConfigMap, and Swifteq has moved macro full-text search into Advanced Search Plus at EUR 59/mo. The 30-day cap was independently VERIFIED as real, it just no longer creates a gap. SEO is unwinnable: Pythia's Marketplace listings, Zendesk's own help centre, Salto and eesel AI's programmatic content farm own the terms. Residual sliver, genuinely unoccupied: contradiction detection between macro bodies and the knowledge base ("this macro says 30-day returns, your KB says 14") plus dead-link checking inside macros — real, in Yuvraj's wheelhouse, but a one-sprint feature for Pythia and downstream of an integration surface Pythia already owns |
| Conversation QA / scorecards for small support teams (3-20 agents) | **Intercom shipped it natively and flat-priced, killing the entire thesis.** Monitors plus Custom Scorecards on the Pro add-on: "evaluate and improve the quality of your teammates' conversations at scale", criteria AI-scored or human-scored and mixed on one scorecard, weights 0-100, critical flags, pass thresholds, 90-day backfill, 20 live Monitors per workspace. Price: **"The Pro add-on costs $99 per month for up to 1,000 conversations"**, billed per conversation not per seat, with overage $0.12/$0.10/$0.06, and explicitly **"Reviewing more teammates costs nothing extra"** with "no additional per-conversation charge" for AI scoring. Grandfathering ended 2026-05-12, so it is live and being charged for. The candidate's whole thesis was that per-seat pricing locked small teams out; the platform owner removed per-seat pricing. The no-self-serve finding about the pure-plays HELD UP on fresh checking (Scorebuddy all three tiers "Request a price"; MaestroQA rebranded to Rippit March 2026, still custom; Intryc sales-gated; Oversai self-serve but "$500/month platform fee"; Zendesk QA ~$35/agent/mo per third-party analyses = $350/mo for a 10-agent team vs Intercom's $99 flat) — it simply stopped mattering, because the gap was a distribution gap and the platform owner closed it from the inside. **Compounding kill: zero verbatim demand evidence after a targeted search.** Every "small teams and spreadsheet QA" artifact is a lead magnet published by a QA vendor (Scorebuddy, Kaizo, The CX Team), which inverts the signal — wide circulation of those templates is evidence of vendor content marketing, not unmet demand. Buyer arithmetic also says QA is structurally an above-30-agent practice: the category's $30-125/agent/mo annual-contract architecture only amortises over a headcount big enough for a dedicated reviewer, and a 10-agent team's lead reviews a handful of tickets by hand. OSS anchor genuinely absent (only AI-agent eval tools, no human-agent scorecard project), and SEO is one of the most heavily farmed comparison-keyword sets in support ops. Residual cell, unoccupied but not a business: flat-priced self-serve QA for Help Scout / Front / Gorgias / Freshdesk teams of 3-20 agents — dead because Intercom just set the public reference price at $99 flat, because removing Zendesk and Intercom removes most buyers who run a QA programme at all, and because the ALIVE rating rested entirely on inferring an unserved buyer from vendor pricing pages, which is the exact inference that failed on the sibling candidates |

**Verification is now 4 for 4 in overturning first-pass survivors** (screenshot staleness, AI-billing
reconciliation, macro hygiene, small-team QA). Every flip came from one of the two named patterns: a
sales-opaque vendor whose real capability is visible only in its own product pages, or a 2026
platform-owner release. This is no longer a caution, it is the base rate: **treat a first-pass ALIVE as
"not yet killed" and budget a verification pass for every survivor before spending a day on it.**

A pattern worth naming across B3 and several earlier kills: **inferring an unserved buyer from vendor
pricing pages ("nobody sells self-serve, therefore small teams are shut out") is not demand evidence.**
Three candidates have now died where the only support was that inference. Demand evidence means a dated
complaint from a named non-vendor, like B1's 125-vote Zendesk request or the 489-point HN screenshot
thread. Where the only artifacts are vendor lead magnets, the signal is inverted.

### 2026-08-20 final: E1 verified — the FIRST CONFIRMED ALIVE in 50 screenings

**DSAR / right-to-erasure execution across Zendesk products (one erasure request, fanned out across
Support + Chat + Talk + Guide + community + AI agents, with an audit trail).** Verification hunted
specifically for both session killers and neither fired.

- Sparkly is real (Amsterdam, apps.sparkly.dev; Marketplace app 206749 "GDPR Search & Destroy", 100+
  installs, 36 reviews, updated 2025-11-12, $99/$249 flat/mo) but is a **delete-only bulk engine driven by
  Support search queries — "Works with: Support"**. No redaction, no retrieval, no other products. Its
  architecture quote is the model to copy: "The app installs inside your Zendesk, and none of the data
  will actually leave Zendesk at any point."
- GrowthDot ($50/$65 flat) also never leaves Support: its April 2026 changelog (54 features) touches Chat
  only as ticket-attached transcripts; Talk, Guide, community, side conversations, AI agents all absent.
- Zendesk's native fan-out covers only the identity row ("Deleting the user in Support also deletes the
  user in Guide, Chat (for agents), Message, Talk, and Explore") while its CURRENT docs state: "deleting
  an end user in Support doesn't delete the end user's visitor profile in Chat"; Guide needs manual
  archive-then-delete ("Simply editing the article to remove the personal data is not enough" — revision
  history); "There's no way to redact information in conversations of closed tickets"; six per-product
  compliance articles; a separate AI agents Delete User Data API that does not remove trained expressions.
  ADPP is Enterprise-gated retention, not per-subject fan-out.

Corrections: Explore caches 24h not 90d; the 2020 side-conversation quote is STALE (Zendesk shipped
side-conversation redaction for email/child ticket/Teams) — the gap rests on current docs now, do not
reuse the old quotes. Buyers pay $50-249 flat, twice proven. Distribution is the Zendesk Marketplace
category, not SEO (head terms owned by support.zendesk.com, long tail farmed by eesel AI; Sparkly built
100+ installs with no content operation).

**Open risks:** (1) technical, decisive, half-a-day to check: can a ZAF in-Zendesk app reach Chat visitor
profiles, Guide revision history, community comments, Talk recordings and the AI agents API without an
external server? Losing "no data leaves Zendesk" loses the only answer to having no SOC 2. (2) Both
incumbents stayed in Support; possibly because Support holds ~95% of the personal data — only buyer
conversations resolve that. Unchecked: Slack side-conversation coverage, knots.io, G2 bodies, Sunshine
Conversations, the June/July 2026 Service Data Deletion Policy revision.

**Next step: the ZAF feasibility check, then 20 outreach emails. Not more screening.**

## Method change 2026-08-20: SKILL.md rewritten from scratch

The old skill (kill-test chain, ~2,900 words, three layers of rule corrections) was audited against its
own record — 50 screenings, 1 survivor, 4/4 first-pass survivors flipped on verification — plus outside
references (Rob Walling's "data points, not deal breakers" framing; Strebulaev's funnel base rates showing
a cheapest-stage filter should pass ~30%, and "if the successful deals in your space never survive your
funnel, something serious is off"; the Mom Test evidence hierarchy; Anthropic's skill-authoring guidance
that layered rule-corrections bias a model toward the most conservative reading, i.e. toward KILL).

What changed: kill tests became three hard gates (platform-owner shipped-and-adequate, structural COGS,
access) plus a six-dimension scorecard; verdicts are now KILL / WEAK / WORTH A CHEAP TEST and desk research
can no longer emit "confirmed live"; the verification pass (competitor product docs not pricing pages,
current-year platform releases, refutation framing, evidence re-basing) is a mandatory stage before any
survivor is named; demand evidence is graded on the Mom Test hierarchy with vendor content as inverted
signal and pricing-page inference banned; SEO failure is no longer fatal (distribution scored as a whole —
Sparkly's 100+ installs came from the marketplace category with no content operation); one survivor ends
the round; a 10+ batch with zero survivors flags the filter; kills get a 6-12 month anti-portfolio review.
The old file's full text is in ~/.claude git history. Verdicts in this ledger stand unchanged — the audit
found the kills individually sound; the flaws were sourcing, gate structure, and accumulated contradictions.

## Round 2026-08-20b: first round under the contractual support exclusion. Three screened, three dead

The round opened on support-domain targets (helpdesk backup/restore, Zendesk community-request mining) and
those were abandoned mid-research when the exclusion was stated, so they carry no verdict. Three
non-support targets were screened.

| Idea | Killer |
|---|---|
| Custom-domain / vanity-domain onboarding for multi-tenant SaaS (cert issuance, DNS verification, per-tenant routing) | Gate 1 twice plus buyer arithmetic. Platform owner: Cloudflare for SaaS sells custom hostnames with hostname validation, delegated-TXT/HTTP DCV, zero-downtime migration, apex proxying and WAF for SaaS, documented at developers.cloudflare.com/cloudflare-for-platforms/cloudflare-for-saas (last updated 2026-04-29) with per-hostname pricing an order of magnitude under any app-layer price. Mature permissive OSS: caddyserver/caddy 75,041 stars Apache-2.0 does on-demand TLS in a few lines of config, traefik/traefik 64,505 MIT the same. Position and arithmetic: Approximated's own public pricing page (reviewed 2026-08-05) is **$0.20 per custom domain per month with a $20/month minimum below 100 domains**, self-serve, with a published facts.json and comparison pages against Cloudflare SSL for SaaS, the Vercel Platforms starter kit and "Building it yourself". A $20/mo incumbent floor means ~600 customers to reach $12K MRR. Self-hosted tiers exist at $199/mo and $4,999/mo but those buyers are enterprises with procurement, not a solo vendor's market |
| OAuth / hosted-auth layer for SaaS vendors exposing an MCP server to their customers | Gate 1, platform owners give it away and keep it current. cloudflare/workers-oauth-provider is MIT, 1,860 stars, last pushed 2026-08-19 (a day before screening) and implements the provider side for remote MCP servers; vercel/mcp-handler covers the same ground for Next.js; modelcontextprotocol/typescript-sdk (13,209 stars) ships the transport and auth plumbing in the reference SDK. agentic-community/mcp-gateway-registry (869, Apache-2.0) and tailscale/tsidp (652, BSD-3) cover the gateway and IdP variants. The paid field above that (Stytch, WorkOS, Descope, Auth0) is funded and sales-led, so the down-market slot is not empty, it is free |
| Outbound webhook delivery infrastructure for SaaS (retries, signing, per-tenant endpoints, replay) | Gate 1. svix/svix-webhooks is **MIT, 3,360 stars, pushed 2026-08-19** — the category incumbent is itself permissively licensed and self-hostable, and standard-webhooks (1,730, Apache-2.0) standardises the signing scheme it competes on. No price undercuts `docker run` |

**The structural finding of this round, which outranks the three verdicts.** Removing support removes the
only market the founder knows from the inside, and every axis left to him — edge/CDN and multi-tenant web
infrastructure, document and video generation, LLM application engineering — is *developer
infrastructure*. Developer infrastructure is the worst possible shape for this method's gates: it is where
mature permissive OSS is thickest, where the platform owners (Cloudflare, Vercel, AWS) ship the primitive
free, and where the buyer's engineer genuinely can build it in a day. All three kills above are the same
kill. Selecting more dev-infra targets will keep producing it.

**So the next round must select by BUYER ACCESS, not by technology.** The question to put to Yuvraj is not
"what can you build" but "whose business operations can you interview" — a vertical reachable through
people he knows in India, a trade he has proprietary sight of, an operation whose workflow the search
engine describes badly. Until that answer exists, further desk rounds on the permitted axes are predicted
to be wasted, and this prediction is recorded here so the next session can check it rather than repeat it.

**Sources for this round.** Working: direct vendor and docs page fetches, GitHub search API by stars with
licence and last-push, HN Algolia, the Zendesk Gather community API and Help Center article-search API
(both rich, both now unusable under the exclusion). **WebSearch and WebFetch could not be loaded at all
this session** — four different ToolSearch patterns returned nothing, and no deferred tool was
retrievable; treat the tooling check in SKILL.md as machine-dependent. Bing HTML via curl now returns
parseable results (a seam the ledger previously recorded as blocked) but is geo-localised to India and
returned dictionary and Indian-government noise for product queries, so it was not relied on. Unchecked:
Reddit, G2/Capterra bodies, keyword volumes, Approximated's actual customer count, whether any
non-dev-infra axis exists for this founder.

### Round 2026-08-20b continued: docs axis reopened once the exclusion was narrowed, two more dead

| Idea | Killer |
|---|---|
| OpenAPI spec-versus-runtime drift detection (does the published API reference still match the live API) | Gate 1, mature permissive OSS, shipped and adequate, and the contract test fails alongside it. schemathesis/schemathesis is MIT, 3,540 stars, **pushed 2026-08-20, the day of screening**, and property-tests a live API against its OpenAPI spec; stoplightio/prism 5,010 Apache-2.0 does validation-proxy conformance; apiaryio/dredd 4,222 MIT does spec-versus-implementation testing (unmaintained since 2024-05 but the job is covered twice over without it). Tufin/oasdiff and the OpenAPI spec repo (31,163) cover the diffing half. The buyer's engineer adds schemathesis to CI in an afternoon, which makes this a CI step rather than a product. Note in passing: opticdev/optic, the venture-funded commercial attempt at exactly this, is MIT and has not been pushed since 2026-01-08 — the one piece of evidence in the round that the market may not pay for it at all |
| Docs-to-integration funnel analytics (which documentation pages precede a successful versus failed first API call) | Position: the docs platform owners already join the two halves and put it on the free tier. **ReadMe's pricing page (fetched 2026-08-20) lists "Documentation metrics", a "Developer Dashboard", "Request History" with detailed logs and "Export request history" — on Starter at $0/month**, with extended history as a $100/mo add-on and Pro at $250/mo. The same free tier also carries Custom LLMs.txt, an MCP Server, a Broken Link Checker and Docs Audit, which independently closes the "make your docs AI-consumable" and "docs link rot" variants. Mintlify's Starter is likewise $0/mo with 5 editor seats, the full platform and analytics. Nothing is left for a third party to sell between a free docs platform that owns the pageview data and the customer's own API telemetry |

**What the docs axis adds to the round's structural finding.** Developer documentation turns out to have
the same shape as developer infrastructure, for a different reason: not one platform owner but five
well-funded ones (ReadMe, Mintlify, GitBook, Redocly, Fern) each shipping a broad free tier to win the
seat. Between generous free tiers above and MIT-licensed tooling below, the middle where a solo vendor
would charge $50/mo is thin by construction. Five ideas screened in this round, five dead, all to gate 1.
That is not yet the 10+ zero-survivor batch that should trigger a filter audit, but the *reason* is
identical every time, which is the more useful signal: the gates are working, the target selection is
wrong. Select by buyer access next round, per the note above.


## Round 2026-08-20c: four screened on non-dev-infra buyer-access targets, four dead

Deliberate response to round 2026-08-20b's recorded prediction (dev-infra and docs targets keep dying to
gate 1, so select by buyer access instead). Targets were chosen so the buyer is a business operator, not a
developer, while staying on the permitted axes: India-side operations, document generation, video
generation. It did not help. Same gates fired, plus a new dominant one: no graded demand evidence at all.

| Idea | Killer |
|---|---|
| GeM / government-tender bid-document assembly for Indian MSME sellers | Position and buyer arithmetic. The niche is already thick with self-serve AI entrants (Minaions, incl. a dedicated "GeM Portal Automation" page; QuickBid; BidIndia; ClearBid; SwishX for pharma tenders) and, below them, a large services layer that is the real incumbent — Tender18, TenderDekho, TendersPlus, skillcouncils all sell done-for-you GeM bidding as a service, which is what MSMEs actually buy. Indian MSME ARPU makes the $50+/mo buyer arithmetic worse than any USD market (the same kill as the India regulated-rails entry), and the deliverable shades into acting as a bidding agent, which is service capacity, not software. Zero verbatim buyer complaints found; every artifact on the topic is a vendor or agency blog, i.e. tier 6 inverted signal |
| Investor-update / portfolio-MIS report generation for startups and their VCs | Position taken at both ends and heavily funded. Founder side: Visible.vc, Paperstreet, Cabal, DocSend, Ellty all sell investor updates self-serve, with at least four comparison listicles enumerating 8-9 vendors. VC side: Standard Metrics, Affinity, PortfolioIQ, ChatFin all sell portfolio monitoring. Nothing between a funded founder-side tool and a funded VC-side tool for a solo vendor to charge $50/mo for. The only argument for this target was proprietary access via the 100X.VC network, which is access to a buyer pool, not a gap |
| Vernacular (Indian-language) dubbing and on-screen-text localization for edtech/coaching video libraries | Gate 2 plus position. Sarvam Dub sells AI dubbing across 11 Indian languages as a first-party Indian model provider, i.e. your supplier is also your competitor and sets the price floor. Above it the generic layer is saturated and cheap: Rask.ai, Fliki, Checksub, plus a listicle tail of 10+ tools. Per-minute media cost with a per-minute retail price set by model providers is the dead walkthrough-video-rendering COGS shape exactly |
| Digital work instructions / SOP + audit evidence for manufacturing SMEs | Gate 3 (access) is decisive, with position as backup. The top of the market is a field-implementation sale a solo founder in India cannot run: Dozuki ~$850/mo with a 50-user minimum (~$10,200/yr), VKS reportedly ~$350/user/mo, L2L $150/user/mo, Operations1 from EUR 10,000/yr plus EUR 3,000-50,000 implementation, Poka/Augmentir/Proceedix quote-only — and the same comparison puts typical implementation at $5,000-$100,000, which is the demo-data entry's killer restated (implementation services, the worst access profile available to him). The self-serve floor is simultaneously taken by funded vendors giving it away: Manual.to generates a free AI manual with no account and has no user minimum, Tulip ($120M Series D) ships a free plan covering work instructions via its no-code builder. Demand evidence is tier 6 throughout: the richest source found was manual.to's own pricing-comparison page, i.e. a vendor lead magnet, which inverts the signal |

**The finding that matters, and it is not about these four ideas.** Round 2026-08-20b predicted that further
desk rounds on the permitted axes would be wasted until a buyer-access answer exists, and asked for it. This
round tested whether *guessing* the buyer-access axis works instead. It does not: the four targets above were
selected by plausible buyer type rather than by a market Yuvraj can actually interview, and the tell is that
**not one of the four produced a single dated complaint from a named non-vendor.** Nine consecutive kills
now across 2026-08-20b and 2026-08-20c. That is at the base-rate threshold where SKILL.md says to audit the
filter, and the audit answer is already on record and unchanged: the gates are firing correctly, the target
selection is unsourced. Guessed buyer access is still search-derived sourcing wearing a different label.

**What has to happen before another round is worth running.** One question to Yuvraj, and it is not "what can
you build": *whose business operations can you get on a call this week?* Named people, a trade, a WhatsApp
group, ex-colleagues at Kroto customers, 100X.VC portfolio operators, anyone in Bareilly whose workflow he
has seen from the inside. Targets derived from that answer are the only kind this method has not tried.

### Sources for this round, and a recovered seam worth keeping

**Brave Search HTML via curl now works and returns parseable organic results** (`https://search.brave.com/search?q=`,
desktop UA, results inside `<div class="result-wrapper`). This is the first working general web-search seam
recorded on this machine and it replaces WebSearch for position tests. Parser kept at
`scratchpad/bs.py`; a tag-stripping page fetcher at `scratchpad/f.py`.

Also working: direct vendor page fetches, HN Algolia, GitHub search API by stars.
**Still broken: WebSearch and WebFetch could not be loaded — six ToolSearch patterns returned nothing, and
no deferred tool of any kind was retrievable (scrapling included). Second session in a row.** Bing returns
200 but no extractable organic links (JS-gated); Mojeek now serves a captcha; ecosia 403; r.jina.ai 403;
DuckDuckGo html returns 202 with a challenge. Unchecked this round: Reddit, G2/Capterra bodies, keyword
volumes, and any primary buyer conversation.

## Round 2026-08-20d: E1's shape transplanted to non-support platforms. Two dead, one WEAK

Reasoning behind target selection: the only candidate that ever survived verification (E1) had a specific
shape — a compliance action that must fan out across a fragmented product suite, with an audit trail, sold
through a marketplace category rather than SEO, flat-priced at $50-250/mo. That shape is not support-specific.
Three platforms with marketplaces and business (non-support) buyers were screened in it.

| Idea | Verdict and evidence |
|---|---|
| **D1 GDPR erasure / PII fan-out across Atlassian Cloud (Jira Software + Confluence)** | **WEAK — no hard gate fired, poor scorecard.** Gate 1 does NOT fire: Atlassian's own current GDPR doc still says free-form-text personal data must be found with "the product's global search feature and delete it on a case-by-case basis"; the native Cloud anonymization request **JRACLOUD-76571 has 105 votes, was opened 2021-05-06 and is still "Gathering Interest"**; CONFCLOUD-79383 (anonymize user references in Confluence pages, 2024-08-23) and ROVO-354 (masking/redaction in Rovo Chat, 11 votes, 2025-10-10) are also open. Atlassian Guard Premium ships content-scanning detection but is **sold, not given away, at $8.18/user/month** and only covers Jira and Confluence Cloud, so it is a trajectory risk rather than a fired gate. What sinks the scorecard is position plus founder fit. **Actonic (Actonic Products GmbH) already occupies most of the wedge**, cheaper: "Data Protection Toolkit: GDPR, PII & DLP" for Jira (305 cloud installs) and Confluence (158), priced per-user and tiered — free to 10 users, then $180/yr at 15 users, $600/yr at 50, $1,200/yr at 100, i.e. ~$50/mo at 50 users. Their Cloud docs (actonic.atlassian.net, space GDPRCLOUD) show the Data Cleaner module scoping by JQL/CQL, searching by selected user or regex across Comment, History, Reporter and Attachment name, with rules, event triggers and a clean/status history — that is the fan-out plus audit trail. They separately ship an **Attachment Scanner OCR for Jira** that reads images, scanned PDFs, screenshots, Office files and CSVs and deletes matching attachments on a credit model, which occupies the attachment-content wedge that survived on the Zendesk side. miniOrange sells PII Scanner (DLP) apps too (21 and 18 installs). Genuine residual: cross-product single-subject orchestration, Confluence page version history, attachment content on Confluence, and the new AI surfaces (Rovo). Thin. **Two things make this a WEAK rather than something to test: founder fit is near zero (he has no inside knowledge of Atlassian admin or compliance buyers — the GDPR-fanout expertise he has is Zendesk-specific), and the largest PII surface on Atlassian is Jira Service Management, which is customer support, so the contractual exclusion forces him to sell the weaker half of the market.** Scores: demand 1, position 1, founder fit 0, contract test 2, distribution 2, arithmetic 1 |
| D2 Google Workspace offboarding / user data lifecycle for IT admins | **KILL, gate 2 in the zero-marginal-cost direction, plus arithmetic.** Patronum's public pricing page (fetched 2026-08-20) sells Automated Onboarding and Offboarding, Drive management and Drive compliance at **$2.00 per user per YEAR** (Business tier $8.00/user/year), self-serve with a 30-day no-card trial. That is $0.17-$0.67 per user per month. At 100 seats a whole tenant pays $67-800 per year, so no price undercuts it and reaching $12K MRR would need thousands of tenants. GAT Labs sits alongside |
| D3 HubSpot data-subject erasure fan-out | **KILL, gate 1.** HubSpot ships the capability free in its core API: the CRM contacts reference documents a dedicated `gdpr-delete` endpoint (`/crm/v3/objects/contacts/gdpr-delete`) plus in-app permanent deletion, on the platform every buyer already pays for |

**What this round adds to the method.** Transplanting a proven shape onto a new platform is a legitimate
sourcing move and it did produce the first non-support candidate in twelve screenings where no hard gate
fired. But it also exposes the limit: the shape travels, the founder's inside knowledge does not. D1 fails
on exactly the dimension the skill calls the primary selector, and its best market segment is the one his
contract forbids. **Do not build D1. It is recorded so nobody re-runs the search, and so that if he ever
acquires an Atlassian-admin buyer channel it can be re-opened against one test: whether Actonic's Cloud
Data Cleaner reaches Confluence page version history and attachment content.**

### Sources for this round, with two new seams worth keeping

New and rich: the **Atlassian Marketplace REST API** for install counts and live cloud pricing
(`/rest/2/addons?text=`, `/rest/2/addons/{key}/pricing/cloud/live`), the **public Atlassian issue tracker**
`jira.atlassian.com/rest/api/2/search` with vote counts (the best measurable demand seam found since Zendesk
Gather, and it works for any Atlassian product), and **any vendor's public Confluence Cloud wiki** via
`/wiki/rest/api/content?spaceKey=&expand=body.storage`, which returns full documentation text and defeated
Actonic's JS-rendered marketing site. Marketplace listing descriptions are NOT available via the API
(returns empty) and the listing pages are a SPA, so use the vendor's own docs wiki instead.

Brave Search HTML works but **captchas after roughly eight queries per session**, so spend them on
discovery and use direct fetches for verification. WebSearch/WebFetch still unloadable. Unchecked this
round: Atlassian Community threads (Khoros, not fetched), G2 bodies, keyword volumes, Guard Detect's actual
redaction scope, and whether any Actonic customer complains about the per-product split.

## Method change 2026-08-20e: verdicts became 1-100 scores; tiered pipeline for volume

At Yuvraj's request SKILL.md was rewritten: every candidate now gets a 1-100 composite score (weights:
demand 25, position 20, founder fit 15, distribution 15, arithmetic 15, contract 10) instead of a
categorical verdict. The hard gates survive as score caps, not as averaged-in dimensions: a fired gate
caps at 5, and no candidate may score 70+ before the verification pass (the 4/4 flip base rate).
Bands: 0-15 dead, 16-39 weak, 40-69 promising-unverified, 70+ verified = design the cheap test.
Mapping for every entry above: KILL ≤ 15, WEAK 16-39, WORTH A CHEAP TEST 70+. No old verdict changes.

For throughput, screening is now a four-tier pipeline (tier 0 no-network triage at ~1 min/idea, drop
<30; tier 1 position probe at 2-5 fetches, drop <40; tier 2 full screen for top scorers; tier 3
mandatory verification before 70+), so a round can open with 20-100 raw candidates. The working
research seams were moved from session scratchpads into the skill at `scripts/` (bs.py Brave search,
f.py URL-to-text, jac.py Atlassian tracker votes, mp.py Marketplace installs, price.py Marketplace
pricing, cql.py/space.py/page.py public Confluence wikis). Prior SKILL.md text is in ~/.claude git
history.

## Round 2026-08-20f: 30-candidate sweep of the permitted axes, zero above 40

Batch of 30 across developer/API docs, edge/multi-tenant infra, document/video generation, and LLM
app engineering. check.py sanity check passed ("outbound webhook delivery" HIT). Eight were straight
ledger hits or inherited variants; sixteen died at tier 0 on platform-owner giveaways and OSS anchors
(Cloudflare Bulk Redirects, GitHub auto release notes, Mintlify llms.txt/translations, Scalar,
Stoplight Prism MIT, Ragas Apache, instructor MIT, OpenAI native structured outputs, Postman mocks).
Two reached tier 1 and both died on position, evidence dated 2026-08-20:

**22 | Contract/proposal document assembly API for vertical SaaS.** Self-serve slot occupied at
commodity prices: PDFMonkey free 20 docs/mo then EUR 5/mo (pdfmonkey.io/pricing); Anvil $0.10/PDF
pay-per-use with 2,500 free credits and free template UI (useanvil.com); Carbone Community edition
free AGPL with cloud from EUR 50/mo; Api2Pdf ~$0.005/PDF usage-based. Demand is real (people pay)
but the position dimension scores zero and the price floor is near the COGS gate. Sources: vendor
pricing pages via WebSearch snippets; not re-fetched directly.

**25 | Screen recording to written developer tutorial / docs article.** Loved cheap self-serve
incumbents in the exact slot: Scribe Pro Team $13/seat/mo, Guidde Pro $23/creator/mo, plus Tango,
Trails, iorad, Tutorial AI, Loom SOP drafts; open-source AI-DocGen (CactusQuill, GitHub) does
recording-to-docs free. Founder fit was the highest in the batch (Kroto/Helply video-to-article
pipeline) but the "developer tutorial" twist does not defeat the incumbents — their output embeds in
any docs tool. Noted but not pursued: comparison content says Guidde/Scribe cannot convert EXISTING
video libraries, only new captures; that is one-time migration-shaped demand (trap 4). Licence of
AI-DocGen unchecked.

**Filter audit (base-rate check fired: 0/30 above 40).** The killers were hard evidence — named
free or sub-$25 incumbents, OSS by name with licence, platform-owner releases — not venture-filter
rules, so the filter looks honest. The real finding is sourcing: all 30 were brainstormed from the
permitted axes, which are the most arbitraged spaces in indie hacking. Trap 8 applies beyond
buyer-access ideas: axis-brainstormed batches keep converging on ideas the market already priced at
zero. Next round should start from Yuvraj naming concrete insider pain or reachable operators, not
from another axis sweep.

Unchecked sources this round: G2/Capterra bodies, HN Algolia, Reddit, keyword volumes, Documint
pricing, AI-DocGen licence. Tooling: harness WebSearch/WebFetch LOADED successfully this session via
ToolSearch exact-name select ("select:WebSearch,WebFetch") after regex-pattern searches returned
nothing — the earlier "unloadable" note was a query-syntax artifact, not availability.

## Round 2026-08-20g: insider-pain + proven-shape sourcing; first 40+ since the score rewrite

Sourcing changed per round-f audit: candidates came from multi-tenant SaaS engineering pain (the
founder's daily domain) and transplants of ledger shapes (E1 DSAR fan-out, 78 verified but
Zendesk-barred; change-history class arithmetic). Twelve candidates, ten dead at tier 0/1, one
promising-unverified at 58.

**5 | DSAR/erasure orchestration for B2B SaaS engineering (E1 transplant).** Gate 1 fired: Ethyca
Fides, Apache-2.0, is the exact product — "fulfills any privacy request by connecting directly to
your disparate databases", prebuilt connectors, free self-host, first DSR in under five minutes
(github.com/ethyca/fides, ethyca.com/open-source-dsr, fetched 2026-08-20). Osano and Ketch (from
~$499/mo) hold the downmarket paid slot. The E1 shape only verified alive INSIDE Zendesk, where the
buyer is barred; outside it the OSS anchor kills it.

**25 | SOFTEX/EDPMS/e-BRC reconciliation for Indian exporters.** NIRYAT (theniryat.com) sells the
exact "Compliance OS" (DGFT+ICEGATE+EDPMS+AD-bank reconciliation, eBRC automation) to Rs 5-500cr
exporters; NiryatBox gives a free readiness checker for the SaaS/services segment; payment platforms
(Skydo, Xflow, Karbon) bundle compliance docs free with FX margin; RBI's October 2025 circular lets
entries under Rs 10 lakh close on simple declaration. Position and COGS both collapse. Dated
2026-08-20, WebSearch snippets.

**58 | Per-tenant restore for existing shared-schema Postgres SaaS.** The one survivor. Position
(20x0.7): verification found NO off-the-shelf product in the retrofit slot — 2025 ecosystem consensus
is "choose schema/db-per-tenant so PITR works, or build a logical snapshot + WAL-decoding pipeline
yourself" (ClickHouse multi-tenant architecture guide 2025; AWS Database Blog selective-restore
recipe; SAP was granted US 12,242,359 B2 "tenant-level database recovery" March 2025 — enterprises
build this in-house). Platform owners occupy only the migrate-away path: Neon markets per-tenant
PITR for database-per-tenant fleets, Nile virtualizes tenants with per-tenant backups, Azure SQL
documents it for db-per-tenant. None retrofits an existing pooled RDS database, so gate 1 does not
fire. Demand (25x0.3): tier 5 and stale — HN comments 2022-2023 ("Not having per tenant backups is
sensible? Seems like a bit of an oversight", 2022-04-13; "How do you implement per tenant backups?
Not every db system cleanly separates...", 2022-04-14, both from the Atlassian outage threads —
that outage WAS a weeks-long per-tenant restore failure), refreshed only by 2025 architecture
content naming the problem unsolved. No tier 1-3 evidence found in sources checked. Founder fit
(15x0.8): the founder is the buyer persona. Distribution (15x0.6): long-tail queries unfarmed.
Arithmetic (15x0.5): eng teams pay $100+/mo but production-data trust demands a runs-in-your-VPC /
BYO-S3 design given no SOC 2. Contract (10x0.8): FK-graph slicing + WAL decoding is weeks (patents
exist on it). Total 58. CHEAP TEST DESIGNED (run only if Yuvraj wants it despite <70): 20 Mom Test
outreach emails to eng leads of shared-schema B2B SaaS (Rails/Django companies from HN hiring
threads), asking how they last handled "restore this customer's data" — pass if 4+ describe an
internal script, an incident that ate engineer-days, or ask price. Cost: hours, $0. What would lift
the score past 70: any two dated tier 1-3 items, e.g. named teams that built this internally
post-2024 or paid Neon/Nile specifically to get per-tenant restore.

Unchecked this round: Reddit, G2 bodies, keyword volumes, Nile pricing/traction, Fingerprint current
pricing, GitHub code search (repo search only, found nothing starred — absence not proof). New seam:
scripts/hn.py (HN Algolia, python3 -c is shell-blocked). Ten of twelve kills again named a free/OSS/
platform-owner anchor; the two-round pattern holds — ideas survive only where the pain is too
bespoke for a platform owner to productize (per-tenant restore) or a buyer is contractually barred.

## Round 2026-08-20h: same sourcing, second survivor in the same product family

Twelve more candidates from multi-tenant engineering pain plus transplants of the change-history and
custom-domain shapes. Nine dead, one weak, two promising-unverified (one being round g's 58).

**5 | Cross-tenant leak detection / RLS policy testing in CI.** Gate 1 fired hard: pgrls
(github.com/pgrls/pgrls) is free OSS with 67 lint rules, 20 auto-fixable, a semantic policy-diff for
CI gating, a pytest plugin for isolation tests, and a `verify` mode using the Z3 SMT solver that
"never reports PROVEN unless Z3 proves it". Atlas covers the drift half (`atlas schema lint/test`
blocks PRs that disable RLS or grant BYPASSRLS). Fetched 2026-08-20. Notable: CVE-2025-48757 (170+
Lovable-generated Supabase apps shipped with RLS off) is real demand, but it is already served free.

**10 | Migration safety review / lock analysis in CI.** Squawk free OSS (sbdchd), MigrationPilot MIT
with 80 rules, pgfence source-available doing full lock-matrix classification. One genuine
displacement event found and logged for the anti-portfolio: Atlas v0.38 (2025-10-30) moved
`atlas migrate lint` out of the free tier to $9/dev/mo + $59/CI-project/mo, and third parties wrote
"Atlas Paywalled Their Migration Linter — Here Are Your Free Alternatives". Displacement is real but
the vacated slot was filled by free OSS within weeks, so there is no paid slot to enter.

**5 | Feature flag cleanup.** FlagShark ships a free-forever GitHub Action (13 languages detected,
AST-based, auto-removal PRs for 8 languages and 8 flag providers); LaunchDarkly includes Code
References in Pro. Dead on arrival.

**52 | Per-tenant query performance attribution for pooled Postgres.** Second-highest this round and
the SAME buyer and shape as round g's 58: retrofit tenant-awareness onto an existing pooled database.
Position is genuinely gapped — pg_stat_statements normalizes the tenant_id away by design, pganalyze
exposes no tenant dimension (its own docs route you to auto_explain log samples), citus_stat_tenants
requires being on Citus, and RDS Performance Insights is not tenant-aware. Demand is live and dated
this year: HN 2026-07-16 "I am more worried about the noisy neighbor problem", HN 2026-04-09 "with a
huge multi-tenant database, how do you deal with noisy neighbors?", plus Cloudflare's own engineering
blog describing manual per-tenant limits as "toil that can page an SRE at any hour" (they built
gateway-level per-tenant query queuing in-house). What holds it to 52 rather than higher: (a) a weak
occupant already exists — "Show HN: FaultWall – Which tenant is killing your Postgres?" posted
2026-03-27, which took 2 points and is still not indexed by search engines five months later, which
is negative demand evidence as much as it is competition; (b) the DIY path is a well-documented cheap
recipe (tag queries with a /* tenant:1234 */ comment or per-tenant application_name, then facet in
Datadog/New Relic), so the contract test is weak. Not worth a round of its own.

**Strategic note for the next round.** Rounds g and h independently produced the two highest live
scores (58 per-tenant restore, 52 per-tenant attribution) and they are one product family:
tenant-aware operations retrofitted onto pooled Postgres. Platform owners (Neon, Nile, Citus, Azure)
serve only the migrate-to-us path; the retrofit slot for teams who cannot restructure a production
database is where both gaps sit. If any candidate gets a cheap test, run restore as the wedge and
treat attribution as the second feature, not as a separate product.

Base rate across rounds f+g+h: 54 candidates, 3 above 40 (5.6%), still under the 10-30% target, but
the killers remain named free/OSS/platform-owner anchors rather than filter artifacts. Unchecked this
round: FaultWall's actual site and pricing (not indexed; not fetched directly), Reddit, G2 bodies,
Datadog per-tenant tagging pricing at cardinality, pganalyze current tenant features beyond docs.
