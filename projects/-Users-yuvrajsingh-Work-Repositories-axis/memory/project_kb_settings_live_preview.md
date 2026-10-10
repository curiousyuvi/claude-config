---
name: project_kb_settings_live_preview
description: "KB settings live preview + /search page removal — PR GrooveHQ/axis#1648 MERGED (by 2026-10-10)"
metadata:
  node_type: memory
  type: project
  originSessionId: 4339431e-433d-4efe-89ab-6d716a453cb6
  modified: 2026-10-07T15:37:19.598Z
---

Live preview panel on KB settings showing unsaved edits, plus removal of the SSR `/search` results page. PR GrooveHQ/axis#1648 (single commit, rebased on master fd14b710d). Wiki: `wiki/pages/kb-settings-live-preview.md`.

**Why:** GitBook/Shopify round-trip each change to a server renderer; ours already runs in workerd, so the browser renders with `kb-public/reader/renderPage` into double-buffered `srcDoc` iframes.

**How to apply:**
- Store `preview/kb-preview-store.ts` holds `unsaved: Record<cardId, KbPreviewDraft | null>` — one registration per `KbSettingsCard` (by-value draft key); drives both the preview and `hasUnsavedSettings` (leave-page guard in the settings shell).
- Preview = `diffSettings` + shared `mergeKbSettingsPatch` + schema, so preview equals save. Server only for routing: `GET .../settings/preview` via `KbReaderService.withSettingsPatch` (`KbSettingsOverlayData`); audience = `publishedAudience`.
- Frame swaps go through the `frame-buffer.ts` reducer (only the wanted, loaded page is shown) — fixed the "stuck after toggling back" bug the user hit.
- Web imports the backend reader ONLY via `features/knowledge-base/lib/kb-reader.ts`.
- /search removed with 4 microcopy labels; no artifact bump (old worker falls back to default labels). `search` is no longer a reserved URL segment.
- Remaining: CI green, user's screenshots, review. React Doctor diff warnings left are pre-existing lines in kb-link-list-card / kb-social-card.
Related: [[project_kb_article_prepublish_preview]], [[project_kb_edge_render_redesign]].
