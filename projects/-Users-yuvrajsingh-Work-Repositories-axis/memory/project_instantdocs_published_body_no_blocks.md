---
name: project-instantdocs-published-body-no-blocks
description: "InstantDocs keeps NO block snapshot of a published article, so the KB import CANNOT reproduce an edited-after-publish article's live body — accepted limitation, do not try to solve it again"
metadata: 
  node_type: memory
  type: project
  originSessionId: 57cdaa6a-48d9-4a87-8277-dfa1e8e5fc84
  modified: 2026-07-30T13:20:47.585Z
---

Measured against the InstantDocs dev DB on 2026-07-30, while trying to make the Axis KB import reproduce the
"published with unpublished changes" state:

- `PublishedPage.optimisticBlocksContent` is **NULL for ordinary published articles**. Only the async
  video-publish path in `src/server/helper/publish.ts` (~L1892) writes it; the main path
  (`publishOnlyArtilceGuide`, ~L662) and `save-published-article` write `publishedHTML` only. It is a
  preview-while-rendering field (readers surface it only when `isHTMLRendering`), not a snapshot.
- So **there is no block-level record of what InstantDocs published.** The live body exists only as
  `publishedHTML`, which is baked presentation (hljs spans, KaTeX, `iconify-icon`, `details`,
  Tailwind step/card divs) and cannot be turned back into blocks for anything but plain prose.
- Net effect on the import, accepted deliberately (2026-07-30, Yuvraj's call): an edited-after-publish
  article lands in Axis with the DRAFT body live and no pending-changes state, because the draft is the only
  body the export can supply. **Do not re-attempt an HTML→Plate rebuild for this** — it was built, reviewed
  and reverted as not worth the lossiness.
- If it ever needs solving, the fix belongs on the InstantDocs side: persist the published blocks in every
  publish path. Only helps articles published after that ships.
- Useful measurement: `Page.htmlContent` vs `PublishedPage.publishedHTML` IS an exact dirty test (same
  renderer wrote both; `save-page` refreshes `htmlContent` on every save) — byte-equal on a clean article,
  differing on a dirty one. Better than `Page.modified` (any save sets it) or comparing block JSON (flagged
  127/138 on a real migration).
- Recipes: the KB-import bearer token IS `instantdocs.presharedKey`, so
  `curl -k https://kb.helply.localhost/api/axis/kbs/<kbId>/export?locale= -H "Authorization: Bearer <key>_<workspaceId>"`
  dumps the whole export payload. InstantDocs' DB is a remote PlanetScale branch — a throwaway `tsx` script
  at the repo root with `new PrismaClient()` is the quickest read-only look.

See [[project_kb_import_instantdocs_contract]].
