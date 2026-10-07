---
name: project_kb_settings_live_preview
description: "KB settings live preview (unsaved edits) — BUILT on ys/feat/kb-settings-live-preview (2026-10-07), uncommitted, awaiting user visual check + commit permission"
metadata:
  node_type: memory
  type: project
  originSessionId: 4339431e-433d-4efe-89ab-6d716a453cb6
  modified: 2026-10-07T13:04:55.279Z
---

Live preview panel on KB settings showing unsaved edits. Built 2026-10-07 on branch `ys/feat/kb-settings-live-preview` (uncommitted). Wiki: `wiki/pages/kb-settings-live-preview.md`.

**Why:** GitBook/Shopify round-trip each change to a server renderer; ours already runs in workerd, so the browser renders with `kb-public/reader/renderPage` into double-buffered `srcDoc` iframes.

**How to apply:**
- Draft = what Save writes (`settingsDraft(next)` / Logo / Text kinds) published by `KbSettingsCard` `preview`+`region` props into `preview/kb-preview-store.ts`; preview = `diffSettings` + shared `mergeKbSettingsPatch` + schema, so preview equals save.
- Server only for routing: `GET .../settings/preview` via `KbReaderService.withSettingsPatch` (`KbSettingsOverlayData` overrides `kbShell`; `KbShell` now carries parsed `settings`). Audience = `publishedAudience` (shared with baker).
- `RenderContext.preview` is now `KbPreviewKind` (ArticleDraft gets the banner; any preview skips custom code + analytics).
- `/_kb/*` served on app host; app CSP allows Google Fonts (srcDoc inherits CSP).
- Remaining: user's visual check, commit/PR with permission, react-doctor diff gate after commit. Lazy chunk 507 KB/135 KB gzip. Web build needs NODE_OPTIONS=--max-old-space-size=8192 locally (CI sets it).
Related: [[project_kb_article_prepublish_preview]], [[project_kb_edge_render_redesign]].
