---
name: project_kb_reader_offline_render_verify
description: How to render + visually verify the published KB reader WITHOUT Docker/DB/sandbox
metadata: 
  node_type: memory
  type: project
  originSessionId: e2d6bdd1-c1eb-4450-96a2-d76764ad9a98
  modified: 2026-08-04T16:53:02.050Z
---

The published KB reader (`apps/backend/src/modules/kb-public/application`) is server-rendered HTML with an INLINED stylesheet — so you can render + screenshot it fully offline, no OrbStack Postgres, no `bin/sandbox`, no `pnpm dev`. Fast + laptop-friendly.

**Render:** `KbPageRenderer` (`kb-page-renderer.service.ts`) still renders with no DB, but as of 2026-08-04 it takes a `ConfigService` — construct it as `new KbPageRenderer(new ConfigService({}))` (an empty config also means the asset-CDN rewrite is inert; see [[project_kb_asset_cdn_unsigned_urls]]). `.render(view, ctx)` / `.renderSearch` / `.renderNotFound` return full HTML strings from plain view fixtures (no DB). Copy the fixture builders from `kb-reader.golden.spec.ts` (kbMeta/node/homeView/docView/collectionView/searchView). Run a script with the backend SWC ESM runner: `node --import @swc-node/register/esm-register ./script.mts`. **The script MUST live inside `apps/backend/`** and use relative `./src/...js` + bare `shared/...` imports — a scratchpad-located script can't resolve the `shared` workspace export map (ERR "Cannot find module 'shared/schemas/...'"). Clean up the temp script + its `out/` after.

**Screenshot:** `playwright` isn't require-able by bare name (pnpm), but resolves via the explicit store path `node_modules/.pnpm/playwright@<ver>/node_modules/playwright`; full chromium (not just headless_shell) is installed. Load `file://.../page.html` (`waitUntil:'load'`; the `/_kb/*.js` scripts 404 harmlessly — CSS is inline so layout is complete). Pure-CSS toggles (mobile drawer/menu) open by setting the checkbox `checked` property via `page.$eval('#id', el=>{el.checked=true})` — `:checked` reflects it, so `:checked ~ sibling` fires.

**Run the render specs offline:** backend `vitest.config.ts` `globalSetup` connects to Postgres (`postgres.axis.orb.local`) and blocks pure-render specs. Make a temp `vitest.nodb.config.ts` identical but WITHOUT `globalSetup` (keep `setupFiles` — the query-counter needs no DB for a render), then `npx vitest run --config ./vitest.nodb.config.ts [-u] <spec>`. Golden snapshot lives at `__snapshots__/kb-reader.golden.spec.ts.snap`; the full inlined CSS repeats in every page snapshot, so a CSS edit is a big (expected) diff. See [[project_run_axis_ci_locally]], [[project_local_verify_login]].
