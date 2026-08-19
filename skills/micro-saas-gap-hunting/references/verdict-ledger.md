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
