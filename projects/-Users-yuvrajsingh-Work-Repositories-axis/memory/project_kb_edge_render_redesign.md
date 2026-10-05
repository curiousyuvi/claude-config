---
name: project_kb_edge_render_redesign
description: "ACTIVE (2026-10-06) — move KB page rendering into the kb-edge Worker (bake data, not HTML); spike PASSED; NEXT = strict plan review, then ONE PR on ys/fix/kb-template-rebake-on-deploy"
metadata:
  node_type: memory
  type: project
  originSessionId: efaafd2b-a848-443c-b46f-2adad8af023c
  modified: 2026-10-05T20:06:29.223Z
---

Full handoff for the published-KB render redesign. Read this first when resuming. Related: [[kb-edge-current-state]], [[project_kb_reader_template_parts_split]], [[project_kb_bake_never_deletes_orphans]].

## Where things stand (2026-10-06)
- Branch `ys/fix/kb-template-rebake-on-deploy`, cut from master `a60d311cf`. Nothing committed. Only untracked change: throwaway spike dir `apps/backend/.spike-edge/` (worker.ts, build.mjs, node-bench.mjs, workerd-bench.mjs, wrangler.jsonc, dist/). DELETE IT before the real PR.
- Background (done, merged, deployed): PR #1609 collapsed `slug`/`slug_norm` into one normalized `slug` and fixed the content-only republish bake (route now from `SitemapData.routeByNodeId`; failed edge purge now fails the KB_BAKE job). PR #1610 capped `tsgo --checkers 2` in CI (Backend Build was OOM-killing runners). Production repair done: `kb:artifact-bake --all --repair` rebaked 11 KBs, then manual purge per KB via `KB_EDGE_PURGE_URL`. User confirmed a real-world body-only republish now shows up.

