---
name: project_kb_reader_serves_stored_html
description: "Published KB reader + ticket panel serve STORED publish-time HTML, not on-the-fly render — backend rendering changes need a re-publish to appear"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8850eb64-57e8-4329-98e8-7b7f3a46d0fe
---

The published KB reader (`kb-public` module, e.g. `https://<slug>.helply-kb.localhost/doc/<slug>`) and the ticket KB panel (`kb-article-view.tsx` → `article.html` via `dangerouslySetInnerHTML`) both serve **HTML generated + sanitized at publish time** (`PlateHtmlRenderer` + `sanitizeKbHtml` → stored). They do NOT re-render per request.

Consequence: a change to the backend render/sanitize pipeline (static-components.ts / sanitize-kb-html.ts / kb-prose.css classes) does **not** change an already-published article until it is **re-published**. To verify such a change against an existing published article, re-publish it (or hard-refresh after re-publish), don't just reload the URL.

Local check trick: `curl -sk <published-url>` and grep the served `<iframe>`/`.kb-embed` markup — shows the last-published HTML exactly.

Also handy for local visual checks: `node_modules/.bin/playwright screenshot --ignore-https-errors --full-page <url> out.png` works for URL screenshots, but the `playwright`/`playwright-core` module is NOT script-resolvable via `require` in this pnpm repo (bin-only), so a scripted login flow can't `import` it easily. chromium `headless_shell` also won't render YouTube's player (embeds show blank). See [[project_local_verify_login]].
