---
name: project_kb_reader_preact
description: "Published-KB reader architecture + the Preact-for-the-search-island perf opportunity (Konrad discussion, PR #589)"
metadata: 
  node_type: memory
  type: project
  originSessionId: f77596b0-3faf-495c-b304-f5fb513ff117
---

The published-KB reader (Axis backend, `apps/backend/src/modules/kb-public`) is **server-rendered static HTML** via `renderToStaticMarkup` (`kb-reader-jsx.tsx` orchestrator + `kb-reader-{icons,shared,heads,chrome,bodies}.tsx` — split in PR #589). No hydration, no client framework on the page; interactivity is small vanilla-TS `<script defer>` islands (TOC, sidebar, analytics) served under CSP `script-src 'self'`.

The **one exception**: the search island (`apps/web/src/published-search/index.tsx`, built separately via `vite.kb-search.config.ts` / `build:kb-search`) is a real **React app** (`createRoot` + hooks — inline dropdown + modal). It ships React 19 + react-dom/client ≈ **~45 KB gzip** on every KB page.

**Open perf idea (raised by Konrad, 2026-07-01):** swap that island to **`preact/compat`** — a one-line `resolve.alias` in `vite.kb-search.config.ts` only. Source stays React; the main TanStack SPA is untouched (separate build); drops the island runtime to **~6–8 KB gzip** (~40 KB/page saved). Caveat: preact/compat ≠ 100% React on concurrent/Suspense edge cases — validate with a real before/after build + smoke-test the dropdown/modal before committing. Not yet decided/built. See [[project_kb_native_in_axis]].

Reader output is exact-output-sensitive (served verbatim under strict CSP) — `kb-reader.golden.spec.ts` pins the full HTML per layout×page-type; treat any snapshot diff as a real change.
