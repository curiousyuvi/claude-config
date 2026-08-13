---
name: kb-prose-css-golden-snapshot
description: "Editing packages/shared/src/styles/kb-prose.css breaks 12 kb-reader.golden.spec.ts snapshots — the reader inlines the stylesheet, so regenerate with vitest -u"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5dae7ddb-0438-490a-8169-fab0f2ec4edb
  modified: 2026-07-29T09:32:58.280Z
---

Any edit to `packages/shared/src/styles/kb-prose.css` (or the other reader stylesheets behind `kb-reader-styles.ts`) fails the 12 snapshots in `apps/backend/src/modules/kb-public/application/kb-reader.golden.spec.ts`, because that spec byte-pins the FULL reader HTML and the reader inlines the stylesheet.

**Why:** the golden spec is a deliberate exact-output oracle for the SSR reader (served verbatim under a strict CSP), so it catches unintended markup changes — including stylesheet ones. Nothing in the `knowledge-base` module's own tests covers it, so a CSS-only change looks green until CI runs the `kb-public` suite.

**How to apply:** after touching reader CSS, run
`pnpm vitest run src/modules/kb-public/application/kb-reader.golden.spec.ts -u` from `apps/backend`,
then confirm the snapshot diff contains ONLY your intended rules:
`git diff -U0 -- apps/backend/src/modules/kb-public | grep -E '^[+-]' | sort -u`.
Comments in the CSS ship to every reader page verbatim (the stylesheet is not minified), so keep them tight.

Related: [[kb-html-block-srcdoc-sandbox]]
