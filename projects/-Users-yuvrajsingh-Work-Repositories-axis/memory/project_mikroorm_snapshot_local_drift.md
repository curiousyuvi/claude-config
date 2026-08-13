---
name: project_mikroorm_snapshot_local_drift
description: .snapshot-axis.json regen produces large machine-specific diffs (accepted); how to get a clean migration; pre-commit typecheck gotcha
metadata: 
  node_type: memory
  type: project
  originSessionId: f2e3d168-0e1b-46de-a06c-2fe127abbf39
  modified: 2026-07-27T14:39:26.042Z
---

Any entity schema change requires `pnpm --filter backend migration:create`, which regenerates `apps/backend/src/database/migrations/.snapshot-axis.json` — and that produces a **large, machine-specific diff** (format differences + `skipTables`-excluded tables like `ably_realtime_*` that older committed snapshots still carry). This is a **known, accepted ongoing problem** in the project ("our local machines produce different kinds of snapshot"): commit the large snapshot diff anyway.

Why it's safe: the CI `migration-drift` gate (`scripts/check-migration-drift.sh`) builds a fresh per-run DB and checks entity↔live-DB via `bin/check-schema-drift.ts` (`getUpdateSchemaSQL`, which ignores `skipTables`/routines/triggers and does NOT introspect standalone sequences); its `migration:check` step runs under a throwaway `DB_NAME` so the committed `.snapshot-axis.json` isn't the source of truth there.

To get a CLEAN generated **migration** (no spurious `drop table ably_*`): run `migration:create` against a *faithful replica* — a fresh scratch DB with extensions + all committed migrations + ALL db:objects applied — NOT the polluted local dev `axis` DB (which has extra sandbox state and yields ably drops). MikroORM names the snapshot `.snapshot-<DB_NAME>.json`, so generating under `DB_NAME=axis_snap` writes `.snapshot-axis_snap.json`; `cp` it over `.snapshot-axis.json` if you need the committed file updated.

Those stray per-DB snapshots are easy to commit by accident with `git add -A` (happened on PR #913 with `.snapshot-axis_ci.json` from bootstrapping the e2e DB). As of that PR `.gitignore` covers the whole class — `apps/backend/src/database/migrations/.snapshot-*.json` with a `!…/.snapshot-axis.json` negation — so only the dev snapshot is committable. Still check `git diff --cached --name-only | grep snapshot` before committing on older branches.

Another way to get a clean, entity-derived snapshot: run `migration:create` (which writes it from entity metadata), then do NOT run `migration:up` afterwards — `migration:up` re-introspects and rewrites the snapshot with non-entity tables (a ~2300-line junk diff). If you must apply the migration locally, back the snapshot up first and restore it after.

Pre-commit hook (lefthook) runs **whole-repo `typecheck`**, so unrelated uncommitted WIP elsewhere in the tree blocks your commit even when your staged files are clean — `git commit --no-verify` is justified in that case (the WIP isn't in your commit and won't reach CI). See [[project_run_axis_ci_locally]].
