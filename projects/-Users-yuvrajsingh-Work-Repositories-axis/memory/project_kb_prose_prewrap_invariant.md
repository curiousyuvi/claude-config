---
name: kb-prose-prewrap-invariant
description: ".kb-prose is white-space pre-wrap — soft breaks are literal \\n in text leaves, so nothing may leave FORMATTING whitespace in a leaf"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4c5af0c9-ed68-43fe-a98c-58a7a45b869f
  modified: 2026-07-29T18:51:59.535Z
---

`.kb-prose` (packages/shared/src/styles/kb-prose.css) sets `white-space: pre-wrap` to mirror the editor (Slate's editable is pre-wrap). A soft line break (Shift+Enter) is stored as a literal `\n` inside a text leaf; `serializeHtml` emits it as raw text, never `<br>`, in EVERY block type. The CSS fix is retroactive to already-published stored HTML, no re-publish needed (see [[kb-reader-serves-stored-html]]).

**INVARIANT (two halves, both required):**
1. The renderer must stay minified. Verified: the full showcase fixture renders to 11229 chars with exactly 2 newlines, both `codeLine` trailing newlines inside `<pre>`, 0 multi-space runs, 0 tabs. `<pre>` keeps the UA `white-space: pre` (a cascaded declaration beats an inherited value), so code blocks still scroll. Sanitizer takes no pretty-print option; no post-processing pass injects text; both writers of `variant.html` go through `PlateHtmlRenderer`.
2. **Nothing may leave FORMATTING whitespace inside a text leaf.** This is the half that actually broke. "Imports re-render through the renderer" is NOT sufficient, because an importer can bake source whitespace into the leaf itself, which the minification check cannot see.

Known leak, fixed 2026-07-30 in `markdownToPlate` (`apps/web/src/features/knowledge-base/lib/import-article-content.ts`): a markdown soft wrap means a space, but mdast carries it in the text node's value, so hard-wrapped source gained a break at every wrap column. Fixed with a `remarkCollapseSoftWraps` transformer at the mdast level, the last point where a soft wrap (inside a `text` value) is still distinguishable from a real hard break (a separate `break` node). Fenced code is a different mdast type, so it is untouched. The HTML import path needed nothing: Plate's own deserializer already does `replaceAll(/\n\s*/g, ...)`.

**How to apply:** any NEW path that builds Plate text leaves from an external source must normalize formatting whitespace. Reader goldens carry no newlines in their prose bodies, so they cannot catch this class of bug; pin it at the leaf boundary instead (`import-article-content.test.ts`).

Open follow-up: HTML/PDF export (`export-html-document.ts`) and the KB trash preview render the same stored HTML under their own styles with no `white-space` rule, so soft breaks still collapse there. Not a regression, but the reader and a download now disagree.
