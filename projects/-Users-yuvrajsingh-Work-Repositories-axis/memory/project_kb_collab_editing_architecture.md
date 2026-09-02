---
name: project_kb_collab_editing_architecture
description: "KB realtime collaborative editing (article + custom homepage) — Yjs via @platejs/yjs over a custom Ably provider, collabState bytea persistence, kb_node.changed popover event; decisions and gotchas"
metadata: 
  node_type: memory
  type: project
  originSessionId: 895c88d9-690d-464e-8e95-bf5a1686d6b1
  modified: 2026-09-02T14:36:28.468Z
---

Built 2026-09-02 on branch `ys/feat/realtime-article-editing` (uncommitted at time of writing). Plate's recommended path is `YjsPlugin` + Hocuspocus/WebRTC; we chose `@platejs/yjs` with a **custom provider instance over Ably** (`apps/web/src/features/knowledge-base/lib/collab/ably-yjs-provider.ts`) because Ably token auth, channel leases, presence and CSP already exist and a Hocuspocus WS server on Railway would need sticky routing or a Redis extension.

**Why/how it hangs together:**
- Channel `org:{orgId}:kbcollab:{anchorType}:{id}:{locale}`; token grants `publish` ONLY on `kbcollab:*` (clients must never publish on `kb:*` event channels). Wire: `u` update, `q` state vector, `d` diff, `a` awareness; chunked above 32 KB as `c:<kind>:<id>:<i>:<n>`.
- Persistence = existing autosave + new `collabState` (base64 `Y.encodeStateAsUpdate`) → `bytea` columns on `kb_article_variants` and `kb_homepage_variants` (migration `Migration20260902142020`). Joiner applies stored state BEFORE connecting; any non-collab `content` writer nulls `collabState` (article.service, homepage upsert, translation worker); editors re-seed via Plate's deterministic seed (`slateToDeterministicYjsState`, guid = `${anchorType}:${id}:${locale}`).
- Homepage upsert SKIPS the OCC version check when `draft.collabState` is present (peers are CRDT-merged).
- **`@platejs/yjs` init gotcha:** for provider *instances* the plugin does not wire `onSyncChange`, so `init({autoConnect:true})` waits its 5s sync timeout before seeding. We call `init({autoConnect:false})` then `provider.connect()`, and set `_isSynced/_isConnected` via provider callbacks ourselves.
- **Local vs remote edits:** slate-yjs flushes local ops into the Y.Doc (firing `update`) before Plate's `onChange` runs; the shell flags that and passes `{ remote }` to `onContentChange`. Only local edits (and the provider's `onLocalUpdate`) schedule a save.
- `@platejs/yjs` statically imports `@hocuspocus/provider`, `y-webrtc`, `y-indexeddb` → they had to be installed even though unused (bundle cost accepted; alternative is using `@slate-yjs/core` directly).
- `KbCollabUser` must be a `type` alias, not an `interface` (slate-yjs cursor data bound is `Record<string, unknown>`).
- Publish popover realtime = `kb_node.changed` outbox event (`KbNodeChangeAction` updated/published/unpublished/review_changed) via `kb-node-realtime.publisher.ts`; body-only saves don't publish unless dirty flipped or an approval dropped (`dropApprovedKbReview` now returns boolean). Consumer `KbNodeRealtimeBridge`.
- **Two bugs found only by a two-tab headless probe (2026-09-02), both silent:** (1) React StrictMode's double effect run: the plugin's `destroy()` called the provider's destroy, which removed doc/awareness listeners and nulled the local awareness state; y-protocols' `setLocalStateField` is a no-op on a null state, so nothing was ever published. Fix: provider listeners live for the session, `disconnect` restores local awareness state, and the session is built in an effect (fresh per mount) with `undefined` = pending. (2) **Ably rejects above 50 msgs/s per channel** (`channel.maxRate`); one `u` + one `a` per keystroke hit it, and a dropped `u` strands every later update on the receiver. Fix: merge updates per 100ms with retry-on-reject, throttle awareness to 200ms. Probe pattern: login at inbox.helply.localhost → `/seed-organization/kb/<kb>/<article>`, two browser contexts, type in A, read B's editor text; redo it before claiming collab works.
- **Non-body realtime (2026-09-02 later):** `publishKbNodeChanged` takes an explicit `anchorType/anchorId` (article | collection | knowledge_base) and nullable `locale`. `updated` is published directly from article, collection, article-variant, collection-variant, homepage services; `tree_changed` is published ONCE from `KbEventsWorkerService.handleJob` for the structural domain events set (`TREE_EVENTS`) — covers create/move/duplicate/delete/restore/bulk/trash/import without touching producers, at the cost of queue latency and no own-tab suppression (worker has no request context). Consumers: `KbNodeRealtimeBridge({kbId, anchorType, anchorId})` per open node and `KbTreeRealtimeBridge({kbId})` in `KbWorkspaceShell`. `KbPageHeader`'s AutoTextarea now adopts a remote `value` when idle (no pending edit, not focused). **Local-dev caveat:** everything except Yjs body sync rides `ably_realtime_outbox`, so it is invisible locally until the Ably Postgres connector tunnel is set up (wiki `ably-realtime-db-setup.md`).
- Translation-variant editor (`KbArticleVariantEditor`) is NOT collaborative yet — shell supports `collab` prop, so wiring it is small.

**How to apply:** touch collab only through the provider/hook; never give clients publish on `kb:*`; keep `collabState` nulling in every new backend `content` writer. Verify visually with two browsers on the same article (user does the looking).

Related: [[project_kb_comments_architecture]] [[project_mikroorm_snapshot_merge_corruption]] [[feedback_no_visual_verification]]
