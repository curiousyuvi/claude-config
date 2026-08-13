---
name: project_kb_interlink_durability
description: "KB article interlink feature — durability must come from stable id references resolved to the current URL, NOT from previous-slug redirects"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6085a000-d530-487c-9862-290d55cc4c43
---

Building durable internal links in the axis KB: article content (inline link, button/CTA, card block) can link to another article/collection in the same or another KB in the org, and must not break on slug/path change.

**Design constraint (user, 2026-07-09):** Do NOT rely on the existing previous-slug redirect (`previous-article-slug` / `previous-collection-slug` entities) as the durability mechanism. It is insufficient: redirect chains accumulate, a collection move changes the whole path (not just the article slug), and cross-KB moves / deletes / unpublish aren't covered. Internal links must always resolve to the **current, direct canonical URL** of the target. Redirects are only a net for external inbound links, never the interlink mechanism.

**Chosen foundation (2026-07-09): id-addressed public URLs.** The KB has NO customers / no live-indexed URLs yet, so we're free to change the reader URL scheme with zero SEO/migration cost. Adopt Zendesk-style `/doc/{id}/{slug}` (id routes, slug decorative; uuidv7 has hyphens so id is its own path segment or a base62 short-id). Consequences:
- Internal-link durability is **structural** — the id in the URL survives rename/move, so NO backlink fan-out / re-materialization is needed just to keep links valid.
- The existing `Previous*Slug` subsystem (entities + `recordPreviousSlug` in kb-slug.util.ts + `RedirectOrMiss` in kb-reader.service.ts) becomes dead weight — canonical wrong-slug→current-slug 301 is a stateless id-lookup, no history table.
- **User directive (2026-07-09): remove ALL three** — `PreviousArticleSlug`, `PreviousCollectionSlug`, AND `PreviousKbSlug` — in this same PR. Note `PreviousKbSlug` guarded the KB *subdomain* (host) redirect, which publicId does NOT cover (KBs have no publicId); removing it means a KB subdomain rename no longer 301s old URLs — accepted (no customers). Also removes the subdomain-redirect read in `kb-host-resolver.service.ts` + `recordPreviousSlug` in KB rename.
- The interlink feature reduces to: a **lighter `KbLinkRef`** value in the Plate node (`kind` url|article|collection, `targetId`, `targetKbId?`, `targetLocale?`, display-only `label?`) + one shared picker + resolving **display metadata** (title/icon, cross-KB host) at publish. Public reads stay O(1) (never the instantdocs read-time N+1).

**Scope (2026-07-09):** the article/collection PICKER + `KbLinkRef` reference model + wiring the 3 editor elements are DEFERRED (the future layer). Built only the **id-addressed reader URL foundation**.

**STATUS — foundation MERGED TO MASTER (PR #710, branch `ys/feat/kb-id-addressed-urls`, 2026-07-09):**
- `publicId` = **10-char nanoid** (`generatePublicId` in `knowledge-base/domain/public-id.ts`, `PUBLIC_ID_MAX=10` in shared kb-authoring.schema), on `kb_articles` + `kb_collections`, global non-partial unique index. NOT the PK (uuidv7 PK unchanged — repo convention).
- Reader URL = `/{seg}/{publicId}-{slug}` (seg doc/col). `nodeRoute(kind, publicId, slug, segs)` + `parseNodeToken` (split first hyphen) in `kb-public/application/kb-routes.ts`. Reader resolves BY publicId + stateless canonical 301 on slug mismatch (`kb-reader.service.ts` doc()/collection()).
- ALL 3 previous-slug entities/tables removed (article, collection, KB); `assertSlugAvailable`/`applySlugRename`/`uniquifySlug` KEPT (KB-subdomain uniqueness still uses them). Article/collection slug UNIQUENESS removed (both `slugNorm` unique indexes dropped); duplicate/restore/transfer keep own slug; shared `renameNodeSlug` in kb-slug.util.ts. Client slug-availability UI removed.
- Migrations: `Migration20260709170404` (add publicId nullable→collision-free row_number backfill→NOT NULL + unique; drop 3 slug-history tables) + `Migration20260709173320` (DROP INDEX the 2 slugNorm uniques). Both applied on dev.
- Frontend: 3 URL builders use shared `web .../lib/reader-url.ts` `readerNodeUrl` (guards publicId, normalizes via `slugify`).
- Validated: typecheck 0, biome clean, backend KB 731 tests + web KB 63 tests. Adversarial review + `/code-review max` findings fixed.

**NEXT TASK (active) — the col/article PICKER for link + card + button in the article editor.** Build the authoring layer on top of the merged id-addressed-URL foundation. Design (from this session's research; adapt, don't copy — instantdocs is BlockNote, axis is Plate):
- Store a shared `KbLinkRef` value in the Plate node — `{ kind: url|article|collection, targetId, targetKbId?, targetLocale?, label? }` — NOT a raw href. SHARED code across all 3 elements (one link-value model + one `<ArticleCollectionPicker>` + one link-input that toggles URL vs internal ref).
- The 3 Plate elements: inline link mark (`apps/web/src/shared/editor/plate-nodes/link-toolbar.tsx`), button/CTA (`button-node.tsx`), card (`features/knowledge-base/components/editor/card-group-node.tsx`). Today they store raw scalars (link=`element.url`; button/card=`element.href`).
- Picker UI: model on `features/knowledge-base/components/kb-move-to-popup.tsx` (KbPicker/CollectionPicker searchable tree); search published nodes org-wide via OpenSearch `kb_published` (matches [[project_kb_panel_published_only]]); use query-options factories.
- Resolution is now TRIVIAL: the merged foundation gives every node a durable `publicId`; resolve a ref → `/{seg}/{publicId}-{slug}` (relative same-KB, absolute cross-KB) at publish, in `static-components.ts` link/button/card serializers. No backlink table / re-materialization needed (id-addressing makes it structural).
- Open product decisions to confirm with user: allow linking to DRAFT targets (vs published-only); store denormalized `label` snapshot for editor display. instantdocs prior art to adapt: `link-article.tsx`, `CreateLinkButton.tsx`, its article/collection picker.

**Deferred / follow-ups:** (1) bulk `kb:reindex` CLI — none exists; `reindexKb` is private + no drop-index helper; KB search docs get publicId incrementally on publish (prod index empty = no backfill needed). (2) Deploy runbook: deploy code-BEFORE-migration (NOT NULL); reindex/recreate KB OpenSearch index for the new publicId mapping. (3) Accepted-by-design: legacy slug URLs + renamed-KB-subdomain now 404 (no redirect); generatePublicId has no collision retry (62^10 negligible).

Axis URL scheme lives in `apps/backend/src/modules/kb-public/application/kb-routes.ts` (articles flat `/doc/{slug}`, collections `/col/{slug}`, locale-prefixable, prefixes configurable). Publish already materializes `variant.html` (`article-publishing.service.ts`), reader serves cached html (`kb-reader.service.ts`, never touches Plate JSON). Must be **shared code** across all three elements (link mark / button-CTA / card). Prior art in sibling repo `instantdocs` (BlockNote; axis uses Plate) — [[feedback_instantdocs_project_reference]].
