---
name: project_kb_delete_host_cache
description: "Deleting a KB via raw SQL leaves a stale reader host-resolution cache → published KB 404s (\"Page not found\")"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3c18f6b5-7571-4b19-9866-bc5a9c9f0484
---

The published-KB reader resolves a request host → kbId via a Redis cache in `KbHostResolverService` (`kb-host-resolver.service.ts`), key **`kbpub:v:host:<slug>.<publishedDomain>`** (e.g. `kbpub:v:host:convious.helply-kb.localhost`), TTL 12h, **tagged** `kb-<kbId>` (not *named* by kbId).

Normal KB deletion emits `KB_DELETED` → busts that tag. **Deleting a KB with raw SQL bypasses the event**, so the host key survives and keeps resolving the slug to the now-dead kbId → the reader loads a gone KB and shows "Page not found / hasn't been published" even though a NEW KB with the same slug exists and is fully published.

A `redis-cli --scan --pattern '*<kbId>*' | xargs del` cleanup does NOT catch it (the key is named by host, tagged by id).

**When deleting KBs via SQL, also clear the reader caches by host/slug:**
```
docker exec axis-redis redis-cli DEL "kbpub:v:host:<slug>.helply-kb.localhost"
# or nuke all reader cache: redis-cli --scan --pattern 'kbpub:*' | xargs redis-cli del
```
Also delete OpenSearch docs (`kb_published/_delete_by_query {terms kbId}`) — see [[project_kb_search_island_build]]. FKs are RESTRICT: delete children (article/collection variants → related/featured → articles → collections → kb variants → kb) before the `knowledge_bases` row.
