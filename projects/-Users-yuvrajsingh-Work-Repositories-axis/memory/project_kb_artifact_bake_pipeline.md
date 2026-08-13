---
name: kb-artifact-bake-pipeline
description: Slice 2 of KB caching — bake published KBs into R2 artifacts; one streaming builder shared by bake and reconcile; key derivation is an auth boundary
metadata: 
  node_type: memory
  type: project
  originSessionId: ea441c8c-9d1f-4fc1-9ef3-73ac33678184
  modified: 2026-08-08T09:20:46.947Z
---

Slice 2 of [[kb-published-r2-worker-caching]] landed 2026-08-08 (uncommitted, `KB_ARTIFACT_BAKE_ENABLED` off by default, nothing reads artifacts yet). Builds on [[kb-reader-template-parts-split]].

**Verified end-to-end on the dev DB: 664 pages across 3 KBs / 5 locales, reconciler clean (0 diverged/missing/orphaned).** The C1 template-invariance assertion held over 512 real convious pages in 4 locales — much stronger evidence than fixtures. Dev DB KBs: convious (512 pages, 4 locales), instantdocs (152 pages, 5 locales), plus a small one.

**Core design:** `KbArtifactBaker.buildArtifacts(kbId, sink)` streams every object to a callback. `bakeKb` writes, `KbArtifactReconciler` compares. One builder / two consumers ⇒ a comparison can never be made against a differently-built page, and no KB is held in memory (a big KB would be 100s of MB).

**Deliberate simplifications (cost recorded):** pages are written WHOLE — nav rides in `pages/{locale}/{route}.json`, there are no `nav/` or `nodemeta/` objects. Splitting nav needs the sidebar active state moved client-side (a real no-JS regression) and structural changes already rebake the KB anyway. Cost carried to slice 3/4: a connected card refreshes with its HOST page, not when its target publishes — opposite of the live reader's read-time rewrite.

**BUCKET: artifacts must NOT go in `helply-production`** (proposed 2026-08-08, rejected same day). `helply-production` is bound to R2 custom domain **`cdn.helply.com`** = the KB asset CDN, and an R2 custom domain exposes the WHOLE bucket publicly (no per-prefix privacy; access control = Cloudflare Access/WAF over the entire domain, which would break asset delivery). Artifacts contain full page HTML **including gated KBs**, so that would be an authz bypass, permanent and unpurgeable. `kb-artifacts/host/{hostname}.json` is trivially guessable and leaks the kbId. ⇒ **dedicated PRIVATE bucket, no custom domain, r2.dev disabled.** Also fixes slice 3's "R2 Worker binding can't be prefix-scoped". `KB_ARTIFACT_ROOT='kb-artifacts/'` kept anyway (tidy + keeps `deletePrefix` guard real). Existing `KB_ASSET_BUCKET_*` creds are for helply-production ⇒ NOT reusable; new bucket needs its own bucket-scoped token.

**Guard added**: `KbArtifactStorage` THROWS at boot if `KB_ARTIFACT_BUCKET_NAME` equals `KB_ASSET_BUCKET_NAME` or `BUCKET_NAME` — fail-closed, because that misconfiguration publishes gated KBs' HTML. Needed because `op run` masks the bucket name in `kb:artifact-probe` output (substring masking, see [[op-run-masks-prose-in-bin-output]]), so you cannot tell from the probe WHICH bucket it hit.

**PROD BACKFILL + SOAK PASSED 2026-08-08**: 396 pages / 10 production KBs, reconciler 0 of 10 drifted (427 objects = 396 pages + 11 templates + 10 settings + 10 host). Slice 2 acceptance met.

**Reconciler blind spot found + fixed**: `reconcileKb` lists only the prefix of a KB it already knows, so artifacts for a KB *absent from the DB* (deleted, or baked from another env) are invisible and still report `orphaned=0`. Proven by dev content sitting in the prod bucket after a misconfigured run. `--all --check` now also sweeps `kb-artifacts/kb/` child prefixes with no matching KB (`listChildPrefixes` uses an S3 `Delimiter` so it doesn't enumerate objects); `--repair` deletes them.

**Backfill is latency-bound from a laptop** (Postgres round trip to us-east-1 + bucket PUT per page). Writes batch 12 at a time; **rendering stays SEQUENTIAL on purpose** — it shares one `EntityManager` and MikroORM doesn't promise concurrent safety; a subtly wrong baked page beats a slow bake.

**Queue workers are APP_ROLE-gated** (`BaseWorkerService.onModuleInit` → `shouldRunWorkers()`, true only for `unified`/`worker`). So `KB_ARTIFACT_BAKE_ENABLED` / `KB_EDGE_PURGE_URL` / `KB_ARTIFACT_BUCKET_*` must be set on **whichever Railway service runs workers**, not just `api` — if `api` is `APP_ROLE=server` it never drains the KB queue and nothing bakes on publish. Symptom 2026-08-08: layout change saved, Redis busted, browser unchanged; manual `kb:artifact-bake <kbId>` fixed it instantly, proving bake→R2→Worker→browser works and only the event trigger was missing.

**`--check` needs a real bucket.** With none configured the store is per-process memory, so a bake in one CLI invocation is gone by the next and everything reads back "missing". Only a plain bake is meaningful locally.

**Unexplained, watch during the soak**: a dev-DB bake of convious reported `pages=512 skipped=120` on one run and `pages=632 skipped=0` ~1.5h later (same total 632 route×locale combos). Two consecutive runs are now byte-stable. Most likely Redis reader-cache state (`articleLocales` decides the redirect-vs-page outcome per locale). The event path is ordered correctly — `KbEventsWorkerService` busts tags BEFORE `rebakeArtifacts` — but a CLI backfill can run against a warm cache. If the production soak shows flapping page counts, this is the thread to pull.

**Check a bucket's exposure before putting anything in it**: `GET /accounts/{id}/r2/buckets/{name}/domains/custom` (+ `/domains/managed` for the r2.dev URL).

**Pages keyed by the reader URL PATH**, not locale+route: `kbPageKey(kbId, path)` → `/fr/doc/x` = `pages/fr/doc/x.json`, `/` = `pages/index.json`. Changed 2026-08-08 while writing the Worker (before any prod bake): the locale+route shape forced the Worker to re-implement the backend's locale-prefix parsing = exactly the drift the architecture exists to prevent. Backend already knows the path when it resolves the page ⇒ edge does a lookup that interprets nothing.

**Key derivation is an auth boundary** (`packages/shared/src/kb-artifacts.ts`, shared with the future worker): only `[a-zA-Z0-9._-]`, percent signs REFUSED not decoded (`..%2f`), and exactly ONE leading/trailing slash shed — collapsing a `//` run aliased a protocol-relative path onto a real route's artifact (caught by a test).

Other: only the canonical host is baked (origin+robots are in the bytes) via `KbPublicUrlService`; redirects/misses stay on origin; settings artifact carries the FULL header set not just CSP; `kbArtifactDirty` (next to `invalidationTags`) is coarse on purpose — only `KB_ARTICLE_UPDATED` narrows to one article since bodies embed prev/next+breadcrumbs+child lists. Bake failure is caught+logged, never rethrown (must not lose the cache bust/reindex that already succeeded). No bucket configured ⇒ in-memory store, so `pnpm --filter backend kb:artifact-bake <kbId> [--check|--repair]` is a render smoke test anywhere. Module placement forced by DI direction: knowledge-base imports kb-public, so the baker lives in knowledge-base and the store in the global StorageModule.
