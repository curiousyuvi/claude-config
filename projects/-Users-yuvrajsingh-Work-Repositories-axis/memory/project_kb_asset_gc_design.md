---
name: project_kb_asset_gc_design
description: "KB asset garbage collection — references are DERIVED by Postgres from the documents, so there is no usage table and no delete-path hook"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1e927e1c-86e1-4d35-94a1-f2ea8187e4d2
  modified: 2026-07-31T04:54:32.823Z
---

KB uploads (icons, editor image/video/audio/PDF, KB logo + theme images) all live at `kb-assets/{uuidv7}`. Before this, nothing was ever deleted — `kb-asset.service.ts` said "Orphan cleanup is a later concern" and hard delete (`TrashPurgeService`) only ever touched DB rows.

**The design decision worth remembering: do NOT maintain a usage/refcount table, and do NOT hook the delete paths.** Both are fail-dangerous — miss one writer and the asset reads as unreferenced, so the GC deletes a file that is still on the page. Instead every table that can hold an asset URL carries a STORED generated `asset_ids uuid[]` column (`kb_extract_asset_ids()` regex over the row's own text) plus a GIN index. Postgres derives it, so it cannot drift, and "is this still used?" is one indexed `&&` probe per table at sweep time.

Consequences that fall out for free, rather than being coded:
- Soft delete keeps the row ⇒ references persist ⇒ assets survive. Hard delete removes the row ⇒ assets collectable. **The probe must write no `deleted_at` condition** — that absence IS the rule.
- Restore is free; shared/templated assets survive until the last referencer goes.
- Assets orphaned by an *edit* (image removed, logo replaced, import re-run) are collected too — a delete-path hook would never have caught these.
- The probe is deliberately **not org-scoped**: a body can be pasted across tenants, and the GIN index makes a global probe free.

**Text-regex extraction over a structured Plate walk** is the other key call: every URL contains the literal `kb-assets/{uuid}`, so a new Plate node type with a new URL prop, and assets hiding in a `kb_html` block's raw attributes, are covered with nothing to register. A walker that hasn't been taught about a node under-reports ⇒ deletes live data. (`collectPlateAssetUrls` in `import/kb-plate-assets.ts` still exists for the importer's rewrite pass — different job.)

Two-phase delete: `unreferenced_since` is stamped, and bytes are deleted only a full quarantine window later (default 30d, `KB_ASSET_QUARANTINE_DAYS`). This is the recovery window for a GC that reasons from absence of evidence — a missed referencing surface shows up as marked-but-intact assets instead of permanently lost images. Also `KB_ASSET_UPLOAD_GRACE_HOURS` (24h; an asset is uploaded before the body referencing it is saved) and `KB_ASSET_PENDING_GRACE_HOURS` (6h; reaps presigned-never-confirmed uploads, which the row-at-presign design is what makes findable at all).

**Shipped in `b4f587385` (PR #972).** There is NO hand-written table list: PR review correctly pushed for deriving it, so `KbAssetGcService.referencingTables` filters `em.getMetadata().getAll()` for entities declaring an `assetIds` property (memoized, skips `abstract`/tableName-less). `preview()` returns that list and `kb:asset-gc --dry-run` prints it, so what the probe checked is visible. The spec keeps one enumerated "covers every KB surface" test as the audit anchor. Known accepted gap: a KB asset URL pasted into a ticket reply is not a tracked reference.

Other review outcomes worth remembering: `destroy()` originally wrapped a `SELECT … FOR UPDATE` that was pure theatre (the transaction committed, releasing the lock, before the storage delete began) — deleted, since `unreferenced_since` is written only by the concurrency-1 sweep. `destroy()` and the abandoned-upload reaper collapsed into one `deleteAssets()`; `deleteObject` is just `deleteObjectOrThrow` in a try, so the "strict vs best-effort" split bought nothing. And `state` was dropped as redundant with `confirmed_at`.

Imported KBs are covered: the importer's only asset path is `storeStream`, which takes `orgId` and writes a confirmed row, and its rewritten URLs land in article/homepage bodies, `og_image`, `logo_url` and `settings` — all derived tables. A discarded partial import now reclaims its assets (a 138-article import re-hosts ~824).

STILL OPEN: a backfill for assets uploaded before the migration (they have no row, so they are invisible to the GC forever). Blocked on where `org_id` comes from for an object that is already orphaned, since the storage key does not carry it. Imports are the heaviest asset producer, so this is likely most of what is currently orphaned.

Threading `orgId` into `KbAssetService.presign/confirm/storeBinary/storeStream` also closed a real hole — `confirm` previously accepted any asset id from any org. See [[project_generated_column_drift_and_ordering]] for the schema mechanics.
