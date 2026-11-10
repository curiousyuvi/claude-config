---
name: project-capture-unified-block-model
description: "Follow-up PR after #2026 — one KB block model for the capture planner and review (reviewer point 1), designed but not started"
metadata:
  node_type: memory
  type: project
  originSessionId: f52b7cfa-40e4-4905-aaed-8f32ce04ad40
  modified: 2026-11-10T13:36:09.562Z
---

Follow-up PR to #2026 (decided 2026-11-10): reviewer skinnyiam's point 1, "planner and reviewer read the article through two block models". User agreed it goes in its own PR. Nothing coded yet.

Design I settled on after reading the code:
- `kbMdxBlocks(nodes, { firstNumber, eachListItem, inContainers })` in knowledge-base `ai-format/kb-mdx-edits.ts`. Defaults keep gap drafts byte-identical (list runs merged, only accordion items nested). Capture passes both options.
- `KbMdxBlock` gains `path`; `items` become the nearest blocks inside (accordion items always; callout / kb_accordion_body / column children with `inContainers`), pre-order numbering like accordion items today.
- Rendering: `toKbMdx(nodes, assets, nested)` wraps a nested block as a real `mdxJsxFlowElement` named `block` in the mdast tree (no marker string). The old "first line + items + last line" trick can't reach an accordion answer, which sits after its summary.
- `applyKbMdxEdits`: generic `withItems` rebuilds a container from its edited children by path at any depth; emptied accordion dropped, emptied free container keeps an empty paragraph; identity kept when nothing changed.
- Capture: `PictureBlock` = KbMdxBlock; `pictureBlocks` = kbMdxBlocks with both options; delete renderPictureBlocks/renderNode/hasInner/MARKER; `blockLists` returns only lists whose parent is the root or a free container (no slots after an accordion item, an img there breaks the doc); `allBlocks` walks everything; the review uses `pictureBlocks` too, so ids agree.
- Needs a full eval round: planner and review inputs change (pre-order ids, accordion item tags).

**Why:** removes the string splice and the parallel tree, and lets the review edit inside callouts/columns instead of rewriting whole containers with keepMedia:false. **How to apply:** start here when the user opens the follow-up; see [[project-capture-article-review-design]].