## Update 2026-10-06 (after compaction)
- Rebased branch onto master `b24d7b4c8` (#1611 touches no reader/edge code). Byte parity PASSED: workerd HTML identical to Node for 4 cases.
- Full plan written to untracked repo-root `KB-EDGE-RENDER-PLAN.md` (site/page data artifacts, `packages/kb-reader` built package, shared `composeView` for edge + origin, drop template/parts split, worker build id in cache key, MD5/ETag diff-written bakes, `--repair` purges, kb-edge CI deploy). Next: thermo-nuclear review of it, fix findings, then user sign-off before code.

## The problem being solved
- Every artifact embeds presentation. `template/{locale}.html` inlines ALL of `kb-reader.css` + prose CSS (`READER_BASE_CSS`, `apps/backend/src/modules/kb-public/application/kb-reader-styles.ts`) plus header/footer chrome, so ANY reader CSS/markup deploy makes every KB stale. #1597 (2026-10-02, kb-reader.css) caused the 10-KB template drift found 2026-10-05.
- Every page carries its own nav/breadcrumbs/prev-next/child lists (see class comment on `KbArtifactBaker`, `kb-artifact-baker.service.ts`), so a title change/move/new article rebakes the whole KB (`kbArtifactDirty` → `wholeKb`).
- A bake renders page by page via `KbReaderService.resolveView` (~6-8 sequential DB queries: KB shell, article, visibility, content, locales, tree, connected cards) + 2 React renders (page + embed). From a laptop that is ~1 s/page; the 286-page KB takes minutes. User: "with real customers that rebake would run for days."
- `kb:artifact-bake --repair` writes R2 but does NOT purge the edge (needed a manual curl loop). Fix this in the PR too.

## Rejected (and why)
- Sweep templates after each deploy (render home per locale, compare, rebake on diff): user said still too costly.
- Rebake everything per deploy: far too expensive. Manual "renderer version" constant: someone forgets to bump it. Fixture fingerprint of the renderer: ships test fixtures, misses combos.

## Approved direction: bake DATA, render at the edge
User approved after a plain-language explanation ("the worker builds the page when a visitor asks; Cloudflare caches it").
- Per KB artifacts: `site/{locale}.json` (parsed settings, chrome data, tree: titles/slugs/ids/icons — anonymous-visible nodes only) + `pages/{path}.json` (published body HTML already stored at publish, title, description, SEO, FAQs, locales). Host + settings artifacts stay.
- Worker on cache miss: read the 2 objects, derive active nav/breadcrumbs/prev-next/children/same-KB connected cards from the tree, render with the shared reader code. Embed = same data + flag (drop `embed/` + `embed-template/` copies).
- Cache key includes worker version → deploy needs zero rebake.
- Bake becomes bulk queries + small writes per event: body edit → 1 page file; title/move/new → site file (+1 page); settings → site files. Bake command should run as an in-cluster job, not a laptop loop.

## User constraints
- ONE PR for everything, and include any other published-KB efficiency wins.
- Run `/thermo-nuclear-code-quality-review` on the WHOLE plan before writing any implementation code.
- Usual rules: no commit/push/merge without asking; `op` commands go to the user; no AI attribution; humanizer on PR prose; minimal comments.

## Spike results (2026-10-06) — FEASIBLE
- Real `renderPageParts` (`kb-reader-jsx.tsx`) + `stitchKbPage` bundled with esbuild (`node_modules/.pnpm/esbuild@0.28.1`, platform neutral, conditions workerd/worker/browser, NODE_ENV=production) ran inside local workerd via `apps/kb-edge/node_modules/.bin/wrangler dev --local` (nodejs_compat, no_bundle).
- Bundle 689 KB raw / 171 KB gzip (Workers limit 3 MB free, 10 MB paid). zod/v4 = 327 KB of it (only for `parseKbSettings`) → bake already-parsed settings so the edge drops zod. react-dom/server 197 KB, CSS 69 KB, reader code 47 KB.
- Coupling to fix when extracting: `kb-reader-styles.ts` uses `node:fs` readFileSync (switch to a text/raw import); renderer imports `kb-host.util.ts`, which pulls `node:crypto` via `common/timing-safe-compare.ts` (split the secret check out). `KbPageRenderer` is a Nest service (ConfigService + API_ORIGIN) — keep that wrapper backend-side; the pure core is `renderPageParts(view, ctx)`.
- ms per render, workerd ≈ Node: 30 articles 0.4 | 300 classic 0.5 | 300 embed 0.4 | 300 documentation 1.65 | 3000 classic 1.5 | 3000 documentation 14 | 10000 classic 4.4 | 10000 documentation 53. Measured with a 15 KB body and synthetic tree (25 articles/collection).
- Finding: classic doc page stays ~84 KB regardless of KB size; the documentation layout puts the WHOLE nav in every page (1.8 MB HTML at 3000 articles). Existing inefficiency, a candidate "other optimization" for the PR (e.g. render nav once as a cacheable fragment).
- NOT yet done: byte-parity check (workerd HTML vs Node HTML for the same input) — was running when we paused for compaction. Also not measured: Worker cold start with the bigger bundle, and R2 read latency for the 2 objects.

## Known hard parts for the plan
- Renderer must move into a built package (e.g. `packages/kb-reader`): the backend loads `packages/shared` as raw TS via strip-types (no JSX, no `.js`→`.ts` rewrite, no parameter properties). Golden specs (`kb-reader.golden.spec.ts`, 12 snapshots) are the parity proof.
- kb-edge deploys manually today; needs CI auto-deploy when kb-edge or the renderer changes, or a stale Worker replaces stale templates.
- Gated/member pages still render at origin (backend keeps using the same package). Restricted articles must stay out of site data.
- Artifact version bump (`KB_ARTIFACT_VERSION` in `packages/shared/src/kb-artifacts.ts`) with fallback; keep `slugNorm` wire name or rename in the same bump.
- Connected cards and interlinks: cross-KB cards need other KBs' data; decide edge vs bake-time.
