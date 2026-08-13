---
name: kb-reader-template-parts-split
description: "KB reader composes via template + parts (render once, then split); React 19 hoists head tags so the head slot needs <meta> sentinels"
metadata: 
  node_type: memory
  type: project
  originSessionId: ea441c8c-9d1f-4fc1-9ef3-73ac33678184
  modified: 2026-08-08T05:23:34.484Z
---

Slice 1 of [[kb-published-r2-worker-caching]] landed 2026-08-08: `KbPageRenderer.render()` is now `stitchKbPage(...renderParts())`. `renderPage` deleted — one compose path for published pages, preview, and future origin fallback.

**The technique that made it byte-safe:** render the page ONCE with sentinel elements bracketing each page-varying region, then `splitKbPageParts` lifts them out. Stitching is the exact inverse of splitting, so byte-identity is structural — not two render paths that happen to agree. All 12 goldens passed with no `-u` and no snapshot churn.

**React 19 gotcha (cost a debugging cycle):** `renderToStaticMarkup` hoists `<title>`/`<meta>`/`<link>` to the top of `<head>`. A `<span>` sentinel around the per-page head run gets left behind bracketing NOTHING — head part empty, all hreflang stranded in the template. Fix: head slot uses `<meta>` sentinels (hoisted *with* the tags they delimit, preserving source order); every other slot uses `<span>` because a `<meta>` in `<body>` would itself hoist away. See `SENTINEL_TAG` in `kb-reader-slots.tsx`. The goldens stayed GREEN through this bug (stitched output was unchanged) — only the template-invariance test caught it, which is why that test is the real gate, not the goldens.

**All 3 layouts covered** (documentation / modern_help_center / classic_help_center) across home+article+collection. NON-OBVIOUS: **classic and modern share the help-center chrome** — classic branches only inside `kb-reader-bodies.tsx` (i.e. inside the `body` slot), so their TEMPLATES are byte-equal by design; only the home body differs. A test pins this. Layout switch in settings is safe: `KbSettingsService` emits `KB_UPDATED` (only on a real change) → `KbArtifactScope.Kb` → full rebake; doc→help-center also drops the `nav` part.

**Template identity = KB + locale + LAYOUT** (not per KB). Slots: `head`, `nav`, `body`, `lang`. Three things force content out of the template: the language switcher links to the current route; a doc/collection page narrows `availableLocales` to the locales that node is published in (can delete the whole documentation sidebar footer, so the slot wraps `SidebarFooter` whole, not the switcher); `<main>`/island class lists vary by page kind + TOC presence.

Files: `packages/shared/src/kb-page-parts.ts` (shared with future worker), `kb-reader-slots.tsx`, `kb-page-parts.spec.ts`. Asset-CDN rewrite runs per part — its regex is anchored to attribute/`url()` delimiters so it can't span a boundary. Search page + 404 render whole (`KbSlot` is a no-op outside the `KbSlotCapture` provider). Related: [[kb-prose-prewrap-invariant]], [[kb-prose-css-golden-snapshot]].
