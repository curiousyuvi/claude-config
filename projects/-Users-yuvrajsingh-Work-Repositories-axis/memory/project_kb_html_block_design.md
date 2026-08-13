---
name: kb-html-block-srcdoc-sandbox
description: "KB \"HTML\" block (kb_html) renders author HTML in a script-less sandboxed srcdoc iframe on both sides; scripts can never run (CSP inheritance), editor measures height via allow-same-origin WITHOUT allow-scripts"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5dae7ddb-0438-490a-8169-fab0f2ec4edb
  modified: 2026-07-29T09:13:13.908Z
---

The KB editor's "HTML" block (`kb_html`, ported from InstantDocs' `customHTML`, added 2026-07-29) renders the author's raw fragment inside a `srcdoc` iframe on BOTH sides via the shared `kbHtmlSrcdoc()` builder in `packages/shared/src/kb-embed.ts`.

**Why:** WYSIWYG with full CSS isolation, without weakening the publish sanitizer. Key physics: a srcdoc document inherits the embedding page's CSP, and the published reader's CSP has no inline `script-src` — so scripts in custom HTML could never run on the published page. The design therefore makes "HTML + CSS, no scripts" the uniform contract via sandbox flags instead of a per-KB surprise.

**How to apply:**
- `KB_HTML_IFRAME_SANDBOX` (published, forced by `sanitize-kb-html.ts` on ANY iframe carrying `srcdoc`; `src` is dropped there) = `allow-popups allow-popups-to-escape-sandbox` — no scripts, no origin. Never give a srcdoc iframe the embed sandbox: its `allow-same-origin` would be stored XSS in the reader and the agent app's KB panel.
- `KB_HTML_EDITOR_IFRAME_SANDBOX` adds `allow-same-origin` ONLY so the editor can read `contentDocument` and persist the measured `height` node prop (a fully sandboxed frame can't self-report size; published iframe is a fixed-height box). Safe solely because scripts stay off — never pair it with `allow-scripts`.
- Node contract in `packages/shared/src/schemas/kb-nodes.ts` (`KbHtmlNode { html, height }`); editor kit `custom-html-kit.tsx`; importer maps `customHTML` (drops InstantDocs' pencil-placeholder markup); markdown rule emits a raw mdast `html` node.
- **LANDMINE: Plate's `serializeHtml` entity-DECODES its whole react-dom output** (`decode(renderToStaticMarkup(...))` in @platejs/core static) — any attribute value containing quotes/markup (an `srcdoc`, or the automatic `data-slate-<prop>` dump of node props) is emitted with RAW quotes and shatters the published document. Author HTML must therefore go AROUND the react render: `kb-html-slots.ts` (`extractKbHtmlSlots` strips html/height pre-render → static component emits an empty `kb-htmlslot-N` placeholder div → `injectKbHtmlSlots` swaps in the iframe with self-escaped srcdoc post-sanitize, inside `PlateHtmlRenderer.render`). Same trap awaits any future node prop that can contain a `"` (e.g. quotes in an equation's `texExpression`).
- Articles published while a rendering bug was live serve the broken STORED html — fixes need a re-publish to show.
- The srcdoc declares `color-scheme:light dark`: a dark-scheme embedder (the app sets `color-scheme:dark` on `<html>` in dark mode) + a light-only iframe doc makes the browser paint an opaque WHITE backdrop behind the frame; declaring both schemes keeps it transparent so the block sits on the page background in both themes (the reader never declares a scheme, so published was always fine).

Related: [[project_kb_reader_serves_stored_html]], [[project_kb_embed_unified_architecture]]
