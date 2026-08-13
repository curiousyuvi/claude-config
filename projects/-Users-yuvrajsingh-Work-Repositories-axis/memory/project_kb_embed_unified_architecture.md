---
name: project_kb_embed_unified_architecture
description: KB embeds are unified — one iframe path (no react-lite-youtube-embed); Video node is files-only and provider URLs auto-convert to Embed nodes
metadata: 
  node_type: memory
  type: project
  originSessionId: 8850eb64-57e8-4329-98e8-7b7f3a46d0fe
---

KB embed rendering is unified across editor + published (refactor 2026-07):

- **One iframe path.** `react-lite-youtube-embed` was REMOVED entirely. The editor Embed node (`media-embed-node.tsx`) renders every embed — YouTube, Vimeo, generic — through a single `<iframe src={embed?.url ?? element.url}>` in an `aspect-video` (16:9) box with the reader's sandbox + `strict-origin-when-cross-origin`. `useMediaState` gives the canonical embed URL for providers. Published side is the single `mediaEmbed()` in static-components.ts. Editor ≈ published (both plain iframes).
- **Width + alignment are shared.** `mediaAlignClass(el)` in static-components.ts is used by BOTH `mediaFigure` (img/video/audio) and `mediaEmbed` → `kb-embed kb-align-{left|center|right}` (default center). `.kb-embed` in kb-prose.css shares the `margin:22px auto` + `.kb-align-*` selectors with figures. Editor uses the shared `Resizable` + `usePercentWidth`.
- **INVARIANT: provider video URLs must be Embed nodes, never Video nodes.** The Video block (`KEYS.video`) publishes as a native `<video src>` (mediaFigure), which CANNOT play a youtube/vimeo watch URL → broken. `KbVideoToEmbedKit` (kb-video-to-embed-kit.ts, registered in plate-editor-kit.tsx) is a `normalizeNode` override: any `video` node whose url `parseVideoUrl()` recognizes (youtube/vimeo/youku/dailymotion/coub) is converted `setNodes({ type: KEYS.mediaEmbed })`. The Video node is now files-only (uploads + direct video-file URLs).

Caveat: published reader serves STORED HTML, and kb-prose.css is served fresh — so on deploy, legacy published embeds resized <100% (class `kb-embed`, no align class) shift left→center (they gain no align class until re-published). See [[project_kb_reader_serves_stored_html]] and [[project_kb_youtube_error153_referrer]].
