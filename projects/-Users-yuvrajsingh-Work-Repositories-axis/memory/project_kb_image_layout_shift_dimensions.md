---
name: project-kb-image-layout-shift-dimensions
description: "Published-KB images/videos shift the page because no intrinsic width/height is stored or emitted; Intercom does this, Zendesk does not"
metadata: 
  node_type: memory
  type: project
  originSessionId: 77ab6d5a-7d22-4f52-8ed4-702edb51c357
  modified: 2026-08-05T08:20:36.461Z
---

The "images paint late and shove the content down" complaint on published KBs is a layout-shift bug,
NOT the CDN (that is [[project_kb_asset_cdn_unsigned_urls]], which only makes them arrive sooner).

Cause: `static-components.ts` emits block images as `createElement('img', { src, alt })` with no
`width`/`height`, and `kb-prose.css` has `.kb-prose figure.kb-image img { width: 100%; height: auto; }`.
With no intrinsic ratio the box is 0px tall until bytes land. Same for `figure.kb-video video`. The
embed block does NOT shift because it has a real CSS 16:9 aspect box.

Blocker was: nothing stores intrinsic dimensions. `kb_assets` has only `contentType`/`sizeBytes`, and the
Plate image node stores `url`/`alt`/`align` plus `width` as an author-resize PERCENTAGE.

FIXED on `ys/feat/kb-asset-cdn` (2026-08-05) by measuring in the browser at insert time: the media node
gained `naturalWidth`/`naturalHeight` (validated by `kbMediaDimensions` in `packages/shared/src/schemas/
kb-nodes.ts`), written by `apps/web/src/shared/editor/kb-media-dimensions.ts` fire-and-forget after the
insert, emitted as the `width`/`height` attribute pair by `mediaFigure` in `static-components.ts`. Video
also gets `--kb-media-ratio` on the figure (sanitizer-allowlisted) because the `/_kb/video.js` island
swaps `<video>` for a `<media-controller>` that carries no dimension attributes.

Coverage is NOT retroactive and there is no backfill: media inserted before this, and imported media,
publishes unmeasured and still shifts. Re-inserting is the only cure. Same as Intercom (below).

Competitor evidence (fetched + parsed 2026-08-04, not from memory):
- **Intercom does it.** Every editor-uploaded article image carries raw intrinsic dims, e.g.
  `width="3436" height="2004"`. Older Google-Docs-pasted images (`AD_4nX…`) lack them, so their coverage
  is not retroactive either. No srcset, no lazy loading, no aspect-ratio CSS — the attributes are the
  whole mechanism.
- **Zendesk does not.** Article images carry an author-chosen `width` (250/350/500/600) and never
  `height`, so their help centers shift the same way ours does.
