---
name: recorder-snapshots-plan
description: Recorder snapshots (real stills/GIFs replacing [snapshot@] placeholders in generated KB articles) — decisions, open questions, build order; work started 2026-09-21
metadata:
  type: project
---

Plan handoff PDF: ~/Downloads/recorder-snapshots-plan.pdf (written 2026-09-20). Reference impl is the
instantdocs repo at ~/Work/Repositories/instantdocs (snapshot block src/blocknote/blocks/snapshot.tsx,
element schema src/remotion-v2/helpers/schema.ts, dialog src/components/snapshot-*.tsx).

**Decided:** Remotion rendered locally in a BullMQ worker (renderStill/renderMedia, no Lambda; Axis already
pays a Remotion subscription). Render at snapshot SAVE, never at publish (kills all instantdocs optimistic-
publish machinery, do not port it). GIF in v1. Article generation pre-renders defaults before READY.
Ingest re-encodes webm (VP9, no Cues) to H.264 MP4 once at upload. Recordings deleted 30 days after no
snapshot node references them (generated recording_ids column, mirrors asset GC). No video/voiceover.

**Open:** confirm full re-encode vs remux (CORRECTION 2026-09-21: the plan's "Remotion slow VP9 extraction" rationale for a full re-encode is obsolete; Remotion's page says the slow path is gone since v4 and only ever hit VP8+PNG, so a `-c copy` remux adding Cues/Duration is the real requirement; re-encode is then only about MP4 compatibility/GOP); one asset across locales (leaning yes); GIF-only vs +WebP;
element selection via react-rnd overlay hit-test vs postMessage; output width (assume 1280 capped).

**Build order:** 1 shared types + kb_snapshot Plate node + compiler swap (STARTED 2026-09-21) → 2 ingest
re-encode worker → 3 render worker + generation defaults → 4 dialog port (react-rnd) → 5 GIF.

**Why:** the plan says nothing was built; local master had to be pulled to even see the recorder module.
**How to apply:** asset GC needs no registration (kb_extract_asset_ids regexes `kb-assets/{uuid}` in text).
New node touchpoints: shared/schemas, kb-plate-assets assetSlotsOf, static-components, render-plugins,
kb-markdown-rules, plate-translate, web kit + plate-editor-kit. See [[kb-asset-gc-design]].
