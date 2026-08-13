---
name: project_kb_youtube_error153_referrer
description: "YouTube \"Error 153\" in published KB/panel embeds is caused by iframe referrerpolicy=no-referrer; fix = strict-origin-when-cross-origin"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8850eb64-57e8-4329-98e8-7b7f3a46d0fe
---

YouTube embed shows **"Error 153 / Video player configuration error"** in the published KB reader and the ticket KB panel (but works in the editor). Cause: the embed `<iframe>` had `referrerpolicy="no-referrer"`, which strips the Referer; YouTube's player needs a Referer to identify the embedding host (`errorCode: embedder.identity.missing.referrer`). Google's YouTube API terms explicitly forbid the `noreferrer` feature and recommend `strict-origin-when-cross-origin` (origin-only, no path — privacy-preserving).

The **element-level** iframe `referrerpolicy` attribute overrides the page-level `Referrer-Policy` header (which was already the correct `strict-origin-when-cross-origin`). The editor works because it renders YouTube via `react-lite-youtube-embed`, whose iframe defaults to `strict-origin-when-cross-origin`.

Fix location (TWO backend consts must stay in sync): `sanitize-kb-html.ts` `IFRAME_REFERRER_POLICY` (the security boundary — `transformTags.iframe` force-sets it on EVERY iframe) AND `static-components.ts` `EMBED_REFERRER_POLICY`. The editor's generic-embed branch in `media-embed-node.tsx` had the same `no-referrer` and was aligned too. Do NOT change the unrelated `Referrer-Policy: no-referrer` HTTP headers on attachment/inline-image responses (inline-attachment.controller.ts, presigned-image-asset.service.ts) — different concern. See [[project_kb_panel_published_only]] and [[project_kb_reader_serves_stored_html]].
