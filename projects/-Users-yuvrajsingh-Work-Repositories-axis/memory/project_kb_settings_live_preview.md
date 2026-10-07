---
name: project_kb_settings_live_preview
description: "KB settings live preview (unsaved changes) — client-side render with the edge reader; full scope, no v1; plan awaiting user review (2026-10-07)"
metadata:
  node_type: memory
  type: project
  originSessionId: 4339431e-433d-4efe-89ab-6d716a453cb6
  modified: 2026-10-07T09:19:10.232Z
---

Live preview panel on KB settings showing unsaved edits. Direction chosen 2026-10-07: render in the browser with the same pure reader (`kb-public/reader/renderPage`) kb-edge uses, into `<iframe srcDoc>`; server only supplies the resolved view JSON per path. User said NO v1: logo, custom homepage, locales, in-preview navigation all in scope. Plan written in chat, user reviews before any code.

**Why:** GitBook/Shopify round-trip each change to a server renderer because theirs can't run client-side; ours already runs in workerd, so it runs in a browser.

**How to apply:** draft overlay is `(kb: ReaderKbMeta) => ReaderKbMeta`, composed from every dirty card (settings envelope, KB entity logo, per-locale text). Open spikes: Vite importing backend reader files, root-relative `/_kb/*` scripts dead in srcDoc. Related: [[project_kb_article_prepublish_preview]], [[project_kb_edge_render_redesign]].
