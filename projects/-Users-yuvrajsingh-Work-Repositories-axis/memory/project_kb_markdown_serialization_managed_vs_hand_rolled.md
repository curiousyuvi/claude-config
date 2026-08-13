---
name: kb-markdown-serialization-managed-vs-hand-rolled
description: What @platejs/markdown manages vs what the KB must hand-roll on the SERIALIZE path (measured)
metadata: 
  node_type: memory
  type: project
  originSessionId: 4c5af0c9-ed68-43fe-a98c-58a7a45b869f
  modified: 2026-07-30T07:19:22.771Z
---

Measured against `@platejs/markdown@53.2.2` for the KB markdown export (`PlateMarkdownRenderer` + `kb-markdown-rules.ts`). Do not re-derive this.

**Managed, use the option:**
- `plainMarks` (in `SerializeMdOptions`) degrades marks with no Markdown form. Replaced 7 hand-written rules. See `KB_PLAIN_MARKS`: color, backgroundColor, fontSize, fontFamily, fontWeight, comment, suggestion. Each MUST be listed or the library's default emits `mdxJsxTextElement`, which throws (no `remark-mdx`) and 500s the export.

**NOT managed, hand-rolling is justified:**
- Soft breaks. `splitLineBreaks` is **deserialize-only**; there is no serialize equivalent. A literal `\n` in a leaf is a Markdown soft WRAP (renders as a space), so it must become a hard break.
- The library's own `list` rule is BROKEN for this: it drops the break, and for a newline inside a bold leaf emits character references (`* **H&#xA;**&#x44;`). So `kbMarkdownRules` overrides it. The hook is the mdast key **`list`** (it receives the slate `ul`/`ol` node); keying on `li`, `lic`, `ul` or `ol` is NOT dispatched, and remark plugins do NOT run on the serialize path.
- `spread` option only reaches lists the library builds itself, so a rule that builds its own list must set `spread: false` per node or every item is blank-line separated.
- A `break` at the EDGE of a `strong`/`emphasis`/`link` cannot be written as a backslash; hoist it out of the wrapper (what the library's paragraph path does). The editor produces that shape whenever you soft-break while still bold.
- GFM table cells cannot hold an eol, so a break there still degrades to a space; it needs a literal `<br>`. Left unfixed.

Steps/checklist/card-group/columns all use OUR container rules, so the library builds almost no lists here. Related: [[kb-prose-prewrap-invariant]] (the HTML/PDF side is CSS: `white-space: pre-wrap`), [[prefer-library-options]].
