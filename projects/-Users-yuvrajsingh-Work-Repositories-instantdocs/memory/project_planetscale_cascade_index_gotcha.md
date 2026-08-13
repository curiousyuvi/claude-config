---
name: planetscale-cascade-index-gotcha
description: "relationMode=prisma page/KB deletes hit Vitess 3024 two ways: unindexed inbound FK full scan, and large indexed SetNull/Cascade writes needing pre-drain"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4f7562c3-c4bf-45b5-b43b-a9e716429127
  modified: 2026-08-06T11:40:48.785Z
---

On InstantDocs (PlanetScale, `relationMode = "prisma"`), there are no DB foreign keys — Prisma emulates referential actions app-side. Deleting a Page/KB therefore issues a DELETE/UPDATE against **every model with a relation pointing at it**, including `onDelete: SetNull`. If that inbound FK column is **unindexed** on a large table, the statement does a full-table scan and trips the Vitess deadline (`code = 3024`, message "Canceled") — **even when it matches zero rows**.

This caused the recurring `cron.deleteTrashItems` failures (the cron now runs on the Railway long-task worker via `/api/tasks/delete-trash-items`, dispatched from Vercel). The culprit both times was `PublishedSessionAnalytics.firstPageId` (an `onDelete: SetNull` relation to Page). A red herring along the way: `EditingSession.pageId` looked unindexed but is `@unique` (so already indexed).

**Indexing it was necessary but NOT sufficient.** June 2026 added `@@index([firstPageId])`, which fixed the zero-row full scans. It kept failing for pages with real volume, because the emulated SetNull is still a single `UPDATE` over every matching row inside the page's delete transaction — seekable is not the same as small. Page `cmp3955wu000h1leutr8se4pd` had 6,962 session rows and failed every nightly run from June 23 to Aug 6 2026. Fixed Aug 2026 by adding a step 5 to `deletePageSubtree` in `src/server/helper/trash.ts` that nulls `firstPageId` in `ROW_DELETE_BATCH` chunks before deleting the page. After draining, the delete took 9.4s.

Second trap: `withVitessRetry` classifies 3024 as transient and retries 3x, then `deletePagesInBatches` falls back to per-id and retries 3x more. This failure is deterministic, so the retries only ever burn time and make one stuck row look like a flaky infra problem in Sentry.

**Why:** a 3024 on a delete has two distinct causes that look identical — a missing-index full scan (row count for the failing id is 0, the tell) and a genuinely large indexed write inside the emulated-cascade transaction. Fixing only the first leaves the second live.
**How to apply:** when a Page/KB delete throws Vitess 3024, count the actual rows for the failing id in every model with a relation TO the deleted model — `Cascade` *and* `SetNull`/`NoAction`. Zero rows means missing index; thousands means it needs pre-draining in `deletePageSubtree` (delete for Cascade, null the FK for SetNull — SetNull rows are usually analytics history that should outlive the page). Field-level `@unique` counts as an index. See [[feedback_prisma_types]] for regenerating types after schema edits.
