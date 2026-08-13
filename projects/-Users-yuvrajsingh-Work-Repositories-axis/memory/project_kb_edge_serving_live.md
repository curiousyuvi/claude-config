---
name: project-kb-edge-serving-live
description: "Published KBs now serve from Cloudflare + R2; freshness depends on purgeTags, with s-maxage=86400 only as a backstop"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7cc61853-fad8-4679-9603-21f16494f649
  modified: 2026-08-09T10:04:44.366Z
---

As of 2026-08-09 the published-KB reader serves from the edge, not Railway. `x-kb-edge: artifact` and `cf-cache-status: HIT` on `docs.curiousyuvi.com`.

**What lives where.** Redis keeps only host→KB resolution (`kbpub:v:host:v2:*`, tagged `kb-{id}`) and the two rate limiters; every other reader cache was deleted (PR #1089). Page bytes come from R2 via the Worker.

**Freshness is purge-driven.** Public KBs bake `public, max-age=0, s-maxage=86400, must-revalidate` (`EDGE_SHARED_CACHE`). The 24h is a *backstop*, not the mechanism — every bake calls `purgeTags(['kb-{id}'])`. Gated KBs (password / members / IP) stay `private, max-age=0, must-revalidate` and are never shared-cached.

**The risk this creates:** `KbEdgePurgeClient.purgeKb` returns `true` when unconfigured, so a broken purge reports success and content goes stale for a day instead of never. The rollback lever is dropping `s-maxage` from `EDGE_SHARED_CACHE` in `reader-http.util.ts` then re-baking — no Worker change needed.

**Deploy order that works:** Worker (`cd apps/kb-edge && pnpm run deploy`) → merge backend → `APP_ENV=production pnpm --filter backend kb:artifact-bake --all` → `--all --check` must exit 0. The settings artifact carries the Cache-Control, so a backend deploy alone changes nothing until a re-bake.

The bake CLI is a fresh process, so it reads the DB cleanly even when a long-lived worker's identity map is stale — useful for repairing artifacts.

Related: [[project_kb_gated_edge_and_redis_removal]], [[project_kb_artifact_bake_pipeline]], [[project_pnpm_run_deploy_shadowed]]
