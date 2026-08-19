# Verdict ledger

Ideas already screened. **Read before proposing anything. Append after every screening, dead or alive,
with the specific killer named.** Each dead entry is a search nobody has to run again.

Cleared 2026-08-19 at Yuvraj's request. The prior ledger (22 dead, 9 alive, 9 pending, plus method
notes) is recoverable with:
`git -C ~/.claude show 3e9cc16:skills/micro-saas-gap-hunting/references/verdict-ledger.md`

## Dead

| Idea | Killer |
|---|---|
| Inbox placement / deliverability testing API (was the top candidate) | Position and free-anchor tests failed 2026-08-19. Unspam already sells a per-provider inbox placement API (async, Bearer token). MailerCheck sells placement tests pay-as-you-go at 200 credits = ~$2/test, no subscription. "Inbox Placement Test" (check.live-direct-marketing.online, on Capterra) holds the dev-first slot: free tier 3 tests/day no signup, paid REST API, even an MCP server. Free anchors inside the market: EmailWarmup.com (unlimited free tests, 15+ providers), MailReach (3 free/day), Unspam (10 free/mo), MailGenius. Inbox Radar took the flat-unlimited slot at $23/mo. The seed-mailbox estate turned out to be widely reproduced, not a moat — the old ledger's "zero entrants" read was stale (SpamCipher and Hello Inbox were already the warning) |
| Peppol / e-invoicing API | Position taken several times over: e-invoice.be (€0.18/invoice pay-per-use, "no sales call"), getpeppr (built exactly for embedded multi-tenant SaaS: one key, N legal entities), peppol.sh, Storecove (API-first from €495/mo). Owning the estate also fails the access test: certified AP needs mandatory ISO 27001, ~€1,025 sign-up + €1,800/yr candidate then €4,150/yr certified OpenPeppol fees, 3-stage accreditation, 24/7 AS4 uptime. France Sept 2026 wedge needs separate PA (ex-PDP) certification and 101 PAs are already approved |
| EU Digital Product Passport (battery, deadline 2027-02-18) | Position test failed: DPP-Tool owns the self-serve SME slot at €9/mo, no implementation fee, no sales call. PicoNext and Tappr at ~€520/mo mid-market, Substantio/ProductPass/DPP Automate/Circularise/Siemens above. OSS-anchor test passed (biggest active repo open-dpp, 28 stars AGPL; reference impl archived) but the €9 floor caps pricing and the deadline demand is already being served |
| 3D / CAD thumbnail rendering API | Giant + OSS + position all failed: Autodesk Model Derivative renders 70+ formats incl. STEP/STL thumbnails at ~$0.30/simple job with a free monthly tier arriving under the new APS model; `fpurchess/preview-service` is an MIT docker-run HTTP thumbnail service (stl/obj/ply), stl-thumb + FreeCAD/OpenCascade cover the conversion path free; 3DCompare CAD.ai already holds the niche hosted slot |
| AI support-agent QA / regression testing, TEXT chat and email (the non-voice variant) | Inherits the voice-testing killer and adds a worse one: the platform owners ship it free inside the product the buyer already pays for. Intercom ships Fin batch tests, simulations, staged rollouts and pre-deployment scorecard Monitors natively; Zendesk ships "Test AI agent" in Admin Center plus a dialogue test widget and publishes its own multi-turn test-generation research. Position also taken: Coval sells self-serve text-or-voice simulation from $100/mo with a 7-day trial; Solidroad does AI-support QA with Zendesk/Intercom/Gorgias connectors on a $25M Series A. Free OSS anchors: openai/evals 19,200 stars, deepeval 17,697, evidently 7,819. Free hosted anchors: Braintrust Starter $0 with LLM-as-judge and unlimited experiments, Langfuse Hobby free and self-hostable. **Extend the dead voice entry to AI-agent testing in all modalities** |
| Help-center / KB migration and two-way sync API | Platform owner ships both halves free: Intercom's Zendesk help-center importer is free and no-code, and free hourly "sync public articles with Zendesk" plus Confluence/Guru/Notion sync; Featurebase ships free one-click importers for Intercom, Zendesk and Crisp. Every AI-support entrant subsidises migration to win the account, so the free anchor keeps regenerating. The paid remainder fails buyer arithmetic structurally: Help Desk Migration (Relokia) sells one-time per-record work ($100/1,000 records, $514 at 10,000), and a migration customer churns by definition, so there is no recurring $50+/mo base. Unito already sells two-way Zendesk sync |
| Docs-as-code publishing / git-backed sync for Zendesk-class help centres | The whole product is "render Markdown to HTML and PUT to the Help Center API keyed by an article ID in front matter" — a GitHub Action the buyer's engineer writes in a day, and Zendesk's own docs team publicly documents running exactly that pipeline in-house. The OSS that exists is stale and tiny (zendoc, zenpush, zendesk-helpcenter-cms all low-star), and GitHub tops out at 3 stars for the search, which is absence of pull rather than an opening. Buyers who want docs-as-code already left for GitBook/Mintlify, whose cheap tiers include GitHub sync natively; the Zendesk Guide holdouts are support teams who do not want git |
| Safe-to-embed workflow automation (the n8n Sustainable Use Licence blocked segment) | The best licensing-blocker story found and it still dies. The licence genuinely blocks embedding ("You may distribute the software or provide it to others only if you do so free of charge for non-commercial purposes"), n8n charges ~$50K/yr for the OEM exemption, Activepieces Embed is "from $36k/year" talk-to-sales, and no self-serve mid-market embed tier exists — so the position test actually PASSED. Killed by the free OSS anchor instead: the Activepieces core is MIT Expat (23,888 stars, only `packages/ee/` separately licensed), so a SaaS vendor can legally embed it for $0; what the $36K gates is the SDK and support, not the legal right. Apache-2.0 peers too: sim 29,433 stars, kestra 27,853. Also far beyond a 2-week solo build |
| AGPL-free embedded analytics (the Metabase blocked segment) | Position test failed twice. The leader is not structurally blocked from serving the segment — Metabase sells the commercial exemption itself, published and self-serve, Pro at $575/mo + $12/user/mo with white-label embedding — so the AGPL is a deliberate upsell funnel, which makes any wedge a mere pricing gap. And apache/superset is Apache-2.0 at 74,310 stars, legally embeddable for free, with MIT evidence-dev at 6,862 |
| Embeddable e-signing without AGPL (the Documenso blocked segment) | Position test failed at step 1: Docuseal already sells the flat-priced self-serve developer version, Pro $20/user/mo including "API and Embedding" plus embedded signing at $0.20/completion, no sales call, with a dedicated document-signing-for-SaaS page and React embed components. SignWell and BoldSign also sell cheap self-serve e-sign APIs |
| India regulated rails (GST e-invoice / e-way bill / KYC-KYB verification APIs) | Screened 2026-08-19 as the "jurisdiction as advantage" inversion: being Indian is a credential foreigners cannot get, which should invert the round-4 killer. Both halves fail. Owning the moat is out: a GSP licence requires an Indian *company* in IT/BFSI with >= Rs 2 crore paid-up capital and Rs 5 crore average 3-year turnover, India-based servers, a scored sandbox demo (60% pass mark), and there is no open application batch in 2026 (62 GSPs empanelled). Reselling someone else's GSP leaves no moat. The layer above it fails the position test: Deepvue sells 150+ verification APIs self-serve pay-per-call with a free trial, volume tiers and "no commitments", and Sandbox.co.in publishes a transparent tax-API price page with a free start (Amazon and Tata as references); Surepass has 300+ APIs. The transparent developer-first slot is taken, and Indian ARPU makes the buyer arithmetic worse than USD markets |
| Walkthrough video rendering API | COGS test failed on both sides. Your unit cost is a browser session PLUS a video encode per minute, while the generic renderers already retail below that: Shotstack flat $0.20/min subscribed ($0.40 pay-as-you-go), resolution- and fps-independent, independently benchmarked at ~$0.10-0.84/min across vendors at 1080p. Remotion (which Yuvraj already uses in InstantDocs) is the free programmatic-video anchor and self-hosts on Lambda. App layer is saturated and cheap: Guidde $18/creator, Supademo $27, Arcade with the most generous free plan, plus Trupeer, Screen Studio, Capptivo, HowdyGo. Only-software, no moat. Screened 2026-08-19 |
| Scraping / crawl API, Firecrawl AGPL wedge | The AGPL gap barely exists: using Firecrawl's hosted API or running it internally never triggers AGPL, only distributing modifications does, so the blocked-buyer segment is tiny. Free permissive anchor: Crawl4AI, Apache-2.0, ~68K stars, docker self-host with FastAPI server — "the cleanest architectural replacement, commercial-friendly license". Position also taken: `us/crw` already ships a drop-in Firecrawl-compatible REST API, vakra-dev/reader (Apache-2.0) self-tags "firecrawl-alternative", Spider.cloud owns the speed/transparent-billing slot. Screened 2026-08-19 |

## Alive, small incumbents, correct shape

| Idea | Who is there | Note |
|---|---|---|

## Pending, blocked on a named test

| Idea | What is there | Blocking test |
|---|---|---|

Empty as of 2026-08-19c. Every prior pending has been resolved to a verdict.

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
