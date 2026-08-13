---
name: feedback_reader_match_instantdocs
description: "Published-KB reader's visual design must match InstantDocs' published look, not a fresh/default skin"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f77596b0-3faf-495c-b304-f5fb513ff117
---

The native published-KB reader (server-rendered, see [[project_kb_native_in_axis]]) must visually match the **InstantDocs published KB site**, not a clean-default design. Yuvraj reviewed the first reader render (Slice 3 preview pages) and said it "looks very different from what I had in instantdocs repo."

**Why:** the reader is the product's public face; the InstantDocs look is the proven, expected design.
**Fidelity bar (Yuvraj chose "nudge closer, keep structure", NOT a strict port):** keep the current renderer structure (`apps/backend/src/modules/kb-public/kb-page-renderer.service.ts` + `kb-reader-styles.ts`) and move spacing/cards/typography/colors/hero/sidebar toward the InstantDocs published look — referencing `instantdocs` repo `src/components/published-*` + `src/helper/kb-and-guide-styling.ts` — without a pixel-faithful port.
**When:** deferred — Yuvraj chose to continue the caching/SEO spine (Slices 4-5) first; do the nudge during reader polish.
