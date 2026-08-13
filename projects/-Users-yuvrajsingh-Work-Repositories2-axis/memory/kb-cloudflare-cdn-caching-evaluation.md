---
name: kb-cloudflare-cdn-caching-evaluation
description: Aug 2026 evaluation of putting Cloudflare edge caching in front of the published-KB reader; landed on tag-mirrored purge as the main design
metadata: 
  node_type: memory
  type: project
  originSessionId: 2e503b00-3814-4eef-bd0d-4f456c3e33d2
  modified: 2026-08-07T10:06:31.765Z
---

As of 2026-08-07 the team is weighing published-KB caching designs. Konrad proposed R2 + Workers; the user proposed full-site Cloudflare caching with whole-KB purge; the evaluation landed on a third design as primary: pages emit a Cache-Tag header unioning the Redis cache tags consumed during render, and the KB outbox purges the same tags at Cloudflare that it invalidates in Redis. Whole-KB purge and per-URL purge were rejected (per-URL is incomputable: cards/breadcrumbs/prev-next put any article's content on any page).

Verified facts:
- helply.com zone is Cloudflare Business; ALL purge methods (tag/prefix/hostname/URL) on all plans since 2025-04-03. Business: 10 purge req/s, 100 tags per request. Cache-Tag response header: 16KB / ~1,000 tags, stripped before visitors.
- KB assets already on a separate CDN; only HTML in scope.
- Redis is self-hosted ioredis on Railway (no per-op cost); KB cache isolated as KB_CACHE_REDIS_CLIENT; tag vocabulary in shared/schemas/kb-cache-tags; connected cards resolve at render time via KbNodeMetaCacheService with per-node tags.
- Open items: tag purge behavior on CF-for-SaaS custom hostnames (needs spike); private-KB cache bypass (security); nav-tree staleness decision (N1 bounded staleness vs N2 whole-KB purge on nav edits); whether custom-domain TLS already bills through CF for SaaS.
- Estimation doc (v3) lives in the session scratchpad as kb-caching-estimation.md; headline: baseline scales linearly to ~$16k/mo at 10B pageviews, tag design flat at ~$510-690/mo.

**Why:** future KB caching work will revisit this; re-deriving Cloudflare plan facts wasted a round (I wrongly claimed prefix purge was Enterprise-only from stale knowledge).

**How to apply:** verify Cloudflare capabilities against current docs, never from memory; model origin load as edit-driven (edits x affected pages), not traffic-driven.
