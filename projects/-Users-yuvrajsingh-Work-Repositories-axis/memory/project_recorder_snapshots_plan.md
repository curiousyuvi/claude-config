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

**Build order:** 1 shared types + kb_snapshot Plate node + compiler swap (DONE 2026-09-21) → 2 ingest
REMUX worker, `ffmpeg-static` + `-c copy -cues_to_front 1`, in-place overwrite of video.webm, queue RECORDER_REMUX
(DONE 2026-09-21, user chose remux over re-encode) → 3 render: `packages/snapshot-composition` (TSX, backend only resolves
entry path for @remotion/bundler), `KbSnapshotRenderService` lazy bundle + one browser + serialized, WebP stills/GIF,
inline in article worker via `renderDraftSnapshots` (DONE 2026-09-21; smoke render verified locally; elements/arrows
deferred to the dialog slice; Railway needs Chrome libs + build-time GitHub download for ffmpeg-static, unverified) →
4+5 dialog + elements + GIF (DONE 2026-09-21): SYNCHRONOUS render endpoint `POST /recorder/recordings/:id/snapshots/render`
(no queue/node ids/Ably; dialog writes url into node), `sanitizeSnapshotConfig` rebuilds config (asset URLs must be our
origin), web `components/snapshot/*` with @remotion/player + react-rnd, shared Slider at `src/shared/ui/slider.tsx`.
Preset wallpapers: user chose R2 folder `kb_editor_preset_bgs` (+`thumbs/`) in the public KB asset bucket, populated by
`bin/kb-editor-preset-bgs-publish.ts` from the instantdocs CloudFront (NOT run by me; needs op + a dedicated bucket).
6 (2026-09-21) KB snapshot PRESET (`presets.snapshot`): zoom 1.5x default, zoom centres on the placing click, default background =
first Mac wallpaper resolved by `resolveKbSnapshotBackground` (preset stores `{type:'image'}` with no url; CDN base only known
server-side, also applied in the render sanitizer). `presetBackgroundsBaseUrl` rides the KB settings envelope. Dialog rebuilt as an
inspector + two-thumb GIF range slider; `ColorPickerPopover` promoted to `shared/components` and now backs EVERY ColorField.
Every save = NEW kb-assets uuid (no key reuse); old image orphaned for the asset GC.
UI never visually verified by me. Branch `ys/feat/recorder-snapshot-node`, UNCOMMITTED. → 3 render worker + generation defaults → 4 dialog port (react-rnd) → 5 GIF.

**Why:** the plan says nothing was built; local master had to be pulled to even see the recorder module.
**How to apply:** asset GC needs no registration (kb_extract_asset_ids regexes `kb-assets/{uuid}` in text).
New node touchpoints: shared/schemas, kb-plate-assets assetSlotsOf, static-components, render-plugins,
kb-markdown-rules, plate-translate, web kit + plate-editor-kit. See [[kb-asset-gc-design]].
