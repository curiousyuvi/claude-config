---
name: project-regional-kb-404
description: "Published KB 404 in some countries only = per-region Vercel data cache holding a cached null; quick fix is revalidating the KB's cache tag"
metadata:
  node_type: memory
  type: project
  originSessionId: 7644d419-558a-45e1-a91d-8c3ba8e36c01
  modified: 2026-10-27T13:20:54.444Z
---

Published KB article/collection returns 404 from some regions but 200 from others (confirmed 2026-10-27, covve ticket #92, Austria VPN 404 vs India 200). x-vercel-id header shows the function region (e.g. bom1::bom1); Vercel's data cache (unstable_cache) is per function region.

**Why:** A null slug lookup got cached for 12h in one region, and publish only revalidated locale-doc/kb-structure tags, never doc-slug. Fixed by `cacheNonNull` wrapper (src/server/helper/cache-non-null.ts) replacing every unstable_cache call, plus doc-slug tags on publish.

**How to apply:** For an urgent customer report, revalidating the `entire-kb-<kbId>` tag clears it globally. Then check whether a new code path bypasses cacheNonNull or caches a not-found as data. See [[project-publish-sfn-debugging]].
