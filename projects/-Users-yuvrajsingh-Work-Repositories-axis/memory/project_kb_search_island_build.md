---
name: project_kb_search_island_build
description: Published-KB instant search (⌘K client) needs a separately-built island bundle that pnpm dev does NOT build
metadata: 
  node_type: memory
  type: project
  originSessionId: 3c18f6b5-7571-4b19-9866-bc5a9c9f0484
---

The published-KB instant/⌘K search widget ("the search client") is a self-contained React island served from disk at `apps/backend/public/_kb/search-island.js` (reader CSP is `script-src 'self'`, so it can't be a CDN/SPA chunk). The reader middleware (`kb-reader-asset.handler.ts`) reads it lazily on first `/_kb/search-island.js` request and **memoizes** the result for the process lifetime — a miss caches `null`.

It is built by `pnpm --filter web build:kb-search` (vite.kb-search.config.ts → outDir `apps/backend/public/_kb`). This runs only as part of the full `pnpm build`, **NOT** as part of `pnpm dev`. So a fresh dev sandbox has no island → `GET /_kb/search-island.js` 404s → search silently falls back to the SSR `/search` page → "the search client doesn't come up."

**Fix:** run `pnpm --filter web build:kb-search`, then **restart the backend** (the memoized `null` won't clear otherwise — writing to `public/` isn't a source change so the watcher won't restart).

OpenSearch itself is separate: KB search query/index gated on `OPENSEARCH_URL` (set in apps/backend/.env.local → http://localhost:9200); index `kb_published`. A DB reseed does NOT reindex — stale kbId docs linger; reindex via `pnpm --filter backend search:reindex:all` if needed.
