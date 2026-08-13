---
name: project-kb-edge-static-surface
description: "Branch ys/feat/kb-edge-static-surface: every host baked, robots/sitemap + reader JS served from R2, artifact v4"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7cc61853-fad8-4679-9603-21f16494f649
  modified: 2026-08-09T18:48:57.163Z
---

Built 2026-08-10 on `ys/feat/kb-edge-static-surface` off master. Takes the published reader's whole *static* surface off Railway. **Bumps `KB_ARTIFACT_VERSION` 3 → 4**, so every KB falls through to origin until re-baked — deploy the Worker first, then merge, then re-bake all.

Four pieces:

1. **Bake reaps** — see [[project_kb_bake_never_deletes_orphans]].
2. **Every host is baked.** `KbHostResolverService.hostsForKb(kb)` returns the subdomain plus a servable custom domain; the bake resolves each host separately and writes an artifact per host, so no custom-domain policy is duplicated in the baker. `KbHostArtifact` became a union: `{kind:'kb', resolution}` or `{kind:'redirect', kbId, toHost}` (the Worker 301s from the marker itself). `canonicalHost` was **removed** from the artifact — `isCanonicalHost(resolution, hostname)` in `shared/kb-artifacts` derives it from `customHost` and is the one expression origin and edge share.
3. **robots/sitemap baked** into `kb/{id}/seo.json`, indexable variant only. The Worker substitutes shared `ROBOTS_DISALLOW_ALL` / `EMPTY_SITEMAP_XML` (in `shared/kb-seo`) for a gated KB, an SEO-disabled KB, or any off-canonical host — so one baked copy covers every host and the disallow path reads no artifact.
4. **Reader JS from R2.** `KbEdgeAssetPublisher` (OnModuleInit, fire-and-forget) uploads each script under `assets/current/{name}` and `assets/v/{hash}/{name}`. Old hashed copies are never deleted, which is what lets the loader carry a 5-minute TTL safely.

Non-obvious decisions worth not re-deriving:

- **The cached-entrypoint cache key already includes the hostname**, because the key is the request URL + entrypoint + `ctx.props`. Per-host variants therefore need *no* props change. (I initially planned to add the host to props; unnecessary.)
- **Gateway responses are NOT stored in the Worker cache** (`cache: {enabled:false}`). The `cf-cache-status: HIT` seen previously on `/_kb/toc.js` came from the *subrequest* `fetch()` to origin, not from caching the gateway's own response. So anything that must be edge-cached has to go through a cached entrypoint — hence `CachedAssets` (no props; same bytes for every KB) rather than serving assets straight from the gateway.
- **SEO routes are answered inside `CachedKb`, not the gateway**, purely so they carry the KB's `Cache-Tag` and a publish purge can evict them. That is the fix for robots.txt previously being zone-cached 4h with no tag, making an SEO toggle unpurgeable.
- `/_kb/` cannot be treated as a prefix: it also carries `unlock`, `auth/callback`, `member-recheck` and `search.json`. `shared/kb-assets` names the servable files explicitly.
- `shared/kb-assets.ts` must not import `node:crypto` — it is imported by the Worker.
- Ordering in the gateway: host → redirect → throttle → gates → **assets** → canonical redirect → pageRefusal → CachedKb. Assets sit after gates (matches origin behaviour) and before `pageRefusal`, which would reject their `?v=` as an unknown query.
- `forAssetEntrypoint` strips every query param except `v`, or a caller could mint unbounded cache entries for one script.

Also fixed here: `hostArtifactKbId` in `bin/kb-artifact-bake.ts` read `parsed.kbId` while the artifact nests it under `resolution` — the stray-host sweep had never matched anything.

Verified: backend 691 files / 7415 tests, kb-edge 82 tests, biome + all four typechecks clean.

Related: [[project_kb_edge_serving_live]], [[project_kb_gated_edge_and_redis_removal]], [[project_kb_custom_domains_design]]
