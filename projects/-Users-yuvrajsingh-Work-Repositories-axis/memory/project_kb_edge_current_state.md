---
name: kb-edge-current-state
description: "Published-KB edge architecture as SHIPPED on master (slices 1-6 done); what caches where, and the open embed work"
metadata: 
  node_type: memory
  type: project
  originSessionId: ea441c8c-9d1f-4fc1-9ef3-73ac33678184
  modified: 2026-08-10T15:43:51.736Z
---

Verified against master 2026-08-08 (`cb0f545e3 perf(kb): take Redis out of the published-KB path (#1091)`). Slices 1-6 of [[kb-published-r2-worker-caching]] are all MERGED. Do not answer questions about this from older notes — [[kb-gated-edge-and-redis-removal]] describes the plan, this describes the result.

**Caching (the thing I got wrong once):** public KB pages ARE edge-cached. `packages/shared/src/kb-cache-policy.ts` — public pages `public, max-age=0, s-maxage=86400, must-revalidate` (Cloudflare holds 24h); gated pages `private, max-age=0` (no shared cache, R2 every request, correct since the decision is per-visitor); versioned `?v=` assets 1yr immutable; fixed-URL assets 5min. Freshness is `Cache-Tag: kb-{kbId}` + `purgeTags` on every bake, NOT the TTL — 24h only bounds a lost purge.

**Three Worker entrypoints** (`apps/kb-edge/wrangler.jsonc`): `default` gateway cache DISABLED (resolves host, throttles, runs gates, routes — must run every request); `CachedKb` cache ENABLED keyed on `ctx.props.kbId`; `CachedAssets` cache ENABLED, no props (reader JS is identical bytes for every KB). `CachedKb` is only reachable via loopback binding, so nothing cached serves without passing gates.

**Now edge-served too** (was origin in earlier notes): reader JS via `CachedAssets` (after the gates, so a private KB's scripts are no more reachable than its pages), and robots.txt/sitemap.xml via `apps/kb-edge/src/seo.ts` (non-indexable/gated/non-canonical answered from constants without reading R2). Subdomain→custom-domain redirect is done AT THE EDGE from the host artifact (`host.kind === 'redirect'`). Edge rate limiter `GATE_LIMITER` 10/60s per IP on unlock + auth-callback, running BEFORE gates (the password gate refuses unlock POSTs by design, so throttling after it would never see the flood).

**Redis is GONE from the published-KB path.** Host resolution reads the host artifact; the edge forwards its answer to origin via `EDGE_RESOLUTION_HEADER`, so origin queries run only on fall-through, gate endpoints, or local dev.

**Slice 7 SHIPPED** (#1099, merged `8a0010acb` 2026-08-10, artifact v5): `?embed=1` is baked for articles only into `kb/{id}/embed/{path}.json` + `kb/{id}/embed-template/{locale}.html`, with a second `embedHeaders` map in the settings artifact. **`forCachedEntrypoint` keeps `embed=1` on the URL on purpose** — it strips every other parameter, and the cache key is the URL, so sharing an entry would put `frame-ancestors *` on the main page and make the KB framable by anyone.

Verified in production after deploy: embed and plain page both `cf-cache-status: HIT` on separate entries, embed carrying `frame-ancestors *` + `noindex` and the plain page still `frame-ancestors 'self'` when fetched immediately after. **That check only works against real Cloudflare — entrypoint caching is inert under local workerd, so no test can prove it.** Re-run it after any change to `forCachedEntrypoint`. Cache headers changed in the same slice; see [[kb-public-page-cache-headers]].
