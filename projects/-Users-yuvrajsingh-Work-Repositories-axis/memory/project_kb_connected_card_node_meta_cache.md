---
name: project_kb_connected_card_node_meta_cache
description: "Connected KB cards (Plate card → article/collection) resolve icon/title/desc/url from a per-node Redis meta cache; the converged design, the O(1) reasoning, and the rejected alternatives"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7acef55c-0ad9-443f-8e03-2833d1bfc17c
---

Feature: a PlateJS "card" block connects to a KB node (article OR collection); its icon/title/description/url come from that node and stay fresh **without re-publishing the host article**.

**Converged design (node meta cache):**
- Card already stores durable `KbLinkRef {kind, targetId}` (`packages/shared/src/schemas/kb-nodes.ts`). Add `source: 'custom' | 'node'` (absent ⇒ custom, so existing cards untouched) + a `resolveCardSource()` helper.
- Mechanism = **per-node Redis meta cache** via `TagCacheService.getOrSet`, key `nodemeta:v1:<kind>:<id>:<locale>`, value `{kbId,publicId,slug,status,title,description,iconType,iconValue}`, projected from **published** fields only. **No new DB table / migration** (Redis projection over existing entities). Cache `null` as a tombstone.
- O(1) write: article meta reuses the article body cache's tag triple `[kbArticleTag(id), kbArticleLocaleTag(id,locale), kbArticlesTag(kbId)]` → existing outbox worker busts it free. Collections need a NEW `kbCollectionTag(id)` in `kb-cache-tags.ts`, wired into `kb-events-worker.service.ts` (collection events carry `collectionId ?? nodeId` — MOVED uses `nodeId`; large subtrees drop `subtreeCollectionIds` → TTL self-heal).
- Stored publish HTML holds only an inert class-encoded placeholder `kb-cardref-<kind>__<id>` (sanitizer-safe like existing `kb-icref-*`; `data-*` is stripped). A read-time rewrite util (new, in **kb-public** to avoid a kb-public→knowledge-base cycle) resolves + rewrites it, running per-request AFTER the cached body read (never inside the body cache) in BOTH `KbReaderService.doc()` (SSR) and `getPublishedArticleById()` (panel — the panel runs NO post-sanitize pass, so the util must emit self-contained masked icons).
- Uniform resolution for same-KB / cross-KB / panel. Same-KB text at render locale; cross-KB at the target KB's default locale + absolute URL (`kbPublishedOrigin`), inert when no published domain. Key by the **resolved text locale** (split locale-independent identity vs per-locale text) to avoid cross-KB locale bleed. Do NOT reuse `KbLinkTargetService.resolveLinkTargets` on the public reader — it is drafts-inclusive (no published gate, reads draft title/icon) = leak. The editor preview keeps using that (authoring) resolver; add `description` to its projection.

**Rejected alternatives (don't revisit):**
- Meta/body article-cache split so "meta busts independently" — DEAD: `ArticlePublishingService.publish()` always re-renders `variant.html` and fires one coarse `KB_ARTICLE_PUBLISHED`; there is no meta-only change/event, so the two tags always bust together.
- Resolving cards from the KB-wide nav tree as the PRIMARY path — the tree busts whole-KB on any edit, and doesn't cover the panel (`getArticle` never loads the tree) or cross-KB. (A same-KB SSR tree fast-path via `loaded.nodeById.get(id)` — what related-articles already do — is a valid FUTURE optimization only.)
- Reusing the per-article body cache for cards — it drags the ~100KB html and lacks icon/publicId/slug; no equivalent exists for collections.

**Fundamental:** fresh + O(1)-write + zero-cost/cache-independent read is a pick-two trilemma (a fact in N places = N copies [O(N) write] or a pointer [read deref]). Chose fresh + O(1)-write; read = a batched cache lookup (cold miss = batched DB populate).

Related: [[project_kb_reader_serves_stored_html]], [[project_kb_panel_published_only]].
