---
name: kb-public-page-cache-headers
description: "Published-KB public pages send `public, max-age=30, s-maxage=86400`; why stale-while-revalidate was built then deliberately removed"
metadata: 
  node_type: memory
  type: project
  originSessionId: ea441c8c-9d1f-4fc1-9ef3-73ac33678184
  modified: 2026-08-10T15:43:39.198Z
---

Set in `packages/shared/src/kb-cache-policy.ts` via `pageCacheControl(restricted)`:

- public KB pages: `public, max-age=30, s-maxage=86400`
- gated KB pages: `private, max-age=0, must-revalidate`

`max-age` is short because a browser cache is the one copy a publish cannot evict (`purgeTags` reaches Cloudflare and nothing further). `s-maxage` is long because the edge *can* be purged, so it only bounds a lost purge.

**`stale-while-revalidate` was proposed by Konrad, implemented, then removed before merge. Do not re-add it without re-reading this.** Two independent reasons:

1. **It cannot help.** Freshness comes from `Cache-Tag` + `purgeTags` on every bake, so a publish *evicts* rather than expires. If a purge fully drops the entry there is no stale copy for SWR to serve; if it leaves one stale-servable, SWR returns the pre-edit page, which is the failure being avoided. Cloudflare's docs only say a tag purge "invalidates" and never say which. Either inert or harmful.
2. **It is not additive.** `s-maxage`, `must-revalidate` and `proxy-revalidate` each *disable* `stale-while-revalidate` under RFC 9111 §4.2.4, and Cloudflare implements that literally. Adding the directive alongside `s-maxage` does nothing. Adopting it properly means dropping `s-maxage` and moving the edge TTL to `Cloudflare-CDN-Cache-Control` (the Cloudflare-prefixed one, because plain `CDN-Cache-Control` is forwarded to downstream caches we cannot purge).

Konrad also checked the 1yr `immutable` asset policy: correct as-is, since it applies only to `?v=`-versioned URLs, while fixed URLs like `/_kb/search.js` get 5 minutes.

Related: [[kb-edge-current-state]].
