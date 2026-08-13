---
name: project_run_axis_ci_locally
description: How to replicate the GitHub PR checks (.github/workflows/ci.yml + react-doctor.yml) locally
metadata: 
  node_type: memory
  type: project
  originSessionId: e1935be3-e62b-4abf-92ba-42c11139e7fc
  modified: 2026-07-27T14:38:53.863Z
---

Axis PR CI = `.github/workflows/ci.yml` (11 jobs) + `react-doctor.yml`. To replicate locally:

**No infra needed:**
- lint → `pnpm check` (Biome; also runs react-doctor advisory repo-wide)
- react-doctor gate → `npx -y react-doctor@latest . --project web --scope changed --base origin/master --offline --blocking error` (see [[project_react_doctor_version]])
- build-backend → `pnpm --filter backend openapi:generate` (needs `NODE_OPTIONS=--max-old-space-size=4096`), `db:entities:check`, `typecheck`, `build`
- build-web → `pnpm --filter web typecheck` + `NODE_OPTIONS=--max-old-space-size=4096 VITE_CLERK_PUBLISHABLE_KEY=pk_test_ci VITE_SENTRY_DSN="" pnpm --filter web build`
- web-test → `pnpm --filter web test` (vitest run)
- architecture → `bash scripts/check-file-size.sh` + the inline-route-component grep in ci.yml
- knip → `pnpm exec knip`

**Needs Postgres (OrbStack dev infra `axis-postgres`/`axis-redis` on 5432/6379 works):**
- test-unit → `DB_HOST=localhost DB_PORT=5432 DB_USER=username DB_PASSWORD=password DB_NAME=axis_test pnpm --filter backend test`
- test-e2e → same but `DB_NAME=axis_ci` + `REDIS_HOST=localhost REDIS_PORT=6379 CLERK_PUBLISHABLE_KEY=pk_test_ci CLERK_SECRET_KEY=sk_test_ci SESSION_SECRET=ci-session-secret pnpm --filter backend test:e2e`

**A CONFLICTING PR runs NO checks at all.** GitHub can't build a merge ref for a PR with conflicts, so every `pull_request`-triggered workflow (Pipeline, React Doctor, Railway Preview) simply never fires — `gh run list --branch <b>` is empty and only third-party app checks (CodeRabbit) appear. So a PR showing "1 check, passing" may be a *conflicted* PR, not a green one. Verified 2026-07-27 on PR #913. Always check `gh pr view <n> --json mergeable,mergeStateStatus` before trusting `gh pr checks`; rebase, then re-check. Corollary for monitors: an "all checks non-pending" settle condition is a trap — it fires on the first app check before CI registers. Gate on the *workflow runs* (`gh run list --branch`) reaching a completed count instead.

**`scripts/check-file-size.sh` is also a lefthook pre-commit hook**, and its component limit is **300 lines** (not the 1k rule) — it blocks the commit, so a large new component must be decomposed before it can land. Run it (and `pnpm exec knip`) BEFORE committing, not after.

**Local `axis_ci` starts schemaless**, so `test:e2e` fails on the first table the app touches at boot (`relation "kb_custom_domains" does not exist` via `KbCustomHostRegistry.onModuleInit`) — nothing to do with the branch. Bootstrap it once, in this order: `db-objects --type extensions` → `migration:up` → `db-objects --type tables --type functions --type triggers --type grants`, all with `DB_NAME=axis_ci` and plain `DB_*` env.

Key facts: the test ORM (`src/test-utils/setup-db.ts`) defaults to db `axis_test` on `postgres.axis.orb.local` as `username`/`password`; **vitest does NOT load `.env`**, so unit tests never touch the dev `axis` db. Because the ORM config has those `?? 'username'/'password'` fallbacks, ~all specs pass even with NO `DB_*` env exported — EXCEPT `src/outbox/outbox-listener.service.spec.ts` (4 tests), which builds a raw `pg.Client` from `process.env.DB_HOST/DB_PORT/DB_USER/DB_PASSWORD/DB_NAME` with **no fallbacks** → fails with `SASL: client password must be a string`. So `pnpm --filter backend test` with a bare env shows exactly those 4 failing; they're env-only, not regressions. Export the full `DB_*` set (values above) to get a fully-green run. `refreshTestSchema` refreshes the *schema* but does NOT create the database — create missing ones with `docker exec axis-postgres psql -U username -d postgres -c "CREATE DATABASE axis_test"` (and `axis_ci`). Do NOT run unit + e2e concurrently against the same Redis — BullMQ cross-talk causes flaky failures. `migration-drift` needs host `psql` (not installed on this mac; `brew install libpq`) — but it's a no-op when the diff touches no `migrations/` or `.snapshot` files. `browser-e2e` needs `bin/sandbox` (the [[project_local_verify_login]] flow).
